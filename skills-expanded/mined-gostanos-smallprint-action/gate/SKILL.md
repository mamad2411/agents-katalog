---
name: gate
description: Ask Small Print's record whether, for each MCP server installed here that has a registry name, a change to what it tells an agent is on record since the lock, or a high or critical advisory covers the version installed. Sends the registry name of each server.
allowed-tools: Bash(npx -y smallprint@1.6.0 gate:*)
disable-model-invocation: true
---

# The gate

The command below asked smallprint.dev, for each MCP server installed here that has a registry name, whether a change to its small print is on record between the version in the lock and the pinned version (the newest on record when the config pins none), and whether a high or critical advisory covers the version installed here. A release counts as a change only when it holds a change to the text; a different fingerprint alone does not. It sent the registry name of each server, one request each. It exits with code 3 when a high or critical advisory covers an installed version, and otherwise with code 2 when a change to the small print is on record.

```!
npx -y smallprint@1.6.0 gate || true
```

Show the user the result above as it was printed, in a code block. Then say, in plain sentences, what it means: which servers have a change to their small print on record, carry an advisory, or could not be answered, with the link the command printed for each one. Where the command says no change is on record, say that, not that the server is unchanged. Do not judge whether a server is safe; say what the record holds and where to read it.
