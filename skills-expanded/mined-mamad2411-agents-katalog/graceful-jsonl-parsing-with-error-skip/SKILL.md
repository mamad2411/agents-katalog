---
name: graceful-jsonl-parsing-with-error-skip
description: Parse JSONL files gracefully, skipping corrupt lines without failing the whole read
category: data-pipeline
version: 1.0.0
version_origin: extracted
confidence: high
tags: [evolver, data-pipeline, jsonl, resilience]
source_type: extracted-from-git
source_url: https://github.com/EvoMap/evolver.git
source_ref: main
source_commit: 22773782475cecf43dc9c1af264bf5f9cacc28bc
source_project: evolver
source_paths:
  - src/proxy/mailbox/store.js
  - scripts/gep_personality_report.js
imported_at: 2026-04-18T00:00:00Z
---

# Fault-tolerant JSONL reader

Append-only logs inevitably accumulate malformed lines (crash during write, disk full, concurrent truncation). A strict reader breaks observability precisely when you need it. A tolerant reader logs and skips.

## Mechanism

```js
function readJsonl(path, { tailLines = 5000 } = {}) {
  const out = [];
  const lines = fs.readFileSync(path, 'utf8').split(/\r?\n/).slice(-tailLines);
  for (const raw of lines) {
    const line = raw.trim();
    if (!line) continue;
    try { out.push(JSON.parse(line)); }
    catch (e) { console.warn('jsonl parse skip:', e.message); }
  }
  return out;
}
```

- Tail the last N lines so you don't blow memory on huge logs.
- Emit a warn (not error) per skip so partial corruption is visible but non-fatal.

## When to reuse

Event logs, audit trails, message mailboxes, any JSONL store with writes from long-running processes.
