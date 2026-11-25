---
name: squad-code-review-mandatory
description: Require independent review under the repository policy, with a portable self-contained briefing and evidence-bound findings.
allowed-tools:
  - Task
  - Bash
  - Read
disable-model-invocation: false
---

# Code review is mandatory, not optional

Self-review catches the obvious. An independent reviewer catches the rest. The structural answer to "did I miss anything" is to spawn an agent whose only job is to find what you missed.

## When to use this skill

Invoke this skill before every commit on a claimed item. Yes, even a one-line typo fix. Yes, even a documentation tweak. Yes, even when you are sure the change is trivial. The trivial-change exception is the most common path to production bugs — and it costs ~30 seconds of agent time to disprove the trivial assumption.

## The rule

Every item, before commit:

1. Run `squad review-request <ID>` (or `/review <ID>`) — this records that review is in flight and posts to the item thread.
2. Construct the self-contained briefing below. If available, the optional
   `superpowers:requesting-code-review` integration can help prepare it.
3. Use the repository-approved independent review mechanism. For local agent
   review, spawn an independent read-only reviewer using the selected client's
   supported subagent capability; Muse, Claude and Codex are eligible. A
   `superpowers:code-reviewer` agent is one integration, not a required tool name.
   Do not substitute this for a required managed reviewer/model/Check, launch
   a duplicate review, or manufacture a verdict when a tool is unavailable.
4. Verify each finding against evidence; the optional
   `superpowers:receiving-code-review` integration does not change this obligation.
   Do not perform-agree.

## What to include in the briefing

The reviewer needs:
- The item file path — the `## Acceptance criteria` section is the contract.
- The diff to review (`git diff main...HEAD` or `git diff --staged`). Paste inline if small; give the command if large.
- File:line references for the major changes.
- Specific concerns you want them to focus on.
- Output format: prioritized findings (Critical / High / Medium / Low) with file:line and a suggested fix per finding.
- **Premise-validation latitude.** Add: "If the claimed failure seems dubious, verify it against pre-fix code in an isolated disposable checkout when the review contract permits execution. Never revert or patch the author's checkout or frozen input. Report non-reproduction or an unverified premise with evidence; a snapshot-only review stays within its supplied bundle."
- **Working-tree hygiene.** Add: "The author's checkout and review tuple are read-only. Keep permitted experiments in an isolated disposable checkout; clean up only your own test artifacts. A client that shares the working directory does not grant shared-file mutation authority."

## Why this matters

The review is a structural check on you. You wrote the code; you cannot see the bugs you wrote. The reviewer brings a fresh state of mind, no anchoring on your design choices, and the explicit instruction to find what you missed. That second pair of eyes catches: off-by-one in loop bounds, missing nil checks, race conditions in concurrent code, error paths you forgot, edge cases the tests do not cover, premature abstraction, and — sometimes — that the bug you "fixed" did not exist in the first place.

The review costs less than a minute of wall-clock. A production incident costs hours of debugging plus a customer-facing failure. The math is not close.

## How to handle findings

- **If correct:** a bound Agent Loop Worker first reads its installed role's
  `references/review-readiness.md` blocking-finding repair protocol: the authorized
  implementer-model transition, original/affected-invariant coverage and recurrence
  reassessment. A standalone plugin session follows its own repository/workspace
  model policy without requiring an Agent Loop installation or Dispatcher. Keep
  the reviewer independent. Fix, rerun relevant gates and the required complete-diff
  review before delivery; retain actual evidence and consumed attempts.
- **If wrong or based on a misreading:** push back with evidence. Cite the actual code, the test that covers it, or the documentation. Do not silently rewrite to placate.
- **If real but out of scope:** file a new BUG/DEBT item, link via `relates-to`, address only the in-scope portion in this commit.
- **If the reviewer found the bug does not reproduce:** reclassify the item per `squad-premise-validation` and the squad-loop close-out.

## Anti-patterns to avoid

- "It is just a one-line fix, no review needed." That assumption ships the most bugs.
- Performative agreement: "good catch, fixing now" without verifying the finding is correct. Produces worse code than no review at all.
- Not pasting the diff in the briefing. Reviewers without the diff produce shallow reviews.
- Spawning the reviewer without the item file path. Without the AC, the review is unanchored.
- Treating "Low" findings as "ignore." Low findings still go in a follow-up item if you do not address them now.
