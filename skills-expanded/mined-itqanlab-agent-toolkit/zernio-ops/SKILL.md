---
name: zernio-ops
description: "Run several Zernio workspaces from one MCP server, so the agent can post, schedule and read analytics across every social account at once. Triggers: 'connect my Zernio', 'add a Zernio workspace', 'which Zernio accounts are connected', 'is my Zernio key working', 'post this through Zernio', 'set up the zernio hub', 'zernio'. Zernio ties each API key to one workspace, and an MCP entry sends one key, so a normal setup sees one workspace at a time. This plugin ships one MCP server that holds every key and sends each call to the workspace that owns the account. Keys stay in one local file and never pass through the conversation. Works on macOS, Windows and Linux."
license: MIT
compatibility: "Requires Node 18 or newer. Run scripts/setup-deps.sh (or scripts/setup-deps.ps1 on Windows) to check for it and install it if missing. Needs network access to mcp.zernio.com and api.zernio.com. The plugin's .mcp.json registers the MCP server when the plugin is installed."
metadata:
  author: itqanlab
  version: 1.0.0
  category: productivity
  short: "Use every Zernio workspace from one MCP server"
  starter: "show me every Zernio account that is connected"
---

# Zernio

Two scripts. `scripts/zernio-hub.mjs` is the MCP server. `scripts/setup.mjs` sets up the keys and checks them. Both read the keys through `lib/store.mjs`, the toolkit's shared credential store.

## Why this exists

Zernio is a social media API. Each Zernio API key belongs to one workspace, and each workspace has its own connected accounts. Many people end up with several workspaces, for example one per brand, or one per pair of accounts on a free plan.

An MCP entry sends one fixed key, so it can only ever see one workspace. The usual workaround is one MCP entry per workspace, which means one copy of every tool per workspace and keys sitting in the MCP config.

The hub is one MCP server in front of all of them. It exposes Zernio's own tools once, adds an optional `workspace` argument to each, and sends every call to the right workspace. Nothing in it fixes how many workspaces there are: one key line is one workspace, whether that is one or thirty.

## Who you are doing this for

Assume the person has never opened a terminal. **You run the commands; they never do.** They do two things by hand, because only they can: connect their social accounts in the Zernio dashboard, and paste each API key into a file so it never passes through the conversation.

## Before anything else: check the dependencies

```
sh scripts/setup-deps.sh --check
```

Non-zero exit means Node is missing or too old. `sh scripts/setup-deps.sh` (Windows: `.\scripts\setup-deps.ps1`) prints the right install command for that machine and asks before running it.

## Set up the keys

```
node scripts/setup.mjs status
```

That prints the keys file and, for each workspace, whether its key works and which accounts it can see. It never prints a key.

To add a workspace:

1. Ask the person to sign in to Zernio and make an API key in that workspace's settings.
2. Pick a short name for the workspace: a letter (`a`, `b`) or a word (`brand`, `client_2`). Ask the
   person if they have a naming habit already. Run `node scripts/setup.mjs add <name>`. That writes
   an empty `ZERNIO_KEY_<NAME>=` line.
3. Give them the file path on its own line, and ask them to paste the key right after the `=` sign.
4. Run `node scripts/setup.mjs status` again. A rejected key gets a plain message about what to do.
5. Ask them to restart the agent. The MCP server reads the keys only when it starts.

The keys file is `<store root>/credentials/zernio.env`. The store root is `AGENT_TOOLKIT_HOME` when that is set, otherwise `.itqan-agent-toolkit` in the home folder. It is the same store every toolkit skill uses, mode 600 on macOS and Linux. A good `status` run records the workspace names (never the keys) under `zernio` in `state/setup.json`.

**Never** ask for a key in the chat, print the keys file, or put a key in an MCP config or a repository.

## Using the tools

The tools are Zernio's own: `accounts_list`, `posts_create`, `analytics_get_analytics`, `call_tool`, and the rest. Each one takes an extra optional `workspace`, the name in lowercase.

- **`accounts_list` with no `workspace`** lists every workspace and its accounts. Call it first. The account ids it returns are what the other tools need.
- **Any call with an `account_id`** goes to the workspace that owns that account. You do not need to pass `workspace`. This also works inside `call_tool`, where the real arguments sit one level down.
- **A call with neither** (for example `profiles_list`) needs `workspace`. Without it the hub stops and says so, instead of guessing.

## Things that are easy to get wrong

- **A new key needs a restart.** Adding a line to the keys file does nothing to a server that is already running.
- **A Zernio "success" is not proof the post went out as intended.** Check the post on the platform itself.
- **Do not retry a failed publish blindly.** Some platforms publish even when the call returns an error. List the posts first and look.
- **On Zernio's free plan, an extra workspace is a separate signup.** Inviting a member into an existing team shares its account limit, so it does not add free slots.

## What this cannot do

It does not connect social accounts. That is a login in the Zernio dashboard, and only the person can do it.

It adds nothing to Zernio's own tools. It forwards them. What a tool can do, and the exact arguments it takes, comes from Zernio and changes when Zernio changes it. Read the tool's own schema, not a copy of it.

## Updates

This skill is versioned. Its version is `metadata.version` in the header of this file. `CHANGELOG.md` in this folder lists what changed in each version, newest first.

To check for a newer version, open the address on the `Latest:` line of `CHANGELOG.md` and compare its top version with the installed one. If the newer one is ahead, read every entry between the two and tell the user what changed before anything is updated. A `Breaking` section means the user has to do something. To update, reinstall the skill from its source repository, the same way it was installed.
