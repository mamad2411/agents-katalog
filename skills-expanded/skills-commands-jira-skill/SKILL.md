---
name: Jira Issue Management
description: Create and manage Jira issues (bugs, epics, stories, tasks) for SRVKP project with intelligent routing and project-specific conventions
invocation_pattern: /jira:create <type>
---

# Jira Issue Management

This skill provides a unified interface for creating Jira issues in the **SRVKP project** with intelligent routing to specialized sub-skills based on issue type.

## ⚠️ CRITICAL RESTRICTIONS

**PROJECT RESTRICTION:**
- ✅ **ONLY SRVKP project** is supported
- ❌ All other projects are **DISABLED** (OCPBUGS, CNTRLPLANE, etc.)
- Any attempt to use other projects will be rejected

**CONFIRMATION REQUIRED:**
- ✅ **MUST show complete issue preview** before creation
- ✅ **MUST get explicit user confirmation** (yes/no)
- ❌ **NEVER create issues** without user approval
- ❌ **NEVER auto-create** or "assume" confirmation

**PROJECT-SPECIFIC CONVENTIONS:**
- ✅ **Auto-suggest components** based on summary context
- ✅ **Apply SRVKP-specific templates** for each issue type
- ✅ **Provide component list** when needed
- ✅ **Validate required fields** for SRVKP

## Authentication and Automatic Fallback

### MCP → CLI Fallback Decision Tree

When creating or searching Jira issues, follow this decision tree — **no exceptions**:

```
Step 1 ─── Call MCP tool
           mcp__atlassian__jira_create_issue(project_key="SRVKP", ...)

Step 2 ─── Inspect result
           │
           ├─ SUCCESS (result contains issue key)
           │   └─ Return issue key and URL to user ✓
           │
           └─ ERROR (result contains any of the following messages)
               • "Tool rejected: User rejected MCP"
               • "MCP server does not exist"
               • "Connection refused" / timeout
               │
               └─ Step 3: Switch to CLI fallback
                   Run: acli jira workitem create
                        --project "SRVKP"
                        --type   "<same type>"
                        --summary "<same summary>"
                        --description "$(cat <<'EOF' ... EOF)"
                        [--parent "<same parent>"]
                        --label "ai-generated-jira"
                        --json
                   (Same parameters, same field values — payload-identical)
                   └─ Return issue key and URL to user ✓
```

> The LLM cannot catch MCP exceptions in code. Instead, **check whether the tool result
> contains an error message** (step 2) and branch accordingly.

Full `acli` command syntax and examples: [`reference/cli-fallback.md`](reference/cli-fallback.md)

### CLI Authentication (One-Time Setup)

If falling back to CLI, ensure authentication is configured. **Use your own Red Hat Jira email** in `--email` and **store your API token outside this repo** (the examples use `~/.jira.d/token`; you may use another path and adjust `--token` accordingly).

**One-Time Setup:**

1. **Generate API token** (only if you don't have one):
   - Visit: https://id.atlassian.com/manage-profile/security/api-tokens
   - Click "Create API token"
   - Copy the token (you won't see it again!)

2. **Store token locally** (only if not already stored):
   ```bash
   echo "YOUR_API_TOKEN" > ~/.jira.d/token
   chmod 600 ~/.jira.d/token
   ```

**Authenticate (safe to run multiple times):**
```bash
acli jira auth login \
  --site "https://issues.redhat.com" \
  --email "YOUR_REDHAT_ID@redhat.com" \
  --token < ~/.jira.d/token
```

**Note:** This command uses your existing token - it doesn't create new ones. Running it again will just re-authenticate using the same token.

**Verify Authentication:**
```bash
acli jira me
```

**Expected Output:**
```
✓ Authentication successful
  Welcome, <your Jira display name>
```

**When CLI is Used:**
- Issue creation uses `acli jira workitem create` commands
- Search uses `acli jira workitem search --jql "<query>"`
- Field queries use `acli jira field list`
- Project info uses `acli jira project list`

**Issue Creation Examples:**
```bash
# Simple issue creation
acli jira workitem create \
  --project "SRVKP" \
  --type "Epic" \
  --summary "Epic title" \
  --description "$(cat <<'EOF'
Epic description with Jira wiki markup.

h2. Epic Objective
Enable feature X for users

h2. Acceptance Criteria
# Criterion 1
# Criterion 2
EOF
)" \
  --label "ai-generated-jira" \
  --json

# Issue creation with parent link
acli jira workitem create \
  --project "SRVKP" \
  --type "Story" \
  --summary "Story title" \
  --description "$(cat <<'EOF'
As a user, I want to do X, so that I can achieve Y.

h2. Acceptance Criteria
* Test that behavior 1 works
* Test that behavior 2 works
EOF
)" \
  --parent "SRVKP-12345" \
  --label "ai-generated-jira" \
  --json
```

**Note:** Use here-doc with `$(cat <<'EOF' ... EOF)` for multi-line descriptions with wiki markup. No temp files needed.

**Search Examples:**
```bash
# Search for epics
acli jira workitem search \
  --jql 'project = SRVKP AND issuetype = Epic AND summary ~ chains' \
  --fields "key,summary,status" \
  --json

# Search for features
acli jira workitem search \
  --jql 'project = SRVKP AND issuetype = Feature' \
  --fields "key,summary,status" \
  --json
```

**Note:** The skill will automatically detect if MCP is unavailable and use CLI commands as fallback.

## Invocation

```bash
/jira:create <type> [SUMMARY] [OPTIONS]
```

**Note:** Project is always SRVKP - you don't need to specify it.

**Supported issue types:**
- `bug` - Bug reports with reproduction steps
- `epic` - Epics with scope and acceptance criteria
- `feature` - Strategic features containing multiple epics
- `story` - User stories with acceptance criteria
- `task` - Technical/operational tasks

## Usage Examples

```bash
/jira:create bug "Pipeline fails when using workspaces with PVC"
/jira:create epic "Recursive Image Manifest signing in Tekton Chains"
/jira:create feature "Tekton Chains Signing Enhancements"
/jira:create story "Enable pipeline caching for faster builds"
/jira:create task "Update Tekton Chains documentation for v0.20"
```

## How It Works

This skill acts as a dispatcher:

1. **Enforce SRVKP-only**: Reject any project other than SRVKP
2. **Parse command**: Extract issue type, summary, and options
3. **Route to sub-skill**: Delegate to the appropriate creation skill
4. **Apply SRVKP conventions**: Auto-suggest components, apply templates
5. **Interactive guidance**: Sub-skills guide you through required fields
6. **Preview and confirm**: Show complete issue before creation
7. **Create only after approval**: User must explicitly confirm

## Issue Types

### Bug (`/jira:create bug`)
Creates detailed bug reports with:
- Problem description
- Steps to reproduce
- Actual vs expected results
- Environment details

**Delegates to:** `create-bug/SKILL.md`

### Epic (`/jira:create epic`)
Creates epics with:
- Epic objective and scope
- Acceptance criteria
- Timeline and dependencies
- Parent feature linking (with auto-discovery and creation)
- Duplicate detection

**Delegates to:** `create-epic/SKILL.md`

### Feature (`/jira:create feature`)
Creates strategic features with:
- Strategic objective and business value
- Strategic outcomes and success metrics
- Planned epics
- Timeline (multi-quarter)

**Delegates to:** `create-feature/SKILL.md`

### Story (`/jira:create story`)
Creates user stories with:
- "As a... I want... So that..." format
- Acceptance criteria
- Parent epic linking

**Delegates to:** `create-story/SKILL.md`

### Task (`/jira:create task`)
Creates technical tasks with:
- Description of technical work
- Motivation/context
- Acceptance criteria
- Technical details

**Delegates to:** `create-task/SKILL.md`

## Command Syntax

### Basic Syntax

```bash
/jira:create <type> "<summary>"
```

**Examples:**
```bash
/jira:create bug "Authentication service returns 500 error"
/jira:create story "Enable service health dashboard"
```

### With Options

```bash
/jira:create <type> "<summary>" --parent <parent-key> --component "<component>"
```

**Examples:**
```bash
/jira:create story "Add metrics endpoint" --parent SRVKP-100
/jira:create task "Update monitoring config" --component "Infrastructure"
/jira:create bug "Memory leak in API service" --component "Backend Services"
```

### Short Form (Interactive)

If summary is omitted, you'll be prompted:

```bash
/jira:create bug
# Will prompt for summary and guide through all fields
```

## Options

### Common Options

| Option | Description | Example |
|--------|-------------|---------|
| `--parent <key>` | Link to parent epic/feature | `--parent SRVKP-100` |
| `--component <name>` | Set component (or accept suggestion) | `--component "Backend Services"` |
| `--labels <label1,label2>` | Add labels | `--labels "urgent,regression"` |

### Parent Linking

Different issue types use different parent relationships:

- **Story → Epic**: Uses Epic Link field
- **Epic → Feature**: Uses Parent Link field  
- **Task → Story/Epic**: Can use standard parent field

The appropriate field is selected automatically based on issue type and parent type.

## SRVKP Component Suggestions

Components are auto-suggested based on keywords in your summary. The authoritative keyword
→ component mapping and full component list are in [`_common.md`](_common.md).

## Implementation Logic

### Step 1: Enforce SRVKP-Only

```
If user specifies a project other than SRVKP:
  → Reject immediately with:
    "❌ ERROR: This skill only works with SRVKP project.
     You specified: <project>
     Correct usage: /jira:create <type> '<summary>'"
  → Stop processing

Always set project = "SRVKP"
```

### Step 2: Parse Command

Extract components from the command:

```
/jira:create bug "API crashes" --component "Backend Services"
            ↓    ↓                     ↓
         type   summary            options
```

### Step 3: Validate Issue Type

Check that the issue type is supported:
- ✅ `bug`, `epic`, `feature`, `story`, `task`
- ❌ Invalid type → Show usage and supported types

### Step 4: Route to Sub-Skill

Based on issue type, read and invoke the appropriate sub-skill:

| Type | Sub-skill |
|------|-----------|
| `bug` | `create-bug/SKILL.md` |
| `epic` | `create-epic/SKILL.md` |
| `feature` | `create-feature/SKILL.md` |
| `story` | `create-story/SKILL.md` |
| `task` | `create-task/SKILL.md` |

### Step 5: Pass Context

Pass parsed arguments to the sub-skill:
- Project key (always "SRVKP")
- Summary
- Component (if specified, otherwise will be suggested)
- Parent (if specified)
- Additional options

### Step 6: Sub-Skill Execution

The sub-skill handles:
- Component suggestion based on summary keywords
- Interactive field collection
- Apply SRVKP-specific templates
- Validation
- **PREVIEW issue** with all fields
- **REQUIRE user confirmation** (yes/no)

### Step 7: Create Only After Confirmation

```
Show complete preview of all fields
↓
Ask: "Create this issue? (yes/no): "
↓
Wait for explicit response
├─ "yes" → call MCP tool; if MCP returns an error → run acli fallback (same payload)
│           return issue key and URL
└─ "no"  → "Issue creation cancelled. No changes made to Jira."
            Offer: 1) modify details and retry  2) cancel completely
```

## SRVKP Project-Specific Conventions

This skill is **exclusively for SRVKP** (OpenShift Pipelines project).

### Auto-Applied Conventions

- **Project**: Always SRVKP
- **Labels**: Automatically add "ai-generated-jira"
- **Component Suggestions**: Based on summary keywords
- **Templates**: Issue-type specific templates for SRVKP

### Component Detection

The keyword → component mapping is defined in [`_common.md`](_common.md) (single source of truth).

### Required Fields for SRVKP

**All issue types:**
- Summary (clear, specific)
- Description (detailed, formatted)
- Component (suggested or manual)

**Bugs:**
- Steps to reproduce
- Actual vs expected results
- Version (if applicable)

**Stories:**
- User story format ("As a... I want... So that...")
- Acceptance criteria (at least 2)

**Epics:**
- Epic objective and scope
- Epic acceptance criteria
- Timeline

**Tasks:**
- Description of work
- Motivation/context
- Acceptance criteria (recommended)

## Error Handling

### Wrong Project Specified

```bash
/jira:create bug OCPBUGS "Summary"
```

**Response:**
```
❌ ERROR: This skill only works with SRVKP project.

You specified: OCPBUGS
This skill is restricted to: SRVKP

Correct usage:
  /jira:create bug "Summary"
  
The project is automatically set to SRVKP - you don't need to specify it.
```

### Invalid Issue Type

```bash
/jira:create widget "Summary"
```

**Response:**
```
Invalid issue type "widget".

Supported types:
  /jira:create bug      - Bug reports
  /jira:create epic     - Epics
  /jira:create feature  - Strategic features
  /jira:create story    - User stories
  /jira:create task     - Technical tasks

Usage: /jira:create <type> "<summary>" [options]
```

### Missing Arguments

```bash
/jira:create bug
```

**Response:**
```
Let me help you create a bug report for SRVKP project.

What is the bug summary?
> 
```

### User Cancels Confirmation

```bash
Create this issue? (yes/no): no
```

**Response:**
```
Issue creation cancelled. No changes made to Jira.

Would you like to:
1. Modify the issue details and try again
2. Cancel completely
```

### MCP Server Unavailable

If MCP Atlassian server is not available:
1. Check MCP server status
2. Provide clear error message
3. Suggest checking server configuration

## Prerequisites

### Required

- ✅ **MCP Atlassian server** (primary) — configured and running in Cursor → Settings → MCP
- ✅ **`acli`** (automatic fallback) — installed and authenticated for when MCP is unavailable
- ✅ User has permission to create issues in SRVKP project

See [README.md](README.md) for full install and auth instructions for both paths.

### Verification

1. **MCP:** In Cursor, open **Settings → MCP** and confirm the Atlassian Jira server is enabled, connected, and lists Jira tools.
2. **acli:** Run `acli jira me` — expected output: `✓ Authentication successful`.

## Sub-Skill Documentation

For detailed information about each issue type:

- **Bugs**: See `create-bug/SKILL.md`
  - Bug report best practices
  - Reproduction steps template
  - Component and version handling
  - Security validation

- **Epics**: See `create-epic/SKILL.md`
  - Epic scoping guidelines
  - Epic vs Feature vs Story
  - Parent linking to features
  - Acceptance criteria for epics

- **Stories**: See `create-story/SKILL.md`
  - User story format ("As a... I want... So that...")
  - Acceptance criteria formats
  - Story sizing and splitting
  - Epic linking

- **Tasks**: See `create-task/SKILL.md`
  - Task vs Story distinction
  - Technical task best practices
  - Investigation task patterns
  - Parent linking

## Reference Documentation

- **Shared conventions:** [`_common.md`](_common.md) — safety rules, component table, confirmation flow, MCP→CLI fallback
- **CLI fallback:** [`reference/cli-fallback.md`](reference/cli-fallback.md) — `acli` command syntax and examples
- **Prerequisites & setup:** [`README.md`](README.md) — install guide, test plan, file layout

## Safety Rules

⚠️ **CRITICAL SAFETY RULES:**

1. **SRVKP ONLY** - Reject all other projects immediately
2. **CONFIRMATION REQUIRED** - MUST show preview and get explicit "yes" before creating
3. **NEVER AUTO-CREATE** - Never create issues without user approval
4. **NEVER DELETE ISSUES** - All skills are for creation only
5. **NEVER use `jira_delete_issue`** MCP tool
6. **Validate sensitive data** - Scan for credentials, API keys, secrets
7. **Create, don't delete** - If issue created incorrectly, create a new one

### Confirmation Flow (MANDATORY)

```
1. Collect all required fields
2. Apply SRVKP conventions and templates
3. Show complete issue preview:
   
   ═══════════════════════════════════
   PREVIEW: SRVKP Bug Report
   ═══════════════════════════════════
   
   Project: SRVKP
   Type: Bug
   Summary: [summary]
   Component: [component] (suggested)
   Description:
   [formatted description]
   
   ═══════════════════════════════════

4. Ask: "Create this issue? (yes/no): "
5. Wait for response
6. Only create if response is "yes"
7. If "no", offer to modify or cancel
```

## Dispatcher Logic (step-by-step)

```
Input: /jira:create bug 'Authentication service returns 500' --component 'Backend Services'

1. Parse command → type=bug, summary="...", component="Backend Services"

2. Enforce SRVKP-only
   If project specified and ≠ SRVKP → reject (see Step 1 above)
   Always set project = "SRVKP"

3. Validate type
   Allowed: bug | epic | feature | story | task
   Otherwise → show usage and supported types

4. Suggest component (if not provided)
   Scan summary for keywords → pick from component table in _common.md

5. Read and invoke sub-skill
   create-bug/SKILL.md  ← receives: project, type, summary, component, options

6. Sub-skill handles (in order):
   a. Component suggestion / confirmation
   b. Interactive field collection
   c. Apply SRVKP templates
   d. Show complete PREVIEW
   e. Ask "Create this bug? (yes/no)"
   f. On "yes": MCP call → if error → acli fallback (same payload)
   g. Return issue key and URL
```

## Workflow Summary

```
User invokes: /jira:create <type> ...
        ↓
Enforce SRVKP-only (reject other projects)
        ↓
Parse command arguments
        ↓
Validate issue type
        ↓
Suggest component based on summary keywords
        ↓
Route to appropriate sub-skill
        ↓
Sub-skill applies SRVKP templates
        ↓
Sub-skill collects required fields interactively
        ↓
SHOW COMPLETE PREVIEW of issue
        ↓
GET EXPLICIT USER CONFIRMATION (yes/no)
        ↓
If YES: Create issue (MCP first; same payload via `acli` on fallback)
        ↓
Return issue key and URL
        ↓
If NO: Offer to modify or cancel
```

## Practical Examples with Component Suggestions

### Bug Examples

```bash
# Pipeline execution issue
/jira:create bug "TaskRun fails with OOMKilled error in step container"
# → Suggests: Tekton Pipelines

# Signing/attestation issue
/jira:create bug "Tekton Chains signature verification fails for OCI images"
# → Suggests: Tekton Chains

# Event/webhook issue
/jira:create bug "EventListener returns 500 on GitHub webhook"
# → Suggests: Tekton Triggers

# CLI issue
/jira:create bug "tkn pipeline start hangs on large pipeline definitions"
# → Suggests: Tekton Cli
```

### Story Examples

```bash
# Caching feature
/jira:create story "Enable result caching for pipeline tasks"
# → Suggests: Tekton Cache

# UI enhancement
/jira:create story "Add pipeline visualization in dashboard"
# → Suggests: UI

# PipelineAsCode feature
/jira:create story "Support GitLab merge request triggers in PipelineAsCode"
# → Suggests: Pipeline as Code
```

### Epic Examples

```bash
# Multi-component epic
/jira:create epic "Enhanced supply chain security and provenance"
# → Suggests: Tekton Chains

# Results improvement
/jira:create epic "Scalable results storage and querying"
# → Suggests: Tekton Results
```

### Task Examples

```bash
# Documentation task
/jira:create task "Update Operator installation guide for OpenShift 4.16"
# → Suggests: Operator

# Cleanup/maintenance
/jira:create task "Configure pruner retention policy for production"
# → Suggests: Pruner
```

## Best Practices

1. **Use specific issue types**: Don't use "bug" for user stories or vice versa
2. **Provide clear summaries**: Help the skill with good initial input
3. **Use Tekton terminology**: Keywords help suggest the right component
4. **Let sub-skills guide**: Interactive prompts ensure completeness
5. **Review before submit**: Confirm fields before creation
6. **Link related work**: Use `--parent` to maintain issue hierarchy

## Troubleshooting

### Issue Type Selection

**Q: Should this be a Bug or Task?**
- Bug: Something is broken, needs fixing, has reproduction steps
- Task: Technical work, documentation, refactoring

**Q: Should this be a Story or Task?**
- Story: User-facing functionality, delivers user value
- Task: Internal/technical work, not visible to end users

**Q: Should this be an Epic or Feature?**
- Epic: Body of work for one quarter, 2-8 sprints
- Feature: Strategic initiative, multiple quarters, multiple epics

### Common Issues

**"MCP server not found" or "User rejected MCP"**

If the MCP Jira server is not working, use the **CLI fallback** (see Authentication section above):

1. **Authenticate with Jira CLI:**
   ```bash
   acli jira auth login \
     --site "https://issues.redhat.com" \
     --email "YOUR_REDHAT_ID@redhat.com" \
     --token < ~/.jira.d/token
   ```

2. **Verify authentication:**
   ```bash
   acli jira me
   # Expected: ✓ Authentication successful
   ```

3. **Retry issue creation:**
   The skill will automatically use CLI commands instead of MCP.

**CLI Setup Issues:**

**Error: `acli: command not found`**
- Install Atlassian CLI tools from: https://bobswift.atlassian.net/wiki/spaces/ACLI/overview
- Add to PATH if needed

**Error: `Authentication failed`**
- Verify API token in `~/.jira.d/token`
- Get token from: https://id.atlassian.com/manage-profile/security/api-tokens
- Check token hasn't expired
- Verify email matches Jira account

**Error: `Site not found`**
- Verify site URL is correct: `https://issues.redhat.com`
- Check network connectivity to Jira

**"Permission denied"**
- Verify user has create permission in SRVKP project
- Check authentication credentials
- Confirm project key is correct (SRVKP)

**"Field required" errors**
- Sub-skill will prompt for missing fields
- Some projects have specific required fields
- Provide requested information when prompted

## See Also

- [Create Bug Skill](create-bug/SKILL.md) - Bug report creation
- [Create Epic Skill](create-epic/SKILL.md) - Epic creation
- [Create Story Skill](create-story/SKILL.md) - User story creation
- [Create Task Skill](create-task/SKILL.md) - Task creation
- MCP Atlassian server documentation
- SRVKP project conventions and Tekton component documentation
