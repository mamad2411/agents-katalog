---
name: check
description: List the MCP servers, skills and instruction files this machine's agents have installed, using Small Print's check. Nothing is sent anywhere.
allowed-tools: Bash(npx -y smallprint@1.6.0 check --no-upload:*)
disable-model-invocation: true
---

# What Small Print found on this machine

The command below was run on this machine with `--no-upload`, so nothing was sent anywhere. It read the MCP configuration files, skills and instruction files of the agent apps the command knows; https://smallprint.dev/cli names them.

```!
npx -y smallprint@1.6.0 check --no-upload
```

Show the user the list above as it was printed, in a code block, without leaving anything out. Then tell them, in two or three plain sentences: that nothing was sent; that `npx smallprint check --upload` would send the names, versions, hosts and file hashes of those items to smallprint.dev and return grades and any advisories on record for them; and that `/smallprint:locked` checks the same list against a lock file and `/smallprint:gate` asks Small Print's record whether, for each MCP server installed here that has a registry name, a change to what it tells an agent is on record since the lock, or a high or critical advisory covers the version installed. Do not run either of those unless the user asks.
