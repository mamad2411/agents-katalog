---
name: optimal-subagents
description: Choose the right model and coordinate subagents for research, coding, documents, analysis and independent plan review before action. Covers delegation, model evidence, workload-specific comparisons and refreshing recommendations as models change.
---

# Optimal subagents

Read this entrypoint at each session start when required by host instructions.
Use it to decide whether delegation helps; reading it does not require spawning.
Keep the current user's scope, exact model requests and required review gates.
The parent chooses each child's model and effort; these task-specific choices
are not installation-wide subagent defaults. Pass them explicitly for fresh
and partial-history children. Choose full native history inheritance deliberately.
This guide does not replace the installed pre-commit-review procedure. Its
[review routing source](references/reviews.md) is bundled unchanged in that
plugin; the installed review plugin's release copy governs a running review.

## Decide before spending

1. Work locally by default; a trivial, quick or tightly coupled task stays local.
   Delegate a concrete, bounded part when it improves the expected result:
   a better-fit model or an independent check raises quality, the parent cannot
   meet the capability floor, or the part runs independently of the parent's
   live context and overlaps useful parent work, keeps bulky output out of the
   parent context, or needs a separate tool or write boundary. The brief, the
   fresh-context child, the result read and parent verification must return more
   in quality, time or context than they consume; cost is one factor, not the
   test. If the parent is the wrong fit for most of the task, say so and ask the
   user to change the session model rather than relaying the whole task.
2. Identify the capability floor: tools, modality, context, reliability and
   consequence of error. Check the active runtime's callable tools and catalogue.
   A picker entry, an accepted spawn and a verified served model are different.
3. Select by model capability and comparable published cost, independent of
   subscriptions, account plans or billing routes. Never promote a model because
   it appears free under a plan. Resolve its callable identifier after selection.
4. Choose the cheapest eligible model and effort likely to pass the task's acceptance check.
   Include parent context, reasoning/output, retries and verification in cost.
   A cheap failed attempt followed by a full redo can cost more than one capable
   attempt. Use observed task success when available, not token prices alone.
5. Start with one child; add parallel children only for independent work that
   saves useful time. Avoid duplicate recon, ceremonial reviewers, and asking
   every child to reread the entire conversation. Required review lanes still run.
6. For department work, brief the child with its department skill: [sales](../sales-subagent/SKILL.md),
   [CSM](../csm-subagent/SKILL.md), [support](../support-subagent/SKILL.md),
   [finance](../finance-subagent/SKILL.md), [operations](../operations-subagent/SKILL.md).
   The brief sets role, inputs, authority and acceptance; this skill still owns model choice.

## Current starting choices

Evidence checked **2026-11-11**, using Artificial Analysis Intelligence Index
v5.0.1. These are task-specific public-evidence priors, not local proof.
Read [the catalogue evidence](references/catalogue.md) when selecting a model;
refresh live prices before material spend, long runs, or relying on a promotion.

| Work | Starting point | Escalate when the acceptance check needs it |
| --- | --- | --- |
| Bounded text extraction, simple edits, recon | Muse Ember `max` for supplied-source, checkable work; GLM Flash `max` is a cheap fixed-token alternative | Terra 6.1 `high` for a higher capability floor; Luna `max` for small mechanical helpers |
| Repository investigation, scripts, bounded implementation, tool workflows | Ember `max` for investigation; Terra 6.1 `max` for implementation | Sol 6.1 `max`; Kimi K3.1 Pro `max` or Carbon `high` for difficult terminal work. DeepSeek Flash **1017** `max` is economical for tightly specified slices |
| Synthesis and business documents | Ember `max` for source-grounded prose; Sol 6.1 `high` for complex synthesis | Sonnet 5.5 `max` for demanding polished deliverables; Opus 5.5 `max` for a demonstrated gap. Muse Spark/Wonder remain candidates, not blanket defaults |
| Independent review of a proposed plan before action | Muse Ember `max` for bounded plans; read [planning advisor](references/planning.md) | GPT-6.1 Sol `max` for intricate reasoning; domain-specific requirements still apply |
| UI and frontend | Carbon `high` for design direction; DeepSeek Flash 1017 or Terra 6.1 `max` for agreed implementation | Opus 5.5 `max` for a demonstrated visual gap. Qualify taste with rendered references; Fable 5.2's Arena result is at `xhigh`, not `max` |
| Images and multimodal reasoning | Verify actual input support; Gemini 3.8 Flash `high` or GPT-6.1 Terra `max` | Gemini 4 Carbon `high` or Astra `max`; use modality-specific checks, not text scores |
| Long-document extraction | DeepSeek Flash 1017 or GPT-6.1 Terra `max`, with citations and spot checks | Kimi K3.1 Pro `max` for demanding long-context reasoning; check the active route's context limit |
| Pre-commit review | Use the installed review skill and its bundled model routing | Apply its authorized fallbacks; exact user requirements still take precedence |

**Cybersecurity exception:** read [security model selection](references/cybersecurity.md)
before assigning any cybersecurity work, including defensive analysis, pentesting,
incident response, vulnerability research or a security acceptance decision.
Establish accuracy, scope and usable access first;
then optimise cost among qualifying models. The cheapest general-purpose row is
not the default for high-consequence security work. This does not change the
installed pre-commit review policy.

For persistent owners, combined roles, or a project roster, read
[roster model selection](references/roster.md). It separates leadership from
cheap worker jobs, gives role-specific model/effort candidates, qualifies
visual taste, and distinguishes roster choices from actual chat settings.

**Select effort with the model:** use an explicitly supported, evidenced pair.
The catalogue table gives comparison defaults; role guidance also uses separately
measured Sol `high`/`xhigh` and Terra `high`. Never apply a max score to a high
request, silently downgrade an assigned effort, or assume max is always best
value. Native GPT-6 Sol is a different version from GPT-6.1 Sol. Do not use an
automatic delegation mode such as `ultra` for a bounded child or invent an effort.

Pre-commit reviews use their separate model-agnostic review policy, including
configured supported effort; these general task choices do not constrain them.

**Muse policy:** standard 1.3 uses `max`. Treat its `xhigh` evidence as a similar
practical tier, per user preference, while preserving the separate measurements.
This is not a claim of equal scores, latency or billed reasoning.
Contributor (`meta/muse-spark-1.3-contributor`) uses `xhigh`: $0.10/$0.20
per million input/output tokens on 2026-11-11, but its own benchmark identity
is unverified and its terms permit training use. Use it only when that data use
is acceptable and a representative task check passes. Never transfer standard
Muse scores to Contributor or silently replace the requested route.

Effort names are provider-specific. If the selected level is unavailable,
report that constraint and select another eligible model; do not silently
change the level or borrow another effort's benchmark score.

For an unavailable model, read [fallback orders and failure handling](references/fallbacks.md).
Use the workload's next eligible model at its fixed effort, preserve acceptance
checks and data constraints, and report material substitutions. Stop model
cycling for a shared transport failure or an exact-model review gate.

## Run a bounded delegation

MANDATORY: before the first spawn in this session, read your runtime's part of
[tool operation and communication](references/tool-guide.md) in full, and
re-read it when acting as a child. No delegation without it: the entrypoint
alone does not authorize a spawn. Claude Code reads the Claude Code section,
because the Codex collaboration tools and fork options do not exist there.
Codex reads the Codex sections, which include exact examples for the current
collaboration tools, fork restrictions, replies, waiting and failure handling.
Codex's `ALL_TOOLS` lists exec-callable tools, not every native tool. An empty
search there does not prove that delegation is unavailable. Read the current
native definitions and the guide's discovery section before reporting a blocker.
On the mixed-provider Codex route, if `collaboration_plaintext` handoff tools
are offered, use them for every subagent assignment, message and follow-up,
whatever the recipient. Otherwise use the `collaboration` tools. Pass model and
reasoning_effort explicitly; external children need `fork_turns="none"`.

When the active client cannot spawn the selected router model as a native
child, as in a Claude desktop Code session in the subscription profile, run
it with [router workers](../router-workers/SKILL.md). Model choice, briefs
and verification stay as described here.

Give each child: one deliverable, relevant context/paths, write authority,
acceptance checks, cost/retry limits where useful, and a stop condition. One
writer owns each worktree/delivery stream; parallel agents must not edit the same
files or shared browser. Default children to no recursive delegation.

Start every initial or follow-up assignment message with the requested model,
effort, role/pass and task or plan context. For example: "GLM 5.3 Flash Max —
Parser investigation for the empty-input fix." Use the actual
selected model and a real task identifier; do not invent a plan number. Repeat
the label in a file-based brief. This labels the request, not verified serving
identity; keep recording the returned identity separately.

Keep parent work moving. Verify material claims and artifacts yourself before
integration. For an unexpected failure, distinguish transport, authorization,
identity, provider and task-quality errors. One diagnostic retry is usually
sufficient for a deterministic pre-inference failure; do not buy repeated calls
that cannot reach the task. Preserve exact required model gates.

Close or release finished agents if the runtime exposes that operation. Report
what was verified, remaining gaps, and material model/cost substitutions; do not
claim a spend total without actual usage evidence.

## Refresh the guide

Read [refresh methodology](references/refresh.md) to add models, update prices,
recompute workload-specific Pareto frontiers and validate new recommendations.
The bundled [evidence snapshot](references/model-evidence.json) is dated public
research. [pareto.py](scripts/pareto.py) computes reproducible candidate sets;
it does not make network calls or infer missing model scores.

This skill ships with the SCG router, which delivers and refreshes it; see
[automatic updates](references/updates.md). There is no per-plugin updater or
schedule to configure. Respect explicit read-only scope.
