---
name: draft-replies-email
description: Find unanswered emails, detect unfollowed promises, draft contextual replies matching the user's writing style, and save them as Gmail drafts for manual review and sending. Use when the user mentions unanswered emails, email inbox review, emails I missed, email catch-up, draft email replies, or email follow-ups.
---

# Draft Replies — Email

Find unanswered emails, classify them by priority, draft replies matching the user's writing style, and save them as **Gmail drafts** (properly threaded) for manual review and sending.

## Capabilities

- Scan Gmail inbox for unanswered emails (received messages with no reply sent)
- Detect unfollowed promises (emails where the user committed to follow up but hasn't)
- Merge duplicate threads — detect "bumping this" follow-ups and combine into a single draft
- Classify emails into High, Medium, and Low priority tiers
- Analyze user's writing style from recent sent emails (language mix, tone, formality, signature)
- Draft contextual replies matching the user's voice
- Reply-all awareness — automatically determine reply vs reply-all based on thread patterns
- Save all drafts as **Gmail reply drafts** — properly threaded so they appear in the correct conversation
- Label processed threads for tracking

## Prerequisites

**Run `/google-auth` first** to authenticate with Google Workspace. The skill uses the `gmail_builder.py` helper from the `fe-google-tools` gmail skill.

```bash
# Locate the gmail_builder.py helper
GMAIL_BUILDER=$(find ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/gmail/resources/gmail_builder.py 2>/dev/null | head -1)

# Check auth
python3 $(find ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py 2>/dev/null | head -1) status
```

## Input

The skill accepts optional arguments for timeframe and priority:

- **Timeframe** (required — prompt user if not provided):
  - **Relative**: Number of days to look back, e.g. `7`, `30`, `14`
  - **Absolute range**: Two dates in DD-MM-YYYY format, e.g. `01-02-2026 15-03-2026`
  - If the user does not specify a timeframe, **ask them** before proceeding: "What timeframe should I check? (e.g. 'last 7 days', 'last 30 days', or 'between 01-02-2026 and 15-03-2026')"
- **Priority filter** (default: "all"): Which priority levels to draft for — "high", "medium", "low", or "all"
- **Style override**: If the user specifies a tone or style preference, use that instead of auto-detected style

Examples:
- `/draft-replies-email` — prompts for timeframe, then drafts all priorities
- `/draft-replies-email 30` — scan last 30 days, all priorities
- `/draft-replies-email 10 high` — scan last 10 days, only high priority
- `/draft-replies-email 01-02-2026 28-02-2026` — scan Feb 1-28, all priorities
- `/draft-replies-email 01-02-2026 28-02-2026 high` — scan Feb 1-28, high priority only

## Workflow

### Phase 1: Authenticate and Identify the User

1. Ensure Google auth is active:

```bash
GOOGLE_AUTH=$(find ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py 2>/dev/null | head -1)
GMAIL_BUILDER=$(find ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/gmail/resources/gmail_builder.py 2>/dev/null | head -1)

python3 "$GOOGLE_AUTH" status || python3 "$GOOGLE_AUTH" login
TOKEN=$(python3 "$GOOGLE_AUTH" token)
```

2. Get the user's email address:

```bash
curl -s "https://gmail.googleapis.com/gmail/v1/users/me/profile" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```

3. Store: `user_email`, `user_name` (from profile)

### Phase 2: Load or Analyze Writing Style (Cached)

The writing style analysis is expensive (fetches 250+ sent emails). To save time and cost, the result is cached locally and only regenerated quarterly or on first use.

**Cache location**: `~/.claude/personal-plugins/style-cache/email-style-profile.md`

1. **Check for cached profile**:
   - Read the file `~/.claude/personal-plugins/style-cache/email-style-profile.md`
   - If the file exists, check the `generated_date` in its YAML frontmatter
   - If the profile exists AND `generated_date` is less than 90 days old → **use the cached profile**, skip to Phase 3
   - If the file does not exist OR `generated_date` is more than 90 days old → **regenerate** (continue below)

2. **Regenerate style profile** (only when cache is missing or stale):
   - Fetch a large sample of the user's recent **sent emails** (last 6 months) to build a thorough style profile. Aim for **250+ messages** by paginating through results:

   ```bash
   # Get sent messages — paginate to collect 250+ messages
   # First page
   curl -s "https://gmail.googleapis.com/gmail/v1/users/me/messages?q=in:sent+newer_than:180d&maxResults=100" \
     -H "Authorization: Bearer $TOKEN" \
     -H "x-goog-user-project: gcp-sandbox-field-eng"

   # Continue with nextPageToken until 250+ messages collected
   curl -s "https://gmail.googleapis.com/gmail/v1/users/me/messages?q=in:sent+newer_than:180d&maxResults=100&pageToken=${NEXT_PAGE_TOKEN}" \
     -H "Authorization: Bearer $TOKEN" \
     -H "x-goog-user-project: gcp-sandbox-field-eng"
   ```

   - Read 250+ sent messages in full to analyze:
     - **Language mix**: What percentage is English vs German (or other languages)?
     - **Message length**: Short (1-2 sentences), medium (3-5 sentences), or long (5+ sentences)?
     - **Tone markers**: Formality level, exclamation marks, casual vs corporate
     - **Greeting patterns**: "Hi [Name]", "Dear [Name]", "Hey [Name]", direct start
     - **Sign-off patterns**: "Best", "Thanks", "LG", "VG", "Cheers", custom signatures
     - **Language switching rules**: German for DACH contacts, English for international?
     - **Signature block**: Does the user include a standard signature? Capture it.
   - Build a style profile summary

3. **Save the profile to cache**:
   - Write the style profile to `~/.claude/personal-plugins/style-cache/email-style-profile.md` with YAML frontmatter:
   ```markdown
   ---
   generated_date: YYYY-MM-DD
   platform: email
   message_count: <number of messages analyzed>
   ---

   <style profile summary text>
   ```

4. Use the style profile (cached or freshly generated) to guide draft generation in Phase 5.

### Phase 3: Find Unanswered Emails

This phase uses a Python helper script (`email_scanner.py`) to handle mechanical pre-filtering — automated senders, mailing lists, bulk emails — so the LLM only processes threads that actually need attention.

**NOTE**: Calendar invites are intentionally NOT filtered. Email threads are often written around calendar invites, so filtering them would risk missing important conversations.

```bash
# Locate the helper script
EMAIL_SCANNER=$(find ~/.claude/plugins/cache/fe-vibe/fe-draft-replies-email/*/skills/draft-replies-email/resources/email_scanner.py 2>/dev/null | head -1)
# Fallback to personal-plugins if not installed via marketplace
[ -z "$EMAIL_SCANNER" ] && EMAIL_SCANNER=$(find ~/.claude/personal-plugins/fe-draft-replies-email/skills/draft-replies-email/resources/email_scanner.py 2>/dev/null | head -1)
```

1. **Parse timeframe**: Convert the user's input into Gmail search date format:
   - Relative (e.g. `30`): `newer_than:30d`
   - Absolute (e.g. `01-02-2026 28-02-2026`): `after:2026/02/01 before:2026/02/28`

2. **Find emails received but not replied to (batch + filter)**:

Strategy: Fetch all thread metadata in bulk, pre-filter with the helper script, then only fetch full content for threads that pass.

```bash
# Step 1: Get all threads in inbox within timeframe (paginate to collect all)
curl -s "https://gmail.googleapis.com/gmail/v1/users/me/threads?q=in:inbox+newer_than:${DAYS}d&maxResults=100" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"

# Step 2: For each thread, fetch ONLY metadata (From, Subject, List-Unsubscribe, Precedence)
# Batch these — fetch 10-20 threads per iteration using lightweight metadata format
curl -s "https://gmail.googleapis.com/gmail/v1/users/me/threads/${THREAD_ID}?format=metadata&metadataHeaders=From&metadataHeaders=To&metadataHeaders=Subject&metadataHeaders=Date&metadataHeaders=List-Unsubscribe&metadataHeaders=Precedence&metadataHeaders=List-Id&metadataHeaders=X-Mailer" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"

# Step 3: Save all thread metadata to a temp file as JSON array
# Each item: {"thread_id": "...", "last_message_from": "...", "headers": {...}}

# Step 4: Run the Python helper to pre-filter
python3 "$EMAIL_SCANNER" filter-threads /tmp/thread_metadata.json \
  --user-email "$USER_EMAIL" \
  > /tmp/filtered_threads.json
```

The helper script automatically filters out:
- no-reply@, noreply@, do-not-reply@ addresses
- notifications@, alerts@, updates@, newsletter@ addresses
- Emails with `Precedence: bulk/list` headers
- Emails with `List-Unsubscribe` or `List-Id` headers
- Known automated senders (GitHub notifications, Google Drive shares, etc.)
- Auto-replies and out-of-office messages (by subject pattern)
- Threads where the user already sent the last message

The output includes stats showing how many threads were skipped and why — log these for the summary.

**Step 5**: Read `/tmp/filtered_threads.json` — this contains ONLY threads needing attention, with Gmail links already constructed. Now fetch full content only for these threads.

- Skip emails where the user is only CC'd (unless directly addressed in body)

3. **Find emails in specific labels** (beyond INBOX): Also check `STARRED`, `IMPORTANT`, and any custom labels the user may use for follow-up tracking.

### Phase 3b: Find Unfollowed Promises

Search the user's **sent emails** for messages containing follow-up language — promises the user made but may not have kept.

1. **Search for promise messages in sent mail**:

```bash
# Search sent emails with follow-up language
curl -s "https://gmail.googleapis.com/gmail/v1/users/me/messages?q=in:sent+newer_than:${DAYS}d+%22get+back+to+you%22&maxResults=20" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```

Run multiple searches for common promise phrases:
- **English**: "get back to you", "will follow up", "let me check", "will share", "will send", "I'll look into", "will update you", "circle back", "by end of", "by tomorrow", "by Monday", "early next week"
- **German**: "melde mich", "schaue ich mir an", "klaere ich", "kummere mich", "komme darauf zurueck", "schicke ich dir", "bis Ende der Woche"

2. **Check for follow-through**: For each promise message found:
   - Get the thread ID of the promise email
   - Fetch the full thread to see if the user sent a subsequent message in that thread after the promise
   - If no follow-up message exists from the user after the promise, mark it as **unfollowed**

3. **Calculate promise age**: Record how many days have elapsed since each unfollowed promise was made.

### Phase 3c: Merge Duplicate Threads (Bump Detection)

Before classification, detect cases where the same sender sent a follow-up "bump" email about the same topic. These should be merged into a single draft rather than generating separate drafts for the original and the bump.

1. **Group unanswered threads by sender**: After Phase 3 collects all unanswered threads, group them by the sender's email address.

2. **For each sender with multiple unanswered threads**, check if any are bump/follow-up duplicates:

   **Bump detection signals** — a thread is a bump if:
   - The subject line is identical or nearly identical (ignoring "Re:", "Fwd:", "Reminder:", "Following up:")
   - The later message references the earlier one (e.g., "per my previous email", "just following up", "bumping this", "any update on this?", "circling back", "wanted to check in")
   - German equivalents: "nochmal hierzu", "kurze Erinnerung", "gibt es ein Update", "wollte nochmal nachfragen"
   - The messages are from the same sender and within the same timeframe
   - The later message body quotes or references the earlier message

   **Detection logic**:
   ```
   For each sender with 2+ unanswered threads:
     Sort threads by date (oldest first)
     For each pair of threads (A, B) where B is newer:
       subject_match = normalize(A.subject) == normalize(B.subject)
       body_has_bump_language = any(phrase in B.body for phrase in BUMP_PHRASES)
       b_references_a = A.message_id in B.references_header

       if subject_match OR body_has_bump_language OR b_references_a:
         → MERGE: combine A and B into one item
   ```

3. **Merge strategy**: When threads are merged:
   - Use the **most recent** thread/message for the draft reply (reply to the bump, not the original)
   - Include context from **all** merged threads in the draft (acknowledge the original + the follow-up)
   - Set `is_bump = true` and `bump_count = N` on the merged item
   - The draft should acknowledge the delay more prominently since the sender felt the need to follow up
   - Include a note like: "Sorry for the delayed response — I see you followed up on this as well."
   - Bump the priority up by one tier (LOW → MEDIUM, MEDIUM → HIGH) since a follow-up indicates the sender considers it important

4. **Example merge**:
   ```
   Thread A (Mar 3): "Q2 Planning Input Needed" from jane@company.com
     → "Hi Matthias, could you share your team's Q2 priorities?"

   Thread B (Mar 7): "Re: Q2 Planning Input Needed" from jane@company.com
     → "Hi Matthias, just following up on this — we need to finalize by Friday."

   → MERGED into single item:
     reply_to: Thread B (most recent)
     context: includes both messages
     priority: bumped from MEDIUM → HIGH (sender followed up)
     draft includes: apology for delay + answer
   ```

### Phase 4: Classify Emails

Classify each unanswered email into priority tiers:

**HIGH PRIORITY** — Action or decision required:
- Direct questions expecting an answer ("Can you...?", "Could you please...?", "Are you available...?")
- Emails from leadership, executives, or direct reports
- Approval requests (budget, hiring, comp, travel)
- Customer-facing emails requiring response
- Deadline-driven requests
- **Broken promises (>7 days old)**: Unfollowed promises from Phase 3b where more than 7 days have elapsed

**MEDIUM PRIORITY** — Response warranted:
- Meeting or scheduling requests
- Internal collaboration requests
- Follow-ups to the user's own emails
- Event/planning emails that may need input
- **Recent unfollowed promises (<=7 days old)**: Promises that the user may still intend to follow through on but should be reminded about

**LOW PRIORITY** — Informational or quick ack:
- Thank-you emails
- FYI/informational updates
- Congratulations and kudos
- Well-wishes and personal messages
- Emails where a brief "Thanks!" suffices

### Phase 5: Draft Replies (with Reply-All Awareness)

For each unanswered email (filtered by requested priority level):

#### 5a: Determine Reply vs Reply-All

Before drafting, analyze the thread to decide whether to reply to sender only or reply-all:

1. **Fetch the full thread** to inspect the reply pattern of all participants:

```bash
curl -s "https://gmail.googleapis.com/gmail/v1/users/me/threads/${THREAD_ID}?format=metadata&metadataHeaders=From&metadataHeaders=To&metadataHeaders=Cc&metadataHeaders=Reply-To" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```

2. **Analyze the thread's reply pattern**:

   **Use REPLY-ALL** (`--reply-all`) when:
   - The thread has 3+ participants (To + Cc combined) AND the most recent messages used reply-all (all recipients preserved across messages)
   - The thread is a group discussion where multiple people have contributed
   - The email was sent TO multiple people (not just Cc) — indicates a group conversation
   - The thread subject suggests a collaborative topic (contains "team", "all", "group", "planning", "review")
   - The sender explicitly addressed "Hi all", "Hi team", "Everyone" in the greeting

   **Use REPLY (sender only)** when:
   - The email was sent directly TO the user with others only in Cc
   - The thread is a 1:1 conversation (only 2 participants total)
   - The question/request is specifically addressed to the user by name ("Hi Matthias, could you...")
   - Previous replies in the thread were reply-to-sender (recipients narrowed down over the thread)
   - The email is sensitive/personal in nature (comp, feedback, HR topics)
   - The user is the only person in the To field

   **Detection logic**:
   ```
   For each unanswered thread:
     messages = thread.messages
     last_msg = messages[-1]

     to_recipients = parse_addresses(last_msg.headers['To'])
     cc_recipients = parse_addresses(last_msg.headers['Cc'])
     all_recipients = to_recipients + cc_recipients

     # Check if user is the sole To recipient
     user_is_sole_to = (len(to_recipients) == 1 and user_email in to_recipients)

     # Check thread reply pattern: did participants use reply-all?
     if len(messages) >= 3:
       recipient_counts = [len(parse_all_recipients(m)) for m in messages[-3:]]
       reply_all_pattern = all(c >= 3 for c in recipient_counts)
     else:
       reply_all_pattern = False

     # Check for group greeting
     group_greeting = any(g in last_msg.body[:100].lower()
       for g in ["hi all", "hi team", "hey all", "everyone", "hi zusammen", "hallo zusammen"])

     # Decision
     if len(all_recipients) <= 2 or user_is_sole_to:
       reply_mode = "reply"
     elif reply_all_pattern or group_greeting:
       reply_mode = "reply-all"
     elif len(to_recipients) > 2:
       reply_mode = "reply-all"
     else:
       reply_mode = "reply"  # Default to reply when uncertain
   ```

3. **Store the decision** alongside each item: `reply_mode = "reply" | "reply-all"`

#### 5b: Draft the Reply

1. Consider the recipient — use German for German-speaking contacts, English for others
2. Match the user's detected writing style (tone, length, greeting, sign-off)
3. For **merged bump threads** (from Phase 3c): acknowledge the follow-up and apologize more prominently
4. Draft a reply that:
   - Addresses the specific content/question
   - Feels natural and authentic to the user's voice
   - Matches the formality level of the original email
   - Includes the user's typical sign-off/signature
   - Includes apology for delay if email is >3 days old (stronger apology if `is_bump = true`)
   - For **reply-all** drafts: address all participants appropriately (e.g., "Hi all" instead of "Hi [Name]")
   - For **reply** drafts: address only the sender

For LOW priority emails where no text reply is needed, note: "_(No reply needed — consider archiving)_"

### Phase 6: Create Gmail Drafts (Batched)

For each draft reply, create an actual Gmail draft that is **properly threaded** so it appears in the correct email conversation. Use the `reply_mode` decision from Phase 5a to determine reply vs reply-all.

**Batch strategy**: Instead of creating drafts one-by-one (which is slow and expensive), collect all draft data first, then create them in a batch loop. This minimizes round-trips and allows progress tracking.

1. **Build the draft list first** — collect all draft parameters into an array before making any API calls:

```python
drafts_to_create = []
for item in classified_items:
    drafts_to_create.append({
        "message_id": item["original_message_id"],
        "body": item["draft_text"],
        "reply_all": item["reply_mode"] == "reply-all",
        "is_bump": item.get("is_bump", False),
        "priority": item["priority"],
        "subject": item["subject"],
        "sender": item["sender"],
    })
```

2. **Create all drafts in a batch loop** — process in groups of 5 to stay within rate limits:

```bash
# For each draft in the batch
for draft in drafts_to_create:
    REPLY_ALL_FLAG=""
    if draft["reply_all"]:
        REPLY_ALL_FLAG="--reply-all"

    python3 "$GMAIL_BUILDER" create-reply-draft \
      --message-id "${draft[message_id]}" \
      --body "${draft[body]}" \
      ${REPLY_ALL_FLAG}
done
```

Use the `gmail_builder.py` helper to create reply drafts:

```bash
# Create a REPLY draft (sender only) — when reply_mode = "reply"
python3 "$GMAIL_BUILDER" create-reply-draft \
  --message-id "${ORIGINAL_MESSAGE_ID}" \
  --body "Draft reply text here"

# Create a REPLY-ALL draft — when reply_mode = "reply-all"
python3 "$GMAIL_BUILDER" create-reply-draft \
  --message-id "${ORIGINAL_MESSAGE_ID}" \
  --body "Draft reply text here" \
  --reply-all

# For HTML-formatted replies (either mode)
python3 "$GMAIL_BUILDER" create-reply-draft \
  --message-id "${ORIGINAL_MESSAGE_ID}" \
  --html "<p>Draft reply text here</p>" \
  ${REPLY_ALL_FLAG}
```

**Reply mode selection**:
- Pass `--reply-all` ONLY when Phase 5a determined `reply_mode = "reply-all"`
- Omit `--reply-all` when `reply_mode = "reply"` (sends to sender only)
- The `gmail_builder.py` handles recipient resolution: reply-all includes all To + Cc from the original, minus the user

**For merged/bumped threads** (from Phase 3c):
- Reply to the **most recent** message (the bump), not the original
- The draft text should reference both the original ask and the follow-up
- Use the `ORIGINAL_MESSAGE_ID` of the bump message, not the first message

```bash
# For bumped threads — reply to the latest bump message
python3 "$GMAIL_BUILDER" create-reply-draft \
  --message-id "${BUMP_MESSAGE_ID}" \
  --body "Sorry for the delayed response — addressing your question from the original thread as well as your follow-up. [draft text]" \
  ${REPLY_ALL_FLAG}
```

**Important**: The `create-reply-draft` command automatically:
- Fetches the original message
- Sets proper threading headers (In-Reply-To, References)
- Builds the reply subject with "Re:" prefix
- Quotes the original message
- Associates the draft with the correct thread
- Resolves recipients based on reply/reply-all mode

For unfollowed promises, create a new draft reply in the original thread:

```bash
# Get the thread's latest message ID for proper threading
python3 "$GMAIL_BUILDER" create-reply-draft \
  --message-id "${PROMISE_THREAD_LAST_MESSAGE_ID}" \
  --body "Follow-up reply here"
```

### Phase 7: Summary Output

After creating all drafts, print a summary table to the user in the CLI:

| # | Priority | From | Subject | Reply Mode | Bump | Draft Status |
|---|----------|------|---------|------------|------|-------------|
| 1 | HIGH | [Sender] | [Subject line] | Reply-All | 2x bumped | Draft created |
| 2 | HIGH | [Sender] | [Subject line] | Reply | — | Draft created |
| 3 | MEDIUM | [Sender] | [Subject line] | Reply-All | — | Draft created |
| ... | ... | ... | ... | ... | ... | ... |

**Column notes**:
- **Reply Mode**: Shows "Reply" or "Reply-All" so the user knows who will receive the response
- **Bump**: Shows "2x bumped" (or similar) if duplicate threads were merged, indicating the sender followed up. Empty for non-bumped threads.

Then the unfollowed promises section:

| # | Priority | To | Your Promise | Days Ago | Draft Status |
|---|----------|----|-------------|----------|-------------|
| 1 | HIGH | [Recipient] | "I'll get back to you on..." | 12 | Draft created |
| ... | ... | ... | ... | ... | ... |

And the message:

```
✅ [X] reply drafts created in Gmail.
   Reply: [A] | Reply-All: [B]
   Merged bumps: [C] threads combined from [D] originals
⏳ [Y] follow-up drafts created for unfollowed promises.

Open Gmail → Drafts to review and send each reply.
Each draft is properly threaded in its original conversation.
⚠️  Review Reply-All drafts carefully — check the recipient list before sending.
```

## Examples

### Example: No timeframe given
User says: "check my unanswered emails"
Result: Asks "What timeframe should I check?", then proceeds with user's answer

### Example: Relative timeframe
User says: "/draft-replies-email 30 high"
Result: Scans last 30 days, only drafts for HIGH priority emails, creates Gmail drafts

### Example: Absolute date range
User says: "/draft-replies-email 01-01-2026 31-01-2026"
Result: Scans January 2026, drafts replies for all priorities, creates Gmail drafts

### Example: Quick catch-up after vacation
User says: "I was on vacation for 2 weeks, help me catch up on emails"
Result: Parses "2 weeks" as 14 days, classifies all unanswered emails, creates threaded Gmail drafts for each

## Notes

- **Drafts are NOT sent automatically** — they are saved in Gmail Drafts for manual review and sending
- Each draft appears in the correct email thread (properly threaded with In-Reply-To and References headers)
- The user can edit any draft before sending
- Automated/bulk emails (newsletters, notifications, no-reply) are automatically filtered out
- **Reply-all awareness**: The skill analyzes thread patterns to decide reply vs reply-all. When uncertain, it defaults to reply (sender only) to avoid accidentally broadcasting. Review reply-all drafts before sending.
- **Bump detection**: When the same sender sends a follow-up about the same topic, threads are merged into one draft. The priority is bumped up one tier since the sender considered it important enough to follow up.
- The skill requires Google Workspace authentication via `/google-auth`
