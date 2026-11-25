---
name: hunt-race-condition
description: Hunting playbook for race-condition / TOCTOU vulnerabilities — concurrent-request abuse, HTTP/2 single-packet attacks, double-redeem / double-spend, MFA-OTP & email-verify races, rate-limit bypass. Use when hunting races or TOCTOU bugs.
---

# Hunting Race Conditions

A hunting playbook for race-condition / TOCTOU vulnerabilities, built from 12 public bug-bounty and coordinated-disclosure cases. Race conditions are high-severity because they break the financial, access-control, and integrity assumptions defenders rarely stress-test: double-spending credits, inflating votes, bypassing per-user limits, and racing token/state transitions. The enabling primitive for modern targets is the **HTTP/2 single-packet attack**, which collapses the race window to sub-millisecond and makes rate-limited, distributed, load-balanced backends race-able.

## Quick-start

1. **Enumerate one-time / limited-use actions** — every endpoint enforcing "once per user", "limited quantity", or "deduct balance". The gap between its state read and state write is your window.
2. **Capture a clean baseline** request and confirm the expected single-use behaviour.
3. **Stage parallel requests** — prefer Turbo Intruder `Engine.BURP2` (single-packet HTTP/2) when the target advertises `h2`; otherwise fall back to parallel HTTP/1.1.
4. **Fire 10–50 simultaneous requests** with last-byte sync, then look for multiple successes, duplicate effects, or stale-state where only one should have won.
5. **Verify the effect and reproducibility** (3/5 attempts), then run Gate 0 before reporting.

Full detail is loaded on demand — see References.

## References

Each file is loaded on demand — read one only when the task needs that depth (progressive disclosure).

- `references/methodology.md` — crown-jewel targets, attack-surface signals (URLs, headers, JS/tech-stack tells), the 10-step hunting methodology, common root causes, defender bypass techniques, Gate 0 validation, and real impact examples · read when scoping targets, planning the hunt, or validating/writing up a finding.
- `references/payloads.md` — copy-paste Turbo Intruder, `curl`-parallel, and Python `asyncio` race templates, plus source-audit grep patterns and the HTTP/2 capability check · read when you need a ready-to-fire PoC or to audit source for unlocked read-then-write.
- `references/single-packet-attack.md` — the HTTP/2 single-packet deep reference: why it works, last-byte-sync mechanics, Wireshark validation, h2.0 vs h2.cl variants, race-window estimation, connection/stream shapes, the annotated `Engine.BURP2` template, Flatt's first-sequence-sync (N>30), operator playbook, and anti-patterns · read when building or debugging a single-packet exploit or deciding which attack shape to use.
- `references/disclosed-reports.md` — the per-bug-class catalog of the 12 disclosed cases (GitLab CVE-2022-4037, Worldcoin, Stripe ×2, Reverb gift card, Cosmos faucet, InnoGames, Flatt PIN-bruteforce, nopCommerce CVE-2024-58248, …) with payload, root cause, and bounty · read when matching your target to a known race class or citing precedent.

## Related Skills & Chains

- **`hunt-business-logic`** — Race conditions are the "concurrency arm" of every business-logic state machine. Chain primitive: business logic (coupon/promo) + race-condition single-packet attack → coupon redeemed N times → direct financial loss.
- **`hunt-mfa-bypass`** — OTP-expiry windows and replay protection are classic race targets. Chain primitive: race + MFA-validate endpoint → bypass OTP expiry by submitting N concurrent validations within the validity window.
- **`hunt-ato`** — Race conditions on password reset, email change, and account creation enable persistent ATO. Chain primitive: race on email-change endpoint + atomic-update missing → swap victim email + read reset token before user notice.
- **`hunt-api-misconfig`** — Wallet/balance/credit endpoints without atomic UPDATE are double-spend candidates. Chain primitive: race + atomic-update missing → double-spend balance → withdraw N× user balance.
- **`security-arsenal`** — Load the Turbo Intruder single-packet template, h2.cl smuggling for atomic submit, and `curl --next` parallel multi-request patterns.
- **`triage-validation`** — Apply the Statistical-Sampling gate: a single anomalous response is noise; require 1 successful + N duplicate / over-quota / stale-state demonstrations with response screenshots before reporting.
