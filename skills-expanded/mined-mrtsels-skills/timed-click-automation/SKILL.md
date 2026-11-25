---
name: timed-click-automation
description: Timed clicks at an exact wall-clock moment (course reg).
metadata:
  imported_from: hermes
---

# Timed Click Automation (click exactly at HH:MM:SS)

Covers any browser automation that must click an element at a precise
wall-clock moment: course registration opening, flash sales, ticket drops.

## Core principle

`new Date()` in the browser follows the OS clock, which carries a small NTP
offset (typically tens of ms). The click MUST land strictly AFTER the real
target time — clicking early = the server rejects it (window not open yet).

Design = **poll interval** (detection lag) + **post-detection buffer**.
The buffer MUST exceed the measured clock offset, or you risk clicking early.

## Step 1 — Measure clock offset FIRST (before choosing parameters)

- **NTP is sub-millisecond accurate**; HTTP `Date` headers are
  second-granularity (useless for ms calibration, ±500ms error).
- macOS: `sntp -sS time.apple.com` — read the leading `+0.xxx` / `-0.xxx`
  seconds. Sample 3×, cross-check 2-3 independent sources
  (time.google.com, time.nist.gov, pool).
- **Check for NTP hijack**: if `nslookup <ntp-host>` resolves to `198.18.x.x`
  (reserved segment), a transparent proxy is intercepting NTP traffic — the
  configured source (`cat /etc/ntp.conf`) may not be the actual reference.
- Use the max observed offset as the design value (e.g. ~70ms).

## Step 2 — Size poll interval + buffer

- Poll = `setInterval` interval. **Browsers throttle background tabs** — a
  nominal 10ms setInterval actually fires ~50ms (measured). Use 50ms as the
  honest value; don't bother with 10ms.
- Buffer = `setTimeout` after detection fires. Must be `> offset + margin`.
  Offset 70ms → buffer 80ms → click lands target+80..130ms.
- NEVER shrink buffer below the measured offset — that inverts the guarantee.

## Step 3 — Inject via CDP (chrome-devtools-mcp / mcporter)

- **Strip the IIFE wrapper**: `(function(){...})();` → `function runScript(){...}`
  before passing to `evaluate_script`, or you get `Unexpected token ';'`.
- mcporter syntax: `--args '{"function": "<fn>", "dialogAction": "2026-08-10 10:00:00"}'`
  — `dialogAction` string is the `window.prompt` reply. key=value form fails
  with -32602; `--args` JSON form is required.
- `evaluate_script` returning `undefined` is NORMAL — the script has no return
  value; side effects are in the DOM. Verify via the DOM, not the return.
- Scripts die on navigation (confirm-redirect, form submit). Re-inject after
  the page loads. Detect "wrong page" by `document.title` + DOM elements,
  NOT by URL (SPA apps share one base URL).

## Step 4 — Verify the ACTUAL click time (don't trust "it ran")

```js
var ns = performance.timeOrigin;
performance.getEntriesByType("resource")
  .filter(e => e.initiatorType === "xmlhttprequest")
  .slice(-1).map(e => new Date(ns + e.startTime).toISOString())
```
Compare against the target time. Expected delay = buffer + poll lag
(e.g. +80..130ms). If the user disputes timing, this is the evidence.

## Pitfalls

- **macOS default APFS is case-INSENSITIVE**: `mkdir cusis-auto-reg`
  silently collides with an existing `CUSIS-Auto-Reg` — they are the SAME
  directory. Before creating a dir whose name differs only by case from an
  existing one, `ls` the parent and `git status` the candidate — I once moved
  files into a cloned repo thinking it was a fresh dir. Verify the target is
  not an existing git repo before moving files in.
- **Never run two browser instances logged into the same account**: course
  systems detect multi-session and lock the original one
  ("Restricted Multiple Login Error"). A Selenium test instance I launched
  beside the user's real Chrome triggered it. Fix: quit browser completely,
  reopen, re-login (one session). This also means: for testing logged-in
  flows, reuse the user's session, don't spawn a second instance.
- **Background-tab throttling**: fast setInterval is unreliable; account for
  it in buffer sizing.
- **Write portable paths in docs/skills**: never hardcode `/Users/<user>/...`;
  use `os.path.expanduser('~/...')` or `~` — hardcoded user paths leak
  identity and break on other machines.

## Reference

- `references/cusis-timed-enroll-case.md` — real measured values: NTP offsets
  across sources, hijacked NTP detection, 102ms actual click delay vs target,
  the multi-login lockout incident.
