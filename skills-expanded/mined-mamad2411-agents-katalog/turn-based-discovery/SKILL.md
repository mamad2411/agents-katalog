---
name: turn-based-discovery
description: |
  Use the AskUserQuestion tool (the same multiple-choice mechanism plan mode uses) to get clarity from the user.
  Each question is multiple-choice plus a free-format "Other" escape. Ask in small batches — up to 4 questions
  per call (the tool's max), more if needed across calls. Use when scoping work, resolving ambiguity,
  or surfacing answers a research pass already raised. Triggers: `/turn-based`, `ask me`, `clarify`,
  `discovery mode`, `interview me`.
---

# Turn-Based Discovery

## Purpose

Get clarity, not depth. Replace prose interrogation with structured multiple-choice questions that have a free-format escape.

This is **not** a deep-digging interview. It's a clarity tool — useful when:
- a request is ambiguous and you need a few decisions before acting,
- a research pass produced open questions that need quick answers,
- you'd otherwise be guessing on small, load-bearing details.

## The Rules

1. **Use the `AskUserQuestion` tool.** Don't ask in prose when you could ask via the tool. The tool auto-adds the free-format "Other" option — never add it yourself.
2. **Batch up to 4 questions per call** (the tool's hard max). If you genuinely need 5+ unknowns answered, send a second batch after the first returns — don't pad with filler.
3. **Only ask what's blocking.** If you can read it from the filesystem, infer it, or safely assume it, do that instead.
4. **Each question has 2–4 real options.** Each option should be a distinct choice the user could plausibly pick — not strawmen pointing at your preferred answer.
5. **Phrase for clarity, not for funneling.** Aim to surface what the user actually wants, not to confirm what you already assumed. Recommendations are fine — mark them `(Recommended)` and put them first — but the alternatives must be live.

## Question Shape

Each question passed to `AskUserQuestion`:

- **`question`** — clear, ends with a question mark.
- **`header`** — ≤12 chars, names the decision axis (e.g. "Scope", "Storage", "Format").
- **`options`** — 2–4 distinct choices. Each with:
  - `label` — 1–5 words.
  - `description` — one line on what picking it implies.
- **`multiSelect`** — `false` by default; `true` only when options genuinely combine.

The tool always appends "Other" for free-format input. Don't duplicate it.

## When to Use

- After a research/exploration pass that surfaced open decisions.
- Before starting work when the request leaves real ambiguity.
- Mid-task when you hit a fork that's cheap to ask about but expensive to guess wrong.

## When NOT to Use

- The answer is obvious from context, files, or prior conversation.
- The question is reversible and low-cost — just pick and proceed.
- You're already mid-implementation and asking would be performative.
- The user said "just go" / "you decide".

## Examples

### Good — batched clarifying questions

After researching options, ask 2–4 at once:

- **Storage**: "Where should results be persisted?" → SQLite / Postgres / JSON file / In-memory only
- **Trigger**: "How does the job start?" → Manual CLI / Cron / On file change / HTTP endpoint
- **Output**: "What format do you want back?" → JSON / Markdown / Plain text

The user answers all three, picks "Other" on any that don't fit, and you proceed.

### Good — single clarifier

When only one thing is unclear, ask one. Don't pad to four.

### Bad — fake options

> "Should I use Postgres?" → Yes / Yes with caching / Maybe / No

All paths lead to Postgres. Use real alternatives or don't ask.

### Bad — trivia

> "What's the name of the file you mentioned?"

If it's in the conversation or filesystem, find it. Don't ask.

## Anti-Patterns

- **Walls of prose questions** — use the tool, in batches.
- **Padding to hit a number** — 2 real questions beats 4 with filler.
- **Manually adding "Other"** — the tool does this; doing it yourself wastes a slot.
- **Asking after deciding** — if you've started, don't pretend to consult.
- **Deep funnels** — this skill is for clarity, not interrogation. If you find yourself planning question 5 based on the answer to question 1, you're in the wrong mode — use the `brainstorming` skill instead.

## Interaction with Other Modes

- **Plan mode**: use this to gather inputs that feed the plan. Don't call `ExitPlanMode` from here.
- **Brainstorming skill**: if deep, one-at-a-time exploration is needed, defer to `brainstorming` — it owns that discipline.
- **Auto mode**: still applies. When the user explicitly invokes this skill, ask anyway.

## Checklist Before Calling the Tool

- [ ] Is each question actually blocking progress?
- [ ] Are the options genuinely distinct?
- [ ] Did I keep it to ≤4 per call?
- [ ] Did I leave "Other" to the tool?

If any answer is no, revise before calling.
