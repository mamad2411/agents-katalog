---
name: garen-debate
description: Multi-round structured debate orchestration for evaluating competing solutions. Use when the user is unsure which approach is best, asks 該用 A 還是 B, wants to compare approaches, says "not sure on architecture", or invokes /garen-debate explicitly. Host interviews user about scenario, assigns N defender agents (3-6) each championing one approach, runs dynamic rounds of Defense + Counter-attack + Strengthening until consensus or no new points surface, then synthesizes a verdict with full tradeoff table and actionable next steps. Make sure to use this skill ANY TIME the user has to pick between multiple non-trivial technical approaches — including "should I use X or Y", "evaluate options", "decision between", "哪個方案比較好", "compare approaches", "not sure on architecture".
---

# Garen Debate

Orchestrate a multi-round structured debate among defender agents to evaluate competing solutions and deliver a decisive verdict.

## Quick Rule

- Use when user faces a non-trivial technical choice between 2+ approaches and needs structured evaluation
- Auto-trigger on: 該用 A 還是 B / 哪個方案 / "should I use X or Y" / "compare approaches" / "not sure on architecture" / "evaluate options" / "decision between"
- Skip for: purely factual questions, single-option implementation tasks, or trivial preference questions

---

## Workflow Overview

| Phase | What happens |
|-------|-------------|
| 1. Interview | Host extracts scenario, constraints, success criteria, candidates (see `references/interview-questions.md`) |
| 2. Setup + Cost guard | Create workspace dir, run cost estimate, confirm with user |
| 3. Round 1 — Opening | Parallel defenders write independent opening proposals |
| 4. Round 2-N — Debate | Parallel defenders read all proposals, append Defense + Counter-attack + Strengthening per round; stop on consensus or 7-round cap |
| 5. Judge verdict | Single judge agent synthesizes `verdict.md` with tradeoff table + next steps |

---

## Phase 1: Interview

Goal: gather enough context to define debate candidates and constraints.

Read `references/interview-questions.md` for the full question script.

Key extractions:
1. Scenario context — what decision is being made?
2. Constraints — budget, team skills, scale, deadline, existing tooling, compliance
3. Success criteria — what does "good" look like? what's the deal-breaker?
4. Candidate approaches — user provides 0-N; brainstorm to fill gap to 3-6 total
5. Out of scope — what's explicitly off the table?

Batch up to 4 questions per message. Extract from user's initial message first; only ask what's missing.

When user provides fewer than 4 candidates (i.e., 0-3), brainstorm and offer:
> "Beyond what you mentioned, I'd add: {A, B, C}. Reject any you don't want. Add others I missed."

User-provided candidates are usually the obvious choices. Brainstorming 1-2 additional candidates from the 4-axis framework consistently improves debate quality even when user already provided 3.

Confirm all candidates with user before proceeding to Phase 2.

---

## Phase 2: Setup + Cost Guard

**Workspace path:**
```
{CLAUDE_HOME}/debates/{YYYYMMDD-HHMMSS}-{topic-slug}/
```

Where CLAUDE_HOME resolves per platform:
- Windows: `C:\Users\<user>\.claude` (use `C:/Users/<user>/.claude` with forward slashes in subagent prompts)
- macOS/Linux: `$HOME/.claude` (or `~/.claude` when running interactively)

When passing paths to subagents, always use forward slashes (`C:/Users/garet/.claude/debates/...`) — backslash escaping breaks in nested prompt contexts.

Create this directory. All proposal files and verdict go here.

**Slugification rules:**
- Lowercase
- Replace spaces and special chars with hyphens
- Strip leading articles (a, an, the) and common stopwords (for, to, and)
- Max 40 chars (truncate at word boundary)
- Example: "real-time notification system for a Next.js SaaS app" → "real-time-notification-system-nextjs-saas"

If `{workspace_path}` already exists (rare race condition or same-second invocation), append `-2`, `-3`, etc. to the slug until path is unique.

**Cost estimate:**
```bash
bash S:\git\15-skills\garen-agent-skills\skills\garen-debate\scripts\estimate-cost.sh <n_defenders> <expected_rounds>
```

**Show user before proceeding:**
> 預計 spawn {N} agents × ~{R} rounds = {total_calls} calls, ~${cost_low}-{cost_high} 美元，確認繼續？

Wait for explicit confirmation. If user declines, offer to reduce defenders or rounds.

---

## Phase 3: Round 1 — Opening Proposals

Spawn one defender subagent per candidate — run ALL in PARALLEL.

For each defender, use the Round 1 template from `agents/defender-prompt.md`, filling in:
- `{LETTER}` — a, b, c, ...
- `{PROPOSAL_NAME}` — the approach name
- `{WORKSPACE_PATH}` — full path to debate workspace
- `{TOPIC}` — 1-sentence topic description
- `{CONTEXT_SUMMARY}` — constraints + success criteria from Phase 1

Each defender writes `proposal-{letter}.md` to the workspace. Defenders do NOT read other proposals this round.

Round 1 output format is defined in `references/round-protocol.md` (Round 1 section).

---

## Phase 4: Round 2-N — Debate Rounds

### Snapshot isolation requirement

Round N defenders MUST be spawned only after ALL Round N-1 writes are confirmed complete. Because subagents are spawned in a single Task batch and the orchestrator awaits all results before proceeding, this is satisfied automatically — as long as you do NOT mix Round N-1 and Round N spawns in the same batch.

**Anti-pattern:** spawning Defender A Round 2 + Defender B Round 2 + Defender C Round 1 in one batch. Don't.
**Pattern:** complete Round N for all defenders, await all, then dispatch Round N+1.

Run rounds sequentially (one round at a time). Within each round, spawn all defenders in PARALLEL.

**Per round:**
1. Each defender reads ALL `proposal-*.md` files (snapshot at round start — do not re-read mid-round)
2. Each defender APPENDS a `## Round {N} Update` section to their own proposal file
3. Follow strict format from `references/round-protocol.md` (Round 2-N section)

**Dynamic stop condition** — stop after a round if:
- ≥2 defenders ended their update with `<NO_NEW_POINTS>` or `<CONCEDE>`
- OR round number reached 7 (hard cap)

After each round, scan proposal files for stop signals before spawning the next round:
```bash
# Count files where signal appears within the last 3 lines (tolerates up to 2 trailing blank lines)
for f in {WORKSPACE_PATH}/proposal-*.md; do
  tail -3 "$f" | grep -qE "^(<NO_NEW_POINTS>|<CONCEDE>)$" && echo "$f"
done | wc -l
```
If the count is ≥2, stop debate and move to Phase 5.

**Never overwrite previous rounds.** Each round is appended.

---

## Phase 5: Judge Verdict

Spawn a single Sonnet judge agent using `agents/judge-prompt.md`, filling in:
- `{TOPIC}` — debate topic
- `{WORKSPACE_PATH}` — full path to debate workspace
- `{CONTEXT_SUMMARY}` — constraints + success criteria from Phase 1
- `{TOTAL_ROUNDS}` — actual final round number (e.g., `3` if debate ran 3 rounds)

Judge reads all `proposal-*.md` files and writes `{WORKSPACE_PATH}/verdict.md`.

Verdict structure is defined in `references/verdict-template.md`. Judge must follow it exactly.

---

## Reporting Back to User

After verdict is written:
1. Show the full path to `verdict.md`
2. Read `verdict.md` and synthesize a 1-paragraph summary (2-4 sentences) covering: (1) which proposal won and the single most decisive reason, (2) one specific idea worth borrowing from a losing proposal. Do NOT copy verdict sections verbatim — synthesize.
3. Remind user: "Full debate logs are in `{WORKSPACE_PATH}/` — each proposal file shows round-by-round evolution."

---

## Trigger Contexts (for skill-loader)

Explicit: `/garen-debate`

Auto-trigger phrases:
- 該用 A 還是 B / 哪個方案比較好 / 哪個架構好
- "should I use X or Y"
- "compare approaches" / "evaluate options"
- "not sure on architecture" / "not sure which"
- "decision between X and Y"
- "pros and cons of X vs Y"
- "which approach is better"
- "I can't decide between"
- "help me choose"
- "tradeoffs between"
