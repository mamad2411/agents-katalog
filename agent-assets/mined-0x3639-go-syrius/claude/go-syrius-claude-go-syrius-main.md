# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

The wallet is **substantially built**: Phases 0–5 and Phase 7a are shipped and merged to `main`. Working today: read-only wallet, send/receive, wallet lifecycle (create/import/manage), both node modes (remote/embedded), the full Network-of-Momentum feature set (plasma, staking, pillars, sentinels, tokens, accelerator), and CI. **Remaining:** Phase 7b–7f (release builds, signing/notarization, auto-update, a11y/telemetry, security pass + docs). **Phase 6 (Ledger) is deferred** (out of scope for now). See "Working order" below for per-phase status.

`plan.md` is the authoritative spec; read it before substantial work, and keep it in sync as decisions change. Per-phase design specs and plans live under `docs/superpowers/{specs,plans}/`, and per-phase acceptance records under `docs/phase*-acceptance.md`.

## What this project is

A reimplementation of the Zenon `syrius` wallet (originally Flutter/Dart) as a **Go + Wails v2** desktop app. The core insight driving the whole design: the hard cryptographic/node backend already exists in Go — `github.com/0x3639/znn-sdk-go` (BIP39/BIP44 HD wallets, keystore encryption, pure-Go PoW, all 11 embedded-contract APIs, WebSocket RPC) and `go-zenon` (the full node). Because Wails runs a Go backend, these are direct imports rather than FFI boundaries. The work is therefore mostly a **web frontend rebuild plus a thin, security-reviewed binding layer** over an SDK the author owns.

## Stack (locked decisions — see plan.md §6)

- **Wails v2** (v2.12.0; not v3 — stability for a funds-handling app)
- **Go 1.26** (go.mod `go 1.26.0`, `toolchain go1.26.7`), importing `znn-sdk-go` (pinned, author-controlled; currently v0.5.0) and `go-zenon`
- **Vue 3 + TypeScript + Vite**, **Tailwind CSS 4**, **Pinia** for state, **vue-router** (memory history). UI built on **nom-ui** (Vue component library, `github:digitalSloth/nom-ui` pinned) — Dialog/Tabs/Address/TxStatus/TxDirection/TokenIcon/toast + its blockchain primitives. *(Originally scaffolded in Svelte; migrated to Vue 3 + nom-ui — merged to main `a9c2880`, 2026-06-25. The Go backend + Wails bindings were untouched by the migration.)*
- Build via Wails CLI + GitHub Actions cross-platform matrix

## Architecture

### Binding boundary (the central invariant)

The frontend (WebView) must **never** receive a private key, mnemonic seed, or decrypted keystore. The frontend sends *intent* ("send X ZNN to Y"); Go builds → PoWs → signs → publishes. Mnemonics surface exactly once at creation and via an explicit, password-gated `RevealMnemonic`. Every state-changing Go method re-validates its inputs — never trust frontend validation. Long operations (especially PoW, which takes seconds) emit progress events instead of blocking.

### Service layout (planned — see plan.md §4)

Wails-bound services live under `app/`, each a clear seam: `WalletService` (unlock/lock/accounts), `NodeService` (node modes + status events), `TxService` (build→pow→sign→publish), `NomService` (plasma/stake/pillar/sentinel/token/accelerator), `LedgerService` (Phase 6), `ConfigService` (settings/data dir). Non-bound internals under `internal/`: `signer/` (software | ledger abstraction), `powmgr/` (cancellable PoW), `compat/` (keystore compatibility + tests). Frontend under `frontend/src/` (Vue): `views/` (route components: public Unlock/Create/ImportMnemonic, plus authenticated Dashboard/Transfer/Receive/Tokens/NetworkPage/Settings/AddressBook), `components/AppShell.vue` (layout route wrapping every authenticated screen — Sidebar + TopBar + the single global data bootstrap/refresh after unlock), `router/` (vue-router + lock guard; authenticated routes nest under AppShell, `/` redirects to `/dashboard`), `stores/` (Pinia: wallet/node/balances/tx/txs/unreceived/token/plasma/pillar/stake/sentinel/accelerator/governance/contacts/price/ui/autoReceive), `components/` (+ `components/panels/` for the NoM panels rendered by NetworkPage), `lib/format.ts` (BigInt `formatAmount`/`formatAmountExact` — never use nom-ui `Amount` for balances, it loses precision), and the generated `frontend/wailsjs/` bindings.

### Two node modes

`NodeService` abstracts both behind one interface so the frontend only sees "mode / connected / syncing / height / peers":
1. **Remote** — `wss://` third-party node (built first)
2. **Embedded** — `go-zenon` imported and run in-process (goroutine); the feature where Wails materially beats the Flutter original

Local mode removed 2026-08-03 (`docs/superpowers/specs/2026-08-03-node-mode-hardening-design.md`) — self-hosted `znnd` users point Remote at `ws://127.0.0.1:35998`.

### Frontend ⇄ Go contract

Methods and events are enumerated in plan.md §5. Events flow Go→frontend via `runtime.EventsEmit`: `node:status`, `node:sync`, `wallet:locked`, `tx:pow-progress`, `tx:signed`, `tx:published`, `tx:received`, `balance:updated`. Define this contract early and keep it stable; both sides build against it.

## Correctness-critical compatibility (plan.md §2)

These invariants determine whether wallet files and transactions interoperate with the original syrius. Most are *inherited* from `go-zenon`'s `common/types` and crypto via the SDK rather than reimplemented — that is why the project is tractable. Do not diverge from them:

- **Keystore format** — must read/write existing syrius `.dat` keystores byte-compatibly: same Argon2 variant + params (memory/iterations/parallelism), same AES mode, same layout.
- **Address derivation** — BIP39 → BIP44 → Ed25519 → `z1…` must match syrius byte-for-byte.
- **PoW links** — nonce algorithm + difficulty must match go-zenon's verifier exactly.
- **Tx hashing & signing** — AccountBlock hash + Ed25519 signature must verify on-chain.
- **ABI encoding** — embedded-contract call encoding must match.

The acceptance test for compatibility: a wallet created here opens in syrius and vice-versa.

## Working order (phases — plan.md §3)

Ordered by risk; do not start UI-heavy work before the foundation is proven.
- **Phase 0 ✅** — de-risking spike: keystore round-trip against a *real* `.dat`, read-only RPC, one testnet tx end-to-end. Proved compatibility before any UI.
- **Phase 1 ✅** — Wails skeleton + read-only wallet (remote node only)
- **Phase 2 ✅** — send/receive (the correctness-critical milestone)
- **Phase 3 ✅** — wallet lifecycle (create/import/manage)
- **Phase 4 ✅** — embedded & local node modes
- **Phase 5 ✅** — NoM features (plasma, staking, pillars, sentinels, tokens, accelerator). *Manual GUI write-flow testnet acceptance for 5b–5f remains user-run; automated + live-read gates pass.*
- **Phase 6 ⏸ DEFERRED** — Ledger (out of scope for now; cleanly separable behind the `signer/` seam)
- **Phase 7** — hardening, packaging, signed releases. **7a ✅** (CI: GitHub Actions PR gate). **7b–7f remaining:** release build matrix, signing/notarization, auto-update, a11y/keyboard/telemetry, security pass + docs.

## Security rules (non-negotiable — plan.md §7)

- No secrets ever cross into the WebView; treat the frontend as untrusted for key material.
- **Confirm-what-you-sign:** the confirm modal renders the effect derived from the *built block*, not from raw form inputs.
- Minimize decrypted-seed lifetime; never log anything sensitive.
- Testnet-gate everything; the crypto-critical path (keystore, derivation, hashing, signing, PoW) gets independent review before any mainnet path ships.
- CI runs `govulncheck` and `gosec`; deps pinned with `go.sum`.

## Commands

**Local dev hazard:** a parent `go.work` on the author's machine references a missing sibling module, so local `go`/`wails` commands need `GOWORK=off` (and `GOTOOLCHAIN=auto`, since go.mod pins go 1.26.0 / toolchain go1.26.7). CI does **not** need these (standalone checkout). The build emits an unrelated gopsutil/IOKit cgo deprecation warning — not an error.

- **Run / build the app:** `GOWORK=off wails dev` (run), `GOWORK=off wails build` (package). Linux build needs `-tags webkit2_41` (+ `libgtk-3-dev libwebkit2gtk-4.1-dev`).
- **Backend tests:** `GOWORK=off GOTOOLCHAIN=auto go test ./...` (plus `go vet ./...`, `go build ./...`). Integration/live-node tests are behind `//go:build integration` and need `ZNN_NODE_URL` (e.g. `... go test -tags integration ./internal/spike -run TestReadOnly... -v`).
- **Frontend** (in `frontend/`, pnpm 10.17.1): `pnpm install --frozen-lockfile`, `pnpm run typecheck` (vue-tsc), `pnpm test` (vitest + @vue/test-utils), `pnpm run build` (Vite). nom-ui ships uncompiled source, so the build carries `tailwindcss-animate` + a couple of tsconfig accommodations.
- **Security gates:** `bash scripts/govulncheck-gate.sh` (allowlist gate over `govulncheck ./...`), `gosec -conf .gosec.json ./...`.
- **CI:** `.github/workflows/ci.yml` runs on PR→main / push→main — jobs `frontend`, `security`, and a `build-test` matrix (ubuntu/macOS/windows: go vet/test + `wails build`).
