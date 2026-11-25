---
name: covalent-bond-test
description: How to write, run, and debug tests for Covalent Bond: the runner, the in-process mock relay, deterministic polling, port allocation, cleanup conventions, and what every kind of change must cover. Use when adding or modifying a test, when a suite fails, or before committing any behavior change.
---

# Testing Covalent Bond

`npm test` runs every `test/*.test.js` file as a separate process via
`test/run-all.js`. A suite passes when its process exits 0; use plain
`assert` and let a failed assertion crash the process. No test framework;
keep it that way (small surface is a feature).

## Ground rules

- **Every bug fix and every new behavior ships with a test.** Put it in the
  matching existing suite, or a new `*.test.js`; the runner picks it up
  automatically.
- **The `mitm` suite is the security-model guardrail.** It must stay green,
  and any change to the key schedule, handshake, or abort logic needs a case
  there (or a clearly linked one).
- Tests must run **offline**: no network, no wrangler, no deployed relay.
  Everything talks to the in-process mock relay.
- Tests may `console.log` freely (they are standalone processes, not loaded
  by the MCP server).

## Using the mock relay

```js
import { startMockRelay, stopMockRelay, resetMockRelay } from './mock-relay-server.js';

await startMockRelay(PORT);   // pick a UNIQUE port per suite (see below)
resetMockRelay();             // wipe sessions + rate limits between suites
// ... test ...
await stopMockRelay();
```

**Port allocation:** each suite binds its own port so suites can never
collide: 8791 handshake, 8792 mcp-routing, 8793 payload-hardening,
8794 rate-limiting, 8795 hardening-regressions. A new suite takes the next
free number. 8787 is reserved for `npm run relay:dev`.

The mock mirrors the production worker's API exactly (sequence numbers,
create-clobber refusal, rate limits, payload caps, security headers, error
codes). Protocol constants (TTL, caps, throttle, error codes) live once in
`relay/constants.js`; the mock imports them and the Worker keeps mirrored
copies that `relay-parity.test.js` verifies by reading `worker.js`. If you
change the worker's behavior, change the mock in the same PR, keep the shared
constants in sync, and cover the difference with a test.

## Deterministic polling (never sleep)

Do not `start()` the interval poller and wait. Drive the protocol manually:

```js
const polling = new PollingManager(relayClient, sessionManager, handlers);
await polling.pollOnce();     // one deterministic protocol step
```

For unit-level packet handling, bypass the relay entirely with a stub:

```js
const fakeRelay = { getSession: () => ({ routingId: 'x' }),
                    disconnect: async () => {}, poll: async () => [] };
await polling.handleMessage({ from: 'peer', payload: encryptedBlob, timestamp: Date.now() });
```

For a confirmed pair without any relay, run the offline handshake:
`createSession` → `joinSession` → `completeKeyExchange` → `confirmPeer`
(see `confirmedPair()` in `test/hardening-regressions.test.js`).

## Cleanup conventions

`test/run-all.js` sets `COVALENT_HOME` to a fresh temp directory, so suites
never touch the user's real `~/.covalent/` (audit log, incoming files); the
temp directory is removed after a fully green run. When building a
`.covalent` path in a test, always honor the override:
`process.env.COVALENT_HOME || path.join(os.homedir(), '.covalent')`, which
also keeps the suite runnable file-by-file outside the runner.

- Delete any file you write (accepted transfers, temp payload files).
- Session state is memory-only (nothing is persisted to disk), so there is
  no session file to clean up, but leave the legacy
  `~/.covalent/sessions.json` cleanup lines in older suites alone; they are
  harmless.
- Temp outbound files go in `os.tmpdir()` with a suite-specific name.
- `clearSession()` / `stop()` / `disconnect()` anything you started;
  a leaked interval keeps the process alive and the suite hangs.

## What each kind of change must cover

| Change | Must test |
|--------|-----------|
| Crypto / key schedule | Positive AND negative path (wrong code, wrong role, tampered tag) in `crypto-session`; MITM implication in `mitm` |
| Protocol / packet handling | Abort vs drop behavior in a `PollingManager` test; replays are dropped, decrypt failures abort |
| Relay API | Mock-relay behavior test + the same change mirrored in `cloudflare-worker/worker.js` |
| Validation / limits | Both the allowed and the blocked side of the boundary |
| MCP tools | Drive it through `handleToolCall` like `mcp-routing` does; assert on the tool-result text |

## Debugging a failing suite

Run it alone for full output: `node test/<name>.test.js`. The runner only
prints a suite's output when it fails. If a suite hangs, look for an
unstopped `PollingManager` or an un-closed mock relay first.
