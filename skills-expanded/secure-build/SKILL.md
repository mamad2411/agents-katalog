---
name: secure-build
description: "Use when writing, auditing or deploying code: security defaults and a review pass."
version: 1.1.0
author: coder role of hermes-fleet-apps
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [security, secrets, audit, hardening, privacy, threat-model, dependencies]
---

# Secure Build

Security is not a phase at the end. It is a set of defaults applied while typing, plus a
review pass before anything is exposed to a network or another person.

For local apps and tools, the threat model that matters is: leaked credentials, an
exposed service, a malicious dependency, and data leaving the owner's machines without
the owner choosing it.

## The non-negotiables

**Secrets never enter code, logs, or the conversation.**
You are a language model running on someone else's infrastructure. Anything you read
leaves the machine. So:

- Never read, echo, copy, or move an API key, token, password, private key, certificate,
  or seed phrase — not even "just between two local files".
- When one is needed: stop, state the exact file path and the exact variable name, and
  let the owner type it.
- Secrets live in `.env` (or the OS keyring). Settings live in config files. Never
  reversed.
- `.env`, `*.pem`, `*.key`, `id_*`, `credentials.json` go in `.gitignore` before the
  first commit, not after.
- Before any commit or upload: grep the diff for key-shaped strings.

**No unconsented file access.**
Read what the task needs, inside the working directory. Going outside it, or scanning
broadly, needs the owner's explicit yes first. Never index or summarise their filesystem
"to be helpful".

**Least privilege, always.**
Run as a normal user, not root or Administrator. Bind services to `127.0.0.1` unless the
job is explicitly to expose them. Containers get read-only mounts and a non-root user
where possible. A token gets the narrowest scope that works.

## Writing code: the default checklist

| Risk | Default |
|---|---|
| Shell injection | Never build a shell string from input. Pass an argument list — `subprocess.run([...])`, never `shell=True` with interpolation. |
| SQL injection | Parameterised queries only. No f-strings in SQL, ever. |
| Path traversal | Resolve and confirm the path stays inside the intended root before opening it. |
| Untrusted input | Validate at the boundary: type, length, range, allowed set. Reject, do not sanitise-and-hope. |
| Deserialisation | Never `pickle`, `eval`, `yaml.load` on untrusted data. Use JSON or `yaml.safe_load`. |
| Secrets in logs | Redact before logging. Log the field name, not the value. |
| Dependencies | Pin exact versions. Check the package is real, maintained, and correctly spelled — typosquats are the common attack. |
| Transport | HTTPS with certificate verification on. Never disable it to make an error go away. |
| Auth on a web app | Hash passwords with argon2 or bcrypt. Never roll custom crypto. Use a library's session handling. |
| File permissions | Config with secrets: `chmod 600`. Never world-readable. |

## Review pass

Run this before anything is exposed, published, or handed to another person. Report
findings as: **what, where, severity, fix** — one line each. No essays.

1. **Secrets** — grep the whole tree for keys, tokens, passwords, private keys. Include
   git history, not just the working tree.
2. **Inputs** — list every place external data enters (args, HTTP, files, env, stdin).
   Confirm each is validated.
3. **Exposure** — what ports are open, to what interface, with what auth? Anything on
   `0.0.0.0` needs a stated reason.
4. **Dependencies** — count them. Each one is trust extended to a stranger. Check for
   known advisories (`pip-audit`, `npm audit`, `uv pip list --outdated`).
5. **Permissions** — what does this run as, and what can it reach if compromised?
6. **Failure mode** — when it crashes, does it leak a stack trace with paths, queries,
   or tokens to the user?
7. **Data flow** — what leaves the machine, to where, and did the owner choose that?
   Telemetry in a dependency counts.

## Self-hosting notes (containers, VMs)

- One service per container. A compromise should not reach the rest of your data.
- Reverse proxy in front, TLS terminated there, service itself not exposed.
- Mounts read-only unless the service must write.
- Backups before any migration. Verify the backup restores — an untested backup is a
  rumour.
- No service exposed to the internet without auth in front of it, even "just for a test".

## Pitfalls

**Disabling a security check to fix an error.** `verify=False`, `--no-check-certificate`,
`shell=True`, a wildcard CORS — each is a real bug being hidden. Fix the cause.

**Assuming local means safe.** A local service with no auth is one misconfigured
firewall rule away from public.

**Trusting a dependency because it has stars.** Check the last commit date, the
maintainer count, and whether the name is the one actually intended.

**Auditing only the working tree.** A secret committed then deleted is still in git
history and still leaked. Say so plainly; rotation is the only fix and the owner does it.

**Writing a threat model nobody asked for.** Match the depth to the stakes. A personal
script and a public web app get different passes.
