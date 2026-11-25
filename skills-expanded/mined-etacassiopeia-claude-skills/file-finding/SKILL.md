---
name: file-finding
description: "File a GitHub issue for a concrete, out-of-scope defect or gap discovered during implementation or review — deduped against open issues, labeled `agent-found` + `needs-triage`, with provenance (source PR/issue, evidence, proposed fix) so it is /fix-issue-ready. A finding that proposes new surface must also record whether its should-question is settled or open, so /triage-issue can decide desirability cheaply. Held for human triage: not auto-implemented. Usage: /file-finding \"<finding>\""
user_invocable: true
argument-hint: "\"<one-line finding description>\""
allowed-tools:
  - Bash(gh issue list:*)
  - Bash(gh issue view:*)
  - Bash(gh search:*)
  - Bash(gh label list:*)
  - Bash(gh label create:*)
  - Bash(gh issue create:*)
  - Bash(gh issue comment:*)
  - Bash(git remote get-url:*)
---

## Live Context (loaded at invocation)

- **Finding (args)**: `$ARGUMENTS`
- **Repo remote**: !`git remote get-url origin 2>/dev/null`
- **Existing labels**: !`gh label list --limit 100 2>/dev/null`
- **Recent open issues**: !`gh issue list --state open --json number,title --limit 60 2>/dev/null`

---

# File Finding — record a worth-fixing discovery as an issue

**Goal:** turn a concrete defect or gap discovered *during other work* (implementing an issue,
reviewing a PR, diagnosing CI) into a well-formed, deduped, `/fix-issue`-ready GitHub issue —
**without** implementing it now. Findings are **held for human triage**, never auto-fixed in the
same run (they carry `needs-triage`, which the `ship-issues` orchestrator excludes from `--all`).

The caller provides the finding in context (via `$ARGUMENTS` and/or the invoking prompt): what's
wrong, where, the evidence, a proposed fix, and the source (the PR/issue/session that found it).

## The quality bar — file only if ALL hold

Filing noise is worse than not filing. Only file when:

1. **Concrete** — a specific defect or gap, not a vague worry. You can name the file/function and
   the wrong behaviour.
2. **Worth a fix** — a real bug, correctness/safety gap, silent failure, or missing capability with
   user impact. **Not**: style nits, speculative refactors, "might be nice", or TODOs already noted.
3. **Out of the current scope** — fixing it now would be scope-creep on the work in hand. (If it's
   in scope, just fix it; don't file.)
4. **Actionable** — you can state a proposed fix or at least a concrete first step.
5. **Wanted, not merely absent** — this bar applies only when the finding proposes a **new
   capability or surface** rather than correcting behaviour that is already wrong. There,
   *"it doesn't exist"* is not by itself a reason it should: name the recorded principle, doc or
   issue that sanctions it, and if nothing does, record the should-question as **open** instead of
   assuming the answer. A defect fix rarely trips this — the intended behaviour is already settled.

If 1–4 fail, do **not** file — report "no finding worth filing" and stop. Bar 5 is different: a
finding with an open should-question is still **filed**, with the question recorded (see Step 3);
it is not silently dropped, because deciding it is a human's call, not yours.

## Step 1 — Dedup (mandatory, before any create)

Search for an existing issue covering this finding:

- `gh search issues --repo <owner/repo> --state open "<key terms>"` and scan *Recent open issues*.
- Match on the underlying defect, not exact wording (same file+symptom = duplicate).

Outcomes:
- **Duplicate found** → do **not** create. Add a short comment on the existing issue with the new
  evidence/source *only if it adds something* (`gh issue comment <n>`), then return
  `duplicate of #<n>`. Never open a second issue for the same defect.
- **No duplicate** → proceed to Step 2.

## Step 2 — Ensure labels exist

Ensure `agent-found` and `needs-triage` labels exist (create if missing — ignore "already exists"):
`gh label create agent-found --color BFD4F2 --description "Discovered by an agent during other work" 2>/dev/null || true`
`gh label create needs-triage --color FEF2C0 --description "Awaiting human triage before implementation" 2>/dev/null || true`
Add an area label too if one obviously applies (from *Existing labels* — never invent new area labels).

## Step 3 — File the issue

`gh issue create` with:

- **Title**: a precise, imperative summary of the defect (matches how issues in this repo are
  titled — see *Recent open issues* for tone). Not "bug found in X".
- **Labels**: `agent-found`, `needs-triage` (+ area label if applicable).
- **Body** using this template:

  ```markdown
  ## Problem
  <what's wrong, where — name the file/function and the incorrect behaviour>

  ## Evidence
  <repro steps, failing input→output, log/CI excerpt, or the code path that proves it>

  ## Proposed fix
  <the fix or a concrete first step; note the compatibility/scope contract if relevant>

  ## Should this exist?
  <!-- New capability/surface only — omit this section entirely for a plain defect fix. -->
  <SETTLED — cite the principle, doc or issue that sanctions it
   | OPEN — the one-sentence question a human must answer before this is implemented>

  ## Provenance
  Found by an agent while <implementing #N / reviewing PR #M / diagnosing CI on PR #M>.
  Out of scope for that work, filed as a follow-up.
  ```

**Why the should-question is recorded here, at filing time.** A finding can be *factually* correct
in every claim and still be the wrong thing to build: `achird-labs/rift-cluster` #365/#366 were
precise, survived independent premise checks, and were refused outright because the console was
never meant to hold that power. You are the last reader who has the surrounding context — whoever
triages this later sees only the issue body, so an unexamined "X is missing" reads as self-evidently
worth closing. Recording the question is what lets `/triage-issue` return `question-design` or
`rejected-by-design` cheaply, instead of it surfacing once someone has written the code. **You are
not answering the question — you are making sure it is visible while declining is still free.**

Record and **return the new issue number/URL**. Keep the body tight and specific — it should be
implementable directly without re-investigation.

## Output

Return exactly one of:
- `filed #<n> — <title>` (new issue), or
- `duplicate of #<n>` (existing issue, optionally commented), or
- `no finding worth filing` (bar not met).

This is the return value for a calling skill — no preamble, no transcript.
