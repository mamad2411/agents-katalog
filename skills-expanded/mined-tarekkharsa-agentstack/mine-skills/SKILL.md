---
name: mine-skills
description: Mine your past agent sessions (Claude Code, Codex) for recurring failures and re-explained procedures, then distill the best candidates into reusable skills that land in the central library via `agentstack more lib add`. Local and read-only until you approve a draft.
---

# Mine skills from your sessions

Use when you want to turn *what kept going wrong* into *skills that stop it
going wrong* — analyze the last week/month of agent sessions, find the moments
worth teaching, and draft skills from them.

A one-off mistake is not a skill. A mistake you corrected twice — or a
procedure you re-explained in three different sessions — is the definition of
one.

## Where the data is

- **Claude Code:** `~/.claude/projects/<project-hash>/<session-id>.jsonl` —
  one event per line; assistant turns carry `message.usage` token counts,
  tool-use events name the tool/skill invoked, user turns hold corrections.
- **Codex:** `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl` — lines are
  `{timestamp, type, payload}`; payload types include `user_message`,
  `message` (roles user/assistant/developer), `function_call` /
  `function_call_output`, `token_count`, `task_started` / `task_complete`.

Both formats are undocumented and drift — tolerate unknown lines, never
assume a fixed schema. Use python for the parsing, not shell one-liners.

## The loop

1. **Harvest** — walk both transcript trees, scoped by date (e.g. last 30
   days). Note which agents you could actually see; coverage is uneven.
2. **Detect** skill-worthy moments (signals below).
3. **Cluster & rank** — group recurrences of the same failure across
   sessions; rank by `frequency × wasted tokens`. Two strong clusters beat
   twenty weak ones — propose few, high-signal candidates.
4. **Draft** — for each top cluster, write the *corrected* procedure as a
   SKILL.md (use the skill-creator skill if available). The skill teaches the
   right way, not a description of the failure.
5. **Land it on the rails** — show the draft to the user; on approval:
   `agentstack more lib add ./<draft-dir> --name <name> --write`. That path
   content-scans it, records provenance, checksums it, and makes it
   referenceable by name from any project (and syncable via `lib sync`).

## Detection signals (strongest first)

- **Re-explained procedures** — the same multi-step instruction reconstructed
  from scratch in different sessions. The best single signal.
- **User corrections** — "no, do X instead", "that's wrong", an immediate
  redo of the same file or command after feedback.
- **Retry storms** — the same tool/command repeated with small tweaks before
  it finally works (e.g. a build flag discovered by trial and error).
- **Long recoveries** — many turns or an outsized token spike between a task
  starting and landing.

## Rules

- **Local, read-only, aggregate.** Never send transcript content anywhere;
  quote only the minimum needed to justify a candidate. Prompt bodies can
  contain secrets — never copy them into a draft skill.
- **Propose, don't install.** A draft becomes a library skill only after the
  user reviews it. Never run `lib add --write` without approval.
- **Require recurrence.** Default bar: seen in ≥ 2 distinct sessions. Below
  that, mention it at most as an honorable mention.
- **Prefer updating an existing skill** over minting a near-duplicate — check
  `agentstack more lib list` first.
