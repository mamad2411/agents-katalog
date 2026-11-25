---
name: toolkit-credentials
description: "Shared credential setup and storage for any skill that needs an API key or token. Triggers: 'set up my credentials', 'connect my account', 'add an API key', 'where are my tokens stored', 'the skill says my credential is missing', 'toolkit credentials'. Walks a user of any experience level through getting a credential from the provider, storing it in one standard place that works on macOS, Windows and Linux, and verifying it — without the secret ever being typed into the conversation. Other skills call this instead of inventing their own key handling."
license: MIT
compatibility: Requires Node 18 or newer — every script here is written in it. Run scripts/setup.sh (or scripts/setup.ps1 on Windows) to check for Node and install it if it is missing. Nothing else is needed; network access is only whatever the provider being connected requires.
metadata:
  author: itqanlab
  version: 2.1.1
  category: productivity
  short: "Set up and keep API keys safely"
  starter: "set up the API key this skill needs"
---

# Toolkit credentials

Skills that talk to a service need a credential. Without a shared convention every skill invents its own — a different file, a different variable name, a different failure message — and the user is asked to paste a secret into a chat window, where it lands in a transcript and often in a log.

This skill is the convention. One store, one setup flow, one rule.

## Who you are doing this for

Assume the person asking has never opened a terminal and should not have to. **You run the commands; they never do.** The only thing they are asked to do by hand is open one file and paste one value, because that is the one step that must not pass through the conversation.

So:

- Do not print a command and wait. Run it, and say what happened in ordinary words.
- Do not name a flag, a path, or an exit code unless they need to act on it. The one path that matters is the file they must open, and that gets its own line.
- When something fails, say what to do next, not what went wrong internally. "That token is missing one permission — go back to the page and add this row" beats any error text.
- If they clearly are comfortable with a terminal, drop the hand-holding and let them drive. Read which kind of person you are talking to; do not make everyone sit through the same script.

## Before anything else: check the dependencies

Nothing here runs without Node 18 or newer, and a first-time user will not have it as often as you would expect. Check before starting a setup, never after failing one:

```
sh scripts/setup.sh --check
```

Exit status 0 means ready. Non-zero means missing or too old — run `sh scripts/setup.sh` (Windows: `.\scripts\setup.ps1`) which shows the exact install command for that machine and asks before running it. Add `--yes` to install without asking. When there is no package manager it prints instructions the person can follow themselves, including a route that needs no admin rights.

Never assume the tools are present because they are present on your own machine.

## The rule

**A secret value never appears in the conversation.** Not typed by the user, not printed by a script, not echoed back for confirmation.

The flow is always: the agent creates an empty file, the user opens that file and pastes the value in themselves, the agent checks that something is now there. The agent reads the value only inside a running script, at the moment of an API call.

Consequences, all enforceable:

- Never ask the user to paste a credential into the conversation.
- Never display the contents of a credential file. Not to check it, not to help debug.
- Never write a credential into a project directory, a repository, or anywhere a version control system might pick it up.
- `store.mjs` deliberately has no command that prints a value. `has` reports set or not set, and the character count, which is enough to diagnose a bad paste.

## Where things live

```
<store root>/
  credentials/
    <provider>.env      one file per service, e.g. cloudflare.env
  state/
    setup.json          which providers are configured, when last verified,
                        token ids for later revocation — never values
```

The store root is `AGENT_TOOLKIT_HOME` when that variable is set, otherwise a directory named `.itqan-agent-toolkit` in the user's home directory. The publisher prefix is deliberate: "agent-toolkit" alone is a generic phrase that another project could claim, and two tools sharing one directory would be an unpleasant thing to debug. Setting the variable is how an organisation relocates the whole store without touching any skill.

On macOS and Linux the directories are created mode 700 and the files 600. Windows does not enforce these; `store.mjs status` says so plainly rather than implying a protection that is not there.

## Setting up a provider

Run every step through `scripts/store.mjs`. Node is the only requirement, and no packages are installed.

**1. Check first.** Never start a setup the user has already done.

```
node scripts/store.mjs has <provider> <VARIABLE_NAME>
```

Exit status 0 means it is set and you should carry on silently. Non-zero means it needs setting up, and the message says which of the three cases it is: no file, empty file, or the example text still in place.

**2. Create the file.**

```
node scripts/store.mjs scaffold <provider> --var "VARIABLE_NAME:short note about what this is"
```

This writes a commented file with the variable present and empty, and prints its full path.

**3. Tell the user how to get the value.** This is the part that decides whether a non-technical person succeeds, so it is worth doing properly:

- Give the exact web address to open, as a full link.
- Name the button they click, in the words shown on screen.
- If permissions or scopes must be chosen, list every one, exactly as the provider labels it. Do not summarise; a missing scope produces an error message that means nothing to a beginner.
- Say what the value looks like, so they can tell they copied the right thing — roughly how long it is, whether it has a prefix.
- Warn about anything that happens only once, such as a value that is displayed a single time and cannot be retrieved again.

**4. Hand over the file.** Give the full path from step 2 and say: open this file in any text editor, paste the value after the `=`, save it, then say you are done. No quotes, no spaces.

**5. Verify.** Re-run `has`. Then make one real, harmless call against the service — reading the account name is ideal. Report who the credential belongs to and what it can do. Never report the value.

**6. Record it.**

```
node scripts/store.mjs record <provider> '{"verified_at":"<timestamp>","token_id":"<id if the provider gives one>"}'
```

Store the identifier of the credential when the provider issues one, so it can be revoked later without the user hunting through a dashboard.

## When a provider can create its own credential

Some services let a small starter credential create a larger one through their API. Where that is possible, prefer it: the user ticks two boxes instead of forty, which is often the difference between a setup that finishes and one that is abandoned.

The shape is:

1. The user creates a minimal starter credential by hand — usually just the permission to manage credentials.
2. They paste that one into the file, as above.
3. A script uses it to create the real credential, and writes it back without it ever being displayed:

```
<script that mints the credential> | node scripts/store.mjs set-stdin <provider> <VARIABLE_NAME>
```

`set-stdin` reads from standard input precisely so the value never appears in a command line, a process list, or shell history.

4. The script revokes the starter credential, and records the new one's id.

## Using a credential from another skill

Import the helpers; do not shell out and parse.

```js
import { readSecrets } from './lib/store.mjs';

const { CLOUDFLARE_API_TOKEN } = readSecrets('cloudflare');
if (!CLOUDFLARE_API_TOKEN) {
  console.error('Cloudflare is not set up yet. Run the credential setup first.');
  process.exit(1);
}
```

Because each skill directory has to work on its own wherever it is copied, a provider skill carries its own copy of `store.mjs` under `lib/`. Copy it verbatim from this skill and do not edit it, so every skill agrees on the file format and the location.

## Failure messages

The user is often not an engineer, and the error is the only instruction they will read. Every failure says what happened, what to do, and where.

Good: `Cloudflare is not set up yet. Run the credential setup for cloudflare, then try again.`

Bad: `ENOENT: no such file or directory, open '.../cloudflare.env'`

When a call is refused for lack of permission, name the exact permission to add and where to add it, then offer to re-verify. Do not make the user guess which of forty checkboxes was missing.

## Commands

| Command | Does |
| :-- | :-- |
| `path` | Print the store root |
| `status` | List configured providers, when each was last verified, and any permission warnings |
| `has <provider> <KEY>` | Report whether a value is set. Exit 0 set, non-zero not. Never prints the value |
| `scaffold <provider> --var "NAME:note"` | Create the file for the user to edit |
| `set-stdin <provider> <KEY>` | Store a value read from standard input, for credentials a script creates |
| `record <provider> <json>` | Save non-secret bookkeeping about the credential |

## Checklist for adding a provider

- One file, named for the service, holding every variable that service needs.
- Setup is idempotent — running it again when it is already configured does nothing and says so.
- Verification makes a real call and reports the account identity, never the value.
- Every documented permission or scope is listed in full, with the provider's own wording.
- The credential's id is recorded, so revoking it later does not require a dashboard hunt.

## Updates

This skill is versioned. Its version is `metadata.version` in the header of this file. `CHANGELOG.md` in this folder lists what changed in each version, newest first.

To check for a newer version, open the address on the `Latest:` line of `CHANGELOG.md` and compare its top version with the installed one. If the newer one is ahead, read every entry between the two and tell the user what changed before anything is updated. A `Breaking` section means the user has to do something. To update, reinstall the skill from its source repository, the same way it was installed.
