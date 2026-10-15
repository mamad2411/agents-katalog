---
name: submit-paper
description: Pre-submission checklist for LaTeX academic papers. Use when the user wants to submit a paper, check submission readiness, prepare camera-ready, switch to final mode, or verify a paper is ready for a conference deadline.
argument-hint: "[project-dir] [--venue <venue>] [--mode <anonymous|camera-ready|arxiv>] [--compile]"
allowed-tools: Read, Edit, Bash, Glob, Grep
---

# Submit Paper — Pre-Submission Checklist

Run a systematic readiness check on a LaTeX paper project before submitting to a conference. Covers submission mode, mandatory sections, drafting artifacts, bibliography, anonymity, and optional compilation.

---

## Step 1 — Locate the LaTeX project

// turbo
Find the paper directory:

```bash
# If we're inside a project-init project, look for paper/ sibling
git rev-parse --show-toplevel 2>/dev/null
ls "$(git rev-parse --show-toplevel 2>/dev/null)/../" 2>/dev/null || true

# Find main.tex
find . -maxdepth 3 -name "main.tex" 2>/dev/null | head -5
```

Determine `$PAPER_DIR` — the directory containing `main.tex`.

If `$ARGUMENTS` provides a path, use it directly.
If in a `project-init` project structure, check for `paper/` sibling.

---

## Step 2 — Ask for submission context

Ask the user **in a single message**:

1. **Submission type**: Initial submission (anonymous) / Camera-ready / arXiv preprint?
2. **Deadline**: When is the deadline? (helps prioritize what to fix)
3. **Compile check**: Should I run pdflatex to check compilation and page count? (adds ~30s)

If venue can be inferred from `venue_preamble.tex` (Step 3 will read it), skip asking.

Wait for the answer before proceeding.

---

## Step 3 — Run the check script

// turbo

```bash
bash <submit-paper-skill-dir>/scripts/check.sh "$PAPER_DIR" [--compile]
```

**Important**: Resolve `<submit-paper-skill-dir>` as the installed directory for this skill and use the absolute path to `check.sh`.

The script performs:
| Check | What it looks for |
|---|---|
| Project detection | `main.tex` present, venue from `venue_preamble.tex` |
| Drafting artifacts | `\todo`, `\fixme`, `\red{}`, author comment macros, TODO/FIXME text |
| Anonymity | Acknowledgements, funding disclosures, personal URLs/emails |
| Bibliography | `.bib` file non-empty, `\bibliography{}` call present |
| Mandatory sections | Venue-specific required sections (see below) |
| Abstract length | ~30–350 words (warns outside range) |
| Figures & tables | All `\label{fig:*}` and `\label{tab:*}` are `\ref`'d |
| Compilation | (opt) pdflatex + bibtex: page count, overfull boxes, undefined refs |

---

## Step 4 — Fix submission mode in venue_preamble.tex

After reading the script output, check `venue_preamble.tex` and verify the `\usepackage` option matches what the user said in Step 2.

**If the mode is wrong**, show the user what to change and offer to fix it:

| Submission type | venue_preamble.tex should contain |
|---|---|
| Initial / anonymous | e.g. `\usepackage{neurips_<year>}`, `\usepackage[review]{cvpr}`, or `\usepackage[review]{iccv}` |
| arXiv / preprint | e.g. `\usepackage[preprint]{neurips_<year>}` |
| Camera-ready | e.g. `\usepackage[final]{neurips_<year>}`, `\usepackage{cvpr}`, or `\usepackage{iccv}` |

Ask "Should I update `venue_preamble.tex` to `[mode]` mode?" — then edit if confirmed.

---

## Step 5 — Report findings and action plan

Present results in a structured format:

```
## Submission Readiness: <venue> — <mode>

### ✅ Passed (N)
- ...

### ⚠️ Warnings (N) — review before submitting
- ...

### ❌ Must Fix (N) — blocking submission
- ...

### Action Plan
1. <highest-priority fix>
2. ...
```

For each failure or warning, provide the **specific file and line** and the **exact fix**.

---

## Step 6 — Offer targeted fixes

For common failures, offer to fix them immediately:

- **Drafting artifacts**: Show the list; ask if you should remove them.
- **Missing mandatory sections**: Offer to create a placeholder that the user can fill in.
- **Wrong submission mode**: Offer to edit `venue_preamble.tex`.
- **Empty bib file**: Remind user to add references to `bib/refs.bib`.

Do **not** auto-fix without confirmation.

---

## Venue Reference: Mandatory Sections & Page Limits

| Venue | Deadline | Pages (main) | Mandatory extras |
|---|---|---|---|
| ICML | Jan | 9 | `sections/impact.tex` (Broader Impact) |
| ACL | Feb | 8 | `sections/limitations.tex` |
| ICCV | Mar (odd) | 8 | — |
| ECCV | Mar (even) | 14 total incl. figs | — |
| NeurIPS | May | 9 | `sections/impact.tex` + `sections/checklist.tex` |
| EMNLP | May | 8 | `sections/limitations.tex` |
| ICLR | Sep | ~9 (soft) | — |
| CVPR | Nov | 8 | — |
| NAACL | Dec | 8 | `sections/limitations.tex` |
| ACM | varies | varies | CCS concepts, `\acmConference` (camera-ready) |

**References and mandatory extras do not count toward page limits** (all venues listed above).

---

## Submission Mode Quick Reference

### NeurIPS
```latex
% Anonymous submission (default):
\usepackage{neurips_<year>}
% arXiv preprint:
\usepackage[preprint]{neurips_<year>}
% Camera-ready:
\usepackage[final]{neurips_<year>}
```

### ICML
```latex
\usepackage{icml<year>}           % anonymous
\usepackage[accepted]{icml<year>} % camera-ready
```

### ICLR
```latex
\usepackage[submitted]{iclr<year>_conference}  % anonymous
\usepackage[accepted]{iclr<year>_conference}   % camera-ready
```

### CVPR
```latex
\usepackage[review]{cvpr}   % anonymous
\usepackage{cvpr}           % camera-ready
\usepackage[pagenumbers]{cvpr}  % arXiv (shows page numbers)
```

### ICCV
```latex
\usepackage[review]{iccv}   % anonymous
\usepackage{iccv}           % camera-ready
\usepackage[pagenumbers]{iccv}  % arXiv (shows page numbers)
```

### ACL / EMNLP / NAACL
```latex
\usepackage[review]{acl}   % anonymous
\usepackage{acl}           % camera-ready
```

### ECCV
```latex
\usepackage{eccv}            % anonymous (blind review)
\usepackage[final]{eccv}     % camera-ready
```

---

## Camera-Ready Checklist (additional items)

When `--mode camera-ready` or submission type is camera-ready, additionally verify:

- [ ] `venue_preamble.tex` set to `[final]` / `[accepted]` mode
- [ ] Author names and affiliations filled in `main.tex`
- [ ] Acknowledgements added (funding, compute credits, etc.)
- [ ] All author comment macros removed (`\jieke{}`, `\jerry{}`, etc.)
- [ ] `sections/acknowledgement.tex` is non-empty
- [ ] Copyright / license statement added if required (ACM)
- [ ] Final bibliography formatted correctly (no "Anonymous" entries)
- [ ] Supplementary material packaged separately if required
- [ ] Source `.tex` files zipped and ready for upload (many venues require source)

---

## arXiv Submission Notes

arXiv has different packaging requirements from venue submission:

- Must submit `.tex` source (not just PDF)
- Flatten `\input{...}` if using many files (some arXiv setups require a single `.tex`)
- Switch to `[preprint]` mode (removes venue branding / anonymization)
- Include all `.sty`, `.bst`, `.cls` files in the zip
- Remove any `\usepackage{times}` if it causes font issues on arXiv
- arXiv compiles with an older TeX Live — check for package compatibility

---

## Example Invocations

```
/submit-paper                                   # check current directory
/submit-paper ~/Papers/my-neurips-paper         # check specific project
/submit-paper . --compile                       # include pdflatex check
/submit-paper . --mode camera-ready             # camera-ready checklist
```
