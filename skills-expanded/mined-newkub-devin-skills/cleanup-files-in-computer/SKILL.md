---
name: cleanup-files-in-computer
description: Delete unnecessary files and caches on the machine via a mise cleanup task in the global mise.toml
argument-hint: "[target]"
related:
  - report-idea-cleanup-files-in-computer
  - follow-tool-mise
  - alternative
  - delete
  - report
  - run-clean
  - run-cleanup
---

## Goal

Clean up files and caches on the machine with `mise run cleanup` as defined in the global `mise.toml`

## Scope

- Inspect and create `[tasks.cleanup]` in the global `mise.toml` (`~/.config/mise/config.toml` or `~/.config/mise.toml`)
- Delete only safe caches, temp files, logs, and old artifacts
- Never delete source code, configs, secrets, or personal files

## Execute

### 1. Verify Environment

> Goal: Check mise and the global config

1. Run `mise --version`
2. Run `mise config` to find the global config path
3. If there is no global config yet → create `~/.config/mise/config.toml`
4. Run `mise doctor` to check health

### 2. Evaluate Cleanup Tools

> Goal: Pick the right cleanup tools

1. Check installed package managers/CLIs: `bun`, `pnpm`, `npm`, `pip`, `cargo`, `scoop`, `mise`, `uv`, `pnpm`
2. Use `/alternative` to evaluate cleanup tools such as:
   - `mise cache prune` vs `mise prune`
   - `bun pm cache clean` vs `npm cache clean`
   - `scoop cleanup *` vs `scoop cache rm *`
   - `cargo-sweep` vs `cargo clean`
   - `pip cache purge` vs `uv cache clean`
3. Pick the safe tools that actually exist on the machine

### 3. Define cleanup Task

> Goal: Create `[tasks.cleanup]` in the global `mise.toml`

1. Open the global `mise.toml`
2. Add or update `[tasks.cleanup]`:
   ```toml
   [tasks.cleanup]
   description = "clean temp files and caches"
   shell = "pwsh -NoProfile -Command"
   run = '''
   # dry-run mode: pass --dry-run to see what would be deleted
   param($dryRun = $false)

   $cmds = @(
       @{ name = "mise cache prune"; cmd = "mise cache prune" },
       @{ name = "mise prune";       cmd = "mise prune" },
       @{ name = "bun cache";        cmd = "bun pm cache clean" },
       @{ name = "pnpm store";       cmd = "pnpm store prune" },
       @{ name = "npm cache";        cmd = "npm cache clean --force" },
       @{ name = "pip cache";        cmd = "pip cache purge" },
       @{ name = "uv cache";         cmd = "uv cache clean" },
       @{ name = "scoop cleanup";    cmd = "scoop cleanup *" },
       @{ name = "cargo sweep";      cmd = "cargo sweep -r ~" }
   )

   foreach ($c in $cmds) {
       Write-Host "[$($c.name)]"
       if ($dryRun) {
           Write-Host "  would run: $($c.cmd)"
       } else {
           try { Invoke-Expression $c.cmd } catch { Write-Host "  skipped: $_" }
       }
   }
   '''
   ```
3. Adjust commands per OS: Windows uses PowerShell, macOS/Linux uses bash/zsh
4. Save the global config

### 4. Dry Run

> Goal: Show what would be deleted before doing it for real

1. Run `mise run cleanup -- --dry-run`
2. Or `mise run cleanup --dry-run`
3. Collect output: cache paths, sizes, commands
4. Produce a summary with `/report` or `/report-idea-cleanup-files-in-computer`

### 5. Confirm

> Goal: Get explicit confirmation

1. Ask the user whether they really want to delete
2. If the user agrees → go to step 6
3. If the user declines → stop and report

### 6. Run Cleanup

> Goal: Run the real cleanup

1. Run `mise run cleanup`
2. Check the exit codes
3. If any command fails → record it and report

### 7. Validate

> Goal: Confirm the cleanup finished

1. Run `mise list` to verify the tools
2. Check disk space before/after with `dua`, `duf`, or `Get-PSDrive`
3. Report what was deleted, space saved, and errors

## Rules

### 1. Dry Run First

- Always dry run first
- Never run destructive actions without user confirmation
- Show the commands that will run

### 2. Safe Targets

- Delete only caches, temp files, logs, and old artifacts
- Never delete source code, `.env`, secrets, or credentials
- Never delete system directories such as `C:\Windows`, `C:\Program Files`

### 3. Tool-Specific Cleanup

- Use each tool's own cleanup command, e.g. `bun pm cache clean` instead of `rm -rf`
- Never delete `.mise` files or `~/.local/share/mise` directly
- Use `mise cache prune` and `mise prune` for mise

### 4. Global Config

- Edit only the global `mise.toml`
- Do not edit a project `mise.toml` without permission
- Commit or back up the global config before editing if needed

- Use /follow-tool-mise if needed
- Use /delete if needed
- Use /run-clean if needed
- Use /run-cleanup if needed

## Expected Outcome

- `[tasks.cleanup]` exists in the global `mise.toml`
- `mise run cleanup --dry-run` lists what would be deleted
- After user confirmation, the selected cache/temp/artifacts are deleted
- Report of disk space saved and errors

