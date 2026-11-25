---
name: cli-audit-wizard
metadata:
  author: clement
description: >
  Audit configuration wizard UX and lifecycle quality (setup, doctor, edit, migrate).
  Scores the 4 Laws (ask once, defaults, recap, config-as-code), credential discovery,
  multi-surface consistency (CLI/MCP/web), and scriptability. Detects wizard anti-patterns.
  Use on 'wizard', 'setup flow', 'config UX', 'init command', 'doctor mode',
  'wizard audit', 'onboarding UX', 'first-run experience', 'config lifecycle',
  'wizard broken', 'interactive setup', 'MCP config', 'config reload'.
argument-hint: "[wizard-file-or-project-directory]"
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
  - Agent
---

> **Optimization:** This skill uses on-demand loading. Heavy content lives in `references/` and is loaded only when needed.

> **Language rule:** Skill instructions are written in English. When generating user-facing output, detect the project's primary language (from README, comments, docs, commit messages) and produce the report in that language. If the project is bilingual, ask the user which language to use before proceeding.

# Audit Wizard -- Wizard Quality Index (WQI)

Audit configuration wizards for UX quality, lifecycle completeness, and multi-surface exposure (CLI, MCP, web).

> "The worst time for users to make choices is before they've started using the system."
> -- OpenBSD design philosophy

## Natural laws mapped to wizard rules

Each analogy maps to a concrete, testable audit check. Only actionable rules are listed here.

| Source | Wizard rule (testable) |
|--------|----------------------|
| **Seed germination** | Ask 3-5 seed values max. If more, you're encoding the tree in the seed |
| **Axolotl** (facultative metamorphosis) | Never show advanced options by default. `--advanced` is opt-in |
| **Immune system** | Doctor checks are pattern-based (schema, connectivity), not intent-based |
| **Homeostatic set point** | `wizard apply` is idempotent: run 1x or 100x, same result (the idempotence/determinism toolkit is shared in `../shared/determinism.md`) |
| **Tardigrade** (cryptobiosis) | Every config section has a safe degraded state when dependencies are down |
| **Principle of least action** | Every question must reduce configuration entropy. Derivable = don't ask |
| **2nd law of thermodynamics** | Config drifts without doctor. Doctor is the energy that fights entropy |
| **Hick's Law** | Max 5 options per prompt. More? Filter or nest |
| **Miller's Law** | Max 7 fields per wizard screen. Group into chunks |
| **Recognition > recall** | Pre-fill values on re-run. Enter-through should produce working config |
| **Portal's 4-step** | Each wizard step teaches one concept. Never combine two new things |
| **Save/checkpoint** | Auto-backup config before every destructive `apply` |

> The full 27 analogies across 5 domains (biology, physics, information theory, game design, cognitive science) are in `references/analogies.md`. Each includes the biological/physical mechanism, mapping table, and a named **Rule**.

## The 4 Laws of Good Wizards

These are non-negotiable. A wizard that violates any of these is broken. The Laws are factored into `../shared/cli-ergonomics.md` so `cli-audit-shell` (S9), `cli-forge-chef` (prompt design), and `cli-forge-infra` (operator wrappers) can reuse the same semantics across CLI, TUI, agent prompt, and CI surfaces.

A wizard lives at **rung 1** of `../shared/escalation-ladder.md` — a setup CLI that asks once, recaps, and writes config-as-code. A "wizard" that drives a vendor GUI through screenshots and clicks is rung 5 and fails all 4 Laws by construction (no scripting, no recap, no replayability). If the only path is GUI driving, that's not a wizard — that's a last-resort bridge, and the lower rungs of the ladder must be exhausted first.

### Law 1 -- Ask once, derive the rest (Germination)

If you can calculate a value from another, do not ask the question.
`step ca init` asks the domain name, derives the ACME URL automatically.
A good wizard asks 3-5 **seed questions** and grows the full config.

### Law 2 -- Defaults are decisions (OpenBSD philosophy)

Every default is an opinionated choice, documented and justified.
No empty strings, no `null`, no "please configure". Caddy defaults `http_port: 80` -- you don't think about it.

### Law 3 -- Recap before apply (Dry-run)

Show what will change before touching the system. OpenBSD recaps before install. Talos has `--dry-run`.
The user must be able to review and abort.

### Law 4 -- Config-as-code output (Committable)

The wizard generates a **file on disk**, not hidden state. The file is committable, diffable, readable.
Re-running the wizard reads the existing config and proposes a diff. Never a black box.

## The Lifecycle State Machine

A wizard is not a one-shot setup. It's a **config lifecycle manager**.

```
wizard --run
  |
  +-- config ABSENT -> SETUP mode
  |     +-- seed questions (3-5 max)
  |     +-- credential discovery cascade (see below)
  |     +-- recap -> confirm -> write config.toml
  |     +-- doctor run (immediate post-setup validation)
  |
  +-- config PRESENT -> DOCTOR + EDIT mode
  |     +-- lint config (missing values, deprecated keys, schema drift)
  |     +-- test connectivity (ping backends, check creds validity)
  |     +-- compare against current schema (migration needed?)
  |     +-- show current config summary
  |     +-- PROPOSE EDIT: "Modify config? [backends / credentials / rules / all / skip]"
  |     |     +-- user picks section -> wizard opens ONLY that section pre-filled
  |     |     +-- user changes values -> recap diff -> confirm -> apply
  |     |     +-- skip -> exit (config unchanged)
  |     +-- re-run credential discovery if any creds are expired/invalid
  |
  +-- explicit flags
        +-- --setup     force setup from scratch (ignores existing config)
        +-- --doctor    force doctor only (no edit prompt)
        +-- --edit [section]  jump directly to editing a section
        +-- --dry-run   show what would change, don't apply
```

**Key behavior: re-run always reads existing config.** The wizard is never amnesic. On re-run it loads current values, shows them, and lets the user modify. It never starts from zero unless `--setup` is explicit.

Reference implementations: `rustup check`, `brew doctor`, `helm lint`, `talosctl health`.

## Credential Discovery Cascade

Credentials (API keys, OAuth tokens) are the hardest part of any setup. The wizard should never just ask "paste your API key" as first option. Instead, it runs a **discovery cascade** -- try the easiest path first, fall back progressively.

This is the universal three-tier hierarchy used by `gh`, `gcloud`, `aws`, `railway`, `vercel`, `wrangler`, and every well-designed CLI. Deviation is an anti-pattern.

> Credential hygiene (file permissions, .env in .gitignore, raw secrets in config) is checked by `cli-audit-code` dimension C9 (Security & Input Validation).

```
credential_discovery(service):
  |
  +-- 0. ENV VAR CHECK (before any prompts -- blocks wizard if found)
  |     +-- $ANTHROPIC_API_KEY, $OPENAI_API_KEY, $MISTRAL_API_KEY, etc.
  |     +-- Found + valid? -> use it, skip interactive auth entirely
  |     +-- Found + invalid? -> warn "ANTHROPIC_API_KEY set but invalid", continue
  |     (gh pattern: "The value of GH_TOKEN is being used for authentication.")
  |
  +-- 1. SCAN -- look for existing tokens on disk
  |     +-- ~/.config/claude/credentials.json     (Claude Code)
  |     +-- ~/.config/github-copilot/hosts.json   (Copilot)
  |     +-- keychain / secret-tool / pass          (OS keyring)
  |     +-- ~/.netrc                                (legacy but common)
  |     +-- 1Password CLI / Bitwarden CLI          (if installed)
  |
  |     Found? -> "Found Claude token at ~/.config/claude/. Use it? [Y/n]"
  |               Validate token (API ping) before accepting.
  |
  +-- 2. OAUTH / DEVICE FLOW (RFC 8628 -- modern standard)
  |     +-- Show device code: "First copy your one-time code: 7CDF-8959"
  |     +-- Open browser automatically to authorization page
  |     +-- Poll until user authorizes -> receive token
  |     +-- HEADLESS FALLBACK 1: show URL + code for manual entry
  |     |     "Visit: https://provider.com/device -- Enter code: 7CDF-8959"
  |     +-- HEADLESS FALLBACK 2 (gcloud pattern): output bootstrap command
  |     |     "Run on a machine with a browser: tool auth --remote-bootstrap=..."
  |     +-- Token stored in OS keychain; plaintext fallback with warning
  |
  |     Worked? -> "Authenticated via OAuth. Token stored."
  |
  +-- 3. API KEY -- manual paste (last resort)
  |     +-- Show link to token page: "Generate a key at https://console.anthropic.com/keys"
  |     +-- "Paste your API key: ********"
  |     +-- Validate immediately (API ping)
  |     +-- Invalid? -> show expected format + "Try again or Ctrl-C to skip"
  |     +-- Valid? -> store in config (env var reference, not raw key)
  |
  +-- 4. SKIP -- defer credential setup
        +-- "No credentials configured. Some features will be unavailable."
            Config is written with placeholder. Doctor mode will flag it.
```

> Read `references/reference-flows.md` for concrete auth flows from gh, gcloud, aws, railway, vercel, wrangler, supabase.

### Rules for credential handling

1. **Env var check comes first and blocks the wizard.** If `$TOOL_TOKEN` is set, the interactive auth flow never runs. This is universal across `gh`, `gcloud`, `aws`, `railway`, `vercel`. The wizard should print what env var it found and exit.
2. **Never store raw secrets in the config file.** Store a reference: `api_key_env = "ANTHROPIC_API_KEY"` or `api_key_cmd = "pass show anthropic"` or `api_key_keyring = "anthropic-api"`.
3. **Always validate before accepting.** A token found on disk may be expired or revoked. Ping the API.
4. **On re-run, re-validate existing credentials.** Doctor mode checks that stored creds are still valid. If expired, re-trigger the discovery cascade for that specific service only.
5. **Multiple providers = multiple cascades.** If the tool supports Claude + OpenAI + Mistral, run the cascade independently for each. The user might have Claude via OAuth but needs to paste a Mistral key.
6. **OAuth must have a headless fallback.** Three tiers (from gcloud): browser auto-open -> manual URL + code -> remote bootstrap command. Headless servers, SSH sessions, and containers can't open a browser.
7. **Auto-skip when only one choice.** If there is one provider, one account, one role -- select it automatically, don't ask. (AWS SSO pattern.)

### Re-run credential flow

```
wizard --run (config exists, credentials present)
  |
  +-- doctor checks creds validity
  |     +-- Claude token: [PASS] valid, expires in 45 days
  |     +-- Mistral key:  [FAIL] 401 Unauthorized
  |     +-- OpenAI key:   [WARN] not configured (optional)
  |
  +-- "Mistral key is invalid. Reconfigure? [Y/n]"
  |     +-- Y -> run credential_discovery(mistral) cascade
  |
  +-- "Add OpenAI backend? [y/N]"
  |     +-- y -> run credential_discovery(openai) cascade
  |
  +-- "Modify other config? [backends / rules / all / skip]"
```

### MCP credential tools

```
wizard_check_credentials()       -> { providers: [{name, status, expires_at, source}] }
wizard_discover_credential(svc)  -> runs cascade, returns { found: bool, source, valid }
wizard_set_credential(svc, ref)  -> stores credential reference, validates, returns { ok, valid }
```

## Multi-Surface Architecture

One wizard engine, three surfaces. The engine writes the same config file regardless of entry point.

```
CLI (Huh/Gum/cliclack)  -+
MCP tool calls           -+---> wizard engine ---> config.toml ---> app reload
Web UI (Caddy-served)    -+
```

### Surface: CLI

| Language | Recommended library | Notes |
|----------|-------------------|-------|
| Go | **Huh v2** (Charm) | Best-in-class. Groups-as-pages, dynamic fields, accessible mode |
| Go (shell) | **Gum** | Composable bash prompts, ideal for just/Makefile wizards |
| Rust | **cliclack** | Modern, Clack-inspired, themed. Prefer over dialoguer (testability issues) |
| Python | **questionary** | Best wizard-style prompts. Pair with Rich for output |
| Node/TS | **@clack/prompts** | The original that cliclack cloned. Gold standard |

### Surface: MCP

Each wizard step = one MCP tool. The agent calls tools sequentially, same engine.

```
wizard_get_config()          -> read current TOML, return struct
wizard_set_{section}(...)    -> modify one value, write TOML, return diff
wizard_run_doctor()          -> return pass/warn/fail per check
wizard_diff()                -> show pending changes before apply
wizard_apply()               -> reload app with new config
```

The MCP surface writes TOML, not JSON. JSON is only transport (tool call payloads, API responses).
The user never sees JSON on disk.

> Read `references/mcp-patterns.md` for MCP tool design patterns and MCP Apps UI spec.

### Surface: Web UI

Pattern: Caddy Admin API model -- live config via REST, no restart.

| Method | Endpoint | Function |
|--------|----------|----------|
| GET | `/config/[path]` | Read config at path |
| PUT | `/config/[path]` | Update value at path |
| POST | `/config/` | Replace entire config |
| DELETE | `/config/[path]` | Remove value |

- Optimistic concurrency via `Etag` / `If-Match` headers
- Validation before commit -- reject bad config, keep old running
- Atomic rollback on failure
- CLI wraps API: `tool reload` is sugar over `curl -X POST /load`

## Server vs Client Mode

### Server mode (remote + reverse proxy)

```
[wizard] -> generates:
  - app.toml           (backends, routing, rules)
  - Caddyfile          (TLS termination, reverse proxy -> app)
  - compose.yaml       (or k8s manifest)
  -> apply via SSH or Caddy Admin API
```

### Client mode (local)

```
[wizard] -> generates:
  - ~/.app/config.toml  (server endpoint, API key, local port)
  -> app client points to remote server
```

Both modes use the same wizard engine. The mode is determined by one seed question or auto-detected.

## Mitosis — Scale to scope

| Scope | Tier | Behavior |
|-------|------|----------|
| Single wizard file | **S** | Audit that one wizard flow, skip multi-surface analysis |
| Directory or small project (1-3 wizards) | **M** | Full audit, all dimensions |
| Large project (4+ wizard surfaces) | **L** | Audit each surface individually, then cross-surface consistency |

For tier **S**: skip the Multi-Surface Architecture section entirely.

## Input

`$ARGUMENTS` is the target to audit:

- **File** (`cmd/wizard.go`, `setup.py`): audit that wizard implementation
- **Directory** (`cmd/`, `src/`): find and audit all wizard/setup flows
- **Empty**: scan the entire project for wizard patterns

## Workflow

### Step 0 -- Discover wizard surfaces

1. Find wizard/setup entry points:
   ```
   grep -r "wizard\|setup\|init\|configure\|doctor" --include="*.go" --include="*.rs" --include="*.py" --include="*.ts" -l
   ```
2. Find config file schemas/templates:
   ```
   glob: **/*.toml.example, **/*.yaml.example, **/config.*.toml, **/schema.json
   ```
3. Find MCP tool definitions:
   ```
   grep -r "wizard_\|config_\|setup_" --include="*.go" --include="*.rs" --include="*.py" --include="*.ts" -l
   ```
4. Find web config endpoints:
   ```
   grep -r "/config\|/api/config\|admin.*api" --include="*.go" --include="*.rs" --include="*.py" --include="*.ts" -l
   ```

### Step 1 -- Audit the 4 Laws

For each wizard surface found, check compliance with each law:

**Law 1 -- Ask once, derive the rest**
- Count total questions asked
- For each question: can the answer be derived from a previous answer or environment detection?
- Flag derivable questions as violations
- Check: does the wizard detect existing environment (OS, installed tools, running services)?

**Law 2 -- Defaults are decisions**
- List all config keys generated
- For each: is there a default value? Is the default documented/justified?
- Flag keys with empty string, null, or placeholder defaults
- Check: can a user accept all defaults and get a working system?

**Law 3 -- Recap before apply**
- Does the wizard show a summary/diff before writing config?
- Is there a `--dry-run` flag?
- Can the user abort after recap?
- Is the diff human-readable (not raw JSON dump)?

**Law 4 -- Config-as-code output**
- Does the wizard generate a file on disk?
- Is the file in a committable format (TOML, YAML, not binary)?
- Can the wizard re-read an existing config and diff against it?
- Is the config file documented (comments, inline help)?

### Step 2 -- Audit lifecycle completeness

| Mode | Check | How to verify |
|------|-------|---------------|
| **Setup** | Config-absent path works | Remove config, run wizard -> verify seed questions + config file generated |
| **Re-run edit** | Config-present opens edit flow | Run wizard with existing config -> verify it loads values, proposes edit, shows diff |
| **Doctor** | Health checks run automatically | Run wizard with existing config -> verify pass/warn/fail checks before edit prompt |
| **Edit section** | Section-level editing works | `--edit backends` opens only that section, pre-filled with current values |
| **Migrate** | Schema version handling | Change schema version, verify wizard detects and proposes migration |
| **Dry-run** | No side effects | `--dry-run` writes nothing to disk, returns proposed changes |
| **Idempotent** | Re-run safety | Run wizard twice with same inputs, verify identical output |

### Step 2b -- Audit credential discovery

Verify the wizard implements a credential discovery cascade (not just "paste your API key"):

| Check | How to verify |
|-------|---------------|
| **Scan existing tokens** | Unset env vars, place a token file at known path -> wizard finds it |
| **Validate before accepting** | Place an expired/revoked token -> wizard rejects it, continues cascade |
| **OAuth fallback** | Block token scan -> wizard offers OAuth browser flow |
| **Device flow fallback** | Run in headless env (no DISPLAY) -> wizard offers manual URL + device code |
| **Manual key fallback** | Block OAuth -> wizard offers API key paste + immediate validation |
| **Skip/defer option** | User can skip credential setup -> config written without it, doctor flags it |
| **Re-run re-validates** | Run wizard with existing valid creds -> doctor checks them. Expire one -> wizard offers to re-discover that specific provider |
| **No raw secrets on disk** | After setup, grep config file for raw keys -> must use `_env`, `_cmd`, or `_keyring` references |
| **Multiple providers independent** | Configure 2 providers, expire 1 -> wizard only prompts for the expired one |

### Step 3 -- Audit doctor checks

Read `references/doctor-checks.md` for the standard check categories (including credentials).

For each check found in the doctor mode, verify:
- Clear pass/warn/fail status
- Actionable fix recommendation for each warn/fail
- Independent execution (one failing check doesn't block others)
- Exit code reflects overall status (0 = all pass, 1 = warnings, 2 = failures)
- Credential checks re-trigger discovery cascade on failure (not just "key invalid, fix it yourself")

### Step 4 -- Audit multi-surface consistency

If the wizard has multiple surfaces (CLI + MCP, CLI + web):

- Do all surfaces write the same config file format?
- Do all surfaces use the same validation logic?
- Can a config written by one surface be read/edited by another?
- Is there a single source of truth (one config file, not scattered state)?

### Step 5 -- Detect anti-patterns

Read `references/anti-patterns.md` for the named anti-patterns with detection heuristics.

### Step 6 -- Audit scriptability

- Does every interactive prompt have a corresponding CLI flag?
- Can the wizard run fully non-interactive via flags/env vars?
- Is there a `--yes` / `--accept-defaults` flag for CI usage?
- Can config be piped in via stdin?

### Step 7 -- Score and report

Finding tier and confidence semantics are canonical in `../shared/triage.md` (Tier 3/2/1 + GRADE + triangulation). Law violations are Tier 3 by default; lifecycle gaps are Tier 2.

## Output Format

```markdown
# Wizard Audit -- {project-name}

**Date:** {date}
**Scope:** {what was analyzed}
**Wizard surfaces found:** {CLI / MCP / Web / count}
**Config format:** {TOML / YAML / JSON / other}
**Wizard Quality Index:** {X}/100

## Law Compliance

| Law | Status | Evidence |
|-----|--------|----------|
| 1. Ask once, derive the rest | {Pass/Warn/Fail} | {N} derivable questions found |
| 2. Defaults are decisions | {Pass/Warn/Fail} | {N} keys without meaningful defaults |
| 3. Recap before apply | {Pass/Warn/Fail} | Dry-run: {yes/no}, Recap: {yes/no} |
| 4. Config-as-code output | {Pass/Warn/Fail} | Format: {format}, Committable: {yes/no} |

## Lifecycle Coverage

| Mode | Status | Notes |
|------|--------|-------|
| Setup (config absent) | {Implemented / Missing} | |
| Doctor (config present) | {Implemented / Missing} | |
| Edit (section) | {Implemented / Missing} | |
| Migrate (schema version) | {Implemented / Missing} | |
| Dry-run | {Implemented / Missing} | |
| Idempotent re-run | {Pass / Fail} | |

## Doctor Checks ({N} found)

| Check | Category | Status | Fix suggestion |
|-------|----------|--------|---------------|
| Config schema valid | Schema | {pass/warn/fail} | |
| Backend reachable | Connectivity | {pass/warn/fail} | |
| TLS cert valid | Security | {pass/warn/fail} | |

## Multi-Surface Consistency

| Surface | Config format | Validation shared | Interoperable |
|---------|--------------|-------------------|---------------|
| CLI | {format} | {yes/no} | {yes/no} |
| MCP | {format} | {yes/no} | {yes/no} |
| Web | {format} | {yes/no} | {yes/no} |

## Anti-Patterns Detected

| # | Pattern | Severity | Evidence | Fix |
|---|---------|----------|----------|-----|
| 1 | Premature Interrogation | Major | Setup asks 12 questions, 8 derivable | Derive from first 4 |

## Scriptability

| Check | Status |
|-------|--------|
| All prompts have flags | {yes/no, N missing} |
| Non-interactive mode | {yes/no} |
| --yes / --accept-defaults | {yes/no} |
| Stdin config input | {yes/no} |
| CI-friendly exit codes | {yes/no} |

## Recommendations

| # | Action | Impact | Effort | Target |
|---|--------|--------|--------|--------|
| 1 | Add --dry-run flag | High | Low | cmd/wizard.go |
| 2 | Implement doctor mode | High | Medium | cmd/doctor.go |
```

## Scoring

```
wqi = 100
  - (law_1_violations x 5)         # derivable questions
  - (law_2_violations x 5)         # empty/null defaults
  - (law_3_missing x 15)           # no recap/dry-run
  - (law_4_missing x 15)           # no config-as-code
  - (missing_lifecycle_modes x 8)  # setup/doctor/edit/migrate/dry-run
  - (anti_pattern_count x 7)       # named anti-patterns
  - (non_scriptable_prompts x 3)   # prompts without flags
  - (surface_inconsistency x 10)   # multi-surface divergence
  clamped to [0, 100]
```

| Score | Verdict |
|-------|---------|
| 80-100 | Excellent -- wizard follows all 4 laws, lifecycle complete |
| 60-79 | Good -- minor gaps, usable but could be smoother |
| 40-59 | Rough -- missing lifecycle modes or law violations |
| 20-39 | Broken -- users will struggle, significant rework needed |
| 0-19 | Anti-pattern factory -- start over with the 4 laws |

## Rules for the Auditor

1. **UX over implementation.** This skill audits the user experience of configuration, not the config file format itself. That's cli-audit-code's job.
2. **Test the absent path.** Always check what happens when config doesn't exist yet. First-run UX is the most critical moment.
3. **Test the re-run path.** A wizard that works once but breaks on re-run is worse than no wizard.
4. **Scriptability is not optional.** If a wizard can't run in CI, it's incomplete.
5. **Doctor mode is not a nice-to-have.** It's half the wizard. Setup without doctor is a one-shot anti-pattern.
6. **Gotchas** -- read `../gotchas.md` before producing output to avoid known mistakes.

## Integration with other cli-* skills

| Skill | Relationship |
|-------|-------------|
| `cli-audit-code` | C9 (Security) checks credential **hygiene** (permissions, .gitignore). wizard audits the **UX flow** for setting them up |
| `cli-audit-code` | Scores code **quality** inside the wizard. wizard scores **UX flow** |
| `cli-audit-shell` | If wizard is bash/gum-based, shell audit covers script quality |
| `cli-audit-tangle` | Checks wizard config **dependency topology** (circular config refs) |
| `cli-forge-infra` | Generates infra configs. wizard audits **how** those configs are generated |
| `cli-forge-pipeline` | CI/CD pipelines. wizard audit checks **non-interactive CI mode** |
| `cli-cycle` | Should call cli-audit-wizard as part of the full project review; emit `.claude/cli-audit-wizard.json` per `../shared/result-schema.md` for orchestrator aggregation |

## Dynamic Handoffs

| Condition detected | Recommend | Why |
|-------------------|-----------|-----|
| Wizard is a bash script with UX issues | `/cli-audit-shell` | Shell quality audit |
| Wizard generates YAML/config files | `/cli-forge-infra` | Validate generated configs |
| Wizard has no --help or getopts | `/cli-audit-shell` (S9 CLI Ergonomics) | Shell quality audit |
| Setup is idempotent but downstream perf benches drift (medians move between runs on same input) | `/cli-forge-perf` | The reproducibility toolkit (`../shared/determinism.md`) governs both — wizard fixes the setup, perf measures the consequence |

**Rule:** Recommend, don't auto-execute.

## What this skill does NOT do

- **Does not design wizards** -- it audits existing ones and recommends improvements
- **Does not generate config files** -- it checks that the wizard generates them correctly
- **Does not replace user testing** -- it catches structural issues, not subjective UX feel
- **Does not audit config file syntax** -- TOML/YAML validity is a linter's job
