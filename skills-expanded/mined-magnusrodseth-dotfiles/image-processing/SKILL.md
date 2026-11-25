---
name: image-processing
description: "Process images in TS/JS with Bun's Bun.Image API: resize, crop, rotate, compress, convert (JPEG/PNG/WebP/HEIC/AVIF), thumbnails, LQIP/ThumbHash placeholders, EXIF. Replaces sharp on Bun."
---

# Image Processing with Bun.Image

`Bun.Image` is Bun's built-in image pipeline (Bun 1.3.14+). Zero npm deps, no native addon build step, runs off the JS thread, faster than `sharp` in most benchmarks. API shape mirrors `sharp`: construct → chain → pick output format → `await` a terminal.

## Preflight

- Confirm the project uses Bun (`bun --version` ≥ 1.3.14, or `package.json` `engines.bun` / a `bunfig.toml`). If on plain Node.js, recommend `sharp` instead — don't force a runtime switch just for images.
- No imports needed — `Bun.Image` is a runtime global.
- HEIC/AVIF: macOS/Windows only. Linux rejects with `ERR_IMAGE_FORMAT_UNSUPPORTED` — wrap with a WebP fallback (see REFERENCE.md).

## Quick start

```ts
// Resize, compress, and convert in one chain.
await Bun.file("photo.jpg")
  .image()
  .resize(800, 600, { fit: "inside" })
  .webp({ quality: 80 })
  .write("thumb.webp");
```

The pipeline is lazy — **nothing runs until a terminal is awaited** (`.write`, `.bytes`, `.buffer`, `.blob`, `.toBase64`, `.dataurl`).

## Common workflows

### Generate a thumbnail

```ts
await Bun.file("photo.jpg").image().resize(400, 400, { fit: "inside" }).webp({ quality: 80 }).write("thumb.webp");
```

`fit: "inside"` preserves aspect ratio; default `fit: "fill"` stretches.

### Compress without resizing

```ts
await Bun.file("hero.png").image().webp({ quality: 75 }).write("hero.webp");
```

For screenshots / UI assets, indexed PNG is usually 3-5× smaller than WebP:

```ts
await Bun.file("screenshot.png").image().png({ palette: true, colors: 64, dither: true }).write("screenshot.png");
```

### Read metadata without decoding pixels

```ts
const { width, height, format } = await new Bun.Image(input).metadata();
```

### Generate an LQIP (blurry placeholder)

```ts
const lqip = await Bun.file("hero.jpg").image().placeholder();
// data:image/png;base64,… — inline as <img src={lqip}> or CSS background.
```

400–700 bytes, ThumbHash-rendered, no client-side decoder needed. For batch usage (every image on a blog), see [REFERENCE.md](REFERENCE.md#lqip-batch-pattern).

### Bulk convert a directory

```ts
import { Glob } from "bun";
for await (const file of new Glob("**/*.{jpg,jpeg,png}").scan("./images")) {
  await Bun.file(`./images/${file}`)
    .image()
    .resize(1600, null, { withoutEnlargement: true })
    .webp({ quality: 80 })
    .write(`./images/${file.replace(/\.[^.]+$/, ".webp")}`);
}
```

### Serve resized images from `Bun.serve`

```ts
Bun.serve({
  routes: {
    "/avatar/:id": async req => {
      if (!/^[a-z0-9]+$/.test(req.params.id)) return new Response(null, { status: 400 });
      // Await the terminal so encoding runs off the JS thread.
      const out = await Bun.file(`avatars/${req.params.id}.png`).image().resize(128, 128).webp().blob();
      return new Response(out);
    },
  },
});
```

**Always validate `:id` / user input** before building a filesystem path — passing user-controlled strings to `Bun.Image` is an arbitrary-file-read primitive.

### Read from / write to S3

```ts
const png = await Bun.s3("bucket/photo.jpg").image().resize(800).png().bytes();
await img.resize(512).webp().write(Bun.s3("bucket/thumb.webp"));
```

## Pipeline cheat sheet

| Stage | Methods |
|-------|---------|
| Input | `new Bun.Image(path \| Buffer \| Blob \| BunFile \| S3File)`, `Bun.file(p).image()` |
| Transform | `.resize(w, h?, opts)`, `.rotate(deg)`, `.flip()`, `.flop()`, `.modulate({ brightness, saturation })` |
| Output format | `.jpeg(opts)`, `.png(opts)`, `.webp(opts)`, `.heic(opts)`, `.avif(opts)` |
| Terminal (awaitable) | `.write(dest)`, `.bytes()`, `.buffer()`, `.blob()`, `.toBase64()`, `.dataurl()`, `.metadata()`, `.placeholder()` |
| Clipboard | `Bun.Image.fromClipboard()`, `hasClipboardImage()`, `clipboardChangeCount()` |

## Gotchas

- **Don't mutate buffers** passed to the constructor while a terminal is pending (decode borrows the bytes off-thread). `SharedArrayBuffer` and resizable buffers are refused.
- **`autoOrient` defaults to `true`** — JPEG EXIF orientation is applied before any op. Pass `{ autoOrient: false }` to opt out.
- **`maxPixels` guards decompression bombs** (default ~268 MP, matches sharp). Reject images larger than your largest legitimate input.
- **`.write(path)` without a format method** picks encoding from the path extension (`.jpg`/`.png`/`.webp`/`.heic`/`.avif`).
- **HEIC/AVIF on Linux**: rejects. Catch `err.code === "ERR_IMAGE_FORMAT_UNSUPPORTED"` and fall back to WebP.
- **AVIF encode on macOS**: Apple Silicon M3+ only. M1/M2/Intel reject.

## Reference

Full API surface, every option, all platform-backend caveats, and edge cases: see [REFERENCE.md](REFERENCE.md).
