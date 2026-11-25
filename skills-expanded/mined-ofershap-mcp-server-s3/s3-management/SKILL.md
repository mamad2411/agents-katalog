---
name: s3-management
description: Manage AWS S3 buckets and objects via MCP. Use when the user asks to list S3 buckets, browse a prefix, download a config file from S3, upload text to a key, delete an object, or create a presigned URL.
---

# AWS S3 Management via MCP

Use this skill when you need to manage S3 buckets, browse objects, upload/download files, or generate presigned URLs.

## Available Tools

| Tool            | What it does                                         |
| --------------- | ---------------------------------------------------- |
| `list_buckets`  | List all S3 buckets in the AWS account               |
| `list_objects`  | List objects in a bucket with optional prefix filter |
| `get_object`    | Download and read an object's content as text        |
| `put_object`    | Upload text content to an S3 object                  |
| `delete_object` | Delete an object from a bucket                       |
| `presigned_url` | Generate a temporary presigned URL for an object     |
| `bucket_info`   | Check if a bucket exists and get basic info          |

## Workflow

1. Start with `list_buckets` to discover available buckets
2. Use `list_objects` with a prefix to browse directories within a bucket
3. `get_object` reads text content; for binary files, use `presigned_url` instead
4. `presigned_url` generates a temporary shareable link (default 1 hour expiry)

## Key Patterns

- `list_objects` uses prefix-based filtering (S3 doesn't have real directories): `prefix: "uploads/2026/"`
- `get_object` returns text content only; it won't work for images, binaries, or large files
- `put_object` takes string content; use it for config files, JSON, text, not binary uploads
- `presigned_url` is the right tool for sharing files or accessing binary content

## Error Scenarios

- AccessDenied: IAM policy missing S3 actions for the bucket/key
- NoSuchBucket or NoSuchKey: verify names with `list_buckets` / `list_objects`
- `get_object` garbled or failed: object may be binary or too large; use `presigned_url` instead
- Region errors: set `AWS_REGION` to the bucket's region

## Safety

- Always confirm before `delete_object`; S3 deletions are permanent (unless versioning is enabled)
- Always confirm before `put_object` to an existing key; it overwrites without warning
- Presigned URLs grant temporary access to anyone with the link; warn users about this
