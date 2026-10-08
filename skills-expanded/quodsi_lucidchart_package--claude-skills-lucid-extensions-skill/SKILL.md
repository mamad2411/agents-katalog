# Lucid Extension Development Skill

## Overview
This skill provides comprehensive guidance for building Lucid Extension Packages using the Lucid Extension API. It covers editor extensions, data connectors, OAuth providers, link unfurling, and Lucid Cards integrations for Lucidchart and Lucidspark.

**Note:** This skill explicitly excludes Custom Shapes and Formulas functionality.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Extension Package Structure](#extension-package-structure)
3. [Editor Extensions](#editor-extensions)
4. [Data Connectors](#data-connectors)
5. [OAuth Configuration](#oauth-configuration)
6. [Link Unfurling](#link-unfurling)
7. [Lucid Cards](#lucid-cards)
8. [Testing & Debugging](#testing--debugging)
9. [Publishing](#publishing)
10. [Best Practices](#best-practices)

---

## Getting Started

### Prerequisites
1. **Unlock Developer Tools**: Access to the Developer Menu and Developer Portal
   - For Team/Enterprise accounts: Enable through user settings or contact admin
   - Developer tools required to test and distribute extensions
   - Not needed to use published extensions from Lucid Marketplace

2. **Required Tools**:
   - Node.js and npm installed
   - `lucid-package` CLI: `npm install lucid-package`
   - `lucid-extension-sdk`: Automatically installed with package creation

3. **Important Resources**:
   - Developer Portal: https://lucid.app/developer
   - Documentation: https://developer.lucid.co
   - Sample Extensions: https://github.com/lucidsoftware/sample-lucid-extensions
   - Developer Forum: https://community.lucid.co/lucid-for-developers-6

### Creating a New Extension Package

```bash
# Create a new extension package
npx lucid-package@latest create

# Follow the prompts to configure:
# - Package name
# - Extension type (editor extension, data connector, etc.)
# - Target products (Lucidchart, Lucidspark, or both)
```

The CLI will generate a complete package structure with:
- `manifest.json` - Package configuration
- `editorextensions/` - Editor extension code
- `data-connectors/` - Data connector implementations (optional)
- TypeScript configurations
- Webpack configuration

---

## Extension Package Structure

### Manifest File (`manifest.json`)

The manifest is the central configuration file for your extension package:

```json
{
  "id": "your-package-uuid-from-developer-portal",
  "version": "1.0.0",
  "extensions": [
    {
      "name": "my-editor-extension",
      "title": "My Editor Extension",
      "products": ["chart", "spark"],
      "codePath": "editorextensions/my-editor-extension/bin/extension.js",
      "scopes": [
        "READ",
        "WRITE",
        "SHOW_MODAL",
        "CUSTOM_UI",
        "NETWORK"
      ]
    }
  ],
  "oauthProviders": [],
  "dataConnectors": []
}
```

### Key Manifest Fields

**Package Level:**
- `id`: UUID from Developer Portal (get after creating application)
- `version`: Semantic version (must increment for each upload)

**Extension Entry:**
- `name`: Internal identifier (matches folder name)
- `title`: User-facing display name
- `products`: Array of `["chart", "spark", "teamspaces"]`
- `codePath`: Path to compiled JavaScript entry point
- `scopes`: Permission scopes required

### Directory Structure

```
my-extension-package/
├── manifest.json
├── editorextensions/
│   └── my-extension/
│       ├── src/
│       │   ├── extension.ts          # Entry point
│       │   └── importmodal.ts        # Example modal
│       ├── resources/
│       │   ├── import.html           # Modal HTML
│       │   └── resource.d.ts         # Resource types
│       ├── public/                   # Static assets (served via URL)
│       ├── bin/                      # Compiled output
│       ├── package.json
│       ├── tsconfig.json
│       └── webpack.config.js
├── data-connectors/                  # Optional
│   └── my-connector/
│       ├── actions/                  # Action handlers
│       ├── src/
│       │   └── index.ts
│       └── debug-server.ts
└── package.json
```

---

## Editor Extensions

### Core Concepts

Editor extensions run custom code directly inside Lucid editors, enabling:
- Custom menus and actions
- Data import and manipulation
- Custom UI panels
- Document automation
- External API integration

### Entry Point (`extension.ts`)

```typescript
import {
  EditorClient,
  Menu,
  MenuType,
  Viewport,
  Panel,
  PanelLocation
} from 'lucid-extension-sdk';

// Initialize the editor client
const client = new EditorClient();
const menu = new Menu(client);
const viewport = new Viewport(client);

// Register custom actions
client.registerAction('my-action', async () => {
  const selection = viewport.getSelectedItems();
  // Perform operations on selected items
});

// Add menu items
menu.addDropdownMenuItem({
  label: 'My Custom Action',
  action: 'my-action',
  menuType: MenuType.Main
});
```

### Permission Scopes

Scopes control what your extension can access. **Always request minimum scopes needed.**

| Scope | Purpose | Use When |
|-------|---------|----------|
| `READ` | Read document contents | Analyzing shapes, reading data |
| `WRITE` | Modify document contents | Creating/updating shapes |
| `DOWNLOAD` | Download document data | Exporting content |
| `SHOW_MODAL` | Display modal dialogs | User interactions, forms |
| `CUSTOM_UI` | Create custom panels | Building right-dock panels |
| `NETWORK` | Make network requests | API calls, data fetching |

**Example scope configuration:**
```json
{
  "scopes": ["READ", "WRITE", "SHOW_MODAL", "NETWORK"]
}
```

### Custom UI Panels

Create custom panels in the right dock or left toolbox:

```typescript
import { Panel, PanelLocation, EditorClient } from 'lucid-extension-sdk';

class MyPanel extends Panel {
  constructor(client: EditorClient) {
    super(client, {
      title: 'My Panel',
      iconUrl: 'https://example.com/icon.png',
      location: PanelLocation.RightDock, // or PanelLocation.ContentDock
      url: 'public/panel.html' // Serve from public/ directory
    });
  }
}

// Create panel instance
const myPanel = new MyPanel(client);
```

**Requirements:**
- Must add `CUSTOM_UI` scope to manifest
- Can use HTML + JavaScript or React
- Panel HTML can use iframe with relative URLs
- Static assets go in `public/` directory at package root

### Modals

Display modal dialogs for user input:

```typescript
import { Modal } from 'lucid-extension-sdk';

const modal = new Modal(client, {
  title: 'Import Data',
  url: 'public/import-modal.html',
  width: 600,
  height: 400
});

modal.show();
```

### Working with Document Elements

**Get selected items:**
```typescript
const selection = viewport.getSelectedItems();
for (const item of selection) {
  if (item instanceof BlockProxy) {
    // Work with shapes
    console.log(item.boundingBox);
  }
}
```

**Create shapes:**
```typescript
const page = viewport.getCurrentPage();
const block = page?.addBlock({
  boundingBox: { x: 0, y: 0, w: 100, h: 100 },
  style: {
    fill: { color: '#ff0000' }
  }
});
```

**Modify shapes:**
```typescript
block.setStyle({
  fill: { color: '#00ff00' },
  stroke: { color: '#0000ff', width: 2 }
});
```

### Data Management

**Create data collections:**
```typescript
const dataSource = client.getDataSourceProxy();
const collection = dataSource.addCollection('my-collection', {
  primaryKey: 'id',
  fields: [
    { name: 'id', type: 'string' },
    { name: 'title', type: 'string' },
    { name: 'status', type: 'string' }
  ]
});

// Add data items
collection.addItem({
  id: '1',
  title: 'Task 1',
  status: 'In Progress'
});
```

**Link data to shapes:**
```typescript
block.shapeData.set('customField', 'value');
const value = block.shapeData.get('customField');
```

---

## Data Connectors

### When to Use Data Connectors

Use data connectors when you need:
- **Bidirectional sync** between Lucid and external systems
- **Automatic updates** from external data sources
- **Push changes** from Lucid back to external systems
- **Server-side processing** of data actions

**Alternative:** For simple data imports without bidirectional sync, use `EditorClient.oauthXhr()` directly in your editor extension.

### Data Connector Architecture

Data connectors run on a separate server (not in the Lucid editor):
1. Editor extension calls `client.performDataAction()`
2. Lucid servers make POST request to your data connector
3. Data connector processes request, fetches external data
4. Data connector sends formatted data back to Lucid
5. Lucid updates the document

### Creating a Data Connector

```bash
# Create data connector
npm run create-data-connector my-connector
```

### Manifest Configuration

```json
{
  "dataConnectors": [
    {
      "name": "my-connector",
      "oauthProviderName": "my-oauth-provider",
      "callbackBaseUrl": "https://myserver.com/connector/",
      "dataActions": {
        "import": "import",
        "sync": "sync",
        "create": "create"
      }
    }
  ]
}
```

**Fields:**
- `name`: Internal identifier
- `oauthProviderName`: Associated OAuth provider for authentication
- `callbackBaseUrl`: Base URL where your connector is hosted
- `dataActions`: Maps action names to URL suffixes

### Implementing Data Actions

**Editor Extension Trigger:**
```typescript
client.performDataAction({
  dataConnectorName: 'my-connector',
  actionName: 'import',
  actionData: { requestedItems: ['id-1', 'id-2'] },
  asynchronous: true
});
```

**Data Connector Handler (`actions/import.ts`):**
```typescript
import { DataConnectorClient } from 'lucid-extension-sdk';

export async function handleImport(
  request: DataAction,
  client: DataConnectorClient
) {
  const { actionData, oauthToken } = request;
  
  // Fetch data from external API using OAuth token
  const externalData = await fetchFromExternalAPI(
    oauthToken,
    actionData.requestedItems
  );
  
  // Transform to Lucid format
  const lucidData = transformData(externalData);
  
  // Send to Lucid
  await client.sendDataUpdate(request.dataUpdateToken, lucidData);
}
```

### Local Development

For development, use the debug server:

```typescript
// debug-server.ts
import { DataConnectorClient } from 'lucid-extension-sdk';
import { makeDataConnector } from './dataconnector';
import * as express from 'express';
import * as crypto from 'crypto';

const client = new DataConnectorClient({ Buffer, crypto });
const dataConnector = makeDataConnector(client);
dataConnector.runDebugServer({ express });
```

**Development workflow:**
1. Start data connector: `npm start` (in data-connector directory)
2. Start extension: `npx lucid-package test-editor-extension my-extension`
3. Use local callbackBaseUrl: `http://localhost:3001/?kind=action&name=`

### Production Hosting

For production:
1. Host data connector on publicly accessible server
2. Update `callbackBaseUrl` in manifest to production URL
3. Ensure server handles HTTPS requests
4. Validate request signatures for security

---

## OAuth Configuration

### When to Use OAuth

OAuth is required when your extension needs to:
- Access external APIs on behalf of users
- Authenticate with third-party services
- Make authorized API requests to external systems

### OAuth Provider Configuration

Add OAuth provider to manifest:

```json
{
  "oauthProviders": [
    {
      "name": "my-oauth-provider",
      "title": "My Service",
      "authorizationUrl": "https://api.myservice.com/oauth/authorize",
      "tokenUrl": "https://api.myservice.com/oauth/token",
      "scopes": ["read", "write"],
      "domainWhitelist": ["https://api.myservice.com"],
      "clientAuthenticationMethod": "clientParameters",
      "grantType": "authorizationCode"
    }
  ]
}
```

**OAuth Grant Types Supported:**
- `authorizationCode`: Standard OAuth 2.0 authorization code flow
- `clientCredentials`: Client credentials flow (no user authorization)

### Development Credentials

For local development, create `<provider-name>.credentials.local` in package root:

```json
{
  "clientId": "your-dev-client-id",
  "clientSecret": "your-dev-client-secret"
}
```

**Note:** This file should NOT be committed to version control.

### Production Credentials

For production, credentials are configured in the Developer Portal:
1. Go to your application in Developer Portal
2. Navigate to OAuth Providers section
3. Add client ID and secret for your production OAuth application

### Using OAuth in Extensions

**Get OAuth token:**
```typescript
const token = await client.getOAuthToken('my-oauth-provider');
```

**Make authenticated requests:**
```typescript
const response = await client.oauthXhr('my-oauth-provider', {
  url: 'https://api.myservice.com/data',
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  }
});

const data = JSON.parse(response.responseText);
```

**Scope requirements:**
- Must add `NETWORK` scope to extension manifest
- OAuth provider must be declared in package manifest
- Domain must be whitelisted in OAuth provider configuration

---

## Link Unfurling

### What is Link Unfurling?

Link unfurling converts pasted URLs into rich, visual blocks with:
- Thumbnail images
- Titles and descriptions
- Provider branding (logo, name)
- Optional expandable iframes
- Multiple image previews

**Use cases:**
- Visualize content from external platforms
- Embed previews of documents, designs, or dashboards
- Create rich integrations without full data sync

### Implementing Link Unfurling

**Register unfurl handler:**
```typescript
import {
  EditorClient,
  UnfurlDetails,
  LinkUnfurlBlockProxy
} from 'lucid-extension-sdk';

const client = new EditorClient();

// Define unfurl callback
async function performUnfurl(url: string): Promise<UnfurlDetails | undefined> {
  // Match your URL pattern
  const regex = /^https:\/\/myapp\.com\/item\/([a-zA-Z0-9-_]+)/;
  const match = regex.exec(url);
  
  if (!match) return undefined;
  
  const itemId = match[1];
  
  // Fetch metadata from your API
  const metadata = await fetchMetadata(itemId);
  
  return {
    providerName: 'My App',
    providerFaviconUrl: 'https://myapp.com/favicon.ico',
    unfurlTitle: metadata.title,
    previewImageUrl: metadata.thumbnailUrl
  };
}

// Register handler with domain
client.registerUnfurlHandler('myapp.com', {
  unfurlCallback: performUnfurl
});
```

### Domain Matching

The domain parameter supports:
- Exact domains: `'example.com'`
- Subdomains: `'*.example.com'`
- Wildcards in subdomain only: `'app-*.example.com'`

**Not supported:**
- Paths: `'example.com/path'`
- Wildcards in domain: `'exam*.com'`

### Advanced Unfurling Features

**After-unfurl callback** (for additional processing):
```typescript
async function afterUnfurl(
  block: LinkUnfurlBlockProxy,
  url: string
): Promise<void> {
  // Perform additional operations after block creation
  const additionalData = await fetchDetailedData(url);
  block.setTitle(additionalData.detailedTitle);
}

client.registerUnfurlHandler('myapp.com', {
  unfurlCallback: performUnfurl,
  afterUnfurlCallback: afterUnfurl
});
```

**Expandable iframe:**
```typescript
async function performUnfurl(url: string): Promise<UnfurlDetails | undefined> {
  return {
    providerName: 'My App',
    unfurlTitle: 'Document Title',
    previewImageUrl: 'https://myapp.com/preview.png',
    iframeUrl: 'https://myapp.com/embed?url=' + encodeURIComponent(url)
  };
}
```

**Multiple preview images:**
```typescript
return {
  providerName: 'My App',
  unfurlTitle: 'Gallery',
  previewImageUrls: [
    'https://myapp.com/image1.png',
    'https://myapp.com/image2.png',
    'https://myapp.com/image3.png'
  ]
};
```

**Expand callback** (custom expand button behavior):
```typescript
async function handleExpand(
  block: LinkUnfurlBlockProxy,
  url: string
): Promise<void> {
  // Custom logic when user clicks expand
  const embedUrl = await generateEmbedUrl(url);
  block.setIframe({
    iframeUrl: embedUrl,
    aspectRatio: UnfurlIframeAspectRatio.Widescreen
  });
}

client.registerUnfurlHandler('myapp.com', {
  unfurlCallback: performUnfurl,
  expandCallback: handleExpand
});
```

### Link Unfurling Limitations

- Thumbnail images cannot be resynced after initial extraction
- Bidirectional data sync not supported
- Video players not supported in-editor (must open in new tab)
- Updates to titles/images cannot be pushed back to source

### Programmatic Link Import

Import links programmatically (they'll be unfurled by registered handlers):

```typescript
const linksToImport = [
  'https://myapp.com/item/123',
  'https://myapp.com/item/456'
];

viewport.getCurrentPage()?.importLinks(linksToImport);
```

---

## Lucid Cards

### What are Lucid Cards?

Lucid Cards enable rich, bidirectional integrations with task management systems:
- Import tasks/items from external systems
- Create new tasks directly in Lucid
- Convert Lucid shapes to external tasks
- Two-way sync keeps both systems updated
- Customizable card layouts and fields

**Typical use cases:**
- Project management (Jira, Asana, Monday.com)
- Spreadsheet integration (Google Sheets, Airtable)
- Custom task tracking systems

### Lucid Cards Architecture

1. **Editor Extension**: Implements `LucidCardIntegration` class
2. **OAuth Provider**: Handles authentication
3. **Data Connector**: Manages data synchronization (import/sync/create actions)

### Creating a Lucid Cards Integration

**Step 1: Extend LucidCardIntegration**

```typescript
import {
  EditorClient,
  LucidCardIntegration,
  LucidCardIntegrationImportModal
} from 'lucid-extension-sdk';

class MyCardIntegration extends LucidCardIntegration {
  constructor(client: EditorClient) {
    super(client, {
      dataConnectorName: 'my-connector',
      oauthProviderName: 'my-oauth',
      
      cardImportSettings: {
        cardStructure: {
          title: 'title',
          fields: [
            { name: 'status', type: 'badge' },
            { name: 'assignee', type: 'text' },
            { name: 'dueDate', type: 'date' }
          ]
        }
      },
      
      cardSyncSettings: {
        syncChanges: true,
        syncInterval: 300000 // 5 minutes
      }
    });
  }
}

// Initialize
const cardIntegration = new MyCardIntegration(client);
```

**Step 2: Implement Import Modal**

```typescript
const importModal = new LucidCardIntegrationImportModal(client, {
  oauthProviderName: 'my-oauth',
  dataConnectorName: 'my-connector',
  
  // Define search functionality
  getSearchFields: async () => {
    return [
      {
        name: 'project',
        label: 'Project',
        type: 'dropdown',
        options: await fetchProjects()
      },
      {
        name: 'query',
        label: 'Search',
        type: 'text'
      }
    ];
  },
  
  // Handle search
  search: async (searchParams) => {
    const results = await searchTasks(searchParams);
    
    return results.map(task => ({
      itemId: task.id,
      displayText: task.title,
      previewData: {
        title: task.title,
        status: task.status,
        assignee: task.assignee
      }
    }));
  }
});
```

**Step 3: Implement Data Connector Actions**

Your data connector needs to handle these actions:

**Import Action:**
```typescript
async function handleImport(request: DataAction, client: DataConnectorClient) {
  const { itemIds } = request.actionData;
  const tasks = await fetchTasksFromAPI(itemIds, request.oauthToken);
  
  const lucidData = {
    collections: [
      {
        collectionId: 'tasks',
        primaryKey: 'id',
        items: tasks.map(task => ({
          id: task.id,
          title: task.title,
          status: task.status,
          assignee: task.assignee,
          dueDate: task.dueDate
        }))
      }
    ]
  };
  
  await client.sendDataUpdate(request.dataUpdateToken, lucidData);
}
```

**Create Action** (for two-way sync):
```typescript
async function handleCreate(request: DataAction, client: DataConnectorClient) {
  const { taskData } = request.actionData;
  
  // Create task in external system
  const newTask = await createTaskInAPI(taskData, request.oauthToken);
  
  // Return created task data
  await client.sendDataUpdate(request.dataUpdateToken, {
    collections: [{
      collectionId: 'tasks',
      items: [{
        id: newTask.id,
        title: newTask.title,
        status: newTask.status
      }]
    }]
  });
}
```

**Sync Action** (periodic updates):
```typescript
async function handleSync(request: DataAction, client: DataConnectorClient) {
  // Get modified tasks from Lucid
  const localChanges = request.actionData.localChanges;
  
  // Push changes to external system
  for (const change of localChanges.modified) {
    await updateTaskInAPI(change, request.oauthToken);
  }
  
  // Fetch latest data from external system
  const latestTasks = await fetchAllTasks(request.oauthToken);
  
  await client.sendDataUpdate(request.dataUpdateToken, {
    collections: [{
      collectionId: 'tasks',
      items: latestTasks
    }]
  });
}
```

### Card Field Configuration

Lucid Cards support various field types for display:

```typescript
cardStructure: {
  title: 'title', // Main title field
  fields: [
    { name: 'status', type: 'badge', color: 'statusColor' },
    { name: 'assignee', type: 'text' },
    { name: 'priority', type: 'number' },
    { name: 'dueDate', type: 'date' },
    { name: 'description', type: 'longText' },
    { name: 'tags', type: 'multiSelect' }
  ]
}
```

### Card Creation Methods

Users can create Lucid Cards four ways:

1. **Import Modal**: Select items from external system
2. **New Task**: Create new task directly (requires two-way sync)
3. **Drag from Toolbar**: Place blank card and edit
4. **Convert Shape**: Right-click shape → Convert to Card

---

## Testing & Debugging

### Local Development Setup

**1. Start Debug Server:**
```bash
# Test single extension
npx lucid-package@latest test-editor-extension my-extension

# Test multiple extensions
npx lucid-package@latest test-editor-extension ext1 ext2 ext3

# Test all extensions
npx lucid-package@latest test-editor-extension
```

**2. Enable Developer Mode in Lucid:**
- Open Lucidchart or Lucidspark
- Click "Developer" in top menu
- Click "Enter developer mode"
- Developer status panel appears at top

**3. Load Your Extension:**
- Extension auto-loads when Developer Mode enabled
- Use "Refresh" button to reload after code changes
- Enable "Auto-refresh" for automatic reloading

### Development Environment

**Local vs. Published Behavior:**
- Local: Code runs via scoped eval (allows debugging)
- Published: Code runs in sandboxed JavaScript VM (more restrictive)

**⚠️ Important Limitations in Published Extensions:**
- Cannot access browser DOM APIs directly
- Cannot use certain JavaScript features blocked by sandbox
- Test published versions to catch sandbox restrictions

### Debugging Tools

**Browser DevTools:**
- Full access when running locally
- Set breakpoints in source code
- Inspect variables and network requests
- View console logs

**Debug Logging:**
```typescript
console.log('Debug info:', data);
console.error('Error occurred:', error);
```

### manifest.local.json

Override manifest settings for local development:

```json
{
  "dataConnectors": [
    {
      "callbackBaseUrl": "http://localhost:3001/"
    }
  ]
}
```

Keeps production config in `manifest.json` while allowing local overrides.

### Common Development Issues

**Extension not loading:**
- Verify webpack compilation succeeded
- Check browser console for errors
- Ensure Developer Mode is enabled
- Try manual refresh

**OAuth not working locally:**
- Create `.credentials.local` file with dev credentials
- Verify domain whitelist includes your API
- Check OAuth provider configuration

**Data connector not responding:**
- Ensure connector server is running (`npm start`)
- Verify callbackBaseUrl points to localhost
- Check connector logs for errors
- Validate request/response format

**Safari Limitations:**
- Local extension loading NOT supported in Safari
- Use Chrome, Firefox, or Edge for development

---

## Publishing

### Publishing Overview

Extensions can be:
- **Privately published**: Available only to your Lucid account
- **Publicly published**: Available on Lucid Marketplace (requires approval)

### Prerequisites

1. **Create Application in Developer Portal:**
   - Go to https://lucid.app/developer
   - Click "New Application"
   - Copy package UUID from URL
   - Add UUID to `manifest.json` `id` field

2. **Bundle Extension:**
```bash
npx lucid-package@latest bundle
```
   This creates `package.zip` ready for upload.

3. **Upload to Developer Portal:**
   - Go to your application
   - Click "Packages" tab
   - Click "+ New Version"
   - Upload `package.zip`

### Version Management

- Version in manifest must increment for each upload
- Cannot reuse version numbers
- Semantic versioning recommended (1.0.0, 1.0.1, 1.1.0, etc.)
- `bundle` command auto-increments version

### Private Publishing

**Who can use private publishing:**
- Team Admins on Team/Enterprise accounts
- App must have uploaded package version

**How to publish privately:**
1. Go to application in Developer Portal
2. Navigate to Publishing section
3. Select package version
4. Click "Publish Privately"
5. Extension available to all users on your account

**No marketplace listing required** for private publishing.

### Public Publishing (Lucid Marketplace)

**Requirements:**
1. **Create Zendesk ticket** using [this form](https://lucidchart.zendesk.com/hc/en-us/requests/new?ticket_form_id=13656325495060)
   - Record ticket ID for submission
   - Used for Lucid review communications

2. **Create Marketplace Listing:**
   - Application name and description
   - Logo/icon images
   - Privacy policy URL
   - Terms of service URL
   - Support contact information
   - Screenshots/demo videos

3. **Submit for Review:**
   - Go to Publishing section in Developer Portal
   - Select package version to publish
   - Click "Submit for Approval on Lucid Marketplace"
   - Provide Zendesk ticket ID

**Review Process:**
- Lucid team reviews functionality, security, UX
- May request changes or clarifications via Zendesk
- Approval typically takes 1-2 weeks
- You'll be notified when published

**Publishing Roles:**
- **App Owner**: Can request first-time publication
- **Code Editor**: Can request updates to already-published apps
- Other collaborators cannot publish

### Installation Options

**For unpublished extensions:**
1. "Install for me" - Install on your account only
2. "Install for my whole account" - Team Admins can install for entire account

**For published extensions:**
- Available in Lucid Marketplace
- Users can install directly from marketplace
- May appear in integration recommendations

### Revoking Packages

- Can revoke unpublished package versions
- Cannot revoke published versions
- Revoked versions cannot be re-published
- Users already using revoked version keep access

---

## Best Practices

### Code Organization

**Modular Structure:**
```typescript
// services/api.ts
export class APIService {
  async fetchData() { /* ... */ }
}

// handlers/import.ts
export async function handleImport() { /* ... */ }

// extension.ts
import { APIService } from './services/api';
import { handleImport } from './handlers/import';

const apiService = new APIService();
client.registerAction('import', () => handleImport(apiService));
```

### Error Handling

**Always handle errors gracefully:**
```typescript
client.registerAction('fetch-data', async () => {
  try {
    const data = await fetchFromAPI();
    await processData(data);
  } catch (error) {
    console.error('Failed to fetch data:', error);
    client.alert('An error occurred. Please try again.');
  }
});
```

### Performance Optimization

**Minimize document operations:**
```typescript
// ❌ Bad: Multiple operations
for (const item of items) {
  const block = page.addBlock({/* ... */});
  block.setStyle({/* ... */});
}

// ✅ Good: Batch operations
const blocks = items.map(item => ({
  boundingBox: calculateBox(item),
  style: calculateStyle(item)
}));
page.addBlocks(blocks);
```

**Async operations:**
```typescript
// Use async/await for better readability
async function importData() {
  const token = await client.getOAuthToken('provider');
  const data = await fetchData(token);
  await processData(data);
}
```

### Security Best Practices

**1. OAuth Security:**
- Never commit credentials to source control
- Use environment variables or `.credentials.local`
- Validate OAuth tokens before use
- Handle token expiration gracefully

**2. Data Connector Security:**
- Always validate request signatures
- Use HTTPS for all connections
- Sanitize user input
- Don't log sensitive data

**3. Input Validation:**
```typescript
function validateInput(data: unknown): data is ValidType {
  if (!data || typeof data !== 'object') return false;
  // Validate structure
  return true;
}

if (!validateInput(userInput)) {
  throw new Error('Invalid input');
}
```

### User Experience

**Loading States:**
```typescript
client.registerAction('import', async () => {
  client.alert('Importing data...');
  
  try {
    await performImport();
    client.alert('Import complete!');
  } catch (error) {
    client.alert('Import failed. Please try again.');
  }
});
```

**Progress Feedback:**
- Use modals for long operations
- Show clear error messages
- Provide undo capabilities where possible
- Use intuitive menu labels

### Testing Strategy

**1. Local Testing:**
- Test with Developer Mode extensively
- Try edge cases and error scenarios
- Test with different document states
- Verify OAuth flows

**2. Published Testing:**
- Install published version on test account
- Verify sandbox restrictions don't break functionality
- Test with actual users for feedback
- Monitor for errors in production

**3. Cross-Product Testing:**
- If targeting both Chart and Spark, test in both
- Verify behavior differences between products
- Test common workflows in each product

### Documentation

**Inline Comments:**
```typescript
/**
 * Imports tasks from external system
 * @param taskIds Array of task IDs to import
 * @returns Promise resolving when import completes
 */
async function importTasks(taskIds: string[]): Promise<void> {
  // Implementation
}
```

**README for Users:**
- Include setup instructions
- Document OAuth requirements
- Provide usage examples
- List known limitations

### Version Control

**Git Best Practices:**
```gitignore
# .gitignore
node_modules/
*.credentials.local
manifest.local.json
bin/
*.zip
.DS_Store
```

**Commit Messages:**
- Use clear, descriptive messages
- Reference issue numbers when applicable
- Keep commits focused and atomic

### Maintenance

**Monitor Extension Health:**
- Check Developer Forum for user issues
- Review error logs if available
- Test against Lucid product updates
- Keep dependencies updated

**Deprecation Strategy:**
- Announce breaking changes early
- Maintain backward compatibility when possible
- Provide migration guides
- Support old versions during transition

---

## Common Patterns

### Pattern: Import Modal Workflow

```typescript
// 1. Show modal
const modal = new Modal(client, {
  title: 'Import Data',
  url: 'public/import.html'
});

// 2. Handle modal communication
client.registerModalCallback((message) => {
  if (message.action === 'import') {
    performImport(message.data);
  }
});

modal.show();

// 3. In import.html
function submitImport() {
  window.parent.postMessage({
    messageName: 'modalCallback',
    data: {
      action: 'import',
      data: selectedItems
    }
  }, '*');
}
```

### Pattern: Menu with Submenus

```typescript
const menu = new Menu(client);

// Add parent menu
menu.addDropdownMenu({
  label: 'My Extension',
  menuType: MenuType.Main
});

// Add submenu items
menu.addDropdownMenuItem({
  label: 'Import Data',
  action: 'import-data',
  menuType: MenuType.Main,
  parent: 'My Extension'
});

menu.addDropdownMenuItem({
  label: 'Export Data',
  action: 'export-data',
  menuType: MenuType.Main,
  parent: 'My Extension'
});
```

### Pattern: Context Menu Actions

```typescript
// Add item to right-click context menu
menu.addContextMenuItem({
  label: 'Process Selected Items',
  action: 'process-items'
});

// Handler checks selection
client.registerAction('process-items', () => {
  const selection = viewport.getSelectedItems();
  if (selection.length === 0) {
    client.alert('Please select items first');
    return;
  }
  processItems(selection);
});
```

### Pattern: Data Collection with Relationships

```typescript
// Create related collections
const dataSource = client.getDataSourceProxy();

// Projects collection
const projects = dataSource.addCollection('projects', {
  primaryKey: 'id',
  fields: [
    { name: 'id', type: 'string' },
    { name: 'name', type: 'string' }
  ]
});

// Tasks collection with project reference
const tasks = dataSource.addCollection('tasks', {
  primaryKey: 'id',
  fields: [
    { name: 'id', type: 'string' },
    { name: 'title', type: 'string' },
    { name: 'projectId', type: 'string' } // Foreign key
  ]
});

// Link block to task with project relationship
block.linkToData(tasks, 'task-123');
const projectId = block.getLinkedData()?.get('projectId');
const project = projects.getItem(projectId);
```

### Pattern: Retry Logic

```typescript
async function fetchWithRetry(
  url: string,
  maxRetries: number = 3
): Promise<any> {
  let lastError;
  
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await client.oauthXhr('provider', {
        url,
        method: 'GET'
      });
      return JSON.parse(response.responseText);
    } catch (error) {
      lastError = error;
      console.warn(`Attempt ${i + 1} failed:`, error);
      
      if (i < maxRetries - 1) {
        await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
      }
    }
  }
  
  throw lastError;
}
```

### Pattern: Keyboard Shortcuts

```typescript
// Register keyboard shortcut (Ctrl/Cmd + K)
client.registerKeyboardShortcut({
  key: 'k',
  modifiers: ['ctrl', 'cmd'],
  action: 'quick-action'
});

client.registerAction('quick-action', () => {
  // Handle shortcut
});
```

---

## Additional Resources

### Official Documentation
- Extension API Docs: https://developer.lucid.co/docs/lucid-extension-api
- Developer Portal: https://lucid.app/developer
- REST API Reference: https://developer.lucid.co/reference/overview

### Sample Code
- GitHub Repository: https://github.com/lucidsoftware/sample-lucid-extensions
- Example integrations:
  - Asana Cards: https://github.com/lucidsoftware/sample-lucid-extensions/tree/main/asana-cards
  - Data Connector Example: https://github.com/lucidsoftware/sample-lucid-extensions/tree/main/data-connector-example

### Community & Support
- Developer Forum: https://community.lucid.co/lucid-for-developers-6
- Help Center: https://help.lucid.co
- Partnership Program: https://lucid.co/partners

### TypeScript & Development
- lucid-package NPM: https://www.npmjs.com/package/lucid-package
- lucid-extension-sdk NPM: https://www.npmjs.com/package/lucid-extension-sdk
- Release Notes: https://developer.lucid.co/docs/release-notes

---

## Skill Maintenance

**Version:** 1.0.0  
**Last Updated:** November 2025  
**Excluded Topics:** Custom Shapes, Formulas  
**Coverage:** Editor Extensions, Data Connectors, OAuth, Link Unfurling, Lucid Cards

This skill should be updated when:
- Major API changes occur
- New extension capabilities are added
- Best practices evolve
- Common patterns emerge from community usage
