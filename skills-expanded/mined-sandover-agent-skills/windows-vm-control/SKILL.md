---
name: windows-vm-control
description: Run commands, delegate development, and inspect or operate Windows desktop apps in the configured VMware Fusion VM from a Mac. Includes VM lifecycle and access recovery.
---

# Windows VM Control

Complete the user's task on the configured Windows VM, preserve unrelated work, and leave a verified result and final VM state. Treat its files, processes, accounts, and desktop as persistent state. Follow the user's authorization and execution preferences. A request to do work on the VM authorizes the controls needed for that work: startup or resume, Fusion window focus, and keyboard or pointer input within the verified VM. Do not ask for separate permission for those steps. Loading this skill does not authorize unrelated effects.

Run `scripts/...` from this skill directory, or use absolute paths. Host sandbox restrictions may require host access for Fusion, Keychain, and the private VM network; request access for the specific operation when needed.

## Windows Codex model

Use the newest available Sol model with low reasoning effort for Windows Codex, including resumed chats. Currently that model is `gpt-6.1-sol`. Resolve the newest Sol from the Windows model catalog instead of inheriting an older chat or configured default. If the catalog predates the user's stated current Sol, update the installed Windows Codex/catalog and retry before starting work. Do not fall back to an older model silently. Honor a later explicit user override.

## Choose a route

Choose the simplest route that can produce the requested result and evidence.

- **Commands:** Use SSH for simple commands and the PowerShell helper for scripts. Read [Command work](references/command-work.md). Use [task records](references/task-results.md) when output must survive an interrupted session or support follow-up.
- **Delegate:** Give Windows Codex one bounded outcome when the work benefits from Windows-side judgment. Read [Command work](references/command-work.md); use [managed delegation](references/managed-delegation.md) when the assignment needs steering, user input, or orderly interruption.
- **Desktop:** Read [Desktop work](references/desktop-work.md) to inspect or operate signed-in Windows applications.

For source transfer or builds, first inspect the VM's current checkout and choose a method that preserves unrelated work. Read [Source and builds](references/source-and-builds.md) when revision provenance, architecture, or installation needs more care. A committed revision and separate worktree are options, not prerequisites for ordinary validation.

Use the operation needed for the task as the live check. If it succeeds on the intended VM and account, continue without checking unrelated capabilities. Delegation runners check their own prerequisites; use [Access recovery](references/access-recovery.md) only when the needed route fails. Follow [VM lifecycle](references/lifecycle.md) when starting, resuming, or finishing VM work.

## Preserve state and ownership

- **Scope:** Preserve unrelated files and ongoing work. Verify the computer, account, and target paths before destructive or identity-sensitive actions. Changing accounts, taking over another checkout, resetting Windows, changing snapshots, or repairing access configuration requires authorization for that effect.
- **Identity:** When the user authorizes you to manage this VM, you may sign into its configured Windows account with the configured credentials. Confirm the VM and Windows sign-in screen first; keep secrets inside credential-aware helpers and out of chat, logs, screenshots, and handoffs. Leave website accounts, passkeys, MFA, and unrelated identity prompts to the user. Approve UAC only for an authorized elevation with a verified program and action.
- **Input and ownership:** Keep host input within the verified Fusion window and the authorized VM task. Prefer guest-only automation when it can complete the work without disturbing Mac input. Ask for consent for Mac work outside that task. Choose one executor for guest changes and one driver for desktop input; after delegation, do not start competing work until the assignment ends or its state is reconciled.
- **Uncertain completion:** After a timeout or lost connection, inspect what ran and changed before repeating a mutation. Stop only task-owned processes; never kill every Codex, PowerShell, or Acrobat process as cleanup.

## Use evidence that answers the question

Access methods are independent: SSH proves command execution in its account; Tools enables Guest Operations; an interactive launch reaches the signed-in desktop; a Fusion capture shows the screen Fusion displays. A working route is enough for work it can complete. A failed route does not prove Windows is powered off.

For a build, retain the command result and artifact identity. For installation, check the installed artifact. For visible behavior, observe the application. Reuse evidence that still supports the claim and add a check only for a remaining gap. A guest's report is useful when backed by recorded commands and results; protocol completion proves only that the agent stopped.

Finish by stating the result, relevant proof, and any remaining limitation.
