---
name: product-marketing-md
description: >
  Use when an LLM is about to write ads, copy, emails or posts for a business and knows
  nothing about it — or when someone says the output "sounds generic", "could be any company",
  or "doesn't sound like us". Also when starting a new marketing project and wanting the
  context written down once instead of re-explained every time.
  Triggers on: "product-marketing.md", "marketing context", "set up context", "positioning",
  "who is my ICP", "describe my product", "contexto de marketing", "quién es mi cliente ideal".
  Self-contained: no other skills required.
version: 0.1.0
author: GrowthLab (growthlab.mx)
license: MIT
---

# product-marketing-md

> GrowthLab-original content. MIT licensed (see repo `LICENSE`).

> **Purpose:** Produce `product-marketing.md` — a compact context file that tells an LLM
> *what you sell, to whom, and why they buy* before it writes a single line for you. It is
> the business half of your AI context. The visual half is `design.md` (see the `design-md`
> skill). Neither works alone.

**No skill dependencies.** This skill never calls another skill; everything it needs is inline.

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

Ask an LLM for "a landing page for my product" and it will give you something that looks
finished and says nothing. Not because the model is weak — because you never told it who the
product is for, what problem it removes, or the exact words your customers use. So it fills the
vacuum with the average of everything it has read: fluent, generic, forgettable.

`product-marketing.md` removes the vacuum. It is the difference between:

| Instead of | You get |
|---|---|
| "write copy for my app" | copy aimed at *this ICP*, naming *their* problem |
| "make it sound professional" | your actual voice, with the words to use and the words to avoid |
| "our product is great" | a differentiator a competitor can't also claim |
| "customers love the speed" | the verbatim line a customer actually said |

The failure this prevents is not bad writing. It is *plausible, on-topic, and useless* — output
that passes a skim and converts no one, because it could be about any product in your category.

### The pair: `product-marketing.md` + `design.md`

They are two halves of one context, and they answer different questions:

| File | Answers | Skill |
|---|---|---|
| `product-marketing.md` | **What** you sell, **to whom**, **why they buy**, **how they talk** | this skill |
| `design.md` | **How** you look and **how** you sound (colors, type, logo, tone) | `design-md` |

`design.md` alone makes on-brand work that says nothing. `product-marketing.md` alone makes
sharp arguments that look generic. Together they make work that is *both* on-brand and on-message
— which is the only kind that sells.

Three skills in this repo read them: `landing-md` builds the page, `social-calendar` plans and
writes the month, `content-humanize` uses the voice to rewrite anything a model drafted. Write the
two files once and all three get sharper. Make reading them step 1 of every task.

---

## Inputs

Accept whatever the user has. In descending order of quality:

1. **A real conversation with the founder / marketer.** The highest-value source, because the
   words come out unpolished — which is exactly what you want (see "Capture verbatim" below).
2. **The live site + existing marketing** — homepage, about page, pricing, sales decks, old ads.
   Good for a first draft you then correct.
3. **The codebase / README** — for technical products, the docs often state the real use case
   more honestly than the marketing does.
4. **Nothing but a vague idea** — build a provisional file, mark every unknown `[TBD]`, and ask.

If you have more than one source and they disagree (the deck says "enterprise," the actual
customers are solo founders), record the conflict and ask which is true. Do not silently average
them — a blurred ICP produces blurred copy.

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

### Step 1 — Check for an existing file

Look for `product-marketing.md` in the project root and in `.agents/`.

**If you find one, check whose it is before you touch it.** Read only its first section and
compare the product and company named there against the business you were asked about. If they
do not match, that file belongs to someone else: **do not read on, do not merge, do not
overwrite.** Write a new file under a distinct name (`product-marketing-<business>.md`) and tell
the person both files now exist so they can decide what to do. A repo with several clients in it
is normal; silently merging two of them is not recoverable.

If it is the same business: read it, summarize what's captured, and ask which sections to
update — don't re-interview from zero.

If it doesn't exist, offer two paths and let the user pick:

- **Auto-draft** (faster): you read the site / repo / existing marketing, draft a v1, then ask
  *"what's wrong and what's missing?"* Most people prefer this.
- **From scratch** (higher fidelity): walk the sections below conversationally, one at a time.

### Step 2 — Gather, one section at a time

Don't dump every question at once. For each section: say what you're capturing in a sentence,
ask, confirm, move on. Push past polished answers to concrete ones:

- Not *"what problem do you solve?"* → **"What's the #1 frustration that makes someone go
  looking for you in the first place?"**
- Not *"who's your audience?"* → **"Describe the last customer who was a perfect fit. Role,
  company, what triggered the search."**
- Not *"what makes you different?"* → **"What can you say that a competitor honestly can't?"**

**Capture verbatim.** When the user says *"I was drowning in spreadsheets at 11pm,"* keep that
sentence in quotes. Do not upgrade it to *"struggling with manual data workflows."* The raw line
is the asset — it is how the customer's brain actually stores the problem, and copy written in
those words converts better than copy written in yours. A file full of clean paraphrases has had
the value polished out of it.

### Step 3 — Write the file

Use the schema in "Output" below. Fill only the sections that apply (a solo B2C product may skip
Personas). Mark anything unconfirmed `[TBD]` and anything unsourced `[SIN FUENTE — no publicar]`.
A neutral, filled example is in `references/product-marketing-template.md`.

### Step 4 — Confirm and place it

Show the file, ask what needs adjusting, then save it where the agent will actually read it
(see "How to use"). Tell the user: *"Every marketing task from now on should read this first —
run this skill again anytime to update it."*

---

## Output — the `product-marketing.md` schema

Emit these sections, in this order. Keep it tight; this is a context file, not a brand book.
Open with a one-line provenance note (source + date) so a reader knows how fresh it is.

```markdown
# Product Marketing Context — [Product / Company]

*Source: [conversation / site / repo] · Last updated: [date]*

## 1. Product
- **One-liner:** what it is, in one sentence a stranger would understand
- **What it does:** 2–3 sentences
- **Category:** the "shelf" customers look on (how they'd search for it)
- **Business model & pricing:** [with source for any price]

## 2. Ideal Customer (ICP)
- **Who they are:** role / company type / stage — be specific
- **Trigger:** what just happened that made them start looking
- **Job to be done:** the 1–3 things they "hire" you to accomplish
- **Not a fit (anti-persona):** who to turn away, and why

## 3. Problem
- **Core problem:** the pain before they find you
- **Cost of the problem:** time / money / stress it creates
- **Why current alternatives fall short:** (name them)

## 4. Competitors
| Competitor | How they position | Where they fall short for the customer |
|---|---|---|
| | | |

## 5. Differentiation
- **What we can say that they can't:** (must be honestly ours)
- **Why that matters to the customer:** the benefit, not the feature

## 6. Customer Language (verbatim)
- **How they describe the problem:** "[exact quote]"
- **How they describe us:** "[exact quote]"
- **Words to use:**
- **Words to avoid:**
- **Glossary:** terms specific to this product/industry

## 7. Voice
- **Tone:** 3–5 adjectives (keep any contrast, e.g. "confident, not hype")
- **Style:** direct / conversational / technical
- **Pairs with:** `design.md` for the visual + written identity rules

## 8. Proof (sourced only)
- **Results / metrics:** [each one WITH its source, or omit]
- **Named customers / logos:** [if allowed to use]
- **Testimonials:** > "[quote]" — [who]
> No source? It doesn't go here. See "the one hard rule."

## 9. Goals
- **Business goal:** the outcome that matters this quarter
- **Primary conversion action:** the one thing you want a visitor to do
- **Target metric (if known):** [with source]
```

---

## Verify before you hand it over

State the result of each check; don't just assert "done."

| Check | Fails when |
|---|---|
| **No invented numbers** | A figure appears without a source and without a `[SIN FUENTE]` flag |
| **ICP is specific** | "Small businesses" / "everyone" — not a person you could picture |
| **Verbatim language is present** | Section 6 has zero real quotes, only paraphrases |
| **Differentiator is honest** | Section 5 lists something a competitor could equally claim |
| **Anti-persona is sourced** | Section 2 names an anti-persona nobody stated, unmarked. An empty `[TBD]` here passes; an invented one does not |
| **Competitor claims are sourced** | Section 4 asserts what a competitor believes, charges or is bad at, without a source and unmarked |
| **Customer psychology is sourced** | Section 3 asserts what the customer feels or fears, with no quote and no mark |
| **Unknowns are labelled** | A guessed value is left unmarked instead of `[TBD]` or `[ASSUMED]` |
| **Provenance is recorded** | The reader can't tell where the file's claims came from |

**What a failure means.** A failed check is not a note, it is a stop. Fix it, or mark the value
and say so when you hand the file over: *"this file has N unresolved checks; do not generate paid
copy from it until they close."* Never resolve a check by deleting the check, and never hand over
a file that fails one without saying which.

**Never invent to pass a check.** If a check asks for something nobody gave you — an
anti-persona, a competitor weakness — the passing answer is `[TBD — no preguntado]`, not a
plausible guess. A check that pressures you into fabricating has failed at its job, and so have
you.

If a check fails, fix it or flag the value. Never resolve a failed check by deleting the check.

---

## How to use `product-marketing.md`

Put it where the agent reads it first:

- **Project root** — `product-marketing.md`. Simplest.
- **`.agents/product-marketing.md`** — if you keep agent context in one folder.
- **Referenced from `CLAUDE.md`** — one line does it:
  `Before any marketing task, read product-marketing.md and design.md, and follow both.`

Then make reading it **step 1 of every marketing task** — the first instruction, not a note in
the middle of a prompt. The file only helps if it's loaded before the model starts writing; a
model can't retroactively un-generalize.

Two habits that keep it honest:

1. **Update it when the product or the market moves.** It goes stale like anything else.
2. **When the model writes something generic, don't just rewrite the output — check whether the
   file was specific enough.** Most generic copy traces back to a vague ICP or an empty
   Customer-Language section.

---

## References & credits

**No third-party skill, framework, or copyrighted text is reproduced here.** The schema and
process above are GrowthLab-original, MIT licensed. The general idea of a reusable
product-context file is common practice across marketing teams; this is our own take on it —
leaner than our internal version, with the "never invent a number" rule that our own delivery
runs on.

**On lineage.** The section taxonomy also draws on a product-context skill we adopted and use
internally, whose original authorship we were unable to identify — it carried no author or
license. Everything here is reimplemented in our own words, not copied. If you are that author
and recognize your ideas, please open an issue or email hola@growthlab.mx and we'll credit you
by name.

Pairs with the [`design-md`](../design-md/SKILL.md) skill in this repo. Use both.

### About GrowthLab

These skills are the free half of a working method. [GrowthLab](https://growthlab.mx) is a
paid-media agency in México that runs its delivery on Claude Code — the context files, the
gates and the QA you just used are how our own client work ships. If you would rather have
the campaigns, the pages and the content *run for you* on top of this method, that is the
paid half: [growthlab.mx](https://growthlab.mx) · hola@growthlab.mx.
