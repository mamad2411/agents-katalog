---
name: fortax-plan-and-run
description: Working method for CA jobs bigger than a reply - scope a vague ask into a five-line brief the CA confirms, write a plan with blockers first and one action per step, run it step by step ticking the plan and stopping instead of guessing, and run the same return for several clients in parallel with one checklist and one consolidated status table. The last step is always the CA's filing. Typical asks - "Sharma ji ka kaam kar do", "is mahine ke saare GSTR-1 nikalo", "audit file ready karni hai, plan bana lo", "11 clients ka 3B batch", "dekh lo kya karna hai".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
  credits: "Brief-first questioning, no-placeholder plans, step-by-step execution with stop-and-ask, and parallel dispatch patterns adapted from obra/superpowers (brainstorming, writing-plans, executing-plans, dispatching-parallel-agents), https://github.com/obra/superpowers (MIT)"
---

# Plan and run

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

Four moves, used only when they pay for themselves: **scope** the ask when a wrong reading would
waste work, **plan** when the job is bigger than one sitting, **run** the plan without improvising,
and **fan out** when the same job repeats across clients. A lookup, a due-date question, one portal
sign-in, a one-file read or a short draft needs none of this — just do it.

## 1. Scope the ask

### When

Only when a wrong reading would waste real work or produce something the CA cannot use:

- The client is not named, or several clients could match ("Sharma ji ka kaam kar do").
- The period is missing and the answer changes with it.
- The output is unclear — a note, a working paper, a filled return, a client mail.
- The scope could reasonably be one return or a whole year.

**Not** when a sensible default is obvious. "GSTR-3B for Sharma Traders" means the current period —
take it, say which period you took, carry on. Asking a question you could have answered yourself is
friction, not diligence.

### How to ask

- **One question at a time.** Not a form, not a list of four. Ask the one whose answer changes what
  you do next, wait, then decide whether you still need another.
- **Three questions is the ceiling.** Still unclear after three: the job is bigger than a
  clarification — say so and offer to write a plan.
- **Offer the likely answer.** A question with options is faster to answer:
  > Sharma Traders ke liye 3B — August 2026 ka, ya September ka? (August lagta hai, wo abhi due hai.)
- **Never ask for something you can look up.** The client's GSTIN (`CLIENT.md`), the folder contents,
  what is already filed, what the calendar says — find those yourself. Ask only what only the CA
  knows.

### The brief

Once it is clear, write it back and get a yes:

```
Client:   <Name (PAN)>
Period:   <month / quarter / FY, and the AY where it applies>
Job:      <what you will produce, in one line>
I need:   <documents or decisions you are waiting on, or "nothing">
Not in:   <what you are deliberately leaving out>
```

Short jobs keep the brief in chat. Longer ones: it becomes the head of the plan file.

**When the CA is vague on purpose** — "dekh lo kya karna hai" often means they want your reading, not
a questionnaire. Give it: what you would do and why, in two lines, and ask them to confirm or correct.

Nothing starts before a confirmed brief. If the ask was clear all along, skip this and work.

## 2. Plan the work

### When

When **two or more** of these are true:

- More than three steps, or work that will not finish in one sitting.
- More than one client, or more than one return period.
- The CA has to supply something (a document, a portal session, a decision) before you can finish.
- The output is a filing, an audit file, or anything that leaves the firm.

A plan for a two-minute job wastes the CA's time.

### Write it

Save it in the client folder (one client) or the firm's calendar or working folder (several clients),
as `YYYY-MM-DD_<job>_plan.md`. Show the CA the summary, not the whole file.

```markdown
# <Job> — plan
Client: <Name (PAN)>   Period: <FY / month / quarter>   Prepared: <DD-MM-YYYY>

Goal: <one sentence — what exists at the end>
Scope: <what is in>   Not in scope: <what is deliberately out>

## What I need from you
- [ ] <exact document, a decision, or a portal session you will sign in to>   (blocks step N)

## Steps
- [ ] 1. <one action, one sitting> -> <the file or state it produces>
- [ ] 2. ...
- [ ] N. Hand to the CA for review and filing

## Rules used
| Rule | Value | Source | Checked |

## Check before filing
- <what the CA must confirm with their own eyes>
```

### Rules for the steps

- **One action per step**, each ending in something real: a file written, a page downloaded, a
  reconciliation that ties. "Review the data" is not a step; "run the 2B reconciliation
  (`python3 scripts/fortax.py gstr2b ...`) and list every unmatched invoice" is.
- **Name the file.** Every step says which file it reads and which it writes, with the full path.
- **No placeholders.** Never "TBD", "handle exceptions", "as applicable", "check the relevant
  section". Not knowing the rate, form or due date yet is itself a step: look it up
  (`fortax-knowledge-base`) and cite it.
- **Blockers first.** Everything you need from the CA goes at the top, each naming the step it
  blocks. A plan that starts with work you cannot do is not a plan.
- **The last step is always the CA's.** You never plan to type a password, solve a captcha, enter an
  OTP, sign with DSC, pay, or click the final Submit or File. Plan up to the review screen and stop
  (`fortax-portal-work`).
- **Name the skill** a step uses where one exists — `fortax-gstr1-and-3b`,
  `fortax-gstr2b-reconciliation`, `fortax-bank-statement-to-books`, `fortax-client-comms` — so the
  step can be run by someone, or a subagent, that has never seen this client.

### Read it back before you show it

- Does every item in Scope have a step? List anything with none.
- Does any step depend on a figure, form or rate that no earlier step produces or cites?
- Could a colleague who has never seen this client run step 4 without asking you?

Fix what you find. Then give the CA the goal, the blockers, the step count and the first step — and
ask whether to start. Do not start a long job without that yes.

## 3. Run the plan

### Before the first step

Read the whole plan again, not just step 1. Then say one of two things:

- "Ready. Starting step 1." — and start, or
- your concerns, before touching anything. A plan you doubt is raised now, not discovered halfway.

Check the blockers. If something you need is still missing, say which step it blocks and ask for it.
Do not start work that will stall.

### Each step, in order

1. Do exactly what the step says. If it names a file, use that file.
2. Verify the step's own output before ticking it — open the file you wrote, recompute the total
   with a formula or script, re-read the page you downloaded (`fortax-evidence-discipline`).
3. Tick the checkbox in the plan file itself, so the plan stays the record.
4. Move on.

Report in batches, not per step. After every few steps, or at any checkpoint the plan marks, tell the
CA in three lines: what is done, what it produced, what is next. They should never have to ask where
you are.

### Stop, do not improvise

Stop and ask the moment any of these is true:

- A document, portal session, figure or decision you need is not there.
- A step's instruction does not match what you find in the files.
- A rule the plan cites turns out to be different for this period.
- A verification fails twice.
- The work is drifting outside the plan's stated scope.

Say what you were doing, what you found, and the two or three ways forward. Never guess a figure,
never substitute a document, never quietly widen the scope. A stopped job with a clear question is
fine; a finished job built on a guess is not. For a failed portal or upload step, see
`fortax-when-a-step-fails`.

### When the plan itself is wrong

If the approach is wrong — not one step, the shape of it — stop and say so, and rewrite the plan
rather than patching step after step. Three steps that each needed a workaround means the plan was
wrong, not unlucky.

### Finishing

The last step of every plan is the CA's. When the work before it is done:

1. Re-read what you produced; do not trust your own summary of it.
2. Fill the **Rules used** table with what you actually applied and where each came from.
3. Write the **Check before filing** list — the specific things the CA must look at.
4. Tell them plainly: it is ready for their review and their filing, and it is **not filed**.

Output: the plan file with every box ticked, the deliverables in the client folder, and a closing
message — what was produced, where it is, what is left for the CA, and anything unresolved.

## 4. Parallel filings

### When

The same job, several clients, one period — GSTR-1 for eleven clients, 3B for a month's batch, TDS
returns for a quarter, DIR-3 KYC season — and the clients are genuinely independent.

**Not** for one client, for steps that must run in order, or when clients share a figure (a group
with inter-company entries reconciles together, not in parallel).

### Before you start anything

1. **Fix the roster.** List the clients from the CA's client list or compliance calendar with the
   period and the return. Show it and get a yes. A batch on the wrong roster wastes every branch.
2. **Write the checklist once.** One list of steps every client goes through, in the same order,
   producing the same named files, so outputs are comparable and a gap is visible.
3. **Check what is missing before you fan out.** Any client with no data, no portal session arranged
   with the CA, or an unfiled prior period comes out now and goes on a short "cannot start" list.
   Discovering it in branch nine wastes eight branches of context.

### Running them

- **One branch per client.** If your tool has subagents, give each client its own with a complete
  brief: client, PAN/GSTIN, period, folder path, the checklist, the exact command (for example
  `python3 scripts/fortax.py gstr1 --sales <path> --gstin <GSTIN> --fp <MMYYYY>`), and where the
  output goes. A subagent sees only its own brief — put every file path inside it and never say "same
  as the previous client". Without subagents, run the clients one after another from the checklist.
- **One browser tab per client per portal.** Never reuse a tab across clients. A session left signed
  in as the wrong client is how a filing goes to the wrong GSTIN.
- **Keep the batch small enough to watch.** Four to six at a time. Finish the wave, report, start the
  next.
- **A branch that stops does not stop the batch.** Record why, park that client, carry on.
- **Check each branch yourself.** Open the files it says it wrote; a subagent's "done" is a claim,
  not evidence.

### The rules do not relax because there are eleven of them

Every branch still carries its sources, fills its **Rules used** table, and stops before the
password, captcha, OTP, DSC, payment and final Submit. Volume is a reason to be stricter: a wrong rate
applied once is an error; applied to eleven clients it is a pattern the department will notice.

If two branches give different answers to the same rule question, stop the batch. One of them is
wrong and you do not yet know which.

### Report

One table, saved as `YYYY-MM-DD_<job>_batch.md` in the firm's calendar or working folder, not eleven
messages:

| Client | Period | Status | Output | Needs the CA |
|---|---|---|---|---|
| Sharma Traders | Aug 2026 | Ready for filing | `.../GST/2026-08/GSTR1_09ABCDE1234F1Z5_082026.json` | Review, then upload and file |
| Gupta Textiles | Aug 2026 | Blocked | — | Purchase register missing |

Then three lines: how many are ready, how many are blocked and on what, and what to do first. The CA
files them; you never do.

## Attribution

The questioning, planning, execution and parallel-dispatch discipline follows patterns from
[obra/superpowers](https://github.com/obra/superpowers) (MIT; licence in
`LICENSE-THIRD-PARTY-superpowers.txt`), rewritten here for CA filing work.
