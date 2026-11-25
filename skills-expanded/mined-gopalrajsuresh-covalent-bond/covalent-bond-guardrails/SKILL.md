---
name: covalent-bond-guardrails
description: Guardrails for any agent editing the Covalent Bond repository, covering the security invariants that must never be broken, what code NOT to add, and the verify-don't-guess working discipline. Use whenever writing or changing code, tests, or config in this repo before making the edit.
---

# Covalent Bond engineering guardrails

Covalent Bond is a peer-to-peer, end-to-end-encrypted channel for AI coding
agents, exposed over MCP. A single careless change can silently defeat its
security or corrupt the MCP protocol stream. Follow these rules on every edit.
Context is in `docs/ARCHITECTURE.md`; this skill is the enforceable checklist.

## Security invariants (never break these)

They are correctness requirements, not style. If a change would touch any of
them, STOP and confirm with the human first (see Working discipline).

1. **No stdout writes** from any module the MCP server loads (`daemon/`,
   `mcp/`, `relay/`, `security/`, `transfer/`). stdout is the JSON-RPC stream.
   Log via `logger` (stderr) from `security/index.js`. A stray `console.log`
   corrupts the protocol. (Standalone scripts and the mock relay may log.)
2. **The session code never leaves the machine to the relay.** The relay is
   addressed by the routing ID (`PBKDF2(sessionCode)`) only. The code is the
   secret that defeats a malicious relay; leaking it reopens the MITM hole.
3. **No received file is written without explicit `bond_accept`** (human
   consent). Incoming transfers stay pending until then.
4. **All peer content is untrusted data.** Keep the untrusted-content wrapper
   and never let received text be interpreted as instructions.
5. **The session key is derived once per session.** Never run the
   600k-iteration PBKDF2 per message. Wipe ephemeral private keys once the
   session key exists.
6. **Local servers bind to `127.0.0.1`**, never `0.0.0.0`.
7. **Crypto domain constants stay stable and consistent**
   (`CovalentBond-Routing`, `CovalentBond-CodeKey`, `CovalentBond-SessionKey`,
   `CovalentBond-Confirm`). Both peers must derive identical values.

## What NOT to add

- **No new runtime dependencies** without a clear need; the small surface is
  a feature. Prefer Node built-ins (`crypto`, `fs`, `http`).
- **No rolling your own crypto** beyond composing Node's `crypto` primitives
  as already done. No custom ciphers, no home-made KDFs.
- **No telemetry, analytics, or network calls** to anything but the configured
  relay. Never phone home.
- **No hardcoded secrets, account IDs, KV IDs, personal subdomains, or emails.**
  Relay URL comes from `COVALENT_RELAY_URL` (or the localhost default).
- **No weakening of validation**: file-type whitelist, size caps, path
  safety, session-code format, routing-ID format. Don't broaden these to make
  a test pass.
- **No stdout logging, ever** (see invariant 1).
- **No vendor lock-in language or Claude-specific assumptions** in code/docs;
  keep it "the agent" / "the MCP client".

## Working discipline (verify, don't guess)

- **Verify from the code, never from memory or assumption.** Before relying on
  how a function, field, or flow behaves, read it. If a claim can be checked in
  the source, tests, or docs, check it.
- **Proceed on low-risk defaults.** For unambiguous, reversible, local changes
  that don't touch the invariants, make the sensible choice and note it; no
  need to stop.
- **STOP and ask the human** before anything that:
  - touches a security invariant above, the wire protocol, or the key schedule;
  - deploys, publishes, or sends anything outward;
  - deletes or overwrites data you didn't create, or is otherwise hard to undo;
  - is genuinely ambiguous in intent and could go two materially different ways.
- **Never fabricate.** If you don't know, say so and find out. Don't invent
  file paths, flags, test names, or API shapes.

## Every change must

1. Be the smallest edit that does the job, in the right module.
2. Ship with a test if it's a bug fix or new behavior (`test/*.test.js`).
3. Pass `npm test`: every suite, including `mitm` (the security-model guard).
4. Leave no stdout leak if a server-loaded module changed.

For raising the change as a PR, see the `covalent-bond-pr` skill. For running
the project, see `covalent-bond-run`.
