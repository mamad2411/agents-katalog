---
name: google-toolkit
description: Consolidated toolkit for google. Covers google-analytics-automation, google-drive-automation
---
# Google Toolkit

## Core Capabilities
# Google Toolkit

# Google Analytics Automation via Rube MCP

Automate Google Analytics 4 (GA4) reporting and property management through Composio's Google Analytics toolkit via Rube MCP.

## Prerequisites

- Rube MCP must be connected (RUBE_SEARCH_TOOLS available)
- Active Google Analytics connection via `RUBE_MANAGE_CONNECTIONS` with toolkit `google_analytics`
- Always call `RUBE_SEARCH_TOOLS` first to get current tool schemas

## Setup

**Get Rube MCP**: Add `https://rube.app/mcp` as an MCP server in your client configuration. No API keys needed — just add the endpoint and it works.

1. Verify Rube MCP is available by confirming `RUBE_SEARCH_TOOLS` responds
2. Call `RUBE_MANAGE_CONNECTIONS` with toolkit `google_analytics`
3. If connection is not ACTIVE, follow the returned auth link to complete Google OAuth
4. Confirm connection status shows ACTIVE before running any workflows

## Core Workflows

### 1. List Accounts and Properties

**When to use**: User wants to discover available GA4 accounts and properties

**Tool sequence**:
1. `GOOGLE_ANALYTICS_LIST_ACCOUNTS` - List all accessible GA4 accounts [Required]
2. `GOOGLE_ANALYTICS_LIST_PROPERTIES` - List properties under an account [Required]

**Key parameters**:
- `pageSize`: Number of results per page
- `pageToken`: Pagination token from previous response
- `filter`: Filter expression for properties (e.g., `parent:accounts/12345`)

**Pitfalls**:
- Property IDs are numeric strings prefixed with 'properties/' (e.g., 'properties/123456')
- Account IDs are prefixed with 'accounts/' (e.g., 'accounts/12345')
- Always list accounts first, then properties under each account
- Pagination required for organizations with many properties

### 2. Run Standard Reports

**When to use**: User wants to query metrics and dimensions from GA4 data

**Tool sequence**:
1. `GOOGLE_ANALYTICS_LIST_PROPERTIES` - Get property ID [Prerequisite]
2. `GOOGLE_ANALYTICS_GET_METADATA` - Discover available dimensions and metrics [Optional]
3. `GOOGLE_ANALYTICS_CHECK_COMPATIBILITY` - Verify dimension/metric compatibility [Optional]
4. `GOOGLE_ANALYTICS_RUN_REPORT` - Execute the report query [Required]

**Key parameters**:
- `property`: Property ID (e.g., 'properties/123456')
- `dateRanges`: Array of date range objects with `startDate` and `endDate`
- `dimensions`: Array of dimension objects with `name` field
- `metrics`: Array of metric objects with `name` field
- `dimensionFilter` / `metricFilter`: Filter expressions
- `orderBys`: Sort order configuration
- `limit`: Maximum rows to return
- `offset`: Row offset for pagination

**Pitfalls**:
- Date format is 'YYYY-MM-DD' or relative values like 'today', 'yesterday', '7daysAgo', '30daysAgo'
- Not all dimensions and metrics are compatible; use CHECK_COMPATIBILITY first
- Use GET_METADATA to discover valid dimension and metric names
- Maximum 9 dimensions per report request
- Row limit defaults vary; set explicitly for large datasets
- `offset` is for result pagination, not date pagination

### 3. Run Batch Reports

**When to use**: User needs multiple different reports from the same property in one call

**Tool sequence**:
1. `GOOGLE_ANALYTICS_LIST_PROPERTIES` - Get property ID [Prerequisite]
2. `GOOGLE_ANALYTICS_BATCH_RUN_REPORTS` - Execute multiple reports at once [Required]

**Key parameters**:
- `property`: Property ID (required)
- `requests`: Array of individual report request objects (same structure as RUN_REPORT)

**Pitfalls**:
- Maximum 5 report requests per batch call
- All reports in a batch must target the same property
- Each individual report has the same dimension/metric limits as RUN_REPORT
- Batch errors may affect all reports; check individual report responses

### 4. Run Pivot Reports

**When to use**: User wants cross-tabulated data (rows vs columns) like pivot tables

**Tool sequence**:
1. `GOOGLE_ANALYTICS_LIST_PROPERTIES` - Get property ID [Prerequisite]
2. `GOOGLE_ANALYTICS_RUN_PIVOT_REPORT` - Execute pivot report [Required]

**Key parameters**:
- `property`: Property ID (required)
- `dateRanges`: Date range objects
- `dimensions`: All dimensions used in any pivot
- `metrics`: Metrics to aggregate
- `pivots`: Array of pivot definitions with `fieldNames`, `limit`, and `orderBys`

**Pitfalls**:
- Dimensions used in pivots must also be listed in top-level `dimensions`
- Pivot `fieldNames` reference dimension names from the top-level list
- Complex pivots with many dimensions can produce very large result sets
- Each pivot has its own independent `limit` and `orderBys`

### 5. Run Funnel Reports

**When to use**: User wants to analyze conversion funnels and drop-off rates

**Tool sequence**:
1. `GOOGLE_ANALYTICS_LIST_PROPERTIES` - Get property ID [Prerequisite]
2. `GOOGLE_ANALYTICS_RUN_FUNNEL_REPORT` - Execute funnel analysis [Required]

**Key parameters**:
- `property`: Property ID (required)
- `dateRanges`: Date range objects
- `funnel`: Funnel definition with `steps` array
- `funnelBreakdown`: Optional dimension to break down funnel by

**Pitfalls**:
- Funnel steps are ordered; each step defines a condition users must meet
- Steps use filter expressions similar to dimension/metric filters
- Open funnels allow entry at any step; closed funnels require sequential progression
- Funnel reports may take longer to process than standard reports

### 6. Manage Key Events

**When to use**: User wants to view or manage conversion events (key events) in GA4

**Tool sequence**:
1. `GOOGLE_ANALYTICS_LIST_PROPERTIES` - Get property ID [Prerequisite]
2. `GOOGLE_ANALYTICS_LIST_KEY_EVENTS` - List all key events for the property [Required]

**Key parameters**:
- `parent`: Property resource name (e.g., 'properties/123456')
- `pageSize`: Number of results per page
- `pageToken`: Pagination token

**Pitfalls**:
- Key events were previously called "conversions" in GA4
- Property must have key events configured to return results
- Key event names correspond to GA4 event names

## Common Patterns

### ID Resolution

**Account name -> Account ID**:
```
1. Call GOOGLE_ANALYTICS_LIST_ACCOUNTS
2. Find account by displayName
3. Extract name field (e.g., 'accounts/12345')
```

**Property name -> Property ID**:
```
1. Call GOOGLE_ANALYTICS_LIST_PROPERTIES with filter
2. Find property by displayName
3. Extract name field (e.g., 'properties/123456')
```

### Dimension/Metric Discovery

```
1. Call GOOGLE_ANALYTICS_GET_METADATA with property ID
2. Browse available dimensions and metrics
3. Call GOOGLE_ANALYTICS_CHECK_COMPATIBILITY to verify combinations
4. Use verified dimensions/metrics in RUN_REPORT
```

### Pagination

- Reports: Use `offset` and `limit` for row pagination
- Accounts/Properties: Use `pageToken` from response
- Continue until `pageToken` is absent or `rowCount` reached

### Common Dimensions and Metrics

**Dimensions**: `date`, `city`, `country`, `deviceCategory`, `sessionSource`, `sessionMedium`, `pagePath`, `pageTitle`, `eventName`

**Metrics**: `activeUsers`, `sessions`, `screenPageViews`, `eventCount`, `conversions`, `totalRevenue`, `bounceRate`, `averageSessionDuration`

## Known Pitfalls

**Property IDs**:
- Always use full resource name format: 'properties/123456'
- Numeric ID alone will cause errors
- Resolve property names to IDs via LIST_PROPERTIES

**Date Ranges**:
- Format: 'YYYY-MM-DD' or relative ('today', 'yesterday', '7daysAgo', '30daysAgo')
- Data processing delay means today's data may be incomplete
- Maximum date range varies by property configuration

**Compatibility**:
- Not all dimensions work with all metrics
- Always verify with CHECK_COMPATIBILITY before complex reports
- Custom dimensions/metrics have specific naming patterns

**Response Parsing**:
- Report data is nested in `rows` array with `dimensionValues` and `metricValues`
- Values are returned as strings; parse numbers explicitly
- Empty reports return no `rows` key (not an empty array)

## Quick Reference

| Task | Tool Slug | Key Params |
|------|-----------|------------|
| List accounts | GOOGLE_ANALYTICS_LIST_ACCOUNTS | pageSize, pageToken |
| List properties | GOOGLE_ANALYTICS_LIST_PROPERTIES | filter, pageSize |
| Get metadata | GOOGLE_ANALYTICS_GET_METADATA | property |
| Check compatibility | GOOGLE_ANALYTICS_CHECK_COMPATIBILITY | property, dimensions, metrics |
| Run report | GOOGLE_ANALYTICS_RUN_REPORT | property, dateRanges, dimensions, metrics |
| Batch reports | GOOGLE_ANALYTICS_BATCH_RUN_REPORTS | property, requests |
| Pivot report | GOOGLE_ANALYTICS_RUN_PIVOT_REPORT | property, dateRanges, pivots |
| Funnel report | GOOGLE_ANALYTICS_RUN_FUNNEL_REPORT | property, dateRanges, funnel |
| List key events | GOOGLE_ANALYTICS_LIST_KEY_EVENTS | parent, pageSize |

---

# Google Drive Automation via Rube MCP

Automate Google Drive workflows including file upload/download, search, folder management, sharing/permissions, and organization through Composio's Google Drive toolkit.

## Prerequisites

- Rube MCP must be connected (RUBE_SEARCH_TOOLS available)
- Active Google Drive connection via `RUBE_MANAGE_CONNECTIONS` with toolkit `googledrive`
- Always call `RUBE_SEARCH_TOOLS` first to get current tool schemas

## Setup

**Get Rube MCP**: Add `https://rube.app/mcp` as an MCP server in your client configuration. No API keys needed — just add the endpoint and it works.

1. Verify Rube MCP is available by confirming `RUBE_SEARCH_TOOLS` responds
2. Call `RUBE_MANAGE_CONNECTIONS` with toolkit `googledrive`
3. If connection is not ACTIVE, follow the returned auth link to complete Google OAuth
4. Confirm connection status shows ACTIVE before running any workflows

## Core Workflows

### 1. Upload and Download Files

**When to use**: User wants to upload files to or download files from Google Drive

**Tool sequence**:
1. `GOOGLEDRIVE_FIND_FILE` - Locate target folder for upload [Prerequisite]
2. `GOOGLEDRIVE_UPLOAD_FILE` - Upload a file (max 5MB) [Required]
3. `GOOGLEDRIVE_RESUMABLE_UPLOAD` - Upload large files [Fallback]
4. `GOOGLEDRIVE_DOWNLOAD_FILE` - Download a file by ID [Required]
5. `GOOGLEDRIVE_DOWNLOAD_FILE_OPERATION` - Track long-running downloads [Fallback]
6. `GOOGLEDRIVE_GET_FILE_METADATA` - Verify file after upload/download [Optional]

**Key parameters**:
- `file_to_upload`: Object with `name`, `mimetype`, and `s3key` (file must be in internal storage)
- `folder_to_upload_to`: Target folder ID (optional; uploads to root if omitted)
- `file_id`: ID of file to download
- `mime_type`: Export format for Google Workspace files only (omit for native files)

**Pitfalls**:
- `GOOGLEDRIVE_UPLOAD_FILE` requires `file_to_upload.s3key`; files must already be in internal storage
- For non-Google formats (Excel, PDF), do NOT set `mime_type`; it causes errors for native files
- Download responses provide a temporary URL at `data.downloaded_file_content.s3url`, not inline bytes
- Use `GOOGLEDRIVE_RESUMABLE_UPLOAD` for files >5MB or when basic uploads fail

### 2. Search and List Files

**When to use**: User wants to find specific files or browse Drive contents

**Tool sequence**:
1. `GOOGLEDRIVE_FIND_FILE` - Search by name, content, type, date, or folder [Required]
2. `GOOGLEDRIVE_LIST_FILES` - Browse files with folder scoping [Alternative]
3. `GOOGLEDRIVE_LIST_SHARED_DRIVES` - Enumerate shared drives [Optional]
4. `GOOGLEDRIVE_GET_FILE_METADATA` - Get detailed file info [Optional]
5. `GOOGLEDRIVE_GET_ABOUT` - Check storage quota and supported formats [Optional]

**Key parameters**:
- `q`: Drive query string (e.g., "name contains 'report'", "mimeType = 'application/pdf'")
- `corpora`: Search scope ('user', 'domain', 'drive', 'allDrives')
- `fields`: Response fields to include (e.g., 'files(id,name,mimeType)')
- `orderBy`: Sort key ('modifiedTime desc', 'name', 'quotaBytesUsed desc')
- `pageSize`: Results per page (max 1000)
- `pageToken`: Pagination cursor from `nextPageToken`
- `folder_id`: Scope search to a specific folder

**Pitfalls**:
- 403 PERMISSION_DENIED if OAuth scopes insufficient for shared drives
- Pagination required; files are in `response.data.files`; follow `nextPageToken` until exhausted
- `corpora="domain"` may trigger 400; try `"allDrives"` with `includeItemsFromAllDrives=true`
- Query complexity limits: >5-10 OR clauses may error "The query is too complex"
- Wildcards (*) NOT supported in `name`; use `contains` for partial matching
- 'My Drive' is NOT searchable by name; use `folder_id='root'` for root folder
- User email searches: use `'user@example.com' in owners` (NOT `owner:user@example.com`)

### 3. Share Files and Manage Permissions

**When to use**: User wants to share files or manage access permissions

**Tool sequence**:
1. `GOOGLEDRIVE_FIND_FILE` - Locate the file to share [Prerequisite]
2. `GOOGLEDRIVE_ADD_FILE_SHARING_PREFERENCE` - Set sharing permission [Required]
3. `GOOGLEDRIVE_LIST_PERMISSIONS` - View current permissions [Optional]
4. `GOOGLEDRIVE_GET_PERMISSION` - Inspect a specific permission [Optional]
5. `GOOGLEDRIVE_UPDATE_PERMISSION` - Modify existing permission [Optional]
6. `GOOGLEDRIVE_DELETE_PERMISSION` - Revoke access [Optional]

**Key parameters**:
- `file_id`: ID of file to share
- `type`: 'user', 'group', 'domain', or 'anyone'
- `role`: 'owner', 'organizer', 'fileOrganizer', 'writer', 'commenter', 'reader'
- `email_address`: Required for type='user' or 'group'
- `domain`: Required for type='domain'
- `transfer_ownership`: Required when role='owner'

**Pitfalls**:
- Invalid type/email combinations trigger 4xx errors
- Using `type='anyone'` or powerful roles is risky; get explicit user confirmation
- Org policies may block certain sharing types, causing 403
- Permission changes may take time to propagate
- Use `GMAIL_SEARCH_PEOPLE` to resolve contact names to emails before sharing

### 4. Create and Organize Folders

**When to use**: User wants to create folder structures or move files between folders

**Tool sequence**:
1. `GOOGLEDRIVE_FIND_FILE` - Check if folder already exists [Prerequisite]
2. `GOOGLEDRIVE_CREATE_FOLDER` - Create a new folder [Required]
3. `GOOGLEDRIVE_GET_FILE_METADATA` - Verify created folder [Optional]
4. `GOOGLEDRIVE_MOVE_FILE` - Move files between folders [Optional]
5. `GOOGLEDRIVE_UPDATE_FILE_PUT` - Update file metadata/parents [Alternative]

**Key parameters**:
- `name`: Folder name
- `parent_id`: Parent folder ID (NOT name); omit for root
- `file_id`: File to move
- `add_parents`: Destination folder ID for move
- `remove_parents`: Source folder ID to remove from

**Pitfalls**:
- `GOOGLEDRIVE_CREATE_FOLDER` requires `parent_id` as an ID, not a folder name
- Using `parent_id="root"` creates at top level; for nested paths, chain folder IDs
- `GOOGLEDRIVE_FIND_FILE` returns ~100 items/page; follow `nextPageToken` for large drives
- Move operations can leave items with multiple parents; use `remove_parents` for true moves
- Always verify parent folder exists before creating children

## Common Patterns

### ID Resolution
- **File/folder name -> ID**: `GOOGLEDRIVE_FIND_FILE` with `q` parameter
- **Root folder**: Use `folder_id='root'` or `'root' in parents`
- **Shared drive -> driveId**: `GOOGLEDRIVE_LIST_SHARED_DRIVES`
- **Contact name -> email**: `GMAIL_SEARCH_PEOPLE` (for sharing)

### Query Syntax
Google Drive uses a specific query language:
- Name search: `"name contains 'report'"` or `"name = 'exact.pdf'"`
- Type filter: `"mimeType = 'application/pdf'"` or `"mimeType = 'application/vnd.google-apps.folder'"`
- Folder scoping: `"'FOLDER_ID' in parents"`
- Date filter: `"modifiedTime > '2024-01-01T00:00:00'"`
- Combine with `and`/`or`/`not`: `"name contains 'report' and trashed = false"`
- Boolean filters: `"sharedWithMe = true"`, `"starred = true"`, `"trashed = false"`

### Pagination
- Follow `nextPageToken` until absent for complete results
- Set `pageSize` explicitly (default 100, max 1000)
- De-duplicate results if running multiple searches

### Export Formats
For Google Workspace files, set `mime_type` to export:
- **Docs**: `application/pdf`, `text/plain`, `text/html`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
- **Sheets**: `text/csv`, `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- **Slides**: `application/pdf`, `application/vnd.openxmlformats-officedocument.presentationml.presentation`

## Known Pitfalls

- **Internal storage required**: Upload requires files in internal S3 storage (s3key)
- **Export vs download**: Set `mime_type` ONLY for Google Workspace files; omit for native files
- **Temporary URLs**: Downloaded content via `s3url` is temporary; fetch promptly
- **Query complexity**: >5-10 OR clauses may error; split complex searches into multiple queries
- **Shared drive scoping**: Missing drive permissions yield empty results; verify access first
- **No wildcards**: Use `contains` operator instead of `*` for partial name matching
- **Folder creation chains**: Always pass folder IDs (not names) as `parent_id`
- **Multiple parents**: Move operations may leave items with multiple parents; use `remove_parents`
- **Rate limits**: Heavy searches/exports can trigger 403/429; implement backoff

## Quick Reference

| Task | Tool Slug | Key Params |
|------|-----------|------------|
| Search files | `GOOGLEDRIVE_FIND_FILE` | `q`, `corpora`, `pageSize` |
| List files | `GOOGLEDRIVE_LIST_FILES` | `folderId`, `q`, `orderBy` |
| Upload file | `GOOGLEDRIVE_UPLOAD_FILE` | `file_to_upload`, `folder_to_upload_to` |
| Resumable upload | `GOOGLEDRIVE_RESUMABLE_UPLOAD` | file data |
| Download file | `GOOGLEDRIVE_DOWNLOAD_FILE` | `file_id`, `mime_type` (Workspace only) |
| File metadata | `GOOGLEDRIVE_GET_FILE_METADATA` | `fileId`, `fields` |
| Create folder | `GOOGLEDRIVE_CREATE_FOLDER` | `name`, `parent_id` |
| Move file | `GOOGLEDRIVE_MOVE_FILE` | `file_id`, `add_parents`, `remove_parents` |
| Share file | `GOOGLEDRIVE_ADD_FILE_SHARING_PREFERENCE` | `file_id`, `role`, `type`, `email_address` |
| List permissions | `GOOGLEDRIVE_LIST_PERMISSIONS` | `fileId` |
| Update permission | `GOOGLEDRIVE_UPDATE_PERMISSION` | file_id, permission_id |
| Delete permission | `GOOGLEDRIVE_DELETE_PERMISSION` | file_id, permission_id |
| List shared drives | `GOOGLEDRIVE_LIST_SHARED_DRIVES` | `pageSize` |
| Drive info | `GOOGLEDRIVE_GET_ABOUT` | (none) |
| Create shortcut | `GOOGLEDRIVE_CREATE_SHORTCUT_TO_FILE` | target file_id |

---
