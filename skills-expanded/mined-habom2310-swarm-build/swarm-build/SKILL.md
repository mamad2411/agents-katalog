---
name: swarm-build
description: Add the swarm-build animation to a website, where a swarm of named, coloured cursors draws boxes and builds a screenshot region by region, or rebuilds a whole live page block by block, like a multiplayer design file. Use when the user wants a hero or product image to "build itself", wants multiplayer or Figma-style cursors on a page, or names swarm-build. Works with plain HTML and any framework (React, Next.js, Vue, Svelte, Astro).
---

# swarm-build

swarm-build is one dependency-free ES module (`src/swarm-build.js`, about 600 lines) plus an optional CSS file (`src/swarm-build.css`).
It has two modes:

- **Image mode**, `swarmBuild(img)`: a blank canvas covers an `<img>` (or an element with a CSS `background-image`), and each region of it sweeps in after a cursor drags out its box with a live `W × H` badge.
- **Page mode**, `swarmBuildPage("[data-swarm-block]")`: the marked elements of a live page disappear, then the cursors rebuild them one by one. Plain-text blocks (headings, short paragraphs) type themselves in. A block inside another block waits for its parent. Blocks below the fold wait until they scroll into view, so the swarm follows the reader down the page.

In both modes the cursors leave at the end and every change the library made is undone.

## 1. Install

Copy `src/swarm-build.js`, `src/swarm-build.d.ts` and `src/swarm-build.css` from this repo into the project (for example `lib/swarm-build/`) and import them with relative paths.
There are no dependencies and no build step.

Only if `npm view swarm-build` shows the package is published: `npm install swarm-build`, then `import { swarmBuild } from "swarm-build"` and `import "swarm-build/style.css"`.

## 2a. Page mode: mark the blocks

1. Read the page's markup and pick the blocks a designer would draw: nav bar, hero heading, hero paragraph, each button, each card, chart, table, footer. A typical landing page has 25 to 60.
2. Add `data-swarm-block` to each one.
   - Mark containers (a card) and the text inside them (its heading and paragraph) to get "frame first, then fill it in".
   - Mark headings and short paragraphs whose content is plain text: those type in. Elements with inline markup (links, `<b>`) sweep in instead.
   - Skip wrappers that only do layout (grids, sections without their own background). Hiding them hides everything inside at once.
3. Do not mark fixed or sticky UI the visitor needs right away, such as a cookie banner or chat widget.
4. Call it after the content is in the DOM:

```js
import { swarmBuildPage } from "./lib/swarm-build/swarm-build.js";
swarmBuildPage("[data-swarm-block]", { speed: 1.5 });
```

To hide the blocks before the script runs (no flash of the finished page), also add `data-swarm-pending` to each block and include the CSS file.

## 2b. Image mode: choose the regions

Regions decide what gets built and in what order.
Good regions are what makes the animation look intentional, so do not skip this step.

1. Open the image and look at it (read the image file, or take a screenshot of the page).
2. List the 6 to 15 meaningful blocks a designer would draw: navigation rail, header, search bar, cards, chart, list, footer.
3. Write each block as `x y w h` in percent of the image's width and height (0 to 100). Measure from the pixel size: `x = left / imageWidth * 100`.
4. Order them the way a person would build the screen: chrome first (rail, header), then content top to bottom.
5. Leave small gaps. Anything no region covers appears when the canvas fades at the end, so regions do not need to cover every pixel.

Put them on the image as `data-swarm-regions="0 0 18 100, 21 3.5 47 5.5, ..."`, or pass `regions: [{ x, y, w, h }]` in JavaScript.
Without regions the library uses a generic sidebar, header and cards layout, which rarely matches the image.

## 3. Wire it in

Plain HTML:

```html
<link rel="stylesheet" href="/lib/swarm-build/swarm-build.css" />
<img src="/shot.png" alt="..." width="1200" height="800"
     data-swarm-pending
     data-swarm-regions="0 0 18 100, 21 3.5 47 5.5, 21 13 24 16" />
<script type="module">
  import { swarmBuild } from "/lib/swarm-build/swarm-build.js";
  swarmBuild(document.querySelector("img[data-swarm-regions]"));
</script>
```

React or Next.js (client component):

```tsx
"use client";
import { useEffect, useRef } from "react";
import { swarmBuild } from "@/lib/swarm-build/swarm-build.js";

export function BuiltImage(props: React.ComponentProps<"img"> & { regions: string }) {
  const ref = useRef<HTMLImageElement>(null);
  useEffect(() => {
    const swarm = swarmBuild(ref.current!);
    return () => swarm.destroy();
  }, []);
  const { regions, ...img } = props;
  return <img ref={ref} {...img} data-swarm-pending="" data-swarm-regions={regions} />;
}
```

For Vue, Svelte or Astro, do the same: call `swarmBuild(el)` after mount and `destroy()` on unmount.
Several images (for example an iPad and a phone) can share one swarm: `swarmBuild([ipadImg, phoneImg])`.

## 4. Options

| Option | Default | Use |
| --- | --- | --- |
| `regions` (per target) | `data-swarm-regions`, then generic | What to build, in order |
| `agents` | 6 built-in names and colours | `[{ name, color, text }]`, match the site's palette and audience |
| `speed` | `1` | `2` halves the duration (about 6 to 8s at 1 for 10 to 15 regions) |
| `start` | `"visible"` | `"now"` starts at once instead of when the image scrolls into view |
| `canvas` | `"#fff"` | Colour of the unbuilt canvas; match the screenshot's background |
| `zIndex` | `2147483000` | Stacking of the fixed cursor layer; lower it if a modal or header must stay on top |
| `onDone` | none | Called once when the build completes or `finish()` is called |
| `typeSpeed` (page mode) | `1` | Speed of typed text; `2` types twice as fast |

The return value has `finished`, `finish()` and `destroy()`:

- `finished` is a Promise that always resolves, however the swarm ends.
- `finish()` jumps to the finished image, and `onDone` runs.
- `destroy()` removes everything now, and `onDone` does not run. Call it on unmount.
- `setSpeed(n)` changes the speed while it runs.

In page mode `start` defaults to `"now"`; in image mode to `"visible"`.

## 5. Rules to keep

- `data-swarm-pending` plus the CSS file keep the image hidden until the script starts, so it does not flash finished first. If the script never runs, the CSS shows the image after 4 seconds. Leave the attribute off when the image is the page's LCP element and load time matters more than the effect.
- Reduced motion (`prefers-reduced-motion: reduce`) shows the finished image and never animates. Do not override this.
- In page mode, hidden blocks are `inert` until they start to appear, so keyboard focus never lands on something invisible. If a block holds the control that started the build, move focus somewhere visible (for example a Finish button).
- Cursors live in a fixed, full-viewport layer above the page (`pointer-events: none`).
- While it runs, the library inserts an overlay right after the image, inside the image's parent. If the parent was static, it also sets `position: relative` on it. Both are undone at the end.
  - Give the image a block-level parent of its own, such as a `<div>` or `<figure>`. Inline parents like `<a>` or `<picture>` can misplace the overlay.
  - Sibling CSS like `:last-child` or Tailwind `space-y-*` can briefly change while the overlay is there.
- The image is copied as a CSS background stretched to the image's content box. Borders and padding on the image are fine, but `object-fit: cover` or `contain` crops are not reproduced.
- Under a strict CSP or Trusted Types no change is needed: the library builds every element with DOM calls, sets styles through the CSSOM, and uses no `innerHTML`, `<style>` or inline script. The image URL must be allowed by `img-src`.

## 6. Verify

1. Load the page and watch one full build. Each box should land on a real UI block of the image, not on empty space or across two blocks.
2. Check a phone width (375px). Badges and name tags are a fixed size, so very small images may feel crowded; use fewer, larger regions there.
3. Turn on reduced motion in the OS or browser dev tools: the image must show at once, with no cursors.
4. Check the console for errors, and that no `aria-hidden` swarm elements are left in the DOM after it finishes.
