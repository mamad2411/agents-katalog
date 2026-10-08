---
name: writer-com
description: Use Writer.com API for content review, AI detection, grammar/style checking, and style guide enforcement. Use when editing essays, blog posts, or any content that needs humanization, style review, or AI trope detection.
---

# Writer.com Skill

Content review and style enforcement using Writer.com API.

## Capabilities

| Tool | Endpoint | Use |
|------|----------|-----|
| AI Detection | `/v1/tools/ai-detect` | Detect AI-generated content |
| Content Check | Enterprise API | Check against style guide (grammar, style, terminology) |

## API Configuration

| Setting | Value |
|---------|-------|
| API Key | See TOOLS.md (`WRITER_API_KEY`) |
| Base URL | `https://api.writer.com` |
| Enterprise URL | `https://enterprise-api.writer.com` |

## AI Detection

Detect if content is AI- or human-generated.

**Requirements:**
- Content must be at least 350 characters
- Returns confidence score (0-1)

**Request:**
```bash
curl -X POST https://api.writer.com/v1/tools/ai-detect \
  -H "Authorization: Bearer $WRITER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"content": "Your text here..."}'
```

**Response:**
```json
{
  "label": "fake" | "real",
  "score": 0.87
}
```

**Interpretation:**
- `fake` + high score = likely AI-generated
- `real` + high score = likely human-written
- Score < 0.6 = uncertain

## Content Check (Enterprise)

Check content against your Writer.com style guide.

**Note:** Requires `organizationId` and `teamId` from Writer.com dashboard.

**Request:**
```bash
curl -X POST "https://enterprise-api.writer.com/content/organization/{orgId}/team/{teamId}/check" \
  -H "Authorization: Bearer $WRITER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Your text here...",
    "settings": {
      "suggestions": ["grammar", "style", "terminology"]
    }
  }'
```

**Response:**
```json
{
  "issues": [
    {
      "type": "grammar",
      "message": "Consider revising...",
      "position": {"start": 0, "end": 10}
    }
  ]
}
```

## Editor Pipeline

The writer-com skill is part of the editor pipeline:

1. **Humanizer** (humanizer skill) - Add conversational tone
2. **Writer.com Review** (this skill) - Check grammar, style, AI detection
3. **Tone/Voice Rules** - Apply brand voice (custom rules)
4. **AI Trope Check** - Flag overused AI phrases

### Pipeline Workflow

```bash
# Step 1: Run AI detection first
# If score > 0.8, content needs humanization

# Step 2: Humanize content
# Use humanizer skill

# Step 3: Check style guide
# Run content check against style guide

# Step 4: Review issues and apply fixes
# Iterate until issues < 5
```

## Common Patterns

### Check Essay Before Publishing

```bash
# Check AI score
AI_SCORE=$(curl -s -X POST https://api.writer.com/v1/tools/ai-detect \
  -H "Authorization: Bearer $WRITER_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"content\": \"$ESSAY\"}" | jq '.score')

if (( $(echo "$AI_SCORE > 0.7" | bc -l) )); then
  echo "Content feels AI-generated (score: $AI_SCORE). Run humanizer."
else
  echo "Content passes AI detection (score: $AI_SCORE)"
fi
```

### Batch Style Check

For longer content, check in sections:
1. Split content into paragraphs
2. Check each section
3. Aggregate issues
4. Apply fixes systematically

## Rate Limits

Writer.com has rate limits. For bulk operations:
- Batch requests where possible
- Add delays between API calls
- Cache results for unchanged content

## Integration Points

| Skill | Integration |
|-------|-------------|
| humanizer | Run before Writer.com check |
| content-publishing | Run after essay is complete |
| speaking-framework | Apply when converting to video script |

## Notes

- Writer.com updates may change endpoints; check `dev.writer.com` for latest docs
- Enterprise API requires org/team IDs from dashboard
- Content check returns position data for precise fixes