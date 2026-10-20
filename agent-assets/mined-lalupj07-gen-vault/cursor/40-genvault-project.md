---
description: GenVault project context; overrides generic web rules where more specific
alwaysApply: true
---

# GenVault Project Rules

Stack: Tauri 2 (Windows + Android), Rust core in `src-tauri/`, Next.js static export UI in `src/`. Offline, zero-knowledge vault: AES-256-GCM, Argon2id, TOTP + passwords. Android package `com.genvault.auth`.

Project docs (read only what the task needs): `.devin/skills/Gen Vault/` (`SKILL.md`, `security_rules.md`, `crypto_rules.md`, `architecture.md`, `testing_rules.md`, `windows_rules.md`, `release_checklist.md`).

## Applying the generic rules here

- No server, API routes, cookies or third-party scripts ship in the app. Auth/session rules map to the local unlock session, auto-lock and travel/duress/panic modes in Rust.
- `30-launch-checklist` and `website-compliance-gate` apply to the marketing site (genxisinnovation.in) and store listings, not the app shell. Store copy (`store/`) must match real behaviour.
- `20-copy-rules` apply to in-app UI and store copy.
- Release audits use `.cursor/skills/preproduction-security-audit`, with Phase 17 (mobile) and Phase 19 (cargo + npm + gradle deps) in scope.

## Hard rules

- Never log or return secrets, TOTP seeds, passwords, master keys or usernames. No plaintext seeds on disk.
- Secret material lives in `Zeroizing` / zeroize-on-drop types. Compare secrets in constant time.
- Travel mode blocks export, restore and autofill. Duress shows only the decoy vault. Keep these gates in Rust, not only in UI.
- Never commit keystores, `keystore.properties` or signing passwords. Use `store/keystore.properties.example`.
- Security-sensitive changes need a negative test in `src-tauri/tests/`.
