---
name: stitch-images
description: Use when handing the user a group of images that belong together so they get a single image.
---

# stitch-images: many images, one sheet

Images that are read together belong on one sheet. Build it with `montage`.
`-tile 2x` sets two columns, `-tile 1x` stacks, `-tile x1` makes a single row.

```sh
magick montage -font /System/Library/Fonts/Helvetica.ttc \
  -background '#1a1a1a' -fill white -pointsize 26 \
  -gravity north -tile 2x -geometry +14+14 \
  -label 'Before: sidebar collapsed' before.png \
  -label 'After: sidebar pinned'     after.png \
  out.png
```

Look at the finished sheet before sending it. Layout mistakes are obvious on
sight and invisible in the command.

## Notes

- `-font` is required on every call, even one drawing no visible text, or the default filename labels fail with ``unable to read font `' ``.
- `-geometry +14+14` sets tile padding and keeps images at full size. Without it you get 120x120 thumbnails.
- Each `-label` captions the file after it. `-title` adds a heading over the sheet.
- `-gravity north` aligns tiles at the top. Without it each one centers in a cell sized to the largest, so captures of differing height drift out of line.
- Keep tiles at native size. The user can zoom, so downscaling only throws detail away. If a set genuinely needs shrinking, fit on width alone, as in `-geometry 620x+14+14`. A `620x620` fit builds a square cell and strands the caption far below its image.
