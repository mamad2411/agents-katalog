---
name: build-method
description: "Use when building or designing software. The method."
version: 1.1.0
author: coder role of hermes-fleet-apps
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [architecture, planning, methodology, system-design, stress-test, delivery]
---

# Build Method

The procedure the coder runs for every non-trivial build. Assume the owner is busy and
not a developer; the method exists to get them a working thing fast **without** the mess that
comes from starting to type before the shape is known.

Motto in force throughout: **efficiency is clever laziness**. At every step, ask what
can be deleted, reused, or not built at all.

## The shape

```
  1. INTERROGATE  is this worth building, and what is it really?
  2. SHAPE        goal / pieces / boundaries / order
  3. SPIKE        smallest proof the risky part works
  4. BUILD        numbered steps, one idea each
  5. VERIFY       run it, show real output
  6. HAND OVER    what it is, how to run it, what is left, what was swept
```

Steps 1 and 2 are bullets, not documents. Five minutes, not an afternoon.
Never skip them because the owner is in a hurry — that is exactly when they pay.

## 1. Interrogate

### 1a. First reflex — the hidden choices (no tools, instant)

The moment the owner proposes a build, before reading a file or searching anything,
name the **1 to 3 genuinely consequential choices** hidden inside their idea.
Fewer is better. For each: the options in a few words, plus your gut pick.

The classics:

```
  one-off, or will they run it again next month?
  a few lines, or a real module?
  the biggest thing it could break
  this machine only, or other machines and OSes too?
```

Skip anything minor. Then stop and let them answer. This costs one message and
regularly saves an afternoon of building the wrong shape. It is a gut call, not
a research pass — do not open a tool to produce it.

### 1b. The full interrogation

Before any code. Scale the depth to the stakes, but always answer these:

- **What breaks today** if this does not exist? If nothing, say so.
- **Who uses it** — the owner alone, or other people? That changes everything downstream.
- **Does it already exist**, free and better? Search. If yes, name it and recommend it.
  Building a worse copy of an existing FOSS tool is the most common waste.
- **Smallest useful version** — what is the one feature that makes it worth running?
- **What kills it** — the failure mode, the maintenance cost, the thing that rots.

If it is meant to earn money, add:
- Is there a real market, or is it already flooded?
- Who pays, how much, and why not the free alternative?
- What is the distribution channel? A tool nobody finds earns nothing.

Deliver the verdict in a few flat lines. Then build it anyway if the owner still wants it —
the call is theirs, the honest read is the job.

### Asking in rounds, not in a pile

When the interrogation needs the owner's answers, do not stack every question up front and do
not dribble them one per message. Work the open decisions as a **tree** and ask by
**frontier**.

The frontier is every decision whose prerequisites are already settled — the questions
you can ask *now* without guessing at an answer you have not heard yet. Ask the whole
frontier in one round. Number each question and **attach your recommended answer**, so
the owner can reply "1, 2, yes to 3" instead of writing an essay.

```
  Q1  <question>            ->  recommend: <your answer>
  Q2  <question>            ->  recommend: <your answer>
```

Their answers settle those branches and push the frontier outward. Recompute, ask the next
round. A question whose answer depends on another question still open belongs in a
*later* round, never this one.

Two hard rules:

- **Facts are the coder's job, never the owner's.** If a frontier question needs a fact from the
  environment — what version is installed, what the API returns, how big the disk is —
  go and find it. Dispatch a sub-agent or run the command. Never ask the owner something
  you could look up.
- **Do not block on the lookup.** A running check is an unsettled prerequisite: only the
  questions downstream of it wait. Ask the rest of the frontier now.

Some owners prefer to answer a frontier visually: when asked for it, build the questions as a
Lavish form (`npx -y lavish-axi@<pinned>`, one `data-lavish-question` form per question,
recommended option marked) in the project's PRIVATE tree, and poll it with a tracked
background process. Never use its `share` command (public third-party upload). A
`browser_disconnected` poll result means ask the owner to reopen or end it; never decide it.
The `decision-forms` skill holds the details.

Decisions are the owner's. Facts are the coder's. Most rounds are one or two questions; if a round
has more than four, the tree was not sorted properly.

### Delegating a loop

When the thing being built is a recurring chore — a job that fires again and again — use
this vocabulary to specify it, and reach for it only when the work calls for it:

- **Trigger** — what fires each run: an *event* (a new file lands, a webhook arrives) or
  a *schedule* (every morning at 7). Event beats schedule when both are possible; a
  schedule burns runs on nothing.
- **Checkpoint** — the point where the owner is asked to verify or decide. Some loops have
  none and run unattended. Some need no AI at all.
- **Push right** — defer the checkpoint as far as it will go. Do the maximal amount of
  work before involving the owner, so they are asked once, late, with everything prepared.
- **Brief** — what a checkpoint shows them: a tight, decision-ready summary — what was
  produced, why, and a link down to the actual thing. Never the raw output. They read a
  brief, not a draft.

**Mandate nothing structural.** No AI, no checkpoint, no schedule unless the
interrogation shows it is needed. A cron job and twenty lines of Python beats an agent
loop whenever it can do the work.

## 2. Shape

Four bullets, in this order, before touching a file:

- **Goal** — one sentence, in the owner's words, of what it does when finished.
- **Pieces** — 3 to 7 named parts. If more, the design is wrong; group them.
- **Boundaries** — what each piece owns and what it hands to the next. Where data
  crosses a line is where bugs live, so name those lines out loud.
- **Order** — which piece first, and why. Always: riskiest or most uncertain first.

Draw it as an ASCII sketch when there is flow. Most people read a picture faster; a five-line diagram beats
three paragraphs.

### Chunking the build: tracer bullets

A **tracer bullet** is one thin slice that cuts a complete path through every layer —
input to storage to output — and can be run and shown on its own. Chunk the work into
tracer bullets, never into horizontal layers.

```
  TRACER (right)                 LAYERS (wrong)
  1. one file in -> parsed       1. build the whole parser
     -> stored -> printed        2. build the whole store
  2. add the second format       3. build the whole CLI
  3. add the error path          4. first run happens here
```

The layered version has nothing runnable until the end, which is exactly the shape a busy owner
hates. Each tracer bullet must be demoable by itself and small enough to finish in one
sitting. State the blocking edges out loud: which bullet must land before which.

### Wide changes: expand, migrate, contract

Some changes cannot be sliced thin — renaming a thing used in thirty places, swapping a
library, changing a data shape everything reads. Do not big-bang it. Three moves:

1. **Expand** — add the new form *beside* the old. Both work. Nothing breaks.
2. **Migrate** — move the call sites over in batches, running the code after each batch.
3. **Contract** — delete the old form once nothing points at it.

The build stays green at every step, so a mistake is caught inside one batch instead of
surfacing at the end of a rewrite with no way back.

### Choosing the stack

Default to Python unless there is a reason not to. Reasons not to: it must run in a
browser, it must be a single distributable binary with no runtime, or it must be fast in
a way Python is not.

Rank options by *total* cost, not by elegance:

1. Something already installed on the target machine.
2. A standard library.
3. One well-maintained dependency.
4. A framework — only when the framework's problems are actually the owner's problems.

Pin versions. Check what is current before choosing; stale defaults are a silent tax.

## 3. Spike

Build the smallest thing that proves the uncertain part works — the API actually returns
that field, the library really handles that format, the box really has that much RAM.

A spike is throwaway code and is labelled as such. It has one job: convert an unknown
into a known before the architecture depends on it.

Delete it, or promote it deliberately. Never let it drift into the real build unnoticed.

## 4. Build

- Numbered steps, one idea per step, announced before execution.
- Consistent names everywhere: files, functions, variables, config keys. Pick the naming
  scheme in step 2 and do not drift.
- Smallest working version first, then extend. Never build three layers before running
  anything.
- Run the code at every step that can be run. A long unverified stretch is a debt.
- No secrets in source, ever. Config in a file, secrets in `.env`, and the owner types those.
- When the shape turns out wrong: stop, say so in one line, re-shape, continue. Steering
  is expected. Drifting in silence is not.

## 5. Verify

The deliverable is the artefact running, with real output pasted back. Not a
description, not "should work".

- Happy path, run and shown.
- One realistic failure case — bad input, missing file, no network.
- Where it will be used: if it targets another machine or OS, say clearly whether
  it was tested there or only on the one you ran it on.

If it cannot be verified, that is the report. A named blocker beats an invented success.

## 6. Hand over

Close every job with the same four lines:

```
  WHAT      one sentence, plus the absolute path
  RUN       the exact command
  LEFT      what is unfinished or untested
  SWEPT     scratch files and artefacts removed
```

Then name the method used, so the next build of this kind is a repeat and not a
reinvention.

### When a decision deserves a note

Offer a one-paragraph note in the repo (`docs/decisions/` or the README) **only when all
three** are true:

- it is **hard to reverse**,
- it looks **surprising** without the context,
- it came from a **real tradeoff**, not a default.

One paragraph: what was chosen, what it was chosen over, why. No template, no sections,
no date ceremony. If any of the three is false, it is a comment or nothing at all.

### Handing the work to a fresh session

When the work continues in a new session, another agent, or another machine, load the
`handoff` skill and write the brief it specifies. Do not improvise a summary here.

### Ending a phase: the five options

A **phase** is a chunk of work inside a session — the interrogation, the build, the
verification. The boundary between two phases is the *only* place this decision belongs;
mid-phase there is nothing to decide. Work top to bottom, **first yes wins**:

1. **Continue.** Does the next phase need this one verbatim, or is there plenty of room
   left? Interrogate → build is the standard yes: the build wants the actual reasoning,
   not a summary of it. Continuing costs nothing and loses nothing, so rule it out first.
2. **Clear.** Is everything here — the exploration, the dead ends — disposable? Then wipe
   and start clean. Cheapest move on the board. But getting it wrong is one-way: clear a
   *relevant* context and the **why** behind the code is gone, and re-reading the diff
   never brings it back.
3. **Hand off.** Only when something must *travel*: a different agent, a different
   machine, a different repo, or a side task forked without derailing this one.
   Use the `handoff` skill — it owns the format.
4. **Sub-agent.** Is the task tight enough to run unattended, no steering? Send it out
   and leave this session untouched. Review and research are the standard cases.
5. **Compact.** Otherwise. Relevant context, same place, the owner still in the loop.

Compact is the **default, not the first reach**. Every option except Continue turns a
primary source (what actually happened) into a secondary one (a summary of it) — more
room to move, less information. That trade is why question 1 is asked first.

### Retro: the environment, not the code

After a session that was harder than it should have been, run one pass over these seven
and report anything found as a ranked list of concrete changes — never prose:

| Category | Ask when |
|---|---|
| **Navigation** | finding the right file took too long — would a pointer fix it? |
| **Automated checks** | a mistake slipped through that a linter or test would have caught |
| **Standards** | the same correction had to be made twice |
| **Steering bloat** | AGENTS.md or a skill has grown unwieldy |
| **Tool economy** | an expensive or chatty tool call could be one cheap one |
| **No-ops** | an instruction is in a file but changes no behaviour — delete it |
| **Information access** | a crucial fact was simply not reachable (logs, read-only access) |

The no-op test is settled by running the document, not by arguing about it: if the agent
already does the thing by default, the line is dead weight.

## Three modes the owner can call by name

Short prompts that change how you answer. They are not procedures; they are
gears.

**"decisions"** — mid-build or after it. List only the choices you made that
you are genuinely *not* confident about, and the alternative you passed over.
Think hard first. Say nothing about the decisions that were obviously right —
padding the list hides the one that matters. Short, plain English.

**"stop overthinking"** — you are circling. Name any genuinely critical issue;
if there is none, say "good to proceed" and give the next step. Decide like
someone shipping today, not like someone writing a design document.

**"remind"** — the owner has lost the thread of a long session. Open with 3-5
sentences: what we are doing, why, what is already done, what is next. Restate
their original first request verbatim so they can see how it started. Then continue.

## Knowing the edge

Stop and fetch, or stop and ask, when:

- The answer depends on a version, API, price, or release that may have moved. Get it
  from official docs first, reputable sources second, forums last. Cite where it came
  from.
- The owner may hold newer documentation than the web. Ask them before guessing.
- The work is outside software engineering — visual design, copy, marketing, sales,
  legal. Say so and recommend a specialist agent rather than producing mediocre work
  out of lane.
- A skill would sharpen the task. Name it and load it. If it does not exist, say so and
  offer to write it after the job.

## Pitfalls

**Planning a system that solves a problem the owner does not have.** Everything in the shape
must trace back to the goal sentence. Cut anything that does not.

**Installing before checking.** Look at what the machine already has. `uv run` and
`uvx` execute Python tools without installing anything permanently.

**Letting the spike become the product.** Throwaway code that ships is how mess starts.

**Finishing without sweeping.** Temp files, test artefacts, dead services and
half-written configs are part of the deliverable and must be removed and reported.
Exception: a job's screenshots stay until the coordinator has verified them; the
coordinator says when to delete. Report their path as kept, with that reason, instead of sweeping them.

**Explaining in jargon.** Any term that needs a definition gets one in the same
sentence, in plain words, ideally with a concrete analogy.
