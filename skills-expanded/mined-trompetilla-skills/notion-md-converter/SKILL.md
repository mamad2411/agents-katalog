# SKILL.md - Notion Markdown Converter

Convert Markdown content to Notion blocks using the Martian library.

## When to Use

- Creating Notion pages from Markdown content
- Converting journal entries, notes, or documentation
- Batch importing Markdown files to Notion
- Preparing formatted content for Notion databases

## Installation

```bash
cd ~/.openclaw/workspace/skills/notion-md-converter
npm install
```

Set environment variable:
```bash
export NOTION_TOKEN="ntn_your_token_here"
```

## Usage

### Option 1: Use the Library

```javascript
const { convertMarkdownToBlocks, createNotionPageFromMarkdown } = require('./skills/notion-md-converter/src/converter');

// Convert markdown to blocks
const { success, blocks, error, warning } = convertMarkdownToBlocks(`
## Today's Progress

Completed tasks:
- [x] Research complete
- [x] Design approved
- [ ] Implementation pending

> [!TIP]
> Remember to update the task plan!
`);

if (success) {
  // Use blocks with Notion API
  console.log(`Converted to ${blocks.length} blocks`);
}
```

### Option 2: Create Page Directly

```javascript
const result = await createNotionPageFromMarkdown({
  parentId: 'your-parent-page-id',
  title: 'Journal Entry - 2026-02-10',
  markdown: content,
  notionToken: process.env.NOTION_TOKEN
});

if (result.success) {
  console.log(`Created page: ${result.url}`);
}
```

### Option 3: CLI Tool

```bash
node tools/md2notion.js \
  --parent-id "abc123" \
  --title "My Page" \
  --file content.md \
  --token "ntn_xxx"
```

## Supported Markdown

| Markdown | Notion Block |
|----------|--------------|
| `# Heading` | `heading_1` |
| `## Heading` | `heading_2` |
| `### Heading` | `heading_3` |
| `**bold**` | Rich text annotation |
| `*italic*` | Rich text annotation |
| `` `code` `` | Inline code |
| `- list item` | `bulleted_list_item` |
| `1. numbered` | `numbered_list_item` |
| `- [x] task` | `to_do` (checked) |
| `- [ ] task` | `to_do` (unchecked) |
| ````code```` | `code` block |
| `> quote` | `quote` or `callout` |
| `> [!NOTE]` | Blue callout |
| `> [!WARNING]` | Yellow callout |
| `> [!CAUTION]` | Red callout |
| `\| table \|` | `table` |

## Error Handling

The skill handles common issues gracefully:

- **Invalid markdown**: Returns fallback plain text block
- **Content too long**: Auto-truncates to 100 blocks with warning
- **API errors**: Returns detailed error message
- **Missing token**: Clear error about NOTION_TOKEN

## Limitations

- Notion API limits: 100 blocks per request
- Image URLs must be publicly accessible
- Tables have limited formatting options
- Nested blocks >2 levels may be flattened

## Integration with Journal System

This skill is designed for the Galatea Journal system:

```javascript
// In your Journal cron or automation
const { createNotionPageFromMarkdown } = require('./skills/notion-md-converter/src/converter');

async function createJournalEntry(date, content) {
  return await createNotionPageFromMarkdown({
    parentId: process.env.JOURNAL_DATABASE_ID,
    title: `Journal - ${date}`,
    markdown: content
  });
}
```

## Testing

```bash
npm test
```

## Dependencies

- `@tryfabric/martian`: Markdown to Notion block conversion
- `@notionhq/client`: Official Notion API client

## License

MIT
