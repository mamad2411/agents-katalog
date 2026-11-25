---
name: rift-qa
description: "Run and extend the live-cluster QA harness for rift-cluster at ~/rift-qa-backup — provisions tenants/principals/imposters/scenarios/spaces/routes/sources against a running fleet, asserts the console can reach all of it, and sweeps for u64 values JavaScript cannot read back. TRIGGER whenever rift-cluster console or admin-API behaviour is being verified by hand, before declaring UI work done, or after a change that touches the admin API, the console, or the OpenAPI contract. Usage: /rift-qa [seed|parity|u64|all]"
user_invocable: true
argument-hint: "[seed|parity|u64|all]"
---

# rift QA harness

The harness lives at `~/rift-qa-backup/` — **outside the repo, deliberately**. It provisions and
asserts against a *running* fleet, which is a different artifact from `web/e2e/` (the single-node
fixture the project ships and CI runs). Read `~/rift-qa-backup/README.md` first; it is the runbook
and it explains what each file covers.

## When to use it

- Before saying console or admin-API work is done.
- After any change to the admin API, the console, or `docs/api/openapi-ee.yaml`.
- Whenever a defect is reported by hand — reproduce it here, then leave a case behind.

## Running it

Needs a cluster on `:12525` with `MB_APIKEY=rift-local-bootstrap-key`.

```sh
cd ~/rift-qa-backup
python3 seed.py          # provision + API assertions, incl. the RBAC matrix
~/Projects/rift-enterprise/web/node_modules/.bin/playwright test --config parity.config.ts
python3 u64_sweep.py     # integers above 2^53-1, which JS silently rounds
```

`node_modules` is a symlink to `web/node_modules`; recreate it if the harness is moved.

## The rule this exists to enforce

Everything doable through the API must be doable through the console. `seed.py` proves the API
accepts it; `parity.spec.ts` asks whether an operator can reach it. A gap between them is a
finding even when nothing crashed.

## How to extend it — this is the part that matters

Most rift-cluster defects found on 2026-08-04 came from **tests that modelled something the real
system does not do**: a list fixture carrying a payload the server never sends, single-digit node
ids that cannot round-trip wrong or wrap mid-digit, a component harness that fed `onChange` back as
props so a blank row persisted only in the test. Every one passed its suite and was broken in the
browser.

So when adding to this harness:

1. **Assert against the fleet, not against a literal.** Read the API, then check the screen agrees.
   A test that asserts what it just typed in proves only that React works.
2. **Use hostile values.** Real 19-digit ids, names past the 34-character truncation cut, non-ASCII,
   nameless and zero-stub objects, bodies in the wrong envelope. Tidy fixtures cannot catch untidy
   bugs.
3. **Beware the shared channel.** An oracle that reads the API through the same lossy path as the
   screen is blind to corruption in that path — this is exactly how a `u64` equality check passed
   while both sides were rounded. `u64_sweep.py` intercepts raw integer text via `parse_int` for
   that reason.
4. **Triage a failure before reporting it.** Decide whether the harness or the product is wrong.
   Several early failures here were harness bugs; reporting them as defects would have been worse
   than not running it.
5. **Leave a case behind for every hand-found defect.** That bug is proof the suite was blind.

## Fix vs file

Fix a contained defect and open a PR (per the repo's own convention). File an issue when the change
needs a design decision — a contract change, a new authorization tier, or a new class of capability.
`#335` (a server endpoint that originates outbound traffic) and `#336` (what a malformed stub body
should do against a contract with no required fields) are the worked examples.
