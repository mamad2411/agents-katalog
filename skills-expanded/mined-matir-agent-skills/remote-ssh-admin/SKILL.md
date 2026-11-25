---
name: remote-ssh-admin
description: Perform remote system administration, diagnostics, and file management via SSH/SFTP. Requires key-based authentication for remote Linux/macOS hosts.
---
# Remote SSH & SFTP Administration

## Core Workflows

### 1. Remote Execution (SSH)
Use `ssh` for running commands on remote hosts. 
- **Command:** `ssh -o BatchMode=yes <user>@<host> '<command>'`
- **Batch Mode:** Always use `-o BatchMode=yes` to avoid interactive prompts.
- **Sudo:** If sudo is required, use `ssh -t` to force a pseudo-terminal if needed, or ensure NOPASSWD is configured for the user.

### 2. File Management (SFTP)
Use `sftp` or `scp` for file transfers.
- **Upload:** `scp <local_path> <user>@<host>:<remote_path>`
- **Download:** `scp <user>@<host>:<remote_path> <local_path>`
- **Recursive:** Use `-r` for directories.

### 3. Diagnostics & Troubleshooting
For detailed diagnostic commands, refer to [diagnostics.md](references/diagnostics.md).

### 4. Remote Configuration
- **Editing Files:** Download the file, edit locally, and then upload back.
- **Service Management:**
  - **Linux (systemd):** `systemctl <action> <service>`
  - **MacOS (launchctl):** `launchctl <action> <service>`

## Best Practices
- **Host Reachability:** Always test connection with a simple `uptime` or `echo "pong"` before running complex operations.
- **Structured Output:** Prefer commands that return structured output (e.g., JSON or CSV) when available.
- **Safety:** Use absolute paths for all remote operations to avoid ambiguity.
- **Error Handling:** Check exit codes of remote commands. A non-zero exit code usually indicates failure.

## Troubleshooting Connections
- **Permission Denied:** Ensure your SSH key is added to the agent (`ssh-add -l`).
- **Connection Timeout:** Check network connectivity and firewall rules.
- **Host Key Verification Failed:** Verify the host key if it has changed, or use `-o StrictHostKeyChecking=accept-new` if appropriate for the environment.
