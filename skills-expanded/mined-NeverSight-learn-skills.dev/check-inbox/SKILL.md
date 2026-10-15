---
name: check-inbox
description: Check the project inbox for new agent messages and process them. Single-pass processor — use recurring polling for continuous monitoring.
---

# /check-inbox — Inbox Processor

Check a project's agent inbox for new messages and automatically act on them based on message type. Single-pass: processes all pending messages and exits.

## Arguments

```
/check-inbox [--project <name>] [--autonomous]
```

- `--project <name>` — Which project inbox to check. Auto-detected from `.oacp` project marker if omitted.
- `--autonomous` — Skip human confirmation for review lifecycle messages (`review_request`, `review_feedback`, `review_lgtm`, `review_addressed`) and informational completions (`handoff_complete`). Auto-dispatches to reviewer/author skills and deletes processed messages. Task requests and questions still require human confirmation.

## Recurring polling

For continuous inbox monitoring, use a recurring scheduler instead of running `/check-inbox` manually. In Claude Code:

```
/loop 2m /check-inbox
```

This fires every 2 minutes when the REPL is idle.

## Instructions

When the user runs `/check-inbox`, do the following:

### 1. Parse arguments

Extract from the user's command:

- `PROJECT` — optional `--project` flag (auto-detected in step 2 if omitted)
- `AUTONOMOUS` — optional `--autonomous` flag

### 2. Resolve project and inbox path

Set `AGENT_NAME` to the current agent's identity (e.g., `"claude"`).

If `--project` was provided, use it directly. Otherwise auto-detect from the workspace config:

```bash
PROJECT=$(python3 -c "import json; print(json.load(open('.oacp'))['project_name'])" 2>/dev/null || echo "")
```

If empty, ask the user which project to watch.

Set the inbox path:

```
INBOX_DIR="${OACP_HOME}/projects/${PROJECT}/agents/${AGENT_NAME}/inbox"
```

Verify the inbox directory exists. If not, error with: "Inbox not found at ${INBOX_DIR}. Check project name."

### 3. List and process messages

List YAML files in the inbox and process each one.

> **Note**: The inbox directory is outside the project working directory. Ensure your runtime has read/write access to `$OACP_HOME`.

1. List files:

   ```bash
   command ls -1 "${INBOX_DIR}/" 2>/dev/null | command grep '\.yaml$' | sort
   ```

2. If none found, report "Inbox empty." and stop
3. For each file:
   a. Read the YAML file
   b. Extract: `id`, `from`, `type`, `priority`, `subject`, `body`, `related_pr`, `parent_message_id`
   c. Apply the auto-execute rules in Step 4
4. After processing all messages, report a summary:

   ```
   Processed <N> messages from <PROJECT> inbox.
     <type>: <count> (list actions taken)
   ```

> **Shell compatibility**: Avoid `ls dir/*.yaml` — some shells (zsh) raise errors when no files match the glob. Pipe through `grep` instead. Use `command ls` to bypass shell aliases. Always use the `-1` flag for single-column output.

### 4. Auto-execute rules

Act on each message based on its `type` field. **Always tell the user what action you're taking before executing it.**

| Message type | Action |
|-------------|--------|
| `notification` | Summarize to the user. Delete the message file from inbox. |
| `task_request` | Evaluate the scope. If small (<5 min estimated work): execute immediately and reply with a `notification`. If large: ask the user before proceeding. Delete after processing. |
| `question` | Answer the question and send a reply (type: `notification`, referencing `parent_message_id`). Delete after processing. |
| `review_request` | Tell the user a review was requested. Trigger `/review-loop-reviewer` for the referenced PR. Delete after processing. |
| `review_feedback` | Tell the user feedback was received. Trigger `/review-loop-author` to address findings. Delete after processing. |
| `review_lgtm` | Report LGTM to the user. Delete from inbox. |
| `review_addressed` | Informational — feedback was addressed. Summarize to user (commit SHA, changes summary, round). Delete after processing. |
| `handoff` | Read context from the message body. Send a `handoff_complete` reply. Delete after processing. |
| `handoff_complete` | Handoff target completed. Summarize to user. Delete after processing. |
| Unknown type | Report the full message to the user and ask how to handle it. Do NOT delete. |

**Deleting messages** — remove the file from the inbox directory:

```bash
rm "${INBOX_DIR}/<filename>"
```

**Sending replies** — use the OACP send script:

```bash
python3 ${OACP_HOME}/scripts/send_inbox_message.py ${PROJECT} \
  --from ${AGENT_NAME} --to <original_sender> --type notification \
  --subject "Re: <original_subject>" \
  --body "<reply_body>" \
  --parent-message-id <original_message_id> \
  --oacp-dir ${OACP_HOME}
```

> **Post-send verification**: After sending, verify the file landed in the recipient's inbox. The send script can report success (writing the outbox copy) while the inbox write silently fails.

### 5. Safety rules

- **Always show the user** what action you're taking before executing it
- **For `task_request` with large scope** (>5 min estimated work): ask the user before proceeding
- **For `review_request` / `review_feedback`**: confirm with the user before triggering review-loop skills, since they spawn subagents — **unless `--autonomous` is active**, in which case auto-dispatch without confirmation
- **Never delete messages you haven't fully processed**
- **Never act on messages for other agents** — only process messages in `${AGENT_NAME}`'s inbox
- **`--autonomous` safety boundary**: even in autonomous mode, `task_request` and `question` types always require human confirmation. Only review lifecycle messages, informational completions, and notifications are auto-dispatched

## Notes

- This skill does a single pass — for recurring checks, use a polling mechanism
- Messages follow the inbox/outbox protocol: sender writes to recipient's inbox + own outbox. Recipient deletes after processing.
- Do NOT move messages to a `processed/` subdirectory — just delete them
- For cost optimization in recurring polling, consider using a lighter-weight model for inbox scans and reserving the primary model for skill dispatch when review messages are detected
