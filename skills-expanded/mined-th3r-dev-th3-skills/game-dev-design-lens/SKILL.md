---
name: game-dev-design-lens
description: >-
  Design a game from player motivation instead of from mechanics. Reads MDA (Mechanics, Dynamics,
  Aesthetics) through Octalysis's eight core drives plus sensation, the "unified theory of game
  design" approach, so the design runs forward: who plays → which drive → which kind of fun →
  which dynamics → which mechanics. Ends with a white-hat / black-hat audit. Use WHENEVER the work
  is "game idea", "is this fun", "why do players quit", "core loop", "rewards", "progression",
  "player types", "MDA", "Octalysis", "engagement", "retention", "monetization ethics",
  "game brief", "ออกแบบเกม", "เกมไม่สนุก", or before writing a game brief or a GDD.
---

# Design lens: motivation first

Source: *The Unified Theory of Game Design: The Journey Begins (Part 1)* by Anshul Rustaggi with
Nimisha Parashar (Medium), which combines MDA with Yu-Kai Chou's Octalysis. Part 1 sets out the
problem and the combination; this method applies it. Part 2 (building each emotion with
Octalysis) was not available when this was written.

## Why not MDA alone

The article's critique, in short. Keep it in mind when a design "has everything" on paper:

- MDA is mostly used to **take a finished game apart**. Run forward, there is no clear path from a
  kind of fun to the dynamics that produce it.
- It **assumes every player feels the same fun**. Different players come for different things, so
  a list of all eight aesthetics for one game says little.
- Its eight aesthetics sit on **one level**, though Sensation is physical (and often depends on
  the hardware) while Challenge is psychological. Some overlap too, such as Fantasy and Narrative.
- It **names no motivations and no manipulative ("black hat") pulls**, which are often what keep
  people playing.

## The drives (Octalysis)

| # | Core drive | Pulls the player because… | Hat |
|---|---|---|---|
| 1 | Epic Meaning & Calling | they are part of something bigger | white |
| 2 | Development & Accomplishment | they get better and it shows | white |
| 3 | Empowerment of Creativity & Feedback | they try things and see results | white |
| 4 | Ownership & Possession | they own and grow something | neutral |
| 5 | Social Influence & Relatedness | others see, help, compete | neutral |
| 6 | Scarcity & Impatience | they can't have it yet | black |
| 7 | Unpredictability & Curiosity | they don't know what comes next | black |
| 8 | Loss & Avoidance | they will lose something if they stop | black |
| + | Sensation | it feels good physically: sound, touch, motion | depends on hardware |

White-hat drives make players feel good and in control; black-hat drives create urgency and can
keep people playing after they stop enjoying it. Drives 2 and 4 lean on logic and owning
(extrinsic); 3, 5 and 7 lean on creativity and people (intrinsic).

## Method

Write each step as a short paragraph in the brief. Do the steps in order.

1. **Players.** Name one to three player groups by what they come for, not by age or platform
   ("wants to show off a build", "plays for ten minutes after school with friends").
2. **Drives.** For each group, pick **one main drive and at most two supporting ones**. A game that
   serves every drive serves none.
3. **Fun.** Translate each drive into the MDA aesthetic the player would feel (Challenge,
   Fellowship, Expression, Discovery, Fantasy, Narrative, Submission, Sensation). This is the
   target, not a list of features.
4. **Dynamics.** For each aesthetic, the behaviour that happens in play when it works: "players
   race the same course and compare times", not "a leaderboard".
5. **Mechanics.** Only now the rules and systems that cause that behaviour: timers, checkpoints, a
   leaderboard, trading. Every mechanic traces back up to a drive; one that does not is cut or
   left for later.
6. **First minute.** What the player does in the first sixty seconds, and which drive it touches
   first. If it is none, the first minute is wrong.
7. **Audit.** Run the checklist below.

## White-hat / black-hat audit

For each mechanic, write its drive and hat. Then:

- **Balance.** Black-hat mechanics (timers, limited offers, streaks you lose, random rewards) are
  allowed to start an action, never as the only reason to keep playing. Each one needs a white-hat
  reason to stay.
- **Money.** Nothing that is paid for may use drive 6, 7 or 8 to push the purchase (countdown
  offers, paid random boxes, "lose your progress unless…"). Check the platform's rules: Roblox
  has its own for paid random items and for younger players.
- **Young players.** On a platform with many children (Roblox), no loss-aversion or scarcity
  pressure around spending, and no social pressure to pay.
- **Sensation.** If the fun depends on feel (game feel, haptics, audio), say what hardware the
  players have, and test on it.

## Output

In `design/game-brief.md` (or the template's brief), a section **Motivation** with: the player
groups, each one's main drive, the aesthetic target, the dynamics, the mechanics traced to drives,
the first minute, and the audit table. Keep it under one page.
