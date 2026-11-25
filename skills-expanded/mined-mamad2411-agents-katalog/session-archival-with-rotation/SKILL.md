---
name: session-archival-with-rotation
description: Archive old sessions when count exceeds threshold, keep N most recent
category: data-pipeline
version: 1.0.0
version_origin: extracted
confidence: medium
tags: [evolver, data-pipeline, rotation, retention]
source_type: extracted-from-git
source_url: https://github.com/EvoMap/evolver.git
source_ref: main
source_commit: 22773782475cecf43dc9c1af264bf5f9cacc28bc
source_project: evolver
source_paths:
  - src/evolve.js
imported_at: 2026-04-18T00:00:00Z
---

# Count-based session rotation

When the live session directory exceeds a trigger (e.g., 100 files), move the oldest down to an `archive/` sibling until only the newest N remain (e.g., 50). Preserves original filenames for traceability and keeps the hot directory small so directory listings stay fast.

## Mechanism

```js
function rotateSessions({ dir, archive, trigger, keep }) {
  const files = fs.readdirSync(dir)
    .map(f => ({ f, mtime: fs.statSync(path.join(dir, f)).mtimeMs }))
    .sort((a, b) => a.mtime - b.mtime);
  if (files.length <= trigger) return;
  fs.mkdirSync(archive, { recursive: true });
  for (const { f } of files.slice(0, files.length - keep)) {
    fs.renameSync(path.join(dir, f), path.join(archive, f));
  }
}
```

## When to reuse

Conversation logs, session transcripts, per-run artifact trees — anywhere a unbounded working set would slow listing or indexing.
