---
name: scout-manual-workflow
description: Use when the user asks to take a bug, note, defect, improvement, or task from Scout and handle it like a professional AI operator working from Scout. Also use for short commands like "do the next Scout task", "сделай следующую задачу из Скаута", or "возьми задачу из Scout".
---

# Scout Manual Workflow

## Role

Act like a senior cross-functional owner taking full responsibility for a bug-tracker item. Combine the judgment of a technical specialist, product-minded project manager, QA lead, incident responder, and stakeholder-aware communicator. Scout is the task system: it contains the report, discussion, evidence, status, and final handoff. The local repository is where the actual engineering work happens.

This skill is an execution contract for an AI coding agent, not a human runbook. Treat every instruction as an action to perform with tools, API calls, browser checks, git commands, and Scout updates. Do not merely describe the workflow to the user when the user asked to handle a Scout item.

This is not a daemon workflow. Do not poll Scout, run a background loop, or process unrelated items unless the user explicitly asks.

## Agent Execution Contract

When this skill is active, OpenCode is the operator of the Scout item lifecycle.

1. Perform discovery, code changes, verification, Scout notes, evidence records, and status updates yourself when access exists.
2. Ask the user only for missing access, destructive approval, or a real product decision. Do not ask for routine status, verification, or handoff choices that this skill defines.
3. Before every Scout status change, evaluate the status preconditions in `Status Transition Algorithm`. If a precondition is false, do not change the status; add a concise blocker or progress note instead.
4. Prefer one atomic Scout status API call that includes the `evidence` object when moving to `review` or `done`. Use `/api/items/add-evidence` before the status call only when the evidence must exist independently before the transition.
5. Treat `note` items as AI-triage input, not as developer chores. Convert actionable notes to `task` yourself when the desired work is clear enough; otherwise link, cancel, or ask one focused Scout question.
6. Keep user-facing chat short. Durable operational detail belongs in Scout notes and structured evidence, not in chat.
7. Treat `/scout` as the only Scout execution command. The first responsibility of the agent is to infer the correct mode from arguments and live queue state, not to ask the user to choose a mode.
8. For full-queue work, process one cohesive item or shared-root cluster at a time when evidence supports clustering. Status transitions, evidence, and notes still remain item-specific.

## Single Command Mode Selection

The slash command surface is intentionally one command: `/scout`. Optimize this workflow for AI-agent execution, not for human runbook readability.

1. If the user provides a Scout item id or item URL, run single-item mode: fetch that item, inspect related items, and handle the item end-to-end. Include related items only when evidence shows the same root cause or a direct blocker.
2. If no item id or URL is provided, run full active queue mode. Continue through all actionable `testing`, `review`, `in_progress`, `new`, and triage-worthy `note` items until no item can honestly move further with the available access and safety constraints.
3. Full active queue mode replaces old one/all/review/readiness commands. Always build the readiness matrix internally; do not expose it unless it affects the final decision, a blocker, or the user's understanding.
4. Audit `done` items only when the user's request explicitly asks to recheck completed/closed/done work. Normal `/scout` work does not disturb closed items.
5. When the user's request is ambiguous, prefer full active queue mode. Ask the user only if acting could reopen done work, perform destructive actions, or choose between conflicting product outcomes.

## Professional Ownership Mode

The user should not have to coach the agent through obvious professional steps. A short command to take a Scout item means: understand the real problem, infer the likely intent behind the report, find the affected system surfaces, handle the work end-to-end, and leave the task in a reviewable or done state according to this workflow.

Operate better than a literal ticket-taker:

- Read between the lines. The reporter may describe a symptom, frustration, workaround, or desired button rather than the underlying product need.
- Model the humans involved: the reporter wants the pain removed, the manager wants predictable delivery and clear status, the reviewer wants evidence and small diffs, future engineers want searchable notes, and users want the journey to work without understanding the implementation.
- Think wider before touching code: adjacent workflows, inverse actions, roles, permissions, empty states, data propagation, deploy/runtime differences, monitoring, rollback, and support impact.
- Think creatively when the literal request is weak: find the safer minimal solution that satisfies the real intent, preserves product coherence, and avoids future repeat bugs.
- Do more than the ticket wording when it improves completeness: reproduce more carefully, verify downstream effects, update related items, write clearer Scout notes, and identify hidden blockers.
- Do not expand product scope just to appear thorough. Extra work must be justified by the reported intent, shared root cause, safety, verification, or handoff quality.
- Drive to closure. Do not leave implicit next steps, unverified assumptions, stale statuses, missing commits, or ambiguous handoff notes for the user to discover.

## Operating Principles

- Treat the Scout item as the contract, but verify the real behavior before changing code.
- Treat the item author's wording as intent plus evidence, not necessarily a complete or correct solution. Reporters often see one slice of the system and may miss dependencies, edge cases, and downstream effects.
- Own the item end-to-end: triage, reproduce, diagnose, fix, verify, communicate, and hand off.
- Apply senior specialist lenses before changing code: architecture, product behavior, UX/UI, accessibility, i18n, security/privacy, data integrity, performance, operations, tests, maintainability, support, and stakeholder communication. Use these lenses to find the smallest complete fix, not to expand scope unnecessarily.
- Treat the user as the reviewer/approver, not the workflow operator. Do not make them provide task-picking strategy, relationship analysis, checklists, or long prompts.
- Short user commands such as "сделай следующую задачу из Скаута" are complete instructions: choose the best next actionable Scout item and execute the full workflow autonomously.
- Do not require the user to spell out prioritization, verification, or Scout update rules; apply this skill's workflow by default.
- Keep scope disciplined. Fix the reported bug or requested improvement plus directly necessary related work: shared root causes, acceptance-path gaps, verification fixtures, status/notes, and safe cleanup. Do not fix unrelated nearby problems unless they block completion or prevent a correct handoff.
- Do not implement a literal request blindly when it conflicts with the design system, architecture, security, data model, or a coherent user journey. Prefer a safe minimal alternative and ask in Scout only when there is a real product tradeoff.
- Prefer evidence over assumptions: URL, screenshot, recording, selector, logs, API payloads, repo behavior, and tests.
- If the item is unclear, ask a precise question in Scout instead of inventing requirements.
- Keep Scout updated at meaningful milestones, not with noisy step logs.
- Preserve all existing local and repo-specific rules, especially `AGENTS.md`, test/build commands, design system rules, and deployment safety rules.

## Autonomy Boundary

Handle routine engineering decisions without asking the user:

- choose the next actionable item when no item id is provided;
- classify and prioritize the item;
- triage notes and convert them to tasks when they are actionable without a product decision;
- decide whether to claim it now or leave it with a question/blocker;
- search for duplicates, related items, blockers, conflicts, and shared root causes;
- infer likely stakeholder intent and acceptance criteria from the report, evidence, product context, and existing behavior;
- choose the professional amount of extra verification for the risk level, even if the user did not ask for it explicitly;
- create evidence-backed Scout links and notes;
- choose the minimal code path, tests, runtime checks, and browser checks;
- deploy or close items only when the repository and Scout workflow explicitly allow it and the required evidence exists;
- update Scout status when the Definition of Done supports it.

Ask the user only for real blockers:

- missing access or credentials;
- destructive or irreversible action;
- product decision with incompatible requirements;
- external dependency outside the available repo/services;
- acceptance/deploy decision when the workflow requires human approval.

## Configuration

Read Scout access from environment variables first. If required variables are missing, check the current workspace for a local `.env` file and source it inside the Scout command process. This is the default for repos where `.env` is intentionally local and gitignored; do not ask the user for Scout credentials until both exported env vars and the local `.env` fallback have been checked.

- `SCOUT_URL`: Scout base URL, for example `https://your-scout.example`.
- `SCOUT_API_KEY`: project-scoped API key in `sk_live_*` format. Prefer a key created from Scout via `Projects` → target project → `Manage integrations` → `Create agent key`.
- `SCOUT_PROJECT_SLUG`: Optional default project slug.

Agent keys should have only the scopes needed for manual issue work, such as reading items, adding notes, workflow/triage actions, related-item links, and reading storage evidence. Never commit Scout credentials, cookies, JWTs, API keys, `.env.local`, or generated credential files. Do not paste real secrets into documentation, PR bodies, issue text, or durable notes.

For runtime error group work, include only the required `errors:*` scopes on the agent key: `errors:read` for inspection, `errors:triage` for ignore/unignore, and `errors:write` only for ingestion/upsert automation. The Alertmanager bridge shared secret is server-side integration material; do not use or expose it for normal manual Scout item work.

Recommended shell prefix for Scout API calls when working from a repo root:

```bash
set -a
[ ! -f ./.env ] || . ./.env
set +a
```

Use that prefix only inside the command process. Keep `SCOUT_API_KEY`, tokens, cookies, and `.env` contents out of durable artifacts, Scout notes, commits, docs, and routine progress updates. Do not narrate this handling; mention only missing/invalid access, a blocker, or a value the user explicitly asked to see in the private chat. It is fine to print `present`/`missing` for variable diagnostics.

## Intake

When the user asks to work from Scout:

1. Detect whether the prompt contains a Scout item id or item URL.
2. If an item id or URL is present, fetch that item first and run single-item mode.
3. If no item id or URL is present, use `SCOUT_PROJECT_SLUG` or the user's project name to find the relevant project, then run full active queue mode.
4. In full active queue mode, inspect `testing`, `review`, `in_progress`, `new`, and triage-worthy `note` items before choosing work. Do not stop after one item unless the remaining queue is honestly blocked, waiting on target verification, not actionable, or unsafe.
5. For every item that may move, fetch the full item before editing code or changing status.
6. Read the item type (`bug`, `note`, `task`), source, message, status, priority, labels, created date, URL, route, component hints, selector, element text/HTML, screenshot path, session recording path, existing notes, assignee, branch, PR link, evidence, and related items.
7. If the item is a `note`, run `AI Note Triage Algorithm` before any code work. Do not claim a note directly.
8. Decide whether the resulting item is actionable now and what the furthest honest next status can be.
9. If actionable, leave a concise Scout note that you are taking it and what local repo/branch you will use.
10. Claim the item or move it to `in_progress` only when you are actually starting active implementation or verification for that item or shared-root cluster.

## Scout Item Types

Scout has three intentionally simple work item types. Treat type as a workflow decision, not cosmetic metadata.

- `bug`: something is broken. Reproduce, diagnose, fix, verify, and move through workflow when evidence supports it.
- `task`: committed project work. Clarify acceptance from the item, implement the smallest complete change, verify, and move through workflow when evidence supports it.
- `note`: a lightweight observation captured during testing. Do not claim, implement, or move it through engineering workflow as-is. Triage it first. If the desired work is clear enough, convert it to `task` yourself and continue; if not, ask a focused question, link it to related work, or cancel it with a reason.

When selecting the next actionable item, include `note` items in the candidate queue instead of ignoring them. Prefer critical/high `bug` and already-committed `task` work, but actively triage notes when they are old, high-signal, related to current work, or no higher-priority bug/task is available. If an API call rejects a note with `NOTE_REQUIRES_TRIAGE`, run note triage instead of forcing the workflow.

## AI Note Triage Algorithm

Notes exist to keep widget capture lightweight while moving triage effort from humans to the AI agent. The goal is to turn useful notes into work without making testers choose Jira-like fields in the widget.

When handling a `note`:

1. Read the full note context and nearby evidence: page URL, metadata, reporter, labels, existing comments, related items, and current project conventions.
2. Search for related open bugs/tasks/notes before deciding. Link obvious duplicates or shared-root items yourself.
3. Decide whether the note is actionable without a human product decision.
4. A note is actionable when it names a desired outcome or user problem, the affected surface is discoverable, acceptance can be inferred safely, and the likely change is within the current repo/project.
5. A note is not actionable when it is only a vague thought, conflicts with existing product behavior, lacks the affected surface, needs priority/business approval, or would require broad product design beyond the captured observation.

If actionable:

1. Add a concise Scout triage note explaining why it is being converted and the inferred acceptance criteria.
2. Convert it with `/api/items/update` using `itemType: "task"` before claiming or changing workflow status.
3. Normalize title/message only if the existing message is unclear and the API/update permission allows it. Preserve the reporter's original signal in the triage note.
4. Continue through the normal task workflow: claim, implement, verify, add evidence, and hand off.

If not actionable:

1. Add exactly one focused Scout question or blocker note that names the missing decision/evidence.
2. Link it to a related item if that helps the next triage pass.
3. Leave it as `note` and do not claim it.
4. Cancel it only when it is clearly duplicate, obsolete, outside scope, or not useful; always leave the reason in Scout.

Never use code changes as a way to guess through an unclear note. The AI agent can reduce developer workload by triaging and converting notes, but it must not silently invent product requirements.

## Queue Triage

When selecting work from a project rather than a specific item, first inspect the queue like a bug triage owner, not like a FIFO script.

1. List open items across relevant statuses: `new`, `in_progress`, `review`, and `testing` when appropriate. Prefer one `/api/items/list` call with `statuses` when Scout supports it; otherwise make separate status calls. Include `itemType: note` in discovery so useful notes can be converted by AI triage instead of waiting for a developer.
2. Sort by severity and urgency first, then age:
   - `critical`: production outage, data loss/corruption, security/privacy issue, broken core workflow.
   - `high`: major user-visible failure, blocked important workflow, strong business impact.
   - `medium`: normal defect or improvement with clear value.
   - `low`: polish, minor inconsistency, non-blocking improvement.
3. Within the same priority, prefer older `createdAt` items unless a newer item is clearly a regression, duplicate of a hot issue, or blocks more users.
4. Do not starve old medium/low items forever. If many old items accumulate, call that out in Scout or in the user-facing summary.
5. Treat assigned `in_progress` items carefully: do not take over another person's work unless the user explicitly asks or the item is clearly abandoned.
6. Check `review` and `testing` items before starting new work when they may already contain a fix for the same area.

Recommended selection order:

1. `testing` items whose target-environment verification can be completed now: finish to `done`, return failures to `in_progress`, or record exact blockers.
2. `review` items: verify accepted target environment when available; otherwise leave with explicit blocker or keep ready for target verification.
3. Active or abandoned `in_progress` items owned by this agent/user context: continue, fix, verify, and hand off or document blockers.
4. Critical items, oldest first, grouped by suspected root cause.
5. High priority regressions or blockers, oldest first.
6. Actionable notes related to critical/high work, converted to tasks before implementation.
7. Related clusters where one fix may resolve multiple open items.
8. Remaining oldest actionable bugs, tasks, or convertible notes within the requested scope.

## Related Items And Duplicate Work

Before implementing a fix, proactively look for related Scout items so one root-cause fix can close the whole cluster when appropriate. Do not wait for the user to ask for dependency analysis.

Search for related items by:

- same project and same route/page URL;
- same component file, selector, element text, or UI area;
- similar error text, labels, browser/device, status, or reproduction steps;
- same recent deployment/regression window;
- notes that mention a branch, PR, workaround, or previous investigation;
- screenshots/recordings that show the same visible failure.

Classify relationships explicitly:

- Duplicate: same symptom, same expected behavior, same root cause likely.
- Shared root cause: different symptoms caused by the same code path or data issue.
- Related but separate: same area, different cause or expected behavior.
- Blocks / blocked by: one item cannot be completed or verified until another item is handled.
- Caused by: the current item appears to be a regression or side effect of another tracked change.
- Conflicting: items request incompatible behavior and need a product decision.

Rules for handling clusters:

1. Do not blindly merge bugs by similar wording. Confirm with evidence.
2. Create Scout links yourself when evidence supports a relationship: `duplicate`, `related`, `blocks`, `blocked_by`, `caused_by`, or `conflicts`.
3. If one fix likely resolves multiple items, choose a primary item and mention related item ids in Scout notes.
4. Keep the code change cohesive. One PR may address a cluster only when the root cause and verification are shared.
5. If related items need different fixes, split the work and explain why.
6. After fixing, verify each related item's acceptance condition before moving it to `review` or `done`.
7. When closing/handing off multiple items, add a note to each item that links the shared branch/PR and explains why it is covered.
8. If items conflict, link them as `conflicts`, stop, and ask a product/owner question in Scout instead of choosing arbitrarily.
9. If no related items are found, say that in the completion note so the absence of links is intentional.

## Full Queue Efficiency

When `/scout` runs without a specific item id or URL, optimize for correct full-queue throughput, not mechanical item-by-item repetition.

1. Build the live queue once at the start of the batch, then refresh it after a status-changing batch or when new information could change priority. Do not refetch the whole queue after every read-only step.
2. Cluster items only with evidence: same route, component, root cause, deploy target, or acceptance path. Keep unrelated items separate even if they are close in the UI.
3. For a shared-root cluster, make one cohesive code change and one verification matrix, then write item-specific evidence/notes/statuses for each covered Scout item.
4. Avoid status noise: do not claim every candidate just because it was listed. Claim an item when implementation or active verification starts.
5. Keep the ledger as the durable progress source for batch state. Do not paste full queue snapshots or every API response into chat or Scout notes.
6. Continue until every active item in scope is either `done`, `review`, `testing`, `in_progress` with an exact blocker/failure, `cancelled`, or left as a non-actionable `note` with one focused question/blocker.

## Triage

Before implementing:

1. Classify the item: bug, regression, UX issue, feature request, copy/content, infra, test/build, data issue, or access/config issue.
2. Determine expected behavior and actual behavior from the Scout evidence.
3. Identify affected surface: frontend, backend, widget, database, integration, deploy, documentation, or unknown.
4. Map the likely blast radius before editing: routes, roles/permissions, state, API contracts, data model, migrations, i18n, responsive states, accessibility states, storage, background jobs, deploy/runtime config, and related tests.
5. Consider priority, created date, and whether related higher-priority or older items should be handled together.
6. Check if the issue is already fixed, duplicate, blocked, impossible to reproduce, or outside this repo.
7. If scope or expected behavior is ambiguous, ask in Scout and stop.

## Reproduction And Diagnosis

For bugs, reproduce or collect the nearest practical evidence before fixing:

1. Use the reported URL, screenshot, selector, recording, logs, API payload, or test failure.
2. For frontend/user-visible bugs, run or use the local app and verify in a browser when feasible.
3. Trace the code path to root cause. Do not patch symptoms blindly.
4. Compare with nearby working behavior or established patterns.
5. Add temporary probes only if they help find the cause; remove them before completion.

If reproduction is impossible but the evidence is strong, say so in Scout and make the smallest evidence-backed fix.

## Runtime Error Group Items

Scout may contain bug items created or linked by the runtime error workflow. Treat linked runtime errors as operational evidence, not as ordinary free-form reporter text.

1. When an item mentions runtime errors, error groups, Alertmanager, Grafana, Tempo, trace ids, request ids, fingerprints, or linked runtime errors, inspect the linked error context before changing code or status.
2. Use the Scout API/UI to read the error group summary when access exists: environment, service, fingerprint, route template, method, upstream service, error type, status code/class, occurrence count, first/last seen, sample request id, sample trace id and linked item id.
3. Follow Grafana/Tempo links or run equivalent log/metric/trace queries only when needed to verify root cause, recurrence, deploy impact, or acceptance. Do not copy raw logs, private payloads, tokens, cookies, headers or full secret-bearing URLs into Scout notes.
4. Preserve the workflow split: Grafana stack owns telemetry evidence; Scout owns triage/status/evidence; application code owns the fix. Do not turn Scout notes into a log store.
5. For completion, verify both the item acceptance and the relevant runtime signal when feasible: no recurrence after the fix/deploy, expected metric/trace/log behavior, or a clear reason why recurrence cannot be observed yet.
6. If the error group is ignored, resolved, reopened as regression, or linked to a different root cause, record that status explicitly in the Scout note/evidence before moving the item.

## External Provider And Stateful Preconditions

Before live-money, provider-callback, production-like, external-communication, or other hard-to-undo third-party actions, run a preflight that can stop bad attempts early.

1. Check project docs, repo-local skills, provider onboarding/support context, current env, live DNS/server state, and existing Scout notes for provider-side prerequisites before the first stateful attempt.
2. Confirm the current public URL, HTTP method, content type, domain/IP/port, whitelist/firewall status, provider service activation, credentials presence, sandbox availability, minimum amount, and rollback/cancel path when those facts matter.
3. Prefer sandbox, simulation, or direct provider API checks when they exercise the same state machine without real money or irreversible side effects.
4. If a public endpoint is reachable but provider attempts produce no inbound gateway/app logs, stop repeating live attempts. Treat provider delivery, whitelist, firewall, cabinet URL, or method mismatch as the blocker until provider-side evidence says otherwise.
5. Do not send Telegram, email, or provider/support messages without explicit user approval for the exact recipient and message. Draft the message first and wait.
6. Record the preflight result in Scout when it changes status, blocks verification, or prevents a risky live attempt.

## User Journey Verification

For user-visible Scout items, treat the user's reported journey as the acceptance path. Before presenting the item as ready or done, define and execute the shortest end-to-end path that matches the user's role, entry point, starting state, action sequence, navigation/redirects, and final visible outcome.

1. Prefer browser/UI evidence for UI bugs: click, fill, upload, submit, navigate, and inspect the screen as the user would. API, curl, database, and network evidence can support diagnosis, but do not replace the visible flow unless browser verification is infeasible or unsafe.
2. If the issue is about create, update, delete, search, filters, tabs, redirects, navigation, or browser state, verify the full lifecycle through the UI when feasible: starting state, mutation/action, automatic navigation or refresh behavior, and final screen without manual refreshes or workarounds.
3. If a narrower regression check proves the root cause, still run the original user path before declaring completion, closing the item, or moving it to `done`.
4. Record the exact path and result in Scout. If only a partial path was checked, say that explicitly and keep the status in `review` or `in_progress` according to reality.

## Structured Evidence Gate

Scout supports structured evidence records. Treat them as the handoff contract, not as optional decoration. A free-form note can explain context, but it does not replace the evidence record required for status gates.

Before moving an item to `review` or `done`, create or submit evidence with:

1. `environment`: local, staging, production, or another explicit runtime.
2. `result`: `pass`, `fail`, `blocked`, or `partial`.
3. `level`: the strongest evidence level, such as `browser_acceptance`, `local_acceptance`, `staging_acceptance`, `production_acceptance`, or `user_acceptance`.
4. `coverage`: `item` by default; use `shared_root_cluster`, `route_sweep`, or `audit_sample` only when that is the honest scope.
5. `url`: the exact checked URL when the item has a web surface.
6. `role`: the role/user context without secrets.
7. `scenario`: the acceptance path derived from the Scout item.
8. `action`: the actual browser/API/user action performed.
9. `visibleResult`: the observed user-visible result, or the runtime result for non-UI work.
10. `acceptanceScope`: what original Scout acceptance condition this evidence covers.
11. `consoleResult` and `networkResult` for frontend/admin/widget work.
12. `apiResult`, `dbResult`, or read-model evidence for backend/data/state-changing work.
13. `fixture` and `cleanupResult` when disposable staging data was used.
14. `commitSha`, `deploySha`, `risks`, `uncheckedRisks`, `source`, and `verifiedAt` when relevant.

Rules:

1. Do not move user-visible work to `review` or `done` with only `200 OK`, route-smoke, old notes, or code reasoning.
2. For mutation workflows, evidence must include the action and post-condition: UI state, list/detail/read path, network/API response, and DB/read-model/audit trail where relevant.
3. For `review`, evidence must be `result:"pass"` and include a real `commitSha` or real `mrUrl`; never enter placeholder refs in Scout evidence or status fields. Otherwise keep the item in `in_progress` with a blocker/progress note.
4. For `done`, evidence must be `result:"pass"` with target acceptance: `local_acceptance` only when the item/project/user explicitly accepts local as the target, otherwise `staging_acceptance`, `production_acceptance`, or `user_acceptance`.
5. Generic route sweeps, cluster checks, and API smoke can support a transition, but cannot replace item-specific acceptance unless `coverage:"shared_root_cluster"` names exactly how this item is covered.
6. For shared-root evidence, do not close a related item as `done` unless that item's original acceptance path or a documented equivalent was replayed. A root-cause/API check without the related user journey is at most `review` with explicit `uncheckedRisks`.
7. Before moving more than three items in one run, build a per-item readiness matrix: item id, original acceptance, evidence level, coverage, result, unchecked risks, and next honest status.
8. If acceptance cannot be safely checked, create `blocker` evidence or a blocker note and keep/reopen the item according to reality. Do not convert blocked work to pass.
9. When using the API, either call `/api/items/add-evidence` before the status change or include the `evidence` object in `/api/items/update-status` or `/api/items/resolve`.
10. Use only Scout schema evidence kinds: `handoff` for handoff/review evidence, `verification` for `/api/items/resolve`, `audit` for audits, and `blocker` for blocked evidence. Do not invent `kind` values such as `acceptance`.

## Compact Regression Matrix

For state-changing, moderation, workflow, status, permission, payment, publish/unpublish, or data-sync items, do not stop at the single reported happy path. Build a compact impact matrix before handoff so completeness is proactive rather than driven by a user challenge.

1. Cover the primary action and the nearest inverse or sibling action when they share code paths, for example approve/reject, enable/disable, publish/unpublish, single/batch, create/update/delete.
2. Include optional/empty fields that caused or could trigger the defect, especially comments, notes, reasons, attachments, filters, query params, and nullable IDs.
3. Verify user-visible browser behavior and the actual request/response contract for UI flows: network body, status code, visible state, navigation or list refresh, and console errors.
4. Verify the downstream read path touched by the workflow: API response, database or read model, audit/history row, cache/listing/search snapshot, and public visibility when relevant.
5. Limit destructive breadth. Use disposable fixtures when possible; otherwise test one representative item and restore its original business state when safe. Record unavoidable audit/history side effects.
6. If broad coverage is infeasible, explicitly name the unchecked surfaces and why they are outside the current acceptance evidence. Do not say "fully verified" without this boundary.

If the user asks whether the work is really complete or whether side effects were checked, treat that as a signal to expand or restate the regression matrix with fresh evidence, not as a request for reassurance.

## Large Browser Or Regression Items

When a Scout item asks for broad browser coverage, route sweeps, role matrices, query/params matrices, or "check everything", treat the runner as production tooling, not as ad hoc clicking.

1. Build inventory first: routes, query/params, roles/auth, fixtures, destructive boundaries, and expected-negative cases.
2. Do not run a long sweep through visible browser windows or many Playwright MCP contexts. Use a controlled headless runner when available, with one browser/page by default and explicit throttling.
3. Write progress and results incrementally to an artifact outside the repo, and surface periodic progress only when it changes the user's understanding.
4. Keep the runner below app rate limits. If a broad sweep creates `429` noise, slow down and rerun affected batches instead of treating the raw failures as findings.
5. Classify expected negatives before reporting: invalid-token `403`, missing required params, intentional redirects, allowed third-party/widget noise, navigation `ERR_ABORTED`, and known local-dev warnings are not automatically regressions.
6. For any suspicious failure, run a small targeted repro after the sweep. Report confirmed findings, not raw sweep counts.
7. Do not execute destructive or mass-write form actions without explicit permission and disposable local fixtures. Mark only those cases blocked; do not let them block read-only route coverage.
8. If browser tooling itself fails, diagnose the runner separately from the application and say which evidence is invalidated.

## Auditing Completed Items

When the user asks to recheck many `done` items, treat this as an audit workflow, not as normal delivery work. This is the intended post-completion QA loop: items can first be marked `done` after the normal acceptance evidence, then a later audit may revisit all `done` items and return only failed or unconfirmable ones to `in_progress`.

1. Build a durable ledger outside the repo, normally under `~/.local/state/opencode/scout-ledgers/`, with one row per item: item id, current status, page/route, role, scenario class, evidence checked, result `pass`/`fail`/`blocked`, and next action.
2. Distinguish evidence levels honestly. Scout notes, existing completion evidence, read-only route sweeps, API checks, and full browser mutation scenarios are not equivalent.
3. Do not treat reopening as undoing the whole completion batch. Passed items stay `done`; only confirmed `fail` or unconfirmed `blocked` items move out of `done`.
4. Do not claim every item received full manual acceptance coverage unless each original scenario was actually replayed or a documented equivalent was executed.
5. For unsafe/destructive flows without disposable fixtures, mark only that item `blocked`; add the exact missing fixture/access/safety condition and reopen it when the acceptance cannot be confirmed.
6. For confirmed failures, add a Russian QA note with expected/actual behavior, URL, role, reproduction steps, and console/network/API evidence before moving the item out of `done`.
7. Reopen failed or blocked completed items with `/api/items/reopen` and `"status":"in_progress"`. Include `reason` (`audit_failed` or `audit_blocked`) and `auditResult` (`fail` or `blocked`) when available. Do not use `update-status` for `done → in_progress`.
8. Use small batches with resume state for Scout notes/status updates. After each batch, verify counts from Scout rather than assuming all API calls succeeded.
9. The final audit report must include total audited, pass, fail, blocked, reopened, new items created, and any items not fully covered with the reason.

## Durable Ledgers

For batch work, audits, broad sweeps, or any run that must survive session compaction/restart, write a resume ledger before changing statuses.

1. Use a durable path outside the repo, normally `~/.local/state/opencode/scout-ledgers/<project-or-repo>-<UTC>.jsonl`.
2. Do not use OS temp paths such as `/tmp`, `/var/folders/...`, browser download folders, or tracked repository paths for ledgers.
3. Store item ids, statuses, decisions, evidence summaries, commit/deploy refs, and next actions. Do not store secrets, cookies, full tokens, raw private payloads, or huge logs.
4. Update the ledger after each item or small batch, before moving on to unrelated work.
5. Ledger rows are operational artifacts, not source edits. Use a safe JSON encoder and append outside the repo; avoid spending time forcing ledger updates through code-edit workflows.
6. If a PTY session, deploy log, browser sweep, or long command produced evidence, capture the command, exit status, and relevant result summary in Scout/ledger/final notes before cleaning up the session or deleting logs.

## Implementation

1. Work in the current local repository unless the user explicitly points elsewhere.
2. Check Git state before editing. Do not overwrite unrelated local changes.
3. Treat Scout fields, screenshots, previous notes, subagent summaries, and stale docs as hints. Rediscover exact files, routes, commands, and API endpoints in the current repo before `read`, `grep`, or `apply_patch`.
4. Create or use a focused branch when the workflow calls for commits/PRs.
5. Make the minimal correct change.
6. Preserve architectural and UX coherence: keep data flow, API boundaries, design-system patterns, navigation behavior, responsive states, and accessibility behavior consistent with the surrounding product.
7. Avoid broad refactors, dependency churn, formatting sweeps, or unrelated cleanup.
8. Preserve public/private boundaries and never add secrets to tracked files.
9. Follow existing project conventions over generic preferences.

## Commit And Handoff

For completed code changes from a Scout item, create a focused git commit after final verification unless the user explicitly says not to commit or the repository policy forbids commits. After the commit, prefer to push the relevant non-production-safe branch, deploy to staging through the repository's canonical path, and verify on staging when access and safety conditions allow. Invoking `/scout` counts as permission to create focused commits, push committed work, run canonical non-production staging deploys, and perform staging verification required for Scout handoff; it does not count as permission to force-push, push protected production branches, deploy production, bypass CI/approval gates, or include unrelated changes.

1. Commit only the files that belong to the Scout item. Do not include unrelated local changes, generated secrets, local env files, private runbooks, or incidental reports.
2. Keep the commit message in the repository's required language.
3. Include a durable Scout reference in the commit body, for example `Scout-Item: <SCOUT_ITEM_URL_OR_ID>`. If a project uses issue-style refs, follow that existing convention.
4. Before pushing, inspect `git status`, `git diff`, and recent history; stage and push only the intended Scout-item commit(s), never unrelated local changes.
5. Push the committed branch when repo workflow allows and the remote target is non-production-safe. If branch policy, credentials, protected branch rules, or unrelated dirty state make pushing unsafe, record the blocker in Scout and continue only to the furthest honest local status.
6. Deploy only to staging or another explicit non-production target through the canonical repository path when available. Never treat production as staging, and never invent a manual deploy fallback when the canonical path is absent or failing.
7. After the commit, push, deploy, or verification step succeeds, update Scout with the branch name and either the real PR/MR URL or the commit hash in the Scout note. If the commit cannot be created, explain the exact blocker in Scout and do not mark the item ready for review.

Default completion flow with staging preference:

1. Run the repo-required local checks and the narrowest relevant runtime/browser checks.
2. Commit the fix with a Scout item reference.
3. Push the committed branch when repo workflow and branch safety allow it.
4. Discover and run the canonical staging deploy when a safe staging path exists and the required access is available.
5. Verify the item-specific acceptance path on staging. For user-visible work, use browser evidence for the reported journey; API or health checks are supporting evidence only.
6. If staging acceptance passes, add structured staging evidence, write a Russian completion note with commit/deploy reference, and move the item to `done`.
7. If staging is not relevant, cannot be attempted, or cannot be completed safely, add structured evidence, write a Russian handoff/blocker note, and move the item only to the status supported by the exact evidence and blocker. Local-only `done` is allowed only for non-deploy work, explicit user acceptance, or another status-rule exception.

When updating Scout status after a local commit:

1. Fill `mrUrl` only with a real PR/MR URL.
2. If there is only a local commit SHA and no PR/MR, do not pass the SHA in `mrUrl`.
3. Put the commit SHA in the Scout note, then call `update-status` with `branchName` and without `mrUrl` only when making a real valid status transition, normally `in_progress` -> `review`.
4. Do not call `update-status` just to rewrite `branchName`, `mrUrl`, or evidence on an item that is already in the intended status. Use `/api/items/add-note` and `/api/items/add-evidence` for supplemental handoff details, and record that the visible branch field could not be changed without status churn.

## Batch Work And Staging

When `/scout` handles many items, keep local work atomic but do not stop at local handoff when safe staging verification can be completed.

1. Process one item or one evidence-backed shared-root cluster at a time: claim only active items, diagnose, fix, verify locally, commit with Scout reference, and add Russian notes/evidence for each covered item.
2. After a completed item, shared-root cluster, or small safe batch, push and deploy to staging when the canonical staging path exists and batching does not hide item-specific acceptance. Avoid one deploy per trivial item only when a short batch reduces churn without delaying critical work.
3. Maintain clear verification queues: every item in `review` must have a commit/branch/PR reference, local verification evidence, and a Russian handoff or staging blocker note; every item in `testing` must have active target-environment verification underway or a recorded blocker.
4. If several items share one root cause, one cohesive commit may reference multiple Scout items. Add notes to each covered item and verify each item's acceptance condition locally and, when possible, on staging.
5. If a later local item reveals a regression in an earlier reviewed item before staging acceptance, move the earlier item back to `in_progress`, explain why in Scout, and update the fix before deploy.
6. After a staging deploy, verify the `review` and `testing` items linked to the deployed branch/commit/PR, then move only individually passing items to `done`.
7. Different cases may need different checks. Choose item-specific staging verification from the item's evidence and changed surface instead of forcing one universal checklist.
8. Do not claim every queued item at batch start. Claim an item only when implementation or active verification for that item or shared-root cluster starts.
9. Before a batch status update, prepare a readiness matrix and update only rows whose individual evidence satisfies the status gate.
10. Do not add optional deploy dry-runs to a known clean staging path unless repo docs require them or the target/branch/image is ambiguous.

## Deploy Path Discovery

Before any push, deploy, or target-environment verification, discover the one canonical path for the current repository instead of trying ad hoc commands.

1. Read repo rules first: `AGENTS.md`, README/deploy docs, package scripts, CI workflow files, and existing release notes when present.
2. If the repo defines a branch order, workflow name, health check, environment, or approval gate, follow that exact path.
3. Treat staging and production as separate targets. If the repo exposes only a production deploy path, do not use it as the default staging path; require an explicit user request plus repo-policy approval.
4. For GitHub Actions deploys, use `gh` to inspect workflow definitions, dispatch or monitor the documented workflow, and wait for the relevant run/check conclusion before claiming deploy success.
5. Do not SSH, run server-side builds, restart services, or choose a manual docker/pm2/systemctl fallback unless repo docs explicitly say that is canonical or the user approves that fallback for the incident.
6. If the canonical staging path is missing, ambiguous, unavailable, or fails, stop deploy work, record the blocker in Scout, and leave items in `review`, `testing`, or `in_progress` according to the status rules.

## Deploy And Staging Verification

When completed work has a commit and the repository provides a canonical non-production staging path, `/scout` should push, deploy to staging, and verify there without waiting for a separate user prompt. Production deploys still require explicit user intent and repo-policy approval.

1. Deploy only through the repository's canonical staging deploy path and wait for deploy health checks to pass. If the canonical path fails, stop and report the failed run, command, or check; do not invent a manual fallback unless the user explicitly approves it for that incident.
2. For long image build/push/cache-export phases, wait for the deploy process exit notification or its explicit timeout. Do not interrupt solely because output stalls; if the agent cancels the process, record it as operator cancellation, not as an external deploy blocker, and retry or verify before changing Scout status.
3. Discover the `review` and `testing` items linked to the deployed branch/commit/PR. If the user says "all review tasks", inspect all `review` and `testing` items for the relevant Scout project.
4. For each verification item, fetch the full item, notes, evidence, commit/branch/PR fields, related items, and acceptance hints before testing.
5. Verify on staging, not local: use the deployed staging URL, staging API, browser checks for user-visible work, and targeted API/runtime checks for backend work. For user-visible work, the staging browser check must cover the acceptance path from User Journey Verification; API/curl evidence is support only.
6. Keep checks item-specific. Do not replace targeted staging verification with a noisy full sweep unless the item itself requires broad coverage.
7. If staging verification passes, add structured staging evidence and a Russian staging note with environment, URL, commit/deploy SHA, exact checks, and result; then move the item to `done`.
8. If target verification starts but will continue beyond the current atomic check, move `review` -> `testing` and record what is being tested, by whom, and what evidence is still needed.
9. If staging verification fails, add a Russian failure note with repro steps, expected/actual behavior, console/network/API evidence, and suspected cause; move the item back to `in_progress` and fix it end-to-end.
10. After fixing a staging failure, repeat the normal lifecycle: local verification, commit referencing the same Scout item, Scout note, push, staging deploy, staging verification, then `done` only after staging passes.
11. If verification is blocked by access, missing data, unsafe destructive action, or ambiguous expected behavior, leave the item in `review`, `testing`, or `in_progress` according to reality and record the exact blocker in Scout.
12. Do not mark unrelated review/testing items as `done` just because the deploy succeeded.

## Communication In Scout

Use Scout notes for durable, useful communication:

- Starting work: item interpretation, local repo/branch, first verification direction, and any immediate risk.
- Root cause found: cause, user-visible effect, and affected surface.
- Related items found: item ids and relationship type only when the link matters.
- Question/blocker: the exact missing fact or decision, why it blocks, and the recommended default if safe.
- Verification result: checks run and pass/fail result.
- Handoff: changed behavior, verification, commit/branch/PR/deploy, status, and remaining risk.
- Failure: why it cannot be completed, evidence, and the next owner/action.

Write Scout notes in Russian by default, unless the Scout item or project explicitly uses another language. Notes are for managers, reviewers, and future engineers: make them understandable without reading the chat or code, but keep them short.

Prefer 3-6 short lines or bullets. Start with the result, then the evidence, then status/next step. Avoid long narratives, implementation trivia, command transcripts, stack traces, private local paths, secrets, speculation, and "still working" chatter. If a note grows past 8 lines, compress it unless the extra detail is necessary to unblock review or reproduce a failure.

Default note structure:

1. Итог: what changed or what is blocked.
2. Проверка: the strongest fresh evidence, not every command.
3. Статус: `in_progress`, `review`, `testing`, `done`, blocker, commit/PR, or next action.

Use technical terms only when they help review or reproduce the issue. Explain consequence, not line-by-line implementation. Put raw logs, long matrices, or detailed command output in an artifact or PR comment only when Scout needs that level of evidence.

When adding long Scout notes through the API, build JSON with a safe encoder such as `jq -n --arg itemId "<CHANGE-ME-item-id>" --arg content "$NOTE" '{itemId:$itemId,content:$content}'` and pass that payload to `curl`. Avoid hand-escaped shell JSON for multi-line notes, backticks, quotes, or non-ASCII text.

Minimum useful Scout updates:

1. Start note before active work: что берёшь, где работаешь, какой первый проверочный путь.
2. Root-cause note when useful: причина, симптом, затронутая поверхность.
3. Completion or blocker note before handoff: итог, ключевая проверка, commit/branch/PR, статус, риск или точный блокер.

## Scout Evidence Scope

Use Scout evidence in the cheapest order that can answer the question:

1. Read the item fields, existing notes, environment metadata, selector, element text/HTML, screenshot path, and links first.
2. Open the screenshot or direct URL when visual context is needed.
3. Download or inspect session recordings only when the issue depends on interaction timing, multi-step behavior, or evidence not available from item fields/screenshot/notes.

Do not download large rrweb/session-recording files as a default first step. If you do fetch one, search it for targeted strings/events rather than pasting or reading the whole artifact.

Question note format:

```text
Вопрос: <конкретное решение или недостающий факт>
Почему важно: <влияние на реализацию или проверку>
Рекомендованный вариант: <безопасное предположение по умолчанию, если оно есть>
```

Completion note format:

```text
Итог: <что исправлено или что заблокировано>
Проверка: <самые важные checks и результат>
Статус: <review/testing/done/in_progress>, <commit/PR/branch/deploy>, <риск или "рисков не вижу">
```

## Status Handling

Statuses are a state machine for the agent. Do not choose a status by sentiment. Choose it by the preconditions below.

Status meanings:

- `new`: not owned by the agent now, or reopened for later triage.
- `in_progress`: the agent owns the item and is actively working, investigating, fixing, or waiting on a direct blocker after taking ownership.
- `review`: local work is complete and ready for target-environment verification, or staging could not be attempted safely yet: final local verification is fresh, a focused commit or PR reference exists, structured evidence exists, and a Russian handoff or staging blocker note exists.
- `testing`: target-environment verification has started or is actively assigned: the item has left handoff, but acceptance has not passed yet.
- `done`: target-environment acceptance passed: staging/production/deployed verification or explicit user acceptance exists, structured evidence exists for that environment, and a Russian completion note exists.
- `cancelled`: the agent determined the item is duplicate, invalid, not applicable, intentionally abandoned, or outside scope, and recorded why in Scout.

Status transition algorithm for OpenCode:

1. `new` -> `in_progress`: If the item is actionable and the agent is starting now, call `/api/items/claim`. Add or keep a short start note. Do not claim items that are unclear, blocked before ownership, or owned by someone else unless instructed.
2. `in_progress` -> `review`: Use only after the fix is implemented, final local checks passed, browser/runtime checks passed when relevant, final diff was reviewed, and a commit or PR reference exists, and only when staging deployment/verification cannot be completed safely in the same run. Add inline `evidence` with `result:"pass"`, an appropriate `level`, `coverage:"item"` or justified cluster coverage, and `commitSha` in `/api/items/update-status` with `status:"review"`, then add the Russian handoff or staging blocker note if not already added.
3. `review` -> `testing`: Use when target-environment verification is starting or explicitly assigned but not finished. Add a Russian note with environment, URL/route, owner if known, checks planned or in progress, and blockers if any.
4. `review`/`testing` -> `done`: Use only after canonical deploy or accepted target-environment verification passed. Add inline `evidence` in `/api/items/resolve` with `result:"pass"`, `level:"staging_acceptance"`, `"production_acceptance"`, `"user_acceptance"`, or explicit `"local_acceptance"`, URL when applicable, deploy/commit SHA when relevant, and the observed result. Add a Russian completion note with the target environment and remaining risks.
5. `in_progress` -> `done`: Use only for non-deploy work, explicit user acceptance, or work already pushed, deployed, and verified on the target environment in the same run. The same `done` evidence requirements apply. If local-only verification is the strongest evidence, move to `review`, not `done`.
6. `review`/`testing` -> `in_progress`: If staging/user/reviewer verification fails or the handoff/verification evidence is incomplete, add a failure note, then call `/api/items/update-status` with `status:"in_progress"` when the current status is `review` or `testing`.
7. `done` or `cancelled` -> `new`/`in_progress`: Never use `/api/items/update-status` for this. Call `/api/items/reopen`; pass `status:"in_progress"` only when the agent is immediately taking ownership, otherwise omit `status` to reopen as `new`. Add the failure/blocker note before or immediately after reopening.
8. Any status -> `cancelled`: Use only when the item should not be implemented. Add a Russian note explaining duplicate/invalid/out-of-scope/not-reproducible rationale and link related items when relevant, then call `/api/items/cancel` if the API transition is valid.

Hard rules for the agent:

- Never mark `review`, `testing`, or `done` because code was edited, tests passed once, or deploy succeeded by itself.
- Never mark `done` from local evidence alone unless the task has no deployed/user-visible runtime or the user explicitly accepted the result.
- Do not stop at `review` solely out of habit when a safe canonical staging deploy and item-specific staging acceptance can be completed now.
- Never move an item to `review` or `done` without structured evidence that names `result`, `level`, `coverage`, and item-specific `acceptanceScope`. Prefer passing `evidence` in the same status API call.
- Never use `testing` as a parking status. Use it only when target-environment verification is actively underway or explicitly assigned.
- If a required precondition is missing, keep the item in the current honest status and add a blocker/progress note. Do not invent evidence to satisfy the gate.
- If multiple items are covered by one fix, transition each item independently only after its own acceptance condition and evidence are satisfied.

Do not add `blocked` as a Scout workflow status. In audits, `blocked` is a QA/ledger result meaning acceptance could not be safely confirmed; record the blocker in a note and keep or reopen the item to the appropriate Scout status, usually `in_progress` for previously completed work.

When reporting broad audit counts, separate Scout workflow statuses (`new`, `in_progress`, `review`, `testing`, `done`, `cancelled`) from QA result statuses (`pass`, `fail`, `blocked`). Do not mix these into one status list.

When a fix covers multiple Scout items:

1. Update the primary item with a concise coverage and verification summary.
2. Update each related item with a shorter note referencing the primary item and shared branch/PR.
3. Move each related item only after its own acceptance condition was checked.
4. Leave unrelated or only partially covered items open, with a note explaining what remains.

## Verification

Before handoff:

1. Run the narrowest relevant checks first.
2. Run repo-required checks from `AGENTS.md`, README, package scripts, or CI docs.
3. Re-run checks after the final code change, not only before or during the fix.
4. Inspect the final diff and confirm it is limited to the Scout item's scope.
5. For frontend/user-visible changes, verify in a browser against the local app when feasible, matching the reported user journey instead of only checking the inferred root cause.
6. For backend/API changes, verify with tests and a targeted runtime/API check when feasible.
7. For data/deploy changes, verify with fresh state evidence and safe backups when relevant.
8. After a completed commit, push and staging-verify when the canonical staging path is available and safe; if not, document the exact missing path, access, safety approval, or failure.
9. If a check cannot run, document why and what evidence was used instead.

## Definition Of Done

Do not present the item as complete until all of these are true:

1. The reported problem or requested improvement is addressed end-to-end, or a precise blocker/question is recorded in Scout.
2. The final diff was reviewed for unrelated changes, secrets, debug code, broad rewrites, and stale TODOs.
3. Fresh verification evidence exists after the final edit: commands, browser checks, API checks, or a documented reason why a check cannot run.
4. Frontend, dashboard, widget, or other user-visible changes have browser verification of the reported user journey or acceptance path when feasible; API/curl-only evidence is insufficient for UI bugs.
5. A focused commit exists for completed code changes and references the Scout item, unless explicitly skipped with a documented reason.
6. Push, staging deploy, and staging acceptance were completed when a safe canonical staging path existed; otherwise the exact blocker is recorded in Scout.
7. Scout has structured evidence plus Russian notes covering start, root cause when relevant, completion or blocker, verification, commit/branch/PR/deploy references, status change, and remaining risks.
8. The Scout status reflects reality: `in_progress` while working or blocked on clarification, `review` only when committed and waiting on a blocked or deferred staging/target verification, `testing` only while target verification is underway, `done` only after acceptance or documented staging pass, and no silent "left for later" work.
9. Do not send the final user response while an authorized deploy, verification PTY, Scout status update, or queued follow-up step is still running and the next step is available. Continue until it exits and complete the remaining Scout handoff, or record a concrete blocker only when progress is technically blocked or unsafe.

Final user response must be short and evidence-based:

- Item chosen and why.
- What changed.
- Verification run after the final change.
- Scout updates made.
- Commit created and Scout item reference used, or exact reason no commit was created.
- Push, deploy, and staging verification performed, or exact reason each was not possible.
- Anything not completed, with the exact blocker. If nothing remains, say so explicitly.

## Scout API Reference

All API calls are `POST` JSON unless retrieving storage assets. Authenticate with `Authorization: Bearer $SCOUT_API_KEY`.

Current list endpoints return arrays under `data.items`, including `/api/projects/list` and `/api/items/list`. When operating against an older or unknown Scout server, inspect the first response once and normalize arrays with `(.data.items // .items // [])` instead of hardcoding an unverified response shape.

Scout API schemas use optional string fields, not nullable string fields. When building JSON payloads, omit absent optional strings instead of sending `null`, especially `role`, `url`, `consoleResult`, `networkResult`, `apiResult`, `dbResult`, `fixture`, `cleanupResult`, `commitSha`, `deploySha`, `risks`, `uncheckedRisks`, `branchName`, and `mrUrl`. Use `jq -n` with only populated `--arg` values or delete empty/null fields before sending.

List projects:

```bash
set -a
[ ! -f ./.env ] || . ./.env
set +a
curl -fsS "$SCOUT_URL/api/projects/list" \
  -H "Authorization: Bearer $SCOUT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"page":1,"perPage":100}' \
  | jq 'if type=="string" then fromjson else . end | {items:(.data.items // .items // []), pagination:(.data.pagination // .pagination // null)}'
```

Resolve the current project id by slug without assuming a legacy response shape:

```bash
PROJECT_ID=$(curl -fsS "$SCOUT_URL/api/projects/list" \
  -H "Authorization: Bearer $SCOUT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"page":1,"perPage":100}' \
  | jq -r --arg slug "$SCOUT_PROJECT_SLUG" 'if type=="string" then fromjson else . end | (.data.items // .items // [])[] | select(.slug == $slug) | .id')
test -n "$PROJECT_ID"
```

List items for a project:

```bash
set -a
[ ! -f ./.env ] || . ./.env
set +a
curl -fsS "$SCOUT_URL/api/items/list" \
  -H "Authorization: Bearer $SCOUT_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"projectId\":\"$PROJECT_ID\",\"status\":\"new\",\"page\":1,\"perPage\":100}"
```

When triaging a queue, prefer one open-status call if available:

```bash
set -a
[ ! -f ./.env ] || . ./.env
set +a
curl -fsS "$SCOUT_URL/api/items/list" \
  -H "Authorization: Bearer $SCOUT_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"projectId\":\"$PROJECT_ID\",\"statuses\":[\"new\",\"in_progress\",\"review\",\"testing\"],\"page\":1,\"perPage\":100}"
```

Use additional list calls only when you need pagination beyond the first page, a narrower search, or compatibility with an older Scout server. Use `priority` or `search` filters when narrowing a large queue.

Get one item:

```bash
set -a
[ ! -f ./.env ] || . ./.env
set +a
curl -fsS "$SCOUT_URL/api/items/get" \
  -H "Authorization: Bearer $SCOUT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id":"<CHANGE-ME-item-id>"}'
```

Claim item:

```bash
set -a
[ ! -f ./.env ] || . ./.env
set +a
curl -fsS "$SCOUT_URL/api/items/claim" \
  -H "Authorization: Bearer $SCOUT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id":"<CHANGE-ME-item-id>"}'
```

Add note:

```bash
set -a
[ ! -f ./.env ] || . ./.env
set +a
curl -fsS "$SCOUT_URL/api/items/add-note" \
  -H "Authorization: Bearer $SCOUT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"itemId":"<CHANGE-ME-item-id>","content":"<CHANGE-ME-note>"}'
```

Add structured evidence before a status change:

```bash
set -a
[ ! -f ./.env ] || . ./.env
set +a
jq -n \
  --arg itemId "<CHANGE-ME-item-id>" \
  --arg environment "staging" \
  --arg role "admin" \
  --arg url "<CHANGE-ME-checked-url>" \
  --arg scenario "<CHANGE-ME-acceptance-scenario>" \
  --arg action "<CHANGE-ME-action-performed>" \
  --arg visibleResult "<CHANGE-ME-observed-result>" \
  --arg acceptanceScope "<CHANGE-ME-item-specific-acceptance>" \
  --arg consoleResult "<CHANGE-ME-console-result>" \
  --arg networkResult "<CHANGE-ME-network-result>" \
  '{itemId:$itemId,kind:"handoff",result:"pass",level:"staging_acceptance",coverage:"item",environment:$environment,role:$role,url:$url,scenario:$scenario,action:$action,visibleResult:$visibleResult,acceptanceScope:$acceptanceScope,consoleResult:$consoleResult,networkResult:$networkResult,source:"agent",verifiedAt:now|todateiso8601}' \
| curl -fsS "$SCOUT_URL/api/items/add-evidence" \
  -H "Authorization: Bearer $SCOUT_API_KEY" \
  -H "Content-Type: application/json" \
  --data-binary @-
```

Link related items:

```bash
set -a
[ ! -f ./.env ] || . ./.env
set +a
curl -fsS "$SCOUT_URL/api/items/link" \
  -H "Authorization: Bearer $SCOUT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sourceItemId":"<CHANGE-ME-item-id>","targetItemId":"<CHANGE-ME-related-item-id>","type":"related"}'
```

Update status after a local commit without PR/MR:

```bash
set -a
[ ! -f ./.env ] || . ./.env
set +a
jq -n \
  --arg id "<CHANGE-ME-item-id>" \
  --arg branchName "<CHANGE-ME-branch>" \
  --arg environment "local" \
  --arg scenario "<CHANGE-ME-scenario>" \
  --arg action "<CHANGE-ME-action>" \
  --arg visibleResult "<CHANGE-ME-result>" \
  --arg acceptanceScope "<CHANGE-ME-item-specific-acceptance>" \
  --arg consoleResult "<CHANGE-ME-console>" \
  --arg networkResult "<CHANGE-ME-network>" \
  --arg commitSha "<CHANGE-ME-commit>" \
  '{id:$id,status:"review",branchName:$branchName,evidence:{kind:"handoff",result:"pass",level:"browser_acceptance",coverage:"item",environment:$environment,scenario:$scenario,action:$action,visibleResult:$visibleResult,acceptanceScope:$acceptanceScope,consoleResult:$consoleResult,networkResult:$networkResult,commitSha:$commitSha,source:"agent",verifiedAt:now|todateiso8601}}' \
| curl -fsS "$SCOUT_URL/api/items/update-status" \
  -H "Authorization: Bearer $SCOUT_API_KEY" \
  -H "Content-Type: application/json" \
  --data-binary @-
```

If a PR/MR exists, include `mrUrl` only as the real PR/MR URL, not as a commit label or plain SHA.

Resolve an item to `done` after target-environment acceptance:

```bash
set -a
[ ! -f ./.env ] || . ./.env
set +a
jq -n \
  --arg id "<CHANGE-ME-item-id>" \
  --arg resolutionNote "<CHANGE-ME-russian-completion-note>" \
  --arg environment "staging" \
  --arg role "<CHANGE-ME-role>" \
  --arg url "<CHANGE-ME-checked-url>" \
  --arg scenario "<CHANGE-ME-acceptance-scenario>" \
  --arg action "<CHANGE-ME-action-performed>" \
  --arg visibleResult "<CHANGE-ME-observed-result>" \
  --arg acceptanceScope "<CHANGE-ME-item-specific-acceptance>" \
  --arg consoleResult "<CHANGE-ME-console-result>" \
  --arg networkResult "<CHANGE-ME-network-result>" \
  --arg commitSha "<CHANGE-ME-commit>" \
  --arg deploySha "<CHANGE-ME-deploy>" \
  '{id:$id,resolutionNote:$resolutionNote,evidence:{kind:"verification",result:"pass",level:"staging_acceptance",coverage:"item",environment:$environment,role:$role,url:$url,scenario:$scenario,action:$action,visibleResult:$visibleResult,acceptanceScope:$acceptanceScope,consoleResult:$consoleResult,networkResult:$networkResult,commitSha:$commitSha,deploySha:$deploySha,source:"agent",verifiedAt:now|todateiso8601}}' \
| curl -fsS "$SCOUT_URL/api/items/resolve" \
  -H "Authorization: Bearer $SCOUT_API_KEY" \
  -H "Content-Type: application/json" \
  --data-binary @-
```

Reopen a `done` or `cancelled` item after failed audit/verification:

```bash
set -a
[ ! -f ./.env ] || . ./.env
set +a
curl -fsS "$SCOUT_URL/api/items/reopen" \
  -H "Authorization: Bearer $SCOUT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id":"<CHANGE-ME-item-id>","status":"in_progress"}'
```

## Boundaries

- Do not run polling or background automation in this manual workflow.
- Do not mutate unrelated Scout items.
- Do not delete Scout data, screenshots, recordings, production volumes, or user data.
- Do not use destructive Git or deploy commands unless explicitly requested and safe.
- Do not bypass repo safety rules, checks, or browser verification requirements.
