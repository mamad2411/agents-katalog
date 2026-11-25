---
name: adr-governance-orchestrator
description: "Orchestrates the complete lifecycle of Architectural Decision Records (ADRs). Manages the end-to-end process from initial discovery and requirement analysis to drafting (using templates like MADR, Nygard, Y-Statement), enforcing governance via gatekeeping, and managing lifecycle states (Proposed, Accepted, Superseded). Ensures every decision is properly linked, indexed, and synced to the project memory. Keywords: adr-governance, adr-management, decision-log, adr-lifecycle, adr-audit, adr-orchestrator, architecture-decisions."
version: 1
created: "2024-05-22"
updated: "2024-05-22"
---

# ADR Governance Orchestrator - Full Lifecycle Management

This skill acts as the central command for all Architectural Decision Record (ADR) operations. It automates the transition from a vague "we need to make a choice" to a formally recorded, gatekept, and indexed architectural decision.

## When to Use
Use this skill whenever you need to:
- Start a new ADR process from scratch.
- Audit existing ADRs to find gaps or outdated records.
- Update an existing ADR with new information.
- Supersede an old decision with a new one.
- Perform a full "Audit" of the architectural decision log.

## The Orchestrated Workflow
When invoked, this skill follows a strict sequential pipeline:

### Phase 0: Infrastructure Verification
1. **Directory Check**: Verify if `docs/adr` exists.
2. **Auto-Provisioning**: If the directory is missing, automatically invoke `install-adr-gatekeeper` to initialize the infrastructure, set up rules, and create the initial index.
3. **Continuity**: Once provisioned, proceed to the standard discovery and analysis phases.

### Phase 1: Discovery & Analysis
1. **Audit Existing State**: Call `adr-discovery` to identify existing ADRs and detect potential overlaps or conflicts.
2. **Requirement Gathering**: Analyze the user's request to determine:
   - The **Context** (Why are we doing this?)
   - The **Drivers** (Performance, Cost, Security, etc.)
   - The **Alternatives** (What else did we consider?)
   - The **Consequences** (What are the trade-offs?)

### Phase 2: Drafting & Authoring
3. **Template Selection**: Based on the analysis, select the appropriate template (MADR, Nygard, or Y-Statement).
4. **Content Generation**: Invoke `adr-authoring` to generate the draft.
5. **Refinement**: Review the draft with the user, ensuring it captures the "Knowledge Delta" (expert-only trade-offs).

### Phase 3: Gatekeeping & Validation
6. **Governance Check**: Pass the draft to `adr-gatekeeper`. This ensures the ADR is not just "good" but "compliant" with project standards (e.g., no redundant content, proper status, and clear consequences).
7. **Correction**: If the gatekeeper identifies issues, loop back to the authoring phase to address them.

### Phase 4: Lifecycle & Integration
8. **Finalization**: Once approved, invoke `adr-lifecycle-management` to:
   - Set the correct status (Accepted, Proposed, etc.).
   - Update the master index (README.md) in `docs/adr/`.
   - Handle superseding links (if replacing an old ADR).
9. **Memory Sync**: Trigger the local memory capture to ensure the new record is indexed in the project's long-term memory (OKF/ChromaDB).

## Freedom Calibration & Constraints
- **Constraint Level: High**
  - **Rigidity**: The sequence of the pipeline is mandatory. You MUST NOT skip the Gatekeeping phase or the Index update.
  - **Freedom**: The specific content of the ADR is flexible, provided it satisfies the "Consequences" requirement.

## Critical Anti-Patterns (NEVER List)
| Anti-Pattern | Description | Alternative / Solution |
| :--- | :--- | :--- |
| **NEVER** skip the Gatekeeper | Bypassing the check leads to inconsistent records and "token waste." | Always run the gatekeeper check before finalization. |
| **NEVER** delete an ADR | Even if a decision is bad, the record of that decision is vital. | Mark as "Deprecated" or "Superseded." |
| **NEVER** lose the link | Failing to link a new ADR to the one it supersedes breaks the decision chain. | Always use bidirectional linking in the lifecycle phase. |

## Verification
1. A new ADR is created in the correct directory with a unique ID.
2. The ADR passes the `adr-gatekeeper` validation.
3. The master index in `docs/adr/README.md` is updated.
4. The decision is captured in the project's memory system.
