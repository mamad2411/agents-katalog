---
name: atd-fresh-install
description: Reset the production Atd installation on macOS for a fresh installation experience, including application data, credentials, and permissions, while preserving the development version. Use when manually invoked to prepare installation and first launch again; not for routine updates, cache-only cleanup, or resetting only the onboarding flag.
---

# Atd Fresh Install

Leave the user ready to install and launch Atd themselves: the old production app is in Trash, application data and identified credentials are removed, permission results are explicit, a verified installer is available, and the development version is preserved.

## Invocation and scope

Manual invocation: `$atd-fresh-install Completely reset production Atd data and permissions so I can experience installation and first launch again.`

- An explicit reset request or existing authorization in the same task is sufficient; do not ask for it again. Creating, editing, explaining, or evaluating this skill does not authorize resetting a real installation. Honor narrower instructions instead of inferring a full wipe.
- Prepare an existing official installer by default. Commit, push, or publish only when separately requested. If the user requests publication first, follow repository rules and wait for the requested release and artifact verification before deleting data. Do not independently bump versions or change application code.
- Production uses `com.junerdd.ai`; development uses `com.junerdd.ai.dev`. Verify `Info.plist`, not the app name or icon. Do not delete with `Atd*` or `com.junerdd.ai*` wildcards.
- Preserve development, preview, and recording apps and their services, data, and credentials. Never reset the entire machine's permissions, login keychain, LaunchServices database, or login items database.

## Workflow

1. **Prepare the installer.** Resolve the current official release unless the user specifies a version. Follow [Installer preparation and verification](references/installer.md) to download it, check its hash, version, and signature, and preserve download quarantine. Do not install or launch the new app to verify it; that would consume the user's first-run experience.
2. **Inspect without mutation.** Run `scripts/reset_atd.py` from this skill. Its default mode is read-only. Review the identified apps, paths, production service identity, processes, and blockers. If storage has changed, reconcile the scope with `apps/agent-service/src/storage.ts`, `apps/agent-service/src/credentials/keyring.ts`, and the macOS shell's path configuration before proceeding.
3. **Check additional permissions.** Follow [macOS reset details](references/macos-reset.md) for production notifications and login/background items. These are outside `tccutil reset All`. Handle existing grants through supported application or system settings before quitting the old app when necessary.
4. **Apply the reset.** Briefly state the actual cleanup scope immediately before deletion, relying on authorization already given. Choose a private, Git-ignored temporary report path and run the command below. The helper stops processes only inside verified installed apps, resets production TCC grants, deletes exact keychain namespaces before their identity files, removes data, then unregisters and moves old apps to Trash.
5. **Verify and hand off.** Read the report and recheck production paths, credentials, processes, and development preservation. Eject only identified old production installer volumes. Give the user the installer link and the next step: drag Atd into Applications, then launch it. Do not perform the first launch or grant new permissions for them.

```sh
# Run from the repository root. Default: no changes to apps, data, permissions, or keychain.
python3 .agents/skills/atd-fresh-install/scripts/reset_atd.py

# After reset authorization, installer verification, and additional permission checks:
python3 .agents/skills/atd-fresh-install/scripts/reset_atd.py \
  --apply --report "$reset_report"
```

Set `reset_report` to a new JSON file inside this task's private temporary directory. Reports contain non-secret identifiers and operation results needed to investigate partial failures; do not commit or publish them.

## Boundaries and failures

- The legacy Electron directory `AI` and `AI Safe Storage` have broad names. Add `--include-legacy-ai` only after establishing that they belong to Atd. Other legacy candidates are documented in the reference; do not expand deletion through fuzzy matching.
- Read the service identity from production `AgentService/service.json`. It is not the app version. If missing, do not invent a UUID or delete all `ai-agent-service:*` entries. Use `--service-id` only for a production identity captured earlier in this same task with ownership evidence.
- Default installation candidates are `/Applications/Atd.app` and `~/Applications/Atd.app`. Use `--app` for a verified nonstandard installed path. Do not treat temporary builds, development instances, or apps inside DMGs as installed production apps to remove.
- Stop the affected destructive operation for an unowned live service, symlink, shared production/development identity, permission failure, or deletion failure. Investigate and continue after resolving the specific cause. Do not blindly retry, broaden matching, elevate privileges, or change system security settings.
- A failed main-app TCC reset must not be reported as revoked permissions. Widgets may lack an independently resolvable bundle registration; report that result separately without inferring success or resetting permissions globally.
- Protected container metadata can remain. Distinguish cleared application data from complete absence of all system records. Disclose credentials, notification state, login items, or protected files that could not be verified.

The final response states the actual version and installer path, data/credential/permission results, development preservation, remaining limitations, and whether the new app is still uninstalled and unlaunched. Claim completion only for verified outcomes.
