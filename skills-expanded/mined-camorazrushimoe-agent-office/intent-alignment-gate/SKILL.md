---
name: intent-alignment-gate
description: "Scrum Master's intent gate — before a team starts a ticket or a series, verify the planned work still serves the goal the customer actually stated. Reconstructs the intent chain (intake → breakdown → tickets), returns ALIGNED / DRIFTED / UNCLEAR, and has authority to STOP work and escalate to the customer. Use when an agent asks 'is this work aligned', 'gate check', 'сверка с целями', 'можно брать в работу', 'проверь соответствие', or before any team moves a Linear ticket to In Progress."
version: 1.0.0
author: local
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [agent-office, scrum-master, foundation, intent, gate, escalation, linear]
prerequisites:
  commands: [python3]
---

# Intent Alignment Gate

**The problem this exists for:** a task changes shape as it passes through hands. The human states a goal → it gets routed → broken into tickets → an agent picks one up. By the time work starts, what is being built can quietly stop being what was asked for. Each step is locally reasonable; the drift is only visible end to end.

**Nobody else sees the whole chain.** The team sees its ticket. The human sees the original ask. Only Scrum Master sits at both ends. So the gate is Scrum Master's job.

**Your authority here is real:** you may **stop work** and escalate. An idle factory costs less than a factory building the wrong thing.

## When you are called

- An agent asks before pulling a ticket (or a series) into `In Progress` — this is mandatory under OFFICE-STANDARD golden rule 11
- You are routing new work to a team
- A ticket has been sitting while its context changed
- Anything about a plan smells like it grew a life of its own

Gate a **series** where you can, not every ticket. One check for `BON-35..39` beats five checks. The gate must cost minutes, or teams will start routing around it.

## Procedure

### 1. Reconstruct the intent chain

Get all four levels. If you cannot find one, that is itself a finding.

| Level | Where to look |
|-------|---------------|
| **Stated goal** — what the customer said they want, and *why* | the original intake message, the commission/spec doc, `project.created` events on the bus |
| **Routing decision** — what you or Office decided to do about it | `project.assigned` events, your own portfolio memory |
| **Breakdown** — the tickets as written | Linear project + issues |
| **Planned execution** — what the team is actually about to do | the team's own comments, plan, or PR |

```bash
# bus history for this project
python3 /opt/crew/office-log.py --count 50 --project "<project>"
```

One-shot mode, talks TCP to `OFFICE_BUS_URL` — no docker needed. `--project` and `--team` filters exist; your container has `OFFICE_BUS_URL=redis://shared-memory:6379` set.

### 2. Ask the four questions

For the ticket or series in front of you:

1. **What business outcome does this serve?** Name it in one sentence, in the customer's own terms. If you have to invent the sentence, that is drift.
2. **Would the customer recognise this as what they asked for?** Not "is it defensible" — would *they* say yes.
3. **What is the cheapest thing that would satisfy the actual goal?** If the plan is much bigger than that, ask why.
4. **What would make this not worth doing at all?** If nothing could, you have not understood the goal well enough to gate it.

### 3. Look for the known drift patterns

- **Scope inflation** — tickets cover more than the intake asked for, each addition individually sensible
- **Proxy substitution** — the team is measuring something adjacent because the real thing is hard
- **Means became the end** — building the tool instead of answering the question
- **Stale premise** — the intake's assumption has since been disproved (often by our own earlier findings)
- **Inherited assumption** — a decision made in an earlier hand, now treated as a requirement nobody can source
- **Unbounded exploration** — plenty of activity, no stated finish line
- **Orphan work** — a ticket nobody can trace back to any stated goal

### 4. Return a verdict

**ALIGNED** — work serves the stated goal. Say which goal, in one line. Release the team.

**DRIFTED, fix is obvious** — name the drift, state the correction, adjust the tickets, release. Log it; do not silently rewrite.

**DRIFTED, fix is not obvious** — **STOP. Escalate.** Do not let the team start "while we clarify".

**UNCLEAR — you cannot tell whether this should be done at all** — **STOP. Escalate.** This is the case the gate exists for. Guessing here is the expensive failure.

Never return ALIGNED just because the work is well-formed. A well-planned answer to the wrong question is the exact thing you are here to catch.

## Stopping and escalating

When you stop work:

1. Move affected tickets to `Blocked` and comment why, with a link to the escalation
2. Tell the team explicitly: **stop, do not start, wait**
3. Publish to the bus so the stop is not silent:

   ```bash
   python3 /opt/crew/publish-event.py work.gate.blocked scrum-master \
     "BON-35..39 blocked: cannot establish that Phase 0 serves the stated goal" \
     --target lab-1 --project "<project>"
   ```

4. Escalate to the customer with this shape — questions, not a complaint:

```
GATE: STOPPED — <ticket or series>

WHAT WE WERE ABOUT TO DO
  one paragraph, plainly

THE GOAL AS WE UNDERSTAND IT
  quote or cite the intake

WHY WE CANNOT CONNECT THEM
  the specific gap, not a vague worry

WHAT WE NEED FROM YOU
  1-3 concrete questions, each answerable in a sentence

WHAT WE RECOMMEND
  your best guess, so a yes/no unblocks us

MEANWHILE
  what is paused, and what (if anything) safely continues
```

Then **wait**. Do not iterate on the plan while blocked — that is how a stop turns into a loop. And a stop must never be a parking lot.

**Timeouts and unblock path.** If the customer has not answered within **24 hours** (default window), re-escalate to the **human operator** with the same shape — recommendation plus an explicit "proceed or cancel" question — and publish `work.gate.escalated` so the wait is auditable. You also gate **your own Office tickets**: record the verdict on the ticket/PR and publish `work.gate.passed`; the guardrails (bias to release, no double-gating) apply with full force.

Ask for the goal in business terms, never for a technical spec. "What decision will this let you make?" and "what would make this a waste of money?" are the two questions that recover intent fastest.

## Passing the gate

```bash
python3 /opt/crew/publish-event.py work.gate.passed scrum-master \
  "BON-35..39 aligned: verifies the corpora before research spend; serves 'do we have usable data'" \
  --target lab-1 --project "<project>"
```

Record in the ticket or thread: **the goal it serves**, in one line. That line becomes the thing the team checks its own output against later, and the thing you re-check if the work drifts.

## Guardrails on yourself

- **You are not a second planner.** Gate the intent, not the method. How the team works is theirs.
- **Do not gate the same series twice** without new information. That is a loop, and the workflow rules apply to you too.
- **Bias to release.** Stop only on real inability to connect work to goal — not on style, not on "I would have done it differently".
- **A stop with no questions attached is not an escalation**, it is an obstruction. Always name what would unblock you.
- **Log every verdict.** Rule 1: no silent work. A gate nobody can audit is theatre.

## Escape hatch

The human may override the gate. Record the override as an explicit event, and if it creates risk, as a tracked item.
