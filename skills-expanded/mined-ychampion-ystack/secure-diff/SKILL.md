---
name: secure-diff
description: >-
  Security self-check of your own diff before you hand it over: scan for secrets, then walk every new
  input path for injection, missing authorization, unsafe file and network access, and risky defaults,
  and prove each suspect with a quick probe. Use before committing or pushing agent-written code, for
  "security check my changes", "is this diff safe", "check for secrets", or any change touching auth,
  user input, files, shell commands, SQL, HTML output, URLs or config.
---

# Secure diff

Agents add input paths fast and forget who can reach them. This is a short pass over your own change,
done by the author, before anyone else reviews it. It complements a full review; it doesn't replace one.

## When it applies

- Any diff that takes outside input, touches auth or permissions, runs commands, builds queries or
  HTML, reads or writes files by name, fetches URLs, or changes config and defaults.
- Before the first push of agent-written code.

## Procedure

### 1. Secrets

Scan the diff and any new files, including test fixtures, logs and notebooks:

```bash
git diff <base> | grep -nEi '(api[_-]?key|secret|token|passw|bearer|private key|-----BEGIN)'
```

Use a real scanner if installed (`gitleaks`, `trufflehog`). Any real value found: remove it, use an
env var or the project's secret store, and tell the user the value must be rotated if it was ever
committed or pushed.

### 2. List the new inputs

Every place the diff accepts data it didn't create: request params, headers, bodies, CLI args, env,
files, uploads, webhooks, messages, model output. One line each, with file:line.

### 3. Walk each input to where it is used

| Sink | Check |
| --- | --- |
| SQL / queries | parameters, never string concatenation |
| Shell / process spawn | argument arrays, no shell string built from input |
| HTML / templates | escaped by default; no raw-HTML escape hatch on input |
| File paths | resolved and confined to an allowed directory; no `..` escape |
| URLs fetched by the server | allowlist hosts; block internal addresses |
| Deserialization / eval | no `eval`, unsafe YAML or pickle on outside data |
| Redirects | only to known targets |
| Logs | no secrets or personal data written |

### 4. Authorization

For each new route, action or tool: who may call it, and where is that checked? Check that one user
can't read or change another user's object by changing an id. A check in the UI only is not a check.

### 5. Defaults and failure

New config defaults closed (off, deny, private), not open. Errors fail closed and don't leak stack
traces, paths or secrets to the caller. New dependencies are real, maintained packages.

### 6. Probe what you suspect

For each suspect, run something: a request with `../../etc/passwd`, `' OR 1=1 --`, `<script>`, another
user's id, an internal URL. Record the command and the result. A probe that gets through is a finding.

## Report

```
Secrets: none found | <removed: where; rotation needed: yes/no>
Inputs: <n>   Findings:
| # | file:line | Issue | Probe | Result | Fixed |
Not covered: <anything you couldn't check>
```

## Rules

- Never paste a found secret into the report; give its location only.
- A suspect is settled by a probe or a quoted guard, not by "looks fine".
- For high-stakes changes (auth, payments, sandboxing), also get an independent review.
