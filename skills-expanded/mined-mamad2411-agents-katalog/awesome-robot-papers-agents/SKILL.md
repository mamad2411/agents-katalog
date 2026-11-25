# Repository Guidelines

## Project Structure & Module Organization

This repository supports robotics paper research: downloading papers, analyzing key ideas, identifying practical problems solved, and mapping useful methods to the user's own robot projects. Keep top-level docs in the root. Use `papers/` for PDFs, `notes/` for analyses, `data/` for metadata, `assets/` for figures, and `scripts/` for utilities.

## Build, Test, and Development Commands

There is no application build system yet. Use lightweight checks before submitting changes:

- `npx prettier --check "**/*.md"` checks Markdown formatting if Prettier is available.
- `rg "TODO|FIXME"` helps find unfinished notes before opening a pull request.

Run every Python script inside the repository conda environment:

- `conda create -n awesome-robot-papers python=3.11`
- `conda activate awesome-robot-papers`
- `python scripts/example.py`
- `python scripts/convert_to_markdown.py papers/example.pdf papers/example.md` converts supported documents to Markdown with MarkItDown.

Record Python dependencies in `requirements.txt` and install them with `pip install -r requirements.txt`.

## Coding Style & Naming Conventions

Write Markdown with concise headings, short paragraphs, and stable relative links, for example `[papers/example.pdf](papers/example.pdf)`. Use lowercase kebab-case filenames such as `humanoid-manipulation.md`. Paper entries should include title, authors, venue/year, source link, local PDF path, key innovation, solved problem, and robot application idea.

## Testing Guidelines

For documentation changes, validate readability, links, and paper metadata. Keep list ordering consistent with the surrounding section. If scripts are added, include a matching test command and place tests near the script or under `tests/`.

## Paper Analysis Guidelines

Each analysis should generate both English and Chinese Markdown notes. If the source paper is not Markdown, save both the original file and a converted Markdown copy in `papers/`; prefer `scripts/convert_to_markdown.py` for conversion. The content should be actionable, not just a summary. Include the research question, method, key innovation, experiments, limitations, and practical robotics impact. End with `Application to My Robot` / `应用到我的机器人`: integration idea, required sensors or compute, expected benefit, and risks. When a follow-up question analyzes a specific paper, append the answer under a `Question Analysis` / `问题分析` section in that paper's corresponding note.

## Commit & Pull Request Guidelines

Git history is unavailable in this checkout, so use clear imperative commits such as `Add mobile manipulation papers` or `Fix broken dataset links`. Pull requests should include a short summary, reason for the change, validation performed, and linked issues when available.

## Agent-Specific Instructions

Keep automated edits narrow. Do not reformat unrelated sections or reorder large paper lists unless asked. Preserve local citation style, verify titles, venues, and URLs before adding papers, and update `requirements.txt` for any new Python dependency.
