---
name: agent-traffic
description: Classify HTTP traffic as agents, AI crawlers, search crawlers, bots or humans using the agent-traffic dataset. Use when adding agent or bot detection to request handlers, middleware, analytics, server logs or SQL queries, or when someone asks how much of their traffic comes from agents.
---

# Classify agent traffic

[agent-traffic](https://github.com/mintlify/agent-traffic) classifies HTTP requests as agents, AI crawlers, search crawlers, bots or humans. The dataset and rules are already written. Use them for whatever the user asks, whether that's classifying requests, analyzing logs or answering questions about their traffic, without changing what the rules mean.

## Sources

Read these before writing anything:

- [`GUIDELINES.md`](https://github.com/mintlify/agent-traffic/blob/main/GUIDELINES.md) has the categories, decision order and verification rules.
- [`data/agents.json`](https://github.com/mintlify/agent-traffic/blob/main/data/agents.json) lists known agents and crawlers: user agent patterns, `Accept` and `Signature-Agent` fingerprints, verification sources and real example user agents.
- [`data/http-clients.json`](https://github.com/mintlify/agent-traffic/blob/main/data/http-clients.json) lists generic HTTP libraries and headless browsers.

If the package is installed, the same data is at `node_modules/@mintlify/agent-traffic/dist/data/`. Every pattern is a case-insensitive regular expression.

## 1. Find out what's available

Before choosing an approach, look at the user's code or schema and confirm:

- **Where classification can run:** in request-handling code, in an ingest pipeline, or only over stored logs.
- **Which fields exist:** the user agent, the `Accept` header, other request headers, and the client IP. Also check whether that IP is the real client or a proxy or CDN address.
- **What they want out:** a single label, per-agent breakdowns, or verified-only numbers.

Every result needs at least the user agent. The `Accept` header and the real client IP make it much more accurate. If the user can add fields to their logs, recommend logging `Accept` and the real client IP.

## 2. Pick the approach

### JavaScript or TypeScript at request time

Install the package and call `classify` where requests are handled. Don't reimplement the rules.

```
npm i @mintlify/agent-traffic
```

```js
import { classify, loadIpRanges } from '@mintlify/agent-traffic'

let ipRanges

async function classifyRequest(request) {
  ipRanges ??= loadIpRanges()
  return classify({ headers: request.headers, ip: request.headers.get('cf-connecting-ip') }, { ipRanges: await ipRanges })
}
```

- **Use the real client IP.** Take it from the header the user's own proxy sets, such as `CF-Connecting-IP` on Cloudflare or the platform's equivalent. Never use the leftmost `X-Forwarded-For` value, which the client controls. If there's no trustworthy IP, omit `ip`.
- **Only pass `headersComplete: true` when browser headers arrive intact.** That means HTTPS, with no proxy stripping `sec-fetch-*`.
- **Refresh IP ranges about daily** in long-running processes.
- **Store the result** if it feeds analytics: `category`, `kind`, `id` and `verified`.

### Another language at request time

Port `classify` from [`src/classify.ts`](https://github.com/mintlify/agent-traffic/blob/main/src/classify.ts), reading `agents.json` and `http-clients.json` at startup. Keep the check order from GUIDELINES.md exactly:

1. agent patterns in file order;
2. then exact `Accept` fingerprints;
3. then `Signature-Agent` on signed requests only;
4. then markdown-first `Accept`;
5. then HTTP clients;
6. then browser checks;
7. then the fallbacks.

### SQL over stored logs

There are two options. Prefer the first.

**A. Lookup table.** Classify each distinct user agent once with the real package, load the results as a table, and join on it. The output is identical to request-time classification, and there are no regex dialect issues.

```js
import { classify } from '@mintlify/agent-traffic'
const rows = distinctUserAgents.map((ua) => ({ user_agent: ua, ...classify({ userAgent: ua }) }))
```

Write `user_agent, category, kind, id, name, operator` to a table and `JOIN ON user_agent`. Re-run it on a schedule so new user agents and dataset updates get picked up.

**B. Generated `CASE` expression.** Use this when a lookup table isn't practical. Build one `CASE` from the data, with a `WHEN` per pattern in this order: every `agents.json` entry in file order, then every `http-clients.json` entry. Map each match to that entry's `id`, `category` and `kind`. Generate it with a script rather than by hand, and regenerate it when the dataset changes.

Translate patterns for the engine:

| Engine | Match expression | Translation needed |
|---|---|---|
| ClickHouse | `match(ua, '(?i)<pattern>')` | none |
| DuckDB | `regexp_matches(ua, '<pattern>', 'i')` | replace named groups `(?<name>` with `(?:` |
| Postgres | `ua ~* '<pattern>'` | replace `(?<name>` with `(?:`, and `\b` with `\y` (in Postgres, `\b` means backspace) |
| BigQuery, Snowflake, others | check the engine's regex docs | test every pattern; Snowflake has no `\b` or lookarounds |

The first three rows were verified against every example in the dataset. For any other engine, run the test in step 3 before trusting the output.

Results from logs use only the user agent unless the logs also kept `Accept`. Agents that send a browser user agent and ask for markdown will show as `human`; say so in any report you produce. To apply the markdown rule in SQL, classify the request as an `agent` when the `Accept` column ranks `text/markdown` or `text/x-markdown` ahead of `text/html`.

## 3. Test it

Every entry in `agents.json` has real `examples`. Run all of them through the implementation you built. Each must come back with that entry's `id` and `category`. Also check these:

| User agent | Expected |
|---|---|
| `curl/8.7.1` | `bot` / `http-client` |
| `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36` | `human`, or no match in SQL |
| `Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Code/1.109.3 Chrome/142.0.0.0 Electron/39.2.3 Safari/537.36` | not GitHub Copilot |
| `Claude-Code-Docs-Fetcher/3.0` | not Claude Code |

Don't report the work as done until these pass.

## 4. Report the numbers correctly

- **Keep `agent` and `ai-crawler` separate.** Crawlers are scheduled and usually far larger, and combining them hides real agent usage.
- **A markdown fetch by curl, axios or a script is a `bot`, not an agent,** unless it identifies itself or asks for markdown in `Accept`.
- **Don't call unverified identities verified.** With no real client IP, every identity is self-declared.
- **Re-label carefully when replacing an older classification.** If the user already shows an "AI traffic" number that a stricter definition would shrink, offer two numbers instead of shrinking the headline:
  - a broad one: agents, plus AI crawlers, plus automated reads of `.md` and `llms.txt`;
  - a narrow one: just `agent`.

  Explain the difference to the user.

## Don't

- Match bare product words like `Cursor`, `Copilot` or `Code`. Use the anchored patterns from the data.
- IP-check entries marked `"runsOn": "user"`. Those agents run on the user's machine.
- Treat a range-file mismatch as spoofing when the file is older than 180 days, or when the IP isn't a single valid address.
- Copy a pattern list into code by hand. Read it from the dataset so updates flow through.
