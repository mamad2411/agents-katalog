---
name: skill-scout
description: >-
  Discover the best Claude Code extensions on the web AND tell the user how safe each one is
  before installing. Reads the user's Claude Code setup (project context, memory, history), asks a
  few questions to understand their goal (general or a specific idea), then surfaces a ranked
  shortlist - name, what it does, what outputs it gives, a 0-100 trust score, a one-line
  why/why-not, and a link. On a chosen extension it runs a deep static safety scan and returns a
  final risk verdict (always caveated), then installs it on approval (SHA-pinned). Covers Skills,
  MCP servers, plugins, and slash commands. Triggers - "find me a skill", "recommend a skill",
  "which skill should I use", "is this skill safe", "vet this extension", "check this MCP",
  "מצא לי סקיל", "האם הסקיל הזה בטוח", "/skill-scout".
allowed-tools: Bash, Read, Glob, Grep, WebFetch, WebSearch, Task, AskUserQuestion
---

# skill-scout

The safety layer for growing your Claude Code setup. Every directory online ranks **popularity**;
none tells you if an extension will read your `.env` or rug-pull after you trust it. skill-scout
adds the missing signal: it finds the good ones **and vets them**.

`SKILL_DIR` below = the folder this file lives in. Run the CLI as
`python3 SKILL_DIR/scripts/scout.py ...` (no `cd` needed). Requires Python 3.9+ and git; the `gh`
CLI is optional but removes GitHub rate limits.

## Golden rules (never break)

1. **Never promise "safe".** This is static analysis + reputation. Always give the caveat
   (`references/verdict-template.md`) and separate "**what I scanned in the code**" (facts) from
   "**what is a reputation signal**" (inference).
2. **Never install without explicit approval**, and never offer install for **band 4-5**.
3. **SHA-pin every install** and record it, so a future update can be re-vetted (rug-pull defense).
4. **Respond in the user's language.** No em-dashes - use a hyphen.
5. The vetter never runs the cloned code. Don't work around that.

---

## Mode A - Discover ("find me a skill for…")

Use when the user wants ideas, or has a goal but not a specific repo.

**1. Understand them first (don't ask what you can read).**
Skim their Claude Code setup: `CLAUDE.md`, any memory file, recent history, installed extensions.
Form a one-line hypothesis of what they do and where an extension could help.

**2. Ask 2-4 sharp questions** (use AskUserQuestion). Pick what's actually unclear:
- General sweep or a specific idea in mind?
- The goal behind it (what would "great" look like)?
- Which ecosystems are in scope - Skills / MCP servers / plugins / commands? (default: all)
- Any hard constraints (no cloud, no API key, must be free)?

**3. Translate intent to English search terms** - the directories are English-indexed, even if
the user writes in another language.

**4. Run discovery** (once per ecosystem in scope):
```
python3 SKILL_DIR/scripts/scout.py discover "<english query>" --eco skill --limit 8
```
`--eco` ∈ skill | mcp | plugin | command. Returns JSON: ranked candidates each with `score`
(0-100 Tier-1 reputation), `score_band`, stars, source, repo_url, `requires_code_execution`.

**5. Present the shortlist** per `references/verdict-template.md` (table: # · name · what it does ·
outputs · score 1-100 · why/why-not · link), in the user's language. State plainly that the score
is **reputation, not a code audit**. Close by offering a deep vet on any of them.

---

## Mode B - Vet ("is this safe?")

Use when the user names a specific extension, or picks one from the shortlist.

**1. Run the deep static scan:**
```
python3 SKILL_DIR/scripts/scout.py vet <repo_url> [--ref <branch-or-sha>]
```
Returns JSON: `band` (1-5), `band_label`, `sha` (the exact commit scanned), `findings`
(category · severity · file:line · snippet), `green_flags`, `severity_counts`.

**2. Adjudicate findings yourself (this is the LLM half of "hybrid").**
- **band 1-2:** trust the scan. Summarize.
- **band 3+ or any HIGH/CRITICAL:** do NOT just relay the scanner. **Read the actual flagged
  lines** (fetch the file - raw GitHub URL or `git show`) and judge real-vs-false-positive. The
  scanner is deliberately trigger-happy; your job is to confirm intent.
- **Borderline trust:** escalate reputation - a quick `WebSearch`/`WebFetch` on the publisher +
  repo (or spawn a research subagent) for incidents, age, who they are.

**3. Give the final verdict** per `references/verdict-template.md`: risk band + label, the **code
facts**, the **reputation signal**, green flags, one honest bottom line, and the **mandatory
caveat**. Optionally collapse to a 1/2/3 shorthand (rubric) but keep the 1-5 band in any record.

**4. Scoring meaning** lives in `references/scoring-rubric.md`; the detection rules in
`references/threat-model.md`. Read them if unsure how a number was reached.

---

## Install on approval (only after a vet)

For **band 1-2** (or band 3 the user explicitly accepts after your review):
```
python3 SKILL_DIR/scripts/scout.py install <repo_url> --name <name> --sha <sha> --band <N> --score <N>
```
This clones the **exact vetted commit** into `~/.claude/skills/<name>/`, strips `.git` (static
copy), records it in `~/.claude/skill-scout/registry.json`, and reports whether a `SKILL.md`
loaded. Then tell the user: it's pinned to `<sha>`; if it updates later, ask skill-scout to re-vet
before pulling the new version.

- **MCP / plugins (Phase 2):** `install` returns the exact `claude mcp add` / `/plugin install`
  command for the user to run - it does **not** auto-execute these yet. Hand them the command +
  your verdict; never run it silently.
- **band 4-5:** never offer install. State it's not recommended and why, in one clear line.

---

## Honesty discipline

- Mark every claim: scanned-in-code vs reputation-signal.
- "Clean scan" = "no known red flags found", **not** "proven safe". Say it that way.
- If a source failed or returned nothing (e.g. a flaky directory), say so - don't imply full
  coverage.

## Scope notes
- This release fully covers the **Skills** ecosystem (discover + vet + install). MCP / plugins /
  commands: discovery works now; deep MCP-poisoning + hooks scanning and auto-install are planned.
  Be honest about that boundary when asked.
- Sources are config: `references/sources.yaml`. The skills.sh audit is a cross-check, never sole
  truth.
