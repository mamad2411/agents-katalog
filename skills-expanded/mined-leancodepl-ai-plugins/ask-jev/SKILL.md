---
name: ask-jev
description: >
  Ask Jev (TypeSafe's System One model) for calibrated, typed judgments — yes/no probabilities,
  rubric scores, picks from a fixed set — instead of relying on your own opinion. Use when a
  task turns on a judgment call or a rating rather than on generated text: triaging or ranking
  findings, scoring every item in a list, or a second opinion on work you just produced.
---

# Jev

Jev answers typed questions with numbers. You hand it some **state** and a set of typed
**questions**; it returns a number per question — a probability, a rating, or a pick with a
probability distribution behind it. No prose, no reasoning, nothing to parse. Roughly 70–500 ms
and a fraction of a cent per call, which is what makes it reasonable to ask about every item in
a list rather than a sample.

This skill is how you hand a judgment over without mangling it. Jev reads a question
literally, answers each one in isolation, and explains nothing, so the framing carries the whole
weight: one factor per question, the right type for the job, state cut to what the question needs.
What follows is the general discipline. A question that keeps coming back earns a **recipe** —
a written decomposition, kept in `references/`.

## Before the first call

Read these first, in this session, before sending anything:

- [`concepts/state.md`](https://docs.typesafe.ai/concepts/state.md) — every time.
- The page for each question type you are about to use.

| What you need | Page |
| --- | --- |
| Yes/no — probability that a condition holds | [`primitives/noul.md`](https://docs.typesafe.ai/primitives/noul.md) |
| Position on ordered levels you describe | [`primitives/score.md`](https://docs.typesafe.ai/primitives/score.md) |
| One of a fixed set, with the distribution | [`primitives/choice.md`](https://docs.typesafe.ai/primitives/choice.md) |
| Reading confidence and picking thresholds | [`confidence.md`](https://docs.typesafe.ai/confidence.md) |
| Fields, limits, and error codes | [`api.md`](https://docs.typesafe.ai/api.md) |
| Combining several scored dimensions | [`patterns/composite-scoring.md`](https://docs.typesafe.ai/patterns/composite-scoring.md) |

Start from the [index](https://docs.typesafe.ai/llms.txt) for anything not listed. Every page
serves Markdown by appending `.md` to its path; fetch that form, which returns the page itself
rather than a summary of it, and resolve relative links against `https://docs.typesafe.ai`.

**The request contract below is not a substitute for these pages.** It says what the API accepts.
The pages say what the numbers mean and how to frame a question so the number is worth having. A
request that satisfies the contract and ignores the pages comes back as a confident number about
the wrong thing, and nothing in the response marks it.

**If a page will not load, stop and tell the user.** Being unable to read the docs is a reason to
raise the problem, not a reason to call Jev anyway.

## Calling it

`scripts/jev.py` sends the request. In a plugin install it sits at
`<plugin-root>/scripts/jev.py`; standalone, next to this skill.

```bash
python3 <plugin-root>/scripts/jev.py ask \
  --state '{"ticket": "The export button crashes the settings page in Safari.", "reported_by": "support"}' \
  --questions '{"is_bug": {"type": "noul", "instructions": "Does `ticket` report a software defect?"}}'
```

State is a JSON object whenever it has more than one part, so each part carries a name a question
can point at with a backticked path. A bare string is for a single indivisible blob — a diff, a
log, one document — and `jev.py` makes you say so with `--state-format text` once such a string
runs long, because several items flattened into one blob is the mistake that costs the most.

It reads the API key from `~/.config/typesafe/env` on its own, retries 429s and 529s, and prints
the API's JSON. `--state-file <path>` sends a file instead — reach for it whenever the state is a
diff, a log, or anything else large, because a file passed by path never enters this transcript.
`--questions-file` does the same for the questions. `key-status` answers whether a key was found
and from where.

The request contract, which the script checks before spending a call:

- **Questions** are a map of your id to `{type, instructions, criteria?}`. **The model never sees
  the id**, so `instructions` carries the whole meaning — `api_break` says nothing to it.
- **`noul`** takes `criteria` only if you want them: a map describing the true and the false
  side. Leaving them out is normal.
- **`score`** takes `criteria` as an **ordered array** of level descriptions, at most 10. The
  answer is 0-indexed and can land between levels. The `legend` in the response comes back keyed
  by index; the request never takes that shape.
- **`choice`** takes `criteria` as a **map** of option id to description, at most 255.
- `--model` defaults to `jev-latest`.
- Limits: ~64k tokens per request, ~32k for the state plus the longest single question. Text only.

When a call errors, `references/setup.md` covers the failures by symptom.

## Why ask Jev instead of just answering

Three reasons, and they are worth knowing so you can tell when none of them apply:

- **It scales across a list without drifting.** Jev evaluates every question in a call
  independently and in parallel — question 40 gets the same attention as question 1. Your own
  judgment measurably degrades down a long list; Jev's does not, by construction.
- **It has no stake in the work.** When you are judging code or a document you just produced,
  you are a compromised reviewer. Jev sees only the state.
- **It is consistent.** Semantically similar inputs produce quantitatively similar outputs, so
  the same rubric means the same thing today and next week. Your read drifts between sessions.

If none of those matter — a single one-off judgment on something you have no stake in — just
answer. A tool call is not free, and a Jev number wrapped around your own opinion is worse than
your opinion plainly stated.

## What Jev is good at, and what it is not

Jev makes the judgment a knowledgeable person makes in a few seconds from what is in front of
them. Is this urgent? Which of these three buckets? How severe, on this scale?

It is unreliable at anything requiring several hops of reasoning, at simulating what would
happen downstream of a choice, and at arithmetic, counting, and date comparison. It also reads
questions **literally** — it answers what you wrote, not what you meant.

This gives you the single most useful rule here: **if a question needs you to weigh several
independent factors, it is not one Jev question.** Split it into one question per factor and do
the weighing yourself. "Is this refactor a good idea?" is not a Jev question. "Does this change
alter the public API?", "Does it have test coverage?", and "How invasive is it, on this scale?"
are three Jev questions, and the judgment you build on top of them is yours — and visible.

## The loop

1. **Name the decision.** What will you do differently depending on the answer? If nothing,
   do not ask.
2. **Decompose it** into atomic questions and pick a type for each: `noul` for a yes/no
   probability, `score` for a position on ordered levels, `choice` for one of a fixed set. The
   number means something different in each, and the three are not interchangeable.
3. **Build the state.** Only what the questions need. Accuracy falls as irrelevant material
   grows, and the state is capped around 32k tokens. Filter first.
4. **One `jev.py ask` call** carrying every question, including speculative ones you may not end
   up using. They run in parallel, so a second question costs tokens but almost no time.
5. **Report the numbers next to the questions that produced them.** The framing is the part a
   human needs to check, and it is the part you invented.

## Habits that matter

**Batch into one call.** Separate calls throw away the parallelism and cost an agent turn each.

**Give Choice somewhere to land.** A Choice is relative — it always picks the best of what you
offered, even when nothing fits. Add an `other` or `none_of_the_above` option, or use per-item
Nouls, which are absolute and can all be low.

**Pass the full list, not a shortlist.** A Choice takes up to 255 options and each costs a few
tokens. Pass every team, category, or candidate you have. Pre-filtering to the plausible ones is
you making the judgment you were about to delegate.

**Count in code.** For "how many of these match", ask one Noul per item in a single call and add
the results up yourself. A question that asks Jev to count, total, or compare dates measures
nothing.

**Score dimensions separately and weight them yourself.** `risk = 0.4 × blast_radius +
0.4 × reversibility + 0.2 × coverage` beats one "how risky is this" Score, because when a ranking
surprises someone they can see which dimension caused it. A single flattened number invites
agreement without inspection.

**Keep the rubric, vary the state.** Criteria are the part worth writing once and reusing — your
severity ladder, your bar for "worth raising". The instruction and the state stay contextual.
That split is what makes scores comparable across runs, and it is what a recipe captures.

**Show your questions.** Report the instruction and criteria alongside the answer. A confidently
wrong number usually comes from a badly framed question, and that is the only way anyone catches
it.

**Never launder a number into a verdict.** Jev returns no reasoning, so if you present "0.82"
as "this is fine", nobody can audit the step in between. Report the number, the question, and
your interpretation as three separate things.

**Do not carry thresholds between types.** A cutoff tuned on a Noul means nothing on a Choice.
And `P(x)` from one Noul and `1 − P(not x)` from another will not agree; the model guarantees no
arithmetic identities between separate questions.

## References

Read the one you need, when you need it.

| File | What it covers |
| --- | --- |
| `references/setup.md` | **Meta:** the API key file, and what each failure means |
| `references/writing-a-recipe.md` | **Meta:** how to add a new recipe reference, honestly |

### Recipes

A recipe takes one recurring high-level question — the kind a person actually asks — and shows
how to decompose it into questions Jev is good at, with the criteria in full and an honest note
on what it leaves unanswered. When you work out a decomposition that holds up, write it down as a
new file here and add a row, following `references/writing-a-recipe.md`.

| File | The question it answers |
| --- | --- |
| `references/evaluating-a-test.md` | Is this unit test built well enough to be worth its lines? |
| _(more wanted)_ | Candidates: how good is this code change · which tool or pattern fits here · is this review finding worth raising |
