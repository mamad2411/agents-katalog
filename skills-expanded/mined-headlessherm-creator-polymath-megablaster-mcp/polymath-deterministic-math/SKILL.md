---
name: polymath-deterministic-math
description: Use when a task needs exact math, date/timezone arithmetic, unit conversion, subnet/IP math, exact string distance, great-circle distance, or GPT token counting — any case where an approximate or guessed numeric answer is unacceptable. Calls the polymath-megablaster-mcp MCP server's tools instead of computing the value from model reasoning. Do NOT use for simple arithmetic you can already verify confidently in one step, or for anything requiring network access, file I/O, or non-deterministic judgment — this skill covers pure, local, deterministic computation only.
license: MIT
metadata:
  category: developer-tools
  requires: polymath-megablaster-mcp (MCP server)
---

# Polymath Deterministic Math

Routes numeric/date/conversion/networking/distance/token-counting work to the `polymath-megablaster-mcp` MCP server instead of computing it from model reasoning. The server is pure local computation (no network calls, no telemetry) — see its own README for the full tool list and setup.

## When to use this skill

Use it when the task involves any of:

- **Exact arithmetic on large numbers** — factorials, permutations, combinations, or any expression where float64 rounding would produce a wrong answer
- **Date/time math** — adding/subtracting dates across leap years or month boundaries, computing business-day differences, converting between IANA timezones
- **Unit conversion** — length, weight, volume, temperature — where an approximated conversion factor would be wrong
- **Statistics** — mean, median, standard deviation, variance, percentiles on a real list of numbers
- **Base conversion** — decimal/hex/binary/octal
- **Networking math** — CIDR subnet calculations, checking whether an IP falls in a private/reserved range
- **Exact string distance** — Levenshtein edit distance or similarity ratio between two strings
- **Great-circle distance** — exact distance between two lat/long coordinates
- **Token counting** — counting GPT tokens in text before sending a large prompt, to manage context budget

**Don't use this skill for:**
- Arithmetic simple enough to state with full confidence in one step (e.g. `12 * 4`)
- Anything requiring network access, file reads, or external data — polymath's tools are pure computation on the inputs you give them
- Approximate/subjective judgments (this skill is specifically for cases where guessing is unacceptable)

## Prerequisites

The `polymath-megablaster-mcp` MCP server must be configured in the calling client. See https://github.com/headlessherm-creator/polymath-megablaster-mcp for setup — in short:

```bash
git clone https://github.com/headlessherm-creator/polymath-megablaster-mcp.git
cd polymath-megablaster-mcp
npm install
```

Then point your MCP client config at `src/index.js` (Node.js v18+). If the server isn't configured, tell the user it's required rather than attempting to approximate the answer yourself.

## Procedure

1. **Identify which category the task falls under** (see "When to use" above).
2. **Call the matching polymath tool** rather than computing the value yourself:
   - `calculate`, `factorial`, `permutations`, `combinations`, `compute_statistics` — exact math
   - `date_add`, `date_diff`, `convert_timezone` — date/time
   - `convert_unit`, `convert_base` — conversion
   - `calc_subnet`, `check_ip_type` — networking
   - `levenshtein_distance` — text
   - `haversine_distance` — geo
   - `count_tokens` — agent utility
3. **Pass the tool's result through directly** — do not re-derive or "sanity check" the exact value with your own mental math; the tool exists specifically because that step is unreliable.
4. **If the MCP server isn't available**, say so explicitly rather than silently falling back to approximate reasoning — the whole point of this skill is avoiding a guessed answer in exactly this situation.

## Pitfalls

- Polymath has no network access by design — don't expect it to fetch live data (current exchange rates, live timezone-rule changes, etc.); it only computes on the inputs you give it.
- A paid "Pro" tier exists for 4 additional tools (`hmac_text`, `compare_semver`, `aes_encrypt`, `aes_decrypt`) — not covered by this skill's trigger list; the 15 free tools above are what this skill routes to.

## Verification

- The tool call returns a value; confirm it was actually invoked (not skipped) before presenting the number as exact.
- If a computation could plausibly use more than one polymath tool (e.g. a date-math problem that also needs timezone conversion), chain the calls rather than picking one and approximating the rest.
