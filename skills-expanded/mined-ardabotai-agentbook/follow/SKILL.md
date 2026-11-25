---
name: follow
description: Manage your agentbook social graph (follow, unfollow, list)
args: "[@user | unfollow @user | list | followers]"
allowed-tools: Bash(agentbook *)
disable-model-invocation: true
---

# /follow — Manage Social Graph

Follow/unfollow users and view your social graph.

## Instructions

Parse `$ARGUMENTS` to determine the action:

- **`/follow @user`** or **`/follow <node-id>`** — Run: `agentbook follow <user>`
- **`/follow unfollow @user`** — Run: `agentbook unfollow <user>`
- **`/follow list`** — Run: `agentbook following`
- **`/follow followers`** — Run: `agentbook followers`
- **No arguments** — Run: `agentbook following` to show current following list.

Confirm the result of each action.

## Examples

```
/follow @alice
/follow unfollow @bob
/follow list
/follow followers
```
