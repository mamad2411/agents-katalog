---
title: Civil Mobile Field Operations
description: Execute Phase 2 5-phase mobile field operations workflow: field setup, site assessment, quality control, progress monitoring, and issue management for construction sites
version: 1.0
frequency_percent: 65.0
success_rate_percent: 90.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/civil-mobile-field-ops
gigabrain_tags: civil-engineering, mobile, field-operations, site-inspection, progress-monitoring, quality-control
openstinger_context: mobile-field-workflows, offline-first
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/domain-knowledge/00850_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/domain-knowledge/00850_GLOSSARY.MD
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/00850_AGENTS-REGISTRY-SUMMARY.MD
related_skills:
  - pre-task-assessment-readiness
  - mobile-procurement
  - civil-quality-assurance
  - offline-procurement
---

# Civil Mobile Field Operations

## Overview

Execute the 5-phase mobile field operations workflow for civil engineering construction monitoring: Field Setup (session initialization), Site Assessment (data collection), Quality Control (digital inspection), Progress Monitoring (construction tracking), and Issue Management (field problem resolution). Designed for offline-first operation in remote construction environments.

**Announce at start:** "I'm using the civil-mobile-field-ops skill to conduct field operations for civil engineering construction monitoring."

## When to Use This Skill

**Trigger Conditions:**
- Construction site inspection or quality control visit scheduled
- Progress monitoring data collection required
- Defect or non-conformance identified on site
- Daily/weekly progress report needs to be generated
- Field survey or as-built data collection required
- Construction hold point inspection scheduled

**Prerequisites:**
- Mobile app installed and authenticated
- Project data downloaded for offline operation
- Relevant ITPs and inspection checklists available
- CE-MOBILE-001 or CE-FIELD-001 agent available
- GPS, camera, and sensors operational

## Step-by-Step Procedure

### Phase 1: Field Setup (Session Initialization)

**Prepare for field operations:**

**Setup checklist:**
- [ ] Biometric/PIN authentication completed
- [ ] GPS location verified against project geofence
- [ ] Project data package downloaded (ITPs, drawings, checklists, BOQ)
- [ ] Device diagnostics passed (GPS accuracy <5m, camera operational, battery >20%)
- [ ] Last synchronization timestamp recorded
- [ ] Offline mode confirmed if no network available

**Session parameters:**
| Parameter | Value | Purpose |
|-----------|-------|---------|
| Project ID | — | Links all field data to correct project |
| Phase | Setup / Assessment / QC / Progress / Issue | Determines workflow and available features |
| Location | GPS coordinates or zone | Context for data collection |
| Inspector | Name/ID | Accountability for actions |
| Weather | Observed | Context for quality observations |

### Phase 2: Site Assessment (Field Data Collection)

**Capture comprehensive site data:**

**Data collection tools:**
| Tool | Function | Accuracy |
|------|----------|----------|
| GPS Survey | Point capture with RTK correction | ±0.02m (RTK), ±2m (standard) |
| Photo Documentation | Geotagged, timestamped | Visual with coordinates |
| Laser Distance Meter | Linear measurements | ±2mm |
| Level Gauge | Vertical measurements | ±3mm |
| Voice Notes | Dictated observations | Transcribed to text |
| Checklist Forms | Structured data entry | Validated against ITP |

**Data quality validation (real-time):**
- [ ] GPS coordinates within expected project boundaries
- [ ] Photos clear, well-lit, and in focus
- [ ] Measurements physically reasonable
- [ ] Voice transcriptions accurate (human correction available)
- [ ] Checklist all fields completed, no blank required fields

### Phase 3: Quality Control (Digital Inspection)

**Perform structured quality inspections against ITP:**

**Inspection workflow:**
1. **Select ITP** from project checklist
2. **Navigate to location** using map and GPS guidance
3. **Record inspection data** for each checklist item
4. **Capture evidence photos** (defects, workmanship, materials)
5. **Assign Pass/Fail/Hold** status to each item
6. **Generate NCR automatically** if any item fails
7. **Digital sign-off** by inspector (biometric or PIN)
8. **Notify responsible party** if defects found

**NCR auto-generation from failed inspection:**
When checklist item fails:
- Inspector records defect description
- Photos attached automatically
- Specification clause referenced from ITP
- Severity assigned (Critical/Major/Minor)
- Recommended action prompted from defect library
- NCR number auto-assigned
- Distribution list auto-populated

### Phase 4: Progress Monitoring (Construction Tracking)

**Track construction progress against schedule:**

**Progress data captured:**
- Percentage complete per work element
- Quantities installed vs. planned
- Productivity rates (output per crew per day)
- Delay events with cause and duration
- Resource utilization (labor, equipment, materials)
- Weather impact on productivity
- Safety observations

**Progress calculation:**
For each work element:
1. Measure actual quantity installed (linear meters of pipe, cubic meters of concrete, etc.)
2. Compare to planned quantity from BOQ
3. Calculate percentage = actual / planned × 100%
4. Apply weight factor based on element complexity
5. Compute weighted progress index

**Progress report generation:**
- Daily: Site diary with photos, progress %, issues
- Weekly: Progress summary with earned value analysis
- Monthly: Comprehensive report with S-curve and forecast

### Phase 5: Issue Management (Field Problem Resolution)

**Identify, document, and resolve construction issues:**

**Issue types:**
| Type | Urgency | Action |
|------|---------|--------|
| Safety hazard | Immediate | Stop work, alert site manager, photograph hazard |
| Quality defect | Same day | Log NCR, notify superintendent, corrective action |
| Design conflict | Within 48h | Raise RFI, photograph conflict location, reference conflicting documents |
| Schedule delay | Within 24h | Document cause, quantify impact, notify project manager |
| Site condition different | Within 4h | Document with photos and survey, notify geotechnical engineer |

**Resolution tracking:**
- Each issue assigned unique tracking number
- Status tracked: Open → In Progress → Resolved → Verified → Closed
- Photo evidence required at each status change
- Automatic escalation if issue exceeds resolution SLA
- Lessons learned captured at closure

### Phase 6: Data Synchronization

**Sync field data with office systems when connectivity restored:**

**Sync priority order:**
1. Safety reports (immediate)
2. NCRs and critical defects (within 1 hour)
3. RFI submissions (within 2 hours)
4. Progress updates (within 4 hours)
5. Routine checklists and photos (next available bandwidth)
6. Large photo batches and video (overnight batch)

**Conflict resolution:**
- Office system is source of truth for updated documents
- Field data is preserved if it was captured before office updates
- Manual review required if simultaneous edits detected

## Success Criteria

- [ ] Field session initialized with full offline capability
- [ ] All planned inspections completed with signed checklist
- [ ] NCRs generated for all identified defects within 24 hours
- [ ] Progress data captured for all active work fronts
- [ ] All issues logged with tracking numbers and evidence photos
- [ ] Data synchronized with office systems within SLA priorities
- [ ] Daily report generated and distributed automatically

## Common Pitfalls

1. **Incomplete Offline Preparation** — Always download the full project package before going to site. Missing drawings or ITPs in the field wastes time.
2. **Poor Photo Documentation** — Photos must be clear, show the full extent of the defect, and include a reference scale. Blurry photos are useless.
3. **Delayed Synchronization** — Don't hoard field data waiting for perfect connectivity. Sync critical data (safety, NCRs) through any available channel immediately.
4. **Skipping Checklist Items** — Every ITP item must be checked. Marking N/A without justification creates audit gaps.
5. **Unsigned Reports** — Digital signatures establish accountability. Never issue an inspection or NCR without inspector sign-off.

## Cross-References

### Related Skills
- `civil-quality-assurance` — Inspection results feed NCR and design review
- `offline-procurement` — Offline capability patterns and data sync
- `mobile-procurement` — Mobile workflow patterns shared with procurement
- `pre-task-assessment-readiness` — Assess readiness before field visit

### Related Agents
- `CE-MOBILE-001` (OpenClaw) — Mobile workflow orchestration
- `CE-FIELD-001` (OpenClaw) — Field data collection agent
- `CE-QC-001` (JS Swarm) — Construction quality control
- `CE-PROGRESS-001` (JS Swarm) — Progress monitoring and reporting
- `CE-RFI-001` (JS Swarm) — Field RFI submission and tracking

## Example Usage

**Scenario:** Daily quality inspection for drainage pipe installation at chainage 0+100 to 0+250

1. **Field Setup:** Session initialized at 07:30, GPS verified at site boundary, offline mode confirmed, drainage ITP loaded
2. **Site Assessment:** 250m of drainage route surveyed, cover levels spot-checked at 5 locations, photos captured at each test point
3. **Quality Control:**
   - Pipe bedding: 92% MOD AASHTO density (requires 95%) — FAIL → NCR generated
   - Pipe joints: All watertight — PASS
   - Pipe alignment: Within 10mm tolerance — PASS
   - Backfill: Clean granular material per spec — PASS
4. **Progress:** 250m of 800m total pipe installed (31.25%). Planned: 35%. Behind schedule by 3.75%
5. **Issue:** Unforeseen rock encountered at CH 0+180 requiring excavation method change — RFI raised with photos
6. **Sync:** NCR and RFI submitted via mobile signal at 12:00. Daily report synced via site WiFi at 17:00.

## Performance Metrics

**Target Performance:**
- Inspection completion rate: 100% of scheduled inspections
- NCR turnaround time: <24 hours from identification to issuance
- Progress update frequency: Daily for all active work fronts
- Data sync reliability: 99.9% successful synchronization
- Offline functionality: 100% core features available without network
- Photo evidence rate: 100% of NCRs include geotagged photos