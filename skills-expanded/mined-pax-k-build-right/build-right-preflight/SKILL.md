---
name: build-right-preflight
description: Guide founder/product pre-execution setup before AI implementation. Use when the user invokes /build-right-preflight, wants to bootstrap a blank or existing project, capture founder intent, validate assumptions, create product truth, define MVP scope, create operating docs, create Sprint 0 tasks, or prepare the first executable AI task.
---

# Build Right Preflight

Use this skill to prepare a project before repetitive AI execution begins.

Core rule:

```text
AI drafts the map.
Founder validates the terrain.
Evidence upgrades assumptions into truth.
Only then AI executes.
```

## Required Reading

- Always read `references/workflow.md` before acting.
- Read `references/founder-gates.md` before asking founder questions,
  deciding readiness, or advancing past a stop/ask gate.
- Read `references/research-and-delegation.md` only when web research,
  public-evidence claims, existing-project inventory, conflict review, or
  subagent delegation triggers apply.
- Read `references/artifact-contract.md` before creating or updating docs or
  tasks.
- Read `references/domain-language.md` when overloaded terms, aliases, multiple
  actors, or missing domain expertise affect requirements.
- Read `references/prototype-routing.md` when a behavioral or visual question
  can be answered empirically before planning.
- Read `../build-right-engineering-principles/references/principles.md` when
  creating or changing architecture boundaries, execution rules, package
  ownership, provider boundaries, generated-code rules, or enforceable
  engineering policy.
- Use files in `assets/templates/` as starting points when creating artifacts.
- Use bundled `scripts/preflight-check.ts` for deterministic inventory,
  readiness signals, and one preflight decision. Treat script output as input
  to judgment, not authority.
- Use bundled `scripts/ensure-openspec.ts` after repository inventory. This is
  Build Right's idempotent managed planning setup; do not ask the user to
  install, initialize, configure, or invoke the planning provider.
- Invoke every managed helper used as evidence as its own direct Bun shell
  command. Do not chain it with `&&`, `;`, pipes, redirects, or trailing
  commands; the native evidence gate binds success to that isolated invocation.

## Operating Mode

1. Inspect the project first.
2. Classify it as blank/new or existing.
3. Classify source mode as `founder-fed`, `web-assisted`, or
   `public-first-prototype`.
4. Run the read-only preflight helper when available:

   ```sh
   bun <skill-path>/scripts/preflight-check.ts --cwd <project> --mode all --format markdown
   ```

   Then run managed planning setup before artifact creation or readiness:

   ```sh
   bun <skill-path>/scripts/ensure-openspec.ts --cwd <project> --format markdown
   ```

   Stop fail-closed on provider/runtime, compatibility, or setup failure.

5. Report the helper findings before writing:

   ```text
   Preflight decision: <decision>
   Confidence: <confidence>
   Project type: <blank/new | existing>
   Next action: <next action>
   Missing artifacts: <paths or none>
   Readiness warnings: <warnings or none>
   Founder input gaps: <gaps or none>
   ```

6. Reconcile the helper decision before continuing:

   - `delegate-inventory`: run or prompt an existing-project inventory review.
   - `ask-founder`: ask the smallest useful founder-question batch.
   - `run-research`: run bounded public research and record public evidence.
   - `write-artifacts`: create or update missing canonical docs.
   - `create-sprint0`: create Sprint 0 and the first bounded executable task.
   - `ready-for-execution`: prepare handoff to execution.
   - `blocked`: record the blocker and stop or ask.

7. Announce a concise file plan:

   ```text
   Create:
   - <path> - <purpose>

   Update:
   - <path> - <purpose>

   Leave untouched:
   - <path> - <reason>

   Needs user input:
   - <question or blocker>
   ```

8. In interactive runs, ask a focused founder-question batch before treating
   founder intent, customer, positioning, MVP, or product promise as captured.
   If those answers are already explicit in the prompt or repo docs, record the
   evidence path instead of asking again.
9. Look up repository and public facts directly. Ask founders for decisions,
   not discoverable facts. When missing knowledge belongs to a domain expert,
   create a bounded questionnaire instead of inventing an answer.
10. Create or update `CONTEXT.md` only when overloaded terms, important aliases,
    or multiple actors/concepts materially affect requirements. Keep it
    implementation-free and optional.
11. Route empirically answerable behavioral or visual uncertainty to
    `$build-right-prototype`. Record the result as prototype evidence or a
    `prototype-assumption`, never customer validation.
12. Create or update docs and task files by default after the file plan.
13. Stop before writing only when the user requested planning-only mode, a write
   would overwrite substantial ambiguous content, project state is too unclear
   for a safe edit, or the target belongs to an unrelated generated workflow.
14. Ask founder questions in small batches. Do not ask for everything at once.
   If the user does not answer, continue only with repo-evidence inventory and
   mark founder-owned claims as blocked or needing founder validation.
15. If founder context is thin and fast prototyping is allowed, use bounded web
   research to fill gaps and mark those claims as `prototype-assumption` or
   `public-evidence-backed`.
16. Use subagents when a required delegation trigger applies and subagent tools
    are available. If a trigger applies but subagents are unavailable or the
    user forbids them, record the skipped review and reduce confidence.
17. Mark unsupported claims as assumptions. Do not invent product truth.
18. Prepare the first executable task, but do not complete it unless the user
   explicitly asks to continue into execution.
   For an existing project whose completed baseline and blueprint explicitly
   route next to `build-right-feature-planning`, preserve that handoff instead
   of inventing a duplicate non-managed execution task.
19. Run the preflight helper again after artifact creation when available, then
    reconcile its warnings against the readiness gate.
20. Report the helper decision again before claiming readiness.
21. End with an explicit readiness result. If founder input, external evidence,
    required research, or required review is missing, stop at the gate instead
    of advancing as if ready.

## Project Classification

Treat a project as blank/new when it lacks most product docs, task trackers, and
authority docs. A scaffolded codebase with no product truth still counts as
pre-execution blank.

Treat a project as existing when it has meaningful docs, code structure, task
tracking, release process, or prior product decisions. Preserve existing
structure and create a source index before filling gaps.

## Stop States

Use one of these closeout states:

```text
Go for prototype
Go for Sprint 0
No-go for product features
Needs founder/customer validation before product commitment
First blocker: <task path>
First executable AI task: <task path>
```

## Automatic Action Boundary

Never automatically commit, push, merge, publish, deploy, or abort or resolve
an existing Git operation. Perform those actions only when the user explicitly
authorizes the exact action and target.

## User-Visible Status Badge

End every final response with exactly one status badge block:

```text
🟢 [GREEN] Status: ALL GREEN
Decision: <decision/result>
Next action: <next action or none>
Needs user input: <none | concise ask>
Blocked by: <none | blocker>
```

Use this status map:

- `🟢 [GREEN] Status: ALL GREEN` for `ready-for-execution`,
  `Go for Sprint 0`, `Go for prototype`, or first executable task ready.
- `🟡 [YELLOW] Status: NEEDS INPUT` for `ask-founder` or
  `Needs founder/customer validation before product commitment`.
- `🟠 [ORANGE] Status: NEEDS WORK` for `delegate-inventory`,
  `run-research`, `write-artifacts`, or `create-sprint0`.
- `🔵 [BLUE] Status: WAITING EXTERNAL` for missing external proof,
  publishing, indexing, credentials, paid services, production access, or
  third-party state.
- `🔴 [RED] Status: BLOCKED` for `blocked`, `No-go for product
  features`, open conflicts, failed verification, stale/source mismatch, or
  invalid state.

Do not claim product-feature readiness until product truth, MVP scope, evidence,
operating rules, and at least one bounded executable task exist.
