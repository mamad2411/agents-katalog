---
name: vulnbench-benchmark
description: >-
  Score an AI security harness's findings against vulnerability ground truth
  (Cyber Harness Eval / vulnbench). Use when asked to run the vulnbench
  benchmark, benchmark or evaluate a cyber/SAST/pentest harness, score a Mantis
  historical_learnings.jsonl or finding-object file, build the ground-truth
  datasource, or check the harness accuracy / regression. Covers setup, build,
  score, and verify.
allowed-tools: Bash, Read, Grep, Glob
---

# vulnbench — benchmark a cyber harness

All actions go through one entrypoint: `labs/b2.10-eval-harness/scripts/vulnbench.sh`. Run it from the
repo root. Do not hand-roll the Python invocations — the entrypoint keeps every
agent (Claude Code, Copilot, humans) running the identical steps.

## Steps

1. **Check prerequisites.**
   ```bash
   labs/b2.10-eval-harness/scripts/vulnbench.sh doctor
   ```
   If it reports the venv or checkov missing, run `labs/b2.10-eval-harness/scripts/vulnbench.sh setup`
   (creates `.venv`, installs `pyyaml checkov anthropic jsonschema`).

2. **Build the ground truth** (only if `doctor` says the datasource is not built
   — this clones the vulnerable repos on first run, ~552 rows):
   ```bash
   labs/b2.10-eval-harness/scripts/vulnbench.sh build
   ```

3. **Score the harness's findings.** The findings file is JSONL in Mantis's
   `historical_learnings.jsonl` schema or the richer `finding` object.
   ```bash
   labs/b2.10-eval-harness/scripts/vulnbench.sh score --findings <path/to/findings.jsonl> \
       --harness <name> --run-id <id> --gt-source secllmholmes-handcrafted --min-acc 0.80
   ```
   - `--gt-source`: `secllmholmes-handcrafted` | `secllmholmes-realworld` | `terragoat` (omit to score all).
   - `--min-acc <t>`: non-zero exit if Expert Accuracy drops below `t` (use in CI).
   - `--judges`: real Anthropic judges (needs `ANTHROPIC_API_KEY`); offline heuristic otherwise.
   - `--no-validate`: skip the google/mantis schema check.

4. **Sanity-check the pipeline** anytime with the shipped fixture — must print
   Expert Accuracy `0.9479` and the planted CWE-22 miss / CWE-476 wrong-CWE /
   CWE-89 false positive:
   ```bash
   labs/b2.10-eval-harness/scripts/vulnbench.sh verify
   ```

## Reading the result
Report the **Expert Accuracy** (headline), the **by-CWE** table (where it fails),
and whether the run passed `--min-acc`. Distinguish **conformance** (schema
validity, ~100%, structural) from **accuracy** (correctness) — never quote
conformance as quality. If `score` exits non-zero, that is a regression: surface
it, don't hide it.

## When there is no findings file yet
If the user wants to benchmark a *model as the harness* (blind audit), use the
`vulnbench-blind-audit` skill instead.
