---
name: build-brand
description: Build or refresh the brand brief by reading the user's website. Use whenever the user pastes a URL and says anything like "here's my site", "this is my product", "build my brand file", "set up the brand", "update the brand", or drops a link at the start of a project with no other instruction. Also use if make-slides or swipe reports that brand.md is empty or still has placeholders.
---

# Build Brand

Turn a URL into a filled-in `context/brand.md`.

## Critical: how to fetch

WebFetch does not return page content. It takes a URL **and a question**, and answers the
question. So don't ask it to "get the content" — ask it specific things, one fetch per
question cluster.

If WebFetch returns thin or empty results (common on JS-heavy single-page apps), fall back to:

```bash
curl -sL "<url>" | sed 's/<[^>]*>//g' | tr -s ' \n' ' \n' | head -c 20000
```

If that's also empty, the site is client-rendered. Say so and ask me to paste the copy directly.
Do not guess what my product does.

## Steps

1. **Fetch the homepage** with this question:
   > What does this product do, who is it for, what problems does it claim to solve, what
   > are its main features, and what tone does the copy use? Quote the headline and subheadline.

2. **Find and fetch the sub-pages that exist.** Try in this order, skip 404s silently:
   `/pricing`, `/about`, `/features`, `/blog`, `/use-cases`, `/customers`
   - pricing → the price and plan names
   - about → the founder story and voice
   - features → the concrete capability list
   - customers → real proof, only if numbers are actually stated on the page

   Stop at 4 successful fetches. More is diminishing returns.

3. **Extract pain points — this is the hard part and the most important.**
   Marketing copy states features. I need complaints. Convert each feature into the
   frustration it implies, written in my customer's voice, first person.

   - Site says: "Automated invoice reconciliation"
   - Bad pain point: "Users need automated reconciliation"
   - Good pain point: "i spend every sunday matching payments to invoices in a spreadsheet"

   Produce at least 5. If the site is thin, say which ones you inferred rather than read,
   and mark them `[inferred]` so I can correct them.

4. **Write `context/brand.md`** using the existing template structure. Fill every section
   you can support from the fetch. For anything unsupported, leave the bracketed placeholder
   in place rather than inventing content.

5. **Proof section is special.** Only write numbers that literally appear on the site.
   If there are none, leave it empty and note that formula F06 stays locked.

6. **Report back** in chat with: the one-line product description, the 5 pain points, and a
   list of anything you couldn't determine. Keep it short. I'll correct the pain points —
   they're the thing worth getting right, and I know my customers better than my landing page does.

## Rules

- Never invent a statistic, customer count, funding number, or testimonial.
- The "what they call themselves" field should be their words, not the site's marketing segment.
  If the site says "SMB decision-makers," that is not what anyone calls themselves. Infer
  something human and mark it `[inferred]`.
- If I'm refreshing an existing `brand.md`, preserve any section I've hand-edited. Show me a
  diff of what you'd change and wait before overwriting.
- Landing pages oversell. Treat the copy as a claim, not a fact.
