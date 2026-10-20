---
name: canvas-chromakey-bg-removal
description: Browser-side background removal for sprite sheets and JPEG assets using canvas pixel data with white/color key to transparency
category: design
triggers:
  - remove white background
  - chroma key browser
  - sprite sheet transparent
  - make image background transparent css
tags:
  - canvas
  - image-processing
  - chroma-key
  - transparency
version: 1.0.0
---

# Canvas Chroma-Key Background Removal

Convert any JPEG/PNG with a solid-color (usually white) background into a transparent image at runtime using the Canvas 2D API. Useful when source assets only come in JPEG or you can't modify the file.

## Simple white-key

For sprite sheets with pure white/near-white background:

```js
function removeWhiteBackground(srcUrl) {
  return new Promise(resolve => {
    const im = new Image();
    im.onload = () => {
      const canvas = document.createElement('canvas');
      canvas.width = im.naturalWidth;
      canvas.height = im.naturalHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(im, 0, 0);
      const data = ctx.getImageData(0, 0, canvas.width, canvas.height);
      const d = data.data;
      for (let i = 0; i < d.length; i += 4) {
        if (d[i] > 230 && d[i+1] > 230 && d[i+2] > 230) d[i+3] = 0;
      }
      ctx.putImageData(data, 0, 0);
      resolve(canvas.toDataURL('image/png'));
    };
    im.src = srcUrl;
  });
}
```

## Flood-fill variant (for complex backgrounds)

When the character contains similar colors to the background (e.g. white clothing on white background), naive chroma-key over-matches. Use flood-fill from the image corners instead — only connected background pixels get cleared:

```js
// Flood-fill from 8 seed points (corners + edge midpoints) with tolerance
const stack = [[0,0],[w-1,0],[0,h-1],[w-1,h-1], /* edges */];
while (stack.length) {
  const [x, y] = stack.pop();
  if (visited[y*w+x]) continue;
  const i = (y*w+x)*4;
  // color distance < TOL to any seed color
  if (colorNearSeeds(d, i, seeds, TOL)) {
    d[i+3] = 0; visited[y*w+x] = 1;
    stack.push([x+1,y],[x-1,y],[x,y+1],[x,y-1]);
  }
}
```

Flood-fill preserves character's interior white (not connected to edges) while clearing the background.

## Injecting into CSS background-image

For sprite sheets used as CSS background (not `<img>`), inject the processed data URL via a dynamic style element:

```js
const url = canvas.toDataURL('image/png');
const style = document.createElement('style');
style.textContent = `.char { background-image: url(${url}) !important }`;
document.head.appendChild(style);
```

The `!important` is needed only if the original CSS rule is more specific.

## Cache aggressively

Chroma-key on a 600×400 sprite sheet takes ~30–60ms. Cache the data URL in a Map and reuse across the session:

```js
const cache = new Map();
function process(src) {
  if (cache.has(src)) return Promise.resolve(cache.get(src));
  return removeWhiteBackground(src).then(url => { cache.set(src, url); return url; });
}
```

## Tuning

- Threshold `230` is aggressive — if characters have very bright pixels that shouldn't be removed, drop to `245` or match only pure white (`255`).
- For JPEG sources with compression artifacts, tolerate ±10 around the seed color.
- For pixel art, feather edges by setting alpha to a ramp based on adjacent transparency — otherwise hard edges look "cut out".
