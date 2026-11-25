---
name: photo-post
description: Turn the user's own photos into slideshow text — hooks, slide copy, and captions built around the specific images they sent. Use whenever the user sends plain photographs with no text overlay, no hook, and no slide structure: their own product shots, lifestyle photos, screenshots of their app, event photos, or anything from their camera roll. Triggers on "here are my photos", "write text for these", "what should I put on these", or a bare image drop with no reference-post framing. This is the handler for images the user OWNS. Use the swipe skill instead when the image is a screenshot of someone else's finished post.
---

# Photo Post

Their photos, my words. The images are the constraint, not decoration.

## Routing check first

Look at the image before anything else.

| The image has | Use |
|---|---|
| text overlay, a hook, visible slide structure, TikTok/IG UI chrome | `swipe` — it's someone's post |
| no text, just a photograph | this skill — it's their asset |

If mixed, handle each accordingly and say which is which. If genuinely ambiguous, ask once.

## Steps

1. **Read `context/brand.md`, `context/formulas.md`, `context/swipe-file.md`.**
   If the swipe file has fewer than 5 entries, say once at the top that output is formula-driven
   rather than pattern-matched. Don't repeat the warning per slideshow.

2. **Inventory the photos.** Label them Photo A, B, C... with a one-line description each.
   Then classify every photo as one of:
   - **payoff shot** — the good outcome, the thing the viewer wants
   - **problem shot** — the pain, the mess, the before
   - **proof shot** — the product actually in use, a screen, a result
   - **texture** — atmosphere, no narrative job

   State the mix out loud. It determines what's buildable.

3. **Name the constraint.** This is the step that makes this skill worth having.
   If all photos are payoff shots, say so: the problem slides will have to be plain text,
   which is native to the format and costs nothing. If there are no proof shots, say the
   product mention will have to be a text slide. Be specific about what the photo set
   can't do rather than quietly working around it.

4. **Pick formulas that fit the photos**, not the other way around. A set of five group
   photos suits F08, F02, F09. A set of before/after shots suits F03, F07. If a formula
   needs a shot type the user doesn't have, skip it and say why.

5. **Write 3 slideshows** to `output/YYYY-MM-DD-batch-N.md`, following the output contract
   in `CLAUDE.md`.

6. **Image direction is an assignment, not a description.** Every slide names a specific
   Photo letter or says "plain text slide." Never write a description of an image the user
   would have to go find — that's the whole point of them sending their own.

7. **Use the whole bank.** Across the batch, every photo should appear at least once. If one
   genuinely has no job, say which and why rather than silently dropping it.

## Rules

- All voice rules in `CLAUDE.md` apply. Hook ≤ 12 words, no banned words, product mentioned once.
- Run `context/scorecard.md` before output. Photo sets often FAIL scroll_stop_power on slide 1 —
  reassign a stronger photo rather than rewriting the hook.
- **Never invent a personal detail.** No fabricated anecdotes, no "the time I...", no specifics
  about the user's life that they didn't tell you. If a slot needs a real story, write the
  slide as a placeholder and flag it in a blockquote at the end: what you'd need from them
  and why their real version will outperform yours.
- Plain text slides on a flat background are a legitimate and native choice. Don't apologize
  for them or pad the deck with photos that don't earn their place.
- Don't describe photos back to the user in detail. They took them. One line each is enough.

## Do not

- Generate, edit, crop, or offer to make images.
- Ask for more photos before producing a first draft. Work with what arrived, then say what
  a second batch would need.
