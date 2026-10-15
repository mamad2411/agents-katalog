---
name: cancerrisk-formal-v3
description: |
  Use when converting health-checkup files into four audit-grade CancerRisk
  reports with MinerU OCR, ontology-backed factor filling, deterministic
  snapshot/longitudinal risk math, screening recommendations, and a
  per-person health record archive.
safety: |
  Reports are health-management and screening-decision aids only. They must
  never produce a diagnosis, treatment plan, medication advice, or triage.
---

# CancerRisk Formal Skill

This skill is a thin operating guide. Load the referenced files only when
the current stage needs them. The orchestrator is the single entrypoint:

```bash
python cancerrisk-skill/scripts/run_formal_analysis.py \
  --input <file-or-folder> \
  --analysis-output <out> \
  --person-id <stable_id>
```

Default personal health record location:
`cancerrisk-skill/docudatabase/<person_id>/` (same directory level as
this `SKILL.md`). Override `--archives-root` only for explicit tests or
deliberate relocation.

## Use / Refuse

Use for:

- health-checkup files that need `health_summary.html`,
  `snapshot_risk.html`, `longitudinal_risk.html`, and `index.html`;
- longitudinal runs for the same person;
- reruns against updated evidence, answers, or archive history.

Refuse or redirect for diagnosis, treatment selection, medication
dosing, urgent triage, or single-symptom clinical Q&A.

## Non-Negotiables

- LLM/agent work may only fill factual fields from source text or user
  answers. It must not invent factor IDs, cancer IDs, probabilities,
  OR/RR/HR, LR, sensitivity, specificity, screening intervals, or advice.
- Use only closed vocabularies emitted by the orchestrator:
  `risk_factor_master.json`, `structured_risk_factors_timeline`,
  `tumor_markers.candidate.json`, and evidence-store JSON.
- `evidence_text` must be a literal substring of the named source md.
- Do not skip required user answers in real runs. If answers are missing,
  stop and ask the user.
- Do not write to the personal archive before longitudinal analysis.
  `archive_update_proposal.json` is the入档 prompt; confirmed入档 is a
  separate step.
- For the four agent checkpoints below, do the file reads/writes in this
  agent loop. Do not delegate these deterministic fills to sub-agents.

## Minimal Workflow

1. Run MinerU and stop:

   ```bash
   python cancerrisk-skill/scripts/run_formal_analysis.py \
     --input <input> --analysis-output <out> --stop-after mineru
   ```

2. **Checkpoint 1: Refine.** For each
   `artifacts/mineru/<data_id>/content.md`, write `refined.md` in the
   same folder. Keep demographics, abnormal rows, tumor-marker rows
   including normal values, imaging/test conclusions, and positive
   findings. See `references/runtime_workflow.md`.

3. Run to interactive:

   ```bash
   python cancerrisk-skill/scripts/run_formal_analysis.py ... \
     --stop-after interactive
   ```

4. **Checkpoint 2: Interactive answers.** After `--stop-after interactive`
   the orchestrator exits with code 8. Read
   `artifacts/interactive_questionnaire.json`, present **every question**
   to the user in the conversation, collect their answers, write an answers
   JSON file, then re-run with `--answers <answers.json>`.

   **Never pre-fill, guess, or silently supply answers.** The interactive
   flow is the sole mechanism for collecting user-specific risk-factor
   history; skipping it produces clinically wrong output.

   Fast ask-first path (before the first pipeline run):

   ```bash
   python cancerrisk-skill/scripts/build_questionnaire.py \
     --sex <male|female> --age <age> --output /tmp/q.json
   ```

5. Run to master template:

   ```bash
   python cancerrisk-skill/scripts/run_formal_analysis.py ... \
     --stop-after master-template
   ```

6. **Checkpoint 3: Master fill + imaging + tumor markers.**
   Fill `structured_risk_factors_timeline.candidate.json` and
   `tumor_markers.candidate.json` using only emitted allowlists. Validate:

   ```bash
   python cancerrisk-skill/scripts/validate_timeline_candidate.py \
     --candidate <out>/artifacts/structured_risk_factors_timeline.candidate.json
   python cancerrisk-skill/scripts/validate_tumor_markers.py \
     --candidate <out>/artifacts/tumor_markers.candidate.json
   ```

   Then re-run with `--stop-after cp3-verify`:

   ```bash
   python cancerrisk-skill/scripts/run_formal_analysis.py ... \
     --stop-after cp3-verify
   ```

7. **Checkpoint 3.1: Verification audit (mandatory).**
   The orchestrator prints a structured audit task. As an **independent
   auditor** (not the CP3 extractor), re-read each `refined.md` and
   check for omissions:

   - Read every `refined.md` listed in the audit task independently.
   - Identify ALL clinical abnormal findings in the document.
   - For each finding not in the recorded list, look up a matching
     `factor_key` in `risk_factor_master.json`.
   - If found: add the record to `structured_risk_factors_timeline.candidate.json`
     (same format as CP3 records; `evidence_text` must be a literal
     substring of the source `refined.md`).
   - If no matching `factor_key` exists: do not force-fit; it will
     appear in the "证据库外异常提示" section automatically.
   - If no omissions are found: proceed without editing the candidate.

   After audit (with or without additions), continue to health-summary:

8. Run to health-summary API:

   ```bash
   python cancerrisk-skill/scripts/run_formal_analysis.py ... \
     --stop-after health-summary-api
   ```

8. **Checkpoint 4: Health-summary structuring.** Convert the API
   markdown into `health_summary_structured_summary.json`. **MUST use
   `finalize_structured_summary.py` — do NOT write the JSON directly
   (direct writes are truncated by most agent runtimes):**

   ```bash
   python cancerrisk-skill/scripts/finalize_structured_summary.py \
     --analysis-output <out> --fills <fills.json>
   ```

9. Run the final pipeline (without `--auto-apply-archive` first):

   ```bash
   python cancerrisk-skill/scripts/run_formal_analysis.py ... \
     --person-id <id>
   ```

   **Exit code 4** means the archive proposal is ready but not yet written.
   The orchestrator stderr will contain `[task8] HALT_FOR_USER_CONFIRMATION`
   with the proposal file path.

   **Agent MUST follow this exact flow — no skipping:**

   1. Read `<out>/artifacts/archive_update_proposal.json` and show a summary
      to the user.
   2. Ask the user **explicitly**: "确认入档？（是/否）"
   3. Wait for the user's answer:
      - **用户选"是"** → re-invoke adding `--auto-apply-archive`:
        ```bash
        python cancerrisk-skill/scripts/run_formal_analysis.py ... \
          --person-id <id> --auto-apply-archive
        ```
      - **用户选"否"** → end session; do **not** re-run; no archive written.

   Do **not** add `--auto-apply-archive` on the first run and do **not**
   silently skip the user confirmation step — the spec requires explicit
   user confirmation before any archive write ("用户确认后才写入档案").

## Archive Contract

The personal health record has two roles:

- longitudinal input: existing timeline history plus the current run,
  merged in memory;
- confirmed入档: after longitudinal analysis, dedup and write the
  processed current result into `docudatabase/<person_id>/`.

Default structure:

```text
cancerrisk-skill/docudatabase/
├── person_index.json
└── <person_id>/
    ├── factor_timeline.json
    ├── screening_test_timeline.json
    ├── report_index.json
    └── snapshots/YYYY-MM-DD.json
```

Every archive path must go through
`scripts/archive_manager.py::resolve_person_archive`. Details:
`references/risk_prediction.md`.

## Output Contract

Final user-facing reports:

- `health_summary.html`
- `snapshot_risk.html`
- `longitudinal_risk.html`
- `index.html`

Key audit artifacts:

- `conversion_manifest.json`
- `interactive_questionnaire.json`
- `interactive_answers.md`
- `risk_factor_master.json`
- `structured_risk_factors_timeline.candidate.json`
- `structured_risk_factors_timeline.json`
- `tumor_markers.candidate.json`
- `merged_risk_factors.json`
- `health_summary_api_response.md`
- `health_summary_structured_summary.json`
- `snapshot_risk.json`
- `voi_ranking.json`
- `longitudinal_risk.json`
- `archive_update_proposal.json`
- `manifest.json`

## Progressive References

Open only the file needed for the current task:

| Need | File |
|---|---|
| Full checkpoint recipes and run order | `references/runtime_workflow.md` |
| MinerU API/client behavior | `references/mineru_api.md` |
| Evidence ontology and derived assertions | `references/evidence_ontology.md` |
| Health-summary API/template structuring | `references/health_summary_rebuild.md` |
| Snapshot, VoI, longitudinal, archive rules | `references/risk_prediction.md` |
| Timeline event shape and slim/full keys | `references/event_format.md` |
| Runtime config | `config/formal.yaml` |
| Deterministic implementation | `scripts/*.py` |
| Regression contracts | `tests/test_v3_*.py`, `tests/test_v4_*.py` |

## Safety Boundaries

- Reports are decision aids, not diagnoses.
- Cancers outside the ontology never affect probability math.
- Sex-mismatched cancers use `posterior_probability: null`.
- Conversion/extraction failures halt before probability math.
- Production MinerU should use a user token in `config/local.yaml`; the
  bundled demo token is only a fallback.

## Verification

```bash
python3 -m pytest -q
```

Run focused tests for edited areas before full verification.
