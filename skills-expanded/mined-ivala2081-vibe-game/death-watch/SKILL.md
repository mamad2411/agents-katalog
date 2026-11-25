---
name: death-watch
description: "Project health diagnostic. Detects scope creep, playtest gaps, prolonged inactivity, and asks the hard questions most indie devs avoid. Outputs a triage: pivot / ship-what-you-have / cut-and-continue / abandon. Trigger when the user feels stuck, when 2+ weeks pass without a playtest, or on a recurring cadence (monthly recommended for long projects)."
disable-model-invocation: false
---

# death-watch

> **Most indie projects die silently.**
> This one calls it out. Honestly. Without flattery.

## When to invoke

- User says: "I'm stuck" / "I don't know what to do" / "should I keep going?"
- Last playtest was 14+ days ago (auto-trigger threshold)
- Scope has grown >50% past the brief's budget
- Recurring monthly check on projects >3 months old
- Before any major refactor — "is the project healthy enough to absorb this?"

## Hard rules

1. **No false hope.** If indicators are bad, say so. Indie devs are gaslit by their own enthusiasm enough — they need honest mirror.
2. **No mercy-kill recommendations without data.** Cite specific signals (commits/week, last playtest, brief drift).
3. **Always offer 4 paths** — PIVOT / SHIP / CUT-AND-CONTINUE / ABANDON. Each one is a legitimate choice. Not loaded.
4. **The user decides.** This skill diagnoses. It does not execute.
5. **Refer to [Tyroller M17](../../taste/tyroller-mistakes.md#m17--ignoring-the-kill-switch)** — *"the kill switch is the most important indie discipline."*

## Diagnostic checklist

Run these checks before writing the report:

### Signal 1 — Activity
```
git log --since='14 days ago' --oneline | wc -l    → commits in last 14 days
```
- 0 commits: project may be quietly dead (red flag)
- 1-5: slow, possibly stalled
- 6-20: healthy iteration
- 20+: high activity (good IF other signals positive)

### Signal 2 — Playtest cadence
- When was the last `/feel-check` or recorded playtest in `FEEL-CHECK.md` or `Builds/`?
- 0-7 days ago: healthy
- 7-14: warning
- 14-30: serious gap
- 30+: red flag, [[tyroller-mistakes#M5]]

### Signal 3 — Scope drift
Compare brief's `Scope budget` to actual:
- Features in build vs. features in brief: count delta.
- If build has >150% of brief features: scope creep ([[tyroller-mistakes#M1]])

### Signal 4 — "It'll be fun when..." count
Grep recent commits / session notes for phrases:
- "when the art is in"
- "when I add music"
- "when there's a tutorial"
- "after the polish pass"

If 3+ excuses found: [[tyroller-mistakes#M6]] — *"the gray-box prototype must be fun NOW."*

### Signal 5 — External validation
- Has anyone outside the dev played it in the last 21 days?
- 0 → vacuum risk
- 1 → minimum acceptable
- 3+ → healthy

### Signal 6 — Time invested vs. core loop satisfaction
- Hours logged on project (estimate from commits, brief decision log)
- Latest `/feel-check` overall score
- If hours >100 AND feel-check <5: serious diagnostic flag.

## Report format

```
DEATH-WATCH REPORT — {{project name}}
─────────────────────────────────────
Date: 2026-MM-DD
Project age: __ days

Signals:
  ⚠ Commits last 14d:        __  (target >5)
  ⚠ Days since playtest:     __  (target <14)
  ✓ Scope drift:             __% past brief budget
  ⚠ "It'll be fun when..."   __ excuses detected
  ⚠ External playtests in 21d: __
  ⚠ Hours vs feel-check:     __h / __ score

Pattern detected:
  {1-2 sentence honest read of where the project is}

THE FOUR PATHS

1. PIVOT
   What it means: keep the team/skills/codebase, change the game.
   When to choose: core loop never landed despite multiple feel-checks <5.
   Cost: weeks of work discarded, but psychologically clean.
   Risk if not taken: 6 more months on a game that won't ship.

2. SHIP WHAT YOU HAVE
   What it means: lock scope today, polish only, release in 1-2 weeks.
   When to choose: current build is at feel-check >5 and you're afraid
   to ship more than you're motivated to add.
   Cost: imperfect release. Audience: small.
   Risk if not taken: another year passes, project dies in private.

3. CUT AND CONTINUE
   What it means: aggressive /cut, refocus on the brief, 30-day sprint.
   When to choose: scope drift is the problem; the core loop is good.
   Cost: discard several features you've grown attached to.
   Risk if not taken: scope keeps growing, project never finishes.

4. ABANDON
   What it means: stop, save the lessons in a post-mortem, move on.
   When to choose: you can't honestly answer "what's the verb?"
   in one word, OR you haven't worked on it in 30+ days.
   Cost: emotional, time invested feels lost.
   Risk if not taken: project becomes a guilt anchor for years.

RECOMMENDATION: {one of the four, justified in 2 sentences}

(But you decide. This skill diagnoses, not executes.)
```

## Tone

- **Honest.** Not cruel. Not flattering.
- **Specific.** Numbers, not vibes.
- **Compassionate but firm.** Indie devs are people. People shouldn't grind on dead projects.
- **No "but you got this!"** Cheerleading is what got the project here.

> "You've put 240 hours into this. Last playtest was 31 days ago. Last
> outside playtest: never. Your feel-check has been hovering at 4-5 for
> three months. This is a 4-AbANDON or 1-PIVOT pattern, not a polish
> problem. I think you know. What does pivoting cost vs. continuing?"

## Anti-patterns

- ❌ Soft language ("maybe consider possibly thinking about...")
- ❌ Recommending without citing specific signal values
- ❌ Picking the user's path for them (just lay out the four)
- ❌ Refusing to mention ABANDON (it's a legitimate path, and pretending otherwise is dishonest)
- ❌ Triggering when project is genuinely young (<30 days) — too early for death-watch

## Cross-references

- Reads: git log, [[vibe-brief]] (scope budget), latest feel-check report, `BUGS-FIXED.md`
- Calls into context: [[cut]] (if path 3 selected), [[ship]] (if path 2 selected)
- Anti-pattern sources: [[tyroller-mistakes#M5]], [[tyroller-mistakes#M6]], [[tyroller-mistakes#M17]]
- Related agent: [[scope-killer]] — if path 3, scope-killer runs aggressively next
