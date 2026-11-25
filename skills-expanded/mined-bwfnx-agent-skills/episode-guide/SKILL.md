---
name: episode-guide
description: build a season-by-season guide to the best and most skippable episodes of any tv series, podcast, or movie franchise — god mode peaks, fan favorites, core arc episodes, skim and skippable filler, an arc-only path for serialized long shows or a best-of path for episodic ones, and the single best episode of the series. use when asked for "best episodes of x", "episodes to watch with my kids", "what can i skip in x", "watch guide for x", or "is x worth finishing".
---

# Episode Guide

Produce a researched, spoiler-light guide that tells the user what to watch, what matters, and what to skip — season by season, in original release order.

## Inputs

- **Title** (required). If ambiguous (remakes, reboots, same-name shows), ask which one before researching.
- **Scope** (optional): whole series, specific seasons, or "just tell me what to skip."
- **Spoiler level**: default spoiler-light (see Rules). Honor "spoilers fine" or "zero spoilers" if the user says so.
- **Watching with kids** (optional): the child's age, or "family" with no age. Turns on the family flag and Family Path below. Default age if none given: 8.
- **Already watched** (optional): entries the viewer has seen. Mark them "seen" in the tables, and start the Family Path or any path at the first unseen entry.

Works for:
- **TV series** — seasons and episodes
- **Podcasts** — seasons, or years if the show has no seasons; entries are episodes
- **Movie franchises** — group by era or phase; entries are films

## Tiers

Assign every listed entry exactly one tier. Do not list unremarkable "fine" episodes unless the user asks for a complete list.

| Tier | Meaning | Test |
|---|---|---|
| 👑 **Series Best** | The single best entry of the whole run | Highest combined standing across all sources. Exactly one, and it must be a regular episode (see Specials below). |
| ⚡ **God Mode** | The show at its absolute peak | Rated well above the series average (roughly top 5–10%) AND appears on critic or major-outlet best-of lists |
| ❤️ **Fan Favorite** | Beloved rewatch staples | Strong fan ratings/polls or cultural staying power, even if critics are lukewarm |
| 🧵 **Core Arc** | Needed to follow the main story | Advances the central mythology, character arcs, or sets up payoffs. Not necessarily great. |
| 👀 **Skim** | Weak episode with a few scenes that matter | Below average, but contains a key scene, reveal, or introduction. Name what to catch ("watch the last 5 minutes") without spoiling it. |
| ⏭️ **Skippable** | Safe to skip | Below the series average AND standalone with no arc impact. Must meet both. |

If an entry qualifies for multiple tiers, use the highest (Series Best > God Mode > Fan Favorite > Core Arc > Skim). A skippable episode can never also be Core Arc or Skim — if anything in it matters to the story, it is not skippable, however bad it is.

**Specials and clip shows.** Retrospectives, reunions, and "best of" specials often top rating lists on nostalgia alone. They can be ❤️ Fan Favorites, but never 👑 Series Best — pick that from regular episodes and mention the special in the Headline if it outranks the pick.

A clip show that **reuses footage the viewer has already seen** (recaps, outtake reels, countdown specials) is ⏭️ Skippable by default, even without a below-average rating, because it adds nothing new. Exception: a clip show made of **new material** — a parody of the format, flashbacks to events that never aired ("Paradigms of Human Memory" in Community, "Clip Show" parodies) — is a real episode. Tier it on its ratings like any other.

**Arc flag (separate from tier).** Tag every entry the main story needs as `arc: yes`, whatever its tier. A Fan Favorite or God Mode episode can also be arc-essential ("Tall Tales", "Death's Door"), and the tier alone would hide that. Show the flag in the table ("also needed for the arc") and use it to build the Arc-Only or Best-Of Path.

**Family flag (separate from tier, only when watching with kids).** Mark each listed entry for the child's age:
- 👪 **Kid pick** — fun and suitable for this age: clear stakes, not frightening, nothing the child needs a lot of context for.
- ⚠️ **Not for this age** — frightening imagery, gore, sexual content, or heavy themes (death of a child, torture, body horror). Always show this, even on ⚡ God Mode or 👑 Series Best episodes, with a one-line reason ("body-horror ending").
- Unmarked — fine to watch but may bore or confuse a young kid.

**Show-level ratings only.** Often a parent guide rates the whole show or film series but not individual episodes. Then report the show-level age and its main concerns in a short family note at the top, leave episodes unmarked, and say plainly that episode-level calls weren't possible. Don't invent 👪 or ⚠️ tags to fill the gap. For films, each film usually has its own rating and parent review, so mark each one.

Quality and suitability are separate calls: a God Mode episode can be ⚠️, and a middling episode can be a great 👪 pick. You can list extra entries purely as 👪 picks (tier them Fan Favorite or leave the tier as the ratings dictate). Base the call on parent-focused sources, not the show's overall rating.

## Research

Blend sources and cite them. Search each separately rather than in one combined query.

1. **Ratings**: IMDb episode ratings (or Rotten Tomatoes / Letterboxd for films; Apple/Spotify ratings and listener rankings for podcasts). Note the series average so "above average" means something.
2. **Critics**: best-episode lists from major outlets (Vulture, The A.V. Club, Rolling Stone, IGN, Collider, etc.).
3. **Fans**: Reddit threads and polls ("best episode of X", "what can I skip in X", "filler episodes X"), fan wikis for arc/mythology tags.
4. **Arc mapping**: fan wikis or episode guides that label mythology vs. standalone ("monster of the week") episodes.
5. **Parent guides** (family flag only): Common Sense Media, IMDb Parents Guide, and "best episodes for kids" lists. Never mark ⚠️ or 👪 on a guess; if no parent source covers an episode, leave it unmarked.

Verify air dates and episode numbers against a reliable episode list (Wikipedia episode list or IMDb). Never guess an air date — if unverified, say so.

When sources disagree, note it briefly ("critics love it, fans are split").

**When a source is blocked or unreadable** (Reddit, Fandom wikis, and IMDb episode pages often refuse automated fetches), move down this fallback order instead of guessing:
1. IMDb-derived articles (Screen Rant, Collider, CheatSheet "highest-rated episodes" pieces) for ratings
2. Wikipedia per-episode pages, which often list critic scores (IGN, TV Fanatic, Den of Geek)
3. Long-form fan viewing guides on Medium, Substack, or fan sites for watch/skip calls
4. Critic "worst episodes" lists to confirm skip candidates

Say in the Sources section which sources were blocked. If a season still has too little data to call skips, leave its skip list empty and say so — never pad it.

## Long-series mode

Trigger when the series has **8+ seasons or 100+ episodes** (e.g., Supernatural, The Simpsons, Grey's Anatomy) or when the user asks for it.

First, decide the show type — it changes which path you build:
- **Serialized** (a story runs across episodes: Supernatural, Lost, Breaking Bad) → build an **Arc-Only Path**.
- **Episodic** (each episode stands alone: sitcoms like 30 Rock, procedurals, anthologies, docuseries and reality like MythBusters) → build a **Best-Of Path** instead. An arc path for an episodic show is short, dull, and misses why people watch.
- **Mixed** (monster-of-the-week with a spine: The X-Files, Buffy) → build the Arc-Only Path, and offer the Best-Of Path in one line.

State the show type and which path you chose in the Headline.

In this mode:
- Be more aggressive about identifying ⏭️ Skippable standalones — this is the main value for long shows.
- **Arc-Only Path** (serialized/mixed): the minimum list of episodes needed to follow the story — every entry flagged `arc: yes`, plus all ⚡ God Mode and the 👑 Series Best — in release order, with a total episode count and rough runtime saved. Include 👀 Skim entries with their "what to catch" note.
- **Best-Of Path** (episodic): 👑 Series Best + all ⚡ God Mode + all ❤️ Fan Favorites, plus any `arc: yes` entries (character milestones, finales), in release order, with a total episode count and rough runtime saved. For episodic shows the `arc` flag marks the few relationship or format milestones worth knowing about, not a plot.
- Flag seasons that are weak overall ("Season 8 is widely considered a dip — the path is enough here").

## Output

### 1. Headline
- **👑 Series Best**: title, S#E#, original air date, one spoiler-light line on why.
- One sentence on the show's overall arc quality (e.g., "Peaks in seasons 2–5; later seasons are skim-friendly").

### 2. Season tables
One table per season, entries sorted by **original release date**:

| Ep | Title | Air date | Tier | Arc | Why (spoiler-light) |
|---|---|---|---|---|---|
| S1E03 | ... | 2005-09-27 | ⚡ God Mode | yes | One line that sells it without giving it away |

### 3. Season watch guides
Under each table, 2–4 sentences: how strong the season is overall, which episodes are non-negotiable, and what can safely be skipped. Keep it conversational.

### 4. Arc-Only Path or Best-Of Path (long-series mode only)
Whichever the show type calls for. Numbered list in release order, plus: total episodes, episodes skipped, approximate hours saved.

### 5. Family Path (only when watching with kids)
The 👪 Kid picks in release order, plus a short "Hold off until they're older" list of every ⚠️ entry with its one-line reason. State the age it was built for.

### 6. Sources
Short list of links used.

## Rules

- **Spoiler-light by default**: describe the hook, tone, or stakes — never the twist, death, reveal, or ending. "A case goes sideways in a way that changes the show" is fine; "X dies" is not. Skip the one-liner entirely for episodes whose premise itself is a spoiler.
- **Release order only**: sort by original air/release date, not streaming or production order. Note it if the two differ meaningfully.
- **Multi-part episodes count once**: a two-parter or double-length episode that aired as one block ("Hogcock! / Last Lunch", a one-hour finale) is a single entry with a code range (S7E12–13) and the first air date. Two parts that aired on different nights stay separate entries, each tiered on its own.
- **Numbering conflicts**: when sources disagree on season or episode numbers (common for docuseries, reality, and anything re-cut for streaming), pick one source — the network's or Wikipedia's list — say which in the Headline, and use it consistently. Prefer episode titles over numbers in one-liners so the reader can match either scheme.
- **No filler padding**: if a season has no God Mode episodes, say so instead of stretching the tier.
- **Be honest about thin data**: for niche podcasts or obscure shows with few ratings, say the rankings rest on limited sources.
- **Keep one-liners to one line.**
- If the output is long (big series), offer the full guide as a document the user can keep, and give the headline + the path in chat.

## Lessons from testing

- **Pull tables verbatim.** When extracting episode lists from a web page, ask for the table rows copied as-is, one year or season block at a time. Spot-lookup summaries have mixed up rows and dates.
- **Reread notes against the data before publishing.** Explanatory notes ("two episodes stay in because...") drift from the table as you edit. Check every sentence that describes the data against the final entries.
- **Test changes on a deliberately different case.** Each rule in this skill came from a show that broke the previous version: sitcom arcs (30 Rock), clip shows (MythBusters, Community), family ratings (TNG, MythBusters), and films (Star Wars). Before changing a rule, run it on a show unlike the last one.
