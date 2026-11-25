---
name: fresh-review
description: Review an artifact with an independent agent that has no access to the author's reasoning, then classify its findings.
arguments:
  - name: target
    description: The file, diff, document or plan to review. If omitted, ask the user.
    required: false
---

# Skill: Fresh-Context Review

Get an independent review of an artifact from an agent that has not seen the conversation that produced it. The goal is to catch defects the author cannot see.

Use it on: a diff before merge, a plan before approval, a test fixture before it becomes a baseline, a document before it is relied on.

---

## 1. Define the review

1. Identify the target (path, diff range, or document).
2. Write the acceptance criteria the artifact must meet. Take them from `docs/ROADMAP.md` if the project has one; otherwise ask the user.
3. Decide what the reviewer should check and what it should ignore.

---

## 2. Build the brief

The reviewer receives ONLY:

- the target artifact;
- the acceptance criteria;
- the project rules from `CLAUDE.md` that apply;
- the output format below.

The reviewer does NOT receive the author's reasoning, the conversation, or a summary of what the author thinks is right. This avoids anchoring.

---

## 3. Run it in a fresh context

Run the review in a separate agent with no shared context: a subagent, or a new session. The reviewer must not modify any file.

Ask the reviewer to return findings in this format, or "No findings":

- **Finding:** what is wrong
- **Location:** file and line, or section
- **Evidence:** what in the artifact shows it
- **Severity:** high, medium or low
- **Suggested fix:** one sentence

---

## 4. Classify the findings

For each finding, check it against the artifact yourself and label it:

- **Real** — confirmed.
- **False positive** — the artifact is correct.
- **Unclear** — needs the user's judgment.

Fix the real findings with the smallest change. Do not add tests, features or refactoring that no finding asks for. Show the user the unclear ones and count them separately; never fold them into "real".

"No findings" is a valid result. Do not ask the reviewer to try again just to get findings.

---

## 5. Record

Report these counts:

- number of findings;
- number real;
- number false positives;
- number unclear;
- the artifact that was reviewed.

If the project has the `log-event` skill, append them as a `review_result` event with it. Otherwise, show them to the user at the end of the review.

These counts are the evidence for whether fresh reviews are worth their cost. The `audit` skill, when present, reads them.
