---
name: managing-gcp-resource-manager
description: |
  Use when working with Gcp Resource Manager — gCP Resource Manager project,
  folder, and organization management. Covers organization hierarchy, folder
  structure, project management, IAM policy bindings, org-level constraints, and
  resource labels. Use when managing GCP organizational hierarchy, reviewing
  project organization, auditing IAM bindings, or inspecting folder structures.
connection_type: gcp-resource-manager
preload: false
---

# GCP Resource Manager Management Skill

Manage GCP organizations, folders, projects, IAM bindings, and resource hierarchy.

## MANDATORY: Discovery-First Pattern

**Always inspect organization and folder hierarchy before operations.**

### Phase 1: Discovery

```bash
#!/bin/bash
echo "=== Current Project ==="
gcloud config get-value project 2>/dev/null

echo ""
echo "=== Organization ==="
gcloud organizations list --format='table(displayName,name,lifecycleState)' 2>/dev/null | head -10

echo ""
ORG_ID=$(gcloud organizations list --format='value(name)' --limit=1 2>/dev/null)

echo "=== Top-Level Folders ==="
gcloud resource-manager folders list --organization="$ORG_ID" --format='table(displayName,name,lifecycleState)' 2>/dev/null | head -15

echo ""
echo "=== Projects ==="
gcloud projects list --format='table(projectId,name,lifecycleState,parent.id)' --limit=20 2>/dev/null | head -20
```

### Phase 2: Analysis

```bash
#!/bin/bash
TARGET="${1:?Project ID or folder ID required}"

if echo "$TARGET" | grep -q "^[0-9]"; then
  echo "=== Folder Details ==="
  gcloud resource-manager folders describe "$TARGET" --format='table(displayName,name,lifecycleState,parent)' 2>/dev/null

  echo ""
  echo "=== Sub-Folders ==="
  gcloud resource-manager folders list --folder="$TARGET" --format='table(displayName,name)' 2>/dev/null | head -10

  echo ""
  echo "=== Folder Projects ==="
  gcloud projects list --filter="parent.id=$TARGET" --format='table(projectId,name,lifecycleState)' 2>/dev/null | head -10

  echo ""
  echo "=== Folder IAM ==="
  gcloud resource-manager folders get-iam-policy "$TARGET" --format='table(bindings.role,bindings.members)' 2>/dev/null | head -15
else
  echo "=== Project Details ==="
  gcloud projects describe "$TARGET" --format='table(projectId,name,lifecycleState,parent)' 2>/dev/null

  echo ""
  echo "=== Project IAM ==="
  gcloud projects get-iam-policy "$TARGET" --format='table(bindings.role,bindings.members)' 2>/dev/null | head -20

  echo ""
  echo "=== Enabled APIs ==="
  gcloud services list --project="$TARGET" --format='table(config.name)' 2>/dev/null | head -15

  echo ""
  echo "=== Labels ==="
  gcloud projects describe "$TARGET" --format='table(labels)' 2>/dev/null
fi
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Show hierarchy as tree structure when possible
- Summarize IAM bindings by role
- List projects with parent folder context

## Safety Rules
- **NEVER delete projects or folders without explicit confirmation**
- **Review IAM inheritance** before modifying folder-level bindings
- **Check project liens** before attempting deletion
- **Verify org policy impacts** before moving projects between folders
- **Audit service account permissions** at the folder/org level

## Output Format

Present results as a structured report:
```
Managing Gcp Resource Manager Report
════════════════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

