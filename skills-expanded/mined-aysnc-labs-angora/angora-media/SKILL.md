---
name: angora-media
description: Process images from `inbox/` into the media system — read each image visually to generate alt text under 125 characters, extract dimensions, assign a nanoid filename, move the file to `public/media/`, and insert a row into the `media` table. Trigger whenever the user wants to process, pipeline, ingest, or register images from inbox (jpg, png, webp, avif, gif, svg). Phrases like 'process the photos in inbox', 'pipeline the hero images', 'generate alt text for the screenshots in inbox', 'get the product photos into the media table', 'handle the avatars in inbox' all trigger this. Do NOT use for importing CSV/JSON data (→ angora-import).
---

# Media

Process images from the `inbox/` directory into the media system.

## Before you start

1. **Check inbox contents** — list `inbox/` directory. If empty (only `.gitkeep`), report "Inbox is empty. Drop images into `inbox/` and run this again."
2. **Check current media table** — run:
```bash
node -e "
  import db from './src/data/db.ts';
  import { media } from './src/data/schema/tables/media.ts';
  const rows = db.select().from(media).all();
  console.table(rows);
"
```

## Pipeline (for each image)

### 1. Visual analysis

Read the image file with the Read tool (Claude vision). Write alt text:
- Describe what's in the image, under 125 characters
- Don't start with "Image of" or "Photo of"
- Use `alt=""` for purely decorative images (backgrounds, dividers)

### 2. Read dimensions

```bash
node -e "
  import { imageSize } from 'image-size';
  const result = imageSize('inbox/<filename>');
  console.log(JSON.stringify(result));
"
```

Skip for SVGs (scalable — dimensions not meaningful).

### 3. Generate unique filename

```bash
node -e "
  import { nanoid } from 'nanoid';
  console.log(nanoid(8));
"
```

Preserve the original extension. Result: `V1StGXR8.jpg`

### 4. Move file

```bash
mv inbox/<original> public/media/<nanoid>.<ext>
```

### 5. Insert into media table

```bash
node -e "
  import db from './src/data/db.ts';
  import { media } from './src/data/schema/tables/media.ts';
  db.insert(media).values({
    path: 'media/<nanoid>.<ext>',
    alt: '<alt text>',
    type: 'image',
    width: <width>,
    height: <height>,
    sourceName: '<original filename>',
  }).run();
  console.log('Inserted.');
"
```

### 6. Summary table

After processing all images, show a summary:

| Original | New path | Dimensions | Alt text |
|----------|----------|------------|----------|
| hero-bg.jpg | media/V1StGXR8.jpg | 1920x1080 | Dark gradient background with subtle grid pattern |

## Rules

- **Supported types:** jpg, jpeg, png, gif, webp, avif, svg
- **SVGs:** skip dimension reading (scalable), set type to `svg`
- **Never delete inbox files without explicit permission** — ask after processing
- **Skip non-image files** — report them: "Found non-image files: [list]. These can be processed with the import skill (`/angora-import`)."
- Process images one at a time to ensure accuracy of alt text