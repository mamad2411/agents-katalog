---
name: vibe-start
description: "Bootstrap a new Unity indie project the vibe-game way. Captures a 1-page Vibe Brief (mood, verb, references, hook, anti-features, scope), detects or creates the Unity project, and sets up the working surface for the other vibe-game skills. Trigger when the user is starting a new game, opening a fresh Unity project, or wants to set vision before code."
disable-model-invocation: false
---

# vibe-start

> **Mood and verb come before mechanics.**
> No code until the brief is sharp.

## When to invoke this skill

- User says: "let's start a new game" / "I have an idea for a game" / "new project"
- The Unity project has no `vibe-brief.md` in its root or `Assets/_Project/`
- User runs `/vibe-start` explicitly

## Hard rules

1. **You may not write Unity code** until the Vibe Brief is filled and the user confirms it.
2. **Cite [Tyroller M2](../../taste/tyroller-mistakes.md#m2--no-prototype-lots-of-planning)** if user wants to skip the brief — *but* keep the brief to 1 page. Tyroller M2 cuts *both* ways: no prototype AND too much planning are bad.
3. Brief must fit on one page. If sections balloon, prune ruthlessly.
4. Save the brief to `Assets/_Project/vibe-brief.md` (or `vibe-brief.md` at repo root if no Unity project yet).

## Procedure

### Step 1 — Detect context

Run these checks (Glob/Read):

- Is there a `ProjectSettings/ProjectVersion.txt`? → Unity project exists. Read the version.
- Is there a `Packages/manifest.json`? → Read it. Note the Input System version, render pipeline, Cinemachine, Unity Recorder.
- Is there an existing `vibe-brief.md`? → Read it. If yes, ask if user wants to **edit** the existing brief or **start fresh**.
- Is the repo empty? → We'll create a Unity project later via `/prototype` or instruct user to create one.

**Report what you found in 3 lines max:**
> Unity 6000.0.23f1 detected. URP, new Input System 1.7.0, Cinemachine 3.0. No vibe-brief found.

### Step 2 — Gather the brief (interactive)

Ask the user the 8 brief sections **one or two at a time**, never all at once.
Use `AskUserQuestion` when there are clear option sets. For free-text (verb, hook), just ask in chat.

**Order matters:**

1. **Mood** (3 adjectives) — set the soul first
2. **Verb** (1 word) — what does the player DO
3. **References** (3 games + 1 outside-games thing)
4. **Hook** (1 sentence)
5. **Anti-features** (what we are NOT)
6. **Win / Lose**
7. **Core loop** (60 seconds of gameplay)
8. **Scope budget + Success definition**

For each, **push back if the answer is generic:**

- "fun, exciting, cool" → reject. *"Those are non-answers. Give me 3 specific adjectives. Look at the [game-feel-swink](../../taste/game-feel-swink.md#failure-modes-swinks-taxonomy) failure modes for vocabulary."*
- Verb is "play" or "do" → reject. Verbs are physical: drift, weave, build, scream.
- References without specifics → reject. *"Yes, but WHICH part of Hotline Miami? The combat? The visuals? The score?"*

### Step 3 — Save the brief

Write `Assets/_Project/vibe-brief.md` (or repo root) from the [vibe-brief template](../../templates/vibe-brief.md), filling all `{{PLACEHOLDERS}}`.

Append:

```markdown
---
*Created by /vibe-start on YYYY-MM-DD.*
*Next: run `/prototype` to build a playable scene supporting the Verb + Core loop.*
```

### Step 4 — Scope sanity check

Before signing off, do a quick [Tyroller M1](../../taste/tyroller-mistakes.md#m1--scope-explosion) check:

- Is the scope budget realistic for the timeline?
- Does the verb match the references? (e.g., "drift" + reference *Civilization* = mismatch)
- Are anti-features genuinely cutting things, or vague?

If concerns, surface them. The user can override, but they should *know*.

### Step 5 — Hand-off

End with a single, clear next step:

> ✓ Vibe Brief saved to `Assets/_Project/vibe-brief.md`.
>
> **Next:** run `/prototype` and I'll build a playable scene that supports
> "{{VERB}}" with mood "{{MOOD}}". Estimated time: 30 minutes.

## Anti-patterns (do NOT do)

- ❌ Skip the brief and dive into code (defeats the purpose)
- ❌ Accept generic answers (mood = "fun")
- ❌ Let the brief bloat into a GDD
- ❌ Make 50 design decisions for the user — surface options, let them pick
- ❌ Forget to cite the taste library when pushing back

## Example session (abbreviated)

```
User: /vibe-start

Skill: Unity 6000.0.23f1 detected, URP + new Input System. No vibe-brief yet.
       Let's define the soul before code. First: what's the mood — 3 adjectives?

User: tense, methodical, cold

Skill: ✓ Solid mood. Now the verb — 1 physical word for what the player DOES.

User: stalk

Skill: ✓ "Stalk" — strong verb. References next: 3 games + 1 thing
       outside games. For each, the SPECIFIC part you want to channel.

User: Hitman (the planning), Manhunt (the dread), Disco Elysium (the dialogue
      gravitas). Plus the bus stop scene from Drive (2011).

Skill: ✓ Coherent reference cocktail. Hook in 1 sentence?

[...]

Skill: ✓ Vibe Brief saved. Run /prototype next.
       Estimated 30 min to a playable scene.
```

## Cross-references

- Output drives: [[prototype]], [[juice]], [[cut]], [[ship]]
- Reads from: [[vibe-brief]] template, [[tyroller-mistakes]] for scope checks
- Anti-pattern source: [[tyroller-mistakes#M2]]
