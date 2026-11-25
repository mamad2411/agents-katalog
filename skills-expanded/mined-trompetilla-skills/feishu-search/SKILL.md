# Feishu Search Skill

Unified search interface for Feishu (Lark) resources.

## Features

- **Search Messages**: Find chat history across private and group chats.
- **Search Docs**: Locate documents, sheets, and bitables.
- **Search Calendar**: (Planned) Find events.

## Usage

```bash
# Search messages
node skills/feishu-search/index.js search_messages --query "bug report" --limit 10

# Search docs
node skills/feishu-search/index.js search_docs --query "Q3 Roadmap"
```

## Configuration

Requires standard Feishu environment variables (`FEISHU_APP_ID`, `FEISHU_APP_SECRET`) or a valid `FEISHU_TOKEN`.
The skill uses the shared `skills/common/feishu-client.js` if available, or falls back to local auth.
