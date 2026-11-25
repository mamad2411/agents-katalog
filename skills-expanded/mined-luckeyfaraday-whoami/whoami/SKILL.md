---
name: whoami
description: Build a complete picture of who the user is and what they do by scanning their machine (git, projects, toolchains, AI-agent session history across Claude/Codex/Droid/OpenCode/Gemini/Qwen, dotfiles, normal files) AND interviewing them. Produces a portable profile any agent can load as instant context. Use when the user types `/whoami`, asks to onboard, build their profile, or "figure out who I am".
---

# whoami

Goal: produce `~/.whoami/profile.md` — a dense, accurate portrait of the user (identity, role, expertise, current work, tooling, working style, goals) that any future agent can read in seconds to skip the "getting to know you" phase.

Two information sources, combined:
1. **Machine scan** — objective signals already on disk.
2. **Interview** — intent, goals, and preferences the machine can't reveal.

Never invent facts. Scan tells you *what*; the interview tells you *why*. Where they conflict, ask.

## Phase 1 — Scan

Run the bundled scanner and read its output. It only emits dev/work signals + normal-file structure, and redacts anything matching secret patterns.

`scan.sh` lives in **this skill's own directory** (the base directory shown when the skill loads, e.g. `<skill-dir>/scan.sh`). Use that path — it works whether the skill is installed as a plugin or symlinked manually. If `$CLAUDE_PLUGIN_ROOT` is set, the script is at `$CLAUDE_PLUGIN_ROOT/skills/whoami/scan.sh`.

```bash
bash "<skill-dir>/scan.sh"                      # full scan
bash "<skill-dir>/scan.sh" --max-repos 40 --depth 2   # cap noise on huge machines
```

Sections it returns: Identity, System, Toolchains & languages, Installed packages, Git repositories, Editor/dotfile config, Claude Code context (incl. authored MEMORY.md files), **AI agent sessions across CLIs** (Claude, Codex, Droid/Factory, OpenCode, Gemini, Qwen — counts, recent project dirs, recent prompts), Shell history (most-used + recent), Home folder structure, Recently modified files.

Read it as evidence. Note: agent project paths are decoded leniently (`_` and `/` both show as `/`) — treat them as hints. Form hypotheses but don't finalize:
- What do they build? (languages, repos, recent commits, agent prompts)
- What are they working on *now*? (recent files, recent agent sessions, active branches)
- How do they work? (which agents/editors/tools dominate, shell patterns)
- Who are they? (git identity, the projects' subject matter)

## Phase 2 — Interview (onboarding)

This is the heart of the skill — be thorough, ask **many** questions. Use the machine scan to make questions specific and grounded, never generic. Prefer the `AskUserQuestion` tool with concrete multiple-choice options drawn from what you found (the user can always pick "Other").

Ask in small batches (2–4 questions at a time), adapting follow-ups to answers. Cover, at minimum:

1. **Identity & role** — name to use, profession/title, company or solo, seniority. (Confirm git identity; it may be a pseudonym.)
2. **What they do** — primary focus area(s); confirm/refine the project list found on disk. Which repos are active vs. archived vs. someone else's?
3. **Current priorities** — what are they working on this week/month? What's the big goal?
4. **Expertise & stack** — strongest languages/domains; what they're learning; what they avoid.
5. **Working style & preferences** — how they like agents to behave (terse vs. explanatory, ask-first vs. autonomous, test-first, commit conventions). Cross-check against any feedback memories found.
6. **Tools & environment** — primary editor, primary agent CLI, OS quirks, anything an agent should know to not break their setup.
7. **Collaboration & output** — solo or team? Who's the audience for their work? Public (GitHub handle, content channels) vs. private?
8. **Constraints & boundaries** — anything off-limits, privacy concerns, regulated data, hard rules.
9. **Goals beyond code** — career, business, learning, or creative goals that give agents the "why."
10. **Anything the scan missed** — open-ended: "What's the most important thing about how you work that I wouldn't guess from your files?"

Drill into surprises from the scan (e.g. "I see 411 Codex sessions but you're now in Claude Code — did you switch? why?"). The interview should feel like a sharp colleague who already read your repos.

## Phase 3 — Synthesize & write

Merge scan + interview into `~/.whoami/profile.md`. Create `~/.whoami/` if needed. Structure:

```markdown
# whoami — <name>
_generated <date> · sources: machine scan + interview_

## Snapshot
<2–3 sentence elevator description of the person and what they do>

## Identity
## Role & focus
## Current work        # active projects, priorities, goals (dated)
## Expertise & stack
## Tooling & environment   # agents, editors, OS, conventions
## Working style & preferences   # how agents should behave with them
## Constraints & boundaries
## Goals
## Open questions / low-confidence   # things to confirm later
```

Rules for the profile:
- Mark each major claim's basis implicitly: scanned facts are reliable; interview statements are authoritative for intent. Put anything uncertain under "Open questions."
- Convert relative dates ("this week") to absolute dates.
- Keep it dense and skimmable — this is loaded as context, not prose to enjoy.
- Also write `~/.whoami/scan-raw.txt` (the raw scan) so a profile can be regenerated.

Then offer two follow-ups:
- **Persist to Claude memory** — write key durable facts into the user's `~/.claude/.../memory/` as `user` / `feedback` memories (follow the memory format) so they apply automatically in future sessions.
- **Re-run** — `/whoami` is idempotent; on re-run, diff against the existing profile and ask only about what changed.

## Privacy contract

- Scope is conservative + normal-file *structure*. The scanner redacts secrets and never prints file contents of personal docs (only names/paths).
- Everything stays local. Never transmit the profile or scan anywhere without explicit user say-so.
- If the user asks for broader scope (browser history, SSH hosts, doc contents), confirm first, then extend.
