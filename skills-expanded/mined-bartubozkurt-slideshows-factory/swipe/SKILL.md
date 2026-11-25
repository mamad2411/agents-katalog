---
name: swipe
description: Turn screenshots of OTHER PEOPLE'S finished social posts into ready-to-use hooks, captions, and slide text for the user's own product. Use when the sent image shows a completed post — text overlay, a hook, visible slide structure, or TikTok/Instagram UI chrome. Triggers on "make me something like this", "analyze this", "steal this format", "what makes this work". Use the photo-post skill instead when the images are the user's OWN plain photographs with no text on them.
---

# Swipe

Image in → adapted hooks, captions, and slide text out. One pass, two halves.

Read `context/brand.md`, `context/formulas.md`, and `context/swipe-file.md` first.
If `brand.md` is empty or full of placeholders, run `build-brand` instead and ask for my URL.

**Routing check.** If the image has no text overlay, no hook, and no slide structure, it is my
own photograph, not a post to break down. Switch to `photo-post` and say so in one line.

---

## Half 1 — Read the post (keep this short)

Output at most 6 lines. I don't need an essay.

- **Hook (verbatim):** transcribe exactly, including lowercase and typos — those are signals
- **Structure:** one short line per slide, summarized in your own words
- **Formula:** match to `formulas.md`, or `NEW` with a proposed F## definition
- **Mechanic:** the one reason it stops a scroll. Be specific — "curiosity gap" is useless,
  "promises a number then withholds the best item until the last slide" is useful
- **Transfers to:** which of my pain points this structure can carry, or "doesn't transfer"

Never transcribe body slides word for word. We take structure, not sentences.

---

## Half 2 — Give me the inspiration (this is the point)

Apply the mechanic to my brand. Produce all three blocks:

### Hooks — 5 of them

Same mechanic as the original, my subject matter. Each ≤ 12 words. Vary the angle: don't
give me five rewordings of one idea, give me five different pain points wearing the same
structure. Number them so I can say "3."

### Slide text — for the strongest hook only

Full slide-by-slide script for whichever hook is best. Follow the output contract in
`CLAUDE.md`. Match the original's slide count and rhythm.

### Captions — 3 of them

Different lengths: one very short (under 8 words), one medium, one that adds context the
slides didn't cover. Plus 4-6 hashtags, mixed broad and niche.

Then one line: **why this should work** — tie it to the mechanic.

---

## Half 3 — Log it

Append the entry to `context/swipe-file.md` using that file's template. Increment E##.
Never overwrite existing entries. If you identified a `NEW` formula, append it to
`context/formulas.md` too.

Do this silently. Just say "logged as E07" at the end. Don't paste the entry back at me.

---

## Rules

- Multiple images in one message may be slides of ONE post rather than several posts.
  Check the visual style before assuming. Ask once if unsure.
- If the screenshot is a niche far from mine, still do it — say the transfer is a stretch
  and adapt the mechanic rather than the topic.
- Never reproduce the original's body copy in my version. If a hook I produce is close to
  the source's wording, rewrite it.
- All voice rules in `CLAUDE.md` apply. Hook ≤ 12 words, no banned words, no invented
  numbers, product mentioned once.
- If the image is unreadable or the hook is cut off, say so and work from what's visible
  rather than guessing at the missing text.

## Do not

- Describe how to recreate the image, or offer to make images.
- Pad Half 1. The analysis is scaffolding; the hooks are the deliverable.
