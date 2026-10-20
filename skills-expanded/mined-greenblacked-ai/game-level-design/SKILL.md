---
name: game-level-design
description: "Lay out a game level as a space: fix the player metrics — standing and crouching height, step height, jump height and distance, sprint speed, cover height, door width, and the blockout grid — then derive every dimension from them, step the grid down from massing to detail, sort each segment into explore, combat, choreo or puzzle and chart intensity over time so no category repeats back to back, build wayfinding cues into the blockmesh and playtest there before art, and place streaming and occlusion seams while the structure can still move. Use whenever someone says 'lay out this level', 'my players get lost', 'the pacing drags in the second half', 'blockout', 'greybox' or 'level metrics'. Not for engine choice or game feel (game-builder), enemy stats and difficulty (game-balance), frame budgets (game-performance), the feature spec (game-design-doc) or import settings (game-assets)."
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Game Level Design

A level is finished as a design when every dimension in it came from a player metric fixed before the geometry existed, when its pacing can be read off a chart instead of argued about, and when the guidance it gives was proved by watching people walk through grey boxes rather than asserted by the person who built them.

Two failures produce most of the wasted work, and neither is the one people expect. The first is geometry before metrics: rooms are built to what looks right on screen, the character controller is tuned afterwards, and now the step heights are unclimbable, the cover is chest-high for the wrong chest and the doorways read as tight. The second is treating guidance as a checklist — landmarks placed, leading lines drawn, lighting warm at the exit — and then shipping without ever watching a player fail to use any of it, because the checklist felt like evidence and nothing in it is falsifiable. This skill exists to put a gate in front of both: numbers before shapes, and observed behaviour before art.

Everyone already knows to block out before art; restating it changes nothing. What is worth saying is why the stage collapses in practice. The blockout gets art applied to it while the layout is still being argued, so every subsequent layout change costs an art re-do, and the layout stops changing — not because it is right, but because it became expensive. The stage gate below is the version of that rule with teeth: the pacing chart and the wayfinding playtest both have to be done, and their findings acted on, while the level is still coloured boxes.

## Scope

Use for: laying out a level, a map, an arena, a hub or a mission space; fixing a level whose players get lost, whose pacing sags, whose fights are shooting galleries or corridors with one route; deciding the player metrics and the blockout grid before a team starts building rooms; running a beat chart over an existing level to find what repeats; and deciding where the streaming and occlusion seams go while the macro-structure can still move.

Do not use for: choosing an engine, building the core loop or tuning how the character feels to control — that is `game-builder`, which makes the thing this skill lays out space for. Enemy statistics, difficulty curves, spawn counts and economy are `game-balance`: this skill owns the shape of the arena and hands over everything that is a number on an enemy. Frame budgets, capture and the optimisation pass are `game-performance`; the only part of that here is the layout consequence of where a streaming or occlusion boundary lands. The feature specification, its acceptance criteria and the cross-functional review process are `game-design-doc`. Texture compression, LOD and import settings are `game-assets`.

## Scale and game type

Scale here means what the work requires rather than a headcount or a budget: indie/A is one small team wearing every hat; AA adds specialised roles, several platforms and a publisher's milestones; AAA adds many specialised disciplines, external studios and a simultaneous multi-platform launch.

| | Indie/A | AA | AAA |
| --- | --- | --- | --- |
| Who builds and tests | One person owns metrics, blockout and the step 7 playtest | Level design and the playtest are different people, and streaming seams are a shared call with an engineer | A level team per zone, plus a dedicated streaming or technical-art owner for step 6 |
| Playtesting (step 7) | A handful of testers, run by whoever built the level | Internal QA runs the wayfinding pass on a schedule rather than ad hoc | Playtests run at the order of magnitude step 7 cites, across multiple builds |
| Streaming seams (step 6) | Streaming may be skipped when the level fits in memory whole, but the occlusion and culling seams step 6 describes — areaportals on windowless doors, where the engine needs them — still apply | Settle while the macro-structure can still move | Mandatory before the structure locks, across every zone that streams |

Open world and large 3D games carry the most risk from this skill: the streaming and occlusion work in step 6 and a metrics-first blockout are load-bearing rather than optional. Competitive multiplayer levels lean instead on the arena properties in step 4 — route count, verticality and flanking space — over the pacing chart in step 3, which assumes a single-player beat structure.

## Workflow

### 1. Fix the player metrics before any geometry exists

This is the gate the whole discipline rests on. Before a single wall is placed, write down and commit to:

standing height, crouching height, step height, jump height and jump distance, walk speed, sprint speed, camera height, cover height, door width, and the blockout grid itself.

Every dimension in the blockout is then a multiple of one of those numbers, not a judgement made in the viewport. A level built to eye rather than to metrics is one where the fixes are structural: a cover piece that is two units too tall does not read as two units wrong, it reads as a fight that does not work.

Source engine numbers, which are published on the Valve Developer Community wiki and are worth citing as a worked example of the relationships rather than as values to copy: standing bounding box 72 units tall, crouching 36 units — exactly half — minimum walkable opening 73 units, standard door 56 by 112 units. Note that the walkable opening is one unit taller than the standing box; that unit of slack is the kind of detail a metrics table carries and a screenshot does not.

Derive the equivalent numbers in the engine actually in use by measuring the character controller, not by copying a figure found in a forum thread. For Unreal in particular, community sources disagree about the default capsule dimensions and there is no single authoritative document to settle it, so a number quoted from memory is a number that will be wrong in a way nobody catches until a doorway is built to it.

**On the cost of changing them later, state the claim accurately.** For modular kits it is documented: Joel Burgess and Nate Purkeypile, "Skyrim's Modular Approach to Level Design" (GDC 2013), describe a late change to the kit's tile grid meaning the existing kit no longer fitted levels that had already been built with it — the pieces stopped lining up, at a point where a great deal had been built. For hand-built levels the same mechanism generalises, and it is the reason to fix the metrics first there too, but that generalisation is not independently proven in the published sources. Do not present it as if it were.

`references/player-metrics.md` — read at this step, before placing geometry: the full metrics checklist, the Source numbers with what each relationship means, the grid-stepping progression, and how to measure the equivalents in another engine.

### 2. Step the grid down as the level moves from massing to detail

Block out on a coarse grid and subdivide it only as the level's questions get smaller. The Level Design Book documents Quake's progression: 64 units for massing, then 32, then 16, then 8 as detail arrives.

The point is not tidiness. A coarse grid makes a whole room cheap to move, which keeps the layout arguable during the stage where argument is cheap. Detail-grid geometry is expensive to move, so a level that goes to an 8-unit grid early has locked its macro-structure without anyone deciding to.

### 3. Chart the pacing rather than defending it

Valve's beat method, as documented in the Level Design Book, is the one procedure here that produces a checkable artefact. Sort every segment of the level into one of four categories:

| Category | What the player is doing |
| --- | --- |
| Explore | Moving through space, finding the way, taking it in |
| Combat | Fighting |
| Choreo | Watching something scripted happen |
| Puzzle | Solving something |

Then plot the level: time along the horizontal axis, intensity from 0 to 100% on the vertical.

**The gate:** the same category must not repeat back to back without a deliberate, written reason. Two combats in a row is a sequence that will read as a slog; two explores in a row reads as empty. A reason can be a good one — a rising three-fight crescendo is a real design — but it has to be a decision on the chart rather than an accident of how the level grew.

`references/beat-chart.md` — read at this step and keep it open while charting: the four categories with worked examples of what falls into each, how to assign intensity without it becoming a vibe, a worked chart, and what the common failure shapes look like.

### 4. Build encounters as spaces before they are enemy counts

An arena is a layout problem first. Kurt Loudy and Jake Campbell, "Embracing Push Forward Combat in DOOM" (GDC 2018), describe the space that makes aggressive combat work: vertical routes through the arena, several routes across the ground so the player cannot be cornered, and resource placement that pays the player for moving towards the fight rather than away from it.

Own four properties of the space and check each before anyone tunes a number:

- **Route count.** How many ways across the arena are there, and does closing one leave the player with an option.
- **Verticality.** Can the player change elevation during the fight, and does elevation change what they can see and reach.
- **Cover geometry.** Where does cover exist, how tall is it against the metrics from step 1, and does it hold up when the threat arrives from the other side.
- **Flanking space.** Can the player be approached from more than one direction, and can they do the same in return.

A fight that is not working is usually a space with one route and no elevation, and no enemy statistic fixes that. Hand enemy health, damage, spawn counts and difficulty tuning to `game-balance`: this skill decides the room the fight happens in.

### 5. Build the guidance into the blockmesh, and playtest it there

There is no formula that predicts whether players will find their way. The Level Design Book is explicit that playtesting — watching where players actually go — is the only way to know, and nothing published offers a substitute.

The procedure that is a gate comes from David Shaver and Robert Yang, "Invisible Intuition: Blockmesh and Lighting Tips to Guide Players and Set the Mood" (GDC 2018): build the guidance cues into the blockmesh itself, and playtest them at blockmesh stage, before art. Guidance that only works once the art is in is guidance nobody can afford to change.

Landmarks, leading lines, contrast and lighting are the techniques to apply. They are techniques, not evidence: a level with all four applied and no playtest behind it has been decorated, not validated. Apply them, then go to step 7 and find out.

### 6. Settle the streaming and occlusion seams while the structure can still move

Two technical facts shape layout early enough that retrofitting them means re-authoring macro-structure.

- **Source engine, areaportals.** Attach an areaportal to every windowless door. A door in this engine is two things at once — a gameplay chokepoint and a mandatory visibility-culling seam — and a layout that has no such doors has no place to put the seams. Discovering that after the level is built means changing where rooms meet.
- **UE5 World Partition.** Loading range should be at least twice the cell size, and three to four times for fast movement such as vehicles or flight; the default cell size is 256 m. These figures are corroborated across community sources rather than read from Epic's primary documentation, so treat them as a starting point to verify in the project rather than as a specification.

What this skill owns is the layout consequence: where the seams fall, and whether the level's shape gives them somewhere to be. The frame budget, the capture and the optimisation pass belong to `game-performance`.

`references/technical-gates.md` — read at this step, and again before the layout is signed off: areaportals and what a windowless door costs when it has none, World Partition cell size and loading range with the caveat on their provenance, and how a streaming boundary constrains a layout.

### 7. Playtest by watching, and refuse the number that would make it feel rigorous

Observe behaviour rather than collecting opinions. Where does the player stop moving. Where do they backtrack. Where do they hesitate at a junction. Where do they die more than twice. Each of those is a location in the level, which is something you can change; "I found it a bit confusing" is not.

Self-report is the weaker instrument in both directions — players rationalise being lost as their own fault, and they cannot report a cue they never consciously noticed. Watch first, ask afterwards, and treat what they say as a hypothesis about what you saw.

On scale: Valve's documented practice for Half-Life 2 was roughly 100 playtesters per chapter. That is the order of magnitude a studio brought to this problem, not a requirement for a two-person team — and it is a count of sessions, not a threshold for a decision.

**There is no published threshold, and inventing one is the failure this skill exists to prevent.** No studio has published a rule of the form "if N% of players get lost, redesign the area", and a number invented to make a playtest report sound rigorous is worse than no number, because it moves the argument from what was observed to whether the made-up bar was cleared. Report what you watched: how many testers, how many took the wrong branch at which junction, where they backtracked, and what you changed as a result.

## Anti-patterns

**Geometry before metrics.** The rooms look right and the character cannot use them, and the fixes are structural rather than cosmetic.

**Copying capsule or bounding-box numbers from a forum.** The number is quoted with confidence, disagrees with the engine in use, and is only found to be wrong when a doorway built to it feels tight.

**Going to the detail grid early.** Macro-structure gets locked by the cost of moving it, not by anyone deciding the layout was right.

**A wayfinding checklist as evidence.** Landmarks placed, leading lines drawn, lighting warm at the exit, and no one has yet watched a player fail to use any of it.

**Art on a blockout whose layout is still moving.** Every subsequent layout change now costs an art re-do, so the layout quietly stops changing.

**An invented playtest threshold.** "Redesign if more than 30% get lost" sounds like a standard and is not one; it turns an observation anyone could act on into a bar nobody agreed to.

**A pacing chart made after the level is built.** Drawn to justify what exists rather than to change it, which is why the repeated category on it never gets fixed.

**Enemy counts as the fix for a fight that does not work.** The arena has one route and no elevation; adding or removing enemies changes how long the same problem lasts.

**A level with no windowless doors in an engine that needs them for culling.** There is nowhere to put the visibility seams, and the discovery arrives after the macro-structure is set.

**Asking testers what confused them instead of watching where they stopped.** The answer is a rationalisation, and it points at a feeling rather than at a junction you could move.

## References

- `references/player-metrics.md` — read at step 1, before placing any geometry: the metrics to fix, the Source engine worked example and what each relationship means, the grid-stepping progression, how to derive the same numbers in another engine, and the accurate version of the cost-of-changing-them claim.
- `references/beat-chart.md` — read at step 3 and keep open while charting: the four Valve categories, how to assign intensity, a worked chart, the repeated-category check, and the failure shapes that show up on a finished plot.
- `references/technical-gates.md` — read at step 6 and before sign-off: areaportals and windowless doors in Source, World Partition cell size and loading range with their provenance marked, and how each constrains a layout that is already built.
- `references/further-reading.md` — read when you want the source rather than the summary: the Level Design Book, the four GDC talks this skill draws on, Valve's developer commentary tracks, and the Valve Developer Community wiki, with what each is good for and which of them teaches reading levels rather than building them.
