---
name: yield-to-lesson
description: "Turn the Change items of a retro into checks the next inspection can fail on, instead of resolutions. A change item is accepted only as a lessons-file entry (how it shows up, the check that catches it, where it was first found) plus a benchmark case: a seeded diff and the verdict the inspector must return. Covers rejecting a lesson with no case, the inspector reading the lessons file first, promoting a lesson caught twice to a mechanical check, and reporting catch rate and false alarms per run. Use when a yielder retro lists things to change, a defect class recurs across slices, or an inspector needs a tested memory. Not for writing the retro (yielder), an incident postmortem (postmortem), enforcing a rule mechanically (agent-guardrails), or general agent benchmarks (agent-evaluation)."
allowed-tools: Agent(yielder), Agent(inspector), Read, Write, Edit, Grep, Glob, Bash(git:*)
---

# Yield to lesson

A Yield is finished when every Change item in the retro is either a check the next Inspect can fail on or was rejected with a reason.

A retro that ends in "be more careful about X" changes nothing, because nothing exercises it. The lesson lives in the retro document, the next inspector never reads it, and the defect returns with the same shape. The opposite failure is a lessons file that grows by prose alone: entries nobody can tell are still being caught, so they are either all trusted or all ignored. A lesson earns its place by being paired with a case that proves the inspector catches it, and by having its catch rate measured.

## Scope

Use for: converting `yielder`'s Change list into lessons, deciding whether a lesson is accepted, wiring the lessons file into inspection, and measuring whether inspection still catches what it was taught.

Do not use for: the retro itself (`yielder`), an incident timeline (`postmortem`), turning one rule into a lint, hook or test (`agent-guardrails`), a finding that recurs inside one change's inspect and fix loop (`fresh-inspector-rounds`), or evaluating an agent's task performance in general (`agent-evaluation`).

## What an accepted lesson is

Two artifacts, both required:

- **A lessons-file entry** with four parts: the class (the kind of mistake, named generally enough to recognise in another file), how it shows up (the concrete shape, specific enough to search for), the check that catches it, and where it was first found.
- **A benchmark case**: a seeded diff, the smallest real change that reproduces the defect against today's tree, and the verdict the inspector must return, with the phrases its findings must contain.

Read `references/lesson-entry.md` for the entry shape and what separates a lesson from a resolution. Read `references/benchmark-case.md` for the case format, honest clean changes and how the two scores are computed.

## Workflow

### 1. Sort the Change items

Product changes belong to the next Frame. Process changes are lesson candidates. Drop resolutions to try harder: they cannot fail anything.

### 2. Write the entry

Name the class generally, describe how it showed up in this slice, and name the check that would catch it. If the honest answer is "a person would have to notice", the lesson is not ready.

### 3. Seed the case, and watch it miss first

Build the smallest diff that reproduces the defect and run the inspector on it without the new entry, a fixed number of times (three is enough) on one model and effort. If it already returns `FIX` for the right reason in most of those runs, the lesson is clutter and is not added. Otherwise add the entry and run the same number of times on the same model and effort. Accept the entry only if it catches in most runs and in at least two more runs than the baseline did. Retrying until a run catches measures luck, not the lesson, because the inspector's answers vary.

### 4. Reject at the Yield gate

A lesson with no case is rejected, whatever its quality. The gate is the point: it is the only place the unexercised lesson can be stopped cheaply.

### 5. Wire the file into inspection

The inspector reads the lessons file before its own procedure, so a known class is checked first and not found by luck during the open-ended read. Say so in the inspector's brief or instructions.

### 6. Report two numbers per run

Catch rate is the share of defect cases the inspector flags for the right reason. False alarms are the clean cases it flags anyway. Either number alone misleads: catch rate rewards an inspector that flags everything.

### 7. Promote what is caught twice

A class the inspector catches in two separate slices is cheaper to prevent than to catch. Hand it to `agent-guardrails` to become a lint rule, test or hook, and prune the entry once the mechanical check makes the mistake impossible, naming the check in the commit that prunes it.

## Anti-patterns

**The lesson with no case.** It is memory nobody tests, and the inspector's behaviour on it is unknown.

**The case that no longer applies.** A seeded diff written against an old tree rots. Check it applies before trusting a miss.

**Catch rate alone.** An inspector that flags every diff scores perfectly and ships nothing.

**Restating a gate.** If a linter already fails on it, the entry adds reading cost for no catch.

## References

- `references/lesson-entry.md`: read at step 2 for the four-part entry, a worked example and the resolution test.
- `references/benchmark-case.md`: read at step 3 for the case format, clean changes, and how catch rate and false alarms are counted.
