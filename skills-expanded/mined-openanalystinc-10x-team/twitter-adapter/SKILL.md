---
name: twitter-adapter
description: |
  Twitter/X automation adapter for the 100X Outreach System.
  Use this skill when performing Twitter actions like following, DMing, liking tweets, replying, or retweeting.
  This skill controls the 10x Team Browser Extension to execute Twitter actions with templates.
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

# Twitter/X Adapter Skill

Automates Twitter/X actions using the 10x Team Universal Browser Extension with intelligent template rendering.

## 10x Team Browser Extension: Local Control

**Fast, local browser automation!** The 10x Team extension provides direct control over your browser via WebSocket.

Benefits of WebSocket integration:
- ✅ **Faster**: Local execution, no cloud latency
- ✅ **Free**: No usage costs
- ✅ **Visible**: See actions in real-time
- ✅ **Persistent**: Uses your real Twitter/X account
- ✅ **Activity Tracking**: All actions logged automatically
- ✅ **Rate Limiting**: Smart rate limits prevent Twitter detection

## Architecture

```
Claude Code (You)
    ↓ HTTP API
Canvas Server (localhost:3000)
    ↓ WebSocket
Browser Extension
    ↓ Chrome APIs
Twitter.com / X.com
```

## IMPORTANT: You Control the Extension

**You are the brain that orchestrates the extension.** This skill tells you exactly how to:
1. Load and render templates
2. Send commands to the extension via HTTP API
3. Wait for action results
4. Monitor and report progress

## When to Use This Skill

Use this skill when the user wants to:
- Follow Twitter accounts
- Send Twitter DMs
- Like tweets
- Reply to tweets
- Retweet or quote tweet
- Engage with Twitter content

## Available Twitter Actions

| Action | Description | Max Steps |
|--------|-------------|-----------|
| `follow` | Follow a Twitter user | 6 |
| `like_tweet` | Like a specific tweet | 5 |
| `retweet` | Retweet a tweet | 5 |
| `reply` | Reply to a tweet | 8 |
| `dm` | Send a direct message | 10 |
| `quote_tweet` | Quote tweet with comment | 8 |

## Available Templates

### DMs (`templates/twitter/dms/`)
- `cold_dm.md` - Cold outreach DM
- `after_follow.md` - DM after following
- `mutual_follower.md` - Mutual follower intro
- `reply_to_tweet.md` - DM after tweet interaction
- `collaboration.md` - Collaboration request
- `thank_you.md` - Thank you message
- `founder_outreach.md` - Founder outreach
- `thought_leader_outreach.md` - Thought leader outreach
- `influencer_outreach.md` - Influencer collaboration
- `expert_consultation.md` - Expert consultation request
- `podcast_guest.md` - Podcast guest invitation
- `investor_intro.md` - Investor introduction

### Tweets (`templates/twitter/tweets/`)
- `engagement_reply.md` - Engagement reply
- `quote_tweet.md` - Quote tweet template
- `mention.md` - Mention someone
- `thread_starter.md` - Start a thread

### Replies (`templates/twitter/replies/`)
- `value_add.md` - Add value to conversation
- `question.md` - Ask a question
- `agreement.md` - Agree with insight
- `insight.md` - Share an insight
- `build_in_public.md` - Build in public engagement
- `milestone_congrats.md` - Congratulate milestones

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

3. **User must be logged into Twitter/X** in their browser

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

### Step 2: Load and Render Template

Read the template file and render with Jinja2:

```bash
# List available templates
python .claude/scripts/template_loader.py list --platform twitter --category dms

# Render a template with variables
python .claude/scripts/template_loader.py render --path twitter/dms/cold_dm --var first_name "John" --var topic "AI" --var my_name "Your Name"
```

This returns the rendered message text.

### Step 3: Send Action to Extension

Send Twitter action command via HTTP API:

```bash
# Follow user
curl -X POST http://localhost:3000/api/twitter/action \
  -H "Content-Type: application/json" \
  -d '{
    "type": "follow",
    "username": "elonmusk"
  }'

# Send DM
curl -X POST http://localhost:3000/api/twitter/action \
  -H "Content-Type: application/json" \
  -d '{
    "type": "dm",
    "username": "founder123",
    "message": "Hey! Love what you're building with your startup..."
  }'

# Like tweet
curl -X POST http://localhost:3000/api/twitter/action \
  -H "Content-Type: application/json" \
  -d '{
    "type": "like",
    "tweetUrl": "https://x.com/user/status/123456789"
  }'

# Reply to tweet
curl -X POST http://localhost:3000/api/twitter/action \
  -H "Content-Type: application/json" \
  -d '{
    "type": "reply",
    "tweetUrl": "https://x.com/user/status/123456789",
    "text": "Great insights! This really resonates..."
  }'

# Retweet
curl -X POST http://localhost:3000/api/twitter/action \
  -H "Content-Type: application/json" \
  -d '{
    "type": "retweet",
    "tweetUrl": "https://x.com/user/status/123456789"
  }'

# Quote tweet
curl -X POST http://localhost:3000/api/twitter/action \
  -H "Content-Type: application/json" \
  -d '{
    "type": "quote_tweet",
    "tweetUrl": "https://x.com/user/status/123456789",
    "text": "This! Adding to this point..."
  }'
```

### Step 4: Wait for Result

The API call returns immediately with the result:

**Success Response:**
```json
{
  "success": true,
  "action": "dm",
  "timestamp": "2026-01-22T17:30:00Z",
  "status": "sent",
  "rateLimit": {
    "allowed": true,
    "remaining": 28,
    "limit": 30,
    "resetDate": "2026-01-22"
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "action": "dm",
  "error": "Daily DM limit reached (30/day). Resets tomorrow.",
  "timestamp": "2026-01-22T17:30:00Z"
}
```

### Step 5: Report to User

Tell the user what happened:
- ✅ "Successfully sent DM to @founder123 (28 DMs remaining today)"
- ❌ "Failed to send DM: Daily limit reached. Resets tomorrow."
- ⏸️ "Already following @username. Skipping."

### Step 6: Activity Tracking (Automatic)

The extension automatically records all Twitter activity:
- Tracks follows, DMs, likes, retweets, replies
- Stores in browser IndexedDB
- Forwards to analytics database
- Triggers automated follow-up workflows

No manual recording needed!

## Example: Send Twitter DM

**User:** "DM @founder123 about a collaboration"

**You should:**

1. **Check extension:**
   ```bash
   curl http://localhost:3000/api/extension/status
   ```
   → Verify extension is connected

2. **Render template:**
   ```bash
   python .claude/scripts/template_loader.py render --path twitter/dms/collaboration --var first_name "Founder" --var my_name "Your Name" --var topic "AI tools"
   ```
   → Get rendered message: "Hey Founder! Love your content on AI tools..."

3. **Send to extension:**
   ```bash
   curl -X POST http://localhost:3000/api/twitter/action \
     -H "Content-Type: application/json" \
     -d '{
       "type": "dm",
       "username": "founder123",
       "message": "Hey Founder! Love your content on AI tools..."
     }'
   ```

4. **Get result (immediate):**
   ```json
   {
     "success": true,
     "status": "sent",
     "rateLimit": { "remaining": 28, "limit": 30 }
   }
   ```

5. **Report to user:**
   ```
   ✅ DM sent to @founder123 successfully! (28 DMs remaining today)
   ```

That's it! The extension handles all the browser automation automatically.

## Example: Follow and Engage Sequence

**User:** "Follow @techguru and like their latest tweet"

**You should:**

1. Show preview:
   ```
   ═══════════════════════════════════════════
   TWITTER ENGAGEMENT - @techguru
   ═══════════════════════════════════════════

   Actions:
   1. Follow @techguru
   2. Wait 2-3 minutes
   3. Like their latest tweet

   Estimated time: ~5 minutes
   ═══════════════════════════════════════════

   Proceed?
   ```

2. After approval, execute sequentially:
   ```bash
   # 1. Follow user
   curl POST /api/twitter/action { "type": "follow", "username": "techguru" }

   # 2. Wait (humanize)
   sleep(random(120, 180))

   # 3. Like their latest tweet
   curl POST /api/twitter/action { "type": "like", "tweetUrl": "..." }

   # 4. Report
   print("✅ Followed and engaged with @techguru")
   ```

## Example: Bulk DM Outreach (Single Approval)

**User:** "DM these 5 founders about my product"

**You should:**

1. Show preview:
   ```
   ═══════════════════════════════════════════
   TWITTER DM OUTREACH - 5 MESSAGES
   ═══════════════════════════════════════════

   Template: Founder Outreach

   Targets:
   1. @founder1 - John (CEO at StartupA)
   2. @founder2 - Jane (Founder at TechB)
   3. @founder3 - Bob (CTO at ProductC)
   4. @founder4 - Alice (Founder at AppD)
   5. @founder5 - Mike (CEO at PlatformE)

   Rate Limit: 30 DMs remaining today
   Estimated time: ~15 minutes (3 min/DM)
   ═══════════════════════════════════════════

   Proceed with all 5 DMs?
   ```

2. After single approval, execute ALL autonomously:
   ```bash
   for founder in targets:
     # 1. Render template
     message = render_template(founder)

     # 2. Send to extension
     result = curl POST /api/twitter/action {
       "type": "dm",
       "username": founder.handle,
       "message": message
     }

     # 3. Report progress
     print(f"✅ {founder.name}: {result.status}")

     # 4. Smart delay (2-4 minutes between DMs)
     sleep(random(120, 240))
   ```

3. Final summary:
   ```
   ✅ Bulk DM outreach complete!
   - 5/5 DMs sent successfully
   - 25 DMs remaining today
   - Activity recorded automatically
   ```

## Rate Limits (Built into Extension)

The extension automatically enforces these daily limits:

| Action | Daily Limit | Auto-Tracked | Error if Exceeded |
|--------|-------------|--------------|-------------------|
| follow | 50 | ✅ | "Daily follow limit reached" |
| dm | 30 | ✅ | "Daily DM limit reached" |
| like | 100 | ✅ | "Daily like limit reached" |
| reply | 50 | ✅ | "Daily reply limit reached" |
| retweet | 50 | ✅ | "Daily retweet limit reached" |

**All limits reset at midnight (local time).**

## Check Rate Limits

```bash
# Check extension status and rate limits
curl http://localhost:3000/api/twitter/limits
```

Response:
```json
{
  "follows": { "used": 15, "remaining": 35, "limit": 50 },
  "dms": { "used": 5, "remaining": 25, "limit": 30 },
  "likes": { "used": 40, "remaining": 60, "limit": 100 },
  "replies": { "used": 10, "remaining": 40, "limit": 50 },
  "retweets": { "used": 8, "remaining": 42, "limit": 50 },
  "resetDate": "2026-01-23"
}
```
   - Final summary when complete

## Rate Limits

| Action | Daily Limit | Min Delay | Max Delay |
|--------|-------------|-----------|-----------|
| follow | 50 | 60s | 300s |
| like_tweet | 100 | 30s | 120s |
| retweet | 50 | 60s | 300s |
| reply | 75 | 60s | 300s |
| dm | 50 | 60s | 300s |
| quote_tweet | 50 | 60s | 300s |

## Check Rate Limits

```bash
# Check remaining actions
python .claude/scripts/rate_limiter.py --user default --platform twitter --remaining

# Check if specific action is allowed
python .claude/scripts/rate_limiter.py --user default --platform twitter --action dm --check
```

## Special Considerations

### DMs Require Mutual Following or Open DMs
- If you can't DM someone, try following them first
- Some users have DMs open to everyone
- Some require mutual following

### Tweet Character Limits
- Tweets/replies: 280 characters max
- DMs: 10,000 characters max
- Adapter automatically truncates if needed

### Rate Limit Sensitivity
Twitter is very sensitive to automation. The delays are designed to mimic human behavior:
- Random delays between actions
- No actions during unusual hours
- Burst detection and cooldown
