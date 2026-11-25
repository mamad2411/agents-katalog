---
name: secure-file-upload
description: Hardens upload endpoints by checking type, size, name and storage location, blocking path traversal, executable content and image bombs.
---

# Secure file upload

Never trust the filename, the extension or the Content-Type header from the client.

## Steps

1. Find every upload handler (multipart parsers, presigned URL generators, import jobs) and follow a file from request to final location and later download.
2. Size: set a hard limit at the parser and at the proxy, and stream to storage instead of reading the whole file into memory. Limit the number of files per request.
3. Type: allow a short list of extensions, then verify the content with magic bytes (file signature) or a library, and make sure both agree. For images, re-encode with a trusted library; this strips embedded scripts and metadata, and caps pixel dimensions to stop decompression bombs.
4. Name: discard the original name. Generate a random one (UUID) and keep the original only as display metadata, escaped on output. Reject names with `..`, slashes, null bytes or reserved Windows names.
5. Location: store outside the web root, or in object storage with a private bucket. Resolve the final path and confirm it starts with the base directory. Never write with execute permission.
6. Serving: send `Content-Disposition: attachment` for non-images, set `X-Content-Type-Options: nosniff`, and use a separate domain for user files where possible. Check authorization on download.
7. Archives: when unzipping, check each entry path against the destination and cap total expanded size.
8. Consider malware scanning for files shared between users.

## Rules

- A blocklist of "bad extensions" is not a defence.
- Add tests: a `.php` file renamed `.jpg`, `../../x` as the name, an oversized file, an empty file.

## Report

Handlers reviewed, issues fixed with `path:line`, limits chosen, and tests added.
