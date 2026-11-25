---
title: Mobile Procurement Operations
description: Consolidated mobile procurement skill combining voice ordering, GPS approvals, offline operations, field procurement, and site-based procurement workflows
version: 1.0
frequency_percent: 40.0
success_rate_percent: 85.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/01900_procurement/procurement-mobile
gigabrain_tags: disciplines, 01900_procurement, mobile-procurement, voice-ordering, gps-approvals, offline-procurement, field-procurement, site-procurement
openstinger_context: mobile-procurement-workflow, field-ordering, site-approval
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/01900_procurement/agent-data/prompts/01900_PROCUREMENT_ORDER_PROMPT.md
  - docs_construct_ai/disciplines/01900_procurement/agent-data/domain-knowledge/1900_GLOSSARY.MD
  - docs_construct_ai/disciplines/01900_procurement_mobile/workflow_docs/01900_PROCUREMENT_MOBILE_WORKFLOW.MD
related_skills:
  - pre-task-assessment-readiness
  - procurement-order-management
  - voice-command-integration
  - gps-approval-configuration
  - offline-procurement
---

# Mobile Procurement Operations

## Overview

Consolidated mobile procurement workflow combining voice-powered ordering, GPS-enabled approvals, offline-first operations, field procurement, and site-based material management. Enables complete procurement functionality from mobile devices in construction sites and supply chain environments.

**Announce at start:** "I'm using the mobile-procurement skill to execute a mobile procurement operation."

## When to Use This Skill

**Trigger Conditions:**
- User initiates procurement from mobile device at construction site
- Voice ordering required for hands-free operation
- GPS-enabled approval with location verification needed
- Offline operation required (remote site, no connectivity)
- Field procurement with urgency classification (emergency, urgent, standard)
- Site-based material receipt and quality inspection

**Prerequisites:**
- Mobile app installed and configured
- User authenticated and authorized
- Project context available (project, WBS, site location)
- For offline: initial data cached before going offline

## Step-by-Step Procedure

### Step 1: Mobile Procurement Initiation

Determine the procurement initiation method:

| Method | Use Case | Requirements |
|--------|----------|--------------|
| Voice Command | Hands-free ordering at site | Microphone, voice recognition, noisy-environment support |
| Form Entry | Standard mobile order via app | Mobile device, internet or offline mode |
| Photo-Based Ordering | Ordering from photo of needed item | Camera, image recognition for item identification |
| QR Code Scan | Reorder from existing item/PO | Camera, QR code scanner, item database |

### Step 2: Voice-Powered Order Creation (If Voice Initiated)

Process voice command with context-aware recognition:

1. **Capture Voice Command**: "Need 20 bags of cement at Zone 3, urgent"
2. **AI Parse**: Quantity: 20 bags, Item: cement, Location: Zone 3, Priority: urgent
3. **Context Enrichment**: Verify cement exists in catalog, confirm Zone 3 is valid delivery location
4. **Real-Time Validation**: Budget check, lead-time, urgent prioritization
5. **Voice Feedback**: "20 bags cement, Zone 3, urgent. Estimated R4,000. Supplier: CemCo Gold tier. Proceed?"
6. **User Confirms**: "Yes" → Continue to approval

### Step 3: Field Procurement with Urgency Classification

Apply urgency classification to procurement workflow:

| Urgency Level | Description | Approval Time Target | Workflow Adjustments |
|---------------|-------------|---------------------|---------------------|
| Emergency | Materials required within 24 hours for safety, critical path | <4 hours | Expedited routing, retroactive documentation, emergency supplier matching |
| Urgent | Required within 48-72 hours | <12 hours | Standard routing with priority flag, preferred supplier only |
| Standard | Required within 1-4 weeks | <48 hours | Full workflow with standard approval |

### Step 4: GPS-Enabled Approval Routing

Configure and execute location-based approval:

1. **Verify Approver Location**: GPS coordinates confirmed within geofence of site or office
2. **Biometric Authentication**: Fingerprint or Face ID verification of approver identity
3. **GPS-Embedded Signature**: Sign-off with GPS coordinates, timestamp, device ID
4. **Location-Based Authority**: Determine approver authority based on proximity to project
5. **Audit Trail**: Complete location history from approval request to decision

### Step 5: Offline-First Operations

If network connectivity is unavailable:

1. **Switch to Offline Mode**: App detects no connectivity → offline mode with indicator
2. **Use Cached Data**: Order forms, supplier lists, templates available from local cache
3. **Create Order Locally**: Complete all order fields using offline forms
4. **Queue for Sync**: Order queued with HIGH priority for next connectivity
5. **Sync on Reconnect**: When network returns, queued orders synced with server
6. **Conflict Resolution**: If order modified online, user notified to re-apply changes

### Step 6: Site-Based Supplier Coordination

For site-based procurement:

1. **Preferred Site Supplier Matching**: Match order to preferred site supplier (if available)
2. **Real-Time Availability Check**: Check supplier current stock for emergency items
3. **Expedited Ordering**: If item available, order bypasses standard approval → expedited routing
4. **Delivery Confirmation**: Supplier confirms delivery time, GPS tracking initiated
5. **Site Receipt**: Delivery arrives at site gate → GRN created → quality check initiated

### Step 7: Automated Receipt and Quality Verification at Site

Process delivery receipt on mobile device at construction site:

1. **Delivery Notification**: App notifies receiver of arriving delivery
2. **Quantity Verification**: Receiver confirms delivered quantity matches PO
3. **Quality Inspection**: Receiver inspects materials, records any defects or damage
4. **Photo Documentation**: Photos taken for delivery proof and quality record
5. **GRN Finalized**: GRN created and signed digitally with GPS coordinates
6. **Sync to Server**: GRN synced to procurement and finance systems

## Success Criteria

- [ ] Voice command captured, parsed, and understood correctly
- [ ] Field urgency classification applied correctly (Emergency/Urgent/Standard)
- [ ] GPS-enabled approval completed with verified location and biometric authentication
- [ ] Offline operations complete with successful synchronization on reconnect
- [ ] Site-based supplier coordination functional with real-time availability check
- [ ] Automated receipt and quality verification completed at site with photo documentation
- [ ] All procurement data synced to procurement and finance systems

## Common Pitfalls

1. **Voice Recognition Failure in Noise** — Construction sites are noisy. Ensure noise-cancelling microphone or fallback to text input when voice recognition fails.
2. **GPS Accuracy Issues** — GPS accuracy can be poor in canyons, near tall buildings, or underground. Use multiple positioning sources (GPS, WiFi, cellular) for better accuracy.
3. **Offline Data Staleness** — Cached data only reflects the last sync. If offline for an extended period, check budget and supplier data before finalizing orders.
4. **Quality Inspection Rushed** — At busy construction sites, quality inspection may be rushed. Don't skip quality checks even on urgent deliveries — poor quality materials cause more costly problems later.
5. **Photo Documentation Missing** — Photo documentation is critical for delivery proof and quality records. Always capture photos at delivery and inspection.

## Cross-References

### Related Skills
- `voice-command-integration` — Voice-powered ordering
- `gps-approval-configuration` — GPS-enabled approval routing
- `offline-procurement` — Offline-first operations
- `procurement-order-management` — Core order creation workflow
- `supply-chain-integration` — Supplier coordination and delivery tracking
- `pre-task-assessment-readiness` — Complete assessment before mobile procurement deployment

### Related Agents
- `Mobile Workflow Designer` (DomainForge) — Mobile workflow architecture
- `Mobile Testing Specialist` (DomainForge) — Mobile feature testing
- `Mobile API Integration Specialist` (InfraForge) — Mobile API infrastructure
- `Supply Chain Integration Specialist` (InfraForge) — Supplier coordination

## Example Usage

**Scenario:** Emergency rebar order at construction site with offline approval

1. **Initiation:** Site foreman at Zone B needs emergency rebar for concrete pour tomorrow. Voice command: "Emergency 200 rebar 16mm at Zone B, needed tomorrow 6am"
2. **Voice Parsing:** Item: rebar 16mm, Quantity: 200, Location: Zone B, Required: Tomorrow 6am, Urgency: Emergency
3. **Validation:** Rebar in catalog (yes), Zone B valid delivery point (yes), Budget check — within WBS 01900-STR budget (yes), Lead-time — standard 1 week (too long), Emergency supplier SteelCo has 500 pieces in stock (yes, local yard 2km from site)
4. **Approval:** GPS verification — foreman at Zone B, PM at site office (confirmed via GPS, biometric Face ID), approved in 2 minutes
5. **Order:** PO created and sent to SteelCo → confirmation in 15 minutes → delivery confirmed by 2am
6. **Receipt:** Materials delivered, GRN created with photo evidence, quality inspected, pour proceeds at 6am
7. **Result:** Emergency procurement completed, full audit trail, site notified