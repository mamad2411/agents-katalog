---
name: cron-agent-flow
title: Agent-in-the-Loop Cron Pipeline
description: Design pattern for Hermes cron jobs where a script collects data and the LLM agent does reasoning + action. Use this for any "fetch on schedule, judge, then take action" workflow.
tags: [cron, agent, pipeline, data-collection, classification]
triggers:
  - New cron job that needs LLM judgment between data collection and action
  - Replacing an old cron that used skill dependencies or Python heuristics
  - Any "fetch data on schedule, then decide what to do" pattern
---

# Agent-in-the-Loop Cron Pipeline

## Why This Pattern

Simple cron scripts (no_agent=true) work for pure watchdog/notification tasks, but many workflows need judgment: classify emails, rank results, decide if something is actionable. Using an LLM agent in the cron (default no_agent=false) gives you flexible reasoning without maintaining brittle heuristic code.

## Architecture

```
[Schedule fires]
     |
     v
+---------------------+
| Script (data pipeline)|  <- no_agent=false, script: field
| - fetch raw data     |
| - extract/parse/clean|
| - output structured JSON|
| - can also do DB writes|
|   (but NO classification)|
+---------+-----------+
          | stdout injected as context
          v
+---------------------+
| LLM Agent           |  <- the prompt: field
| - receives JSON     |
| - classifies/judges |
| - produces summary  |
| - calls actions     |
|   (mark-read, etc.) |
| - updates state     |
+---------------------+
          |
          v
   Deliver to user
```

## Key Design Rules

### 1. Script = Pure Data Pipeline

The script (~/.hermes/scripts/) should:
- Accept a mode/arg for time window or scope
- Fetch data from source (Apple Mail SQLite, web API, file system)
- Extract full content (not truncated) for the LLM to reason over
- Output clean structured JSON
- Provide DB mutation actions (mark-read, flag, update-state) as separate --action flags
- NEVER hardcode classification rules, business logic, or judgment heuristics

Good trigger: when you start reaching for keyword lists, sender blacklists, or regex patterns in Python -- stop, put that logic in the cron prompt instead.

### 2. Rules in Context (Preferred for Maintainability)

Put decision rules in a separate file, referenced by the shell wrapper script. The wrapper outputs the rules file content, then the email data, as the LLM's context:

```bash
#!/bin/bash
# email-triage-2pm.sh
cat ~/.hermes/skills/email-triage/rules.md   # rules go into context
echo ""
echo "=== EMAIL DATA ==="
echo ""
exec python3 ~/.hermes/scripts/email_triage.py --window 2pm
```

The cron prompt then only carries operational instructions (what to do, not how to judge):

```yaml
script: email-triage-2pm.sh     # outputs rules + data
prompt: |
  The context has two sections:
  1. === CLASSIFICATION RULES === : sorting rules
  2. === EMAIL DATA === : data with previously_reported_ids
  
  Classify each email NOT in previously_reported_ids.
  Output in English. Only show IMPORTANT items.
  
  1. Mark UNIMPORTANT as read: terminal -> python3 ... --action mark-read --ids <IDS>
  2. Flag IMPORTANT: terminal -> python3 ... --action flag --ids <IDS>
  3. Update state: terminal -> python3 ... --action update-state --ids <ALL new IDs>
```

This keeps classification rules in an editable file (edit rules.md = all 4 crons pick up changes) while keeping the cron prompt focused on actions.

### 3. Prompt with Inline Rules (Alternative)

If a separate rules file is not desirable, the prompt can carry rules inline. This is less maintainable (editing rules means editing N cron jobs).

### 4. State File for Dedup (Legacy Pattern)

Many workflows process data on a rolling window and need to avoid re-reporting the same items:
- Use a JSON state file at ~/.hermes/scripts/<workflow>_state.json
- The script reads the state and includes previously_reported_ids in its output
- The LLM agent updates the state after processing via --action update-state
- State file contains: { "reported_ids": [int], "last_run": "iso-timestamp" }

### 4b. Date-Window Approach (Alternative to State File)

Instead of maintaining a persistent state file, define "new" items as those received after a fixed cutoff (e.g. midnight of the current day). This is simpler because:

- No state file to manage, no dedup logic
- Every run fetches the same time window and re-classifies — the LLM's judgment determines what's "newsworthy"
- Works well when the data source supports date-based filtering (e.g. `agently-cli message +list --after <ISO-timestamp>`)
- Use when: the user says "新邮件 = 当日0点到执行时间时" or similar time-window definitions
- Cleanup: delete any old state files since they're no longer used

Trade-off: the LLM re-sees and re-classifies the same items on every tick. Ensure the classification rules handle already-processed items correctly (e.g. the rules file should define what makes an item "actionable" vs "already handled").

### 4c. Thread Grouping

When the data source produces items that belong to natural threads/conversations (e.g. email reply chains with Re: subjects), add thread grouping to the script output:

1. Strip prefixes (Re:/Fwd:/回复:/转发:/回覆:/轉寄:) from subjects using `strip_thread()`
2. Build a `threads` dict mapping thread_root → list of item IDs
3. Include `thread_root` field on each item
4. In the cron prompt, instruct the LLM to merge same-thread items into unified summaries

This avoids repeating the same conversation across multiple digest entries.

### 4d. Memory Lookup Before Summarization

Before writing the final digest, the cron agent should search Hermes memory for records related to the items being summarized:

- If an event was already handled (e.g. "Gmail forwarding confirmed yesterday"), include the result in the summary: "originally confirmed on MM/DD — no action needed"
- If a deadline is recorded in memory, cross-reference: "mentioned in memory as due on MM/DD"
- The prompt should include an explicit step: "Step N: search memory using the memory tool for past records of these events"

This prevents the cron from reporting events as "new/action needed" when they've already been resolved.

### 5. LLM Handles All Classification

The LLM gets full body text and:
- Applies the judgment rules from the prompt
- Produces human-readable natural language output
- Takes DB actions based on decisions

### 6. Pure ASCII Prompts

Cron prompts must be pure ASCII. Invisible Unicode (U+200B zero-width space) triggers security blocks and causes silent cron failures. Verify with:
```bash
hexdump -C prompt.txt | grep "e2 80 8b"
```

## Pitfalls

- Do NOT invent output categories or concepts the user never agreed to (e.g. "待处理"). Only use the approved tiers (IMPORTANT / UNIMPORTANT / UNCERTAIN). Invented concepts cause user frustration and require rewrites.
- Dont try to be clever with Python heuristics -- the user will reject them and tell you to put classification in the prompt. Save yourself the iteration.
- Time windows should be cumulative (0-9, 0-14, 0-19, 0-24) unless the user explicitly asks for segmented windows.
- State file must be managed by the LLM -- the script reads it, the LLM updates it. Make sure the cron prompt includes the update-state step explicitly.
- Large payloads -- if the script outputs many items (50+), the LLM context fills up fast. Add delegate_task usage hints to the prompt for parallel subagent processing.
- Rate limits -- if the cron delivers to WeChat, rate limits can cause false 'failed' appearance even when the cron itself ran fine. Recovery is NOT automatic when the delivery fails mid-window — the output is lost, not queued. See Delivery Failure Recovery below.
- No_agent=true is NOT the right default for judgment tasks -- no_agent=false means the script output IS fed to the LLM. Only set no_agent=true when the script output IS the final message.
- **OAuth stale token: auth status lies, API calls fail** — Some CLIs (e.g. agently-cli) have a local `auth status` command that checks cached credentials, not server-side token validity. The token may silently expire (typically ~7 days) while `auth status` reports `logged_in`. Only a real API call reveals the `invalid_grant`. Scripts should perform a lightweight API probe (e.g. list 1 item) before assuming auth works. Recovery requires the user to re-authenticate (OAuth flow needs browser interaction — cannot be automated in cron).

- **Absolute paths for cron scripts** — Cron environment has a minimal PATH. If your script calls a CLI binary installed via npm/pipx/homebrew, use the absolute path (e.g. `/Users/minimx/.npm-global/bin/agently-cli`) rather than the bare command name. Verify the path with `which <command>` in your own terminal session, then hardcode it.

## Delivery Failure Recovery

When a cron job's `last_status` is `error` and `last_delivery_error` mentions rate limiting, the LLM agent ran fine but the output was never delivered to the user — the delivery channel (especially WeChat) throttled it and the output is lost, not queued.

### Detection

```
cronjob action=list  # check last_status + last_delivery_error
```

- `last_status: error` + `last_delivery_error: "... rate limited"` = delivery failed, script/LLM succeeded
- `last_status: ok` with no delivery error = delivered successfully

### Recovery steps when user asks about missing output

1. Run the underlying data script manually to get fresh data:
   `python3 ~/.hermes/scripts/<script.py> --window auto`
2. Process the output and deliver the result directly in the current conversation
3. Do not re-run the cron job blindly — it may hit the same rate limit, compounding the failure

### Caveats

- Re-running the cron job (`cronjob action=run`) will trigger the full agent pipeline again and may re-hit the rate limit.
- The `--window auto` flag recalculates the time window from current time, so the report will include any new emails that arrived since the failed run.
- If the cron has a state file for dedup, the old run's processed IDs may already be saved — the new run will only see emails not in the state file.

## When to Use This Skill

Use this skill whenever you are designing a new cron job that needs more than just raw data delivery:

- Email triage / inbox classification
- RSS feed reading with LLM summarization
- Content monitoring + change detection + alert generation
- Scheduled data audit + report generation
- Any "fetch data periodically -> judge it -> act on it" workflow

Do NOT use for: simple watchdog scripts (use no_agent=true), one-shot experiments (use spike), or tasks better suited to webhook-subscriptions.
