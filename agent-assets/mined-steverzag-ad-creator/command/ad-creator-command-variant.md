---
description: Produce test variants of an existing ad that differ in exactly one element
argument-hint: [what to vary, e.g. "elevia-seguro-resbalon: 3 headlines"]
---

Produce variants: **$ARGUMENTS**

If the variable isn't clear, ask which one — headline, image, CTA, angle or
format. That single answer is the whole design of the test.

## 1. One variable

A variant set exists to attribute a result to a cause. Change **one** element
and hold everything else identical; two changes at once make the test
unreadable, which is worse than not running it.

If the user asks to vary several things, say what that costs and offer either a
set per variable or a single best-guess ad. Don't quietly vary two.

Default count is 3 unless asked otherwise. Past 4 the traffic per variant gets
too thin to separate.

## 2. Siblings, not edits

Variants are separate folders sharing a prefix — `<slug>-a`, `<slug>-b`,
`<slug>-c`. Never mutate the original into one of them; the baseline has to
survive as a comparison.

Copy the source ad's files rather than re-scaffolding, so everything except the
varied element is byte-identical. Keep the same brand, formats, duration and
config.

## 3. Make them genuinely different

Three headlines that are the same sentence reworded test nothing. Vary the
*mechanism*, using the patterns in `references/copywriting.md` — a specific
outcome against a named objection against a direct question. For an angle test,
the ads should argue differently, not just open differently.

The claim boundary is per variant and unchanged: no variant may introduce a
statistic, price, rating or testimonial the brief didn't supply, and a "bolder"
variant is not licence to invent one.

## 4. Render, look, report

Follow `/render` for each, then `Read` one format per variant — a variant that
breaks the layout isn't a variant, and copy length is exactly what breaks it.

Report as a table: variant, the varied element's value, the folder. State the
variable in one sentence and what a win for each would tell the user.
