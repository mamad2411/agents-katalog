---
name: write-iut-thesis
description: Draft, expand, revise, structure, and maintain a full Islamic University of Technology BSc thesis from source documents using the local iutbscthesis LaTeX template. Use when writing or editing thesis metadata, front matter, abstract, chapters, related works, methodology, results, discussion, conclusion, citations, appendices, figures, tables, code listings, or compile guidance for main.tex. Also use when the user expects an AI agent to turn papers, notes, PDFs, LaTeX sources, bib files, data tables, and assets into a substantial thesis manuscript chapter by chapter without requiring repeated babysitting.
---

# Write IUT Thesis

Use this skill to write thesis content that fits an Islamic University of Technology BSc thesis template while also behaving like an agentic thesis-writing workflow. The skill governs both formatting and the practical process of turning source material into a full thesis book.

## Operating Principle

Do not merely make a template-valid short draft. Build the thesis deliberately from the user's source documents. A thesis chapter should normally be more expansive than the corresponding paper section because it must explain motivation, background, definitions, design choices, assumptions, evidence, interpretation, limitations, and links to the overall thesis claim.

When source papers are available, treat them as ground truth. Extract, reorganize, and expand from them; do not compress them into a superficial summary unless the user explicitly asks for brevity.

## 0. Template Bootstrap — Fetch the Unwritten Template (Required First Step)

The authoritative unwritten IUT thesis template lives in the `Template/` (also referred to as `template/`) folder of this repository:

```
https://github.com/sakhadib/IUT-Thesis-Skill-for-AI.git
```

That folder (`Template/main.tex`, `Template/iutbscthesis.cls`, `Template/frontmatter.sty`, `Template/personnelhandler.sty`, `Template/citations.bib`, `Template/ImageA.png` etc.) is essential to start writing. Do not invent a template or ask the user to provide one if it is missing — fetch it.

### Procedure for the AI agent (execute via bash/powershell — do not ask user to do it manually)

1. **Check if the template is already present.** Look for `Template/main.tex` (or `template/main.tex`) and `iutbscthesis.cls` in the current workspace:
   ```bash
   ls -la Template/ 2>/dev/null || ls -la template/ 2>/dev/null || echo "TEMPLATE_MISSING"
   test -f Template/main.tex && test -f Template/iutbscthesis.cls && echo "TEMPLATE_OK" || echo "TEMPLATE_INCOMPLETE"
   test -f main.tex && test -f iutbscthesis.cls && echo "ROOT_TEMPLATE_OK" || true
   ```
   If any of these checks shows the template is present (either in `Template/` or in the workspace root), use that copy as ground truth and skip fetching.

2. **Detect OS and available fetch tools.** The user may be on Windows, macOS, or any Linux distro, and may not have `git` installed. Detect before fetching:
   ```bash
   # Tool availability
   command -v git >/dev/null 2>&1 && echo "git: $(git --version)" || echo "git: MISSING"
   command -v curl >/dev/null 2>&1 && echo "curl: OK" || echo "curl: MISSING"
   command -v wget >/dev/null 2>&1 && echo "wget: OK" || echo "wget: MISSING"
   command -v gh >/dev/null 2>&1 && echo "gh: OK" || echo "gh: MISSING"
   command -v python3 >/dev/null 2>&1 && echo "python3: OK" || echo "python3: MISSING"
   command -v tar >/dev/null 2>&1 && echo "tar: OK" || echo "tar: MISSING"
   command -v unzip >/dev/null 2>&1 && echo "unzip: OK" || echo "unzip: MISSING"

   # OS / distro detection
   uname -a 2>/dev/null; echo "---"
   cat /etc/os-release 2>/dev/null || cat /etc/lsb-release 2>/dev/null || sw_vers 2>/dev/null || echo "OS: unknown"
   echo "WSL: $(grep -qi microsoft /proc/version 2>/dev/null && echo yes || echo no)"
   command -v apt >/dev/null 2>&1 && echo "pkg: apt (Debian/Ubuntu/Mint/Pop!_OS)"
   command -v apt-get >/dev/null 2>&1 && echo "pkg: apt-get (Debian/Ubuntu)"
   command -v dnf >/dev/null 2>&1 && echo "pkg: dnf (Fedora/RHEL 8+/CentOS 8+/Rocky/Alma)"
   command -v yum >/dev/null 2>&1 && echo "pkg: yum (RHEL/CentOS 7)"
   command -v pacman >/dev/null 2>&1 && echo "pkg: pacman (Arch/Manjaro/EndeavourOS)"
   command -v zypper >/dev/null 2>&1 && echo "pkg: zypper (openSUSE)"
   command -v apk >/dev/null 2>&1 && echo "pkg: apk (Alpine)"
   command -v brew >/dev/null 2>&1 && echo "pkg: brew (macOS/Linuxbrew)"
   command -v winget >/dev/null 2>&1 && echo "pkg: winget (Windows 10/11)"
   command -v choco >/dev/null 2>&1 && echo "pkg: choco (Windows)"
   command -v scoop >/dev/null 2>&1 && echo "pkg: scoop (Windows)"
   powershell.exe -Command "Write-Host 'powershell: OK'" 2>/dev/null || pwsh -Command "Write-Host 'pwsh: OK'" 2>/dev/null || echo "powershell: not-detected (likely not Windows)"
   ```

3. **If template is missing, fetch it — use the first available method (git is preferred but not required).**

   **3a. If `git` is available — shallow clone (fastest, all OS):**
   ```bash
   if [ ! -d "Template" ] && [ ! -f "main.tex" ]; then
     git clone --depth 1 https://github.com/sakhadib/IUT-Thesis-Skill-for-AI.git /tmp/iut-thesis-skill-tmp
     mkdir -p Template
     cp -r /tmp/iut-thesis-skill-tmp/Template/* Template/ 2>/dev/null || cp -r /tmp/iut-thesis-skill-tmp/template/* Template/ 2>/dev/null || true
     [ -f "Template/main.tex" ] && [ ! -f "main.tex" ] && cp Template/main.tex ./ 2>/dev/null || true
     [ -f "Template/iutbscthesis.cls" ] && [ ! -f "iutbscthesis.cls" ] && cp Template/iutbscthesis.cls ./ 2>/dev/null || true
     rm -rf /tmp/iut-thesis-skill-tmp
   fi
   ls -la Template/
   ```

   **3b. If `git` is MISSING — do NOT block. Try git-less archive download immediately (works on Linux/macOS/WSL/Git-Bash):**
   ```bash
   # curl path (most common)
   if ! command -v git >/dev/null 2>&1; then
     mkdir -p /tmp/iut-thesis-skill-tmp
     if command -v curl >/dev/null 2>&1; then
       curl -L https://github.com/sakhadib/IUT-Thesis-Skill-for-AI/archive/refs/heads/main.tar.gz | tar -xz -C /tmp/iut-thesis-skill-tmp --strip-components=1
     elif command -v wget >/dev/null 2>&1; then
       wget -qO- https://github.com/sakhadib/IUT-Thesis-Skill-for-AI/archive/refs/heads/main.tar.gz | tar -xz -C /tmp/iut-thesis-skill-tmp --strip-components=1
     elif command -v python3 >/dev/null 2>&1; then
       python3 -c "import urllib.request, tarfile, io; data=urllib.request.urlopen('https://github.com/sakhadib/IUT-Thesis-Skill-for-AI/archive/refs/heads/main.tar.gz').read(); tarfile.open(fileobj=io.BytesIO(data), mode='r:gz').extractall('/tmp/iut-thesis-skill-tmp')"
       # python tar extracts with top-level folder; strip it
       if [ -d /tmp/iut-thesis-skill-tmp/IUT-Thesis-Skill-for-AI-main ]; then mv /tmp/iut-thesis-skill-tmp/IUT-Thesis-Skill-for-AI-main/* /tmp/iut-thesis-skill-tmp/ 2>/dev/null; fi
     else
       echo "No curl/wget/python3 available for download"
     fi
     if [ -d /tmp/iut-thesis-skill-tmp/Template ]; then
       mkdir -p Template
       cp -r /tmp/iut-thesis-skill-tmp/Template/* Template/ 2>/dev/null || cp -r /tmp/iut-thesis-skill-tmp/template/* Template/ 2>/dev/null || true
       [ -f "Template/main.tex" ] && [ ! -f "main.tex" ] && cp Template/main.tex ./ 2>/dev/null || true
       [ -f "Template/iutbscthesis.cls" ] && [ ! -f "iutbscthesis.cls" ] && cp Template/iutbscthesis.cls ./ 2>/dev/null || true
     fi
     rm -rf /tmp/iut-thesis-skill-tmp
     ls -la Template/ 2>/dev/null || echo "TEMPLATE_FETCH_FAILED"
   fi
   ```

   **3c. Windows PowerShell fallback (when bash/curl not available but PowerShell is):**
   ```powershell
   # Run in PowerShell / pwsh if bash tools are missing (Windows native)
   if (-not (Test-Path Template/main.tex)) {
     $zipUrl = "https://github.com/sakhadib/IUT-Thesis-Skill-for-AI/archive/refs/heads/main.zip"
     $tmpZip = "$env:TEMP\iut-thesis-skill-tmp.zip"
     $tmpDir = "$env:TEMP\iut-thesis-skill-tmp"
     if (Get-Command Invoke-WebRequest -ErrorAction SilentlyContinue) {
       Invoke-WebRequest -Uri $zipUrl -OutFile $tmpZip
     } elseif (Get-Command curl.exe -ErrorAction SilentlyContinue) {
       curl.exe -L $zipUrl -o $tmpZip
     } elseif (Get-Command wget -ErrorAction SilentlyContinue) {
       wget $zipUrl -O $tmpZip
     }
     if (Test-Path $tmpZip) {
       Expand-Archive -Path $tmpZip -DestinationPath $tmpDir -Force
       $extracted = Get-ChildItem $tmpDir | Select-Object -First 1
       $src = Join-Path $extracted.FullName "Template"
       if (-not (Test-Path $src)) { $src = Join-Path $extracted.FullName "template" }
       if (Test-Path $src) {
         New-Item -ItemType Directory -Force -Path Template | Out-Null
         Copy-Item -Path "$src/*" -Destination Template -Recurse -Force
       }
       Remove-Item $tmpZip -Force -ErrorAction SilentlyContinue
       Remove-Item $tmpDir -Recurse -Force -ErrorAction SilentlyContinue
     }
   }
   Get-ChildItem Template | Format-Table
   ```

   **3d. `gh` CLI alternative (if installed):**
   ```bash
   gh repo clone sakhadib/IUT-Thesis-Skill-for-AI /tmp/iut-thesis-skill-tmp -- --depth 1
   mkdir -p Template && cp -r /tmp/iut-thesis-skill-tmp/Template/* Template/ && rm -rf /tmp/iut-thesis-skill-tmp
   ```

4. **Optionally install `git` if user wants it (non-blocking — do not require git to proceed).** Only attempt if the git-less download above failed or user explicitly asks for git. Detect OS first, then offer/run:

   **Debian / Ubuntu / Mint / Pop!_OS / WSL-Ubuntu:**
   ```bash
   sudo apt update && sudo apt install -y git curl wget ca-certificates
   ```

   **Fedora / RHEL / CentOS / Rocky / Alma:**
   ```bash
   # Fedora 22+ / RHEL 8+
   sudo dnf install -y git curl wget ca-certificates
   # RHEL/CentOS 7 fallback
   sudo yum install -y git curl wget ca-certificates
   ```

   **Arch / Manjaro / EndeavourOS:**
   ```bash
   sudo pacman -Sy --needed git curl wget ca-certificates
   ```

   **openSUSE (Leap/Tumbleweed):**
   ```bash
   sudo zypper install -y git curl wget ca-certificates
   ```

   **Alpine:**
   ```bash
   sudo apk add git curl wget ca-certificates
   ```

   **macOS:**
   ```bash
   # Option 1: Xcode CLT (no Homebrew needed)
   xcode-select --install
   # Option 2: Homebrew
   brew update && brew install git curl wget
   # Option 3: MacPorts
   # sudo port install git
   ```

   **Windows:**
   ```powershell
   # Option 1: winget (Windows 10/11)
   winget install --id Git.Git -e --source winget
   # Option 2: Chocolatey
   choco install git -y
   # Option 3: Scoop
   scoop install git
   # Option 4: Manual — download Git for Windows from https://git-scm.com/download/win
   ```

   After installing git, retry the `git clone` command in 3a. If install fails (no admin/sudo, managed device), fall back to the git-less archive methods in 3b/3c — never block thesis writing on git.

5. **Verify after fetch.** Confirm `Template/main.tex`, `Template/iutbscthesis.cls`, `Template/frontmatter.sty`, and `Template/personnelhandler.sty` exist. If the user's project already has a `main.tex` elsewhere, do not overwrite it — keep the fetched `Template/` as reference and copy only missing class/style files into the project root when needed.

6. **If all automated fetch fails** (no network, no git/curl/wget/python/powershell, or blocked download), tell the user to manually obtain the template by ONE of these (ordered by OS):
   - **With git (any OS):** `git clone https://github.com/sakhadib/IUT-Thesis-Skill-for-AI.git` then copy `Template/` into workspace.
   - **Without git — browser download:** open `https://github.com/sakhadib/IUT-Thesis-Skill-for-AI` → Code → Download ZIP → unzip → copy `Template/` folder into workspace.
   - **Without git — CLI (Linux/macOS/WSL):** `curl -L https://github.com/sakhadib/IUT-Thesis-Skill-for-AI/archive/refs/heads/main.zip -o thesis.zip && unzip thesis.zip && cp -r IUT-Thesis-Skill-for-AI-main/Template ./`
   - **Without git — PowerShell (Windows):** `Invoke-WebRequest -Uri https://github.com/sakhadib/IUT-Thesis-Skill-for-AI/archive/refs/heads/main.zip -OutFile thesis.zip; Expand-Archive thesis.zip -DestinationPath .; Copy-Item IUT-Thesis-Skill-for-AI-main\Template -Destination Template -Recurse`
   Do not proceed to invent thesis structure without the real template.

## First Checks

- Ensure the template bootstrap above has succeeded — `Template/main.tex` (or `main.tex` at workspace root) must exist before drafting.
- Read `main.tex` before editing or drafting so local chapter names, labels, bibliography keys, and project conventions stay intact.
- Read the relevant chapter files before editing so numbering, labels, citations, and narrative continuity are preserved.
- Inspect all available source material before writing substantive content — including `Papers/`, `assets/`, `data/`, `figures/`, `chapters/`, bibliography files, and any user-provided `PDF`, `DOCX`, `TXT`, `PPT`/`PPTX` (slides, drafts, reports). Assume the user may have *only* PDFs/Office files and no extracted figures, tables, or `.tex` sources.
- Treat `iutbscthesis.cls`, `frontmatter.sty`, and `personnelhandler.sty` as the source of truth for supported commands.
- Preserve the template structure unless the user explicitly asks for a structural change.
- Do not leave instructional filler, placeholder text, sample chapters, `TBD`, or `TODO` in final thesis-facing content.
- Prefer academic prose with clear claims, evidence, citations, and transitions.

## Source Format Handling — PDF / DOCX / TXT / PPT and Figure/Table Extraction

Users may provide their work in any form — `PDF`, `DOCX`, `TXT`, `PPT`/`PPTX`, scanned reports, or mixed folders — and may have no separate figures, tables, or `.tex` sources. The AI must handle all of these directly; never require the user to pre-extract or provide `.tex`.

**Detection (run via bash, do not ask user to convert manually):**
```bash
# List potential sources — incl. Office formats and case variants
find . -type f \( -iname "*.pdf" -o -iname "*.docx" -o -iname "*.doc" -o -iname "*.txt" -o -iname "*.pptx" -o -iname "*.ppt" -o -iname "*.tex" -o -iname "*.bib" -o -iname "*.md" -o -iname "*.csv" \) | head -n 100
ls -R Papers/ 2>/dev/null; ls -R figures/ 2>/dev/null; ls -R assets/ 2>/dev/null; ls -R data/ 2>/dev/null
```

**Reading & extraction — try in this order, fall back gracefully:**
- **PDF:** Use the `Read` tool’s PDF mode first (it returns text + page images). If the PDF is scanned or text extraction is poor, fall back to `pdftotext` / `python3 -m fitz` (PyMuPDF) / `pdfminer`:
  ```bash
  pdftotext -layout "Papers/paper.pdf" - | head -n 300
  python3 -c "import fitz; d=fitz.open('Papers/paper.pdf'); print(d[0].get_text())"
  # Extract embedded images to figures/
  python3 -c "import fitz, pathlib; d=fitz.open('Papers/paper.pdf'); pathlib.Path('figures/extracted').mkdir(parents=True, exist_ok=True); [open(f'figures/extracted/fig_p{p}_i{i}.png','wb').write(img[4]) for p in range(len(d)) for i,img in enumerate(d[p].get_images())]"
  ```
- **DOCX/DOC:** Try `Read` tool, else `pandoc` or `python3-docx`:
  ```bash
  pandoc "Report.docx" -t plain | head -n 400
  python3 -c "import docx; d=docx.Document('Report.docx'); print('\n'.join(p.text for p in d.paragraphs[:80])); [print(t.text) for t in d.tables[:2]]"
  ```
- **PPT/PPTX:** Try `Read` tool, else `python-pptx` or export to PDF then read:
  ```bash
  python3 -c "import pptx; prs=pptx.Presentation('Slides.pptx'); print('\n'.join(s.text for s in prs.slides[0].shapes if s.has_text_frame))"
  # Alternative: libreoffice --headless --convert-to pdf Slides.pptx 2>/dev/null && pdftotext -layout Slides.pdf -
  ```
- **TXT/MD/CSV:** Read directly with `Read` tool; treat as ground truth for plain-text contributions.

**Figures & tables when only PDFs/Office files exist:**
- Assume figures and tables are *embedded* in the PDF/slides and not yet extracted. Re-extract them: save embedded images from PDFs to `figures/extracted/` (as above), screenshot or export slide images, and re-type tables faithfully into `booktabs` LaTeX (`\toprule`/`\midrule`/`\bottomrule`) preserving every number and caption.
- If an image is low-resolution/scanned, keep it as-is and note the source page/slide in the caption (e.g., `Source: Paper.pdf p.4, Fig.2`). Do not redraw or invent data.
- If table extraction is uncertain (merged cells, OCR noise), transcribe conservatively and add a brief `% TODO: verify vs. p.X` comment in the `.tex` only if blocking; otherwise ask the user to confirm the specific cell.
- Every extracted figure/table must be referenced in prose with `\autoref{...}` and given a descriptive label (`fig:`, `tab:`).

If the user has only PDFs/Office files, treat the extracted text + re-extracted figures/tables as ground truth for that chapter. Prefer extraction over asking the user to do manual conversion.

## Agentic Thesis-Building Workflow

For any request to write a chapter, expand a chapter, merge papers into a thesis, or continue the thesis book:

1. **Inventory the evidence first.** Read the source paper sections, appendices, tables, figures, datasets, code, bib entries, and existing chapter material relevant to the requested chapter. Handle *any* format the user provides — `PDF`, `DOCX`, `TXT`, `PPT`/`PPTX` included — using the Source Format Handling procedure above. If `.tex`/`.bib`/`.md` is available it is easier to cite, but if the user has only PDFs/Office files, extract text, figures and tables from those files and treat the extraction as ground truth.
2. **Make a chapter coverage map.** Identify every source element that belongs in the chapter: claims, definitions, research questions, methods, equations, algorithms, prompts, datasets, models, tables, plots, limitations, and results. Decide what belongs elsewhere so the chapter does not duplicate earlier content.
3. **Write expansively by default.** Expand each source element into thesis prose that explains why it matters, how it was produced, what assumptions it carries, and how it supports the thesis argument. Avoid one-paragraph collapse of multi-page paper sections.
4. **Use figures and tables proactively.** Include relevant source figures, diagrams, heatmaps, charts, algorithms, and result tables when they support the chapter. Refer to each with `\autoref{...}` before or near placement.
5. **Preserve traceability.** Every substantive empirical claim must be tied to a cited source, a local table, a figure, an equation, a dataset description, or a previously reported result. Do not invent numbers, model lists, dataset sizes, prompts, or conclusions.
6. **Build chapter by chapter.** Add or revise one chapter at a time unless asked for a whole-book pass. Include the chapter in `main.tex` only when it is ready to compile.
7. **Verify after editing.** Compile when practical, inspect log errors, and fix LaTeX/reference failures introduced by the edit. See LaTeX Environment Setup below for install/compile handling.

## Expansion Norms

When the user says "write", "expand", "make it detailed", "use the papers", or asks for a thesis chapter, assume they want a substantial thesis treatment:

- Introduce the problem and motivation before technical details.
- Define terms before using them as results.
- Explain methodology sequentially enough that another researcher can reproduce the work.
- Include equations, algorithms, prompts, and pipelines when they are part of the source work.
- Report important result tables rather than paraphrasing them away.
- Discuss figures in the text, not just as decorations.
- Connect each subsection back to the chapter's role in the thesis.
- End major result sections with interpretation, not only numbers.
- State limitations and scope boundaries where the evidence requires them.

Do not take the short path just because the user did not specify length. If the source material is large, the thesis chapter should reflect that size.

## No-Hallucination Rules

- Papers, source `.tex`, datasets, code, and user-provided notes beat secondary summaries.
- If a summary file conflicts with the source paper, follow the source paper and mention the conflict only if relevant.
- If a number, prompt, model name, or dataset detail cannot be verified locally, do not fabricate it. Search the repo first; ask the user or mark the gap only if it blocks the chapter.
- Preserve exact model names, metric names, and dataset sizes when the source gives them.
- Do not merge incompatible axes or instruments without explaining the mapping and its limits.
- Do not attribute a result to a study that did not produce it.

## Template Contract

Use `\documentclass{iutbscthesis}` and keep bibliography resources in the preamble when bibliography is required.

Required metadata before `\begin{document}`:

```latex
\title{Title of the Thesis}
\addauthor{Name}{Student ID}
\supervisor{Name}{Designation}{Department}
\department{Department of Computer Science and Engineering}
\program{BACHELOR OF SCIENCE IN COMPUTER SCIENCE AND ENGINEERING}
\defensedate{DD}{Month}{YYYY}
```

Rules:

- Use one and only one `\supervisor{...}{...}{...}`.
- Use one `\addauthor{...}{...}` per student.
- Use `\addcosupervisor{...}{...}{...}` only when co-supervisors exist.
- Do not put commas inside author, supervisor, or co-supervisor name/designation/department arguments because `personnelhandler.sty` uses comma-separated internal lists.
- Keep `\defensedate` as three arguments: day, month name, year.

## Front Matter Order

Keep front matter in this order unless the local template or user explicitly requires a change:

```latex
\coverpage
\pagenumbering{roman}
\titlepage
\declarationofcandidate
\dedicatedto{...}
\tableofcontents
\listoffigures
\listoftables
\clearpage
\begin{abbreviations}
  \abbr{ABC}{Expanded Term}
\end{abbreviations}
\begin{acknowledgement}
...
\end{acknowledgement}
\begin{abstract}
...
\end{abstract}
\pagenumbering{arabic}
```

Front matter norms:

- Write acknowledgements formally and specifically. Include supervisors, co-supervisors, collaborators, family, tools, funding, lab support, department, and institution when verified or requested.
- Write the abstract as one compact summary covering context, problem, method, results, and conclusion.
- Keep abbreviations alphabetized when practical and define only terms used in the thesis.

## Chapter Norms

A normal thesis body often includes:

1. `Introduction`
2. `Related Works`
3. `Data and Models` or `Background`
4. `Methodology` / study chapters
5. `Results`
6. `Discussion`
7. `Conclusion`

Adapt chapter names to the repository's existing structure. Do not force a five-chapter generic outline onto a thesis whose evidence requires more chapters.

### Introduction

Introduce the topic for readers outside the immediate research area. Define key terms early. Explain motivation, practical relevance, research gap, problem statement, objectives, contributions, scope, and thesis organization. Use teaser figures when the source work has strong visual anchors.

### Related Works

Make this a large synthesis chapter when the source bibliography is large. Group prior work by theme, method, dataset, limitation, or debate. Compare studies, show disagreements, connect them to the thesis gap, and end by motivating the methodology. Do not produce an annotated list.

### Data And Models / Background

Document datasets, instruments, statement lists, model cohorts, coordinate systems, preprocessing, projection models, and implementation assumptions. Include source statement lists, diagrams, and algorithms when they are necessary for reproducibility.

### Methodology

Explain the complete approach sequentially. For each component, state role, input, output, method, theoretical basis, implementation choices, alternatives considered, and justification. Include equations, algorithms, prompts, and pipeline diagrams when used by the research.

### Results

Report raw and summarized results clearly in tables and figures. Interpret how each result answers the research questions. Include major appendix results from papers when those results are necessary for the thesis argument.

### Discussion

Synthesize across chapters. Explicitly state each thesis-level claim and support it with earlier experiments, data, tables, figures, equations, or cited literature. Discuss implications, limitations, threats to validity, and what the thesis proposes.

### Conclusion

Restate objectives and research questions, summarize key findings, explain contributions, acknowledge limitations, suggest future work, and end with a clear final statement. Do not overclaim beyond the evidence.

## Figures, Tables, Algorithms, Listings

- Refer to every figure and table in the text before or near its placement, using `\autoref{...}` where possible.
- Use descriptive labels such as `fig:architecture`, `tab:metrics`, `alg:projection`, and `lst:preprocessing`.
- Use `[H]` only when fixed placement is genuinely needed; otherwise use standard float placement.
- Tables use `booktabs` style when possible: `\toprule`, `\midrule`, `\bottomrule`.
- The template configures table captions on top and figure captions below; follow that convention.
- Use `subfigure` for grouped images and label both the group and meaningful subfigures.
- Use `algorithm`/`algpseudocode` for important algorithms when the template loads them.
- Use `lstlisting` for short code excerpts only when code itself is part of the argument.

## Citations

- Use `biblatex` commands already supported by the template: `\cite`, `\textcite`, `\parencite`, `\footcite`, and `\textcites`.
- Keep bibliography entries in `.bib` resources already used by `main.tex`.
- Cite claims about prior work, datasets, algorithms, external facts, and source-paper methods.
- Use multi-citations for grouped related evidence, e.g. `\cite{key1,key2,key3}`.
- If adding a citation key, verify it exists in an active `.bib` file or add a complete entry from a reliable source.
- Print references with `\printbib` in the back matter unless the template uses a different command.

## Language Rules

- Use precise academic language, active voice where natural, and concrete claims.
- Prefer "we" when the existing thesis uses it.
- Avoid generic filler such as "this is very important" unless the sentence states why.
- Avoid starting every related-work paragraph with author names; begin from the concept, gap, method, or finding.
- Use transition phrases to connect chapters and studies.
- Use `\emph{...}` for emphasis sparingly.
- Use `\verb|...|` or `\texttt{...}` only for packages, commands, filenames, code identifiers, or literal technical tokens.
- Use correct punctuation for hyphen, en dash, and em dash in prose.

## LaTeX Environment Setup & Compile Guidance

The class loads `stix2`, `biblatex` with `backend=biber`, and other CTAN packages. Compilation requires a working LaTeX distribution. The agent must handle three cases: LaTeX is present, LaTeX is missing but installable, LaTeX is missing and user declines install.

### 1. Detect OS and whether LaTeX is installed

Run detection before attempting to compile (use bash tool — do not ask user to run manually):

```bash
# Detect LaTeX tools
command -v pdflatex >/dev/null 2>&1 && echo "pdflatex: $(pdflatex --version | head -n1)" || echo "pdflatex: MISSING"
command -v xelatex  >/dev/null 2>&1 && echo "xelatex: $(xelatex --version | head -n1)"  || echo "xelatex: MISSING"
command -v biber    >/dev/null 2>&1 && echo "biber: $(biber --version | head -n1)"      || echo "biber: MISSING"
command -v latexmk  >/dev/null 2>&1 && echo "latexmk: OK" || echo "latexmk: MISSING"

# Detect OS / environment
uname -a
cat /etc/os-release 2>/dev/null || cat /etc/lsb-release 2>/dev/null || sw_vers 2>/dev/null || echo "OS: unknown"
echo "WSL: $(grep -qi microsoft /proc/version 2>/dev/null && echo yes || echo no)"
command -v apt >/dev/null 2>&1 && echo "pkg: apt (Debian/Ubuntu)"
command -v dnf >/dev/null 2>&1 && echo "pkg: dnf (Fedora/RHEL)"
command -v pacman >/dev/null 2>&1 && echo "pkg: pacman (Arch)"
command -v brew >/dev/null 2>&1 && echo "pkg: brew (macOS/Linuxbrew)"
command -v winget >/dev/null 2>&1 && echo "pkg: winget (Windows)"
command -v choco >/dev/null 2>&1 && echo "pkg: choco (Windows)"
```

If `pdflatex` (or `xelatex`) and `biber` are found, skip installation and go straight to compilation.

### 2. Try minimal install automatically (when LaTeX is missing)

If LaTeX is missing, attempt a minimal install for the detected OS/environment. Ask for confirmation only if `sudo` will be required; otherwise try directly and report the result.

**Debian / Ubuntu / WSL-Ubuntu:**
```bash
sudo apt update && sudo apt install -y texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra texlive-bibtex-extra biber texlive-xetex latexmk
```

**Fedora / RHEL / CentOS:**
```bash
sudo dnf install -y texlive-scheme-medium texlive-collection-latexextra texlive-collection-fontsrecommended biber latexmk texlive-xetex
```

**Arch Linux / Manjaro:**
```bash
sudo pacman -Sy --needed texlive-basic texlive-latexrecommended texlive-latexextra texlive-fontsrecommended texlive-bibtexextra biber texlive-xetex
```

**macOS (Homebrew):**
```bash
# Prefer MacTeX no-GUI (large) if user accepts, otherwise BasicTeX + tlmgr
brew update
brew install --cask mactex-no-gui  # or: brew install --cask basictex
# After BasicTeX:
# sudo tlmgr update --self && sudo tlmgr install stix2 biblatex biber booktabs caption subcaption geometry hyperref listings xstring pgf etoolbox appendix floatrow
```

**Windows (PowerShell / CMD):**
```powershell
winget install --id MiKTeX.MiKTeX -e
# or
choco install miktex -y
# After install, in MiKTeX Console set "Install missing packages on-the-fly: Yes"
```

After attempting install, re-run the detection commands. If `pdflatex` and `biber` now resolve, compile succeeds — report to user what was installed.

### 3. If automatic install fails

If the install fails (no `sudo`, no network, permission denied, package not found, or user is on a managed/locked-down machine):

1. Use web search to find current OS-specific LaTeX install instructions (search e.g. `"install texlive ubuntu 2024"`, `"install mactex macOS 2024"`, `"install miktex windows 2024"` for the detected OS). Summarize the authoritative steps (CTAN, TeX Live, MacTeX, MiKTeX official docs) and give the user the exact commands/links to run manually outside the agent session.
2. Tell the user they can install later and the thesis files are still valid — the agent will continue editing without compiling.

Example fallback message to give the user:
> Automatic LaTeX install failed (`<reason>`). To compile locally, install TeX Live / MacTeX / MiKTeX manually: <OS-specific steps found via search, with official links>. You can also skip local install — see next section.

### 4. If user does not want to install LaTeX — edit anyway and use Overleaf / Prism

If the user explicitly says not to install LaTeX (or install is not possible/desired):

- **Continue editing anyway.** All thesis writing, front matter, chapters, citations, figures, and `main.tex` edits do not require a local LaTeX install. Never block writing on compilation.
- **Tell the user to compile externally:** upload the `Template/` folder (or the whole project) to **Overleaf** (`https://www.overleaf.com` — New Project → Upload Project) or **OpenAI Prism** and compile there with `pdfLaTeX`/`XeLaTeX` + `Biber`. Both provide full TeX Live without local setup.
- **Prepare the project for upload:** ensure `main.tex` is at the project root (copy from `Template/main.tex` if needed), include `iutbscthesis.cls`, `frontmatter.sty`, `personnelhandler.sty`, `citations.bib`, and any `Image*.png` / `figures/` the thesis uses. Zip if helpful:
  ```bash
  zip -r thesis_for_overleaf.zip main.tex iutbscthesis.cls frontmatter.sty personnelhandler.sty citations.bib Template/ figures/ 2>/dev/null || tar -czf thesis_for_overleaf.tar.gz main.tex iutbscthesis.cls frontmatter.sty personnelhandler.sty citations.bib Template/ figures/
  ```
- Mention that Overleaf/Prism will auto-install missing CTAN packages on first compile.

### 5. Compile when LaTeX is available

Standard bibliography-aware build (run from the directory containing `main.tex`):

```bash
pdflatex -halt-on-error main.tex
biber main
pdflatex -halt-on-error main.tex
pdflatex -halt-on-error main.tex
# or: latexmk -pdf -bibtex -halt-on-error main.tex  (or latexmk -xelatex -bibtex main.tex if XeLaTeX is required)
```

If LaTeX prompts `Enter file name:`, stop and install the missing package (see install steps above). Do not type `main.tex` at that prompt. If the class requires `xelatex` (check `Template/main.tex` first line `% !TeX program = xelatex/pdflatex`), use `xelatex` instead of `pdflatex`.

After a successful build, report the PDF path. After any edit that touches preamble, bibliography, or class files, re-compile and fix errors before moving to the next chapter.
