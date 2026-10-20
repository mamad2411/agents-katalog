# Content-search execution boundary

- [routes/search.ts](../routes/search.ts) owns `GET /api/search`: validates the
  project/path via `readPathParam`, floors finite positive limits, accepts regex mode
  as `1` or `true`, and returns an empty result for an empty query without walking.
  Search errors (including invalid regex syntax) become HTTP 400. Cancellation uses
  the response's `close` only while `!res.writableEnded`: a consumed GET request can
  close while its response is pending. The route suppresses replies after disconnect
  and removes its close listener in `finally`.
- [search.ts](../search.ts) is the orchestration/public boundary. Preserve exports
  `searchProjectContents`, `regexSource`, `SearchOptions`, and `SearchResult` and their
  import paths/signatures. It canonicalizes the root, translates/compiles the query
  for syntax validation, defaults the match cap to 2000, tries rg, then collects files
  for `runBoundedJsGrep`. Main-thread compilation does not execute the user pattern.
- [ripgrep.ts](../ripgrep.ts) detects and memoizes optional rg availability;
  `LATTICE_DISABLE_RG=1` disables it and `LATTICE_RG_PATH` supplies the first candidate.
  A child process walks and matches; a failed attempt logs a warning and falls back
  to JS (including regex features rg cannot compile). `RgPathCollector` incrementally
  decodes UTF-8/NUL-delimited paths, retains at most `limit`, and signals the caller
  to kill rg on the next complete match instead of buffering the remaining output.
- [jsGrepWorker.ts](./jsGrepWorker.ts) runs file reads and regex matching in a worker
  thread. Untrusted regex can backtrack indefinitely inside one synchronous `test`;
  keeping it off the backend event loop lets the parent enforce a wall-clock budget
  and terminate it. The default worker budget is 5000 ms, overridden by a positive
  finite `LATTICE_SEARCH_JS_BUDGET_MS`; it does not cover the preceding file collection.
  The worker uses up to 32 concurrent reads, skips files over 2 MiB, unreadable files,
  and files with NUL in the first 8192 bytes. Its inline plain-JS `eval` source avoids
  locating a `.ts`/`.js` worker sibling differently under tsx and compiled `dist`.
  A port listener keeps it alive after `done` until the parent terminates it.

File selection follows the scanner: [collectSourceTree.ts](../scanner/collectSourceTree.ts)
uses `SOURCE_EXTS`; [ignore.ts](../scanner/ignore.ts) combines `IGNORE_DIR_NAMES`, the
root `.gitignore`, and common-gitdir `info/exclude`. The sets live in
[health/constants.ts](../health/constants.ts). rg uses extension/directory globs,
`--hidden`, and `--no-require-git` so `.gitignore` also applies before `git init`.
Keep returned paths absolute and identical to file-node IDs in
[graphAggregate.ts](../scanner/graphAggregate.ts).

Keep `regexSource` wildcard translation aligned with
[frontend filename matcher](../../../frontend/src/components/forceGraph/searchMatcher.ts):
escape regex metacharacters, translate `*` to `.*` and `?` to `.`, and match unanchored,
case-insensitively. Regex mode passes through the raw pattern.

For match caps, both paths need a `limit + 1`th match to establish `truncated`; an
exactly complete result at the cap is not truncated. Worker budget expiry or an
unexpected exit before settlement returns collected partial matches with truncation;
worker errors reject. rg reports `scanned = matches.length`, while a normal worker
result counts eligible files read/tested, including misses. Worker timeout, unexpected
exit, and cancellation use the partial match count for `scanned`.

[constants.ts](./constants.ts) supplies the shared 100 ms `CANCEL_POLL_MS`. Worker
settlement (success, failure, timeout, exit, or cancellation) clears both timers and
terminates the worker. rg cancellation kills the child, drops later output, and
returns empty/untruncated on close; cap termination preserves truncated matches.
rg settlement clears its poll timer as the process exits/fails. JS cancellation
returns partial/untruncated results; the disconnected route discards them.

Regression references: [ReDoS/worker](../__tests__/searchRedos.test.ts), [HTTP cancellation](../__tests__/searchHttpCancellation.test.ts),
[limit parsing](../__tests__/searchLimit.test.ts), [rg collector](../__tests__/ripgrepCollector.test.ts),
[rg early exit](../__tests__/ripgrepEarlyExit.test.ts), [gitignore without a repo](../__tests__/ripgrepGitignoreNoRepo.test.ts).
