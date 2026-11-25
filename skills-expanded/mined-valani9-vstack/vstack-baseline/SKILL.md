---
name: vstack-baseline
description: Set + verify monitoring baselines for any vstack pattern so subsequent runs can detect drift. Records a healthy run as the baseline, stores it in ~/.vstack/baselines/, and on later runs compares the live detection against the stored baseline to surface only the *changes*.
---

# /vstack-baseline

Two-step workflow: **record** a baseline now, **compare** future detections against it later. Every vstack pattern that supports calibration (most of the 34 do) ships `record_baseline()` and `compare_to_baseline()` helpers; this skill orchestrates them through the user's MCP client.

## When to invoke

- "Set up monitoring for our agent crew."
- "I want to know when this metric drifts."
- After fixes from `/vstack-post-incident` / `/vstack-audit-crew` / `/vstack-bottleneck` land — bank the new healthy state as the baseline.
- Quarterly health-check cadence.
- Before a major change (model upgrade, prompt rewrite, framework swap).

## Preflight

Decide **which patterns** to baseline. Three useful default bundles:

| Use case | Patterns |
|---|---|
| Single-agent quality monitoring | `lewin`, `goleman_ei`, `bias_stack` |
| Multi-agent crew health | `lencioni`, `psych_safety`, `trust_triangle`, `process_gain_loss` |
| Org / structural | `span_of_control`, `org_structure` |
| Culture drift | `schein_culture`, `robbins_culture` |

Ask the user which bundle (or which specific patterns) and what trace they want to baseline against. The baselined trace must be one the user is willing to call **the standard** — a recent healthy run, or the canonical pre-launch run.

## Workflow

### Step 1 — Verify the baselines directory

```
vstack-config path baselines
```

Should print something like `/Users/.../.vstack/baselines/`. If `VSTACK_HOME` is set elsewhere, surface that to the user so they know where files are written.

### Step 2 — Record baselines (one per chosen pattern)

For each chosen pattern:

```
vstack_<pattern_name> with:
  <full trace shape>
  mode: forensic     # depth-mode: baselines deserve the highest-fidelity capture
  baseline_path: <leave empty -- the analyzer writes to ~/.vstack/baselines/<name>.json by default>
```

The analyzer runs normally **and** records the resulting metrics / scores / profile-pattern label to disk as the new baseline. Note: each pattern's `record_baseline()` is invoked transparently when `baseline_path` is supplied; some patterns require explicit opt-in via a `record_baseline=True` kwarg — read the pattern's analyzer signature to confirm.

If a baseline already exists at the same path, prompt the user before overwriting: "There is already a `<pattern>` baseline from <timestamp>. Replace? (y/n)" — never silently overwrite.

### Step 3 — Compare future runs against the baseline (later, on demand)

When the user re-invokes this skill in compare mode (or another skill chains in), each pattern is called with `baseline_path` pointing at the stored file. The analyzer's response then includes a `BaselineComparison` block with per-metric `delta`, `direction`, `significance` fields.

The synthesis shows only the **changes**:

```
## Drift report — <crew name>, <pattern_name>

**Baseline date:** <stored timestamp>

**Metrics that moved:**
- <metric>: <baseline_value> -> <current_value> (Δ=<delta>, sig=<significance>)
- ...

**Profile pattern:** <baseline label> -> <current label> (stable / drifted)

**No-change axes** (collapsed): <count>

**Headline:** <one sentence summarizing the dominant drift>

**Recommended action:**
- If significant drift -> route to the appropriate diagnostic skill (`/vstack-post-incident`, `/vstack-audit-crew`, etc.) on the current trace
- If marginal drift -> re-baseline and document the change
- If no drift -> nothing to do; baseline is intact
```

### Step 4 — Document the baselines

After recording, print:

```
Recorded baselines (under ~/.vstack/baselines/):
- lewin.json           (recorded <ts>, mode=forensic, profile=<label>)
- lencioni.json        (recorded <ts>, mode=forensic, profile=<label>)
- ...

To compare a future run, re-invoke /vstack-baseline in compare mode (or any other vstack skill — they auto-detect baselines at ~/.vstack/baselines/<name>.json).
```

## Failure modes

- **`~/.vstack/` not writable.** Surface the OS error verbatim. Common cause: VSTACK_HOME pointing somewhere with bad permissions.
- **Pattern's analyzer doesn't accept `baseline_path`.** Most do, but if you find one that doesn't (the registry's PatternEntry won't say which), surface the analyzer error and skip that pattern's baseline. The rest of the bundle still records.
- **User wants to baseline a "best ever" run that's not in the trace store.** That's fine — record against any trace they can produce. The baseline isn't a population reference; it's a *named reference point*.

## Composition

- Upstream: `/vstack`, post-fix from `/vstack-post-incident` / `/vstack-audit-crew` / `/vstack-bottleneck`, or a standalone monitoring setup.
- Downstream: nothing automatic. Baselines are read transparently by future skill invocations.
- Compose with: any other vstack skill — they all benefit from baseline-driven drift detection.

## What you don't do here

- Don't record a baseline against a *failed* run by default. The skill recommends a healthy reference; flag explicitly if the user insists on baselining a failure (sometimes useful for regression detection).
- Don't auto-overwrite existing baselines. Always confirm.
- Don't run more than ~5 patterns in a single baseline-recording invocation. Forensic mode × 5 patterns = a lot of LLM calls. Bigger bundles → batch across sessions.
