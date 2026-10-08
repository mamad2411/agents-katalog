---
name: close-studio-pro
description: Gracefully close Mendix Studio Pro and its child processes (running runtime, MxBuild, Java helpers) so subsequent CLI ops can run without tripping the Studio-Pro-lock check. Also cleans up Mendix toolchain orphans left over from a Studio Pro crash (node/esbuild/sass/mxbuild under \Mendix\<ver>\(modeler|runtime)\ whose parent studiopro is dead) so Studio Pro can relaunch. Defaults to graceful (sends WM_CLOSE, lets Studio Pro prompt about unsaved changes). Auto-invoke when a /mx-shadow-write or /mx-scaffold-microflow needs Studio Pro closed and Neo has confirmed it's safe to do so, OR when Studio Pro is failing to launch and orphan toolchain processes are suspected. Also invocable as /close-studio-pro [project-name].
---

# close-studio-pro

The "make Studio Pro stop holding the .mpr lock" primitive. Wraps `~/.claude/lib/Close-StudioPro.ps1` with project-allowlist awareness and friendly verification. Also handles the post-crash recovery case: when Studio Pro itself has died but its bundled toolchain (node/esbuild/sass/mxbuild/java) is still running with a dead parent and blocking new launches.

## North star

> **Close gracefully; force only on explicit ask.**

Studio Pro caches unsaved model edits. The running runtime holds a SQLite DB lock. Force-killing either loses data or corrupts state. Always WM_CLOSE first; let Studio Pro prompt about unsaved changes; only escalate when Neo asks.

## When to invoke

**Auto-invoke** when:

- About to run a CLI op (`/mx-shadow-write`, `/mx-scaffold-microflow`, `/mx-entity-add`) and Studio Pro currently has the project open.
- Neo says "close Studio Pro" / "close the testbed" / "close the test project."
- After a successful `/mx-handoff` step where Neo replied "done" -- Studio Pro should be closed before the verification CLI ops run, but auto-invoke this skill is the cleanest path.
- Neo says **"Studio Pro won't start"** / "Studio Pro keeps crashing on launch" / similar. The likely cause is a bundled-toolchain orphan from a prior crash; this skill's `-OrphansOnly` mode is the fix. Run with `-List` first to confirm orphans are present before any kill.

**Do not invoke** for:

- Casual cleanup / housekeeping. Closing Studio Pro is intrusive; only do it when there's a downstream CLI op that needs it.
- Any project not on the testbed allowlist, unless Neo passes `--any-project` explicitly.

## What it does

1. **Resolve project context.**
   - Default project: TestOSApp3 (testbed, per `~/.claude/rules/mendix-testbed.md`).
   - Default runtime port: 8082 (testbed runtime, per the same rule).
   - Override via skill args: `/close-studio-pro <project-name>` or invoke with `--any-project`.

2. **Allowlist check.**
   - If `<project-name>` is provided and is NOT on the testbed allowlist, refuse with the standard testbed-refusal block (see `mendix-testbed.md`). Closing Studio Pro on a live project's window during the developer's workflow could silently lose unsaved real work.
   - `--any-project` bypasses the allowlist BUT requires explicit confirmation from Neo in the same turn (paste the request back in the response and ask "confirm `--any-project`?").

3. **Invoke the engine.** Either route works -- pick by context:

   *Inside a Mendix project, or when Neo wants to invoke from the MendixToolkit folder:*
   ```powershell
   pwsh C:\Workspace\MendixToolkit\mx-close.ps1 -Project TestOSApp3
   pwsh C:\Workspace\MendixToolkit\mx-close.ps1 -List           # safe inventory, no kills
   pwsh C:\Workspace\MendixToolkit\mx-close.ps1 -OrphansOnly    # post-crash cleanup
   ```
   The wrapper auto-supplies `-RuntimePort 8082` when `-Project TestOSApp3`, defaults to `-List` with no args, and forwards everything else.

   *Direct invocation of the engine:*
   ```powershell
   pwsh ~/.claude/lib/Close-StudioPro.ps1 `
       -ProjectName 'TestOSApp3' `
       -RuntimePort 8082 `
       -TimeoutSeconds 20
   ```
   (Substitute project / port / timeout from skill args.)

   *For post-crash recovery (Studio Pro not running, but orphan toolchain blocking relaunch):*
   ```powershell
   pwsh ~/.claude/lib/Close-StudioPro.ps1 -List          # confirm orphans first
   pwsh ~/.claude/lib/Close-StudioPro.ps1 -OrphansOnly   # then kill them
   ```

4. **Interpret the result:**
   - **Exit 0:** clean. Report "Studio Pro closed; port 8082 free." (or "orphans cleared; ready to relaunch.")
   - **Exit 2:** Studio Pro did NOT exit within timeout. The most common cause is an open "Unsaved changes" prompt. Report this exact line: *"Studio Pro likely has an unsaved-changes prompt open. Click through the dialog, then I'll re-try."* Wait for Neo to confirm before retrying.
   - **Exit 3:** survivors remain after the sweep. Report each one to Neo; ask whether to retry with `-Force`.

5. **Verify post-close (downstream-skill prerequisite):**
   - Run `Get-Process studiopro` -- must return nothing for a full close.
   - If `RuntimePort` was provided, verify port is free.
   - Report final state in 3 lines max.

## Hard rules

- **Never auto-invoke `-Force` on the first attempt.** Always graceful first. Force is an explicit Neo decision.
- **Refuse on non-testbed projects** unless `--any-project` AND Neo explicitly confirms it in the same turn.
- **Never close Studio Pro to "clean up"** when no downstream op needs it. Studio Pro startup is slow (15-30s); the friction matters.
- **If Studio Pro is open on a DIFFERENT project than expected** (window title mismatch), report the open titles and stop. Do not assume which one to close.
- **If port 8082 is bound by a process that is NOT a Studio Pro descendant**, that's an orphan runtime. Report it; do not auto-kill -- ask Neo whether to add it to the close set.

## Output format

```
## /close-studio-pro

**Project filter:** <name or "any">
**Runtime port:** <port if checked>
**Result:** CLOSED | TIMEOUT | SURVIVORS | NO-OP

**State after:**
- Studio Pro processes: <count, with PIDs if any survive>
- Port <N>: <FREE | bound by PID X>

**Next step:**
- (if CLOSED) <e.g., "Ready to run /mx-shadow-write">
- (if TIMEOUT) "Click through the unsaved-changes prompt, then I'll retry"
- (if SURVIVORS) "Survivors: <pids>. Retry with -Force?"
```

## Orphan toolchain (post-crash recovery)

When Studio Pro crashes hard, it can leave its bundled toolchain (`node.exe`, `esbuild.exe`, `dart.exe` (sass), and sometimes `mxbuild`/`java` from `\Mendix\<ver>\(modeler|runtime)\`) running with a dead parent. The next Studio Pro launch tries to spawn its own copies, collides with the orphans (stdio pipes / file locks / shared state), and dies on startup.

The engine auto-detects these via parent-PID probing (`NtQueryInformationProcess`, not WMI -- WMI can hang on EDR-managed boxes) and includes them in the kill set. An orphan is a process whose path matches `\Mendix\*\(modeler|runtime)\`, name is not `studiopro`, AND whose parent is dead, PID-reused, or not a `studiopro`. Orphan survivors are auto-killed without `-Force` because their parent is dead by definition -- there is no in-flight Studio Pro state to lose. Live Studio Pro descendants still require `-Force` to kill, preserving the "graceful first" rule.

To use this path explicitly:
- `-List` to inventory current studiopro processes + orphans (read-only).
- `-OrphansOnly` to sweep orphans without touching any live Studio Pro window.
- `-NoOrphanTools` to disable orphan detection (falls back to original Studio-Pro-descendants-only behavior).

## Cross-reference

- Engine: `~/.claude/lib/Close-StudioPro.ps1`.
- Top-level wrapper: `C:\Workspace\MendixToolkit\mx-close.ps1`.
- Allowlist: `~/.claude/rules/mendix-testbed.md`.
- Safety pillars (pillar 3 = Studio Pro lock check): `~/.claude/rules/mendix-safety.md`.
- Skills that frequently need this: `/mx-shadow-write`, `/mx-scaffold-microflow`, `/mx-entity-add`, `/mx-handoff` (post-handoff verification).
