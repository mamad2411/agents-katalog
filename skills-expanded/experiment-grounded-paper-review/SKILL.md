---
name: experiment-grounded-paper-review
description: Use this skill when the user wants to review, verify, or revise a TeX or PDF research paper by checking whether claims, tables, figures, citations, and conclusions are actually supported by code, experiment runs, logs, and reproducible evidence. The manuscript must not be more confident than the experiments.
---

# Experiment-Grounded Paper Review

## Overview

This skill is for papers that need evidence-constrained verification rather than ordinary prose polishing. It links manuscript claims to executable evidence: code repositories, commands, logs, tables, and reproducible outputs.

Its governing rule is simple:

`The paper is not allowed to be more confident than the experiments.`

Use this skill when the user wants to check whether a paper draft is actually supported by the available code and results, or when the user wants help running reproduction experiments and forcing the paper to align with what those runs can honestly support.

## When To Use

Use this skill when the user asks for any of the following:

- Verify whether a paper is consistent with code and experiments
- Review a `.tex` project or `.pdf` draft against logs, tables, and repos
- Extract paper claims and build an evidence ledger
- Search for related or official repositories to reproduce baselines
- Run evaluation commands and compare outputs with manuscript numbers
- Identify unsupported, overstated, or contradicted claims
- Produce safe rewrites and LaTeX patch suggestions constrained by evidence

Do not use this skill when the main need is only:

- Pure writing polish without experimental verification
- Citation formatting cleanup alone
- Figure generation alone
- General brainstorming without a concrete paper or experiment target

## Inputs

Collect as many of these as available:

- Paper files: `.tex`, `.pdf`, `.bib`, appendix, tables, figures
- Optional local code repo path or remote GitHub URL
- Optional experiment logs or output directories
- Benchmark names, dataset names, metric names, and baseline names
- Claimed key numbers from the draft
- Target venue
- Any constraints on compute, time, or environment

If the user provides only partial inputs, still build the claim ledger and mark unresolved evidence explicitly.

## Core Principle

The manuscript must obey the evidence.

If a claim is not supported by experiments, code, logs, tables, figures, or verified citations, the skill must:

- delete it
- weaken it
- narrow its scope
- mark it as requiring new experiments

The skill must never:

- invent new results
- smooth over failed reproductions
- report subset experiments as full-benchmark evidence
- call a result significant without statistical evidence
- call a method state-of-the-art without strong baseline coverage

## Default Workflow

Follow this sequence unless the user asks for a narrower slice:

1. `Parse Manuscript`
   Extract title, section structure, claims, tables, figure references, equations, and citations.
2. `Build Claim Ledger`
   Normalize every notable claim into a machine-readable record with type, scope, location, and required evidence.
3. `Retrieve Repository Candidates`
   Generate repository search queries from paper title, method, datasets, benchmarks, metrics, and cited implementations.
4. `Run Code Verification`
   Clone or inspect repos, record commit hashes, run smoke tests and evaluation commands, and capture logs honestly.
5. `Compare Paper vs Evidence`
   Check whether tables, deltas, rankings, captions, abstract claims, and conclusion claims are supported.
6. `Enforce Evidence-Constrained Revision`
   Produce inconsistency reports, safe rewritten claims, missing-experiment lists, and optional LaTeX patch suggestions.

## Claim Types

Every claim should be classified into one of these buckets:

- `empirical`
- `comparative`
- `robustness`
- `generalization`
- `efficiency`
- `mechanistic`
- `novelty`
- `qualitative`
- `speculative`

Claim type determines the evidence bar. For example:

- `empirical`, `comparative`, `robustness`, `generalization`, and `efficiency` claims require experimental support.
- `mechanistic` claims ideally require ablations.
- `novelty` claims require strong related-work checking.
- `speculative` claims must be softened unless explicitly marked as future work.

## Working Rules

- Preserve scientific fidelity. Do not add unsupported findings, baselines, or conclusions.
- Record the exact manuscript sentence for each claim whenever possible.
- Track scope carefully: full benchmark, subset, seed count, metric definition, and evaluated categories.
- Treat missing robustness tests, missing ablations, and missing variance reports as evidence gaps, not minor wording issues.
- Prefer structured ledgers over free-form opinions.
- Treat failure to reproduce as signal. Do not hide it.
- If numbers differ, calculate both absolute and relative deltas before judging the text.
- Rewrite claims narrowly enough that they are fully supported by the verified evidence.

## Output Modes

- `ledger-only`: claim ledger plus required evidence
- `repo-search`: repository candidate ranking and reproduction plan
- `experiment-runner`: repo setup plus command execution ledger
- `consistency-review`: claim/evidence inconsistency report
- `latex-rewrite`: safe rewritten claims plus LaTeX patch suggestions
- `full-audit`: end-to-end paper-code-experiment review

## Expected Artifacts

This skill may create the following artifacts in a task-local output directory:

- `CLAIM_LEDGER.md`
- `CLAIMS.json`
- `REPO_CANDIDATES.md`
- `REPRO_CONFIG.example.json`
- `EXPERIMENT_LEDGER.md`
- `EXPERIMENTS.json`
- `INCONSISTENCY_REPORT.md`
- `REVISION_PLAN.md`
- `latex_patch_plan.json`

## Scripts

This skill ships helper scripts in [scripts](./scripts):

- `discover_paper_files.py`
- `extract_tex_claims.py`
- `run_paper_audit.py`
- `find_related_repos.py`
- `auto_prepare_reproduction.py`
- `run_reproduction.py`
- `extract_numeric_evidence.py`
- `extract_structured_tables.py`
- `backfill_claim_evidence.py`
- `compare_results.py`
- `check_claim_result_alignment.py`
- `patch_latex_claims.py`

Use them as the deterministic backbone when possible instead of retyping the same audit logic in free-form text.

## Reference Files

Read these as needed:

- [references/review_rubric.md](./references/review_rubric.md)
- [references/claim_schema.md](./references/claim_schema.md)
- [references/experiment_schema.md](./references/experiment_schema.md)
- [references/revision_rules.md](./references/revision_rules.md)

## Quick Start

Typical sequence:

1. Run `discover_paper_files.py` on the paper directory to detect the main manuscript, bib files, tables, figures, and supplemental files.
2. Run `run_paper_audit.py` on the paper directory to build a first-pass manifest, metadata file, claim ledger, GitHub repo candidates, cloned repos, an automatic reproduction config, an experiment ledger, extracted numeric evidence, structured table evidence, and an enriched claim ledger.
3. Review `AUTO_REPRO_CONFIG.json`, `EXPERIMENT_LEDGER.md`, `NUMERIC_EVIDENCE.md`, and `TABLE_EVIDENCE.md` to see whether the automatic probe found runnable eval or test commands and reusable result tables.
4. If needed, tighten commands manually and rerun `run_reproduction.py` for deeper reproduction.
5. Use `CLAIM_LEDGER_ENRICHED.md` and `INCONSISTENCY_REPORT.md` to see which claims now have partial numeric or table grounding and which still need new experiments.
6. If the user wants direct manuscript changes, prepare `latex_patch_plan.json` and apply it with `patch_latex_claims.py`.
