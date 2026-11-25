---
name: poc-spec-driven-builder
description: Use this skill whenever the user wants Claude Code to build a proof of concept (PoC), prototype, or "prove this idea works" — even if they just describe an idea informally and don't say "PoC" or "skill." Also trigger for "build this from scratch," "design then build," or any request to validate technical feasibility before full development. Works on any language/framework — the stack is researched fresh each time, never assumed. This skill runs the whole pipeline autonomously and without pausing to ask the user clarifying questions — (0) verify git + gh CLI are present (refuses to proceed otherwise), (1) research best practices for the idea's domain/stack, (2) write a lightweight SRS (requirements spec), (2.2) pressure-test the SRS with a five-advisor council and apply its verdict, (2.5) file a tracking ticket in whichever of Jira/Monday.com/GitHub Issues is available and branch feat/<ticket>-<slug> off dev, (3) derive a full test-case matrix that covers every SRS requirement BEFORE any implementation code is written, (4) build to make the tests pass, (5) report results, open questions, and what a full build would still need, (6) push the branch and open a PR via gh CLI, titled feat followed by the ticket ID and a short description. Use this instead of jumping straight into code whenever the user's request implies "is this feasible" / "prove this works" / "make sure it's grounded in best practice" rather than "just write me code."
---

# PoC Spec-Driven Builder

Turns a loosely-described idea into a working, evidence-backed proof of concept — research → spec (SRS) → council review → test matrix → implementation → verification → PR — run end-to-end without interrupting the user for clarification. Ambiguity is resolved by making the most reasonable assumption and logging it, not by asking.

This mirrors how modern AI coding agents are meant to work: specs and tests are the source of truth the agent builds *to*, not decisions made ad hoc while writing code. A PoC only proves something if what it's proving was written down first.

Stack-agnostic by design: Step 1 always researches the conventions of whatever language/framework the target repo actually uses (Rust, TypeScript, Python, Go, Dioxus, Next.js, …) — nothing here assumes a particular stack. What's fixed is the *process* (spec → tests → build → ticket → PR), not the technology.

## Core principle: never block on questions

Default behavior for this skill is autonomous execution. When something is unspecified:
1. Pick the most conventional, lowest-risk, industry-standard choice for that domain.
2. Write it into the SRS's **Assumptions** section with a one-line rationale.
3. Keep going.

Only break this rule if the user's message contains an explicit, irreversible constraint that's actually contradictory (e.g., they named two mutually exclusive databases) — then state the conflict plainly and pick one anyway, noting it's an assumption to revisit, rather than stopping.

## Workflow

### Step 0 — Scope the idea (silent, no output yet)
Read the user's request and restate it internally as: what capability is being proven, for whom, and what's explicitly out of scope. A PoC proves ONE core technical uncertainty — not a full product. If the request bundles several unproven ideas, identify the riskiest/most load-bearing one as the PoC's focus and note the others as "not in scope for this PoC" in the SRS.

### Step 0.5 — Check prerequisites, refuse if missing
This skill ends in a real PR against a real branch, so it needs the tools for that to be true before it writes a single line of the SRS. Run `scripts/check_prereqs.sh` from the skill directory.

- If it exits non-zero: **stop immediately.** Do not research, do not write an SRS, do not touch code. Tell the user exactly which prerequisite is missing and the one command that fixes it (the script's own error message gives you this). This mirrors "never block on questions" — the only thing this skill blocks on is a missing tool, never an ambiguous requirement.
- If it passes: also check, from your own available tools, whether a Jira or Monday.com MCP integration is connected (tool names containing `Atlassian`/`Jira` or `monday_com`). Record which tracker you'll use for Step 2.5:
  1. Jira MCP, if connected.
  2. Monday.com MCP, if connected and Jira isn't.
  3. Otherwise, GitHub Issues via `gh issue create` — always available once the prereq check passes, since `gh` is already required. This means a tracker is *never* unavailable; it's just a question of which one.
  If more than one is connected, ask the user once which to use for this project and remember it — this is a standing project choice, not a per-PoC ambiguity, so it's fine to ask.

### Step 1 — Research best practices
Before designing anything, research the domain the idea lives in:
- Search for established patterns, common pitfalls, and reference architectures for this category of problem (e.g., "real-time collaboration conflict resolution," "OAuth device-code flow," "vector search reranking").
- Identify the standard/boring technology choices for this stack unless the user specified otherwise — PoCs should use mature, well-documented tools, not novel ones, because the goal is to isolate risk in the *idea*, not in unfamiliar tooling.
- Note any known failure modes or gotchas specific to this kind of system; these become edge-case test cases in Step 3.

Keep this research proportional — a few searches for a small PoC, more for something with real architectural uncertainty. Summarize findings in 3-6 bullet points; this becomes the "Background / Prior Art" section of the SRS.

### Step 2 — Write the SRS (before any code)
Produce a lightweight Software Requirements Specification as a markdown file (`SRS.md`) in the project. Keep it tight — a PoC spec is a page or two, not an enterprise document. Required sections:

```markdown
# SRS: <project name>

## 1. Purpose
One paragraph: what technical question this PoC answers, and why it's uncertain enough to need proving.

## 2. Scope
- In scope: the specific capability being demonstrated
- Out of scope: everything adjacent that this PoC deliberately does not attempt

## 3. Background / Prior Art
Bullet points from Step 1's research — patterns used, tools chosen, why.

## 4. Functional Requirements
Numbered, testable, one behavior each:
- FR-1: <system> shall <specific behavior> when <condition>
- FR-2: ...
Every requirement must be phrased so a test can pass or fail against it. Reject vague ones ("shall be user-friendly") — rewrite until measurable.

## 5. Non-Functional Requirements
Only the ones that matter for THIS PoC's core question (performance, data volume, latency, concurrency, security boundary). Skip categories that aren't relevant — don't pad.

## 6. Assumptions
Every unspecified decision made autonomously, with a one-line rationale. This is the log of everything that wasn't asked about.

## 7. Success Criteria
The concrete, binary condition(s) under which this PoC is considered to have proven (or disproven) the idea.

## 8. Council Review
Filled in by Step 2.2: agrees / clashes / blind spots / verdict / first move.
```

Fundamentals to hold to while writing this, regardless of domain:
- Every requirement is falsifiable — if you can't imagine a test failing it, rewrite it.
- Prefer fewer, sharper requirements over broad coverage — a PoC that nails the risky 20% beats one that shallowly covers 100%.
- State success criteria before any design decisions that could bias what "success" means later.

### Step 2.2 — Council the SRS
Before the spec is filed or tested, put it in front of a council: five subagents, each with one opposed lens (Contrarian, First Principles, Expansionist, Outsider, Executor), write a short critique in parallel; five more review those critiques blind (shuffled, labelled A–E); then you, as chairman, decide, **edit the SRS to match**, log each accepted or rejected change in §6, and write the verdict into §8. Personas, brief templates, model tiers and the no-subagent fallback are in [`references/council.md`](references/council.md); read it before running this step.

This never asks the user anything: the council stands in for the clarifying question. If it shows the PoC can't fail as written, rewrite §1 and §7 before Step 2.5.

### Step 2.5 — File the ticket, cut the branch
The SRS's Purpose and Scope sections (§1–2) are already a ready-made ticket description — use them directly instead of writing a separate summary.

1. Create one ticket in the tracker selected in Step 0.5 (`createJiraIssue`, `create_item`, or `gh issue create` — whichever applies), titled after the SRS's project name, body = SRS §1 Purpose + §2 Scope. Capture the ticket's identifier exactly as the tracker returns it (Jira key like `PROJ-123`, Monday item ID, or GitHub issue number like `42`) — this is `<TICKET-ID>` for every step below.
2. Run `scripts/ensure_branches.sh <TICKET-ID> <slug>`, where `<slug>` is a short kebab-case description of the feature (e.g. `ensure_branches.sh PROJ-123 csv-export`). It creates `dev` off the repo's default branch if `dev` doesn't exist yet (pushing it), then cuts and checks out `feat/<TICKET-ID>-<slug>` off `dev` — refusing to run if that branch already exists locally, so it never silently clobbers in-progress work. Do all work in Steps 3–5 on the branch it leaves you on.

If ticket creation fails (auth expired, tracker down), don't let that block the PoC itself — log it as a noted limitation in the SRS's Assumptions section, branch off `dev` using a `feat/poc-<slug>` fallback name, and continue. The PR in Step 6 just won't have a ticket number to reference.

### Step 3 — Derive the full test matrix from the SRS (still before implementation)
For **every** FR and relevant NFR, write at least one test case before writing implementation code. Produce `TEST_PLAN.md` (or actual test files if the stack/framework is already clear — prefer real executable tests over a prose plan when feasible):

```markdown
## Test Matrix

| Test ID | Requirement | Scenario | Type | Expected Result |
|---------|-------------|----------|------|------------------|
| T-1     | FR-1        | Happy path: ... | unit/integration | ... |
| T-2     | FR-1        | Edge case: ... | unit | ... |
| T-3     | FR-2        | ... | ... | ... |
```

Coverage rules:
- Every FR gets at least a happy-path test AND at least one edge/failure-path test (empty input, boundary value, invalid state, concurrent access — whichever apply).
- Pull edge cases from Step 1's "known failure modes" research, not just from imagination.
- Every NFR that's testable gets a test (e.g., a latency budget gets a timed test, not just a comment).
- Requirements with no corresponding test are a spec bug — go back and add the test, don't skip it.
- If the stack supports it, write these as actual runnable test files (pytest/jest/etc.) in a `tests/` directory so Step 4 has something to run against, not just prose to eyeball.

### Step 4 — Build to the tests
Implement the minimum code that satisfies the test matrix, in requirement order (build what T-1's requirement needs, confirm it passes, move to the next). Do not add functionality that isn't backed by an FR/NFR in the SRS — scope creep in a PoC defeats the point of isolating one risky question. If mid-build you discover the spec was wrong or incomplete, update `SRS.md` and `TEST_PLAN.md` first, then continue — the spec stays the source of truth, not an artifact you drift away from.

Run the test suite (or walk through the test matrix manually if no test framework applies to this stack) before declaring anything done.

### Step 5 — Report
Close out with:
- Pass/fail status against every requirement in the SRS (a simple table is fine).
- Whether the PoC's Success Criteria (SRS §7) were met — answer the actual technical question, don't just say "done."
- The Assumptions log (SRS §6) surfaced explicitly, since these are exactly the decisions a real build would need a human to confirm or override.
- What's deliberately NOT proven (out-of-scope items) and what a next iteration or full build would need to address.

### Step 6 — Ship it
Once Step 4's tests pass and Step 5's report is written:

1. Commit the SRS, test plan/files, and implementation on the `feat/<TICKET-ID>-<slug>` branch (if not already committed incrementally during Step 4).
2. Push the branch: `git push -u origin feat/<TICKET-ID>-<slug>`.
3. Open the PR against `dev` (not `main` — features land on `dev` first): `gh pr create --base dev --title "feat: <TICKET-ID>-<what the feature does>" --body "<link/summary of the SRS success criteria, the council verdict (SRS §8) and Step 5's report>"`. If the tracker is GitHub Issues, start the body with `Closes #<TICKET-ID>` so merging the PR auto-closes the ticket — Jira/Monday.com have no equivalent auto-link, so for those just reference the ticket ID in the body text.

The PR title is intentionally the same shape as the ticket + one-line description, so anyone scanning the PR list can trace it straight back to the ticket. If Step 2.5 fell back to `feat/poc-<slug>` (no ticket), the PR title drops the ticket segment: `feat: <what the feature does>`.

## Fundamentals checklist (apply throughout, not just at the end)

- **One core uncertainty per PoC.** If you're proving three unrelated things, you have three PoCs — say so and either scope down or run them as separate phases.
- **Boring technology by default.** Novelty is a variable to control for, not to introduce, unless the novel tool IS the thing being proven.
- **Spec before code, tests before implementation.** Never write implementation logic before the corresponding requirement and test exist on paper.
- **Assumptions are logged, not silent.** A reader of the SRS should be able to find every place Claude guessed instead of being told.
- **Small and disposable.** PoC code optimizes for answering the question fast and clearly, not for production hardening, unless an NFR explicitly says otherwise.
- **The spec survives a council before tests are built on it.** A blind-reviewed critique is cheaper than a test suite written to the wrong spec.
- **Falsifiable success.** If there's no way the PoC could have failed, it didn't prove anything.
- **No PR without a passing build.** Step 6 only runs after Step 4's tests pass — an open PR is a claim the work is real, so it must follow verification, never substitute for it.
