---
name: social-calendar
description: >
  Use when a business has to start posting and nothing is written yet, or when content
  gets drafted one post at a time and the voice drifts. Also when someone has topics but no
  calendar, or a calendar but no finished copy.
  Triggers on: "plan my social content", "content calendar", "write my social posts",
  "editorial calendar", "calendario de contenido", "planea mis publicaciones", "posts para redes".
  Self-contained: no other skills required.
version: 1.0.0
author: GrowthLab (growthlab.mx)
license: MIT
---

# social-calendar

> GrowthLab-original content. MIT licensed (see repo `LICENSE`).

> **Purpose:** Get two weeks of finished social content out of your head and into a file — not
> a list of topics someone still has to write, but captions you can paste. One channel, two
> formats, done in one sitting.

**No skill dependencies.** This skill never calls another skill. It *reads* two optional context
files, `product-marketing.md` and `design.md`, and works without them — see Step 1. It pairs with
`content-humanize` as a final gate at Step 6 if you have it.

---

## The set

This skill is one of five in the same repo. Two of them write a context file; three read it.

`product-marketing-md` writes `product-marketing.md` (what you sell, to whom, why they buy).
`design-md` writes `design.md` (how you look and how you sound). Those two files are read by
`landing-md`, `social-calendar` and `content-humanize`.

**You need none of them to run this one.** They are separate downloads from
[github.com/jeremidelacruz/growthlab-skills](https://github.com/jeremidelacruz/growthlab-skills),
and if this file is all you have, everything below still works.

---

## Why this works

Most content plans die one of two ways. Either they are a list of topics that someone still has
to turn into posts, so nothing ships. Or they get written one post at a time over three weeks,
so the voice drifts and the last one sounds like a different company.

This fixes both by doing the whole stretch in one sitting, with the audience and tone held
constant, and by finishing each piece instead of leaving it as a prompt for later.

Two weeks is the unit on purpose. Long enough that you have to think about mix and sequence,
short enough that you will actually finish it.

---

## Inputs

| Input | Required | Where it comes from |
|---|---|---|
| Start date and channel | Yes | You |
| 5–10 topics, offers or key dates | Yes | You, or drawn from the pillars in Step 2 |
| Audience, offer, tone | Yes | `product-marketing.md` if it exists, otherwise Step 1 asks |
| Visual rules | No | `design.md` if it exists |

---

## The source rule

Everything you write about the business, its customers or its competitors has to trace back to
something you were given. **Not just numbers. Claims too.**

A claim is anything a reader could check and find false:

- how the service works, or what is included in it
- a security, safety or privacy property ("the connection is read-only")
- a turnaround time, a guarantee, a policy
- what a competitor believes, charges or is bad at
- what the customer feels, fears or wants

Three moves, in this order:

1. **Cite it.** It came from a context file or the person told you. Use it.
2. **Cut it.** No source? Delete the sentence. Replacing it with a vaguer sentence is not a fix.
3. **Mark it.** If the piece structurally needs something you were not given, write it and mark
   that line `[ASSUMED — confirm before publishing]`.

**Nothing unsourced and unmarked ships.** A marked guess is a question for the owner. An unmarked
guess is a promise they get held to.

> This rule is wider than it used to be for a reason. In testing, a run of this skill published
> "the connection is read-only" about a fintech product, and another asserted that a mechanic
> keeps every removed part on a labeled tray. Neither is a number, so a numbers-only rule waved
> both through. Both are promises somebody would have been held to.

### When you cannot ask

If you are running unattended, or inside someone else's workflow, and the questions below cannot
be answered: **do not stop, and do not assume silently.** State the questions, answer each with
the most defensible assumption you can support, mark them, and put them in an `## Assumptions`
block at the top of what you deliver. The reader needs to see the guesses before they see the work.

---

## Process

### Step 1 — Load the context

Read `product-marketing.md` if it exists and pull: who the audience is, what you sell, the tone,
and the words customers actually use. If it does not exist, ask four questions and do not start
before you have answers:

1. Who reads this, specifically? (Not "small businesses" — the person, and what they are worried about.)
2. What do you sell them, and what does it cost?
3. What should these two weeks accomplish? Pick one: awareness, leads, or launch.
4. What must never appear? (Topics, claims, competitors, anything legally restricted in your category.)

Hold these constant for the entire batch. Re-establishing context per post is what makes a
batch of posts sound like four different writers.

### Step 2 — Set the pillars

Four pillars, no more. Every piece belongs to exactly one, and you should be able to say which
without thinking. A default set that works for most businesses:

| Pillar | What it does | Roughly |
|---|---|---|
| **Teach** | Something useful the reader can act on today | 40% |
| **Prove** | Evidence you can do the thing: results, process, before/after | 20% |
| **Position** | What you believe that others in your category don't | 25% |
| **Human** | The people, the workspace, the mistakes, the reasons | 15% |

Adjust the mix to the goal: a launch leans Prove and Position, a quiet stretch leans Teach.
Write the mix down. It is what stops week two from being five sales posts.

**When the brief is too thin to fill a pillar, the source rule wins.** Prove wants evidence and
Position wants a belief the business actually holds; on a one-paragraph brief you will have
neither. Do not manufacture them to fill the slot. Write the piece as a marked shell — the angle,
the structure, and `[ASSUMED — confirm before publishing]` on the claim it needs — and tell the
owner that piece is waiting on them. A labelled hole is a question they can answer in a minute.
An invented belief is one they find out about from a customer.

**The percentages will not divide evenly, and that is fine.** Six pieces cannot express
40/25/20/15. Treat the mix as an ordering, not arithmetic: **most** pieces in the biggest pillar,
**at least one** in every pillar, **never more than half** in any single one. At six pieces that
lands near 3/1/1/1. Write the real counts in the header, not the percentages you aimed at.

### Step 3 — Build the calendar

Pick **one channel** and a cadence you could sustain for six months, not one. Three good pieces
a week beats seven rushed ones.

For each slot decide: **date . pillar . format . topic . call to action.**

Two formats. Alternate them as a default, and break the alternation when the content asks for
it — a carousel needs an idea with parts, and forcing one on a piece that doesn't have parts
produces eight slides of filler. Roughly a third carousels is a healthy ratio for an account
that has never posted.

- **Feed post** — single image or text, one idea
- **Carousel** — one idea per slide, 5 to 8 slides

One call to action per piece. Two is not twice the conversion, it is half.

### Step 4 — Write every piece

Draft all of them before polishing any of them. Polish per piece and the voice drifts.

**Feed post**

```
Hook       — the first two lines, all that shows before "see more"
Body       — 3–5 concrete points, or one story with a turn in it
Close      — one call to action, phrased as a thing to do
Hashtags   — 5–10 specific ones, no generic walls
```

Hook formulas that hold up. Rotate them; do not use one twice in two weeks:

- **Curiosity** — "What nobody tells you about [thing]."
- **Story** — "Last week a client asked us [question]." *(only if it happened)*
- **Useful** — "How to get [result] without [the usual painful part]:"
- **Contrarian** — "We stopped doing [common practice]. Here's what changed."
- **Cost** — "This mistake costs more than people think."

**Carousel**

- Slide 1 stops the scroll: a claim, a number, or a question with a real answer coming
- Slides 2–N: one idea each, 15 words maximum on the slide, the rest in the caption
- Last slide: the call to action

### Step 5 — Say what the image should be

One or two sentences per piece, enough that someone else could make it without asking you: the
format and size, what is on it, and whether it is a photo or type only. If `design.md` exists,
name the exact colors and typefaces from it. If it does not, say so plainly rather than
inventing a palette.

### Step 6 — Check before you ship

- [ ] Every piece has one call to action, and it is a thing to do
- [ ] No two pieces open with the same phrase or the same hook formula
- [ ] Every pillar appears at least once, and no pillar takes more than half the pieces
- [ ] Every number, result or case is real — nothing invented to make a post land better
- [ ] Nothing from the "must never appear" list in Step 1 got in
- [ ] Read three captions aloud. If you stumble, rewrite that line

---

## Output

One file, named for the **start date**: `content-calendar-YYYY-MM-DD.md`. The day matters —
a span that crosses a month boundary has no single month, and two runs in the same month would
otherwise overwrite each other.

**Write it into the folder the person is working in, and say the full path when you hand it
over.** If you are running as a subagent, your working directory is inherited and is probably not
where this belongs — ask, or write it beside the context files you read, and say which you did.
A calendar that lands in a random folder is a calendar nobody finds.

```markdown
# Content calendar — March 3 to 16

**Goal:** <the one thing these two weeks are for>
**Pillars:** Teach 3 · Position 1 · Prove 1 · Human 1  ← real counts, not the percentages you aimed at
**Channel and cadence:** <channel, how many per week>

| # | Date | Pillar | Format | Topic | CTA |
|---|------|--------|--------|-------|-----|
| 01 | Mar 3 | Teach | Carousel | ... | Save |

---

## 01 · Mar 3 · Teach · Carousel

**Copy**
<the finished caption, ready to paste>

**Hashtags:** #... #...

**Slides:** <carousels only — one line per slide, 15 words max each>

**Image:** <one or two sentences>

**Notes:** <anything the scheduler needs to know>
```

Write the file into the folder you are working in, and say the path when you hand it over.

Then repeat the block for every piece. One file, everything in it, nothing left as a prompt.

---

## What this skill does not do

**It does not work unattended on a thin brief.** This is the honest one. The purpose line
promises captions you can paste; that holds when you brought real material — what you sell, what
you believe, something that actually happened. From a one-paragraph brief, obeying the source
rule strips out nearly everything specific, and what you get is a well-labelled questionnaire
wrapped around caption skeletons. That is the correct output, and it is not what "paste-ready"
means. Bring the material, or expect to answer questions.

It plans **two weeks, one channel, two formats**. That is a starter plan, and it stops there on
purpose:

- No video: no short-form scripts, no shot lists, no hooks written for sound-on
- No stories, no lives, no community management, no comment or DM handling
- No image production — it describes the visual, it does not build it
- No scheduling, no publishing, no platform integrations
- No analytics: it does not read what performed, so it cannot tell you what to make next
- No multi-channel sequencing, no repurposing one idea across platforms
- No decision about which organic post deserves paid budget

The hard part of content is not the first two weeks. It is month seven, when the obvious topics
are gone and the only way to pick the next one is to read what the last thirty did. That loop is
a different job than writing captions. It happens to be ours: [growthlab.mx](https://growthlab.mx).

---

## References & credits

**No third-party skill, framework or copyrighted text is reproduced here.** The pillar model,
the process, the hook formulas, the script structure and the output format are
GrowthLab-original, MIT licensed.

The general practices this skill organizes — content pillars, batching, hook-first writing for
mobile feeds — are common editorial knowledge documented widely across the social marketing
field. No single source is reproduced.

**Pairs with:** `product-marketing-md` and `design-md` (context files, this repo) and
`content-humanize` (copy gate, this repo). All three are optional; this skill runs without them.

**External tools:** none. No runtime, no dependencies, no API keys.

### About GrowthLab

These skills are the free half of a working method. [GrowthLab](https://growthlab.mx) is a
paid-media agency in México that runs its delivery on Claude Code — the context files, the
gates and the QA you just used are how our own client work ships. If you would rather have
the campaigns, the pages and the content *run for you* on top of this method, that is the
paid half: [growthlab.mx](https://growthlab.mx) · hola@growthlab.mx.
