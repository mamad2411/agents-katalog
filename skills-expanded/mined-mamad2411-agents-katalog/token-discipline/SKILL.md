---
name: token-discipline
description: Stretch Claude Code context. Use when sessions are running long, hitting context/usage limits, working through large repos, doing multi-day work, or burning through tokens faster than expected. Apply these habits proactively on any non-trivial task.
---

# Token Discipline

You are operating with a finite context window. The user is paying for tokens — directly (API) or indirectly (plan limits and rate caps). Your job is to do the work fully **and** keep the conversation cheap. Most context is wasted on echoing file contents, re-reading the same files, holding plans as prose, and dumping unfiltered tool output. None of that is the work — it's just exhaust.

Treat context like a budget. Spend it on thinking, decisions, and the diff. Don't spend it on noise.

## The seven habits (apply by default, not just when "running low")

### 1. Read with `offset` and `limit` — never gulp whole files

The Read tool defaults to ~2000 lines. Most files don't need that. Most tasks touch 10-50 lines.

- File < 100 lines: read it whole.
- File 100-500 lines: scan structure first (`grep -n` for symbols), then read just the slice with `offset` + `limit`.
- File > 500 lines: never read whole. Locate first, then read a window.

Re-reading a file you just edited is almost always wrong. The harness already tracked the change.

### 2. Delegate research to subagents — protect main context

Anything that takes 3+ file reads to answer should be a subagent (Explore for read-only lookups, general-purpose for multi-step research). The subagent burns its own context and returns a paragraph.

Examples that should be a subagent, not direct reads:
- "Where is X defined and what calls it?"
- "Find all places we handle Y"
- "Is there an existing helper for Z?"
- Any open-ended "where / how is this done in the codebase" question.

Do not also do the same searches yourself afterward. Trust the subagent's report.

### 3. Pipe long output — never let raw bash dumps land in context

Default tail/head everything that could be long.

- Builds and tests: `... | tail -50`
- Discovery (`find`, `ls -R`, `grep -r`): `... | head -50`
- Long logs: `... | tail -200` or `grep <pattern>` first
- Skip JSON pretty-printing entire payloads; pipe through `jq '.field'` to extract.

The full output isn't useful if it scrolls past the actual signal. Filter at the source.

### 4. Use `TodoWrite` (or your equivalent task tracker) — don't hold plans as prose

A multi-step plan written in conversation text gets re-included in every subsequent turn. The same plan tracked in TodoWrite is held in a single compact structure and updated in place.

Rule: if you would write a numbered list of "I'll do A, then B, then C" in a message, write it to TodoWrite instead and reference it by status. One source of truth.

### 5. Drop checkpoint summaries every 3-4 tool rounds

Write one sentence: "Found the bug in `auth.go:142` — guard clause inverted. Fixing next." This anchors you when context compresses, and lets a future turn pick up cold without re-deriving state.

This is not narration of intent. It's a stake in the ground for what's *known* now.

### 6. Never echo file contents — go straight to analysis

If you just read a file, don't restate it back. The user can see it (or saw it via the Read tool result). Skip "Here's what's in the file:" and go to "The bug is on line 42 — `x` is shadowed."

Same rule for grep results, git log, find output. Don't recap. Act.

### 7. Use the skill system itself

Skills load their description into context but only load the body when invoked. That means a 200-line skill doc costs ~30 tokens until it fires. Same for `references/` files — load on demand. Push deep how-to into a reference file rather than the SKILL.md body.

## Antipatterns to kill on sight

- **Re-reading after Edit.** The Edit tool errors if the change failed. Re-reading is paranoia tax.
- **`cat`-ing whole config files to check one value.** Use `grep -E '^KEY=' file` — never let secrets land in context either.
- **Reading the same file in three turns.** If you keep coming back to it, read once with the right window and write down the relevant line numbers.
- **Asking permission for reversible work.** Edits, reads, tests are reversible. Just do them. Reserve confirmation for destructive or shared-state actions.
- **Multi-paragraph end-of-turn summaries.** Two sentences max. The diff speaks.
- **Reading files in series when you could batch.** Independent reads should be parallel tool calls in one message, not one-per-turn.
- **Carrying dead context.** Old plans, old tool results that are no longer relevant. If the conversation has clearly moved on, don't keep referencing the old thread.

## When the user explicitly hits a limit

If they say "running out of context," "near the limit," "things are getting slow":

1. Drop a sharp checkpoint summary (current state, decisions made, next step). Make it complete enough to resume cold.
2. Move work-in-progress detail into TodoWrite or a memory file rather than conversation text.
3. Aggressively delegate the next research/exploration step to a subagent so the result lands as a paragraph, not a transcript.
4. Suggest `/compact` (Claude Code) or starting a fresh session with the checkpoint as the kickoff message.

## The mindset

Every tool call has a cost: the call itself, the output it returns, and the context it occupies for the rest of the session. A read of 400 lines you didn't need follows you for 50 turns. A subagent's one-paragraph summary follows you for 50 turns.

Optimize for *signal density per token*. The work is the diff and the decisions. Everything else is overhead.
