# FounderOS - Gemini CLI Context

Context loader for Gemini CLI and other non-Claude agents operating in this repo.

This file is a thin bridge, not a separate rulebook. The canonical instruction file is `CLAUDE.md` - the full cross-agent reference (repo map, roles, slash commands, substrate, hooks, what-not-to-do) lives there. `AGENTS.md` is a peer bridge that carries the same cross-agent deltas for Codex-style agents. Read `CLAUDE.md` at session start.

---

## Read first

1. `CLAUDE.md` - the source of truth for how this OS behaves, and the full cross-agent reference (repo map, roles, skills, commands, hooks, substrate).
2. `AGENTS.md` - a peer bridge listing the same cross-agent deltas (slash commands not executable, skills as procedural reference, do not claim hooks ran).
3. `README.md` - the product picture and setup path.

Do not duplicate or override those files here. If anything in this file ever disagrees with `CLAUDE.md`, `CLAUDE.md` wins.

---

## Gemini-specific operating notes

- The slash commands in `.claude/commands/` are Claude Code specific. You cannot run them. Treat them as documented procedures, not executable actions.
- Run only what your environment actually supports, and say plainly what you can and cannot do. Slash commands and hooks are Claude Code only, so do not claim they fired. If you are pointed at the folder with write access you can run `reasoning` and `local-writes` skills directly; if your environment cannot run a script, read the produced artifacts for a `local-exec` skill instead of running it. Never claim that setup, hooks, a file write, MCP authentication, or a scheduled routine happened when it did not.
- Skills in `skills/<name>/SKILL.md` are readable as procedural reference. The trigger frontmatter is for Claude's auto-invocation; the protocol body is portable and you can follow it by hand.
- Runtime honesty and the per-skill `Runs on:` contract: every skill declares its runtime class (`reasoning`, `local-writes`, or `local-exec`) on a `Runs on:` line in its `SKILL.md`. The full contract and the honest-degradation rule live in `CLAUDE.md`. Read it there. If you are pointed at the folder with write access you may run a `local-writes` skill; if you cannot run a script you read the produced artifacts for a `local-exec` skill and say so. If anything here disagrees, `CLAUDE.md` wins.
- Do not invent the operator's identity, priorities, decisions, clients, or revenue. If the six context files named in `CLAUDE.md` are missing, the OS is not set up - point the user to the setup wizard and stop.
- When you give an opinion of consequence, follow the output bias self-check in `rules/biases.md`: attach a counter-case, a confidence level, what evidence is absent, and the do-nothing option. There is no bias-free advice; name the most likely bias and argue the other side rather than claim none exists.
- If you do recurring work in this OS (an SEO pass, outreach drafting, a content pipeline), you are a candidate digital employee. The team contract - charters in `roles/employees.yaml`, propose-only vs draft-only, seats earned through recorded runs, nothing sent on the operator's behalf - is in `AGENTS.md` under "Joining the operator's team". It applies to you the same way.

---

## Writing and commits

- No em dashes, no en dashes. Simple hyphens with spaces.
- No banned words (delve, robust, seamless, leverage as a verb, comprehensive, governance, diagnostics, and the rest listed in `rules/writing-style.md`).
- Commit messages follow `rules/commit-naming.md`: plain-language subject, no version-only subjects, no AI attribution trailers.

---

## Built by

[ARCAS Systems](https://arcassystems.com).
