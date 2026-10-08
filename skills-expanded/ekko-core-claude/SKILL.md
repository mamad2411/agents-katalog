# Ekko core — session bootstrap

The browser extension (`src/`) + the self-hostable key directory (`server/`, zero npm
dependencies). Post-quantum encrypted messaging on top of the apps people already use. New wire
output is `EKK1*` and readers keep `RSN1*` compatibility (see `docs/PROTOCOL.md` — internal KDF
labels are frozen on purpose). The iOS half lives in github.com/useekko/ekko-ios.

**Read `docs/ADAPTERS.md` and `docs/DESIGN.md` before touching a messenger adapter or any UI;
`docs/DIRECTORY.md` before touching `server/`.**

## The invariants — break these and the product is a lie

- **Private keys never leave the device.** Servers see public keys only. If a change would put a
  private key, a passphrase, or a plaintext anywhere but the user's device, the change is wrong.
- **An adapter must never guess the recipient.** If it cannot identify the peer, it fails VISIBLY
  (the muted "identifying this chat" glyph). Encrypting to the wrong person is worse than not
  encrypting, because the user believes they are safe.
- **`src/core` and ekko-ios's `EkkoCore` must agree byte for byte.** The Swift repo's committed
  interop vectors are generated from THIS repo's TypeScript; a crypto change updates both sides.
- **Mono is machine output only** (ciphertext, safety numbers, the 24 words) — never a label.
- **Verification is server state, never a client guess.** Never render "verified" from a local
  assumption. That bug has already shipped once. Server-side, exactly ONE code path sets
  `verified_at` (`verifyPlatformHandle` in `server/src/store.mjs`) — never add a second door.
- **No overclaiming in copy.** Never "unbreakable", never "military-grade". Say what is true,
  including what an attacker can still reach (`docs/THREAT_MODEL.md`).

## Gotchas that have each cost a day

- Safari rejects `"type": "module"` service workers, so the background is rebuilt as an IIFE by
  `scripts/ios-safari-sync.mjs`. Without it Safari loads the extension with **no background at all**.
- Safari on macOS cannot load an unpacked extension: it needs a signed container app.
  `scripts/mac-safari.sh` builds one. "Allow Unsigned Extensions" resets whenever Safari quits.
- Messengers re-render their composers mid-send (Meta's Lexical editor ignores execCommand);
  composer writes go through the shared Selection-based writers in `src/content/dom.ts` — do not
  reintroduce execCommand paths.

## Working here

- `npm test` + `npm run typecheck` must be green before any PR; `cd server && npm test` too if
  you touched the directory.
- Branch `feat/*`, open a PR, no direct pushes to `main`.
