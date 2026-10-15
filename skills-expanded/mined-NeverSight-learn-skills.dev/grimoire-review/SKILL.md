---
name: grimoire-review
description: Systematic code review that prioritizes correctness and maintainability, distinguishes blocking issues from suggestions, and uses objective constructive language.
---

# Purpose

Systematic code review that prioritizes correctness and maintainability, distinguishes blocking issues from suggestions, and uses objective, constructive language.

# Scope

This skill controls how code changes are reviewed and how feedback is structured and delivered.

Outside scope: writing or modifying code, executing tests, merging changes, deployment.

# Leading words

- **finding** — a single observed issue or observation in the code
- **blocking** — must be resolved before merge
- **suggestion** — optional improvement; author decides
- **severity** — classification of a finding (blocking, suggestion, or praise)

# Workflow

## 1. Understand context

Read the changes (diff, files, or PR description).

Identify:

- what problem does this change solve?
- what is the design intent behind the approach?
- what constraints shape the solution (existing architecture, deadlines, dependencies)?

Completion: a one-sentence summary of the change's purpose. If the purpose is unclear, ask the author before continuing.

---

## 2. Review by category

Examine the code through each lens in order of priority. For each category: list findings or confirm the category is clean.

| Priority | Category            | Key question                                                                                             |
| -------- | ------------------- | -------------------------------------------------------------------------------------------------------- |
| 1        | **Correctness**     | Does the code do what it claims? Are edge cases, nulls, and errors handled? Is there potential for bugs? |
| 2        | **Architecture**    | Do the components fit the system design? Are boundaries and dependency direction respected?              |
| 3        | **Maintainability** | Will future developers understand this? Is naming clear? Is complexity justified or accidental?          |
| 4        | **Security**        | Are inputs validated? Is sensitive data protected? Are there injection, leak, or escalation risks?       |
| 5        | **Performance**     | Are there unnecessary allocations, blocking calls, N+1 queries, or algorithmic hotspots?                 |

Rules:

- Skip correctness and security only when the change is trivial (typo fix, config value).
- Skip performance only when the change has no measurable impact (UI text, documentation).
- Skip formatting entirely if the project has an auto-formatter or established style guide.

Completion: every applicable category has been examined. Findings are listed per category.

---

## 3. Classify severity

Assign severity to each finding using the classification guide.

Quick reference:

- **blocking** — incorrect behavior, security vulnerability, data loss risk, architectural violation that causes future breakage, regression from existing behavior
- **suggestion** — alternative approach worth considering, readability improvement, minor optimization, style inconsistency, naming preference

Rules:

- When uncertain between blocking and suggestion, label it blocking and ask the author to decide.
- Praise good design choices explicitly; label as **praise**.
- Drop findings that have no concrete impact. Every observation must explain why it matters.

See: [references/severity-guide.md](./references/severity-guide.md)

Completion: every finding has a severity label. No zero-impact observations remain.

---

## 4. Write review

For each finding, write:

1. **Location** — file:line or code snippet
2. **Observation** — what was found, described objectively
3. **Impact** — why it matters in concrete terms
4. **Recommendation** — what to do, actionable and specific
5. **Severity** — blocking | suggestion | praise

Language rules:

- Describe code, not author: "This function has a race condition" not "You wrote a race condition."
- Use objective framing: "This query runs per-row; batching would reduce round-trips" not "This is inefficient."
- Offer reasoning, not commands: "Consider extracting this to a helper because the same logic appears in three places" not "Extract this to a helper."
- When multiple valid approaches exist, frame as tradeoff discussion, not correction.

Completion: every finding has all five fields. Language is objective and constructive.

---

## 5. Summarize

Provide:

- Overall assessment (1–2 sentences on readiness)
- Count of blocking issues (with brief list)
- Count of suggestions
- Any themes or patterns observed across findings

Completion: summary is delivered. Review is ready for author consumption.

---

# Rules

- Never review formatting if the project has an auto-formatter or established style guide — skip to substance.
- One finding per issue. Do not bundle unrelated observations into one finding.
- Respect author design choices. When multiple approaches are valid, frame as tradeoff discussion, not correction.
- If the change's purpose is unclear from context, ask before reviewing. Review without understanding is noise.
- Severity classification details live in [references/severity-guide.md](./references/severity-guide.md). SKILL.md controls workflow only.

---

# References

- [severity-guide.md](./references/severity-guide.md) — detailed severity classification with concrete examples
- [review-patterns.md](./references/review-patterns.md) — common review scenarios and how to handle them
