# Desktop Application Security

## Purpose
Harden desktop applications at their unique trust boundaries: IPC channel validation, custom protocol/deep-link handling, signed auto-update verification, OS sandbox and entitlement confinement, and secret storage in platform keychains — with fail-secure defaults throughout.

## Use when
- Auditing or implementing IPC (Electron ipcMain/ipcRenderer, Tauri commands, native messaging) and its validation.
- Handling custom protocol handlers, deep links, file-open events, or drag-drop payloads from untrusted sources.
- Implementing auto-update with signature verification (Squirrel, Sparkle, custom feed).
- Confining the app with OS sandbox profiles/entitlements and storing secrets in Keychain/Credential Manager/libsecret.

## Do not use when
- Securing browser-only web apps without native bridges (use `api-security`, `auth-security`).
- General network transport hardening without desktop specifics (use `network-security`).
- Signing or notarizing release binaries for store submission rather than runtime enforcement (release engineering concern).

## Required context
- IPC surface inventory: channels, message schemas, and privilege of each endpoint.
- Native integration points: protocol handlers, deep links, auto-update feed URLs.
- Sandbox/entitlement model and secret-storage mechanism (keychain/libsecret).

## Procedure
1. **Map Trust Boundaries**: Draw the boundary between untrusted (renderer, deep links, dropped files, update feed) and privileged (main process, filesystem, keychain). Every crossing gets a numbered entry: channel, direction, data schema, privilege required.
2. **Validate IPC Strictly**: Allowlist channels; validate every message against a schema (types, ranges, string lengths) in the privileged side before acting. Example: `open-file` accepts only absolute paths under the workspace root, resolved with symlink evaluation, rejected otherwise. Never expose raw `fs` or `shell` to the renderer.
3. **Quarantine Protocol & File Input**: Treat custom-protocol URLs and opened files as attacker-controlled. Parse with strict grammars, enforce size caps, and open documents in a sandboxed parser before granting broader access. Log and reject malformed payloads.
4. **Pin Auto-Update**: Verify update manifests and binaries against pinned public keys (Ed25519/minisign or platform equivalent) before install; enforce HTTPS with no downgrade; require version monotonicity (never install an older build). A failed signature aborts the update and alerts, never retries silently.
5. **Confine & Store Secrets Right**: Apply least-privilege entitlements (no JIT/network/filesystem beyond need); store tokens in Keychain / Credential Manager / libsecret — never in plaintext config or localStorage. Memory holding secrets is zeroed after use.
6. **Verify**: Run `scripts/verify.sh`. Prove with abuse tests: malformed IPC rejected, traversal deep-link blocked, tampered update refused, sandbox escape attempt contained.

## Decision rules
- **Renderer Is Attacker**: The renderer process is untrusted; all security decisions execute in the privileged side.
- **Fail Securely**: Validation failure denies the operation and logs; it never degrades to a permissive fallback.
- **Signatures Before Install**: No update binary executes without a verified signature from a pinned key.
- **No Plaintext Secrets**: Credentials in plaintext files, logs, or localStorage are release-blocking findings.

## Evidence required
- IPC boundary map with per-channel schemas and privilege levels.
- Abuse-test logs: malformed IPC, traversal payloads, tampered updates, sandbox probes.
- Entitlement manifest and secret-storage audit.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Desktop threat-model audit with IPC and update-channel findings.
- IPC validation and update-signature enforcement patches.
- Sandbox-escape and protocol-handler abuse test evidence.

## Stop conditions
- IPC validated, updates signature-pinned, sandbox enforced with passing abuse tests.
- Zero plaintext-secret or raw-capability exposures remain.
- Token budget exhausted.

## Escalation rules
- Escalate to lead architect if a required native capability has no sandboxed API (needs platform-risk acceptance).
- Escalate immediately on discovery of an exploitable renderer-to-main escape or update-spoofing vector.
