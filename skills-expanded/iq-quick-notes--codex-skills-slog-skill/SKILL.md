---
name: slog
description: Structured logging workflow for debugging code paths with per-run log files in `.context/slog`. Use when the user says "use slog", asks for structured logging, wants you to instrument a flow, run it, and inspect logs. Triggers on requests like "use slog", "add structured logs", "log this flow", or "debug with slog".
---

# Structured Logging with slog

Use this skill to debug or verify a concrete code path by writing newline-delimited JSON logs to a run-specific file in `.context/slog`, exercising the path, and then reading the output.

In this repo, treat `slog` as a default self-verification tool:

- Use it when fixing bugs.
- Use it when building new features.
- Use it during planning when you need to verify your understanding of the current runtime path before making changes.
- Prefer it whenever the task depends on what the code actually does at runtime, not just what it appears to do from static reading.

## Default workflow

1. Create a fresh run file. Do not reuse the previous file.

```bash
bun .codex/skills/slog/scripts/slog.ts new signup-before-fix
```

2. The helper also writes `.context/slog/current.env`. In this repo, the local dev scripts source that file automatically via `scripts/load-worktree-env.sh`, so a normal restart of `web`, `trigger`, `hocuspocus`, `admin`, or `desktop` is enough to pick up the new slog target.
3. Use the printed `THOUGHTFUL_SLOG_FILE`, `THOUGHTFUL_SLOG_RUN_ID`, and `THOUGHTFUL_SLOG_LABEL` values only for one-shot commands that do not go through the shared dev scripts.
4. Add focused structured logs near decisions, boundaries, and surprising state changes.
5. Trigger the code path yourself when possible.
6. Read the log file and summarize what changed.
7. For the next run, mint a new file name again instead of appending to the previous run.

This is the default verification loop:

1. Form a hypothesis about the current behavior or the behavior you expect after a change.
2. Mint a fresh slog run.
3. Add focused logs around the branch or boundary that should prove or disprove that hypothesis.
4. Exercise the real path.
5. Read the slog file and confirm what happened.

## Per-run file naming

The helper script creates files like:

```text
.context/slog/20260402T193501Z-a1b2c3d-dirty-signup-before-fix.jsonl
```

The name captures:

- Timestamp
- Current git SHA
- Dirty/clean state
- Human label for the run

This makes it easy to compare log output across code changes.

## Standard log shape

Use JSONL. Write one JSON object per line with stable keys.

```json
{
  "ts": "2026-04-02T19:35:01.123Z",
  "runId": "20260402T193501Z-a1b2c3d-dirty-signup-before-fix",
  "source": "apps/web/src/server/example.ts",
  "event": "signup.user-created",
  "step": "after-insert",
  "data": {
    "userId": "123",
    "workspaceId": "456"
  }
}
```

Rules:

- Keep keys stable across runs so diffs are meaningful.
- Prefer small scalar fields and shallow objects.
- Do not log secrets, tokens, cookies, raw auth headers, or full request bodies unless the user explicitly asks and the data is safe.
- Include IDs, counts, branch decisions, and error summaries.

## TypeScript helper pattern

Use a small local helper when the code path does not already have one:

```ts
import fs from "node:fs";
import path from "node:path";

function appendSlog(
  source: string,
  event: string,
  data: Record<string, unknown> = {},
  step?: string,
): void {
  const file = process.env.THOUGHTFUL_SLOG_FILE;
  if (!file) return;

  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.appendFileSync(
    file,
    JSON.stringify({
      ts: new Date().toISOString(),
      runId: process.env.THOUGHTFUL_SLOG_RUN_ID ?? "manual",
      source,
      event,
      step,
      data,
    }) + "\n",
  );
}
```

Guidance:

- Prefer adding logs at system boundaries: request entry, parsed input, DB read/write result, branch selection, downstream call, returned output, caught error.
- If the code already uses a logger, keep it. Add file logging alongside it only for the investigation.
- Default to removing temporary instrumentation after the debugging session unless the user wants to keep it.

## Triggering the code path

After instrumenting, try to run the code path yourself.

Preferred order:

1. Existing unit or integration test
2. Small targeted script
3. Existing CLI command
4. Local HTTP request
5. Browser flow using `agent-browser`

If you cannot trigger it directly, give the user exact steps:

1. The command to create a fresh slog run
2. Whether the relevant service needs a restart to pick up `.context/slog/current.env`
3. The exact action to perform manually
4. The command to read the log file afterward

## Reading logs

Use the helper to recover the latest run:

```bash
bun .codex/skills/slog/scripts/slog.ts latest
bun .codex/skills/slog/scripts/slog.ts latest file
bun .codex/skills/slog/scripts/slog.ts list
```

Useful follow-up commands:

```bash
tail -n 200 "$(bun .codex/skills/slog/scripts/slog.ts latest file)"
jq -c . "$(bun .codex/skills/slog/scripts/slog.ts latest file)"
rg '"event"' "$(bun .codex/skills/slog/scripts/slog.ts latest file)"
```

## Comparing runs

When behavior changes between edits:

1. Create a new run file with a label that captures the hypothesis, such as `before-null-guard` or `after-parse-fix`.
2. Keep the old file.
3. Compare the normalized outputs.

Example:

```bash
jq -S . .context/slog/20260402T193501Z-a1b2c3d-dirty-before-null-guard.jsonl > /tmp/run-a.jsonl
jq -S . .context/slog/20260402T194122Z-e4f5g6h-dirty-after-null-guard.jsonl > /tmp/run-b.jsonl
diff -u /tmp/run-a.jsonl /tmp/run-b.jsonl
```

## Completion standard

Do not stop after adding logs. The full `slog` workflow is:

1. Create a new run file
2. Instrument the code path
3. Run the path if possible
4. Read the file
5. Explain what the logs say

If step 3 is impossible in the current environment, explicitly say what the user needs to do manually.
