---
name: desktop-autoupdate
description: Autoupdate specialist. Owns update channels, delta / full download, signature verification, rollback, staged rollout, and update UX. Auto-invoked when designing, changing, or debugging the update mechanism.
---

# Desktop Autoupdate

An app that can't update itself safely is a liability; an update that can't roll
back is a bigger one. The updater is remote code execution by design — signature
verification and staged rollout are what keep it from being remote code execution
for someone else.

## When to reach for this

- Designing or swapping the update mechanism (Squirrel, Sparkle, Tauri updater, MSIX, custom)
- Adding channels (stable / beta / nightly / enterprise) or staged rollout gating
- Debugging failed, looping, or partially-applied updates
- Deciding update UX: mandatory vs optional vs deferred, and the restart flow

## Principles

1. **Verify the artifact signature before swap** — never execute unverified bytes.
   TLS on the feed is not enough; a compromised CDN bucket defeats it. Verify the
   downloaded artifact's signature against a key you ship, then swap.
2. **Staged rollout by default** — 1% → 10% → 50% → 100% over days, never all at
   once. Build the percent gate into the feed/server, not the client.
3. **Telemetry-gated promotion** — crash-free rate and update-success rate must
   stay flat against the previous version before each stage advances; auto-halt
   on regression. A rollout without a kill switch is a rollout you can't stop.
4. **Rollback is a feature** — keep the previous version installed (or one
   download away) and make reverting a published, tested path, not an incident
   improvisation.
5. **Delta with full fallback** — deltas only apply against a verified base hash;
   on any mismatch, fall back to the full download instead of patching blindly.
6. **Mandatory updates are rare** — reserve them for security fixes, always
   explain why, and never block the user mid-task to restart.

## Framework defaults by stack

| Stack | Default updater | Notes |
|---|---|---|
| Electron | `electron-updater` | macOS path requires a signed + notarized app; Squirrel.Windows on Windows |
| macOS native | Sparkle 2 | EdDSA-signed appcast; works sandboxed |
| Tauri | `tauri-plugin-updater` | minisign signatures; key generated at project setup — custody it like a signing cert |
| Windows (Store/MSIX) | MSIX | OS handles download/swap; channel + staging configured via App Installer |

Update flow to design and test end-to-end: **check → download → verify → stage →
swap → restart**, with explicit behavior defined for a failure at each arrow.

## Pitfalls

- Trusting HTTPS alone and skipping artifact signature verification
- Delta applied against the wrong base — always hash-check the *resulting* artifact, not just the patch
- No server-side kill switch; halting a bad rollout requires shipping another update
- Update check blocking app startup or running on the UI thread
- Restart loops when an update fails repeatedly — cap retries, then fall back to a full download
- Rotating the signing identity mid-channel without a transition plan, which breaks updaters that pin the publisher

---
*Related: `desktop-code-signing` (keys, notarization, identity rotation),
`desktop-installer` (initial install vs update path), `security-checklist` ·
domain agent: `desktop-architect` · output/ADR format: `playbook-conventions`*
