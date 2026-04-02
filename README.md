# Oakley Gompels — Personal Website

Live at **[oakleyg.github.io](https://oakleyg.github.io)**

---

## Project Structure

```
Website/
├── index.html          # Main portfolio page
├── style.css           # All shared styles (CSS variables, layout, components)
├── evolution.html      # Standalone site evolution / version history page
├── versions.json       # Version history data — update this with every new version
├── Oakley Gompels CV.pdf
├── Pictures/           # Photography images
├── Projects/           # Lab report PDFs
└── .vscode/
```

---

## Git Workflow

Every design iteration lives on its own named branch. The full history is preserved — you can jump back to any version at any time.

### Starting a new version

```bash
git checkout main
git checkout -b v4-whatever-youre-changing
```

Make your changes, then:

```bash
git add index.html style.css   # (or whichever files changed)
git commit -m "v4: describe what changed"
```

### Merging into main and going live

```bash
git checkout main
git merge v4-whatever-youre-changing
git push origin main
git push origin v4-whatever-youre-changing   # preserves branch history on GitHub
```

GitHub Pages deploys automatically on every push to `main`. The live site updates within ~60 seconds.

---

## versions.json — IMPORTANT

**This file must be updated with every new version before merging.**

It powers the interactive branch graph on `evolution.html`. Each entry looks like this:

```json
{
  "version": "v4",
  "branch": "v4-whatever-youre-changing",
  "date": "YYYY-MM-DD",
  "message": "Short title — longer description of what changed",
  "merged": true,
  "commitHash": "full-commit-hash-here",
  "compareUrl": "https://github.com/OakleyG/OakleyG.github.io/compare/prevHash...newHash"
}
```

- `merged` should be `false` while the branch is open, `true` once merged into main
- `compareUrl` for the first commit of a branch: use the GitHub compare URL between the previous version's hash and the new one
- The `versions.json` update should always be the **last commit** in a set of changes

---

## Version History

| Version | Branch | Description |
|---------|--------|-------------|
| v1 | `main` | Initial HTML & CSS portfolio — hero, about, projects, photography, CV, contact |
| v2 | `v2-redesign` | n8n-inspired dark redesign — navy theme, orange accents, Inter font, dark cards |
| v3 | `feature/git-history-visual` | Site Evolution page — Gitgraph.js visualisation, evolution.html, version cards |

---

## Known Git Quirks

The local `.git` directory is on a FUSE-mounted filesystem that **blocks file deletion**. This means stale lock files (`.git/index.lock`, `.git/HEAD.lock`) can get stuck after a crashed git process.

**Fix:** delete them manually from your Mac terminal:

```bash
rm .git/index.lock
rm .git/HEAD.lock
rm .git/refs/heads/<branch-name>.lock   # if a specific branch lock is stuck
```

These are empty marker files — safe to delete as long as no git process is actually running.

---

## Stale Lock Checklist (if git refuses to run)

```bash
# See what locks exist
find .git -name "*.lock"

# Remove them all at once
find .git -name "*.lock" -delete
```

---

## Editing the Site

The site uses plain HTML and CSS — no build tools, no npm.

- **CSS variables** are all defined at the top of `style.css` under `:root` — change colours, fonts, and spacing there
- **New sections** follow the pattern: `<section id="x" class="section">` with a `.section-label`, `h2`, and `.container`
- **`section-alt`** class gives a section the slightly lighter `#111128` background, alternating the visual rhythm

---

*Built with HTML, CSS & Git · Hosted on GitHub Pages*
