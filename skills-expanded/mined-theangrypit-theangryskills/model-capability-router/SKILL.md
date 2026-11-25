---
name: model-capability-router
description: "Use when the operator asks for model or reasoning-effort routing using a GPT-only or OpenClaw subscription palette, including a standing request."
---

# Model Capability Routing

Use the host's native model, effort and agent selection. Respect the operator's
selected main model and effort; this skill does not switch an active task.
The edition profiles are policy recommendations. They do not establish the
current host configuration or model selected by a running task; check those
separately before describing them as configured. Choose the execution
arrangement before a delegated worker's model.
Authorization to delegate alone does not require consulting this router.

When this policy is used inside T3 Code, read the conditional
[T3 transport mapping](references/t3-runtime.md) before dispatch. It maps
existing role choices to host capabilities; it does not replace the native
Codex policy or authorize another model, provider or spending route.

## Execution arrangement

Keep small, tightly coupled work and immediate follow-ups with the agent that
already holds the relevant context. A cheaper worker model alone does not
justify a handoff. Batch related operations rather than delegating each one.

When the operator requests delegation, preserve that workflow for suitable
bounded work. Otherwise delegate when the benefit justifies briefing, startup,
coordination, verification and likely correction costs. Reuse a suitable worker
and its relevant context for related follow-ups, without assuming cache reuse.
Give it the context needed for its acceptance checks.

Parallelise independently executable packages with clear ownership when the
benefit outweighs duplicated context and integration costs. Sequence dependent
work. Faster completion and lower consumption are separate benefits.

Continue the current thread when its context remains useful. A fresh task suits
an independent objective; a full-history fork copies history rather than
providing a clean context.

Keep one visible task per coherent outcome. Use native subagents for useful,
bounded work inside that task. Create a separate user-owned task only on the
operator's explicit request, for an independent or durable outcome, a schedule,
or a required host/cloud boundary.

## Choose one edition

| Edition | Palette | When to use |
|---|---|---|
| [GPT-only](references/gpt-only.md) | GPT-6 Astra, GPT-6 Luna, GPT-6.1 Sol and GPT-6.1 Terra | Default for Codex/T3 and any explicit GPT-only request. |
| [OpenClaw subscriptions](references/openclaw-subscriptions.md) | GPT-6.2 Sol/Astra, Luna/Terra and Claude, Composer, Grok, Gemini Argon/Pro/Flash/Flash-Lite | Use in OpenClaw under the operator's standing request for this edition, or when explicitly selected. |

Read the selected edition before making a routing decision. Its role table
replaces the other edition's recommendations; shared execution, authority,
verification and specialist rules below still apply. Neither edition switches
the running agent or rewrites an explicit binding. When the edition is unclear,
retain an existing edition; otherwise use GPT-only. Keep both editions in this
one canonical skill so their shared rules and installation cannot drift.
Select them in ordinary language: "use model-capability-router, GPT-only" or
"use model-capability-router, OpenClaw subscriptions".

The GPT-only edition recommends Sol high for coordination, Astra medium for
judgment, Luna high/xhigh/max for bounded execution, and workload-specific Terra
efforts. The OpenClaw edition has its own version choices: see the
[GPT-6.2 pricing and role review](references/gpt62-20261117.md). It adds
task-specific choices without requiring a provider handoff or enabling new
billing routes. The GPT-only edition and its pstack presets are unchanged.

Choose directly for the task. Use an Astra → Sol → Luna sequence only when
coordination materially helps the outcome; a direct bounded worker or the
current agent is enough when it does not. There is no mandatory model ladder,
failed-attempt retry, coordinator stage, automatic planning/review delegation,
CLI resolver, receipt workflow or mandatory preset wrapper. Requested planning
or review delegation remains available when suitable. Importance alone does
not justify XHigh. A read-only task can still need Astra. Patch size alone does not prove
that Luna suits autonomous systems administration.

Luna Max is available when justified by the work; it requires no repeated
approval merely for that effort. Choose effort for the workload; higher effort does not guarantee better results.
GPT-6 supports cache-preserving effort updates through its documented mechanism;
do not assume every client uses it or that cache is shared across models or tasks.
For the Terra workload and effort tradeoffs behind these profiles, consult
[references/gpt61-terra-20261028.md](references/gpt61-terra-20261028.md).
The GPT-6.1 Sol launch evidence is in
[references/gpt61-sol-20260929.md](references/gpt61-sol-20260929.md). The
historical GPT-6 evidence remains in
[references/gpt6-20260922.md](references/gpt6-20260922.md). These profiles do
not authorise new spending routes, external actions or additional access. Astra
Max and Ultra are outside the habitual GPT-only palette. Other supported models remain
available when selected by the operator or bound to a specialist.
Honour explicit selections and fixed bindings, including those outside this
palette.

For GPT-only pstack's three role-aware presets, use the single canonical mapping in
[references/pstack-role-presets.json](references/pstack-role-presets.json).
Equilibrado is the default for unbound roles in a new setup with no existing
role choices. Economia, Equilibrado and Power preserve explicit model/effort
choices, panel lists, aliases, named specialists and the operator's selected
main model/effort. Show a preserved binding that differs from a preset as an
explicit override. If a requested model or effort is unavailable on its
channel, keep it unchanged and mark it as needing a choice. Select either a
role-aware preset or one upstream global budget; never apply the global effort
target over a role-aware preset.

The OpenClaw edition does not rewrite these GPT-only pstack presets. Select
its task-specific roles directly; preserve existing preset and specialist bindings.

## Changing selection during work

Keep the selected edition's recommendation (Sol high for coordination) and choose
task-specific overrides through the native surface that actually supports them.
Honor an explicit native effort selection, including low; this recommendation
does not require changing a home configuration or an active thread. In CLI,
`/model` changes model and
supported effort within a session. A task follow-up tool may expose model and
effort overrides; use them only when that tool supports the target. Do not
message the current task recursively to simulate self-switching. The current
agent cannot claim to change its own model without an exposed control and
confirmation. Use the existing bounded specialist delegation when suitable.
Changing `config.toml` sets a default, not proof that an active turn switched.

## Runtime and delegation

Before selecting compute, check the exact channel's current advertised models
and efforts. Current-task, native-subagent and user-owned-task support differ.
Do not invent unsupported capability, create a task to work around it, or
silently substitute. Report the gap and continue locally when the existing
selection can meet the proof bar; otherwise surface the specific decision
needed.

For permitted delegation, give bounded ownership, relevant context, expected
output and verification requirements. A differently modelled native worker
needs fresh or bounded context: full-history forks inherit the parent model.
Respect actual available slots; a concurrency ceiling is neither a target nor
permission to spawn.
Do not make specialists coordinators or enable recursive delegation implicitly.
The coordinator integrates and verifies the result.

Creating a user-owned task, forking, moving or archiving tasks still requires
the corresponding explicit user request. Routing grants no authority over
hosts, accounts, private data, credentials, publication or destructive actions.
Respect native approvals and refusals. Do not force feature flags.

Before accepting a delegated deliverable, check the requested elements against
the actual result and verification evidence. Concise reporting must not remove
required work or presentation quality. Correct omissions before delivery;
change the assignment or model when observed failures justify it.

## Cost and evidence

Compare the remaining whole task, including parent and worker input, output,
briefing, startup, coordination, verification and rework. Reusing a relevant
worker can save context transfer; cached input is possible, not guaranteed
across tasks, models or changed prefixes. Do not add speculative cache
retention, keepalive prompts or repetitive polling merely to preserve context
or show activity. Count reasoning and child usage once if a meter already
includes them. API token prices and benchmarks inform comparisons but do not
measure this account's Codex or provider subscription allowance or prove a routing saving. Use observed
account usage or a like-for-like native task comparison for such claims; state
when that evidence is unavailable. Keep changing prices and benchmark scores
out of durable profile rules. The [November benchmark refresh](references/benchmarks-20261106.md)
records current comparisons and their limitations. Subscription routing uses
the existing authorized provider account and its actual allowance, supported
models, effort controls and cooldowns. API prices are contextual evidence;
subscription access is not unlimited or proof that an API route is included.

## Installation and updates

The sole install source is `TheAngryPit/TheAngrySkills`, not Workbench.

```bash
npx skills add https://github.com/TheAngryPit/TheAngrySkills.git -g -a codex -y -s model-capability-router
```

Use one canonical installed skill per OS user, shared by Codex profiles through
native discovery or links. A profile link is not a second independent version.
Keep source metadata pointed at the normal repository. `npx skills` records
update provenance; it does not provide an automatic update schedule. Inspect
the installed CLI's update/check behavior before using it as a read-only check.

## Native named-agent profiles

This skill is also the public distribution surface for the native named-agent
profiles used by the adapted pstack workflows:

- `assets/agents/comment-sicko.toml` is the named reviewer for
  `cursor-no-comments`.
- `assets/agents/poteto-agent.toml` is the named delegate for
  `cursor-poteto-mode` playbooks.

Keep these pstack specialist identities, ownership and verification contracts
when the profiles are used; model routing does not flatten named roles.

The assets are not loaded merely because this skill is installed. To make the
profiles selectable by a new Codex session, run the bundled checked installer
from this skill directory:

```bash
python3 scripts/check-native-agent-profiles.py \
  --install --installed-dir ~/.codex/agents
```

The bundled script travels with an individual skill installation; it does not
depend on the repository-level `scripts/` directory.

The command refuses to replace a differing existing profile unless
`--replace` is supplied explicitly. Run it again with only
`--installed-dir ~/.codex/agents` for a byte-for-byte check. This validates
distribution and configuration, not that a newly started session has loaded or
selected the profile; that must be checked by the host session.

## Additional Cursor source profiles

The profile assets also preserve Dylan, Advisor, compatibility review, continual-learning, plugin architecture, CI watching, and Thermos roles. `sources/cursor-plugins/agent-coverage.json` in the source repository records all 14 upstream agent mappings and their hashes. Source distribution is not installation or fresh-session loading. The existing checked installer above selects the two Pstack profiles; other assets remain separately selectable source profiles and must be explicitly installed and proven on the target host. Missing exact native types are reported, never claimed from these files alone.
