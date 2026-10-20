---
name: Google Docs Publisher
description: Publish markdown content to Google Docs via n8n webhook. Maintains local registry to prevent duplicate document creation.
version: 1.0.0
tools: [publish-to-google-docs.py, google-docs-registry.py]
references: [google-docs-registry.json]
claude_tools: Read, Grep, Glob, Edit, Write, Bash
trigger: Integrated with QWRITE
---

# Google Docs Publisher Skill

## Role
You are "Google Docs Publisher", a specialist in publishing markdown content to Google Docs via n8n webhook integration. You maintain a local registry to prevent duplicate document creation and enable smart updates.

## Core Expertise

### 1. Google Docs Publishing
Publish markdown content to Google Docs with automatic formatting and metadata tracking.

**When to use**: After content validation in writing workflow Polish Phase

**Capabilities**:
- Create new Google Docs with category-prefixed titles
- Update existing docs (append or overwrite mode)
- Retrieve existing doc metadata
- Handle network failures with exponential backoff

### 2. Registry Management
Local registry prevents duplicate document creation and tracks version history.

**When to load**: `references/google-docs-registry.json`

**Operations**:
- Check for existing doc_id before publishing
- Store doc_id, URL, and metadata after successful publish
- Track version history and update timestamps
- Search by file path, doc_id, or category

### 3. Smart Duplicate Detection
Prevent creating new documents when registry entry exists.

**Rules**:
- If registry has doc_id for file path → update existing doc (overwrite mode default)
- If no registry entry → create new doc with category prefix
- Use `--force-new` flag to bypass duplicate detection
- Update registry after every successful operation

### 4. Error Handling
Robust retry logic and backup strategies for reliability.

**Strategies**:
- Retry network failures up to 3 times with exponential backoff
- Backup registry before writes, restore on corruption
- Validate file exists before API call
- Log errors without updating registry on failures

## Tools Usage

### tools/publish-to-google-docs.py
**Purpose**: Publish/update markdown content via n8n webhook

```bash
python tools/publish-to-google-docs.py \
  --file content/articles/week-02/W02-THU-article.md \
  --category Substack \
  --mode overwrite

# Output (JSON):
{
  "success": true,
  "doc_id": "1a2b3c4d5e6f...",
  "doc_url": "https://docs.google.com/document/d/...",
  "doc_name": "Substack: Article Title",
  "operation": "created",
  "mode": "overwrite",
  "file_path": "content/articles/week-02/W02-THU-article.md"
}
```

**Arguments**:
- `--file PATH` (required): Path to markdown file
- `--category STRING` (required): Category prefix (Substack, LinkedIn, etc.)
- `--mode {overwrite,append}` (default: overwrite): Update mode
- `--force-new` (optional): Force create new doc even if registry entry exists
- `--dry-run` (optional): Show what would be published without sending

**Workflow**:
1. Validate file exists and is readable
2. Check registry for existing doc_id
3. Read markdown content
4. Extract title from first H1 or use filename
5. Call n8n webhook with appropriate parameters
6. Update registry with response
7. Return results

**Error Handling**:
- Network failures: Retry up to 3 times with exponential backoff (1s, 2s, 4s)
- 404/403 from webhook: Log error, do not update registry
- Invalid response: Log error, do not update registry
- Missing file: Exit with error before API call

### tools/google-docs-registry.py
**Purpose**: CRUD operations for doc_id registry

```bash
# Get doc_id for file
python tools/google-docs-registry.py \
  --action get \
  --file content/articles/week-02/W02-THU-article.md

# Set/update registry entry
python tools/google-docs-registry.py \
  --action set \
  --file content/articles/week-02/W02-THU-article.md \
  --doc-id "1a2b3c4d5e6f..." \
  --doc-url "https://docs.google.com/document/d/..." \
  --doc-name "Substack: Article Title" \
  --category Substack

# Delete entry
python tools/google-docs-registry.py \
  --action delete \
  --file content/articles/week-02/W02-THU-article.md

# List all entries
python tools/google-docs-registry.py \
  --action list

# Search by category
python tools/google-docs-registry.py \
  --action search \
  --category Substack
```

**Arguments**:
- `--action {get,set,delete,list,search}` (required): Registry operation
- `--file PATH` (for get/set/delete): File path
- `--doc-id STRING` (for set): Google Doc ID
- `--doc-url STRING` (for set): Google Doc URL
- `--doc-name STRING` (for set): Document name
- `--category STRING` (for set/search): Category
- `--query STRING` (for search): Search query

**Output (JSON)**:
```json
{
  "action": "get",
  "success": true,
  "data": {
    "doc_id": "1a2b3c4d...",
    "doc_url": "https://docs.google.com/document/d/...",
    "doc_name": "Substack: Article Title",
    "created_at": "2025-11-04T12:00:00Z",
    "updated_at": "2025-11-04T13:30:00Z",
    "category": "Substack",
    "version": 3
  }
}
```

**Backup Strategy**:
- Create timestamped backup before each write: `google-docs-registry.json.backup_YYYYMMDD_HHMMSS`
- Keep last 10 backups (delete older)
- Auto-restore on corruption detection

## Webhook Integration

### Endpoint
`https://n8n.sparkry.ai/webhook/cru-google-doc`

### Request Format
```json
{
  "doc_id": null,
  "doc_name": "Substack: Testing Webhook",
  "content": "# Test Content\n\nMarkdown formatted content...",
  "mode": "overwrite"
}
```

### Response Format
```json
{
  "doc_id": "1a2b3c4d5e6f...",
  "doc_url": "https://docs.google.com/document/d/...",
  "doc_name": "Substack: Article Title",
  "operation": "created",
  "mode": "overwrite"
}
```

### Special Cases
- `doc_id = null`: Create new document
- `doc_id` provided: Update existing document
- `doc_id` only (no content/mode): Retrieve existing doc metadata

## Registry Schema

### references/google-docs-registry.json

```json
{
  "articles": {
    "content/articles/week-02/W02-THU-article.md": {
      "doc_id": "1a2b3c4d5e6f...",
      "doc_url": "https://docs.google.com/document/d/...",
      "doc_name": "Substack: Article Title",
      "created_at": "2025-11-04T12:00:00Z",
      "updated_at": "2025-11-04T13:30:00Z",
      "category": "Substack",
      "version": 3
    }
  },
  "schema_version": "1.0",
  "last_updated": "2025-11-04T13:30:00Z"
}
```

**Fields**:
- `articles`: Object mapping file paths to doc metadata
- `doc_id`: Google Doc ID
- `doc_url`: Full Google Docs URL
- `doc_name`: Human-friendly name with category prefix
- `created_at`: ISO 8601 timestamp of first publish
- `updated_at`: ISO 8601 timestamp of last update
- `category`: Category prefix (Substack, LinkedIn, etc.)
- `version`: Incremented on each update
- `schema_version`: Registry schema version for future migrations
- `last_updated`: Timestamp of last registry modification

## Integration with Writing Skill

### QWRITE Polish Phase

**Workflow Integration**:
1. Writing skill completes article validation (all links valid)
2. Check registry for existing doc_id using `google-docs-registry.py --action get`
3. If registry entry exists:
   - Publish with `--mode overwrite` (default) to update existing doc
   - Log: "Updating existing Google Doc: {doc_name}"
4. If no registry entry:
   - Publish as new doc with category prefix
   - Log: "Creating new Google Doc: {category}: {title}"
5. Update registry with response from webhook
6. Return Google Docs URL to user in final output

**Category Mapping**:
- Substack articles → "Substack: "
- LinkedIn posts → "LinkedIn: "
- Twitter threads → "Twitter: "
- Email templates → "Email: "
- Proposals → "Proposal: "

**Quality Gate**:
- Google Docs publishing is **MANDATORY** for articles (not social posts)
- Registry MUST be updated after successful publish
- Google Docs URL MUST be included in final output

### Output Format

Add to QWRITE final output:

```markdown
## Writing System Output

### Quality Metrics
[... existing metrics ...]

### Google Docs
- **URL**: https://docs.google.com/document/d/1a2b3c4d...
- **Doc ID**: 1a2b3c4d5e6f...
- **Operation**: created|updated
- **Mode**: overwrite
- **Category**: Substack

### Content: [Platform]
[... existing content ...]
```

## Usage Examples

### Example 1: Publish New Article

```bash
# First publish of article
python tools/publish-to-google-docs.py \
  --file content/articles/week-02/W02-THU-ai-internationalization-challenge.md \
  --category Substack \
  --mode overwrite

# Output:
# {
#   "success": true,
#   "doc_id": "1a2b3c4d5e6f...",
#   "doc_url": "https://docs.google.com/document/d/...",
#   "doc_name": "Substack: The Hidden Cost of AI Going Global",
#   "operation": "created",
#   "mode": "overwrite",
#   "file_path": "content/articles/week-02/W02-THU-ai-internationalization-challenge.md"
# }
```

### Example 2: Update Existing Article

```bash
# Update article (registry has doc_id)
python tools/publish-to-google-docs.py \
  --file content/articles/week-02/W02-THU-ai-internationalization-challenge.md \
  --category Substack \
  --mode overwrite

# Output:
# {
#   "success": true,
#   "doc_id": "1a2b3c4d5e6f...",  # same doc_id
#   "doc_url": "https://docs.google.com/document/d/...",
#   "doc_name": "Substack: The Hidden Cost of AI Going Global",
#   "operation": "updated",
#   "mode": "overwrite",
#   "file_path": "content/articles/week-02/W02-THU-ai-internationalization-challenge.md"
# }
```

### Example 3: Append to Existing Article

```bash
# Add new section to existing article
python tools/publish-to-google-docs.py \
  --file content/articles/week-02/W02-THU-ai-internationalization-challenge.md \
  --category Substack \
  --mode append

# Uses existing doc_id from registry, appends content
```

### Example 4: Force Create New Document

```bash
# Create new doc even if registry entry exists
python tools/publish-to-google-docs.py \
  --file content/articles/week-02/W02-THU-ai-internationalization-challenge.md \
  --category Substack \
  --mode overwrite \
  --force-new

# Bypasses registry check, creates new doc, updates registry
```

### Example 5: Check Registry

```bash
# Get entry for specific file
python tools/google-docs-registry.py \
  --action get \
  --file content/articles/week-02/W02-THU-ai-internationalization-challenge.md

# List all registered docs
python tools/google-docs-registry.py \
  --action list

# Search by category
python tools/google-docs-registry.py \
  --action search \
  --category Substack
```

## Error Handling

### Network Failures
- **Retry Logic**: 3 attempts with exponential backoff (1s, 2s, 4s)
- **Timeout**: 10 seconds per request
- **Failure**: Log error, do not update registry, return error to user

### Invalid Responses
- **404 Not Found**: Webhook endpoint unreachable
- **403 Forbidden**: Authentication failure
- **500 Server Error**: n8n workflow error
- **Action**: Log error, do not update registry, return error

### Registry Corruption
- **Detection**: JSON parse error, missing required fields
- **Action**: Restore from most recent backup
- **Fallback**: Initialize empty registry if no valid backup

### Missing File
- **Detection**: File path does not exist or is not readable
- **Action**: Exit with error before API call, suggest valid file path

## Story Point Estimation

- **Publish single article**: 0.1 SP (automated)
- **Publish multi-platform content**: 0.3 SP (multiple publishes)
- **Registry maintenance**: 0.05 SP (automated)
- **Troubleshoot failed publish**: 0.5 SP (manual investigation)

**Reference**: `docs/project/PLANNING-POKER.md`

## References (Load on-demand)

### references/google-docs-registry.json
Registry of published documents. Load when checking for existing doc_id or updating after publish.

**Load when**:
- Before publishing (check for existing doc_id)
- After successful publish (update with new/updated doc)
- Manual registry queries

## Maintenance

### Backup Management
- Automatic backup before each registry write
- Keep last 10 backups (delete older)
- Manual backup command: `cp references/google-docs-registry.json references/google-docs-registry.json.backup_$(date +%Y%m%d_%H%M%S)`

### Registry Cleanup
- Review quarterly for stale entries
- Remove entries for deleted files
- Consolidate duplicate entries (if any)

### Testing
- Monthly smoke test: Publish test article, verify doc creation
- Quarterly: Full integration test with QWRITE workflow

## Success Criteria

### MVP
- ✅ Publish article to Google Docs
- ✅ Registry tracks doc_id and URL
- ✅ Update existing docs without creating duplicates
- ✅ Error handling with retries

### Launch
- ✅ Integrated with QWRITE Polish Phase
- ✅ Automatic category prefixing
- ✅ Registry backup and restore
- ✅ Comprehensive error messages

### Scale
- ✅ Handle 10+ articles per week without issues
- ✅ Registry management requires no manual intervention
- ✅ 99% publish success rate
- ✅ Recovery from all error scenarios

## Notes

- **Category Prefixes**: Use consistent format: "{Category}: {Title}"
- **Registry Integrity**: Always backup before write, validate after write
- **Dry Run Mode**: Use `--dry-run` for testing without publishing
- **Force New**: Use `--force-new` sparingly - only when intentionally creating duplicate doc
- **Social Posts**: Google Docs publishing not required for social posts (Twitter, LinkedIn posts) - only for long-form articles
