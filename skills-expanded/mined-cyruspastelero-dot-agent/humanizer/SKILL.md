---
name: humanizer
description: Use when writing or reviewing any text a person will read — App Store descriptions, release notes, in-app copy (buttons, empty states, errors, onboarding), READMEs, PR descriptions, docs, landing-page and marketing copy. Strips the tells that make text read as machine-generated and rewrites it in the product's own voice. Invoke before shipping copy, not after.
---

# Humanizer

Text that ships should read like a person wrote it. This skill is the pass that
makes that true: identify the tells, then rewrite — never just delete.

## When to run it

Run it on **every user-facing string before it ships**, in one sweep rather than
line by line:

- App Store: description, subtitle, keywords, promotional text, release notes
- In-app: buttons, labels, empty states, error messages, confirmations, onboarding
- Repo: README, PR descriptions, docs, changelogs

Run it *after* the copy exists and *before* it is uploaded or committed. It is a
revision pass, not a drafting technique.

## Step 1 — Build the reference corpus first

Before rewriting anything, collect **3–5 strings from the product that already
sound right** (or, for a new product, 3–5 lines from a competitor or the
founder's own writing that hit the target register). That is the voice you are
matching.

Skipping this step is how a de-slopping pass flattens a product's personality
into generic terseness — which is its own kind of slop.

## Step 2 — Find the tells

Read every string as a set, aloud. Flag:

**Hype verbs and filler**
"unlock", "elevate", "empower", "supercharge", "seamlessly", "effortlessly",
"delve", "harness", "leverage", "journey", "game-changing", "robust",
"cutting-edge", "revolutionize". An empty state reading "Unlock your fitness
journey!" becomes what the screen actually does.

**Template cadence**
Three parallel clauses in a row. "X. Y. Z." staccato taglines. Every sentence the
same length. Headline-and-subhead pairs that restate each other. Rule-of-three
padding where two items would do.

**Robotic mechanics**
Em-dash chains. "Note that…", "Simply…", "Please note", "It's worth noting".
Exclamation marks on surfaces that aren't celebrating anything. Title Case Mid
Sentence. Stacked hedges ("may", "might", "could" in one sentence). Arrow chains
(`A → B → fails`) standing in for a sentence.

**Wrong register**
Errors that apologize theatrically ("Oops! Something went wrong 😢") or lecture
the user. Confirmations that over-celebrate a trivial action. Marketing voice on
a utility surface — a settings toggle does not need a value proposition.

**Announcement throat-clearing**
"We're excited to announce", "Introducing", "Say hello to", "In today's
fast-paced world". Release notes that describe the release rather than what
changed for the user.

## Step 3 — Rewrite to the bar

The bar: **read it aloud — if it sounds like a press release, a chatbot, or
nobody, it fails.**

Rewriting rules:

- **Say the concrete thing.** "Log your lifts and watch your numbers climb" beats
  "Elevate your fitness journey." Specifics are the cheapest humanizing move
  available.
- **Labels say what happens**, not what the widget is: "Start Workout", not
  "Workout Action".
- **Errors say what failed and what to do next**, in the product's voice, with no
  apology theatre.
- **Vary sentence length deliberately.** Uniform rhythm is the loudest tell.
- **Cut, don't soften.** If a clause carries no information, delete the clause
  rather than hedging it.
- **Keep the contractions.** "Doesn't" reads human; "does not" reads legal.
- Length is not the goal. A longer sentence that sounds like a person beats a
  clipped fragment that sounds like a log line.

## Step 4 — Know what is yours to change

- **Utility surfaces** (buttons, errors, settings, empty states): rewrite freely.
- **Brand-carrying surfaces** (onboarding, paywall, App Store description,
  taglines): these are product decisions. Rewrite, but **present the before/after
  and flag it** rather than silently shipping a new brand voice.
- **Never invent claims.** De-slopping is a rewrite of tone, not of facts. If the
  original claims a feature, the rewrite claims exactly that feature — no more.
  Do not add benefits, numbers, or superlatives that weren't there.

## Output

Report as a before/after table, tightest first:

| Surface | Before | After | Why |
|---|---|---|---|

Then apply the changes. If a rewrite is on a brand-carrying surface, apply it but
call it out explicitly so a human can veto it.

## Anti-pattern

"The copy is fine, it's just a button." Every audit of 'fine' copy has found at
least one string that reads machine-written. Read them as a set; the tells show
up in the aggregate rhythm far more than in any single line.
