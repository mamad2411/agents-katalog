---
name: incident-forensics
description: "Agent MUST load when diagnosing a system failure whose evidence is perishable (freeze, crash, OOM, corruption, performance collapse), when the user asks to track or resume an investigation, or before running the first evidence-gathering command of one."
---
--- # workaround: anthropics/claude-code#13003
triggers:
    - read:
        - Skill(llm-kb)
        - Skill(llm-sessions)
        - Skill(llm-subtask)
        - Skill(upstream-reporting)
        - Skill(walled-web)
---

# Incident forensics

An investigation whose findings live only in a chat transcript is lost
at the next compaction, and its evidence is gone from the machine long
before that. This skill trades a few minutes of structure for an
investigation that survives context loss, that a fresh agent can resume
cold, and that pays out upstream.

## Start the kb before the first command

Not after the first finding -- before the first capture, because the
first capture is the one that expires.

> [!@bukzor] ruled 2026-09-23, recorded 2026-09-23, sensatim -- "Incident
> forensics are recorded into ~/.claude/sessions.kb/, as a companion kb
> to the relevant session entry."

The skeleton is never free-standing at some ad hoc path; it nests inside
the sessions.kb entry this investigation belongs to (`Skill(llm-sessions)`).
Find or start that entry first -- `~/.claude/sessions.kb/$(hostname
-s).kb/SESSION-SLUG.md`, from `.template.md` if none exists yet -- then
copy the skeleton into its companion kb, one subdirectory per incident:

```bash
H=$(hostname -s)
cp -r ~/.claude/skills/incident-forensics/skeleton/. \
  ~/.claude/sessions.kb/$H.kb/SESSION-SLUG.kb/SUBJECT-YYYY-MM-DD/
```

Directory name: `SUBJECT-YYYY-MM-DD` (the incident date, not today's).
Then fill the root `CLAUDE.md` incident paragraph, point the session
entry's `## Addenda` at the new directory, and start capturing. Worked
example: `pnpm-11-tooling-and-cron-health.kb/pnpm-corepack-cjs-mjs-2026-09-12/`
in `~/.claude/sessions.kb/penguin.kb/`. The eight collections and their
boundaries are documented in the skeleton's own `CLAUDE.md` files -- read
those, not this list:

| collection        | holds                                        |
| ----------------- | -------------------------------------------- |
| `evidence.kb/`    | raw output, append-only, one capture per file |
| `timeline.kb/`    | dated events with source and confidence       |
| `findings.kb/`    | evidence-backed conclusions, status-tracked   |
| `root-cause.kb/`  | competing explanations; `root-cause.md` decides |
| `environment.kb/` | static machine context                        |
| `remediations.kb/`| prevention and recovery measures              |
| `reports.kb/`     | outbound upstream contributions               |
| `todo.kb/`        | open actions                                  |

## Triage by perishability, not by suspicion

Order the first captures by how fast the source disappears, ignoring
which one you think will pay off:

1. ring buffers and in-memory state (`dmesg`, process listings, mounts,
   `/proc/pressure`, current cgroup counters)
2. anything a reboot or a service restart destroys
3. logs subject to rotation or vacuuming (journals, app logs, host-side
   logs on a machine you reach only through the user)
4. package versions, configs, and anything else the filesystem will
   still hold next week

Every capture gets its method recorded as a sibling script, so file both
in one step:

```bash
~/.claude/skills/incident-forensics/bin/incident-forensics-capture \
  --title 'Journal, previous boot' \
  -- journalctl -b -1 --no-pager        # pipelines: -- bash -c '...'
```

That writes `evidence.kb/DATE-NNN-slug.md` (frontmatter, fenced output,
exit status) beside the `.sh` that produced it. The capture is
append-only; the method script may be improved in place. Never edit a
capture to match a conclusion.

## Separate what happened from what it means

The discipline that makes the kb worth having:

- A **timeline event** carries `at`, `source`, and `confidence:
  observed|inferred`. Never launder an inferred time into an observed
  one; the difference is what lets a later reader re-open the question.
- A **finding** is one claim with `status` and pointers to the evidence
  that supports it. Refuted findings keep their file and say what
  refuted them -- the dead ends are half the value on resume.
- **Root causes compete.** One file per candidate, at most one
  `leading`, and `root-cause.md` states the current answer. Close it by
  rewriting that file, keeping the losers as the record of why.

Watch for the systemic version of the finding. The proximate trigger and
the reason a safeguard didn't fire are different findings, and the
second one is usually the one worth reporting.

## When the data is behind a wall

Some of the truth lives where you cannot reach: another VM, the host OS,
a vendor console, a browser-only page. Do not narrate the difficulty --
hand the user an exact command and an exact destination path, one step
at a time, and file a todo for the datum so a resumed session knows it's
still missing. Browser walls specifically: `Skill(walled-web)`.

## Close the loop in both directions

An investigation ends with two mechanisms running, not with an
explanation:

- **Localhost:** remediations with an adoption `status`, and monitoring
  that would catch a recurrence. Verify the monitor actually runs after
  installing it -- a crashed watchdog is worse than none, because it
  buys false confidence. Record what monitoring now exists in
  `environment.kb/`, since that's what the next incident starts from.
- **Upstream:** if any finding is a bug in someone else's code, it gets
  reported. `Skill(upstream-reporting)` covers dupe-search, paste
  hygiene, and reply-watching.

## The cold-start test

Before you consider the kb done, ask what a fresh agent given only this
directory could say. It should be able to state what happened, what is
known versus suspected, what was ruled out, what changed on the machine,
and what to do next -- without the transcript. Anything it couldn't say
is a file you still owe.
