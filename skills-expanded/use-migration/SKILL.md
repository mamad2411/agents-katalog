---
name: use-migration
description: >
  Moving an existing project onto this architecture: the launch GATE that must pass before anything
  begins, nineteen stages in order with what each ends with, and ten probes to run before writing code
  over somebody else's data. Load it when the mode is `migration`, when the owner says "we are moving
  this project" / "port my app" / "here is the repo we migrate from" — and **at the very first message**,
  because §1 decides where the session must be standing, which cannot be repaired later. Load it again
  at the start of every session of such a move: a migration outlives dozens of them and you locate
  yourself by its stage. The mode itself, the four questions about rights, and the rules for foreign
  code live in `CLAUDE.md` §`migration`; this file does not repeat them.
---

# use-migration

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.
>
> 🔒 One boundary: the freedom is about **HOW** you build, never about whether the work is recorded as
> a step and the state written down.

Everything here was earned by one complete migration. Every ✗ is a failure that actually happened.

## 0. Read first, do not restate

`CLAUDE.md` §`migration` already carries: switching the mode on, *foreign code is read as a DESCRIPTION
and never rewritten*, the four questions about application type and rights, no token for the source
repository, never execute foreign code on the server. Read it. This file carries what it does not:
**the stages, the probes, and the traps of each phase.**

## 1. Stage 1 is a GATE, not a step — nothing begins until it passes

A migration is the one kind of work that needs **two trees open at once**, so it needs a working folder
of its own with exactly two repositories inside. ✗ getting this wrong cost the first day of the real
move: the session stood in the wrong place, the result's corpus of laws was absent from the agent's
context, and it invented its own `Migration/` folder to track work — the handover that folder was
supposed to protect never existed.

**① Explain it to the owner in his words, before anything else:**

> A move needs two projects side by side — the one we read and the one we build. Make **one new folder
> for this project** and put both inside it: **source** — what we are moving, it dies when the move
> ends; **result** — the Fractera project it becomes. Then **start the session from that new folder**,
> not from a repository you already had open.

**② Demand a confirmation in words, and do not accept silence:** *"yes, the session is started in the
project folder"*.

🔒 **Why a confirmation and not a command.** You can check where you ARE; you cannot check where you
STARTED — and the instruction files in your context were loaded at start, not at `cd`. This is not a
beginner's mistake: an already-open terminal is the default for everyone, and experienced developers
lose it just as often.

**One self-check does detect it and costs one read:** open the project folder's `CLAUDE.md`. **If its
content is new to you, you did not start here.** Stop and ask for a restart from the project folder.

**③ Verify with your own tools — all six, before the first plan:**

| # | Check | ✗ what it prevents |
|---|---|---|
| 1 | the working directory is the project folder, not a general repository | every path below lands in the wrong tree, and it shows up days later |
| 2 | both folders exist and are non-empty | "I cloned it" and "it is there" are different facts |
| 3 | both are git repositories — `.git` present in each | a downloaded archive is not a repository: no history, no diff, nothing to recover from |
| 4 | the result has a remote — **presence only, never print the URL** | ✗ a live access token was embedded in a remote address, and merely reading state printed it |
| 5 | the result carries the guest corpus: `CLAUDE.md`, `.claude/skills/`, `development-steps/` | if it does not, this is not a Fractera result folder and nothing below applies |
| 6 | the source is never written to — say it aloud as a rule, no flag enforces it | an agent that edits the original destroys the only reference the move has |

**④ Write the project folder's `CLAUDE.md` — a step, not a formality.** The session sits in the PARENT
folder, so **the result's own instruction is not loaded automatically** and its entire corpus is missing
from your context until you name it. That file states in words: which folder is the source and that it
dies · which is the result · and **what to read at the start of every session** — the result's
`CLAUDE.md`, its `current-steps.md`, its steps folder, its `ANTI-PATTERNS.md`.

✗ Without that section the agent builds its own bookkeeping. It did, on day one — and `check:steps` in
the result fails the build over a folder that should never have existed.

🛑 **The gate:** six checks pass · the confirmation is given in words · the parent instruction exists
and names the reading addresses. Until then there is no inventory, no passport and no code.

## 2. Three laws that govern the whole move

🔒 **A migration MOVES, it does not develop.** "Should this route be dynamic?", "should these entities
merge?" are questions about developing the product and lie **outside** the move. ✗ an entity×role matrix
was proposed as a design aid: good architecture device, bad migration device — it makes you redesign
instead of move, throwing away the only support a migration has, a working original.

🔒 **The original is a source of QUESTIONS, not answers.** It answers exactly one — *what is already
built here*. Two failures, mirror images of each other: a property of the source was carried onto a
decision about the result (the source was single-language → the result was assumed single-language; the
result's CONFIG decides that); and the ABSENCE of something in the source was read as absence in the
product (patients did not log in → "no `account` group needed"; the owner said otherwise). **The source
describes what was built, not the boundary of what was intended.**

🔒 **A fresh word from the owner that contradicts a RECORDED decision of the owner is a question, not
permission.** The new sentence sounds like an order and the record looks like history, so the agent
executes the sentence and cancels the decision in silence — **the worst kind of invention, because it
looks like implementation.** Show both sides, name the cost of each, stop.

🔒 **"Done" for the whole move is defined from the REASON for moving, and defined before stage 2.**
Ask why they are leaving, and write the acceptance of the entire migration in those terms. ✗ in the
real move the owner arrived believing a migration is "the interface is carried over"; the reasons were
a scheduler the old host would not run, a regulator forbidding foreign storage, and cost — so
"succeeded" meant **timed chains running on their own server against their own database**, and the
interface was the cheapest part of the work.

**Expect that definition to be corrected twice, and say it out loud both times.** It happened at
stage 2, when the inventory showed the product's core did not exist in the source at all, and again
around stages 10–12, when the silent defects turned out to live in data rather than in screens. An
owner whose picture of the job changes is normal; an agent that lets the acceptance drift with it in
silence is not.

## 3. The map — nineteen stages in four phases

The order IS half the skill. Do not reorder it for a project that "is different".

| # | Stage | Ends with |
|---|---|---|
| **A** | **before any code** | |
| 1 | **placement — the GATE of §1** | six checks pass, the owner confirms in words, the parent instruction names the reading addresses |
| 2 | inventory of the source | a map with the column *what it turns into* — and a measurement of how much of the core exists at all |
| 3 | project passport — `development-docs/PASSPORT.md` | its start light is clear: while any ⛔ stands, no code |
| 4 | first live update | four proofs, not "the site opened" |
| 5 | application type and rights (`CLAUDE.md`) | the owner's decision, recorded verbatim |
| 6 | route design, in TWO answers with a stop | an agreed tree, not one you chose |
| **B** | **structure** | |
| 7 | skeleton: the whole tree as stubs | the owner walks every address by navigation |
| 8 | deleting the template's own pages | no address exists that the tree does not name |
| 9 | clearing the furniture: menus, header, drawer | behind every element there is a live page |
| **C** | **data** | |
| 10 | data foundation: tables and domain model | a query to any table answers — no screens, no doors, no integrations |
| 11 | first live READ of the source, read-only | a second run changes no counter |
| 12 | first screens on live data **+ the audit screen** | it is visible which numbers can be trusted |
| 13 | *(usually unplanned)* fetching fields the source withheld | born from the audit screen, not from the queue |
| 14 | the first entity the PRODUCT fills, not the source | a safety catch refuses a real person |
| **D** | **product** | |
| 15 | the core: automation that decides by itself | its selection equals an independent query |
| 16 | reference data — from fact, not from a directory | the catalogue carries a measure |
| 17 | screens waiting on external channels | empty HONESTLY: the screen says why, in words |
| 18 | analytics — second to last | numbers match independent measurements |
| 19 | sweeping up the remaining stubs | no stub left in the tree |

**Three laws about the order itself:**

🔒 Between the foundation and the first screen stands the **live read**, and the three do not merge. ✗
proved in reverse: three silent defects found at stage 12 belonged to stages 10 and 11, and were told
apart only because the stages were separate.
🔒 The **audit screen is early** and pays for itself the same day — it found the defect that would have
made the product write to 481 people who had refused contact in writing.
🔒 **Analytics is second to last** because it consumes all data at once and so works as the last
detector of silent defects. Earlier, it finds the same things on incomplete data — unconvincingly.

## 4. How a session of a migration starts

**Every session, first two moves: check 1 of the gate, then `current-steps.md`.** The folder question
does not go away after the first day — a session started from the wrong place on day nine looks exactly
like one started from the right place, until a path lands in the wrong tree. Then find the stage and
read its row and its phase below.

**A migration outlives dozens of sessions**; the queue is in the owner's `new-steps/`, the accounting is
`use-development-steps` with no exception for this mode.

🔒 **Check the premises of the step before its first action** — usually one command each. ✗ the most
transferable law of the whole run: both premises of a planned step were false, and both were checkable
in a single command that nobody ran.

## 5. Ten probes — run them, do not reason about them

The corpus's own meta-law: *a statement about state, written as a law, rots — replace it with a command
that checks*. These are that replacement. Each costs one query and buys a class of silent defect.

| # | Before you… | Run | Read as |
|---|---|---|---|
| 1 | write any selection | count non-empty vs total for **every column it touches** | filled for a minority = **not a data source, a trap** |
| 2 | write any condition on a status/flag | `GROUP BY` that column over the whole base | it almost always has more values than its name implies |
| 3 | trust a flag | same query | one value at 100% = **never used**, not "everyone agreed" |
| 4 | trust a foreign API response | compare requested field list against keys **present** in the payload | an absent field impersonates an empty one |
| 5 | build a per-item crawl | look for a bulk/company endpoint in the API index | ✗ 15 minutes planned per-record vs 7.5 s for the whole base |
| 6 | build a screen joining source entity to platform entity | count rows carrying the join key | ✗ e-mail present for 242 of 1844 — the screen can only say "to whom", never "granted" |
| 7 | declare a data move accepted | write it as `source_total − named deductions = stored_count` | every deduction owns a name and a counter in the sync report |
| 8 | call a sync idempotent | run it twice, diff every counter | ✗ a `NULL` inside a composite `UNIQUE` broke this and the report still looked right |
| 9 | believe an automation's selection | recompute the number by a hand-written query to the base | two routes, one number — this is proof plane #1 for the whole phase |
| 10 | rate-limit a crawl | put the pause **at the address**, then re-count what was read | ✗ the pause lived in one loop and not the other; 27% went unread in silence |

🔒 **An empty result of probe 1 or 9 looks exactly like "nobody matches".** That is the migration's
signature defect: no error, no red gate, a plausible answer. **Distinguish them by the probe, never by
the look of the output.**

## 6. Phase A traps — before any code

- 🔒 **The inventory names, for every element, HOW it moves:** *literally* · *by meaning* (a person's
  rhythm: a median moved out of SQL into TypeScript) · *by structure* ("a client is a STATE, not a flag"
  → a cases table beside the person) · **does not move** (multi-tenant ids, one clinic's service names
  living in code). Without that column it is a copy list, and copying foreign architecture carries its
  compromises along with its decisions.
- 🔒 **Second column: has this field a CONSUMER?** ✗ a flag existed in the original and was read by
  nothing. It either does not move, or moves owing a consumer in the next step.
- 🔒 **Measure how much of the core actually EXISTS.** ✗ of five links in the chain, two were built: the
  "migration" was half a move and half a new build. Measure at stage 2 or the estimate is understated
  twofold. **The most valuable line of the map is "no answer".**
- 🔒 **This is the one cheap moment to drop the original's compromises** — list them before code; later
  they are your debt, not theirs.
- 🔒 **Stage 3 fills `development-docs/PASSPORT.md`** — the fifth address of memory. **Its ten sections
  and its start light are defined in `CLAUDE.md` § *Your memory*; do not invent a shape for it here.**
  What is specific to a migration is only the SOURCE of the answers: §1, §2 and §7 are read out of the
  original's code and then confirmed by the owner, while §3–§6 and §9 can only come from him.
  ✗ the reason it exists: everything the owner had explained lived only in chat, and the agent mixed
  things up not because it was poor but because that explanation had not reached it.
- 🔒 **The four questions of stage 5 can come back answered CONTRADICTORILY, and that is not a
  mistake.** ✗ one answer said a person "will not be connected to the auth system at all" and in the
  same breath needed a role for them "so that they get into the system". The owner said himself the
  purpose was unclear. **An owner who does not know and an owner who answered inconsistently need
  different handling; to neither do you substitute your own answer.** Carry it forward as an open
  question, with a ban on deciding it silently.
- 🔒 **When delivery fails, find the FIRST broken link, not the one the error names.** ✗ the whole
  delivery chain was built and shipped while the agent's key had never been issued: the environment
  export skipped a block in silence, and the script refused naming the *second* link ("set the
  variable") instead of the first ("no key was issued"). A chain that reports the wrong link looks
  exactly like an agent that will not obey.
- 🔒 **A required proof can be unobtainable by construction — say so, never substitute an easy one.**
  ✗ the canonical delivery proof reads a build stamp that only one of the two build paths writes, so on
  the other path it is `null` and the proof cannot exist. Name the hole; do not quietly prove something
  else.
- 🔒 **Stage 6 is AGREEMENT, in two answers.** First the source's architecture as it is — tree, groups,
  route types, what is public — **with not one opinion in it**; he says continue; only then your
  proposal. Merged, he never sees the original, only an opinion about it.
- 🔒 **Addresses move ONE TO ONE**, the sole exception being the language prefix, carried even with one
  language enabled. ⚠️ Two reasons stand behind the rule — search rankings, people's habits — and
  **checking which applies here is part of it**: ✗ almost nothing was public in the real move, and
  reciting the memorised reason costs trust exactly where you are right.
- 🔒 **Exactly three things may make the result's structure differ, exhaustively:** permission-group
  folders · the language prefix · routes grown from the owner's decisions.
- **Form: a TREE IN CHAT**, not a file. Under it one of three verdicts for EVERY source route: kept
  1:1 · changed and why · not moved and what instead. **A route lost in silence is this stage's main
  defect.**

## 7. Phase B traps — structure

- 🔒 **Stage 7 builds the structure ENTIRELY and finishes no page.** `layout`, header and footer stay
  untouched, or the owner cannot walk the tree and the stage is unverifiable. **A route counts as
  created when it is REACHED by navigation**, not by typing its address.
- 🔒 **Reproduce before you delete.** Stage 8 removes the specimens; whatever was not carried into the
  new routes vanishes with them. Compare **file by file** — a route's genus is set by its dynamic
  segment, not by its layer, and genera have different file sets.
- 🔒 **Before deleting a page ask the fourth question: who DEPENDS on it** — a guard, a generator, a
  `prebuild` step. ✗ one page passed the three older questions and was the only specimen of all 31
  catalogue kinds. **Verify deletion by a FULL `prebuild`, not a list of gates**: ✗ its first step
  failed before any gate would have run.
- 🔒 **"Remove the link" ≠ "delete the shared thing".** Links live in the sitemap, the machine-reader
  registry, the PWA manifest, list generators. No file is deleted; each loses the piece pointing at
  nothing.
- 🔒 **Footer pages are NEVER deleted** (owner, 2026-08-25). Their absence from the agreed tree is not a
  decision to remove them — that tree mapped the source's routes. If the project has its own footer
  pages, that is a separate step about CONTENT: our pages stay, his text arrives.
- 🔒 **Clearing the furniture is its own stage, after deletion, before the build.** Menus are not
  checked by gates — visibility is courtesy, not protection — so they survive untouched and lead to 404.
  **A link to nowhere is worse than a missing page:** nobody looks for a missing page, a menu item gets
  clicked. Both menu sources, **under every role**; the negative control is not "extra items are gone"
  but **"every address of the agreed tree is still reachable"**.
- 🔒 **Silence in a list is not permission.** A template widget appeared in neither the delete nor the
  keep list: the right move was to ask.
- 🔒 **Emptying a page breaks whatever stood on its content.** ✗ removing the home page's blocks also
  removed its heading: a `titleInBody` flag was set because a section printed the H1. **A setting
  explained by a neighbouring piece outlives that piece and lies in silence.** After emptying, re-read
  the settings that existed FOR the content.
- 🔒 **A negative result, proved by negative controls, is worth exactly as much as a positive one.**
  ✗ stage 9 removed **zero** menu items: the premise "menus surely still point at deleted pages" did not
  hold, because the group manifests lived inside the deleted section folders. That could only be
  established by walking every menu — and the walk IS the work of the stage. Do not report "nothing to
  do" as a skipped stage.
- 🔒 **Your own note in `ANTI-PATTERNS` can make you misread a REAL failure.** ✗ an observation about
  false alarms was written at stage 4, and at stage 7 a genuine gate failure was dismissed by its own
  author under that note. **A wrong law is more dangerous than a missing one**, so every entry you write
  during a migration owes a third field beside symptom and cure: **how to tell this case from the one it
  resembles.**

## 8. Phase C and D traps — data and product

- 🔒 **A capability with no data behind it is the OWNER'S decision, not a development task.** ✗
  birthdays empty for 1845 of 1845 — no API call changes that. Hand him that list as its own document
  **before screens are planned**, or you build an interface onto nothing. Mark the trigger dead, do
  **not** forbid it: data may appear, and silence leaves him waiting for months.
- 🔒 **A rule moved ahead of its data looks like it works.** ✗ a "no consent" catch sat in the code for
  three stages and refused nobody, because the field was not being fetched. **Acceptance for a rule is
  a refusal that fired on a real person**, never its presence.
- 🔒 **Safety catches live in the DOMAIN MODEL, not in the route.** Duplicate a rule into the route and
  the scheduler that one day calls the same function outside HTTP runs without any catches.
- 🔒 **Reference data is born from FACT, not from a directory**; **the key binding a row to its history
  is never renamed** — rename it and the row detaches, numbers zeroing out with no explanation;
  **counts are computed, not stored.**
- 🔒 **A foreign DBMS limitation does not move together with its workaround.** ✗ the original merged
  three queries in JavaScript and said why in its own code — its database was strict about grouping.
  **Read the REASON the author wrote down, not the shape of the code.** It swings both ways: changing
  databases silently breaks what was moved literally.
- 🔒 **A number never measured has no right to render as a digit.** "Measured and empty" and "not
  measured" are different facts, and the SCREEN must tell them apart, not only the code.
- 🔒 **Name your disagreement with the original out loud**, leaving the owner the right to reverse it:
  *"this is my decision, said here; correct me if you see it otherwise"*.

## 9. The queue, and what you write down

🔒 **An agreed queue is a hypothesis, not a schedule.** In the real move one step was born from a defect
the audit screen found, one was pushed back by the owner, one was never in the queue at all. **Unplanned
steps are the NORM: record each the moment it appears, with its cause** — otherwise the cost of the move
is understated and the next estimate lies, always downwards.

🔒 **Defects of the original are named in the step** — a line "what we do NOT repeat" — never carried
over in silence.

🔒 **The wording of an acceptance is part of the instruction, and a bad one invites a bad proof.** ✗
"the route shows its page title" invited searching the response body — and the menu prints every page's
label on every page. The wording that works demands **distinguishability**: the same check on a
neighbouring address must give a different answer.

## 10. Read the account once, before your first migration

`ACCOUNT.md`, beside this file. It is the same migration told **from the owner's side**, in order, from
the first minute to stage 19 — what he believed when he started, where his picture of the job was wrong,
which of his own decisions he reversed, and at which stage each realisation arrived.

**Why it exists next to a skill.** This file says WHAT to do. The account says **what the process feels
like from inside and in what order understanding arrives** — which is exactly what a list of laws cannot
carry, and what explains why these laws and not others. Read it once; do not load it every session.

## 11. What this skill does not know

It was assembled from **one** migration: a CRM-fed loyalty service, PostgreSQL → this stack, one
country, one owner. **Phases A and B and all ten probes are stack-independent** and should hold
anywhere. **The order inside phases C and D reflects that product's shape** — a project whose core is
not automation over imported records may legitimately reorder 15–18. Reordering is a decision to state
out loud, not a silent liberty.

## Proof

Two proofs from different planes, and for a migration one of them is almost always **the same number
obtained twice by different routes** (probe 9). The build is never one of the two.
