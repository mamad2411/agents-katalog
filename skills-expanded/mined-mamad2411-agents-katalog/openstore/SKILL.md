---
name: openstore
description: Use when the user wants you to recall something about them or their world, remember a durable fact for later, or correct/undo something previously stored. OpenStore is a private GitHub repo of plain Markdown reachable through bash-like MCP tools (ls, find, grep, cat, head, tail, tree, git_log, git_show, git_diff, pwd, write, mv, rm, git_revert). Trigger on requests like "remember that...", "what do you know about...", "forget/undo that", or whenever durable personal/project context would help answer the current question.
---

# OpenStore

OpenStore is the user's own private Git repository, read and written through bash-like MCP
tools. There is no database behind it — the repo on GitHub is the only copy of anything. Treat
every write as a real commit the user can see, diff, and revert.

## When to use this skill

- The user asks you to recall something about themselves, their setup, their preferences, or a
  project ("what router do I have?", "what do I use my Mac mini for?").
- The user shares a durable fact worth keeping ("remember that I switched ISPs", "my new email
  is...", "I decided to use Postgres for pocket-watch").
- The user wants to correct, update, or undo something previously written.
- You are about to answer a question where checking the store first would make the answer more
  accurate or personal — check before asserting; don't guess when you can look.

Do not use it for scratch/ephemeral task state, secrets, credentials, or anything the user hasn't
implied should be durable and personal.

## The workflow

1. **Search first.** `grep -ril` (or plain `grep -r`) for the topic across the whole store before
   assuming a fact isn't there, and before creating a new file. Follow up with `find` if you're
   looking by filename/folder shape instead of content.
2. **Read before writing.** `cat` the matching file(s) to see current content, structure, and any
   existing `Source:` line before proposing a change.
3. **Show the exact change.** Before calling `write`, tell the user in chat exactly what the new
   or changed text will be (not just "I'll save that") — enough that agreeing to it is informed
   consent. This is the only consent gate; there are no approval pages or PRs.
4. **Write only after the user agrees.** Never call `write`, `mv`, or `rm` speculatively or in the
   same turn as an unconfirmed ask. If the user's message already contains clear, explicit
   instruction to save something (e.g. "remember that X"), that instruction itself is the
   agreement — you don't need to ask again before writing it.
5. **Report the result concretely.** After a write, tell the user the file path, a one-line
   summary of the change, and the short SHA the tool reports (seven characters, e.g.
   `1f7abd7`). Never say something is "saved" or "remembered" until the write tool has actually returned success — distinguish
   clearly between "I found this in the store" and "I haven't written this yet."

## Rules

- **Update over duplicate.** If a fact already lives in a file, edit that file (or use `write`
  to replace it in place) rather than creating a second file that says something similar.
- **Follow existing folders.** New facts go into the existing structure (`profile/`, `home/`,
  `technology/`, `projects/`, `preferences/`, `people/`, etc.) by topic. Only create a new
  top-level folder when nothing existing fits and the user's store doesn't already have an
  obvious place for it.
- **Keep files focused.** One topic per file. Don't let a file become a junk drawer — split it
  when it outgrows its subject.
- **Note source and date when it helps.** For facts that could go stale or that came from a
  specific conversation, add a short `Source:` line (e.g. `Source: told by John, 2026-09-06`).
  Not required for stable, obvious facts.
- **Never store secrets.** No passwords, API keys, tokens, or anything else sensitive belongs in
  the store — it's Markdown meant to be read, not a vault. If a user asks you to store a secret,
  say no and explain why.
- **Surface contradictions.** If new information conflicts with what's already written, point out
  the conflict to the user and ask which is right instead of silently overwriting or silently
  keeping both.
- **No unnecessary reorganization.** Don't restructure folders or rewrite unrelated files as a
  side effect of a small change.
- **Repo-scoped, text only.** You can only see plain text files (`.md .markdown .txt .yml .yaml
  .json .csv`) inside the repo; dotfiles/dot-directories and non-text files are invisible, not
  just off-limits.

## Worked examples

### Example 1 — Recalling a fact

User: "What's my home network setup again?"

Call `grep`:
- tool: `grep`
- args: `-ril "network"`
- (no `content` — grep is a read tool)

Output:
```
home/network.md
```

Call `cat`:
- tool: `cat`
- args: `home/network.md`
- (no `content`)

Output:
```
# Home network

- Gateway: UDM Pro Max.
- Replaced a previous Amplifi Alien gateway.

Source: seeded 2026-09-06 from OpenStore project notes; confirm with John
```

Reply to the user: "Your gateway is a UDM Pro Max — it replaced an Amplifi Alien, per
`home/network.md`."

### Example 2 — Remembering a new fact into an existing file

User: "Remember that I also added a Ubiquiti switch alongside the UDM Pro Max."

Step 1, search: tool `grep`, args `-ril "UDM Pro Max"` → `home/network.md`.

Step 2, read: tool `cat`, args `-n home/network.md` → shows the current file above with
line numbers.

Step 3, show the change in chat: "I'll update `home/network.md` to add the switch:
```
# Home network

- Gateway: UDM Pro Max.
- Replaced a previous Amplifi Alien gateway.
- Switch: Ubiquiti switch alongside the gateway.

Source: seeded 2026-09-06 from OpenStore project notes; confirm with John
Source: told by John, 2026-09-06
```
Save this?" User says "yes."

Step 4, write:
- tool: `write`
- args: `-m "Add Ubiquiti switch to home network" home/network.md`
- content:
```
# Home network

- Gateway: UDM Pro Max.
- Replaced a previous Amplifi Alien gateway.
- Switch: Ubiquiti switch alongside the gateway.

Source: seeded 2026-09-06 from OpenStore project notes; confirm with John
Source: told by John, 2026-09-06
```

Output: `wrote home/network.md (+1 -0) @ a1b2c39`

Step 5, report: "Done — added the switch to `home/network.md` (commit `a1b2c39`)."

### Example 3 — Undoing a change with git_log + git_revert

User: "Actually, undo that last network change."

Call `git_log`:
- tool: `git_log`
- args: `--oneline -5 -- home/network.md`

Output:
```
a1b2c39 Add Ubiquiti switch to home network
7d4e9f2 write home/network.md
```

Confirm in chat: "That was commit `a1b2c39`, 'Add Ubiquiti switch to home network.' I'll revert
it — want me to?" User says "yes."

Call `git_revert`:
- tool: `git_revert`
- args: `-m "Undo: remove Ubiquiti switch note" a1b2c39`
- (no `content` — git_revert only takes args)

Output: `reverted a1b2c39 "Add Ubiquiti switch to home network" @ f00d12e`

The quoted subject is the *original* commit's message; the sha after `@` is the new revert commit.

Report: "Reverted — `home/network.md` is back to just the UDM Pro Max gateway (commit `f00d12e`).
Nothing was deleted from history; `a1b2c39` is still there if you ever want it back."
