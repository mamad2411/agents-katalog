---
title: Offline Procurement Operations
description: Implement offline-first procurement architecture with intelligent queuing, background synchronization, conflict resolution, and data integrity verification
version: 1.0
frequency_percent: 35.0
success_rate_percent: 82.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/offline-procurement
gigabrain_tags: disciplines, 01900_procurement, offline-procurement, offline-sync, conflict-resolution, intelligent-queuing, background-sync
openstinger_context: offline-procurement, disconnected-operations, mobile-offline
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/01900_procurement/agent-data/prompts/01900_PROCUREMENT_ORDER_PROMPT.md
  - docs_construct_ai/disciplines/01900_procurement/agent-data/domain-knowledge/1900_GLOSSARY.MD
related_skills:
  - pre-task-assessment-readiness
  - procurement-order-management
  - approval-routing
  - gps-approval-configuration
---

# Offline Procurement Operations

## Overview

Implement offline-first procurement architecture with intelligent caching, prioritized data storage, queuing, background synchronization, conflict resolution for concurrent changes, and data integrity verification. Enables complete procurement functionality without network connectivity.

**Announce at start:** "I'm using the offline-procurement skill to configure or execute offline procurement operations."

## When to Use This Skill

**Trigger Conditions:**
- User initiates procurement actions in areas without network connectivity (remote sites, underground, shielded areas)
- Configuring offline-first architecture for the procurement system
- Setting up intelligent queuing and background synchronization
- Resolving conflicts between offline changes and online data
- Verifying data integrity after synchronization

**Prerequisites:**
- Offline-first app installed on device
- Initial data cached before going offline
- Local storage available for queuing offline actions

## Step-by-Step Procedure

### Step 1: Offline Detection and Adaptation

Detect network disconnection and adapt procurement workflows:

| Detection Method | Adaptation Action |
|-----------------|-------------------|
| No network response to API call | Switch to offline mode, display offline indicator |
| Network quality degraded | Queue non-critical requests, proceed with critical offline |
| User manually enables offline mode | Force offline mode with clear status indicator |

### Step 2: Offline-First Data Caching and Prioritization

Cache critical procurement data for offline access, prioritized by importance:

| Priority | Data Category | Cached Fields | Reason for Priority |
|----------|--------------|---------------|---------------------|
| P0 (Critical) | Project/WBS Data | Project name, WBS codes, cost codes, budget per WBS | Required for order creation and validation |
| P0 (Critical) | Supplier Data | Supplier name, code, tier, status, contact, approved items | Required for supplier selection and matching |
| P0 (Critical) | Template Data | Template name, fields, validation rules, required sections | Required for order form generation |
| P1 (High) | Catalog Data | Item code, description, specification, unit price | Required for standard item selection |
| P1 (High) | Approval Rules | Thresholds, approver assignments, routing types | Required for approval routing configuration |
| P2 (Medium) | Order History | Recent orders, status, SO acknowledgments | Required for reference and duplicate checking |
| P3 (Low) | Analytics Data | Dashboards, KPIs, trends | Not critical offline, sync on reconnect |

### Step 3: Intelligent Queuing and Background Synchronization

Queue offline actions for processing when connectivity is restored:

| Action Type | Queue Priority | Sync Timing | Conflict Risk |
|-------------|---------------|-------------|---------------|
| Order Creation/Modification | HIGH | Immediately on reconnect | HIGH (order may be modified by another user) |
| Approval Actions | HIGH | Immediately on reconnect | MEDIUM (approval authority must be verified) |
| SO Acknowledgment | MEDIUM | Within 5 minutes of reconnect | LOW |
| GRN Recording | HIGH | Immediately on reconnect | HIGH (GRN may affect payment processing) |
| Supplier Rating/Feedback | LOW | Background sync (within 30 minutes) | LOW |
| Template Updates | LOW | Background sync (within 30 minutes) | MEDIUM |

### Step 4: Conflict Resolution for Concurrent Changes

Resolve conflicts when offline changes conflict with online data:

| Conflict Type | Resolution Strategy |
|---------------|---------------------|
| Order modified offline and another user modified the same order online | Server wins — offline changes are discarded user notified and asked to re-apply |
| GRN recorded offline, but order already closed online | Conflict flagged — offline GRN held for manual review by procurement team |
| Supplier tier changed online, but offline change used old tier | Server wins — offline change reconciled with current supplier tier |
| Budget reduced online, offline order would exceed new budget | Conflict flagged — order held for approval until budget increased or order value reduced |
| Template updated online, offline form used old version | Conflict resolved gracefully — offline changes preserved, new template version applied on sync with field mapping |

### Step 5: Data Integrity Verification

Verify data integrity after offline synchronization:

| Integrity Check | Method | Expected Result |
|----------------|--------|-----------------|
| Record Count Match | Count of offline-created orders vs. online records after sync | Counts match — all orders synced successfully |
| Data Field Completeness | Verify all fields of synced records populated | No null or empty fields |
| Referential Integrity | Verify all WBS codes, supplier codes, and template IDs valid | All references resolve |
| Sequence Number Continuity | Verify order numbers, GRN numbers, and SO numbers sequential | Gaps flagged and investigated |
| Audit Trail Completeness | Verify all approvals, changes, and actions recorded in audit log | Audit log matches actions |

### Step 6: Offline Approval Processing

Process approvals when approver is offline:

1. Capture approver name, decision, timestamp, and GPS coordinates
2. Store approval record locally with cryptographic signature
3. Verify GPS coordinates match project site or office location
4. Queue approval for synchronization when connectivity restored
5. After sync, notify order owner of approval decision

### Step 7: Offline Synchronization and Reconnection

When connectivity is restored:

1. **Detect Connectivity**: Monitor for network restoration
2. **Prioritize Sync Queue**: Process HIGH priority queues first
3. **Execute Sync**: Send queued actions to server
4. **Resolve Conflicts**: Apply resolution strategies for conflicts
5. **Notify User**: Inform user of sync results and any actions requiring attention
6. **Cache Update**: Update local cache with latest server data
7. **Switch to Online Mode**: Resume normal online operations if connectivity is stable

## Success Criteria

- [ ] Offline detection functioning reliably and adaptation triggers correctly
- [ ] Critical data (P0/P1) available offline for procurement operations
- [ ] Offline actions queued correctly with appropriate priority
- [ ] Background synchronization processes all queued actions on reconnect
- [ ] Conflict resolution handles all 5 conflict types correctly
- [ ] Data integrity verification passes all 5 checks after synchronization
- [ ] Offline approvals processed and synced with complete audit trail
- [ ] User notification provided for all sync issues requiring manual intervention

## Common Pitfalls

1. **Stale Data** — Offline data is only as fresh as the last cache. If going offline for an extended period, critical data (budget, supplier tiers, approval authorities) may be outdated. Warn users before they use potentially stale data.
2. **Lost Offline Actions** — If the device crashes or the app is killed before queued actions are synced, the actions are lost. Ensure queued actions are persisted to durable local storage and survive app restarts.
3. **Conflict Storm** — If many users were making offline changes to the same records, synchronization will trigger many conflicts. Prioritize resolution and avoid creating conflicts that cascade.
4. **Data Size Limits** — Caching too much data for offline use can cause mobile storage exhaustion. Keep cache under 500MB — prioritize P0/P1 data, exclude P3 analytics.
5. **Security Exposure** — Offline data is stored on the device and may be accessible if the device is lost or stolen. Encrypt all cached procurement data and require device PIN/biometric authentication for app access.

## Cross-References

### Related Skills
- `procurement-order-management` — Offline orders use the same workflow with local processing
- `approval-routing` — Offline approvals queued and synced with routing rules
- `gps-approval-configuration` — Offline approvals capture GPS coordinates locally
- `voice-command-integration` — Voice orders can be created offline and queued for sync

### Related Agents
- `Mobile Workflow Designer` (DomainForge) — Offline workflow architecture and UX design
- `Mobile Testing Specialist` (DomainForge) — Offline functionality and synchronization testing
- `Mobile API Integration Specialist` (InfraForge) — Offline sync API and conflict resolution

## Example Usage

**Scenario:** Field worker creates emergency order and records GRN while underground with no connectivity

1. **Offline Detection:** App detects no connectivity → switches to offline mode with indicator
2. **Data Available:** Critical data cached — project ABC, WBS codes, supplier list, templates
3. **Order Creation:** User creates WO for emergency excavation using offline form — order queued as HIGH priority
4. **GRN Recording:** User records GRN for materials received — GRN queued as HIGH priority
5. **Reconnection:** When user returns to surface and connectivity is restored, sync queue is processed — order created, GRN recorded, both matched to online records
6. **User Notification:** App notifies "2 actions synced successfully: WO-2026-0912 created, GRN-2026-0445 recorded"