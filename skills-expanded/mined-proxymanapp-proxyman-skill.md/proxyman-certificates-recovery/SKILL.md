---
name: "proxyman-certificates-recovery"
description: "Safely manage Proxyman certificates and destructive recovery workflows on macOS. Use for generated or custom root certificates, custom server or client certificates, Copy Debug Info, Debug Mode, Reset Network Proxy, or Factory Reset. Do not use for ordinary display preferences or device-specific CA setup."
---

# Proxyman Certificates And Recovery

Keep certificate roles, trust, diagnostics, and reset scope separate. These operations can change the macOS trust store, disclose private-key material, interrupt live TLS connections, or delete Proxyman data.

## Select The Relevant Reference

- Read [Root certificates](references/root-certificates.md) for the generated Proxyman CA, automatic/manual trust, custom root import, replacement, removal, MCP, or CLI boundaries.
- Read [Custom server and client certificates](references/custom-server-client-certificates.md) for TLS-to-client certificates, mTLS client identity, PEM/DER/P12 imports, host/port matching, replacement, or CLI automation.
- Read [Diagnostics and recovery](references/diagnostics-and-recovery.md) for Copy Debug Info, Debug Mode, Reset Network Proxy, data/backup folders, or Factory Reset.

Read more than one reference only when the task crosses those boundaries.

## Establish Current Behavior

1. Identify the installed Proxyman version, distribution, and whether the task is GUI, MCP, or CLI driven.
2. Fetch `https://docs.proxyman.com/llms.txt` when current behavior matters, then fetch the selected official `.md` page and cite its public URL.
3. Use the installed UI, live MCP schema, or installed `proxyman-cli --help` as the exact interface authority. The bundled references are a reviewed macOS snapshot.
4. If no dedicated public page exists for Debug Mode or Factory Reset, say so and use the installed Help menu plus the source-grounded behavior in this skill.

Do not generalize this macOS trust/Keychain workflow to Windows, Linux, mobile devices, simulators, Java, Firefox, or containers. Route target-specific trust setup to `proxyman-https-capture`.

## Classify Before Acting

- **Generated Proxyman root CA:** Proxyman generates the signing identity used for ordinary HTTPS interception; install and trust it on the current Mac.
- **Custom root CA:** replaces the generated signing identity inside Proxyman and must include its private key.
- **Custom server certificate:** Proxyman presents it to matching clients based on certificate names; it is not an upstream mTLS identity.
- **Custom client certificate:** Proxyman presents it to one configured upstream host and port for mutual TLS.
- **Debug Mode:** increases production console diagnostics; it is not a reset and does not export a support bundle.
- **Factory Reset:** removes certificates and preferences, with an optional broader deletion of app-managed data including rules and backups.

If the user says only “add a certificate,” ask which TLS direction and goal. Choosing the wrong role can break handshakes or widen trust unnecessarily.

## Safe Operating Workflow

1. Inspect current certificate/status/rule state and record the exact item being changed.
2. Pause or finish important captures before any custom-certificate mutation; the reviewed app closes live connections when custom certificate state changes.
3. Preserve recoverable inputs outside Proxyman-managed folders: original certificate/key files, passwords in the user's approved secret store, relevant debugging-rule exports, and any required logs/backups.
4. Explain the exact trust, routing, secret, interruption, or deletion effect.
5. Obtain confirmation immediately before a privileged trust-store change, certificate/private-key import or deletion, Reset Network Proxy, or Factory Reset. For Debug Mode, an explicit request to enable it is sufficient; agree on the reproduction and log-sharing scope before launching the app from Terminal or sharing output.
6. Make one scoped change. Do not retry a password/sudo/Keychain failure repeatedly; inspect the resulting partial state first.
7. Verify through an independent status and a fresh controlled TLS connection or post-relaunch state.
8. Restore the prior certificate/configuration or disable diagnostics after the requested result is captured.

## Interface Boundary

- GUI is the complete reviewed interface for generated and custom certificates, Debug Mode, and Factory Reset.
- MCP can inspect current root status, generate/install the default Proxyman CA, and remove the current managed root. It cannot import or CRUD custom root/server/client certificates or invoke Debug Mode/Factory Reset.
- `proxyman-cli install-root-cert` imports a custom P12 root; `custom-cert` manages P12 server/client certificates. Discover version-matched help before constructing commands.
- Reviewed GUI supports PEM/DER certificate plus matching private key or P12 for server/client certificates. Reviewed CLI supports P12 only.
- Factory Reset and Debug Mode are GUI-only. Never emulate Factory Reset by recursively deleting Application Support or Keychain content.
- `proxyman-cli export` backs up debugging-tool rules only. It is not a backup of App Settings, certificates/private keys, captured sessions, license state, or Proxyman's backup folder.

Route ordinary Settings-tab questions to `proxyman-app-settings`, capture/trust on another target to `proxyman-https-capture`, and exact CLI execution to `proxyman-cli`.

## Sensitive Data Rules

- Never read, paste, or retain a private key, P12 payload, passphrase, sudo password, Keychain token, captured TLS secret, or full console log unless the user explicitly approves the exact exposure.
- Prefer GUI password prompts. The reviewed CLI accepts certificate passwords as arguments, which can expose them through shell history or process inspection; provide placeholders for user-run commands rather than receiving the real secret.
- Import only certificates the user owns or is authorized to use. A custom server certificate does not authorize bypassing pinning in a third-party production app.
- Preview debug information and console logs before copying or sharing them with support.
