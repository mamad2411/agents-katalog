---
name: apc-drive-pdf-upload-archive
description: Upload newly generated APC/Academy of Celebrants brochure, leaflet, business-card, or print-proof PDFs to the correct Google Drive client folder while archiving the previous live PDF safely. Use this whenever the user asks to upload a celebrant/APC proof PDF to Drive, replace leaflet.pdf/business-cards.pdf, archive the old proof, send the final proof to the Academy of Celebrants folder, or finish a brochure/card generation workflow from any current project. This should trigger even if the user only says “upload it to Drive”, “put the PDF in the right APC folder”, “archive the old leaflet”, “replace the client proof”, or references a current celebrant brochure/card project.
compatibility:
  tools: [read, bash, mcp]
  optional_bins: [pdfinfo, rclone, gws]
---

# APC Drive PDF Upload Archive

Use this skill to complete the last mile of APC/Academy of Celebrants print-proof work: put the newest generated PDF into the correct Google Drive client folder under `Academy of Celebrants`, keep the live filename predictable, and preserve the old live PDF in `Archive`.

The core safety rule: **do not report the Drive upload as complete until cloud state is verified**. If you only staged files through Google Drive Desktop, say that plainly and continue verification.

## Inputs to resolve first

Determine these before mutating Drive:

- **Source PDF**: the newly generated local proof PDF.
  - If the user says “current project” or “upload it”, infer from the current repo by looking for the newest relevant `*.pdf`, especially names like `*template-proof.pdf`, `*proof.pdf`, `*leaflet*.pdf`, or `*business-card*.pdf`.
  - If more than one plausible PDF exists, ask which one to use.
- **Client Drive folder name**: usually the celebrant/client name, e.g. `Sample Celebrant`.
  - Infer from the filename/repo/docs when obvious, otherwise ask.
- **Live Drive filename**: usually `leaflet.pdf` for brochures/leaflets and `business-cards.pdf` for cards.
  - Keep this exact live filename in the client folder so shared review links/workflows stay predictable.
- **Parent Drive folder**: default to `Academy of Celebrants` unless the user says otherwise.

## Local PDF verification

Before touching Drive, verify the source artifact:

```bash
pdfinfo "/absolute/path/to/source.pdf"
stat -f "%z bytes %N" "/absolute/path/to/source.pdf"
```

Acceptable minimum checks:

- File exists.
- File size is non-zero.
- `pdfinfo` succeeds when installed.
- Page count and page size look right for the deliverable.

If `pdfinfo` is missing, continue with `file` and `stat`, but mention the lighter verification in the final response.

## Preferred path: Drive connector / API write

Prefer a real Google Drive connector/API path because it gives immediate cloud truth. Use whatever Drive-capable tool is available in the environment (`mcp` Drive tools, `gws drive`, `gog`, or another configured connector). Use read/list calls first to ground every ID.

### 1. Discover the target folders

Find the parent folder:

```json
{
  "query": "",
  "topn": 20,
  "special_filter_query_str": "mimeType = 'application/vnd.google-apps.folder' and name contains 'Academy'"
}
```

Then list the parent folder and locate the exact client folder.

### 2. Inspect current client folder state

List the client folder and identify:

- Current live file matching the live filename, e.g. `leaflet.pdf`.
- Existing `Archive` folder, if any.
- Any naming collisions in `Archive`.

Read metadata for the current live file before moving it:

```json
{
  "fileId": "<LIVE_FILE_ID>",
  "fields": "id,name,mimeType,parents,modifiedTime,createdTime,size,webViewLink"
}
```

The `parents` value matters. When moving a file, remove only the verified current client folder parent.

### 3. Create or reuse `Archive`

If absent, create it under the client folder:

```json
{
  "name": "Archive",
  "parent_folder": "<CLIENT_FOLDER_ID>"
}
```

If `Archive` already exists, reuse its ID.

### 4. Move old live file into `Archive`

Use metadata-only update semantics:

```json
{
  "fileId": "<LIVE_FILE_ID>",
  "addParents": "<ARCHIVE_FOLDER_ID>",
  "removeParents": "<CLIENT_FOLDER_ID>"
}
```

If `Archive/<live filename>` already exists, avoid overwriting silently. Prefer a timestamped archive name for the older archive file or ask the user which historical copy to preserve. The live client-folder filename should stay predictable; archive filenames can be descriptive when needed.

### 5. Upload the new PDF as the live filename

```json
{
  "file_uri": "/absolute/path/to/source.pdf",
  "file_name": "leaflet.pdf",
  "mime_type": "application/pdf",
  "parent_folder_id": "<CLIENT_FOLDER_ID>"
}
```

Use `business-cards.pdf` or the user-provided live filename when appropriate.

### 6. Verify cloud state

List both folders after mutation:

- Client folder should contain the new live PDF with the expected size plus any other client files.
- `Archive` should contain the old live PDF.

Where possible, read metadata for the new live file and archived file and compare sizes to the local source and old live file metadata.

## If connector write fails

If the connector returns `ACCESS_TOKEN_SCOPE_INSUFFICIENT`, missing scopes, auth errors, or a write-permission failure:

- Do **not** say the Drive upload is complete.
- Say the Drive connection needs reauthentication with write scopes.
- Then try the Drive Desktop fallback only if the target folder exists in the local Google Drive mount.

## Fallback: Google Drive Desktop mount

Use this only when API/connector writes are blocked, or when the user explicitly wants local Drive Desktop staging.

Typical mount pattern:

```text
/Users/<local-user>/Library/CloudStorage/GoogleDrive-<account>/My Drive/Academy of Celebrants/<Client Name>
```

Before staging, check available disk space because DriveFS can fail or silently stall when disk is critically low:

```bash
df -h / /Users/jack/Library/CloudStorage "$(pwd)"
```

Use the bundled helper for safer local staging:

```bash
/Users/jack/.agents/skills/apc-drive-pdf-upload-archive/scripts/stage-drive-desktop-pdf-upload.sh \
  --client "Client Name" \
  --source "/absolute/path/to/new-proof.pdf" \
  --live-name "leaflet.pdf" \
  --drive-root "/absolute/path/to/My Drive"
```

Optional flags:

```bash
--parent "Academy of Celebrants"
--account "your-google-account@example.com"
--drive-root "/custom/My Drive/path"
```

The helper:

- Verifies the source PDF exists and has non-zero size.
- Finds the client folder in the local Drive mount.
- Creates `Archive` if needed.
- Moves the old live file into `Archive` without silently overwriting an existing archive file.
- Copies the new PDF into the client folder using the live filename.
- Prints file sizes and DriveFS item IDs when available.

After using Drive Desktop, wait briefly and verify xattrs:

```bash
xattr -p com.google.drivefs.item-id#S "/path/to/client/Archive" 2>/dev/null || true
xattr -p com.google.drivefs.item-id#S "/path/to/client/leaflet.pdf" 2>/dev/null || true
```

Then verify through the Drive connector/listing. A local file without a Drive item ID, or unchanged cloud readback, means the upload is only locally staged and not confirmed.

## Fallback: rclone

Use `rclone` only after confirming the remote works read-only:

```bash
rclone listremotes
rclone lsf "gdrive:Academy of Celebrants/Client Name" --format "pst" --separator "|"
```

If the token is expired (`invalid_grant`), stop and report the recovery step:

```bash
rclone config reconnect gdrive:
```

Do not attempt writes until the read-only listing succeeds.

## Final response format

Separate the outcome into these sections so the user can tell cloud truth from local staging:

```markdown
Done / Not done yet: [one sentence]

Local source verified:
- PDF: ...
- Pages/size: ...

Verified Drive cloud state:
- Client folder: ...
- Live file: ... size ... ID/link if available
- Archive: ... old file ... size ... ID/link if available

Local staged state, if any:
- ...

Blockers / recovery, if any:
- ...

Next step:
- ...
```

If verification failed, lead with “Not done yet” and give the exact blocker/recovery command. This prevents accidentally telling Jack a client proof is uploaded when it is only queued or stuck locally.

## Template privacy note

This reusable pack intentionally contains no client-specific Drive paths, IDs, examples, or cloud-state captures. Resolve the current client folder and IDs with read-only provider calls at runtime, then record only the redacted evidence appropriate to that client handover.
