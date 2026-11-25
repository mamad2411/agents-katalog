---
name: devlog
description: "Generate a devlog post from recent project activity. Reads git log, brief, recent juice/feel-check changes, then produces a GMTK-style narrative post in three lengths (Twitter/X, itch.io devlog, blog). Includes GIF placement guidance. Trigger after a significant change, weekly cadence, or when shipping a milestone."
disable-model-invocation: false
---

# devlog

> **Indie marketing dies of silence.**
> One GIF + 200 words per week beats one big launch post.
> ([Tyroller M10](../../taste/tyroller-mistakes.md#m10--marketing-as-an-afterthought))

## When to invoke

- User says: "make a devlog" / "post update" / "write something for Twitter"
- After a significant change (new mechanic, juice pass, balance overhaul)
- Weekly cadence (recommended — schedule it)
- Auto-triggered by `/jam-mode` at 25/50/75% checkpoints
- Auto-triggered after `/ship`

## Hard rules

1. **Lead with a hook.** First sentence must promise something. Boring openers ("This week I worked on...") are banned.
2. **One GIF per post, minimum.** Indicate where to insert it. Devs scroll fast.
3. **Three lengths produced** — pick whichever fits the channel:
   - **Twitter/X (280 chars):** 1 hook + GIF + 1 follow-up tweet
   - **itch.io devlog (300-500 words):** more context, screenshots, links
   - **Blog (800-1500 words):** the story of the week
4. **Reference the brief's mood** — if "tense, methodical", devlog reads weighty. If "frenetic", reads kinetic.
5. **No engineering brag.** Players don't care about your refactor. They care about *feel* and *progress*.
6. **End with an ask.** "Wishlist?" "Feedback on the dash?" "DM me your high score." Audience action = engagement.

## What to gather before writing

Read these (use Bash/Grep as needed):

| Source | What to extract |
|---|---|
| `Assets/_Project/vibe-brief.md` | Game mood, verb, current scope |
| `git log --since='7 days ago' --oneline` | Recent commits — what got done |
| `examples/*/JUICE-LOG.md` or session juice changes | Cited polish work |
| `examples/*/FEEL-CHECK.md` or recent feel-check report | Current health score |
| `Builds/` | Did we ship recently? |
| `CREDITS.md` | New art/audio attributions worth shouting out |

If `git log` shows nothing in 7+ days → push back. *"Nothing changed this week. A devlog about nothing is worse than no devlog. Either ship something small in the next 2 hours, or skip this week."*

## Output structure

### Section 1 — The hook (1-2 sentences)
- What's the most *visceral* thing that happened? Show it, don't tell.
- Bad: "I added screen shake."
- Good: "Punches finally land. They hit-stop now."

### Section 2 — The GIF (placeholder)
```markdown
![Before/after GIF — show the punch landing with the new hit-stop](path/to/gif.mp4)
```

Tell user explicitly where to record and what to capture. **Recording instructions:**
- 5-15 seconds, looped
- Show the change clearly (before/after if comparative)
- Crop to gameplay only, no chrome
- Tools: Unity Recorder (best for game), ShareX, ScreenToGif

### Section 3 — Why it matters (2-3 sentences)
- Frame the change in terms of *player feel*, not implementation.
- Cite the source if applicable: "Vlambeer's hit-stop principle (P4) — 60ms freeze on melee impact. The brain finally registers the punch."

### Section 4 — What's next (1-2 sentences)
- One concrete thing happening in the next 7 days.
- Builds anticipation. Sets a public deadline (accountability).

### Section 5 — The ask
- Wishlist link (if Steam)
- Itch page (if jam)
- "Reply with your high score"
- DM for playtesting

## The three lengths

### Twitter/X (280 char hook + 1 follow-up)

```
Tweet 1 (280 char):
{hook}.

[GIF here]

{itch.io URL}

Tweet 2 (reply):
{why it matters in 1 sentence}
Built with #vibegame on #madewithunity
```

### itch.io devlog (300-500 words)

Full structure (hook → GIF → why → next → ask), narrative voice.

### Blog (800-1500 words)

Add a **Process** section: what you tried, what didn't work, what shipped. Be honest. Devs read other devs' devlogs for the failures, not the successes.

## Tone calibration to mood

- **Tense, weighty mood:** sparse prose, short sentences, restrained adjectives.
  *"Hit-stop landed. 60ms. Punches mean something now."*

- **Frenetic, ridiculous:** exclamation marks earned, italics, more energy.
  *"OK the SCREENSHAKE is now COMPLETELY out of control and I love it."*

- **Cozy, warm:** invite the reader in. Use "we" subtly. Soft transitions.
  *"This week the cat learned to nap on the windowsill. Look at this little guy."*

## Anti-patterns

- ❌ "Spent the week refactoring the input system" (player-irrelevant)
- ❌ Posting without a GIF/screenshot (gets ignored)
- ❌ Multi-week silences then a wall of text (people forgot you exist)
- ❌ Self-deprecation as a personality ("idk if this is good lol") — read as low confidence
- ❌ Generic openers ("This week I worked on...") — first 5 words are the whole battle

## Example output (abbreviated)

```markdown
# Hit-stop landed.

Punches finally have weight. 60ms of frame freeze on impact (Vlambeer P4),
and now every hit is a tiny event. The room notices.

[GIF — 8 seconds, before/after comparison of punching]

Why it matters: the brain doesn't process micro-events. It processes
*pauses*. The freeze is the punch.

Next week: knockback + screen kick (Vlambeer P13, P10). Aiming for the
moment where one good hit feels like a sentence ending in an exclamation.

Wishlist Cleave on itch: itch.io/...
```

## Cross-references

- Reads: [[vibe-brief]], git log, juice/feel-check artifacts, [[gmtk-patterns]]
- Triggered by: [[jam-mode]] checkpoints, [[ship]] completion, weekly cadence
- Anti-pattern source: [[tyroller-mistakes#M10]]
