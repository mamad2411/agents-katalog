---
name: sol-terra-luna-auto-router
description: Optimize quality per token across GPT Codex, GPT Work, and Codex CLI by automatically selecting the best-fit GPT-5.6 Luna, Terra, or Sol profile and reasoning effort for the main task and every delegated subtask. Prioritize direct visible Codex execution and importance-aware subagent routing. Use automatically for nontrivial work where model or effort choice can affect quality or token cost, when delegating to subagents, when the user asks GPT or Codex to choose or switch models, or when the user invokes $sol-terra-luna-auto-router.
---

# Sol Terra Luna Auto Router

Prioritize the common GPT Codex workflow: the user asks for repository work and continues directly in a visible Codex task running the selected model and effort. Apply the same routing policy in GPT Work and Codex CLI. Optimize the balance between result quality and total input, reasoning, rework, verification, and handoff tokens.

## Preserve the authority boundary

- Treat invocation of this skill, explicit or implicit, as an instruction to classify the task and use the surface's native model-routing mechanism. The skill explicitly authorizes bounded model routing; it does not authorize unrelated side effects.
- Route only within the GPT-5.6 family: `gpt-5.6-luna`, `gpt-5.6-terra`, and `gpt-5.6-sol`. Never route to, downgrade to, or use a fallback from GPT-5.5 or another non-5.6 model. When the selected 5.6 profile is unavailable, choose another appropriate 5.6 profile or report the unavailable gate honestly.
- For a nontrivial Codex request, current model and effort must be positively known to exactly match the selected route before work may stay in place. Unknown current model or effort is a mismatch. When `fork_thread`, `send_message_to_thread`, and navigation are available, a mismatch requires exactly one visible same-directory routing fork.
- Never claim that the current host task changed models or reasoning effort. A profile label in prose is not execution evidence. Report a routed child only after the model-aware send succeeds; when settings readback is available, verify that readback before claiming the switch executed.
- If no model-aware adapter is available, continue in the current task using the selected operating profile and report the model and effort as a recommendation, not an executed switch.
- Do not infer authority for deployment, destructive commands, external messages, purchases, or other consequential actions from model-routing authority.

## Establish context

1. Restate the outcome, acceptance checks, constraints, and permitted mutations.
2. For repository work, inspect the current branch, revision, dirty files, and applicable instructions before routing.
3. Treat ALEXAI as the user's operating context when the workspace or request is related to OpenCrab, Harness, ontology packs, or the user's established projects. Verify actual repository, owner, runtime, and deployment state before making project-specific claims.
4. When OpenCrab MCP pack tools are available and ontology-backed reasoning is relevant, resolve and use `Fable5xGLM5.2` before other packs. Use it when its reasoning quality or avoided rework is worth the added context; skip it for trivial or already-settled tasks. Prefer a live name lookup; the known preferred package handle is `a9f5a9a9-cfca-4d9a-b17b-79c24a94ae0e`, but verify it when practical. If OpenCrab tools are unavailable, continue without pretending the pack was used.
5. Determine whether the work is one phase or a relay. Do not force all three models into every task.

## Select the surface adapter

Detect capabilities instead of trusting a UI label. Keep the classification, Ultra lock, handoff format, and completion gates identical across surfaces.

Maintain these cross-surface invariants:

- Keep the routing policy self-contained in this `SKILL.md`; do not require a helper script or local-only reference to classify work.
- Do not require repository, filesystem, terminal, or persistent-thread tools in GPT Work. Use only capabilities actually exposed in that task.
- Use the same model IDs, effort values, Ultra lock, escalation rules, compact briefs, and verification gates in Work, Codex, and CLI.
- Keep every direct task, persistent task, subagent, and CLI subprocess inside the GPT-5.6 Luna, Terra, and Sol model set. Availability never authorizes a GPT-5.5 or other non-5.6 fallback.
- Let only the execution adapter differ. A missing adapter must degrade to an honest in-task profile instead of failing the user's work.

### GPT Codex direct work

Use this adapter first when the user is working normally in the Codex app.

1. If a native control can change the calling task's model and effort directly, use it and verify the resulting settings before continuing. At present, do not assume such a control exists.
2. Execute in place only for trivial work or when the current task's model and effort are positively known to exactly match the selected route. Unknown current settings are a mismatch, not permission to stay in place.
3. Otherwise, for nontrivial work, call `fork_thread` without a source ID and request a same-directory fork of the calling task. When `fork_thread`, `send_message_to_thread`, and navigation are all available, this visible fork is mandatory rather than discretionary.
4. The fork contains completed history but not the active request. Immediately send the active request and a compact execution brief to the returned child with `send_message_to_thread`, setting the selected `model` and `thinking` explicitly. A successful model-aware send is required switch evidence; if the surface exposes settings readback, confirm the child matches before work begins.
5. Prefix the child brief with `Router role: Codex direct execution child`. A task carrying this marker must execute directly and must not create another routing fork for the same phase.
6. After the explicit model-aware send succeeds, navigate the Codex app to the child task so the user continues working directly in the selected model task. Keep the original task as the routing record.
7. Use at most one direct fork per request. Create a later fork only when new evidence genuinely changes the required model tier, and never run two writers concurrently in the same directory.
8. If same-directory forking or thread steering is unavailable, fall back to a native worker subagent and integrate its changes in the parent. Report that this was a fallback rather than a direct task switch.

When the user explicitly requests a clean new or background task instead of continuity, use project listing and task creation with the selected `model` and `thinking`. Resolve the exact project first and monitor the task to a terminal result.

### GPT Work

Use native multi-agent tools when `spawn_agent` accepts `model` and `reasoning_effort`.

1. Spawn the selected Luna, Terra, or Sol child for a concrete phase with the mapped model ID and effort.
2. Default `fork_context` to false and send a compact self-contained brief. Fork context only when reconstructing necessary state would cost more tokens or lose critical intent.
3. Use a worker for bounded artifact production, an explorer for a specific codebase question, and the default role for general reasoning.
4. Wait only when the result blocks the next action. Integrate the artifact or evidence, then close completed agents that are no longer needed.

Do not invoke `codex exec` from inside GPT Work or GPT Codex when a native app adapter is available.

### Codex CLI

Prefer native subagent tools when the CLI host exposes them. Otherwise, on explicit invocation of this skill, run one selected phase through `codex exec` with an ephemeral session:

```bash
codex exec --ephemeral \
  -m gpt-5.6-terra \
  -c 'model_reasoning_effort="high"' \
  -C "$PWD" -
```

Replace the model and effort with the selected route and pass the compact phase brief over standard input. Preserve the current sandbox and approval policy; never add a dangerous bypass flag automatically. Allow only one writing process in a checkout, capture its terminal result, and verify produced artifacts in the parent. Do not launch a subprocess when the work can be completed at equal quality in the current CLI task.

## Optimize quality per token

Apply these rules before choosing a model:

- Start with a lightweight classification pass. Choose Luna Low only when the path and finish line are clear; choose Terra or Sol immediately when important reasoning signals are already present.
- Prefer one selected execution task and one model. A mandatory direct Codex fork is an execution handoff, not optional parallel work: use it for every nontrivial unknown or mismatched route, but do not create extra children for simple or known-match work.
- Default to zero additional children. Use at most one direct writing child for normal work, two for high-risk multi-phase work, and three only for an authorized production incident or an explicit user request.
- Select the effort with the best expected quality-to-token ratio. Do not underfund reasoning when an early mistake would cost more tokens through rework, and do not use higher effort when it does not materially improve the gate result.
- Raise both model tier and effort when important reasoning is required: conflicting evidence, architectural tradeoffs, subtle invariants, security or data boundaries, costly reversibility, or a repeated non-obvious failure. Prefer Terra High for bounded complexity and Sol High or Extra High for open-ended or high-risk judgment.
- Never select Ultra automatically. Use `ultra` only when the user explicitly requests Ultra in the current task. Prior preferences, task importance, production risk, or model availability do not count as permission.
- Pass paths, commits, and compact evidence pointers instead of conversation transcripts. Never paste the full parent context into a child brief.
- Read only the files, logs, documentation sections, and pack evidence needed for the current decision.
- Reuse verified artifacts and prior handoffs by reference. Do not ask another model to rediscover settled facts.
- Combine planning and implementation in one task when the plan is obvious. Split them only when a wrong plan would create more rework tokens than the handoff costs.
- Add independent review only for meaningful regression, security, data, or production risk.
- Keep progress updates and final route reporting concise. Do not narrate internal scoring unless it changes the route or the user asks.

## Classify the work

Evaluate four dimensions before selecting a route:

- **Clarity:** Is the desired behavior and implementation path already known?
- **Scope:** Is the work local and mechanical, or cross-module and architectural?
- **Risk:** What is the blast radius, reversibility, security impact, and production exposure?
- **Evidence:** How difficult is it to verify the outcome and resolve conflicting evidence?

Choose the strongest signal, not an average that hides one severe dimension.

| Profile | Use when | Default effort | Raise effort when |
| --- | --- | --- | --- |
| **Luna** | Fast reconnaissance, deterministic edits, formatting, focused tests, status checks, settled release mechanics | Low | Several branches or tools must be coordinated; use Medium or High, or hand judgment to Terra |
| **Terra** | Normal implementation, tests, refactors, bounded debugging, code review, converting a settled plan into working artifacts | Medium | The change has subtle invariants or failed for a non-obvious reason; use High, then Extra High only if needed |
| **Sol** | Ambiguous planning, architecture, hard diagnosis, high-risk review, conflicting evidence, route repair | High | A decision is costly to reverse, production-critical, or security-sensitive; use Extra High |

Use these user-facing effort mappings when task tools require API values:

| Effort | Tool value |
| --- | --- |
| Low | `low` |
| Medium | `medium` |
| High | `high` |
| Extra High | `xhigh` |
| Ultra | `ultra` |

Luna does not support Ultra. Move an explicitly user-authorized Ultra phase to Terra or Sol. Never use the hidden `max` value in this router.

Treat Ultra as user-locked. Even when a phase appears Ultra-grade, use Sol Extra High and report the remaining uncertainty. Ask for explicit Ultra authorization only if the gate cannot be passed safely at Extra High. Do not treat phrases such as "important," "deeply," "do your best," or "production-critical" as Ultra authorization.

## Optimize every subagent delegation

Classify each proposed subtask independently before delegation. Do not inherit the parent model or effort merely because the parent is using it.

| Subtask importance | Signals | Default assignment |
| --- | --- | --- |
| **Low** | Reversible, mechanically verifiable, settled path, narrow blast radius | Luna Low |
| **Low with coordination** | Several files or tools, but little judgment and cheap failure | Luna Medium |
| **Normal** | Standard implementation, bounded debugging, focused review | Terra Medium |
| **Important and bounded** | Subtle invariants, cross-module coupling, expensive rework, non-obvious failure | Terra High; raise to Extra High only when needed |
| **Important and open-ended** | Architecture, conflicting evidence, security or data boundary, production-critical diagnosis | Sol High; raise to Extra High when the decision is costly to reverse |

Apply these delegation rules:

1. Decompose the parent task into concrete outputs before spawning. Assign importance from the subtask's own ambiguity, impact, reversibility, coupling, and verification difficulty.
2. Set `model` and `reasoning_effort` explicitly on every `spawn_agent` call. For persistent Codex tasks, set `model` and `thinking` explicitly. Never omit them and accidentally inherit an overpowered or underpowered parent profile.
3. Use Luna Low or Medium for file discovery, status collection, deterministic edits, formatting, focused test execution, and mechanical release checks.
4. Use Terra Medium for normal coding. Use Terra High or Extra High for subtle implementation, bounded diagnosis, and reviews that require judgment.
5. Use Sol High or Extra High only for high-impact planning, architecture, conflicting evidence, hard diagnosis, security or data boundaries, and risky decision review.
6. Never assign Ultra to a subagent automatically. The same current-request user lock applies to parents, direct Codex forks, persistent tasks, CLI subprocesses, and every subagent.
7. Default `fork_context` to false for low-importance agents. Supply only paths, artifacts, constraints, and acceptance gates. Fork context only when reconstructing essential state would reduce quality or consume more tokens.
8. Parallelize independent low-importance subtasks when useful. Give one clear owner to important decisions and avoid several agents independently spending tokens on the same high-level question.
9. Keep urgent critical-path work in the parent unless a different model is necessary to pass the gate. Delegate side work that can advance in parallel without blocking the parent.
10. Reclassify when a subtask reveals new ambiguity or risk. Send focused corrections at the same tier for brief defects; create a new higher-tier agent when the required model changes, passing the actual artifact rather than replaying full context.
11. Verify every delegated output against its gate in the parent. A low-importance agent may gather evidence, but it must not make an unreviewed high-impact decision.

Use this compact brief for every delegation:

```markdown
Importance: <low/normal/important>
Assigned: <Luna/Terra/Sol> <Low/Medium/High/Extra High>
Role: <phase responsibility>
Outcome: <one concrete result>
Inputs: <minimal paths, artifacts, and evidence>
Constraints: <scope, authority, and forbidden actions>
Acceptance: <checks proving completion>
Return: <artifact or concise evidence-backed handoff>
```

## Select the route

Apply these routes as defaults, then adapt to the evidence:

- **Clear, mechanical work:** Luna Low in the current task. Raise to Medium for several coordinated checks.
- **Bounded investigation:** Luna Medium gathers and interprets evidence. Move to Terra Medium only when judgment is required.
- **Normal feature or bug fix:** Terra Medium implements and tests in one task. Raise to High for subtle invariants. Add Luna only when independent verification materially reduces risk.
- **Cross-module refactor or subtle defect:** Terra High first. Use Sol High to settle the approach only when architecture or evidence is genuinely ambiguous; return implementation to Terra only when the phases cannot be combined safely.
- **Production incident:** Luna Medium captures live evidence; Sol High or Extra High diagnoses only if needed; Terra High fixes and adds regression coverage; Luna Medium deploys and monitors only when authorized.
- **Research or product design:** Luna Medium handles bounded synthesis; Sol High resolves open-ended ambiguity. Add a separate Terra prototype only when it will change the decision.
- **Irreversible migration, security boundary, or costly architecture:** Sol Extra High coordinates. Isolate write scopes and make every downstream gate explicit. Use Ultra only when the user explicitly requests it in the current task.

Prefer one selected model for a single-phase task. Use a relay only when a handoff meaningfully reduces uncertainty, separates write ownership, or provides independent verification.

## Execute routed phases

Use the selected surface adapter and build a short route only when more than one phase is justified:

1. Build the route:

```markdown
| Phase | Model | Effort | Deliverable | Gate |
| --- | --- | --- | --- | --- |
| ... | Luna/Terra/Sol | Low/Medium/High/Extra High/Ultra | ... | ... |
```

2. Create each child or subprocess with the exact model ID and supported effort:

| Profile | Model ID |
| --- | --- |
| Luna | `gpt-5.6-luna` |
| Terra | `gpt-5.6-terra` |
| Sol | `gpt-5.6-sol` |

3. Give each routed phase a self-contained brief:

```markdown
Importance: <low/normal/important>
Assigned: <Luna/Terra/Sol> <Low/Medium/High/Extra High>
Role: <phase responsibility>
Outcome: <one concrete result>
Inputs: <paths, commits, URLs, evidence, and prior artifacts>
Constraints: <scope, invariants, authority, and forbidden actions>
Acceptance: <checks proving completion>
Return: <artifact or concise evidence-backed handoff>
```

For a Codex direct child, add this first line:

```text
Router role: Codex direct execution child
```

4. For nontrivial Codex work, treat unknown current settings as a mismatch and complete the mandatory `fork_thread` -> model-aware `send_message_to_thread` -> navigation sequence before writing. Permit only one writing child at a time in the same checkout. Use a worktree only for explicitly requested isolation or genuinely independent changes, and include an integration gate.
5. Observe each routed phase until it reaches a terminal result. Creation is not completion.
6. Verify the actual artifact, diff, test output, or production evidence before passing it forward. A prose summary is not a substitute for the artifact.
7. Send focused corrections to the same child when the adapter supports continuation. Create a new child when responsibility moves to another model.
8. Keep direct and persistent Codex tasks visible and unarchived unless the user requests archival. Close temporary native agents after integration.
9. Cancel planned downstream phases when the current artifact already satisfies their gates. Do not spend tokens to complete a route for symmetry.

## Escalate deliberately

- Retry the same model and effort only for transient failure or an incomplete brief. Prefer a focused correction over replaying the full task.
- Raise effort when the route remains valid but the reasoning depth was insufficient.
- Move Luna to Terra when the task becomes judgment-heavy.
- Move Terra to Sol when evidence conflicts, architecture changes, or the safe path is no longer settled.
- Re-plan with Sol when new evidence invalidates the route. Do not pile fixes onto a broken plan.
- Never silently lower model tier or effort. Report quota, policy, availability, latency, or cost constraints that force a substitution.
- Never substitute GPT-5.5 or another non-5.6 model. If the selected 5.6 profile is unavailable, select a suitable available 5.6 profile and report that substitution; if no suitable 5.6 profile is available, stop at that gate.
- Never escalate to Ultra as part of an automatic retry or recovery route. Stop at Extra High unless the user explicitly requests Ultra.
- If Sol is unavailable for a genuinely Sol-grade decision, stop at that gate and return completed artifacts rather than disguising a weaker result as equivalent.

## Apply completion gates

- A plan passes when it identifies affected surfaces, decisions, risks, acceptance checks, and integration order.
- Implementation passes when requested behavior exists, focused tests pass, and unrelated user changes remain intact.
- Review passes when actionable findings are fixed and rechecked or rejected with evidence.
- Deployment passes only with the deployed revision and a user-visible or data-visible health check.
- OpenCrab pack workflows pass only after the applicable live ingest/status and pack QA gates, not merely local artifact generation.

## Report the actual route

Lead with the finished outcome. In one compact line, report the surface adapter and route actually used, including each delegated subtask's importance, agent/task ID when available, model, effort, and gate result. For Codex, state whether execution stayed in place, moved to a visible direct fork, or used a worker fallback. Do not describe Luna, Terra, or Sol as executed from prompt language, a recommendation, or an intended profile alone. Mention only material substitutions, escalations, unavailable tools, and residual risks. Never present a proposed route as one that actually ran.
