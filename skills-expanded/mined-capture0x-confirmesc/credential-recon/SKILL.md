---
name: credential-recon
description: Use CONFIRMED credential-recon findings from confirmesc (readable SSH keys, .env, .netrc, history) to pivot or escalate by reusing another user's secrets.
---

# Credential recon

confirmesc flags files that belong to another user but are readable by you: SSH
private keys, `.git-credentials`, `.netrc`, `.my.cnf`, `.pgpass`, `wp-config.php`,
`.env`, and shell history files.

## When to use

confirmesc reports findings like:

```
[CONFIRMED] Readable private SSH key belonging to another user
[CONFIRMED] Readable credential file belonging to another user
```

## How to use

- SSH key: `ssh -i <key> <user>@<host>` to become that user.
- `.env` and config secrets: database and service passwords are frequently
  reused for sudo or for other accounts.
- Shell history: look for inline passwords, tokens, and one-off privileged
  commands.
- Chain it: a reused password may unlock a sudo-capable or root account.

## Verify

Authenticate as the recovered identity (ssh, su, or a service login) and confirm
the new context.

## Rules

- Authorized targets only. Reusing found credentials stays in scope only within
  your authorization.
