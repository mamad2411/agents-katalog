---
name: postkit-render
description: Render a post's slides to PNG using the postkit Puppeteer pipeline. Use when the user wants to see a post, export it, generate images, or preview after edits. Also use right after /postkit-new unless the user says to wait.
---

# /postkit-render — render slides to PNG

You render `posts/<slug>/slide-*.html` to PNG at the post's native dimensions.

## What to do

1. **Figure out which post to render.** If the user named one, use it.
   Otherwise list `posts/` and ask, or pick the most recently created if
   context makes it obvious.
2. **Sanity-check the post folder.** It must contain at least one
   `slide-*.html` and preferably a `post.json`. If `post.json` is missing,
   rendering defaults to `9:16`.
3. **Shell out to postkit** from the project root:

   ```bash
   npx postkit render posts/<slug>
   ```

   Output lands in `posts/<slug>/output/slide-N.png`. The command prints each
   file as it renders.
4. **Report back** with the output directory and the list of rendered files.
   If the user asked for a different format than `post.json` specifies, pass
   `--format 1:1` (or whichever) to the same command.

## If rendering fails

- **"No .html slide files found"** → the slug is wrong, or slides weren't
  created yet. Offer to run `/postkit-new`.
- **Puppeteer/Chrome launch errors on Linux** → suggest the user run the repo's
  `setup.sh` (installs Chromium deps) or use the `Dockerfile`.
- **Fonts look wrong** → the renderer waits 1.5s for web fonts; if a
  custom Google Font was added recently, re-render. Persistent issues usually
  mean the `@import` in `theme.css` is missing or typo'd.

## Multiple posts at once

If the user asks to render a series, call the command once per post:

```bash
npx postkit render posts/series-01
npx postkit render posts/series-02
npx postkit render posts/series-03
```

Batch the results in a single report at the end.

## Important

- Don't edit slide HTML here. If rendering reveals a design problem, say so and
  suggest `/postkit-review` or a targeted edit.
- Don't commit or push anything. Rendered PNGs are gitignored by default.