---
name: readme-brand
description: Write or restructure a README in the house style, with a centered header block, grouped shields.io badge rows, a live demo link, and a screenshot table, keeping the body lean and deferring detail to docs/. Use when creating a README, restyling one, adding or fixing badges, or checking that a markdown file's links, images, and heading anchors still resolve. Runs scripts/check_readme.py.
---

# readme-brand

## Check before and after

```bash
python <skill>/scripts/check_readme.py          # README.md
python <skill>/scripts/check_readme.py --all    # every markdown file
```

It reports relative links and images that do not resolve, and in-page anchors with no matching heading. Anchors are the ones that rot silently: renaming a heading breaks every table-of-contents entry pointing at it and nothing complains. External URLs are counted, not fetched.

## Structure

1. **Header block**, centered. Name, one-line definition or tagline, and the sentence that says what it is. When the name is unusual, give the etymology or pronunciation, it earns the reader's attention.
2. **Badges**, grouped by category. See below.
3. **Live demo link**, immediately after the header when one exists. Put it above the fold, never at the bottom.
4. **What it is**, two or three paragraphs. What problem, for whom, and the one design idea that makes it different.
5. **Screenshot table**, a two-column `<table>` of images with alt text that describes what is happening, not what the file is.
6. **Features or how it works**, short.
7. **Run it**, the minimum to get it running locally.
8. **Docs index**, linking into `docs/`.

## Badges

Group by category, each group with its own caption line, all centered:

```html
<!--- AI / ML --->
<p align="center"><sub><b>AI / ML & Frameworks:</b></sub></p>
<p align="center">
  <img src="https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white">
</p>
```

Always `style=for-the-badge`. Group into three or four rows at most: language and frameworks, then infrastructure, then status badges (CI, license, version). A single wall of twenty badges reads as noise.

URLs for the common ones are in [references/badges.md](references/badges.md). Copy from there rather than reconstructing them, the logo slugs and hex colors are easy to get subtly wrong.

## Keep the body lean

The README answers "what is this and should I care". It does not answer "how does the scoring work" or "how do I deploy it". Those go in `docs/` with a one-line pointer from the README.

A README past roughly 150 lines is usually holding something that belongs in `docs/`. Methodology, deployment and environment setup, and API detail are the three that migrate most often.

## Writing

Prose follows [prose-guard's rules](../prose-guard/references/rules.md), which bite hardest here. READMEs attract marketing vocabulary more than any other file in a repo. Run the linter when done:

```bash
python <skill>/../prose-guard/scripts/prose_lint.py README.md
```

Alt text describes the moment, not the asset. "The ledger filling in beside the real record, then a thread pulled to an event's causes" beats "screenshot of the dashboard".

## Screenshots

Regenerate them when the UI changes, and move superseded images into an archive directory rather than deleting them. A README showing a UI that no longer exists is the most visible form of doc rot.
