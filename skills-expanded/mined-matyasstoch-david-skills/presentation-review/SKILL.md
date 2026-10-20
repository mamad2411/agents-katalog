---
name: presentation-review
description: Use when David is building or reviewing a YouTube video presentation (Google Slides) slide-by-slide. Covers the Firebase Studio alternating explain/show structure, the coverage tracker, and the bullet-by-bullet iteration loop. Triggers on presentation slides, slide outline, video deck, Google Slides, slide structure, "what's the next slide", "give me options for this bullet", presentation review.
---

# Presentation Review

Build and refine David's YouTube video presentations slide-by-slide, alternating with him.

## Visual Style

- **Background:** White. **Text:** Black. Title in serif, big.
- **Key phrases:** Highlighted in yellow.
- **Each slide:** One concise title + ~3 bullet points (teleprompter notes telling David what to say).
- **Bullets:** Plain English sentences. NOT "word — explanation" format. David hates that.
- **Showcase slides:** Red title on near-empty slide (just the action name + any URL).

## Firebase Studio Structure (THE core format)

Alternate ~2 explain slides → 1 showcase step, repeating. Never 20 min of talking then 20 min of demo. Dynamic, vibrant, alternating. This format got David's Firebase Studio video ~400k views.

- **Explain slides** = educational, talked over.
- **Showcase slides** (🎬 / ✅) = live screen recording of setup/implementation.
- Big or lead-magnet moments can get 2 showcase steps back-to-back.

## Working Files

Keep these in the video's folder (`work/youtube/<video>/`):

- `EXPLAIN.md` — numbered list of all educational topics.
- `SHOWCASE.md` — numbered list of all setup/showcase steps.
- (optional) `topics.csv` — coverage tracker; column 2 = `mentioned` (YES/NO). Use to verify the deck covers 90-95% of the master doc.

Mark completed items in EXPLAIN.md / SHOWCASE.md with ✅ as slides get built.

## The Iteration Loop (how David works)

David builds the deck in Google Slides himself. He pastes screenshots and asks for help one piece at a time. Your job per turn:

1. **He pastes a slide screenshot.** Read it fully.
2. **He asks for the next move.** Usually one of:
   - "What should the next 2 explain slides be, and why?" → give top 3 options, each concise, with a one-line WHY. Recommend one.
   - "What should we show/setup next?" → name the SHOWCASE step(s) + why they pay off a promise just made.
   - "Give me N options for this bullet point." → give N plain-English sentences, then your pick + one-line reason.
   - "Mark these with the emoji." → add ✅ to the matching EXPLAIN/SHOWCASE rows.
3. **Keep flow continuity.** Every suggestion must flow naturally from the previous slide and pay off promises already made ("easy to customize" → show editing files).

## Rules

- **Be very concise.** Short options, short WHY. No verbose essays.
- **Plain sentences only** in bullets — never the "label — sentence" format.
- **Fact-check claims** when David asks, before they go on a slide.
- **ZERO REPETITION.** Never reuse an example, quote, screenshot, stat, or person across slides. Cross-check against earlier slides; flag duplicates.
- Every slide adds NEW value and earns its ~3 bullets.
- Retention: weave in distinct reasons to keep watching; pattern-break dense slides with simple/visual ones.

## Slide 1 & 2

- **Slide 1:** Big visual hook, often minimal text. Punchy, exciting — it's the first frame.
- **Slide 2:** What the video is + why to care. Bullet 3 = what the viewer gets by watching to the end.
