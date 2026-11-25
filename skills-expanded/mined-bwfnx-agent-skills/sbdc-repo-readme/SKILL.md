---
name: sbdc-repo-readme
description: build or rebuild the public github readme for an sbdc-related tool or repo in the house style — navy maryland sbdc banner, a before/after hero of the star tool, a three-tool highlights strip, grouped catalog, folded install, faq — with light/dark images rendered from html. use when brandon creates a new sbdc repo, says a readme looks plain or off-brand, asks for a readme "like the sbdc toolkit" or "like a popular repo", or wants a repo overview, banner, or hero image for anything sbdc-facing.
---

# SBDC Repo README

Builds the README that shipped on `bwfnx/sbdc-toolkit` on 2026-10-15 — the one Brandon said he liked everything about. That README is the reference: https://github.com/bwfnx/sbdc-toolkit. When in doubt, match it.

The structure borrows from popular open-source repos (paperclipai/paperclip): brand first, proof second, install folded away. The styling comes from the Maryland SBDC guide pages, so the repo and its docs look like one product.

## The non-negotiables

- **Brainstorm before building.** Show what's off today and the recommended layout, then wait. Ask questions one at a time with a "park it" option.
- **Fictional data only** in every image and sample: made-up business, people, town, numbers, case IDs. Reuse Harbor Lane Bakery (owner Dana, Cliffmont, $45,000 oven + walk-in) when it fits.
- **Adoption claims stay public-safe.** Use what Brandon has cleared. As of Oct 2026: "In use by SBDCs in 7 states" — never name the states.
- **Counts must match the files.** Count the tools in the repo; never trust the old README's number.
- **Brandon approves before anything is pushed.** Ship as a branch + pull request; merge only when he says so.

## Workflow

### 1. Gather (no questions yet)
- Read the current README, the repo tree, and any `docs/` guide site. Pull its CSS tokens if it has one.
- List every tool/skill with its one-line job and its guide URL.
- Pick the **star**: the tool people use most (for advising work this is usually the transcript → follow-up email skill).
- Pick **three highlights** with the most visible output. Three, never more — the catalog covers the rest.
- Note the urgency hook if there is one (e.g. OpenAI retiring custom GPTs on Enterprise workspaces Dec 11, 2026).

### 2. Brainstorm and get the go
Send one message: what's off today (bullets), the recommended section order (below), the one constraint (GitHub strips CSS, so styling lives in images), and **one** question — usually the public wording of a claim. Wait for approval.

### 3. Build the images
Copy `assets/readme-kit/` into the target repo at `docs/img/src/`. Edit the three HTML files — content only; `base.css` holds the tokens.

| Image | File | Contents |
|---|---|---|
| Banner | `banner.html` → `banner.png` (one version; navy works in both themes) | Red brand tag `MARYLAND SBDC · <TAG>`, repo name in Archivo 900, red rule, one sentence (bold promise + plain clause), pill row: white proof pill first, then platforms, then license |
| Hero | `hero.html` → `hero-light/dark.png` | Eyebrow = star tool name; headline "X in. Y out."; input card left (sunken), red arrow labeled "ONE SKILL", output card right; "Also in the reply" chips |
| Highlights | `highlights.html` → `highlights-light/dark.png` | Three cards: eyebrow, outcome headline, one context line with a bold detail, a mini mock of the real output, one "Also:" footer line |

Render: `pip install weasyprint` then `python3 docs/img/src/render.py` (needs `pdftoppm`). Chromium/Playwright downloads are blocked in the cloud sandbox; WeasyPrint is the path that works. Output is 2x for retina.

**Look at every PNG, light and dark, before moving on.** Known traps:
- Fixed-height cards overflow when text runs long — let cards size to content, keep footers in normal flow.
- Labels that wrap to two lines look broken; shorten them.
- Skip thick left-border callouts and 01/02/03 number badges inside images; use a plain tinted box and word labels (DECK, FORM, EMAIL, PDF).

### 4. Write the README
Start from `references/readme-template.md`. Section order:

1. Banner (centered, `width="760"`)
2. Centered nav row: Guides · Install · Skills · Resources · Latest release
3. Badges (shields.io): license `002d62`, release `002d62`, count `d11142`, proof `1f7a4d`
4. Hero `<picture>` with dark source
5. H1 one-line promise with the correct count
6. One paragraph; first sentence bold, says what a skill/tool *is* in plain words
7. 01 / 02 / 03 table — the star tool's job in three steps
8. "This is for you if" — ✅ bullets, bold the key phrase, include the urgency hook
9. "Three more worth a look" — highlights `<picture>` + centered links to the three guides
10. Catalog — HTML table, three columns, grouped by job with a bold group row, every name linked to its guide, ⭐ on the star
11. Install — one `<details>` per platform, then a one-line "Updating" note
12. Adapting for your state (if the tools encode Maryland practice) — table inside `<details>`
13. FAQ — 3–4 real questions (Is this a GPT? Does client data leave? Not an SBDC? Who maintains?)
14. Notes (how to rebuild images; sample data is fictional), License (include the OFL line for Archivo), centered `<sub>` footer line

### 5. Check
Run `python3 <this-skill>/scripts/check_readme.py README.md --pages-base <guide-site-url>` from the repo root. It fails on any missing local image/file and any guide link with no matching `docs/*.html`. Then confirm the count in the H1, banner, and badge match the tool folders.

### 6. Ship
- Branch, commit, push. Open the PR with `gh api repos/<owner>/<repo>/pulls -f title=… -f head=… -f base=main -F body=@file` — the GitHub connector's create-PR returns 403 and `gh pr create` is blocked (GraphQL) in the cloud sandbox.
- PR body: what changed, how to rebuild images, a 3-item check-before-merge list (rendered look, dark mode swap, public wording of claims).
- Merge only on Brandon's word (`gh api -X PUT …/pulls/<n>/merge -f merge_method=squash`). Branch deletion may be blocked by the proxy; tell him to click **Delete branch**.

## Style rules for the copy
- Plain language, short sentences, "you." No corporate filler.
- Promise in the H1, proof in the banner and badges, detail folded away.
- Name the real tool, step, or link — never "various features."

## Brand tokens (from the guide pages)
Navy `#002d62`, red `#d11142`, success `#1f7a4d`. Display font Archivo (700–900), body Arial. Masthead: navy with a soft red radial glow top-right, red brand tag, red 56–72px rule under the title. Dark theme: page `#0d1117`, card `#111f36`, text `#f3f5f8`.
