# Sui Agent Wallet — Ubuntu TESTNET integration

This port is a **first-party signing-only integration**, not a third-party wallet extension. Node.js 22+ and npm replace Bun. The old extension is incompatible and unsupported: do not load it. Its unauthenticated/WebSocket routes are disabled by the new server. No browser or live-chain integration has been verified.

## Install and start

```sh
cd sui-agent-wallet/server
npm ci
npm test
# Explicitly create a NEW disposable wallet; the parent directory must exist and be safe.
node cli.mjs init "$HOME/.sui-agent-wallet-testnet"
SUI_AGENT_WALLET_DIR="$HOME/.sui-agent-wallet-testnet" \
SUI_AGENT_ORIGINS="https://your-first-party-app.example" npm start
```

Optional `SUI_AGENT_PORT` defaults to 3847. Bind is always 127.0.0.1. Startup never creates or repairs a wallet. Never use production keys for this integration. Import an existing disposable Sui encoded private key only via `node cli.mjs init ABSOLUTE_NEW_DIRECTORY ABSOLUTE_PRIVATE_KEY_FILE`; the source must be a 0600 regular single-link file in a 0700 safe directory, with a lowercase/dot filename. Never pass secret values in argv, browser configuration, or logs.

Linux storage is plaintext protected by owner-only 0700 directory/0600 files, NOT encrypted storage. Symlinks, unsafe ancestors, ownership, hardlinks, corruption, and overwrite are rejected. Existing macOS Keychain identity loading remains in code but was not tested; Linux initialization is the supported setup path.

## Operator and dApp separation

A trusted local operator reads `control.token` privately and uses bearer authentication with **no Origin header**. Do not expose this token to the page. Controller routes:

- `GET /address`, `GET /pending`
- `POST /sessions` with `{origin}`: returns a short-lived, origin-bound dApp token.
- `POST /approve/<id>` with the **entire unchanged review object** only after reviewing the exact bytes, hash, sender, gas owner, network, origin and expiry.
- `POST /reject/<id>`; `POST /revoke` with `{token}`.

The page receives only its session token. Browser Origin must exactly match the allowlist. DApp routes are `GET /account`, `POST /requests` with `{account,network,bytes}`, and one-shot `GET /results/<id>`. Request TTL and bounded queues prevent indefinite accumulation. Replay, mismatched approval, and parallel approval fail closed. The service signs only; it does not simulate, submit, execute, switch account/network, export mnemonic, or support raw/direct-sign shortcuts.

## First-party Wallet Standard adapter

Bundle `integration/wallet-standard.mjs` using a browser-aware bundler that resolves the pinned dependencies in `server/`. Instantiate `createAgentWallet({endpoint: 'http://127.0.0.1:3847', origin: location.origin, sessionToken})`, then register the returned object with your app's Wallet Standard registry. Registration, production bundling and browser local-network permissions are not covered by this port's tests.

Supported features: `standard:connect`, `standard:disconnect`, `standard:events`, `sui:signTransaction` v2. No sign-and-execute or personal-message feature is advertised. Name: **Sui Agent Wallet — TESTNET integration**. Input must contain a fully resolved SDK2 transaction with `toJSON()`. The SDK builds `Transaction.from(json)` without any client/RPC; unresolved gas/object data fails. It never manually reconstructs commands. The service signs exact canonical BCS bytes; the adapter verifies returned byte equality and cryptographic signer identity. Disconnect cancels delivery locally; the trusted operator should revoke the session to cancel pending server requests.

TESTNET is an immutable application policy, not cryptographic chain binding: Sui transaction signatures do not independently encode this UI network label. Use disposable keys and inspect every approval. A malicious same-origin page can use its session to enqueue requests but cannot approve them. A compromised local user/process can read plaintext keys; this is not a hardware wallet.

## Verification scope

`npm test` uses actual loopback HTTP, disposable keys and SDK signature verification, including a fully built sponsored transaction with a different gas owner. Startup smoke launches the actual Node entrypoint in a subprocess and checks authenticated/unauthenticated HTTP. No funds, faucet, chain RPC, transactions, production service, canonical ledger, browser profile or global provider authentication are touched. Browser wallet UX and live sponsorship remain untested. There are no build/typecheck scripts for the plain `.mjs` service.
