---
name: static-project-gallery-upload
description: Use when a user provides project/portfolio/gallery images for a static website and wants them displayed on the site, exact duplicate images removed, visually related building views kept together, images optimized, and a host upload folder such as "UP FILE" prepared. Triggers include Persian requests like "عکس پروژه ها", "تکراری نباشن", "توی سایت نمایش داده بشن", "فایل های هاست", "UP FILE".
---

# Static Project Gallery Upload

Turn a loose folder of project images into a production-ready static-site gallery and upload package.

## Core rule

Remove **only exact duplicates** unless the user explicitly asks for visual deduplication.

- Exact duplicate = same file bytes / same cryptographic hash, even if filenames differ.
- Similar image, same building, different angle, crop, lighting, render alternative, or facade view = **keep it**.
- If multiple views belong to the same building or design alternative, place them near each other in the gallery order.
- Do not delete the user's original source images unless explicitly instructed; create a clean derived output instead.

## Workflow

### 1. Discover the project shape

Inspect the root before editing.

Check:

- Is the site static HTML/CSS/JS, Astro, React, Next, or another stack?
- Where are current gallery/project images referenced?
- Where are public assets served from?
- Does the project already have an upload/output folder convention such as `UP FILE`?
- Are image tools already available, e.g. `sharp` in `package.json`?

Completion criterion: you know which files must be edited, which folders are source-only, and which files must be copied to the host package.

### 2. Inventory and exact-dedupe the source images

List every image in the user-provided folder and compute SHA256 hashes.

Use exact-hash grouping as the authoritative duplicate test:

```powershell
Get-ChildItem "<source-image-folder>" -File |
  Get-FileHash -Algorithm SHA256 |
  Group-Object Hash |
  Where-Object { $_.Count -gt 1 }
```

For each exact duplicate group, keep one representative. Prefer:

1. The filename without copy suffixes like `(1)`, `(2)`.
2. The filename already referenced by the site.
3. Otherwise the earliest/cleanest name.

Completion criterion: you have a source-to-output mapping where every exact hash appears once, and no visually distinct angle was removed.

### 3. Preserve visual families in gallery order

Sort the kept images intentionally.

Guidelines:

- Keep existing on-site project order first if the site already had a gallery.
- Put sequential camera/photo filenames together when they likely represent the same building.
- Put render alternatives together, e.g. `render2`, `render3`, `alternative 1..5`.
- If a perceptual hash says two images are similar but their SHA256 differs, treat that as a grouping hint only, not a deletion reason.

Completion criterion: related views are adjacent, and the count still equals exact-unique source images.

### 4. Create web-safe optimized assets

Generate derived files with stable ASCII names in the site's asset folder, for example:

```text
assets/images/projects/project-01.webp
assets/images/projects/project-02.webp
...
```

Recommended optimization with Sharp:

- Auto-rotate from EXIF.
- Resize within a practical max box, e.g. width `1200`, height `1600`, `fit: "inside"`, `withoutEnlargement: true`.
- Encode WebP around quality `80-84`.
- Keep source images untouched.

Also write a local report such as `projects-report.json` containing:

- total source file count
- exact unique count
- exact duplicate groups
- generated output files
- original dimensions and output sizes

Do not include internal reports in the host upload folder unless the user asks.

Completion criterion: optimized image count equals exact-unique image count, filenames are host-safe, and each output file opens/has nonzero size.

### 5. Update the site gallery

Modify the existing gallery instead of creating a disconnected new section.

For static HTML:

- Update the visible image count.
- Replace old `img src` paths with the optimized asset paths.
- Use useful `alt` text matching the company/project context.
- Add `loading="lazy"` and `decoding="async"` for gallery images.
- Keep existing classes, animation delays, accessibility attributes, and JavaScript hooks unless they are broken.

For framework projects:

- Follow the project's existing image import/public-asset convention.
- Do not introduce a new framework or image library unless already in use or explicitly requested.

Completion criterion: the gallery references every generated project image exactly once and no longer references the loose source folder.

### 6. Prepare the host upload package

Create or refresh the user's upload folder, e.g.:

```text
<project-root>/UP FILE
```

Copy only production-needed files:

- HTML pages
- CSS and JS bundles/files used by those pages
- image assets referenced by HTML/CSS, including optimized project images
- `robots.txt`, `sitemap.xml`, favicon, or other root production files when present

Exclude:

- `node_modules`
- `backups`
- source-only `docs` unless the site references it
- reports/contact sheets/helper scripts unless requested
- package files unless the host specifically needs a build environment

Completion criterion: the upload folder mirrors the deployable site root and contains no unnecessary development folders.

### 7. Validate before final answer

Run a deterministic validation pass.

Check at minimum:

- Every local `src`/`href` referenced by HTML exists in the upload folder.
- The gallery image count in HTML equals the number of optimized project files.
- No gallery image path points to the source-only folder, e.g. `docs/proj`.
- No exact duplicate generated project files exist in the upload folder.
- CSS/JS cache-busting versions were updated if the project uses query versions.
- Total file count and total upload size are known.

Example Node validation pattern:

```js
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const root = "<upload-folder>";
const html = fs.readFileSync(path.join(root, "index.html"), "utf8");
const refs = [];
for (const pattern of [/<(?:img|script)[^>]+src=["']([^"']+)["']/g, /<link[^>]+href=["']([^"']+)["']/g]) {
  let match;
  while ((match = pattern.exec(html))) refs.push(match[1]);
}

const missing = refs
  .filter((ref) => !/^(https?:|mailto:|tel:|#|\/\/)/.test(ref))
  .filter((ref) => !fs.existsSync(path.join(root, ref.split("?")[0].split("#")[0])));

const projectDir = path.join(root, "assets/images/projects");
const hashes = new Map();
for (const file of fs.readdirSync(projectDir).filter((name) => /^project-\d+\.webp$/.test(name))) {
  const hash = crypto.createHash("sha256").update(fs.readFileSync(path.join(projectDir, file))).digest("hex");
  hashes.set(hash, [...(hashes.get(hash) || []), file]);
}

console.log({
  missing,
  projectRefs: [...html.matchAll(/assets\/images\/projects\/project-\d+\.webp/g)].length,
  projectFiles: fs.readdirSync(projectDir).filter((name) => /^project-\d+\.webp$/.test(name)).length,
  duplicateGeneratedFiles: [...hashes.values()].filter((group) => group.length > 1)
});
```

Completion criterion: validation reports no missing files, no exact duplicate generated project images, and no source-folder references in the deployable output.

## Final response checklist

Tell the user:

- How many source images were found.
- How many exact-unique images were kept.
- Which exact duplicate groups were collapsed, summarized by filenames or counts.
- Where optimized images were written.
- Where the upload-ready folder is.
- What validation passed.

If the user speaks Persian, answer in Persian and use their terms, especially `پروژه‌ها`, `تکراری دقیق`, `زاویه متفاوت`, and `UP FILE`.