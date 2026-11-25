---
name: vibe-report-issue
description: Report an issue with vibe by summarizing the current conversation, describing the problem, and filing a GitHub issue in the vibe repo. Use when something went wrong, a skill didn't invoke correctly, or results were unexpected.
---

# Vibe Report Issue

Reports issues with vibe skills, agents, or behavior by collecting context from the current conversation and filing a GitHub issue.

## Instructions

### Step 1: Summarize the Conversation

Review the current conversation and create a concise summary that captures:

- What the user was trying to accomplish
- Which skills were invoked (by name, e.g. `fe-google-tools:gmail`)
- Which tool calls were made (tool names only, e.g. `Bash`, `Read`, `Skill`, `Task`)
- What the outcome was

**CRITICAL - Sanitize for sensitive information:**
- NEVER include API keys, tokens, passwords, or credentials
- NEVER include personal email content, message bodies, or private data
- NEVER include customer names, account details, or internal business data
- NEVER include file contents that may contain secrets
- Replace any sensitive values with `[REDACTED]`
- Only include skill names, tool names, error messages, and general behavioral descriptions

Present the summary to the user and ask them to confirm it looks correct before proceeding.

### Step 2: Prompt the User for Issue Details

Use AskUserQuestion to gather the following:

**Question 1: What type of issue is this?**
- "Unexpected result" - A skill or agent produced an incorrect or unexpected output
- "Wrong skill invoked" - The wrong skill was triggered for the prompt
- "Skill not invoked" - A skill that should have been triggered was not
- "Error or failure" - A skill or tool call failed with an error

**Then ask the user to describe the issue in their own words:**

Use AskUserQuestion or ask them directly:
- What did you expect to happen?
- What actually happened?
- Any additional context?

### Step 3: Create the GitHub Issue

Use `gh` to create the issue in the vibe repo.

```bash
gh issue create \
  --repo databricks-field-eng/vibe \
  --title "[Bug Report] <short description>" \
  --body "$(cat <<'EOF'
## Issue Type
<type from step 2>

## Conversation Summary
<sanitized summary from step 1>

## Skills Invoked
<list of skills that were invoked during the session, or "None">

## Tool Calls
<list of tool types used, e.g. Bash, Read, Skill, Task - no sensitive arguments>

## Expected Behavior
<what the user expected>

## Actual Behavior
<what actually happened>

## Additional Context
<any extra details from the user>

---
*Filed via vibe-report-issue skill*
EOF
)" \
  --label "bug"
```

**After creating the issue:**
- Display the issue URL to the user
- Thank them for reporting the issue

### Important Notes

- If `gh` is not authenticated, instruct the user to run `gh auth login` first
- If the `bug` label doesn't exist, omit the `--label` flag and create without it
- Always confirm the sanitized summary with the user before filing
- Keep the issue concise but include enough detail to be actionable
