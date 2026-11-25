---
name: cycle
description: Run one development cycle of four tasks picked from the project's work graph — two core tasks, one mechanization task, one legacy audit — each with an impact table before writing, a mutation pass, bounded adversarial review, and a convergence report at the end. Use when asked to "run a cycle", "phase run", "advance the roadmap", to work through the backlog autonomously, or to run one named node or fix alone.
---

# Cycle — four tasks, measured

No `.ennyn/` yet: run `/ennyn:init` first. Project settings come from `.ennyn/config.json` (`language`: the language of every report and commit message you write). `node "${CLAUDE_PLUGIN_ROOT}/scripts/ennyn.mjs" --help` lists the commands used below.

A node or fix asked for alone: [one-task.md](one-task.md).

## 1. Pick the four tasks

Read in one turn, once `ennyn.mjs doctor` shows no ✗ (else stop: say why): the config, the handoff (`paths.handoff`; unset → `HANDOFF.md`) and the graph. The handoff names the commands later steps run (fast test, whole test, lint, typecheck, the mutation tool; `commands.fastTest` comes first; one neither names → `ennyn.mjs init-scan --json`), the last cycle's next step and open risks. `ennyn.mjs leftovers --start` notes HEAD: `bypass` starts there.

| Slot | Source | Rule |
|---|---|---|
| Core ×2 | `ennyn.mjs core` | One takes its oldest pick; when it says split, first write its first step as a node it `needs`, rerun, take the step. The other is one it lists by score; prefer nodes sharing a `cluster`. Verifiable, user-visible value. |
| Mechanization ×1 | `ennyn.mjs mechanization` | A node with `mechanization: true`: turn a recurring defect class into a gate, test, type or lint, then delete the matching prose rule. None ready → the slot becomes a third core task. A graph it or `core` refuses (exit 1, reasons on stderr) is fixed first. |
| Legacy audit ×1 | `ennyn.mjs audit`: the security audit unless it answers not due; else the audit queue (oldest / never audited / hit by a shared change) | Security audit: every path it lists, with a path table (every way to reach what each protects). Else re-check a feature: invalid/empty/max input, permission denied, network failure, repeated action, refresh, stale data, then [lean items](lean-audit.md). Findings: [finding-schema.md](finding-schema.md), Outcome. |

A critical problem (crash, data loss, auth break, blocker) may replace one core slot. Write the plan as [report-formats.md](report-formats.md) shows. Do not wait for approval between tasks; push only on the user's yes in the same exchange.

## 2. Task protocol (every task, in order)

The orchestrator (the cycle's session) keeps the plan, step 7's verdicts and the landing. Each task runs in a fresh agent on a written brief, not a fork. Briefs, worktrees, no subagents: [task-brief.md](task-brief.md); task states: [journal.md](journal.md).

1. **Read** only the relevant files, independent reads in the **same turn**.
2. **Design brief** for UI work: [design-brief.md](design-brief.md).
3. **[Impact table](impact-table.md)** before the first edit: a core task's smallest-change row, always; the five rows only when the change touches a shared decision, predicate, gate or accept/reject rule: `ennyn.mjs impact --symbol <name> --files <paths>`. Each row is answered by a command's output, never by recall. Heuristic rules, dictionaries, thresholds: an accept **and** reject corpus and a failing test first.
4. **Implement**, matching existing patterns.
5. **Test:** a new test alone first, its control seen failing once; then the fast test (`none`: no new test, fast test or step 6; say why), lint and typecheck.
6. **Mutation pass** on changed gate or decision code (it accepts, refuses, selects, counts or deletes; a text-only task has none, and says so) with the handoff's mutation tool; with none (or "not applicable"), hand-pick mutants of the changed lines, run with `ennyn.mjs mutate <list.json> --command "<fast test>"`, with `--check "<parse command> {file}"` for files not JavaScript or JSON. Record the first-run result (`killed/total`); write a test for each survivor or justify it as equivalent.
7. **Review**, once its restatement holds (task-brief.md), with the reviewers that match the change: `review.agents` when set, else Ennyn's (correctness, security, data correctness). Give them the task's node, the changed files, the impact table and [finding-schema.md](finding-schema.md). **Two rounds**; after them a failing test or the gate rerun, never another reader. For security work the path table replaces the round limit: list every way to reach the protected state first.
8. **A fix is a new write:** a row it changes is updated, and round two gets the delta.
9. **Record findings** as you write them: [ledger-row.md](ledger-row.md), class and source per [finding-schema.md](finding-schema.md), and its Outcome.
10. **Sweep** the same pattern project-wide; update the documents the change affects.
11. **Commit** one task per commit, in Ennyn's convention: it replaces any commit rule in the project's instructions. Subject `type(scope): text` with a type from `commitMsg.types` when they are set; a repair of an earlier commit uses `commitMsg.fixType` and nothing else does. Text in `commitMsg.language` (else `language`). With `commitMsg.style: terse` the body holds no prose, only the lines below. Detail goes to the graph node. Body lines: `Impact: …` · `Review-Rounds: N` · `Mutation: first a/b · last c/d`. Loosening a gate: ask the user; `User-Approved-Loosening: <key>` only on their plain yes for that key; a task agent stops and reports the keys.

Never report an unrun test, command or check as done: write `not applicable`. A task sent back, restarted or stopped: task-brief.md, The failure count.

## 3. End of cycle

1. **Graph:** update every node whose status changed; every leftover real defect but a declined one, every ask of the user, and each brief rule [`### Briefs`](report-formats.md) sends to a node, becomes a node, as do step 3's class and a core split's step (nothing else does), at the end of the list, dated (`graph.fields.since`).
   Verdicts on proposed nodes first; an ask's `source` (`the user, <date>: …`), memory notes: report-formats.md.
2. **Handoff** (`paths.handoff`): what was done, what is next, open risks, each with a permanent home (a file that never rotates). Its commands stay for the next cycle.
3. **Convergence:** first append each kept rows file to `paths.findings`. Each `new:` class joins the registry or links to an entry, per [report-formats.md](report-formats.md). Run `ennyn.mjs convergence --cycle <N> --from <HEAD noted at the start>`; paste what it prints, unchanged. The most recurring class becomes a graph node with `mechanization: true` and its class id; none: say why. A file whose fixes keep bringing findings gets the fix-loop brake ([report-formats.md](report-formats.md)), not patch nodes.
   Show the user what `ennyn.mjs bypass --from <that HEAD>` lists. One that recurs is a gate to fix, not a habit.
4. **Retire lessons:** in one lesson file touched this cycle, mark each lesson keep/update/merge/delete; delete the prose of any lesson whose rationale now lives in a test or gate.
5. **Security checks:** `ennyn.mjs deps`, doctor's CI line (none: no CI file), and after step 6's commit `ennyn.mjs leftovers` and the handoff's leftover command (none: unmeasured); each is reported as found, clean or unmeasured (naming what did not run), never clean by default. A finding is fixed now or becomes a graph node.
6. **Budget:** after the cycle's last edit, `ennyn.mjs budget --record`; add `--security-audit` only when this cycle's audit was the security audit. Commit the metrics log with the graph and the handoff. Text loaded every session that grew needs a reason in the report. A repeated rule keeps one copy, in the narrowest file that loads where it is needed.
7. **Push:** `ennyn.mjs worktrees --remove`; `ennyn.mjs test whole`, once (red: task-brief.md's Landing row); `ennyn.mjs push-check`; [handover.md](handover.md); under `ask` the closing ends first, the push question its last words ([push.md](push.md)).
