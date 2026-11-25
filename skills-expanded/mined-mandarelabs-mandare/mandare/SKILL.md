---
name: mandare
description: >-
  Work under a Mandare accountability door: check your remaining budget before
  expensive work, read and explain gateway refusals (budget caps, revocations,
  approval holds), verify the tamper-evident action ledger, export integrity
  certificates, and hit the kill switch when the human asks you to stop.
  Use when the agent runs behind a Mandare gateway, when an LLM/API call is
  refused with a mandare code, or when the human asks what an agent spent,
  why it was refused, or for proof of what happened.
homepage: https://github.com/mandarelabs/mandare
metadata:
  openclaw:
    emoji: 🛂
    requires:
      bins:
        - mandare
      env:
        - MANDARE_LEDGER_DB
    install:
      - kind: npm
        package: "@mandarelabs/cli"
        bins:
          - mandare
        note: >-
          Not yet on npm (repo pre-launch): install from a checkout with
          `pnpm install && pnpm build`, then use `node apps/cli/dist/main.js`
          as the mandare binary or link it onto PATH.
---

# Mandare — act under a mandate, prove what you did

You are running behind a **Mandare door**: a local gateway that meters every
LLM/API call against a human-signed mandate (budget caps, approval
thresholds) and records everything in a tamper-evident ledger. This skill
gives you **visibility and proofs**: you can read budgets, explain refusals,
and prove the trail. The **kill switch** section works only if the human gave
your environment operator-level door access (see its note) — and that same
access could reopen doors, so the rules below are yours to keep, not a lock
that keeps you.

Everything below uses the `mandare` CLI and the ledger at
`$MANDARE_LEDGER_DB` (ask the human for the path if unset).

## Check the budget before expensive work

Before a long loop, a batch job, or anything with real spend, read the
mandate's remaining room:

```bash
mandare verify --db "$MANDARE_LEDGER_DB" --spend
```

- `settled` is spent; `reserved` is committed to in-flight calls.
- `counters: CONSISTENT` means the live budget counters equal a fresh replay
  of the ledger — if it says anything else, STOP and tell the human.
- If the remaining budget is clearly too small for the task, say so BEFORE
  burning it.

## When the gateway refuses a call

A refusal is an HTTP 403 with a JSON body like
`{"code": "PER_DAY_EXCEEDED", "reasons": [...], "denied_entry": "<hash>"}`.
It is also recorded on the ledger. Codes you will meet:

| code | meaning | what to do |
|---|---|---|
| `PER_TX_EXCEEDED` / `PER_DAY_EXCEEDED` / `PER_TASK_EXCEEDED` / `TOTAL_EXCEEDED` | a mandate cap would be crossed | stop; report spend so far and what the cap is; ask the human to raise the mandate if warranted |
| `APPROVAL_REQUIRED` / approval timeout | the call waits for an async human approval | wait/retry once; if denied, accept it |
| `AGENT_REVOKED` / `MANDATE_REVOKED` | you or your permission slip was killed | STOP ALL WORK immediately and tell the human |
| `WINDOW_INVALID` | the mandate expired | report it; the human must issue a new one |

**Never try to route around a refusal** — no direct provider calls, no
credential scavenging, no retry storms. The refusal is the product working.
Report it honestly, with the `denied_entry` hash as the receipt.

## Prove what happened (for the human, an auditor, a client)

Full verification — hash chain, signatures, spend trail, revocations,
approvals:

```bash
mandare verify --db "$MANDARE_LEDGER_DB" --spend --json
```

If a witness is configured (`$MANDARE_WITNESS_URL` +
`$MANDARE_WITNESS_PUBLIC_KEY`), also prove nothing was truncated or
rewritten, and export a certificate a third party can check WITHOUT the
ledger:

```bash
mandare verify --db "$MANDARE_LEDGER_DB" --witness "$MANDARE_WITNESS_URL" --witness-key "$MANDARE_WITNESS_PUBLIC_KEY"
```

If the human gave you the door's public key out-of-band, append
`--door-key <hex>` to the verify command: without it the witness check is
bound to the source the ledger file itself declares, and the output says
"self-declared source" — report that caveat, don't hide it.

```bash
mandare certify --db "$MANDARE_LEDGER_DB" --witness "$MANDARE_WITNESS_URL" --witness-key "$MANDARE_WITNESS_PUBLIC_KEY" --out certificate.json
```

Give the human the certificate file, not a screenshot.

## The kill switch (closing doors is always allowed)

If the human says stop, or you observe an agent (including yourself)
misbehaving with spend:

```bash
mandare kill "$AGENT_DID" --reason "human asked to stop"
```

`--mandate <id>` kills one permission slip (the agent survives); `--all`
halts the whole door. The kill is local, offline, and fail-closed — the
gateway refuses the subject on its next request.

**Operator-level access.** `mandare kill` signs a ledger entry with the
door's signing key (from the vault, or the `.doorkey.pem` beside the ledger),
so it runs only where that key is readable. Anything that can read the key
can also run `mandare reinstate` and sign other ledger entries: an
environment where this command works is an operator environment. If yours
cannot reach the key, the kill fails — tell the human to run it.

## What this skill will NOT do (operator actions)

Issuing passports, mandates, or access tokens, and reinstating a killed
agent, are OPERATOR actions. If asked, do not run them yourself — tell the
human the command to run (`mandare passport issue`, `mandare mandate issue`,
`mandare token issue`, `mandare reinstate`) and why the separation exists:
an agent that can widen its own permissions has no permissions at all.

This is a rule you follow, not a boundary the tooling enforces: if your
environment can run `mandare kill`, it holds the door key those commands
need too. Never use that access to reopen a door or write to the ledger.
