---
name: loop-and-economy
description: Analyze a game's core loop, progression pacing, and resource economy for dead ends, runaway inflation, and dominant strategies. Use when the user is designing progression, upgrades, currencies, crafting, or difficulty curves; when playtesters report boredom or grind; or when they ask whether a system is balanced.
category: design
---

# Loop and Economy

Balance problems are structural, not numeric. Tuning numbers on a broken structure produces a game that is differently broken. Find the structure first.

## Name the core loop

Write it in one line: **do X → get Y → spend Y to do X better**.

*Kill enemies → earn gold → buy weapons → kill enemies faster.*

If it cannot be written in one line, that is the finding — the game has several loops competing for the player's attention and none of them is the reason to keep playing. Common structural faults:

- **No feedback** — the player does X but nothing compounds. Feels like work.
- **Loop closes too slowly** — the reward is twenty minutes away. Attention is lost long before.
- **Loop closes instantly** — no anticipation, so no satisfaction.
- **Two loops competing** — a crafting system that pulls players out of the combat loop they came for.

## Sources and sinks

Every currency needs both, and they must be listed explicitly:

- **Sources**: where it enters the economy
- **Sinks**: where it leaves permanently

Failure modes, all of which show up in playtests as vague complaints:

- **Source with no sink** → inflation, currency becomes meaningless, late game is trivial
- **Sink with no source** → grind, players farm instead of playing
- **A dominant source** → one strategy crowds out everything else; the game collapses to it
- **Sinks that all buy the same kind of thing** → no meaningful choice, just an ordering

Write the table. Most economy problems are visible the moment sources and sinks are in two columns.

## Progression pacing

Two things must scale together: **player power** and **challenge**. When they diverge, the game breaks in one of two directions.

- Power outruns challenge → boredom, the second half is a victory lap
- Challenge outruns power → a wall, and players grind or quit

Both feel like "bad balance" to a player and neither is fixed by changing one number.

Multiplicative upgrades compound. Two independent 50% upgrades are a 125% increase, not 100%, and by the tenth upgrade the curve has left the design behind. Additive scaling is easier to keep control of; use multiplicative deliberately and sparingly, if at all.

## Dominant strategy check

For every meaningful choice, ask: is there a reason to ever pick the other option?

If one weapon is better in every situation, the others are not choices, they are decoration. Real choices need genuine trade-offs — power vs speed, safety vs reward, now vs later. A choice with a strictly correct answer is a tutorial about that answer.

## Testing without a full build

Model it in a spreadsheet before implementing. Twenty rows of "player at level N has X power, encounters challenge Y" surfaces a broken curve in ten minutes, where finding it by playing takes a week. Simulating a thousand runs of a proposed economy in a short script is usually a better use of an hour than tuning it live.

## Questions to ask the user

- What is the player doing in minute one, minute ten, and hour five? If those are the same, the loop lacks development.
- What is the thing that keeps someone playing past the first session?
- Which currency has the most sinks? Is it also the one with the most sources?
- What is the strongest strategy you know of, and why would anyone play differently?
