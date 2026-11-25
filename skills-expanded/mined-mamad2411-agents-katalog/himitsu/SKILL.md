---
name: himitsu
description: "Use when reading Himitsu secrets. Bind HOME=~"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [himitsu, secrets, credentials, hindsight]
    category: software-development
    related_skills: [remote-browser-mcp, endpoint-auth-audit]
---

# Himitsu from Hermes

Read secrets from Cooper's Himitsu store (`czxtm/secrets`) without leaking values and without creating a rogue identity under Hermes `$HOME`.

## When to Use

- User says creds are in Himitsu / `himitsu` / `czxtm/secrets`
- Any API/token lookup the user expects to be automated
- Hindsight Cloud, Slack bot tokens, LiteLLM keys, and other `himitsu search` hits

Don't use for: Vessel MCP bearer <REDACTED> `~/.config/vessel/mcp-auth.json` — see `remote-browser-mcp`). Don't dump secret values into chat, MEMORY.md, or skills.

## Invoke (always this env)

Hermes `$HOME` is `/var/lib/hermes`. A bare `himitsu` call **inits a new unused age keypair** there. Always bind Cooper's identity:

```bash
export PATH="~/.nix-profile/bin:$PATH"
export HOME=~
export HIMITSU_AUTO_PULL=false
```

Binary: `~/.nix-profile/bin/himitsu`
Config: `~/.config/himitsu/config.yaml` (`default_store: czxtm/secrets`)
Keys: `~/.local/share/himitsu/{key,key.pub}`

Completion: `himitsu search <name>` lists a path in `czxtm/secrets` without printing the value.

## Commands

| Goal | Command |
|---|---|
| Find a secret | `himitsu search <term>` |
| List store | `himitsu ls` / `himitsu ls --offset N` |
| Read for scripting | `himitsu read <path>` (plaintext stdout, no decoration) |
| Inject into a child | `himitsu exec -- <cmd>` |
| Metadata only | `himitsu get` still prints the value — prefer `search`/`ls` |

Never `echo` / `cat` a `himitsu read` result. Probe by length + prefix only:

```bash
TOKEN=<REDACTED>
printf '%s' "$TOKEN" | python3 -c 'import sys; d=sys.stdin.buffer.read(); print("ok", "len", len(d), "prefix", d[:4].decode())'
```

Or keep the token in-process (Python `subprocess.check_output`, curl via env) and print only HTTP status + redacted JSON.

## Pitfalls

1. **Missing `HOME=~ — himitsu prints `First run — initializing himitsu` and writes `/var/lib/hermes/.local/share/himitsu` + `~/.config/himitsu`. Delete that orphan identity; it is not a store recipient.
2. **`HIMITSU_AUTO_PULL` default** — set `false` unless the user asked to sync. Search/read work against the local checkout.
3. **Printing values** — user-facing replies: path + prefix/length + whether auth succeeded. Never the secret.
4. **`himitsu` not on default PATH** — expected. Use the export above; do not treat as "himitsu unavailable."
5. **Search is substring-broad** — `himitsu search omp` hits unrelated `*omp*` paths. Prefer exact path once known.

## Verification

- [ ] `HOME=~ and `HIMITSU_AUTO_PULL=false` were set before the first himitsu call
- [ ] No new keypair under `/var/lib/hermes/.local/share/himitsu` (delete if created)
- [ ] Secret used in-process; chat shows path + outcome only

## Hindsight Cloud

Token path: `hindsight-api-key`. API, banks, no-leak probe, and **read-only mining** (`memories/list`, mental-models, recall): `references/hindsight-cloud.md`.

"the omp memory bank" = bank_id `omp`. Do not retain. Do not switch Hermes off Honcho unless asked.
