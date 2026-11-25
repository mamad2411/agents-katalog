---
name: build-product-with-owner
description: >
  The path from confirmed cases to a working prototype, walked together with the owner. Load it the
  moment a case is confirmed and you are about to build something from it, when the mode is `cases`,
  and when the owner says "let's start" / "build it" / "what's next" — and again at the start of every
  session of such a product, because this path outlives dozens of them. It carries what nothing else
  does: the honest pact that opens the work, the four decisions that must be made before the first
  route, how the furniture (drawer, top menu, footer) is designed rather than inherited, how long an
  iteration may be, and where the prototype line runs. Who may confirm a case and where the queue lives
  is `use-use-cases`; this file does not repeat it.
---

# build-product-with-owner

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.
>
> 🔒 One boundary: the freedom is about **HOW** you build, never about whether the work is recorded as
> a step and the state written down.

## 0. Read first, do not restate

| Skill | Already carries |
|---|---|
| `use-use-cases` | who may confirm a case, where the queue lives, that a step names its case |
| `use-products-config` | the dossier: record, phases, the pages plan, four roots per product |
| `use-development-steps` | how a step is carried, the handover, the closing report |
| `place-page-in-menu` | the MECHANICS of menus — two sources, which one is speaking |
| `use-roles` · `use-multi-lang` · `use-static-pages` · `use-dynamic-pages` | how each decision below is IMPLEMENTED |

**This file is the PATH.** It says what happens in what order, what only the owner can answer, and how
small a piece of work may be. It links to the skills above; it never copies them.

---

## 1. 🛑 The pact — the first thing you do, and it is a gate

Confirmed cases exist. Before anything else, tell the owner plainly what kind of work this is going to
be. Your words, this meaning:

> Your cases are ready, and from here we build together — I cannot do this part alone. Not because the
> work is hard: because a product stands on decisions that are in neither the cases nor the code. Who
> logs in and what each of them may do. Which languages. What a search engine must see. What this
> business actually needs. You know those; no model derives them.
>
> Here is how we will work. Small pieces. After each one you get a link, you open it, you look, you
> say what is wrong. At the beginning the pieces are deliberately tiny, so that you see your project
> as early as possible rather than trusting me on faith.
>
> First I will ask you four things. Then we build the skeleton and you walk it. Then one case at a
> time, until every case you confirmed is true on your screen.

🔒 **Say this softly and once.** It is not a disclaimer and not self-deprecation — it is the honest
shape of the work, and a person who does not hear it expects a finished product tomorrow and reads
every question of yours as incompetence.

🔒 **Wait for an answer in words.** "Yes, let's go" is the gate. Without it you are guessing that he
agreed to a way of working he never heard described.

**What you carry alone, and say so:** the architecture, the code, the gates, the proofs, the
accounting, the search for what already exists instead of building it twice.

---

## 2. This product is not the first — the map and the dates

🔒 **Before planning anything, read every dossier in `PRODUCTS-CONFIG/` and write out the dates.**
`createdAt`, `updatedAt`, `confirmedAt`. Then **name out loud the new product's relation to each
existing one:**

| Relation | What follows |
|---|---|
| independent | nothing shared beyond `components/` and `lib/` |
| reuses code | name WHAT, and that moving something shared is declared in the step |
| continues | the earlier product's decisions apply here until the owner says otherwise |
| replaces | ask directly what happens to the old one — it does not disappear by itself |

**Why the dates decide it.** Two products can hold contradictory decisions about the same thing; the
later `confirmedAt` is what the owner believes NOW. Without the dates you will argue from the version
that happened to be read first.

✗ Silence here builds a second copy of something already built — and the copy is found months later,
by which time both have users.

---

## 3. Four decisions, before the first route

Each one goes into `development-docs/PASSPORT.md` — its sections and start light are defined in
`CLAUDE.md` § *Your memory*. **Write the owner's words verbatim, with the date.**

| # | Decision | Passport § | Why it cannot wait |
|---|---|---|---|
| 1 | **roles and access** | §3 | decides which layer a route lives in, which permission group it joins, what lock its door carries, what a guest sees — getting it wrong relays the skeleton, not a page |
| 2 | **languages** | §4 | the set comes from this project's CONFIG; a language added later is a move of every dictionary |
| 3 | **static against dynamic**, page by page | §5 | what a crawler and a person without JavaScript must see; a `force-dynamic` at the root makes the whole subtree dynamic |
| 4 | **furniture** — drawer · top menu · footer | §6 | §4 below: it is the one thing nobody has ever designed |

🔒 **How you ask — a rule, not politeness.** The answer **follows** from the cases → do not ask from
zero: state your assumption out loud ("here is what I assume, please confirm"). It does **not** follow
→ ask him to state it plainly, with no guesswork and no "I will take this for now".

🛑 **No answer is a lawful stop**, announced together with what becomes impossible. ✗ a role chosen "for
now" becomes permanent, and every door built on it has to be rebuilt.

**Three of the four are invisible to him**, so say what each one costs in his terms: roles decide who
can break what; languages decide who can read the site; static decides whether search finds it at all.

---

## 4. The furniture — three questions, and "not needed" is a real answer

**Nobody has ever designed this.** In every project so far the drawer, the top menu and the footer
arrived from the template and stayed by inertia. They are not one thing, and they are not decided
together.

| Element | The question you ask | What decides it |
|---|---|---|
| **footer** | "which of your own pages belong down here?" | legal and service pages belong to every project and are never removed — you only ask about HIS content |
| **top menu** | "what does a visitor who has not logged in need to reach?" | the public layer. A one-page product may legitimately have no top menu at all |
| **drawer** | "who sees this, and which of them needs a shortcut?" | 🔒 **follows from the ROLES decision, never the reverse** — the drawer lists groups, and the groups come from the roles |

🔒 **The drawer is courtesy, not protection.** The lock is in the group's `layout.tsx` and in the data
doors; the entry only shows the road to somebody who already has access. An entry names its GROUP, not
a list of roles — copy the roles in and it will one day either tease with a refusal or hide something
reachable.

🔒 **Ask about placement as a QUESTION, never as a statement.** "Shall I put it in the administration
drawer?" — because the answer is sometimes no: a page can be a step of a wizard, the target of a link
in an e-mail, or part of another page, and a menu entry would be wrong for it.

**Mechanics live elsewhere:** which of the two menu sources is speaking (`nav.top` / `nav.footer` in
the panel against the repository's defaults) is `place-page-in-menu`, and it matters — once the owner
has pressed Save in the panel even once, editing the repository default changes nothing a visitor sees,
with no error anywhere.

---

## 5. The first link, as early as possible

A skeleton that RUNS, plus the furniture from §4. Every route answers, every heading is its own, the
navigation walks.

**Ends with:** the owner opens one link and reaches every address of his product **by clicking**,
without typing an address by hand. Nothing is finished inside; that is the point.

🔒 **Do not improve the skeleton before he has walked it.** The walk is the cheapest moment he will ever
have to say "this page should not exist" or "where is the one for X" — and the answer costs a folder
rename now, a rebuilt tree later.

---

## 6. The size of an iteration is a rule, not a preference

🔒 **An iteration ends with something the owner can SEE by following a link.** Not "half the form is
written" — "the button is there and it saves".

**The first iterations are the shortest of all**, deliberately. That is where a person decides whether
he trusts the process; three days of silence followed by something large is how trust is lost, even
when the large thing is good.

Cannot make it visible? Then it is not an iteration — it is a piece of one, and the boundary is in the
wrong place. Look for the line where something becomes true on screen.

**After each one, three sentences:** what is now true · the link · what you plan next. Then stop and
let him look.

---

## 7. Cases, one at a time

**Order is not chosen for the convenience of the code.** First goes the case that makes the essence of
the product visible — the one he would show someone to explain what this thing is. A product whose
first working screen is its settings page teaches its owner nothing.

**Closing an iteration, use the question from `use-use-cases`:** not "does it work" but **"what
promised in this case is now true"**. Name the case's slug and quote the promise.

🔒 **A request that fits no confirmed case is a FORK, not a refusal.** He asked for something real. Say
plainly that it belongs to no case, and offer both roads: add it as a case in the panel (his intake,
his confirmation), or do it as it stands and record that it answers none. **Never build it silently
into a case it does not belong to** — that is how a case stops meaning anything.

---

## 8. The prototype line

🔒 **Prototype = every confirmed case is true on the owner's screen, and no stub is left.**

Proved by **enumeration**, not by a summary: list the cases, one line of answer each. "Broadly ready"
is not a state.

| Case | What is true on screen | Where |
|---|---|---|

**A stub that survives to the demonstration is the worst outcome of this whole path** — it makes
everything beside it suspect, including what genuinely works.

---

## 9. After the prototype — a different kind of work

What comes next is real and usually larger: strengthening what exists, or adding external tools to
extend it. **Both are NEW CASES, not a continuation of this path.**

This matters because the path has an end. Say it out loud when you reach it: *the prototype is done,
here is what it does, and from here we work case by case.* A path with no end quietly becomes a project
with no delivery.

**And the path starts again from §1 for the next product** — with §2 now carrying real neighbours.

---

## 10. The traps of this path

- ✗ **A decision taken silently on his behalf.** The most expensive thing here, because it looks like
  progress. Whenever you notice you are choosing rather than implementing, stop and ask.
- ✗ **A page nobody can reach.** A page with no incoming link exists only for whoever types the
  address. Ask where it is found — the rule and the table are in `use-static-pages`.
- ✗ **Furniture pointing at nothing.** Menus are not checked by any gate; a deleted or renamed page
  leaves its entry behind, and **a link to nowhere is worse than a missing page** — nobody looks for a
  missing page, but a menu entry gets clicked.
- ✗ **An iteration that grew.** If you cannot say in one sentence what he will see, it grew. Cut it.
- ✗ **Reporting the build.** A green build is not a proof of behaviour, ever. Two proofs from different
  planes, one carrying a negative control — `use-testing`.
- ✗ **The passport left behind.** Decisions arrive during the work, not only at §3. A decision recorded
  only in a chat gets reversed by the next session, silently.

## Proof

Two proofs from different planes, and for this path one of them is almost always **the owner having
looked**: the link, and what he said about it. His word is not a substitute for a measurement — it is
the other plane, and it is the one that answers "is this what was ordered".
