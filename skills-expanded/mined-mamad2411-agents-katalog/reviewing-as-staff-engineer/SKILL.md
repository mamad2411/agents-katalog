---
name: reviewing-as-staff-engineer
description: Review a diff or PR from a fresh-context perspective, challenging implementation shortcuts, hidden assumptions, missing tests, security risks, design regressions, and maintainability decay. Output is a severity-tagged review with explicit blockers, considerations, and nits. Use after any significant implementation, ideally invoked from a fresh session by a Claude that did not write the code being reviewed. Skip for trivial diffs (typo fixes, single-line changes, dependency bumps) and for diffs the same session just produced.
---

# Reviewing as Staff Engineer

The implementer's session is the worst place to review the implementer's work. By the time the code is written, the implementer (human or AI) has rationalized every shortcut, internalized every assumption, and stopped seeing the gaps. Review needs fresh eyes.

This skill is the external check. It runs in a session that did not write the code, has no memory of the trade-offs that were debated, and treats the diff as a stranger's work. The bias to fight is sycophancy: AI's natural mode is to congratulate the implementation. A staff engineer's review is not congratulation. It asks "what would break this?" before asking "does it work?"

A different skill — `defining-done` — is the implementer's self-check before declaring complete. Use that one before opening the PR; use this one *on* the PR.

## Process

1. **Refuse if context is contaminated.** If the current session wrote any of the code being reviewed, stop. Tell the user: "I wrote some of this — my judgment is biased. Start a fresh session and have that Claude review." Then stop. This is the most important rule of the skill.
2. **Read whatever artifacts exist to ground the review.** The diff itself is mandatory; the rest are informative if present:
   - `SPEC.md` — the contract the implementation must satisfy. If absent, derive an explicit acceptance list from the original request (PR description, commit messages, linked issue, or what the user tells you the diff is supposed to do) and review against that. If even that's unclear, say so in the review and ask the user before proceeding.
   - `PLAN.md` — the module-level plan, including scope. If absent, infer expected scope from the description of the change.
   - `CONTEXT.md` — landmines, conventions, hard rules. If absent, review against conventions visible in the surrounding code.
   - `UBIQUITOUS_LANGUAGE.md` — canonical vocabulary. If absent, check naming consistency against terminology already used in the affected modules.
3. **Read the diff once for shape.** What's the change at a high level? Which modules changed? Does the scope match `PLAN.md` (or, if no plan, the stated intent of the change)?
4. **Read the diff a second time for risk.** Walk the review lenses below. For each, note specific concerns with file:line references.
5. **Run the code mentally and operationally.** What happens under load? Under concurrent access? Under partial failure? At scale? At zero?
6. **Check that the acceptance criteria are actually verified by the diff.** Walk the SPEC's criteria if one exists; otherwise walk the list you derived in step 2. Produce an explicit two-column mapping — left column: the criterion verbatim; right column: the test name and file:line that proves it, or the observable behavior in the diff that demonstrates it. If the right column is empty for any row, that row is a Blocker (or "What's missing"). Don't paraphrase the criteria — copy them so a missing match is impossible to miss.
7. **Check the diff hygiene** — debug code, TODOs, type bypasses, scope creep — same list as `defining-done`. The implementer should have caught these; the reviewer catches what slipped through.
8. **Tag every comment by severity** (Blocker / Consideration / Nit) so the implementer can triage.
9. **Output the review** in the format below. Be direct. Be specific. Cite file:line.
10. **End with the disposition:** Approve, Request Changes, or Block.

## Rules

- **Fresh context only.** If you wrote the code, you cannot review it. Refuse.
- **Anchor in something explicit, not in your taste.** A review against `SPEC.md` and `PLAN.md` is grounded; a review against your own taste is noise. If those don't exist, anchor in the original request (PR description, linked issue, or what the user tells you the diff is supposed to do) and state in the review what you anchored against. Don't invent acceptance criteria silently.
- **Be specific.** "This looks fragile" is not a review comment. "Line 42: `parseInt(userInput)` will return `NaN` for empty string and is then compared with `>=`, which is always false — empty input silently routes to the default branch. Add an explicit empty-input check or use `Number(userInput)` and validate with `isFinite`" is a review comment.
- **Tag severity.** Every comment is **Blocker**, **Consideration**, or **Nit**. Without tags, every comment looks equal weight.
- **Refuse sycophancy.** Don't open the review with "great work, just a few small things." Open with the disposition. Praise that has no effect on the merge decision is noise.
- **Don't hide blockers.** If something must be fixed before merge, say "Blocker" plainly and explain the consequence. Don't soften with hedges.
- **Look for what the diff doesn't include.** A review of what's there misses the change that should have been made and wasn't. Check the acceptance criteria (from the SPEC if present, otherwise from the derived list) for unimplemented items, and the test directory for missing coverage.
- **Distinguish "wrong" from "different from how I'd do it."** Style preferences are nits, not blockers. A pattern that violates a documented convention (in `CONTEXT.md` if present, or otherwise visible in the surrounding code) is a Consideration. A bug, a security gap, or a design regression is a Blocker.

## The review lenses

Walk these in order. For each, look for specific concerns and tag severity.

### 1. Correctness against the stated intent

Does the diff actually do what was asked? Walk each acceptance criterion — from the SPEC if one exists, otherwise from the list you derived from the request — and point at the code or test that satisfies it. Look for off-by-one errors, null/undefined paths, type-coercion surprises, and gaps between what the code *appears* to do and what it actually does.

### 2. Failure modes

What happens with empty input, oversized input, malformed input? Under network or dependency failure? Under concurrent access (races on shared state)? On partial completion and retry (idempotency)? At the boundaries — zero, one, max?

### 3. Security

Injection vectors (SQL, command, template). Authorization gaps — could user A access user B's data? Secrets in logs or error messages. Untrusted input crossing trust boundaries without validation. Untrusted data being deserialized.

### 4. Design regression

Shallow modules introduced where deep ones existed (Ousterhout)? Information previously hidden now exposed? Pass-through methods adding interface cost without functionality? Duplicated patterns where an existing abstraction would serve? Naming consistent with the project's domain vocabulary — `UBIQUITOUS_LANGUAGE.md` if it exists, otherwise the terminology already established in the surrounding code?

### 5. Operability

Can this be rolled back without data loss? Are metrics, logs, or traces sufficient to debug failure? Does it require coordinated deploy? Will it break on partial deploy where old and new code run simultaneously? Where appropriate, are feature flags or kill switches in place?

### 6. Tests

Tests verify behavior through public interfaces, not implementation details. Failure modes from §2 are covered. Mocks are at trust boundaries (HTTP, time, randomness), not internal collaborators. No snapshot tests covering up bugs by passing for the wrong reason. Coverage of new code is adequate — not just the minimum to claim TDD.

### 7. Diff hygiene

Debug code, commented-out blocks, new TODOs, type system bypasses (`any`, `# type: ignore`, `unwrap()`), magic literals, scope creep beyond `PLAN.md` (or, if no plan exists, beyond what the stated intent of the change required), surprise dependencies.

### 8. Maintainability

Understandable in six months without the context the implementer had? Comments explain *why*, not restate *what*? Did this make a god file bigger or deepen a module?

## Output format

```
# Review: <PR title or one-line description of diff>

**Reviewer context:** Fresh session. Read the diff and whichever of `SPEC.md`, `PLAN.md`, `CONTEXT.md`, `UBIQUITOUS_LANGUAGE.md` exist (list them; if none, state what was used as the anchor — PR description, linked issue, user-stated intent). Did not write any of the code being reviewed.

**Disposition:** Block / Request Changes / Approve

## Summary

<2–3 sentences: what the diff does, the dominant concern (if any), and the disposition rationale.>

## Blockers

Things that must be fixed before merge.

- **<short title>** — `path/to/file.ts:42`. <Specific concern with consequence and recommended fix.>
- ...

## Considerations

Things worth addressing, but not blocking.

- **<short title>** — `path/to/file.ts:80`. <Concern, why it matters, recommended fix or follow-up.>
- ...

## Nits

Small style or polish items. Optional.

- **<short title>** — `path/to/file.ts:115`. <Suggestion.>
- ...

## What's missing from the diff

Things the stated intent required that the diff doesn't address. If a SPEC/PLAN exists, walk those; otherwise walk the acceptance list derived from the request.

- <Acceptance criterion X has no test or implementation>
- <Edge case "<empty input>" was expected but not handled in code>
- <Open question Q was not resolved in this diff or in a follow-up>

Omit this section if nothing is missing.

## What's strong

One or two specific things the diff does well, if any. Skip generic praise. Useful for the implementer to know what to keep doing.

- <Specific thing, e.g., "The seam introduced in `service.ts` makes the dependency injection clean and the test in `service.test.ts:42` exercises it well.">

Omit this section if there's nothing specific to call out.
```

## Anti-patterns to refuse

- **Reviewing code the same session wrote.** Refuse. Sycophancy is unavoidable when context is contaminated. Send the user to a fresh session.
- **Generic praise to soften the review.** Refuse. "Looks good overall, just a few things..." is sycophancy disguised as politeness. Open with the disposition.
- **Hedging blockers.** Refuse. If something must be fixed, say "Blocker" — not "you might want to consider possibly looking at..."
- **Reviews without file:line references.** Refuse. Vague reviews are useless. Cite specifics.
- **Reviews with no anchor.** Refuse. Reviewing against your own taste produces noise. Anchor in the SPEC if it exists, otherwise in the explicit acceptance list derived from the request — and state in the review which you used.
- **Equally-weighted comment lists.** Refuse. Without severity tags, the implementer can't triage. Every review comment must be Blocker, Consideration, or Nit.
- **Skipping the "what's missing" check.** Refuse. Whatever you anchored against has acceptance criteria; the review must verify each one is covered. Omitting this lets ghost requirements ship.

## Post-output instruction

After producing the review, state:

> **Disposition: <Block / Request Changes / Approve>.** <If blockers: implementer must address before merge. If considerations only: implementer's call whether to address now or file as follow-up. If approve: ready to merge after CI.>
