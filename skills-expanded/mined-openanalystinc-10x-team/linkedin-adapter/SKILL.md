---
name: linkedin-adapter
description: |
  LinkedIn automation adapter for the 100X Outreach System.
  Use this skill when performing LinkedIn actions like connecting, messaging, viewing profiles, liking posts, or commenting.
  This skill controls the 10x Team Browser Extension to execute LinkedIn actions with templates.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - TodoWrite
  - AskUserQuestion
  - WebFetch
---

# LinkedIn Adapter Skill

Automates LinkedIn actions using the 10x Team Universal Browser Extension with intelligent template rendering.

## 10x Team Browser Extension: Local Control

**Fast, local browser automation!** The 10x Team extension provides direct control over your browser via WebSocket.

Benefits:
- ✅ **Faster**: Local execution, no cloud latency
- ✅ **Free**: No usage costs
- ✅ **Visible**: See actions in real-time
- ✅ **Persistent**: Uses your real LinkedIn account
- ✅ **Activity Tracking**: Built-in LinkedIn Lookback integration
- ✅ **Rate Limiting**: Smart rate limits prevent LinkedIn detection

## Architecture

```
Claude Code (You)
    ↓ HTTP API
Canvas Server (localhost:3000)
    ↓ WebSocket
Browser Extension
    ↓ Chrome APIs
LinkedIn.com
```

## IMPORTANT: You Control the Extension

**You are the brain that orchestrates the extension.** This skill tells you exactly how to:
1. Load and render templates
2. Send commands to the extension via HTTP API
3. Wait for action results
4. Monitor and report progress

## When to Use This Skill

Use this skill when the user wants to:
- Send LinkedIn connection requests
- Message LinkedIn connections
- View LinkedIn profiles (warm-up)
- Like/comment on LinkedIn posts
- Send InMails

## Available LinkedIn Actions

| Action | Description | Max Steps |
|--------|-------------|-----------|
| `view_profile` | View someone's LinkedIn profile | 5 |
| `like_post` | Like a recent post | 8 |
| `comment` | Comment on a post | 10 |
| `connect` | Send connection request | 12 |
| `message` | Send a direct message | 12 |
| `inmail` | Send an InMail | 12 |

## Available Templates

### Connection Requests (`templates/linkedin/connection-requests/`)
- `cold_outreach.md` - General cold outreach
- `startup_founder.md` - Reach out to founders
- `thought_leader.md` - Connect with thought leaders
- `speaker_invitation.md` - Invite speakers
- `content_collaboration.md` - Content collab requests
- `alumni_connect.md` - Alumni connections
- `potential_client.md` - Sales outreach
- `mutual_connection.md` - Mutual connection intro
- `same_industry.md` - Same industry connection
- `recruiter.md` - Recruiter outreach
- `investor_outreach.md` - Investor connections
- `event_attendee.md` - Event attendee connections

### Messages (`templates/linkedin/messages/`)
- `intro_after_connect.md` - First message after connecting
- `follow_up_no_response.md` - Follow up on no response
- `meeting_request.md` - Request a meeting
- `collaboration_proposal.md` - Propose collaboration
- `value_offer.md` - Offer value
- `thank_you.md` - Thank you message
- `partnership_proposal.md` - Partnership proposals
- `sales_intro.md` - Sales introduction
- `referral_request.md` - Ask for referrals
- `expertise_request.md` - Ask for expert advice
- `podcast_invitation.md` - Podcast guest invitation

### InMails (`templates/linkedin/inmails/`)
- `cold_inmail.md` - Cold InMail
- `executive_outreach.md` - Executive outreach
- `job_opportunity.md` - Job opportunities

### Comments (`templates/linkedin/comments/`)
- `thoughtful_engagement.md` - Thoughtful comment
- `question_comment.md` - Ask a question
- `congratulations.md` - Congratulate them

## CRITICAL: Step-by-Step Execution Flow

### Prerequisites

1. **Canvas server must be running:**
   ```bash
   cd canvas && npm start
   # Server at http://localhost:3000
   # WebSocket at ws://localhost:3000/ws
   ```

2. **Browser extension must be installed:**
   - Load `.claude/skills/browser-extension` in Chrome
   - Extension badge should show "✓" (connected)

3. **User must be logged into LinkedIn** in their browser

### Step 1: Check Extension Connection

Verify the extension is connected:

```bash
curl http://localhost:3000/api/extension/status
```

Expected response:
```json
{
  "connected": true,
  "extensionId": "abc123...",
  "capabilities": ["linkedin", "instagram", "twitter", "google"]
}
```

If not connected, tell user to check extension popup.

### Step 2: Load and Render Template

Read the template file and render with Jinja2:

```bash
# List available templates
python .claude/scripts/template_loader.py list --platform linkedin --category connection-requests

# Render a template with variables
python .claude/scripts/template_loader.py render --path linkedin/connection-requests/cold_outreach --var first_name "John" --var company "Acme Inc" --var industry "AI/ML" --var my_name "Your Name"
```

This returns the rendered message text.

### Step 3: Send Action to Extension

Send LinkedIn action command via HTTP API:

```bash
# Connection request
curl -X POST http://localhost:3000/api/linkedin/action \
  -H "Content-Type: application/json" \
  -d '{
    "type": "send_connection",
    "profileUrl": "https://linkedin.com/in/johnsmith",
    "note": "Hi John, I came across your profile..."
  }'

# Send message
curl -X POST http://localhost:3000/api/linkedin/action \
  -H "Content-Type: application/json" \
  -d '{
    "type": "send_message",
    "profileUrl": "https://linkedin.com/in/johnsmith",
    "message": "Thanks for connecting! I wanted to reach out..."
  }'

# View profile (warm-up)
curl -X POST http://localhost:3000/api/linkedin/action \
  -H "Content-Type: application/json" \
  -d '{
    "type": "view_profile",
    "profileUrl": "https://linkedin.com/in/johnsmith"
  }'

# Like post
curl -X POST http://localhost:3000/api/linkedin/action \
  -H "Content-Type: application/json" \
  -d '{
    "type": "like_post",
    "postUrl": "https://linkedin.com/feed/update/urn:li:activity:123456"
  }'

# Comment on post
curl -X POST http://localhost:3000/api/linkedin/action \
  -H "Content-Type: application/json" \
  -d '{
    "type": "comment",
    "postUrl": "https://linkedin.com/feed/update/urn:li:activity:123456",
    "comment": "Great insights! I especially liked..."
  }'

# Send InMail (requires Premium)
curl -X POST http://localhost:3000/api/linkedin/action \
  -H "Content-Type: application/json" \
  -d '{
    "type": "send_inmail",
    "profileUrl": "https://linkedin.com/in/johnsmith",
    "subject": "Partnership Opportunity",
    "body": "Hi John, I have an exciting partnership opportunity..."
  }'
```

### Step 4: Wait for Result

The API call returns immediately with the result:

**Success Response:**
```json
{
  "success": true,
  "action": "send_connection",
  "timestamp": "2026-01-22T17:30:00Z",
  "status": "sent",
  "note": "Hi John, I came across your profile...",
  "rateLimit": {
    "allowed": true,
    "remaining": 14,
    "limit": 15,
    "resetDate": "2026-01-22"
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "action": "send_connection",
  "error": "Daily connection limit reached (15/day). Resets tomorrow.",
  "timestamp": "2026-01-22T17:30:00Z"
}
```

### Step 5: Report to User

Tell the user what happened:
- ✅ "Successfully sent connection request to John Smith (14 connections remaining today)"
- ❌ "Failed to send connection: Daily limit reached. Resets tomorrow."
- ⏸️ "Profile already connected. Skipping."

### Step 6: Record Activity (Automatic)

The extension automatically records all LinkedIn activity:
- Tracks profile views, connections, messages
- Stores in browser IndexedDB
- Forwards to LinkedIn Lookback database
- Triggers automated follow-up workflows

No manual recording needed!

## Example: Send Connection Request

**User:** "Connect with John Smith on LinkedIn with a cold outreach message"

**You should:**

1. **Check extension:**
   ```bash
   curl http://localhost:3000/api/extension/status
   ```
   → Verify extension is connected

2. **Render template:**
   ```bash
   python .claude/scripts/template_loader.py render --path linkedin/connection-requests/cold_outreach --var first_name "John" --var company "UNKNOWN" --var my_name "Your Name"
   ```
   → Get rendered message: "Hi John, I came across your profile..."

3. **Send to extension:**
   ```bash
   curl -X POST http://localhost:3000/api/linkedin/action \
     -H "Content-Type: application/json" \
     -d '{
       "type": "send_connection",
       "profileUrl": "https://linkedin.com/in/johnsmith",
       "note": "Hi John, I came across your profile..."
     }'
   ```

4. **Get result (immediate):**
   ```json
   {
     "success": true,
     "status": "sent",
     "rateLimit": { "remaining": 14, "limit": 15 }
   }
   ```

5. **Report to user:**
   ```
   ✅ Connected with John Smith successfully! (14 connections remaining today)
   ```

That's it! The extension handles all the browser automation automatically.

## Example: Bulk Outreach (Single Approval)

**User:** "Connect with these 5 LinkedIn profiles"

**You should:**

1. Show preview:
   ```
   ═══════════════════════════════════════════
   LINKEDIN OUTREACH - 5 CONNECTIONS
   ═══════════════════════════════════════════

   Template: Cold Outreach

   Targets:
   1. John Smith (CEO at Acme)
   2. Jane Doe (CTO at TechCo)
   3. Bob Wilson (Founder at StartupX)
   4. Alice Chen (VP at BigCorp)
   5. Mike Brown (Director at MidCo)

   Rate Limit: 15 connections remaining today
   Estimated time: ~15 minutes (3 min/connection)
   ═══════════════════════════════════════════

   Proceed with all 5 connection requests?
   ```

2. After single approval, execute ALL actions autonomously:
   ```bash
   for person in targets:
     # 1. Render template
     message = render_template(person)

     # 2. Send to extension
     result = curl POST /api/linkedin/action {
       "type": "send_connection",
       "profileUrl": person.url,
       "note": message
     }

     # 3. Report progress
     print(f"✅ {person.name}: {result.status}")

     # 4. Smart delay (2-5 minutes between connections)
     sleep(random(120, 300))
   ```

3. Final summary:
   ```
   ✅ Bulk outreach complete!
   - 5/5 connections sent successfully
   - 10 connections remaining today
   - Activity recorded in LinkedIn Lookback
   ```

## Rate Limits (Built into Extension)

The extension automatically enforces these daily limits:

| Action | Daily Limit | Auto-Tracked | Error if Exceeded |
|--------|-------------|--------------|-------------------|
| view_profile | 100 | ✅ | "Daily profile view limit reached" |
| like_post | 50 | ✅ | "Daily like limit reached" |
| comment | 30 | ✅ | "Daily comment limit reached" |
| connect | 15 | ✅ | "Daily connection limit reached" |
| message | 40 | ✅ | "Daily message limit reached" |
| inmail | 5 | ✅ | "Daily InMail limit reached" |

**All limits reset at midnight (local time).**

## Check Rate Limits

```bash
# Check extension status and rate limits
curl http://localhost:3000/api/linkedin/limits
```

Response:
```json
{
  "connections": { "used": 5, "remaining": 10, "limit": 15 },
  "messages": { "used": 12, "remaining": 28, "limit": 40 },
  "profileViews": { "used": 45, "remaining": 55, "limit": 100 },
  "likes": { "used": 20, "remaining": 30, "limit": 50 },
  "comments": { "used": 5, "remaining": 25, "limit": 30 },
  "inmails": { "used": 0, "remaining": 5, "limit": 5 },
  "resetDate": "2026-01-23"
}
```
