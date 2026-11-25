---
name: brief-writer
description: Finishes a Fetchproof project's handoff - drafts research/BRIEF.md with brief.mjs, answers the two sections the corpus cannot fill (Contradictions, Decision with a concrete first build step and what is out of scope), and declares the review with "Reviewed by: agent". Use on a collector once preflight prints PASS, when brief.mjs --state says draft, or when the user asks for the brief or the handoff.
---

# Brief writer

The brief is phase 1's deliverable and the only file phase 2 is required to read.

## Steps

1. `node "$HOME/.agents/fetchproof/bin/preflight.mjs"` - PASS first. The brief records
   the gate state and its warnings; it does not hide them.
2. `node "$HOME/.agents/fetchproof/bin/brief.mjs"` - drafts it from the corpus: intent,
   verified claims with sources, known unknowns with their day-one steps.
3. Answer the two **TODO** sections:
   - **Contradictions and how they were resolved** - both sides, which is trusted and
     why, and whether corroboration was independent (`source-grader`). If there were
     none, say what was compared.
   - **Decision** - what to build first, concretely enough to start from this file
     alone, and what is explicitly out of scope.
4. Replace the `Reviewed by:` placeholder with `Reviewed by: agent` - a declaration of who
   did the review steps (ADR-0074, ADR-0107).
5. `node "$HOME/.agents/fetchproof/bin/brief.mjs" --state` - `authored`.
6. `node "$HOME/.agents/fetchproof/bin/handoff.mjs"` - exit 0 - then commit the corpus
   **with** `research/raw/.fetches.jsonl` (`git add -f` it by name if a dotfile rule hides it).

## Rules

- Re-running `brief.mjs` after an edit refuses without `--force`; `--force` keeps the old
  one as `BRIEF.md.bak-<date>`.
- A claim not in `research/EVIDENCE.md` does not enter the brief.
