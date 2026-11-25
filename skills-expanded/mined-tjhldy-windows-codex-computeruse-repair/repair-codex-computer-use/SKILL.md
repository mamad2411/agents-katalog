---
name: repair-codex-computer-use
description: Windows-only diagnosis and repair for specific Windows Codex Desktop Computer Use and Chrome plugin loading failures. Use when openai-bundled is missing, chrome@openai-bundled or computer-use@openai-bundled are not installed, or @oai/sky@0.4.10 throws Package subpath ... is not defined by exports for computer_use_client_base.js. Do not use on macOS, Linux, ChatGPT web, or as a general account, region, feature-flag, antivirus, enterprise-policy, or sandbox-permission fix.
---

# Repair Codex Computer Use

Use this skill only for Windows Codex Desktop Computer Use and Chrome plugin
loading failures caused by missing `openai-bundled` marketplace registration or
the known `@oai/sky@0.4.10` exports mismatch.

This is Windows-only. Do not use this skill for macOS, Linux, ChatGPT web, or
non-Windows Codex environments.

Inspiration: this community skill was inspired by Douyin creator whl.

Do not present this as a universal Computer Use unlocker. It does not fix
account entitlement, regional rollout, feature flags, enterprise policy,
antivirus blocks, unsupported Codex versions, or native service failures after
imports already work.

## Rules

- Start with read-only diagnosis.
- Do not modify `WindowsApps` permissions or ownership.
- Do not delete the whole `~/.codex` directory.
- Back up `~/.codex/config.toml`, `~/.codex/.codex-global-state.json`, and
  any edited `@oai/sky/package.json`.
- Prefer the smallest change that restores plugin loading.
- Do not automatically switch sandbox mode to `unelevated`; explain it as a
  fallback only after plugin loading and imports are fixed.

## Workflow

1. Run `scripts/diagnose.ps1`.
2. If `openai-bundled` is missing from `codex plugin marketplace list`, run
   `scripts/register-openai-bundled.ps1 -Apply -InstallPlugins`.
3. If Computer Use fails with `Package subpath ... is not defined by "exports"`,
   run `scripts/patch-sky-exports.ps1 -Apply`.
4. Verify `codex plugin list` shows:

```text
chrome@openai-bundled        installed, enabled
computer-use@openai-bundled  installed, enabled
```

5. Verify the `@oai/sky` import test succeeds.
6. Restart Codex Desktop or start a new Codex thread so plugin discovery reloads.

If `diagnose.ps1` shows the marketplace, plugins, and import test are already
good, stop and investigate a different category: sandbox, OS policy, account
availability, or a newer Codex/runtime bug.

## Expected Runtime Mismatch

Known affected shape:

```text
@oai/sky@0.4.10
```

The plugin imports:

```text
@oai/sky/dist/project/cua/sky_js/src/targets/windows/internal/computer_use_client_base.js
```

The target file exists, but `@oai/sky/package.json` does not export it. The fix
is to add that exact subpath to the `exports` object.

## Validation

Treat the repair as successful only when:

- `openai-bundled` appears in `codex plugin marketplace list`.
- `chrome@openai-bundled` and `computer-use@openai-bundled` are installed and
  enabled.
- The `WindowsComputerUseClientBase` import test succeeds.
- If possible, the real Computer Use runtime can list Windows apps.

Do not call the repair successful merely because the scripts ran. Call it
successful only when the plugin list and import/runtime checks pass.

## Rollback

Use backups created by the scripts to restore modified files. To remove the
registered marketplace or plugins, prefer:

```powershell
codex plugin remove computer-use@openai-bundled
codex plugin remove chrome@openai-bundled
codex plugin marketplace remove openai-bundled
```
