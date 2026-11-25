---
name: social-repurpose
description: Turn a clip or takeaway into platform-native posts — X thread, LinkedIn post, and short-form caption — each in that platform's real voice.
metadata: { "openclaw": { "emoji": "🔁" } }
---

# Social Repurpose

Takes one clip or takeaway and rewrites it into the native format of each platform you post to. The same idea reads completely differently as an X thread, a LinkedIn post, and a Shorts caption — this skill respects those differences instead of cross-posting one blob everywhere.

## When to use (trigger phrases)

Use this skill when the user says:

- "turn this clip into posts"
- "write an X thread / LinkedIn post from this"
- "caption this Short / Reel / TikTok"
- "repurpose this takeaway for social"
- "make platform versions of this idea"

## How it works

1. **Take the input.** A clip from `clip-finder` (quote + hook + timestamp), a key takeaway from `show-notes`, or a raw idea the user pastes. Ask which platforms they want if they don't say.
2. **Load the creator's voice.** Ask for 2–3 of their existing posts, or a one-line voice note ("dry, no hype, lowercase, short sentences"). Match cadence, casing, and vocabulary. When unsure, write plainer, not louder.
3. **Write each platform in its native format** (only the ones requested):
   - **X thread:** A hook tweet that stands alone and earns the tap (≤ 280 chars, a claim or tension — no "a thread 🧵👇" filler). Then 4–8 tweets, **one idea per tweet**, concrete over clever. Close with a soft CTA and the link/clip in the **last** tweet, not the first. No hashtag walls.
   - **LinkedIn:** A one-line hook, then a blank line, then a short story or insight with generous whitespace (LinkedIn truncates at ~3 lines before "…see more" — earn the click). Plain, first-person. **Put outbound links in the first comment, not the body** — link-in-body suppresses reach. 1–2 relevant hashtags max, at the end.
   - **Short-form caption (TikTok / Reels / Shorts):** Two parts — (a) the **spoken/overlay hook** for the first 1–2 seconds of the video, and (b) the post caption: one line of context + a soft CTA + 3–5 specific tags (not `#fyp #viral`). Keep it tight; these platforms reward brevity.
   - **Instagram carousel (optional):** A slide-by-slide outline — hook slide, 4–6 point slides (one idea each), CTA slide — plus the caption.
4. **Keep every claim true to the source.** Don't inflate a measured statement into a guarantee, don't invent numbers, don't manufacture a hot take the guest didn't make. Repurposing is translation, not embellishment.
5. **Return drafts ready to paste,** clearly separated per platform, with the intended clip/link noted for each.

## Output

For one clip, requesting X + LinkedIn + Shorts:

```markdown
## X thread
1/ Your churn problem is a lie.

You don't have a churn problem. You have an empty-state problem.

2/ Nobody abandons a product that's already full of their stuff. Notes, history,
teammates, data — that's the moat, and it's built in session one.

3/ So the question isn't "why do they leave?" It's "did the first session leave
anything behind worth coming back to?"

4/ Three fixes that move D30:
– shorten time-to-value
– kill the empty state
– earn the first notification

5/ Full breakdown with Dr. Chen here → [link]

## LinkedIn
Your churn problem is probably a lie.

Most teams treat retention as a product-depth problem. It's usually a
first-session problem: nobody abandons a product that's already full of their
own stuff.

Fix the empty state before you touch the roadmap.

(Full episode linked in the comments.)

#retention #productgrowth

## Shorts / Reels / TikTok
Overlay hook: "Your churn problem is a lie"
Caption: The retention reframe most founders miss. Full episode in bio.
Tags: #productmanagement #startups #retention #saas #founders
```

## Notes

- **These are drafts, not published posts.** OpenClaw can write and save them; actually posting requires a channel you configure — a scheduler skill (Typefully, Buffer, Hypefury), a platform API, or manual paste. This pack does not post on your behalf.
- **The LinkedIn link-in-comments rule is real** and worth keeping — links in the body measurably cut reach. Same for X: the payoff/link goes in the last tweet.
- **No engagement bait, no fake stats, no manufactured outrage.** If the clip is calm and useful, the posts should be calm and useful. Sustainable beats a spike.
- Voice-matching gets much better with 2–3 real samples. Without them, default to plain and let the user dial it up.
- Character limits drift; keep the hook tweet well under 280 and assume LinkedIn shows only the first ~3 lines before the fold.
