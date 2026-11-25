---
name: tokenwise
description: Use for LARGE multi-part tasks (many files to read or change, several independent pieces, roughly 15+ tool calls) to route each piece to the right model (Claude Haiku, Sonnet, Opus) and reasoning effort, delegating mechanical pieces to cheaper subagents. Also use whenever an image must be generated (icons, banners, OG images, illustrations) via ChatGPT Codex, when the user mentions limits, usage, cost or saving quota, or asks which model to use. Not for small tasks.
---

# tokenwise

Goal: spend Opus only where it changes the outcome; push mechanical work to cheaper models.

## 0. Small task? Stop here.

If the whole request fits in about 10 tool calls, or has no self-contained piece that needs lots of reading, **do it inline and ignore the rest of this skill**. Don't read the reference files. Routing small work costs more than it saves.

## 1. Pick the model per piece

| Tier | Model | Typical work |
|------|-------|--------------|
| Light | `haiku` | find files/symbols, grep, list usages, read and summarize many files or long logs, count/inventory things, run a command and report |
| Standard | `sonnet` | implement from a clear spec, write tests, mechanical multi-file edits, known-cause bug fixes, docs |
| Heavy | `opus` | design decisions, unknown root cause, security/data integrity, final review of risky changes |

Unsure? Pick the cheaper tier, unless a mistake would be hard to undo.

## 2. Delegate only when it pays off

Delegate a piece when ALL hold: it's self-contained (short brief, clear "done"), it needs ~5+ tool calls or reading lots of content, and you only need a short result back. Otherwise do it inline.

Good delegation targets: "read these 30 files and give me a table", "replace X with Y in every file under src/", "write tests for module Z", "find every usage of W".
Keep inline: anything that needs the conversation's context, and the final integration/verification.

## 3. Pick the effort

Count these signals: **many interacting parts**, **ambiguity**, **a prior failed attempt**, **costly mistake**.
0 → `low`, 1 → `medium`, 2+ → `high`. `xhigh` only for Heavy work after `high` failed. Never `max` unless the user asks.
Model and effort are independent: `opus/low` (quick judgment call) and `sonnet/high` (big routine refactor) are both fine. Raise effort before raising the model.

## 4. How to call

Agent tool with explicit `model` + `effort` (this skill authorizes setting effort):
- Light → `subagent_type: "tokenwise-scout"` (read-only) or `model: "haiku"`
- Standard → `subagent_type: "tokenwise-builder"` or `model: "sonnet"`
- Heavy → `subagent_type: "tokenwise-architect"` or `model: "opus"`

Don't `fork` to save usage (forks use the parent's model). Dispatch independent pieces in parallel in one message. Each brief: files/area, what to do, done-condition, what to return (short). Verify cheap results that matter; escalate one rung if they're wrong.

## 5. Report

One line when you delegated: `Model routing: haiku/low (inventory of 30 files), sonnet/medium (tests); main: opus.`

## Read only when needed

- Images, ChatGPT Codex / Gemini workers → `references/external-workers.md`
- Suggesting a main-session model/effort change, or the session runs in ultracode/max → `references/session-modes.md`
- Unsure which model/effort fits a task type → `references/effort-guide.md` (~50 examples)
