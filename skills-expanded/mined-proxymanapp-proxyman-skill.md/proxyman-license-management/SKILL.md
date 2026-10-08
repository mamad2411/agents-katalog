---
name: "proxyman-license-management"
description: "Safely activate, unlink, revoke, transfer, and manage Proxyman licenses and device seats. Use for license keys, activation failures, deactivation, License Manager, old devices, purchase emails, seat assignment, renewal, corporate proxy activation, or moving a license."
---

# Proxyman License Management

Handle license tasks with minimal secret exposure and an explicit distinction between the current app, `proxyman-cli`, and the web License Manager.

## Verify Current Official Guidance

Before giving entitlement, seat-count, renewal, supported-platform, or portal instructions:

1. Fetch `https://docs.proxyman.com/llms.txt`.
2. Fetch the current License and License Manager `.md` pages listed there.
3. Follow the License Manager access-link URL from the freshly fetched official page. Do not hardcode or guess the portal domain because official Proxyman domains and redirects can change.
4. Avoid hardcoding prices, device allowances, subscription terms, or trial terms; these can change.

Read [license workflows](references/license-workflows.md) for operation-specific checks.

## Protect The License Key

Treat a Proxyman license key, purchase email, activation response, and License Manager access link as secrets.

- Never repeat the full key in chat, logs, screenshots, issue text, or final output.
- Never ask the user to paste the key into chat or an agent tool call.
- Ask the user to enter a key directly in Proxyman when GUI activation is possible.
- Prefer GUI activation for ordinary use because a CLI argument may remain in shell history or appear in process inspection.
- The reviewed CLI accepts the key only as a positional argument. Never execute that form with a real key through the agent host. Discover the installed help, provide a command shape containing `<LICENSE_KEY>`, and have the user substitute the key and run it directly in their own terminal.
- Only reconsider agent-side CLI activation if version-matched help explicitly exposes a non-argument secret input such as stdin, a file descriptor, or an interactive prompt, and the user authorizes that method.
- Do not save the key in a script, repository, skill, environment file, or shell profile.
- Do not access the user's mailbox unless an available email connector is explicitly authorized for that task.

## Route The Request

### Activate This Device

Preferred GUI path:

1. Open Proxyman's License/Activate screen.
2. Have the user paste the key directly into the app.
3. Activate and verify the app shows the expected licensed state and account email.

CLI path is currently supported on macOS builds that include `proxyman-cli`. Use the `proxyman-cli` skill and discover `activate --help`, but do not execute the reviewed positional-argument form through the agent host. Give the user a verified command shape with `<LICENSE_KEY>` so they can substitute the key and run it directly in their terminal. After the command succeeds, have the user restart Proxyman before verifying the licensed state. Do not quit the app on their behalf unless they explicitly authorize it.

If activation fails, collect the exact sanitized error, app version/platform, current license state, network reachability, and external/corporate proxy state. Do not repeatedly retry a key or guess its validity.

### Activate Proxyman For iOS

Fetch the current iOS activation section from the official License page because navigation and device entitlements can change. Have the user enter the key directly in the standalone iOS app's protected license/unlock screen, then verify the app shows the licensed state. The reviewed desktop MCP and `proxyman-cli` do not activate the standalone iOS app; do not claim parity.

### Unlink This Device

Unlink affects the active device and may contact the license server before local license data is removed. Treat it as destructive.

1. Confirm the user means the current device.
2. Verify current licensed state.
3. Explain that access on this device will be removed.
4. Use the GUI unlink action or version-matched `proxyman-cli unlink` only after immediate confirmation.
5. Verify the app is no longer activated.

Do not use unlink when the user needs to recover a lost, replaced, or unavailable device; use License Manager.

### Revoke Or Remove Another Device

Use License Manager, not the local unlink command.

1. Open the official access-link page.
2. The user enters the purchase email or license key on the official site.
3. Proxyman sends an access link to the purchase email; the user opens it themselves unless they explicitly authorize mailbox access.
4. Identify the exact device/seat using the portal's metadata.
5. Confirm immediately before remove/revoke/transfer.
6. Verify the device is gone or the seat is available, then activate the replacement device separately.

Never guess which device to revoke based only on a generic name.

### Manage Seats, Emails, Transfer, Or Renewal

Use the current License Manager page and portal UI. First establish the user's license type and the desired device/email/seat. Describe any billing or entitlement consequence shown by the portal and require confirmation before the final action.

There is no general Proxyman MCP action for license management and no documented public License Manager automation API in this package. Do not improvise HTTP calls or scrape authenticated portal state.

## Corporate Proxy Or Network Failure

- Confirm general connectivity and capture the sanitized activation error.
- If the environment requires an upstream proxy, configure Proxyman's External Proxy using the current official guide. Ask before sending credentials.
- Recheck system date/time and TLS interception policy if the error indicates certificate or connection failure.
- Do not disable security controls or advise sharing the key with support logs.

## Finish With

- operation requested and surface used (GUI, CLI, or License Manager);
- device/account target without secret values;
- verified result or exact sanitized blocker;
- next safe action, including replacement-device activation when relevant.
