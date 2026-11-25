---
name: local-secrets
description: >-
  The rule and the mechanism for values that must never be written into a
  repository — passwords, API keys, tokens, account logins, local DB
  credentials. Source files carry only the NAME of a value; the value itself
  lives in the machine's keychain and is fetched at run time. Load whenever a
  script, skill or command needs a credential, whenever a stored credential
  stops working, or before hardcoding any value that looks like a secret.
---

# Local secrets — names in the repo, values in the keychain

## The rule

A repository stores the **name** of a value, never the value. `password`,
`api_key`, `token`, `client_secret`, an account email, a DB user — all of them
are referenced by name and resolved at run time. This holds for private repos
too: history is forever, clones spread, and a private repo can be made public
by one click.

## Fetching a value

```bash
DB_PASSWORD="$(scripts/secret-get.sh LOCAL_DB_PASSWORD)" || exit 1
```

`secret-get.sh` prints the value on success. When nothing is stored it exits 1
and prints the exact command to ask for — do not invent a value, do not fall
back to a default, and do not put the value in the source file.

## Asking for a value (once)

Ask the person to run it themselves, so the value goes from their keyboard to
the keychain without passing through the conversation:

```
! <plugin>/scripts/secret-set.sh LOCAL_DB_PASSWORD
```

It prompts on their terminal, does not echo, and stores the value in the login
keychain. After that every later run resolves it silently — nobody is asked
twice.

If the person instead types a value into the chat, store it immediately with
`secret-set.sh <NAME> --stdin` and then say plainly that a value typed into the
conversation is also written to the session transcript on disk, so it should be
rotated if it matters.

## When a stored value stops working

Authentication failing is a signal the stored value is stale, not a reason to
retry it:

```bash
scripts/secret-forget.sh LOCAL_DB_PASSWORD
```

Then ask for a fresh one exactly as above. Never loop on a failing credential —
several wrong attempts lock accounts.

## What belongs in the repo instead

- The **name**, in documentation and in the usage header of the script.
- A `.env.example` listing names with empty or obviously fake values.
- A clear error when the value is missing, naming what to set.

Anything else — a real address, a real key, a working password, a personal
login — is a finding the pre-commit secret scan is meant to block, and a
reviewer must treat as blocking.
