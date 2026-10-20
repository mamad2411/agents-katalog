---
name: bitwarden-machine-account-ops
description: Design and operate scoped Bitwarden Secrets Manager machine accounts without leaking credentials. Use when provisioning host, service, CI, or SDK secrets; runtime injection; token rotation or revocation; recovery tests; compromise response; or non-secret contract validation across Windows, WSL, containers, Proxmox guests, and automation.
---

# Bitwarden Machine Account Operations

Use this skill for **machine-readable infrastructure secrets**. Separate a human Bitwarden account from a non-human machine account and its access token. Keep only contracts, identifiers, owners, expiry/review metadata, validation methods, and incident records in version control; never keep a secret value, an access-token value, or a rendered environment file there.

Read `references/official-bitwarden-secrets-manager.md` before changing a machine account, token, project scope, CLI configuration, or workflow. Read `references/cli-and-sdk-integration.md` before using `bws` commands, adding an SDK dependency, selecting a wrapper, or interpreting an SDK schema. Read `references/runtime-and-recovery.md` before injecting, rotating, revoking, recovering, or responding to a suspected exposure.

## Security baseline

1. **Define the trust boundary first.** Create one machine account per host, service deployment role, or CI boundary. Assign only the project or projects the consumer requires. Default to **Can read**; write access requires a documented capability need, a constrained project boundary, a human owner, and explicit confirmation.
2. **Separate identities.** Never reuse a machine-account token between Windows, WSL, Proxmox, containers, CI, recovery, or environments. Do not grant a user or group machine-account membership casually: those members can create access tokens for, and access all secrets within, that machine account’s scope.
3. **Record the contract before creating secrets or tokens.** Use `templates/secret-contract.md`. Define consumer, project IDs, required key names, token expiry/review, integration mode, trusted runtime entrypoint, host-local credential location, CLI/SDK version, and recovery route. Do not put a value in the contract.
4. **Create tokens deliberately.** A token is shown once and cannot be retrieved later. Choose an expiry; `Never` requires an explicit operational justification and review date. Store the token outside Git in an owner-only, host-local credential mechanism or approved independent recovery system. Never place it in chat, a command-line argument, shell history, profile, `.env`, Compose file, service definition, container image, build argument, CI log, or transcript.
5. **Prefer reviewed CLI injection.** Use a process-local `BWS_ACCESS_TOKEN` only to authenticate `bws`. Prefer `bws run --project-id <id> --no-inherit-env -- <trusted-entrypoint>` when one project can satisfy the process. `--no-inherit-env` reduces inherited-variable conflicts; it is **not a sandbox**, and `PATH` plus shell-created variables can remain. Do not change the selected shell or rely on shell parsing without explicit review.
6. **Use an SDK only by exception.** Choose an SDK only when an application must perform programmatic Secrets Manager work that `bws run` cannot safely provide. Pin the language binding and its documented API version, use the official generated binding rather than hand-written schemas, define an owner-only token/state boundary, constrain the typed operation, and redact logs/errors/telemetry. Do not copy a vendor SDK sample with debug logging, prints, local defaults, interactive prompts, or destructive calls into a service.
7. **Treat output as a disclosure path.** Do not use `bws secret get`, `bws secret list`, `--output env`, `bws run -- 'echo …'`, `set -x`, PowerShell transcripts, verbose CI logs, Docker inspection, or diagnostic artifacts as routine validation. Validate trusted consumer health or non-secret project metadata only. Do not run `bws run` around an arbitrary agent shell, ad-hoc script, or unreviewed binary.
8. **Preserve platform boundaries.** Keep Windows and WSL machine identities distinct. Do not bake tokens or application secrets into Dockerfiles, images, build layers, Compose `environment:` blocks, system service definitions, or command lines. Use one reviewed runtime entrypoint. CI uses its own read-only machine account and token, a pinned integration/action revision, explicit secret IDs, and no untrusted pull-request code after secrets are injected.
9. **Rotate before revoking.** Create a replacement with the correct scope and expiry, validate without output and validate the affected service, then revoke the old token or replace the secret. Revocation breaks active machines’ ability to retrieve and decrypt secrets, so schedule it as a controlled cutover.
10. **Contain a suspected exposure.** Stop or isolate the affected consumer, preserve non-secret machine-account event evidence, create and validate a replacement, revoke the compromised token, remove affected client identity or runtime state as appropriate, then run a disposable recovery test. Do not delete a machine account until the incident record and required replacement path are complete.

## CLI and SDK decisions

| Need | Preferred decision | Prohibited shortcut |
|---|---|---|
| Authenticate `bws` | Process-local `BWS_ACCESS_TOKEN` delivered through a host-local owner-only mechanism | `--access-token <value>` in a command, script, job definition, or shell history |
| Limit application secret scope | A dedicated machine account and `bws run --project-id` when applicable | Inject every project secret into a broad interactive session |
| Select a shell | Use the platform default with a fixed reviewed entrypoint; record any explicit `--shell` selection | Launch an interactive shell or depend on unreviewed quoting, expansion, or user-controlled input |
| Handle incompatible secret names | Use POSIX-compatible names, or use `--uuids-as-keynames` and map them inside the reviewed entrypoint | Depend on a shell to safely interpret arbitrary secret names |
| Manage CLI state | Owner-only `~/.config/bws/config` plus state directory/encrypted state files; record `bws --version` | Commit, copy across trust boundaries, or casually retain state after compromise |
| Use an SDK | A version-pinned official binding with a narrow typed operation, redaction, and an owner-only state-file decision | Hand-write SDK JSON schemas, run vendor examples unchanged, or return/log secret objects |
| Validate | A trusted service health check or metadata-only non-secret check | Printing, listing, diffing, serializing, or exporting secret values |

## Confirmation gates

Creating or deleting a project or machine account, changing membership or project permissions, creating a token or secret, modifying a secret, revoking a token, adding/changing an SDK dependency, changing CI secrets, or altering a host’s credential/runtime boundary changes security state. Obtain explicit user confirmation immediately before each exact change.

A `bws run` invocation is privileged because its child process receives injected values. An SDK process authenticated with a machine-account token is equally privileged within that token’s scope. Review the complete executable or application version, script path, arguments, working directory, dependencies, state-file behavior, logs, telemetry, and destination before executing it. Do not approve a generic agent, shell, package installer, `docker compose` command, or unknown script as the injection target.

## Bundled resources

- Read `references/official-bitwarden-secrets-manager.md` for authoritative lifecycle, machine-account, audit-event, and source information.
- Read `references/cli-and-sdk-integration.md` for verified CLI forms, SDK-selection criteria, wrapper/schema boundaries, and unsafe-example warnings.
- Read `references/runtime-and-recovery.md` for host-local storage, `bws run`, SDK state, container/service, CI, rotation, compromise, and recovery procedures.
- Use `templates/secret-contract.md` before approving a machine-account/token, CLI runtime-injection, or SDK integration change.
- Use `templates/rotation-record.md` for every planned token or secret rotation, revocation, SDK credential cutover, and compromise response.
- Run `scripts/validate_secret_contract.py <completed-contract.md>` to statically reject incomplete or apparently secret-bearing contract files; it does not contact Bitwarden or read secret values.
