---
name: project-skill-drafter
description: Use this the first time you work in a project that has no project-level skill or CLAUDE.md yet, or whenever the founder says something like "learn this codebase", "set up vovy for this project", "generate a project skill", or "remember how this project works". Analyzes this {{PROJECT}} project's actual stack and structure and drafts a tailored project-specific skill file, so future requests in this project automatically come with the right context without the founder having to explain the stack every time.
---

# Project Skill Drafter

Generic advice is worse than no advice — a skill that says "use good practices" doesn't help a founder whose project is a specific Next.js app with a specific database and a specific folder layout. This skill's job is to turn facts about *this* project into a short, specific instruction file the host tool will automatically load on every future request in this project.

## What to do

1. **Call the `analyze_project` MCP tool** (served by `@vovy-ai/mcp-server`, already registered if Vovy is installed) to get deterministic, non-guessed facts about the project: detected stack/framework, package manager, key directories, test setup, and any obvious footguns (e.g. a committed `.env` file). This tool does no reasoning — it just reports what's actually in the repo. If the tool isn't available for some reason, do the equivalent by reading `package.json` and the top-level folder structure yourself.
2. **Turn those facts into judgment**, which is the part the tool can't do: what does this stack actually imply about how to work in this repo? (e.g., "this is a Next.js App Router project — server components by default, routes live under `app/`" or "tests run with `pnpm test`, there is no CI yet").
3. **Draft a short project skill file** — for Claude Code, this is `.claude/skills/project-context/SKILL.md` (or `CLAUDE.md` at the repo root if that convention is already in use); for Codex CLI, `.agents/skills/project-context/SKILL.md`; match whatever convention the host tool you're running in actually uses. Keep it to what a returning contributor would need on day one:
   - Stack and key libraries/frameworks, with versions if they matter
   - How to install, run, test, and build
   - Where things live (a few key directories, not a full file tree)
   - Project-specific conventions actually observed in the code (naming, folder patterns, state management approach) — only include what you actually saw, don't invent conventions
   - **Constraints with their why**, never bare rules. "Don't use native modules" invites a future session to relitigate it; "don't use native modules — installs must work on machines with no compiler" transfers the judgment to cases nobody anticipated. If `.vovy/memory/` exists in the repo, fold its `constraint` entries in here (or point to them) instead of restating rules from scratch — that's where the why already lives.
   - Anything that looked like a footgun worth flagging (secrets in version control, missing `.env.example`, etc.) — pair this with the Founder Explainer skill's guidance rather than duplicating it
4. **Show the draft to the founder before writing it** if a project skill file already exists — don't silently overwrite prior context someone may have hand-edited. If none exists yet, it's safe to create it directly.
5. **Keep it short.** A project skill file that's too long won't get fully read by the host's context budget on every turn. Prefer a tight, high-signal file over an exhaustive one — this mirrors why Agent Skills load progressively in the first place.

## Why this matters

This is how Vovy delivers "auto-generated, project-specific skills" without ever running its own model: the `analyze_project` tool supplies verified facts for free (plain static analysis, no LLM call), and this skill instructs the founder's own already-paid host model to turn those facts into judgment. Nothing here requires a Vovy-hosted service.
