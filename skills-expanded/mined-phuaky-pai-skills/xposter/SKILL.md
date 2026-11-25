---
name: XPoster
description: Transform raw ideas into Balaji-style X posts — assertive, numbered, evidence-backed. USE WHEN tweet, X post, Twitter, draft post, publish, social media, process input, score tweet, check quality, generate image, update algorithm, daily digest.
---

# XPoster

Autonomous agent for processing raw ideas into Balaji Srinivasan-style X posts.
Assertive voice. Numbered points. Evidence in every claim. No engagement bait.

**Two formats:** Short numbered post (100-500 words) OR long article (500-3000+ words). Nothing in between.

## Customization

**Before executing, check for user customizations at:**
`~/.claude/skills/PAI/USER/SKILLCUSTOMIZATIONS/XPoster/`

## Voice Notification

**When executing a workflow, do BOTH:**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Running the WORKFLOWNAME workflow in the XPoster skill"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **WorkflowName** workflow in the **XPoster** skill...
   ```

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **Draft** | "/post", "/capture", "draft:", "tweet about", "post about", "turn this into a post" | `Workflows/Draft.md` |
| **BatchProcess** | "process input", "scan input", "process captures", "session posts", "batch process" | `Workflows/BatchProcess.md` |
| **Validate** | "validate", "score", "quality check" | `Workflows/Validate.md` |
| **Organize** | "organize", "move to ready/drafts" | `Workflows/Organize.md` |
| **Schedule** | "schedule", "queue for posting" | `Workflows/Schedule.md` |
| **GenerateVisual** | "generate image", "add visual" | `Workflows/GenerateVisual.md` |
| **UpdateAlgorithm** | "update algorithm", "fetch nikita" | `Workflows/UpdateAlgorithm.md` |
| **DailyDigest** | "daily digest", "what did I build today", "session digest", "digest my day", "today's sessions" | `Workflows/DailyDigest.md` |

## Tools

```bash
bun run ~/.claude/skills/XPoster/Tools/ScoreTweet.ts "Your tweet"
```

> **NOTE:** ScoreTweet.ts uses legacy scoring logic. Use `ContentRules.md` as ground truth for quality assessment until the tool is updated.

## MCP Integration

```javascript
mcp__x-server__create_tweet({ text: "content" })
mcp__x-server__reply_to_tweet({ tweet_id: "id", text: "reply" })
```

## Full Documentation

- Content & scoring rules: `ContentRules.md`
- X algorithm: `XAlgorithm.md`
- Post templates: `TweetFormats.md`
- Account setup: `AccountStructure.md`

## Examples

**Example 1: Draft from conversation**
```
User: "/post"
-> Invokes Draft workflow (conversation source)
-> Finds thesis in conversation
-> Writes numbered post with evidence
-> Returns Balaji-style draft
```

**Example 2: Draft from idea**
```
User: "draft: replaced Calendly with 200 lines of TypeScript"
-> Invokes Draft workflow (inline source)
-> Structures as numbered post: thesis, evidence points, conclusion
-> Returns assertive, evidence-backed draft
```

**Example 3: Batch processing**
```
User: "process input for software30"
-> Invokes BatchProcess workflow
-> Scans INPUT folder, finds thesis for each item
-> Structures as Balaji-style posts, saves to OUTPUT/drafts/
```
