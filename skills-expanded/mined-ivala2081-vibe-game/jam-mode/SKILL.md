---
name: jam-mode
description: "Game jam workflow — locks the project into shippable scope for a fixed time budget (48h, 72h, week). Forces CC0 asset sources, kills feature creep at hour 24, auto-generates devlog updates, and enforces a 'ship at hour T-6' checkpoint. Trigger when the user joins or starts a game jam, has a hard time budget, or says 'I need to finish in N days'."
disable-model-invocation: false
---

# jam-mode

> **You don't have time. Act like it.**
> Jam wins are won by scope-killers, not feature-adders.

## When to invoke

- User says: "I'm doing a game jam" / "48 hour jam" / "Ludum Dare" / "GMTK Jam" / "I have N days"
- A jam is starting soon and the user wants to prep
- Any time-boxed project (not just public jams — internal sprints count)

## Pre-conditions

1. A Vibe Brief exists (or `/vibe-game:vibe-start` is run inline).
2. Time budget is declared up front (e.g., 48h / 72h / 7 days).
3. Theme (if applicable) is recorded in the brief's Hook section.

## Hard rules

1. **Scope is locked at hour 0.** No features added past `T - (total/3)`. Period. `/cut` runs aggressively.
2. **Assets must be CC0** (Kenney, OpenGameArt CC0 filter, freesound CC0). No "I'll get art later" — `/grab-asset` runs first hour.
3. **Ship checkpoint at `T - (total/8)`.** At this point, no new code. Only polish, bug-fix, build.
4. **Devlog at every 25% milestone** — auto-generated, ready for posting.
5. **No menus, no settings, no save system.** The game IS the loop. ([Tyroller M8](../../taste/tyroller-mistakes.md#m8--tutorial-bloat))
6. **Final hour: ship build + page + post.** Not negotiable.

## The jam timeline (48h example)

```
HR 0    /vibe-start     — brief in 30 min max
HR 1    /grab-asset     — all CC0 art + SFX downloaded
HR 2    /prototype      — playable loop running
HR 6    /feel-check     — first juice pass starts
HR 12   /cut            — aggressive cut (lock scope)
HR 18   /juice          — second juice pass
HR 24   /feel-check     — midpoint health check
HR 30   /devlog         — midpoint devlog post
HR 36   SCOPE LOCK      — no new features. Polish only.
HR 42   /ship           — first build attempt
HR 46   /ship           — final build + page + submit
HR 48   POST + SLEEP    — submission live, devlog tweet
```

For 72h: multiply everything by 1.5. For 7-day jams: by 3.5. The proportions hold.

## Procedure

### Step 1 — Lock the time budget

Ask once, write to brief:

> What's the time budget?
> - 48h (typical Ludum Dare, GMTK Jam)
> - 72h
> - 7 days
> - 30 days (Game Off)
> - Custom (specify in hours)

Compute the checkpoint times and **write them to `Assets/_Project/jam-schedule.md`** so they survive across sessions.

### Step 2 — Theme lock (if applicable)

If the jam has a theme, write it in the brief's **Hook** section as the constraint. Theme can't be ignored — it's how you stand out.

Push back on weak theme interpretations:

> User: "Theme is 'fragility', my game is about a cat."
> Skill: "How does fragility express in the cat? If you can't answer in one sentence, the theme is decorative, not structural. Try again."

### Step 3 — Anti-features upfront

For jam mode, **default anti-features** auto-added:
- ❌ No menus, no title screen
- ❌ No save system
- ❌ No tutorial
- ❌ No settings
- ❌ No multiple levels (one well-tuned level beats five rough ones)
- ❌ No multiplayer
- ❌ No leaderboards beyond local

User can lift specific anti-features with explicit justification — costs are real.

### Step 4 — Auto-checkpoint enforcement

The skill writes a small `jam-state.json` and updates it as time passes. At each checkpoint:

- **Hour 12 / 25% (Scope Lock):** `/cut` runs unilaterally. Anything not in current build is removed from the brief.
- **Hour 24 / 50% (Mid-check):** `/feel-check` runs. If overall score <5/10, recommend pivot or cut more.
- **Hour 36 / 75% (Polish Lock):** No new mechanics. `/juice` only.
- **Hour 42 / 87.5% (Ship Start):** `/ship` first build. Fix any RED checks.
- **Hour 47 / Final hour:** Final build, itch upload, devlog post.

### Step 5 — Devlog cadence

`/devlog` auto-fires at 25%, 50%, 75%. Drafts go to `Builds/devlog-hr{N}.md`. User can edit and post.

### Step 6 — Final ship

At T-2h, `/ship` runs even if user hasn't asked. Submission deadlines don't move.

## Anti-patterns

- ❌ Adding features past Scope Lock ("just one more...")
- ❌ Skipping `/grab-asset` ("I'll find art later" — you won't)
- ❌ Polishing menus that don't exist (Tyroller M3)
- ❌ Skipping the mid-check feel-check ("I'm in the zone, don't interrupt me" — the zone is lying)
- ❌ Skipping the final devlog ("I'll write it after submission" — submissions with day-1 devlog get more attention)

## Tone

Urgent but not panicked. Specific deadlines. Reference the brief mood — but jam mode overrides mood for the *workflow*, not the *game itself*.

> "You're at hour 30. Scope is locked. Stop adding the dash. Your last feel-check was 5.5/10 — that's a ship-able number. Now: /juice the core loop one more time, then /ship at hour 42."

## Cross-references

- Reads: [[vibe-brief]], `jam-schedule.md`, `jam-state.json`
- Calls: [[vibe-start]], [[prototype]], [[juice]], [[feel-check]], [[cut]], [[grab-asset]], [[ship]], [[devlog]]
- Anti-pattern sources: [[tyroller-mistakes#M1]], [[tyroller-mistakes#M3]], [[tyroller-mistakes#M8]]
