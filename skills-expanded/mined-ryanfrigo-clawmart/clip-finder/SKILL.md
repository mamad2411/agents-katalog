---
name: clip-finder
description: Surface the 5-8 most clippable moments in an episode with exact timestamps and a scroll-stopping hook for each.
metadata: { "openclaw": { "emoji": "✂️" } }
---

# Clip Finder

Finds the short-form gold buried in a long recording. Reads a clean transcript, scores every moment against what actually performs on short-form, and returns 5–8 self-contained clips with exact in/out timestamps and a hook line for each. This is where "one recording, a week of content" starts.

## When to use (trigger phrases)

Use this skill when the user says:

- "find the best clips in this episode"
- "what should I cut for Shorts / TikTok / Reels?"
- "pull the most viral moments"
- "give me timestamps for clips"
- "where are the good soundbites?"

## How it works

1. **Read the canonical transcript** (`transcript.clean.md`; run `transcript-clean` first if needed). You need timestamps — if the source had none, tell the user your in/out points are estimates.
2. **Score moments against a rubric.** A moment is clippable when it hits one or more of these — the more, the better:
   - **Contrarian take** — "Everyone says X; that's wrong because…"
   - **Concrete story** — a specific, named, time-bound anecdote (not a generality).
   - **Emotional peak** — surprise, conviction, frustration, a laugh.
   - **Quotable one-liner** — a sentence that stands alone without context.
   - **Actionable tip** — a do-this-now instruction with a clear payoff.
   - **Tension / disagreement** — host and guest pushing on each other.
   - **Surprising data or reframe** — a number or mental model that flips the listener's assumption.
3. **Pick 5–8 non-overlapping segments.** Each must be **self-contained** — it makes sense to someone who never heard the rest of the episode. Target **20–90 seconds** (15–45s for TikTok/Shorts/Reels, up to 90s for a LinkedIn/X video). Reject anything that needs "as I said earlier" to land.
4. **Set tight in/out points.** Start on the *payload*, not the wind-up — cut the "yeah, so, I think what's interesting is…" preamble. End on the punch line or the period, never mid-thought. Give the trimmed start/end timestamps, not the raw paragraph bounds.
5. **Write a hook for each.** The hook is the on-screen text / opening line that stops the scroll. Make it a promise, a tension, or a bold claim drawn from the clip — never clickbait the clip can't pay off. 3–8 words is the sweet spot for an overlay.
6. **Tag each clip** with: the verbatim quote, why it works (which rubric items), best platform(s), and a one-line caption. Rank the list best-first so the user cuts the top 2–3 even if they're short on time.
7. **Hand off for cutting.** Output the timestamps in a form a video tool can use. If the user wants, provide an `ffmpeg` command per clip (see Notes) — but the actual cut happens in their editor, not here.

## Output

A ranked list. Example (two of six shown):

```markdown
### 1. "You don't have a churn problem" — 00:22:40–00:23:18 (38s)
**Hook:** "Your churn problem is a lie"
**Quote:** "You don't have a churn problem, you have an empty-state problem.
Nobody leaves a product that's already full of their stuff."
**Why it works:** contrarian + quotable one-liner + reframe. Stands alone.
**Best for:** Shorts, Reels, X video. **Caption:** The retention reframe most
founders miss. Full episode in bio.

### 2. The 3am pager story — 00:31:05–00:32:20 (75s)
**Hook:** "The night we deleted prod"
**Quote:** "It's 3am, I'm half asleep, and I run the migration on the wrong
database…"
**Why it works:** concrete story + emotional peak. Great for LinkedIn video.
**Best for:** LinkedIn, X. **Caption:** A hard-won lesson about backups.
```

Followed by an optional cut sheet:
`Clip 1 → in 00:22:40 out 00:23:18 · Clip 2 → in 00:31:05 out 00:32:20 …`

## Notes

- **OpenClaw finds the moments and writes the hooks — it does not cut video.** Hand these timestamps to your editor: Descript, Opus Clip, CapCut, Premiere, or an ffmpeg-based skill. If a clip is off by a beat, nudge it in the editor; ASR timestamps drift by a second or two.
- **Optional ffmpeg cut** (requires `ffmpeg` installed by the user): to lift a clip losslessly,
  `ffmpeg -i episode.mp4 -ss 00:22:40 -to 00:23:18 -c copy clip1.mp4`. For vertical 9:16 with re-encode, crop/scale in a second pass. This is a convenience, not the product — verify the cut.
- **The hook is a promise the clip must keep.** Don't write a hook the segment can't pay off — it tanks watch-time and trust. No fake stats, no "this one trick."
- **Self-contained beats "best line."** A brilliant sentence that needs three minutes of setup is a worse clip than a good sentence that stands alone.
- Spot-check the top clips against the actual audio before publishing — tone and timing don't fully survive text.
