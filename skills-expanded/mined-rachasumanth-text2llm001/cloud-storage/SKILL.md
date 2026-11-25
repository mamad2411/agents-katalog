---
name: cloud-storage
description: Sync Text2LLM artifacts to user cloud storage providers with user-scoped OAuth, resumable uploads, and quota-aware checkpoint handling.
---

# Cloud Storage

Use this skill to persist Text2LLM project artifacts to user-selected cloud storage.
The agent must never own provider credentials; user authorization is required.

## Supported Providers

- Google Drive (`pydrive2`, OAuth 2.0)
- Dropbox (`dropbox` SDK, OAuth 2.0 PKCE)
- OneDrive (`msal` + Microsoft Graph, OAuth 2.0)
- MEGA (`mega.py`, session auth)
- AWS S3 (`boto3`, IAM credentials or SSO)
- Google Cloud Storage (`google-cloud-storage`, service account or ADC)
- Azure Blob Storage (`azure-storage-blob`, connection string or managed identity)

## Credential and OAuth Rules

- The user completes provider-side OAuth/auth flows.
- The agent never stores raw provider credentials in prompts, logs, or static config files.
- Store only minimal session-scoped tokens/handles required for active sync.
- If auth expires, request re-authentication and resume safely.

## Standard Project Layout

Use this canonical remote path per project:

`Text2LLM/<project>/{data,tokenizer,checkpoints,evals,model}/`

Map artifacts consistently:

- data artifacts -> `data/`
- tokenizer files -> `tokenizer/`
- training checkpoints -> `checkpoints/`
- evaluation outputs -> `evals/`
- final published model assets -> `model/`

## Automatic Checkpoint Sync

- After each training checkpoint save, enqueue an upload job.
- Prioritize newest + best checkpoints first when bandwidth is constrained.
- Confirm upload integrity (size/hash where provider supports it).
- Emit sync status updates with file, step, and provider destination.

## Resumable Uploads

- Use chunked/resumable uploads for large files.
- On interruption, resume from the last successful chunk rather than restarting.
- Retry with bounded backoff and clear failure reason reporting.

## Provider Selection Memory

- Let the user choose a provider per project.
- Persist provider selection metadata per project for future sessions.
- Allow explicit provider override when user requests a different target.

## Quota Awareness

- Check available storage before starting large uploads.
- Warn early when free space is low relative to queued artifacts.
- Recommend cleanup/compression/tiering actions when quota risk is high.
- Block uploads only when provider reports hard quota exhaustion.

## Python Dependencies

- `pydrive2`
- `dropbox`
- `msal`
- `requests`
- `mega.py`
- `boto3`
- `google-cloud-storage`
- `azure-storage-blob`

## Deliverables

1. `cloud_sync_config.json` (provider + project mapping, no raw secrets)
2. `sync_manifest.json` (uploaded files, versions, remote paths)
3. `sync_status.md` (latest run status + quota notes)

## Preflight Validation

Before starting any sync operation, validate:

- Required credentials/env vars are set for the selected provider.
- Provider API is reachable and auth is valid.
- Sufficient quota/storage is available for queued artifacts.

Report clear errors identifying which credentials are missing and where to set them.
