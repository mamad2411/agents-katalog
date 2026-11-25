---
name: whyslow
description: Diagnose why a Mac is slow and what is filling its disk, clean caches safely, and show how much better the Mac got. Use when the user says their Mac is slow, laggy, hot, out of memory or out of storage; asks what is using RAM, swap or disk space; asks which background services, launch agents, daemons, dev servers or Docker containers are running (the macOS equivalent of systemctl); wants to free up space or clear caches (npm, pnpm, pip, Cargo, Gradle, Xcode, VS Code extensions, browser and app caches, node_modules and other build folders); or asks whether their Mac has improved.
---

# whyslow

`scripts/whyslow.ts` in this skill's folder does the work and prints compact output. It needs Node 22.18 or newer and runs TypeScript directly:

```sh
node --no-warnings <this skill's folder>/scripts/whyslow.ts <command>
```

| Command | Use it for |
|---|---|
| `diagnose` (default) | why the Mac is slow; prints a 0-100 score and, after the first run, a `vs last check` line |
| `progress` | how much better the Mac is since the first check, and how much space `clean` has freed |
| `services` | launchd jobs (the macOS systemctl), servers listening on ports, Docker containers |
| `disk` | what fills the disk, largest first (10-30 seconds) |
| `big [folder]` | biggest items in one folder (default: home), to drill into space `disk` doesn't explain |
| `clean <id...>` | dry run of deleting cleanable targets; add `--yes` to delete |

1. Run `diagnose` first. `!!` lines are the main causes, `!` lines are smaller wins. Explain them to the user biggest first, in plain words, each with its `fix:`. If there is a `vs last check` line, tell the user whether things got better or worse.
2. For background load, run `services`. Explain what each running job or server is, and how to stop it.
3. If disk space is low or the user asks about storage, run `disk`. Each row shows size, target id, and either `cache` (safe to delete, rebuilt on demand) or `manual:` (personal data or VMs the user must free by hand). Use `big ~/Library` or `big <folder>` to dig into anything large that has no row.
4. To clean, run `clean <id...>` without `--yes` first and show the user what it would delete. Add `--yes` only after the user agrees to those exact targets. For `projects`, ask which projects to keep and pass `--keep word1,word2`; `--days N` sets how long a project must be idle (default 30, `--days 0` for all).
5. After cleaning or fixing, run `progress` so the user sees what improved.
6. Never delete `manual:` targets yourself; give the user the hint instead. Ask before running any `fix:` or stop command such as `killall`, `kill`, `brew services stop` or `colima stop`.
