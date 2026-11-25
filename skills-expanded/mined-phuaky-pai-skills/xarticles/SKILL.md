---
name: XArticles
description: Create long-form X Articles with templates, scoring, and promotion workflows. USE WHEN article, X article, long-form, write article, deep dive, tutorial, publish article, promote article, article draft.
---

# XArticles

Autonomous agent for creating engagement-optimized long-form articles on X (formerly Twitter Articles/Notes).

**X Articles = on-platform long-form content.** Up to ~100K characters (~15K words). Rich formatting (bold, italic, headers, lists, images, embeds). Premium required. No link penalty since content stays on X.

**Key advantage:** Articles avoid the -25% link penalty, increase dwell time, and generate conversation-style engagement that the algorithm rewards (reply-to-reply = 150x a like).

## Customization

**Before executing, check for user customizations at:**
`~/.claude/skills/PAI/USER/SKILLCUSTOMIZATIONS/XArticles/`

## Voice Notification

**When executing a workflow, do BOTH:**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Running the WORKFLOWNAME workflow in the XArticles skill"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **WorkflowName** workflow in the **XArticles** skill...
   ```

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **Draft** | "write article", "article about", "deep dive on", "article draft", "long-form" | `Workflows/Draft.md` |
| **Promote** | "promote article", "tweet about article", "share article" | `Workflows/Promote.md` |

## Publishing Note

X does not currently offer an API for creating Articles. The Draft workflow outputs formatted text optimized for pasting into X's WYSIWYG article editor. The Promote workflow handles the automated part — tweeting about your published article via `mcp__x-server__create_tweet`.

## MCP Integration

```javascript
// For promotion tweets (not article creation itself)
mcp__x-server__create_tweet({ text: "promotion tweet content" })
mcp__x-server__reply_to_tweet({ tweet_id: "id", text: "self-reply with link" })
```

## Full Documentation

- Article templates: `ArticleFormats.md`
- Scoring & quality rules: `ArticleRules.md`
- Tweet promotion quality: `../XPoster/ContentRules.md` (cross-reference)
- X algorithm context: `../XPoster/XAlgorithm.md` (shared)

## Examples

**Example 1: Article from idea**
```
User: "write article about building a 79-skill AI system"
-> Invokes Draft workflow
-> Selects Build Log Deep Dive template
-> Structures article with hook, sections, visuals
-> Scores, iterates, returns formatted draft
```

**Example 2: Article from conversation**
```
User: "turn this into an article"
-> Invokes Draft workflow (conversation source)
-> Mines conversation for article-worthy content
-> Expands into full long-form piece
-> Returns formatted draft for X's editor
```

**Example 3: Promote published article**
```
User: "promote article" (with article URL or title)
-> Invokes Promote workflow
-> Drafts companion tweet using XPoster quality rules
-> Drafts self-reply thread with key takeaways
-> Posts via MCP
```
