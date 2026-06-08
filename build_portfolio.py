#!/usr/bin/env python3
"""
Scan the portfolio/ folder, generate lightweight thumbnails, and (re)generate
portfolio/manifest.json.

Why thumbnails?
    The originals are full-resolution (some 15+ MB). Loading 90+ of those into
    a grid is painfully slow on mobile. Instead the grid loads small thumbnails
    from portfolio/thumbs/, and the full-resolution original is only fetched
    when someone opens the lightbox or downloads the photo.

The portfolio page (portfolio.html) reads manifest.json to know which images
to display, because a static site can't list a folder's contents at runtime.

Usage:
    python build_portfolio.py

Normally you never run this by hand — the GitHub Action
(.github/workflows/build-portfolio.yml) runs it automatically on every push.
Running it locally before a push works too.

Requires Pillow:  pip install Pillow
"""

import datetime
import json
import pathlib

from PIL import Image, ImageOps

# EXIF tag IDs we care about for ordering
EXIF_DATETIME_ORIGINAL = 36867   # when the photo was actually taken
EXIF_DATETIME = 306              # generic "date/time" fallback
EXIF_SUBIFD = 0x8769             # pointer to the Exif sub-IFD holding 36867

# Folders / files, relative to this script's location
ROOT = pathlib.Path(__file__).resolve().parent
PORTFOLIO_DIR = ROOT / "portfolio"
THUMBS_DIR = PORTFOLIO_DIR / "thumbs"
MANIFEST = PORTFOLIO_DIR / "manifest.json"

# Image types we publish
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}

# Longest edge of a generated thumbnail, in pixels. The grid columns are ~320px
# wide, so ~720px stays crisp on retina screens while keeping the grid fast.
# (The full-resolution original is always used for the lightbox and downloads.)
THUMB_MAX_EDGE = 720
THUMB_QUALITY = 72


def caption_from_file(stem: str) -> str:
    """Turn 'swiss_vict' into 'Swiss Vict' for the alt text."""
    return " ".join(part.capitalize() for part in stem.replace("-", " ").replace("_", " ").split())


def capture_key(path: pathlib.Path) -> str:
    """
    Return a sortable 'YYYY:MM:DD HH:MM:SS' string for when the photo was taken.

    Prefers the EXIF capture date; falls back to the generic EXIF date, then to
    the file's modification time. Because the format is fixed-width, plain string
    comparison sorts chronologically.
    """
    try:
        with Image.open(path) as im:
            exif = im.getexif()
            if exif:
                # DateTimeOriginal lives in the Exif sub-IFD
                try:
                    sub = exif.get_ifd(EXIF_SUBIFD)
                    dt = sub.get(EXIF_DATETIME_ORIGINAL)
                except Exception:
                    dt = None
                if not dt:
                    dt = exif.get(EXIF_DATETIME)
                if isinstance(dt, str) and dt.strip():
                    return dt.strip()
    except Exception:
        pass

    # No usable EXIF — fall back to the file's modification time.
    mtime = datetime.datetime.fromtimestamp(path.stat().st_mtime)
    return mtime.strftime("%Y:%m:%d %H:%M:%S")


def make_thumb(src: pathlib.Path, dest: pathlib.Path) -> None:
    """Write a downscaled JPEG thumbnail of `src` to `dest` (skips if up to date)."""
    if dest.exists() and dest.stat().st_mtime >= src.stat().st_mtime:
        return  # thumbnail already current

    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)          # respect camera rotation
        im.thumbnail((THUMB_MAX_EDGE, THUMB_MAX_EDGE))
        if im.mode not in ("RGB", "L"):
            im = im.convert("RGB")                # drop alpha / palette for JPEG
        im.save(dest, "JPEG", quality=THUMB_QUALITY, optimize=True, progressive=True)
    print(f"  thumb: {dest.name}")


def main() -> None:
    PORTFOLIO_DIR.mkdir(exist_ok=True)
    THUMBS_DIR.mkdir(exist_ok=True)

    images = [
        p for p in PORTFOLIO_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS
    ]
    # Newest first by capture date; filename breaks ties for a stable order.
    images.sort(key=lambda p: (capture_key(p), p.name), reverse=True)

    # Remove orphaned thumbnails whose source image is gone.
    valid_thumb_names = {p.stem + ".jpg" for p in images}
    for t in THUMBS_DIR.glob("*.jpg"):
        if t.name not in valid_thumb_names:
            t.unlink()
            print(f"  removed orphan thumb: {t.name}")

    manifest = []
    for p in images:
        thumb_name = p.stem + ".jpg"
        make_thumb(p, THUMBS_DIR / thumb_name)
        manifest.append({
            "file": p.name,                       # full-res original (lightbox + download)
            "thumb": "thumbs/" + thumb_name,       # small image for the grid
            "alt": caption_from_file(p.stem),
        })

    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {MANIFEST.relative_to(ROOT)} with {len(manifest)} image(s).")


if __name__ == "__main__":
    main()
