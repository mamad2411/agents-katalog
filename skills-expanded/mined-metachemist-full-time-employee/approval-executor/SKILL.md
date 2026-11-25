---
name: approval-executor
description: |
  Process approved actions from vault/Approved/ and execute them. Reads each
  APPROVAL_*.md file, identifies the action type (send_email, send_linkedin_post),
  dispatches to the correct sender skill, logs the result, and moves files to
  vault/Done/. Use when the user has moved approval files to /Approved and wants
  them executed, or when running as part of the autonomous action loop.
---

# Approval Executor

Dispatch and execute all approved actions from `vault/Approved/`.

This skill is the **final link** in the HITL chain:

```
Watcher → Needs_Action → Planning Engine → Pending_Approval
                                                    ↓ (human approves)
                                               Approved/
                                                    ↓ (this skill)
                                         Action Executed → Done/
```

## When to Use

- Manually: when the user says "execute approved actions" or "process approvals"
- In the Ralph Wiggum loop: after checking for new items in `/Approved`
- Scheduled: via cron every N minutes to run the action loop

## Workflow

### 1. Scan for Approved Actions

```bash
ls vault/Approved/APPROVAL_*.md 2>/dev/null | head -20
```

For each file found, read its `action` frontmatter field to determine what to execute.

### 2. Action Routing Table

| `action` value | Skill to use | Script |
|----------------|-------------|--------|
| `send_email` | gmail-sender | `.claude/skills/gmail-sender/scripts/send_email.py` |
| `send_linkedin_post` | linkedin-poster | `.claude/skills/linkedin-poster/scripts/create_post.py` |

### 3. Parse the Approval File

For each `vault/Approved/APPROVAL_*.md`:

**Extract these fields:**
```
action:       → determines which script to call
Target:       → recipient (name or email)
Subject/Title: → email subject or post title
Message/Content section → body / post text
```

**Example parse for email:**
```yaml
# Frontmatter
action: send_email

# From body
- **Target:** Sarah Chen <sarah.chen@example.com>
- **Subject / Title:** Re: Pricing inquiry

## Message / Content
  Dear Sarah,
  [body text with 2-space indent — strip the indent]
```

### 4. Execute Each Action

**Email:**
```bash
python .claude/skills/gmail-sender/scripts/send_email.py \
  --to "Sarah Chen <sarah.chen@example.com>" \
  --subject "Re: Pricing inquiry" \
  --body "Dear Sarah, ..."
```

**LinkedIn Post:**
```bash
python .claude/skills/linkedin-poster/scripts/create_post.py \
  --content "Post text here..."
```

### 5. Update the Vault After Each Action

**Success:**
```bash
# Move approval file to Done
mv "vault/Approved/APPROVAL_*.md" "vault/Done/"

# Update source plan status to "done"
# (find via source_plan field in approval frontmatter)

# Write audit log
echo '{"timestamp":"...","event":"action_executed","action":"send_email","to":"...","result":"success"}' \
  >> vault/Logs/$(date +%Y-%m-%d).jsonl
```

**Failure:**
- Edit the approval file: set `status: failed`, add `error: <message>`
- Move to `vault/Done/` (never leave failures in `Approved/`)
- Write error audit log entry
- Note the failure in Dashboard.md

### 6. Update Dashboard

After all actions are processed:
- Re-run `orchestrator/planning_engine.py --vault ./vault --once` to refresh counts
- OR manually update `vault/Dashboard.md` with the new `Done` count

## Batch Execution Script

Use `execute.py` to process all approved files in one pass:

```bash
python .claude/skills/approval-executor/scripts/execute.py \
  --vault ./vault \
  --dry-run          # preview without executing

python .claude/skills/approval-executor/scripts/execute.py \
  --vault ./vault    # execute all pending approvals
```

Output per action:
```
[SEND_EMAIL        ] Sarah Chen <sarah@example.com> → sent ✓  (msg_id: 18e4bc...)
[SEND_LINKEDIN_POST] Post published ✓  (url: https://linkedin.com/...)
```

## Error Recovery

| Situation | Recovery |
|-----------|----------|
| Script exits non-zero | Log error, mark file `status: failed`, move to Done |
| Session expired | Halt execution, alert user, write `requires_reauth: true` to failed file |
| Contact not found | Mark `status: failed_contact_not_found`, move to Done, log |
| Rate limit hit | Pause 60 s, retry once, then halt and alert |
| Network error | Retry 3× with exponential backoff |

## Rules (non-negotiable)

- **Never** execute an action from `Pending_Approval/` — only from `Approved/`
- **Never** re-execute an action whose file has `status: sent` or `status: failed`
- **Always** log every execution attempt to `vault/Logs/`
- **Always** move the approval file to `vault/Done/` after execution (success or fail)
- **Max 20 actions per hour** across all action types combined
- **Always** read `Company_Handbook.md` if unsure whether an action is permitted

## Quick Status Check

```bash
# Count pending approvals
ls vault/Approved/ | grep -c "APPROVAL_"

# Show what types are pending
grep -h "^action:" vault/Approved/APPROVAL_*.md 2>/dev/null | sort | uniq -c
```
