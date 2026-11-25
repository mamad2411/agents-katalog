---
name: rz-linkedin-audit
description: >
  Use when Riché invokes /rz-linkedin-audit, asks to "run the monthly
  LinkedIn audit", "audit my LinkedIn", "do my LinkedIn monthly review",
  "review LinkedIn post performance", or when a Cowork shortcut fires
  the first-Sunday-of-month trigger with body "Run the rz-linkedin-audit
  skill." Also invoke for: LinkedIn audit, monthly LinkedIn review,
  compounder/late-bloomer/format-decay analysis, ICP match analysis,
  newsletter gate progress check. Runs 6 pillars (Reach & Velocity,
  Audience Composition, Thesis Resonance, Conversion & North Star,
  Competitive Benchmarking, Voice & Brand Hygiene) against the latest
  30-day LinkedIn Creator Analytics export. Updates the Master Tracker
  Sheet, writes a page to the Monthly LinkedIn Audits Notion DB, issues
  up to 3 Linear tasks, posts a one-line headline to #brand, and surfaces
  Top 5 Deep Dive candidates for separate enrichment.
---

# LinkedIn Audit — Riché Zamor

Monthly audit of Riché's LinkedIn presence. Runs first Sunday of each month at 8:30pm America/New_York via Claude Cowork shortcut, or manually via `/rz-linkedin-audit` in Claude Code. Produces a structured Notion page, issues up to 3 prioritized Linear tasks, and posts a single-line headline to Slack.

LinkedIn is the primary surface for Riché's professional brand. Website is secondary. X is published-to but not audited (deferred). The audit feeds the newsletter launch decision and the engagement-rate diagnostic.

## Before beginning work

The corpus has migrated to Notion. Notion is the source of truth — the local `corpus/*` paths cited below are historical and may drift. Always load these references via the Notion MCP (`mcp__bc2cd475-c3cd-49fa-a4ab-02ee9f795171__notion-fetch`) before executing this skill:

1. **Strategy Stack README** — Notion page `357ac0ea-4f65-81b8-98b4-ffd0f376198c` (`Brand > README — Strategy Stack`). Doc ownership, canonical constants (LinkedIn primary channel framing, cadence, North Star), and the Decision-of-Record log. Honor it; flag drift.
2. **Your sections of the Corpus** at `Projects > RZ Claude Skills > Corpus`:
   - `linkedin-audit` → page `357ac0ea-4f65-815f-8c78-eec2b573cc4a` (canonical: methodology, 6 pillars, deep-dive criteria, views, databases)
   - `growth` → page `357ac0ea-4f65-812a-a480-d3b7ab463bc2` (ICP definition, flywheel, engagement-quality framework, monthly dump workflow)
   - `voice` → page `357ac0ea-4f65-8194-ae1e-e5147adad60c` (Fatal Fifteen, anti-tells, 50/30/20 domain balance — P6 hygiene checks reference this)

Each Corpus directory page lists its child entries. Fetch only the specific entries you need.

## Cross-skill dependencies (read these first)

The audit is a tactical skill. It does not own voice canon or audience strategy. It LEVERAGES sources owned by other role-based skills.

**Brand voice is owned by `rz-copywriting`.** Pull from `corpus/voice/` for the Fatal Fifteen AI-tells list, voice anti-patterns, and the 50/30/20 domain balance frame. The audit's P6 voice checks are detection rules ON TOP of the voice canon; they do NOT redefine voice rules.

**Audience strategy is owned by `rz-growth-marketing`.** Pull from `corpus/growth/` for the ICP definition (VP/CPO/founder-level operators at Series A-C AI companies), audience flywheel logic, and the engagement quality framework. P2 and P3 reference these as source of truth. The LinkedIn export workflow Riché runs monthly lives at `corpus/growth/playbook/linkedin-monthly-dump-workflow.md`.

If a corpus entry's text contradicts these source-of-truth corpora, the source-of-truth corpora win. Surface the contradiction in `rz-self-improve` for cleanup.

## Load from corpus

Read these in order before running. The corpus carries the actual audit logic; this file is the orchestrator.

**Methodology (always)**
- `corpus/linkedin-audit/methodology/bootstrap.md`
- `corpus/linkedin-audit/methodology/export-parsing.md`
- `corpus/linkedin-audit/methodology/master-tracker-update.md`
- `corpus/linkedin-audit/methodology/pillar-analysis.md`
- `corpus/linkedin-audit/methodology/deep-dive-candidate-selection.md`
- `corpus/linkedin-audit/methodology/report-assembly.md`
- `corpus/linkedin-audit/methodology/task-issuance.md`
- `corpus/linkedin-audit/methodology/slack-notification.md`

**Database schemas (always)**
- `corpus/linkedin-audit/databases/monthly-audits-notion-schema.md`
- `corpus/linkedin-audit/databases/master-tracker-sheet-schema.md`

**Six pillars (run in order)**
- `corpus/linkedin-audit/pillars/p1-reach-velocity.md`
- `corpus/linkedin-audit/pillars/p2-audience-composition.md`
- `corpus/linkedin-audit/pillars/p3-thesis-resonance.md`
- `corpus/linkedin-audit/pillars/p4-conversion-north-star.md`
- `corpus/linkedin-audit/pillars/p5-competitive-benchmarking.md`
- `corpus/linkedin-audit/pillars/p6-voice-brand-hygiene.md`

**Master Tracker views**
- `corpus/linkedin-audit/views/compounders.md`
- `corpus/linkedin-audit/views/late-bloomers.md`
- `corpus/linkedin-audit/views/format-decay-curves.md`

**Deep dive (referenced, not run by default)**
- `corpus/linkedin-audit/deep-dive/trigger-criteria.md`
- `corpus/linkedin-audit/deep-dive/enrichment-checklist.md`

## Constants

```
RUN_TIMEZONE                = America/New_York
RUN_CADENCE                 = First Sunday of each month, 20:30
EXPORT_WINDOW_DAYS          = 30
MAX_MONTHLY_TASKS           = 3
DEEP_DIVE_CRITERION         = top-5-by-absolute-impressions
NEWSLETTER_GATE_IMPRESSIONS = 5000
NEWSLETTER_GATE_ENG_RATE    = 0.03
NEWSLETTER_GATE_SUSTAIN_WK  = 8
NEWSLETTER_GATE_WAITLIST    = 200
DOMAIN_BALANCE_TARGET       = 50% Context Intelligence / 30% PM / 20% Leadership
ICP_SENIORITY_FILTER        = Senior + Director + CXO + Owner
VOICE_DRIFT_SAMPLE_SIZE     = 4

DRIVE_EXPORT_FOLDER_PATH    = Brand > Linkedin Archive > _Content Analytics
DRIVE_TRACKER_FILE_PATH     = Brand > Linkedin Archive > _Content Analytics > _LinkedIn_Post_Performance_Master
MASTER_TRACKER_FILE_ID      = 17DPE9FNx3gOAJNgbaMNUPYMteKRwv59XDZyZEcNw2G4
MASTER_TRACKER_SHEET_ID     = 17DPE9FNx3gOAJNgbaMNUPYMteKRwv59XDZyZEcNw2G4

ZAPIER_SHEETS_APP           = google-sheets
ZAPIER_RAW_REQUEST          = _zap_raw_request
SHEETS_API_BASE             = https://sheets.googleapis.com/v4/spreadsheets

LINEAR_TEAM_ID              = 72132418-b477-4450-a30a-77391d5cfc47
LINEAR_PROJECT_ID           = 085484ef-b523-4142-bce2-7f9a23a05fa1
LINEAR_ASSIGNEE_ID          = 646e8aef-65f5-47de-ba40-4f2ad99bbc15

NOTION_BRAND_PARENT_ID      = 333ac0ea4f658086bcafcd3f53299b89
NOTION_AUDITS_PAGE_ID       = 356ac0ea4f6580278a7ac7be039b8987       (Brand → Audits — parent of LinkedIn Audits DB)
NOTION_LINKEDIN_AUDIT_DB_ID = 9ccff092811d479891a684c402e6da91       (Monthly LinkedIn Audits DB)
NOTION_LINKEDIN_AUDIT_DS_ID = d5206b14-756d-422d-b54b-74d57560e321   (Monthly LinkedIn Audits data source)
CONTENT_TOPICS_DB_ID        = 0fcb9c17695f4c04a72b6b03fe074f8b       (Content Topics — actual published-content tracker; multi-select Format + Domain + Content Type)
CONTENT_TOPICS_DS_ID        = bb5c7ff7-40ac-49d6-9d1a-7bbee1e3f92e   (Content Topics data source)
COMPETITORS_DB_ID           = c99eaa6d2e7448f0859ce6feba22a3ac
COMPETITORS_DS_ID           = 596ee7d6-46d8-464a-adfc-489576de0052

SLACK_CHANNEL               = #brand
```

**Notion DB property names (canonical):** `Audit` (title), `Audit Date`, `Period Start`, `Period End`, `Overall Status`, `Posts Published`, `Total Impressions`, `Engagement Rate`, `Avg Impressions Per Post`, `Net Follower Growth`, `Total Followers EOP`, `ICP Match Pct`, `Top Format`, `Top Domain`, `Domain Mix Drift`, `Gate 1 Impressions`, `Gate 2 Engagement`, `Gate 3 ICP Quality`, `Gate 4 Waitlist`, `Linear Tasks Issued`, `Deep Dive Candidates`. Overall Status options: `Green` / `Yellow` / `Red` (no emoji prefix in the DB; emoji used in the page body and Slack post).

## Process

### Step 1 — Bootstrap
Per `methodology/bootstrap.md`:
1. Verify required MCP connectors are reachable (Notion, Linear, Slack, Google Drive).
2. Find the latest export in `DRIVE_EXPORT_FOLDER_PATH`. Identify the previous-month export for the diff baseline.
3. Read Posts Master, Snapshots, Monthly Summary tabs from the Master Tracker.
4. Read Content Topics DB rows that match the period (for format/domain mapping of new posts).
5. Read Competitors DB rows where Tier ∈ {Direct, Aspirational}.
6. Initialize an empty findings buffer keyed by pillar.

### Step 2 — Parse the export
Per `methodology/export-parsing.md`. Read all 5 sections: DISCOVERY, ENGAGEMENT, TOP POSTS by Engagements, TOP POSTS by Impressions, FOLLOWERS, DEMOGRAPHICS. Surface any parsing anomalies (unexpected schema changes from LinkedIn) as a P0 finding under P1 Reach & Velocity.

### Step 3 — Update the Master Tracker
Per `methodology/master-tracker-update.md`. Uses Zapier `_zap_raw_request` to call the Sheets API directly:

1. Generate the three tab CSVs in bash.
2. `values:batchUpdate` to upsert Posts Master rows (key = Post URL, column A).
3. `values:append` to append Snapshots rows (append-only).
4. `values:append` to append the Monthly Summary row.
5. First run only: `values:batchClear` then `values:batchUpdate` to write QUERY formulas into A1 of Compounders and Late Bloomers tabs.

Do NOT use Drive MCP (creates new files, can't update cells). Do NOT use Claude in Chrome MCP (`docs.google.com` blocked at policy level).

### Step 4 — Run the six pillars
For each pillar corpus entry, evaluate against parsed export + updated tracker. Write findings to the buffer with severity (P0/P1/P2). Order:

1. P1 Reach & Velocity
2. P2 Audience Composition
3. P3 Thesis Resonance
4. P4 Conversion & North Star
5. P5 Competitive Benchmarking
6. P6 Voice & Brand Hygiene

P5 is the longest block (~10 minutes for web_fetch on Direct + Aspirational competitors).

### Step 5 — Identify Deep Dive candidates
Per `methodology/deep-dive-candidate-selection.md`. Using `DEEP_DIVE_CRITERION`, select 5 post URLs. Write to the Notion audit page property `Deep Dive Candidates` as comma-separated. Do NOT enrich — that's a separate sub-workflow Riché triggers manually.

### Step 6 — Newsletter gate check
Compute current state for each of the 4 gates. Mark each as Met / Not Met / Approaching. The audit narrative includes a one-line trajectory ("Engagement rate trending +0.05pp/month — at this rate, gate 2 is met in {N} months").

### Step 7 — Assemble report
Per `methodology/report-assembly.md`. Build the audit page in memory. Compute headline color: Green if all 6 pillars at P2 or better AND no newsletter gate regressed; Yellow if 1–2 P1 findings OR a gate regressed; Red if any P0 finding OR 2+ gates regressed. Do not write to Notion yet.

### Step 8 — Issue tasks
Per `methodology/task-issuance.md`. Take the top P0 + P1 findings, capped at `MAX_MONTHLY_TASKS` (3). Create Linear issues in `LINEAR_PROJECT_ID`, assigned to `LINEAR_ASSIGNEE_ID`, with due dates spread Mon–Wed–Fri across the first week of the month. Use the create-then-update pattern. Capture the TRZ-### IDs.

### Step 9 — Write Notion page
Single write to the Monthly LinkedIn Audits DS (`NOTION_LINKEDIN_AUDIT_DS_ID`). Page title format: `LinkedIn Audit — {Month YYYY}`. Properties per `databases/monthly-audits-notion-schema.md`. Include the Linear TRZ-### IDs in the `Linear Tasks Issued` property and the body's Linear Tasks Issued section. Set `Overall Status` last, after task issuance is confirmed.

### Step 10 — Slack notification
Per `methodology/slack-notification.md`. One-line headline to `SLACK_CHANNEL` with traffic-light emoji, period name, key finding, task count, and Notion page link.

## Deep dive sub-workflow (manual trigger)

Triggered by Riché after he reviews the audit's Deep Dive Candidates list. Invocation: `/rz-linkedin-audit deep-dive {post-url}` or natural-language equivalent. Per `corpus/linkedin-audit/deep-dive/enrichment-checklist.md`, gather:

- Engagement type breakdown (reactions, comments, bookmarks, shares — NOT in the bulk export)
- Commenter list with ICP match flagged
- Click data where applicable
- Post copy and thesis classification
- Comments themed (substantive vs. drive-by)
- Inferred mechanism

Source: LinkedIn Community Management API once the context management system has it; manual or browser-assisted in the meantime. Output: appended to the current month's Notion audit page as a "Deep Dive: {post URL}" sub-section.

## What this skill does NOT do

- It does not draft or publish content. P3 fires Linear tasks; Riché writes via `/rz-draft-content`.
- It does not auto-tag posts by Format or Domain. Tagging is done in the Content Topics DB at publish time. Untagged posts surface as Unclassified for manual cleanup.
- It does not measure X. X is published-to but not audited (deferred).
- It does not enrich Deep Dive candidates automatically. That's a separate sub-workflow Riché triggers per candidate.
- It does not own voice canon or audience strategy. Reads those from `rz-copywriting` and `rz-growth-marketing`.
- It does not compute follower-count gates. The follower-count newsletter gate is retired (Riché surpassed it). Engagement quality is the gate.
- It does not create the Master Tracker Google Sheet. Riché creates it once per `databases/master-tracker-sheet-schema.md`.
- It does not use Claude in Chrome for Master Tracker updates. `docs.google.com` is blocked at policy level; Zapier Sheets API is the canonical path.

## Cross-skill connections

**Upstream (the audit reads from these for canonical knowledge):**

- `rz-copywriting` — owns the Fatal Fifteen AI-tells list and 50/30/20 domain balance. P6 voice checks read from `corpus/voice/`.
- `rz-growth-marketing` — owns the ICP definition, audience flywheel, and the LinkedIn monthly export workflow. P2/P3 reference `corpus/growth/`; the export workflow (`linkedin-monthly-dump-workflow.md`) is the upstream cadence this audit depends on.
- `rz-website-audit` — shares the Competitors DB (`COMPETITORS_DB_ID`). P5 reads the same Direct + Aspirational tier rows used for the website audit's competitor benchmarking.

**Downstream (the audit hands off to these for fixes):**

- `rz-draft-content` — when P3 fires for low Context Intelligence engagement, the resulting Linear task may reference rz-draft-content for the next CI piece.
- `rz-copywriting` — P6 voice findings reference rz-copywriting's voice rules. The audit detects drift; rz-copywriting fixes it.
- `rz-quarterly-review` — reads the Monthly LinkedIn Audits DB (this skill's output) for trend context. The quarterly review now consumes monthly audit pages instead of re-parsing raw LinkedIn data.
- `rz-self-improve` — runs as the SessionEnd hook in retrospective mode; logs any audit-time exceptions for next-run improvement.

## Common Mistakes

| Mistake | What goes wrong | Fix |
|---|---|---|
| Issuing more than 3 tasks per audit | Compounds into unmanageable backlog at monthly cadence | MAX_MONTHLY_TASKS = 3; reserve P2 findings for narrative-only |
| Treating P5 as P0/P1-eligible | P5 is informational; competitive findings inform strategy but don't seed tasks | Keep P5 narrative-only |
| Auto-enriching all 5 Deep Dive candidates | Burns 75-150 min on candidates that may not warrant it | Surface candidates in audit; Riché picks 0-5 to enrich manually |
| Skipping Voice Drift Sample because "the posts looked fine" | Voice drift is the silent killer; small-sample lint is the discipline | P6 always runs; 4 random posts every month |
| Modifying past Snapshots rows in the Master Tracker | Append-only discipline broken; time series corrupted | Surface bad rows as P2 anomalies; never rewrite |
| Writing Notion page before Step 8 completes | Linear Tasks Issued property becomes stale | Order matters: Step 8 (Linear) before Step 9 (Notion) before Step 10 (Slack) |
