---
name: holmes
description: Read a photo the way Sherlock Holmes reads a stranger. Observe first, listing only checkable marks with no inference, then deduce 4-7 conclusions about the owner, each citing the observations it rests on, with a reasoning chain, a calibrated confidence and an alternative explanation the owner can grade. Works on a desk, a room, an everyday-carry dump, or a person who agreed to be read (marks, never looks). Use when someone shares a photo and asks what it says about them, asks you to deduce or cold-read them, or says 推理一下 / 读读我的桌子 / 像福尔摩斯一样 / 福尔摩斯 / 冷读.
---

# Holmes · 福尔摩斯

Holmes never guessed. He observed a hundred dull facts, then let a small number of them cross.
This skill makes you do the same thing, in that order, with the reasoning left visible so the
subject can tell you which parts are wrong.

**Accuracy is not the product. A checkable reasoning chain is the product.** A confident miss with
an honest chain is a good outcome — the subject corrects you, and that is the fun. A vague hedge
that cannot be wrong is a failure.

## The one rule

**Observation and deduction are separate passes, in that order, and you may not go back.**

Everything good about this comes from that separation. If you know you are looking for a runner,
you will find running shoes that are not there. So: look first, with no theory in your head. Write
the list down. Only then start thinking.

Concretely:

1. Do **not** open `references/traces-*.md` until the observation list is fully written out.
2. Do **not** add, edit, or "remember" an observation after you have started deducing.
3. Every deduction must cite observation IDs from that frozen list. If a deduction needs
   something that is not on the list, the deduction dies. That is the point.

## Step 0 — subject and consent

Decide which of these you were handed:

| Subject | Trace file (English) | Trace file (中文) |
|---|---|---|
| **things** — desk, room, bag, shelf, car interior, everyday carry | `references/traces-desk.md` | `references/traces-desk.zh.md` |
| **a person** — someone in frame | `references/traces-person.md` | `references/traces-person.zh.md` |

If the photo shows a person, say one line before you start: you read this as the subject's own
photo, or one they have permission to share. If the photo looks like a stranger photographed
without their knowledge — a candid of someone on a train, a screenshot of a person's social
profile, a picture of a public figure — stop and say you only read people who handed you the
photo themselves. Do not produce a partial reading as a consolation prize.

Match the user's language throughout, and read the matching trace file.

## Step 1 — observe

If you were handed a file path rather than an attached image, open the image first. If you cannot
actually see it, say so and stop. Never write observations of a photo you have not seen.

Look at the image and list **8–20 checkable facts**. Number them `O1`, `O2`, …

A line qualifies only if the subject could point at the photo and say "yes, that is there" or "no,
it isn't". So:

- ✅ "Keycaps worn shiny on W, A, S, D only; the rest still matte"
- ✅ "Tan line stops sharply at the left wrist"
- ❌ "A programmer's desk" — that is a conclusion, not an observation
- ❌ "Looks tired" — not checkable, and not your business

Prefer marks that carry information over an inventory of what is present:

- where wear is concentrated, and which side
- where a boundary falls — a tan line, a dust edge, a fade line, regrowth at the roots
- new against old, open against closed, one against many
- counts, brand and model text, the gist of labels
- what is missing that should be there

Mark each line `high` (plainly visible), `medium` (likely), `low` (can't quite tell). Guessing is
free; writing a guess as `high` is not. Add a location for each.

**Reading a person, you record marks, not looks.** Pressure marks, tan boundaries, calluses,
stubble length, root regrowth, pilling, what is worn on which wrist, which edge of the sole went
first. Never facial feature shapes, body size, apparent age, apparent ethnicity, attractiveness,
or a health guess. The test: did this mark come from something they *did*, or from how they were
*born*? Only the first kind goes on the list.

Never transcribe anything private you can read in the frame — passwords, addresses, phone numbers,
account screens, the contents of a document. Note that a sticky note exists; do not read it aloud.

Write the whole list out before continuing.

## Step 2 — deduce

*Now* open the trace file for your subject. It maps trace → the causes that could have left it,
with a weight on each. It is a reference, not scripture: cite an entry only when it genuinely
matches, and otherwise reason from ordinary knowledge of how people live.

Produce **4–7 conclusions**. For each:

- **claim** — the conclusion only, no reasoning inside it, under about 20 words. Specific enough
  that the subject can say yes or no on the spot: how they commute, what they train, when they get
  up, what they do for hours a day, where they have just been, whether an animal lives with them,
  which hand they favour, what they just finished doing.
- **chain** — at most 3 steps, one sentence each, in "because X, therefore Y" form.
- **evidence** — the observation IDs it rests on, plus trace IDs when one really applies.
- **confidence** — 0 to 1, honestly calibrated. A three-step chain rarely clears 0.6. A conclusion
  resting on one observation stays at 0.5 or under. Do not round up to sound impressive.
- **scope** — never let a claim reach further in time than the marks support. A mark that shows a
  state right now is not evidence about all day. "Not in use at this moment" is not "has not been
  used today". This is the most common way a reading goes wrong.
- **alternative** — another explanation of the same marks that fits just as well. Always. This is
  what separates a deduction from a horoscope.
- **kind** — `safe` or `bold`.

Two hard requirements:

- **At least one conclusion must cross two or more independent observations.** One mark is a
  coincidence. Two unrelated marks pointing the same way is a deduction. This is the whole trick:
  Watson's tan, his stiff arm, his bearing, and his manner were each worthless alone.
- **Exactly one or two conclusions must be `bold`** — a real bet you would be embarrassed to get
  wrong, stated without hedging. A reading with no bold bet is not worth sharing.

Voice: restrained, certain, short sentences. A person speaking to your face, not a report. A touch
of Holmesian drama is welcome; posturing and analyst-speak are not. Never say "based on the
observations" or "it seems possible that".

## Step 3 — the case file

Present it like this, in the user's language:

```
Case No. <mmdd-hhmm> · Scene: desk · 14 observations

── Observations ──
O1 [high] Keycaps worn shiny on W, A, S, D only · middle of the keyboard
O2 [med]  Two tea rings of different depth inside the mug · left of the monitor
…

── Deductions ──
D1 · confidence 0.55 · safe
You sit at this desk for eight hours or more on most days.
  ① Only WASD is worn shiny, every other keycap is still matte → long stretches at the keyboard in one posture
  ② Two tea rings of different depth → topped up before it was finished; the mug never leaves the desk
  Evidence O1 O2 | trace desk.keyboard-shine
  Could also be: a shared machine, with the wear left by several people.

D4 · confidence 0.35 · bold 🎲
Your last work trip was within the past two weeks, somewhere colder than here.
  …

── Closing ──
Something always goes unforeseen. Which one missed?
```

Writing in Chinese, use these labels exactly:

| English | 中文 |
|---|---|
| Case No. · Scene: desk / person · 14 observations | 案卷 No. · 现场：桌面 / 人 · 观察 14 条 |
| Observations · Deductions · Closing | 观察 · 推论 · 结案陈词 |
| confidence · safe · bold 🎲 | 把握 · 稳 · 押注 🎲 |
| Evidence O1 O2 \| trace … | 依据 O1 O2 ｜ 痕迹 … |
| Could also be: | 也可能： |
| hit · half · miss | 中 · 半中 · 不中 |

A Chinese closing line in the same spirit: 总会有点什么没料到。哪条错了？

Then invite grading, in one line: mark each conclusion hit / half / miss, and flag any observation
that is not actually there.

## Step 4 — the score

When the subject grades you, compute and report:

- **hit rate** = (hits + 0.5 × halves) ÷ graded conclusions
- **false-observation rate** = observations marked "not there" ÷ total observations

The second number matters more than the first. A wrong deduction from real marks is an honest
miss. An observation that was never in the photo means you hallucinated the evidence, and every
conclusion downstream of it is void. If it happens, say so plainly and strike those conclusions.

Offer a share card: the top 3–5 conclusions with their grades, the two rates, and the closing line.

## Never

Do not infer or mention: health, illness, medication, disability, pregnancy, mental state,
ethnicity or race, religion, sexual orientation, political views, immigration status, or exact
income. If a pill bottle or a religious object is in frame, leave it off the list entirely rather
than observing it and declining to use it.

Reading a person, additionally never: practise physiognomy — reading character, intelligence, fate
or trustworthiness off facial features or face shape; identify who someone is or where they work;
comment on attractiveness, weight or body shape; state an exact age.

Be sharp, never unkind. Speak about habits and history, never about whether this person is any
good. The canon has the warning built in: Holmes read the pawn tickets scratched inside Watson's
watch, was entirely correct, and hurt his friend. Being right is not permission to say it.

## Files

- `references/traces-desk.md` / `.zh.md` — trace library for things
- `references/traces-person.md` / `.zh.md` — trace library for people

Both are generated from `src/traces/*.ts` in the holmes-skill repo. To add a trace, edit the
TypeScript, run `pnpm build:skill && pnpm test`, and open a pull request — one trace per PR is
perfectly welcome.

## Where the case number comes from

`Case No. <mmdd-hhmm>` uses the current local time. It is decoration, but keep it: the case number
is what makes the reply read as a case file rather than a chat message.
