---
name: save-on-stop
description: When an agent session ends (Claude Code stop hook, Cursor tab close, Windsurf disconnect, Cline finish, OpenClaw shutdown), capture the just-finished work into Graphory via the MCP `save_message` tool so it becomes durable, searchable memory across sessions and tools. Trigger on phrasings like "save this session", "remember this for later", "log what we just did", or automatically via the host agent's stop/shutdown hook.
---

# save-on-stop

This skill turns every meaningful agent session into durable memory inside the user's Graphory graph. The host agent (Claude Code, Cursor, Windsurf, Cline, OpenClaw, or any MCP-aware client) calls `save_message` over MCP at the end of a session - either via an explicit user prompt ("save this") or via a stop/shutdown hook the user has wired up.

It runs on your own AI at zero inference cost: composing the summary and making the tool call happen inside the agent you are already using.

The point: nothing about a session should disappear when the tab closes. The next session - in the same tool or a different one - should pick up where this one left off because Graphory has the context.

## When to trigger

Run this skill when:

- The user explicitly asks to save the session: "save this", "remember this", "log what we did", "save my work", "ingest this conversation".
- The host agent's stop/shutdown event fires (configured per-tool in the `examples/` folder).
- A long working session reaches a natural pause and the user has been working on something substantive (rule of thumb: more than ~10 substantive turns OR a clearly-scoped piece of work that completed).

Do NOT trigger for:

- Trivial single-question chats ("what time is it", "convert 5 lbs to kg").
- Sessions where nothing was decided, learned, or built.
- Sessions where the user said "don't save this" or asked for a private/throwaway conversation.

When in doubt, ask once: "Worth saving this to your graph?"

## Required tool

`save_message` (Graphory MCP). The user must already have Graphory's MCP server configured in their AI client. If it isn't configured, point them at `https://docs.graphory.io/mcp` and stop - this skill cannot run without it.

## What to save

Build a structured summary, not a raw transcript. The goal is something the user's future-self (or another agent) can pick up cold.

Compose `content` with these sections (omit any that don't apply):

```
## What we worked on
<1-3 sentence framing of the topic / project>

## Decisions
- <each decision made, one per bullet>

## Code / artifacts
- <files touched, PRs opened, commits made - paths or URLs>

## Open questions
- <anything left unresolved>

## Next steps
- <action items with an owner if known>
```

`title` should be a one-line label that would make sense in a list a week from now. Lead with the agent name so the source is obvious at a glance. Examples:
- "Cursor session: Refactored billing webhook to use Stripe events"
- "Claude Code: Debugged the checkout race condition"
- "Windsurf: Drafted Q3 OKR doc with Casey"

Avoid titles like "Chat from Tuesday" - those are useless six weeks out.

## Required call shape

```python
save_message(
  title="<agent name>: <one-line session label>",
  content="<structured summary, see template above>",
  entity="<the company / project this is about>",
  type="session_log",
  linked_entities=json.dumps([
    # Anyone you talked about by name
    {"name": "Sarah Chen", "context": "mentioned"},
    # Any project / account this session is about
    {"name": "Stripe Migration", "context": "subject"},
  ]),
)
```

The agent identity lives in the `title` prefix (e.g. "Cursor session: ..."). There is no separate `source` parameter. Each `linked_entities` item uses a `context` key - one of `participant`, `subject`, `mentioned`, `author`, `recipient`.

`entity` must always be set. If the user works with multiple companies and you can't infer it from context, ask: "Which company should I file this under?"

## After saving

Confirm to the user in one sentence:

> Saved this session to your Graphory under "<title>". It'll show up in your morning brief and in any future search.

Do NOT echo the full saved content back to the user - they were just there for it.

## Examples

See the `examples/` folder for per-tool wiring:

- `examples/claude-code-hook.json` - a Claude Code stop hook that triggers this skill automatically.
- `examples/cursor-rule.md` - a Cursor rules entry that fires the skill when a chat tab closes.
- `examples/windsurf-cline-openclaw.md` - equivalent setup for the other major MCP-aware agents.

## Safety rails

- **Never save credentials, secrets, or tokens.** If the session contained a paste of an API key or password, redact it before composing `content`. If you can't redact reliably, ask the user before saving.
- **Never save without `entity`.** A note with no entity is dead weight in the graph.
- **Don't save the same session twice.** If the user re-prompts "save this" later, write a follow-up note that references the prior save instead of duplicating.
- **Respect "don't save".** If the user said it during the session, honor that and skip the hook.
