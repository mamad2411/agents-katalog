---
name: Create Jira Bug
description: Implementation guide for creating well-formed Jira bug reports in SRVKP project
---

# Create Jira Bug

This skill provides implementation guidance for creating well-structured Jira bug reports with complete reproduction steps and clear problem descriptions for the **SRVKP project**.

## When to Use This Skill

This skill is automatically invoked by the `/jira:create bug` command to guide the bug creation process.

## Prerequisites

- MCP Jira server configured and accessible, **or** `acli` installed and authenticated
- User has permissions to create issues in SRVKP project
- Bug information available (problem description, steps to reproduce, etc.)

**Shared conventions** (safety rules, component table, confirmation flow, MCP→CLI fallback):
→ Read and follow [`../_common.md`](../_common.md) before proceeding.

**CLI reference:** [`../reference/cli-fallback.md`](../reference/cli-fallback.md)

## Project: SRVKP Only

This skill is **exclusively for SRVKP** (OpenShift Pipelines project).
Component auto-suggestion keywords and the full component list are in [`../_common.md`](../_common.md).

## Bug Report Best Practices

### Complete Information

A good bug report contains:
1. **Clear summary** - Brief description that identifies the problem
2. **Detailed description** - Complete context and background
3. **Reproducibility** - How often the bug occurs
4. **Steps to reproduce** - Exact sequence to trigger the bug
5. **Actual vs expected results** - What happens vs what should happen
6. **Environment details** - Version, platform, configuration
7. **Additional context** - Logs, screenshots, error messages

### Summary Guidelines

The summary should:
- Be concise (one sentence)
- Identify the problem clearly
- Include key context when helpful
- Avoid vague terms like "broken" or "doesn't work"

**Good examples:**
- "API server returns 500 error when creating namespaces"
- "Control plane pods crash on upgrade from 4.20 to 4.21"
- "Memory leak in etcd container after 24 hours"

**Bad examples:**
- "Things are broken"
- "Error in production"
- "Fix the bug"

## Bug Description Template

Use this template structure for consistency:

```
Description of problem:
<Clear, detailed description of the issue>

Version-Release number of selected component (if applicable):
<e.g., 4.21.0, openshift-client-4.20.5>

How reproducible:
<Always | Sometimes | Rarely>

Steps to Reproduce:
1. <First step - be specific>
2. <Second step>
3. <Third step>

Actual results:
<What actually happens - include error messages>

Expected results:
<What should happen instead>

Additional info:
<Logs, screenshots, stack traces, related issues, workarounds>
```

## Interactive Bug Collection Workflow

When creating a bug, guide the user through each section interactively:

### 1. Problem Description

**Prompt:** "What is the problem? Describe it clearly and in detail."

**Tips to share:**
- Provide context: What were you trying to do?
- Be specific: What component or feature is affected?
- Include impact: Who is affected? How severe is it?

**Example response:**
```
The kube-apiserver pod crashes immediately after upgrading a hosted control plane cluster from version 4.20 to 4.21. The pod enters CrashLoopBackOff state and all API requests to the cluster fail.
```

### 2. Version Information

**Prompt:** "Which version exhibits this issue? (e.g., 4.21.0, 4.20.5)"

**Tips:**
- Include full version number if known
- Specify component version if different from platform version
- Note if issue affects multiple versions

**Format:** Use "Pipelines X.XX.X" format (e.g., "Pipelines 1.15.2")

### 3. Reproducibility

**Prompt:** "How reproducible is this issue?"

**Options:**
- **Always** - Happens every time following the steps
- **Sometimes** - Happens intermittently, even with same steps
- **Rarely** - Hard to reproduce, happened once or few times

**Use case for each:**
- Always: Easiest to debug and fix
- Sometimes: May be timing-related or race condition
- Rarely: May be environmental or complex interaction

### 4. Steps to Reproduce

**Prompt:** "What are the exact steps to reproduce this issue? Be as specific as possible."

**Guidelines:**
- Number each step
- Be precise (exact commands, button clicks, inputs)
- Include environment setup if needed
- Use code blocks for commands
- Mention any prerequisites

**Example:**
```
Steps to Reproduce:
1. Create a ROSA HCP cluster on version 4.20.0:
   rosa create cluster --name test-cluster --version 4.20.0 --hosted-cp
2. Wait for cluster to be fully ready (about 15 minutes)
3. Initiate upgrade to 4.21.0:
   rosa upgrade cluster --cluster test-cluster --version 4.21.0
4. Monitor the control plane pods:
   oc get pods -n clusters-test-cluster -w
5. Observe kube-apiserver pod status
```

**Validation:**
- Ensure at least one step is provided
- Check that steps are numbered/ordered
- Verify steps are specific enough to follow

### 5. Actual Results

**Prompt:** "What actually happens when you follow those steps?"

**Guidelines:**
- Describe exactly what occurs
- Include error messages (full text)
- Mention symptoms (crashes, hangs, wrong output)
- Include relevant logs or stack traces
- Note timing (immediate, after 5 minutes, etc.)

**Example:**
```
Actual results:
The kube-apiserver pod crashes immediately after the upgrade completes. The pod restarts continuously (CrashLoopBackOff). Error in pod logs:

panic: runtime error: invalid memory address or nil pointer dereference
[signal SIGSEGV: segmentation violation code=0x1 addr=0x0 pc=0x...]

API requests to the cluster fail with:
Error from server: error dialing backend: dial tcp: lookup kube-apiserver: no such host
```

### 6. Expected Results

**Prompt:** "What should happen instead? What is the expected behavior?"

**Guidelines:**
- Describe the correct behavior
- Be specific about expected state/output
- Contrast with actual results

**Example:**
```
Expected results:
The kube-apiserver pod should start successfully after the upgrade. The pod should be in Running state, and API requests to the cluster should succeed normally.
```

**Validation:**
- Ensure expected results differ from actual results
- Check that expected behavior is clearly stated

### 7. Additional Information

**Prompt:** "Any additional context? (Optional: logs, screenshots, workarounds, related issues)"

**Helpful additions:**
- Full logs or log excerpts
- Screenshots or recordings
- Stack traces
- Related Jira issues or documentation
- Workarounds discovered
- Impact assessment (severity, affected users)
- Environment specifics (region, network config, etc.)

**Example:**
```
Additional info:
- Pipeline definition: 50+ tasks, complex dependencies
- OpenShift version: 4.15
- Full pod logs attached: taskrun-abc123.log
- Related issue: Tekton Pipelines #7890 (similar OOM in different context)
- Workaround: Set resources.requests.memory: 2Gi in TaskRun spec
- Affects: Large repository clones (>2GB)
```

## Component and Version Handling

### Auto-Detection

Analyze the bug description for component hints:
- Product names: "OpenShift", "ROSA", "ARO", "HyperShift"
- Component names: "API server", "etcd", "networking", "storage"
- Platform: "AWS", "Azure", "GCP", "bare metal"

### Version Fields for SRVKP

SRVKP uses version fields as follows:

- **Affects Version/s**: Version where bug was found (e.g., "Pipelines 1.15.2")
- **Fix Version/s**: Version where fix will be delivered (e.g., "Pipelines 1.15.4")
- Use format "Pipelines X.XX.X" for consistency

### Version Format

Always use the format: **"Pipelines X.XX.X"**

Examples:
- ✅ "Pipelines 1.15.2"
- ✅ "Pipelines 1.16.0"
- ❌ "1.15.2" (missing "Pipelines" prefix)
- ❌ "v1.15.2" (don't use "v" prefix)

## Field Validation

Before submitting the bug, validate:

### Required Fields
- ✅ Summary is not empty and is clear
- ✅ Description contains problem description
- ✅ Component is specified (or project doesn't require it)
- ✅ Affects version is specified (if required by project)

### Description Quality
- ✅ "Steps to Reproduce" has at least one step
- ✅ "Actual results" is different from "Expected results"
- ✅ "How reproducible" is specified (Always/Sometimes/Rarely)

### Security
- ✅ No credentials, API keys, or secrets in any field
- ✅ Logs are sanitized (passwords, tokens redacted)
- ✅ Screenshots don't expose sensitive information

## MCP Tool Parameters

### Basic Bug Creation

```python
mcp__atlassian__jira_create_issue(
    project_key="SRVKP",
    summary="<bug summary>",
    issue_type="Bug",
    description="<formatted bug template>",
    components="<component name>",  # one of the Tekton components
    additional_fields={
        "versions": [{"name": "Pipelines X.XX.X"}],  # affects version
        "labels": ["ai-generated-jira"]
    }
)
```

### With SRVKP-Specific Fields

```python
mcp__atlassian__jira_create_issue(
    project_key="SRVKP",
    summary="TaskRun fails with OOMKilled in git-clone step",
    issue_type="Bug",
    description="""
h2. Description of problem

TaskRun fails when the git-clone step attempts to clone large repositories. The step container is terminated with OOMKilled status.

h2. Version-Release number

Pipelines 1.15.2

h2. How reproducible

Always

h2. Steps to Reproduce

# Create a Pipeline with git-clone task from Tekton Hub
# Create a PipelineRun targeting a large repository (>2GB)
# Observe the git-clone step execution
# Step fails with OOMKilled after ~30 seconds

h2. Actual results

The git-clone step container is killed by Kubernetes OOM killer with exitCode 137.

h2. Expected results

The git-clone step should complete successfully with sufficient memory allocation.

h2. Additional info

Default memory limit: 512Mi. Large repos require 1-2Gi. Workaround: Set resources.requests.memory: 2Gi in TaskRun.
    """,
    components="Tekton Pipelines",
    additional_fields={
        "labels": ["ai-generated-jira"]
    }
)
```

## Jira Description Formatting

Use Jira's native formatting (Wiki markup).

## Error Handling

### Missing Required Information

**Scenario:** User doesn't provide required fields.

**Action:**
1. Identify missing required fields
2. Prompt user for each missing field
3. Provide context/examples to help
4. Re-validate before submission

**Example:**
```
Summary is required but not provided. Please provide a brief summary of the bug:
Example: "API server crashes when creating namespaces"
```

### Invalid Version

**Scenario:** Specified version doesn't exist in project.

**Action:**
1. Use `mcp__atlassian__jira_get_project_versions` to fetch valid versions
2. Suggest closest match or list available versions
3. Ask user to confirm or select different version

**Example:**
```
Version "Pipelines 1.15.5" not found for project SRVKP.
Available versions: Pipelines 1.14.0, Pipelines 1.15.2, Pipelines 1.15.4, Pipelines 1.16.0
Did you mean "Pipelines 1.15.4"?
```

### Component Required But Not Provided

**Scenario:** Project requires component, but none specified.

**Action:**
1. Ask user which component the bug affects
2. If available, fetch and display component list for project
3. Accept user's component selection
4. Validate component exists before submission

### Security Validation Failure

**Scenario:** Sensitive data detected in bug content.

**Action:**
1. STOP submission immediately
2. Inform user what type of data was detected (without echoing it)
3. Provide guidance on redaction
4. Request sanitized version

**Example:**
```
I detected what appears to be an API token in the "Steps to Reproduce" section.
Please replace with a placeholder like "YOUR_API_TOKEN" or "<redacted>" before proceeding.
```

### MCP Tool Error

**Scenario:** MCP tool returns an error when creating the bug.

**Action:**
1. Parse error message
2. Translate to user-friendly explanation
3. Suggest corrective action
4. Offer to retry

**Common errors:**
- **"Field 'component' is required"** → Prompt for component
- **"Version not found"** → Use version error handling
- **"Permission denied"** → User may lack project permissions, inform them to contact admin

## Examples

### Example 1: Simple Bug

**Input:**
```bash
/jira:create bug "tkn pipeline start command fails with invalid workspace error"
```

**Interactive prompts:**
```
What is the problem? Describe it clearly.
> The tkn CLI pipeline start command fails with "invalid workspace" error when using emptyDir workspace type.

Which version exhibits this issue?
> Pipelines 1.15.2

How reproducible is this issue?
> Always

What are the exact steps to reproduce?
> 1. Install tkn CLI version 0.35.0
> 2. Run: tkn pipeline start my-pipeline --workspace name=source,emptyDir=""
> 3. Observe error message

What actually happens?
> Command fails with error: "invalid workspace: emptyDir type not supported in this context"
> Exit code: 1

What should happen instead?
> The command should successfully create a PipelineRun with emptyDir workspace.

Any additional context?
> Works fine with volumeClaimTemplate. Only affects emptyDir workspace type.
```

**Result:**
- Issue created in SRVKP
- Type: Bug
- Component: Tekton Cli (auto-detected from "tkn")
- Summary: "tkn pipeline start command fails with invalid workspace error"
- Description: Formatted with bug template

### Example 2: Bug with Auto-Detection

**Input:**
```bash
/jira:create bug "EventListener webhook returns 500 error on GitHub push events"
```

**Auto-applied:**
- Project: SRVKP
- Component: Tekton Triggers (detected from "EventListener", "webhook")
- Labels: ai-generated-jira

**Interactive prompts:**
- Bug template sections (same as Example 1)

**Result:**
- Full bug report created with SRVKP conventions applied

### Example 3: Bug with Component Specified

**Input:**
```bash
/jira:create bug "Pruner fails to cleanup old TaskRuns" --component "Pruner"
```

**Minimal prompts:**
- Description of problem
- Steps to reproduce
- Actual/expected results
- Additional info

**Result:**
- Bug created with specified component
- Only prompts for description content

### Example 4: SRVKP Project Bug

**Input:**
```bash
/jira:create bug "PipelineRun fails with OOMKilled in git-clone step"
```

**Interactive prompts:**
```
What is the problem? Describe it clearly.
> PipelineRun fails when the git-clone step attempts to clone a large repository (>2GB). The step container is terminated with OOMKilled status.

Which version exhibits this issue?
> Tekton Pipelines v0.56.0

How reproducible is this issue?
> Always (when cloning repositories > 2GB)

What are the exact steps to reproduce?
> 1. Create a Pipeline with git-clone task from Tekton Hub
> 2. Create a PipelineRun targeting a large repository (e.g., github.com/kubernetes/kubernetes)
> 3. Observe the git-clone step execution
> 4. Step fails with OOMKilled after ~30 seconds

What actually happens?
> The git-clone step container is killed by Kubernetes OOM killer.
> 
> TaskRun status shows:
> {
>   "terminated": {
>     "exitCode": 137,
>     "reason": "OOMKilled"
>   }
> }
> 
> Container logs show partial clone progress before termination:
> Cloning into '/workspace/source'...
> remote: Enumerating objects: 1234567, done.
> remote: Counting objects: 100% (1234567/1234567), done.
> [terminated]

What should happen instead?
> The git-clone step should complete successfully with sufficient memory allocation.
> Either:
> - Default memory limits should be increased for git operations
> - Documentation should warn about memory requirements for large repos
> - Users should be able to override memory limits easily

Any additional context?
> - Default memory limit for step containers: 512Mi
> - Large repos require 1-2Gi for git clone operations
> - Workaround: Manually set resources.requests.memory: 2Gi in TaskRun
> - Affects: OpenShift Pipelines 1.14, Tekton Pipelines v0.56.0
> - Related: https://github.com/tektoncd/catalog/issues/xxx
```

**Component Suggestion:**
- Detected keywords: "PipelineRun", "git-clone", "step"
- Suggested component: **Tekton Pipelines**

**Result:**
- Bug created in SRVKP project
- Component: Tekton Pipelines
- Complete reproduction steps and error details
- Labels: ai-generated-jira
- Ready for engineering team to investigate

## Best Practices Summary

1. **Clear summaries:** One sentence, specific problem
2. **Complete steps:** Exact sequence to reproduce
3. **Specific results:** Include error messages and symptoms
4. **Sanitize content:** Remove all credentials and secrets
5. **Add context:** Logs, environment details, workarounds
6. **Use template:** Follow standard bug template structure
7. **Validate before submit:** Check all required fields populated

## Confirmation Flow and Workflow Summary

Follow the **Mandatory Confirmation Flow** and **MCP → CLI Fallback Decision Tree** defined
in [`../_common.md`](../_common.md). The preview label for this type is `PREVIEW: SRVKP Bug Report`.

1. ✅ **ENFORCE SRVKP-only** - reject other projects
2. 🔍 **Suggest component** from summary keywords
3. 💬 Interactively collect bug template sections
4. 📝 Format description with SRVKP template
5. 🔒 Scan for sensitive data
6. ✅ Validate required fields
7. 📋 **SHOW COMPLETE PREVIEW**
8. ❓ **GET USER CONFIRMATION (yes/no)**
9. ✅ **Create the bug** (only if confirmed) — MCP first; same payload via `acli` on fallback
10. 📤 Return issue key and URL

## See Also

- `/jira:create` - Main command that invokes this skill
- SRVKP project conventions and best practices
- OpenShift Pipelines / Tekton bug workflow documentation
