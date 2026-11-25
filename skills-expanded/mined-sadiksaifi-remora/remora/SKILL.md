---
name: remora
description: Remote desktop control through the Remora app's `remora` CLI, over RDP or VNC. Use when a task needs the screen of a remote Windows, Linux or Mac machine, or mentions Remora.
---

# Remora

Learn the `remora` CLI from `remora --help` and each command's `--help`. Pass `--json`, and follow `error.hint` when a command fails.

- A successful input command means only that Remora sent the input. Trust what a screenshot shows, and check one before you report the task done.
- Stay out of the user's way: connect with `--background` unless they ask to watch.
- The user can take over or stop your control at any time. From then on the session is theirs: do what the hint says, and leave the session open when you finish.
- Ask the user before you accept a certificate or supply a password.
- When you finish, release control, and close only a session you opened.
