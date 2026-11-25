---
name: draft-replies-slack
description: Find unanswered Slack messages and draft contextual replies staged in the user's Slackbot DM. Use when the user mentions unanswered slack messages, draft slack replies, slack inbox review, check slack, messages I missed, or slack catch-up.
---

# Draft Replies — Slack

Find unanswered Slack messages, classify them by priority, draft replies matching the user's writing style, and stage all drafts in the user's Slackbot DM channel for manual review and copy-paste sending.

## Capabilities

- Scan Slack DMs, @mentions, group DMs, channel threads, and channel mentions for unanswered messages
- Fetch full thread context for accurate, conversation-aware draft replies
- Filter out messages the user already acknowledged with emoji reactions
- Smart bot filtering — skip automated noise but keep actionable bot notifications (Salesforce, PagerDuty, JIRA)
- Detect unfollowed promises with context-aware filtering (skip casual/social promises)
- Classify messages into High, Medium, and Low priority tiers with channel-based weighting
- Analyze user's writing style from recent Slack history (language mix, tone, emoji usage, message length)
- Draft contextual replies matching the user's voice, with confidence scoring per draft
- Stage all drafts in the user's Slackbot DM as a review queue with deep links to original messages
- Batch-post all drafts efficiently using the Slack batch write API

## Input

The skill accepts optional arguments for timeframe and priority:

- **Timeframe** (required — prompt user if not provided):
  - **Relative**: Number of days to look back, e.g. `7`, `30`, `14`
  - **Absolute range**: Two dates in DD-MM-YYYY format, e.g. `01-02-2026 15-03-2026`
  - If the user does not specify a timeframe, **ask them** before proceeding: "What timeframe should I check? (e.g. 'last 7 days', 'last 30 days', or 'between 01-02-2026 and 15-03-2026')"
- **Priority filter** (default: "all"): Which priority levels to draft for — "high", "medium", "low", or "all"
- **Style override**: If the user specifies a tone or style preference, use that instead of auto-detected style

Examples:
- `/draft-replies` — prompts for timeframe, then drafts all priorities
- `/draft-replies 30` — scan last 30 days, all priorities
- `/draft-replies 10 high` — scan last 10 days, only high priority
- `/draft-replies 01-02-2026 28-02-2026` — scan Feb 1-28, all priorities
- `/draft-replies 01-02-2026 28-02-2026 high` — scan Feb 1-28, high priority only

## Workflow

### Phase 1: Identify the User

1. Get the user's Slack identity using the Slack MCP read tool:
   - Call `auth.test` to get the authenticated user's ID and display name
   - If that fails, look up the user via `users.lookupByEmail` using their Databricks email

2. Store: `user_id`, `user_name`, `user_email`

### Phase 2: Load or Analyze Writing Style (Cached)

The writing style analysis is expensive (fetches ~100-200 messages). To save time and cost, the result is cached locally and only regenerated quarterly or on first use.

**Cache location**: `~/.claude/personal-plugins/style-cache/slack-style-profile.md`

1. **Check for cached profile**:
   - Read the file `~/.claude/personal-plugins/style-cache/slack-style-profile.md`
   - If the file exists, check the `generated_date` in its YAML frontmatter
   - If the profile exists AND `generated_date` is less than 90 days old → **use the cached profile**, skip to Phase 3
   - If the file does not exist OR `generated_date` is more than 90 days old → **regenerate** (continue below)

2. **Regenerate style profile** (only when cache is missing or stale):
   - Fetch the user's recent messages (last 3 months) from several DM and channel conversations using `conversations.list` + `conversations.history`
   - Analyze ~100-200 messages for:
     - **Language mix**: What percentage is English vs German (or other languages)?
     - **Message length**: Short (<50 chars), medium (50-200), or long (200+)?
     - **Tone markers**: Emojis, exclamation marks, ellipsis, casual vs formal
     - **Greeting/closing patterns**: "Have a wonderful weekend", "Danke!", etc.
     - **Language switching rules**: Which colleagues get German vs English?
   - Build a style profile summary

3. **Save the profile to cache**:
   - Write the style profile to `~/.claude/personal-plugins/style-cache/slack-style-profile.md` with YAML frontmatter:
   ```markdown
   ---
   generated_date: YYYY-MM-DD
   platform: slack
   message_count: <number of messages analyzed>
   ---

   <style profile summary text>
   ```

4. Use the style profile (cached or freshly generated) to guide draft generation in Phase 5

### Phase 3: Find Unanswered Messages

This phase uses a Python helper script (`slack_scanner.py`) to handle mechanical filtering — empty conversations, sender checks, bot filtering, reaction checks, and permalink construction — so the LLM only processes messages that actually need attention.

```bash
# Locate the helper script
SLACK_SCANNER=$(find ~/.claude/plugins/cache/fe-vibe/fe-draft-replies-slack/*/skills/draft-replies-slack/resources/slack_scanner.py 2>/dev/null | head -1)
# Fallback to personal-plugins if not installed via marketplace
[ -z "$SLACK_SCANNER" ] && SLACK_SCANNER=$(find ~/.claude/personal-plugins/fe-draft-replies-slack/skills/draft-replies-slack/resources/slack_scanner.py 2>/dev/null | head -1)
```

1. **Parse timeframe**: Convert the user's input into a start and end timestamp:
   - Relative (e.g. `30`): `start = now - 30 days`, `end = now`
   - Absolute (e.g. `01-02-2026 28-02-2026`): parse DD-MM-YYYY into Unix timestamps
   - If no timeframe was provided, ask the user now before continuing

2. **DMs (batch + filter)**:
   a. List all DM conversations using `conversations.list` with `types=im`
   b. Use `slack_batch_read_api_call` to fetch `conversations.history` for ALL DM channels in a single batch request (pass `oldest` and `latest` params for each)
   c. Save the batch response to a temp JSON file, structured as `{"channel_id": {"messages": [...]}, ...}`
   d. Run the Python helper to filter:
   ```bash
   python3 "$SLACK_SCANNER" filter-unanswered /tmp/dm_histories.json \
     --user-id "$USER_ID" \
     --workspace "https://databricks.slack.com" \
     > /tmp/dm_unanswered.json
   ```
   e. Read `/tmp/dm_unanswered.json` — this contains ONLY the conversations with unanswered messages, with permalinks already constructed. The script automatically handles:
      - Skipping empty conversations (zero messages in timeframe)
      - Skipping conversations where the user already replied (last message from user)
      - Skipping bot noise (blocklist-based filtering)
      - Skipping messages the user acknowledged with reactions (thumbsup, checkmark, etc.)
      - Flagging messages with engagement reactions (thinking_face, etc.) as needing LOW priority
      - Constructing permalinks without API calls
   f. The output includes stats showing how many conversations were skipped and why — log these for the summary

3. **Group DMs (batch + filter)**: Same approach as DMs:
   a. List group DMs using `conversations.list` with `types=mpim`
   b. Batch-fetch all histories in one call
   c. Save to temp file and run the same `filter-unanswered` command
   d. Read filtered output — only group DMs with unanswered messages mentioning the user

4. **Channel mentions**: Search for `@user` mentions in channels the user is a member of (`search.messages` with `from:-<user_id>` and mentioning the user)
5. **Channel scanning (extended)**: Scan public and private channels where the user is mentioned but hasn't replied:
   - Use `search.messages` with query `<@user_id> -from:<@user_id>` scoped to the timeframe
   - For each match, verify the user hasn't already responded by fetching the thread via `conversations.replies` (using the message `ts` as `thread_ts`) and checking whether any reply in that thread is from `user_id`
   - Filter results to actual channels only: skip conversations where `is_im=true` or `is_mpim=true`
   - Apply smart bot filtering (see 3a below)
   - Deduplicate against matches already found in step 4

For channel results (steps 4-5), apply the following checks per message:
- Check if the last message is FROM someone else (not the user) — this means the user hasn't replied
- For threads: check if the user was mentioned/tagged but hasn't responded in the thread
- Apply reaction filter (see 3b below) — skip messages the user already acknowledged
- Apply smart bot filter (see 3a below)

#### 3a: Smart Bot/App Filtering

Not all bot messages are noise. Apply a whitelist/blocklist approach:

**SKIP these bot messages** (automated noise — no reply needed):
- Slack workflow notifications (`subtype: bot_message` from `Slackbot`, `Workflow Builder`)
- Calendar reminders and meeting join links
- CI/CD notifications (Jenkins, GitHub Actions, CircleCI)
- Deployment notifications
- Channel topic/purpose change notifications (`subtype: channel_topic`, `channel_purpose`)
- File share notifications (`subtype: file_share`) unless they mention the user by name
- Messages from bot IDs with no meaningful question content

**KEEP these bot messages** (actionable — may need human response):
- **Salesforce/SFDC alerts**: UCO updates, opportunity changes, account alerts — check if the message contains a question or requests action
- **PagerDuty/OpsGenie**: Incident alerts mentioning the user
- **JIRA notifications**: Ticket assignments, comment mentions — especially ES tickets
- **Emburse/ChromeRiver**: Expense approval requests
- **Concur/travel**: Booking confirmations that need acknowledgment
- **Custom Slack apps** that forward messages from external systems (e.g., customer-facing channels)

**Detection logic**:
```
For each message with subtype "bot_message" or from an app:
  1. Check bot_id / app_id against the blocklist → SKIP
  2. Check bot_id / app_id against the whitelist → KEEP
  3. If unknown bot: check if message text contains the user's @mention → KEEP
  4. If unknown bot: check if message text contains a question mark or action verb → KEEP (as LOW priority)
  5. Otherwise → SKIP
```

#### 3b: Reaction-Aware Filtering

Before marking a message as "unanswered", check if the user already acknowledged it with an emoji reaction. This prevents false positives for messages the user intentionally chose not to reply to.

1. **For each candidate unanswered message**, check its `reactions` field (included in `conversations.history` and `conversations.replies` responses).

2. **If the user reacted**, apply these rules:
   - **Acknowledgment reactions** — treat as "answered", SKIP the message entirely:
     - `:thumbsup:`, `:+1:`, `:white_check_mark:`, `:heavy_check_mark:`, `:done:`, `:thankyou:`
     - `:eyes:` (seen/acknowledged), `:raised_hands:`, `:pray:`, `:100:`
   - **Engagement reactions** — the user engaged but may still owe a reply, keep as LOW priority:
     - `:thinking_face:`, `:hourglass:`, `:soon:`, `:memo:`
     - `:laughing:`, `:joy:`, `:heart:` (on substantive messages that asked a question)
   - **No reaction** — proceed with normal unanswered classification

3. **Check reaction by user_id**: The `reactions` array contains `users` lists per reaction name. Only check if `user_id` appears in any reaction's `users` array.

```
For each candidate message:
  reactions = message.get('reactions', [])
  user_reacted = any(user_id in r['users'] for r in reactions)
  if user_reacted:
    reaction_names = [r['name'] for r in reactions if user_id in r['users']]
    if any(r in ACK_REACTIONS for r in reaction_names):
      → SKIP (already acknowledged)
    elif any(r in ENGAGEMENT_REACTIONS for r in reaction_names):
      → KEEP but downgrade to LOW priority, note "user reacted with :{name}:"
  else:
    → KEEP (no reaction, truly unanswered)
```

#### 3c: Fetch Full Thread Context

For every message identified as unanswered, fetch the complete thread context — not just the single message. This enables drafting replies that reference earlier discussion points.

1. **For each unanswered message**:
   - If the message has a `thread_ts` (it's in a thread), fetch all replies using `conversations.replies` with `channel` and `ts=thread_ts`
   - If the message is a top-level message with `reply_count > 0`, also fetch replies
   - If it's a standalone DM with no thread, fetch the **5 preceding messages** in the conversation for context using `conversations.history` with `latest=message_ts` and `limit=6` (5 context + the message itself)

2. **Store the thread context** alongside each unanswered message:
   ```
   unanswered_message = {
     "message": <the unanswered message>,
     "thread_context": [<preceding messages in thread or conversation>],
     "thread_summary": "<brief summary of what the thread is about>",
     "channel_id": "C...",
     "channel_name": "#channel-name",
     "message_ts": "1234567890.123456",
     "thread_ts": "1234567890.000000",  # if in a thread
     "permalink": "<slack permalink>"    # for deep linking
   }
   ```

3. **Permalinks — REQUIRED for every message, no exceptions**:
   Every unanswered message MUST have a `permalink` field before it can proceed to classification or drafting. Messages without a permalink MUST NOT be staged.

   **How to ensure every message has a permalink:**
   - **DMs and Group DMs** (steps 2-3): The `slack_scanner.py` helper already constructs permalinks — they are in the `permalink` field of each unanswered item.
   - **Channel mentions from `search.messages`** (steps 4-5): The Slack search API returns a `permalink` field in each match. Use it directly.
   - **Fallback construction** (if neither source provides a permalink): Build it manually — no API call needed:
     ```
     https://databricks.slack.com/archives/{channel_id}/p{message_ts_with_dot_removed}
     ```
     Example: channel `C09BT0NHH0Q`, ts `1773397124.276299` → `https://databricks.slack.com/archives/C09BT0NHH0Q/p1773397124276299`
   - Alternatively, use the helper script:
     ```bash
     python3 "$SLACK_SCANNER" build-permalinks /tmp/channel_messages.json \
       --workspace "https://databricks.slack.com"
     ```

   **Validation gate**: Before proceeding to Phase 4, iterate over ALL collected unanswered messages and verify each has a non-empty `permalink`. For any message missing one, construct it using the fallback formula above. Log a warning but do NOT skip the message.

4. **Limit context fetching**: Cap at 20 messages per thread to avoid excessive API calls. For threads with 20+ replies, fetch the first 5 and last 15.

### Phase 3b: Find Unfollowed Promises (Context-Aware)

Search for messages FROM the user that contain follow-up language — promises the user made but may not have kept. Apply context-aware filtering to avoid false positives from casual/social promises.

1. **Search for promise messages**: Use `search.messages` with `from:<@user_id>` scoped to the timeframe, then filter locally for messages containing follow-up language:
   - **English**: "get back to you", "will follow up", "let me check", "come back to you", "will share", "will send", "will do", "on Monday", "by end of day", "tomorrow", "I'll look into", "will update you", "circle back"
   - **German**: "melde mich", "schaue ich mir an", "klaere", "kummere mich", "komme darauf zurueck", "bis Ende der Woche", "schicke ich dir"

2. **Context-aware filtering** — not all promises are equal. For each candidate promise, fetch the message it was replying to and classify:

   **KEEP as real promise** (work-related, specific deliverable):
   - Promises in response to a work request ("Can you share the doc?" → "will send")
   - Promises with a specific deliverable ("I'll send the architecture diagram")
   - Promises in work channels (#escalations, #accounts-*, project channels)
   - Promises mentioning a customer, ticket, or document
   - Promises with a deadline reference ("by Friday", "end of week")

   **SKIP as casual/social** (not actionable):
   - "will do" in response to "have a great weekend" or "enjoy your vacation"
   - "I'll look into it" in #random or social channels
   - "let me check" in response to trivia, non-work topics, or memes
   - Promises in channels matching `#random`, `#fun-*`, `#social-*`, `#watercooler`
   - One-word "will do" without clear work context in the parent message

   **Detection logic**:
   ```
   For each promise candidate:
     1. Fetch the parent message (what the user was replying to)
     2. Check channel name — social channels → SKIP
     3. Check parent message content:
        - Contains customer name, ticket ID, technical terms → KEEP
        - Contains weekend/vacation/social language → SKIP
        - Contains a question with "?" → KEEP
        - Is a greeting or pleasantry → SKIP
     4. Check promise specificity:
        - Mentions a concrete noun (doc, spreadsheet, email, ticket) → KEEP
        - Generic "will do" with no specifics and social parent → SKIP
   ```

3. **Check for follow-through**: For each promise message that passes the context filter:
   - Determine the conversation and thread context (channel + `thread_ts` or just channel)
   - Fetch subsequent messages from the user in that conversation/thread using `conversations.history` or `conversations.replies` with `oldest` set to the promise message timestamp
   - If the user sent a substantive follow-up message after the promise (not just reactions), consider the promise fulfilled
   - If no follow-up is found, mark it as an **unfollowed promise**

4. **Calculate promise age**: Record how many days have elapsed since each unfollowed promise was made. This feeds into the classification phase.

### Phase 4: Classify Messages (with Channel Weighting)

Classify each unanswered message into priority tiers. Apply **channel-based weighting** to boost or reduce priority based on where the message originated.

#### 4a: Channel Priority Weighting

Before applying content-based classification, assign a channel weight that can promote or demote the final priority:

**HIGH-weight channels** (boost priority by one tier, e.g. LOW → MEDIUM, MEDIUM → HIGH):
- DMs from the user's manager or skip-level
- `#escalations`, `#urgent`, `#incidents`, `#sev-*`, `#p0-*`, `#p1-*`
- `#leadership-*`, `#exec-*`, `#staff-*`
- Channels matching the user's team (e.g. `#fe-emea-*`, `#sa-*`)
- DMs from direct reports (use team member list from `~/.vibe/profile` if available)

**NORMAL-weight channels** (no adjustment):
- Regular project channels, account channels, general work channels
- Group DMs with colleagues
- Most public channels

**LOW-weight channels** (demote priority by one tier, e.g. HIGH → MEDIUM, MEDIUM → LOW):
- `#random`, `#fun-*`, `#social-*`, `#watercooler`, `#off-topic`
- `#announcements` (usually broadcast-only, no reply needed)
- Large broadcast channels with 200+ members where the user is not directly mentioned

**Detection**: Use `conversations.info` to get channel name, member count, and purpose. Cache channel metadata to avoid repeated lookups.

#### 4b: Content-Based Classification

Classify each unanswered message based on its content, then apply the channel weight adjustment:

**HIGH PRIORITY** — Action or decision required:
- Direct questions expecting an answer ("Can you...?", "Are you ok to...?", "Could you take a look...?")
- Approval requests (comp, nominations, reviews)
- Escalations or organizational issues flagged to the user
- Deadline-driven requests
- **Broken promises (>7 days old)**: Unfollowed promises from Phase 3b where more than 7 days have elapsed since the user committed to follow up

**MEDIUM PRIORITY** — Response warranted:
- Meeting or scheduling requests
- Helpful contributions that deserve acknowledgment
- Event/planning messages that may need input
- Follow-ups to the user's own questions
- **Recent unfollowed promises (<=7 days old)**: Promises from Phase 3b that are still within a week — the user may still intend to follow through but should be reminded

**LOW PRIORITY** — Informational or quick ack:
- Thank-you messages
- FYI/informational updates
- Kudos and praise
- Well-wishes and personal messages
- Messages where a thumbsup react suffices
- Messages where the user already reacted with an engagement emoji (from Phase 3b filtering)

#### 4c: Apply Channel Weight

```
final_priority = adjust(content_priority, channel_weight)

Where adjust():
  HIGH channel + LOW content → MEDIUM
  HIGH channel + MEDIUM content → HIGH
  HIGH channel + HIGH content → HIGH (no change, already max)
  LOW channel + HIGH content → MEDIUM
  LOW channel + MEDIUM content → LOW
  LOW channel + LOW content → LOW (no change, already min)
  NORMAL channel + any content → no change
```

**Exception**: DMs from the user's manager are ALWAYS HIGH priority regardless of content (unless content is purely a thank-you/acknowledgment).

### Phase 5: Draft Replies (Thread-Aware, with Confidence Scoring)

For each unanswered message (filtered by requested priority level):

#### 5a: Draft Using Full Thread Context

1. Consider the sender — use German for German-speaking colleagues, English for others
2. Match the user's detected writing style (tone, length, emoji usage)
3. **Use the thread context from Phase 3c** to draft a reply that:
   - Addresses the specific content/question in the unanswered message
   - References earlier points in the thread where relevant (e.g. "Building on what [Name] said about...")
   - Acknowledges any decisions or conclusions already reached in the thread
   - Does NOT repeat information already stated in the thread
   - Feels natural and authentic to the user's voice
   - Is appropriately brief (match user's typical message length)
   - Includes apology for delay if message is >3 days old

4. **Thread-aware drafting rules**:
   - If the thread has 10+ messages and the user is asked a specific question: answer only the question, don't summarize the thread
   - If the thread is a decision discussion: take a position consistent with the user's past opinions/role
   - If the thread references a document, ticket, or customer: include that context in the draft
   - If multiple people asked the user different things in the same thread: address all of them in one reply

For LOW priority messages where no text reply is needed, use this format (note the `🔗` link is still REQUIRED):

```
📝 *[Sender Name]* ([Date] — [context summary])
_Priority: LOW | Confidence: 🟢 | Channel: #[channel-name]_
🔗 <[permalink]|Jump to message>

> [Original message text, first 150 chars]
_(No reply needed — just a quick :thumbsup: react)_
```

The `🔗 Jump to message` link is essential even for thumbsup-only messages — the user needs it to navigate to the original message and add the reaction.

#### 5b: Confidence Scoring

After generating each draft, self-evaluate its quality and assign a confidence score:

**HIGH confidence** (score: 3/3) — draft is ready to send with minimal editing:
- The question/request is clear and specific
- The user likely has the answer (based on their role/context)
- The draft addresses the exact ask
- Sufficient thread context was available

**MEDIUM confidence** (score: 2/3) — draft needs review, may need user's input:
- The question is somewhat ambiguous
- The draft makes reasonable assumptions but the user may want to adjust
- Limited thread context available
- The topic requires domain knowledge the skill may not have

**LOW confidence** (score: 1/3) — draft is a placeholder, user must rewrite:
- The message is vague or unclear
- No thread context available to understand what's being asked
- The topic is highly specific (e.g., technical architecture, customer-specific details)
- The draft is generic and may not actually answer the question
- The message references external context (a meeting, a call, a document) that wasn't scanned

**Assign the score** to each draft and include it in the Slackbot staging format. This helps the user prioritize which drafts to review carefully vs. which can be sent as-is.

```
For each draft:
  confidence = 3  # Start at max
  if no_thread_context: confidence -= 1
  if ambiguous_question: confidence -= 1
  if references_external_context: confidence -= 1
  if topic_is_highly_specific: confidence -= 1
  confidence = max(1, min(3, confidence))  # Clamp to 1-3
```

### Phase 6: Stage in Slackbot DM (Batch Post with Deep Links)

1. Open the user's self-DM channel (Slackbot notepad) by calling `conversations.open` with the user's own user ID

2. **Build all messages first, then batch-post** using `mcp__slack__slack_batch_write_api_call` for efficiency. Construct an array of `chat.postMessage` calls and send them in a single batch request. This is significantly faster than posting one-by-one.

3. **Message format — header**:

```
📬 *Unanswered Messages Review* — [date]
Scanned last [N] days | [X] messages found | Priority: [filter]
Confidence: 🟢 = ready to send, 🟡 = needs review, 🔴 = placeholder only
```

4. **Message format — each draft** (the `🔗` link line is REQUIRED, not optional):

```
📝 *Draft reply for [Sender Name]* ([Date] — [context summary])
_Priority: [HIGH/MEDIUM/LOW] | Confidence: [🟢/🟡/🔴] | Channel: #[channel-name]_
🔗 <[permalink]|Jump to message>

> [Original message text, first 150 chars]

[Draft reply text here]
```

**CRITICAL — every draft MUST include the `🔗` link**: The `🔗 <[permalink]|Jump to message>` line is a REQUIRED part of the template, not a decoration. It MUST appear in every single staged message — HIGH, MEDIUM, LOW priority drafts, thumbsup-only messages, and unfollowed promises. Without this link the draft is useless because the user cannot find the original conversation.

**How to construct the link**: Use the `permalink` field from the unanswered message object (populated in Phase 3c). Format as Slack mrkdwn: `🔗 <https://databricks.slack.com/archives/C.../p...|Jump to message>`. If the permalink is missing (it should not be after the Phase 3c validation gate), construct it as `https://databricks.slack.com/archives/{channel_id}/p{message_ts_with_dot_removed}`.

**Confidence indicators**:
- 🟢 (score 3/3): Draft is ready — user can copy-paste with minimal changes
- 🟡 (score 2/3): Draft needs review — reasonable but may need adjustments
- 🔴 (score 1/3): Placeholder only — user must rewrite based on their knowledge

5. **Message format — unfollowed promises section**:

```
⏳ *Unfollowed Promises* — [count] found
```

For each unfollowed promise:

```
🔔 *Promise to [Recipient Name]* ([Date] — [channel/DM context])
_Priority: [HIGH/MEDIUM] | Age: [N] days_
🔗 <[permalink]|Jump to original promise>

*Your original message:*
> [User's original promise text]

*Suggested follow-up:*
[Draft follow-up message, e.g. "Hey [Name], circling back on this — [contextual follow-up]. Sorry for the delay!"]
```

6. **Batch posting implementation**:

```
# Build all messages as an array
messages = [header_message] + draft_messages + [promise_separator] + promise_messages + [footer_message]

# Post using batch write API — all messages in one call
mcp__slack__slack_batch_write_api_call with:
  requests: [
    {"method": "chat.postMessage", "params": {"channel": self_dm_id, "text": msg["text"], "mrkdwn": true}}
    for msg in messages
  ]
```

**Fallback**: If batch write fails (e.g., too many messages), fall back to posting in groups of 10. The batch API typically supports up to 50 requests per call.

7. **Footer message**:

```
✅ [X] drafts staged above. Copy-paste each reply into the actual conversation.
   🟢 [A] ready to send | 🟡 [B] need review | 🔴 [C] need rewrite
For messages marked with :thumbsup:, just react on the original message.
⏳ [Y] unfollowed promises flagged — review and follow up where needed.
Click 🔗 links to jump directly to each conversation.
```

### Phase 7: Summary Output

Print a summary table to the user in the CLI:

| # | Priority | Sender | Context | Status |
|---|----------|--------|---------|--------|
| 1 | HIGH | [Name] | [Brief context] | Draft staged in Slackbot |
| 2 | MEDIUM | [Name] | [Brief context] | Draft staged in Slackbot |
| ... | ... | ... | ... | ... |

And the message: "Open your Slackbot DM in Slack to review all drafts."

## Examples

### Example: No timeframe given
User says: "check my unanswered slack messages"
Result: Asks "What timeframe should I check?", then proceeds with user's answer

### Example: Relative timeframe
User says: "/draft-replies 30 high"
Result: Scans last 30 days, only drafts for HIGH priority messages, stages in Slackbot DM

### Example: Absolute date range
User says: "/draft-replies 01-01-2026 31-01-2026"
Result: Scans January 2026, drafts replies for all priorities, stages in Slackbot DM

### Example: Quick catch-up
User says: "what slack messages did I miss in the last 2 weeks?"
Result: Parses "2 weeks" as 14 days, shows classified list, drafts and stages all replies
