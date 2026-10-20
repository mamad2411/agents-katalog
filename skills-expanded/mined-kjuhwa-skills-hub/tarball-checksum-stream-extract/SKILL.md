---
name: tarball-checksum-stream-extract
description: Stream-download a .tar.gz with SHA-256 verification before extraction using the tarfile data filter for path-traversal safety.
category: devops
version: 1.0.0
version_origin: extracted
tags: [downloads, security, tarfile, checksum, httpx]
source_type: extracted-from-git
source_url: https://github.com/jamiepine/voicebox.git
source_ref: main
source_commit: 476abe07fc2c1587f4b3e3916134018ebacd143d
source_project: voicebox
confidence: high
imported_at: 2026-04-18T00:00:00Z
---

# Tarball checksum stream-extract

## When to use
An app downloads upgrade archives (models, plugin bundles, runtime libraries) from a release host and must never extract an unverified or tampered tarball onto user disks.

## Steps
1. Fetch the expected SHA-256 **first**, from a sibling `.sha256` file at the same URL. Fail fast if the checksum fetch errors — it's non-optional. The `.sha256` format is `<hex>  <filename>\n`; split on whitespace and keep index 0.
2. Stream the archive to a sibling temp file (`.download-<label>.tmp`) under the final destination directory, not `/tmp`. Being on the same volume makes the final move atomic and avoids cross-filesystem failures.
3. Use a chunked stream (`async for chunk in response.aiter_bytes(chunk_size=1 MB)`) and push a progress update after every chunk. Compute a running SHA only if you want a single pass — otherwise hash after download completes.
4. After download, verify the SHA by streaming the temp file through `hashlib.sha256()` with 1 MB reads. Compare hex digests; on mismatch, raise a clear `ValueError` — don't try to repair.
5. Extract with `tarfile.open(temp, "r:gz")`. On Python 3.12+, use `tar.extractall(path=dest_dir, filter="data")`. The `data` filter strips setuid/setgid, refuses absolute paths and symlink escapes, and blocks the classic path-traversal attack.
6. Always clean up the temp file in a `finally` so a verification failure doesn't leave a partial archive on disk.
7. Write a JSON manifest (`cuda-libs.json`, `plugins.json`, etc.) after successful extraction so the next startup knows what version is installed without re-scanning the directory.

## Counter / Caveats
- Never skip the checksum fetch "because the download link is HTTPS". TLS protects transport, not integrity of the origin blob.
- Avoid `tarfile.extractall` without a filter on untrusted input — CVE-2007-4559 is still shipping wild in 2024.
- Under concurrency, guard the whole download with an `asyncio.Lock` (or a named mutex) so two callers don't race on the temp file.
- If you support resume, name the temp file based on the content hash rather than a fixed label — otherwise two different versions in flight will collide.

Source references: `backend/services/cuda.py` (`_download_and_extract_archive`, `download_cuda_binary`).
