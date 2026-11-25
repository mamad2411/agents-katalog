---
name: adversarial-challenge
description: >-
  Devil's-advocate attack on AI workflow designs — threat model, assumption
  challenges, code critiques, and hypothetical redesigns with no file edits. Use
  for "attack this design", devil's advocate, or hostile challenge on
  agents/tools/summarization/tokens. Not for PR peer review (code-review) or
  self-review that applies fixes (ai-systems-review). Prefer: this skill →
  decide → ai-systems-review.
---

# adversarial-challenge

Hostile **devil’s advocate** for an AI-powered workflow. Do not assume the design
is correct. Attack it; do not praise it. Process examples are chat/context-heavy —
map each section onto the subsystem that actually changed.

## Not this skill

| This skill | `ai-systems-review` | `code-review` |
| --- | --- | --- |
| Attack design; **hypotheticals only** | Hostile pass → **real edits** | Peer PR/diff → **verdict** |

**Hard rule:** Do **not** modify project files.

## Operating rules

- Setup: `git status` and `git diff` (staged + unstaged). If the tree is clean, ask which paths to review.
- Adapt failure modes to the changed subsystem; do not force a summarization lens onto unrelated code.
- No praise. No edits. Hypothetical code is for inspection only.

## Process

### 0. Setup

- Run `git status` and `git diff` (include staged). Confirm the change set before attacking.

### 1. Ruthless threat model

- Top failure modes and weird edge cases, especially:
  - Server restarts and deploys
  - Background jobs (never run, run twice, out of order)
  - LLM failures (timeouts, partial responses, malformed JSON, rate limits)
  - Token overflows and bad token estimates
  - High concurrency on the same session/resource
  - Tool/agent races, attachment failures, aborted streams
- For each: *How likely?* *User-visible impact?* *What data/context do we lose or corrupt?*

### 2. Attack the assumptions

Question assumptions including:

- When/why background work (e.g. summarization) runs: thresholds, rapid bursts, stale/missing/partial results
- “Last N messages + summary is enough”: which workflows break; interaction with tools, long tool outputs, attachments
- Infrastructure: fire-and-forget with no queue on deploys/crashes/scale-out; DB/blob always succeeding

For each assumption: argue **why unsafe**, or define **strict conditions** where it’s acceptable and the tradeoffs chosen.

### 3. Concrete code-level critiques

- Point to **specific functions/blocks** (file + function) that are risky.
- Explain **exactly why** (hidden coupling, mixed responsibilities, swallowed errors, happy-path-only).
- Be explicit: “This line is dangerous because…” / “This function will behave badly if…”

### 4. Propose stronger alternatives (no code changes)

- For highest-impact risks, describe how you would redesign/harden (minimal queue behavior, retries, better token accounting, stricter triggers, etc.).
- For each: tradeoffs (complexity, cost, latency) and why it’s better under real load/failures.
- Do **not** modify the code.

### 5. Hypothetical code for review

- Sketch **example** changes for top issues (not final edits).
- Comment with file paths/function names (e.g. `// api/chat/[sessionId]/route.ts`) and what each change solves.
- Goal: concrete, reviewable diffs the user can accept or reject.

### 6. Final verdict

- **Risk summary:** If we ship this as-is, the biggest realistic risks are: …
- **Priority list (3–5)** of hypothetical changes to consider first.
