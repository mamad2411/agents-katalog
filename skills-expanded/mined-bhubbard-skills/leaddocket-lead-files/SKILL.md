---
name: leaddocket-lead-files
description: >
  Upload, download, and manage files attached to Leads in LeadDocket.
  Covers standard multipart upload (up to 30MB), large file upload via SAS URL
  (up to 500MB), finalizing large uploads, associating uploaded files with
  custom fields, and downloading files by ID. Use for attaching documents,
  photos, medical records, or any file to a lead. For e-sign documents use
  leaddocket-docusign.
---

# LeadDocket — Lead Files

All endpoints require API key authentication. Base URL: `https://{instance}.leaddocket.com`.

---

## Upload a file (standard, up to 30MB)

```http
POST /api/leads/{id}/files/upload?uploadedBy={name}&allowDuplicateFilesOnLead={bool}
Content-Type: multipart/form-data

[file binary in body]
```

| Param | Required | Description |
|-------|----------|-------------|
| `id` (path) | Yes | Lead ID |
| `uploadedBy` | No | Uploader name shown in the UI |
| `allowDuplicateFilesOnLead` | No | Default `true` — set `false` to reject duplicate filenames |

Returns `200 OK` with `LeadFileUploadApi` including the new `FileId`.

---

## Upload a large file (up to 500MB) — 3-step process

### Step 1: Get an upload URL

```http
POST /api/leads/{id}/files/getuploadurl?fileName={name.ext}&uploadedBy={name}
```

Returns `BlobUrlResponseModel`:

```json
{
  "UploadUrl": "https://storage.azure.com/...",
  "FileId": 4567,
  "Headers": {
    "x-ms-blob-type": "BlockBlob"
  }
}
```

The upload URL is valid for **45 minutes**.

### Step 2: PUT the file to the blob URL

```http
PUT {UploadUrl}
x-ms-blob-type: BlockBlob
Content-Type: {file mime type}

[file binary]
```

Include all headers from the `Headers` map in the response. This is a direct Azure Storage call — no auth header needed.

### Step 3: Finalize the upload

```http
POST /api/leads/{id}/files/{fileId}finalizeupload
```

Returns `200 OK` with `LeadFileUploadApi`. The file is now visible on the lead.

---

## Associate a file with a custom field

Links an uploaded file to a file-type custom field on the lead.

```http
POST /api/leads/{id}/files/{fileId}/associatefilewithfield/{fieldId}
```

| Path param | Description |
|-----------|-------------|
| `id` | Lead ID |
| `fileId` | File ID from the upload response |
| `fieldId` | Custom field ID (from `GET /api/customfields/list`) |

Returns `200 OK` with `LeadFileUploadApi`.

---

## Download a file

```http
GET /api/leads/files/download/{id}
```

Returns the file binary with appropriate `Content-Type` header. Stream the response to disk.

---

## Best Practices

- **Under 30MB → standard upload**: Simpler, single request. Use for most documents.
- **Over 30MB → large file upload**: Must use the 3-step SAS URL flow. The 45-minute window is generous but start the upload promptly.
- **Check `IsValid` on blob URL response**: If `IsValid` is `false`, check `ErrorMessage` before attempting upload.
- **Duplicate guard**: Set `allowDuplicateFilesOnLead=false` in automated workflows to prevent uploading the same document twice.
- **Custom field association**: Required when the lead form expects a file in a specific field. Get field IDs from `GET /api/customfields/list` (see `leaddocket-lead-custom-fields`).
- **Finalize is mandatory for large uploads**: Skipping finalize leaves the file in a pending state and it will not appear in the lead UI.
