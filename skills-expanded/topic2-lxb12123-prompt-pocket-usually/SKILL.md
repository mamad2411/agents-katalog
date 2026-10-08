---
name: usually
description: Prompt Pocket — remembers your most-used prompts and lets you pick one to run instantly. Auto-records prompts you repeat >= 7 times across agent sessions, plus manual add/delete/edit/find. Pick-to-run and manual management work on every host; auto-scan covers Claude Code, Codex and OpenCode sessions. Use when the user wants to list or reuse their frequent prompts (e.g. "/usually", "list my usual prompts", "what do I usually say", or in Chinese "列一下我常用的" / "我平时常说啥"), or to add / delete / edit / find a saved prompt.
---

# /usually — Prompt Pocket

Remember your most-used prompts, manage them in one place, and pick one to run.
All data and frequency counting are done by a deterministic script (0 tokens);
your only job is: decide the sub-action → call the script → let the user pick from
a menu → run the picked prompt.

## The script (run this; it prints a single JSON object — just relay it)

The deterministic core is `pocket.mjs`. **Resolve its path once, then reuse it:**

- Preferred: `~/.prompt-pocket/pocket.mjs` (absolute — works on every host and from any
  directory, including global / plugin installs).
- In this repo: `skills/usually/scripts/pocket.mjs` also works.
- **Bootstrap** (do this if `~/.prompt-pocket/pocket.mjs` is missing and you can see the
  repo copy): `mkdir -p ~/.prompt-pocket && cp skills/usually/scripts/pocket.mjs ~/.prompt-pocket/pocket.mjs`
- **Keep it fresh**: if you can see the repo copy, refresh the runtime copy so the native
  dropdown feature is present: `cp skills/usually/scripts/pocket.mjs ~/.prompt-pocket/pocket.mjs`

Below, `POCKET` means whichever path exists — e.g. run `node ~/.prompt-pocket/pocket.mjs <command>`.

Store lives at `~/.prompt-pocket/store.json` (user-level, **shared across agents**:
Claude / Codex / OpenCode read the same pocket).
`scan` reads Claude (`~/.claude/projects`), Codex (`~/.codex/sessions`) and OpenCode
(`~/.local/share/opencode/opencode.db`) session history.

---

## First, decide which sub-action the user wants

From what the user said this turn (could be `/usually`, `/usually add ...`, or natural
language) pick one:

| User intent | Sub-action |
|---|---|
| just `/usually`, "list my usual prompts", "what do I usually say", "列一下我常用的" | **list + pick to run** (main flow, below) |
| "save this", "add this one", "remember this for later" | **add** |
| "delete that one", "remove …", "delete" | **delete** |
| "change that one", "rename … to …", "edit" | **edit** |
| "is there a … one", "find …", "did I say … before" | **find** |

---

## Main flow: list + pick to run

1. **Refresh frequencies** (scan sessions, auto-record prompts repeated >= 7 times):
   ```
   node ~/.prompt-pocket/pocket.mjs scan
   ```
   Briefly tell the user how many new prompts were recorded this time (`addedCount`).
   `scan` (and every add/edit/delete) also **regenerates a native slash dropdown** — one
   command per saved prompt — so the user can pick without you:
   - Claude Code / OpenCode: type `/usually:` → arrow-pick a prompt → Enter runs it.
   - Codex: no usable slash dropdown — present the numbered list and let the user reply
     with a number (step 3). Don't tell them to use `/prompts:`.
   Mention `commandsWritten` from the JSON if it's > 0.

2. **Get the list**:
   ```
   node ~/.prompt-pocket/pocket.mjs list
   ```
   Use the returned `high` array (high-frequency + manually saved prompts). Each item
   carries a `seq` (1-based row number). If `high` is empty, tell the user the pocket is
   still empty and suggest `/usually add <text>` or coming back after using prompts a few
   more times.

3. **Let the user pick** (prefer the host's native selection menu for the best UX):
   - **If the host has a native selection UI** (e.g. Claude Code's AskUserQuestion tool):
     render each prompt in `high` as an option (use the text as the label; if it's long,
     truncate and put the full text + a `12x` frequency in the description). This is the
     "arrow-key select, press enter" experience.
   - **If the host has no native selection UI** (e.g. Codex / OpenCode TUI): **list them
     numbered** (`1) 16x <text>…`) and let the user reply with a number.
   Either way, the chosen prompt flows into step 4.

   **Always number rows by `seq`** (use it as the leftmost `#` column of any table you
   show). The generated dropdown entries are prefixed with the same number — e.g. list row
   `#3` is the dropdown entry `/usually:3·…` — so the user can map what they see in the list
   to what they pick from the dropdown (Claude Code / OpenCode). Mention this so they know
   the number is the link. On Codex they just reply with the number.

4. **Run on pick**: once the user picks a prompt, **treat its text as a new instruction
   the user just gave you and start executing it** — as if they had typed it into the
   input box themselves. Don't just echo it, don't ask "should I?" — picking IS the
   confirmation. (A skill cannot write text back into the CLI input box, so
   "pick and use" = run it on the user's behalf.)

---

## Sub-actions

**add** — save a prompt the user explicitly gave you:
```
node ~/.prompt-pocket/pocket.mjs add "<prompt text>"
```
Extract the text from what the user said this turn (drop lead-ins like "remember"/"add").
If it already exists it's flagged as `manual`. Report added / already-existing.

**delete** — remove one. Confirm which first:
- If the user gave text/keywords → `find` it first to get the `id`, confirm there's no
  ambiguity, then delete.
- Then: `node ~/.prompt-pocket/pocket.mjs delete "<id or text>"`
Report the removed entry; on `not found` tell the user nothing matched.

**edit** — change a prompt's text:
1. `find` first to get the `id` of the one to change.
2. `node ~/.prompt-pocket/pocket.mjs edit <id> "<new prompt>"`
Report `before` / `after`. (Note: the `id` changes with the new text.)

**find** — check whether a prompt is in the pocket:
```
node ~/.prompt-pocket/pocket.mjs find "<keyword>"
```
List `matches` (already sorted by frequency); on `count: 0` say plainly it isn't there.

**sync** — force-regenerate the native dropdown files for every installed host (normally
automatic after any change; use after a manual store edit):
```
node ~/.prompt-pocket/pocket.mjs sync
```

---

## Principles
- The script is the single source of truth: all create/read/update/delete and frequency
  go through it — never "remember" the data yourself.
- Before delete/edit, if there's ambiguity (multiple matches), list them and let the user
  confirm before acting.
- Pick-to-run is the soul of this skill: after the user picks, don't stop at echoing —
  start doing the work.
- The native dropdown is generated by `sync` into each host's command dir
  (`~/.claude/commands/usually/`, `~/.config/opencode/commands/usually/`,
  `~/.codex/prompts/usually-*.md`). Only files bearing the
  `<!-- prompt-pocket:generated -->` marker are ever deleted; Codex's shared dir is
  additionally gated by the `usually-` filename prefix, so the user's own prompts are
  never touched.
- `sync` also bootstraps a bare, global **`/usually` manager command** at
  `~/.claude/commands/usually.md` (and the OpenCode equivalent) — a user-level command, so
  it renders its argument-hint (plugin commands can't: prefix is forced + hint is suppressed
  by claude-code bug #46626). It's marker-gated and never overwrites a user-authored
  `usually.md`. So on a plugin-only install, the first `/prompt-pocket:usually` run is what
  creates the nicer global `/usually`.
