---
name: read-up-on
description: Jog the agent's memory on a topic, person, or project that lives somewhere in the user's Obsidian vault (second brain). Works from any directory on the machine. Use when the user says "read up on X", "catch me up on X", "what do I know about X", "remind yourself about X", or otherwise asks for a briefing on a subject they expect to be in their vault but won't say where.
---

# Read Up On

Build a briefing on a topic by discovering and synthesizing everything the vault already knows about it. The user invokes this when they want full context loaded before continuing; they don't know (or care) which files hold the answer.

Can be invoked from ANY project on the machine.

## Configuration

Resolve the vault location first, then use `$VAULT` everywhere below:

```bash
if [ -d "$HOME/dev/personal/vault" ]; then
    VAULT="$HOME/dev/personal/vault"          # local machine (any cwd)
else
    VAULT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)" # cloud: repo is the vault
fi
```

The fallback matters in Claude Code cloud/web sessions, where the vault is cloned to a sandbox path and `$HOME/dev/personal/vault` does not exist. On a local machine the first branch always wins, so behaviour there is unchanged.

All searches below run against `$VAULT`, regardless of the current working directory.

The vault's auto-memory lives at `$HOME/.claude/projects/*-dev-personal-vault/memory/MEMORY.md` (glob it; the project dir name encodes the username, which differs between machines). **This path does not exist in cloud sessions.** If the glob matches nothing, skip the auto-memory step and rely on the notes and git history instead. Do not treat its absence as an error.

> [!important] Auto-memory is a pointer layer, never a fact source
> Since 01.08.2026 the split is: **memory holds what is true about the agent and the tooling, the vault holds what is true about Magnus's life.** Memory files whose frontmatter says `type: pointer` contain no facts at all, only the path of the vault note that owns the topic.
>
> Use memory to find *which note to open*, then get every fact from the note. Never quote a project, person, date or number out of memory. That layer went stale silently for five days and claimed a compensation figure 500 000 NOK above the real one, while the vault had it right the whole time.

## When to use

Trigger phrases: "read up on ...", "catch me up on ...", "what do I have on ...", "refresh on ...", "load context on ...".

Topics can be:
- A **project** (e.g. "REMA 1000 tech lead role")
- A **person** (e.g. "Øistein", "Daniel Pedersen")
- A **concept or domain** (e.g. "agentic commerce", "padel")
- A **company/product** (e.g. "Capra", "Shopify")

If the request is ambiguous (multiple candidate topics), ask one quick clarifying question before searching.

## Workflow

Run steps 1-3 in parallel. Then read, then synthesize.

### 1. Discover candidates (parallel)

Cast a wide net. Norwegian + English variants matter; many vault notes are in Norwegian.

- **Filename matches**: `find "$VAULT" -iname "*<keyword>*" -type f` for each keyword variant
- **Full-text grep**: `grep -r -l -i "<keyword>" --include="*.md" "$VAULT"` for each variant
- **Auto-memory, for pointers only**: read `$HOME/.claude/projects/*-dev-personal-vault/memory/MEMORY.md` and any topic-related memory files next to it, to learn *which vault note owns the topic*. Take no facts from them
- **Recent activity**: `git -C "$VAULT" log --since="30 days ago" --name-only --pretty=format: -- "*.md" | grep -i <keyword>` to surface recent edits
- **Email threads in Codex, when load-bearing**: use the [@Gmail](plugin://gmail@openai-curated-remote) plugin, when available, to search for and read the relevant full thread. Use it when the request refers to an email or thread, or when the vault indicates that newer details may exist in email. Keep this read-only unless the user separately asks for an email action. If Gmail is unavailable, say so and continue from the vault and other read-only sources.

### 2. Rank candidates

Score each match. Read the top 5-10.

| Signal | Weight |
|---|---|
| Filename matches the topic | +++ |
| Lives in `Projects/` or `Meetings/` | ++ |
| Lives in `Personal/People/` (for person topics) | +++ |
| Named as canonical by auto-memory | ++ (as a pointer to the note, not as a fact) |
| Edited in the last 14 days | ++ |
| Lives in `Learning/` or `Notes/` | + |
| Single passing mention | - (skip) |

Skip files where the keyword appears only once in passing (e.g. a tangential `[[link]]` in an unrelated note).

### 3. Read top notes (parallel)

Use the Read tool on the top-ranked files in a single batch. Note frontmatter `type`, `related:`, and any `[[wikilinks]]` in the body.

### 4. Expand one level (selective)

From the notes you just read, collect `[[wikilink targets]]` that look load-bearing (people mentioned, sister projects, key concepts). Also run a quick backlinks check: `grep -r -l "\[\[<TopNoteName>" --include="*.md" "$VAULT"` to find what links *to* the cluster. Read 2-5 of these. **Stop here** unless the user asks to go deeper.

### 5. Synthesize the briefing

Output in this structure (skip empty sections):

```
## <Topic>

**Summary**: 2-3 sentences on what this is and the user's relationship to it.

**Key facts**
- Bullet of the load-bearing facts (dates, decisions, stakes)

**People**
- [[Name]]: role / relevance

**Recent activity** (last 30 days)
- DD.MM.YYYY: what changed, in which note

**Open threads / next steps**
- Anything marked TODO, "waiting on", or implied by recent notes

**Sources**
- [[Note Name]] (Projects/): one-line why this matters
- [[Note Name]] (Meetings/): ...
```

Cite every claim with a `[[wikilink]]` to its source note. Don't invent facts the notes don't support.

## Heuristics

- **Norwegian + English**: search both. "Tech lead" and "team lead" and "teamleder" can all hit.
- **People topics**: always check `Personal/People/` first, then meetings they attended.
- **Project topics**: always check `Projects/` first, then linked meetings and learnings.
- **Don't read >12 files** on the first pass. If you need more, surface a "want me to go deeper?" prompt.
- **Respect language**: if source notes are in Norwegian, the briefing can mix Norwegian quotes with English framing; match what the user used in their request.

## Example

User: "read up on everything REMA 1000 and the tech lead role"

1. Parallel: `find "$VAULT" -iname "*rema*"`, `grep -ril rema "$VAULT"`, `grep -ril "tech lead\|team lead\|teamleder" "$VAULT"`, read `MEMORY.md`, `git -C "$VAULT" log --since="30 days ago" | grep -i rema`.
2. Rank: `Projects/REMA 1000 App - Team Lead Opportunity.md` (filename match + project folder) ranks top. Next: meetings with Øistein/Henning, then `Personal/People/Øistein Burøy Olsen.md`, then prep docs in `Projects/`.
3. Read top 8 in one batch.
4. Follow `[[Øistein Burøy Olsen]]`, `[[Anders Rodem]]`, `[[Henning Hønsvall Meierhaugen]]` wikilinks. Backlinks grep on the main project note.
5. Output a structured briefing with sources.
