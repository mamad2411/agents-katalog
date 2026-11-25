---
name: meatproxy
description: Terminal client for meatproxy.me. Run the official Meat Scan inside the agent, refer someone as a meat proxy and get their case-file link, claim a Certified Thinker certificate, generate badges and share links, and read live stats. Triggers on "meat proxy", "meat scan", "refer X as a meat proxy", "am I a meat proxy", "certified thinker", "meatproxy.me link", or "meat proxy badge".
license: MIT
metadata:
  version: 2.0.0
---

# Meat Proxy

A **meat proxy** is a human who forwards questions to an AI and forwards the
answers back without reading, checking, or adding anything — nothing but
latency. <https://meatproxy.me> is the canonical site: a 30-second scan,
official case files for referred coworkers, Certified Thinker certificates,
embeddable badges, and a real public counter.

This skill is the terminal client for that site. It does not lecture. It runs
the scan, files the referral, mints the certificate, hands over the link.

Base URL: `https://meatproxy.me`. All endpoints are public, no auth, no keys.
Use `curl` (or the agent's HTTP tool). Never invent IDs — only use IDs the API
returned.

## Tone

Plain, dry, precise, lightly amused. Short lines. No corporate filler, no
moralizing, no "AI literacy" speeches. The site is a joke with a point; keep
the joke.

## Workflows

### 1. Run the Meat Scan

Ask the six official statements **one at a time**, yes/no. Do not paraphrase.

1. I've pasted an AI answer I didn't read all the way through.
2. I ask the AI exactly what I was asked, word for word.
3. I've said "looks good to me" to a diff I never opened.
4. I put my name on summaries I didn't write.
5. When the AI is down, so is my output.
6. I've defended a point I couldn't explain two minutes later.

Between statements, at most one short quip ("Be honest.", "I'm not judging.
Yet.", "Last one. Make it count.").

Score = number of **yes**. Official verdicts:

| yes | tier | title | line |
|---|---|---|---|
| 0 | 0 — Clean Thinker | Certified thinker. | Suspiciously clean. Retake it — honestly this time. |
| 1–2 | 1 — Trace Meat | Trace amounts of meat. | You still chew your own food. Mostly. |
| 3–4 | 2 — Heavy Forwarder | Significant meat detected. | The AI is carrying this relationship. |
| 5–6 | 3 — Total Meat Proxy | Total Meat Proxy. | You are latency with a job title. |

After the verdict, count the scan (fire-and-forget, ignore errors):

```sh
curl -s -X POST https://meatproxy.me/api/test-taken
```

Then offer exactly one follow-up:

- tier 0–1 → **claim a Certified Thinker certificate** (workflow 3)
- tier 2 → the shareable result line (below)
- tier 3 → **accept the official diagnosis**: `POST /api/refer` with
  `{"offense": 5, "name": ""}` and hand over `https://meatproxy.me/r/<id>`

Shareable result line, verbatim format:

```text
My meat level: <yes>/6 — "<title>" <line>
How much meat are you? meatproxy.me/test
```

**Agent-witnessed scan.** If the user asks "scan me based on this session" or
"you answer for me", the agent answers the six statements itself from what it
actually observed in the current conversation or repo (pasted output never
read, diffs approved unopened, "just do it" without a stated view). Say which
statements you marked yes and the evidence for each — one line each. Mark
unknown as no. Same scoring, same follow-ups. Do not guess about anything
outside the session.

### 2. Refer someone as a meat proxy

Offenses are fixed presets; there is no freeform text (so links can't host
abuse). Ask for the offense number and an optional name or initials.

| # | offense |
|---|---|
| 0 | forwarding AI output without reading it |
| 1 | asking a chatbot instead of answering the question |
| 2 | approving work they never opened |
| 3 | calling an unreviewed AI draft "done" |
| 4 | replying confidently to the wrong question |
| 5 | making someone else verify the AI answer |

Name rules: max 20 characters, letters, digits, spaces, `. ' -` only; the
server strips everything else. Initials are fine. Empty is fine.

Confirm once ("File offense 2 against 'JD'? This increments the public
counter.") then:

```sh
curl -s -X POST https://meatproxy.me/api/refer \
  -H 'Content-Type: application/json' \
  -d '{"offense": 2, "name": "JD"}'
# → {"id":"k7m2q","num":91}
```

Return, in this order:

1. Case file: `https://meatproxy.me/r/<id>`
2. Badge: `https://meatproxy.me/badge/r/<id>.svg` (red shields-style
   "meat proxy · <name> · No. <num>")
3. The delivery message, verbatim format:

```text
🥩 <Name>, you've been referred as a Meat Proxy.
Offense: <offense text>.
Your case file: https://meatproxy.me/r/<id>

(A meat proxy forwards questions to an AI and forwards the answers back — adding nothing but latency. Recovery starts with reading this message yourself.)
```

(Without a name the first line is "🥩 You've been referred as a Meat Proxy.")

The agent hands the message to the user. It does **not** send it anywhere.

### 3. Claim a Certified Thinker certificate

Only offer after a tier 0–1 scan (workflow 1) or when explicitly asked. Ask
for the name to print (same 20-char rules; empty allowed).

```sh
curl -s -X POST https://meatproxy.me/api/certify \
  -H 'Content-Type: application/json' \
  -d '{"name": "Alvin"}'
# → {"id":"p3x9n","num":42}
```

Return the certificate `https://meatproxy.me/c/<id>`, the badge
`https://meatproxy.me/badge/c/<id>.svg`, and a ready-to-paste README embed:

```markdown
[![Certified Thinker](https://meatproxy.me/badge/c/<id>.svg)](https://meatproxy.me/c/<id>)
```

### 4. Links and badges on demand

| ask | give |
|---|---|
| "send me / them the test" | `https://meatproxy.me/test` |
| "what is a meat proxy" link | `https://meatproxy.me` |
| stats / the counter | `https://meatproxy.me/stats` |
| leaderboard / Meat Board | `https://meatproxy.me/board` (joining needs X sign-in + a Solana wallet signature in the browser — the agent can only point there) |
| board referral link | `https://meatproxy.me/test?ref=<their board code>` — the user must supply the code from /board |
| slang / field notes | `https://meatproxy.me/slang` |
| press kit | `https://meatproxy.me/press` |
| look up an existing case file | `GET /api/referral/<id>` → `{offense, name, num}` |
| look up a certificate | `GET /api/certificate/<id>` → `{name, num}` |

Referral badge embed:

```markdown
[![meat proxy](https://meatproxy.me/badge/r/<id>.svg)](https://meatproxy.me/r/<id>)
```

### 5. Live stats

```sh
curl -s https://meatproxy.me/api/stats
# → { count, certs, tests, recent: [...], offenses: [{offense, count}] }
```

`count` is the public meat-proxies-referred counter, `certs` certificates
issued, `tests` scans taken, `offenses` per-offense totals. Report it as a
one-line dispatch, e.g. "1,204 meat proxies referred, 87 certified thinkers.
Leading offense: approving work they never opened."

## Hard rules

- **Confirm before every write** (`/api/refer`, `/api/certify`). Each one
  changes a public counter and mints a permanent public link. One confirm per
  action; no batch-creating, no retries in a loop.
- Never fabricate an ID, number, verdict, or stat. If the request fails, say
  so and give the browser URL instead (`/refer`, `/test`).
- Names go to a public page. Never submit a name the user did not type; offer
  initials when the target is a real coworker.
- Do not modify the six statements, the thresholds, the verdict copy, or the
  offense list. They are the official ones.
- The agent generates links and messages. It never posts, emails, DMs, or
  contacts anyone.
