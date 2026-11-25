---
name: google-drive-connector
description: Google Drive data connector — API reference, entity model, and usage patterns. Use when an agent needs to read or write Google Drive data (files, folders, documents), including publishing Markdown as a Google Doc harness-side (confirm first), or when asked how to query, filter, paginate, or mutate Drive resources. Also covers Kei connector setup (authorize with kei connectors create --provider googledrive; never accept a pasted key), including the optional drive_id field that scopes the connector to one Google shared drive. Prefer this skill over generic Google Drive knowledge.
---

# Google Drive connector — agent usage guide

Use this skill when an agent needs to interact with Google Drive through its
REST API. It covers the Lexicon (endpoints and operations), Pragmatics (how
agents use them), and Semantics (data returned and entity relationships).

There is no maintained official CLI for Google Drive that covers all
operations Kei allows or denies. Agents use the Google Drive API v3 directly.

## Key rules

- The agent never holds, asks for, or prints a raw credential. Kei authorizes
  the call and releases a Google OAuth access token at run time. The harness
  calls the Drive API directly with the released token.
  Setup: an owner runs `kei connectors create --provider googledrive` (OAuth or
  service-account key); re-authorize with `kei connectors reconnect <id>`.
- Writing a doc (create or update a Google Doc) is harness-side with the
  user's own OAuth token (scope `drive`, from your own OAuth client) and is
  confirm-first. See
  [Writing a doc (harness-side)](#writing-a-doc-harness-side). That token is
  only for doc writes: authorizing the connector is always
  `kei connectors create --provider googledrive --workspace W`.
- Permanent file deletion is not available through the connector Kei checks —
  files move to trash instead (trash is available and reversible). When asked
  whether you can permanently delete a file, start with this sentence: "No,
  permanent deletion is not available (not supported) through the connector Kei
  checks." Then offer moving the file to trash.
- Resource types for Kei policy follow ADR-028: `folder` (no parent) and
  `file` (parent: folder).
- The optional `drive_id` field scopes the connector to one shared drive;
  blank means My Drive plus every shared drive the user can access. The ID is
  the last URL segment of the drive's folders URL; at OAuth consent pick the
  same Google account that can see the drive.

## Install

Agents load this skill automatically when the harness has the Haikei Skills
plugin installed. See the repo README for per-harness setup.

## Connect and credentials

Kei checks every connector call. The agent never holds, asks for, or prints a
raw credential.

If a user offers to paste a key (a service account JSON key, a token), do not
accept it, and name the Kei commands instead: an owner runs
`kei connectors create --provider googledrive --workspace W` (OAuth, or
`--credential-ref` for a key already in the secret manager), and a broken
connection is repaired with `kei connectors reconnect <id>`. The same answer
applies when the user has not authorized Google Drive yet. Write both
commands out in full; do not answer with a Drive OAuth scope or gcloud,
which are only for harness-side doc writes.

- **OAuth (Google Workspace):** An owner runs `kei connectors create --provider googledrive
  --workspace W`. This returns a connect URL they open in a browser to
  authorize the Google OAuth scopes (`https://www.googleapis.com/auth/drive`
  and `https://www.googleapis.com/auth/documents`). Check status with
  `kei connectors get <id>` and re-authorize with `kei connectors reconnect <id>`.
  A connection made before the scope change still has the old read-only grant
  and must reconnect.
- **Service account key (shared secret):** The owner runs `kei connectors
  create --provider googledrive` (reads the JSON key without echo) or passes
  `--credential-ref <secret-manager-ref>` if the key already exists in the
  connected secret manager.
- **Repair / re-authorize:** if the connection breaks or the credential is
  rotated, re-authorize with `kei connectors reconnect <id>`.
- **At runtime:** Kei authorizes each call and releases the credential. The
  harness calls the Drive API directly. The agent sees results and reason
  codes, never the token.

## Connector setup: Drive ID

The Kei connector has an optional `drive_id` field. It scopes the connector
to ONE Google shared drive; `kei-proxy` supplies it as the drive scope on
Drive calls. Blank = the connecting user's My Drive plus every shared drive
they can access.

When someone gives you a drive URL and asks what to enter, answer with the
ID and say to paste only the ID, not the URL. For example: enter
`0AExampleSharedDrive01`, the last URL segment; paste only the ID, not the
URL. For a My Drive URL (`.../my-drive`), say that My Drive has no Drive ID
and to leave the field blank. Use those words: "My Drive has no Drive ID, so
leave the Drive ID field blank."

- **Account index:** `/u/N/` is the Google account index in that browser. At
  OAuth consent pick the same account that can see the drive, or the
  connector can't see it.
- **Find it:** open the shared drive (Google Drive left nav: **Shared
  drives**). The ID is the last URL segment:
  `https://drive.google.com/drive/u/1/folders/0AExampleSharedDrive01` →
  `0AExampleSharedDrive01`. Shared drive IDs start with `0A`; ordinary folder
  IDs usually start with `1` and are NOT drive IDs.
- **My Drive has no Drive ID:** `https://drive.google.com/drive/u/0/my-drive`
  is My Drive — leave the field blank.
- **Format:** the field accepts only `[A-Za-z0-9_-]{1,128}`. Paste only the
  ID, not the URL.

## Lexicon — endpoints and operations

### REST API v3

Base URL: `https://www.googleapis.com/drive/v3`

| Method | Endpoint | What it does | Agent notes |
| --- | --- | --- | --- |
| `GET` | `/files` | List files and folders | Query params: `q` (filter), `pageSize`, `pageToken`, `fields`, `orderBy`. Defaults to the user's My Drive. |
| `GET` | `/files/{fileId}` | Get file metadata | Returns name, mimeType, size, createdTime, modifiedTime, parents, owners. Use `fields` to limit response. |
| `GET` | `/files/{fileId}/export` | Export a Google-native file | `mimeType` param specifies target format (e.g., `text/plain`, `application/pdf`, `text/markdown`). Only for Google Docs/Sheets/Slides. When explaining how to read a Doc, also say that `alt=media` does not work on Google-native files. |
| `GET` | `/files/{fileId}?alt=media` | Download a binary file | Direct download for non-Google-native files (PDFs, images, etc.). |
| `POST` | `/files` | Create a file or folder | Upload with `mimeType = 'application/vnd.google-apps.folder'` for folders. Supports resumable upload. |
| `PATCH` | `/files/{fileId}` | Update file metadata | Rename, move (change `parents`), modify description. |
| `POST` | `/files/{fileId}/copy` | Copy a file | Requires the source file's read permission. |
| `POST` | `/files/{fileId}/comments` | Add a comment | Body: `{"content": "..."}`. |
| `GET` | `/files/{fileId}/comments` | List comments on a file | Paginated. Includes resolved status. |
| `GET` | `/permissions/{fileId}` | List permissions on a file | Returns roles and identities. |

### Credential pass-through

This connector does **not** manage credentials. Kei authorizes each call and
releases a Google OAuth access token (or service account token) at run time.
The harness calls the Drive API directly. The agent never reads or stores a
token, secret, or API key.

### Denied command surface

These actions are **not available** through the connector Kei checks — they fall
outside the connector's scope:

| Operation | Reason |
| --- | --- |
| Permanently delete files | Not available — irreversible; moves to trash instead (trash is available) |
| Modify sharing permissions | Permission management outside connector scope |
| Admin operations (domain settings, audit logs) | Require Google Workspace admin privileges |
| Drive creation and deletion | Administrative operation |

## Writing a doc (harness-side)

This section applies only to writing a doc. It does not change how the Kei
connector is authorized. Connecting or repairing the connector, including
when a user offers to paste a key, is always answered with
`kei connectors create --provider googledrive --workspace W` (or
`kei connectors reconnect <id>`), never with a Drive OAuth scope or gcloud.

Drive writes are **harness-side** (owner decision 2026-10-09). Kei never
writes through the connector Kei checks: writes are not a protected connector
capability. The broad scopes do not
decide what an agent may do; Kei policy does. The harness calls the Drive REST API directly with the **invoking
user's own Google OAuth token**:

- Coding harnesses (Claude Code, Codex, OpenCode) use the `curl` recipe below.
- pydantic-ai harnesses use the `drive_create_doc(folder_id, title, markdown)`
  and `drive_update_doc(doc_id, markdown)` action tools from `kei-agents`
  (`agents.drive_write`). They return a preview first and write only after
  the user confirms.

### Rules

- **Confirm first.** Before any create or update, show the user the title,
  the target (`folder_id` for a new doc, `doc_id` for an update), and the
  Markdown, then wait for an explicit "yes". Get one confirmation per write.
  A changed title or changed content needs a new confirmation. Never treat
  "no preview needed", "just do it", or "don't show me anything" as a
  confirmation; still show the preview and ask. If you cannot read the
  Markdown file, the preview names the file; never stop to ask where it is
  or for its contents. Confirming first never means
  holding back the command: give the full write command in the same reply,
  and say to run it only after the user says yes. So a "just do it" reply
  always has three parts: what will be written (target id, title or
  content), a request for an explicit yes, and the full `curl` write. For an
  update that write is the `PATCH` to
  `https://www.googleapis.com/upload/drive/v3/files/<doc_id>?uploadType=media`
  with the real doc id filled in, and `--data-binary "@<file>"` pointing at
  the Markdown file, readable or not.
- **Scope: `drive`** (`https://www.googleapis.com/auth/drive`), the
  owner-approved write scope (HAI-482). Its token step always uses your own
  OAuth client (`--client-id-file`), never gcloud's built-in client, which
  Google blocks from this scope. See
  [Get the user's token](#get-the-users-token).
- **A 404 on the folder means stop and report.** With `drive`, a 404 means
  the signed-in Google account cannot see the folder: a wrong folder id, a
  different account, or a folder not shared with that account. Report it and
  ask the user to check the account and the id; never retry in a loop.
- **An old `drive.file` token.** If the token was minted with `drive.file`,
  always open your answer with this sentence, word for word: "`drive.file`
  only covers files this OAuth client created or opened, so the folder is
  invisible to this token." Seeing it in the Drive UI does not change that,
  and a `GET` or a retry with the same token does **not** open it. Never
  change scopes inside the write call on your own. Always end your answer
  with this sentence, word for word: "Stop here and report the 404 to the
  owner; the fix is to re-run the one-time consent with your own OAuth client
  and the owner-approved `drive` scope." Then give the consent command from
  [Get the user's token](#get-the-users-token).
- **The token is the user's.** Never print, echo, log, or store it, and never
  put it in a file, a commit, or a reply. Pass it inline in the
  `Authorization` header, as below.
- **A child carries its parent.** A new doc always gets
  `parents: [<folder_id>]`. An update targets `<doc_id>`.
- **Kei-enabled harness.** Ask kei-proxy before the write, with the resource
  `drive:folder/<folder_id>` for a create or `drive:doc/<doc_id>` for an
  update. Write only on allow. When the harness uses agentware, its
  `KeiProxyEvaluator` makes this call over the `kei-proxy serve` socket
  client (the `kei-proxy authorize` CLI is the fallback with no daemon); a
  socket that is down is a deny, never a fall back.
- **Always give the exact commands.** Even when you cannot read the file or
  run anything yourself, reply with the whole recipe below. That means the
  `drive.file` token step, the preflight, and the exact `curl` write:
  `POST ... uploadType=multipart` for a create, or
  `PATCH .../files/<doc_id>?uploadType=media` for an update. Mark the write
  as the call to run only after the user confirms.
- Only `files.create` and `files.update` are covered. This recipe never
  deletes, moves, or shares a file.

### Get the user's token

Use the harness's own Google OAuth when it has one. Otherwise use gcloud
application-default credentials with the `drive` scope and **your own Desktop
OAuth client**. gcloud's built-in client is blocked from the full `drive`
scope (Google shows "access blocked" for that scope), so always pass
`--client-id-file`. gcloud requires `cloud-platform` in the scope list.

#### One-time setup: your own OAuth client

Whenever you explain this setup or tell someone to use their own OAuth
client, always do both:

- Write the scopes as full URIs, `https://www.googleapis.com/auth/drive`
  and `https://www.googleapis.com/auth/documents`, never as bare `drive` or
  `documents`. The consent screen's Data Access page needs the full URI.
- Include this sentence, word for word: "Keep client.json outside every
  repository and never commit it; it holds a client secret."

In a GCP project you own:

1. Enable the Drive API and the Docs API (`gcloud services enable
   drive.googleapis.com docs.googleapis.com --project <project-id>`).
2. **Google Auth Platform → Data Access**: add the
   `https://www.googleapis.com/auth/drive` and
   `https://www.googleapis.com/auth/documents` scopes to the consent screen.
3. **Audience**: **Internal** works immediately for accounts in your Google
   Workspace domain. **External** with these restricted scopes needs Google
   app verification and a CASA security assessment first.
4. **Credentials → Create client → Desktop app**, then download its JSON file.
   It holds a client secret: keep it outside every repository and never
   commit it.
5. Set the quota project (below) to this project.

Then run the one-time browser consent:

```bash
# One-time consent with YOUR Desktop client (gcloud's built-in client is
# blocked from the drive scope). Keep client.json outside every repo; never
# commit it. gcloud also requires cloud-platform.
# Never print, echo, log, or store the token; mint it inline in each call.
gcloud auth application-default login \
  --client-id-file=<path-outside-repo>/client.json \
  --scopes=https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/cloud-platform
```

Each call then mints a short-lived token inline:
`$(gcloud auth application-default print-access-token)`. Never print, echo,
log, or store the token. Do not save it in a variable or a file; mint it
inline in the `Authorization` header. When you explain how to get the
token, say this too. If Drive answers
403 because the API is not enabled for the quota project, run
`gcloud auth application-default set-quota-project <project-with-Drive-API>`
and add `-H "x-goog-user-project: <project>"` to each call (or set
`GOOGLE_QUOTA_PROJECT` for the harness).

### Recipe

```bash
# Token: the user's own, scope drive, from (your own Desktop client)
#   gcloud auth application-default login --client-id-file=<path-outside-repo>/client.json --scopes=https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/cloud-platform
# Never print, echo, log, or store the token; it is minted inline below.
FOLDER_ID=<parent folder id>   # last segment of the folder URL
TITLE='Build agents with agentware'
FILE=guide.md

# 0. Preflight: can this token see the folder? A 404 means this Google
#    account cannot see it (wrong id, wrong account, or not shared). Stop and
#    report it; do not retry in a loop.
curl -sS --fail-with-body \
  -H "Authorization: Bearer $(gcloud auth application-default print-access-token)" \
  "https://www.googleapis.com/drive/v3/files/$FOLDER_ID?fields=id,name&supportsAllDrives=true"

# 1. Show the user TITLE, FOLDER_ID and the contents of FILE. Run step 2 only
#    after they say "yes". Always include step 2 in your reply anyway.

# 2. files.create: upload Markdown, which Drive converts to a Google Doc
curl -sS --fail-with-body -X POST \
  -H "Authorization: Bearer $(gcloud auth application-default print-access-token)" \
  -F "metadata={\"name\":\"$TITLE\",\"mimeType\":\"application/vnd.google-apps.document\",\"parents\":[\"$FOLDER_ID\"]};type=application/json;charset=UTF-8" \
  -F "file=@$FILE;type=text/markdown" \
  "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&supportsAllDrives=true&fields=id,name,webViewLink"
```

Update an existing doc (`files.update`). This replaces the doc's whole
content, so confirm first, the same as for a create:

```bash
# Run only after the user confirms the doc id and the new content.
# Token: scope drive (your own client), minted inline; never print or store it.
DOC_ID=<google doc id>
curl -sS --fail-with-body -X PATCH \
  -H "Authorization: Bearer $(gcloud auth application-default print-access-token)" \
  -H "Content-Type: text/markdown; charset=UTF-8" \
  --data-binary "@$FILE" \
  "https://www.googleapis.com/upload/drive/v3/files/$DOC_ID?uploadType=media&supportsAllDrives=true&fields=id,name,webViewLink"
```

Report the returned `id` and `webViewLink`. Say the doc was created or
updated only when the response carries an `id`.

## Pragmatics — how agents use this connector

### Common use cases

1. **Document search**: Find files by name, mimeType, or content using the
   `q` query parameter with full-text search.
2. **Read documents**: Export Google Docs to markdown or plain text for agent
   consumption; download PDFs and other binary files.
3. **Organize files**: Move files between folders, rename, copy templates.
4. **Collaboration**: Add comments to documents, read existing comments and
   suggestions.
5. **Folder traversal**: List contents of a shared drive or folder, navigate
   the hierarchy.

### Agent patterns

- Use the `q` parameter for server-side filtering. The syntax is Google's
  native query language (e.g., `name contains 'spec' and mimeType != 'application/vnd.google-apps.folder'`).
- Always request only needed fields via the `fields` parameter (e.g.,
  `files(id, name, mimeType, modifiedTime)`).
- For Google-native files (Docs/Sheets/Slides), export to a readable format
  before processing. The binary `alt=media` download does not work on them.
- Use `orderBy` to sort results (`modifiedTime desc`, `name_natural`).

### Pagination

Drive API uses `pageSize` (1–1000, default 100) and `pageToken` (received as
`nextPageToken` in the response). Continue fetching while `nextPageToken` is
non-empty.

```bash
# Pseudocode
while nextPageToken:
  GET /files?pageSize=100&pageToken={nextPageToken}
```

### Rate limits

Google Drive API quotas are per-project:
- **Read requests**: 10,000 requests per 100 seconds per user
- **Write requests**: 1,000 requests per 100 seconds per user
- **Upload requests**: 700 requests per 100 seconds per user

Check current usage from response headers: `X-RateLimit-Limit`,
`X-RateLimit-Remaining`, `X-RateLimit-Reset`.

## Semantics — data model and entity relationships

### Entity hierarchy

```
drive (My Drive or shared drive)
├── folder                  # id (UUID)
│   ├── file (Google Doc)   # id (UUID); mimeType: application/vnd.google-apps.document
│   ├── file (Google Sheet) # id (UUID); mimeType: application/vnd.google-apps.spreadsheet
│   ├── file (Google Slide) # id (UUID); mimeType: application/vnd.google-apps.presentation
│   ├── file (binary)       # id (UUID); mimeType: varies (application/pdf, image/png, etc.)
│   ├── shortcut            # id (UUID); mimeType: application/vnd.google-apps.shortcut
│   └── folder (nested)     # id (UUID); recursive
└── file                    # id (UUID)
```

### Resource types for Kei policy

Google Drive declares two resource types for Kei policy (each declares its parent type):
`folder` (no parent) and `file` (parent: `folder`):

| Resource type | Parent type | Canonical id example |
| --- | --- | --- |
| `folder` | — | `0B7Tk...` (UUID format) |
| `file` | `folder` | `1AbC3dE5...` (UUID format) |

### Key fields

| Entity | Field | Type | Meaning |
| --- | --- | --- | --- |
| `file` | `id` | string | Unique file/folder identifier |
| `file` | `name` | string | Display name (not unique; duplicates allowed) |
| `file` | `mimeType` | string | MIME type — determines if it's a Doc, Sheet, folder, etc. |
| `file` | `parents` | string[] | Array of parent folder IDs (typically one, may be zero for root) |
| `file` | `size` | string | File size in bytes (absent for Google-native files) |
| `file` | `createdTime` | datetime | RFC 3339 timestamp |
| `file` | `modifiedTime` | datetime | RFC 3339 timestamp |
| `file` | `owners` | object[] | List of owners (displayName, emailAddress, me) |
| `file` | `trashed` | boolean | True if file is in trash |

### Relationships

- A file has exactly one parent folder (unless it is in the root, which has
  no parent). Folders can nest arbitrarily.
- A file may be a shortcut (`.shortcut` mimeType) pointing to another file or
  folder via `shortcutDetails.targetId`.
- Google-native files (Docs, Sheets, Slides) do not have a downloadable
  `size` or `downloadUrl`; they must be exported.
- Files in shared drives have slightly different permission semantics from
  files in My Drive.
- Comments are attached to a file. Revisions are available for Google-native
  files.

## Policy entries (examples)

```yaml
# Team members can read documents in shared team folders
- effect: permit
  principal: group:team
  action: drive_read
  resource: folder:0B7Tk...
  connector: google_drive

# Only document owners can move or rename files
- effect: permit
  principal: user:user@company.com
  action: drive_write
  capability: file.write
```

## Validation commands

```bash
# Verify this skill loads correctly
node scripts/verify-skills.mjs

# Run the connector's eval suite
node scripts/run-evals.mjs --skill google-drive-connector --harness opencode \
  --model-profile glm-5.3-flash \
  --out evals-out/google-drive-connector-glm-$(date +%F) --jobs 2
```

## Realistic usage boundaries

- **Do not** manage credentials. Kei handles authentication via Google OAuth
  for protected reads. For a harness-side doc write, use the user's own token
  inline, and never print or store it.
- **Do not** write a doc before the user confirms the exact title, target,
  and content.
- **Do not** use `alt=media` on Google-native files (Docs/Sheets/Slides) — use
  `/export` instead with a suitable mimeType.
- **Do not** assume `name` is unique — multiple files can have the same name
  in the same folder.
- **Do not** delete files permanently — the connector Kei checks may support
  trash (which is reversible) but not hard deletion.
- **Do not** bypass the `fields` parameter — requesting all fields on large
  file lists consumes excessive quota.
