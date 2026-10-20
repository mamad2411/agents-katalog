---
name: brainstorm
description: "Explores a product or web-game idea before specification — audience, problem, competitors, constraints, differentiation, MVP candidates; for games also MDA and core loop. Produces a concept brief. Use when the idea is vague."
argument-hint: "[topic or idea]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Bash, WebSearch, AskUserQuestion
---

# Brainstorm

Reply in the project conversation language (CLAUDE.md → Language); code, identifiers, paths and commit messages stay in English.

Reference: `stack-reference/index.md` (what the studio builds and with which versions); the brief feeds the
`product-spec.md` / `game-concept.md` templates that follow. This skill delegates nothing: the conversation, the framing and the brief are the director's own work, so `Task` is not among its tools. In the commands below, `<hooks>` is `.claude/hooks/` in copy mode and `${CLAUDE_PLUGIN_ROOT}/hooks/` in plugin mode.

## Phase 1: Conversation
Clarify via `AskUserQuestion`, one question at a time; with no argument, the first question is the idea itself.
1. For whom.
2. Which pain or desire.
3. What already exists on the market: allow `WebSearch` for 3–5 comparable products. When `WebSearch` is unavailable, say so in one line, ask the user for the comparables they know, and carry them into the brief marked `unverified (named by the user)` — never a comparable invented from memory.
4. Constraints: time, budget, stack, platforms.
5. For games: genre, session, the player's "verb" (the most frequent action).

## Phase 2: Framing
Generate 3 positioning variants (narrow/medium/wide scope) with cost and risk; for games — 3 core-loop variants (MDA: mechanics → dynamics → aesthetics).
Propose success metrics and "what must be true" for the idea to work (hypotheses to validate).

## Phase 3: Concept brief
1. Draft `docs/specs/concept-brief.md` **from `.claude/docs/templates/concept-brief.md`**: the eight sections in the template's order (essence, personas, pain, differentiation, MVP candidate, hypotheses with a validation table, risks, next step). `/product-spec` Phase 1 reads this file as its input, so a brief that invents its own shape costs the next skill the facts it came for.
2. A section with nothing behind it is written as `n/a — reason`, never dropped.
3. Show the draft in the chat, then "May I write `docs/specs/concept-brief.md`?" — one `AskUserQuestion`: write (Recommended) · show the draft/diff first · not now. After the "write" answer: `touch .claude/.write-consent` (rule 7 — the consent-guard hook checks the marker).

## Phase 4: Commit (documents lane)
Right after the write, one commit gate (rule 7 (4), `.claude/docs/git-workflow.md` § Documents): one `AskUserQuestion` offering `docs: concept brief`, staging exactly the written files — `docs/specs/concept-brief.md`. Record the gate before asking — `<hooks>session-state.sh set Gate "/brainstorm Phase 4: commit?"` — and clear it after the answer (`<hooks>session-state.sh set Gate "—"`).
- On the default branch when no story work is in progress.
- When HEAD is a story branch, name it and offer: switch to the default branch and commit there (Recommended — a pipeline-wide document) · commit here (the document belongs to this story) · leave uncommitted.
- Code, configs, workflows and scripts never ride the `docs:` commit.

Nothing is committed without the answer.

Verdict: `COMPLETE`. Next step — one `AskUserQuestion`: `/setup-stack` (Recommended) · `/product-spec` or `/game-concept` directly · revise the brief.
