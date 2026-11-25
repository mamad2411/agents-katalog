---
name: mac-storage-cleanup
description: Diagnose and clean up a Mac that is low on disk space or memory, then leave it set up so the storage crisis does not come back. Covers caches, AI model caches, agent temp folders in /private/tmp, runaway logs, old installers, duplicate or beta Xcodes, DerivedData, iOS DeviceSupport, simulators and runtimes, package-manager caches, swap and memory pressure, and virtual machine sizing (Parallels, UTM), and finishes by offering a deeper clean and malware scan with CleanMyMac when it is installed. Use whenever the user says the disk is full, "storage crisis", "clean up my Mac", "free up space", "why is my Mac slow", "optimize for my RAM", asks what is taking up space, or asks to clear logs, caches, simulators or Xcode junk - even if they only name one of those.
allowed-tools: Bash(df:*), Bash(du:*), Bash(find:*), Bash(ls:*), Bash(sysctl:*), Bash(vm_stat:*), Bash(memory_pressure:*), Bash(ps:*), Bash(pgrep:*), Bash(lsof:*), Bash(sw_vers:*), Bash(system_profiler:*), Bash(tmutil listlocalsnapshots:*), Bash(xcode-select -p), Bash(xcrun simctl list:*), Bash(xcrun simctl runtime list:*), Bash(xcrun simctl delete unavailable), Bash(brew cleanup:*), Bash(prlctl list:*), Bash(mdls:*), Bash(open cleanmymac5:*), Bash(cleanmymac --help), Bash(cleanmymac help:*), Bash(cleanmymac --version), Bash(cleanmymac ignore list)
---

# Mac storage cleanup

This skill turns "my disk is full and everything is slow" into a short diagnosis in plain words, a cleanup the user approves, and habits that keep it from happening again. It was written from a real cleanup on a 16 GB M2 MacBook Air that had 15 GB free on a 926 GB drive and ended with 361 GB free. Nothing the user needed was lost.

The user may be blind and using a screen reader. Run every command yourself and report in plain sentences and short lists. Never hand shell commands back for the user to run. If a deletion is blocked by the permission system, say so in one line and ask the user to approve it, or to switch to a mode where they can approve it. Do not paste the command for them.

## Act like an assistant, not a report

Do as much of the work yourself as you can: measure, look inside folders, check what's in use, and work out what each item really is. The user should only have to make decisions, never investigate.

Turn every decision into a short question with AskUserQuestion. Each option needs a size, a plain-words description of what happens, and what it costs (for example "your next build will be slow" or "Xcode can download it again"). Put the option you recommend first and mark it. Use multiSelect when the items are independent. Group related items so there are one to three questions, not a long list to read. For a screen reader user, a few clear choices are much faster than a wall of text.

Before you ask, look inside anything a tool calls "junk". A cleaner's category name is not enough to go on. CleanMyMac CLI's "System Junk" turned out to be 99% Xcode, including the simulators the user tests with and the build data for current projects. So split items like that into what's safe and what isn't, and ask about the parts that matter.

If an answer is blank or unclear, don't delete anything. If the user rejects a question by accident and says "continue", ask it again.

## Before you start: tell the user about manual mode

Claude Code's auto mode has a safety check that blocks commands that permanently delete files, because they can't be undone. That covers `rm`, `cleanmymac clean` and `purge`, and even a CleanMyMac scan, since the same command can delete. The diagnosis and suggestions (steps 1 to 3) are read-only and run in any mode. The cleanup itself (step 4, and the CleanMyMac clean in step 5) needs manual mode, so the user approves each deletion.

Never change the user's settings, permission rules or permission mode, and never offer to. Claude can't switch modes anyway; only the user can. Explain what's needed, and let the user do it.

At the start, before diagnosing, tell the user in plain words, for example:

> "Heads up: I'll check everything first, which works in any mode. The cleanup part deletes files, and Claude Code's auto mode blocks that on purpose because it can't be undone. When we get there, I'll ask you to switch to manual mode by pressing Shift+Tab, so you can approve each step."

When the diagnosis is done and the user has picked what to remove, remind them at that moment: "Ready to clean. Please press Shift+Tab until the status line says manual mode is on (from auto mode, that's one press), then say go." If they're already in manual mode, just start.

Communication rules: never just say "I can't". Say what's needed, why, and what happens next. If something is blocked anyway, say what was blocked and why, and don't retry it in pieces or by another route. Never skip a step quietly.

## The four steps

Work in this order and don't skip ahead to deleting. Step 5 is optional. Steps 1 to 3 are read-only and run in any mode. Step 4 and the CleanMyMac clean in step 5 need manual mode.

### 1. Diagnose

Measure first. These commands are all read-only, so run them in parallel.

- **Disk:** `df -h /System/Volumes/Data`. That volume is the real one on modern macOS, because `/` is the sealed system volume and always looks small.
- **Memory:** total RAM from `sysctl -n hw.memsize`, then `memory_pressure | tail -3`, `sysctl vm.swapusage`, and the top processes by RSS (`ps -axo rss,comm -m | head -15`).
- **Where the space went:** `du -xhd1 ~ | sort -rh | head -15`, then go one level into whatever is big. Always look in these places:
  - `~/Library/Caches`, `~/Library/Developer`, `~/Library/Containers`, `~/Library/Logs`
  - `~/Downloads`, `~/.Trash`, `~/.cache`, and other dot-folders in home such as `.npm`, `.cache/huggingface`, `.ollama`, `.unsloth`, `.codex`
  - `/private/tmp`, `/private/var/tmp`, `/private/var/folders`. Coding agents such as Codex and Claude Code leave whole build folders and DerivedData copies in `/private/tmp`, often several GB each.
- **Local Time Machine snapshots:** `tmutil listlocalsnapshots /`.

Use `du -x` so it doesn't cross into other volumes, and give long scans a timeout of several minutes.

### 2. Explain in plain terms

Before suggesting anything, tell the user what you found the way a person would: "Your disk is 99% full. 143 GB of that is a cache from AI model experiments on September 18 that nothing is using." Lead with the three or four biggest items. Say why it matters for speed too: when the disk is nearly full, macOS has no room for swap, so a Mac with little RAM slows to a crawl even though RAM isn't the real problem.

### 3. Suggest, sorted by how safe it is

Sort what you found into three groups and say which group each item is in.

**Safe to clear now.** These rebuild themselves and hold no user work. Clear them in step 4 without asking item by item, but list them and their sizes afterwards.
- Compiled-model and ML caches under `~/Library/Caches`, such as `coreai-cache`, after checking with `pgrep` and `lsof` that nothing is using them.
- Old build folders in `/private/tmp` and `/private/var/tmp` that no running process uses. Check `ps` first: an app may be *running from* a `/private/tmp` DerivedData folder. Skip anything in use, and skip the current session's own scratch folder.
- Package-manager caches: `brew cleanup -s`, and `~/Library/Caches/pip`, `node-gyp`, `pnpm`, `org.swift.swiftpm`.
- `xcrun simctl delete unavailable`, which removes simulators for runtimes that are no longer installed.

**Ask first.** Name each item with its size, its last-modified date, and what it is, then let the user pick. Use AskUserQuestion with multiSelect. If an answer comes back blank, treat it as "nothing yet" and don't delete anything.
- Model weights and datasets the user downloaded or made (Hugging Face, Ollama, custom model folders). These are the user's work, even when they are huge.
- `~/Library/Developer/Xcode/iOS DeviceSupport`. Xcode rebuilds it when a device is plugged in, which takes a few minutes per iOS version.
- DerivedData for projects that haven't been built in more than 7 days. Check the newest file inside the folder, not the folder's own date. Never touch the folders for current projects, or the shared `CompilationCache.noindex`, `ModuleCache.noindex` and `SDKExplicitPrecompiledModules`, because clearing those makes every next build slow.
- Duplicate or old Xcode apps. Keep the one `xcode-select -p` points to, and check each copy's version with `mdls -name kMDItemVersion`. Leftover `*.incomplete-backup` folders and `.xip` installers can go.
- Simulator runtimes for OS versions the user no longer targets (`xcrun simctl runtime list`), and simulator devices that haven't been booted in months.
- Installers in Downloads (`.dmg`, `.iso`, `.xip`, `.pkg`) for apps that are already in `/Applications`.
- Logs. Keep anything from the last few days, because the user may be in the middle of a testing session. Watch for a single runaway log file: a `device-live.log` that ran for days reached 26 GB.
- The Trash. Items owned by root can't be removed without admin rights, so tell the user to empty the Trash from Finder for those.

**Leave alone unless the user names it.** Messages, iCloud Drive (`Mobile Documents`), Documents, Photos, Mail, app containers that hold real data, and anything a running app has open.

### 4. Clean up, check, and report

Delete only what the user approved. The user may approve in casual speech ("delete the big stuff, keep yesterday's logs, don't touch Xcode stuff I'm using"), so turn that into a concrete list, state the list back in one line, and then act.

Do it as one batch, then run `df -h` again and check the big paths to confirm they're really gone. Report the before and after free space, what was removed with sizes, what failed and why, and what was kept on purpose.

If the permission system blocks the deletion, don't retry it in pieces or by another route. Tell the user what was blocked and ask them to approve it.

### 5. Offer a deeper clean with CleanMyMac

When the cleanup is finished, check whether CleanMyMac is installed:

`ls -d /Applications/CleanMyMac*.app /Applications/Setapp/CleanMyMac*.app 2>/dev/null`

If it's there, offer it in plain words, for example: "Want to do a deeper clean with CleanMyMac? It's an excellent Mac cleaner from MacPaw. It finds system junk, app leftovers and big forgotten files I don't go looking for, and it also scans for malware and adware." Only go ahead if the user says yes. If it isn't installed, mention it once as an option and move on. Don't push it.

**How to control it: use the CLI first.** MacPaw makes an official command-line tool, CleanMyMac CLI (developer preview, July 2026). Install it with `brew install --cask macpaw/taps/cleanmymac-cli`. That adds `cleanmymac`, plus the short name `cmm`. It is separate from the app and works without it. Commands:
- `cleanmymac clean`: system junk, developer-tool caches, AI tool junk (Claude Code, Codex) and the Trash. You can narrow it with `junk`, `dev`, `ai` or `trash`.
- `cleanmymac purge [path]`: build artifacts in projects, such as node_modules, .build, .venv and .next. Artifacts older than 7 days are preselected.
- `cleanmymac analyze [path]`: explore what's using space.
- `cleanmymac optimize`, `optimize ram`, `optimize purgeable`: maintenance tasks, freeing inactive memory, and purgeable space.
- `cleanmymac ignore add <path>`: protect a folder from clean and purge. Add the user's active Xcode projects and anything in the "leave alone" group before cleaning.

Without `--force`, every command shows a review list and waits for confirmation. With `--force`, it cleans the preselected items with no review, so only use it after the user has approved what the scan found. Auto mode treats any `cleanmymac clean` or `purge` command as destructive and blocks even a scan, so it needs manual mode.

**Driving the CLI from Claude Code** (tested with version 1.0.0):
- **First run:** in a real terminal, the CLI shows MacPaw's Terms of Use and Privacy Policy and waits at "Continue? [Y/n]". Ask the user with AskUserQuestion whether they accept, and give both links. Answer `y` only after they say yes.
- **Results:** there's no dry-run or report option. To read the results, run the command inside a pseudo-terminal (a short Python script using `pty.fork()`, with `TERM=xterm-256color` and a window size set), wait for "items selected", and send keys:
  - Right arrow opens a category, Left goes back, Down moves.
  - `a` selects or deselects everything.
  - `q` quits without cleaning.
  - Enter confirms and cleans, so never send Enter while you're only looking. Strip the escape codes from the output to read sizes and paths.
- **Without a terminal:** with input from `/dev/null`, it skips the terms screen, renders the scan summary, and exits without deleting. That's a quick way to get the totals.
- **`--force`:** cleans only the preselected items. In `clean`, AI Junk isn't preselected, so `clean ai --force` removes nothing. To clean it after the user approves, run `clean ai` in the pseudo-terminal, press `a`, then Enter.
- **What the categories hold:** `clean dev` covers package-manager caches (npm, pnpm, uv, pip, Homebrew and others) and is safe. `clean trash` empties the Trash. `clean junk` covers user logs plus "Xcode Junk", which includes all of DerivedData, simulator devices and simulator runtimes. Don't run `clean junk --force` on a developer's Mac. Handle Xcode yourself with `xcrun simctl runtime delete <id>`, `xcrun simctl erase` and the DerivedData rules in step 3, and use `find -mtime +3` for logs so recent ones stay.

The CLI has no malware scan. For that, use the app's Protection module.

**Controlling the app.** Use this for the malware scan, or when the CLI isn't installed. The app has links that open each module, `cleanmymac5:///modules/<name>`, which you run with `open "cleanmymac5:///modules/protection"`. In version 5 the modules are:
- `smartCare`: one scan that covers everything
- `cleanup`: system junk
- `protection`: malware
- `performance`: maintenance tasks and login items
- `applications`: uninstalling apps and removing their leftovers
- `myClutter`: large and old files and duplicates
- `spaceLens`: a map of what's using space

Older versions use a different scheme, so check `CFBundleURLSchemes` in the app's Info.plist if a link doesn't work. A link only opens the screen. Scanning and cleaning mean driving the window with the computer-use tools. Tell the user what was found, by category and size, before cleaning, and never remove anything in the "leave alone" group from step 3.

**Known catches**
- On first launch, CleanMyMac shows a privacy and terms screen. The user has to accept the terms themselves. Don't accept a legal agreement for them. Then tell the user it's ready and continue.
- The App Store version (`CleanMyMac_5_MAS`) is sandboxed, so it asks for access to the home folder and to Applications before it can scan them. The user approves those prompts, or you click them only after the user says yes.
- Its UI is dark and low contrast. Read screenshots carefully, and zoom in before clicking small buttons.
- When VoiceOver is running, its on-screen overlay covers the whole screen, so the computer-use tools refuse every mouse click with "would land on VoiceOver". Permission can't be requested for VoiceOver, and CleanMyMac's window doesn't show up to AppleScript UI scripting either. What does work: the module links, and the Return key, which presses the default button (Scan, Grant Access, Run). The Review screens can't be reached, so if the user wants anything unticked before Run, ask them to do it with VoiceOver, or ask whether to run everything.
- If a screenshot comes back all black, CleanMyMac isn't the front window. Call `open_application` and take the screenshot again.
- Smart Care finds results in five areas: Cleanup (junk), Protection (malware), Performance, Applications (updates), and My Clutter (duplicates in Downloads). By default, Cleanup and My Clutter are ticked to run.

## Look past today: optimize overall

A cleanup that doesn't change anything comes back in a month. After the cleanup, check these and suggest what fits.

- **Memory and swap.** On an 8 or 16 GB Mac, check memory pressure, swap use, and pageouts. Name the heaviest always-running apps and background helpers.
- **Virtual machines.** Run `prlctl list -a -i` for Parallels. Check how much RAM and how many CPUs the VM is given compared with the Mac. On a 16 GB Mac, 4 to 6 GB for Windows is reasonable, and 8 GB or more starves macOS. Look for ISO images still attached to the VM, and VM snapshots. You can only change memory while the VM is shut down, so ask first.
- **VM problems that aren't about space,** such as no sound or a screen reader that won't speak, belong to a separate Parallels skill. Don't try to fix them here. Mention them in the report.
- **iOS and Mac developers.** Suggest these:
  - Keep one stable Xcode and at most one beta, and delete each beta once its release ships.
  - Every few months, remove simulator runtimes for OS versions the user no longer supports.
  - Send agent and CLI builds to one known DerivedData path instead of a new `/private/tmp/<name>-DerivedData` for every task, so builds stop piling up.
  - Clear Xcode Archives after a release ships, and keep only the archive for the build that's live.
  - Watch iOS DeviceSupport after each iOS beta, because every beta adds several GB.
- **AI and ML work.** Model caches and experiment folders are the fastest-growing thing on a developer's Mac. Suggest one models folder and deleting experiment outputs when an experiment ends.
- **Logs.** Point long-running log capture at a size-capped or rotated file, and delete capture folders when the issue they were for is closed.
- **A recurring check.** Offer to set up a monthly check, with the `/schedule` skill or a reminder, that runs step 1 and reports only if free space is under about 15% or a single folder grew more than 20 GB.

## The final report

Always end with a report the user can keep. Cover:

1. **The headline:** free space before and after, and how full the disk is now.
2. **What was removed,** grouped (caches, build folders, logs, installers, model files, CleanMyMac junk), with sizes.
3. **What was kept on purpose, and why.**
4. **What failed or was blocked,** and what it would take to finish.
5. **Security:** the CleanMyMac malware result, if it ran.
6. **What could be done better:** the habits behind the mess, in plain words, each with one concrete fix. For example: "Agents were building in /private/tmp and never cleaning up. Your house rules now forbid it." Or: "A log capture ran for six days and reached 26 GB. Cap log captures or stop them when the test ends." Or: "You keep two copies of Xcode 27. Keep one." Look at what you actually found, not a generic list.
7. **Next check:** when to run this again, or the monthly check if the user set one up.

## Reporting style

Use plain sentences and short lists, with sizes in GB rounded to whole numbers. Wide tables, emojis and decorative formatting make a screen reader slow and noisy, so leave them out. Start with the headline number ("You now have 338 GB free, up from 15 GB"), then what changed, then what's still worth doing.
