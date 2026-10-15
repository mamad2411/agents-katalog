---
version: 0.1.0
name: recon-brief
description: |
  Turn RECON UGC findings into a concrete shoot brief — hooks, beats, and
  shot lists grounded in videos that actually overperformed.
  Use when: "what should I make", "give me video ideas", "write a script
  for TikTok", "turn this into a brief", "what should we shoot this week",
  "adapt this winning video for my product", or any request that moves from
  research to production.
  Always grounds the brief in real indexed videos rather than inventing
  trends. NOT for: finding the videos (use recon-research) or benchmarking
  rivals (use recon-competitors).
allowed-tools: Bash
---

# RECON brief

Never write a brief from imagination. Ground every recommendation in a video that
measurably overperformed, and say which one.

## Sequence

1. **Find the evidence** (see `recon-research`):

   ```bash
   reconugc search --niche <their category> --period last_30_days --limit 10
   ```

2. **Read 2-3 breakdowns** of the highest outliers:

   ```bash
   reconugc breakdown <post-id>
   ```

3. **Extract the transferable part.** A brief is not "copy this video". It is the
   *mechanism*: what the video does structurally that would still work with a
   different product in front of the camera.

   Transferable: "opens mid-problem, no intro, result shown at 0:03."
   Not transferable: "guy in a red hoodie in a Toronto kitchen."

4. **Write the brief.**

## Brief format

```
CONCEPT — <one line, the idea in plain words>
WHY IT SHOULD WORK — <the mechanism + the evidence: @handle, 32x outlier>

HOOK (0:00-0:02)   <the exact first line, written out>
BEAT 2 (0:02-0:06) <what happens on screen>
BEAT 3 (...)       <...>
PAYOFF             <what the viewer walks away with>

FORMAT   <talking head / product demo / skit / ...>
NEEDS    <what they must actually have to shoot it>
```

Three concepts is the right number. One is thin, ten is a homework assignment
nobody shoots.

## Rules

- **Write hooks as spoken lines**, not descriptions. "POV: you just found out your
  screenshots were costing you installs" — not "a hook about screenshots".
- **Respect what they can actually shoot.** If they have no on-camera talent, do
  not brief a talking head. Ask once if you do not know.
- **Cite the outlier score** for every concept so the user can see the idea is
  earned, not invented.
- **No fabricated trends.** If RECON has no strong examples in their category,
  say so and widen to an adjacent one, naming the swap.
- Keep the language plain. This goes to whoever is holding the phone.

## Deploy

RECON's own Deploy surface generates product-specific concepts from a single video
and the user's product profile. If they want that instead of a hand-written brief,
point them at the video's Deploy panel in the app.
