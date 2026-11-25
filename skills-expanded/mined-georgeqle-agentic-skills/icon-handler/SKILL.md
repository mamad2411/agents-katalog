---
name: icon-handler
description: Audit and apply project-root icon assets to favicon, app icon, Apple touch icon, and manifest surfaces
type: execution
version: v0.0
argument-hint: "[audit|fix] [asset filename]"
---

# Icon Handler

Use this skill when a user adds a desired icon image at the project root and wants it applied consistently across website/app icon surfaces. It works like `$hygiene`: audit first, show findings and a correction plan, then modify files only after the user explicitly approves `fix`.

## Process

### 1. Determine Mode and Asset

Parse `$ARGUMENTS`:

- **Mode:** `audit` by default; `fix` applies approved corrections.
- **Asset:** optional filename or path. If omitted, search only the project root for likely icon assets.

Candidate asset names, in priority order:

1. User-provided path.
2. Root files matching `*-icon.png`, `*icon.png`, `*logo.png`, `favicon.png`, or `app-icon.png`.
3. Root SVG equivalents only when the app toolchain can rasterize them safely.

If multiple candidates exist, stop and ask which one to use.

### 2. Identify App Framework

Audit only what is relevant to the repository:

- **Next App Router:** `src/app/favicon.ico`, `src/app/icon.png`, `src/app/apple-icon.png`, `public/manifest.webmanifest`, `public/apple-touch-icon.png`, and `metadata.icons` in `src/app/layout.tsx`.
- **Next Pages Router:** `public/favicon.ico`, `public/icon.png`, `public/app-icon.png`, `public/apple-touch-icon.png`, `_document` or page/head icon links, and any manifest.
- **Vite/React/static:** `public/favicon.ico`, `public/icon.png`, `public/app-icon.png`, `public/apple-touch-icon.png`, `index.html`, and any manifest.
- **Other frameworks:** report the detected framework and only apply conventional public-root assets unless the framework has clear local icon conventions.

Do not assume `icon.ico` is a standard favicon name. The conventional browser-probed file is `favicon.ico`.

### 3. Audit Icon Surfaces

Inspect without modifying:

- Source asset format and dimensions using available tools (`file`, `sips`, `identify`, or framework tooling).
- Existing favicon/app icon files and whether they still contain stale assets.
- Metadata or HTML links for:
  - `/favicon.ico`
  - `/icon.png`
  - `/app-icon.png`
  - `/apple-touch-icon.png`
  - Next App Router `/apple-icon.png`
  - `manifest.webmanifest`
- Whether generated build output or static HTML emits `rel="icon"`, `rel="shortcut icon"`, and `rel="apple-touch-icon"` links.

### 4. Produce Audit Report

Report:

- Detected framework and project root.
- Chosen source asset and dimensions.
- Existing icon surfaces found.
- Missing, stale, or non-standard surfaces.
- Proposed file writes, conversions, and metadata edits.
- Verification commands to run after changes.

Stop after the audit unless the user invoked `fix` or explicitly approves the proposed writes.

### 5. Apply Fixes After Approval

Only after approval:

- Preserve the source asset at its original path unless the user asks to move it.
- Copy the source asset to PNG surfaces that should remain full-size or app-install size.
- Generate `favicon.ico` from a smaller source when conversion tools are available. Prefer:
  - `magick`/ImageMagick when installed.
  - macOS `sips` as a fallback: create a 256px PNG first, then convert that PNG to ICO.
  - If no converter exists, stop and report the exact missing command rather than leaving a stale ICO.
- For Next App Router, prefer:
  - `src/app/favicon.ico`
  - `src/app/icon.png`
  - `src/app/apple-icon.png`
  - `public/apple-touch-icon.png`
  - `public/icon.png`
  - `public/app-icon.png`
- Add or update manifest icons when a manifest exists or when app-install behavior is expected.
- Update Next metadata or static HTML links so the generated site references the conventional paths.

### 6. Verify

Run the smallest relevant checks:

- File format checks for generated assets.
- Framework type/lint checks when metadata or source code changed.
- Production build or static render when available.
- Generated HTML/build-output search for `favicon.ico`, `apple-touch-icon`, `icon.png`, and `manifest.webmanifest`.

For Next App Router, verify `.next/server/app/favicon.ico.body`, `.next/server/app/icon.png.body`, and `.next/server/app/apple-icon.png.body` when a build was run.

### 7. Document and Ship

If the project has task docs, add a concise review note with:

- Source icon path.
- Files changed.
- Verification results.
- Any cache caveat: browsers and iOS may require hard refresh, cache clear, reinstalling the home-screen icon, or waiting for deployment/CDN cache expiry.

Commit and push if the user asked to ship or the active workflow requires it.

## Output Format

In audit mode:

```text
## Icon Audit

Framework: Next App Router
Source asset: calc-mascot-icon.png (1024x1024 PNG)

Findings:
- Missing /apple-touch-icon.png
- Stale src/app/favicon.ico

Proposed fix:
- Generate src/app/favicon.ico from the source icon
- Copy source to src/app/icon.png, src/app/apple-icon.png, public/icon.png, public/app-icon.png, public/apple-touch-icon.png
- Update metadata.icons and manifest.webmanifest

Approval needed: reply "fix" to apply these changes.
```

In fix mode, include the same report plus changed files, validation, and next command.

## Constraints

- Read-only by default.
- Do not overwrite existing branded icon assets without showing the diff/format evidence and getting approval.
- Do not invent framework conventions; verify local framework and file layout first.
- Do not use `icon.ico` as the default favicon path.
- Do not commit generated binary assets until format checks pass.
- Do not touch unrelated visual branding, OG images, logos, or marketing copy unless the user explicitly asks.
- Prefer project-local tooling. Do not install image conversion dependencies without explicit approval.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page at `alignment/icon-handler-{topic}.html`. Use a normalized topic slug derived from the app, feature, research subject, report subject, or output filename.

**Full content requirement.** The alignment page must contain the complete content of every proposed markdown deliverable -- every section, every finding, every detail, every list item. It is a thorough interactive review document, not a summary. Render the full deliverable content in clean, readable HTML with appropriate hierarchy, styling, and navigation. If the skill writes multiple scoped deliverables in one run, build one alignment page that contains all deliverables with anchor-linked navigation. Durable tracker artifacts, such as `research/assumption-tracker.md`, remain canonical markdown outputs but must also be fully rendered into the alignment page before approval.

**Dark-mode styling.** Use a dark color scheme by default. Base CSS variables: `--bg: #0d1117; --surface: #161b22; --border: #30363d; --text: #c9d1d9; --text-muted: #8b949e; --accent: #58a6ff; --green: #3fb950; --red: #f85149; --orange: #d29922; --purple: #bc8cff;`. Apply `background: var(--bg); color: var(--text);` on body. Use `--surface` for cards, nav, and table headers. Use `--border` for all borders. Use `--purple` for question blocks and gate headings. Use `--accent` for links and section headings. Keep headings `color: #fff` or `var(--accent)` for hierarchy. Question block backgrounds should use `#1c2333`.

**Alignment gates.** Treat gates as explicit review sections inside the HTML page. A gate blocks finalization until its required inline questions are answered and compiled into YAML. Include every gate that applies to the skill output, and include these gate types whenever relevant: evidence coverage, assumptions/confidence, scope/non-goals, candidate/verdict decisions, artifact destination, proposed file changes, coverage checkpoint, and post-approval route.

**Report-only research gates.** For report-only or pre-approval research skills, the alignment page must explicitly contain evidence coverage, assumptions/confidence, recommended path, proposed file changes, and approval gates before any canonical research, spec, or task file is created or updated.


**Required inline questions.** Each gate must contain at least one required inline question placed directly under the content it governs, inside a visually distinct question block. Each question must use radio-button inputs and include two standing options after the skill-generated choices: "Other / None of the above" backed by a multi-line text box for free-form input, and "Need clarification" backed by an optional notes box where the user can explain what is unclear. When any radio option other than "Other" or "Need clarification" is selected, show an optional "Additional notes" text box beneath it so the user can qualify their choice. Generate questions based on what genuinely needs user input -- do not add filler questions. Do not create a separate bottom "Decisions & Clarifications" section.

**Gate YAML contract.** At the bottom of the page, include a "Compile Answers" button that aggregates answers from all inline gate questions throughout the page, including free-text notes. The button remains disabled until every required question has a selection, shows a count of remaining unanswered questions, and scrolls to the first unanswered question if clicked early. When every question is answered, generate a structured YAML block with one item per gate answer using this stable shape: `section`, `gate_type`, `status` (`answered`, `other`, or `needs-clarification`), `answer`, optional `notes`, and optional `target_artifact` or `target_path` when the gate controls file output. After successful compilation, automatically attempt to copy the YAML to the clipboard with the Clipboard API, display copy status, and display the YAML in a read-only textarea with an explicit "Copy YAML" button. The copy button must retry clipboard copy when supported and fall back to selecting the textarea contents when clipboard access is unavailable or blocked.

**Pre-approval stop.** Before user approval, the next action is review of the HTML alignment page, not downstream routing. Ask the user to review the page and provide the compiled YAML answers. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language until after compiled YAML has been provided and the approved artifacts have been written or updated.

**Diff highlighting on updates.** When the agent updates an existing alignment page after receiving compiled answers, highlight what changed since the previous version. The agent chooses inline annotation or side-by-side layout per situation.

**Archiving.** Before replacing an existing alignment page, archive it to `docs/history/archive/YYYY-MM-DD/HHMMSS/alignment/icon-handler-{topic}.html`.

**Browser open.** Attempt to open the resulting HTML page in the browser and report whether the open succeeded or was blocked. A blocked browser-open attempt does not make the skill fail when the files were written correctly.

## Default Shipping Contract

- **Next work:** if audit finds issues and approval is missing, the next work is "approve `$icon-handler fix <asset>`".
- **Recommended next command:** `$icon-handler fix <asset>`
