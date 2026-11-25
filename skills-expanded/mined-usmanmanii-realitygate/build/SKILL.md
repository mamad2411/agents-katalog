---
name: build
description: Start or continue building a real, deployable MVP with the RealityGate Build OS — a spec-driven, test-first operating system for a solo founder on a small budget that turns an SRS, idea and research into a shipped product, with adversarial review and human approval on risky decisions. Use when the user wants to start a new app or product, says "start <path to SRS>", shares an SRS, PRD or requirements document to build from, wants to plan an MVP with AI agents, or says continue, resume, status, verify, next, checkpoint, ship, prepare release or plan next release in a project that has BUILD-OS.md.
---

# RealityGate Build OS

First check which case applies: a Build OS project has `BUILD-OS.md` and `.agent/STATE.json`.

## Start (no `.agent/STATE.json` yet)

Go one step at a time and wait for the user's answer at each question. Explain in plain
language; the user may not know the technical terms.

1. **Find the requirements.** If the user named a file ("start docs/SRS.pdf"), use it. If not,
   ask exactly one question, with these options:
   1. "I have an SRS or requirements document": ask for its path.
   2. "I'll drop my files in": tell them to put the SRS, research, notes and screenshots in
      `docs/input/` (any format), then say "ready".
   3. "I only have an idea": they'll fill in `docs/IDEA.md` (rough is fine) or answer your
      questions instead.
   Also ask whether they have research or reference documents; those go in `docs/input/`
   too. Never accept secrets: keys and passwords go in `.env.local`, which they fill in themselves.
2. **Git.** Make sure the folder is a git repo (`git init` if not, after asking the user).
3. **Install the kit.** It never overwrites existing files, and it copies the six Build OS
   subagents into `.claude/agents/`:

   ```bash
   node "${CLAUDE_PLUGIN_ROOT}/bin/realitygate.mjs" init --srs "<path to SRS>"   # or without --srs
   node "${CLAUDE_PLUGIN_ROOT}/bin/realitygate.mjs" doctor
   ```

   (Outside the plugin: `npx --yes realitygate init --srs "<path to SRS>"`.)

4. **Existing code?** If the repo already has application code, say so: Phase 0 adopts it
   (inventory and `realitygate audit`) instead of scaffolding a new app.
5. **Phase 0.** Read `BUILD-OS.md` in full, then `docs/IDEA.md` and every file in
   `docs/input/`, and execute **Phase 0 only**. The SRS is the primary requirements input;
   research informs how to build but never silently overrides an explicit requirement.
   Stop when the Phase 0 exit criteria are met and print: the contradictions and gaps you
   found in the documents, the recommended stack profile and its monthly cost estimate (one
   paragraph), the accounts and keys the user must create themselves, and the first batch of
   Phase 1 questions.

## Existing Build OS project (BUILD-OS.md and .agent/STATE.json exist)

Read `CLAUDE.md` and `.agent/STATE.json`, print one line (phase · release · task · step), and
follow `BUILD-OS.md` for the user's command. Users type these as plain words, not slash
commands (`/status`, `/resume` and `/plan` are Claude Code's own commands):

| User says | Do |
|---|---|
| continue / resume | Resume at exactly `current_step`; reconcile drift against `git status` first. Never skip the gate, the review or the proof step |
| status | Read-only report: phase, task, requirements verified X / Y by ID, counts by status, pending approvals, blockers, cost estimate |
| verify | Run `bash scripts/verify.sh`, report each gate verbatim as pass/fail/not run, change nothing |
| next | Refuse unless the current task is DONE (gate GREEN + review APPROVED + committed) |
| checkpoint | Full test suite, drift audit, `realitygate selftest --gate "bash scripts/verify.sh"`, `realitygate proof`, then a click-through list for the human |
| ship / prepare release | Phase 6 checklist, every line proven by execution; write `docs/RELEASE-READINESS.md`. Never deploy or publish without approval |
| plan next release | Phase 7: refine R1.x/R2 from feedback and measured usage only after R1 is RELEASE READY. Plan; don't build R2 |

Never mark a task DONE without a green gate, an `[APPROVED]` review and a commit. For the review,
use the `verifier` subagent (`.claude/agents/verifier.md`; in a tool without subagents, run
its instructions in a fresh session), and the `review` skill when a second model family is
available.
Never say "production ready", "deployed", "tested", "secure" or "complete" without evidence:
CODE COMPLETE, RELEASE READY and LIVE DEPLOYED are separate states.

End every run with the report in BUILD-OS Part 7 (requirements verified, verification
actually run, blockers, cost, next action, files changed).
