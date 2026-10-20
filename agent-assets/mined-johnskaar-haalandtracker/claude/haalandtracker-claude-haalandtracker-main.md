# HaalandTracker

Static bilingual site (EN at `/`, NO at `/no/`) tracking Erling Haaland's match
record for Manchester City, the Champions League and Norway. Live at
haalandtracker.com / haalandtracker.no. Work directly on `main` — this repo
pushes straight to main, no PRs, per the owner's preference.

## Verifying a match result — do this before writing anything

A real incident (25 Sep 2026): a match card was published showing Norway 2-1
Denmark with 1 Haaland goal, citing a single source (VAVEL). The actual final
score was Norway 3-2 Denmark with a Haaland brace — the cited source had
almost certainly been captured mid-match (a live-blog snapshot), not at full
time. The owner had to report this as a live, public-facing error.

To prevent this:
- Never write a score/goal count from a single source. Cross-check against at
  least two independent outlets (e.g. two of: ESPN, Sky Sports, Sofascore,
  beIN Sports, official club/federation sites, BBC).
- Prefer sources and phrasing that clearly describe a **finished** match
  ("full-time", "FT", a match report published after the final whistle) over
  a live-score page or a headline that could be a snapshot taken during play.
  A live-blog URL in particular ("live score", "live commentary") is a signal
  to re-search for the post-match report instead of trusting its cited number
  directly.
- If you find dedicated "his Nth international/career goal" milestone
  articles, treat them as a strong cross-check on cumulative totals, not just
  color for that one match — they're usually precisely fact-checked and catch
  a wrong goal count that a plain scoreline search would miss.
- Before publishing a new running total (caps/goals), sanity-check it against
  the site's OWN match-card history: count icon-chip goal icons (NOT
  `icon-boot` assist icons — the card markup uses `class="icon-chip"` for a
  goal and `class="icon-chip icon-boot"` for an assist, and both live inside
  `.match-icons`) across all played (non-`is-missed`, non-`is-planned`)
  `comp-nor` cards, and see that it lands on the number you're about to
  write. Do the same for the CAPS count, not just goals: count every played
  `comp-nor` card where Haaland was actually in the squad (i.e. NOT
  `is-missed`) — an externally-reported "Nth goal in game M" milestone is a
  check on both numbers at once, and a mismatch on either is a real signal,
  not noise.
  A mismatch usually means either the new match's goal count is wrong, or an
  earlier friendly was never added at all — this has now happened THREE
  times: Norway-Finland on 4 Sep 2025, Norway-Switzerland on 31 Mar 2026, and
  Norway-Sweden + Norway-Morocco (both pre-World Cup friendlies, 1 Jun and 7
  Jun 2026) were all completely missing from the site until caught this way.
  Friendlies are easy to miss because they don't show up in "World Cup
  qualifying" / "Nations League" style searches; search explicitly for
  Norway's fixture list for the window in question, not just the headline
  competitive matches — this is a recurring gap, not a one-off, so always do
  this check, not just when something already looks off.

## Build

Source of truth is `source/Main.en.dc.html` and `source/Main.no.dc.html`
(Claude Design canvas files: markup + an embedded `<script>` with the JS
state/render logic). They compile to `assets/site.en.js` / `assets/site.no.js`:

```
node build/transform.mjs source/Main.en.dc.html assets/site.en.js
node build/transform.mjs source/Main.no.dc.html assets/site.no.js
```

Run this after every edit to a `.dc.html` file — the compiled JS is what
actually ships.

**`assets/style.css` is the only real stylesheet.** The `<style>` block
embedded in the `.dc.html` files is preview-only for the canvas editor and
never reaches production. A CSS fix always goes in `assets/style.css`.

Every match-card needs a `comp-<key>` class (`pl`, `cl`, `cup`, `efl`,
`bundesliga`, `friendly`, `shield`, `cwc`, `nor`) — the competition filter
toggles hide/show cards by this class, and a missing one leaks the match
into unrelated filter views.

Before pushing, verify visually: serve the repo root
(`python3 -m http.server`) and screenshot the changed area with Playwright
(Chromium at `/opt/pw-browsers/chromium`) on both `/index.html` and
`/no/index.html`, desktop width 1280, checking for text overflow onto the
colored side ribbon.

## Existing automation — check before adding more

A recurring Routine ("Weekly HaalandTracker stats update", Mondays) plus a
fixture-aware one-shot follow-up ("Haaland match result check", retries
every 30 min up to 12 times) already handle finding new results, adding
match cards, and pushing to `main`. Don't create a second, competing
scheduled check for the same thing — extend or read this file instead.

**Timing override (28 Sep 2026, supersedes the 21 Sep 2026 note below):** the
first "Haaland match result check" attempt after a kickoff should fire at
kickoff + 60 minutes (1 hour) — not 120, and not the 140 minutes described
in that Routine's own stored prompt. (History: 21 Sep 2026 had already
moved it from 140 to 120; the owner has now asked for 60.) This file's
instruction takes precedence over that stored wording; a session can't
edit an existing Routine's prompt except from the conversation that owns
it, so use 60 minutes whenever you (re)create or update that one-shot
follow-up, and update the Routine's own stored prompt to match if you're
ever in a position to (e.g. asked to from its own conversation).

**Self-chaining (28 Sep 2026, owner request — "it should fire for each
match after one hour"):** don't wait for the next Monday weekly sweep to
queue the check for the *next* fixture after a match result lands — that
leaves a gap (e.g. the 24 Sep Denmark check fired and correctly updated
the site, but nothing then queued a check for the 27 Sep Portugal match,
which sat un-updated for a full day until this was fixed). Instead, every
time a "Haaland match result check" one-shot successfully finds and
publishes a result, it must immediately WebSearch for Man City's and
Norway's next scheduled match (any competition Haaland could feature in)
and, if a confirmed kickoff is known, create/update-and-rearm a new
one-shot "Haaland match result check" for kickoff + 60 minutes right then
— don't leave that solely to the weekly Routine's step 7. The weekly
Monday sweep remains a backstop for whenever the next kickoff isn't
confirmed yet at the time of the previous check.

**Don't skip an intermediate fixture when chaining (2 Oct 2026):** this
already went wrong once — after the 1 Oct Wales result, the chained
WebSearch for "Norway's next match" landed on the 14 Nov Wales *rematch*
and skipped the actual next match, Norway away at Portugal on 4 Oct 2026,
entirely (it sat missing from the site until the owner caught it:
"portugal norge 4.oktober er ikke med"). A generic "next fixture" search
can easily surface a result for a fixture further out while missing the
truly next one, especially around a Nations League window with two legs
close together. Before trusting a fresh WebSearch for "what's next",
check the site's own `is-planned` cards already in `source/Main.no.dc.html`
in date order first — if one of those is chronologically sooner than what
the search returned, that one is the real "next" fixture, not the search
result.

## Always keep the next fixture visible (25 Sep 2026, owner request)

At any point in time there should be an `is-planned` card for the next
known Manchester City Premier League match, the next known Man City
Champions League match (while City are still involved that season — see
below), and the next known Norway match — not just whichever fixture
happened to be added last. This is an ongoing rule, not a one-time fix:
after every match result update, check whether the competition(s) that
match belongs to still have an upcoming `is-planned` card, and if not,
add the next confirmed fixture for it (WebSearch the club's or
federation's official fixture list — don't guess a date).

- **Premier League**: always keep one `is-planned` comp-pl card for
  City's next PL match, all season. Keep doing this until the season
  actually ends (no PL card to add over the summer break) or Haaland is
  transferred away from Manchester City — if that happens, ask the owner
  how they want the site's scope to change rather than guessing.
- **Champions League**: same, but only "if possible/qualified" — i.e.
  only while Man City are still active in that season's Champions League
  (through the league phase, and however far the knockout rounds take
  them). If City are eliminated or don't qualify for a season, there's
  nothing to add — don't invent a fixture, and don't add a Europa League
  or Conference League one instead unless asked.
- **National team**: same idea for Norway's next confirmed match (World
  Cup/Euro qualifying, Nations League, or a confirmed friendly window) —
  keep exactly one upcoming `is-planned` comp-nor card lined up, the same
  way Portugal (27 Sep 2026) was already being kept as "next up" before
  this rule was written down.
- Match cards are chronological — insert the new `is-planned` card in
  date order among the existing cards (after the current last card in
  that timeline, before `</div>` that closes the timeline / before
  `<div class="timeline-legend">` if it's the very last card overall),
  in BOTH `source/Main.en.dc.html` and `source/Main.no.dc.html`, and only
  fill in kickoff time/venue once it's confirmed (use the existing
  `<span class="score-note">HH:MM kickoff</span>` / `avspark HH:MM`
  pattern; a "TBC" fixture without a confirmed kickoff can be added with
  just the date and `Scheduled · <venue>` if the venue is known, kickoff
  time omitted, like the earlier `is-planned` cards this session added
  did before their kickoff times were confirmed).
- This is on top of, not instead of, converting an existing `is-planned`
  card to a played result once that match has happened (see "Verifying a
  match result" above) — a newly-confirmed match should both close out
  the old placeholder AND get its own new `is-planned` placeholder added
  for whatever comes after it in that same competition.
- **Kickoff time zone (1 Oct 2026, owner request): the EN site shows the
  venue's own local kickoff time; the NO site shows Norwegian local
  time instead.** E.g. Wales–Norway at Cardiff City Stadium kicks off at
  19:45 UK time (BST) — `Main.en.dc.html` shows `19:45 kickoff`, but
  `Main.no.dc.html` shows `avspark 20:45` (Norway, CEST, is 1 hour ahead
  of the UK while both observe DST on the same late-March/late-October
  schedule, which has held for every match added so far). Convert the
  confirmed venue-local kickoff to Norwegian local time whenever you add
  or update an `is-planned` card's kickoff time in the NO file — do not
  just copy the EN file's number across. This applies to EVERY
  competition, not just an away national-team match: Man City's own
  Etihad Stadium is in England too, so a UK-hosted Man City or Champions
  League home fixture needs the same +1-hour conversion in the NO file
  (e.g. the PSG home card: `21:00 kickoff` in EN, `avspark 22:00` in NO).
  A match actually played in continental Europe (most of France,
  Germany, Spain, etc.) is already in Norway's own time zone, so no
  conversion is needed there — only UK/Ireland-hosted matches currently
  need the +1h adjustment; double-check the offset if a fixture ever
  lands somewhere else (North America, the rest of the world) rather
  than assuming it's always +1h.

## Stats cascade — updating hardcoded derived stats after a match

Match cards are added/edited directly, but several other numbers on the
site are hardcoded and do NOT update automatically from the match-card
data. After adding or correcting a played match, update every one of these
that the match's competition affects. Search for the current numbers each
time (don't trust line numbers — the file grows); make every change in
BOTH `source/Main.en.dc.html` and `source/Main.no.dc.html`, mirroring the
exact existing wording/format at each spot.

**Always: the "Last updated" footer badge.** In the footer (search
`foot-updated-row`), a `.topbar-meta`-styled badge reads e.g.
"Last updated: 17 Sep 2026" (EN) / "Sist oppdatert: 17. sep. 2026" (NO).
Whenever you add or correct a played match card (any competition), set
this to that match's own date, in the same "D Mon YYYY" / "D. mnd. YYYY"
format used on match cards — not today's real-world date, the date of
the most recently confirmed match. It moved out of the header into the
footer on 20 Sep 2026 at the owner's request (it was a stale hardcoded
"Aug 2026" that nothing kept in sync); don't move it back.

Progress-percentage formula for any "still achievable" records-chase
entry: `progress = Math.round(currentGoals / targetGoals * 100)`, where
`targetGoals` is the milestone number named in that entry's own title/desc
(e.g. 101 for "Overtake Robert Lewandowski (101 CL goals)", 140 for the
Ronaldo reference, 70 for "70 international goals").

**a) Any Manchester City match (any competition), if Haaland played:**
update the "Manchester City — key stats (club)" stat-mini tile — Games
+1, Goals += goals scored, Average = Goals/Games (2 decimals), and its
note ("All competitions, through City game N, DD Mon YYYY" /
"Alle turneringer, t.o.m. N. City-kamp, D. mnd. YYYY").

**b) Champions League match — additionally:**
- "Manchester City — key stats (CL)" tile (same formula, CL-only tally).
- "Champions League — goals per club" tile: the Man City sub-value, and
  its note ("N CL goals in total so far..." / "N CL-mål totalt så
  langt...").
- `CL_TOP`'s Haaland entry `value` (search `const CL_TOP`).
- `chartCl.entryBars`'s first bar, the Haaland value (search
  `entryBars: [bar('1. E. Haaland'`).
- `chartCl.topRankLabel`'s hardcoded "with N goals"/"med N mål" text
  (search `topRankLabel:`).
- The two CL "Still achievable" entries ("Overtake Robert
  Lewandowski"/"Forbigå Robert Lewandowski" and "Ronaldo and Messi's
  all-time records"/"Ronaldos og Messis totalrekorder"): update each
  `desc`'s goal count and its `progress` per the formula above.
- **The "Record chart — Champions League" race-to-milestone datasets**
  (search `const CL_50`, `const CL_100`, `const CL_150`, in both
  `source/Main.en.dc.html` and `source/Main.no.dc.html`). This was missed
  entirely until 14 Oct 2026, when `CL_100`'s Haaland trajectory (a
  flat `haaland: [...]` array ending at `[95, 100]`) silently drifted out
  of sync with reality — it depicted Haaland as having *already* scored
  100 CL goals (dot sitting on the 100 line) when his real total was 61,
  because nothing had ever updated it since it was first written. `CL_50`
  is low-risk (Haaland genuinely passed 50 CL goals already, so a flat
  solid-only `haaland: [...]` array ending at his real `[games, 50]` stays
  true forever — leave its shape alone). `CL_100` and `CL_150`, by
  contrast, track a milestone Haaland has **not yet reached**, so each
  one's Haaland line MUST use the two-part `haalandSolid`/`haalandDashed`
  split (not a single flat `haaland` array): `haalandSolid`'s last point
  is `[gamesPlayedSoFar, CL_TOP's current Haaland value]` — i.e. it has to
  match `CL_TOP` exactly, since that's the one number this file already
  keeps accurate — and `haalandDashed` starts at that same point and
  projects on to the milestone (100 or 150) using his current scoring
  pace, clearly still a projection, never already-achieved. Update
  `CL_CAPTIONS.m100`/`m150`'s text too if the projection's shape changes
  enough to be worth re-describing (both already say "Haaland's dashed
  line is a projection..."). Do this every time `CL_TOP`'s Haaland value
  changes, the same way every other entry in this list does — don't wait
  for someone to notice the chart looks wrong.
  **The same check applies to every *rival*'s `points` array in these
  three charts, not just Haaland's own line** — found 15 Oct 2026, one
  day after the above fix, when the owner noticed Mbappé's `CL_100` line
  also sat on the 100 line (ending at a fabricated `[125, 100]`) despite
  `CL_TOP` already correctly showing him on 68 (stale itself — the real
  figure, cross-checked across multiple outlets, was 71 in 99 games) —
  and Ronaldo's `CL_150` line and its caption claimed he'd "reached 150"
  at a fabricated `[160, 150]`, when he's permanently frozen on 140 (183
  games, Guinness World Record, retired — `active: false` in `CL_TOP`).
  Rivals have no dashed-projection field (only a flat `points` array), so
  a rival who hasn't reached that chart's milestone needs their `points`
  array truncated to end exactly at their own real current tally (pull it
  from `CL_TOP`, or re-verify if `CL_TOP`'s own entry for that player
  looks like it was never updated either — `CL_TOP`'s non-Haaland rows
  aren't covered by any other rule in this file, so don't assume they're
  current just because Haaland's is) — never left overshooting to the
  milestone itself. A rival who HAS genuinely passed the milestone (e.g.
  Ronaldo/Messi/Lewandowski in `CL_100`) legitimately ends exactly at it;
  that's correct and not the bug. If a milestone caption (like the old
  `m150` text) asserts someone "has reached" it, double-check that
  against the rival's real total before trusting it, the same as any
  other hardcoded claim on this site.

**c) Norway national-team match — additionally:**
- "National team — key stats" tile (Games/Goals/Average + dated note), if
  Haaland played.
- `NAT_NORWAY`'s Haaland entry `value` (search `const NAT_NORWAY`).
- **His own caps count, everywhere else it's quoted — even if he didn't
  score.** This tripped the automation once already (7 Oct 2026): after
  Wales (1 Oct) and Portugal (4 Oct), the "National team — key stats"
  tile correctly moved to 59 games, but the lane-fact line, the merit
  chip, the record-chart caption, and `NAT_WORLD`'s own Haaland `caps`
  field were all left at the old 57 — because those only get touched by
  the "only if he scored" refresh pass below, which correctly skipped
  both matches (no goals), but his own caps/date text isn't gated by
  that rule and still needs bumping on every match he plays, scoreless
  or not. Search for every occurrence of his current caps number (not
  just the ones named above) and update them together, so they can't
  drift out of sync with each other like this again.
- The next round-number milestone's achievable entry (e.g. "70
  international goals") — `desc` and `progress` per the formula above.
- Do NOT edit a frozen historical record-log entry like "Status: 61
  international goals" — that's a snapshot of when a past milestone was
  reached, not a live counter. Only add a brand-new dated History entry
  like it when Haaland crosses a genuinely new, notable milestone.
- **Only if Haaland scored** (this is what moves his own position in the
  world/Europe all-time scorer chart, `const NAT_WORLD`, search for it):
  also refresh every OTHER player in that array marked `active: true` —
  Ronaldo, Messi, Lukaku, Lewandowski, Mabkhout, Kane, Džeko, Mbappé,
  Mitrović and any others currently flagged active (NOT Chhetri or Ali
  Daei/Dahari/Puskás/Kocsis/Klose/Müller/Keane/Ibrahimović/Schlosser —
  those are retired, their numbers are frozen forever). Each entry has a
  `value` (goals) and a `caps` (appearances) field, both displayed as
  "value (caps)" on the chart — update both, not just goals, when either
  changes. Check against a steady source — Wikipedia's "List of men's
  footballers with 50 or more international goals" is the best single
  reference (comprehensive, continuously maintained, covers this whole
  list); cross-check anyone who looks like they moved with one more
  source (UEFA.com's "Europe's top international scorers" piece, or a
  plain WebSearch for "<player> international goals/caps total <month
  year>"). Don't reorder the array unless someone's new value actually
  crosses a neighbour's. Only do this pass when Haaland's own goal count
  just changed — not on every national-team match (e.g. skip it if he
  played but didn't score) and never as a standalone scheduled check.
  Update the "last verified" date in `europeCaption` and the `'world'`
  branch's caption string (search `Other players' totals last verified` /
  `Andre spilleres tall sist verifisert`) to the date you did this pass.
- **The `active` flag is an "on/off" switch tied to a player's actual
  LAST match, not to a retirement announcement.** A player who has
  announced retirement often still has one more official appearance to
  play (a farewell/testimonial match) — don't flip `active` to `false`
  until that match has actually been played. Example: Messi announced
  his retirement from Argentina on 31 Aug 2026 but was still `active`
  with a farewell match confirmed for 6 Oct 2026 vs Benin (his 208th and
  final cap) — a scheduled reminder exists to update his entry (`caps`
  to 208, `active` to `false`) once that specific match is confirmed
  played; don't jump the gun and flip a player inactive on an
  announcement alone, the way this file's own earlier guidance briefly
  did before the owner corrected it.
  Update the "last verified" date in both `europeCaption` and the
  `'world'` branch's caption string (search `Other players' totals last
  verified` / `Andre spilleres tall sist verifisert`) to the date you did
  this pass — that date is allowed to differ from the "Last updated"
  footer badge above, since it covers players other than Haaland.

**d) Premier League match:**
- DO update the live in-progress season entry in `PL_SEASONS` (search
  `const PL_SEASONS`): the current season's key (e.g. `'2026/27'`, added
  8 Sep 2026) has `done: false` and a `solid` array of
  `[matchweek, cumulativeGoals]` points instead of a final `points` array
  — append a new `[matchweek, newCumulativeTotal]` point after every PL
  match (whether or not Haaland scored), and bump `total`/`apps`. This
  feeds the "Record chart — club level" per-season comparison graph
  (`PER SEASON` tab) directly — it has no separate stat-mini tile of its
  own. Give it a `PL_SEASON_COLORS` entry (already set) and make sure its
  key is in the `seasonsOn` default-state object so it's shown by
  default. When the season actually ends, flip `done` to `true` and
  replace `solid` with a final smoothed `points` array in the same style
  as the completed seasons above it.
- Do NOT touch the "150 Premier League goals" / "Alan Shearer's all-time
  record" achievable-chase entries or the PL milestone-race caption (the
  ones citing "112 goals in 132 games" / "2022/23–2025/26 seasons") for
  every match. Those are deliberately frozen as of the end of the last
  completed season by design — a separate chart (`chart.club`, `TOTAL`
  tab) already projects the in-progress season with its own dashed line.
  Leave them alone unless Haaland crosses a big round-number milestone
  worth a new History log entry, or a season has just actually ended.

**e) FA Cup / EFL Cup / Community Shield / Club World Cup match** — only
(a) applies; there's no separate per-competition breakdown for these like
there is for CL.

**f) If a hardcoded stat looks relevant but isn't covered above, or
you're not confident of the right number** — leave it alone and say so in
your report rather than guessing. This is a public, live site; accuracy
beats completeness.
