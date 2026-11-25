---
name: squad-handoff
description: Before signing off — whether you finished an item or stopped mid-flight — post a 3-bullet summary. Shipped, in flight / queued, surprised by. Three bullets, no ceremony.
allowed-tools:
  - Bash
paths:
  - ".squad/**"
disable-model-invocation: false
---

# End-of-session handoff

Every session ends with a 3-bullet brief. The point is to give the next session a one-paragraph cold-start, not a status report. Three bullets, no ceremony.

## When to use this skill

Invoke this skill at the end of every session: when you finish an item, when you pause mid-item for the day, when you hand off to a coworker, or when the user says "wrap up." Also invoke when you are about to run `squad release` or `/handoff`.

## The three bullets

1. **Shipped:** items closed in this session, by ID + one-line outcome. If nothing closed, say "nothing closed."
2. **In flight / queued:** what is `in_progress` or `review` and where it stands. If clear, say "queue clear."
3. **Surprised by:** anything the next session should know that is not in an item file or commit message — a non-obvious gotcha, a surprising perf number, a tool quirk, a customer signal that came in. Skip this bullet entirely if genuinely nothing.

## Mid-flight pause

If you are pausing on an in-progress item, also:

- Leave the item `status: in_progress`.
- Add a `## Session log` section to the item file at the bottom (above `## Resolution`):

```markdown
## Session log
### YYYY-MM-DD
- What I did
- What is left
- Any gotchas / dead-ends to avoid
- Next concrete step
```

- If you have changed code that is not yet tested or committed, leave a note in `STATUS.md` under "In Progress" with `(uncommitted on branch X)`.
- Post `squad say "end of session, picking up <next step> tomorrow"` so peers see the pause.

## True handoff to another agent

If you are truly handing off (not pausing yourself): `squad release <ID> --outcome released` and name the next concrete step in the chat message. The releasing agent owes the next agent a clean starting point, not just a frozen state.

## Capture surprises as learnings

If your "surprised by" bullet is a real gotcha — not a status note — pass `--propose-from-surprises` to the handoff. The command auto-drafts one proposed gotcha-kind learning per surprise (or per `stuck` / surprise-keyword `fyi` post mined from chat history when no explicit `--surprised-by` flags are given). Each stub lands under `.squad/learnings/gotchas/proposed/` with the surprise body pre-filled in `## Looks like`; flesh out `## Is` and `## So` later, or `squad learning reject` ones that don't merit a write-up. Use `--dry-run` to preview, `--max N` to cap volume.

```bash
squad handoff --note "EOD" --propose-from-surprises --dry-run
squad handoff --surprised-by "X" --surprised-by "Y" --propose-from-surprises
```

Don't reach for this on every handoff — only when the surprises bullet has content worth writing up.

## Why this matters

Sessions are not continuous; agents come and go; coworkers pick up where others left off. The handoff is the seam. A bad handoff costs the next session 30+ minutes of reconstruction; a good handoff costs them 30 seconds. The 3-bullet brief is the minimum content that produces a good handoff — less, and the next session re-discovers; more, and the bullets get skimmed.

## How to apply

1. Compose the three bullets in your head. Cut the third if there is genuinely nothing to flag.
2. Post the brief to chat (the conversation, or via `squad say`).
3. If pausing mid-item: write the `## Session log` entry in the item file.
4. If true handoff: `squad release <ID> --outcome released` with the next-step message.
5. Sign off.

## Anti-patterns to avoid

- Skipping the handoff because "I will be back later." Sessions end; later you will not remember the state. Write the handoff.
- Writing five bullets instead of three. Bullets four and five get skimmed.
- Padding the "surprised by" bullet with content the commits already cover. The bullet exists for what the commits do NOT say.
- Leaving an in-progress item with no `## Session log` entry. The next session has no breadcrumb.
- Releasing a claim because you went to lunch. Heartbeat handles absence; release only on true handoff or done.

## After every handoff

Surprise bullets are write-only by default — they land in chat and scroll out of context within a session. Convert each one into a learning artifact so the next session inherits it. The pre-filled `--body` flag means there is no retyping cost:

```bash
squad learning quick --body "the surprise text verbatim" "<short slug-shaped one-liner>"
```

If a surprise genuinely is not worth a learning artifact (it was a status note, not a gotcha), say so explicitly in the same handoff post — `not filed: <one-line reason>`. The mandate is per-bullet: for each surprise bullet, file via `squad learning quick` or explain why not.
