---
name: secrets-hygiene
description: Prevents and responds to leaked credentials in code and git repositories. Use whenever the user commits or pushes code, handles API keys, tokens, passwords, .env files or SSH keys, asks to scan a repo for secrets, set up a pre-commit guard, write a .gitignore for credentials, or says a token was leaked or pasted by mistake, even if they only say "is it safe to push this". Scans with masked output and gives a rotate-first response plan.
---

# secrets-hygiene

Keep credentials out of repositories, and respond correctly when one leaks. The scanner masks every match, so running it never spreads a secret further.

```
secrets-hygiene/
├── SKILL.md
├── scripts/
│   ├── scan_secrets.py     scan staged changes, tracked files or paths; masked output
│   └── install_hook.sh     pre-commit hook that blocks commits containing secrets
└── references/
    └── leak-response.md   rotate-first plan, history purge, .gitignore, prevention
```

## When to use

- Before a commit or push
- Reviewing a repo, zip or config for credentials
- Setting up `.gitignore` and `.env` handling
- A token, key or password was pasted, committed or logged

## Workflow

1. **Scan** before committing: `python3 scripts/scan_secrets.py --staged`
2. **Fix** findings by moving values to environment variables or a secret manager; commit `.env.example` with fake values.
3. **Guard**: `bash scripts/install_hook.sh` so the scan runs on every commit.
4. **Audit** an existing repo: `python3 scripts/scan_secrets.py --all`
5. **If something leaked**, follow the order in `references/leak-response.md`: revoke first, then clean.

## What the scanner finds

AWS access keys, GitHub tokens (classic and fine-grained), Slack tokens, Google API keys, Stripe live keys, private key blocks, JSON web tokens, URLs with embedded credentials, and generic `key = "value"` assignments with high entropy. Placeholders such as `example`, `changeme` and `<token>` are ignored. Mark a known false positive with `secret-scan: ignore` on that line.

The scanner covers the current files and staged changes. It does not search old history: for that, check the provider's own scanning or run `git log -p` through the scanner:

```bash
git log -p | python3 scripts/scan_secrets.py /dev/stdin
```

## Rules

- Treat any secret that reached a remote as public, even if deleted a minute later
- Rotate first, clean history second
- Never print, echo or paste a real secret into chat; mask it as `ghp_ab****yz`
- Never place tokens in remote URLs or command arguments that are saved in history
- Give tokens the least scope and an expiry date
- Do not hide a finding to make a scan pass; either fix it or mark a verified false positive

## What to report back

| Field | Content |
|-------|---------|
| Findings | file, line, type, masked value |
| Real or false positive | and how you decided |
| Action | rotate, remove, move to env var, ignore marker |
| Prevention | hook installed, `.gitignore` entries added |

## Related skills

- `termux-setup`: token and SSH setup for git on a phone
- `commitsmith`: commit the fix with a clear message
- `code-review`: check for security issues beyond secrets
