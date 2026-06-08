# Portfolio images

Drop your best photos straight into this folder (`.jpg`, `.jpeg`, `.png`,
`.webp`, `.gif`, `.avif`). Both portrait and landscape shots work — the page
keeps each image's natural shape and packs them together automatically.

## To publish new photos

1. Copy the image files into this `portfolio/` folder.
2. Commit and push:
   ```
   git add portfolio/
   git commit -m "Add new photos"
   git push
   ```

That's it. On push, a GitHub Action regenerates `manifest.json` (the list the
website reads) and GitHub Pages serves the updated gallery within a minute or
two. You never edit `manifest.json` by hand.

If you ever want to preview locally before pushing, run:
```
python build_portfolio.py
```
