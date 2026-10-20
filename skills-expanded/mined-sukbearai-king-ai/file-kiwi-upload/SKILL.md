---
name: file-kiwi-upload
description: "Upload one to ten explicitly selected local files to file.kiwi with its official end-to-end encrypted Node client, return the share link, or resume an interrupted upload. Use when the user asks to transfer concrete local files through file.kiwi. Do not use for directory scanning, browser-session scraping, or uploads that the user has not explicitly confirmed."
---

# File Kiwi Upload

Upload only files the user has named. This workflow sends file contents to an external service and returns a capability URL whose fragment contains the decryption key.

## Canonical Sources

- Public API and limits: `https://file.kiwi/api`
- Official Node client: `https://github.com/file-kiwi/node.git`
- Pinned client package: `@file-kiwi/node@1.0.9`

Prefer the official client over file.kiwi's internal browser endpoints such as `/api/getPresignedUrls` and `/api/registerFileList`. Those endpoints depend on web-app session state and are not the public upload contract.

## Authorization Gate

Before uploading:

1. Obtain exact local file paths. Never search the computer, expand a directory recursively, infer removable-drive contents, or upload a glob that has not been resolved and shown to the user.
2. Run a dry preflight and report the resolved paths, sizes, count, destination (`file.kiwi`), and that the returned URL grants decryption access.
3. Require an explicit confirmation after that disclosure. A general request to create or inspect this skill is not upload authorization. If the user already supplied exact paths and explicitly said to upload them to file.kiwi in the current request, that is sufficient confirmation.
4. Pass `--confirm-external-upload` only after the gate is satisfied.

Do not transmit a file merely to test the skill. Use `--dry-run` for verification.

## Upload

Locate this skill directory, then preflight:

```bash
node <skill-dir>/scripts/upload.mjs --dry-run --title "<optional title>" -- <absolute-file> [<absolute-file> ...]
```

After explicit confirmation, upload the same resolved paths:

```bash
node <skill-dir>/scripts/upload.mjs --confirm-external-upload --title "<optional title>" -- <absolute-file> [<absolute-file> ...]
```

The wrapper:

- accepts only 1-10 readable regular files and rejects directories, empty files, and files above the documented 999 GiB API limit
- pins the official client version instead of following npm `latest`
- forces the official `https://api.file.kiwi` endpoint instead of inheriting an API override from the shell
- uploads one encrypted chunk at a time through the official client
- creates resumable state under `~/.king-ai/file-kiwi-upload` with private permissions
- prints the full share URL on success; treat it as a secret capability link

The npm package may be downloaded on first use. If package integrity or upstream ownership is in doubt, stop before upload and verify `npm view @file-kiwi/node@1.0.9 repository.url dist.integrity --json` against the canonical repository.

## Resume

An interrupted upload may leave `filekiwi.tmp.<folder-id>.json` in the private state directory. This file contains local paths, upload authorization, and the decryption key; never print, commit, or share it.

Inspect only the filename and permissions, then obtain explicit permission to resume the external transfer:

```bash
node <skill-dir>/scripts/upload.mjs --confirm-external-upload --resume <folder-id>
```

Do not invent a folder ID or resume another user's state file. The official client removes the state file after a successful upload.

## Completion Report

Return:

- the share URL directly to the user
- uploaded file basenames and sizes
- whether the upload completed or remains resumable
- the service-reported retention/free-download information when visible

Do not paste the URL into public logs, issues, commits, or pull requests. The `#secretKey` fragment is the only decryption key; losing it makes the encrypted files unrecoverable, while disclosing it grants access to anyone with the link. Treat file.kiwi's encryption, retention, deletion, and privacy statements as vendor claims rather than independently verified guarantees.
