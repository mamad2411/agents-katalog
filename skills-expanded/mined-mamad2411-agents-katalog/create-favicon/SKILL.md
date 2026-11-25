---
name: create-favicon
description: |
  Generate a standards-aligned browser favicon.ico from a user-supplied source image, embedding PNG rasters at 32×32, 48×48, and 180×180 in one ICO container. Use when the user asks to create a favicon, 生成 favicon、网站图标、从图片做 ico、favicon.ico、create favicon from image.
  从用户提供的源图生成含 32/48/180 三档尺寸的 favicon.ico（ICO 内嵌 PNG）。若用户未上传或未指定可用源图，必须中止并提示上传/路径。
---

# create-favicon

> **Language**: Match the user’s language (中文提问则中文回复).

## Normative references (read before generating)

1. `references/ico-format-and-browser-notes.md` — ICO 结构、MIME、尺寸与 Apple Touch Icon 说明。
2. `USAGE.md` — 输入输出约定与无图门禁话术。

---

## Step 0 · Mandatory source image gate（必须最先执行）

**DO NOT** resize, pack ICO, or write `favicon.ico` until a **usable source image** is confirmed.

Treat the source as **present** only if **至少一项**成立：

- 用户在对话中 **附加了图片**；或
- 用户给出了 **可读的绝对/相对路径**，且你能 `read_file`/打开该图像文件；或
- 用户 **明确指定** 工作区内某文件为源图（例如 `@public/logo.png`），且该文件为常见栅格/矢量图格式（PNG、JPEG、WebP、GIF、SVG 等）。

**IF** none of the above applies — including when the user only says “做个 favicon”而未指定用哪张图、也未附加图片：

- **STOP** immediately.
- **DO NOT** invent a placeholder icon, **DO NOT** pick a random image from the repo, **DO NOT** run conversion tools.
- Reply clearly, e.g. **「请先上传用作 favicon 的源图片，或提供可访问的图片文件路径（如 `public/logo.png`），我才能生成 `favicon.ico`。」**

---

## Step 1 · Resolve output path

- Ask or infer where to write `favicon.ico` (e.g. `public/favicon.ico`, `app/favicon.ico`, or site root). Do not overwrite without user confirmation if a file already exists.

---

## Step 2 · Generate ICO（不污染用户业务项目）

**Goal**: only write the user-approved **`favicon.ico`** into their **application** tree (e.g. `public/favicon.ico`). **Do not** run `pnpm install` / `pnpm build` for this CLI in an **unrelated** app repo root, and **do not** add `node_modules`, CLI `dist/`, or a copied `tools/create-favicon` tree there **unless the user explicitly asks to vendor the tool** (then warn about gitignore / lockfiles).

Pick **one** path **in order**:

1. **This skills monorepo checkout** — If the workspace is (or you can resolve) the repo that already contains `tools/create-favicon/package.json` (e.g. **`stark-skills`**):  
   `cd <absolute-path-to>/tools/create-favicon && pnpm install && pnpm build`  
   then run **`node`** with **absolute** `--input` and `--output` (output may point into the user’s app directory).

2. **Disposable build in OS temp** — If the user’s open project is **only** their site/app and does **not** ship this CLI: clone or copy **only** `tools/create-favicon` (and needed files) under **`$TMPDIR`** / `%TEMP%` / `mktemp -d`, run `pnpm install && pnpm build` **there**, then:  
   `node dist/cli.js --input "<absolute source image>" --output "<absolute path in user app>/favicon.ico"`  
   Remove the temp tree when done (keep the ICO).

3. **Published runner (if documented)** — If this CLI is published as an **`npx <package>`** or global binary in project docs, prefer it so the user’s app directory does not gain a local `node_modules` for this workflow.

4. **Non-Node fallback** — **ImageMagick** / **`magick`** or another approach that satisfies **ICO + three PNG payloads** without leaving Node build artifacts in the user’s app; see `USAGE.md`.

```bash
# Example after building CLI in monorepo or temp dir — always use absolute paths.
# Default: --fit contain（整图可见，非方形时透明或白边，不默认裁切）
node dist/cli.js --input "<absolute-path-to-source.png>" --output "<absolute-path-to-user-app>/public/favicon.ico"

# Only if the user explicitly wants 铺满/裁剪去留白（需确认可能裁掉边缘）:
node dist/cli.js --input "..." --output "..." --fit cover
```

**Framing（构图）**

- **默认 `contain`**：等比缩放，**整张源图都保留在方形内**，居中；有 alpha 的源图留白为**透明**；无 alpha（如 JPEG）留白为**白色**（要透明边请用 PNG/SVG）。**禁止**在用户未要求时用 `cover` 把图裁成「另一张」。
- **`--fit cover`**：**仅当**用户明确说不要留白、要填满、裁剪铺满等，并**提示可能裁边**后，再传入 CLI 或等效流程。

**Multi-size / scaling（多尺寸与画质）**

- **32 / 48 / 180** 共用 **同一套** `fit`、居中、留白规则；只是像素变多/变少，**不要**让某一档单独换裁切方式。
- 参考 CLI 使用 **Lanczos（lanczos3）** 缩放；若 stderr 出现 **过小位图源** 警告，提醒用户换 **更高分辨率** 或 **SVG**。

The CLI writes a single `favicon.ico` containing **three** embedded **PNG** blobs at **32×32**, **48×48**, and **180×180** (ICO container per Windows icon layout; see references).

**Fallback** — if every CLI path fails:

- Use step **4** or stop and explain what is missing (network for clone, Node, `sharp`, or ImageMagick).

---

## Step 3 · Quick verification

- Confirm file size is non-zero and magic `00 00 01 00` at offset 0 (ICO), image count `03 00` at offset 4.
- Optionally decode each embedded PNG signature `89 50 4E 47` at offsets listed in directory entries.

---

## Step 4 · Tell the user

- Output path, the three embedded sizes, **framing used**（`contain` = 整图可见 / `cover` = 可能裁边）, **that all three sizes share the same composition**（仅分辨率不同）, and **high-quality (Lanczos) resize** unless another tool path was used. If `cover` was used, **do not** imply the icon is pixel-identical to the uncropped source. If a small-source warning appeared, relay it. Mention that **iOS 主屏幕** 常用独立 `apple-touch-icon.png`；详见 `references/ico-format-and-browser-notes.md`。
