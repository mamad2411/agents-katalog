---
name: desktop-shell-integration
description: OS shell integration — context menus, file associations, protocol handlers, Spotlight / search, Quick Look, jump lists, dock badges. Auto-invoked when implementing native integrations, debugging why associations don't stick, or cleaning up after uninstall.
---

# Desktop Shell Integration

Shell integration is where an app stops feeling like a port and starts feeling
native — and it's the most under-documented surface in desktop development: every
OS does it differently, every version changes something, and half the APIs are
"deprecated but still required."

## When to reach for this

- Registering file associations, URL/protocol handlers, or context-menu entries
- Debugging associations that don't stick or defaults that silently reset
- Adding search/preview integration (Spotlight importer, Quick Look, Windows Search) or dock/taskbar features (badges, jump lists, progress)
- Auditing what shell artifacts an uninstall must remove

## Principles

1. **Per-OS parity is a myth — aim for per-OS idiom.** A "shell extension" is a
   registry entry on Windows, a separately-signed App Extension target on macOS,
   and a MIME + `.desktop` combo on Linux. Model them as three designs, not one.
2. **Sparse Package on Windows.** COM-registered DLLs are the legacy path; MSIX
   Sparse Packages let unpackaged apps register shell extensions cleanly and
   unregister on uninstall. Default to them.
3. **Validate every deep-link payload.** Inbound protocol-handler URLs are an
   attack surface: parse with a strict grammar, treat query params as untrusted,
   reject malformed input, and never build shell commands from them.
4. **Respect user defaults.** Never re-assert default-handler status on launch —
   that's malware behavior. Prompt once, persist the decline, and offer "make
   default" in settings.
5. **Uninstall means uninstall.** Every hook added must be removed: orphaned
   ProgIds, stale MIME entries, lingering LaunchAgents. Ship a verification
   checklist alongside the registrations.
6. **Verify with the OS's own tools, not the UI.** `assoc` / `ftype` on Windows,
   `lsregister -dump` on macOS, `xdg-mime query default` on Linux — these are
   ground truth; settings panels sometimes lie.

## Registration matrix

| Integration | Windows | macOS | Linux |
|---|---|---|---|
| File association | ProgId under `Software\Classes` (HKCU for per-user) | UTI + `CFBundleDocumentTypes` in Info.plist | MIME XML + `MimeType=` in `.desktop`, then `update-mime-database` + `update-desktop-database` |
| URL scheme | `Software\Classes\<scheme>` with `URL Protocol` value | `CFBundleURLTypes` | `x-scheme-handler/<scheme>` in `.desktop` |
| Context menu | Sparse Package shell extension (COM DLL only if forced) | Finder/App Extension target, own signing | Nautilus/Dolphin file-manager extension |
| Login item | `Run` key or Startup folder | LaunchAgent / `SMAppService` | XDG autostart or systemd user unit |
| Verify | `assoc .ext` / `ftype <ProgId>` | `lsregister -dump \| grep <bundle-id>` | `xdg-mime query default <mime>` |

Match registration scope to install scope: a per-user install writes HKCU and
`~/Library` / `~/.local/share`, never HKLM or system domains.

## Pitfalls

- Re-asserting yourself as default handler on every launch
- Deep-link handlers passing URL fragments into shell commands or file paths unvalidated
- Per-user installs writing HKLM (elevation failure) or system installs writing only the installing user's hive
- macOS associations "not working" because LaunchServices cached a stale bundle — re-register rather than fighting the cache
- Forgetting `update-mime-database` / `update-desktop-database` after writing Linux MIME and `.desktop` files
- Uninstall leaving ProgIds, scheme handlers, or LaunchAgents that point at a deleted binary

---
*Related: `desktop-installer` (writes these registrations at install time),
`desktop-ipc` (deep-link payload crossing into the app), `desktop-code-signing`
(App Extension signing, entitlements), `security-checklist` · domain agent:
`desktop-architect` · output/ADR format: `playbook-conventions`*
