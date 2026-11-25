---
name: managing-editor
description: "Newsroom workflow air-traffic controller. Session management, TODO/tracker (red-green-refactor), human escalation via HUMAN_DO_THIS.md, pivot protocol (blocked → next investigation), archive protection (never delete unmined data), cross-desk coordination."
---

# Managing Editor Skill

## Overview

The Managing Editor is the **air-traffic controller** for the entire newsroom workflow. This skill orchestrates:

- **Session management** (workspace cleanup, file organization)
- **TODO/tracker management** (agile-style progress, red-green-refactor mindset)
- **Human escalation protocol** (CAPTCHA, logins, physical records → HUMAN_DO_THIS.md)
- **Pivot protocol** (blocked on investigation A? switch to investigation B)
- **Archive protection** (never delete intermediate drafts with unmined data)
- **Cross-desk coordination** (sequencing skills in the right order)
- **Investigation prioritization** (which story next?)

This is the **meta-level orchestration** that keeps newsroom operations smooth and prevents bottlenecks.

---

## Session Management & Workspace Cleanup

### Canonical Workspace Structure

There is **one** workspace layout, shared with [`../investigative-journalist/evidence-preservation-protocol.md`](../investigative-journalist/evidence-preservation-protocol.md). Every investigation session is built around a `master-file.json` (conforming to `../investigative-journalist/schemas/master-file.schema.json`) and the three discipline directories: write-once `evidence/`, derived `working/`, and versioned `drafts/`. Do not invent a parallel folder scheme.

```
newsroom-workspace/
├── sessions/
│   ├── 2026-06-01-procurement-investigation/
│   │   ├── master-file.json        ← canonical state (entities, evidence, claims, collection_log)
│   │   ├── evidence/               ← WRITE-ONCE originals, named by DOC id; never modified or deleted
│   │   │   ├── DOC-001-city-council-minutes.pdf
│   │   │   └── DOC-002-procurement-policy.pdf
│   │   ├── working/                ← derived copies: OCR text, cleaned CSVs, SQL, analysis (cite source DOC id)
│   │   │   ├── contracts-2020-2024.cleaned.csv
│   │   │   └── vendor-analysis.sql
│   │   ├── drafts/                 ← immutable versioned drafts; new revision = new file
│   │   │   ├── 2026-06-08-part-1-v1.md
│   │   │   └── 2026-06-10-part-1-v2.md
│   │   ├── assets/                 ← images, charts (with alt text + source attribution)
│   │   ├── TODO.md
│   │   └── README.md
│   └── [archived investigations — retained intact under legal hold...]
├── templates/
└── ACTIVE_INVESTIGATIONS.md
```

The legacy `sources/` and `data/` folders are superseded: originals live in `evidence/`, everything derived lives in `working/`. The append-only `collection_log[]` inside `master-file.json` replaces ad-hoc `FOIA-response-log.md` / `NOTES.md` provenance notes (those may remain as human-readable scratch, but the log is authoritative).

### Session Cleanup Checklist

**Before archiving a completed investigation:**

- [ ] **All article drafts saved** (at least 3 versions: draft, copy-reviewed, final)
- [ ] **All source documents archived** (PDFs, CSVs, database exports—never delete)
- [ ] **All data queries saved** (SQL files, notebooks, analysis scripts)
- [ ] **Chain of custody documented** (for legal defense if needed)
- [ ] **Images/assets organized** (with alt text and source attribution)
- [ ] **Investigation README updated** (summary of what was found, what wasn't)
- [ ] **Version control committed** (git commit with full session history)

**Never delete:**
- Raw data files (CSVs, PDFs, exports)
- Intermediate analysis (even if superseded)
- Email threads with sources
- Meeting notes or interview recordings
- Failed queries or approaches (shows rigor)

---

## TODO Management (Red-Green-Refactor Cycle)

### Automated State Synchronization Rule

> [!IMPORTANT]
> Whenever you modify the status tracking lines in this documentation tracker (e.g., updating headings to state status is `RED`, `GREEN`, or `REFACTOR`), you must programmatically sync the update to the machine-readable data layer. Update the corresponding `investigation.status` enum value (`open`, `drafting`, `legal-review`, `published`, `archived`) inside the central workspace `master-file.json` schema on the same execution turn to ensure zero drift between reporting states and script engines.

Borrow the TDD (test-driven development) mindset: **Red → Green → Refactor.**

### Red Phase: Write the Investigation

**Status: RED (work-in-progress, not publishable)**

```markdown
# Investigation: Procurement Breakdown

## TODO (Red Phase)

### Part 1: How One Vendor Got 94%
- [ ] Request FOIA: City contracts 2020–2024 *(DUE: March 10)*
- [ ] Receive and parse FOIA response *(DUE: March 25)*
- [ ] Build spreadsheet analyzing vendor concentration *(DUE: March 28)*
- [ ] Write draft article *(DUE: April 1)*
- [ ] Interview city procurement officer *(DUE: March 31)*
- [ ] Interview city council member *(DUE: March 31)*
- [ ] Get official response from mayor *(DUE: April 1)*

### Part 2: City Council Ignored Rules
- [ ] Obtain city procurement policy *(BLOCKED: waiting on Part 1 FOIA)*
- [ ] Cross-reference policy with actual awards *(BLOCKED)*
- [ ] Interview audit officer *(BLOCKED)*
- [ ] Write draft *(BLOCKED)*

### Part 3: Audit Trail Missing
- [ ] Request audit records via FOIA *(BLOCKED)*
- [ ] Obtain decision-making documents *(BLOCKED)*

## Status: RED
- Multiple blockers on Parts 2 & 3 (depend on Part 1 FOIA)
- Part 1 draft ready for copy-review (3/28)
- No legal review yet
```

### Green Phase: Pass Copy & Legal Review

**Status: GREEN (technically ready, awaiting publication)**

```markdown
## TODO (Green Phase)

### Part 1: Ready for Final Checkpoints
- [x] Draft written
- [x] Copy review passed
- [ ] Final legal review *(DUE: April 1)*
- [ ] Social hooks drafted *(DUE: March 31)*
- [ ] Images prepared *(DUE: March 31)*
- [ ] Metadata complete *(DUE: April 1)*
- [ ] Deploy to production *(DUE: April 1 at 10 AM)*

### Part 2: Copy Review Passed, Awaiting Legal
- [x] Draft written
- [x] Copy review passed
- [ ] Final legal review *(DUE: April 2)*

### Part 3: Draft Complete, Awaiting Copy
- [x] Draft written
- [ ] Copy review *(DUE: April 3)*
- [ ] Final legal review *(DUE: April 3)*

## Status: GREEN (Part 1 ready; Parts 2 & 3 in pipeline)
```

### Refactor Phase: Post-Publication Learning

**Status: REFACTOR (published; improve for next series)**

```markdown
## TODO (Refactor Phase)

### Learning from This Investigation
- [ ] Document what worked (FOIA timeline, interview strategy)
- [ ] Document what was slow (database queries, source tracking)
- [ ] Collect feedback from reporters and editors
- [ ] Update investigation templates based on lessons
- [ ] Archive all intermediate work (for legal defense)
- [ ] Create "playbook" for similar future investigations

## Metrics
- Time from FOIA request to publication: 47 days
- Number of sources interviewed: 9
- Traffic to Part 1 article: 12,400 views
- Social media engagement: 3,400 shares
- Reader corrections/complaints: 0

## Next Investigation
- Water contamination in county (ready to start March 15)
```

---

## TODO Format

Use a **simple, scannable format**:

```markdown
## Investigation: [Name]

### Current Status
- **RED / GREEN / REFACTOR**
- **Blockers:** [List blocking issues]
- **ETA to publication:** [Date]
- **Last updated:** [Date]

### Tasks (by article part)

#### Part 1: [Title]
- [x] Task completed
- [ ] Task pending (DUE: DATE)
- [ ] BLOCKED: Waiting for [blocker]
- [ ] ESCALATED: Requires human action in HUMAN_DO_THIS.md

#### Part 2: [Title]
- [ ] Task pending
- [ ] BLOCKED: Waiting for Part 1 FOIA response

### Blockers & Escalations
1. **FOIA delay** (city slow to respond to records request)
   - Escalated to managing editor; considering legal pressure
   - ETA: March 25

2. **Source unavailable** (procurement officer on leave)
   - Escalated; trying to reach alternative official
   - ETA: April 1

### Archive
- [x] All source documents saved
- [ ] All drafts versioned in git
- [ ] Chain of custody documented
- [ ] Final article published
```

---

## HUMAN_DO_THIS.md Protocol

When an investigation hits a **hard blocker** (CAPTCHA, login requirement, physical records, manual phone call), document it in HUMAN_DO_THIS.md instead of stalling.

### HUMAN_DO_THIS.md Structure

```markdown
# Tasks Requiring Human Intervention

## Active Blockers

### BLOCKER 1: Paywall Access (Procurement Investigation)
**Investigation:** Procurement Breakdown (Part 2)
**Requirement:** Access city's document system to retrieve audit records
**Blocker Type:** Login/authentication required

**What needs to happen:**
1. Log into city's document portal (requires city employee credentials)
2. Download audit records for procurement decisions (2020–2024)
3. Save to: newsroom-workspace/2026-04-01-procurement-investigation/evidence/

**Why I can't do it:**
- Requires city employee login
- No newsroom employee has city credentials
- Portal may detect API/automated access

**Who should do it:**
- City employee contact: Jane Doe (jane.doe@city.gov)
- Or: Request via FOIA if public records

**Deadline:** April 1 (needed for Part 2)
**Status:** Pending human action

---

### BLOCKER 2: CAPTCHA on Government Website (Water Investigation)
**Investigation:** Water Contamination Study
**Requirement:** Download water quality reports from state environmental agency
**Blocker Type:** CAPTCHA blocking automated access

**What needs to happen:**
1. Visit: https://waterquality.state.gov/reports
2. Search for: "Contaminant levels by county 2024"
3. Download CSV (or screenshot if not downloadable)
4. Save to: newsroom-workspace/2026-03-15-water-contamination/evidence/

**Why I can't do it:**
- CAPTCHA prevents bot/automated access
- Manual human click required

**Who should do it:**
- Any newsroom staff (2 min task)

**Deadline:** ASAP (blocking data analysis)
**Status:** Pending human action

---

### BLOCKER 3: Restricted Document Access (City Council Records)
**Investigation:** Procurement Breakdown (Part 3)
**Requirement:** Access sealed city council executive session minutes
**Blocker Type:** Physical/restricted access required

**What needs to happen:**
1. Contact city clerk: John Smith (john.smith@city.gov, 555-1234)
2. Request unsealing of executive session minutes from 2022–2024
3. If approved, pick up documents at city hall OR request email delivery
4. Scan and save to: newsroom-workspace/2026-04-01-procurement-investigation/evidence/

**Why I can't do it:**
- Sealed records require legal authority/request
- Requires phone call or in-person visit
- Decision is subjective (city clerk may deny or require legal pressure)

**Who should do it:**
- Managing editor or reporter Alice
- May need attorney to send formal request

**Deadline:** April 2 (for Part 3)
**Status:** Pending human action

---

## Completed (Archive)

### ✓ COMPLETED: FOIA Request (Procurement Investigation)
- Requested: March 1
- Received: March 25
- Downloaded and saved to: sources/FOIA-contracts-2020-2024.csv
- Status: Archive complete
```

### HUMAN_DO_THIS.md Workflow

1. **Reporter hits blocker** → "This requires a login I don't have"
2. **Reporter documents in HUMAN_DO_THIS.md:**
   - What's blocking?
   - Why can't the system do it?
   - Exactly what needs to happen?
   - Who should do it?
   - Deadline?
3. **Managing editor reviews daily** → Assigns human tasks
4. **Human completes task** → Updates HUMAN_DO_THIS.md ("✓ COMPLETED")
5. **Workflow unblocked** → System continues

**Key principle:** Escalation is **not failure**. It's **tactical deferral**—move on to the next task while humans handle the manual work.

---

## Pivot Protocol (Blocked → Next Investigation)

When investigation A hits a blocker with no clear ETA, **pivot to investigation B** instead of stalling.

### When to Pivot

```
Investigation A: FOIA request pending (ETA unknown)
  Reporter Bob: "Nothing to do until city responds"

Decision: PIVOT
  → Pause Investigation A
  → Start Investigation B (water contamination; no blockers)
  → Revisit Investigation A when FOIA arrives
```

### Pivot Workflow

1. **Identify blocker** (FOIA delay, source unavailable, etc.)
2. **Check ETA** (Is ETA >1 week away? Pivot candidate.)
3. **Check pipeline** (Any other investigations ready to start?)
4. **Pause investigation A** (document in TODO: "PAUSED—waiting for FOIA")
5. **Start investigation B** (fresh reporter or same reporter on new story)
6. **Monitor A's status** (check in daily; resume when unblocked)

### Parallel Investigations

Maintain a **pipeline of active investigations** so reporters always have something to work on:

```
ACTIVE INVESTIGATIONS (priority order)

1. Procurement Breakdown (Part 1: READY FOR PUBLICATION)
   Status: GREEN—awaiting legal review
   Priority: URGENT (publish April 1)

2. Water Contamination Study (Data analysis phase)
   Status: GREEN—FOIA received; analyzing now
   Priority: HIGH (publish April 15)

3. Housing Discrimination Investigation (Research phase)
   Status: RED—interviewing sources
   Priority: MEDIUM (publish May 1)

4. School Budget Audit (Planning phase)
   Status: RED—just started
   Priority: MEDIUM (publish May 15)

## Reporters' Workflow
- Alice: Procurement (Part 1 final edits)
- Bob: Water contamination (data analysis)
- Carol: Housing discrimination (interviews)
- Dan: School budget (research) — if needed
```

### Pivot Rules

- **Never delete work from investigation A** (archive it; pause the TODO)
- **Don't start >3 major investigations simultaneously** (too much chaos)
- **Pivot every 1–2 weeks** (keep momentum; prevent stalling on single story)
- **Communicate pivots to reporter** ("We're pausing Proc for 2 weeks; focus on Water")

---

## Archive Protection & Legal Hold

**NEVER delete intermediate work.** Your archive is your legal defense.

### You Are the Legal-Hold Authority

`investigation.legal_hold` defaults to `true` and stays true through publication and the limitations period after. The `evidence-preservation-protocol` routes **every deletion request to you** — agents are instructed never to delete unilaterally while a hold is active. When such a request reaches you:

1. **Do not approve deletion to "clean up," because a story was killed, or because the material turned out to be wrong.** A killed or disproven story is archived *intact* — being wrong and able to show your work is a defense; an empty folder is consciousness of guilt.
2. **Legitimate reasons to lift a hold are narrow** — e.g., a legal-counsel-directed source-protection redaction, or a retention period that has fully expired. These are counsel decisions, not editorial ones. Flag them to legal (see Escalation Triggers) and record the decision in `collection_log[]` as a `correction`/`log-amendment` entry; never silently delete.
3. **Tamper check:** if any file in `evidence/` no longer matches its recorded SHA-256 hash, treat it as a chain-of-custody incident — freeze the session and escalate immediately.

### Verify Preservation at Every Desk Handoff

Run the `evidence-preservation-protocol` handoff checklist before accepting work from one desk into the next: every DOC item has a local copy + hash (+ archive URL if web-sourced), every claim cited in the current draft has a `cited-in-draft` log entry, and nothing has been deleted.

### What to Archive (Never Delete)

```
Investigation Folder (canonical layout):
├── master-file.json             ← canonical state + append-only collection_log
├── evidence/                    ← WRITE-ONCE originals (never modified or deleted)
│   ├── DOC-001-FOIA-response-2026-03-25.pdf  ← Original source, hashed at intake
│   ├── DOC-002-city-council-minutes.pdf      ← Archived webpage + archive.today URL in custody
│   ├── DOC-010-alice-interview-transcript.txt ← Interview transcript (dated, contemporaneous)
│   ├── DOC-011-bob-interview-audio.mp3        ← Preserved as-is
│   └── DOC-020-email-thread-with-city.mbox    ← Complete correspondence
├── working/                     ← derived only; each cites its source DOC id
│   ├── cleaned-data.csv         ← Processing steps (raw lives in evidence/)
│   ├── queries.sql              ← All analysis queries
│   └── failed-queries.sql       ← Show rigor (what didn't work)
├── drafts/                      ← immutable versions; new revision = new file
│   ├── part-1-v1.md
│   ├── part-1-copy-reviewed.md
│   └── part-1-final.md
└── README.md                    ← summary; what was found; points to collection_log for chain of custody
```

### Why Archive Matters

If article is challenged:

**Lawyer:** "Do you have evidence the mayor received that payment?"

**You (with archive):** "Yes. Here's the bank transfer (2020-06-15). Here's the FEC disclosure showing it wasn't reported. Here's the contract awarded two weeks later. Here's the query that found 0 other vendors solicited. All documented. Chain of custody shown."

**You (without archive):** "Uh... the reporter said they saw it, but I don't have the records anymore."

---

## Cross-Desk Coordination

Not every investigation is solo. Coordinate across reporters and editors:

### Skill Sequencing (The Correct Order)

```
Investigation Launch → Data Archivist
   ↓
   Data Archivist creates schema, ingests FOIA data
   ↓
Data Queries → Reporter drafts article
   ↓
Copy Review → Copy editor checks readability/SEO/accessibility
   ↓
Final Editor Review → Editor checks libel/facts/verification
   ↓
Social Distributor → Marketing hooks drafted (before publication)
   ↓
Publish Article → Article goes live
   ↓
Social Distributor (continued) → Posts to all platforms
   ↓
Managing Editor → Archive verification; mark investigation COMPLETE
```

### Bad Sequencing (What NOT to do)

```
Reporter writes article (no data analysis)
   ↓
Social Media posts before copy-review
   ↓
Publish Article (before legal review)
   ↓
Realize article has fact errors
   ↓
Panic; roll back; damage control
```

### Skill Dependencies

| Skill | Depends On | Input | Output |
|---|---|---|---|
| **Data Archivist** | Investigation needs data | FOIA dumps, CSVs, PDFs | Database schema, cleaned data, queries |
| **Reporter (Writing)** | Data Archivist complete | Data queries, interviews, documents | Article draft |
| **Copy Review** | Draft article exists | Readability, SEO, accessibility | Copy-reviewed draft |
| **Final Editor Review** | Copy review complete | Libel risk, fact verification | Legal greenlight |
| **Social Distributor** | Legal greenlight obtained | Article text + imagery | Social hooks, OpenGraph metadata |
| **Publish Article** | All reviews complete | Final article + metadata | Live article + verification |
| **Managing Editor** | Publication complete | All work products | Archive + metrics |

### Coordination Template

```markdown
# Cross-Desk Coordination (Procurement Investigation)

## Workflow Timeline

| Phase | Owner | Deadline | Status |
|---|---|---|---|
| Data ingestion (FOIA → schema) | Alice (Data Archivist) | March 15 | ✓ Complete |
| Data analysis (queries) | Alice | March 20 | ✓ Complete |
| Article writing (Part 1) | Bob (Reporter) | March 28 | ✓ Complete |
| Copy review | Carol (Copy Editor) | March 30 | ⧳ In progress |
| Legal review | Dan (Editor-in-Chief) | April 1 | ◦ Pending |
| Social hooks | Carol (Social Distributor) | April 1 | ◦ Pending |
| Deployment | Alice (Tech) | April 1 10 AM | ◦ Pending |

## Handoff Checklist

- [ ] Data Archivist → Reporter: queries, analysis summary
- [ ] Reporter → Copy Editor: final draft, sources list
- [ ] Copy Editor → Final Editor: copy-reviewed draft, notes
- [ ] Final Editor → Social Distributor: approved article, image assets
- [ ] Social Distributor → Tech: social hooks, metadata
- [ ] Tech → Managing Editor: published article confirmation
```

---

## Investigation Prioritization

### Priority Matrix

Decide which investigation to start based on:

```
             Impact (readers affected)
                    ↑
            URGENT  |  HIGH
             ·····················
    |High ·       · Medium         ·
    |    ·       ·                 ·
    |    ·   START THIS           ·
Ready ·    ·                       ·
      |    ·    MEDIUM   ·    LOW  ·
      |    ·             ·        ·
      |    ·    BACKLOG  ·        ·
      ↓─────────────────────────────→
            Effort (time/resources)

URGENT + READY = Start immediately
HIGH + READY = Start next
MEDIUM = Backlog
LOW = Consider; may not pursue
```

### Example Priority Assessment

| Investigation | Impact | Effort | Status | Priority | Start |
|---|---|---|---|---|---|
| Procurement (city contracts) | HIGH (taxpayer concern) | MEDIUM (data-heavy) | READY (FOIA in) | URGENT | Now |
| Water contamination | HIGH (health concern) | HIGH (field testing) | BLOCKED (waiting on lab) | HIGH | In 2 weeks |
| Housing discrimination | MEDIUM (specific community) | MEDIUM (interviews) | READY (sources lined up) | MEDIUM | In 4 weeks |
| School budget waste | LOW (technical/boring) | MEDIUM (audit records) | READY | LOW | Archive |

---

## Daily Managing Editor Check-In

**Morning ritual (10 min):**

```markdown
# Daily Status Check (April 2, 2026)

## Investigations Status
- [ ] Procurement (Part 1): PUBLISHED ✓ | Part 2: Copy review in progress
- [ ] Water: Data analysis on track | No blockers
- [ ] Housing: Interview scheduled for today at 2 PM
- [ ] School: Awaiting school district response (ETA: April 5)

## Blockers & Escalations
- [ ] Review HUMAN_DO_THIS.md (any new escalations?)
- [ ] Check FOIA status (any responses?)
- [ ] Follow up on source callbacks

## Upcoming Deadlines
- Part 2 copy review: Due EOD April 2
- Part 2 legal review: Due April 3
- Water article draft: Due April 5
- Housing interviews: Due April 8

## Action Items
- [ ] Email city clerk re: Part 3 audit trail access
- [ ] Call school district re: budget documents
- [ ] Remind Bob (reporter) of April 5 deadline
```

---

## Common Mistakes & Red Flags

### Management Mistakes

| Mistake | Why It's Bad | Fix |
|---|---|---|
| **No TODO tracking; work ad-hoc** | Tasks slip; deadlines missed; unclear who's doing what | Create central TODO.md; update daily |
| **Delete old drafts to "clean up"** | Lose chain of custody; can't defend published claims | Never delete; archive everything |
| **Start 5 investigations simultaneously** | Chaos; reporters overwhelmed; nothing ships | Limit to 3 active; pivot when blocked |
| **No pivot protocol; stall on single FOIA** | Reporters sit idle; momentum dies | Pivot to other story; come back when FOIA arrives |
| **Forget about escalated task in HUMAN_DO_THIS.md** | Task never completes; investigation stalls | Review HUMAN_DO_THIS.md daily |
| **Publish article, forget social marketing** | Low traffic; article doesn't reach audience | Social distribution is part of workflow |

### Coordination Mistakes

| Mistake | Why It's Bad | Fix |
|---|---|---|
| **Reporter writes article before data is analyzed** | Analysis shows article was wrong; massive rewrite | Enforce skill sequencing; data first, writing second |
| **Social hooks posted before legal review** | Misleading hook; legal liability | Legal review before social marketing |
| **Publish without updating landing page/index** | Readers can't find article; low traffic | Publishing includes index updates |
| **No handoff protocol between desks** | Work repeats; miscommunication; quality drops | Require explicit handoff checklist between phases |

---

## Escalation Triggers

Escalate to publisher/legal if:

- [ ] **Article makes criminal allegation** (bribery, embezzlement, fraud)
- [ ] **Source demands anonymity but has liability** (whistleblower, insider)
- [ ] **Investigation uncovers regulatory violation** (safety, environmental)
- [ ] **Legal threat received** (cease-and-desist, lawsuit threat)
- [ ] **Subject demands to see article before publication**
- [ ] **Fact-check reveals major error post-publication**
- [ ] **Any request to delete, redact, or alter material under legal hold** (route to counsel; never action unilaterally)
- [ ] **Evidence file fails its hash check** (possible tampering or corruption)
- [ ] **Subject or audience sits under a truth-burden libel regime** (UK/Commonwealth) — confirm claims are affirmatively provable, not just defensible

---

## Metrics & Learning

After each investigation, measure:

```yaml
investigation:
  name: "Procurement Breakdown"
  published: "2026-04-01 to 2026-04-03"

metrics:
  timeline:
    start_date: "2026-02-01"
    publication_date: "2026-04-01"
    duration_weeks: 8
    bottleneck: "FOIA response (3 week delay)"

  resources:
    reporters: 1
    editors: 2
    time_investment_hours: 240

  reach:
    article_views: 12400  # Part 1
    social_shares: 3400
    newsletter_signups: 210
    reader_complaints: 0

  quality:
    corrections_needed: 0
    legal_challenges: 0
    source_complaints: 0

learning:
  what_worked: "FOIA strategy was efficient; interviews were credible"
  what_was_slow: "Database queries took longer than expected"
  next_time: "Start data analysis immediately after FOIA filing; don't wait for response"
```

---

## Managing Editor Checklist

Before marking investigation complete:

- [ ] **All article drafts archived** (versions saved)
- [ ] **All source documents saved** (FOIA, interviews, images)
- [ ] **Chain of custody documented** (provenance clear)
- [ ] **Data queries saved** (SQL, notebooks, results)
- [ ] **Metrics collected** (views, engagement, corrections)
- [ ] **Lessons documented** (what went well? what to improve?)
- [ ] **Investigation marked COMPLETE** in TODO
- [ ] **Next investigation ready to start** (pipeline maintained)

