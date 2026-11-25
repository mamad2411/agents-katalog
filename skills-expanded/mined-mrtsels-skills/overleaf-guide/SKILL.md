---
name: overleaf-guide
description: "Use when working with Overleaf end-to-end: CLI/Git-bridge sync, multi-author collaboration, and compilation debugging."
metadata:
  openclaw:
    emoji: "💻"
    category: "tools"
    subcategory: "code-exec"
    keywords: ["Overleaf", "LaTeX", "CLI", "sync", "git", "collaboration", "academic writing"]
    source: "https://github.com/overleaf/overleaf"
---

# Overleaf End-to-End Guide

Trigger: Use this skill whenever a task involves Overleaf — creating or migrating a project, syncing via the Git bridge or overleaf-sync CLI, coordinating multi-author edits, or debugging compilations.

## Getting Started

### Create a Project

| Method | When to Use |
|--------|-------------|
| Blank project | Starting from scratch |
| Upload project | Migrating an existing local LaTeX project |
| Import from GitHub | Existing repo-based project |
| Use a template | Conference/journal submissions (IEEE, ACM, Springer, Elsevier templates available) |
| Copy from existing | Forking a previous project |

### Share and Set Permissions

| Role | Capabilities |
|------|-------------|
| Owner | Full control, can delete project, manage collaborators |
| Editor | Can edit all files, cannot manage collaborators |
| Viewer | Read-only, can download but not modify |

Share via **link sharing** (read-only or edit link; anyone with the link can access) or **email invitation** (role assignment per collaborator).

### Recommended Project Structure

```
project-root/
├── main.tex              # Main document (entry point)
├── preamble.tex          # Packages, macros, custom commands
├── sections/             # 01-introduction.tex ... 06-conclusion.tex
├── figures/              # fig1-overview.pdf, fig2-results.pdf, ...
├── tables/               # results-table.tex
├── references.bib        # Bibliography database
├── custom.sty            # Custom LaTeX macros
├── README.md             # Project notes (not compiled)
├── scripts/              # Local only — not synced to Overleaf
└── .gitignore
```

### Main File Setup

```latex
% main.tex
\documentclass[conference]{IEEEtran}  % or article, etc.
\input{preamble}  % load packages and macros

\begin{document}
\title{Your Paper Title}
\author{Author One \and Author Two \and Author Three}
\maketitle

\begin{abstract}
Your abstract here.
\end{abstract}

\input{sections/01-introduction}
\input{sections/02-related-work}
\input{sections/03-methods}
\input{sections/04-results}
\input{sections/05-discussion}
\input{sections/06-conclusion}

\bibliographystyle{IEEEtran}
\bibliography{references}
\end{document}
```

### .gitignore for CLI-Managed Projects

```gitignore
# LaTeX build artifacts
*.aux
*.bbl
*.blg
*.fdb_latexmk
*.fls
*.log
*.out
*.synctex.gz
*.toc

# Local scripts (don't sync to Overleaf)
scripts/

# OS files
.DS_Store
```

## Command-Line Sync: Git Bridge (paid plans)

Overleaf Server Pro and paid plans expose each project as a Git repository.

```bash
# Clone (the remote is pre-configured)
git clone https://git.overleaf.com/YOUR_PROJECT_ID my-paper
cd my-paper
git remote -v

# Daily workflow: pull → edit locally → push
git pull origin master
vim main.tex
git add -A
git commit -m "Revise methodology section"
git push origin master
```

**Credentials**: use your Overleaf email as username and an Overleaf-generated token as password.

### Conflict Resolution

```bash
git pull origin master
# 1. Open conflicted files (look for <<<<<<< markers)
# 2. Resolve LaTeX merge conflicts
# 3. Verify the document compiles
git add -A
git commit -m "Resolve merge conflict in results section"
git push origin master
```

### Overleaf + GitHub Sync

Overleaf Premium supports bidirectional GitHub sync: Menu > Sync > GitHub, link your GitHub account, select or create a repository, then pull/push changes between Overleaf and GitHub.

## Command-Line Sync: overleaf-sync (free plans)

For free Overleaf accounts without Git bridge access:

```bash
# Install
pip install overleaf-sync

# Login (stores credentials securely)
ols login

# List your projects
ols list

# Download a project
ols download "My Research Paper" --path ./my-paper

# Upload local changes
ols upload ./my-paper --project "My Research Paper"

# Two-way sync (pull then push)
ols sync ./my-paper --project "My Research Paper"
```

### Automated Sync Script

```bash
#!/bin/bash
# sync-overleaf.sh - run periodically or before/after editing sessions
PROJECT_DIR="$1"
PROJECT_NAME="$2"

echo "Pulling latest from Overleaf..."
ols download "$PROJECT_NAME" --path "$PROJECT_DIR" --skip-existing

echo "Compiling locally to verify..."
cd "$PROJECT_DIR"
latexmk -pdf -interaction=nonstopmode main.tex

if [ $? -eq 0 ]; then
    echo "Compilation successful. Pushing to Overleaf..."
    ols upload "$PROJECT_DIR" --project "$PROJECT_NAME"
else
    echo "Compilation failed. Fix errors before syncing."
    exit 1
fi
```

## Editor Integration

### VS Code (LaTeX Workshop)

```json
{
  "latex-workshop.latex.tools": [
    {
      "name": "latexmk",
      "command": "latexmk",
      "args": ["-pdf", "-interaction=nonstopmode", "%DOC%"]
    }
  ]
}
```

### Neovim (VimTeX)

```lua
-- init.lua
vim.g.vimtex_compiler_method = 'latexmk'
vim.g.vimtex_view_method = 'skim'  -- macOS
```

## Multi-Author Collaboration

1. **Assign sections**: each author owns specific `.tex` files to minimize merge conflicts.
2. **Use comments**: Overleaf supports inline comments (`% TODO: revise this paragraph`) and threaded review comments.
3. **Use author-specific annotation commands**:

```latex
% In preamble.tex, define author-specific annotation commands
\usepackage{xcolor}
\newcommand{\alice}[1]{\textcolor{blue}{[Alice: #1]}}
\newcommand{\bob}[1]{\textcolor{red}{[Bob: #1]}}
\newcommand{\todo}[1]{\textcolor{orange}{[TODO: #1]}}

% In text:
This result is surprising \alice{Should we add more analysis here?}
and warrants further investigation \todo{Add statistical test}.
```

4. **Track changes**: Overleaf Premium includes a track-changes mode; for free plans use the `changes` package:

```latex
\usepackage{changes}
\definechangesauthor[name={Alice}, color=blue]{AL}
\definechangesauthor[name={Bob}, color=red]{BO}

% Usage:
\added[id=AL]{This is new text added by Alice.}
\deleted[id=BO]{This text was removed by Bob.}
\replaced[id=AL]{new text}{old text}
```

## Compilation and Debugging

Compile locally to verify before syncing: `latexmk -pdf -interaction=nonstopmode main.tex`.

### Common Compilation Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Undefined control sequence` | Missing package or typo in command | Check `\usepackage` or spelling |
| `Missing $ inserted` | Math symbol outside math mode | Wrap in `$...$` or `\text{...}` |
| `File not found` | Incorrect path in `\input` or `\includegraphics` | Check names — case-sensitive on Overleaf |
| `Overfull \hbox` | Content too wide for column | Resize figure, adjust text, or add `\sloppy` |
| `Citation undefined` | BibTeX entry missing or key mismatch | Verify `.bib` key matches `\cite{}` |

### Debugging Tips

- Use **Recompile from scratch** (Ctrl+Shift+Enter) to clear the cache.
- Check the **Logs and output files** panel for detailed error messages.
- Add `\listfiles` to the preamble to see which packages are loaded.
- Overleaf uses TeX Live 2024; check package compatibility if using older templates.

## Automation Workflows

### Auto-Update Bibliography from Zotero

```python
import subprocess
from pathlib import Path

def sync_bibliography(zotero_lib_id, bib_file, project_dir):
    """Export Zotero library and sync to Overleaf project."""
    # Export from Zotero using Better BibTeX
    subprocess.run([
        "curl", "-s",
        f"http://localhost:23119/better-bibtex/export/library?/"
        f"{zotero_lib_id}/library.biblatex",
        "-o", str(Path(project_dir) / bib_file)
    ])
    print(f"Updated {bib_file} from Zotero library {zotero_lib_id}")
```

### Auto-Regenerate Figures from Data

```python
import subprocess
from pathlib import Path

def regenerate_figures(scripts_dir, figures_dir):
    """Run all figure generation scripts and update outputs."""
    scripts = sorted(Path(scripts_dir).glob("fig_*.py"))
    for script in scripts:
        print(f"Running {script.name}...")
        subprocess.run(["python", str(script)], cwd=figures_dir)
    print(f"Regenerated {len(scripts)} figures in {figures_dir}")
```

### CI/CD PDF Compilation

```yaml
# .github/workflows/compile-paper.yml
name: Compile LaTeX Paper
on:
  push:
    branches: [main]
    paths: ['**.tex', '**.bib', '**.sty']
jobs:
  compile:
    runs-on: ubuntu-latest
    container:
      image: texlive/texlive:latest
    steps:
      - uses: actions/checkout@v4
      - name: Compile PDF
        run: latexmk -pdf -interaction=nonstopmode main.tex
      - name: Upload PDF
        uses: actions/upload-artifact@v4
        with:
          name: paper-pdf
          path: main.pdf
      - name: Check for warnings
        run: grep -i "warning" main.log | grep -v "Font" || true
```

## Submission Workflow

1. **Flatten the project** if the journal requires a single `.tex` file: `latexpand main.tex > submission.tex`
2. **Check formatting**: page limits, font sizes, margin requirements.
3. **Download as zip**: Menu > Download > Source to get all files.
4. **Convert figures**: ensure all figures are in accepted formats (PDF, EPS, or high-res PNG/TIFF).
5. **Clean up**: remove TODO comments, author annotation commands, and debug code:

```latex
% Add to preamble for submission: disable all annotation commands
\renewcommand{\alice}[1]{}
\renewcommand{\bob}[1]{}
\renewcommand{\todo}[1]{}
```

## Keyboard Shortcuts

| Action | Mac | Windows |
|--------|-----|---------|
| Compile | Cmd+Enter | Ctrl+Enter |
| Bold / Italic | Cmd+B / Cmd+I | Ctrl+B / Ctrl+I |
| Comment toggle | Cmd+/ | Ctrl+/ |
| Find & replace | Cmd+H | Ctrl+H |
| Go to line | Cmd+Shift+L | Ctrl+Shift+L |
| Toggle PDF | Cmd+Shift+O | Ctrl+Shift+O |

## Pitfalls

- Git push rejected → Pull first, resolve conflicts, then push.
- Sync tool authentication error → Re-run `ols login`, check 2FA settings.
- Compilation differs locally vs Overleaf → Match TeX Live versions; Overleaf uses TeX Live 2024.
- Binary files (images) cause large diffs → Use `.gitattributes` to mark them as binary.
- Overleaf rate limiting → Add delays between API calls; prefer the Git bridge when available.
- File not found on Overleaf but not locally → File names are case-sensitive on Overleaf; check `\input`/`\includegraphics` paths.
- `<<<<<<<` conflict markers left in the document → Resolve conflicts before compiling, then verify the document compiles.
- Citation renders as `?` in PDF → BibTeX entry missing or key mismatch; verify `.bib` key matches `\cite{}`.

## References

- Overleaf Git integration: https://www.overleaf.com/learn/how-to/Git_integration
- overleaf-sync: https://github.com/moritzgloeckl/overleaf-sync
- LaTeX Workshop (VS Code): https://github.com/James-Yu/LaTeX-Workshop
- latexmk documentation: https://mg.readthedocs.io/latexmk.html
