#!/usr/bin/env python3
"""
Scan the portfolio/ folder and (re)generate portfolio/manifest.json.

The portfolio page (portfolio.html) reads this manifest to know which images
to display, because a static site can't list a folder's contents at runtime.

Usage:
    python build_portfolio.py

You normally never run this by hand — the GitHub Action
(.github/workflows/build-portfolio.yml) runs it automatically on every push.
But running it locally before a push works too.
"""

import json
import pathlib

# Folders / files, relative to this script's location
ROOT = pathlib.Path(__file__).resolve().parent
PORTFOLIO_DIR = ROOT / "portfolio"
MANIFEST = PORTFOLIO_DIR / "manifest.json"

# Image types we publish
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}


def caption_from_file(stem: str) -> str:
    """Turn 'swiss_vict' into 'Swiss Vict' for the alt text."""
    return " ".join(part.capitalize() for part in stem.replace("-", " ").replace("_", " ").split())


def main() -> None:
    PORTFOLIO_DIR.mkdir(exist_ok=True)

    images = sorted(
        p for p in PORTFOLIO_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS
    )

    manifest = [
        {"file": p.name, "alt": caption_from_file(p.stem)}
        for p in images
    ]

    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {MANIFEST.relative_to(ROOT)} with {len(manifest)} image(s).")


if __name__ == "__main__":
    main()
