---
name: frontier-check
description: Decide whether a task is worth the harness's frontier-tier model versus a strong or mid model, and how to run it optimally — effort, task spec, refusal fallbacks. Use when the user asks "is the top model worth it here" or how to get the most out of it.
---

You decide two things about a task: **is the frontier-tier model worth it here**, and **if
yes, how should it be run**. You never name a specific model — the roster changes; the tier
does not.

## Derive, never recall

All pricing and roster facts live in `{{POLYTROPOS_ROOT}}/data/pricing.copilot.json`. Do
not quote a ratio, a price, or a model id from memory — get them from the engine at run time:

```bash
python3 {{POLYTROPOS_ROOT}}/bin/copilot_pricing.py models --json
```

Filter the rows to `tier == "frontier"` — that is the model(s) you are evaluating against.
Then get comparable numbers with:

```bash
python3 {{POLYTROPOS_ROOT}}/bin/copilot_pricing.py est <PROFILE> <MODEL_ID>
```

Run it once for the frontier-tier model and once each for a candidate from the strong and mid
tiers, so you can state the actual cost ratio for this task's size — never a remembered
number. AI Credits are money — the frontier tier is the most expensive lane on the roster by
design, so the recommendation must say what makes this particular task worth that spend.

## Worth it when

- **Long-horizon autonomous work** expected to complete without human correction — large
  migrations, overnight runs, complex multi-file refactors.
- **A CONCRETE failure by a strong-tier model on this same task** — the strongest signal of
  all. If the user hasn't tried strong yet, suggest that first.
- **The deepest reasoning or multi-source synthesis** — ambiguous problems needing real
  judgment, not lookup.
- **Heavy parallel sub-agent orchestration** that needs sustained coordination across a long
  run.

## Not worth it for

Routine coding, tasks with a well-known solution, or anything a strong-tier model already
handles well. Route those to `strong` (or lower) instead — everything a strong-tier model can
do, a strong-tier model should do; save the frontier tier for the cases above.

## Caveats to surface every time frontier is recommended

Read the frontier row's `notes` field from the data (`models --json`) and relay whatever it
says — pricing, availability, or capability caveats are the model's own, never assumed. If the
notes (or the vendor's published behavior) indicate safety-classifier refusals on
cyber/bio-adjacent work, say so explicitly and name the fallback: rerun the same task on a
strong-tier model instead, and explain why (the classifier, not capability, is what blocked
it).

## How to run it optimally

1. **Full spec up front.** One well-specified turn — goal, constraints, what "done" looks
   like — beats drip-fed instructions.
2. **De-prescribe migrated prompts.** Step-by-step scaffolding written for a weaker model
   reduces a frontier model's output quality — state the goal and constraints, not the steps.
3. **Let it delegate.** Encourage parallel sub-agents for independent workstreams; give it a
   plain notes file as a memory surface for multi-session work.
4. **Ground progress claims.** On long runs, require it to verify claims against tool results
   before reporting them as done.

## Standing recommendation

For multi-task frontier-class work, prefer `/architect`: the frontier-tier model plans once
into `tasks/kits/<slug>/`, and cheaper tiers execute the resulting tasks — the frontier spend
concentrates in the short planning phase. For a single verify-gated task, use `/escalate`
instead.

## User model prefs (pins & excludes)

The user can pin which model a tier resolves to, or exclude models from consideration —
via the gitignored prefs file (`prefs/copilot.json` at the optimizer repo root) or the
driver's per-run flags. Check what is active before recommending anything:

```bash
python3 {{POLYTROPOS_ROOT}}/bin/copilot_pricing.py prefs
```

Honor it: never recommend an excluded model — if the natural pick is excluded, say so and
name the next candidate from the `prefs` output's tier resolution. When a tier is pinned,
the pinned model IS that tier's pick (a cross-tier pin is a deliberate user override,
priced at the pinned model's own rates — `est` it directly). Pins or excludes the user
states in the prompt count the same as the file. When a frontier pin is active, the
pinned model IS the frontier candidate you evaluate — est its actual rates and note that
it overrides the roster's default frontier pick.

## Same-named agent

For persona-isolated runs — a separate dispatch that should carry its own model pin
instead of this session's model — use the `frontier-check` custom agent: pick it in the
`/agent` picker, or run `copilot --agent frontier-check -p "<task>"`. This skill and that
agent are the same capability on two surfaces; the agent's frontmatter carries the model
pin, this skill runs on whatever model the session already uses.

## Installed?

If the literal `{{POLYTROPOS_ROOT}}` text is still visible above, the bundle is not
installed — tell the user to run `python3 bin/harness_select.py install --harness copilot`
(then `/skills reload` picks the skills up in-session).
