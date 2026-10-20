---
name: error-message
description: Sanook writes and audits user-facing error and exception messages so they state what failed, why, and the next action — actionable, specific, non-blaming, no leaked internals — applying a consistent voice across CLI/API/UI.
when_to_use: User asks to improve error/exception/validation/toast messages, write copy for failure states, or audit messages for clarity; designing error handling for a CLI/API/form.
---

## When to Use

- Writing or rewriting a single error/exception/validation/toast string.
- Designing error handling for a new CLI command, API endpoint, or form.
- Auditing an existing codebase for vague or leaky failure messages.

Skip if the message is a developer-only debug log never shown to a user — those can stay verbose.

## Steps

Every user-facing message must answer three questions in order: **what failed → why → what to do next**. If a message is missing the "next step", it is not done.

1. **Classify the failure first.** Pick the channel before writing words, because it sets length and tone:
   - `validation` (user input, recoverable) → short, points at the exact field/arg, names the valid format. No error code.
   - `operational` (network/timeout/permission/rate-limit) → state the cause + a retry or fix path. Include a code/correlation id.
   - `fatal` (bug, corrupt state, unhandled) → apologize once, give code + correlation id + where to report. Never dump the stack to the user.

2. **Write the three parts explicitly.** Template: `<what failed in plain terms>. <why / which input>. <imperative next action>.`
   - Bad: `Invalid input`
   - Good: `Config file not found at ./app.config.json. Create it or pass --config <path>.`
   - For CLI, the next action is usually a concrete command or flag. For forms, it is the corrected format. For API, it is the field path plus the allowed value/range.

3. **Strip blame and jargon.** Replace `you entered an illegal value` → `Value must be between 1 and 100`. Drop "illegal/invalid/bad" as the only descriptor; say what *would* be valid. Never imply user fault for system failures (`you broke X` → `X is unavailable`).

4. **Remove internal leakage from anything user-visible.** No raw stack traces, no file paths under home/build dirs, no SQL, no internal class/module names, no secrets/tokens/connection strings, no `undefined`/`null`/`[object Object]`. Route those to the log; show the user a code that maps back to the log entry. Format: `Something went wrong (E_UPLOAD_502, ref a1b2c3). Check logs or report with this ref.`

5. **Match exit/status to severity** so machines and humans agree: CLI non-zero exit + stderr for failures, never stderr-with-exit-0. API: 4xx for caller fixable, 5xx for server fault; put a stable `code` field in the body, not just an HTTP status. Don't return 200 with `{"error": ...}`.

6. **Keep one voice.** Decide person and mood once (recommended: imperative, second-or-no person, present tense, no exclamation marks, no emoji unless the UI's design system already uses them) and apply it to every message. Sentence case, end with a period; no trailing "please".

7. **Audit mode** (when scanning a codebase):
   - Find sites: `rg -n "throw |raise |console\.(error|warn)|res\.status\([45]|reject\(|panic|abort\(" --type-add 'src:*.{ts,tsx,js,py,go,rs}' -tsrc`
   - Find vague/leaky strings: `rg -niE "something went wrong|unknown error|invalid|failed|oops|error occurred|undefined|null|\[object" -tsrc`
   - For each hit: flag if it is missing what/why/next, blames the user, or leaks internals → propose a rewrite inline using the Step 2 template. Group by file. Don't rewrite logger-only calls.

## Common Errors

- **"Next step" gets dropped under pressure.** A message that only says what failed (`Connection refused`) is half-done. Always append the action (`Connection refused. Is the server running on port 5432? Set DB_HOST to override.`).
- **Catch block re-leaks the cause.** `catch (e) { showUser(e.message) }` defeats the whole skill — `e.message` is often a driver/stack string. Map exceptions to curated user messages; log the raw `e` separately.
- **Validation that hides which field failed.** `Invalid request body` forces the caller to guess. Name the path: `body.email must be a valid email address`.
- **Severity/channel mismatch.** A recoverable validation error written as a scary fatal ("FATAL: aborting"), or a real crash swallowed into a friendly toast with exit 0. Tone and exit code must match the class from Step 1.
- **Localized/duplicated strings drift.** If the same error exists in multiple languages or layers (API + UI), changing one and not the other reintroduces the bad copy. Find duplicates before rewriting.
- **Correlation id printed but never logged.** A ref code the user can quote is useless if it isn't also written to the log. Verify both sides exist.
- **Over-apologizing.** "We are so sorry, oops!" on a routine validation error reads as noise. Reserve apology for fatal/server faults, once.

## Verify

- Pick 3–5 rewritten messages: each answers what + why + next, names a concrete field/command, and contains zero internal identifiers or stack text.
- Trigger a real failure (bad input, killed dependency) and read the *actual* rendered output, not the source string — confirm no `undefined`/path/stack leaked through interpolation.
- CLI: failure path returns non-zero exit and writes to stderr. API: 4xx/5xx matches fault owner and body carries a stable `code`.
- For fatal-class messages, confirm the ref/correlation id shown to the user also appears in the log.
- Audit output lists every flagged site with a proposed rewrite; no logger-only call was rewritten by mistake.
