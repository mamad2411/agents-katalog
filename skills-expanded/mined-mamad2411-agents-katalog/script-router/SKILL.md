---
name: script-router
description: >-
  Triage and route any video-script request to the correct scriptwriting skill.
  USE THIS SKILL the moment a user asks for a video script, a hook, help
  scripting/structuring a video, or hands over a topic/brain-dump/draft to turn
  into a script WITHOUT clearly signalling the format — e.g. "write me a script
  for my video," "script this idea," "help me script something," "turn this into
  a video." Its job is to decide whether the request is short-form (sub-60s
  TikTok/Reels/Shorts) or long-form (roughly 3–15 min YouTube), ask one quick
  question only if truly ambiguous, then hand off to the shortform-script or
  longform-script skill. If the user already names the format or platform
  clearly (says "Short/Reel/TikTok" or "YouTube/long-form"), skip this and use
  the matching skill directly.
---

# Video Script Router

A lightweight triage step. It does **not** write the script itself — it decides
which scriptwriting skill should, then hands off. Keep this fast; the goal is to
land on the right skill in one move, not to interrogate the user.

## Step 1 — Read the request for format signals

Scan the user's message for signals of length/platform:

**Short-form signals** → route to `shortform-script`:

- Words: "short," "Short," "Reel," "TikTok," "clip," "under a minute," "30s,"
  "60 seconds," "quick hook."
- Vertical/feed framing, punchy single-idea asks.

**Long-form signals** → route to `longform-script`:

- Words: "YouTube," "long-form," "explainer," "tutorial," "walkthrough,"
  "video essay," "vlog," "deep dive," any minute count of 3+ ("5 minute,"
  "10 min"), "chapters/sections," "b-roll for a longer video."
- Topic depth that clearly can't fit in 60 seconds (multi-step tutorials,
  arguments with counterpoints, narratives).

## Step 2 — Decide or ask (one question max)

- **Clear signal either way** → hand off immediately (Step 3). Do not ask.
- **The ~1–3 minute boundary or genuinely no signal** → ask exactly ONE quick
  question, then route:

  > Quick check — is this a **short-form** clip (TikTok/Reel/Short, under a
  > minute) or a **long-form** YouTube video (a few minutes plus)?

  Don't stack other questions here; the chosen skill will gather the rest.

Tie-breaker defaults if the user is unresponsive or vague:

- Mentions a platform but not length → platform decides (TikTok/IG → short;
  YouTube → long).
- Topic is a multi-step tutorial, an argument, or a story → long-form.
- A single punchy tip, reaction, or one-liner → short-form.

## Step 3 — Hand off

Consult the chosen skill and follow it to produce the script:

- **`shortform-script`** — sub-60s talking-head TikTok/Reels/Shorts.
- **`longform-script`** — roughly 5–15 min talking-head YouTube videos.

Pass along everything the user already gave (topic, bullets, draft, tone, any
mode hints) so they don't repeat themselves. From here, the target skill owns
the output format, tone dial, and quality bar — this router's job is done.
