---
name: ext-native-messaging
description: Browser-extension ↔ native-host bridge via Native Messaging. Auto-invoked when designing the extension/native boundary, debugging stdio framing, or handling installation of the native host.
---

# Extension Native Messaging

Native Messaging is a narrow, security-critical pipe: the extension is sandboxed,
the native host is not. Every byte that crosses the boundary is an authorization
decision, and every framing bug is a silent hang.

## When to reach for this

- Designing the message schema between extension and native host
- Debugging stdio framing ("Native host has exited", hangs, truncated reads)
- Writing the host manifest and its per-OS, per-browser install step
- Deciding what a connected extension is allowed to make the host do

## Principles

1. **Treat the bridge as an RPC boundary.** Small explicit command enum with a
   version field; reject anything unknown. Never eval, never shell-out on
   payload-supplied strings, canonicalize payload-supplied paths before use.
2. **Lock the allowlist hard.** `allowed_origins: ["chrome-extension://<EXACT-ID>/"]`
   — one production ID. Ship a separate manifest for dev builds. A wildcard or a
   leftover dev ID here is a sandbox escape for whoever holds that ID.
3. **Assume the extension is compromised.** Authorize per command, not per
   connection. High-privilege actions (file writes outside a sandbox dir, process
   launch, credential access) require a native-side user confirmation.
4. **Framing is a 4-byte length prefix + UTF-8 JSON** (native byte order —
   little-endian on every platform you will ship). Chromium caps host→extension
   messages at 1 MB. Validate the length before allocating, drain the full
   payload, parse with a size cap — a mismatched prefix shows up as a hang or
   "host has exited", never as a clean error.
5. **Choose connection mode deliberately.** `runtime.sendNativeMessage` spawns a
   host process per message — fine for occasional calls. `runtime.connectNative`
   keeps one process per port: supervise it and exit cleanly on stdin EOF, or you
   leak orphan processes.
6. **Version-gate on connect.** First exchange is a version handshake. If the
   host is older than the extension expects, return a structured
   `upgrade_required` reply — don't crash, don't pretend to work.

## Host manifest install matrix

| Browser / OS | Per-user location |
|---|---|
| Chrome, Windows | `HKCU\Software\Google\Chrome\NativeMessagingHosts\<name>` → path to manifest JSON |
| Chrome, macOS | `~/Library/Application Support/Google/Chrome/NativeMessagingHosts/<name>.json` |
| Chrome, Linux | `~/.config/google-chrome/NativeMessagingHosts/<name>.json` |
| Firefox, Windows | `HKCU\Software\Mozilla\NativeMessagingHosts\<name>` |
| Firefox, macOS / Linux | `~/Library/Application Support/Mozilla/NativeMessagingHosts/` · `~/.mozilla/native-messaging-hosts/` |

Chromium reads `allowed_origins`; Firefox reads `allowed_extensions` (extension
IDs, no `chrome-extension://` scheme) — most cross-browser hosts ship one manifest
per browser. Per-user install avoids admin prompts; system-wide (HKLM,
`/Library/...`, `/etc/...`) is for managed deployments. A defensive reader-loop
and handshake skeleton is in
[`references/host-skeleton.md`](references/host-skeleton.md).

## Pitfalls

- Writing JSON without the length prefix (or with the wrong width/order) — the
  browser reports only "Native host has exited"
- Logging to stdout — stdout *is* the transport; logs go to stderr or a file
- One manifest for dev and prod with both extension IDs in the allowlist
- Forgetting the native host needs its own installer *and uninstaller* — the
  store ships only the extension; the "install companion app" prompt and version
  matching are part of first-run, not an afterthought
- No timeout on host replies — a wedged host hangs the feature silently

---
*Related: `ext-security` (message validation, trust boundaries),
`ext-permissions` (justifying the `nativeMessaging` permission), `ext-ux`
(companion-app install prompts) · domain agent: `ext-architect` · output/ADR
format: `playbook-conventions`*
