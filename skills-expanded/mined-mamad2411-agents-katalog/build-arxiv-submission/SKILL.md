---
name: build-arxiv-submission
description: Build an arXiv submission zip from LaTeX source — copies tex, bib, sty, figures into a flat archive, fixes paths, verifies compilation via Docker + TeX Live. Portable across projects.
user-invocable: true
allowed-tools: Read, Bash
effort: medium
argument-hint: <input.tex> [output.zip]
---

# Build arXiv Submission

Package a LaTeX paper into a self-contained zip ready for arXiv upload. Copies source files, rewrites `\graphicspath` for the flat zip structure, and optionally verifies compilation via Docker + TeX Live.

**Portable:** Copy this entire directory to any project. Only your content (`.tex`, `.bib`, figures) is external.

## Contents

```
build-arxiv-submission/
  skill.md                    # This file
  scripts/
    build.sh                  # Bash build script
    build.ps1                 # PowerShell build script
```

## Prerequisites

- **Docker Desktop** (optional, for compilation verification) — `texlive/texlive:latest`

## Usage

```bash
# Bash (Git Bash / Linux / macOS)
bash <skill-dir>/scripts/build.sh <input.tex> [output.zip]

# PowerShell
powershell <skill-dir>/scripts/build.ps1 -TexFile <input.tex> [-OutputZip <output.zip>]
```

Replace `<skill-dir>` with the path to this skill directory in your project.

## How it works

1. Parses `\graphicspath` and `\bibliography` from the `.tex` file to discover dependencies
2. Finds all `.sty` files used via `\usepackage` that exist in the tex directory or project
3. Copies `.tex`, `.bib`, `.sty`, and all figures into a temp staging directory
4. Rewrites `\graphicspath` to `{figures/}` (flat zip-relative path)
5. If Docker is available and running, compiles the staged source to verify it builds cleanly
6. Zips the staging directory into the output archive
7. Reports file count and total size

## What goes into the zip

```
paper.tex              # main source (graphicspath rewritten)
references.bib         # bibliography (auto-detected from \bibliography{})
neurips_2024.sty       # style files (auto-detected from \usepackage{})
figures/               # all files from the original graphicspath directory
  fig1.png
  ...
```

## arXiv requirements

- arXiv compiles LaTeX server-side — submit source, not just PDF
- Figures: `.pdf`, `.png`, `.jpg` (pdflatex)
- Size: recommended <10 MB, hard limit 50 MB
- No page limit
- Submission guide: https://info.arxiv.org/help/submit/index.html
- LaTeX specifics: https://info.arxiv.org/help/submit_tex.html
