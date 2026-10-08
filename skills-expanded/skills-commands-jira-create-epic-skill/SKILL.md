---
name: Create Jira Epic
description: Implementation guide for creating Jira epics with proper scope and parent linking in SRVKP project
---

# Create Jira Epic

This skill provides implementation guidance for creating well-structured Jira epics that organize related stories and tasks into cohesive bodies of work for the **SRVKP project**.

## When to Use This Skill

This skill is automatically invoked by the `/jira:create epic` command to guide the epic creation process.

## Prerequisites

- MCP Jira server configured and accessible, **or** `acli` installed and authenticated
- User has permissions to create issues in SRVKP project
- Understanding of the epic scope and related work

**Shared conventions** (safety rules, component table, confirmation flow, MCP→CLI fallback):
→ Read and follow [`../_common.md`](../_common.md) before proceeding.

**CLI reference:** [`../reference/cli-fallback.md`](../reference/cli-fallback.md)

## Project: SRVKP Only

This skill is **exclusively for SRVKP** (OpenShift Pipelines project).
Component auto-suggestion keywords and the full component list are in [`../_common.md`](../_common.md).

---

## PHASE 0A: DUPLICATE DETECTION

Before collecting epic details, search for similar existing epics to prevent duplicates.

### Keyword Extraction

Extract significant keywords from epic summary (ignores common words like "the", "and", "in", "for", "to", "add", "create", "enable").

**Example:**
```
Input: "Recursive Image Manifest signing in Tekton Chains"
Keywords: ["recursive", "image", "manifest", "signing", "tekton", "chains"]
```

### Search SRVKP for Similar Epics

Use JQL to search for epics containing keywords:
```bash
acli jira workitem search \
  --jql "project = SRVKP AND issuetype = Epic AND (summary ~ 'keyword1' OR ...)" \
  --fields "key,summary,status"
```

### Duplicate Threshold

Flag as potential duplicate if **3 or more keywords** match.

### User Prompt

```
Found similar epics in SRVKP:

1. SRVKP-11620: Support Pipelines in Pipelines in Tekton Chains
   Matched: chains, tekton, pipelines (3/6 keywords)
   Status: New
   
2. SRVKP-11142: Promote SLSAv1.0 offering of Chains format to beta
   Matched: chains, signing, format (3/6 keywords)
   Status: New

Options:
- Type '1' or '2': View that epic and stop creation
- Type 'none': Proceed with creating new epic
```

If user views existing epic, do NOT create new one.

---

## PHASE 0B: PARENT FEATURE DISCOVERY

Search for appropriate parent Feature using keywords.

### Search for Related Features

```bash
acli jira workitem search \
  --jql "project = SRVKP AND issuetype = Feature AND (summary ~ 'chains' OR ...)" \
  --fields "key,summary,status"
```

### User Prompt

```
Searching for parent Features for this epic...

Found potential parent Features:

1. SRVKP-8485: Enable SLSA v1.0 in Konflux chains
   Status: To Do
   
2. SRVKP-9645: Model Signing capability in Tekton Chains
   Status: New

Link this epic to a parent Feature?
- Type '1' or '2': Select this Feature as parent
- Type 'none': Create standalone epic (no parent)
- Type 'create': Create new parent Feature
```

---

## PHASE 0C: AUTO-SUGGEST FEATURE

If user chooses 'create', generate parent Feature suggestion.

### Feature Name Generation

**Step 1:** Identify component from epic summary
```
"Tekton Chains" (from "Chains")
"Tekton Pipelines" (from "pipeline", "task")
"Pipeline as Code" (from "pac", "pipelinesascode")
```

**Step 2:** Identify capability area from keywords
```
Keywords include "signing" → "Signing Enhancements"
Keywords include "performance" → "Performance Optimization"
Keywords include "security" → "Security Improvements"
```

**Step 3:** Combine
```
Feature Name: "{Component} {Capability Area}"
Example: "Tekton Chains Signing Enhancements"
```

### Feature Preview

```
┌──────────────────────────────────────────────────┐
│ Suggested Parent Feature                         │
├──────────────────────────────────────────────────┤
│ Summary: Tekton Chains Signing Enhancements      │
│ Component: Tekton Chains                         │
├──────────────────────────────────────────────────┤
│ Objective:                                        │
│ Expand Tekton Chains signing capabilities to     │
│ support modern container image formats and       │
│ multi-architecture workflows.                     │
│                                                   │
│ Strategic Outcomes:                               │
│ • SLSA Level 3 compliance for all artifacts      │
│ • Multi-arch workflows fully supported           │
│ • 100% signing coverage                          │
│                                                   │
│ Timeline: Q3-Q4 2026                             │
│                                                   │
│ Will contain:                                     │
│ • This epic: {epic summary}                      │
│ • Future related epics                           │
└──────────────────────────────────────────────────┘

Create this Feature? (yes/no/modify)
- yes: Create Feature, then create epic under it
- no: Create epic standalone
- modify: Edit Feature details first
```

### Create Feature

If approved, invoke `create-feature` skill to create the Feature, then link epic to it.

---

## What is an Epic?

An agile epic is:
- A **body of work** that can be broken down into specific items (stories/tasks)
- Based on the needs/requests of customers or end-users
- An important practice for agile and DevOps teams
- A tool to **manage work** at a higher level than individual stories

### Epic Characteristics

Epics should:
- Be **more narrow** than a market problem or feature
- Be **broader** than a user story
- **Fit inside a time box** (quarter/release)
- Stories within the epic should **fit inside a sprint**
- Include **acceptance criteria** that define when the epic is done

### Epic vs Feature vs Story

| Level | Scope | Duration | Example |
|-------|-------|----------|---------|
| Feature | Strategic objective, market problem | Multiple releases | "Advanced cluster observability" |
| Epic | Specific capability, narrower than feature | One quarter/release | "Multi-cluster metrics aggregation" |
| Story | Single user-facing functionality | One sprint | "As an SRE, I want to view metrics from multiple clusters in one dashboard" |

## Epic Name Field Requirement

**IMPORTANT:** Many Jira configurations require the **epic name** field to be set.

- **Epic Name** = **Summary** (should be identical)
- This is a separate required field in addition to the summary field
- If epic name is missing, epic creation will fail

**MCP Tool Handling:**
- Some projects auto-populate epic name from summary
- Some require explicit epic name field
- Always set epic name = summary to ensure compatibility

## Epic Description Best Practices

### Clear Objective

The epic description should:
- State the overall goal or objective
- Explain the value or benefit
- Identify the target users or stakeholders
- Define the scope (what's included and excluded)

**Good example:**
```
Enable administrators to manage multiple hosted control plane clusters from a single observability dashboard.

This epic delivers unified metrics aggregation, alerting, and visualization across clusters, reducing the operational overhead of managing multiple cluster environments.

Target users: SREs, Platform administrators
```

### Acceptance Criteria for Epics

Epic-level acceptance criteria define when the epic is complete:

**Format:**
```
h2. Epic Acceptance Criteria

* <High-level outcome 1>
* <High-level outcome 2>
* <High-level outcome 3>
```

**Example:**
```
h2. Epic Acceptance Criteria

* Administrators can view aggregated metrics from all clusters in a single dashboard
* Alert rules can be configured to fire based on cross-cluster conditions
* Historical metrics are retained for 30 days across all clusters
* Documentation is complete for multi-cluster setup and configuration
```

**Characteristics:**
- Broader than story AC (focus on overall capability, not implementation details)
- Measurable outcomes
- User-observable (not technical implementation)
- Typically 3-6 criteria (if more, consider splitting epic)

### Timeboxing

Include timeframe information:
- Target quarter or release
- Key milestones or dependencies
- Known constraints

**Example:**
```
h2. Timeline

* Target: Q1 2025 / OpenShift 4.21
* Milestone 1: Metrics collection infrastructure (Sprint 1-2)
* Milestone 2: Dashboard and visualization (Sprint 3-4)
* Milestone 3: Alerting and historical data (Sprint 5-6)
```

### Parent Link to Feature

If the epic belongs to a larger feature:
- Link to parent feature using `--parent` flag
- Explain how this epic contributes to the feature
- Reference feature key in description

**Example:**
```
h2. Parent Feature

This epic is part of [PROJ-100] "Advanced cluster observability" and specifically addresses the multi-cluster aggregation capability.
```

## Interactive Epic Collection Workflow

When creating an epic, guide the user through:

### 1. Epic Objective

**Prompt:** "What is the main objective or goal of this epic? What capability will it deliver?"

**Helpful questions:**
- What is the overall goal?
- What high-level capability will be delivered?
- Who will benefit from this epic?

**Example response:**
```
Enable SREs to manage and monitor multiple ROSA HCP clusters from a unified observability dashboard, reducing the operational complexity of multi-cluster environments.
```

### 2. Epic Scope

**Prompt:** "What is included in this epic? What is explicitly out of scope?"

**Helpful questions:**
- What functionality is included?
- What related work is NOT part of this epic?
- Where are the boundaries?

**Example response:**
```
In scope:
- Metrics aggregation from multiple clusters
- Unified dashboard for cluster health
- Cross-cluster alerting
- 30-day historical metrics retention

Out of scope:
- Log aggregation (separate epic)
- Cost reporting (different feature)
- Support for non-HCP clusters (future work)
```

### 3. Epic Acceptance Criteria

**Prompt:** "What are the high-level outcomes that define this epic as complete?"

**Guidance:**
- Focus on capabilities, not implementation
- Should be measurable/demonstrable
- Typically 3-6 criteria

**Example response:**
```
- SREs can view aggregated metrics from all managed clusters in one dashboard
- Alert rules can be defined for cross-cluster conditions (e.g., "any cluster CPU >80%")
- Historical metrics available for 30 days
- Configuration documented and tested
```

### 4. Timeframe

**Prompt:** "What is the target timeframe for this epic? (quarter, release, or estimated sprints)"

**Example responses:**
- "Q1 2025"
- "OpenShift 4.21"
- "Estimate 6 sprints"
- "Must complete by March 2025"

### 5. Parent Feature (Optional)

**Prompt:** "Is this epic part of a larger feature? If yes, provide the feature key."

**If yes:**
- Validate parent exists
- Confirm parent is a Feature (not another Epic)
- Link epic to parent

## Field Validation

Before submitting the epic, validate:

### Required Fields
- ✅ Summary is clear and describes the capability
- ✅ Epic name field is set (same as summary)
- ✅ Description includes objective
- ✅ Epic acceptance criteria present
- ✅ Timeframe specified
- ✅ Component is specified (if required by project)
- ✅ Target version is set (if required by project)

### Epic Quality
- ✅ Scope is broader than a story, narrower than a feature
- ✅ Can fit in a quarter/release timeframe
- ✅ Has measurable acceptance criteria
- ✅ Clearly identifies target users/stakeholders
- ✅ Defines what's in scope and out of scope

### Parent Validation (if specified)
- ✅ Parent issue exists
- ✅ Parent is a Feature (not Epic or Story)
- ✅ Epic contributes to parent's objective

### Security
- ✅ No credentials, API keys, or secrets in any field

## MCP Tool Parameters

### Basic Epic Creation

```python
mcp__atlassian__jira_create_issue(
    project_key="<PROJECT_KEY>",
    summary="<epic summary>",
    issue_type="Epic",
    description="""
<Epic objective and description>

h2. Epic Acceptance Criteria

* <Outcome 1>
* <Outcome 2>
* <Outcome 3>

h2. Scope

h3. In Scope
* <What's included>

h3. Out of Scope
* <What's not included>

h2. Timeline

Target: <quarter/release>
    """,
    components="<component name>",  # if required
    additional_fields={
        "customfield_epicname": "<epic name>",  # if required, same as summary
        # Add other project-specific fields
    }
)
```

### With SRVKP-Specific Fields

```python
mcp__atlassian__jira_create_issue(
    project_key="SRVKP",
    summary="Enhanced Tekton Results storage and querying capabilities",
    issue_type="Epic",
    description="""
Enhance Tekton Results to provide scalable, high-performance storage and flexible querying capabilities for pipeline execution data across large-scale deployments.

h2. Epic Acceptance Criteria

* Results API can handle 10,000+ PipelineRuns per day
* Query response time < 200ms for typical queries
* Support filtering by status, time range, labels, parameters
* Automated cleanup based on retention policies (default 90 days)
* Results can be exported to S3-compatible storage
* GraphQL API provides flexible querying without performance degradation

h2. Scope

h3. In Scope
* Scalable database backend (PostgreSQL with partitioning)
* Advanced query API with filtering and pagination
* Results retention policies and automated cleanup
* Results export to S3/object storage
* Performance optimization for large result sets
* GraphQL query interface

h3. Out of Scope
* Real-time streaming of logs (separate epic)
* Results analytics and visualization (UI epic)
* Multi-tenancy support (future consideration)
* Integration with external observability platforms (post-MVP)

h2. Timeline

* Target: Pipelines 1.16
* Estimated: 6 sprints

h2. Target Users

* Pipeline operators managing large-scale deployments
* DevOps teams
* Platform administrators

h2. Dependencies

* Requires storage infrastructure improvements
* Depends on API refactoring work
    """,
    components="Tekton Results",
    additional_fields={
        "customfield_epicname": "Enhanced Tekton Results storage and querying capabilities",  # epic name
        "labels": ["ai-generated-jira"]
    }
)
```

### With Parent Feature Link

When linking an epic to a parent feature via `--parent` flag, use the **Parent Link** custom field (NOT Epic Link, NOT standard `parent` field):

```python
mcp__atlassian__jira_create_issue(
    project_key="SRVKP",
    summary="Pipeline caching improvements",
    issue_type="Epic",
    description="<epic content with scope and AC>",
    components="Tekton Cache",
    additional_fields={
        "customfield_12311141": "Pipeline caching improvements",  # Epic Name (required)
        "customfield_12313140": "SRVKP-100",  # Parent Link - links to parent FEATURE (STRING!)
        "labels": ["ai-generated-jira"]
    }
)
```

**IMPORTANT:**
- Epic→Feature uses **Parent Link** (`customfield_12313140`) - value is a STRING
- Story→Epic uses **Epic Link** (`customfield_12311140`) - value is a STRING
- The standard `parent` field does NOT work for these relationships

**See:** `/jira:create` command documentation for complete parent linking hierarchy and implementation strategy.

## Jira Description Formatting

Use Jira's native formatting (Wiki markup):

### Epic Template Format

```
<Epic objective - what capability will be delivered and why it matters>

h2. Epic Acceptance Criteria

* <High-level outcome 1>
* <High-level outcome 2>
* <High-level outcome 3>

h2. Scope

h3. In Scope
* <Functionality included in this epic>
* <Capabilities to be delivered>

h3. Out of Scope
* <Related work NOT in this epic>
* <Future considerations>

h2. Timeline

* Target: <quarter or release>
* Estimated: <sprints>
* Key milestones: <major deliverables>

h2. Target Users

* <User group 1>
* <User group 2>

h2. Dependencies (optional)

* [PROJ-XXX] - <dependency description>

h2. Parent Feature (if applicable)

This epic is part of [PROJ-YYY] "<feature name>" and addresses <how this epic contributes>.
```

## Error Handling

### Epic Name Field Missing

**Scenario:** Epic creation fails due to missing epic name field.

**Action:**
1. Check if project requires epic name field
2. If required, set `customfield_epicname` = summary
3. Retry creation

**Note:** Field ID may vary by Jira instance:
- `customfield_epicname` (common)
- `customfield_10011` (numbered field)
- Check project configuration if standard field names don't work

### Epic Too Large

**Scenario:** Epic seems too large (would take >1 quarter).

**Action:**
1. Suggest splitting into multiple epics
2. Identify natural split points
3. Consider if this should be a Feature instead

**Example:**
```
This epic seems quite large (estimated 12+ sprints). Consider:

Option 1: Split into multiple epics
- Epic 1: Core metrics aggregation (sprints 1-6)
- Epic 2: Advanced dashboards and alerting (sprints 7-12)

Option 2: Create as Feature instead
- This might be better as a Feature with multiple child Epics

Which would you prefer?
```

### Epic Too Small

**Scenario:** Epic could be completed in one sprint.

**Action:**
1. Suggest creating as a Story instead
2. Explain epic should be multi-sprint effort

**Example:**
```
This epic seems small enough to be a single Story (completable in one sprint).

Epics should typically:
- Span multiple sprints (2-8 sprints)
- Contain multiple stories
- Deliver a cohesive capability

Would you like to create this as a Story instead? (yes/no)
```

### Parent Not a Feature

**Scenario:** User specifies parent, but it's not a Feature.

**Action:**
1. Check parent issue type
2. If parent is Epic or Story, inform user
3. Suggest correction

**Example:**
```
Parent issue PROJ-100 is an Epic, but epics should typically link to Features (not other Epics).

Options:
1. Link to the parent Feature instead (if PROJ-100 has a parent)
2. Proceed without parent link
3. Create a Feature first, then link this Epic to it

What would you like to do?
```

### Missing Acceptance Criteria

**Scenario:** User doesn't provide epic acceptance criteria.

**Action:**
1. Explain importance of epic AC
2. Ask probing questions
3. Help construct AC

**Example:**
```
Epic acceptance criteria help define when this epic is complete. Let's add some.

What are the key outcomes that must be achieved?
- What capabilities will exist when this epic is done?
- How will you demonstrate the epic is complete?
- What must work end-to-end?

Example: "Administrators can view aggregated metrics from all clusters"
```

### Security Validation Failure

**Scenario:** Sensitive data detected in epic content.

**Action:**
1. STOP submission
2. Inform user what type of data was detected
3. Ask for redaction

### MCP Tool Error

**Scenario:** MCP tool returns an error when creating the epic.

**Action:**
1. Parse error message
2. Provide user-friendly explanation
3. Suggest corrective action

**Common errors:**
- **"Field 'epic name' is required"** → Set epic name = summary
- **"Invalid parent"** → Verify parent is Feature type
- **"Issue type 'Epic' not available"** → Check if project supports Epics

## Examples

### Example 1: Epic with Parent Feature

**Input:**
```bash
/jira:create epic "Pipeline caching improvements" --parent SRVKP-9000
```

**Interactive prompts:**
```
What is the main objective of this epic?
> Enhance Tekton Cache to provide faster pipeline execution through intelligent result caching

What is included in scope?
> Result caching, cache key computation, cache hit detection, retention policies

What is out of scope?
> Workspace caching (separate epic), distributed cache (future)

Epic acceptance criteria?
> - Tasks can opt-in to caching via annotations
> - Cache key computed from inputs and parameters
> - Cache hit reduces task execution time by 50%+
> - Configurable retention policies

Timeframe?
> Pipelines 1.16, estimate 6 sprints
```

**Implementation:**
1. Pre-validate that SRVKP-9000 exists and is a Feature
2. Create epic with Parent Link field:
   ```python
   additional_fields={
       "customfield_12311141": "Pipeline caching improvements",  # Epic Name
       "customfield_12313140": "SRVKP-9000",  # Parent Link (STRING, not object!)
       "labels": ["ai-generated-jira"]
   }
   ```
3. If creation fails, use fallback: create without parent, then update to add parent link

**Result:**
- Epic created with complete description
- Linked to parent feature SRVKP-9000 via Parent Link field (`customfield_12313140`)
- All SRVKP conventions applied

### Example 2: Epic with Auto-Detection

**Input:**
```bash
/jira:create epic "Advanced pipeline trigger filtering and routing"
```

**Auto-applied:**
- Project: SRVKP
- Component: Tekton Triggers (detected from "trigger", "routing")
- Epic Name: Same as summary
- Labels: ai-generated-jira

**Interactive prompts:**
- Epic objective and scope
- Acceptance criteria
- Timeframe

**Result:**
- Full epic with Tekton Triggers component

### Example 3: Standalone Epic (No Parent)

**Input:**
```bash
/jira:create epic "Improve test coverage for Tekton Hub catalog"
```

**Result:**
- Epic created in SRVKP without parent
- Component: Tekton Hub
- Standard epic fields applied
- Ready for stories to be linked

### Example 4: SRVKP Project Epic

**Input:**
```bash
/jira:create epic "Enhanced Tekton Results storage and querying capabilities"
```

**Interactive prompts:**
```
What is the main objective of this epic?
> Enhance Tekton Results to provide scalable, high-performance storage and flexible querying capabilities for pipeline execution data across large-scale deployments

What is included in scope?
> In scope:
> - Scalable database backend (PostgreSQL with partitioning)
> - Advanced query API with filtering and pagination
> - Results retention policies and automated cleanup
> - Results export to S3/object storage
> - Performance optimization for large result sets
> - GraphQL query interface
>
> Out of scope:
> - Real-time streaming of logs (separate epic)
> - Results analytics and visualization (UI epic)
> - Multi-tenancy support (future consideration)
> - Integration with external observability platforms (post-MVP)

Epic acceptance criteria?
> - Results API can handle 10,000+ PipelineRuns per day
> - Query response time < 200ms for typical queries
> - Support filtering by status, time range, labels, parameters
> - Automated cleanup based on retention policies (default 90 days)
> - Results can be exported to S3-compatible storage
> - GraphQL API provides flexible querying without performance degradation
> - Documentation covers deployment and scaling best practices

Timeframe?
> Q1 2026, estimated 6 sprints
```

**Component Suggestion:**
- Detected keywords: "Results", "storage", "querying"
- Suggested component: **Tekton Results**

**Result:**
- Epic created in SRVKP project
- Component: Tekton Results
- Complete scope definition and acceptance criteria
- Epic Name: "Enhanced Tekton Results storage and querying capabilities"
- Labels: ai-generated-jira
- Ready for child stories to be created

## Best Practices Summary

1. **Clear objective:** State what capability will be delivered
2. **Define scope:** Explicitly state what's in and out of scope
3. **Epic AC:** High-level outcomes that define "done"
4. **Right size:** 2-8 sprints, fits in a quarter
5. **Timebox:** Specify target quarter/release
6. **Link to feature:** If part of larger initiative
7. **Target users:** Identify who benefits
8. **Epic name field:** Always set (same as summary)

## Anti-Patterns to Avoid

❌ **Epic is actually a story**
```
"As a user, I want to view a dashboard"
```
✅ Too small, create as Story instead

❌ **Epic is actually a feature**
```
"Complete observability platform redesign" (12 months, 50+ stories)
```
✅ Too large, create as Feature with child Epics

❌ **Vague acceptance criteria**
```
- Epic is done when everything works
```
✅ Be specific: "SREs can view metrics from 100+ clusters with <1s load time"

❌ **Implementation details in AC**
```
- Backend uses PostgreSQL for metrics storage
- API implements gRPC endpoints
```
✅ Focus on outcomes, not implementation

❌ **No scope definition**
```
Description: "Improve monitoring"
```
✅ Define what's included and what's not

## Confirmation Flow and Workflow Summary

Follow the **Mandatory Confirmation Flow** and **MCP → CLI Fallback Decision Tree** defined
in [`../_common.md`](../_common.md). The preview label for this type is `PREVIEW: SRVKP Epic`.
Also include `Epic Name: [same as summary]` in the preview block.

1. ✅ **ENFORCE SRVKP-only** - reject other projects
2. 🔍 **PHASE 0A: Duplicate Detection** - search for similar epics (3+ keyword match)
3. 🔗 **PHASE 0B: Parent Feature Discovery** - search for related Features
4. ✨ **PHASE 0C: Auto-Suggest Feature** - generate and create parent Feature if needed
5. 🔍 **Suggest component** from summary keywords
6. 💬 Interactively collect epic objective and scope
7. 💬 Interactively collect epic acceptance criteria
8. 💬 Collect timeframe
9. 📝 Format description with SRVKP template
10. 🔒 Scan for sensitive data
11. ✅ Validate epic size and quality
12. ✅ Set epic name field = summary
13. 📋 **SHOW COMPLETE PREVIEW**
14. ❓ **GET USER CONFIRMATION (yes/no)**
15. ✅ **Create the epic** (only if confirmed) — MCP first; same payload via `acli` on fallback
16. 📤 Return issue key and URL

## See Also

- `/jira:create` - Main command that invokes this skill
- `/jira:create feature` - For creating parent features
- `create-feature` skill - Feature creation (invoked automatically if needed)
- `create-story` skill - For stories within epics
- SRVKP project conventions and best practices
