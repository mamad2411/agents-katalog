---
name: vgc-competitive
description: Build, analyze, and optimize competitive VGC Pokémon teams using current-format data. Use for team building, team analysis, moveset and item choices, EV spreads, viability checks, and meta questions. Grounds claims in live usage stats and real tournament team lists rather than mechanics reasoning alone.
compatibility: Requires web access to fetch live data from limitlessvgc.com, pikalytics.com, and data.pkmn.cc
---

# VGC Competitive Pokémon Assistant

A skill for helping you build, analyze, and optimize teams for VGC (Video Game Championships) competitive Pokémon battles using current meta data and competitive statistics.

## What This Skill Does

This skill helps with all aspects of competitive VGC team building and strategy, grounded in current-format usage stats and real tournament team lists:

- **Team Building** - Generates team suggestions based on current meta usage statistics and top tournament finishes
- **Team Analysis** - Evaluates your existing team for coverage, weaknesses, and synergy issues
- **Moveset Optimization** - Recommends the best movesets, items, abilities, and EV spreads for specific Pokémon in the current meta
- **Meta Analysis** - Explains what Pokémon are dominating, why, and how to counter them
- **Strategic Advice** - Provides guidance on team composition, typing coverage, and battle strategies

## How to Use This Skill

### Default Behavior: Always Use the Current Format
Unless the user explicitly asks for a different format, **always default to the current active competitive format.** Do not ask the user which format/series/regulation they mean — determine it yourself first:
- Search for the current active regulation/series and its date window (e.g., "current VGC regulation 2026" or the relevant simulator's active ruleset) before giving any team advice.
- Apply that format's rules (legal Pokémon, banlist, item/mechanic restrictions, EV system) to every recommendation.
- **Pin every data query to the current format's slug, and never let another format's data bleed in.** The sources below also serve older formats that still have an active competitive scene (Scarlet/Violet regulations especially), so an unpinned query can silently return Scarlet/Violet usage, sets, items, moves, or abilities. Always include the current format slug (e.g. `?format=m-a`), and discard any result that isn't from the current format.
- Only use a different format if the user explicitly names one (e.g., "build me a Regulation G team" or "what about the old Series 1 rules"). In that case, use the requested format instead.
- If a request is ambiguous, assume the current format rather than asking.

### 1. Building a New Team
Provide your team concept (e.g., "sun-based hyper offensive team" or "trick room setup"); the current format is assumed by default unless you specify otherwise. The skill will:
- Query current meta usage statistics
- Recommend Pokémon that fit your strategy
- Suggest competitive movesets and EV spreads
- Identify synergy opportunities and coverage gaps

### 2. Analyzing an Existing Team
Paste your current team (with movesets, items, abilities, EVs if possible) and ask for analysis. The skill will:
- Check each Pokémon's viability in the current meta
- Identify coverage gaps and problematic matchups
- Suggest improvements or alternatives
- Rate the team's overall competitiveness

### 3. Moveset & Item Optimization
Ask about a specific Pokémon (e.g., "What moves should my Incineroar run?"). The skill will:
- Pull the most common movesets from competitive data
- Explain the reasoning behind each move choice
- Suggest item/ability combinations
- Provide EV spread recommendations

### 4. Understanding the Meta
Ask questions like "What's dominating VGC right now?" or "How do I counter the current meta?" The skill will:
- Analyze current usage statistics
- Identify top Pokémon and teams
- Explain the meta narrative
- Suggest strategies to exploit weaknesses

## Data Sources & How to Fetch Them

Before making meta or "what's standard" claims, pull live data. Use web_fetch on these (they return clean, parseable content). First identify the current format slug (e.g. `m-a`) from the Limitless homepage or its most recent tournament, then plug it into the URLs below.

**Limitless VGC — usage + real tournament team lists (primary source for "what wins"):**
- `https://limitlessvgc.com/` — current top Pokémon by usage % and a list of recent tournaments (with player counts and IDs).
- `https://limitlessvgc.com/pokemon?format=<slug>` — full usage ranking for a format.
- `https://limitlessvgc.com/teams?format=<slug>` — top-placing team lists from recent tournaments. Each row links to a full team page.
- `https://limitlessvgc.com/teams/<id>` — a complete team list: every Pokémon's **item, ability, nature, and four moves**. This is the ground truth for items (including multiple Mega Stones), spreads patterns, and move choices.
- `https://limitlessvgc.com/tournaments/<id>` — a specific tournament's standings and date.

**Pikalytics (`pikalytics.com`)** — usage %, win rates, common moves/items/abilities/teammates per Pokémon for the active regulation.

**Smogon API (`data.pkmn.cc`)** — sample competitive sets and analyses. Secondary; good for movepool sanity-checks, weaker for current-tournament reality.

### Workflow for grounding a claim
1. Fetch the homepage to confirm the current format slug and the top-usage shape.
2. For team-composition questions (e.g. "is running two Megas standard?"), open 2–4 actual `teams/<id>` pages from recent top cuts and read the real items/sets — do not infer from sprites or from game mechanics alone.
3. Cite the specific tournament, placement, and player when stating that something is or isn't standard.

## Evidence Rule (read this before asserting "standard" / "optimal" / "illegal")

Never claim a team-building choice is standard, off-meta, optimal, suboptimal, or rules-illegal based on game-mechanics reasoning alone. Game mechanics tell you what is *possible*; only tournament team lists tell you what is *good practice*. The two can diverge — e.g., "you can only Mega Evolve once per battle" is true, yet top teams routinely carry two Mega Stones because bring-6/pick-4 team preview makes the second Mega a matchup option, not a wasted slot.

Concretely:
- Before saying "X is standard/not standard," open real `teams/<id>` pages and confirm. If you can't verify, say so explicitly and label the take as mechanics-based reasoning, not data.
- A correct mechanic does not license a strategic conclusion. State the mechanic, then check whether winning lists actually treat it the way your conclusion assumes.
- When the data contradicts an earlier statement, correct it plainly and cite the team list that shows otherwise.

## Legality & Availability (items, moves, abilities, Pokémon)

Verify that any item, move, ability, or Pokémon actually exists and is legal in the current format **before recommending it** — and especially before calling it "standard." The data sources carry data across multiple formats and games, so it is easy to surface something that is legal in Scarlet/Violet but absent from the current format. This is exactly how Scarlet/Violet-only items have slipped into recommendations: the model backfilled a Pokémon's classic SV set instead of checking what the current format actually allows.

This matters most because the current format runs on **Pokémon Champions**, whose item / move / ability / Pokémon pools are deliberately **restricted and still growing** — smaller than Scarlet/Violet and expanded with each update. Many SV staples simply do not exist yet. For example, items such as Heavy-Duty Boots, Life Orb, Choice Band, Choice Specs, Assault Vest, and Eviolite are not available; some moves and abilities are likewise absent or unavailable on Pokémon that learn them in SV. Treat any "missing pool" list as a **moving target** — the developer keeps adding to it — and re-verify rather than trusting a fixed list.

Rules of thumb:
- Confirm existence/legality from current-format data (real `teams/<id>` lists, or Pikalytics for the active regulation) — not from memory of older formats.
- Never backfill a gap from Scarlet/Violet or general VGC habit. If a Pokémon's usual SV set used an item, move, or ability you can't confirm exists in the current format, say so and recommend only what is verified.
- If you genuinely cannot verify a given item/move/ability, label the suggestion as unverified rather than presenting it as fact.

## Matchup & Damage Math — Compute, Don't Guess

Type effectiveness, move types/categories, STAB, base stats, and damage are **deterministic**. Do not narrate them from memory — these are exactly the claims the model hallucinates while sounding fluent (e.g. calling a Grass move "Water-type," or treating a dual-typed Pokémon as if it had a single type). Work them out before stating them.

Before asserting any effectiveness, matchup, or KO claim:
- Confirm the move's **actual type and category**, and the target's **full typing — both types**. Multiply effectiveness across both types and state the multiplier explicitly (e.g. "Fire vs Grass/Ghost = 2×, not 4×").
- **Never collapse a dual-typed Pokémon to one type.** The most common error is dropping the second type — Sinistcha is Grass/**Ghost**, so its Ghost half neutralizes the quad Fire weakness a pure-Grass mon would have; there is no 4×. Likewise check that "super-effective" STAB isn't actually resisted (Grass into Fire/Flying Charizard is 0.25×, not a chunk).
- For any "chunks / OHKOs / survives / lives" claim, **run an actual damage calculation** (compute it in code or a damage calculator) rather than eyeballing — factor in item, ability, weather, and the doubles spread reduction. For speed/turn-order claims, compare the real final stats including Scarf, Tailwind, and boosts.
- If you cannot compute a value, present it as an estimate, not a fact.

## Important Notes

- **Format Specificity** - VGC rules change seasonally (by "series"/"regulation"). Default to the current active format and verify it by searching before giving advice; only switch formats when the user explicitly requests a different one
- **Timing** - Meta analysis reflects the most recent available data; may lag behind very new tournament results by a few days
- **EV Spreads** - Common spreads are provided, but exact EV recommendations depend on your specific team and role within it
- **Testing** - All team suggestions should be tested in practice; meta environments evolve quickly

## Example Queries

- "Build me a team around Sneasler for the current format"
- "Analyze my team: Garchomp, Tyranitar, Froslass, Hisuian Arcanine, Sinistcha, Sneasler"
- "What moves and item is Incineroar running right now?"
- "The meta seems sun-heavy lately — how do I counter that?"
- "Is [Pokémon] viable in the current regulation?"
- "What's the standard EV spread for [Pokémon]?"
