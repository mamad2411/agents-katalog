---
name: secrets-manager-automation
description: Securely connect automation and SSH workflows to password managers and secrets stores using interactive sessions, scoped machine identities, least-privilege vaults, and non-leaking verification.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [secrets, password-manager, service-account, ssh, cli, automation, least-privilege]
created_by: agent
---

# Secrets Manager Automation

Use this skill when a user wants an agent, cron job, SSH shell, CI process, or local application to retrieve secrets from a password manager or secrets service.

The goal is unattended access without turning a human account password into a reusable machine secret. Prefer provider-native machine identities and narrowly scoped vaults over plaintext passwords, broad personal-vault access, or long-lived interactive sessions.

## Safety Contract

1. **Never request, type, echo, log, or persist a human account/master password.** Explicit user acceptance of the risk does not make plaintext password automation a sound design.
2. **Do not put passwords in command arguments or shell history.** Use provider prompts for interactive sign-in; terminal echo must be disabled by the provider.
3. **Separate human and machine authentication.** Human unlock is for interactive use; service accounts/workload identities are for unattended automation.
4. **Use least privilege.** Start with read-only access to a dedicated automation vault containing only required items. Add write/delete/share privileges only for a concrete workflow.
5. **Never print tokens or secret values during setup or verification.** Redirect one-time credentials directly to a protected store and report only sanitized account/vault names, permission sets, counts, and success state.
6. **Treat environment variables as process-visible secret transport, not permanent storage.** If a provider requires an env token, source it from a mode-restricted file, systemd credential, OS keychain, or secret injection mechanism at process start.
7. **Verify scope from the provider.** Confirm the machine identity can read only the intended vault/items and cannot access excluded personal data.

## Choose the Authentication Model

### Interactive terminal or SSH

Use the provider's interactive CLI login. The command may export an ephemeral session token into the current shell; this is acceptable when the token expires and the account password never enters history or an environment file.

- Add/configure the account once using flags for non-secret metadata only.
- Let the CLI prompt for secret key/password with hidden input.
- Sign in on later shells using the account shorthand.
- Explicitly sign out and unset session variables on shared or long-lived shells.

### Remote VPS secret entry

When the application runs on a VPS but the user works from another device, make SSH the default setup surface. Do not open a graphical terminal, browser, or desktop session inside the VPS merely to collect a key.

1. Place a hidden-input configurator on the VPS. It should use `getpass` or the provider CLI's own secret prompt, validate the credential before persistence, update the protected destination atomically, and keep mode `0600`.
2. Give the user one exact command in the form `ssh -t user@host 'python3 /absolute/path/configure_secret.py'`. The `-t` is required for reliable hidden interactive input.
3. Resolve `user@host` from live SSH/Tailscale configuration instead of inventing it. Offer a stable DNS name first and an IP fallback when available.
4. Keep the secret out of argv, shell history, chat, stdout, logs, and diagnostic bodies. Report only presence, mode, HTTP status, provider request ID, length, and a sanitized provider error message.
5. If validation fails, improve diagnostics before asking the user to regenerate or re-enter credentials. Distinguish authentication, authorization, account/project access, model availability, rate limiting, and network errors.
6. Verify that the exact remote destination was modified after success; a user's “listo” is not proof that the intended VPS received the secret.

For VPS operations, this SSH-first workflow is preferred; graphical remote prompts create avoidable friction.

### Desktop-integrated CLI

Use when a person is present to approve unlocks. Enable the vendor's desktop/CLI integration, then authenticate through system biometrics or OS authentication. Do not automate clicks on password, biometric, 2FA, or permission prompts.

### Unattended automation

Use a service account, workload identity, Connect server, or equivalent machine principal.

1. Create a dedicated automation vault/project/namespace.
2. Add only the secrets required by the workflow.
3. Grant read-only permission by default.
4. Create the machine identity and capture its token exactly once without stdout/chat exposure.
5. Store it using an OS/service credential mechanism with restrictive permissions.
6. Test one allowed read and one denied out-of-scope read.
7. Rotate/revoke the token when scope changes or exposure is suspected.

## Migration Pattern for Personal Secrets

Some providers prohibit service-account access to built-in personal/private vaults. Do not attempt to bypass this by storing the human password. Instead:

- Create a new shareable automation vault.
- Copy only selected items; avoid mirroring an entire personal vault unless the user explicitly understands the duplication and exposure.
- Preserve ownership and update workflows deliberately: copies may drift from originals.
- Record which item is authoritative and how rotations propagate.
- Prefer references/injection where the provider supports them over manually duplicated plaintext.

## Verification Checklist

- Human password never appeared in chat, argv, history, logs, source, or env files
- Machine identity uses a dedicated scope
- Permission set is read-only unless justified
- One allowed secret reference resolves successfully without printing its value
- One excluded vault/item is denied
- Token storage permissions and service ownership are correct
- Rotation and revocation path is documented
- Interactive session tokens are short-lived and cleaned up when appropriate

## Pitfalls

- **“The machine is secure, so plaintext env is fine”:** local compromise, process inspection, backups, crash dumps, shell exports, and accidental logging still widen exposure.
- **Using a Service Account as a master-password substitute:** machine identities often cannot access built-in personal/private vaults by design.
- **Copying the full personal vault:** this creates a second broad trust domain and increases rotation drift. Select only required items.
- **Token on stdout:** one-time tokens are frequently shown only once; capture them directly into protected storage instead of terminal scrollback or chat.
- **Overclaiming authentication:** a running desktop app is not proof that the CLI is authenticated; verify with a read-only identity command and sanitize the output.
- **Secret-bearing verification:** never prove access by printing the secret. Verify metadata, exit status, or a downstream operation that does not expose the value.

## References

- See `references/onepassword-cli-and-service-accounts.md` for 1Password-specific SSH sign-in, desktop integration, Service Account limitations, and scoped-vault setup.
- See `references/remote-vps-secret-bootstrap.md` for the SSH-first hidden-input configurator pattern, atomic persistence, sanitized provider diagnostics, and post-setup verification.
