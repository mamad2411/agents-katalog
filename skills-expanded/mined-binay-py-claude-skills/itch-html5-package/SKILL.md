---
name: itch-html5-package
description: Check an HTML5/web game build against itch.io's rules and package it as a correct upload zip. Catches file-name case mismatches that work on Windows/macOS but 403 on itch, absolute "/" paths, http:// requests, index.html in the wrong folder, the 1,000-file / 500 MB / 200 MB / 240-char limits, shipped source files and a missing viewport tag. Use when publishing or updating a web game (three.js, Phaser, PixiJS, Godot/Unity/GameMaker web exports, plain canvas) on itch.io, or when an itch HTML5 game shows a black screen or 403 errors.
---

# itch-html5-package

`scripts/itch-package.mjs` is zero-dependency Node 22+.

```
node itch-package.mjs ./build                 # check, then write ./build-itch.zip
node itch-package.mjs ./build --out game.zip
node itch-package.mjs ./build --check          # report only
```

It exits 1 and writes no zip if anything would break on itch. Fix the ✘ items and run again. Warnings (!) are worth reading but don't block.

## What it checks (itch.io's documented rules)
- `index.html` exists, named exactly that. If it's one folder down (you zipped the parent folder), that folder becomes the root.
- ≤ 1,000 files, ≤ 500 MB extracted, ≤ 200 MB per file, paths ≤ 240 characters.
- **Case-sensitive names.** Every path referenced in HTML, CSS, JS and JSON is resolved, and a reference that only matches with different capitalization is an error. Windows and macOS hide this; itch's servers return 403.
- **Relative paths only.** `/assets/x.png` fails because itch serves the game from a subfolder.
- **External requests must be https.**
- Shipped source files (.psd, .blend, .aseprite …), no viewport meta, and the YouTube Playables SDK, which hangs inside itch's iframe.

It can't see paths built at runtime (`'level' + n + '.json'`). Spot-check those by hand after upload.

## Uploading
On the itch.io project page: **Kind of project → HTML**, upload the zip, tick **"This file will be played in the browser"**, and set the viewport size (or enable "Mobile friendly" and fullscreen for phone games). HTML5 games only take payments as donations; selling needs a downloadable build.

## Engine notes
- **Godot 4 web exports** need SharedArrayBuffer unless exported with thread support off. On itch, enable "SharedArrayBuffer support" in the embed options, or export single-threaded.
- **Unity** builds with Brotli (`.br`) are served correctly by itch. Gzip works too.
- A single self-contained `.html` file can be uploaded directly, with no zip.
