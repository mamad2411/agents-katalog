---
name: effort
description: Control the reasoning-effort dial for Copilot models — Copilot's per-model "Reasoning" setting, covering which models have it, how to set it, and when to turn it up or down. Use when the user asks to raise/lower reasoning effort, run at extra-high, or make a model think harder or cheaper.
---

You control Copilot's reasoning-effort dial: the per-model "Reasoning" setting in the `/model`
picker. You teach the real, confirmed mechanism, and you are honest about what does not exist.

## Get the ladder from data — never from memory

The level vocabulary is DATA, not something to recall. Run:

```bash
python3 {{POLYTROPOS_ROOT}}/bin/copilot_pricing.py knobs
```

Relay exactly what `knobs` prints — the confirmed level names and every mechanism/note string,
straight from `data/pricing.copilot.json`'s `knobs` block. Copilot's display words in the
picker are Title-Case — these are NOT the lowercase tokens other CLIs use for the same
underlying ladder; never mix the two vocabularies, and never enumerate the ladder yourself
from memory — always shell out first.

## The mechanism (the only confirmed one)

Reasoning effort is set INTERACTIVELY, in the `/model` picker:

1. Open `/model` and select the model row you want.
2. Use the left/right arrow keys to cycle its Reasoning value (the picker footer literally
   says "←/→ reasoning effort").

This is a per-model property, not global. Some rows show `—` in the Reasoning column and have
no dial at all — the `knobs` note lists which rows were observed with and without one.

Copilot CLI v1.0.83 and GitHub's CLI command reference confirm both `--effort=LEVEL` and
`--reasoning-effort=LEVEL` for direct/headless runs. Valid token values are `low`, `medium`,
`high`, `xhigh`, and `max`; obtain their display labels from the data's `knobs` block rather than
from memory. The repository's `copilot_execute.py` does **not** forward either flag today, so an
execution-kit run cannot select effort through that driver. Say that limitation plainly; do not
claim the driver supports a flag it does not pass through.

## When to turn it up or down

- Leave the model's default for routine work — don't start at the top.
- Step UP one level at a time, only on concrete failure evidence from the current level: a
  wrong answer, a missed constraint, a shallow pass on a hard problem. Never jump straight to
  the deepest level "just in case."
- Step DOWN for bulk, latency-sensitive, or trivially easy work.

Higher effort means the model spends longer thinking and emits more output tokens — and AIC are
real money, not a bill-free subscription unit: every credit costs
`billing_unit.usd_per_credit` per `data/pricing.copilot.json`. Before turning effort up on an
expensive task, size the stakes:

```bash
python3 {{POLYTROPOS_ROOT}}/bin/copilot_pricing.py est <PROFILE> <MODEL_ID>
```

That estimate is per-run token volume at the model's base rates; a higher reasoning effort
inflates the output-token side of it, so treat the printed number as a floor, not a ceiling.

## Relationship to model choice

The effort dial is orthogonal to picking a model. For "which model should this task run on,"
use `/route`. For verify-gated climbing to a stronger tier on failure evidence, use
`/escalate`. Turning effort up on the model you're already on is usually the cheaper move —
reach for it when the model has the right capability but needs more thinking time; reach for a
tier jump only when the gap is capability, not thinking time.

## Same-named agent

For persona-isolated runs — a separate dispatch that should carry its own model pin
instead of this session's model — use the `effort` custom agent: pick it in the `/agent`
picker, or run `copilot --agent effort -p "<task>"`. This skill and that agent are the
same capability on two surfaces; the agent's frontmatter carries the model pin, this
skill runs on whatever model the session already uses.

## Installed?

If the literal `{{POLYTROPOS_ROOT}}` text is still visible above, the bundle is not
installed — tell the user to run `python3 bin/harness_select.py install --harness copilot`
(then `/skills reload` picks the skills up in-session).
