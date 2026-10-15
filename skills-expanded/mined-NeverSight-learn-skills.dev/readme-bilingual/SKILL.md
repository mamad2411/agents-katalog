---
name: readme-bilingual
description: Creates and maintains dual READMEs (README.md in English, README.pt-BR.md in Portuguese) optimized for GitHub.com, with badges, cross-links, and optional images. Use when creating or updating project docs, when the user asks for a README or bilingual documentation, or when adding a new app.
---

# Bilingual README (EN + pt-BR)

Expert in READMEs for apps in any language. Output is **optimized for GitHub.com**: the repo’s front page, discovery, and Markdown rendering. Always deliver **two files**: main in English, additional in Portuguese (pt-BR). Be creative (8/10), concise, and avoid repetition or filler.

## Output files

| File | Language | Role on GitHub |
|------|----------|----------------|
| `README.md` | English | **Repository front page** (default landing for the repo) |
| `README.pt-BR.md` | Portuguese (pt-BR) | Additional; linked from README.md so visitors can switch |

**If a Portuguese README already exists:** rename/copy it to `README.pt-BR.md`, then create a new `README.md` in English (do not overwrite existing pt-BR content).

## Cross-link between versions

GitHub shows only one README on the repo homepage. In **both** files, near the top (after the title or badges), add one line so visitors can open the other language:

- In **README.md**:  
  `Read in Portuguese: [README.pt-BR.md](README.pt-BR.md)`
- In **README.pt-BR.md**:  
  `Read in English: [README.md](README.md)`

Use **relative** paths so links work on GitHub (no absolute URLs). Adjust wording only if needed for tone.

## Badges

Use **GitHub-friendly** badges so they render correctly on the repo page. Prefer [Shields.io](https://shields.io): e.g. license, language/runtime, GitHub Actions status, release/version, coverage. Place under the title; 3–6 badges. When the repo has Actions/workflows, include a status badge if relevant. Example: `![CI](https://github.com/user/repo/actions/workflows/ci.yml/badge.svg)`.

## Images

GitHub renders images from the repo via relative paths. If the project has **`images/`** or **`docs/images/`** with relevant assets (screenshot, logo, diagram), include 1–2 with a short caption. Use paths like `images/screenshot.png` so they work on GitHub. If there is no such folder or no relevant image, skip.

## Content requirements

- **What the app does**: Always include a short, clear description (1–3 sentences) of what the application does.
- **Sections**: Structure suited to GitHub (e.g. Description, Install, Usage, Config, Contributing, License). Use headings and lists so the page is scannable. Be brief; avoid long paragraphs.
- **Tone**: Professional, direct. Creativity 8/10: varied wording, no generic fluff, no irrelevant details.
- **Links**: Prefer relative links to files in the repo (e.g. `[Contributing](CONTRIBUTING.md)`) so they work on GitHub.

## Checklist before delivering

- [ ] Two files: `README.md` (EN) and `README.pt-BR.md` (pt-BR).
- [ ] Cross-link present in both; links relative for GitHub.
- [ ] Badges added (3–6), GitHub-friendly and rendering on the repo page.
- [ ] App description included in both.
- [ ] Images from `images/` or `docs/images/` used if available; paths relative.
- [ ] Concise; no repetition between EN and pt-BR beyond structure.
