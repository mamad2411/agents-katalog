---
name: windows-sandbox-installer-test
description: Test a Windows installer and uninstaller on a clean machine with Windows Sandbox using sbx or the optional MCP adapter. Use when asked whether a setup.exe or .msi installs silently, what it adds to the system, whether its uninstaller cleans up, why an install hangs, or what an installer leaves behind.
---

# Test an installer

If shell access is available, use the `sbx` CLI; the optional MCP adapter uses the same engine and is not required.

If a tool says the sandbox isn't ready, follow the windows-sandbox-setup skill.

Run `sbx install-test <installer>` or call `sandbox_install_test` with `installer` set to a host path to a `.msi`, `.exe`, `.ps1`, `.cmd` or `.bat`. Both use the same workflow: boot a fresh sandbox and then snapshot, install, snapshot, optionally run a test, uninstall, snapshot again and destroy the sandbox. Allow about two minutes plus the installer's own time.

## Make it silent

An `.msi` gets `/qn /norestart` automatically. An `.exe` needs its silent switch in `args`:

| Installer type | `args` |
|---|---|
| NSIS | `/S` |
| Inno Setup | `/VERYSILENT` |
| Squirrel | `--silent` |
| Burn, InstallShield and others | Often `/quiet`; check the vendor's docs |

Without a silent switch, the installer waits on a dialog until `timeoutSec` (default 600). Set a shorter timeout when probing an unknown installer.

## Uninstalling

`uninstall` defaults to `"auto"`, which uses what the installer registered in Add/Remove Programs: `msiexec /x {ProductCode}`, else `QuietUninstallString`, else `UninstallString` plus `uninstallArgs`. Use `uninstallArgs` for the silent switch when only an `UninstallString` is registered, such as `/S` for NSIS. Set `uninstall` to `"none"` to skip it, or to a command line to run your own.

If the installer registers nothing in Add/Remove Programs, nothing is uninstalled automatically, and the report says so.

## Add a test

`test` is a host `.ps1` that runs inside the sandbox after the install. It gets `$env:SBX_INSTALL_DIR`, `$env:SBX_PROGRAM` and `$env:SBX_OUT`, plus `Get-SbxUiTree`, `Invoke-SbxUi` and `Wait-SbxUi`. Throw or exit non-zero to fail. `SBX_INSTALL_DIR` is empty when the installer doesn't register an install location, so check it before using it.

## Read the result

The result is PASS or FAIL, a diff of what the install changed, a diff of what's left behind after uninstall, and a `report.md` on the host.

**It fails when:**
- the installer or uninstaller exits with an error or hangs (exit codes 0, 1641 and 3010 all count as success; the last two mean a reboot is needed)
- the test script fails
- the program is still listed in Add/Remove Programs after uninstalling

**Leftover files and registry keys do not fail the run** unless you pass `failOnLeftovers: true`. Always read the "Left behind" section and report it, even on PASS.

- **A hung install** comes back with a screenshot of the stuck window and its controls. That's usually a "silent" install waiting for a click, so report which dialog it was.
- **Processes left running** after install (tray apps, updaters) are listed and stopped before the uninstall. Mention them, because they often explain leftovers.
- **Noisy paths** can be ignored with `exclude`. A trailing `*` makes the path a prefix match. Known Windows background noise is already filtered.
- **MSI failures** have a log in the run's `out` folder (`msi-install.log`), and its errors are extracted into the report.

Pass `network: "off"` to prove an installer doesn't need to download anything. Offline runs are a good way to find web-bootstrapper dependencies.
