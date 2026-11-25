---
name: skillx-full-loop-audit
description: Use when operating SkillX full-loop experiments after an inner-loop run completes, especially to audit result validity, classify failures, decide required/recommended reruns, prepare targeted rerun manifests, or determine whether it is safe to proceed to outer-loop optimization.
---

# SkillX Full-Loop Audit

Use this skill after a SkillX inner-loop launcher finishes and before any
outer-loop assignment or schema rewrite consumes the results.

## Core Rule

Run the deterministic audit script first. Do not manually classify pair validity
from dashboard impressions alone.

```bash
python3 scripts/audit_skillx_inner_loop_results.py \
  --materialized-root <materialized-root> \
  --run-label <inner-run-label>
```

The generic outer-loop wrapper already runs this audit by default:

```bash
scripts/run_skillx_outer_loop_step.sh <inner-run-label> <outer-label> <next-materialized-root>
```

By default, the wrapper stops before outer-loop work if `rerun_required > 0`.

## Audit Outputs

Look under:

```text
<materialized-root>/reports/<inner-run-label>/inner_loop_audit/
```

Key files:

- `inner_loop_audit.md`: human-readable classification and rerun rationale.
- `inner_loop_audit.json`: source-of-truth structured audit.
- `required_pair_manifest.json`: pair ids that must be rerun.
- `recommended_pair_manifest.json`: pair ids that should be rerun if cost allows.
- `run_required_rerun.sh`: tmux launcher for required reruns.
- `run_all_flagged_rerun.sh`: tmux launcher for required plus recommended reruns.

## Decision Policy

- `required`: do not feed this result into outer-loop unless the user explicitly
  overrides. Rerun first.
- `recommended`: result may contain useful signal, but a clean rerun is preferred.
- `none`: no rerun needed by default.

Required examples:

- failed run with missing R0 tune_check trial dir.
- completed run whose later rounds failed and selected score is zero.
- basic/Codex fallback when the intended executor family should stay fixed.
- stale or incomplete launcher/run artifacts.

Recommended example:

- completed run with runtime failures, but a later clean selected round has
  positive reward.

Non-rerun notes:

- Claude account fallback alone is not a model-family change.
- hard rate-limit fallback alone is not a rerun reason if final evidence is complete.
- `skipped_baseline_perfect` is an intentional guard outcome.

## Rerun Procedure

For the minimum repair set:

```bash
bash <audit-dir>/run_required_rerun.sh
```

For both required and recommended pairs:

```bash
bash <audit-dir>/run_all_flagged_rerun.sh
```

After the rerun finishes, rerun the audit on the effective run output before
starting the outer-loop step.

## Reference

For the observed round1 examples that define the current policy, see:

```text
docs/plans/skillx/full-loop-post-inner-audit-reference-v0.1.md
```
