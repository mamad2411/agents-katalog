---
name: stream-json-line-buffer-across-chunks
description: When spawning a CLI that emits stream-json (one JSON per newline), buffer stdout across 'data' events and only parse on newline to avoid losing records that straddle pipe-buffer boundaries.
category: backend
triggers:
  - stream-json
  - spawn stdout buffering
  - child_process line splitter
  - large JSON event dropped
tags:
  - nodejs
  - ipc
  - pipe-buffer
version: 1.0.0
---

# stream-json-line-buffer-across-chunks

Pitfall: `child.stdout.on('data', d => d.toString().split('\n').forEach(parse))` drops content that spans two chunks. Node's pipe buffer is 64 KB on most platforms, so large `result` events from `claude -p --output-format stream-json --verbose` (tens of KB with usage + total_cost_usd) get split arbitrarily, and both halves fail `JSON.parse`. Cost/usage accounting silently disappears.

## Pattern

Accumulate a residual string across events. Emit only complete newline-terminated lines. Flush any remainder on `close`.

```js
let stdoutBuf = '';
child.stdout.on('data', (d) => {
  stdoutBuf += d.toString();
  let nl;
  while ((nl = stdoutBuf.indexOf('\n')) !== -1) {
    const line = stdoutBuf.slice(0, nl);
    stdoutBuf = stdoutBuf.slice(nl + 1);
    handleStreamLine(line);
  }
});
child.on('close', () => {
  if (stdoutBuf) { handleStreamLine(stdoutBuf); stdoutBuf = ''; }
});
```

## Why not readline?

`readline.createInterface({ input: child.stdout })` also works and handles CRLF, but it introduces an extra EventEmitter and can't easily share parse state with other listeners. A ~10-line inline buffer is lighter and reveals the split in diffs.

## When to reach for it

Any `spawn`/`exec` where the child emits newline-delimited JSON (NDJSON/JSONL): LLM CLIs, `jq --stream`, log shippers, protobuf-json bridges. If you see intermittent missing records under load, check for chunk-boundary loss first — it's almost always this.
