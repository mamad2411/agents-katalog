---
name: file-stability-polling-for-fs-flush
description: Poll stat size every 100ms and only treat a file as "ready" after 3 consecutive unchanged readings — bridges the gap between bundler exit and OS filesystem flush on Windows / network volumes.
category: build
version: 1.0.0
version_origin: extracted
tags: [filesystem, flush, windows, build-tooling]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: scripts/electron-build-main.ts
imported_at: 2026-04-18T00:00:00Z
---

# File-stability polling before consuming a freshly built file

## When to use
- A build step writes a large output file and immediately another step (launch, verify, archive) reads it.
- On Windows / SMB / slow disks you see intermittent "file is zero bytes" or "truncated" errors.
- You can't force-sync from inside the bundler; you control only the caller.

## How it works
1. Poll `fs.statSync(path).size` every 100ms.
2. Maintain a `stableCount` - incremented when the size matches the previous reading, reset to 0 when it changes.
3. Return "ready" only after 3 consecutive unchanged readings (~300ms of silence).
4. Give up after `timeoutMs` (10s default); caller decides what to do.
5. Also guard against missing file (bundler may not have created it yet) - keep polling.

## Example
```ts
async function waitForFileStable(filePath: string, timeoutMs = 10_000): Promise<boolean> {
  const start = Date.now();
  let lastSize = -1, stableCount = 0;
  while (Date.now() - start < timeoutMs) {
    if (!existsSync(filePath)) { await Bun.sleep(100); continue; }
    const size = statSync(filePath).size;
    if (size === lastSize) {
      if (++stableCount >= 3) return true;
    } else {
      stableCount = 0; lastSize = size;
    }
    await Bun.sleep(100);
  }
  return false;
}
```

## Gotchas
- 3 consecutive readings is a heuristic - tune for your disk. Some network volumes buffer up to 1s.
- Doesn't detect *corruption*, only partial writes. Add `node --check`-style validation after stability for defense-in-depth.
- On Linux with local SSDs this is usually unnecessary - but the paranoid cross-platform build stays this way to avoid flaky CI.
- If multiple writers target the same file, stability polling is racy; use atomic rename (`tmp` -> `final`) instead.
