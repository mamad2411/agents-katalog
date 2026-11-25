---
name: autonomous-runs
description: "Long and overnight runs (AI-First edition): keep working for hours on your own laptop without needing you: a status file you can check, the laptop kept awake, checkpoints, and a morning report. Use for 'work overnight', 'I'm going to bed', 'keep going for a few hours', 'don't ask me anything'."
---

# Long and overnight runs (AI-First edition)

Work for hours without the person, and hand back exactly what they expected.

## Before you start

1. **Agree on the list and the budget.** Turn the ask into a numbered list with a clear stopping point. Say
   roughly how long it may take and that it spends credits (GPT-6.2 Sol at High unless they chose another). One
   session unless they ask for parallel ones.
2. **Write the status file** on the Desktop as `<Project> status.txt` (on Windows, the folder
   `[Environment]::GetFolderPath('Desktop')` returns), and tick items the moment they're verified:

   ```text
   <PROJECT> STATUS (updated <time from the clock>)
   DONE         [x] 1. <item> - <where the result is>
   IN PROGRESS  [ ] 2. <item> - <what's happening>
   NEXT         [ ] 3. <item>
   ASSUMPTIONS  - <decisions made without them>
   NEEDS YOU    - <only what truly needs them, with exact steps>
   ```
3. **Keep the laptop awake,** plugged in with the lid open: `node <this skill>/scripts/keep-awake.mjs start
   --hours 10`. It runs `caffeinate` on a Mac, or a hidden keep-awake on Windows, and changes no settings.
   (On Windows the person can instead set Settings > System > Power & battery > Screen and sleep > "When plugged
   in, put my device to sleep after" to Never, and set it back in the morning.)

## While it runs

- **Never block on the person:** no questions, sign-ins or prompts that need the laptop. Pick a sensible default,
  note it under ASSUMPTIONS and keep going. If something truly needs them, write the exact steps under NEEDS YOU
  and move to the next item.
- **Checkpoint** at each milestone: commit work in progress on the branch, update the status file, and keep a
  short `resume.md` next to it (done, next, branches, running processes), so a restart picks up where it left off.
- **Don't cut corners** to finish sooner, and don't sit in long sleep loops: check, act, move on.
- **Own your processes:** note every server you start (process id, port) and stop only those.
- **Read the time from the clock** (`date`, `Get-Date`) for every update.

## In the morning

Write `<Project> report.txt` on the Desktop: what got done, with links (branches, PRs, live pages, videos), what
didn't and why, and what needs the person. Run `keep-awake.mjs stop`, stop your servers, and open the report.

## Another computer (a what-if here)

To close the laptop and keep going, the work has to run on a computer that stays on, such as a desktop at home or
a cloud machine, reached as VS Code on another machine (Remote Tunnels, dev tunnels or SSH) and picked in the
Agents window's environment picker. The same rules apply there; the laptop only starts the work and reviews it.
Nobody needs this for the workshop.
