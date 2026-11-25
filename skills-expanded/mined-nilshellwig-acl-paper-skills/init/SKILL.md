---
name: init
description: Set up an ACL paper project for the acl-paper skills (literature folder, report.md, CLAUDE.md, Python env, checks).
disable-model-invocation: true
---

Prepare the current folder, which holds a paper written with the official ACL LaTeX template, for the other acl-paper skills. LaTeX setup is out of scope: the template is assumed to be there.

`PK` below means `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/paperkit.py`, run from the project root.

Ask the user every question in this skill; settle nothing by yourself. Existing files are extended, never overwritten.

## 1. Find the paper

Find `.tex` files that contain `\documentclass` and `\usepackage[...]{acl}`. One hit is the main file. Several hits: ask which. None: stop and say this plugin expects the ACL template (github.com/acl-org/acl-style-files).

## 2. pdftotext

Run `command -v pdftotext`. When it is missing, stop with ⚠️ and give the install command (macOS: `brew install poppler`, Debian/Ubuntu: `sudo apt install poppler-utils`, Windows: poppler via conda-forge or WSL). Re-check once the user says it is installed, then continue.

## 3. Python environment

The scripts for the literature sources run in a Python environment the user picks. Collect the candidates, then ask with AskUserQuestion:

- existing envs in the project (`.venv/`, `venv/`, `env/`)
- conda envs (`conda env list`, if conda exists)
- a new `uv` venv `.venv` in the project (offer only if `uv` exists, create only if picked)
- a path the user types

Resolve the choice to the interpreter's absolute path (`<env>/bin/python`) and confirm it runs (`<python> --version`, 3.10 or newer).

## 4. Packages

First settle the English variant. Run `PK detect-english --main-tex <main.tex>`: it counts American and British spellings in the existing text and returns a recommendation with its reason. Ask with AskUserQuestion, putting the recommended variant first with "(Recommended)" and the counts in its description (e.g. "British: 14 of 16 variant spellings, such as analyse, modelling"). Name mixed usage when both counts are above zero, since `proofread` will then flag the minority spellings.

Also ask, in the same AskUserQuestion round, whether the literature goes into git (check `git rev-parse --is-inside-work-tree`; outside a repo, still ask, since the project may become one or sync to Overleaf):

- `files` (Recommended): ignore `literature/pdf/` and `literature/md/`. Publishers' PDFs are often not redistributable and make the repo large; notes, index and `archive.bib` stay versioned, and `PK add` can re-fetch the papers.
- `all`: ignore the whole `literature/` folder, notes and archive included.
- `none`: version everything, for private repos where co-authors should get the PDFs too.

Also ask, in the same round, what the paper is submitted to; `guidelines-check`, `camera-ready`, `reviewer`, `rebuttal`, `revision` and `proofread` branch on it:

- `venue`: `acl-arr` (ACL, EMNLP, NAACL, ... via ARR) or `semeval` (a SemEval shared task; its rules and submission differ from ARR).
- `paper_type`: `long` or `short` for `acl-arr`; `semeval-system` or `semeval-task` for `semeval`.
- `stage`: `review` (the version for peer review) or `camera-ready` (accepted, final version). The `acl{...}` option in the main file hints at it.

Then run `PK init --python <python> --main-tex <main.tex> --english <us|uk> --gitignore <files|all|none> --venue <venue> --paper-type <type> --stage <stage>`. It writes `paper.config.json` (including `venue`, `paper_type`, `stage`), `literature/{pdf,md,notes}/`, `literature/archive.bib`, `literature/index.md` and `report.md`, keeping what exists.

Then run `PK doctor`. For each source with missing packages it prints the exact install command. Show it and ask before running it. (`acl-anthology` needs `typing_extensions` alongside; the command already lists it.)

Tell the user that the first ACL Anthology search downloads the Anthology metadata (about 300 MB, git clone) into `~/.cache/acl-paper/anthology`, shared by all projects. Offer to fetch it now with `PK anthology-update`.

## 5. Bib keys

Read the paper bib named in `paper.config.json`. Native keys are the source's own: ACL Anthology keys look like `hellwig-etal-2025-still`, arXiv keys like `vaswani2023attentionneed`. When existing entries follow another scheme, show three examples and ask which scheme new entries follow. Store the answer as `key_scheme` in `paper.config.json` (`native`, or a short description such as `AuthorYear like Smith2020`). Later skills apply it without asking again.

The template's `custom.bib` ships sample entries (`Aho:72`, ...). The first bib sync moves every uncited entry into `literature/archive.bib`; say so.

## 6. CLAUDE.md

No `CLAUDE.md`: copy `${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.md`. Existing one: add each missing section of the template (`Purpose`, `Project`, `Literature rules`, `Style`, `Terminology`) and leave the rest untouched.

Then fill `## Style`. Strongly recommend doing it now, because the `writing` and `proofread` skills read the user's own rules from there. Offer:

1. the example profile `${CLAUDE_PLUGIN_ROOT}/templates/style-profile.md`: show it, let the user drop or change rules, insert the rest
2. a short interview: British or American spelling, words they dislike, citation habits, caption and table conventions
3. leave it empty for now (say what that costs)

## 7. Finish

Run `PK sync` and `PK doctor`. Report what was created, the chosen environment, and any ⚠️ still open. Close with the next steps: `/acl-paper:proofread` for a first report, the `acl-anthology` and `arxiv` skills for literature, `/acl-paper:new-source` for further sources.
