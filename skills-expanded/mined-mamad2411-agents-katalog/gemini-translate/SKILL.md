---
name: gemini-translate
description: Batch-translate content files using Gemini CLI as a subagent, with Claude orchestrating quality and validation
version: 1.0.0
---

# Gemini Translate

Batch-translate content files (markdown, JSON, YAML frontmatter) using Gemini CLI as a translation subagent. Claude orchestrates the pipeline: identifies gaps, builds prompts with glossary context, dispatches to Gemini in a single CLI call, validates output structure, and writes files.

## Why Gemini CLI

- **Uses your Google AI Ultra plan** via OAuth (no API key needed)
- **1M token context** fits entire glossaries + dozens of source files in one call
- **Single startup cost** (~13s) instead of per-file overhead
- **Claude stays in control** of orchestration, validation, and file writes

## Prerequisites

- Gemini CLI installed and authenticated (`gemini` on PATH, OAuth configured)
- Source content files in a consistent structure (markdown with frontmatter, JSON, etc.)

## Pipeline Overview

```
Claude: find translation gaps (missing .es.* files, parity tests)
  |
Claude: read source files + glossary + existing translations for tone
  |
Claude: build batch prompt and call gemini-translate.sh
  |
Gemini: translate all files in one shot, return JSON
  |
Claude: parse response, validate structure, write .es.* files
  |
Claude: run project tests (i18n symmetry, coverage)
```

## Usage

### Step 1: Identify gaps

Find content files missing their locale counterpart:

```bash
# Generic pattern -- adjust paths and extensions for your project
for f in content/**/*.md; do
  base=$(basename "$f")
  [[ "$base" == *.es.* ]] && continue
  name="${base%.*}"
  dir=$(dirname "$f")
  [ ! -f "$dir/${name}.es.md" ] && echo "MISSING: $f"
done
```

Or run your project's i18n parity tests if they exist.

### Step 2: Prepare the glossary

Create a glossary of terms that must be translated consistently. The glossary is a simple text block embedded in the prompt:

```
## Glossary (EN -> ES)
- "OB/GYN Physician" -> "Medico OB/GYN"
- "High-risk pregnancy" -> "Embarazo de alto riesgo"
- "Certified Nurse Midwife" -> "Enfermera Partera Certificada"
```

If your project has an existing glossary (Python dict, CSV, JSON), convert it to this format before calling the script. The script accepts a glossary file via `--glossary`.

### Step 3: Run the batch translation

```bash
bash gemini-translate.sh \
  --source-lang en \
  --target-lang es \
  --glossary glossary.txt \
  --model gemini-2.5-pro \
  --instructions "Use formal 'usted'. Latin American Spanish, not Spain. Warm but professional tone for patient-facing medical content." \
  file1.md file2.md file3.md
```

The script:
1. Reads all source files
2. Builds a single prompt with glossary + instructions + all file contents
3. Calls `gemini -p "..." -o json --approval-mode plan`
4. Parses the JSON response and prints each translation to stdout as a JSON array

### Step 4: Claude validates and writes

After the script returns, Claude should:

1. Parse the JSON output
2. For each translated file:
   - Verify frontmatter keys match the source exactly
   - Verify links, image paths, and brand names are preserved
   - Verify no `<!-- REVIEW: -->` flags from Gemini (or surface them to the user)
3. Write the `.es.*` files
4. Run the project's i18n tests

## Script Reference

### `gemini-translate.sh`

```
Usage: gemini-translate.sh [OPTIONS] FILE [FILE...]

Options:
  --source-lang LANG    Source language code (default: en)
  --target-lang LANG    Target language code (default: es)
  --glossary FILE       Path to glossary file (term mappings, one per line)
  --instructions TEXT   Additional translation instructions for tone/style
  --model MODEL         Gemini model override (default: system default)
  --max-tokens N        Max estimated input tokens per batch (default: 80000)
  --gemini-bin PATH     Path to gemini binary (bypasses wrapper detection)
  --dry-run             Print the prompt without calling Gemini

Output: JSON array to stdout
  [
    {"file": "about.md", "translation": "---\ntitle: Acerca de\n---\n..."},
    {"file": "careers.md", "translation": "---\ntitle: Carreras\n---\n..."}
  ]

Exit codes:
  0  Success
  1  Gemini CLI not found or not authenticated
  2  No input files provided
  3  Gemini returned an error or unparseable output
```

## Translation Quality Rules

These rules are embedded in the prompt sent to Gemini:

1. **Preserve structure exactly**: frontmatter keys, markdown formatting, links, HTML tags, image paths
2. **Never translate**: brand names, proper nouns, URLs, file paths, credentials (MD, DO, CNM, etc.)
3. **Medical terms**: Use the glossary. When a term is not in the glossary and you are uncertain, wrap it in `<!-- REVIEW: original term -->`
4. **Tone**: Match the source document's tone. For medical patient-facing content, be warm, reassuring, and professional
5. **Output format**: Return the complete translated file content (frontmatter + body), not just the changed parts

## Adapting for Other Projects

This skill is project-agnostic. To use it on a new codebase:

1. **File convention**: Set your project's locale file naming pattern (`.es.md`, `.es.json`, `locales/es/`, etc.)
2. **Glossary**: Extract domain-specific terms into a glossary file
3. **Instructions**: Write a one-paragraph style guide for the target language
4. **Validation**: Point Claude at your project's i18n tests or write a simple key-comparison check

## Gemini CLI Wrapper Compatibility

Many users have a shell wrapper (e.g., `~/bin/gemini`) that adds `--yolo`/`-y` by default. This conflicts with `--approval-mode`. The script avoids this by:

1. Preferring `pnpx @google/gemini-cli` (calls the package directly, no wrapper)
2. Falling back to `gemini` on PATH only if `pnpx` is unavailable
3. Accepting `--gemini-bin /path/to/binary` to override detection entirely

The script uses `-o json` for structured output, which returns a `{session_id, response, stats}` envelope. The embedded Python parser extracts the `response` field and handles markdown code fences, null bytes, and MCP warning prefixes automatically.

## Token-Based Batching

Instead of a fixed file count, the script estimates input tokens (1 token ~ 4 chars) and stops adding files when the budget is reached. The default `--max-tokens 80000` leaves room for the translation output (roughly 1.2x the input for EN->ES). Files that exceed the budget are listed as skipped so the caller can run a follow-up batch.

## Truncation Recovery

When Gemini hits its output token limit and truncates the JSON mid-entry, the script recovers by:

1. Detecting incomplete JSON
2. Progressively trimming from the end to find valid JSON boundaries
3. Dropping the last (likely truncated) entry
4. Reporting how many complete translations were recovered

## Agentic Workflow & Vibe Coding

- **Iterative Translation:** Do not expect perfect linguistic tone or structural preservation on the first batch run. Draft a small test batch, review the output for tone and formatting, isolate any consistent translation errors, refine the glossary or prompt instructions ONE variable at a time, and rerun the test before processing the entire project.
- **Vibe Coding:** Commit your working source content and glossary updates locally *before* running the translation batch, and commit the generated `.es.*` files separately so you can easily revert if the model hallucinated structure.

## Limitations

- **Single language pair per call**: The script handles one source/target pair. For multi-language projects, run once per target language.
- **Gemini CLI startup**: ~13s overhead per batch call. Batching amortizes this.
- **Output token limit**: 80K input tokens is the default budget. If truncation occurs, reduce `--max-tokens`.
- **No streaming**: The script waits for the full response. Large batches may take 30-60s of model time on top of startup.
- **Python 3 required**: The JSON extraction uses an embedded Python script.
