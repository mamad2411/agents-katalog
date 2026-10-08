---
name: Create Jira Task
description: Implementation guide for creating Jira tasks for technical and operational work in SRVKP project
---

# Create Jira Task

This skill provides implementation guidance for creating Jira tasks, which are used for technical or operational work that doesn't necessarily deliver direct user-facing value, for the **SRVKP project**.

## When to Use This Skill

This skill is automatically invoked by the `/jira:create task` command to guide the task creation process.

## Prerequisites

- MCP Jira server configured and accessible, **or** `acli` installed and authenticated
- User has permissions to create issues in SRVKP project
- Understanding of the technical work to be performed

**Shared conventions** (safety rules, component table, confirmation flow, MCP→CLI fallback):
→ Read and follow [`../_common.md`](../_common.md) before proceeding.

**CLI reference:** [`../reference/cli-fallback.md`](../reference/cli-fallback.md)

## Project: SRVKP Only

This skill is **exclusively for SRVKP** (OpenShift Pipelines project).
Component auto-suggestion keywords and the full component list are in [`../_common.md`](../_common.md).

## Tasks vs Stories

### When to Use a Task

Use a **Task** when the work is:
- **Technical/operational** - Infrastructure, refactoring, configuration
- **Not user-facing** - No direct end-user functionality
- **Internal improvement** - Code quality, performance, maintenance
- **Enabler work** - Supports future stories but isn't user-visible

**Examples of tasks:**
- "Update scaling documentation"
- "Refactor authentication utility package"
- "Configure CI pipeline for integration tests"
- "Upgrade dependency X to version Y"
- "Investigate performance regression in component Z"

### When to Use a Story Instead

Use a **Story** when the work:
- Delivers user-facing functionality
- Can be expressed as "As a... I want... so that..."
- Has business value to end users
- Is part of a user workflow

**If in doubt:** Ask "Would an end user notice or care about this change?"
- **Yes** → Story
- **No** → Task

## Task Best Practices

### Clear Summary

The summary should:
- Be concise (one sentence)
- Use action verbs (Update, Refactor, Configure, Investigate, Fix)
- Identify what is being changed
- Optionally include "why" if not obvious

**Good examples:**
- "Update autoscaling documentation for 4.21 release"
- "Refactor scaling controller to reduce code duplication"
- "Configure Prometheus alerts for control plane memory usage"
- "Investigate intermittent timeout in etcd health checks"

**Bad examples:**
- "Do some work on docs" (too vague)
- "Technical debt" (not specific)
- "Various improvements" (not actionable)

### Detailed Description

The description should include:

1. **What needs to be done** - Clear statement of the work
2. **Why it's needed** - Context or motivation
3. **Acceptance criteria** (optional but recommended) - How to know it's done
4. **Technical details** (if helpful) - Specific files, commands, approaches

**Example:**
```
Update the autoscaling documentation to reflect changes in the 4.21 release.

Why: The autoscaling API changed in 4.21 with new fields and behavior. Documentation currently reflects 4.20 and will confuse users.

Acceptance Criteria:
- All autoscaling examples updated to use 4.21 API
- New fields documented with descriptions and examples
- Deprecated fields marked as deprecated
- Documentation builds without warnings

Files to update:
- docs/content/how-to/autoscaling.md
- docs/content/reference/api.md
```

## Task Description Template

Use this structure for consistency:

```
<What needs to be done>

h2. Why

<Context, motivation, or reason this is needed>

h2. Acceptance Criteria

* <Criterion 1>
* <Criterion 2>
* <Criterion 3>

h2. Technical Details (optional)

* Files to modify: <list>
* Dependencies: <related issues or work>
* Approach: <suggested implementation approach>
```

## Interactive Task Collection Workflow

When creating a task, collect necessary information:

### 1. Task Description

**Prompt:** "What work needs to be done? Be specific about what you'll change or update."

**Helpful questions:**
- What component or area is being worked on?
- What specific changes will be made?
- What's the end state after this task is complete?

**Example response:**
```
Refactor the scaling controller to extract common validation logic into a shared utility package. Currently, validation code is duplicated across three controller files.
```

### 2. Motivation/Context

**Prompt:** "Why is this task needed? What problem does it solve?"

**Helpful questions:**
- What prompted this work?
- What will improve after this is done?
- Is this addressing a specific issue or enabling future work?

**Example response:**
```
Code duplication makes maintenance difficult. When validation logic changes, we have to update it in three places, which is error-prone. Consolidating into a shared utility will make the code easier to maintain and reduce bugs.
```

### 3. Acceptance Criteria (Optional but Recommended)

**Prompt:** "How will you know this task is complete? (Optional: skip if obvious)"

**For technical tasks, AC might include:**
- Tests passing
- Documentation updated
- Code review completed
- Specific functionality working

**Example response:**
```
- Validation logic extracted to support/validation package
- All three controllers updated to use shared validation
- Existing tests pass
- New unit tests added for validation utility
- Code review approved
```

### 4. Parent Link (Optional)

**Prompt:** "Is this task part of a larger story or epic? (Optional)"

**If yes:**
- Collect parent issue key
- Verify parent exists
- Link task to parent

### 5. Additional Technical Details (Optional)

**Prompt:** "Any technical details to include? (files to change, dependencies, approach)"

**Example response:**
```
Files to modify:
- hypershift/operator/controllers/nodepool/autoscaling.go
- hypershift/operator/controllers/hostedcluster/autoscaling.go
- hypershift/operator/controllers/manifests/autoscaling.go
- hypershift/support/validation/autoscaling.go (new)

Dependencies:
- Must complete after PROJ-100 (validation refactor epic)

Approach:
- Extract common validation functions to support/validation
- Add comprehensive unit tests for new package
- Update controllers to import and use new package
- Remove duplicated code
```

## Field Validation

Before submitting the task, validate:

### Required Fields
- ✅ Summary is clear and specific
- ✅ Description explains what needs to be done
- ✅ Description includes why (motivation)
- ✅ Component is specified (if required by project)
- ✅ Target version is set (if required by project)

### Task Quality
- ✅ Summary uses action verb (Update, Refactor, Configure, etc.)
- ✅ Work is technical/operational (not user-facing functionality)
- ✅ Description is detailed enough for someone else to understand
- ✅ Acceptance criteria present (if work is non-trivial)
- ✅ Task is sized appropriately (can complete in reasonable time)

### Security
- ✅ No credentials, API keys, or secrets in any field
- ✅ No sensitive technical details that shouldn't be public

## MCP Tool Parameters

### Basic Task Creation

```python
mcp__atlassian__jira_create_issue(
    project_key="<PROJECT_KEY>",
    summary="<task summary>",
    issue_type="Task",
    description="""
<What needs to be done>

h2. Why

<Context and motivation>

h2. Acceptance Criteria

* <Criterion 1>
* <Criterion 2>

h2. Technical Details

<Optional technical details>
    """,
    components="<component name>",  # if required
    additional_fields={
        # Add project-specific fields
    }
)
```

### With SRVKP-Specific Fields

```python
mcp__atlassian__jira_create_issue(
    project_key="SRVKP",
    summary="Update Tekton Chains documentation for SLSA v1.0",
    issue_type="Task",
    description="""
Update the Tekton Chains documentation to reflect the new SLSA v1.0 provenance format introduced in Chains v0.20.

h2. Why

Chains v0.20 introduced breaking changes for SLSA v1.0 support. Current documentation describes v0.2 format which is now deprecated. Users need updated guidance for migration and new features.

h2. Acceptance Criteria

* All SLSA examples updated to v1.0 format
* New attestation fields documented with examples
* Migration guide from v0.2 to v1.0 created
* Breaking changes clearly highlighted
* Verification examples updated for new signature format
* Documentation builds successfully without warnings

h2. Technical Details

Files to update:
* docs/chains/slsa-provenance.md
* docs/chains/attestation-formats.md
* docs/chains/migration-v1.md (new)
* examples/chains/slsa-v1-attestation.yaml

Reference: Chains v0.20 release notes, SLSA v1.0 specification
    """,
    components="Tekton Chains",
    additional_fields={
        "labels": ["ai-generated-jira", "documentation"]
    }
)
```

### With Parent Link

```python
mcp__atlassian__jira_create_issue(
    project_key="SRVKP",
    summary="Add unit tests for cache key computation",
    issue_type="Task",
    description="<task content>",
    additional_fields={
        "parent": {"key": "SRVKP-9000"}  # link to story or epic
    }
)
```

## Jira Description Formatting

Use Jira's native formatting (Wiki markup):

### Task Template Format

```
<Brief description of what needs to be done>

h2. Why

<Context, motivation, or problem this solves>

h2. Acceptance Criteria

* <Criterion 1>
* <Criterion 2>
* <Criterion 3>

h2. Technical Details

h3. Files to Modify
* {{path/to/file1.go}}
* {{path/to/file2.go}}

h3. Dependencies
* Must complete after [PROJ-100]
* Requires library X version Y

h3. Approach
<Suggested implementation approach or technical notes>

h2. Additional Context

<Optional: Links to designs, related issues, background>
```

Use Jira wiki markup in descriptions (for example `h2.` headings and `*` lists) as needed.

## Error Handling

### Task vs Story Confusion

**Scenario:** User tries to create a task for user-facing functionality.

**Action:**
1. Detect user-facing language in summary/description
2. Ask if this should be a story instead
3. Explain the difference
4. Offer to create as story if appropriate

**Example:**
```
This sounds like it might deliver user-facing functionality. The summary mentions "users can configure autoscaling".

Should this be a Story instead of a Task?
- Story: For user-facing features (visible to end users)
- Task: For internal/technical work (not visible to end users)

Would you like me to create this as a Story? (yes/no)
```

### Missing Context

**Scenario:** User provides minimal description without context.

**Action:**
1. Ask for more details
2. Prompt for "why" if missing
3. Suggest adding acceptance criteria if non-trivial

**Example:**
```
The description "Update docs" is a bit brief. Can you provide more detail?

- Which documentation needs updating?
- Why does it need updating? (new features, corrections, clarifications?)
- What specific changes should be made?
```

### Parent Not Found

**Scenario:** User specifies `--parent` but issue doesn't exist.

**Action:**
1. Attempt to fetch parent issue
2. If not found, inform user
3. Offer options: proceed without parent, specify different parent, cancel

**Example:**
```
Parent issue PROJ-999 not found.

Options:
1. Proceed without parent link
2. Specify different parent
3. Cancel task creation

What would you like to do?
```

### Security Validation Failure

**Scenario:** Sensitive data detected in task content.

**Action:**
1. STOP submission
2. Inform user what type of data was detected
3. Ask for redaction

**Example:**
```
I detected what appears to be an API key in the technical details section.
Please use placeholder values like "YOUR_API_KEY" instead of real credentials.
```

### MCP Tool Error

**Scenario:** MCP tool returns an error when creating the task.

**Action:**
1. Parse error message
2. Provide user-friendly explanation
3. Suggest corrective action

**Common errors:**
- **"Field 'component' is required"** → Prompt for component
- **"Invalid parent"** → Verify parent issue exists and is correct type
- **"Permission denied"** → User may lack project permissions

## Examples

### Example 1: Documentation Task

**Input:**
```bash
/jira:create task "Update Tekton CLI documentation for new commands"
```

**Interactive prompts:**
```
What work needs to be done?
> Update the tkn CLI documentation to include new commands added in latest release

Why is this task needed?
> New commands were added, docs need updating to reflect current CLI capabilities

How will you know this is complete?
> All new commands documented with examples, no build warnings, reviewed by maintainers

Any technical details?
> Files: docs/cli/commands.md, docs/cli/reference.md
```

**Result:**
- Task created with complete description
- Component: Tekton Cli (auto-detected from "CLI", "tkn")

### Example 2: Refactoring Task

**Input:**
```bash
/jira:create task "Refactor EventListener validation logic to reduce duplication"
```

**Interactive prompts:**
```
What work needs to be done?
> Extract common validation code from EventListener controller files into shared utility

Why is this needed?
> Code duplication makes maintenance difficult and error-prone

Acceptance criteria?
> - Validation extracted to pkg/validation package
> - All EventListener components use shared validation
> - Tests pass
> - New unit tests for validation utility

Any technical details?
> Files to modify:
> - pkg/reconciler/eventlistener/validate.go
> - pkg/interceptors/validate.go
> New file: pkg/validation/eventlistener.go
```

**Result:**
- Task with detailed technical plan
- Component: Tekton Triggers
- Clear acceptance criteria
- Ready for implementation

### Example 3: Task with Parent

**Input:**
```bash
/jira:create task "Add integration tests for cache key computation" --parent SRVKP-9000
```

**Auto-applied:**
- Project: SRVKP
- Linked to parent story SRVKP-9000
- Component: Tekton Cache (from parent or auto-detected)

**Result:**
- Task created under parent story
- All fields properly set

### Example 4: SRVKP Project Task

**Input:**
```bash
/jira:create task "Update Tekton Chains documentation for SLSA v1.0 support"
```

**Interactive prompts:**
```
What work needs to be done?
> Update the Tekton Chains documentation to reflect the new SLSA v1.0 provenance format and attestation features introduced in Chains v0.20

Why is this task needed?
> Chains v0.20 introduced breaking changes for SLSA v1.0 support. Current documentation describes v0.2 format which is now deprecated. Users need updated guidance for migration and new features.

How will you know this is complete?
> - All SLSA examples updated to v1.0 format
> - New attestation fields documented with examples
> - Migration guide from v0.2 to v1.0 created
> - Breaking changes clearly highlighted
> - Verification examples updated for new signature format
> - Documentation builds without warnings
> - Reviewed by Chains maintainers

Any technical details?
> Files to update:
> - docs/chains/slsa-provenance.md
> - docs/chains/attestation-formats.md
> - docs/chains/migration-v1.md (new)
> - examples/chains/slsa-v1-attestation.yaml
> 
> Key changes:
> - buildType field now uses fully qualified URLs
> - New subject.digest format for multi-platform images
> - materials field replaced with resolvedDependencies
> - New metadata.buildInvocationId field
> 
> Reference: Chains v0.20 release notes, SLSA v1.0 specification
```

**Component Suggestion:**
- Detected keywords: "Chains", "documentation"
- Suggested component: **Tekton Chains**

**Result:**
- Task created in SRVKP project
- Component: Tekton Chains
- Complete with acceptance criteria and technical details
- Labels: ai-generated-jira
- Ready for implementation

### Example 5: Investigation Task

**Input:**
```bash
/jira:create task "Investigate intermittent PipelineRun webhook delivery failures"
```

**Description pattern for investigation tasks:**
```
Investigate intermittent webhook delivery failures causing PipelineRuns not to trigger on GitHub push events.

h2. Why

Users report that PipelineRuns occasionally fail to trigger despite GitHub webhooks being sent successfully. Webhook delivery logs show 5xx errors from EventListener.

h2. Acceptance Criteria

* Root cause identified and documented
* Recommendation provided (fix, workaround, or "no action needed")
* Findings shared with team in investigation summary

h2. Technical Details

Error pattern:
{code}
EventListener returned 503 Service Unavailable
Connection timeout after 10s
{code}

Frequency: ~5% of webhook deliveries
Affected: Pipelines 1.15.x deployments
Logs to review: eventlistener-xxx pods, tekton-triggers-controller

Related issues: GitHub webhook retry behavior
```

**Result:**
- Investigation task with clear scope
- Component: Tekton Triggers
- Defined outcome (root cause + recommendation)
- Context for debugging

## Best Practices Summary

1. **Specific summaries:** Use action verbs, identify what's changing
2. **Explain why:** Always include motivation/context
3. **Add AC:** Even for tasks, AC helps define "done"
4. **Technical details:** Include file paths, commands, approaches when helpful
5. **Right size:** Task should be completable in reasonable time (days, not weeks)
6. **Link to parent:** If task supports a story/epic, link it
7. **Not a story:** If it's user-facing, create a story instead

## Anti-Patterns to Avoid

❌ **Vague summaries**
```
"Update stuff"
"Fix things"
```
✅ Be specific: "Update autoscaling documentation for 4.21 API changes"

❌ **User-facing work as tasks**
```
"Add user dashboard feature"
```
✅ Should be a Story if it delivers user value

❌ **Too large**
```
"Refactor entire codebase"
"Update all documentation"
```
✅ Break into smaller, focused tasks

❌ **No context**
```
Summary: "Update docs"
Description: <empty>
```
✅ Always explain why and what specifically

## Confirmation Flow and Workflow Summary

Follow the **Mandatory Confirmation Flow** and **MCP → CLI Fallback Decision Tree** defined
in [`../_common.md`](../_common.md). The preview label for this type is `PREVIEW: SRVKP Task`.

1. ✅ **ENFORCE SRVKP-only** - reject other projects
2. 🔍 **Suggest component** from summary keywords
3. 💬 Interactively collect task description and context
4. 💬 Interactively collect acceptance criteria (optional)
5. 💬 Optionally collect technical details
6. 📝 Format description with SRVKP template
7. 🔒 Scan for sensitive data
8. ✅ Validate task is appropriate (not a story)
9. 📋 **SHOW COMPLETE PREVIEW**
10. ❓ **GET USER CONFIRMATION (yes/no)**
11. ✅ **Create the task** (only if confirmed) — MCP first; same payload via `acli` on fallback
12. 📤 Return issue key and URL

## See Also

- `/jira:create` - Main command that invokes this skill
- `create-story` skill - For user-facing functionality
- SRVKP project conventions and best practices
- Agile task management best practices
