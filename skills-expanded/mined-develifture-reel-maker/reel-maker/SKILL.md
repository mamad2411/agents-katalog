---
name: reel-maker
description: Plan and write Instagram Reels, TikTok videos, and YouTube Shorts with original hooks, voiceover scripts, shot directions, captions, hashtags, and calls-to-action. Use for short-form video ideas, product demo scripts, hook or caption rewrites, adapting a reference reel, and reviewing an underperforming reel. Informed by 199 analyzed Instagram reels. Produces text and recording directions; use a separate production tool such as HyperFrames when the user requests a rendered video.
metadata:
  author: "Develifture"
  repository: "https://github.com/Develifture/reel-maker"
---

# Reel Maker

Turns a topic into a ready-to-shoot reel pack (hook, script, on-screen text, caption, call-to-action, test plan) using what 199 real reels have in common. The reels are mostly AI and developer-tool content from April to October 2026, median 81K views. Every one was analysed beat by beat and checked by eye.

## Read this first: what the evidence does and does not support

Three findings shape everything below. Say them to the user in plain words when they matter, and never promise views.

1. **The same hook got wildly different results.** "You can now run Claude Code completely free with almost unlimited usage" got 491K from one account and 5.1K from another. "Most people don't realize you can teach Claude to watch YouTube" got 1.26M and 5.5K. Audience size and how long a reel has been live dominate views. A hook is necessary, not sufficient.
2. **No craft choice separated a creator's best reel from their worst.** Hook length, question versus claim, duration, music, captions and cuts were tested within each creator's own catalogue (77 reels, about 40 features) and nothing held up. So the recipe below is table stakes: what winners and losers both do. Do it, then differentiate on topic, specificity and proof.
3. **Two things did show up clearly.** A one-word comment keyword offer: median comments/views 1.6% against 0.1% without. And putting that call-to-action as the first line of the post caption: 1.9% against 1.0% among offer reels. Among reels covering the same tool, earlier ones tended to beat later ones, though reel age confounds this.

Full numbers, tests and caveats are in `references/evidence.md`.

## How to work

1. **Collect only what is missing** (ask at most two questions, otherwise assume and state the assumptions): the topic or thing being shown; who it is for; what the viewer can get from it (link, prompt, file, guide); on camera or screen-only; target length; goal (reach, followers, leads).
2. **Pick the mode:**
   - *New reel* - produce the Reel Pack below.
   - *Critique or rewrite a draft* - score it against the checklist, show before and after, change as little as possible.
   - *Adapt a reference reel* - extract its structure (beat order and word budget) and write fresh wording for the user's topic. Never reuse its sentences: duplicated hooks were the weakest results in the sample.
   - *Post-mortem* - use `references/test-loop.md` to diagnose from the numbers.
3. **Outside AI or developer tools**, keep the structure, numbers and checklist. Swap the topic: a price anchor becomes "this software costs X a year, here is the free route", and so on. `references/hook-bank.md` has notes for translating each archetype.

## The recipe (what nearly every reel in the sample does)

| Element | What the 199 reels do |
|---|---|
| Length | Median 41s, middle half 29 to 52s. 30 to 45s was the most common band. |
| Spoken words | Median 139 (middle half 98 to 184). About 3.4 words per second, so seconds = words / 3.4. |
| Hook | One sentence, median 13 words (9 to 17). 166 of 199 are a bold claim, 19 a question. Claim also shown as on-screen text at the start (192 of 199). |
| Structure | Hook, setup, value, proof, call-to-action (68 reels). Hook, value, proof, call-to-action (26). A call-to-action beat is present in 89%, a proof beat in 69%. |
| Format | Talking head 53%, screen recording 23%, tutorial 6%, skit 6%. Opening visual: a person to camera or a screen/UI. |
| Captions | Bold sans-serif, usually white, centred, word by word, with one highlight colour (yellow most often). |
| Editing | Jump cuts in about 60%, zoom-ins in about 64%, sound effects in about 51%. Music is rare (28%), often just original audio. |
| Offer | 67% offer something for a comment keyword. 130 of 133 use a single word. |
| Post caption | Median 75 words, median 5 hashtags at the end (49 reels use none). |

## Hook

A hook states one specific payoff or stake in the first sentence and proves it visually in the first frame. Write it as: **specific thing + surprising result + stake or cost, in 17 words or fewer.**

- Write 5 variants across at least 3 archetypes from `references/hook-bank.md` (gap, scarcity, gatekeeper warning, price anchor, rank claim, discovery, curiosity question, stakes, contrarian, instant tip, first-person proof, skit). Recommend one and say why.
- Give each variant three parts: the spoken line, the on-screen text at second 0, and the first-frame visual. If it cannot be shown in the first frame, rewrite it.
- Make one noun and one number concrete. The weakest hooks in the sample promise something generic ("skills that will make your life easier", "20 connectors Claude needs"). The strongest versions of the same angle name the thing and the cost or stake.
- Test: could this hook describe any reel in the niche? If yes, it is too vague.

## Hold attention

- Write to the word budget: 15 to 30s is about 85 words, 30 to 45s about 135, 45 to 60s about 175, 60 to 90s about 230.
- Change what is on screen about every 3 to 4 seconds (screen insert, card, zoom, cutaway). In most reels checked, the visual changed at nearly every 4-second sample.
- Show the result before the explanation, or at least by the middle. Tutorials that show the output early read as proof, not promise.
- One idea per beat. In lists, every item is name, what it does, the benefit, in about 25 words.
- Finish with the payoff, then the call-to-action in the last two sentences. Do not trail off.
- Use only relative order of beats, never exact timestamps: the source timestamps were unreliable.

## Convert (call-to-action and caption)

- One short, easy-to-type keyword, tied to the topic (CLAUDE, PROMPT, FILE, REPO). Say what it unlocks in one specific phrase ("the exact prompt", "the setup guide").
- Say it in the last spoken sentence, show it as text on screen, and make it **line 1 of the post caption**.
- Caption template, call-to-action examples and hashtag guidance are in `references/cta-and-caption.md`.
- A plain "like for more" and a "send this to X" share prompt also worked at the top end; use them when a keyword funnel does not fit.

## Honesty and risk

Every claim in the hook must be shown in the reel. In review, 40 of 200 reels were rated low or low-medium credibility, usually staged screens, invented numbers or a claim the demo did not support. Do not invent demos, statistics, earnings or screens. Real proof is cheaper than fixing a reputation. Disclose affiliate links and sponsorships, only offer what you will actually deliver, and check current platform rules for automated DMs and giveaways.

## Reel Pack (output format)

Use this structure. Keep it tight; the user will skim it.

```
# Reel pack: <working title>
Assumptions: <what you assumed>
Angle: <archetype> - <one line on why it fits this topic and audience>
Length: ~NN s | ~NNN spoken words | <talking head / screen / skit>

## Hooks (lead with #N)
| # | Spoken (<=17 words) | On-screen text, second 0 | First-frame visual | Archetype |

## Script (read aloud at ~3.4 words/sec)
| Beat | Spoken | On-screen / visual | ~sec |
(hook, setup, value 1..n, proof, call-to-action)

## Edit notes
Cuts/inserts every ~3-4 s, B-roll or screen captures to record, caption style, sound effects.

## Post caption (copy-paste)
Line 1 = the call-to-action. Then 2 to 4 lines restating the promise. 3 to 5 hashtags last.

## Keyword
KEYWORD -> what it unlocks -> how it is delivered.

## Pre-publish checklist
[ ] Hook <=17 words, specific noun + number   [ ] Claim shown in first frame + text at second 0
[ ] Result visible by mid-reel                [ ] New visual every ~3-4 s
[ ] Word count matches length                 [ ] Call-to-action in last 2 sentences, on screen, and caption line 1
[ ] Every claim has on-screen proof           [ ] Not a copy of another reel's wording

## Test plan
What to vary in the next reel, and what to log (see references/test-loop.md).
```

## References (read when needed)

| File | Read it when |
|---|---|
| `references/hook-bank.md` | Writing or judging hooks. Twelve archetypes with fill-in templates and real examples. |
| `references/script-templates.md` | Choosing a structure. Seven templates with beat-by-beat word budgets. |
| `references/cta-and-caption.md` | Writing the call-to-action, keyword, post caption and hashtags. |
| `references/test-loop.md` | Measuring a reel, benchmarks, diagnosing a flop, planning the next test. |
| `references/evidence.md` | The user asks "how do you know", or you need exact numbers, caveats or the method. |

## Optional video production handoff

When the user requests a finished video and HyperFrames is available, pass the reel pack and supplied footage or audio to its workflow. [HyperFrames](https://github.com/heygen-com/hyperframes) handles composition, animation, preview, and rendering. It is installed separately; the Reel Maker pack is a text deliverable until video production is completed.
