---
name: wreck-trace
description: Trace wreck-it findings to the source code responsible. It maps the route or API endpoint to its handler, follows stack frames, greps for UI strings, reads the code and writes file, line, snippet, why and confidence onto each finding. Never guesses a line. Use as stage 9 of a wreck-it run, or when the user asks "where is this bug in my code" for a wreck-it finding.
---

# wreck-trace

`WRECK` means `npx @miyanishar/wreck-it`.

`WRECK run stage trace running`

Work through `WRECK finding list --json`. Trace every **reproduced** finding that has no `source`, in severity order. Trace unreproduced findings too if time allows.

## Method (per finding)

1. **Start from evidence.**
   - **Console stack trace:** take the top frame inside the project, not inside `node_modules`. In dev builds the file paths are usually real. With bundled paths (`/_next/static/chunks/…`), use source maps if they exist (`.next/**/*.map`, `dist/**/*.map`). Otherwise fall back to grep.
   - **Failing request:** match `evidence.network[].url` against `discovery.json` `api[]` (method and path, where `[id]` matches any segment) to get the handler `file`.
   - **Route:** match against `discovery.json` `pages[]` to get the page file, then follow its imports to the components that render the broken element.
2. **Grep for anchors.** Search the source, excluding `node_modules`, `.next`, `dist`, `build`, for:
   - text visible near the bug: button names, labels, headings
   - the `testId`/label values in `steps`
   - API paths
   - error messages from the console

   Example: `grep -rn "Place order" src app components --include=*.tsx`
3. **Read the code** from where the data comes in to where it goes wrong, and find the faulty line. The faulty line is the one that, if changed, fixes the bug, not just the first line you landed on.
   - A wrong total points at the arithmetic.
   - A 500 points at the unguarded call.
   - A duplicate order points at the missing idempotency or disabled-state check.
   - An N+1 points at the query inside the loop.
4. **Write `source`** with `WRECK finding update WR-007 '<json>'`:
```json
{"source": {
  "file": "app/api/coupon/route.ts", "line": 14,
  "snippet": "const code = coupons[body.code].code.toUpperCase();",
  "why": "Lookup uses the raw input with spaces; coupons[\" SAVE10 \"] is undefined, so .code throws → 500. Trim/normalize before lookup and handle unknown codes.",
  "confidence": "high"
}}
```
   - `file` is relative to the project root, and `line` is 1-based and points at the faulty line.
   - `snippet` is that line, or 1–3 lines around it, copied verbatim.
   - `why` explains the mechanism (input → faulty line → symptom) and hints at the fix in one clause.

## Confidence rules (enforced by the CLI)

- **high:** you read the code and the mechanism fully explains the symptom.
- **medium:** the right file and a very likely line, but one link is unverified (e.g., you couldn't confirm the data shape).
- **low:** you can't pin a line. Give **no `line`** and list 1–5 `candidates` (`"file:line?"` or `"file"`) with a `why` describing what you checked. Never guess a line to look confident.

## Finish

`WRECK run stage trace done`

List any findings you left at low confidence and why.
