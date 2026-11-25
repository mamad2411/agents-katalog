---
name: hyperresearch-8-corpus-critic
description: >
  Step 8 of the hyperresearch V8 pipeline. Spawns one corpus-critic subagent
  to identify "what source, if found, would overturn the current
  direction?" gaps, then runs a targeted fetch wave to fill them.
  Highest-leverage intervention point: corrections applied before drafting
  cost nothing; corrections applied after drafting require patches.
  Invoked via Skill tool from the entry skill (full tier only).
---

# Step 8 — Pre-draft corpus critic (targeted gap-fill)

## Run-scoped artifact contract

Use the active `RUN_MANIFEST` created by the entry skill. Substitute `$ARTIFACT_DIR`, `$TEMP_DIR`, `$CLAIMS_DIR`, `$QUERY_FILE_PATH`, and `$FINAL_REPORT_PATH` from that manifest before reading, writing, spawning subagents, or running Bash. Do not read or write legacy top-level run artifacts such as `research/scaffold.md`, `research/prompt-decomposition.json`, or `research/temp/*`.

**Tier gate:** `full` tier ONLY. Skip for `light`.

**Goal:** before drafting, ask "what source, if found, would overturn the current direction?" and run a targeted fetch wave to fill the most dangerous gaps. This is the highest-leverage intervention point in the pipeline — corrections applied before drafting cost nothing; corrections applied after drafting require patches and risk structural drift.

---

## Recover state

Read these inputs:
- `$ARTIFACT_DIR/scaffold.md` — vault_tag
- `$ARTIFACT_DIR/comparisons.md` — cross-locus tensions
- `$ARTIFACT_DIR/loci.json` — scored loci
- `$TEMP_DIR/source-tensions.json` — expert disagreements
- `$ARTIFACT_DIR/prompt-decomposition.json` — specifically the `time_periods` array

---

## Pre-flight: period-pinned primary-source coverage check

**Run this BEFORE spawning the corpus-critic subagent.** If `prompt-decomposition.json -> time_periods` is non-empty, walk every entry and verify the vault contains a primary source filed *for that exact period* — not "most recent", not narrative commentary, not earnings-call transcripts standing in for tabular filings.

For each `time_period` entry:

1. Search the vault for a primary source matching the `primary_source` description and the `issuer`:
   ```bash
   PYTHONIOENCODING=utf-8 {hpr_path} search "<period> <issuer>" --tag <vault_tag> --include-body -j
   ```
2. Open the candidate notes (`note show <id> -j`) and verify the document's actual reporting period — the filing must cover the SPECIFIC period named in the prompt, not an adjacent one. A Q1 2025 10-Q does NOT satisfy "Q3 2024" — different period, different tabular data.
3. **If the period-pinned filing is missing, add it to `$ARTIFACT_DIR/corpus-critic-gaps.json` as a `priority: critical` gap of type `period-pinned-primary` BEFORE spawning the corpus-critic subagent.** Schema:
   ```json
   {{
     "type": "period-pinned-primary",
     "target_position": "<period> exact figures for <issuer>",
     "search_queries": [
       "site:sec.gov 10-Q \"period ended September 30, 2024\" <issuer>",
       "<issuer> Q3 2024 10-Q filing PDF"
     ],
     "source_type": "primary-filing",
     "priority": "critical",
     "rationale": "Prompt names <period>; vault has no filing covering that exact period. Tabular line items only exist in the period-pinned filing. Without it, the draft will paraphrase rounded numbers from earnings calls and miss the rubric's exact figures."
   }}
   ```

The targeted fetch wave in the next step will pull these filings BEFORE the corpus-critic finishes its broader gap analysis. This ordering matters: numerical-precision misses are the largest single category of avoidable factual-accuracy failures.

---

## Procedure

1. **Spawn ONE `hyperresearch-corpus-critic` subagent** (Sonnet).

   **Spawn template:**
   ```
   subagent_type: hyperresearch-corpus-critic
   prompt: |
     RESEARCH QUERY (verbatim, gospel):
     > {{paste $QUERY_FILE_PATH body}}

     QUERY FILE: $QUERY_FILE_PATH

     PIPELINE POSITION: You are step 8 of the hyperresearch V8 pipeline.
     Step 6 produced $ARTIFACT_DIR/comparisons.md. After you return, the
     orchestrator runs a targeted fetch wave, then step 10 drafts.

     YOUR INPUTS:
     - run_id: <run_id>
     - artifact_dir: $ARTIFACT_DIR
     - temp_dir: $TEMP_DIR
     - claims_dir: $CLAIMS_DIR
     - corpus_tag: <vault_tag>
     - comparisons_path: $ARTIFACT_DIR/comparisons.md
     - loci_path: $ARTIFACT_DIR/loci.json
     - output_path: $ARTIFACT_DIR/corpus-critic-gaps.json
   ```

2. **Read the gaps output** (`$ARTIFACT_DIR/corpus-critic-gaps.json`). Each gap has a `priority` (critical / high) and a `type` (overturning / strengthening / independent-verification).

3. **Targeted fetch wave.** Spawn **2–4 fetcher subagents** (Sonnet) to search for and fetch the sources identified in the gaps.

   **Spawn template:**
   ```
   subagent_type: hyperresearch-fetcher
   prompt: |
     RESEARCH QUERY (verbatim, gospel):
     > {{paste $QUERY_FILE_PATH body}}

     QUERY FILE: $QUERY_FILE_PATH

     PIPELINE POSITION: You are a step 8 fetcher (corpus-critic gap-fill)
     of the hyperresearch V8 pipeline. The corpus critic identified specific
     gaps; you fetch sources targeting those gaps. After you return, the
     orchestrator updates comparisons.md based on what you found.

     YOUR INPUTS:
     - run_id: <run_id>
     - artifact_dir: $ARTIFACT_DIR
     - temp_dir: $TEMP_DIR
     - claims_dir: $CLAIMS_DIR
     - vault_tag: <vault_tag>
     - search_queries: [<gap.search_queries>]
     - source_type: <gap.source_type>
     - gap_id: <gap.id>
   ```

4. **Assess results.**
   - **Overturning source found:** re-read the relevant committed position from the interim note. If the new source genuinely undercuts it, update `$ARTIFACT_DIR/comparisons.md` to note the weakened position — the draft will handle it with appropriate calibration. Do NOT re-run the full depth investigation; adjust the position's confidence level.
   - **Overturning source NOT found:** the committed position gains confidence. Note this in `comparisons.md` — "adversarial search for counter-evidence to [position] returned no substantive challenges."
   - **Strengthening/verification source found:** note the additional support in `comparisons.md`. The draft can assert more confidently.

5. **Log results** to `$TEMP_DIR/corpus-critic-results.md`:
   - Each gap: what was searched, what was found (or not), how it affects the committed positions
   - Updated confidence levels for any positions that changed

---

## Exit criterion

- `$ARTIFACT_DIR/corpus-critic-gaps.json` exists
- All critical gaps attempted (fetched or documented as unfindable)
- `$TEMP_DIR/corpus-critic-results.md` exists
- `$ARTIFACT_DIR/comparisons.md` updated with confidence/strengthening/overturning notes

---

## Next step

Return to the entry skill (`hyperresearch`). Invoke step 9:

```
Skill(skill: "hyperresearch-9-evidence-digest")
```
