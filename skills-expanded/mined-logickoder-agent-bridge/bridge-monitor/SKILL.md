---
name: bridge-monitor
description: Join agent-bridge in monitor mode, where a background monitor delivers peer messages as monitor events instead of direct session messages. Use only when the user types /bridge-monitor, asks for monitor mode, or the bridge skill's join was denied in bypass-permissions mode.
argument-hint: "[name]"
---

# agent-bridge, monitor mode

Invoking this skill started the agent-bridge monitor in the background. Messages from peers arrive as monitor events.

1. Read `${CLAUDE_PLUGIN_ROOT}/shared/peer-messages.md`. It says how to handle messages, names, renames and leaving.
2. Run `agent-bridge join --kind claude --no-push` with the Bash tool, or `agent-bridge join --kind claude --no-push <name>` if the user gave a name. It prints your peer name and who is online. The monitor attaches to it.
3. Tell the user "Joined agent-bridge as <name> (monitor mode)." and who is online. End your turn.

To share this session with other people's agents, host, invite or connect: read `${CLAUDE_PLUGIN_ROOT}/shared/network.md` and follow it.

A monitor event saying another session took over, the session left, or it already receives some other way: tell the user and do nothing else.
