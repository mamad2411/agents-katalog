---
name: deep-research
description: Run Google Deep Research on a topic and save the report to the vault
disable-model-invocation: false
argument-hint: "<research prompt or file path> [--output=path] [--stream] [--enhance] [--latex]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch, AskUserQuestion
---

# Deep Research Skill

Run Google Deep Research (Gemini) on a research prompt and save the comprehensive report to the vault.

## Input

- **$ARGUMENTS** (required): Either a research prompt string OR a path to a prompt file. May optionally include:
  - `--output=<path>`: Custom output path for the report (default: `temp/deep-research-YYYY-MM-DD-<slug>.md`)
  - `--stream`: Use streaming mode for real-time output
  - `--enhance`: Rewrite the prompt using Claude before sending to Gemini (improves relevance, specificity, and self-consistency)
  - `--latex`: Request output in LaTeX format (appends formatting instructions to the prompt)

The input can be:
1. **Inline prompt**: `/deep-research What are the latest advances in quantum computing?`
2. **File path**: `/deep-research temp/research-prompt.md` — reads the file contents as the prompt

## Workflow

### Step 1: Parse Arguments

Extract the research prompt and optional flags from `$ARGUMENTS`:

1. If arguments are empty, ask the user for a research prompt
2. Extract `--output=<path>` if present (remove from prompt text)
3. Extract `--stream` flag if present (remove from prompt text)
4. Extract `--enhance` flag if present (remove from prompt text)
5. Extract `--latex` flag if present (remove from prompt text)
6. Check if the remaining text is a file path (ends in `.md`, `.txt`, or file exists):
   - If it's a file: read its contents as the prompt
   - If it's text: use it as the inline prompt

### Step 1b: Enhance Prompt (if `--enhance`)

If the `--enhance` flag is set, rewrite the user's prompt to be more effective for deep research. You (Claude) should rewrite it yourself — do NOT call an external tool for this.

**Rewriting goals:**
- Make the query more specific and well-scoped
- Add explicit sub-questions that decompose the topic
- Request comparative analysis where appropriate
- Ask for evidence quality assessment (peer-reviewed vs preprint vs blog)
- Add temporal scoping (e.g., "focusing on 2023-2026 developments")
- Request structured output (sections, key findings, open questions)
- Remove ambiguity and vague terms
- Ensure internal consistency (sub-questions should not contradict each other)

**Example:**

User prompt:
> What's happening with quantum computing?

Enhanced prompt:
> Provide a comprehensive survey of quantum computing progress from 2023 to early 2026. Structure the report as follows:
> 1. **Hardware advances**: Compare progress across superconducting (IBM, Google), trapped-ion (IonQ, Quantinuum), and photonic (Xanadu, PsiQuantum) platforms. What are the current qubit counts, error rates, and coherence times for each?
> 2. **Error correction milestones**: What demonstrations of fault-tolerant quantum computing have been achieved? How close are we to logical qubit operation below the error-correction threshold?
> 3. **Algorithms and applications**: What new quantum algorithms or practical applications have emerged? Are there verified quantum advantage results beyond random circuit sampling?
> 4. **Software and ecosystem**: What is the state of quantum programming frameworks, cloud access platforms, and developer tooling?
> 5. **Commercial landscape**: Which companies have raised significant funding or announced product milestones? What is the timeline consensus for practical quantum advantage?
> 6. **Open questions and challenges**: What are the key unsolved problems and most promising research directions?
> Prioritize peer-reviewed sources and distinguish between demonstrated results and vendor roadmap claims.

**After rewriting:**
- Show the enhanced prompt to the user
- Proceed without asking for confirmation (the user can re-run without `--enhance` if they prefer the original)

### Step 1c: Append LaTeX Instructions (if `--latex`)

If the `--latex` flag is set, append the following to the prompt (original or enhanced):

```
Format the entire output as a LaTeX document. Use the following conventions:
- Use \section{} and \subsection{} for headings
- Use \begin{itemize} or \begin{enumerate} for lists
- Use \textbf{} for emphasis and \textit{} for titles
- Use \cite{} style references with a \begin{thebibliography} section at the end
- Use proper LaTeX escaping for special characters (%, &, #, etc.)
- Include a \title{} and \begin{abstract} at the top
- Do NOT wrap in \begin{document} / \end{document} — just provide the body content ready to paste into a template
```

**When both `--enhance` and `--latex` are used:** First enhance the prompt, then append the LaTeX instructions.

**Output file extension:** When `--latex` is active and no custom `--output` is specified, use `.tex` extension instead of `.md` for the output file.

### Step 2: Determine Output Path

If no `--output` was specified:
1. Generate a slug from the first 5-6 words of the prompt (lowercase, hyphens, no special chars)
2. Use path: `temp/deep-research-YYYY-MM-DD-<slug>.md`
3. Ensure `temp/` directory exists

### Step 3: Run Deep Research

Execute the deep research script.

**If the prompt was modified** (by `--enhance` and/or `--latex`), write the final prompt to a temp file and use `--prompt-file`:
```bash
# Write modified prompt to temp file
# (use Write tool to create temp/deep-research-prompt-YYYY-MM-DD-HHMMSS.md)

/Users/anaderi/micromamba/envs/obsidian/bin/python /Users/anaderi/Obsidian/iCloud\ vault/tasks/bin/deep-research.py --output "<output-path>" --prompt-file "temp/deep-research-prompt-YYYY-MM-DD-HHMMSS.md"
```

**For unmodified inline prompt:**
```bash
/Users/anaderi/micromamba/envs/obsidian/bin/python /Users/anaderi/Obsidian/iCloud\ vault/tasks/bin/deep-research.py --output "<output-path>" "<research-prompt>"
```

**For unmodified prompt file:**
```bash
/Users/anaderi/micromamba/envs/obsidian/bin/python /Users/anaderi/Obsidian/iCloud\ vault/tasks/bin/deep-research.py --output "<output-path>" --prompt-file "<prompt-file-path>"
```

**Environment:** The script reads `GEMINI_API_KEY` or `GOOGLE_API_KEY` from environment.

**If streaming mode requested, add `--stream` flag.**

**Important:**
- This can take 2-10 minutes depending on topic complexity
- Use `timeout: 600000` (10 minutes) for the Bash command
- Use `run_in_background: true` if user wants to continue working while research runs

### Step 4: Post-Process the Report

After the script completes successfully:

1. Read the output file
2. Add YAML frontmatter if not present:
   ```yaml
   ---
   type: deep-research
   date: YYYY-MM-DD
   prompt: "<original user prompt (before enhancement)>"
   enhanced: true/false
   latex: true/false
   source: Google Deep Research (Gemini)
   tags:
     - deep-research
   ---
   ```
3. Save the updated file

### Step 5: Report to User

Display a summary:
- Output file path
- Brief summary of what was researched (first few lines or key headings)
- Suggest next steps: review the report, attach to a project note, or extract concepts

## Error Handling

- **No API key**: Tell user to set `GEMINI_API_KEY` or `GOOGLE_API_KEY` environment variable
- **Script not found**: Check path to `deep-research.py`
- **Research failed**: Show error message from script, suggest rephrasing the prompt
- **Timeout**: Inform user the research is taking longer than expected, suggest running with `--stream` to monitor progress
- **Empty result**: Warn user, suggest more specific prompt

## Examples

```bash
# Basic research query
/deep-research What are the latest advances in topological quantum computing in 2025-2026?

# With custom output path
/deep-research --output=1-Project/2026-Quantum/research-tqc.md What are the latest advances in topological quantum computing?

# Streaming mode for real-time updates
/deep-research --stream What is the current state of room-temperature superconductors?

# Research for a specific project
/deep-research Compare transformer-based and GNN-based approaches for molecular property prediction

# Broad literature review
/deep-research Survey the field of AI-assisted scientific discovery, focusing on physics and materials science

# From a prompt file (useful for long, detailed prompts)
/deep-research temp/research-prompt.md

# Prompt file with custom output
/deep-research --output=1-Project/2026-Quantum/survey.md temp/quantum-prompt.txt

# Enhanced prompt (Claude rewrites the query before sending to Gemini)
/deep-research --enhance What's happening with quantum computing?

# LaTeX output format
/deep-research --latex Survey of topological insulators and their applications

# Both enhance and LaTeX
/deep-research --enhance --latex Advances in neural radiance fields for scientific visualization
```

## Output Format

The saved markdown file will contain:
- YAML frontmatter with metadata
- The full Deep Research report (typically 2000-5000 words)
- Structured sections with headings, citations, and references
- Source links where available

## Integration with CLAUDE.md

- Reports saved to `temp/` can be attached to notes via `/attach-resources`
- Key concepts can be extracted with `/add-concept`
- Findings can inform project notes in `1-Project/`
- Reports follow vault conventions for binary-free markdown storage

## Notes

- Deep Research uses Gemini's `deep-research-pro-preview-12-2025` agent
- The agent performs autonomous web research, synthesizing multiple sources
- Results include citations and source links
- Typical execution time: 2-5 minutes for focused queries, up to 10 minutes for broad topics
- API key must be set in environment (shell profile or `.env`)
