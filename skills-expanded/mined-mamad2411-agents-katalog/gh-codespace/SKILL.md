---
name: gh-codespace
description: >-
  GitHub CLI (`gh codespace` or `gh cs`) operations for connecting to, managing,
  creating, or editing GitHub Codespaces.
  You MUST load this skill when working with the `gh codespace` command.
license: MIT
---
<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->
# gh-codespace

Connect to and manage GitHub Codespaces natively from the CLI.

## WHEN TO USE

- When managing, creating, or connecting to GitHub Codespaces natively from the CLI.
- When you need to securely transfer files between the local machine and a Codespace without configuring SCP manually.
- To handle port forwarding for local testing of applications running inside a Codespace.

## WHEN NOT TO USE

- For managing local Docker containers or Devcontainers not hosted on GitHub's infrastructure (use `docker` or `devcontainer` skills instead).
- When attempting to perform automated Git commits (the agent should use native local `git` tools instead of proxying through a Codespace).
- If the user explicitly asks to work locally and has not initialized a Codespace environment.

## Mindmap of Commands

```mermaid
mindmap
  root((gh-codespace))
    code
      Open in VS Code
    cp
      Copy files
    create
      Create a codespace
    delete
      Delete codespaces
    edit
      Edit a codespace
    jupyter
      Open in JupyterLab
    list
      List codespaces
    logs
      Access codespace logs
    ports
      List and manage ports
    rebuild
      Rebuild a codespace
    ssh
      SSH into a codespace
    stop
      Stop a codespace
    view
      View details
```

## Common Pitfalls

- **Interactive Hangs**: Running `gh codespace ssh` in an automated agent session, which blocks execution by dropping the agent into an interactive TTY shell.
- **Dangling Port Forwards**: Starting a port forward with `gh codespace ports forward` without backgrounding it (`&`), locking up the terminal.
- **Ignoring State**: Attempting to execute commands against a Codespace that is currently in a "Stopped" or "Rebuilding" state, causing immediate connection failures.

## Core Principles

- Verify codespace status with `gh codespace list` or `gh codespace view` before attempting interactive connections.
- Use `gh codespace cp` for transferring files between the local machine and the codespace instead of manually configuring SCP.
- Manage port forwarding natively via `gh codespace ports forward` for local testing.

## Commands / Usage Patterns

- **List Codespaces**: View active codespaces to find the `<codespace-name>`:
  `gh codespace list --json name,repository,state`

- **Create a Codespace**:
  `gh codespace create --repo <repository-name> --branch <branch-name>`

- **Copy Files**: Transfer files from a codespace to the local machine:
  `gh codespace cp -c <codespace-name> remote:/path/to/file local/path/`
  Transfer files from local to codespace:
  `gh codespace cp -c <codespace-name> local/path/ remote:/path/to/file`

- **Port Forwarding**: Expose a port from the codespace to your local machine:
  `gh codespace ports forward <remote-port>:<local-port> -c <codespace-name>`

- **Stop/Delete Codespace**: Clean up resources when done:
  `gh codespace stop -c <codespace-name>`
  `gh codespace delete -c <codespace-name>`

## Diagnostics and Troubleshooting

- **Connection Failures**: If `gh codespace ssh` hangs or fails, check codespace logs:
  `gh codespace logs -c <codespace-name>`
- **Rebuilding Environment**: If the Devcontainer configuration is modified or corrupted, trigger a rebuild:
  `gh codespace rebuild -c <codespace-name>`

## What to Avoid

- Do not attempt to SSH manually without using `gh codespace ssh` as it requires specific key exchanges handled by the CLI.
- Avoid using interactive commands (like `gh codespace code` or `gh codespace ssh`) in automated agent workflows. Use them only when providing instructions to the user.

## Limitations

- The CLI depends on active network connections and the GitHub Codespaces service availability.
- Port forwarding `gh codespace ports forward` blocks the terminal and requires background execution (`&`) or a separate process in non-interactive environments.

## References

- [gh codespace manual](https://cli.github.com/manual/gh_codespace)
