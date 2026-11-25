---
name: diagnose-a-deployment
description: Work out why an app on an Impreza VPS is failing, restarting, or not answering — using logs, its own files, and its own command line. Use when a deployment crashed, crash-loops, returns errors, or came up but does not serve.
---

# Why is this app not working

Three sources, in this order. Each one answers something the previous cannot,
and skipping ahead usually means guessing.

## 1. What it printed — logs

`impreza_get_logs` for a block, `impreza_tail_logs` to follow. Start here
always. A crash-loop almost always names its own cause in the last twenty lines
before the restart, and reading them costs one call.

Read the whole stack trace before forming a theory. The first line of a Python
traceback is the least informative line in it.

## 2. What is actually on disk — files

`impreza_inspect_app` reads the app's own storage: list a directory, read a
file, tail it, grep it. This answers the question logs cannot — **did that
variable actually land in the config file**. Logs tell you the app was
unhappy; the config file tells you why.

It is **asynchronous**: it returns a `read_id`, and `impreza_get_app_read`
collects the result. It is also read-only by construction — the storage is
mounted read-only, there is no shell and no command string.

> Output is capped at 256 KB and kept for about a day. It is deliberately not
> in the 30-day call log, because an app's config file is exactly where its
> database password lives. Do not paste a config file back to the customer
> wholesale; quote the line that matters.

## 3. What the app itself says — its CLI

`impreza_app_cli` runs the application's own command line — `wp`, `occ`,
`gitea admin`, a database dump — in a separate container with the app's files,
network and environment. `impreza_get_cli_run` collects the output.

This is how you ask WordPress what it thinks its own site URL is, rather than
inferring it. Same capture rules as a file read: 256 KB, about a day.

## The database is a container too

An app that "cannot connect to the database" is usually not a network problem.
Check whether the database container is up before you go looking at
credentials. `impreza_list_deployments` shows the whole stack.

## Before you say it is fixed

`impreza_probe_deployment` checks public HTTPS from outside. `running` means
the container is alive; it does not mean anyone can reach the site. If the
customer's complaint was "my site is down", the probe is the thing that answers
it, not the status field.

## Restart, redeploy, or neither

- **Restart** (`impreza_restart_deployment`) for a process that is wedged but
  whose configuration is right.
- **Redeploy** (`impreza_redeploy_deployment`) after you changed something that
  only takes effect on a rebuild. It keeps the app and its domain in place.
- **Neither**, if you have not read the logs yet. Restarting a crash-loop
  restarts the crash.

## When nothing explains it

`impreza_doctor` checks the account's own plumbing — credentials, expiry,
agent connectivity. An app that cannot possibly be reached because the agent on
the box is offline will otherwise waste a long time.
