---
name: update
description: >-
  Move the Brigade plugin to the marketplace's current release from inside this session, then have the user run
  /reload-plugins. Use when the user asks to update Brigade, or when you find this session's plugin is behind
  the marketplace's release and moving it is the next useful step.
user-invocable: true
allowed-tools: Bash(claude plugin:*)
---

# Update the plugin

1. Run `claude plugin marketplace update brigade`, then `claude plugin update brigade@brigade --scope user`, then
   `claude plugin update brigade@brigade --scope project` — one per Bash call, from this session, so they act on
   this session's configuration directory. Update BOTH scopes: the user-scope install is the one Brigade's docs
   ask for and it serves every folder under this account; a project-scope install exists only where a repository
   committed `enabledPlugins` for Brigade, and in that folder it is the one a session loads (settings precedence:
   project over user). An answer of `not installed at scope …` is not a failure — it means that scope has no
   install — so relay it in one clause and move on. Relay each command's output. (Updates also arrive on their
   own when the marketplace entry carries `autoUpdate: true`; this skill is for updating right now.)
2. The new version loads only when the user runs `/reload-plugins` or starts a new session; nothing you can run
   does that. The session's background watcher — the process that heartbeats and injects — is replaced by the new
   version at the next prompt after that (0.5.1; before it, a running session kept its old watcher until it
   ended). End with one line telling them to run `/reload-plugins`. If the update reports the plugin is already
   current, say that instead.
