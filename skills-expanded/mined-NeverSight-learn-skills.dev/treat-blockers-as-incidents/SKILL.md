---
name: treat-blockers-as-incidents
description: >-
  Use when a command fails for a reason that is not the change you were asked to
  make: a tool that will not install, a runtime the shell cannot find, an
  authentication that expires mid-task, a permission, a registry, a proxy, a
  container that will not start. Covers noticing you are in one, bounding the
  investigation before it eats the session, probing without guessing, reading the
  tool's own source and its primary documentation, and recording what was learned
  so the next person does not pay again. A workaround that needs contortions is a
  finding, not a fix. Not for a failure in the code you are changing, and not for
  a test that fails because the behaviour is missing.
---

# Treat Blockers as Incidents

**Core principle.** The stone in your shoe is not the walk. It is an incident with a cause, a cost, and a record.

- **The failure is about your task, or it is not.** That single question routes everything below.
- **The weight sits in *Bound it before you start* and *What you may claim*.** Everything else spends what those two allow.
- **You opened this in the middle of something.** This is how to get back to that work, not a replacement for it. Name what you were doing before you start, and return to it when this is done.

## Is this yours

**Answer before touching anything.**

- **A test failing because the behaviour is missing is your task.** That is `test-first-by-evidence`.
- **A defect in the code you are changing is your task.** That is `debugging-by-evidence`.
- **A tool, runtime, credential, network path, or environment that will not do its job is not your task.** It is this.
- **Where you cannot tell, run the same command in a directory the task does not touch.** Still broken means it is not yours.

## Bound it before you start

**Say the budget out loud, in the report, before the first probe.**

- **Name the ceiling.** A number of probes, or a wall-clock span. Without one, "understand it up to a point" has no point.
- **Say what reaching the ceiling means.** Hand back what you have, incomplete, rather than continue.
- **Investigate in a session that is not this one** where the harness allows it. Context spent here is context the original task no longer has.
- **Record as you go, not at the end.** An investigation that runs out of room produces nothing, and it was the one with the most to teach.

## Say which state you are in

**Report it every time.** Each state licenses only what it names.

| State | Means | Licenses |
| --- | --- | --- |
| `BLOCKED` | a command failed for a reason that is not the task | one reproduction, and reading |
| `CHARACTERISED` | the failure reproduces and its trigger is named | probes, documentation, source |
| `EXPLAINED` | the mechanism is observed, not inferred | proposing a fix |
| `CLEARED` | the fix is applied and the original command runs | returning to the task |
| `HANDED BACK` | the ceiling was reached, or the fix is not trivial | nothing further without a decision |

- **No state is reached by assumption.** Each names an observation you made.
- **`CLEARED` requires the original command to run**, not a substitute you found instead.

## Which rules to read

**This table is a gate, not a checklist.** Match the left column against what failed.

- **Read every row whose signal is present.** Report an absent one as not-applicable, naming the signal.
- **A blocker that hides a second blocker matches two rows.** Read both.

| If you see... | Read |
| --- | --- |
| **a workaround forming**: a flag nobody documents, a copied file, a pinned version chosen to make an error go away | `rules/workarounds-are-findings.md` |
| **the same command failing again**, or a fix that made the error move rather than go | `rules/stop-conditions.md` |
| **a non-zero exit from a command that does several things**, or an unrelated tool named in the output | `rules/whose-failure-is-it.md` |
| **the first blocker cleared** and something new failing right behind it | `rules/the-second-blocker.md` |
| **anything about to be deleted, reset, reinstalled, or rotated** to make a command pass | `rules/never-destroy-to-proceed.md` |
| **enough understood to be worth keeping**, or a ceiling reached | `rules/record-the-learning.md` |

**Default stance.**

- **Reproduce once, name the trigger, then stop and decide** whether this is worth a bounded investigation or a handback now.
- **Prefer the primary source over another attempt.** The tool's own documentation and its source answer what a fifth retry will not.
- **Hand back anything whose fix is not obviously clean.** The decision is the developer's, and an unclean fix bought quietly is worse than a blocker reported loudly.

## What you may claim

**Four words, and each one names how you know.**

- **Confirmed.** Observed directly, with the command and its output quoted.
- **Inference.** Reasoned from something Confirmed, and labelled so.
- **Gap.** Not established. State the next concrete observation that would close it.
- **Recommendation.** Never proof.

- **A workaround is a Recommendation until the mechanism is Confirmed.** Reporting it as a fix is the failure this skill exists to prevent.
- **Never claim a command succeeded unless its output was observed.**

## Where the record goes

- **Use the location the request named**, if it named one.
- **Otherwise the one the instruction file declares.**
- **Otherwise a learnings directory that already exists**, in this repository or in the user's agent directory. Writing beside an existing one beats starting a second.
- **Otherwise decide from the finding.** A blocker anyone cloning this repository would hit is written inside it; one only this machine has is written to a learnings directory beside the user's own instruction file, outside any repository.
- **Where you cannot tell, write outside the repository.** A note in the wrong home directory is invisible to everyone; a note committed uninvited is not.
- **Report the path you chose and whether it is tracked.** A wrong guess then costs one line to correct.

## Do not skip this when

- **The workaround already worked.** It worked once, on your machine, for reasons nobody wrote down.
- **The blocker looks trivial.** The ones that eat an afternoon all looked trivial at the first attempt.
- **You are nearly done.** Nearly done is where the second blocker lives.

## Routing

- **The table above selects the rule.** Read a selected rule in full, and say which one you opened.
- **A defect in the code under change belongs to `debugging-by-evidence`.**
- **Judging a change that already exists belongs to `evidence-backed-review`.**
- **A direct instruction from the user outranks anything here.**
