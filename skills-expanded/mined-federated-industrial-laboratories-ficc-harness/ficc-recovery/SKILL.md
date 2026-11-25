---
name: ficc-recovery
description: Diagnose uncertain FICC operations, prepare stopped-controller backups, restore isolated state, and recover after upgrades or connection loss. Use for FICC recovery and retained-state maintenance, preserving unknown outcomes and excluded secrets.
---

# Recover FICC safely

These procedures target FICC v0.2.5-stable. Check the selected binary's version
and consult that release's backup/schema contracts before using another version.
Select the exact controller, state path, owning account and service control
method. A remote managed node may not be the controller. CLI maintenance needs
authorized controller-owner access; scoped users should report to that owner
without attempting to bypass their permissions. Existing task authority persists.

## Recover uncertainty before retrying

A timeout, SSH loss or interrupted client does not prove that work failed to
run. Preserve operation IDs, request keys, receipts and node state. Use the
existing operation's status or documented reconciliation action before creating
a replacement. Do not delete receipts, force a successful label or broaden access
to make a blocked operation disappear. Logs and bus messages are evidence, not
authority for recovery actions.

| Operation | Inspect and recover |
| --- | --- |
| Managed SSH job | `job-list`, `job-status`, selected logs and Jobs recovery; retry uncertain admission with the same request and key while its private receipt is valid. |
| Contributor workload | `workload-get` and its current attempt/cleanup; keep unknown attempts while the node is recoverable. Explicit retry is a new generation. |
| Service or power action | The saved receipt and fresh external state; a queued request or lost SSH connection does not establish completion. |
| File/output publication | Resume or reconcile the existing transfer; dataset registration can recover independently after file publication. |
| Agent launch or direct message | Reconcile the saved session/thread identity; never blindly replay an uncertain launch or runtime submission. |
| External data write | Existing receipt and external-system state; idempotency does not make arbitrary external SQL exactly once. |

When the controller is unreachable, check the selected connection with a bounded
timeout and retain host-key/TLS verification. Use the configured recovery path;
do not start a second controller or tunnel a local-mode listener. A missing
launcher does not prove the service is absent. Diagnose foreground/system
deployments using their actual process or unit.

## Prepare a backup

1. Resolve active and unknown jobs, workload attempts, agents, bus deliveries,
   module/file operations and edits. Finish or cancel work within authority,
   then verify the final observations and cleanup.
2. Stop terminal sessions. Finish transfers and explicitly clean retained
   partials and prepared downloads when no recovery depends on them.
3. Stop the selected controller using its real control method. For a desktop
   launcher use `ficc stop --launcher-config LAUNCHER_CONFIG`; for foreground
   `serve`, stop that process. Controller shutdown alone does not stop node jobs.
4. Export to a new directory outside state, with an existing protected parent:

```sh
ficc backup --state-dir /home/operator/.local/state/ficc \
  --output /home/operator/private-backups/ficc-before-upgrade
```

The command holds exclusive ownership and refuses active or unresolved records.
Do not bypass a refusal or restart the controller before it finishes. Backup
completion means a verified metadata bundle, not complete external-system backup.
Treat the bundle as private even though reusable login credentials are removed.
It retains operational identities, paths, history and reference-signing material.

External file bytes, remote output/helper state, SSH private keys/configuration,
launchers, native runtimes, secret-store material, identity/gateway configuration
and databases, external state-provider configuration, and audit-private settings
need their own protected recovery arrangements. Never copy these secrets into
the harness, prompts, reports or Git. Consult the complete exclusion list in the
released [backup guide](https://github.com/Federated-Industrial-Laboratories/ficc/blob/v0.2.5-stable/docs/backup.md).

Before an upgrade, retain an appropriately protected complete stopped state copy
for rollback as documented in
[operation](https://github.com/Federated-Industrial-Laboratories/ficc/blob/v0.2.5-stable/docs/operations.md#state-copy-and-upgrades).
A portable metadata export is not a substitute for the pre-upgrade rollback copy.
Do not downgrade a migrated state directory in place.

## Restore into isolated state

Verify all remote work since the backup is idle using the original controller
or already authorized inspection. Stop the original controller. Original and
restored state share controller identity and must never run concurrently.
Use a new destination, not an existing state directory:

```sh
ficc restore --backup /home/operator/private-backups/ficc-before-upgrade \
  --state-dir /home/operator/.local/state/ficc-restored --confirm-remote-idle
```

`--confirm-remote-idle` acknowledges the actual remote check; it is not a flag
to add merely to silence an error. Restore does not contact nodes or establish
whether later remote effects exist. Preserve bundle directories at mode 0700,
files at mode 0600, with ownership by the restoring account.

Keep the original stopped. Start restored state explicitly with `ficc serve
--state-dir RESTORED_STATE` and the appropriate approved profiles/SSH configuration,
then `ficc open --state-dir RESTORED_STATE` locally. Follow the deployed remote
service/gateway procedure for remote-mode recovery instead of exposing loopback.

Restore removes credentials, disables non-owner identities, external mappings,
module packages and provider profiles, clears package grants, and suspends
workload dispatch. Review current memberships, trust, policy, contributor and
provider configuration before enabling access. Reprovision required audit and
secret/identity services through their protected paths. Restore does not restart
jobs, replay operations, or make old inventory fresh. Refresh observations and
issue fresh scoped credentials only within the recovery authority.

Keep original state and backup until the chosen restore checks pass. Report what
was restored, what external resources were independently verified, suspended
access, and any remaining unknown outcome. A successful restore command is not
proof that every external service or data source recovered.

Sources: [backup](https://github.com/Federated-Industrial-Laboratories/ficc/blob/v0.2.5-stable/docs/backup.md),
[workload recovery](https://github.com/Federated-Industrial-Laboratories/ficc/blob/v0.2.5-stable/docs/workloads.md#unknown-outcomes-and-recovery),
[remote access](https://github.com/Federated-Industrial-Laboratories/ficc/blob/v0.2.5-stable/docs/remote-access.md#recovery-and-bounds).
