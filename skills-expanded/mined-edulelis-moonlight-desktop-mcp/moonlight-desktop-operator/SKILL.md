---
name: moonlight-desktop-operator
description: Operate a paired Apollo Windows desktop through the configured moonlight-desktop MCP. For visible Windows tasks, start the Desktop stream, capture the UI, send coordinate-matched input, and verify the rendered result.
---

# Moonlight Desktop Operator

Use the `moonlight-desktop` MCP for authorized Windows GUI tasks on the paired
Apollo host. The MCP runs on the invoker and sends video/input over compatible
Moonlight/GameStream transport.
It controls the remote desktop in the active session, not the invoker's local
operating system. A paired profile alone is not proof that a remote desktop is
ready for input: start a session and inspect a current screenshot first.

Stop and let the user complete account sign-in, credential or one-time-code
entry, license activation, and terms or EULA acceptance.

If the target PC is offline, a profile with Wake-on-LAN settings wakes it during
`session_preflight` or `session_start`. Configure it first with
`profile_wol_configure` using a MAC address and LAN broadcast address supplied
by the user or their Moonlight profile; do not guess those network values.

## Operating loop

1. Call `desktop_channel_status` first. Confirm this dedicated headless
   Desktop channel is ready, identify its paired target and any occupied local
   transport or pending launch preparation, and follow `nextAction`. Never
   start a second session while launch preparation is in progress. Refuse
   generic GUI computer-use fallback because it would operate a local
   controller window instead of the remote Desktop.
2. For setup/readiness concerns, call `runtime_status`; then call
   `profiles_list` and `session_preflight` as appropriate. If pairing is
   required, `pairing_begin` returns the PIN and the Apollo web URL.
3. Call `session_start` for the virtual **Desktop**. Use
   `provider_app_start` only for an explicitly requested Apollo/Moonlight
   provider app.
4. Call `screen_capture` and treat its `snapshotId` and dimensions as the
   coordinate source for the next action. Locate targets through visible
   reasoning, `screen_find_text`, `screen_ocr`, or template matching.
   Establish app availability, installer progress, account state, and license
   state from that current capture rather than controller-local assumptions or
   a provider-app registry.
5. Send the smallest fitting input. Prefer `session_mouse_click_at`, named
   key presses, and named hotkeys to independent low-level events.
6. Verify visibly. Use `session_wait_for_change` for material updates and a
   focused region for animated apps. Use `screen_wait_for_text` for visible
   dialogs, menus, and completion notices.
7. Call `session_stop` after success, failure, or ambiguity.

## Boundaries

- Desktop visual interaction is the default. A desktop icon need not appear in
  Apollo's provider-app list.
- Do not force-kill apps unless the user explicitly requests force close.
- Ask when the requested target is materially ambiguous. For example,
  “increase volume” can mean Windows master volume or an app’s own setting.
- Do not save, submit, delete, purchase, send, expose credentials, or finalize
  another consequential action without user authorization.
- If Apollo reports another stream owns the channel, report that exact
  condition and stop.
- Do not claim success before an appropriate visible check confirms it.
