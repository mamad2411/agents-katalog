# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

scaffold-connector is a TypeScript template for building API connector CLIs. It provides multi-profile configuration, Bearer token authentication (customizable), OAuth2 support, and a clean CLI structure using Commander.js.

**This is a SCAFFOLD** - meant to be cloned and customized for specific APIs.

## Build & Run Commands

```bash
# Install dependencies
bun install

# Run CLI in development
bun run dev

# Build for distribution
bun run build

# Type check
bun run typecheck

# Run specific commands
bun run dev profile list
bun run dev config show
bun run dev example list

# Release (auto-bump patch version and publish)
bun run release
bun run release:dry  # Preview only
```

## Code Style

- TypeScript with strict mode
- ESM modules (type: module)
- Use async/await for all async operations
- Minimal dependencies: commander, chalk only
- Type annotations required everywhere
- Use interfaces for all API types

## Project Structure

```
src/
├── api/
│   ├── client.ts     # HTTP client with auth, retry, timeout
│   ├── example.ts    # Example API module (template)
│   └── index.ts      # Main connector class
├── cli/
│   └── index.ts      # CLI commands
├── types/
│   └── index.ts      # Type definitions
├── utils/
│   ├── auth.ts       # OAuth2 authentication
│   ├── bulk.ts       # Bulk operation utilities
│   ├── config.ts     # Multi-profile configuration
│   ├── output.ts     # CLI output formatting
│   ├── settings.ts   # User preferences storage
│   └── storage.ts    # Local data storage
├── index.ts          # Library exports
scripts/
└── release.ts        # Release automation
```

## Key Patterns

### Multi-Profile Configuration

Profiles stored in `~/.hasna/connectors/{connector-name}/profiles/`:
- Each profile is a separate JSON file
- `current_profile` file tracks active profile
- `--profile` flag overrides for single command
- Environment variables override profile config

### Authentication

**Bearer Token (Default)** in `src/api/client.ts`:
```typescript
'Authorization': `Bearer ${this.apiKey}`,
```

**Supported Auth Methods:**
- Bearer token: `'Authorization': 'Bearer ${token}'`
- API Key header: `'X-API-Key': ${apiKey}`
- Basic auth: `'Authorization': 'Basic ' + base64(key:secret)`
- OAuth2: Use the auth utilities (see below)

### OAuth2 Authentication

For APIs that require OAuth2, use the auth utilities:

```typescript
import { getAuthUrl, startCallbackServer, getValidAccessToken } from './utils/auth';

// Start OAuth flow
const authUrl = getAuthUrl({ scopes: 'read write' });
// Open authUrl in browser
const result = await startCallbackServer();
if (result.success) {
  saveOAuthTokens(result.tokens);
}

// Get valid access token (auto-refreshes if needed)
const token = await getValidAccessToken();
```

### Settings Storage

Store user preferences with the settings utility:

```typescript
import { getSetting, setSetting, loadSettings } from './utils/settings';

// Get a setting
const format = getSetting('defaultFormat');

// Set a setting
setSetting('verboseOutput', true);
```

### Local Data Storage

Store local data (like contacts, cache) with the storage utility:

```typescript
import { createStorage, type Storable } from './utils/storage';

interface Contact extends Storable {
  id: string;
  email: string;
  name?: string;
}

const contacts = createStorage<Contact>('contacts');

// Save
contacts.save({ id: 'user@example.com', email: 'user@example.com', name: 'User' });

// Get
const contact = contacts.get('user@example.com');

// Search
const results = contacts.searchByText('example');
```

### Bulk Operations

Process multiple items with concurrency control:

```typescript
import { executeBulk, createProgressReporter } from './utils/bulk';

const result = await executeBulk(
  {
    items: users,
    concurrency: 5,
    dryRun: false,
    onProgress: createProgressReporter('Updating users'),
  },
  async (user) => {
    await api.updateUser(user.id, { status: 'active' });
  }
);

console.log(`Success: ${result.success}, Failed: ${result.failed}`);
```

### Retry and Rate Limiting

The HTTP client includes built-in retry logic:

```typescript
// Retries are automatic for 429 (rate limit) and 5xx errors
const data = await client.get('/endpoint', { retries: 3, timeout: 30000 });
```

### Adding New API Modules

1. Create file in `src/api/` following `example.ts` pattern
2. Add to exports in `src/api/index.ts`
3. Add types in `src/types/index.ts`
4. Add CLI commands in `src/cli/index.ts`

## TODO Markers

When customizing this scaffold, search for `TODO` comments:

- `src/cli/index.ts:22-24` - CONNECTOR_NAME, VERSION, description
- `src/utils/config.ts:5-6` - CONNECTOR_NAME, env var prefix
- `src/utils/auth.ts:10-15` - OAuth URLs and scopes
- `src/api/client.ts:5` - DEFAULT_BASE_URL
- `src/api/client.ts:55-60` - Authentication method
- `src/api/index.ts:7` - Rename Connector class
- `src/types/index.ts` - Replace example types

## Environment Variables

| Variable | Description |
|----------|-------------|
| `CONNECTOR_API_KEY` | API key (overrides profile) |
| `CONNECTOR_TOKEN` | Token (alias for API key) |
| `CONNECTOR_API_SECRET` | API secret (optional) |
| `CONNECTOR_BASE_URL` | Override base URL |

## CLI Global Flags

| Flag | Description |
|------|-------------|
| `-k, --api-key <key>` | Override API key for this command |
| `-p, --profile <name>` | Use specific profile |
| `-f, --format <format>` | Output format (json, pretty, table) |
| `-v, --verbose` | Enable debug output |

## Data Storage

```
~/.hasna/connectors/{connector-name}/
├── current_profile     # Active profile name
├── settings.json       # User preferences
├── data/               # Local data storage
│   └── {entity}/       # Entity-specific storage
│       └── *.json
└── profiles/
    ├── default.json    # Default profile
    └── {name}.json     # Named profiles
```

Profile JSON structure:
```json
{
  "apiKey": "sk-xxx",
  "token": "sk-xxx",
  "apiSecret": "optional",
  "accessToken": "oauth-access-token",
  "refreshToken": "oauth-refresh-token",
  "expiresAt": 1234567890,
  "clientId": "oauth-client-id",
  "clientSecret": "oauth-client-secret"
}
```

## Dependencies

- commander: CLI framework
- chalk: Terminal styling

## Error Handling

The scaffold includes enhanced error types:

```typescript
import { ConnectorApiError, parseApiError } from './types';

try {
  await api.get('/endpoint');
} catch (err) {
  if (err instanceof ConnectorApiError) {
    if (err.isRateLimited()) {
      // Handle rate limiting
    }
    if (err.isAuthError()) {
      // Handle auth errors
    }
    console.log(err.getUserMessage());
    console.log(err.documentationUrl);
  }
}
```
