---
name: brain-mcp
description: Use when the user asks to recall what they know, decided or were working on, to plan or draft something for one of their own projects, or to "remember" or "save this" to their notes, while a brain-mcp (Obsidian second brain) MCP server is connected. Trigger phrases include "what do you know about me", "what was I working on last week", "what did we decide about X", "help me plan the next step for my project", "remember that I prefer Y". Teaches the agent when to load the owner's identity, how to answer from their notes with cited sources, and how to write memories back with their consent. Use it whenever brain_* tools are available and the request touches the user's own work, preferences, projects or notes, even if they never mention the vault.
---

# brain-mcp: work from the owner's second brain

brain-mcp serves the user's Obsidian vault (plain Markdown notes) as MCP tools. The point is that you start from what they already wrote down, their profile, preferences, projects and decisions, instead of asking them to explain themselves again. Used well, the user notices that you already know their context. Used badly, you either ignore the vault or flood the conversation with it.

The person you're talking to is the vault's owner, the name `brain_identity` returns, unless they tell you otherwise. Their "I", "my" and "remember that I..." refer to the notes in it, so their memories belong in the vault, not in a memory file of your own.

Tool names carry a client prefix: `mcp__brain__brain_context` in Claude Code, `mcp_brain_brain_context` in Hermes Agent, plain `brain_context` elsewhere. Match on the part after the prefix. The server may also be registered under another name (for example `second-brain`).

## 1. Check that the server is connected

If no `brain_*` tools are available, tell the user the brain-mcp server isn't connected and show them the setup in `references/setup.md` (one command: `npx debawho-brain-mcp init`). Don't run installs yourself: it changes their machine and their client config, so it's their call.

## 2. Load who the owner is, once

At the start of a conversation about the owner's own work, call `brain_identity` once and treat the result as standing context: who they are, how they want you to work, their projects and recent focus. Memory notes in it often carry a **How to apply** line; follow those, because they are corrections the owner has already given.

- Pass `topic` (a few words, such as `"database backups"`) when the task is narrow. You get a smaller bundle with only the memory notes that apply.
- Skip it for requests with nothing to do with the owner, such as a generic language question. Their private context doesn't belong in unrelated work, and it costs context you will want later.
- Don't call it again in the same conversation unless they ask you to refresh.

## 3. Answer from the vault, with sources

Pick the tool by what the user is after:

| The user wants | Call | Then |
| --- | --- | --- |
| An answer the notes might contain ("what did we decide about the ledger DB?") | `brain_context` with the question in plain words | Answer from the sections; cite note ids |
| To find notes ("where are my notes on OAuth?") | `brain_search`, with `project`, `type`, `topic` or `since` filters when they narrow it | `brain_read` the hits that matter |
| One note in full | `brain_read` (id, title or `[[wikilink]]`; `section` for one heading) | |
| To plan or discuss a project | `brain_project` first (omit the name to list projects) | `brain_context` for specifics |
| What's related ("what else touches OAuth?") | `brain_graph` on the note or concept | |
| What they've been doing ("what was I working on?") | `brain_recent` with `days` | `brain_context` on what stands out |
| How a recorded fact changed, or what was true on a date ("what did I use before Postgres?") | `brain_facts` with `history: true`, or `as_of` a date | |

How to read the results:

- **Cite note ids** (vault paths such as `Projects/Kestrel/Decisions/...md`) when you use something from the vault, so the owner can check it and see where it came from.
- **Respect coverage.** Replies state coverage as good, thin or none. On "none", say the vault doesn't record it; don't present general knowledge as their decision or fact. On "thin", answer with that caveat.
- **Ask in plain words with specific nouns.** Retrieval is hybrid (keywords, meaning and a reranker), so paraphrases work, but names, ids and dates sharpen it.
- **Read before you rewrite.** Before changing a note, `brain_read` it so your edit fits what is there.

## 4. Write back with consent

The vault belongs to the owner and every connected AI client reads it, so a careless write spreads everywhere. Write when the owner asks you to ("remember that...", "save this"), or when their identity bundle says to save without asking. Otherwise, offer in one line, for example: *"Worth saving to your vault: you prefer pnpm over npm. Want me to?"*

| What to keep | Call | Notes |
| --- | --- | --- |
| A durable fact about the owner: preference, correction, constraint, pointer | `brain_remember` | One standalone sentence per call; `category` is user, feedback, project or reference; add `why` and `how_to_apply` |
| A document: meeting notes, plan, decision record, research summary, session log | `brain_capture` | Goes to `Captures/` with frontmatter; give a noun-phrase `title`, a `kind` and the `project` |
| A hand-maintained note under `Notes/` or `Captures/` | `brain_write` (new, or `overwrite`), `brain_edit` (one change), `brain_move`, `brain_delete` | Everything outside those folders is generated and read-only. Deletes go to `.trash/` and can be restored |

- **Duplicates.** `brain_remember` refuses near-duplicates of current facts. That is usually right; tell the user it's already known.
- **Changes.** When a fact replaces one the identity bundle shows, pass `replaces` with the old fact's id (the stamp in its heading, e.g. `"2026-09-22 18:21"`); the old one stays in the file as history and leaves the bundle. If `brain_remember` holds a fact back because it may change a current one, decide: `replaces` if the old one is now wrong, `force: true` if both stay true. For something temporary ("I'm travelling until Friday"), pass `valid_until`.
- **No session trivia.** "We fixed a typo in line 40" isn't a memory. "Always run the migration dry-run first" is.
- **Link in sentences.** Link a related note inside the sentence that says how it relates ("The restore steps are in [[Restore the ledger database]]"), not in a list at the end. The link graph counts links written this way as the strongest and gives bare link lists little weight. When a write reply lists unlinked mentions, link the ones whose sentence states a relation with `brain_edit` (at most three); leave passing mentions alone.
- **Report what you wrote**: the note id or the stored fact, so the owner knows what changed.

## 5. Privacy

- Notes can hold personal and work material. Use what the task needs, and don't paste vault content into things other people will read (pull requests, emails, posts) without asking.
- Keep `[REDACTED:*]` markers exactly as they are, and never try to recover what they hide.
- If a tool says a note is private or out of scope, tell the user instead of working around it.

## Examples

**"What was I working on last week?"**
`brain_recent` with `days: 7`, then group the notes by project and summarise in a few lines, citing note ids. If something stands out, `brain_context` on it for detail.

**"Help me plan the next step for Harbor Ledger."**
`brain_identity` with `topic: "Harbor Ledger"` if not loaded yet, then `brain_project` on `"Harbor Ledger"`. Plan from its latest progress and decisions, and cite them. Offer to `brain_capture` the plan as a `kind: "plan"` note.

**"Remember that I review PRs in the morning, not at night."**
`brain_remember` with `category: "user"`, a `why` if they gave one, and `how_to_apply: "Suggest PR reviews for mornings."` Confirm in one line. If it's refused as a duplicate, say it's already recorded.

**"What's the capital of Peru?"**
Nothing about the owner, so no vault calls.

For every tool's arguments, see `references/tools.md`.
