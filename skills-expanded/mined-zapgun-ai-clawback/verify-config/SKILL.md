---
name: verify-config
description: Config doctor for clawback — loads the merged config (DEFAULTS < global < ./CLAWBACK.md < CLI overrides) exactly as the proxy's loadConfig does, prints a secret-free summary of the resolved values plus the merge-order sources, and exits non-zero if the canonical CLAWBACK.md did NOT take effect (host not 0.0.0.0, tls off, or adminToken missing) so a bad parse fails loudly instead of silently falling back to loopback defaults. Read-only; never prints the adminToken value, only its length. Use to confirm a CLAWBACK.md edit actually parsed and merged before starting the proxy, or to debug which config layer won.
---

# clawback config doctor

Run `.skills/verify-config/scripts/verify_config_parse.mjs` from the project
root. It loads the merged config the same way the proxy would and prints what
actually resolved — no secrets — then fails loudly if the canonical
`CLAWBACK.md` did not take effect.

```bash
node .skills/verify-config/scripts/verify_config_parse.mjs              # resolve from ./ (cwd)
node .skills/verify-config/scripts/verify_config_parse.mjs /path/to/project
```

The optional positional argument is the directory to resolve config from
(defaults to the current working directory).

## What it prints

- **sources (merge order)** — each contributing tier and file path, lowest
  precedence first, exactly the layering in CLAUDE.md's *Config Merging
  Strategy* (`DEFAULTS < global < local < CLI`).
- **resolved** — host, port, tls, cert/key paths, selfSign, passthrough,
  keepAliveEnabled, injectExtendedCacheTtl, adminPathPrefix, and whether an
  adminToken is present (length only — the value is never shown).
- **warnings** — any non-fatal notes `loadConfig` surfaced.

## Exit status

Exits **non-zero** with a `FAIL:` list when any of these are off — the
signature of a `CLAWBACK.md` that did not parse or merge:

- `host` is not `0.0.0.0` (the canonical LAN bind did not stick),
- `tls` is not `true`,
- `adminToken` is missing (a non-loopback bind would have thrown anyway).

Otherwise it prints `OK: canonical CLAWBACK.md parsed and merged`. Pairs with
the [write-config](../write-config/SKILL.md) skill, which generates that file.
