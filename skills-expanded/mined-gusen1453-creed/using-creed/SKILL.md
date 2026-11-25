---
name: using-creed
description: "Use when starting any conversation in a Creed-enabled workspace, or when unsure which Creed skill applies, before any creative, test, debug, or ship work."
---

# Using Creed

> **Output language:** answer and write artifacts in the user's own language (match their messages, not the repo's history).

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, ignore this skill.
</SUBAGENT-STOP>

## When to use this skill

- Session start in a Creed workspace
- Unsure which Creed skill applies
- First use / companion skills may be missing
- Before creative, test, debug, or ship work — pick the right skill first

## Quick Start (install)

Companion skills are required — `using-creed` alone is not enough:

```bash
npx skills add Gusen1453/creed
```

## Detect install

Required skills: `explore`, `grill`, `issue`, `write-spec`, `solid`, `write-plan`, `tdd`, `test-design`, `debug`, `review`, `commit-and-push`.

If any are missing from the workspace skill list: **stop and ask the user to run the install command above** before doing the work. Do not invent Creed workflows from memory.

**Installed but stale?** The repo is only the source; the install is a snapshot, so editing the repo changes nothing until reinstall. Detect a stale install and refresh it (only with the user's explicit confirmation) — see [references/install-and-update.md](references/install-and-update.md).

## How to use

1. Match the task to a skill in the map below.
2. Announce `Using <skill> to …`, read that skill, follow it.
3. If it has a checklist, one todo per item.
4. When several apply, follow the default flow; between two work products run a **transition gate** (§ below) — never auto-advance into the next skill and never auto-review:

```
using-creed
  → explore? → grill → [gate] → issue? → write-spec → [gate] → solid? → [gate]
  → write-plan → [gate] → tdd (+ test-design)
  → [gate] → debug? → [gate] → review → [gate] → commit-and-push
```

`explore?` = Gate when the task modifies or references existing code (refactor / legacy / reuse); skip when greenfield.

`issue?` = at grill's exit gate, one option files the intent as a trackable issue before the spec; picking it returns to the same gate. Skip when nothing is being shelved.

`solid?` = Gate only when the slice adds modules / ports / IO edges; skip when no new boundary. Skipped → the `write-spec → solid` and `solid → write-plan` gates merge into one `write-spec → write-plan` gate (review object stays the spec; only the review-boundaries option drops).

`[gate]` = transition gate — one AskUserQuestion at each handoff; see **Transition gates**.

## Transition gates

Most producing skills end with a **Transition gate** section of their own: one
**AskUserQuestion** at handoff — never auto-advance into the next skill, never
auto-review. **The options are not identical across skills, and not every skill
has one.** grill's gate is proceed / re-open the design / file an issue first /
other, and it has no review option (nothing is written yet to review); `issue`
deliberately has **no gate of its own** — cold-start it just reports, and in the
pipeline it hands control back to grill's gate, so the question is asked once.
The rest follow the shape below. **Read the skill's Hand-off rather than
assuming.**

```
A) Recommended: Proceed → <next skill>
B) Review first — run **review** on the just-finished <object>
   (its rubric in the review skill's `references/`), then return to this gate and re-ask
C) Adjust — go back to <producing skill>, revise the <object>, then re-gate
D) Something else (I will type it)
```

Rules (for the gates that follow the shape above — grill's differ, and `issue` has none):

- **Choose B** → run **review** on that object with its rubric (it checks the
  object against its direct upstream; a claim→case table is mandatory). Fix Critical +
  Important findings, or have the user defer them with a reason. Then **return to
  the same gate** and re-ask — the user may pick A, request another review round,
  or adjust.
- **Choose C** → return to the producing skill, revise, then re-gate the object.
- **Skip only when** the user said "skip the gates this session" or explicitly
  waives a particular gate. The gate is one quick question, not ceremony —
  "too simple to ask" is the anti-pattern.

Two gates are custom: **grill → write-spec** has nothing to review yet (the spec
isn't written — no review option: proceed / re-open the design / file an issue
first); **review → commit-and-push** guards the report verdict (proceed only when
Critical/Important are fixed or waived — never blind auto-ship).

Skipped `solid?` (no new boundary) → the `write-spec → solid` and `solid →
write-plan` gates merge into one `write-spec → write-plan` gate (review object
stays the spec; only the review-boundaries option drops).

## Skill map (scenarios)

| Situation | Skill |
|-----------|--------|
| Refactor / rework existing code — task names methods/classes/tables to change or reference | **explore** → grill → write-spec → … |
| New feature / behavior change / architecture / "grill me" / brainstorm — before any code | **grill** |
| Record / file something to track later — "记一下这个 bug", "提个 issue", "这个先放着", a bug report or feature request | **issue** |
| Approved design → durable product spec (scenarios, scope, decision log) | **write-spec** |
| After spec: lock packages/ports/dependency arrows; or mock piles / coupling smell | **solid** |
| Approved spec (and solid if needed) → break multi-step work into TDD tasks | **write-plan** |
| Writing production code (feature / bugfix / refactor) | **tdd** |
| Writing or reviewing tests: worth testing? unit vs integration? what to assert / mock? | **test-design** |
| Bug, test/CI failure, unexpected behavior, or about to claim "fixed" | **debug** |
| Finished a task slice / before opening or updating a PR | **review** |
| Stage handoff — the user decides what happens next | the producing skill's **Hand-off** section (options vary; `issue` has none) |
| Review a spec / plan / structure decision as its own object (not code) | **review** (routes to `references/{spec,plan,solid}.md`) |
| User asks to commit / push / open a PR (PR needs a Test plan) | **commit-and-push** |

Common pairings:

- **explore → grill** — explore harvests repo facts (anchors, assertion checks, conflicts); grill then asks only the judgment calls.
- **grill → write-spec** — grill aligns decisions; write-spec locks what/why for mentoring and handoff.
- **write-spec vs write-plan** — spec = product scenarios & trade-offs; plan = files, order, RED→GREEN.
- **write-spec → solid? → write-plan** — solid is a Gate when boundaries are new; not a mandatory every-time step.
- **tdd + test-design** — tdd is the rhythm (test first, watch it fail); test-design decides what to feed, assert, and mock. Use both when implementing.
- **debug → tdd** — bug fixes: root cause with evidence first, then a failing regression test.
- **grill & solid** — during grill, only note boundary *smells* in options; do **not** switch the main skill to solid until what/why is locked.

## Minimal task prompt template (for the human)

Three blocks; the agent explores the rest and grills only what the repo can't answer:

```
Task: <one-line intent, name the method/class to change>
Hard constraints: <numbers, policies, red lines — only you know these>
Explore hints (optional): <class/method names to reference; the agent reads them itself — no need to describe>
Acceptance (optional): <one line of demo language: how we'll know it works>

Let the agent explore the repo for the rest; grill it only on judgment calls. Run /grill
```

Rules for the hard-constraints slot:

- Soft-constraint wording ("try not to" / preference style) = **priority, not a prohibition**. If it conflicts with repo reality (e.g., re-run idempotency), explore flags the conflict in the fact checklist and grill turns it into a trade-off question for you to decide.
- Don't write SQL, field names, method signatures, or assembly details — those are repo-answerable facts; writing them risks contradicting the code.

Example (before → after) — the same task: ~600 chars → ~150 chars. Everything cut was repo-answerable (SQL, field names, method signatures, assembly details); everything kept is human-only (concurrency, retry policy, red lines):

```
Before: 6-step flow + 3 SQL snippets + thread-pool/retry/Redis details + "the response format needs to be
List<ImageEmbeddingUpdateRequest.ContentItem> batchContentList" (a guess about the code)

After: Refactor RagRecoverPushJob#imageRecover to re-push dp_research_report_structure_info
(data_source in ('2','3'), id 111~2000) to the vector DB.
Hard constraints: descending pagination, 1000 per batch; 40-concurrency thread pool; on push failure retry
once, then enqueue to Redis for retry; try not to update dp_research_report_image_search.
Explore hints: SecAnnouncementThreadPoolManager, PushImageChunkService#buildReportChunkDto/#sendListToRag.
Let the agent explore the repo for the rest; grill it only on judgment calls. Run /grill
```

## Checklist

- [ ] Companion Creed skills installed (else → Quick Start)
- [ ] Relevant Creed skill identified (or consciously N/A)
- [ ] Skill read/followed; announced
- [ ] Transition gate run at each `[gate]` — user chose one of *that skill's* options (proceed / review / adjust, or grill's re-open / file-an-issue), or explicitly waived
