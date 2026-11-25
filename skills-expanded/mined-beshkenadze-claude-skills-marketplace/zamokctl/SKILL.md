---
name: zamokctl
description: Use when generating/managing the offline root signing key or signing & publishing Zamok product keysets from the terminal (the Swift CLI; the ZamokApp GUI is the co-equal interface). Triggers — "generate root key", "rotate root", "publish keyset", "sign keyset", "escrow root key", "zamokctl", "trusted-roots.json", Tish/Zamok license signature setup.
version: 1.0.0
---

# zamokctl — Zamok offline signing CLI

`zamokctl` (Swift, target in `apps/macapp`) and the **ZamokApp GUI** are two thin interfaces over
one shared `ZamokSigning` core. They share the **same root key in the macOS Keychain** and the same
`/draft → confirm → verbatim-sign → /publish` flow. There is no bun/TS signing CLI (removed).

## Trust model (read once)
- **Root key = offline trust anchor.** Private lives ONLY locally (macOS Keychain, service
  `app.bshk.zamok.root-key`, one item per `kid`); the server never holds it and cannot sign.
- **Per-product roots.** A product's keyset is verified only against that product's roots, listed
  (public keys) in the committed `packages/signing-keys/trusted-roots.json`
  (`{ "<slug>": [{kid,pem}] }`). Adding/rotating a root = edit that file → PR → deploy (audited;
  not env, not admin-mutable).
- **Keychain is `ThisDeviceOnly`** → does NOT survive a wiped/new Mac. **Always escrow** the
  exported `.age` + `.identity` to a vault (e.g. 1Password `op document create`). Escrow = recovery.
- The CLI is ad-hoc-signed/unentitled → uses the file/login keychain; **no per-use biometric prompt**
  (a future hardening needs a keychain-access-group entitlement + data-protection keychain).
- JWS: `alg=EdDSA`, header `kid`, payload = the **verbatim** `/draft` `payloadJson` bytes.
  `kid = "root_" + base64url(sha256(spkiDer))[:16]`.

## Getting the binary
Homebrew (`zamokctl` on PATH) — see `apps/macapp/Distribution/Homebrew/`. Dev build:
`cd apps/macapp && xcodebuild -scheme zamokctl -configuration Debug -derivedDataPath build/cli build`
→ `build/cli/Build/Products/Debug/zamokctl`.

## root-key
```bash
zamokctl root-key generate                 # new Ed25519 root → Keychain; prints kid + public PEM
                                            # + reminds you to export/escrow immediately
zamokctl root-key list                      # kid + created date of local roots (no prompt)
zamokctl root-key export --kid <kid> --out ~/zamok-escrow
                                            # writes <kid>.age + <kid>.identity → escrow BOTH in a vault
                                            # (.identity decrypts .age — keep secret)
zamokctl root-key import --kid <kid> ...    # restore from an age escrow or a raw private PEM
```
Generate one root **per product** for isolation (compromise/rotation stays scoped to one product).

Escrow to 1Password:
```bash
op document create ~/zamok-escrow/<kid>.age      --title "Zamok root [<product>] <kid>.age"      --vault Private --tags zamok-root-key,<product>
op document create ~/zamok-escrow/<kid>.identity --title "Zamok root [<product>] <kid>.identity" --vault Private --tags zamok-root-key,<product>
# restore: op document get <uuid> --out-file <kid>.age  (+ .identity) → zamokctl root-key import
```

## keyset
```bash
zamokctl keyset publish --product <slug> [--kid <root>]
# 1. GET /api/product-keysets/draft?productId=…   (admin auth via `zamokctl auth login`)
# 2. renders the draft FROM the signed bytes: productSlug, version, each key purpose·kid·sha256(pub)[:16]
#    + a DIFF vs the currently published keyset — REVIEW added/removed/changed keys
# 3. confirm (or --yes in CI, which echoes the diff) → signs the verbatim payloadJson with the root
# 4. POST /api/product-keysets/publish
```
Signs the **exact bytes it showed you** (single fetch, no refetch) and aborts if the server's
display `payload` ≠ the signed `payloadJson` — a compromised server can't get attacker keys
root-signed without you approving an anomalous key list.

## Full rollout / rotation
1. `zamokctl root-key generate` (per product) → `export --out ~/zamok-escrow` → escrow in vault.
2. Add the root's **public** key under the product slug in `packages/signing-keys/trusted-roots.json`
   → PR + merge + deploy (server now trusts it).
3. `zamokctl auth login`, then `zamokctl keyset publish --product <slug>` per product.
4. Rebuild + ship the client embedding `trustedRootPublicKeysPEM` + `initialProductKeysetJWS` from
   `GET /api/product-sdk-setup/<productId>`.
5. Verify a clean client: license activates + cloud responses verify. Server `GET /api/health` is
   `degraded` until each product has a trusted root AND a keyset signed by it.

## Gotchas
- Rotating the **root** means re-shipping clients — rare, deliberate. Rotating a **per-product
  signing key** = republish the keyset; clients auto-pick it up, no rebuild.
- Keep `trusted-roots.json` changes in PRs — it's the trust anchor; never make it env/DB-mutable.
- `OSStatus -50`/`-34018` from the keychain store = an outdated build; use the file-keychain store
  (no data-protection keychain / access groups for the unentitled CLI).
