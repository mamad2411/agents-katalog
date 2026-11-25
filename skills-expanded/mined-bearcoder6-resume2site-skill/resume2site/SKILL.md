---
name: resume2site
description: Lightweight Agent Skill for turning resumes, GitHub projects, papers, and optional style references into polished GitHub Pages personal websites. Use when Codex, Claude Code, Cursor, or another coding agent needs to extract a structured profile, choose academic homepage or personal landing-page mode, plan site narrative, generate static HTML/CSS output, recommend licensed assets, protect privacy, and run a lightweight file-based final quality review.
---

# Resume2Site

Use this Skill to guide a coding agent from resume materials to a polished GitHub Pages-ready personal website.

This Skill is not a CLI, parser, crawler, SaaS app, Python package, npm package, or full automation system. Use the agent environment's available file-reading, writing, and development tools.

By default, do not require a browser, Playwright, screenshot capture, local dev server, or visual regression environment. Generate the static HTML/CSS site, run lightweight file-based checks, then give the user the `output/site/index.html` path so they can preview it locally. Browser or screenshot checks are optional only when the user explicitly asks for them or the environment clearly supports them without extra setup.

Always write generated HTML, CSS, JSON, Markdown, and asset-credit files as UTF-8. Every generated HTML page must include `<meta charset="utf-8">` in the `<head>`.

## Required Workflow

1. Read the user's resume and optional materials from the provided paths.
2. If PDF or DOCX extraction is unreliable, ask for `resume.txt`.
3. Do not directly generate a website from the raw resume.
4. Create `work/profile.json` first using `prompts/extract-profile.md`.
5. If the resume appears to contain a portrait, follow `avatar-rules.md` and preserve it when extraction is reliable.
6. Choose academic or landing mode using `mode-rules.md`.
7. If the user did not already choose a style variant and requirements, pause and ask the Style Intake question below.
8. Create `work/site-plan.md` using `prompts/plan-site.md`, `profile-schema.md`, and `information-architecture.md`.
9. Apply privacy rules before deciding what becomes public.
10. Apply the selected built-in style variant from `style-pack.md` and `design-token-rules.md`. User screenshots are optional supplements, not required style research.
11. Search for free/open/licensed visual assets when useful and when the agent has browsing/network capability.
12. Generate `output/site/index.html`, `output/site/styles.css`, `output/site/README.md`, `output/site/.nojekyll`, and assets as needed.
13. If assets are recommended or used, create `work/asset-recommendations.md` and `output/site/ASSET_CREDITS.md`.
14. Run the lightweight final quality checklist from files only, improve the page once if needed, then report the local preview path.

## Style Intake

After `work/profile.json` exists, recommend one style variant from `style-pack.md`, then ask one concise question before generating the site unless the user already made a clear choice.

Use this menu:

```text
I have read the resume. Recommended style: <variant>. Reason: <one short reason>.

Please choose a homepage style, or reply "use recommended":
1. academic-editorial: academic homepage for papers, research, and education-first profiles
2. academic-lab: academic lab feel for AI, engineering, data, or applied research
3. engineering-commercial: polished engineering style for developer, algorithm, and data job seeking
4. business-polished: refined business style for product, consulting, operations, finance, or enterprise profiles
5. creative-portfolio: visual portfolio for design, media, writing, creator, or client work
6. minimal-resume-site: conservative one-page site for formal or sparse resumes

You can add requirements too, such as language, whether to publish email, whether to use the portrait, whether to search for background images, or light/dark preference.
```

Ask this question in the user's language when possible.

If the user replies with "use recommended", "auto", or an equivalent answer, proceed with the recommended variant and record that assumption in `work/site-plan.md`.

## Inputs

Suggested, not required:

```text
input/
  resume.pdf or resume.docx or resume.txt
  avatar.png
  github_links.txt
  paper_links.txt
  website_links.txt
  style_preference.txt
  references/
```

Create folders as needed. Do not require the user to prepare this structure if they already gave concrete file paths.

## Outputs

```text
work/
  profile.json
  site-plan.md
  asset-recommendations.md
  final-review.md

output/site/
  index.html
  styles.css
  assets/
  README.md
  .nojekyll
  ASSET_CREDITS.md
```

Never copy raw resumes, private notes, hidden mappings, or internal extraction logs into `output/site/`.

## Mode Selection

- Academic Homepage: read `academic-layout-rules.md` and `prompts/generate-academic.md`.
- Personal Landing Page: read `landing-layout-rules.md` and `prompts/generate-landing.md`.
- If uncertain, read `mode-rules.md`. Ask the user when evidence is balanced.
- Style variants: read `style-pack.md` and use the selected variant consistently.

## Core References

- `workflow.md`: complete sequence.
- `profile-schema.md`: strict field, link, and metric scope contract.
- `information-architecture.md`: content-priority and section-order rules.
- `privacy-rules.md`: public/private data handling.
- `content-rules.md`: factual language and rewriting.
- `asset-rules.md`: free/open/licensed asset search, verification, and credits.
- `avatar-rules.md`: portrait extraction priority and fallback rules.
- `style-pack.md`: built-in academic and landing visual style guidance.
- `design-token-rules.md`: typography, layout, color, radius, and anti-AI visual tokens.
- `bad-smell-checklist.md`: final content, design, and asset smells to fix.
- `quality-checklist.md`: final review criteria.

## Non-Negotiables

- Extract facts before rewriting them.
- Do not invent missing experience, publications, metrics, awards, affiliations, advisors, testimonials, or credentials.
- Keep numeric evidence in its source context. Project or experience numbers such as latency, API counts, test cases, benchmark results, or cost changes must not be reused as personal/profile metrics.
- Use empty strings or arrays for missing profile fields.
- Keep user-provided facts traceable to sources when possible.
- Ask before publicly including phone numbers or sensitive personal details.
- Do not hide raw resume text in HTML comments.
- Make the page look like a personal website, not a raw resume.
- Do not block completion on screenshots, browser automation, Playwright, or local preview tooling.
- Do not silently drop an existing resume portrait; extract it or record why it could not be extracted.
- Treat style variant names as internal implementation details. Record the selected variant in `work/site-plan.md`, but do not show names such as `academic-editorial`, `engineering-commercial`, or "学术编辑风" as visible page headings, hero text, navigation labels, titles, or footers unless the user explicitly asks.
- Use UTF-8 for generated text files and include `<meta charset="utf-8">` in generated HTML.
