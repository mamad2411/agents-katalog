---
name: kendo-ui-upload-file-workflows
description: Use when Kendo UI Upload or FileManager workflows need chunking, validation, retry, signed endpoint integration, and secure end-to-end file lifecycle behavior.
---

# Kendo UI Upload and File Workflows

## Specialization

Implement and review production-grade file ingestion workflows with Kendo Upload and FileManager, emphasizing reliability, explicit validation boundaries, and secure lifecycle controls.

## Trigger Conditions

- File upload is introduced or expanded.
- Large files require chunked upload.
- File upload retries or resumable behavior are needed.
- Signed URL upload/download patterns are in scope.
- Upload security incidents or validation bypasses are observed.

## Scope Boundaries

In scope:

- Upload component configuration and event contracts.
- Chunking, retry, and resume strategies.
- File type/size validation at UI boundary.
- Workflow contracts for upload success, failure, and cancellation.
- FileManager interaction patterns with backend APIs.

Out of scope:

- Server malware scanning engine implementation.
- Storage platform provisioning.
- Broad security policy ownership (see `kendo-ui-security`).

## Inputs

- Allowed file types and size limits.
- Upload volume and expected network conditions.
- Backend endpoint capabilities (chunk, resume, signed URL).
- Retention and deletion policy constraints.

## Required Outputs

- Upload config contract for limits, chunking, and retries.
- Validation behavior matrix for accepted/rejected files.
- Failure recovery flow and user messaging contract.
- Security handoff checklist to `kendo-ui-security`.
- Test scenarios for cancellation, partial failure, and resume.

## Core Patterns

### Upload Configuration

```javascript
$("#documents").kendoUpload({
    async: {
        saveUrl: "/api/files/upload",
        removeUrl: "/api/files/remove",
        autoUpload: true,
        chunkSize: 1048576
    },
    validation: {
        allowedExtensions: [".pdf", ".docx", ".xlsx"],
        maxFileSize: 10485760
    }
});
```

### Upload Error Handling

```javascript
error: function(e) {
    // Preserve actionable failure details for retry and support triage.
    showUploadError(e.XMLHttpRequest && e.XMLHttpRequest.responseText);
}
```

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Add basic validated upload | Invalid files are blocked |
| L2 Delivery | Chunked upload with retries | Expected network failures recover |
| L3 Hardening | Secure and auditable file lifecycle | Validation and recovery matrix passes |
| L4 Expert | Reusable upload workflow standard | Cross-project upload contracts documented |
