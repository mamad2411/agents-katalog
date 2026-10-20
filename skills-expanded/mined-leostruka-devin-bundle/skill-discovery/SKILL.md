---
name: skill-discovery
description: Use when starting any non-trivial task, before taking any action a skill might apply to, when the user asks how to do something, when no skill seems to match, or when discovering, installing, or evaluating a new skill for Devin CLI.
triggers: [user, model]
---

# Skill Discovery

**If dispatched as a subagent for a specific task, ignore this skill.**

**If there is even a 1% chance a skill applies to what you are doing, you
MUST invoke it.** Not negotiable — no rationalizing.

## The Rule

Invoke relevant skills BEFORE any response or action — including clarifying
questions or exploring. If it turns out wrong for the situation, you don't
have to follow it. Announce "Using [skill] to [purpose]" and follow it; if it
has a checklist, create a todo per item.

Before entering plan mode without brainstorming: invoke `grilling` first.

**Priority:** process skills first (they set the approach), implementation
skills carry it out. "Let's build X" → `grilling` → impl skills. "Fix this
bug" → `debugging` → domain skills. "Just rename this" → `execution`'s
execution to decide if grilling can be skipped.

**Red flags** — you're rationalizing: "just a simple question", "need more
context first", "let me explore first", "I can check files quickly", "doesn't
need a formal skill", "I remember this skill" (skills evolve — read current),
"the skill is overkill", "just this one thing first".

**User instructions** (`.devin/global_rules.md`, `.devin/rules/*.md`, direct
requests) take precedence over skills; skills override defaults.

## Discovery workflow

1. **List:** `skill list --path .` ; `skill list --path ~/.config/devin`
   (Windows `%APPDATA%\devin\skills`).
2. **Search:** `skill search --path <dir> --keywords "<k1> <k2>"`.
3. **Check MCP:** `mcp_list_servers`, `mcp_list_tools --server_name <s>`.
4. **Built-in tools:** `web_search`, `webfetch`, `mcp_call_tool`,
   `run_subagent` for parallel exploration.
5. **Invoke matches immediately**, in parallel if several.
   Exception: skills whose frontmatter declares `agent:`/`subagent:` spawn a
   real autonomous subagent on invoke, costing a full agent loop. Check
   frontmatter first; invoke at most ONE per task, never inside a
   discovery batch.
6. **No local match → external search:** `github:<owner>/<repo>` (this
   bundle — `data/bundle-identity.json`), `gh search repos <kw> skills`,
   `web_search`.
7. **Evaluate before installing:** relevance (README describes the task?),
   compatibility (Devin CLI patterns — `run_subagent`, `skill list`,
   `.devin/skills/`; non-Devin refs need adaptation), quality (recent
   commits, tests, examples, no hardcoded secrets).
8. **Install** into `~/.config/devin/skills/<name>/` (global) or
   `.devin/skills/<name>/` (project); adapt non-Devin tool names/paths,
   bash→Python helpers; verify via `skill list`.
9. **Nothing anywhere** → say so, help directly, suggest a minimal skill if
   the task recurs (`.devin/skills/<name>/SKILL.md`).

## Category shortcuts

| Task | Consider |
|---|---|
| Git / PR | `git-workflows`, `gh`, `code-review` |
| GitHub ops | `gh`, GitHub MCP, `web_search` |
| CSV / data | `python` (pandas), `grep` |
| Debugging | `debugging`, `testing` |
| Verification | `gates` |
| Documentation | `context7`, `web_search`, `webfetch` |
| Exploration | `research` |
| Planning | `planning`, `execution` |
| Context/cost | `context-hygiene`, `mcp-governance` |

## Creating or updating a skill

Wrong/incomplete skill → update it in place first. New recurring pattern →
minimal skill: `SKILL.md` with when-to-use, steps, examples, pitfalls — see
`writing-skills`.
