# Repository Guidelines

## Project Structure & Module Organization

This repository is a Quarto website and blog. Top-level `.qmd` files such as `index.qmd` and `about.qmd` define main pages. Blog listing pages live in `pages/`, including language-specific views like `pages/blog-en.qmd` and `pages/blog-ja.qmd`. Posts live under `posts/YYYY-MM-DD-slug/index.qmd`, with optional per-post references in `refs.bib`. Shared bibliography entries are in `refs/bibliography.bib`. Static assets are under `assets/`, especially `assets/images/`. Site-wide styling is in `styles.css`; browser enhancements are in `scripts/*.js`; reusable content starters are in `templates/`.

## Build, Test, and Development Commands

- `quarto preview`: starts the local development server, usually at `http://localhost:4344/`, with live reload.
- `quarto render`: builds the site into `_site/` using `_quarto.yml`.
- `quarto publish gh-pages`: renders and publishes the site to GitHub Pages.
- `bash scripts/create.sh <slug>`: create a new post with `index.qmd`, `refs.bib`, and manim source directory.
- `bash scripts/create.sh -v <name> [SceneClass]`: create a manim video source at `src/videos/<name>.py`.
- `bash scripts/create.sh -i <name>`: create a plot image source at `src/images/<name>.py`.
- `bash scripts/create.sh -c <course> <slug>`: create a course series post.
- `bash scripts/render_manim.sh <slug> <scene_class> [flags]`: render a Manim scene. Uses `uv run manim`. Example: `bash scripts/render_manim.sh fourier-series WaveScene -qm`.
- `uv run manim src/videos/posts/<slug>/scene.py <SceneClass> -qm`: render Manim directly via uv.
- `uv run manim checkhealth`: verify Manim installation (requires latex/dvisvgm on PATH).
- `bash scripts/export_plots.sh ...`: export generated plots.

## Coding Style & Naming Conventions

Use concise Markdown/Quarto prose with YAML front matter at the top of each `.qmd` file. Name post folders with the date and lowercase hyphenated slug, for example `posts/2026-06-13-fourier-transform/`. Keep image assets in `assets/images/` and use relative paths from the post. Prefer two-space indentation in YAML blocks. JavaScript in `scripts/` should be small, dependency-free, and scoped to site behavior.

## Testing Guidelines

There is no separate automated test suite. Validate changes by running `quarto render` before publishing. For visual or navigation changes, also run `quarto preview` and check the affected pages in a browser. Confirm multilingual posts set `lang: vi`, `lang: en`, or `lang: ja` so they appear in the correct blog listing.

## Commit & Pull Request Guidelines

Recent commits use short imperative summaries, such as `Update README with multilingual writing instructions` or `Add README guide for writing and publishing`. Follow that style: state the user-facing change in one line. Pull requests should describe the content or site behavior changed, list validation performed (`quarto render`, preview checks), link related issues when available, and include screenshots for layout, CSS, or asset updates.

## Security & Configuration Tips

Do not commit credentials, local environment files, or generated virtual environments. `_site/` is build output; only edit source files unless intentionally updating generated artifacts for deployment.
