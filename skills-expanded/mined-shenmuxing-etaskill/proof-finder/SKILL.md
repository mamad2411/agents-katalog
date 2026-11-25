---
name: proof-finder
description: Mine proof-heavy papers, notes, PDFs, Markdown, or LaTeX sources into source-indexed proof-material files. Use when the user wants to extract technically nontrivial lemmas, estimates, definitions, dependencies, reductions, constructions, or proof strategies, preserve paper locations and stable material IDs, run DeepSeek screening/backtests, and update the proof-material index rather than writing directly to proof-usage.
---

# Proof Finder

## Overview

Use this skill to turn proof-heavy sources into source-indexed material. Codex controls the workflow, DeepSeek performs independent first-pass screening and blind backtests, and Codex verifies against the source before writing entries into `proof-material`.

`proof-finder` is a miner, not a librarian. It may suggest candidate tags and cooker hints, but it does not decide the final `proof-usage` taxonomy.

## Pipeline Position

`proof-finder` is the extraction stage:

```text
source PDFs / notes -> proof-finder -> proof-material
```

Its normal output is a source material file plus an updated material index. Stop before final taxonomy work; clustering, de-duplication, and category design belong to `proof-cooker`.

## Dependencies

- Companion skill: `deepseek-agent` for independent screening and blind backtests.
- Companion skill: `proof-material` for source-indexed output files and the material index.
- Downstream companion: `proof-cooker` can later synthesize material into `proof-usage`.
- External tools: `opencode`, plus the wrapper supplied by the installed `deepseek-agent` skill configured with DeepSeek provider credentials.

If DeepSeek is unavailable, stop and report the blocker. Do not replace independent screening or blind backtests with Codex-only judgment unless the user explicitly accepts a degraded run.

## Workflow

1. Establish source boundaries.
   - Accept one or more papers, notes, Markdown files, LaTeX projects, PDFs, or excerpts.
   - Treat the source path or supplied document as the only evidence for mined entries unless the user explicitly provides additional context.
   - Keep scratch prompts, transcripts, extracted text, and local test outputs under an untracked scratch area; do not commit them.

2. DeepSeek first-pass screening.
   - Start a fresh DeepSeek invocation for each source or logically independent batch. Do not use `--continue`.
   - Ask DeepSeek to read only the target source and return a concise list of candidate theorems, lemmas, claims, proof devices, decompositions, dependencies, definitions, and strategies.
   - Require each candidate to be labeled `DETAIL`, `STRATEGY`, `DEFINITION`, `DEPENDENCY`, or `BOTH`.
   - Require paper locations when DeepSeek can identify them.
   - After the run, inspect the result file as the authoritative output and verify that DeepSeek did not edit source files.

3. Codex verifies and rewrites candidates.
   - Read the relevant source passages as needed.
   - Record paper location, public source metadata, local statement, reusable abstraction, proof skeleton, dependencies, candidate tags, and cooker hints.
   - Preserve the source's proof topology; do not flatten items into final technique or strategy buckets.
   - Drop candidates that are routine, too source-specific, not recoverable from the source, or unsafe to publish.

4. DeepSeek blind backtest.
   - Start a new fresh DeepSeek invocation with no source files, no web access, and no permission to inspect local files.
   - Give DeepSeek only the candidate abstraction or distilled problem.
   - Ask it to solve, reconstruct, or identify missing assumptions under a time limit.
   - Record the result only as `Backtest signal`: value, difficulty, self-containedness, missing assumptions, or warnings.
   - Do not let the backtest alone decide final publication or final `proof-usage` placement.

5. Write to `proof-material`.
   - Create or update `proof-material/references/<source-slug>.md`.
   - Assign stable source-local IDs such as `CR24-D01` or `GGSXY25-S02`; never renumber existing IDs.
   - Update `proof-material/references/index.md`.
   - Do not write directly to `proof-usage/references/techniques.md`, `proof-usage/references/strategies.md`, or cooked category files.

## Material Item Format

Use the contract from the `proof-material` skill:

```markdown
### <ID>: <Short name>

- Type: `DETAIL`
- Paper location:
- Depends on:
- Local statement:
- Reusable abstraction:
- Proof skeleton:
- Why it is valuable:
- Backtest signal:
- Candidate tags:
- Cooker hints:
```

## DeepSeek Prompt Templates

Use [references/deepseek-prompts.md](references/deepseek-prompts.md) when drafting first-pass screening or blind-backtest prompts. Adapt field names to the source, but keep source isolation and output contracts.

## Quality Bar

- Every kept material item must have a stable ID, source location, source attribution, tags, reusable abstraction, and proof skeleton.
- Prefer fewer high-value items over a catalog of routine lemmas.
- Preserve mathematical honesty: if assumptions are uncertain, mark the item for cooker verification instead of overstating it.
- Keep private paths, account names, unpublished project details, raw transcripts, OCR dumps, and run logs out of tracked files.
