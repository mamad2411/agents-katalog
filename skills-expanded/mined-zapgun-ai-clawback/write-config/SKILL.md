---
name: write-config
description: Generate or refresh the canonical CLAWBACK.md config. The front matter is built from the live DEFAULTS export in src/config.js (so it can never drift as options are added), with the only forced deviations being the two a LAN-reachable bind needs — host=0.0.0.0 and tls=true. adminToken is left as a null placeholder for you to set (it no longer mints one); a real existing token, or an explicit CLAWBACK_CANONICAL_TOKEN, is PRESERVED, and a token's value is NEVER printed (only presence and length). With no args it writes BOTH ./CLAWBACK.md and the global ~/.config/clawback/CLAWBACK.md. Use to (re)create a canonical config, or after adding an option or changing a default.
---

# clawback canonical config writer

Run `.skills/write-config/scripts/write_canonical_config.mjs` from the project
root. It writes a canonical `CLAWBACK.md`: every option at its DEFAULT value
(generated from the live `DEFAULTS` in `src/config.js`, so it never drifts as
options change), except the two a LAN bind needs set — `host=0.0.0.0` and
`tls=true` (it leaves `adminToken` as a null placeholder for you to set) —
followed by the documentation body in
`canonical_config_body.md` (in this skill's `assets/` directory).

```bash
# write BOTH ./CLAWBACK.md and the global ~/.config/clawback/CLAWBACK.md:
node .skills/write-config/scripts/write_canonical_config.mjs

# write specific target(s):
node .skills/write-config/scripts/write_canonical_config.mjs ./CLAWBACK.md

# inject a real token instead of the null placeholder:
CLAWBACK_CANONICAL_TOKEN=… node .skills/write-config/scripts/write_canonical_config.mjs
```

## adminToken handling (secret-safe)

The `adminToken` fronts live Anthropic credentials, so the script never mints
one and never prints a token's value. It resolves ONE shared value in this
order and writes it to every target so they agree:

1. `CLAWBACK_CANONICAL_TOKEN` from the environment, if set;
2. a real existing token preserved from the first target that already has one
   (a `null` / empty / placeholder token does NOT count — it is overwritten);
3. otherwise `null` — a placeholder you must fill in.

With `host: 0.0.0.0`, the proxy refuses to bind until `adminToken` is set, so a
forgotten placeholder fails loud instead of exposing a guessable secret. Output
reports only presence, length, and origin — never a token's value.

## Files written

- With no args: `./CLAWBACK.md` **and**
  `${XDG_CONFIG_HOME:-$HOME/.config}/clawback/CLAWBACK.md`.
- Each is written `0600` (owner-only; it holds a secret), enforced even when
  the file already existed.

Confirm the result parsed and merged with the
[verify-config](../verify-config/SKILL.md) skill.
