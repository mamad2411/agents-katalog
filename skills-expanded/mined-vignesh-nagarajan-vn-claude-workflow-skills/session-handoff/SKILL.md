---
name: session-handoff
description: Write or read a HANDOFF.md so a new session starts from a short state summary instead of re-exploring the repo. Use when wrapping up, when the user says handoff, pause, stop here, or continue later, when context is running out mid-task, and at the start of a session in a repo that already has a HANDOFF.md.
---

# session-handoff

A cold session spends its first few thousand tokens rediscovering what the last one knew. A handoff file replaces that with a page of text.

## Reading one

If `HANDOFF.md` exists at the repo root, read it before exploring anything. Then open only the files its "Read these first" section names. Do not re-derive the architecture, the handoff already did.

Check the date at the top. If it is older than the last commit, treat it as a lead rather than the truth, and say so instead of acting on a stale claim.

## Writing one

Gather the mechanical facts with the script, so you are not spending tokens on `git log` output you have to parse yourself:

```bash
python <skill>/scripts/handoff_context.py
```

That prints the branch, the head SHA, uncommitted file count, commits since the last handoff, and the files touched. Paste those facts into the template and write the parts only you know.

The template is at `<skill>/assets/HANDOFF.template.md`.

## What actually earns its place

The script covers what git can answer. Your job is the four things git cannot:

**Where things stand.** One paragraph. What is working now that was not before, in plain terms.

**In flight.** The single highest-value section. What is half-finished, which file it is in, and what the next edit is. Be specific enough that the next session does not have to diff to find out.

**Next.** A short ordered list. First item should be startable without any further reading.

**Gotchas.** Anything that cost time and would cost it again: a failing test that is expected to fail, a service that needs to be running, an approach already tried and rejected and why.

## What to leave out

Do not restate the architecture, that belongs in `CLAUDE.md`. Do not list every file changed, the script already has it and the diff is authoritative. Do not summarize the conversation. A handoff over about 60 lines has stopped being cheaper than exploring.

## Housekeeping

Overwrite the existing `HANDOFF.md` rather than appending. It is a snapshot, not a log.

Whether it gets committed depends on the repo. If the repo already tracks handoff files, commit it. Otherwise leave it untracked and mention that to the user.

Prose follows [prose-guard's rules](../prose-guard/references/rules.md), which matters here because handoffs invite hedging. Write what is true, not what might be.
