---
name: guide-and-verify
description: 'Guide a person through a change they must make by hand in a UI you do not control - an admin console, a portal, a settings page, a dashboard - and prove it landed by measuring the system before and after. Use this whenever the agent cannot or must not make the change itself and a human has to click: the user says walk me through it, teach me step by step, how do I do this in the portal, I will do it by hand, you cannot write to this system, or asks for a runbook, handover checklist or click-by-click guide for any console (CRM, cloud portal, DNS, SaaS admin, CI settings, database GUI, router, payment dashboard). Also use it when handing hand-work back at the end of a task the agent could only partly automate. Do not use it for changes the agent can just make itself in code or via an API it is allowed to call.'
---

# Guide and verify

Some changes are not yours to make. The system has no API you may write to, the credentials are not
yours, the change is legally or organisationally the human's, or the safe boundary of the task says a
person clicks and you only read. In every one of those cases the deliverable is the same: **a runbook a
person can follow, plus proof that following it worked.**

The failure this skill prevents is the vague handover — *"remove that field from the forms and the
views"* — which reads as complete, sends the person hunting through a UI, and ends with nobody able to
say whether it is done. The cure is measurement on both ends and a step shape tight enough to follow
while tired.

## The boundary comes first

Before anything else, settle who acts. If the change is the human's, **print the steps and stop.** Do
not do it for them, do not do "just the easy half", and do not quietly widen your access to finish it.
A boundary that you cross once stops being a boundary.

Say the boundary out loud in the handover, because it tells the person that waiting for you is not an
option: *"I read this system. I do not write to it. Every change below is yours."*

## The five phases

### 1. Measure the baseline — before you write a single instruction

**Never write a runbook from a document.** Tickets, wikis, past handovers and your own earlier notes
were true when written and drift silently. Read the live system and count what is actually there.

Two numbers matter and they are not the same:

- **the raw count** — how many times a name appears in the underlying data
- **the actionable count** — how many things the person must actually click

They diverge constantly, because systems store a name once for the real object and again in indexes,
dependency lists, labels and audit fields. Reporting the raw count sends the person hunting for objects
that do not exist. Parse the structure and count the objects; use the raw count only as a cross-check.

Then **locate each one precisely**. "Somewhere on the form" is not a location. "Tab X → section Y →
field Z" is. If you cannot say where it is, you have not measured enough to write the step yet.

Write the baseline down where it survives the session — the ticket, the runbook header, a commit. It is
the only thing that makes the after-measurement mean anything.

**Record each measurement when you take it, not in a batch at the end.** Every time you read the live
system, write that reading onto the ticket before the next read — the number, what it was measured
against, and the time. A session that measures twenty things and records them once at the end has an
unwritten ticket for its whole length: a crash, a compaction or a parallel session loses every fact,
and anyone reading meanwhile sees the document's stale claim instead of the system's answer. The rule
is per-check, not per-session — a measurement that **contradicts the document** is the one most worth
writing immediately, because it is the one nobody can reconstruct.

**Save the full state, not only the numbers you will assert.** For every object a step will touch, write
its complete serialized form — the XML, the JSON, the config, the record — before the person acts. The
assertion proves *whether* something moved; only the snapshot proves *what*. Do this even when the edit
looks reversible: a platform undo you cannot name the target of is not a recovery.

**Put it where it outlives the session** — attached to the ticket, committed, or a directory named in
the runbook. A snapshot in a scratchpad is not a snapshot. It dies with the session and leaves the next
person exactly as blind as if you had never taken it.

**Ask first only when the snapshot needs the person.** If you can read the objects yourself, take it
read-only and say you took it — asking there costs them a turn and buys nothing. If it needs their hands
or a permission you do not hold — an export, a portal download, a wait — ask in one line: *"I will save
the current state of `<the objects>` first — is that all right?"* **Only an explicit no is a decline.** A
vague reply, a changed subject and silence all count as no answer, so you take the snapshot. On an
explicit no, or when you cannot read the objects at all, use the two options in the next paragraph:
borrow their eyes for one export, or label the runbook *"no before-snapshot, by the operator's
decision"* and carry that label into every later claim, the way an unverified baseline is carried.

**If you cannot read the system either.** This is common — often the same missing credentials that stop
you writing also stop you reading. Do not treat that as permission to fall back on the document, which
is how the vague handover gets written in the first place. You have two honest options:

- **Borrow the person's eyes.** Give them one read-only check, and ask them to paste the result back.
  That result becomes the baseline, and it is genuine measurement — it just travelled through them.
- **Declare the baseline unverified.** Write it as *"inherited from `<source>`, `<date>`, not verified
  against the live system"*, and carry that label into every later claim. An unmeasured baseline that
  looks measured is worse than no baseline, because the after-check then certifies a number nobody
  ever confirmed.

Choose the first when you can. What you must never do is state a count in a runbook without saying
where it came from.

### 2. Decide the assertion before the person acts

State now what the numbers must become. `1 control → 0`, `13 rows → 0`, `status pending → active`.
An after-measurement with no pre-declared target is a description, not a check — you will find yourself
reading the result and deciding it looks fine.

**The predicted outcome is a claim, and it needs evidence like any other.** Phase 1 forbids taking
counts from a document; the same applies to what you say *will happen*. "The save will be refused
because the field is required" is a platform-behaviour claim — verify it against the vendor's docs or
a live probe before it enters the runbook. A wrong prediction is worse than none: the person reads a
correct result as a failure, or a broken one as a pass, and the runbook has taught them the wrong
success condition.

Include a **blast-radius assertion**: name what must *not* change. Count the neighbours now (the other
28 handlers, the other 5 rules, the other 12 records) so that after the change you can say nothing else
moved. This is what catches the person deleting one thing too many, which no success check ever does.

### 3. Write the step in a fixed shape

One step is one reversible unit of work. Use this shape every time — the person learns it once and then
reads it fast:

```
## Step N — <what this achieves, in plain words>

**Go to:** <a real address or an exact navigation path>

**Do:**
1. <one action>
2. <one action>
...

**Do not:**
- <thing> — <why, in one clause>

**How to verify yourself:** <a read-only check the person can run alone>

**Then report:** <who to tell, and where the result is written down>
```

Rules that make the shape work:

- **One action per numbered line.** "Select the field and delete it and save" is three lines.
- **A real address beats a description.** Give the URL. If it may not resolve, give it anyway and add
  the click path as a fallback in one line.
- **Every "do not" carries its reason.** A prohibition without a reason gets ignored the moment it is
  inconvenient. *"Do not stop after Save — Save writes a draft, and a draft looks identical."*
- **Include the destructive near-misses.** The dangerous instruction is not the one you gave; it is the
  adjacent thing that looks like it. If they must remove a field from a screen, say explicitly that the
  underlying column stays. If they must disable one rule, name the rule next to it that must not be
  touched, and say what happens if it is.
- **Order by dependency, and say when order does not matter.** People reorder steps that look
  independent. If step 2 must follow step 1, say why in half a sentence.
- **Never batch.** One step, verify, then the next. Batching saves the person a few minutes and costs
  everyone an afternoon when something breaks and nobody knows which change did it.
- **Capture the before-state of anything structured, not only the irreversible.** Ask "if the person
  edits the wrong element, can I name which one?" If you cannot, you owe a before-snapshot, and Phase 1
  says where it goes. That covers ordinary edits to forms, views, configs and records, not just
  deletions and key rotations. For the genuinely one-way — deleting a record, rotating a key, dropping
  a column — "one step, verify, then the next" buys you nothing, because there is nothing to go back to:
  add a numbered line before it that reads the present value and writes it somewhere retrievable, and
  say plainly in the step that this action is not reversible. A person who knows a step is one-way reads
  it twice.
- **Aim the report line at whoever will actually be there.** In a live session it is *"tell me and I
  measure it"*. In a runbook that ships ahead of a release window it must name a destination that
  outlives you — *"record the result and the measurement on `<ticket>`"*. Getting this wrong produces a
  document that tells a reader six weeks from now to report to an agent who is long gone, and the
  result then goes nowhere.

Keep the prose short. The person is reading this with a console open in the other window.

### 4. Verify — read-only, in a different channel

When they report a step done, measure it against the baseline and report before → after. Assert the
success condition **and** the blast radius.

**Verify through a different channel from the one they used to change it.** If they edited in a UI, read
the machine state — an API, a CLI, an export, a query. The editing UI is the one surface guaranteed to
show you what it thinks it just saved, including from its own cache. A second channel is what turns
"it looks right" into evidence.

**When there is no second channel**, which is normal for consumer-grade admin pages, routers and many
SaaS settings screens: say so, and change your wording. The result is then *"reported by the operator,
not independently measured"* — never "verified". This distinction is the whole value you are adding, so
losing it to keep a tidy report defeats the exercise. An unsatisfiable rule gets satisfied creatively:
if you leave yourself no honest way to say "I could not check this", you will accept a screenshot and
call it proof.

If the check fails, say so plainly with the numbers, and diagnose before proposing a redo. Half-applied
is the common outcome, and telling them to "try again" on a step that partly landed makes it worse.

### 5. Teach the self-check, and record the result

Give the person a check they can run **without you**, in that second channel. This is the part that
outlives the session: they will do this again when you are not there, and a runbook whose only verifier
is an agent is a runbook that rots.

Prefer a check that is one action — open a URL, run one command, look at one screen. If the natural
check needs three steps, it is too heavy and they will skip it.

Then write the outcome where the next person finds it, with the measurement attached. "Done" is worth
little. "Done — 1 control on each form became 0, other 28 handlers unchanged, measured 09:14Z" is worth
the whole session.

## The trap that catches nearly every system: saved is not applied

Most systems that a human edits by hand have two states for the same object — an edit that exists and an
edit that is live. The names differ; the failure is identical. **A plain read usually returns the live
copy, so a saved-but-not-applied change reads as "nothing happened".** People then redo correct work, or
conclude the tool is broken.

| System | Edited state | Live state |
|---|---|---|
| CRM / low-code platform | draft customisation | published |
| DNS | edited record | resolving for clients |
| Cloud console | saved configuration | running revision |
| CI / CD | edited definition | definition the next run uses |
| SaaS admin | staged setting | rolled out to users |
| Database GUI | uncommitted transaction | committed |

What closes the gap is either **an explicit apply action** (publish, deploy, commit, restart) or **a
propagation delay** you have to wait out — and sometimes both. Find out which one you are dealing with
before you write the step, because they need different instructions: an apply action is a line in the
runbook, and a delay is a warning not to re-do work that already succeeded.

So do two things. Put the apply step in the runbook as its **own numbered line**, never as a clause
inside another line. And tell the person that their self-check doubles as an apply-detector: *"if the
old value is still there, you did not apply it."* Where the system offers a read of the pending state,
give them that too, so they can tell "not applied" apart from "not saved" — those have different fixes.

## Write for someone who is tired and clicking

Short sentences. One instruction per sentence. Plain words. Match the user's own vocabulary for their
domain — if their glossary distinguishes two similar terms, hold that distinction, because a runbook
that blurs it is the thing that makes them act on the wrong object.

Do not editorialise about risk in the steps. Put the reason in the "do not" clause and move on.

## Say what you could not measure

Some part of the picture will be out of reach — a permission you do not hold, an endpoint that refuses
you, a number that lives only in a UI. Name it, name where the human can see it, and do not let the
gap hide inside a confident summary. A verification that quietly skipped a check reads as coverage it
did not have, and the next person inherits that as fact.

Same for staleness: if your baseline came from a feed that refreshes on a delay, say how old it is.

## When the whole thing is deferred

Sometimes nobody can verify today — the change rides a release, a window, an approval. Then the runbook
**is** the deliverable, and it has to survive months without you. Write every identifier in full, record
the baseline inside the document rather than pointing at a session, and state which checks were actually
run and which are still owed. A checklist that cannot tell a new fault from a known one is what turns a
deferred verification into an argument.
