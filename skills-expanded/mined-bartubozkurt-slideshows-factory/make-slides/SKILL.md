---
name: make-slides
description: Generate new TikTok slideshow scripts as text for the user's own product. Use whenever the user asks for slideshow ideas, hooks, post ideas, content ideas, "give me some posts", "what should I post", "more ideas", a batch of content, or asks to apply a swipe-file pattern to their own brand. Also use as the second half of "make me something like this" after the swipe skill has run.
---

# Make Slides

Produce slideshow scripts. Text only — no images, no code, no design.

## Steps

1. **Load context.** Read `context/brand.md`, `context/formulas.md`, `context/swipe-file.md`
   in that order. If `brand.md` still has bracketed placeholders in Product, Audience, or
   Pain Points, stop and ask me to fill those three sections. Nothing else is blocking.

2. **Check swipe depth.** Fewer than 5 entries in the swipe file → generate anyway, but open
   with one line: output will be generic until more screenshots are added.

3. **Pick formulas.** Default batch is 3 slideshows, 3 different formulas. Weight toward
   formulas that appear in the swipe file and in the "worked" rows of the feedback log.
   Respect the lock rules in `formulas.md` — especially F06 requiring real proof.

4. **Fill the slots** from `brand.md`. Each slideshow targets a **different pain point**.
   Never two posts on the same pain in one batch.

5. **Write the slides.** Follow the voice rules in `CLAUDE.md` exactly. Hook ≤ 12 words.
   One idea per slide. Product appears once, softly, near the end.

6. **Self-check before output.** Two silent passes.

   **Hard rules:** hook ≤ 12 words, zero banned words, no invented statistics, product mentioned
   exactly once, slide count inside the formula's stated range.

   **Scorecard:** run `context/scorecard.md`. Rate six dimensions PASS/WEAK/FAIL. Any FAIL, or
   two WEAK in one slideshow, gets fixed or replaced. Use the diagnostic table — the fix is
   usually structural, not verbal.

   Fix everything before showing me anything. Never show me the checklist or the ratings.
   If one WEAK survives, name that dimension in a single line. Nothing more.

7. **Write to `output/`** as `YYYY-MM-DD-batch-N.md`, then summarize in chat with just the
   three hooks and which formula each used. I'll ask if I want the full text.

8. **Log it.** Add a row to the feedback log in `swipe-file.md` for each formula used,
   verdict blank until I respond.

## Output shape

Use the exact contract in `CLAUDE.md`. Every slideshow needs slides, caption, hashtags,
image direction, and a one-line rationale.

**Image direction** is a plain description of what should be on screen so I can go find it
myself. One sentence per slide. Example: "plain screenshot of a messy spreadsheet, no annotations."
Never offer to make the image.

## On "more"

A follow-up "more" or "again" means a **new batch with formulas not used in the previous
batch** and pain points not yet covered. If every formula has been used, rotate back to the
best-performing one but attack a different pain point.

## Do not

- Write copy that sounds like a landing page.
- Use a hook that only makes sense to someone who already knows the product.
- Produce more than 5 slideshows in one batch. Quality collapses past that.
