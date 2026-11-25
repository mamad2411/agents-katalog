---
name: review
description: "[OMCP] Severity-rated code review pass for pending changes or a specified diff."
orchestrates-agents: "code-reviewer, verifier"
---

# [OMCP] Review

Use this plugin skill to run a structured review on pending changes. Authoring
and review stay in separate passes — if the current Copilot CLI session wrote
the code, hand the review to a separate session.

## Agent orchestration

This skill routes review work through `code-reviewer` for findings and
`verifier` for evidence checks when completion claims need independent proof.

## Run

1. Collect the diff:

   ```bash
   git diff --stat
   git diff
   ```

2. Read the touched files in full to catch issues outside the diff window.
3. Severity-rate every finding:
   - **CRITICAL** — broken behavior, security regression, data loss risk.
   - **HIGH** — incorrect logic, missing tests for high-risk paths,
     undocumented breaking change.
   - **MEDIUM** — missing edge case, weak validation, fragile assumption.
   - **LOW** — style, naming, polish.
4. Cite `file:line` for every finding and state the smallest fix.
5. Return a verdict: APPROVED, REVISE (list of MEDIUM+ items), or REJECT
   (CRITICAL present).

## Rubric

- correctness, including edge cases;
- tests for new behavior and regression coverage;
- security basics (defer deep scans to `security-review`);
- readability — naming, dead code, leftover debug;
- boundaries — does the change respect documented module ownership.

## Goal

- fewer high-signal findings over a long low-signal list;
- never self-approve in the same pass that authored the code;
- escalate to `security-review` when the change touches auth, secrets, or
  untrusted input.
