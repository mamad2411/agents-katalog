---
name: race-condition
description: Race condition and TOCTOU testing for web apps. Use when testing one-time operations, concurrent HTTP abuse, rate-limit bypass, Turbo Intruder gates, HTTP/2 single-packet attacks, and CWE-362-style synchronization gaps.
---

# SKILL: Race Conditions — Testing & Exploitation Playbook

> **AI LOAD INSTRUCTION**: Treat race conditions as **authorization/state integrity** issues: non-atomic read-then-write lets multiple requests observe stale state. Prioritize **one-time** or **balance-like** operations. Combine **parallel transport** (HTTP/1.1 last-byte sync, HTTP/2 single-packet, Turbo Intruder gates) with **application evidence** (duplicate success responses, inconsistent balances, duplicate ledger rows). **Authorized testing only.** Routing note: for business workflows, coupons, inventory, or one-time rewards, start with this skill and cross-load `business-logic-vulnerabilities`.

---

## 0. QUICK START — What to Test First

Target endpoints where **check** and **update** are unlikely to be a single atomic database operation:

| Priority | Operation class | Example paths / parameters |
|----------|------------------|----------------------------|
| 1 | One-time redeem / coupon / bonus | `redeem`, `apply_coupon`, `claim_reward`, `voucher` |
| 2 | Balance / quota / stock deduction | `transfer`, `purchase`, `reserve`, `inventory` |
| 3 | Invite / referral / signup bonus | `invite_accept`, `referral_claim` |
| 4 | Password / email / MFA verification | `verify_token`, `confirm_email`, `reset_password` |
| 5 | Idempotent-looking APIs without strong keys | `POST` that should succeed only once per user |

**First moves (conceptual)**:

1. Capture the **state-changing** request in a proxy.
2. Send **20–100** copies **as simultaneously as your tooling allows**.
3. Classify outcome: **0/1 expected successes** vs **N successes** or **inconsistent final state**.

---

## 1. CORE CONCEPT

### 1.1 TOCTOU (Time-of-check to time-of-use)

```
Thread A                    Thread B
   |                            |
   +-- CHECK (resource OK)      |
   |                            +-- CHECK (resource OK)  ← both see "OK"
   +-- USE / UPDATE             |
   |                            +-- USE / UPDATE           ← duplicate effect
```

**TOCTOU** means the **decision** (check) and the **mutation** (use) are not one indivisible step.

### 1.2 Non-atomic read-then-write

Typical vulnerable pseudo-flow:

```text
balance = SELECT balance FROM accounts WHERE id = ?
if balance >= amount:
    UPDATE accounts SET balance = balance - ? WHERE id = ?
```

Two concurrent requests can both pass the `if` before either `UPDATE` commits.

### 1.3 Database-level vs application-level locking gaps

| Layer | What goes wrong |
|-------|------------------|
| **Application** | In-memory flag, cache, or session says "not used yet" while DB already updated — or the reverse. |
| **ORM / service** | Two instances, no distributed lock; each thinks it owns the decision. |
| **DB** | Missing `SELECT … FOR UPDATE`, wrong isolation level, or logic split across multiple statements without transaction. |
| **API gateway** | Per-IP rate limit is **check-then-increment** — parallel burst passes duplicate checks. |

**Hint**: `UNIQUE` constraints and **idempotency keys** often eliminate entire bug classes — test whether the app **enforces** them on the hot path.

---

## 7. TOOLS

| Tool | Role |
|------|------|
| [PortSwigger/turbo-intruder](https://github.com/PortSwigger/turbo-intruder) | High-concurrency replay, **gates**, scripting in Burp. |
| [JavanXD/Raceocat](https://github.com/JavanXD/Raceocat) | Race-focused HTTP client patterns (verify compatibility with your stack). |
| [nxenon/h2spacex](https://github.com/nxenon/h2spacex) | HTTP/2 low-level / single-packet style experimentation (use responsibly, authorized targets only). |
| **Burp Suite — Repeater** | **Send group (parallel)** / **single-packet attack** for multi-request synchronization. |

---

## 8. DECISION TREE

```text
                         START: state-changing API?
                                    |
                     NO -----------+---------- YES
                      |                        |
                   stop here              one-time / balance / verify?
                                                    |
                          +-------------------------+-------------------------+
                          |                         |                         |
                    coupon-like                 rate limit                  multi-step
                          |                         |                         |
                   parallel same req          parallel vs serial         parallel pipelines
                          |                         |                         |
                   duplicate success?           limit exceeded?          state mismatch?
                     /       \                    /       \                  /       \
                   YES       NO                 YES       NO               YES       NO
                    |         |                  |         |                |         |
              report +    try HTTP/2        report +    try TI        report +   deepen
              evidence    single-packet      evidence    gates                     per-step
                    |         |                  |         |                |         |
                    +----+----+                  +----+----+                +----+----+
                         |                            |                          |
                    tool pick                    tool pick                  tool pick
                         v                            v                          v
              Burp group / h2spacex            TI gates / Raceocat          TI + trace IDs
```

**How to confirm (evidence checklist)**:

1. **Reproducible** duplicate success under parallelism, not flaky single retries.
2. **Server-side** artifact: two rows, two emails, two grants, or wrong final balance.
3. **Correlate** with `x-request` (or similar) markers or unique body fields in logs (authorized environments).

**Routing summary**: if the scenario is more about business rules, pricing, or workflow bypass, load `skills/business-logic-vulnerabilities/SKILL.md`; this file focuses on **concurrency and transport-layer synchronization**.

---

## References

Each file is loaded on demand — read one only when the task needs that depth (progressive disclosure).

- `references/attack-patterns.md` — the core attack categories (limit-overrun, rate-limit-bypass, multi-step), the concrete limit-overrun catalogue (coupon, vote, balance, inventory, referral), and the CVE-2022-4037 reference case · read when picking which abuse to attempt and what success evidence to look for.
- `references/transport-attacks.md` — HTTP/1.1 last-byte sync, the HTTP/2 single-packet attack + detailed mechanics (Nagle/frame coalescing, server queue, h2spacex), and single-packet multi-endpoint bursts · read when you need to actually synchronize the requests on the wire.
- `references/turbo-intruder-templates.md` — ready-to-run Turbo Intruder scripts: same-endpoint gate release and multi-endpoint same-gate, plus the `x-request` correlation header · read when driving the attack from Burp's Turbo Intruder extension.
- `references/database-isolation.md` — the isolation-level exploitation matrix (READ UNCOMMITTED → SERIALIZABLE), canonical vulnerable SQL sequences, and a hot-path audit checklist · read when reasoning about the DB layer or verifying a fix.

---

## Related

- **business-logic-vulnerabilities** — workflow, coupon abuse, and logic-first checklists (`../business-logic-vulnerabilities/SKILL.md`).
