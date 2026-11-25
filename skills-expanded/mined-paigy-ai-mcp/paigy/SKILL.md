---
name: paigy
description: Reach the user through Paigy. Use whenever you need to tell the user something, ask them a question, get a decision or approval, call their phone, wait for or receive their answers, start or check the Paigy listener, or create, assign, defer or complete Paigy Goals.
---
<!-- paigy-skill · source: paigy monorepo packs/skill/paigy/SKILL.md; mirrored to paigy-ai/claude plugins/paigy/skills/paigy/SKILL.md and written by https://paigy.ai/install, which replaces only a file carrying this line. Edit the source, never a copy. -->

# Paigy

The user is remote. Reach them only through Paigy's tools, never the terminal. The server's own instructions and each tool's description are the contract: read them. Every read ends in `next`, the one step to take.

This same guide is inside the MCP: the `help` tool (whole, or one `topic`) and the `/mcp__paigy__help` prompt. `/mcp__paigy__welcome` starts a session.

Hosted (no machine): skip Pairing and Listening; answers wake you.

## Pairing

- Call `configure` first. With a device credential on this machine it hatches you at once.
- Otherwise print its `user_message` to the user, then do what the result says:
  - `awaiting_approval`: call `configure` again with its `device_code` in the same turn. On `pending`, call again.
  - `awaiting_confirmation`: end your turn with the code as your whole reply; call `configure` with the `device_code` next turn. Calling it in the same turn drops the code.
- When it returns `enable_command`, print it for the user to run. Do not run it yourself.
- `configure({ logOut: true })` logs out only this agent, and only when the user asks.

## Listening

- Call `listen` once per session.
  - `listening`: done.
  - `receiving`: a listener runs but cannot wake you. Do not start a second.
  - `unpaired`: call `configure`.
  - `start`: run its `command` exactly, now.
- Claude Code: run it with the **Monitor** tool, never a background Bash command. Start it again whenever the monitor expires.
- Codex: run its `command` as a long-running background process. It queues each answer into this thread (`CODEX_THREAD_ID`).
- With no `listen` tool, run `npx -y -p @paigy/mcp@latest paigy-listen --brief` the same way.
- One listener per session. A `paigy-listen` in `ps` belongs to another session; ask `listen`, never `ps`.
- Each line it prints is work: receive, read the Goal, act.

## Receiving

- On startup and after every wake or listener line: `contact({ wait: false })`.
- Events: `question` (you owe an answer: send `answers`), `update` (something new on your Goal: an answer, a reply, a review), `instruction` (work sent to you).
- Read the Goal with `get_goals` before acting. An answer arrives as an `update` event and lands on the question's Goal. A question reading `replied` means they chose no option: settle it from their words.
- Acknowledge each event you handled: `contact({ ackEventIds })`. Reading acknowledges nothing; events repeat until acknowledged. A `question` event is answered, never acknowledged away.
- `contact({ wait: true })` waits about 45 s. On `expired`, wait again without re-sending, or stop. No while-loops: while any Call is open, keep receiving through empty windows; otherwise stop at one empty window.

## Asking

- One question per object in `questions`, at most 80 characters. Context goes in `units`: at most 12, title ≤50, body ≤200, one idea each.
- `goalId` names an existing Goal. Create it with `manage_goals` first.
- Give options when you have them: up to 6, label ≤50 naming the choice in full, `hint` ≤200 saying what it does. Never "Other" or "Option 2". `pickMode`: `one` (default), `many`, `rank`.
- `workItBlocks` only when you are truly stopped: it asks for a call.
- Read the Goal before asking. Never re-ask an open or answered question, or one whose work shipped.
- Take back a question that no longer matters: `withdrawQuestionIds`.
- An answer you give (`answers`) is at most 80 characters.

## Updates and completions

- An update (`updates`: `message` ≤80, `goalIds`) asks nothing. It reaches the user only when they asked for it, when it answers something they said, or when its Goal is done; otherwise it stays on the Goal as progress.
- Updates never complete a Goal.
- One load-bearing point per report: `message` is the point they must not miss, and a second point that would go wrong or stay unclear later if they missed it is its own update. `units` are context they may open, never something they must hear.
- `reply` is the button in the user's voice instead of "Got it", ≤50 characters ("Sounds good, I'll test later"). Required (`reply_required`) when the update is delivered on request (`userExplicitlyRequested`) or any Goal it names is already done.
- Set `userExplicitlyRequested` only to relay the user's own words: `"any"` for "send it to me", `"call"` for "call me". Never to make a message louder.
- Finish with a completion (`contact.completions`, or `manage_goals` kind `complete`): `goalId`, `message` ≤50, `reply` ≤50, optional `units`, optional next-step `options` {label, hint}. It closes and reports in one step. Say only what your evidence supports.
- Read `results`: each item applies on its own, and a failed one names why.

## Goals

- `manage_goals` `changes`, applied in order:
  - `create`: `title` (1-5 words) and `outcome` (one paragraph, ≤500). More work is child Goals: `parentGoalId`. New ids come back in `results[i].goalId`.
  - `assign`: `ownerId`, a participant as `check_activity` shows it.
  - `defer`: `until`. You are woken when it passes. This is how you follow up later.
  - `dependency`: `add`/`remove`; `goalId` waits on `dependsOnGoalId` to `start` or `complete`.
  - `edit`, `move`, `state` (open, completed, canceled).
- Any open question on a Goal, anyone's, blocks its completion (`goal_blocked`). Before completing, withdraw yours, finish or move its required children, and clear its dependencies.
- On `goal_revision_conflict`, read the Goal again and reconsider.
- Before overlapping work, read `check_activity` and the Goal's other contributors. Every Goal of your person is open to you; your first write puts you on it.
- `search` finds earlier words, Goals and answers. Nothing found is not proof of absence.

## Calls

- Call only when the user asked: `userExplicitlyRequested: "call"` on that item. A question with `workItBlocks` may ring too.
- Any contact while the user is on a call joins that call (`joinedCall` in `results`). Several questions arrive as one call.
- While any Call is open, keep receiving.
- An open Call Delivery is not proof it rang. `get_delivery` reads a Call's state, and with `transcript: true` what was said.
