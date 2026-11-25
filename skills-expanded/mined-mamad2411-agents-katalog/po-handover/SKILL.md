---
name: po-handover
description: Write a PO-session handover file and rotate the session safely — the PO counterpart of disposable worker sessions. Run at 50-60% context usage, or at a natural boundary (a gate just closed, a wave just finished), BEFORE judgment degrades. The new session resumes with /po-resume. Triggers - "po-handover", "prepare the handover", "rotate the PO session".
---

# po-handover — PO session rotation (sending side)

**English** | [日本語](SKILL.ja.md)

**Principle: a PO's state belongs in canonical docs, ledgers, and the inbox —
state that exists only in context is itself a defect.** The handover file is a
**map plus the in-flight deltas that cannot be re-measured** — never a memory
dump. Rotate before confusion, not after.

## When to rotate

- Context usage reaches **50-60%** (confusion past 60% is a measured symptom).
- A natural boundary: a gate closed, a wave completed.
- You notice degraded judgment (late, but better than not rotating).

A refresh is free — same philosophy as workers' "free refresh before a paid
model boost".

## Procedure

### 1. Write the handover file

Fixed path: `<po-dir>/handover/<space>.md` (your project's PO operations
directory). Template:

```markdown
# PO handover: <space>
- rotated: <date time> / outgoing session's role: <one line>

## In-flight (ONLY what cannot be re-measured)
- Gates awaiting GO: <which, whose approval — or "none">
- Expected verdicts/receipts: <from whom, landing at which path>
- Promises to lanes / the owner: <"report when X" items — or "none">
- Recent directives not yet in canonical docs: <content + source;
  having any is itself a warning sign>

## Monitor re-arm list (monitors die with the session — mandatory)
- <each Monitor's description and full command with all arguments>
- (or "none", stated explicitly)

## Inbox baseline
- <inbox dir>: <processed up to this file (top of ls -t + timestamp)>

## Canonical pointers (do NOT copy contents — a copy becomes a second truth)
- Operations doc: <path>
- Ledgers: <model ledger / decision ledger paths>
- Flow canon: <dev-flow doc / design principles paths>
```

### 2. Self-check (fail-closed)

- [ ] Zero references outside this file ("as discussed above" is forbidden)
- [ ] Could a fresh PO act safely from **this file + live measurement** alone?
- [ ] Every in-flight item carries a one-line "next action"
- [ ] Any fact that belongs in a canonical doc but lived only in context:
      write it to the canonical doc **now** — the handover holds pointers only

**If the handover is hard to write, that is the detector** — you were hoarding
state in context. The next generation's discipline: write directives, rulings,
and gate states to canonical docs the moment they happen.

### 3. Clean up after yourself

- Stop the Monitors / background tasks you armed (TaskList → TaskStop). A
  monitor that dies silently with the session drops events — measured in
  production.
- Send any unsent messages before you go.

### 4. Print the bootstrap line

End your final message with the single line the owner pastes into the new
session:

```
/po-resume <po-dir>/handover/<space>.md
```

## Anti-goals

- No transcribing canonical-doc contents into the handover (pointers only).
- No "it was probably like this" — write "unverified" if unsure.
- No writing the handover long after 60% — a map drawn while confused is bent.
