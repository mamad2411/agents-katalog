---
name: multi-agent-skill-sharing
description: >-
  Install a skill once and make it usable across multiple AI coding agents
  (Claude Code, Codex CLI, Cursor, Gemini CLI, Cline, etc.) that work on the
  same repository. Use this when the user wants a skill / ruleset / prompt to be
  shared and switchable across several AI products, asks "why can only one tool
  use this skill", or wants cross-tool consistency. It maps each agent to its
  correct skill-reading directory, installs into the repo so the skill travels
  with Git, and documents the per-tool invocation syntax (which differs — e.g.
  Codex uses `$skill-name` or `/skills`, NOT gstack-style `/design` commands).
license: MIT
---

# multi-agent-skill-sharing

Install a skill **once** and make every AI coding agent working on the same
repository able to read it and invoke it in its own way.

> This skill is tool-agnostic. It works whether you use two agents or six.

## When to use

- You use **multiple AI coding products on the same project** (e.g. Claude Code
  + Codex + Cursor) and want a skill / ruleset / prompt to be shared and
  switchable between them.
- Someone asks **"why can only one tool use this skill?"** or "why can't I call
  it in tool X?"
- A skill is installed but one agent can't find it.
- You want a skill to live **inside the repo and travel with Git**, so it
  survives a new machine or a new teammate.

## The core mental model (read this first, or you'll install it wrong)

**There is no shared skills directory across agents. "Install once, all tools
see it" is literally false.** Each product reads skills from a *different*
directory, and the **invocation syntax differs too**.

Real sharing is achieved by installing the skill into **per-agent directories
that live inside the repository**, so it travels with Git. One physical copy per
agent, all committed, all in sync.

### Where each agent reads skills + how you invoke them

> ⚠️ **Verify paths against the current version of each tool before relying on
> this table.** These conventions move fast. Last verified: **2026-07** (see
> "Verification" below). When in doubt, check the tool's own docs or probe the
> filesystem.

| Agent | Repo-level dir (travels with Git) | User-level dir | How to invoke |
|-------|-----------------------------------|----------------|---------------|
| **Claude Code** | `<repo>/.claude/skills/` | `~/.claude/skills/` | Mention the skill by name in chat. Some suites (e.g. gstack) add `/slash` commands on top. |
| **WorkBuddy** | `<repo>/.workbuddy/skills/` | `~/.workbuddy/skills/` | Mention the skill by name (same convention as Claude Code). |
| **Codex CLI** | `<repo>/.agents/skills/` **and/or** `<repo>/.codex/skills/` (see note) | `~/.agents/skills/` **or** `~/.codex/skills/` (see note) | `$skill-name`, the `/skills` picker, or just name it in the prompt. **NOT** a `/design`-style slash command. |
| **Cursor** | `<repo>/.cursor/skills/` (also reads `.cursor/rules/` `.mdc`) | — | Rules auto-inject; also tolerates `.agents/` skills. |
| **Antigravity** | `<repo>/.antigravity/skills/` (VS Code–based, convention) | — | Mention the skill by name; vendor path unverified. |
| **Gemini CLI** | `<repo>/.agents/skills/` | — | Auto-discovered; name it in the prompt. |
| **Cline** | `<repo>/.cline/skills/`, `.clinerules/skills/`, **or** `.claude/skills/` | `~/.cline/skills/` | Name it; gated behind an experimental toggle. |

### Two things people get wrong about Codex

1. **`.agents/skills/` vs `.codex/skills/`.** OpenAI's official docs list the
   discovery tiers as *system → admin (`/etc/codex/skills`) → user
   (`$HOME/.agents/skills`) → repo (`.agents/skills`)*. **In practice many
   installs read `~/.codex/skills/` and `<repo>/.codex/skills/` instead**, and
   `~/.agents/` may not even exist on the machine. This is version drift. The
   safe move: **install into BOTH `.agents/skills/` and `.codex/skills/`** at
   the repo level (they're cheap Markdown copies), or set the
   `CODEX_SKILLS_PATH` env var to a directory you control.

2. **Codex skills are NOT triggered by `/slash` commands.** Use `$skill-name`,
   the `/skills` picker, or mention the name. A command like `/design` is a
   *gstack* extension specific to Claude Code — other products don't have it.
   (Codex's old `~/.codex/prompts/` custom-prompt mechanism is deprecated;
   don't build on it.)

> 💡 **Emerging convention:** `.agents/` is becoming the *cross-agent* standard
> repo path — Codex, Gemini CLI, and Cursor all accept it, and Cline tolerates
> `.claude/skills/`. When you can only maintain one path, `.agents/skills/` is
> the best single bet for future portability.

## Steps

### 1. Identify the skill's source and shape

- Is it a standard **`SKILL.md`** skill (has a `name:` frontmatter)?
- Pure Markdown, or does it bundle executable scripts?

```bash
# List anything that is NOT documentation — potential scripts to audit
find <skill-src> -type f ! -name '*.md' ! -name '*.txt'
```

If it bundles scripts, **audit them before distributing.**

### 2. Assess size — decide whether it can live in the repo

```bash
du -sh <skill-dir>
```

- **Lightweight (a few KB–MB, pure Markdown) → commit it into the repo.**
  This is the only way to get true multi-agent sharing.
- **Heavy (bundles `node_modules`, hundreds of MB–GB) → global install only.**
  It cannot go in the repo (it would bloat the project and pollute handoffs).
  Such a skill is usable **only by the product it was built for**; document
  that limitation explicitly.

### 3. Detect which agents are in use

```bash
# User-level homes
ls -d ~/.claude ~/.codex ~/.agents ~/.cursor ~/.cline 2>/dev/null
# Repo-level dirs
ls -d .claude .codex .agents .cursor .cline 2>/dev/null
```

Or just ask the user which tools they run.

### 4. Distribute into each agent's repo-level directory

If you already have one good copy, the fastest path is to fan it out. Each skill
must sit **exactly one level deep** in its own subdirectory (agents don't
recurse).

**macOS / Linux:**

```bash
cd <repo>
mkdir -p .claude/skills .agents/skills .codex/skills
# Fan out from one known-good copy (preserves per-skill subdirs):
cp -R .claude/skills/. .agents/skills/
cp -R .claude/skills/. .codex/skills/
```

**Windows (PowerShell):**

```powershell
cd <repo>
New-Item -ItemType Directory -Force .\.claude\skills, .\.agents\skills, .\.codex\skills | Out-Null
Copy-Item -Recurse -Force .\.claude\skills\* .\.agents\skills\
Copy-Item -Recurse -Force .\.claude\skills\* .\.codex\skills\
```

When distributing from a source repo of many skills, use each skill's
frontmatter `name` as its subdirectory name. The bundled
`engine/distribute.py` automates this cross-platform.

### 5. Verify placement

```bash
for d in .claude/skills .agents/skills .codex/skills; do
  echo "=== $d ==="; ls "$d" 2>/dev/null | wc -l
done
head -5 .agents/skills/<a-skill>/SKILL.md   # spot-check frontmatter
```

Confirm every target dir exists, counts match, and core `SKILL.md` frontmatter
is intact.

### 6. Write routing notes into `AGENTS.md`

`AGENTS.md` at the repo root is read by Codex directly (and often symlinked to
`CLAUDE.md`). Add a short section stating **which skills live where, who can use
them, and the correct invocation syntax per tool** — especially the note that
Codex does not use `/slash`. If the project has a docs system, add a fuller
`docs/SKILLS_GUIDE.md` and index it from `AGENTS.md`.

### 7. Commit — it isn't "shared" until it's in Git

The new `.claude/skills`, `.agents/skills`, `.codex/skills` dirs are untracked.
Sharing only lands once they're committed; otherwise a new machine loses
everything.

```bash
git add .claude/skills .agents/skills .codex/skills AGENTS.md
git commit -m "chore: share skills across AI agents"
```

## Pitfalls

- **Treating a user-level install (`~/...`) as "sharing".** It doesn't travel
  with Git and dies on a new machine. Sharing must go **inside the repo**.
- **Assuming a common directory exists.** It doesn't. Each product reads its
  own path.
- **Assuming Codex uses `/slash` to run skills.** It uses `$skill-name` /
  `/skills` / a name mention. `/xxx` is a deprecated custom-prompt mechanism.
- **Betting on a single Codex path.** `.agents/skills/` and `.codex/skills/`
  both appear in the wild — install both, or set `CODEX_SKILLS_PATH`.
- **Committing a GB-scale skill (bundled `node_modules`) into the repo.** It
  bloats the project and pollutes handoffs. Heavy skills stay global-only.
- **Forgetting to commit.** Installing without committing = no sharing.

## Verification

- Each target agent's repo-level skill dir exists, skill counts match, and core
  `SKILL.md` frontmatter is valid.
- `AGENTS.md` (and optional `docs/SKILLS_GUIDE.md`) records per-tool invocation
  syntax, explicitly noting Codex does not use `/slash`.
- Changes are committed to Git.

---

**Last verified:** 2026-07 against Claude Code, WorkBuddy, Codex CLI, Cursor,
Antigravity (plus Gemini CLI and Cline) conventions. Skill-discovery paths
change frequently — re-check the per-tool docs if something doesn't resolve.
