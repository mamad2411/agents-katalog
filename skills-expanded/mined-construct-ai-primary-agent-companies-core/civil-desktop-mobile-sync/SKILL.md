---
title: Civil Desktop-Mobile Sync
description: Manage cross-platform data synchronization between civil engineering desktop design systems and mobile field operation platforms
version: 1.0
frequency_percent: 50.0
success_rate_percent: 95.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/civil-desktop-mobile-sync
gigabrain_tags: civil-engineering, data-synchronization, desktop-mobile, offline, cross-platform, conflict-resolution
openstinger_context: sync-architecture, data-consistency
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/domain-knowledge/00850_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/00850_AGENTS-REGISTRY-SUMMARY.MD
related_skills:
  - pre-task-assessment-readiness
  - civil-mobile-field-ops
  - offline-procurement
  - mobile-procurement
---

# Civil Desktop-Mobile Sync

## Overview

Manage data synchronization between desktop civil engineering design systems (CAD, BIM, analysis software) and mobile field operation platforms (iOS/Android apps). Ensures data consistency, handles offline-first operation, resolves conflicts, and maintains the digital thread from concept through construction completion.

**Announce at start:** "I'm using the civil-desktop-mobile-sync skill to synchronize data between desktop and mobile systems."

## When to Use This Skill

**Trigger Conditions:**
- Mobile data needs to sync with office design systems
- Desktop design updates need to push to offline-capable mobile devices
- Conflict detected between concurrent desktop and mobile edits
- Phase transition requires data handoff (design → construction → as-built)
- Network connectivity restored after offline field session
- Data integrity check required between platforms

**Prerequisites:**
- Mobile app authenticated and project data downloaded
- Desktop system accessible with write permissions
- Sync agent (CE-MOBILE-001 or CE-ORCH-001) available
- Both platforms have consistent project context

## Step-by-Step Procedure

### Step 1: Sync Direction Assessment

**Determine sync direction and scope:**
| Scenario | Direction | Data | Frequency |
|----------|-----------|------|-----------|
| Field data collection | Mobile → Desktop | Survey data, inspection photos, NCRs, progress metrics | Continuous when online |
| Design update | Desktop → Mobile | Updated drawings, revised specifications, new ITPs | On demand before field visit |
| RFI/communication | Bidirectional | RFI text and responses, site instructions | Real-time when online |
| As-built update | Mobile → Desktop | As-built measurements, field changes | Daily at minimum |
| Progress reporting | Mobile → Desktop | Quantities installed, delay events | Daily |
| Design clarification | Bidirectional | Marked-up drawings, design notes | On demand |

### Step 2: Data Prioritization and Bandwidth Management

**Prioritize data for sync under constrained connectivity:**

**Priority tiers:**
| Tier | Data Type | Max Delay | Sync Strategy |
|------|-----------|-----------|---------------|
| P0 - Critical | Safety reports, critical NCRs | 0 (immediate) | SMS/cell fallback, retry every 30s |
| P1 - Urgent | RFIs, hold point results | 1 hour | Cell/wifi, retry every 5 min |
| P2 - Important | Progress updates, routine NCRs | 4 hours | Wifi preferred, cell if available |
| P3 - Routine | Checklists, photos, routine data | 24 hours | Batch sync when wifi available |
| P4 - Bulk | Large photo batches, video, DWG | Overnight | Batch sync during off-peak |

**Bandwidth optimization:**
- Differential sync: Send only changed data, not full datasets
- Compression: Compress large data payloads (photos at 70% quality, DWG at 50%)
- Resumable transfers: Support pause/resume for interrupted connections
- Background sync: Sync continues without user intervention
- Local queue: Unsynced data queued locally with clear status indicator

### Step 3: Conflict Detection and Resolution

**Detect and resolve concurrent edits:**

**Conflict detection rules:**
- Timestamp-based: Last writer wins for non-critical fields
- Version-based: Desktop changes override mobile for design data
- Merge-based: Field data adds to (does not replace) desktop progress data
- Flag-based: Conflicts flagged for human review when automated resolution not possible

**Conflict resolution hierarchy:**
1. **Auto-resolve (non-critical):** Text notes, progress percentages, checklists — last writer wins
2. **Priority-resolve (moderate):** ITP updates, field observations — mobile data preserved, desktop notified
3. **Manual-resolve (critical):** Design changes, specification updates, structural modifications — human review required
4. **Quarantine (uncertain):** Data that cannot be confidently auto-resolved — quarantined for review, original data preserved

### Step 4: Offline-First Data Management

**Ensure full functionality when disconnected:**

**Offline capability model:**
- **Full offline:** All inspection, data capture, and progress functions work without network
- **Local storage:** SQLite database on device with all active project data
- **Optimistic updates:** User actions applied locally immediately, sync attempted in background
- **Sync indicator:** Clear UI showing sync status (✓ synced, ⟳ syncing, ⚠ pending, ✗ offline)

**Data retention for offline:**
- Active ITPs and checklists for current work phase
- Latest 2 revisions of construction drawings for active work areas
- Material specification reference for current work
- Contact list for project team
- Previous 7 days of field data (NCRs, RFIs, inspections)

### Step 5: Cross-Platform Data Format Conversion

**Translate data between desktop and mobile formats:**

**Format mappings:**
| Desktop Source | Mobile Format | Conversion Type |
|----------------|--------------|-----------------|
| DWG/DXF (AutoCAD) | Simplified vector + raster overlay | Heavy conversion |
| RVT (Revit) | IFC-based 3D viewer | Complex conversion |
| PDF drawings | PDF viewer with annotation | Direct pass-through |
| Excel BOQ | Structured data table | Format conversion |
| Word specs | HTML mobile document | Content conversion |
| Database records | JSON API payload | Format conversion |

### Step 6: Sync Verification and Integrity Check

**Verify data consistency after sync:**

**Integrity checks:**
- [ ] Record count matches between mobile and desktop
- [ ] Timestamp sequence logical (no records newer than sync time)
- [ ] No duplicate records created during sync
- [ ] File attachments transferred correctly (checksum verification)
- [ ] Cross-references intact (NCRs link to inspections, RFIs link to drawings)
- [ ] Permission restrictions maintained (user can only access authorized data)

## Success Criteria

- [ ] Sync completes without data loss for all priority tiers
- [ ] Conflicts detected and resolved (or flagged) within SLA
- [ ] Offline functionality maintained for all core mobile features
- [ ] Data format conversion preserves all critical information
- [ ] Post-sync integrity checks all pass
- [ ] Mobile user can clearly see sync status at all times
- [ ] Desktop user receives mobile data within defined SLA per priority tier

## Common Pitfalls

1. **Syncing Everything** — Full dataset syncs waste bandwidth. Always use differential sync when possible.
2. **Losing Offline Data** — If the app crashes during offline work, unsynced data must be preserved in local storage with transaction logs.
3. **Silent Conflicts** — Conflicts that overwrite data without notification are destructive. Always flag conflicts to the user.
4. **Forgetting Permissions** — When mobile data syncs to desktop, mobile user permissions may differ. Always verify recipient permissions before writing to desktop.
5. **Ignoring Sync Status** — Users who don't know their sync status may believe field data is safe when it's queued but not yet transferred. Always show clear sync indicators.

## Cross-References

### Related Skills
- `civil-mobile-field-ops` — Sync is the bridge between mobile and desktop
- `offline-procurement` — Offline sync patterns shared with procurement
- `mobile-procurement` — Mobile sync architecture shared with procurement
- `pre-task-assessment-readiness` — Assess network readiness before sync

### Related Agents
- `CE-MOBILE-001` (OpenClaw) — Mobile sync orchestration
- `CE-ORCH-001` (OpenClaw) — Cross-platform handoff coordination
- `CE-PROGRESS-001` (JS Swarm) — Progress data sync
- `CE-COLLAB-001` (JS Swarm) — Real-time bidirectional sync

## Example Usage

**Scenario:** Sync daily field data from drainage construction site with limited connectivity

1. **Field session (offline):** Inspector completed 3 ITPs (2 pass, 1 fail → 1 NCR generated), took 47 photos, logged progress "420m of 800m pipe installed (52.5%)", raised 2 RFIs
2. **Connectivity restored:** Cellular signal available at 12:00 PM
3. **Sync execution:**
   - P0: No safety reports — skipped
   - P1: 1 NCR + 2 RFIs synced in 18 seconds via cellular
   - P2: Progress update (52.5%) + 3 ITP results synced in 6 seconds
   - P3: 47 photos queued for wifi sync
   - P4: None pending
4. **Verification:** Desktop confirmed receipt — sync complete, 47 photos pending wifi
5. **Desktop push:** Updated drawing CE-0002 (drainage) Rev D queued for mobile download, 45MB — will sync at next wifi connection

## Performance Metrics

**Target Performance:**
- Sync reliability: 99.9% successful synchronization for P0-P2 data
- Conflict detection: 100% of concurrent edits detected and handled
- Offline functionality: 100% core features available without network
- Sync latency: <1 minute from connectivity restore to sync initiation
- Data integrity: Zero data loss incidents attributable to sync failure
- User awareness: 100% sync status visible to users at all times