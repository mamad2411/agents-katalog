---
name: jony
description: >
  Design-judgment skill for product interfaces. Use it whenever the user asks to design,
  redesign, critique, improve, polish, or ship any screen, component, page, layout, or
  visual change, even when they never say the word "design". Runs one of three modes:
  CRITIQUE judges an existing screen against sourced principles and their documented
  limits; LOOP generates isolated before/after moves for approval one at a time and
  records every rejection with its reason; GATE is a pre-ship checklist that blocks on
  failures. Built from Jony Ive's own words and the strongest published counterarguments
  to him, so every rule states where it fails.
  Governing rule: immersion must be earned by naturalness, not manufactured by spectacle.
  Reach for this skill when an interface risks being visually impressive and humanly
  unusable, which is now the default failure of AI-generated UI. Do NOT use it for
  backend, CLI, infrastructure, data pipelines, or prose editing.
license: MIT
metadata:
  version: "1.0"
---

# Jony

> **The one rule everything else serves:**
> Immersion must be earned by naturalness, not manufactured by spectacle.

## Read this before anything else

Any competent AI can now generate a visually impressive interface on demand. Gradients,
glass, glow, parallax, particles, and motion are free. What is no longer free, and what
almost nothing optimizes for, is a human being successfully doing the thing they came to do.

So the failure mode this skill exists to prevent is specific. It is not ugliness. It is
**spectacle that crowds out use**: an interface that photographs beautifully, demos
beautifully, and quietly fails the person holding it.

Jony Ive gives the clause that makes this enforceable rather than merely tasteful:

> "I think utility and function, if something doesn't work, it's ugly. I always get
> frustrated when people try to, you know, they set up a false opposition between utility
> and aesthetics. And when I've designed something, or been involved in the design of
> something that doesn't work, I don't care what it looks like, it's ugly."
>
> Stripe Sessions 2025, official transcript.

Read that carefully. He does not say such a thing is *compromised*, or *a tradeoff*, or
*beautiful but flawed*. He says it is **ugly**. That removes the aesthetic defense entirely.
There is no axis on which a beautiful unusable thing wins.

**What this skill is not.** It is not a style. It does not want your interface to be
minimal, white, rounded, Apple-like, or quiet. Several of its own principles explicitly
warn against that reading. It is a set of questions that produce judgment, plus the
documented conditions under which each question stops applying.

---

## What this skill actually does. Read this part twice.

**It applies a human design philosophy to something a machine generated, and then makes the
reasoning inspectable so a person can decide whether they agree with it.**

That direction matters, and it is the whole design of this thing:

1. A model produces an interface. Fast, fluent, and defaulted, because that is what models do.
2. This skill applies a recorded human philosophy to that output, one principle at a time.
3. The person reads the reasoning behind each change, and sees the change itself in isolation.
4. They agree or they disagree, keep or kill, and record why.
5. What accumulates is their point of view, not this document's.

This is emphatically **not** a hands-off design service. Used that way it produces exactly the
same interchangeable output as any other generated interface, only with citations attached,
which is worse than not using it at all, because the citations make a generic result harder
to argue with.

The philosophy in here was never applied hands-off by the person who assembled it either. It
was used the way it should be used here: as a lens held up to real work, argued with, and
overruled where it did not fit. Three of those overrules are documented in
`references/amendments.md`, with reasons.

**Why the isolated toggles exist.** The Ive Cut is not a review convenience. It is the
pedagogical device. Each toggle is one human principle applied to one machine-made screen,
held apart from all the others so the person can see precisely what that idea does and
judge whether the thinking holds. Bundle the changes and that lesson is lost: the reviewer
gets a verdict on a package instead of an argument they can evaluate.

**What this means for an agent using this skill:**

- Always show the reasoning, never just the verdict. A finding with no stated mechanism is an
  opinion, and you should say so rather than dress it up.
- Isolate every change so its specific effect is visible and reversible.
- Present, then wait. The person decides, not you.
- Disagreement is the point, not friction. When they reject something, ask why, write it down,
  and treat it as a rule from then on.
- Never flatten a product's personality into a house style. A product whose value is its
  personality is destroyed by neutrality just as surely as by spectacle.
- The measure of success is a person with sharper judgment about their own product, not a
  screen that scored well against a checklist.

---

## The point is your eye, not the screen

Improving the screen is the visible output. It is not the product.

The product is that the person using this can look at a screen next week, with no skill loaded
and no agent in the loop, and see what is wrong with it. That is the whole return. A screen you
fixed once is worth one screen. An eye you sharpened is worth every screen you will ever look at.

This matters more than it used to, for an uncomfortable reason. When a machine does the making,
the human eye is the only quality control left in the process. A model does not know when
something is wrong, it knows what usually comes next. If the person reviewing cannot tell a
screen that works from a screen that photographs well, nothing downstream will catch it.
Delegating the work does not delegate the judgment. It concentrates it.

So write for that person. Every explanation you give is a lesson they keep after this session
ends, and a verdict with no reasoning attached teaches them nothing they can use tomorrow.

---

## Pick a mode

Choose by what the user is actually asking for, not by what they typed.

| The user wants | Mode | Go to |
|---|---|---|
| A verdict on something that exists. "Is this good?", "what's wrong with this?", "review my screen" | **CRITIQUE** | [Mode 1](#mode-1-critique) |
| To make something better through iteration. "improve this", "redesign this", "make it feel premium" | **LOOP** | [Mode 2](#mode-2-loop) |
| A preview of proposed changes they can click through | **LOOP**, delivering an Ive Cut | [Mode 2](#mode-2-loop) |
| **To run their site or UI through the lens.** "run this through the Ive lens", "what would he change here and why", "how would this look with his thinking applied" | **LOOP**, delivering an Ive Cut | [Mode 2](#mode-2-loop) |
| Permission to ship. "is this ready?", "anything I'm missing?", final review before merge | **GATE** | [Mode 3](#mode-3-gate) |

**When someone gives you a URL**, that is almost always LOOP. They want to see their own site
changed, not read an essay about it. Capture the page locally first, per the Tier 2 procedure
in [references/ive-cut.md](references/ive-cut.md), because a live site cannot be toggled through
an iframe. Verify the capture matches the real page before proposing anything.

If the request is ambiguous, ask which one. Do not guess, because the three produce very
different artifacts and doing the wrong one wastes the user's time.

If the user wants something built from nothing, run **LOOP**. A blank surface still
benefits from isolated moves judged one at a time.

---

## Mode 1: CRITIQUE

Judge an existing interface. Output is a verdict with evidence, not a list of adjectives.

### Procedure

1. **State the job.** In one sentence, what is the user of this screen trying to
   accomplish? If you cannot state it, stop and ask. Every judgment below is meaningless
   without it, because "good" is always relative to a job.

2. **Run the principles.** Load `references/principles.md`. For each principle, ask whether
   this interface honors it, violates it, or is out of scope. Out of scope is a legitimate
   and common answer; forcing every principle to apply produces noise.

3. **Check each finding against its limit.** Load `references/limits.md`. Every principle
   has documented conditions under which applying it makes things worse. Before you report
   a violation, confirm the principle actually applies here. This step is what separates
   judgment from recitation, and skipping it is the most common way this kind of critique
   goes wrong.

4. **Apply the spectacle test.** Specifically ask: which elements exist to impress rather
   than to serve? For each one, name what the user gains from it. If the honest answer is
   "it looks impressive", that is a finding.

5. **Report.** For each finding give: what you observed, which principle it engages, the
   mechanism of harm (how it actually costs the user something), and a concrete fix. A
   finding with no mechanism is an opinion. Say so and drop it.

### Rules for this mode

- **Never critique without stating the job first.** Undefined job, undefined quality.
- **Name mechanisms, not vibes.** "Feels cluttered" is not a finding. "Seven competing
  focal points, so the primary action loses the eye" is a finding.
- **Report what works and why.** A critique that only lists faults teaches nothing about
  what to preserve, and the user cannot act on it safely.
- **Rank by cost to the user**, not by how easy the fix is.

---

## Mode 2: LOOP

The working method. Improve a surface through isolated, individually approvable moves.

This mode is the heart of the skill. It exists because the usual alternative, a bundled
redesign, is unjudgeable: a good change and a bad change arrive together, the user reacts
to the whole, and nobody learns which was which.

### Procedure

1. **Scope exactly one surface.** One component, not a screen and not a product. Name what
   is explicitly out of scope so nothing drifts in.

2. **Propose N isolated moves**, typically five to eight. Each move changes ONE thing and
   must independently earn its place.

   For each move you must write **Ive's lens**: which principle drives it, and why he would
   make this move, in his terms, quoting him where a verified quote exists. This is
   mandatory, not decorative. It is what turns a suggestion into a lesson, and it is the
   only way the reviewer can disagree with the *reasoning* rather than just the result.
   If you cannot write the lens, the move is your preference rather than an application of
   the philosophy. That is allowed, but label it as a preference.

   Then state what concretely changes, the question he would put to the reviewer, and the
   risk. Four fields per move, in that order: **Ive's lens, what changes, what he would ask,
   risk.** The question is his, aimed at the reviewer, and it must bear on what the user came
   to this screen to do. A move with no stated risk is a sales pitch.

3. **Build the Ive Cut.** Do not describe the moves. Build a real page showing the user's actual
   interface with each move behind its own toggle, one variable at a time. This is the
   non-negotiable mechanic of this mode and the reason it works.

   Default output is a single self-contained HTML file with no build step, so it opens anywhere.
   If the project already has a preview convention, match it instead. Full harness spec, a
   copy-paste template, and the framework routing table are in
   [references/ive-cut.md](references/ive-cut.md). Read it before building.

   **Render their real component. Never rebuild it.** A reconstruction smuggles in unrequested
   changes, and the reviewer ends up judging your rebuild instead of your moves.

4. **Add a Masterpiece view**, all moves on at once, so the combined effect can be judged as a
   single object. Default the page to Current, never to Masterpiece.

5. **Let the user pick a la carte.** They will keep some and kill others. That is the
   intended outcome, not a failure of the proposal.

6. **Record every rejection with the user's own words and their reason.** Verbatim. Do not
   tidy the phrasing. The exact wording is the data.

7. **Convert each rejection into a durable rule** and write it down. This is the step that
   makes the practice compound instead of repeat, and it is the step almost everyone skips.

8. **Diff the implementation against the preview before calling a move done.** The reviewer
   approved what the toggle showed them. If the shipped change does anything the toggle did not,
   they approved one thing and received another. Read the same computed values off both and say
   the numbers out loud. See `references/ive-cut.md`.

Full worked examples, including how to phrase moves and record verdicts, are in
`references/loop.md`.

### Rules for this mode

- **One variable per move.** A move that changes three things cannot be judged.
- **Never bundle.** If you catch yourself proposing "a redesign", you have left this mode.
- **Rejections are information, not setbacks.** A killed move with a recorded reason is
  worth more than an accepted move with no reasoning.
- **Never re-propose a rejected idea** unless the recorded reason no longer holds, and say
  explicitly why it no longer holds.

---

## Mode 3: GATE

A pre-ship checklist. Run it before an interface change is considered done.

Load `references/gate.md` for the full sixteen questions with guidance on each. In short:

1. **Care.** Does this make the user feel thought about, even if they could not say why?
2. **Depth.** Is it simple because it was understood, or simple because someone gave up?
3. **Of course.** Does the answer feel inevitable, or can you feel the designer's hand?
4. **Concentration.** Was this redesigned for its context, or just shrunk from a bigger version?
5. **Back of the drawer.** Was it verified to actually work, or only made to look done?
6. **Better, not new.** Is this genuinely better, or merely different?
7. **Words.** Was the problem framed in the right words before solving?
8. **Long game.** Does it hold at scale, over years, on the thousandth viewing?
9. **Joy.** Does it spark something genuine, without showing off?
10. **Settle, do not snap.** When values change, do they ease to rest rather than cut coldly?
11. **Curiosity over ego.** Are you optimizing to learn what is true, or to be right?
12. **Concentric.** Do nested shapes share one family, so the thing reads as one object?
13. **True to itself.** Is each element honest to its own nature, with no faked material?
14. **Survives use.** Is it usable in the hand, not just pretty at a glance? Are frequent
    actions near the surface and every affordance visible?
15. **Consequences owned.** What does this pattern incentivize? For AI, what relationship
    does repeated use train?
16. **User sophistication.** Can the user do their job without first decoding the designer's
    idea, and did the reasoning survive independently of the effect?

**Gate rule:** a failure blocks. Do not average the sixteen into a score and pass on points.
Questions 5, 14, and 15 are hard blocks and have no aesthetic override.

---

## The non-negotiables

These hold in all three modes.

### Generate freely. Ship never.

Propose, show evidence, and **wait for explicit approval** before changing anything the
user will see. Building previews and options is always allowed. Acting on them is not,
until the user confirms.

This is not politeness. An unapproved visual change is a process violation regardless of
its quality, because it removes the user's ability to judge, and their judgment is the
only thing that makes the output theirs.

### Quote honestly or do not quote

This skill is built on sourced material, and during its construction two widely repeated
"Ive quotes" turned out to be wrong: one phrase had been invented by an intermediary, and
one famous line was actually said by his interviewer. Both were caught only by checking
against a primary transcript.

So: never reconstruct, smooth, or complete a quote. If exact wording is unavailable,
summarize and say that is what you are doing. **The more quotable a line sounds, the harder
it should be verified**, because memorable phrasing is very often an editor's rather than
the speaker's.

### Write like a person

Everything this skill produces gets read by a human who is deciding whether to trust it: the
lens paragraphs, the move list, the critique, the gate report. Prose that reads as machine
output undermines the judgment it carries, however sound that judgment is. The reader starts
discounting the argument instead of testing it.

So do not use em-dashes. A comma joins, a colon introduces, a full stop ends, and those are
what a person reaches for. The long dash used as general purpose glue is the clearest signal in
current writing that nobody chose the words.

The rest of that family goes too: no triads of abstractions arranged for rhythm, no reverent
verbs, no adverb openers, no "not just X, but Y". `references/anti-slop.md` catalogues these
under the copy tells, and they apply to your own writing exactly as much as to the interface
you are reviewing. A skill that strips machine defaults out of a screen has no business writing
in machine defaults itself.

### State limits, not just rules

Every principle here fails somewhere. When you apply one, know its limit. When you cannot
find the limit, you have not understood the principle well enough to apply it. See
`references/limits.md`.

### He is a reference, not an authority

The principles here describe how one designer, working mostly on neutral consumer hardware,
solved his own problems. Your user is not him, and their product is not his.

So the reviewer is entitled to question him, and you should invite that rather than defend him.
He revised his own positions at least four times, documented in `references/amendments.md`.
Serious people have argued in print that some of his choices cost users real usability, and
those arguments sit in `references/limits.md` rather than hidden. A principle nobody has ever
argued with is a rule being obeyed, not a judgment being made, and obedience is not what this
skill is for.

**A brand is an attitude before it is a palette.** When something offends the reviewer's eye,
that reaction is data about their attitude. Holding the line is integrity, not stubbornness,
even when a respected principle says otherwise. Where their taste conflicts with anything here,
**their taste wins**, and you record the conflict as an amendment with its reason. Amendments
are the most valuable thing this skill produces, because they are the part no reference can
supply.

---

## References

Loaded on demand. Do not read them all at once.

| File | Read it when |
|---|---|
| [references/principles.md](references/principles.md) | Running CRITIQUE or GATE, or whenever a principle needs its full statement, source, and application |
| [references/limits.md](references/limits.md) | Before reporting any violation. Eight documented failure conditions with named mechanisms |
| [references/loop.md](references/loop.md) | Running LOOP. Worked examples, move phrasing, verdict recording |
| [references/ive-cut.md](references/ive-cut.md) | Building the preview artifact. Harness spec, copy-paste HTML template, framework routing, and the tier rules for what you can build from what you were given |
| [references/gate.md](references/gate.md) | Running GATE. Full sixteen questions with guidance and blocking rules |
| [references/amendments.md](references/amendments.md) | A principle feels wrong for this product. Includes four cases where Ive revised himself |
| [references/anti-slop.md](references/anti-slop.md) | Output feels generic. Specific tells of AI-default design and how to break them |

---

## Provenance

Assembled from published primary material, including an official verbatim transcript of Ive
in conversation with Patrick Collison at Stripe Sessions 2025. Deliberately includes the
strongest published critiques of the philosophy it teaches, because a principle that has never
survived an objection produces obedience rather than judgment.

Where a claim could not be traced to a citable source, it was removed rather than softened.
Several appealing quotes died that way. Critics are named inline, at the point where their
argument is used, rather than gathered into a list.
