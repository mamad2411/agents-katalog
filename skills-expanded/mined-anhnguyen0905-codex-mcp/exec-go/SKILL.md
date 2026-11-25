---
name: exec-go
description: Go execution idioms to embed into Codex prompts when the target project is Go — error handling, concurrency discipline, and standard project conventions.
---

# Go Idioms (embed when project is Go)

```
Go standards:
- Errors are values: check every err; wrap with context (`fmt.Errorf("doing x: %w", err)`);
  no panic in library code — reserve it for truly unrecoverable programmer errors.
- Accept interfaces, return concrete types; keep interfaces small and defined where consumed.
- Concurrency: every goroutine has a clear owner and exit path (context cancellation, closed
  channel, WaitGroup) — no fire-and-forget leaks; guard shared state with mutex or channels,
  never both ad hoc; pass context.Context as the first parameter through call chains.
- Zero values matter: design structs whose zero value is usable, or provide a constructor.
- defer for cleanup immediately after acquiring the resource.
- Follow gofmt (non-negotiable), golangci-lint if configured, and standard layout the repo
  already uses (cmd/, internal/, pkg/).
- Naming: short receiver names, MixedCaps not underscores, exported identifiers documented with
  a leading-name comment.
- Tests: table-driven with subtests (t.Run), t.Helper() in helpers; use the repo's assertion
  style (stdlib vs testify) — don't introduce a new one.
```
