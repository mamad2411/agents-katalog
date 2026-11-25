---
name: dokploy-ops
description: "Connect one or more self-hosted Dokploy installations once, then run what is deployed on them from the agent. Triggers: 'connect my Dokploy', 'deploy the app', 'what is deployed', 'show me the logs', 'why did the deploy fail', 'restart the app', 'is the site up', 'list my services', 'what domain is this on', 'redeploy', 'check the server health', 'dokploy'. See every app, database and compose stack with its real state, deploy and watch the build to the end, read logs, restart, stop, check domains and environment variables, and find out which service is broken. Setup adopts a key the machine already has, or walks through making one. Several installations are kept apart by name, so a deploy cannot land on the wrong server. Works on macOS, Windows and Linux."
license: MIT
compatibility: "Requires Node 18 or newer — run scripts/setup-deps.sh (or scripts/setup-deps.ps1 on Windows) to check for it and install it if missing. Needs network access to the Dokploy installation itself, which is self-hosted — some are only reachable over a VPN. Endpoint lookup reads the API description from that installation, so it always matches the version actually running."
metadata:
  author: itqanlab
  version: 2.1.2
  category: devops
  short: "Deploy and watch apps on self-hosted Dokploy"
  starter: "tell me why the last deploy failed"
---

# Dokploy

Three scripts. `scripts/setup.mjs` connects installations, `scripts/dk.mjs` does the work, and `scripts/api.mjs` looks up any call the others do not wrap.

## Who you are doing this for

Assume the person asking has never opened a terminal. **You run the commands; they never do.** They are asked to do exactly two things by hand, and only because neither can be done for them: make a key in their dashboard, and paste it into a file so it never passes through the conversation.

Everything else is yours. Report it in plain words: "the new version is live at example.com" is the result they asked for; the deployment id is not. When a build fails, do not hand back a wall of log — read it, and say what broke.

If they are clearly comfortable with a terminal, stop narrating and let them drive.

## Before anything else: check the dependencies

```
sh scripts/setup-deps.sh --check
```

Non-zero exit means Node is missing or too old. `sh scripts/setup-deps.sh` (Windows: `.\scripts\setup-deps.ps1`) prints the right install command for that machine and asks before running it.

## Connect an installation first

```
node scripts/setup.mjs status
```

If nothing is connected, **look before asking for anything** — a machine that talks to Dokploy usually has a key for it already:

```
node scripts/setup.mjs import          shows what was found, changes nothing
node scripts/setup.mjs import --yes    adopts it
```

Otherwise:

```
node scripts/setup.mjs add <a-name-for-it> [https://dokploy.example.com]
node scripts/setup.mjs verify <that-name>
```

`add` writes the empty file, names it, and explains where in the dashboard to make the key. **Never ask for the key in the conversation** — the user pastes it into the file the script names.

### Two values, not one

Dokploy is **self-hosted**, so a credential is an address *and* a key. The address is the dashboard's own — the page they log in to — not a site it hosts. That mistake is common enough that the scripts detect it: an address answering with a web page instead of data gets a message saying exactly this.

### Several installations

```
node scripts/setup.mjs status                every installation, and whether it answers
node scripts/setup.mjs use <name>            make one the default
node scripts/setup.mjs rename <old> <new>
node scripts/setup.mjs forget <name> --yes
```

Any command runs against another installation with `--instance <name>`:

```
node scripts/dk.mjs --instance staging services
```

With several configured and no default set, commands refuse to run rather than guess. Say which installation you are on whenever you report anything.

## Commands

```
node scripts/dk.mjs whoami                  which installation, its version, how much is on it
node scripts/dk.mjs services                everything deployed, worst news first
node scripts/dk.mjs projects                the same, grouped by project and environment
node scripts/dk.mjs service <name>          one service: source, domains, last build
node scripts/dk.mjs health                  the installation itself, plus anything failing
node scripts/dk.mjs servers                 other machines this installation deploys to
node scripts/dk.mjs containers              what is actually running, at the container level
```

Deploying and running:

```
node scripts/dk.mjs deploy <name>           deploy, and wait for the build to finish
node scripts/dk.mjs redeploy <name>         rebuild from scratch
node scripts/dk.mjs restart <name>          restart what is running, without rebuilding
node scripts/dk.mjs stop <name> --yes
node scripts/dk.mjs start <name>
```

Finding out what happened:

```
node scripts/dk.mjs logs <name> [--tail 200] [--search <text>]    what the app is printing
node scripts/dk.mjs deployments <name> [--limit 10]               build history
node scripts/dk.mjs build-log <name>                              output of the last build
node scripts/dk.mjs domains <name>
node scripts/dk.mjs env <name> [--values]
```

Names are only unique within an environment. When one matches more than one service, the command lists them and stops; narrow it with `--in <project>`.

## Things that are easy to get wrong

**"Deployed" is not "deployed successfully".** The API answers the moment a build is queued. `deploy` and `redeploy` therefore follow the deployment to its end and report what actually happened, including the error. Never tell a user something is live off the back of a request being accepted.

**`logs` and `build-log` answer different questions.** `logs` is what the running application is printing — the right thing for "the site is throwing errors". `build-log` is the output of the last build — the right thing for "the deploy failed". Reaching for the wrong one wastes a round trip.

**`restart` does not pick up new code.** It restarts what is already there. A change in the repository needs `deploy`. Content that is still stale after a successful deploy needs `redeploy`, which rebuilds without the cache.

**Environment variables are where the secrets are.** `env` prints names and value lengths only. `--values` prints them in full, which puts every password an application holds into whatever is recording the session. Do not use it to "check" something — read the name, or ask the user to look.

**Stopping takes a site offline.** `stop` refuses without `--yes` and says what will happen. Restarting is `start`, not `deploy`.

**Databases are services too.** Postgres, MySQL, MariaDB, Mongo, Redis and libSQL all appear in `services` and take the same commands. Stopping one takes down everything that depends on it, which is rarely just the one app.

## Before changing anything

**Show the current state first.** `services` or `service <name>`, and say which installation. A deploy against the wrong installation is not recoverable by re-running it somewhere else.

**Check what is already failing before deploying.** `health` in one call. Deploying on top of an installation that is already broken makes the cause much harder to find.

**Deleting and stopping require confirmation.** Show what matched, get an explicit yes, then re-run with `--yes`. Never pass it on the first attempt.

## Anything not wrapped above

Dokploy has around 540 calls and `request()` reaches all of them with the same key. They are named `router.procedure` — reads are GET with query parameters, writes are POST with a JSON body.

**Do not guess which.** Look it up — from the installation itself, so it matches the version actually running:

```
node scripts/api.mjs search backup postgres
node scripts/api.mjs show /backup.create post
```

Then:

```js
import { request, findService } from './scripts/dk.mjs';

const service = await findService('web');
await request('domain.create', { method: 'POST', body: { host: 'app.example.com', applicationId: service.id, port: 3000 } });
```

`findService` exists because **nothing is addressed by name** in this API — every call wants an id, and ids appear nowhere a user would ever see them.

`references/playbooks.md` shows the same pattern in context.

## What this cannot do

It talks to Dokploy, not to the machine underneath it. Disk space, system packages and anything outside a container are a shell session, not a call here.

It also does not create the installation. Dokploy has to be installed on a server and reachable before any of this applies.

## Failure messages

Errors are rewritten for people who do not know the API. A rejected key explains that keys are revoked from the dashboard and how to replace one; an unreachable address lists the three things worth checking, in order, including that some installations are only reachable over a VPN. Keep that habit for anything added here: say what happened, then what to do next.

## Updates

This skill is versioned. Its version is `metadata.version` in the header of this file. `CHANGELOG.md` in this folder lists what changed in each version, newest first.

To check for a newer version, open the address on the `Latest:` line of `CHANGELOG.md` and compare its top version with the installed one. If the newer one is ahead, read every entry between the two and tell the user what changed before anything is updated. A `Breaking` section means the user has to do something. To update, reinstall the skill from its source repository, the same way it was installed.
