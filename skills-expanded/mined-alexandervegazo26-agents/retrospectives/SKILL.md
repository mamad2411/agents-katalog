---
name: retrospectives
version: 1.1.0
description: Running a retrospective that produces real, tracked changes in behavior — structure, psychological safety, and turning takeaways into lessons-learned rather than a document that's filed and forgotten. Load at the end of a project phase, release, or incident cycle.
---

# Retrospectives

## The point is behavior change, not the meeting

A retrospective that produces a document no one revisits is theater. Its only real output is whether the next cycle of work is different because of what was found here.

## Structure

What went well (keep doing), what didn't (stop/change), what's still unclear (investigate) — timeline-based and factual where possible, same discipline as `root-cause-analysis`'s blameless framing: the question is what about the process/system produced this outcome, not who's at fault.

## Psychological safety

People only surface the real, uncomfortable findings (a shortcut that almost caused an incident, a process everyone privately routes around) if raising them doesn't create blame. Model blameless framing explicitly when facilitating.

## Turning takeaways into lessons learned

Every actionable takeaway needs an owner and a tracked follow-up, same as an incident action item — an insight with no owner decays back into "yeah, we all kind of know that" within a month. Persist genuinely durable lessons to `.claude/memory/<project>/lessons-learned.md`, cross-referenced with the source event (release, incident, project phase).

## Look for the faster way, from evidence

A retrospective asks what went wrong; it should also ask what was slow or wasted.
When the work ran through the suite's workflows, that question has a measured
answer: invoke `Skill(improve)` (the command resolves the plugin's
path; a `${CLAUDE_PLUGIN_ROOT}` written in this skill would not expand). It reads the recorded runs
and proposes a concrete change for each recurring waste signal — a phase that
dominates wall-clock, an agent that needs its retry every run, a repair loop that
exhausts both rounds, a gate that repeatedly blocks waiting for a person. Treat each
as a takeaway: an owner, a decision, a follow-up.

The same applies to steps a *person* keeps repeating by hand. If the same
sequence of actions appears in two or more cycles, propose it as a skill or a
tool with its trigger and a required report line — a procedure that exists only
in someone's habit is a procedure the next agent will not follow.

A faster way is never less checking. A proposal that would skip a lens, lower a
review's effort or drop a verification is rejected on sight; speed comes from
removing repeated dispatches, dead rounds and serial waits.

## Closing the loop

Check at the start of the next retrospective whether previous action items were actually completed — a retrospective process that never checks its own follow-through will quietly stop producing real change even while continuing to feel productive.
