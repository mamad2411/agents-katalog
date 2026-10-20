---
agent: design
description: "Generate Enterprise Landing Zone architecture diagrams and ADRs"
---

# Step 3: Design

Act as the Artisan (🎨). Generate architecture diagrams and Architecture Decision
Records (ADRs) for the Enterprise Landing Zone based on the architecture assessment.

## Required Input

- `agent-output/{customer}/02-architecture-assessment.md` — required
- `agent-output/{customer}/01-requirements.md` — optional context
- `agent-output/{customer}/04-governance-constraints.md` — optional context

## Skill Routing

1. Read `.github/skills/azure-diagrams/SKILL.md` first.
2. Follow its routing decision before loading `drawio`, `python-diagrams`, or `mermaid`.
3. Read `.github/skills/azure-adr/SKILL.md` before writing ADRs.

## Process

1. Read `agent-output/{customer}/02-architecture-assessment.md`.
2. Determine the required Step 3 diagram set and any ADRs justified by approved decisions.
3. Generate the canonical Step 3 outputs below.
4. Record design decisions: `alz-recall decide {customer} --key diagram_type --value {drawio|python|mermaid} --json`.

## Diagrams to Generate

- Management group hierarchy using customer `{prefix}` and platform/app LZ subscription placement
- Hub-spoke network topology with CIDRs, peering, Bastion, optional firewall
- Security, governance, and monitoring architecture
- Full ALZ estate overview showing all 4 platform LZs

## Canonical Output Contract

Produce in `agent-output/{customer}/`:
- `03-design-summary.md` — **required** completion artifact and Step 7 handoff manifest

Produce in `agent-output/{customer}/diagrams/`:
- `03-design-management-group-hierarchy.drawio`
- `03-design-management-group-hierarchy.png`
- `03-design-hub-spoke-network-topology.drawio`
- `03-design-hub-spoke-network-topology.png`
- `03-design-security-governance-monitoring.drawio`
- `03-design-security-governance-monitoring.png`
- `03-design-estate-overview.drawio`
- `03-design-estate-overview.png`

If an inline markdown diagram is required, use `03-design-<topic>.md`.

Produce ADRs in `agent-output/{customer}/adr/`:
- `03-design-adr-{NNN}-{slug}.md`

## Summary Contract

`03-design-summary.md` must list the exact relative paths for every generated
diagram and ADR so Step 7 can consume Step 3 outputs without guessing names.
Include:

- diagrams table: name, purpose, formats, relative paths
- ADR table: ADR ID, title, status, relative path
- design notes and assumptions
- source architecture assessment reference

If no ADRs are generated, say so explicitly in the summary.
