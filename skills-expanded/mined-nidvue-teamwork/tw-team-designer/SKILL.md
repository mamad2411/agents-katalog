---
name: tw-team-designer
description: "designing or auditing a team: interview, smallest roster, skills, least privilege, verification, proactivity and routines before work starts"
---

# tw-team-designer

Owner role: **ceo** (created by CEO on 2026-11-02).

Use this skill when: designing or auditing a team: interview, smallest roster, skills, least privilege, verification, proactivity and routines before work starts

## Why this exists

This flow is repetitive, widely reused and must stay consistent across every
ceo instance. Extracted once so it is executed the same way every time.

## Steps

1. **Read the state before you ask anything.** `AGENTS.md`, the role charters,
   `teamwork.py board`, `teamwork.py audit`, `teamwork.py skill candidates`,
   `teamwork.py harness budget`, `teamwork.py parallel`. You are auditing a team,
   not a blank page: an existing seat, skill or routine that already does the job
   is kept, not renamed.

2. **Interview in one batch, then restate.** Ask the user (or the CEO brief) these
   ten questions, one message, no follow-up drip:

   1. What ships, and who uses it?
   2. What are the five acceptance criteria, and who verifies each one?
   3. What is the budget (tokens, wall clock, people) and the deadline?
   4. Which tools, repositories, connectors and credentials does the work actually
      touch?
   5. Which of those are read-only, which write, and which are external or
      irreversible?
   6. What is repetitive today, and where does a fact get copied by hand?
   7. Which periodic checks or routines already exist, and what do they cost?
   8. What has failed before, and what would make the user reject the result?
   9. What is explicitly out of scope?
   10. Who is allowed to say "done"?

   Then **restate the goal, the acceptance criteria and the non-goals in your own
   words** and ask for a yes/no before designing. A restatement that changes the
   scope is a requirement change, not a misunderstanding: resolve it before any
   seat is proposed.

3. **Audit the roster against the smallest-team rule.** Build one table with a row
   per seat: `role | deliverable it uniquely owns | test layer it owns | decision
   right no other role holds | verdict`. A seat with no unique deliverable, layer
   or right is a **lane**, not a role: drop it, merge it into an existing role, or
   record why it must exist. Check the four invariants: one parent per role, one
   neutral reviewer seat (no party rules its own dispute), a test-layer owner per
   layer that is actually required, and the shared services (Architect, Project
   Manager) printed once, never per team. The target is the smallest team that can
   reliably ship, not the largest one the budget allows.

4. **Audit the skills.** Run `teamwork.py skill candidates`; for every repeated
   flow, name the existing skill that covers it or create one in the same task.
   A method that lives only in the conversation is a defect: long context is not a
   storage medium. Check each skill names when to use it, the exact commands, the
   evidence it records and the guardrails it may not bypass. No skill may replace
   `AGENTS.md`, a red line or a gate.

5. **Audit permissions and verification together.** For every seat, write the
   least privilege it needs: paths it may write, tools/connectors it may call, and
   whether the action is external or irreversible. Then write the proof: the
   verifier (a role other than the author) and the command or artifact that
   demonstrates the deliverable. Reject "give every bot every tool", a
   self-verified deliverable, and a bot with its own email or external account.
   A deliverable with no verifier is not designed yet.

6. **Audit proactivity and routines.** Read `attention list` and the pulse report.
   For every routine: the trigger, the budget (tokens/time) and the stop
   condition. A heavy routine gets its own lane; the main context is not a
   scheduler. An idle lane proposes one automation or risk it can remove, and the
   proposal is recorded (`attention add` or a task with `--mandate inferred
   --basis`), never executed as silent autonomy.

7. **Write the one-page design, not a new bot.** The output is a table of
   `adopt | adapt | reject` rows with the concrete surface for each (a skill, a
   task, a settings key, a test), the smallest roster, the permission/verification
   matrix, and the routine list. Every adoption gets an owner, a task id and a
   falsifier (what measurement would show it failed). A seat is created only when
   step 3 proves it; the default answer to "add a role" is a lane, a skill or a
   routine instead.

8. **Hand the design back with a restatement.** End with the goal, the acceptance
   criteria, the roster delta and the first three tasks in the user's words
   (restate again, briefly), and ask for confirmation. Then record the decisions
   (`decision add` with evidence), create the tasks and let the normal loop run.
   The designer does not become a permanent role: it is a skill the CEO loads when
   the team is designed or audited.

**Anti-patterns to name in the report:** many bots with overlapping jobs; every
tool granted to every seat; a skill that is only a prompt; a human relay kept as
the workflow; a schedule with no budget or stop condition; a self-verified
deliverable; a new role created because the model is cheap.

**Falsifiers.** After ten designs, the roster should not grow and the first-pass
review rate should not fall; the no-relay rule should produce at least one
automation task; the routine rule should reduce `harness budget` on the lanes that
moved routines out. If none moves, the design is ceremony and must be revised.

## Evidence

Every run records command + revision + observed result, as the team requires.

## Guardrails

- This skill does not replace `AGENTS.md`, the red lines, or the quality gates.
  If it conflicts with them, they win and this file must be fixed.
- It never bypasses: self-check, independent review, the PR, or the Reviewer-only
  merge. It may not weaken or skip a test layer.
- Changing this skill is normal work: branch, commit with the fixed message style,
  PR, review, merge. Never edit it on `main`.

## Verdict on this skill

verdict: no observed effect

- **What was compared:** one team audit done ad hoc against the same audit run
  through the eight steps above, on the live team during the 2026-11-02 project
  review.
- **On which task and revision:** T-0052 at `4c9410a`, the commit that adds this
  section; the team state audited was `6770f26` plus that review's own queue
  changes.
- **What the run produced, with the command that shows it:** `harness budget`
  exposed a measurement defect - the always-on sum counted `LongTermMemory.md`,
  which `AGENTS.md` says is never loaded: 133160 bytes against a 122880 cap, and
  113610 without it. A shared skill without a verdict row passed CI because the
  EVIDENCE rule reads the gitignored registry. `skill candidates` listed seven
  areas with at least three finished tasks. The review's findings became T-0005
  to T-0007, T-0030 and T-0031.
- **Why this label and not `helped`:** one audit cannot show a change in roster
  size, first-pass review rate or routine cost, and that same review raised five
  findings against the change that carried this skill. The falsifiers above are
  measured over ten designs. `confounded` is not used: it is one run compared with
  one ad hoc pass, with no separate review of the two.
