---
name: configuration-and-secrets
description: Manages configuration and secrets - .env and .env.example, environment variables, API keys for Anthropic, OpenAI and Gemini, startup validation, keeping secrets out of the repo and out of agents. Triggers - .env file, env var, where do I put this API key, dotenv, secret leaked, config validation.
---

# Configuration and Secrets

Configuration fails in two opposite ways. Either it is scattered — `getenv`
calls in forty files, each with its own default, so nobody can say what the
service needs to run — or it leaks: a real key in `.env.example`, a `.env`
committed once, a token printed in a startup log. AI coding agents add a third
failure: the agent reads `.env` to "understand the config" and the secret ends
up in a transcript, a prompt sent to a model provider, or a commit message.

## Three kinds of value

| Kind | Example | Lives in | Committed? |
|---|---|---|---|
| **Constant** | Retry count, page size cap | Code | Yes |
| **Configuration** | Port, log level, feature flag, upstream URL | Environment, with a safe default in code | Defaults yes; per-environment values no |
| **Secret** | API keys, DB passwords, signing keys | Environment, injected at runtime | **Never** |

A value that differs between deployments is configuration. A value whose
disclosure causes harm is a secret. A value that is neither belongs in code —
moving constants into env vars just creates knobs nobody tests.

## The `.env` contract

1. **`.env.example` is committed and complete.** Every variable the program
   reads appears there, with a comment saying what it is, whether it is
   required, and its format. Values are empty or obvious placeholders —
   never a real key, not even an expired one.
2. **`.env` is never committed.** `.gitignore` covers `.env` and `.env.*`,
   with an explicit `!.env.example` exception.
3. **`.env` is a local-development convenience, not a deployment mechanism.**
   Production gets values from the platform: secret manager, orchestrator
   secrets, CI secret store. A `.env` file on a server is a secret on disk with
   no rotation, no audit and no access control.
4. **Precedence is fixed and documented:** real process environment overrides
   `.env`, which overrides code defaults. Never the reverse — an override you
   cannot override from the outside breaks every deployment tool.
5. **Drift is checked mechanically.** A key used in code but missing from
   `.env.example` is a broken onboarding; a key in `.env.example` nothing reads
   is dead weight. Run `scripts/check_env.py` in CI.

## Load once, validate at startup

Read the environment in exactly **one** module at startup, into a typed,
immutable settings object. Everything else receives that object.

- Missing required value → **exit at startup** with a message naming every
  missing key at once. Failing on the first request, an hour later, under load,
  is the expensive version of the same error.
- Parse and validate types and ranges at load: a port is an integer in range,
  a URL parses, an enum value is known.
- **Never print values.** The error says `OPENAI_API_KEY is missing`, not what
  it was set to. Redact secrets in the settings object's string representation.
- No `getenv` outside the settings module. A grep for direct environment access
  outside it should return nothing; enforce it in review or with a lint rule.

| Stack | Typical loader |
|---|---|
| Python | `pydantic-settings`, or `python-dotenv` + a dataclass |
| Node.js ≥ 20.6 | `node --env-file=.env` (built in), plus a schema validator |
| Java / Spring | `application.yml` + `${ENV_VAR}` placeholders; `@ConfigurationProperties` with validation |
| Go | `os.LookupEnv` in one package, struct with explicit parsing |
| Stdlib-only | A 20-line parser for `KEY=VALUE` lines; still one module, still validated |

Discover what the project already uses before adding a library
(`dependency-and-license-policy`).

## Model provider keys

Use each provider's conventional variable name, so SDKs and CLIs pick them up
without glue code:

| Provider | Variable | Notes |
|---|---|---|
| Anthropic | `ANTHROPIC_API_KEY` | |
| OpenAI | `OPENAI_API_KEY` | |
| Google Gemini | `GEMINI_API_KEY` | Some Google tooling also reads `GOOGLE_API_KEY`; set only one to avoid ambiguity about which key is in use |

- One key per environment and per service — never share a personal key with
  a deployed service. A shared key cannot be rotated without breaking someone.
- Set spending limits at the provider. A leaked model key is billed by the token.
- For the agent CLIs themselves (Claude Code, Gemini CLI, Codex), prefer each
  tool's own login flow over an API key in a file: no key on disk is the
  strongest guarantee.

## Keeping secrets away from agents

An agent that can read a file can send its contents to a model provider. Treat
`.env` as off-limits to agents by configuration, not by hoping they don't look.

| Agent | Mechanism |
|---|---|
| Claude Code | `permissions.deny` with `Read(./.env)` and `Read(./.env.*)` in `.claude/settings.json` |
| Gemini CLI | Files matching ignore patterns (`.geminiignore`, and `.gitignore` when respected) are refused by the file-reading tools |
| Codex | Filesystem read-deny rules (`permissions.filesystem.deny_read`) through its requirements configuration |

Ready-made snippets: `templates/agent-secret-guards.md`. Two caveats that the
mechanisms do not remove:

- File-read rules govern file tools. A shell command (`cat .env`, `env`,
  `printenv`) is a different permission; keep shell access gated and sandboxed.
- Secrets already exported into the agent's own process environment are
  visible to anything it runs. Start agent sessions from a shell that has not
  loaded production credentials.

## Rotation and response

- Every secret has an owner and a rotation path that has been exercised once.
- On exposure — committed, logged, pasted into a chat, read by an agent —
  **rotate first**, then clean up. Removing a commit does not un-leak a key.
- Pre-commit and CI run a secret scanner; `check_env.py` additionally flags
  real-looking values in `.env.example` and tracked `.env` files.

## When not to use this

Build-time constants, test fixtures with obviously fake values, and
configuration that genuinely never varies. Do not turn every literal into an
environment variable.

## Exit checklist

- [ ] Every variable the code reads is in `.env.example`, with a comment
- [ ] `.env.example` contains no real or real-looking values
- [ ] `.env` and `.env.*` are gitignored and untracked; `!.env.example` excepted
- [ ] Configuration is loaded in one module, validated, and fails fast
      listing all missing keys
- [ ] No secret value appears in logs, errors, string representations or test output
- [ ] Provider keys use the conventional variable names; spending limits set
- [ ] Agents are denied read access to `.env` files in every agent the team uses
- [ ] `scripts/check_env.py` passes in CI
- [ ] Production secrets come from the platform, not from a file on disk
