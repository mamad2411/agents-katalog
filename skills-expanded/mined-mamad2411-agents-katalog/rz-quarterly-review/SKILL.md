---
name: rz-quarterly-review
description: >
  Use when invoked via /rz-quarterly-review, when Riché asks to "run the quarterly review", "set Q[N] priorities", "do quarterly planning", "review the quarter", "review my strategies", "check strategy alignment", "are my strategies still aligned", or on the first Sunday of January, April, July, or October. The structured 80-100 minute end-of-quarter process: pull metrics, re-score every active channel against the 5-criteria framework, gate-check deferred candidates (newsletter, YouTube, podcast hosting, etc.), review the 5 strategy documents (Product, Growth, Content, Channel, Audience Development) on 4 axes (effectiveness / alignment / drift / cross-doc misalignment), pick 1-3 priorities for the next quarter using the priorities template, write the full review to the Quarterly Reviews Notion DB, and seed Linear tasks for the first concrete action of each priority. Tactical companion to the role-based `rz-growth-marketing`; reads strategic frames from `corpus/growth/` and produces a quarter-specific bet.
---

# Quarterly Review — Riché Zamor

The end-of-quarter strategic review for the personal brand. Runs the 60-min process from `corpus/growth/playbook/quarterly-channel-review.md`, plus 30 min of Notion writing and Linear seeding. Produces one Notion page in the Quarterly Reviews DB, 1-3 named priorities, and 1-3 Linear seed tasks.

This is a tactical skill (sibling to `rz-website-audit`). It executes a process; it does not own the strategic frames. The strategic frames live in `corpus/growth/` and are owned by `rz-growth-marketing`.

## Before beginning work

The corpus has migrated to Notion. Notion is the source of truth — the local `corpus/*` paths cited below are historical and may drift. Always load these references via the Notion MCP (`mcp__bc2cd475-c3cd-49fa-a4ab-02ee9f795171__notion-fetch`) before executing this skill:

1. **Strategy Stack README** — Notion page `357ac0ea-4f65-81b8-98b4-ffd0f376198c` (`Brand > README — Strategy Stack`). **Critical for this skill** — the quarterly review reviews the strategy stack itself: doc ownership, canonical constants, and the Decision-of-Record log. Use it as the index of strategy documents to evaluate. Flag any drift you spot during the 4-axis review.
2. **Your section of the Corpus** at `Projects > RZ Claude Skills > Corpus`:
   - `growth` → page `357ac0ea-4f65-812a-a480-d3b7ab463bc2` (strategic frames, playbook process docs, channel-ROI methodology, database schemas)

Each Corpus directory page lists its child entries. Fetch only the specific entries you need.

## Cross-skill dependencies (read these first)

The review reads from canonical sources owned by other skills.

**Strategic frames are owned by `rz-growth-marketing`.** Pull from `corpus/growth/strategy/` for the channel evaluation framework, channel maturity model, owned-vs-rented allocation rule, audience portability, repurposing matrix, and creator-as-product dynamics. From `corpus/growth/creator-dynamics/` for voice, narrative, and quality-frequency frames. From `corpus/growth/diagnostics/` for engagement-drop and algorithm-change interpretation. The review applies these; it does not redefine them.

**Process and templates are owned by `rz-growth-marketing`.** Pull from `corpus/growth/playbook/quarterly-channel-review.md` for the 60-min Block 1-6 structure, from `corpus/growth/playbook/quarterly-priorities-template.md` for the priority format, from `corpus/growth/playbook/channel-gates-for-adding.md` for deferred-candidate gates, and from `corpus/growth/playbook/cutting-criteria.md` for retirement decisions.

**Channel-ROI methodology is owned by `rz-growth-marketing`.** Pull from `corpus/growth/metrics/channel-roi-calculation.md` for the formula and weights.

**Database schemas:** `corpus/growth/databases/quarterly-reviews-schema.md` defines the output DB structure.

**Recent website audit data** comes from `rz-website-audit`'s most recent Sunday run. The Quarterly Review reads the most recent Weekly Audits DS page (and the prior 12 weekly pages for trend) to inform channel-level signals on richezamor.com performance.

**LinkedIn analysis is owned by `rz-linkedin-audit`** (monthly tactical sibling skill). Each month, `rz-linkedin-audit` parses the LinkedIn data archive + Content Analytics exports, runs 6 pillars, and writes a structured page to the Monthly LinkedIn Audits Notion DB. The quarterly review reads the **prior 3 monthly audit pages** for trend context — same pattern as Step 2a reads the prior 13 weekly website audit pages. Raw LinkedIn data parsing has moved out of this skill into `rz-linkedin-audit`.

If a strategic frame's text is being applied differently than the canonical corpus says, the canonical corpus wins. Surface drift in `rz-self-improve`.

## Constants

```
RUN_TIMEZONE                   = America/New_York
QUARTERLY_REVIEW_MONTHS        = January, April, July, October (first Sunday)
LINEAR_TEAM_ID                 = 72132418-b477-4450-a30a-77391d5cfc47   (Riche Zamor team)
LINEAR_PROJECT_ID              = 085484ef-b523-4142-bce2-7f9a23a05fa1   (Brand project)
LINEAR_ASSIGNEE_ID             = 646e8aef-65f5-47de-ba40-4f2ad99bbc15   (Riché)
NOTION_BRAND_PARENT_ID         = 333ac0ea4f658086bcafcd3f53299b89       (Brand)
NOTION_GROWTH_STRATEGY_PAGE_ID = 356ac0ea4f6580828e68f93292e3ea9d       (Brand → Growth Strategy — also holds Quarterly Reviews DB)
NOTION_QUARTERLY_REVIEW_DB_ID  = f51277cdd4d94f8e83c81cd1c08f82e8       (Quarterly Reviews DB)
NOTION_QUARTERLY_REVIEW_DS_ID  = 1dadc999-7c9b-42de-98b4-75594c10a4b5   (Quarterly Reviews data source)
NOTION_AUDIT_DS_ID             = 889093b4-fb7d-4db5-a871-19e7bbe159fd   (Weekly Audits — read for trend context)
NOTION_LINKEDIN_AUDIT_DB_ID    = 9ccff092811d479891a684c402e6da91       (Monthly LinkedIn Audits DB — Step 2e reads)
NOTION_LINKEDIN_AUDIT_DS_ID    = d5206b14-756d-422d-b54b-74d57560e321   (Monthly LinkedIn Audits data source)
NOTION_PRODUCT_STRATEGY_ID     = 333ac0ea4f658165b821ceecca624346       (Strategy doc 1/5)
NOTION_GROWTH_STRATEGY_DOC_ID  = 356ac0ea4f6580828e68f93292e3ea9d       (Strategy doc 2/5 — same as GROWTH_STRATEGY_PAGE_ID)
NOTION_CONTENT_STRATEGY_ID     = 333ac0ea4f6581518651d730d706e017       (Strategy doc 3/5)
NOTION_CHANNEL_STRATEGY_ID     = 331ac0ea4f6581feaf8fe37afebaeaf5       (Strategy doc 4/5 — "Content Channel Strategy")
NOTION_AUDIENCE_DEV_ID         = 33aac0ea4f65814f8b22f45410901cf6       (Strategy doc 5/5 — Audience Development Strategy)
TARGET_KEYWORDS_DB_ID          = f5521fe72dec42c1808555fbac2d0d62
COMPETITORS_DB_ID              = c99eaa6d2e7448f0859ce6feba22a3ac
CONTENT_STRATEGY_PAGE_ID       = 333ac0ea4f6581518651d730d706e017
SLACK_CHANNEL                  = #brand
MAX_PRIORITIES                 = 3
TIME_BUDGET_CEILING            = 5.25 hrs/week
OWNED_CHANNEL_FLOOR            = 30%
```

## Load from corpus

Read these in order before running. The corpus carries the strategic frames; this file is the orchestrator.

**Process and priority templates (always)**
- `corpus/growth/playbook/quarterly-channel-review.md` — the 60-min Block 1-6 structure
- `corpus/growth/playbook/quarterly-priorities-template.md` — the 1-3 priority format
- `corpus/growth/playbook/channel-gates-for-adding.md` — deferred-candidate gate evaluation
- `corpus/growth/playbook/cutting-criteria.md` — retirement decision rules
- `corpus/growth/playbook/budget-allocation.md` — the 5.25 hr ceiling
- `corpus/growth/playbook/linkedin-monthly-dump-workflow.md` — the LinkedIn data archive convention used by Step 2e
- `corpus/growth/playbook/strategy-review-protocol.md` — the 4-axis strategy review used by Step 5

**Strategic frames (always)**
- `corpus/growth/strategy/channel-evaluation-framework.md` — the 5-criteria scoring
- `corpus/growth/strategy/channel-maturity-model.md` — Experiment→Cut lifecycle stages
- `corpus/growth/strategy/owned-vs-rented-channels.md` — the 30% owned-channel floor
- `corpus/growth/strategy/audience-portability.md` — email list as the portable asset
- `corpus/growth/strategy/repurposing-matrix.md` — derivative production economics
- `corpus/growth/strategy/creator-as-product.md` — the dynamics that filter every decision

**Creator dynamics (always)**
- `corpus/growth/creator-dynamics/authentic-voice-as-moat.md`
- `corpus/growth/creator-dynamics/founder-narrative-as-product.md`
- `corpus/growth/creator-dynamics/frequency-vs-quality-tradeoff.md`
- `corpus/growth/creator-dynamics/vulnerability-vs-authority-balance.md`

**Diagnostic patterns (always)**
- `corpus/growth/diagnostics/engagement-drop-diagnostic.md` — interpret in-quarter drops
- `corpus/growth/diagnostics/algorithm-change-response.md` — interpret platform shifts
- `corpus/growth/diagnostics/deplatforming-prep.md` — verify Plan B status

**Metrics (always)**
- `corpus/growth/metrics/channel-roi-calculation.md` — the per-channel ROI formula
- `corpus/growth/metrics/content-decay-analysis.md` — half-lives that inform allocation
- `corpus/growth/metrics/repurpose-vs-create-decision.md` — content-mix decisions
- `corpus/growth/metrics/segment-proxies-rollup.md` — the segment outcome metrics
- `corpus/growth/metrics/anti-vanity-metrics.md` — what to exclude from headline metrics

**Channel-specific evaluations (load on demand per gated channel)**
- `corpus/growth/channels/newsletter-evaluation.md`
- `corpus/growth/channels/youtube-evaluation.md`
- `corpus/growth/channels/own-podcast-evaluation.md`
- `corpus/growth/channels/github-as-distribution.md`
- `corpus/growth/channels/reddit-niche-engagement.md`
- `corpus/growth/channels/hackernews-launch-mechanics.md`

**Anti-patterns (always — defends every decision)**
- `corpus/growth/anti-patterns/no-channel-sprawl.md`
- `corpus/growth/anti-patterns/no-time-budget-overrun.md`

**Database schema**
- `corpus/growth/databases/quarterly-reviews-schema.md` — the output DB structure

## Process

### Step 1 — Bootstrap (10 min)
Per `quarterly-channel-review.md` Block 1, plus skill-specific setup:
1. Verify required MCP connectors are reachable (Notion, Linear, Slack, HubSpot — Ahrefs/GSC optional but preferred).
2. Pull the prior quarterly review page from `NOTION_QUARTERLY_REVIEW_DS_ID` (if it exists) for diff baseline. If first run, baseline is "no prior review."
3. Pull the most recent Weekly Audit page from `NOTION_AUDIT_DS_ID` plus the prior 12 weeks (one quarter). Extract per-week traffic light, P0/P1 counts, and recurring dimension reds.
4. Pull current Target Keywords DB and Competitors DB state (high level — not full audit).
5. Initialize empty data buffer for review output.

### Step 2 — Pull data (15-20 min)
Concurrent reads across 8 substeps. Each names the MCP tool and the specific query. The data window is the prior 90 days unless otherwise noted.

**Important scope notes:**
- **X is intentionally not pulled.** X is a secondary channel; engagement metrics there are not load-bearing for current quarterly decisions. X cadence is still tracked indirectly via Calendar (see 2h). Revisit when X is repromoted from secondary to primary.
- **LinkedIn engagement *received* (likes/comments/impressions on Riché's posts) is not in the LinkedIn data export.** The skill measures **outbound** activity (cadence, commenting, target-account engagement, connection growth) as the leading indicators per `corpus/growth/metrics/leading-vs-lagging.md`. If engagement-received metrics are needed for a specific priority, Riché must capture them manually as a one-off snapshot.

**2a. Prior 13 Weekly Audit pages (trend context)**
- MCP: `notion-fetch` against `NOTION_AUDIT_DS_ID` (`889093b4-fb7d-4db5-a871-19e7bbe159fd`)
- Query: filter by Date in last 90 days
- Extract: per-week Traffic Light, P0/P1 counts, Overall Dimension Lights
- Output: list of weeks with declining/stable/improving signals per dimension; recurring dimension-reds across the quarter

**2b. Notion DBs (state at end-of-quarter)**
- Target Keywords DB (`f5521fe72dec42c1808555fbac2d0d62`): status distribution; new Won/Deprioritized rows this quarter; position improvements vs Q-start
- Competitors DB (`c99eaa6d2e7448f0859ce6feba22a3ac`): tier distribution; Last Audited freshness
- Content Topics DB (`2c224f29490d44f99e7b58cb2e377086`): articles published this quarter, by domain (Context Layer / PM / Leadership) and topic cluster
- MCP: `notion-fetch` per data source; `notion-search` for cross-DB lookups
- Output: counts + named items per DB

**2c. richezamor.com performance (via Ahrefs)**
- GSC keywords + performance: `mcp__bff08770-..._gsc-keywords`, `_gsc-performance-history`, `_gsc-pages-history` for `richezamor.com`, last 90 days
- Web traffic: `mcp__bff08770-..._web-analytics-stats`, `_web-analytics-source-channels`, `_web-analytics-top-pages`, last 90 days
- Output: keyword count by GSC status, position trends, total clicks/impressions; visits, source breakdown, top-pages by traffic; week-over-week and month-over-month deltas

**2d. AIO citation trends (via Ahrefs Brand Radar)**
- MCP: `mcp__bff08770-..._brand-radar-mentions-history`, `_brand-radar-cited-pages`, `_brand-radar-sov-history`, last 90 days
- Output: citation count trend across the 20-query AIO set; citation rank changes per query; share-of-voice trend

**2e. LinkedIn analysis (via Monthly LinkedIn Audits Notion DB)**

LinkedIn analysis is owned by the monthly `rz-linkedin-audit` tactical skill, which produces structured audit pages in the Monthly LinkedIn Audits Notion DB. The quarterly review reads the **prior 3 monthly audit pages** for trend context — analogous to how Step 2a reads the prior 13 weekly website audit pages.

**MCP query:**
- `notion-fetch` against `NOTION_LINKEDIN_AUDIT_DS_ID` (`d5206b14-756d-422d-b54b-74d57560e321`)
- Filter: `Audit Date` in last 100 days (captures 3 monthly pages with safety margin)
- Sort by `Audit Date` descending

**From each of the 3 monthly audit pages, extract:**
- `Overall Status` (Green / Yellow / Red) — trend over 3 months
- `Posts Published`, `Total Impressions`, `Avg Impressions Per Post`, `Net Follower Growth`, `Total Followers EOP` — period-over-period comparison
- `Engagement Rate` — month-over-month trend (this is the gate-2 signal)
- `ICP Match Pct` — audience composition trend
- `Top Format`, `Top Domain`, `Domain Mix Drift` — content mix trend
- 4 Newsletter Gate checkboxes — trajectory toward newsletter launch
- `Linear Tasks Issued` — what was prioritized, did it ship?
- `Deep Dive Candidates` — what was investigated last month and what came of it

**For each page body, read:**
- Headline narrative (1-line verdict)
- Pillar findings (P1-P6) — flag any pillar that fired the same severity in 2+ consecutive months
- Late Bloomers (cross-quarter compounders worth republishing)
- Format Decay Curves observation (which formats earned their production cost)

**Compute quarterly LinkedIn rollup:**
- Total impressions over the quarter (sum of 3 months)
- Average engagement rate over the quarter
- Net follower growth over the quarter
- Number of months at each Overall Status (e.g., "1 Green, 2 Yellow, 0 Red")
- Recurring pillar patterns (e.g., "P3 fired P1 every month — Context Intelligence underperforming all quarter")
- Newsletter gate trajectory (which gates are approaching met-status?)

**Output (LinkedIn portion of the per-channel summary table):**
- Quarterly rollup of the 5 numeric metrics above
- Top 3 pillar findings of the quarter (most severe, most recurring)
- Newsletter gate trajectory with months-to-met estimate
- Strategic LinkedIn implication for next quarter (e.g., "shift production toward Frameworks; Deep Dives outperforming")

**Gap-handling:**
- If fewer than 3 monthly audit pages exist (skill is new, or runs were skipped): use what's available; note in narrative ("Q1 review uses 1 monthly audit; trend analysis limited").
- If the most-recent monthly audit is older than 5 weeks: note staleness; flag whether `rz-linkedin-audit` was skipped or failed.
- If a monthly audit is missing critical properties (e.g., `Overall Status` null): degrade gracefully, surface as a P2 anomaly.

**This is a major simplification vs. the prior version of Step 2e.** The quarterly review no longer parses raw LinkedIn data; it consumes the structured monthly audit output. Rationale: trend recognition is much easier reading 3 structured pages than re-parsing 90 days of raw exports. Symmetric with how Step 2a consumes weekly website audits.

**2f. HubSpot (Segment 1 / Segment 4 inbound)**
- MCP: `mcp__f20a4db5-..._search_crm_objects`
- Query: contacts created last 90 days, filtered by lifecycle stage and segment tag
  - Segment 1: title contains "VP Product" / "Chief Product" / "Head of Product" / "VP AI" at AI-PM target companies
  - Segment 4: tag includes "event-organizer" or "podcast-host"
- Also: `_get_campaign_analytics` for any campaigns active during the quarter
- Output: counts + named individuals per segment; any direct outreach that landed

**2g. Linear (priority execution status)**
- MCP: `mcp__5f47df39-..._list_issues`
- Query: project = `LINEAR_PROJECT_ID` (`085484ef-b523-4142-bce2-7f9a23a05fa1`), updated in last 90 days
- Extract: tasks completed; tasks in flight; tasks linked to prior-quarter priorities (the TRZ-### IDs from the prior Quarterly Review page)
- Output: prior-quarter priority status — for each prior priority's seed task, mark as done / in-flight / dropped / replaced

**2h. Time investment proxy (Google Calendar)**
- MCP: `mcp__c70f51ca-..._list_events` for primary calendar
- Query: `timeMin` 90 days ago, `timeMax` today
- Extract: events whose title or description contains channel keywords. Bucket per channel:
  - **LinkedIn writing/batch:** "Sunday batch", "LinkedIn", "writing block"
  - **Strategic commenting:** "comment block", "LinkedIn comments"
  - **X cross-post:** "X cross-post", "Twitter"
  - **Speaking/podcasts:** "talk prep", "podcast", "speaking"
  - **richezamor.com articles:** "/thinking article", "article writing"
  - **Networking DMs:** "DM block", "outreach"
- Output: hours per channel, ±15% accuracy. Compare against the budget allocation in `corpus/growth/playbook/budget-allocation.md`. Flag channels significantly over or under their allocated time.

**Compute per-channel ROI** per `corpus/growth/metrics/channel-roi-calculation.md` using the data above:
- Numerator: weighted segment outcomes (Segment 1 contacts ×5, Segment 2 reshares ×3, Segment 4 invites ×4, Segment 3 inbound ×2, signups ×1, hire signals ×10)
- Denominator: hours invested (from 2h)
- Caveat: Segment 2 reshares cannot be directly measured from the LinkedIn dump (engagement received is not in the export). If the prior Quarterly Review page captured a manual snapshot, use it as the baseline; otherwise track Segment 2 reshares qualitatively from observed activity rather than as a hard number.

**Output:** a one-page per-channel summary table containing: hours invested, outcomes by segment, ROI per hour, cadence held Y/N, score change vs prior quarter (filled in Step 3).

### Step 3 — Score active channels (10 min)
Per `quarterly-channel-review.md` Block 2. Re-score every active channel via `corpus/growth/strategy/channel-evaluation-framework.md`. Compare to last quarter's scores (from prior review page if it exists).
- ↑↑ ≥2 points: strong; consider increasing investment
- → ±1 point: stable; maintain
- ↓↓ ≥2 points: investigate; possible stage transition or cut

### Step 4 — Stage check + gate check (15 min)
Per `quarterly-channel-review.md` Blocks 3 + 4 combined:
- Active channels: confirm/transition stage per `corpus/growth/strategy/channel-maturity-model.md`. Document any transitions with date and rationale.
- Deferred candidates: gate-check per `corpus/growth/playbook/channel-gates-for-adding.md`. Note progress per gated channel; identify any that are now launchable.
- Cut evaluation: any active channel meeting `corpus/growth/playbook/cutting-criteria.md`'s 3-criteria rule? If yes, mark as cut candidate for Block 5.

### Step 5 — Strategy review (15-20 min)
Per `corpus/growth/playbook/strategy-review-protocol.md`. Review the 5 strategy documents in Notion against the data + scoring + stage decisions from Steps 2-4.

**Read each of the 5 strategy docs via Notion MCP `notion-fetch`:**
- Product Strategy: `NOTION_PRODUCT_STRATEGY_ID` (`333ac0ea4f658165b821ceecca624346`)
- Growth Strategy: `NOTION_GROWTH_STRATEGY_DOC_ID` (`356ac0ea4f6580828e68f93292e3ea9d`)
- Content Strategy: `NOTION_CONTENT_STRATEGY_ID` (`333ac0ea4f6581518651d730d706e017`)
- Channel Strategy: `NOTION_CHANNEL_STRATEGY_ID` (`331ac0ea4f6581feaf8fe37afebaeaf5`)
- Audience Development: `NOTION_AUDIENCE_DEV_ID` (`33aac0ea4f65814f8b22f45410901cf6`)

For each doc, capture: stated targets, current focus, named segments/channels/priorities, last modified date.

**Score each doc on 4 axes** (per `strategy-review-protocol.md`; budget 4 min/doc × 5 = 20 min cap):
- **Effectiveness** vs Step 2 outcome data (channel ROI, segment proxies, audience composition)
- **Alignment** vs prior-quarter priorities + current channel set
- **Drift** vs last-modified date + decisions taken in the prior quarter
- **Cross-doc misalignment** vs the other 4 docs (look for contradicting segment definitions, conflicting channel decisions, voice-tone mismatches, target-account contradictions)

Each axis scored 🟢 / 🟡 / 🔴 with explicit evidence cited.

**Aggregate to Strategy Drift headline** per the rules in `strategy-review-protocol.md`:
- 🟢 Aligned: every doc 🟢 OR exactly one 🟡 across the matrix
- 🟡 Minor drift: 2-3 🟡s, zero 🔴s
- 🔴 Major misalignment: any 🔴 OR ≥4 🟡s

**Surface strategy-update decisions:**
- 🔴 findings → strategy-update task becomes a candidate quarterly priority for Step 6 (counts against MAX_PRIORITIES = 3)
- 🟡 findings → strategy-update task becomes a P2 backlog item (does NOT count against priority cap; surfaces in the Strategy Review section but does not seed a Linear task)
- 🟢 findings → no action

**Output:** a "Strategy Review" section for the Quarterly Review page body, structured per `strategy-review-protocol.md`. Includes per-doc 4-axis scores with evidence, the aggregate Strategy Drift headline, and the list of recommended strategy updates with classification (priority vs P2).

The Strategy Drift headline gets stored as the `Strategy Drift` property in the Quarterly Reviews DB (separate from the overall `Headline` property — strategy alignment is its own dimension, queryable across quarters).

### Step 6 — Decisions + priority setting (15 min)
Per `quarterly-channel-review.md` Block 5, extended with explicit priority setting:
- **Active channel decisions:** GROW / MAINTAIN / REDUCE / CUT per channel
- **Candidate decisions:** LAUNCH next quarter (with funded cut per `no-channel-sprawl.md`) or DEFER
- **Time allocation lock:** total ≤5.25 hr/week; per-channel breakdown; ~15 min/week buffer
- **Pick 1-3 priorities for next quarter** using `corpus/growth/playbook/quarterly-priorities-template.md`. Strategy-update priorities from Step 5 (🔴 findings) are eligible for inclusion. Each priority must specify: imperative phrase, why-this-quarter, concrete target, strategic frame served, channels involved, time delta, reversal condition, quarterly review check.
- **Compute Headline traffic light** per the rules in `corpus/growth/databases/quarterly-reviews-schema.md`.

### Step 7 — Assemble review (10 min)
Build the full quarterly review page in memory before any Notion write. Sections per `corpus/growth/databases/quarterly-reviews-schema.md`:
1. Executive summary (1 paragraph)
2. Data pull summary (per-channel ROI table)
3. Active channel scoring (with deltas)
4. Stage transitions
5. Deferred candidate gate progress
6. **Strategy review** (per Step 5 output: per-doc 4-axis scores + Strategy Drift headline + recommended updates)
7. Decisions
8. Quarterly priorities (1-3 detailed)
9. Time allocation lock
10. Linear tasks (filled in next step)

Do not write to Notion yet.

### Step 8 — Issue Linear seed tasks (10 min)
For each priority (max 3 tasks total): create a Linear issue in `LINEAR_PROJECT_ID`, assigned to `LINEAR_ASSIGNEE_ID`, with the first concrete action that advances the priority. Examples:
- Newsletter-launch priority → Linear task: "Set up Beehiiv account and import holding list" with due date in week 1 of the quarter
- GitHub-experiment priority → Linear task: "Publish first companion repo for the most-recent /thinking article" with due date in week 1
- Cadence-rebuild priority → Linear task: "Re-establish Sunday batch session and pre-write 2 weeks ahead" with due date this Sunday
- Strategy-update priority (from Step 5 🔴) → Linear task: "Reconcile Audience Development with Content Strategy on primary segment" with the specific edits to make

Use the create-then-update pattern (create with title only, then update with full body) — direct create-with-full-payload is unreliable. Capture the TRZ-### IDs.

### Step 9 — Write Notion page (5 min)
Single create to `NOTION_QUARTERLY_REVIEW_DS_ID`. Page name `Q{N} {YYYY} Review`. Properties per `corpus/growth/databases/quarterly-reviews-schema.md` (including the `Strategy Drift` property from Step 5). Body = the assembly from Step 7 with Linear TRZ-### IDs filled in. Set Headline last, after task issuance is confirmed.

### Step 10 — Slack notification (2 min)
One-line post to `SLACK_CHANNEL` (`#brand`):
```
{traffic-light emoji} Q{N} {YYYY} Review complete — {N} priorities set ({TRZ-### IDs}). Strategy: {strategy drift emoji}. {Notion page link}
```
Same brevity discipline as the weekly audit Slack: index card + link, never the full body. Includes the Strategy Drift headline so the Slack reader sees both signals.

### Step 11 — Update growth-marketing reference (1 min)
The growth-marketing skill should know what the current quarter's priorities are. Append a one-line note to a designated location (option A: a Notion sub-page; option B: a `current-priorities.md` file outside corpus that gets refreshed each quarter; option C: simply the most recent Quarterly Review page). The skill defaults to option C; the priorities are always queryable as the most-recent row in the DB.

## Output summary
Every successful run produces:
- One page in the Quarterly Reviews Notion DB (with Headline traffic light, Strategy Drift headline, all properties populated, body sections complete)
- 1-3 priorities written into the page body, structured per the priorities template
- A Strategy Review section covering all 5 strategy docs on 4 axes
- 1-3 Linear seed tasks (TRZ-### IDs) — one per priority — with due dates in the first week of the new quarter
- One `#brand` Slack post (one line + both headlines + Notion link)

## What this skill does NOT do

- It does not own strategic frames. The strategy lives in `corpus/growth/strategy/` and `corpus/growth/creator-dynamics/`. This skill applies them; it does not redefine them.
- It does not modify channels mid-quarter. Decisions made here are next-quarter; in-quarter changes happen via diagnostics or weekly cadence work.
- It does not substitute for the weekly website audit. The weekly audit covers richezamor.com health; this quarterly review covers the broader portfolio across all channels.
- It does not edit the 5 strategy docs in Notion. The Strategy Review (Step 5) surfaces drift and misalignment as findings; Riché updates the docs himself (or the strategy-update task seeded for the next quarter handles it).
- It does not auto-execute priorities. It seeds the first task for each priority; the work itself happens via cadence + targeted skill invocations across the quarter.
- It does not retro-edit prior review pages. Each review lives in its own dated page; the time series is append-only.
- It does not adjust the 5.25 hr/week budget upward to accommodate more priorities. The budget is the binding constraint; if the priorities don't fit, they get cut to ≤3 that do fit.
- It does not add a "stretch goal" 4th priority. MAX_PRIORITIES is 3 by design; 4+ dilutes focus.

## Cross-skill connections

**Upstream (the review reads from these for canonical knowledge):**
- `rz-growth-marketing` — owns all strategic frames, the priority template, the channel evaluation framework, the channel maturity model, the channel-ROI methodology, the cutting criteria, the gate criteria, and the creator-as-product dynamics.
- `rz-website-audit` — provides per-Sunday richezamor.com data via the Weekly Audits DS. The quarterly review reads the prior 13 weekly audit pages for trend context.

**Downstream (the review hands off to these for execution):**
- `rz-website-audit` — quarterly priority adjustments may require updates to the audit's tracked dimensions or competitor list. The review's decisions inform what the audit watches.
- `rz-content-optimize` — when a priority involves shipping content (e.g., "ship 4 GitHub repos this quarter"), the per-article execution routes through content-optimize.
- `rz-draft-content` — content-shipping priorities feed draft-content for the writing itself.
- `rz-self-improve` — runs at end-of-quarter as the corpus-update trigger; if the review revealed a strategic frame that needs refinement, this skill flags it for self-improve.

## Common Mistakes

| Mistake | What goes wrong | Fix |
|---|---|---|
| Setting 4+ priorities | Priority dilution; nothing meaningful moves | MAX_PRIORITIES = 3 by design; pick the 3 that matter most |
| Setting 0 priorities (just doing the channel review) | Quarterly direction stays vague; the corpus alone is too neutral | Even a maintenance quarter has 1-2 priorities (e.g., "hold cadence through Q1 hiring season") |
| Allocating more than 5.25 hr/week to priorities + baseline | Budget breaks; cadence collapses by week 4 | If the priorities don't fit, cut them down or fund them with explicit retirement of an active channel |
| Picking priorities that aren't measurable | Quarterly review check at end-of-quarter has no way to mark done/extended | Every priority must have a single measurable concrete target |
| Writing this run's priorities INTO the corpus | Corpus is evergreen; priorities are dated | Priorities live in the Notion DB; the corpus has the template only |
| Skipping the prior-quarter review of priorities | The done/extended/dropped call is what makes the cycle work | Block 1 of every review starts with "what happened to last quarter's priorities" |
| Treating Yellow as a problem | Yellow is the most common state; honest assessment | Headline is multi-criteria; mixed quarters get Yellow honestly |
| Skipping the strategy review because "the docs probably haven't changed" | Misses silent drift and cross-doc misalignment that compounds over quarters | Step 5 is non-skippable; even a 5-min scan surfaces the obvious things |
| Updating one strategy doc based on findings without checking the other 4 | Fixes one drift, creates new cross-doc misalignment | Strategy updates are batched: one quarter's review proposes the change, next quarter's verifies cross-doc fit |
| Letting strategy-update tasks pile up as P2 backlog forever | The drift compounds; eventually a priority is forced | Two quarters of accumulated 🟡 strategy findings on the same doc → escalate to a priority |
