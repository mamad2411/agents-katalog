---
name: secrets-management-automation
description: Safely connect automations to password managers and secret stores using scoped machine identities, least-privilege vaults, non-interactive authentication, rotation, and metadata-only verification.
version: 1.2.3
author: Hermes Agent
created_by: agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [secrets, password-manager, service-account, automation, least-privilege, credentials]
---

# Secrets Management Automation

Use this skill when an automation needs durable access to credentials held in a password manager or secret store. It covers desktop-app integration, service accounts/machine identities, scoped vault design, token storage, read-only verification, rotation, and revocation.

## Core Safety Contract

1. **Never automate a human master password.** Do not request, type, persist, or place an account/master password in chat, `.env`, shell history, source control, logs, or scheduler prompts. A trusted host does not make a decrypt-all credential an appropriate automation secret.
2. **Separate human and machine identities.** Use the provider's service account, machine identity, workload identity, or narrowly scoped access token for unattended jobs.
3. **Default to least privilege.** Start with only the required vault/items and read-only access. Add write/share/delete permissions only when a concrete workflow requires them.
4. **Respect non-shareable built-in vaults.** Before promising access, check provider restrictions. If a personal/private vault cannot be shared with machine identities, create a separate automation vault and copy only required items.
5. **Never expose token material to the model.** Generate tokens directly into a protected destination. Do not print them in tool output, chat, diagnostics, or success messages.
6. **Verify with metadata, not values.** Confirm authentication, vault visibility, item count/title references, permissions, and a narrowly scoped lookup without displaying secret fields.
7. **Plan revocation before rollout.** Record where the token is consumed, how to rotate it, and how to disable the automation without locking out the human account.

## Workflow

### 1. Establish the actual requirement

- Restate the user's end goal and name the exact consuming automation before changing vaults, services, or credential files.
- Identify which automation needs which secret, whether it only reads or must also write, and which new secrets the workflow itself will generate.
- Before starting OAuth or another short-lived enrollment, define how generated refresh tokens/keys will reach durable storage. A read-only machine identity cannot write them back; preserve least privilege with a preplanned user-mediated handoff or a separately scoped write target.
- For OAuth grants that intentionally expire in testing, automate the due check, one-time callback, exchange, atomic storage, and verification—but keep login, MFA, scope review, and consent human. Pause reminders until the registered redirect and private HTTPS path are verified; use `references/oauth-human-in-loop-rotation.md`.
- Keep browser callback latency bounded: acknowledge only after exchange and safe token storage, then queue any multi-minute full sync in a background worker with atomic mode-`0600`, secret-free success/failure markers and an escalation path.
- Do not migrate, restart, or harden adjacent services merely because related credentials are present. Keep unrelated credential work deferred unless the user explicitly includes it in scope.
- Prefer item references (vault + item + field) over granting broad vault access.
- Separate interactive desktop use from unattended cron/service use.

### 2. Inspect provider capabilities and restrictions

- Check current official documentation for service-account availability, account-plan requirements, non-shareable vaults, permission names, expiration, and rate limits.
- Inspect only account/vault metadata while authenticated; do not enumerate secret values.
- When reusing a credential already held by another local application, identify it by provider, label, auth type, and presence metadata. Read it directly from the protected source into the consuming process or destination; never print or interpolate it into a command argument.
- Probe the provider before deployment. A valid identity-linked API key may still require non-secret routing metadata such as a workspace or project ID on every request. Treat a missing-routing-header response as an incomplete configuration, not an invalid key.
- Verify the exact requested model through the provider's model-list endpoint, then make one minimal real inference before wiring the application.
- If desktop integration is required, the user performs the initial unlock and security approval manually.

### 3. Create an automation vault

- Use a clearly named, non-built-in vault such as `Automation` or `<Project> Automation`.
- Copy only required items; avoid mirroring an entire personal vault unless the user explicitly accepts the duplication and exposure.
- Keep the original personal vault authoritative when possible and document how copies are refreshed.

### 4. Create the machine identity

- Grant read-only/item-read permission by default.
- Avoid create-vault, write, share, delete, or administrative permissions unless required.
- Check whether vault scope and permissions are mutable after creation. For providers such as 1Password where service-account permissions are immutable, never promise a temporary upgrade of an existing read-only identity; create a separate expiring writer identity for the one-time operation instead.
- Prefer an expiration date when the provider supports it.
- Generate the token with restrictive process/file permissions and direct output redirection; do not capture it in conversational tool output.

### 5. Store and inject the token

Preferred order:

1. OS credential facilities or a service manager credential store.
2. A root/user-readable-only credential file outside the repository, consumed only by the target service.
3. A mode-0600 environment file as a compatibility fallback.

Avoid command-line arguments, shell history, world-readable environment files, project `.env` files, and long-lived global shell exports. Restrict the consuming service's user, filesystem access, logs, and environment inheritance.

### 6. Verify and audit

- Confirm the machine identity can authenticate non-interactively.
- Confirm it can see only the intended vault/items and cannot access unrelated personal/private vaults.
- Test one metadata lookup or field injection without printing the secret.
- Confirm write/delete operations are denied for read-only identities.
- Record token creation/expiration and rotation/revocation instructions without recording the token itself.

## Human-in-the-loop Boundaries

The user must personally handle:

- Master-password entry, biometric approval, and MFA/2FA.
- Approval of desktop CLI integration or browser security prompts.
- Copying a one-time token if the provider cannot redirect it securely.
- Final confirmation before granting broad write, share, delete, or administrative permissions.

The agent may open the app or settings page, inspect non-secret status, prepare scoped resources, and verify access after the user completes the security boundary.

## Pitfalls

- **Master password in `.env`:** gives unattended processes the human decrypt-all credential and leaks through backups, process environments, diagnostics, or accidental reads.
- **Assuming “Personal” is shareable:** many password managers reserve built-in personal/private vaults for the human identity only.
- **Token shown once:** terminal capture and chat logs are still disclosure. Redirect at creation time instead of printing then moving it.
- **OAuth callback URL mistaken for metadata:** callback and redirect URLs can embed `code`, `state`, tokens, or signed parameters in the query or fragment. Treat the complete URL as secret-bearing input. Never print a stored callback URL; inspect only a hard-allowlisted origin/path after stripping query and fragment, or report presence/absence metadata.
- **Full-vault mirror by default:** duplicates exposure and creates synchronization ambiguity. Start with explicit required items.
- **Read-only in prose, write-capable in reality:** verify actual provider permission flags and test that writes fail.
- **Immutable service-account permissions:** some providers, including 1Password, freeze vault access and permission flags at account creation. Do not instruct the user to toggle write access later. For a one-time secret handoff, create an expiring identity scoped to the exact vault with explicit read-plus-write permission, use hidden terminal input, validate the final read path, then revoke/delete it.
- **Read succeeds but edit fails:** this proves the token can locate the intended vault/item but does not have effective write permission. Preserve staged OAuth/rotation material, replace the temporary identity with one created using the exact write permission, and avoid repeating upstream authentication.
- **Desktop integration mistaken for unattended auth:** desktop integration usually still depends on a human-unlocked app; use a machine identity for durable cron/service access.
- **Terminal multiplexer scrollback mistaken for a safe secret channel:** `tmux`/`screen` history, pane captures, screenshots, and process-output polling can expose usernames, MFA codes, generated app passwords, and recovery prompts even when the main password field is hidden. Prove the real CLI prompt before enrollment; once the user starts authentication, stop observing the pane and use metadata-only checks. Clear local scrollback afterward.
- **No rotation path:** automation becomes fragile or permanently overprivileged. Document expiry, consumers, and revocation before deployment.
- **Secret migration becomes the project:** moving credentials for a nearby service can distract from the user's actual automation goal and introduce unrelated restarts or partial breakage. Confirm the consumer and scope first; defer adjacent migrations.

## Verification Checklist

- Human master password never entered or persisted by the agent
- Current provider restrictions checked from official documentation
- Automation vault is shareable and contains only required items
- Machine identity has minimum permissions, read-only by default
- Token never appears in chat, logs, command arguments, or tool output
- Token destination permissions and service scope verified
- Metadata-only authentication test passes
- Unrelated vault access and write/delete operations are denied
- Rotation and revocation procedure documented

## References

- See `references/multi-workspace-api-keys.md` for safely reusing identity-linked API keys, handling required workspace headers, framework configuration overlays, and end-to-end verification.
- See `references/1password-service-accounts.md` for 1Password-specific vault restrictions, desktop integration boundaries, service-account permissions, and secure token handling.
- See `references/headless-interactive-enrollment.md` for SSH/tmux enrollment, terminal compatibility, no-capture boundaries, local secret handoff, and metadata-only verification on VPS/headless hosts.
- See `references/oauth-human-in-loop-rotation.md` for scheduled OAuth reauthorization, one-time callbacks, private HTTPS routing, atomic refresh-token rotation, silent due-check cron behavior, and the Google Health read-only example.
