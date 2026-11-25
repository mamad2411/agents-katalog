---
name: gmail-adapter
description: |
  Gmail email sending adapter for the 100X Outreach System.
  Use this skill to send emails via Gmail using the user's own OAuth2 credentials.
  This is a core skill for email campaigns and workflow email steps.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - TodoWrite
  - AskUserQuestion
---

# Gmail Adapter Skill

Send emails via Gmail API using the user's own OAuth2 credentials.

## IMPORTANT: User's Own Gmail Account

This skill uses the user's Gmail account with their own OAuth2 credentials:
- GOOGLE_CLIENT_ID
- GOOGLE_CLIENT_SECRET
- SENDER_EMAIL

No Browser-Use needed for Gmail - direct API access via Python.

## When to Use This Skill

Use this skill when the user wants to:
- Send individual emails
- Run email campaigns
- Send follow-up emails
- Integrate email into workflows
- Use Gmail templates

## Available Email Actions

| Action | Description |
|--------|-------------|
| `send` | Send a single email |
| `send_campaign` | Send to multiple recipients |
| `send_with_template` | Send using a template |

## Available Templates

### Outreach (`templates/email/outreach/`)
- `cold_email.md` - Cold outreach email
- `warm_intro.md` - Warm introduction
- `referral_intro.md` - Referral introduction
- `partnership.md` - Partnership proposal
- `investor_pitch.md` - Investor pitch

### Follow-up (`templates/email/follow-up/`)
- `no_response_1.md` - First follow-up
- `no_response_2.md` - Second follow-up
- `no_response_final.md` - Final follow-up
- `after_meeting.md` - After meeting
- `after_call.md` - After call
- `check_in.md` - Check in

### Promotional (`templates/email/promotional/`)
- `product_launch.md` - Product launch
- `feature_announcement.md` - Feature announcement
- `discount_offer.md` - Discount offer
- `webinar_invite.md` - Webinar invitation

### Newsletters (`templates/email/newsletters/`)
- `weekly_digest.md` - Weekly digest
- `monthly_update.md` - Monthly update
- `announcement.md` - Announcement

## Setup Required

### 1. Google Cloud Console Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable the Gmail API:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"
4. Create OAuth2 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Select "Desktop app"
   - Download the credentials

### 2. Environment Variables

Add to `.env`:
```env
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
SENDER_EMAIL=your@gmail.com
SENDER_NAME=Your Name
```

### 3. First-Time Authentication

On first use, a browser window will open for OAuth2 authentication.
Grant permission to send emails on your behalf.
Token is saved for future use.

## Step-by-Step Execution Flow

### Step 1: Check Gmail Configuration

```bash
# Check if Gmail is configured
python .claude/scripts/gmail_client.py status
```

### Step 2: Load and Render Template

```bash
# List available email templates
python .claude/scripts/template_loader.py list --platform email --category outreach

# Render a template with variables
python .claude/scripts/template_loader.py render --path email/outreach/cold_email --var first_name "John" --var company "Acme Inc" --var my_name "Your Name"
```

### Step 3: Send Email

```bash
# Send a single email
python .claude/scripts/gmail_client.py send --to "recipient@example.com" --subject "Subject Line" --body "Email body text"

# Send with template
python .claude/scripts/gmail_client.py send --to "recipient@example.com" --template "email/outreach/cold_email" --var first_name "John" --var company "Acme"
```

### Step 4: Record Action (for rate limiting)

```bash
# Record successful email
python .claude/scripts/rate_limiter.py --user default --platform gmail --action send --record --success --target "recipient@example.com"
```

## Example: Send Cold Outreach Email

**User:** "Send a cold email to john@acme.com introducing myself"

**You should:**

1. **Check configuration:**
   ```bash
   python .claude/scripts/gmail_client.py status
   ```

2. **Render template:**
   ```bash
   python .claude/scripts/template_loader.py render --path email/outreach/cold_email --var first_name "John" --var company "Acme Inc" --var my_name "Your Name"
   ```
   → Get rendered subject and body

3. **Send email:**
   ```bash
   python .claude/scripts/gmail_client.py send --to "john@acme.com" --subject "RENDERED_SUBJECT" --body "RENDERED_BODY"
   ```

4. **Record action:**
   ```bash
   python .claude/scripts/rate_limiter.py --user default --platform gmail --action send --record --success --target "john@acme.com"
   ```

5. **Report:**
   ```
   Email sent successfully to john@acme.com!
   Subject: [Subject line]
   ```

## Example: Email Campaign (Single Approval)

**User:** "Send cold emails to these 10 contacts from my Google Sheet"

**You should:**

1. Show preview:
   ```
   ═══════════════════════════════════════════
   EMAIL CAMPAIGN - 10 RECIPIENTS
   ═══════════════════════════════════════════

   Template: Cold Outreach
   Subject: "Quick question about [company]"

   Recipients:
   1. john@acme.com - John Smith (CEO at Acme)
   2. jane@techco.com - Jane Doe (CTO at TechCo)
   3. bob@startup.com - Bob Wilson (Founder at Startup)
   ... (7 more)

   Estimated time: ~15 minutes (with delays)
   ═══════════════════════════════════════════

   Proceed with all 10 emails?
   ```

2. After single approval, execute ALL autonomously:
   - Render template for each recipient
   - Send email via Gmail API
   - Wait for rate-limited delay (1-3 minutes)
   - Report progress after each email
   - Final summary when complete

## Rate Limits

| Action | Daily Limit | Min Delay | Max Delay |
|--------|-------------|-----------|-----------|
| send | 100 | 60s | 180s |
| send_campaign | 100 | 60s | 180s |

## Check Rate Limits

```bash
# Check remaining emails
python .claude/scripts/rate_limiter.py --user default --platform gmail --remaining

# Check if send is allowed
python .claude/scripts/rate_limiter.py --user default --platform gmail --action send --check
```

## Integration with Workflows

Gmail can be used as a step in multi-platform workflows:

```yaml
phases:
  - name: "connect_linkedin"
    platform: "linkedin"
    action: "connect"

  - name: "send_email"
    platform: "gmail"
    action: "send"
    template: "email/outreach/warm_intro"
    delay_after: "24-48 hours"
```

## Gmail vs Browser-Use

| Feature | Gmail API | Browser-Use |
|---------|-----------|-------------|
| Speed | Fast (direct API) | Slower (browser) |
| Reliability | Very reliable | May need retries |
| Setup | OAuth2 required | Browser profile |
| Use case | Email campaigns | Social platforms |

**Gmail API is preferred for email** - faster, more reliable, and easier to manage at scale.

## Troubleshooting

### Authentication Failed
1. Check GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in `.env`
2. Delete `token.json` and re-authenticate
3. Ensure Gmail API is enabled in Google Cloud Console

### Rate Limit Exceeded
1. Gmail has daily sending limits (varies by account type)
2. The system enforces conservative limits (100/day)
3. Check remaining limit before bulk sends

### Emails Going to Spam
1. Warm up new sender accounts gradually
2. Use personalized templates
3. Avoid spam trigger words
4. Ensure SPF/DKIM records are set up
