---
name: game-live-ops
description: "Run a game after launch: a content and season calendar planned ahead rather than assembled week to week, events with a stated purpose, and economy tuning scheduled with guardrails — this decides what changes and when; any single number still goes through game-balance's evidence procedure. Chooses KPIs before a season starts with a written stop rule, sets a hotfix-vs-patch rhythm with a severity threshold, and keeps comms honest: known issues named early, a roadmap nobody has to walk back. Use whenever someone is planning a season, a live-service calendar, a public roadmap, or player-facing patch notes, or asks \"do we hotfix this or wait for the next patch\", \"what ships this season\", \"what KPI proves this event worked\". Not for one number's evidence (game-balance), a versioned changelog (release-notes), building the game (game-builder), or a platform submission (game-certification)."
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Game Live Ops

A live game runs on a season calendar written before the season starts, against KPIs and a stop rule chosen in advance, with a patch rhythm that distinguishes a scheduled release from a hotfix-worthy one by a threshold rather than by whoever is shouting loudest that day.

Live ops is where planning discipline is hardest to keep, precisely because everything feels urgent and nothing feels planned: a metric dips and the reflex is to react that afternoon, a forum thread gets loud and the reflex is to patch the thing it is angry about, a season runs long because nobody wrote down when it should end. None of that is a technical failure — it is a planning failure wearing the costume of responsiveness. This skill exists to put the calendar first: decide the cadence, the KPIs, the stop rule and the hotfix threshold while nobody is under pressure from this week's numbers, so the team spends live weeks executing a plan rather than improvising one. It decides the calendar and the guardrails; it explicitly does not decide any single balance number, which stays `game-balance`'s job with its evidence procedure intact.

## Scope

Use for: planning a content and season cadence as a calendar; planning events with a stated purpose and a planned read; scheduling economy tuning windows and the guardrails each stays inside; choosing KPIs before a season starts, including a written stop rule; setting the rhythm and severity threshold between a scheduled patch and a hotfix; and the discipline behind player-facing communication — patch notes, known issues, and roadmap honesty.

Do not use for: the evidence procedure and playtest behind changing one specific number — that is `game-balance`, and this skill hands it every change once the calendar says it is due. Building the game or a new feature is `game-builder` and `game-design-doc`. A platform's review of a specific patch submission is `game-certification`, though this skill's calendar has to leave room for its lead time. A frame-rate or netcode regression a patch introduced is `game-performance` or `game-netcode`. Turning a range of merged changes into the mechanical changelog — version bump, migration notes, the pre-publish checklist — is `release-notes`; rolling a patch out gradually behind flags or rings is `release-strategy`; this skill decides what a season ships and when, not how a build is versioned or staged technically. Outward communication during an active incident, and the blameless write-up afterward, are `incident-comms` and `postmortem` in the manager plugin — a known-issues note in a patch is routine live ops, a real outage is not. Deciding whether to build the game at all is `game-greenlight`, which this skill assumes already happened.

## Scale and game type

Scale here means what the work requires rather than a headcount or a budget: indie/A is one small team wearing every hat; AA adds specialised roles, several platforms and a publisher's milestones; AAA adds many specialised disciplines, external studios and a simultaneous multi-platform launch.

| | Indie/A | AA | AAA |
| --- | --- | --- | --- |
| Calendar ownership (step 2) | Whoever is left after launch, often informally | A live-ops or production role owns it against a publisher's post-launch commitment | A dedicated live-ops team owns it, coordinated with marketing and regional teams |
| KPI rigour (step 5) | A couple of numbers tracked by hand, chosen honestly rather than dropped entirely | Dashboarded numbers reviewed on a schedule | A KPI review cadence with its own meeting, feeding decisions this skill's calendar has to leave room for |
| Comms staffing (step 7) | The same person who builds the game writes the patch notes | A community manager owns the channel, briefed from this skill's calendar | Community, PR and regional teams coordinate from one roadmap, in more than one language |

This skill matters most for live-service, free-to-play and competitive multiplayer games, where the post-launch plan is close to the whole product. It matters little for a finished single-player game with no planned updates — step 1 exists to say so and stop early rather than run the full discipline against a game that does not need it.

## Workflow

### 1. Decide whether this applies, and stop early if it does not

A finished single-player game with no planned content beyond a day-one patch does not need a season calendar, KPIs or a stop rule — running the full discipline against it produces process with nothing to plan. Confirm there is an actual live season, an actual cadence of updates, or an actual live economy before continuing; if there is only ever going to be one more patch, hand that patch to `game-certification` for its submission and stop here.

### 2. Build the content and season calendar

Fix the season length, the content-drop cadence inside it, and a lead-time buffer for each content type — including whatever a platform's certification turnaround from `game-certification` demands before a drop can ship. Write what "done" commits to for each planned drop before the season starts, so mid-season slippage is visible against a plan rather than absorbed silently.

Read `references/season-calendar.md` for cadence patterns by game type, how to size the lead-time buffer, and a worked calendar.

### 3. Plan events on the calendar

Each event gets a start, an end, a stated purpose, and a planned read of whether it worked — decided before it runs, not assembled from whichever numbers look good afterward. An event with no stated purpose is decoration; one with a purpose but no planned read cannot be judged, only remembered fondly or not.

An event or season opening concentrates players into a spike, so size the servers for it before the date is public; that estimate is `capacity-planning`'s procedure, not this skill's.

### 4. Plan economy tuning as a schedule with guardrails

Decide which number families are open to change this season and on what cadence, and the guardrail band each has to stay inside — this is a scheduling and boundary decision, not a tuning one. The moment a specific number is due to change, hand it to `game-balance`'s full evidence procedure: name the target, instrument it, read the sample, check for dominance, size the change, give it a window. This skill puts the change on the calendar; `game-balance` earns the right to ship it.

A guardrail crossed outside the planned window — an economy metric moving faster than the schedule expected — is the trigger to pull a `game-balance` pass forward, not to ship an unplanned number change to stop the bleeding.

### 5. Choose KPIs before the season starts, with a stop rule

Pick the season's KPIs — retention, engagement, monetisation where the game has one — before the season opens, and measure your own baseline before setting a target: nothing here supplies an industry figure, because a number borrowed from another game's audience, platform and genre measures nothing about this one. Read `references/kpi-and-stop-rules.md` for the candidate KPI table and how to build a baseline from the game's own data.

Write the stop rule in the same sitting: the specific, observable threshold that ends or reverses the season, decided while nobody yet knows what the season's numbers will look like. A stop rule written after a metric has already moved is not a stop rule, it is a justification for whatever the team was already inclined to do.

### 6. Set the patch and hotfix rhythm

Write the severity threshold that separates a hotfix from something that waits for the next scheduled patch — a specific class of bug, exploit or outage that justifies breaking the calendar, stated before an actual candidate is sitting in front of the team demanding a decision under pressure. Without a written threshold, either everything becomes a hotfix and the scheduled cadence stops meaning anything, or nothing does and a genuine emergency waits for a slot it should never have waited for.

A hotfix still owes `game-certification` its own submission on a platform that requires review, and still owes `game-balance` its evidence if it touches a tuned number — the rhythm decides when a fix ships, not whether the normal gates apply to it. Read `references/patch-rhythm-and-comms.md` for the severity table and how to size the threshold to the game's actual player impact.

### 7. Plan community communication

Patch notes state what changed in terms a player experiences, not in terms of the internal ticket that produced it. Known issues are named before players find and report them, wherever that is possible — a known-issues note that ships alongside a patch protects trust that a silent bug does not. Roadmap honesty means never committing a date or a feature the team cannot currently defend; a vague roadmap costs less trust than a specific one that slips.

`references/patch-rhythm-and-comms.md` has the patch-note shape, the known-issues discipline, and the roadmap-honesty anti-patterns in full.

### 8. Hand off

Every single number change goes to `game-balance` with its evidence, on the schedule this skill set. A regression a patch introduced — a frame-time or netcode issue — goes to `game-performance` or `game-netcode`. Every platform submission the season's calendar requires goes to `game-certification`, on the lead time step 2 already accounted for. The mechanical changelog and pre-publish checklist for a given patch is `release-notes`; a staged or flagged technical rollout of the patch itself is `release-strategy`. An actual incident, rather than a routine known issue, is `incident-comms` during and `postmortem` afterward, both in the manager plugin.

## Anti-patterns

**Reactive live ops.** No calendar, and every change is a response to whatever metric dipped or whichever forum thread got loud this week. The team spends the season firefighting rather than executing a plan, and nothing this season teaches carries into the next one.

**The KPI chosen after the season.** Picking the metric that happened to look good and calling it the target is not measurement, it is narrative built backward from a result.

**No stop rule.** The season keeps running past the point it should have ended or reversed, because nobody agreed in advance what ending it would look like, and agreeing in the moment means agreeing under whatever pressure is loudest that week.

**An economy grab-bag with no evidence behind any one number.** Several numbers move in the same patch with no individual prediction or window, and the next reading cannot tell which change did what — the same failure `game-balance`'s own procedure exists to prevent, arrived at here by skipping the hand-off entirely.

**No severity threshold for a hotfix.** Either everything qualifies, and the scheduled cadence stops meaning anything, or nothing does, and a genuine emergency waits for a slot that was never meant to hold it.

**A roadmap promise nobody can currently defend.** A specific date or feature stated to sound reassuring costs more trust when it slips than an honestly vague one ever would have.

**Running full live-ops discipline against a game that does not need it.** A finished single-player title with no planned updates gets a season calendar, KPIs and a stop rule it will never use, which is process spent on a game that already stopped needing it.

## References

- `references/season-calendar.md` — read at step 2: cadence patterns by game type, sizing the lead-time buffer against a platform's certification turnaround, and a worked season calendar.
- `references/kpi-and-stop-rules.md` — read at step 5: the candidate KPI table by category, how to build a baseline from the game's own data rather than an outside figure, and how to write a stop rule that actually binds.
- `references/patch-rhythm-and-comms.md` — read at steps 6 and 7: the severity table that separates a hotfix from a scheduled patch, the patch-note shape, the known-issues discipline, and the roadmap-honesty anti-patterns.
