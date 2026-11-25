---
name: workspace-archives
description: >-
  Package a deliberate set of local files into a ZIP for agent handoff or list the entries of a ZIP. Use when selected evidence or project files need to be bundled for transfer, a reproducible review packet, or a compact support handoff. The tool does not extract archives, include directories, encrypt data, or inspect file contents for secrets or malware.
---

# Workspace archives

This CLI creates ZIP files from explicit file paths and lists ZIP entry names and compressed sizes. It emits one JSON object to stdout; failures use JSON on stderr and exit code 1.

```sh
node scripts/index.js pack README.md reports/summary.json /tmp/handoff.zip
node scripts/index.js list /tmp/handoff.zip
```

## Pack selected files

Syntax: `pack <file...> <output.zip>`. Provide one or more existing regular files followed by the output path. The archive stores each entry under its basename. Because two different source files with the same basename would overwrite each other inside the ZIP, the command rejects such collisions. Inputs under a path segment named `.git` or `node_modules` are excluded. The archive is compressed and written to the requested path; do not choose an output path that contains private material you do not intend to share.

The command accepts at most 1000 inputs. It does not traverse directories or silently add dependencies, hidden files, or neighboring files. Build an explicit allowlist and inspect it before packing. The file list is not content aware: a selected file can still contain credentials or personal data.

Example response:

```json
{"data":{"output":"/tmp/handoff.zip","files":2,"size":1840}}
```

## List and verify

Syntax: `list <archive.zip>`. It reads the ZIP central directory and returns entry names plus compressed byte sizes. The listing operation does not extract files or validate their decompressed contents. Archives larger than 100 MiB and ZIP64 archives are not supported by the listing command.

```json
{"data":{"input":"/tmp/handoff.zip","files":[{"name":"README.md","compressedSize":720}]}}
```

After packing, list the archive and compare the returned entry names with the allowlist. If recipients need directory structure, this version's basename layout is not suitable; package with a tool that preserves an explicitly reviewed relative path map.

## Operational boundaries

- No extraction command exists, so this tool cannot overwrite files from an untrusted archive.
- It does not encrypt, sign, scan, or redact. Treat the ZIP as sensitive as its most sensitive input.
- It does not call system archive utilities. A malformed ZIP may be rejected during listing; a successful listing proves entry metadata was readable, not that each compressed stream is healthy.

## Handoff workflow

1. Build an explicit list of the minimum files the recipient needs. Include context such as a README or sanitized reproduction instructions when useful.
2. Review selected files for credentials, personal data, proprietary content, and generated artifacts before packing. The CLI does not inspect contents, and compression is not encryption.
3. Choose an output path that will not overwrite a valuable file, pack the allowlist, then list the archive and compare its entries with the intended set.
4. Tell the recipient that entries are stored by basename. If folder structure is necessary, use another packaging method with an explicit path map.

The archive is only a container: it does not make contents safe to share, validate source files, or establish who created or changed them.

## Detailed packaging procedure

### 1. Define the recipient's task

Decide whether the ZIP is for a code review, bug reproduction, support request, or evidence handoff. Include only files needed for that task. A small bundle with a short index is easier to review and less likely to expose unrelated material than an entire workspace.

For a reproduction packet, consider including the relevant source/config, sanitized instructions, and a small synthetic fixture. Exclude credentials, local `.env` files, user databases, caches, dependency trees, generated bundles, and personal data unless each is necessary and explicitly safe to share. The CLI excludes path segments named `.git` and `node_modules`, but that is not a content-aware safety filter.

### 2. Review the allowlist and naming

Provide explicit regular files; directories are not traversed. Every entry is stored by basename, so compare basenames before packing and resolve collisions by selecting or renaming inputs outside the archive workflow. Remember that files from different source directories can collide even when their full paths differ. The command accepts at most 1000 inputs.

Inspect the exact selected list for secrets, proprietary content, licenses, and personal information. Choose an output path outside the input list and avoid overwriting a useful archive. ZIP compression does not encrypt files.

### 3. Pack and verify the manifest

Run `pack <file...> <output.zip>`, then run `list` on the result. Compare every returned entry name to the allowlist and confirm expected files were included. The listed `compressedSize` is not the source size or a content-integrity check. Listing reads the central directory; it does not extract the archive or validate every decompressed byte.

### 4. Handoff with context

Tell the recipient what the archive contains, how entries are named, and any files intentionally omitted. If directory structure or relative paths are required, this CLI's basename-only layout is unsuitable; use a packaging tool with an explicitly reviewed path map. If authenticity or tamper detection is required, use an appropriate signing or checksum process separately.

## Troubleshooting and decisions

- **Basename collision:** choose one file or create reviewed unique filenames before packing; do not rely on archive ordering to resolve duplicates.
- **Directory passed as input:** enumerate the intended files explicitly; no recursive directory mode exists.
- **Entry absent from listing:** compare the source path and basename, confirm it was a regular file, and check exclusions for `.git` or `node_modules` path segments.
- **Archive too large or ZIP64:** the `list` command has a 100 MiB limit and does not support ZIP64. Use a compatible archive inspection tool when the package exceeds those constraints.
- **Untrusted archive:** listing is safer than extraction, but it does not certify that compressed contents are healthy or harmless. Use a separate malware/content inspection process before extracting elsewhere.

## Example manifest note

```text
handoff.zip
- README-repro.md: steps to reproduce, with secrets removed
- src/handler.js: implementation under review
- fixtures/request.json: synthetic request payload
Entries are stored by basename; no environment files or production data were
included. The archive has not been signed or malware-scanned.
```

Only state omissions and checks that are true for the actual bundle.
