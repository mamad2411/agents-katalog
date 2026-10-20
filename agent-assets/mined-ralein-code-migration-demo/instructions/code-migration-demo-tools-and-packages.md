---
description: "Pre-installed tools and packages available on this dev machine for repository tasks. Agents should use these instead of re-installing."
applyTo: "**"
---

# Pre-Installed Tools & Packages

Self-Maintaining Instruction: When you install a new system tool or package during any task, append it to the appropriate section below. This avoids redundant installs across sessions and agents.

---

## Host OS

| Property            | Value                                                          |
| ------------------- | -------------------------------------------------------------- |
| OS                  | Linux (paths in run.md use /home/ralein, likely Ubuntu/Debian) |
| Shell               | bash/zsh (examples use bash)                                   |
| Architecture        | x86_64 or arm64 (unspecified — confirm with team)              |
| Path separator      | /                                                              |
| Default line ending | LF                                                             |

## Language Runtimes

| Language   | Version                           | Install method (per OS)          |
| ---------- | --------------------------------- | -------------------------------- |
| Java (JDK) | 17 (local dev), 8 (legacy target) | Team-provided JDK path in run.md |

## Package Managers

| Manager                             | Version | OS  |
| ----------------------------------- | ------- | --- |
| _None detected — confirm with team_ |         |     |

## CLI Tools

| Tool     | Version          | Purpose               | Install                  |
| -------- | ---------------- | --------------------- | ------------------------ |
| Tomcat 9 | 9.0.90 (example) | Servlet container     | Manual download (run.md) |
| curl     | -                | Local endpoint checks | System package           |

## Helper Scripts (in repo)

| Script            | Purpose                                     | Runs on (bash / PowerShell / both) |
| ----------------- | ------------------------------------------- | ---------------------------------- |
| run.md (commands) | Documented run commands for Tomcat and logs | bash                               |
