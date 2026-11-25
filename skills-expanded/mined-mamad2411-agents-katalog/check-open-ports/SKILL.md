---
name: check-open-ports
description: Check whether ports are free or conflicting before run-dev or deploy and find the owning process
argument-hint: "[port...]"
related:
  - run-dev
  - use-pwsh-shell
  - resolve-errors
  - report

---

## Goal

Check that the ports you need are free rather than in use by another process before running a dev server, build, or deploy — and identify the process owning each port

## Scope

- Use before `run-dev`, `run-preview`, or deploy when the config specifies a port
- Covers checking a single port, multiple ports, and port ranges
- Read-only: inspects and reports only, never kills a process unless told to

## Execute

### 1. Identify Ports

> Goal: know which ports to check

1. Take `port...` from the argument
2. If none given → pull ports from the project config: `vite.config.*`, `wrangler.toml`, `package.json` scripts, `.env`, `docker-compose.yml`
3. If nothing is found in config → check common ports: `3000`, `5173`, `8000`, `8080`, `8787`

### 2. Check Port Status

> Goal: check whether each port is free

1. On Windows: use `Get-NetTCPConnection -LocalPort <port> -State Listen -ErrorAction SilentlyContinue`
2. Cross-platform: use `Test-NetConnection -Port <port>` or `netstat -ano | findstr :<port>`
3. On macOS/Linux: use `lsof -i :<port>` or `ss -tlnp`
4. Record the state: `free`, `listening`, `time-wait`

### 3. Identify Owning Process

> Goal: know which process holds the port

1. From `Get-NetTCPConnection` take `OwningProcess`, then `Get-Process -Id <pid>`
2. Show `ProcessName`, `Id`, `Path`, and the command line when possible
3. Note whether the process is the project's previous dev server or some other process
4. If it is an old dev server of the same project → flag it as `restartable`

### 4. Suggest Resolution

> Goal: recommend fixes when a port is taken

1. Suggest the next free port (e.g. `<port>+1` until one is free)
2. If the owning process is an old dev server of the same project → suggest killing it and rerunning
3. If it is another process → report its name and let the user decide
4. Never kill a process automatically — always ask the user first

### 5. Report

> Goal: summarize the results in an easy-to-read form

1. Produce a `/report` with columns: `No.`, `Port`, `Status`, `Process`, `PID`, `Action`
2. Status: `free`, `listening`, `conflict`
3. State whether the machine is ready for `run-dev`

## Rules

### 1. Read-Only Default

- Never kill a process without an explicit instruction from the user
- Never change firewall rules or network config

### 2. Cross-Platform

- Use `/use-pwsh-shell` commands on Windows
- Provide command equivalents for macOS/Linux in the report when relevant

### 3. Accuracy

- Check both the TCP `Listen` state and UDP if the app uses it
- Don't conclude a port is free from a failed `Test-NetConnection` alone — verify the listen state as well

- Use /run-dev if needed
- Use /resolve-errors if needed

## Expected Outcome

- You know whether the target ports are free or conflicting, along with the owning process
- You get free-port options or a conflict-resolution plan
- Ready for `run-dev` or deploy without hitting `EADDRINUSE`
