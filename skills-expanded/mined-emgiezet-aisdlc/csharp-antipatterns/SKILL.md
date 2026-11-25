---
name: csharp-antipatterns
description: Forbidden C# patterns — SQL injection, BinaryFormatter, weak random, async void, exception swallowing. Applies when editing C# files.
paths: ["**/*.cs"]
user-invocable: false
---

# C# anti-patterns — do not write these

Checks run automatically after each edit. Findings reference the IDs below.

## Blockers
- AP-CS-SEC-001 — Use `SqlCommand` parameters or EF parameterized queries; never interpolate into `CommandText`.
- AP-CS-SEC-002 — Replace `BinaryFormatter`/`NetDataContractSerializer` with `System.Text.Json` or MessagePack.
- AP-CS-SEC-003 — Set `ProcessStartInfo.Arguments` separately; never embed user input in the FileName.
- AP-CS-SEC-004 — Use `RandomNumberGenerator.GetBytes` for tokens; `System.Random` is for simulations only.

## Errors
- AP-CS-PERF-001 — Use `async Task` (not `async void`) for all async methods except event handlers.
- AP-CS-MAINT-001 — Catch the specific exception type; log and rethrow; never swallow `Exception` silently.

## Warnings
- AP-CS-SEC-005 — Add `NWebsec` or a custom middleware to set CSP, X-Frame-Options, and HSTS.
- AP-CS-MAINT-002 — Use `StringBuilder` or `string.Join` to concatenate strings in loops.

Details for any ID: `reference/<ID>.md`
