---
name: instagram-adapter
description: |
  Instagram automation adapter for the 100X Outreach System.
  Use this skill when performing Instagram actions like following, DMing, liking posts, commenting, or replying to stories.
  This skill controls the 10x Team Browser Extension to execute Instagram actions with templates.
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

# Instagram Adapter Skill

Automates Instagram actions using the 10x Team Universal Browser Extension with intelligent template rendering.

## 10x Team Browser Extension: Local Control

**Fast, local browser automation!** The 10x Team extension provides direct control over your browser via WebSocket.

Benefits of WebSocket integration:
- ✅ **Faster**: Local execution, no cloud latency
- ✅ **Free**: No usage costs
- ✅ **Visible**: See actions in real-time
- ✅ **Persistent**: Uses your real Instagram account
- ✅ **Activity Tracking**: All actions logged automatically
- ✅ **Rate Limiting**: Smart rate limits prevent Instagram detection

## Architecture

```
Claude Code (You)
    ↓ HTTP API
Canvas Server (localhost:3000)
    ↓ WebSocket
Browser Extension
    ↓ Chrome APIs
Instagram.com
```

## IMPORTANT: You Control the Extension

**You are the brain that orchestrates the extension.** This skill tells you exactly how to:
1. Load and render templates
2. Send commands to the extension via HTTP API
3. Wait for action results
4. Monitor and report progress

## When to Use This Skill

Use this skill when the user wants to:
- Follow Instagram accounts
- Send Instagram DMs
- Like Instagram posts
- Comment on posts
- Reply to stories
- Engage with Instagram content

## Available Instagram Actions

| Action | Description | Max Steps |
|--------|-------------|-----------|
| `follow` | Follow an Instagram user | 6 |
| `like_post` | Like a post | 6 |
| `comment` | Comment on a post | 8 |
| `dm` | Send a direct message | 10 |
| `story_reply` | Reply to a story | 10 |

## Available Templates

### DMs (`templates/instagram/dms/`)
- `cold_dm.md` - Cold outreach DM
- `after_follow.md` - DM after following
- `story_reply.md` - Reply to story
- `mutual_follower.md` - Mutual follower intro
- `collaboration.md` - Collaboration request
- `business_inquiry.md` - Business inquiry
- `thank_you.md` - Thank you message
- `influencer_outreach.md` - Influencer outreach
- `brand_collaboration.md` - Brand collaboration
- `creator_partnership.md` - Creator partnership
- `expert_connect.md` - Expert connection
- `product_feature.md` - Product feature request
- `founder_connect.md` - Founder connection

### Comments (`templates/instagram/comments/`)
- `engagement.md` - General engagement
- `compliment.md` - Compliment their content
- `question.md` - Ask a question
- `support.md` - Show support
- `value_add.md` - Add value
- `appreciation.md` - Show appreciation

### Stories (`templates/instagram/stories/`)
- `story_reply.md` - Reply to story
- `story_mention.md` - Mention in story
- `story_reaction.md` - React to story

## CRITICAL: Step-by-Step Execution Flow

**Same architecture as LinkedIn/Twitter adapters** - see those for detailed flow.

### Quick Start

1. **Verify extension connected:**
   ```bash
   curl http://localhost:3000/api/extension/status
   ```

2. **Render template (if needed):**
   ```bash
   python .claude/scripts/template_loader.py render --path instagram/dms/cold_dm --var first_name "John" --var my_name "Your Name"
   ```

3. **Send action to extension via HTTP API:**

```bash
# Follow user
curl -X POST http://localhost:3000/api/instagram/action \
  -H "Content-Type: application/json" \
  -d '{
    "type": "follow",
    "username": "influencer123"
  }'

# Send DM
curl -X POST http://localhost:3000/api/instagram/action \
  -H "Content-Type: application/json" \
  -d '{
    "type": "dm",
    "username": "brandowner",
    "message": "Hi! Love your brand aesthetic..."
  }'

# Like post
curl -X POST http://localhost:3000/api/instagram/action \
  -H "Content-Type: application/json" \
  -d '{
    "type": "like",
    "postUrl": "https://instagram.com/p/ABC123XYZ"
  }'

# Comment on post
curl -X POST http://localhost:3000/api/instagram/action \
  -H "Content-Type: application/json" \
  -d '{
    "type": "comment",
    "postUrl": "https://instagram.com/p/ABC123XYZ",
    "comment": "Amazing content! Really inspiring!"
  }'

# Reply to story
curl -X POST http://localhost:3000/api/instagram/action \
  -H "Content-Type: application/json" \
  -d '{
    "type": "story_reply",
    "username": "creator456",
    "message": "This is so relatable!"
  }'
```

4. **Get immediate result:**
   ```json
   {
     "success": true,
     "action": "dm",
     "status": "sent",
     "rateLimit": { "remaining": 45, "limit": 50 }
   }
   ```

5. **Report to user:**
   ```
   ✅ DM sent to @brandowner! (45 DMs remaining today)
   ```

## Rate Limits (Built into Extension)

The extension automatically enforces these daily limits:

| Action | Daily Limit | Auto-Tracked | Error if Exceeded |
|--------|-------------|--------------|-------------------|
| follow | 50 | ✅ | "Daily follow limit reached" |
| dm | 50 | ✅ | "Daily DM limit reached" |
| like | 100 | ✅ | "Daily like limit reached" |
| comment | 40 | ✅ | "Daily comment limit reached" |
| story_reply | 50 | ✅ | "Daily story reply limit reached" |

**All limits reset at midnight (local time).**

**Instagram is MORE strict than LinkedIn/Twitter!** The extension uses longer delays:
- 48-72 hours between DMs
- 24-48 hours after following before DMing
- Human-like randomization to avoid detection

## Check Rate Limits

```bash
# Check extension status and rate limits
curl http://localhost:3000/api/instagram/limits
```

Response:
```json
{
  "follows": { "used": 20, "remaining": 30, "limit": 50 },
  "dms": { "used": 5, "remaining": 45, "limit": 50 },
  "likes": { "used": 60, "remaining": 40, "limit": 100 },
  "comments": { "used": 15, "remaining": 25, "limit": 40 },
  "storyReplies": { "used": 10, "remaining": 40, "limit": 50 },
  "resetDate": "2026-01-23"
}
```

## Example: Send Instagram DM

**User:** "DM @influencer about a brand collaboration"

**You should:**

1. **Check extension:**
   ```bash
   curl http://localhost:3000/api/extension/status
   ```
   → Verify extension is connected

2. **Render template:**
   ```bash
   python .claude/scripts/template_loader.py render --path instagram/dms/brand_collaboration --var first_name "Influencer" --var company "My Brand" --var my_name "Your Name"
   ```
   → Get rendered message: "Hi! Your brand aesthetic is amazing..."

3. **Send to extension:**
   ```bash
   curl -X POST http://localhost:3000/api/instagram/action \
     -H "Content-Type: application/json" \
     -d '{
       "type": "dm",
       "username": "influencer",
       "message": "Hi! Your brand aesthetic is amazing..."
     }'
   ```

4. **Get result (immediate):**
   ```json
   {
     "success": true,
     "status": "sent",
     "rateLimit": { "remaining": 45, "limit": 50 }
   }
   ```

5. **Report to user:**
   ```
   ✅ DM sent to @influencer successfully! (45 DMs remaining today)
   ```

## Example: Warm-Up Engagement Sequence

**User:** "Engage with @creator - like their post and leave a comment"

**You should:**

1. Show preview:
   ```
   ═══════════════════════════════════════════
   INSTAGRAM ENGAGEMENT - @creator
   ═══════════════════════════════════════════

   Actions:
   1. Like their most recent post
   2. Leave an engaging comment

   Template: Engagement comment

   Estimated time: ~5 minutes (with delay)
   ═══════════════════════════════════════════

   Proceed?
   ```

2. After approval, execute sequentially:
   ```bash
   # 1. Like post
   curl POST /api/instagram/action { "type": "like", "postUrl": "..." }

   # 2. Wait (humanize)
   sleep(random(90, 420))

   # 3. Post comment
   curl POST /api/instagram/action { "type": "comment", "postUrl": "...", "comment": "Amazing content!" }

   # 4. Report
   print("✅ Engaged with @creator")
   ```

## Example: Bulk Influencer Outreach (Single Approval)

**User:** "Reach out to these 5 influencers about a collaboration"

**You should:**

1. Show preview:
   ```
   ═══════════════════════════════════════════
   INSTAGRAM INFLUENCER OUTREACH - 5 DMS
   ═══════════════════════════════════════════

   Template: Influencer Outreach

   Targets:
   1. @influencer1 - Sarah (50K followers)
   2. @influencer2 - Mike (75K followers)
   3. @influencer3 - Emma (120K followers)
   4. @influencer4 - David (45K followers)
   5. @influencer5 - Lisa (90K followers)

   Estimated time: ~35 minutes
   ═══════════════════════════════════════════

   Proceed with all 5 DMs?
   ```

2. After single approval, execute ALL autonomously:
   ```bash
   for influencer in targets:
     # 1. Render template
     message = render_template(influencer)

     # 2. Send to extension
     result = curl POST /api/instagram/action {
       "type": "dm",
       "username": influencer.handle,
       "message": message
     }

     # 3. Report progress
     print(f"✅ {influencer.name}: {result.status}")

     # 4. Smart delay (1.5-7 minutes between DMs)
     sleep(random(90, 420))
   ```

3. Final summary:
   ```
   ✅ Bulk influencer outreach complete!
   - 5/5 DMs sent successfully
   - 45 DMs remaining today
   - Activity recorded automatically
   ```

## Rate Limits

| Action | Daily Limit | Min Delay | Max Delay |
|--------|-------------|-----------|-----------|
| follow | 30 | 90s | 420s |
| like_post | 60 | 30s | 180s |
| comment | 20 | 90s | 420s |
| dm | 30 | 90s | 420s |
| story_reply | 30 | 90s | 420s |

## Check Rate Limits

```bash
# Check remaining actions
python .claude/scripts/rate_limiter.py --user default --platform instagram --remaining

# Check if specific action is allowed
python .claude/scripts/rate_limiter.py --user default --platform instagram --action dm --check
```

## Special Considerations

### DMs May Require Following
- Some accounts have DMs restricted to followers only
- Consider following first, then DMing later

### Comment Character Limits
- Comments: 2,200 characters max
- But shorter comments (under 150 chars) look more natural

### Story Replies
- Story replies go to their DMs
- Stories expire after 24 hours
- Good way to start conversations naturally

### Instagram is Very Sensitive
Instagram is the most aggressive at detecting automation:
- Longer delays than other platforms
- Random patterns are essential
- Avoid bulk actions in short periods
- The rate limiter has extra safety margins built in
