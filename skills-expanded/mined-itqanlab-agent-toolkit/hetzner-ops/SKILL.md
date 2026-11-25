---
name: hetzner-ops
description: "Connect one or more Hetzner Cloud projects once, then run the servers from the agent. Triggers: 'connect my Hetzner', 'list my servers', 'create a server', 'reboot the server', 'resize my server', 'how much is this server costing', 'add an SSH key', 'what is my server's IP', 'is the server up', 'delete this server', 'add a DNS record on Hetzner', 'show my Hetzner projects', 'hetzner'. List them, create, start, stop, resize, delete, manage SSH keys, firewalls, volumes, private networks, DNS zones and records, and see what the project is costing — without opening the console again. Setup adopts a token the machine already has, or walks through making one in about a minute. Several projects are kept apart by name, so a change cannot land on the wrong one by accident. Works on macOS, Windows and Linux."
license: MIT
compatibility: "Requires Node 18 or newer — run scripts/setup-deps.sh (or scripts/setup-deps.ps1 on Windows) to check for it and install it if missing. Needs network access to the Hetzner Cloud API. Endpoint lookup downloads Hetzner's API description once (about 3 MB) and caches it. Covers Hetzner Cloud only — dedicated servers and storage boxes are a different service with separate credentials."
metadata:
  author: itqanlab
  version: 2.1.2
  category: devops
  short: "Run your Hetzner Cloud servers from your agent"
  starter: "show my servers and what they cost"
---

# Hetzner Cloud

Three scripts. `scripts/setup.mjs` connects projects, `scripts/hz.mjs` does the work, and `scripts/api.mjs` looks up any endpoint the others do not wrap.

## Who you are doing this for

Assume the person asking has never opened a terminal. **You run the commands; they never do.** They are asked to do exactly two things by hand, and only because neither can be done for them: create a token on a web page, and paste it into a file so it never passes through the conversation.

Everything else — checking what exists, making the change, waiting for it to finish, confirming it worked — is yours. Report it in plain words. "The server is back up at 203.0.113.10" is the result they asked for; the action id is not.

If they are clearly comfortable with a terminal, stop narrating and let them drive.

## Before anything else: check the dependencies

These scripts need Node 18 or newer. Check first, so a missing dependency does not surface as a confusing failure halfway through a setup:

```
sh scripts/setup-deps.sh --check
```

Non-zero exit means missing or too old. `sh scripts/setup-deps.sh` (Windows: `.\scripts\setup-deps.ps1`) prints the right install command for that machine and asks before running it; `--yes` skips the question.

## Connect a project first

```
node scripts/setup.mjs status
```

If nothing is connected, **look before asking for anything**. Many machines already have a Hetzner token configured for some other tool, and sending someone to make a second one is wasted effort and a second secret to look after:

```
node scripts/setup.mjs import          shows what was found, changes nothing
node scripts/setup.mjs import --yes    adopts it
```

The originals are left where they are and keep working.

If there is nothing to adopt, run the guided setup and follow what it prints:

```
node scripts/setup.mjs add <a-name-for-it>
node scripts/setup.mjs verify <that-name>
```

`add` writes the empty file, names it, and explains where in the Hetzner console to make the token. **Never ask for the token in the conversation** — the user pastes it into the file the script names. `verify` then checks it and reports whether it can make changes or only read.

### Why the name matters

**A Hetzner token belongs to one project, and Hetzner will not tell you which one.** There is no "who am I" call. The name given at setup is the only label that exists, so choose one the user will recognise — the project's name in the console is the obvious choice.

Every command that changes something prints that name. Do not remove that.

```
node scripts/setup.mjs status            every project, and whether its token still works
node scripts/setup.mjs use <name>        make one the default
node scripts/setup.mjs rename <old> <new>
node scripts/setup.mjs forget <name> --yes
```

Any command runs against another project with `--project <name>`:

```
node scripts/hz.mjs --project staging servers
```

With several projects configured and no default set, commands refuse to run rather than guess.

### Read or Read & Write

Hetzner asks this once, when the token is made, and it cannot be changed afterwards. A read-only token lists things and fails on every change. `verify` says which kind was pasted, so this is caught at setup instead of halfway through a deployment.

## Commands

```
node scripts/hz.mjs whoami                  which project is selected, and its size
node scripts/hz.mjs servers                 every server: status, address, type, price
node scripts/hz.mjs server <name>           one server in full
node scripts/hz.mjs costs                   what this project costs per month
node scripts/hz.mjs metrics <name> [--type cpu|disk|network] [--hours 6]
```

Running servers:

```
node scripts/hz.mjs create <name> --type cx22 --location hel1 [--image ubuntu-24.04] [--ssh-key <name>]
node scripts/hz.mjs power-on <name>
node scripts/hz.mjs shutdown <name>         asks the operating system to stop, cleanly
node scripts/hz.mjs power-off <name> --yes  cuts the power — see below
node scripts/hz.mjs reboot <name>
node scripts/hz.mjs resize <name> <type> [--upgrade-disk] --yes
node scripts/hz.mjs delete <name> --yes
```

Everything else in the project:

```
node scripts/hz.mjs ssh-keys
node scripts/hz.mjs ssh-key-add <name> <path-to-public-key>
node scripts/hz.mjs firewalls
node scripts/hz.mjs volumes
node scripts/hz.mjs networks
node scripts/hz.mjs load-balancers
node scripts/hz.mjs snapshots
node scripts/hz.mjs types [--location hel1]   sizes and prices where you are building
node scripts/hz.mjs locations
node scripts/hz.mjs images
```

DNS, when the domain's zone is hosted at Hetzner:

```
node scripts/hz.mjs zones
node scripts/hz.mjs dns <domain>
node scripts/hz.mjs dns-add <hostname> <type> <value> [--ttl 300] [--append]
node scripts/hz.mjs dns-remove <hostname> --type A --yes
node scripts/hz.mjs check <hostname>          what public resolvers currently return
```

## Things that are easy to get wrong

**`shutdown` and `power-off` are not the same.** `shutdown` asks the operating system to stop and lets it close its files. `power-off` cuts the power like pulling the cable, and anything not yet written to disk is lost. Prefer `shutdown`. `power-off` refuses to run without `--yes` and explains the difference first.

**A stopped server still costs money.** Hetzner bills for the server existing, not for it running. If someone stops a server to save money, tell them plainly that it does not, and that deleting is what stops the billing.

**`--upgrade-disk` cannot be undone.** Growing the disk during a resize is permanent, and a server with a grown disk can never move to a smaller type again. Without the flag the disk is left alone and the change is reversible. Do not add it unless the user has asked for more disk specifically.

**Creating a server without an SSH key is a security decision.** Hetzner then sets a root password and the machine accepts password logins from its first second alive. `create` refuses that path unless `--no-ssh-key` is passed, and when it happens the password is written into the credential file rather than printed, so it does not end up in a transcript.

**Names are unique per project, not globally.** Two projects can both have a `web-01`, and `--project` is the only thing keeping them apart.

**Most changes are asynchronous.** Hetzner answers with an action that is still running. Every command here waits for it to finish before reporting, so a message from these scripts means the change is done, not merely accepted.

## Before changing anything

**Show the current state first.** Run `servers` or `server <name>` and show the user what is there before creating, resizing or deleting. Say which project it is in.

**Deleting and power-cutting require confirmation.** `delete`, `power-off` and `dns-remove` print what they matched and refuse to act without `--yes`. Show that to the user and get an explicit yes before re-running with the flag. Never pass `--yes` on the first attempt.

**Check the price before creating.** `types --location <where>` lists what is available and what it costs. Server types differ by location, and one that exists in one place may not exist in another.

## Anything not wrapped above

The commands cover the everyday work. `request()` from `scripts/hz.mjs` reaches every endpoint with the same token, so the only real question is which endpoint and what it wants.

**Do not guess that.** Look it up:

```
node scripts/api.mjs search load balancer service
node scripts/api.mjs show <path> <method>
```

Then:

```js
import { request, waitForAction, findServer } from './scripts/hz.mjs';

const server = await findServer('web-01');
const { action } = await request(`/servers/${server.id}/actions/enable_backup`, { method: 'POST' });
await waitForAction(action, { label: 'turning on backups' });
```

`waitForAction` is not optional decoration — an action that is returned is not an action that has happened.

`references/playbooks.md` shows the same pattern in context.

## What this cannot do

Hetzner Cloud only. Dedicated servers, storage boxes and the older Robot service are a different product with different credentials, and none of them are reachable from here.

It also does not configure anything **inside** a server. Creating the machine is where this stops; installing software on it is a job for a shell session or a deployment tool.

## Failure messages

Errors are rewritten for people who do not know Hetzner's error codes. A refused change explains that the token is probably read-only and how to replace it; a sold-out server type says to try another location rather than repeating the request. Keep that habit for anything added here: say what happened, then what to do next.

## Updates

This skill is versioned. Its version is `metadata.version` in the header of this file. `CHANGELOG.md` in this folder lists what changed in each version, newest first.

To check for a newer version, open the address on the `Latest:` line of `CHANGELOG.md` and compare its top version with the installed one. If the newer one is ahead, read every entry between the two and tell the user what changed before anything is updated. A `Breaking` section means the user has to do something. To update, reinstall the skill from its source repository, the same way it was installed.
