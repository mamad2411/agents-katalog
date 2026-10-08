---
name: Create Jira Feature
description: Implementation guide for creating Jira features that organize multiple epics into strategic initiatives for SRVKP project
---

# Create Jira Feature

This skill provides implementation guidance for creating well-structured Jira features that organize related epics into strategic initiatives for the **SRVKP project**.

## When to Use This Skill

This skill is automatically invoked by:
- The `/jira:create feature` command
- The `create-epic` skill when auto-suggesting parent Features

## Prerequisites

- MCP Jira server configured and accessible, **or** `acli` installed and authenticated
- User has permissions to create issues in SRVKP project
- Understanding of the feature scope and strategic value

**Shared conventions** (safety rules, component table, confirmation flow, MCP→CLI fallback):
→ Read and follow [`../_common.md`](../_common.md) before proceeding.

**CLI reference:** [`../reference/cli-fallback.md`](../reference/cli-fallback.md)

## Project: SRVKP Only

This skill is **exclusively for SRVKP** (OpenShift Pipelines project).

---

## What is a Feature?

A feature is:
- A **strategic initiative** containing multiple related epics
- Spans **multiple quarters or releases**
- Addresses a **market problem** or **significant capability area**
- The **highest level** of work breakdown in the hierarchy

### Feature vs Epic vs Story

| Level | Scope | Duration | Contains | Example |
|-------|-------|----------|----------|---------|
| **Feature** | Strategic capability | Multiple quarters | Multiple Epics | "Tekton Chains Signing Enhancements" |
| **Epic** | Specific capability | One quarter | Multiple Stories | "Recursive Image Manifest signing" |
| **Story** | User functionality | One sprint | Tasks/Subtasks | "Sign multi-arch manifests automatically" |

### Feature Characteristics

Features should:
- Address **strategic objectives** or **market needs**
- Be **broader than an epic**, narrower than a product roadmap item
- Span **multiple quarters** (2-4 quarters typical)
- Contain **2-10 related epics**
- Have **measurable outcomes** tied to business value

---

## Feature Description Best Practices

### Clear Strategic Objective

The feature description should:
- State the strategic goal or market need
- Explain the business value
- Identify target users or market segments
- Define the overall capability area

**Good example:**
```
Expand Tekton Chains signing and attestation capabilities to support modern container image formats, multi-architecture workflows, and emerging supply chain security standards.

This feature addresses the growing need for comprehensive artifact signing in cloud-native CI/CD pipelines, enabling organizations to meet security compliance requirements and prevent supply chain attacks.

Target users: Platform engineers, Security teams, DevOps practitioners
Market need: Supply chain security compliance (SLSA, in-toto)
```

### Strategic Outcomes

Feature-level outcomes should be measurable and tied to business value:

**Format:**
```
h2. Strategic Outcomes

* <Business outcome 1>
* <Business outcome 2>
* <Business outcome 3>
```

**Example:**
```
h2. Strategic Outcomes

* Organizations can meet SLSA Level 3 requirements for all artifact types
* Multi-architecture image workflows fully supported without manual configuration
* Signing coverage increased to 100% of build artifacts (up from ~70%)
* Developer friction reduced - automatic signing without explicit configuration
```

### Timeline and Epics

Include expected timeline and epic breakdown:

**Example:**
```
h2. Timeline

* Target: Q3-Q4 2026
* Duration: 2-3 quarters
* Key milestones:
  * Q3 2026: Core multi-architecture support
  * Q4 2026: Advanced attestation features

h2. Planned Epics

* Recursive Image Manifest signing in Image Index
* Enhanced attestation formats for multi-arch
* Cross-registry signing support
* (Additional epics to be refined)
```

---

## Interactive Feature Collection Workflow

### 1. Feature Objective

**Prompt:** "What is the strategic objective of this feature? What market need or capability area does it address?"

**Helpful questions:**
- What business problem does this solve?
- What strategic capability will be delivered?
- Who are the target users or market segments?
- Why is this important now?

**Example response:**
```
Expand Tekton Chains signing to support modern container image formats like Image Index and multi-architecture workflows, addressing supply chain security compliance requirements.
```

### 2. Strategic Outcomes

**Prompt:** "What are the measurable strategic outcomes? How will success be measured?"

**Example response:**
```
- Organizations can meet SLSA Level 3 for all artifact types
- Multi-arch workflows fully supported
- Signing coverage reaches 100% of build artifacts
- Reduced manual configuration overhead
```

### 3. Planned Epics

**Prompt:** "What epics are expected under this feature? (Initial list - can evolve)"

**Example response:**
```
- Recursive Image Manifest signing
- Enhanced multi-arch attestation
- Cross-registry signing support
- Signature verification improvements
```

### 4. Timeline

**Prompt:** "What is the target timeline for this feature?"

**Example responses:**
- "Q3-Q4 2026"
- "2-3 quarters starting Q3 2026"
- "Must complete by end of 2026"

---

## Field Validation

Before submitting the feature, validate:

### Required Fields
- ✅ Summary is clear and describes the strategic capability
- ✅ Description includes strategic objective
- ✅ Strategic outcomes present
- ✅ Timeline specified
- ✅ Component is specified (if required by project)

### Feature Quality
- ✅ Scope is broader than an epic
- ✅ Spans multiple quarters
- ✅ Contains or will contain multiple epics
- ✅ Has measurable strategic outcomes
- ✅ Tied to business value

### Security
- ✅ No credentials, API keys, or secrets in any field

---

## Creation Strategy: MCP First, CLI Fallback

Follow the **MCP → CLI Fallback Decision Tree** in [`../_common.md`](../_common.md).

### CLI Feature Creation

```bash
acli jira workitem create \
  --project "SRVKP" \
  --type "Feature" \
  --summary "Tekton Chains Signing Enhancements" \
  --description "$(cat <<'EOF'
Expand Tekton Chains signing capabilities to support modern container image formats and multi-architecture workflows.

h2. Strategic Outcomes

* SLSA Level 3 compliance for all artifact types
* Multi-arch workflows fully supported
* 100% signing coverage without manual configuration

h2. Target Users

* Platform engineers building multi-arch images
* Security teams implementing supply chain security

h2. Timeline

* Target: Q3-Q4 2026
* Duration: 2-3 quarters
EOF
)" \
  --label "ai-generated-jira" \
  --json
```

**Note:** Use `$(cat <<'EOF' ... EOF)` for inline multi-line descriptions with wiki markup. No temp files needed.

### Feature Template Format

```
{Strategic objective paragraph}

h2. Strategic Outcomes

* {Outcome 1}
* {Outcome 2}
* {Outcome 3}

h2. Target Users

* {User segment 1}
* {User segment 2}

h2. Market Need

{Why this feature area matters strategically}

h2. Timeline

* Target: {quarters/year}
* Duration: {estimated time}
* Key milestones: {major deliverables}

h2. Planned Epics

* {Epic 1 - brief description}
* {Epic 2 - brief description}
* (To be refined as feature develops)

h2. Success Metrics

* {Metric 1}
* {Metric 2}
```

---

## Examples

### Example 1: Auto-Generated Feature from Epic

**Context:** User creating epic "Recursive Image Manifest signing in Tekton Chains"

**Auto-generated Feature:**
```
Summary: Tekton Chains Signing Enhancements

Description:
Expand Tekton Chains signing and attestation capabilities to support modern container image formats, multi-architecture workflows, and emerging supply chain security standards.

This feature addresses the growing need for comprehensive artifact signing in cloud-native CI/CD pipelines, enabling organizations to meet security compliance requirements.

h2. Strategic Outcomes

* Organizations can meet SLSA Level 3 requirements for all artifact types
* Multi-architecture image workflows fully supported without manual configuration
* Signing coverage increased to 100% of build artifacts
* Developer experience improved with automatic signing

h2. Target Users

* Platform engineers building multi-arch images
* Security teams implementing supply chain security
* DevOps practitioners managing CI/CD pipelines

h2. Market Need

Modern container deployments require multi-architecture support (amd64, arm64, s390x, ppc64le). Current signing approaches require manual configuration per architecture, creating friction and potential security gaps.

h2. Timeline

* Target: Q3-Q4 2026
* Duration: 2-3 quarters
* Key milestones:
  * Q3 2026: Core recursive signing support
  * Q4 2026: Advanced attestation and verification

h2. Planned Epics

* Recursive Image Manifest signing in Image Index
* Enhanced attestation formats for multi-arch artifacts
* Cross-registry manifest signing support
* (Additional epics to be refined)

h2. Success Metrics

* 100% signing coverage for multi-arch builds
* Zero manual pullspec configuration required
* SLSA Level 3 compliance achieved
* Adoption by 80%+ of multi-arch pipelines
```

**Component:** Tekton Chains

---

### Example 2: Manual Feature Creation

**Input:**
```bash
/jira:create feature "Enhanced Tekton Results storage and performance"
```

**Interactive prompts:**
```
What is the strategic objective of this feature?
> Improve Tekton Results storage efficiency and query performance to support large-scale pipeline deployments with millions of results

Strategic outcomes? (measurable)
> - Support 10M+ pipeline results per cluster
> - Query response times under 100ms for 95th percentile
> - Storage costs reduced by 60%
> - Retention policies configurable per namespace

Planned epics?
> - Database optimization and partitioning
> - Result pruning and archival
> - Query performance enhancements
> - Storage backend flexibility

Timeline?
> Q2-Q3 2026, estimated 2 quarters
```

**Result:**
- Feature created with complete strategic context
- Ready for child epics

---

## Best Practices Summary

1. **Strategic focus:** Features address market needs, not just technical improvements
2. **Business value:** Clearly articulate why this matters
3. **Measurable outcomes:** Define success metrics
4. **Right size:** 2-4 quarters, contains 2-10 epics
5. **Timeline:** Specify target quarters/year
6. **Planned epics:** List expected epics (can evolve)
7. **Target users:** Identify who benefits

## Anti-Patterns to Avoid

❌ **Feature is actually an epic**
```
"Add recursive signing to Chains" (1-2 sprints)
```
✅ Too small, create as Epic instead

❌ **Feature too broad**
```
"Complete Tekton platform redesign" (multi-year, 50+ epics)
```
✅ Too large, break into multiple Features

❌ **No business value**
```
"Technical improvements to Chains"
```
✅ Be specific: What business value? What outcomes?

❌ **Implementation details**
```
"Refactor Chains to use new storage backend"
```
✅ Focus on user value, not implementation

---

## Workflow Summary

Follow the **Mandatory Confirmation Flow** and **MCP → CLI Fallback Decision Tree** in
[`../_common.md`](../_common.md). The preview label for this type is `PREVIEW: SRVKP Feature`.

1. ✅ Parse command arguments
2. 🔍 Search for duplicate features (keyword matching)
3. 💬 Interactively collect strategic objective
4. 💬 Collect strategic outcomes and timeline
5. 💬 Collect planned epics
6. 🔒 Scan for sensitive data
7. ✅ Validate feature size and quality
8. 📝 Format description with Jira markup
9. 📋 Show preview and get confirmation
10. ✅ **Create the feature** (only if confirmed) — MCP first; same payload via `acli` on fallback
11. 📤 Return issue key and URL

## See Also

- `/jira:create epic` - Creating epics under features
- `create-epic` skill - Epic creation (enhanced with feature discovery)
