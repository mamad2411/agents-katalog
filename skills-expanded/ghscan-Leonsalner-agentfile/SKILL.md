---
name: consult
description: Mandatory before any advisor call. Loading never authorizes a call. Trigger, budget, batching, route, independence, and failure rules.
---

Load before placing any consult call. Loading this skill never requires or authorizes a call. Resident core owns triggers and the workflow-wide budget; this skill enforces the call.

## Evidence vs consult

Consult = a directly observed fresh read-only advisor CLI process or isolated harness subagent launched by the actual executing stage owner. Fix its role and freeze its launch specification before launch. Never reuse the executing process or retrospectively count a worker as an advisor.

Evidence = deterministic tool or document output carrying no model judgment. Provenance decides, not reproducibility.

| Thing | Counts |
|---|---|
| Fresh advisor CLI or isolated advisor subagent, executing owner | consult; label provider diversity and transport |
| Cross-provider advisor | consult with provider diversity; no guarantee of independent reasoning |
| Fresh same-provider advisor | labeled non-independent fallback; cannot satisfy cross-provider requirements |
| Deterministic tool or document output, no model judgment | evidence |
| Worker subagent | delegated model output, neither deterministic evidence nor a consult |
| Reused executing process or own-model effort bump | tool, never a consult |
| Unsure whether trigger or budget permits a call | do not call; resolve state or ask the user |

## Models

Permitted consult models are {{.AdvisorModels}}.{{if .Codex}} Astra requires explicit model-specific user approval for the scope; ordinary batch/attempt capacity is insufficient.{{end}} {{.NonAdvisors}}

## Frozen launch specification

For either transport, record provider, model, effort, permissions, and route before launch. Establish the executing provider from launch metadata or harness evidence, not a model’s self-description or inherited sender identity. If unknown, record independence as `unknown`; it cannot satisfy a cross-provider requirement. Ambient system/repository instructions may remain shared; fresh context means no inherited conversation transcript, not guaranteed independence.

For a harness advisor, use a new child with conversation inheritance disabled, the compact packet below, and read-only tool permissions. Prefer no tools when the packet contains all evidence; otherwise allow only required read tools. Disable shell/write/delegation tools for advisors. If the harness cannot supply that isolation and permission boundary, use a CLI route instead. Freeze the spawn arguments and record the returned child ID; wait for the report. Do not send follow-up review requests to that child.

### CLI argv

Never a shell function or alias.{{if .Codex}}{{if .Windows}} For OpenAI, choose one permitted literal model/effort pair and write both literally into the command; do not take either value from the environment.{{else}} For OpenAI, first bind one permitted literal pair in the same shell invocation; do not inherit either value from the environment:

```
ADVISOR_MODEL=gpt-6-sol
ADVISOR_EFFORT=medium
```
{{end}}

Use `gpt-6-sol` with `medium`, `high`, `xhigh` or `max`, or `gpt-6-astra` with `low` or `medium`, exactly as selected under **Advisor selection**.{{end}}{{if .Claude}} Opus 5.5 may use low for a narrow, bounded, checkable question, medium otherwise, and high only for demonstrated hard analysis.{{if not .Windows}} Bind its selected literal effort separately in the same shell invocation; replace the example value when low or high was selected:

```
OPUS_EFFORT=medium
```
{{end}}{{end}} Then use the matching exact launch line:
{{if .Windows}}
```
{{if .Claude}}claude -p <prompt> --model opus --effort <effort> --tools "" --strict-mcp-config --no-session-persistence
{{end}}{{if .Codex}}codex exec -s read-only --ephemeral -m <model> -c model_reasoning_effort=<effort> <prompt>
{{end}}```

Pass the prompt as one argument and close stdin: in PowerShell pipe `$null |` into the command; in cmd.exe redirect `< NUL`. Do not interpolate the prompt through an unquoted variable.
{{else}}
```
{{if .Claude}}command claude -p "$PROMPT" --model opus --effort "$OPUS_EFFORT" --tools "" --strict-mcp-config --no-session-persistence < /dev/null
{{end}}{{if .Codex}}command codex exec -s read-only --ephemeral -m "$ADVISOR_MODEL" -c model_reasoning_effort="$ADVISOR_EFFORT" "$PROMPT" < /dev/null
{{end}}```
{{end}}
{{if .Claude}}The Claude line disables tools and MCP; include the necessary evidence in the packet. {{end}}Set effort to the selected permitted level explicitly. For other advisor transports, use an enforced read-only boundary and disable recursive delegation where supported; instructions alone do not establish isolation.

Prompt goes in argv, never on stdin{{if .Codex}} — piped stdin can hang `codex exec` at exit 0{{end}}. Always close stdin.{{if .Claude}}
For `claude`, the prompt must bind to `-p` *before* `--disallowedTools`: that flag is
variadic and will otherwise eat the whole prompt as deny rules and exit non-zero.{{end}}
Exit 0 does not prove completion — confirm the expected final report is present.

## Prompt preamble

Every consult prompt opens with exactly:

`read-only consult; do not spawn advisors or subagents; do not call or reuse the executing process; do not recurse; you are not a workflow stage; do not load workflow skills or write handoffs.`

Then pass one compact batch packet: the decision checkpoint, every then-known eligible question across all of its boundaries, named alternatives, relevant local evidence/checks, consequences of error, and expected report shape. Include handoff fields only when relevant. Restate the recursion and executing-process bans because the packet may mention advisor commands.

## Call scope

Before calling, confirm a resident-core trigger, remaining completed-batch capacity, and remaining attempt capacity. No trigger or no capacity means no call. Unsure means do not call. If original state is conflicted, a separately explicit exact grant may fund only its specified calls; original allowance remains frozen.

Unused capacity is not a reason to call. If a specific eligible trigger exists but capacity is exhausted, emit `GRANT REQUEST: <scope> +<batches> batch(es)/+<attempts> attempts — <specific trigger>`. Continue safe independent work while the request is pending. A grant approved after a stage change remains usable later in the same scope, subject to its restrictions; it never retroactively authorizes an already-issued launch.

{{if .Codex}}For Astra, also require an explicit model-specific grant. Emit `ASTRA REQUEST: <scope> — <specific frontier need>` without launching it. No reply or a refusal means only that Astra is not granted: spend no attempt, keep eligible {{if .Both}}Opus/Sol{{else}}Sol{{end}} routes, and continue safe work. It is a blocker only when the underlying unresolved Consequential boundary independently requires advice that no granted suitable route can provide.{{end}}

One batch covers one decision checkpoint and contains every then-known eligible question across all of its boundaries, named alternatives, relevant local evidence/checks, consequences of error, and the required report shape. Do not pass irrelevant handoff material. Single-issue calls are forbidden when other eligible questions are already known.

### Dual Monotonic Ledger

Keep one durable owner-maintained ledger per scope, outside disposable worktrees. Record its path in handoffs and embed its complete accounting state so the next owner does not depend on local file access. Only the owner issues advisor launches; workers never consult or recursively delegate. CLI launch requests and advisor-subagent spawn requests share the same counters. Worker spawns do not consume advisor allowance; record their role in delegation state.

- `attempts_started`: record +1 **before issuing a launch request**. Once issued, it is spent even if spawning fails, the request is malformed, a usage limit or auth rejects it immediately, or the process times out, crashes, or is cancelled. Preflight validation that issues no advisor launch spends nothing. An interrupted/uncertain issued launch is never refunded or repeated as free. This is a launch limit, not token accounting; internal CLI retries do not create new owner launches and are not bounded by this counter.
- `completed_batches`: increment once when a batch delivers substantive advice addressing any bundled question, including a conclusion, recommendation, or analysis. Agreement, acceptance, claimed non-reliance, exit code, and presence of a final marker do not control the charge. Boilerplate, progress messages, and infrastructure errors alone are not advice. Record partial output as `partial`, with only its actual coverage. Substantive advice closes the batch: no fallback to complete or improve it. If uncertainty about substantive content cannot be resolved from captured output, freeze remaining allowance rather than claim a free retry.
- A no-advice failure spends only an attempt. One batch permits one initial launch plus at most one fallback, within both global caps. A batch exhausted without advice is terminal but leaves completed-batch capacity unspent. Never reopen it by renaming the batch or changing stage/provider.
- Persist outcome, observed exit status or why absent, failure classification, report status, coverage, and updated counters after each attempt. Never silently reset either counter. If history is missing, contradictory, or protocol-violating, retain it and freeze original remaining allowance until evidence resolves it. Explicit additional grants are separate, exact batch/attempt additions with route and fallback restrictions; they never repair or reset prior history.

A later call needs independently obtained local evidence materially changing a decision or uncovered consequential boundary, or an explicit new user request. Advisor disagreement, advisor-generated questions, rephrasing, question-splitting, a new stage/session/owner/model/provider, elapsed time, unused capacity, or skill reload never authorizes another call. Never seek votes. Partial coverage never satisfies a required full review or clears unresolved uncertainty immediately before a Consequential action.

Raising effort on the owner's own model never substitutes for a missing consult.

## Advisor selection

After confirming trigger, batch, and budget, apply the `routing` skill's **Advisor route** rules. Freeze its ordered candidate list before attempt 1; do not reorder it during the batch.

{{if .Both}}Both Claude and Codex owners prefer cross-provider advice. Either may use a fresh same-provider advisor as fallback unless cross-provider review was explicitly required, preferring an eligible harness subagent over a CLI.{{else}}Only {{.OnlyProvider}} models are selected: every advisor is a fresh same-provider advisor, preferring an eligible harness subagent over a CLI. An explicit cross-provider requirement cannot be satisfied; stop and ask.{{end}} Record actual provider/model/effort, transport, launch specification, child ID when applicable, and `cross-provider|same-provider fallback|unknown` in history.{{if .Both}} For an explicit cross-provider requirement, exclude same-provider and unknown-independence candidates. If required cross-provider review cannot be completed adequately, stop-and-ask; do not label it skipped.{{end}} A changed boundary removes newly ineligible frozen candidates and never adds replacements.

## Timeout / fallback

A timeout has no observed exit status unless a later exit is actually captured; record both events if that happens. Missing/truncated expected output is incomplete even at exit 0. Neither proves provider or allowance unavailability. Apply the ledger first: substantive partial advice closes and charges the batch, with limited coverage. The fallback rules below apply only when no substantive advice was received. Stop or confirm termination of the prior process or child before launching a fallback. A harness tool error is not proof the child stopped; if liveness cannot be resolved, do not launch a fallback. Record harness completion/error/cancellation state and `exit status: n/a (harness)` instead of inventing a process exit code.

Timeout or incomplete output may advance once to the next frozen candidate, only while global attempt capacity remains. The issued launch request spends another attempt. Never add a candidate, reuse the executing process, retry an attempted route, or call an unsuitable route merely to exhaust budget. Substantive advice completes the accounting charge; a valid but disagreeable report is not failure and cannot trigger fallback.

With no frozen candidate left, the consult is terminal. Record the last observed failure's status, `timeout exhausted` or `incomplete output exhausted`, with the reason no alternate remains; keep every prior attempt and its evidence. {{if .Both}}A cross-provider failure may fall back to a frozen same-provider candidate only without an explicit cross-provider requirement; that result is non-independent.{{end}}

Where continuation is already permitted, label `CONSULT: skipped (timeout exhausted)` or `CONSULT: skipped (incomplete output exhausted)` and report it. If an explicit cross-provider review remains unsatisfied or material uncertainty remains immediately before a Consequential action, record the failure and stop to ask; a skipped label never authorizes proceeding.

## Route unavailable

Record every observed route failure in `CONSULT HISTORY`: sanitized CLI command or harness spawn specification/child ID, observed exit status or harness terminal state, and reason (`usage limit/429`, `auth`, `launch`, `provider`, `timeout`, `incomplete`, or `cancelled`). Include report/advice status separately; never infer zero tokens from an immediate failure. A stderr excerpt supplements, never replaces, the observed status. Keep secrets and prompt contents out of the record.

Only a failure without substantive advice may advance once to the next frozen candidate while global attempt capacity remains; the issued launch request spends another attempt. Never append an unknown or newly sampled route. When no candidate remains, report every route failure. Only where continuation is permitted by the gates below, label `CONSULT: skipped (advisor routes exhausted)`; otherwise record `CONSULT: required (blocked: advisor routes exhausted)` and stop.

An explicit cross-provider review left unsatisfied or unresolved material uncertainty immediately before a Consequential action makes exhausted routes stop-and-ask, not permission to proceed.

Route exhaustion never relaxes the standing stop-and-ask rule.

Route exclusions apply to the whole current batch. A later independently eligible batch may reconsider a transient usage-limit/provider/timeout failure using fresh evidence; auth/launch failures need evidence that their cause was corrected. History never grants a retry, and failure never proves a provider permanently dead.

An observed usage-limit/auth failure excludes other transports that share that account for the rest of the batch. A transport switch never resets consumption or creates a retry.
