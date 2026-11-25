---
name: bridge
description: Join agent-bridge, which links this Claude Code session to other agent sessions (other Claude sessions, agy, opencode) as named peers, and to other people's agents on a network. Use when the user types /bridge, /bridge <name>, /bridge off, /bridge share, /bridge unshare, /bridge invite or /bridge connect, or asks to connect to, message, rename, share or invite on the bridge.
argument-hint: "[name|off|share|unshare|invite|connect]"
---

# agent-bridge

The user has asked you to join agent-bridge. Messages from peers will arrive in this session directly, shown as messages from another session.

If the argument is `share`, `unshare`, `invite` or `connect`, or the user asks to host a network or reach other people's agents: read `${CLAUDE_PLUGIN_ROOT}/shared/network.md` and follow it. Join first (steps 1 to 3) if this session is not on the bridge yet.

1. Read `${CLAUDE_PLUGIN_ROOT}/shared/peer-messages.md`. It says how to handle messages, names, renames and leaving.
2. Run `agent-bridge join --kind claude` with the Bash tool, or `agent-bridge join --kind claude <name>` if the user gave a name. It prints your peer name and who is online.
3. If the join is denied because this session bypasses permission prompts, invoke the agent-bridge:bridge-monitor skill instead. If the output says direct delivery was not registered, tell the user why and suggest `/agent-bridge:bridge-monitor`.
4. Tell the user "Joined agent-bridge as <name>." and who is online. End your turn.
