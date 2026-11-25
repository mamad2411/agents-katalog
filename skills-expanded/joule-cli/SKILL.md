---
name: joule-cli
description: >
  Comprehensive SAP Joule CLI (formerly sapdas CLI) assistant for managing digital assistants
  from the command line — compiling capabilities, deploying assistants, running BDD tests,
  linting, and troubleshooting errors. Use this skill whenever the user mentions "joule cli",
  "sapdas", "joule compile", "joule deploy", "joule test", "joule login", "joule lint",
  digital assistant deployment, capability compilation, DAAR files, RTA artifacts, or any
  task involving the Joule command line interface — even if they just say something like
  "deploy my assistant" or "how do I log in to Joule from the terminal". Also trigger when
  the user asks about testing Joule capabilities with Cucumber, linking AI assistants,
  managing deployed assistants, or automating Joule workflows in CI/CD pipelines.
---

# SAP Joule CLI Skill

You are an expert in the SAP Joule CLI (`@sap/joule-cli`), the command-line tool for building, deploying, testing, and managing SAP Joule digital assistants. Help users construct correct commands, automate multi-step workflows, and troubleshoot issues.

The CLI binary is available as both `joule` and `sapdas` (legacy alias). All examples here use `joule`.

## Installation

```bash
npm install -g @sap/joule-cli        # install
npm install -g -f @sap/joule-cli     # force update
npm uninstall -g @sap/joule-cli      # uninstall
```

Requires Node.js v20.12.0 – v24. On Linux, `libsecret` (or compatible keyring) is needed for secure credential storage.

## Global Options

These options apply to every command:

| Option | Description |
|--------|-------------|
| `-V, --version` | Print CLI version |
| `-d, --debug` | Show and store extra debug logs |
| `-w, --no-color` | Disable colorized output |
| `-h, --help` | Print usage info (`joule help` or `joule <command> --help`) |

## Command Reference

### Authentication

#### joule login

Authenticates with Joule on a global account level. Multiple authentication methods are supported.

**Interactive login (recommended for first use):**
```bash
joule login
```
The CLI prompts for auth URL interactively and opens a browser for authentication.

**SSO login:**
```bash
joule login --sso
```
Opens browser for Single Sign-On via Identity Authentication Service (IAS) with PKCE.

**Login with explicit URLs:**
```bash
joule login --authurl https://mytenant.authentication.eu10.hana.ondemand.com
```
The API URL is auto-determined from the auth URL for production landscapes. To override:
```bash
joule login --authurl <AUTH_URL> --apiurl <API_URL>
```

**Service key login (CI/CD):**
```bash
joule login --authurl <AUTH_URL> --clientid <ID> --clientsecret <SECRET> --username <USER> --password <PASS>
```

**Login via environment variables:**
```bash
joule login --use-env              # reads from .env in current directory
joule login --use-env path/to/.env # reads from specific file
```

**SSO passcode login:**
```bash
joule login --sso-passcode <PASSCODE>
```

| Option | Description |
|--------|-------------|
| `-a, --authurl <url>` | Authentication URL (e.g., `https://mytenant.authentication.eu10.hana.ondemand.com`) |
| `--apiurl <url>` | API URL (e.g., `https://mytenant.eu10.sapdas.cloud.sap`) |
| `-c, --clientid <id>` | Service instance client ID |
| `-s, --clientsecret <secret>` | Service instance client secret |
| `-u, --username <user>` | Username |
| `-p, --password <pass>` | Password |
| `-i, --default-idp` | Use the default identity provider |
| `-e, --unsecure-storage` | Store secrets in local public store (not recommended) |
| `--sso-passcode [passcode]` | One-time passcode for login |
| `--sso` | Use Single Sign-On via IAS |
| `--use-env [path]` | Read credentials from environment variables / .env file |
| `--store-password` | Enable password storage |
| `--no-app-tid` | Skip app_tid during IAS login |

**Environment variables** (for `--use-env` or CI/CD): `JOULE_API_URL`, `JOULE_AUTH_URL`, `JOULE_USERNAME`, `JOULE_PASSWORD`, `JOULE_CLIENT_ID`, `JOULE_CLIENT_SECRET`, `JOULE_DEFAULT_IDP`, `JOULE_AUTH_SESSION`, `JOULE_TEST_TIMEOUT`.

**Auth URL patterns:**
- XSUAA: `https://<tenant>.authentication.<landscape>.hana.ondemand.com`
- IAS: `https://<subdomain>.accounts[optional-suffix].<domain>`

**Session info:** Sessions expire; use `joule status` to check. Credentials are stored securely via OS keychain (`keytar`) by default, or in a local config file if `--unsecure-storage` is used.

**Config location:**
- macOS: `~/Library/Preferences/joule-cli/config.json`
- Linux: `~/.config/joule-cli/config.json`
- Windows: `%APPDATA%\joule-cli\config.json`

#### joule logout
```bash
joule logout
```
Clears all stored credentials and tokens.

#### joule status
```bash
joule status
```
Shows current login status (logged in/out), username, API URL, and auth URL.

---

### Building & Deploying

#### joule compile

Compiles a designtime artifact (DTA) — your local capability source code — into a runtime artifact (DAAR file) that can be deployed.

```bash
joule compile                          # compile current directory
joule compile ./my-capability          # compile specific source folder
joule compile ./my-capability ./output # compile to specific target
joule compile --hide-warnings          # suppress warnings
joule compile -b 5                     # compile in batches of 5
```

| Option | Description |
|--------|-------------|
| `[source folder]` | Source DTA folder (default: `.`) |
| `[target folder]` | Target folder for compiled `.daar` (default: `.`) |
| `--hide-warnings` | Suppress compilation warnings |
| `-b, --batch-size <n>` | Number of capabilities to compile at once |

The source folder must contain a `capability.sapdas.yaml` file. The output is a `.daar` (Digital Assistant Archive) file.

#### joule link

Links an AI Assistant definition to create a linked archive (`.aiaar` file).

```bash
joule link                              # link current directory
joule link ./my-assistant ./output      # link with explicit paths
joule link --hide-warnings              # suppress warnings
```

| Option | Description |
|--------|-------------|
| `[source folder]` | AI Assistant source folder (default: `.`) |
| `[target folder]` | Target for linked `.aiaar` (default: `.`) |
| `--hide-warnings` | Suppress warnings |
| `-b, --batch-size <n>` | Batch size for linking |

The source must contain an `ai_assistant.sapdas.yaml` file.

#### joule deploy

Deploys a digital assistant to the Joule service.

```bash
joule deploy                                        # deploy from current dir
joule deploy ./da.sapdas.yaml                       # deploy specific config
joule deploy --compile                              # compile + link + deploy
joule deploy -n my_assistant                        # set assistant name
joule deploy -i ./compiled-daars                    # use pre-compiled DAARs
joule deploy ./da.sapdas.yaml --compile -b 5        # compile in batches, then deploy
```

| Option | Description |
|--------|-------------|
| `[source file]` | Path to `da.sapdas.yaml` (default: `.`) |
| `-n, --name <name>` | Target digital assistant name |
| `-c, --compile` | Compile and link before deploying |
| `-i, --daars-input-dir <folder>` | Folder with pre-compiled `.daar` files |
| `-b, --batch-size <n>` | Batch size for compilation |

**Assistant name rules:** 3–50 characters, alphanumeric and underscores only, must start and end with alphanumeric (`^[a-zA-Z0-9]\w*[a-zA-Z0-9]$`).

**Deploy timeout:** Up to 15 minutes. The CLI polls the job status every 5 seconds.

---

### Managing Deployed Assistants

#### joule list

Lists all deployed digital assistants in the current tenant.

```bash
joule list
joule list --sort name
```

| Option | Description |
|--------|-------------|
| `--sort <field>` | Sort by: `id`, `name`, `description`, `display_name` |

#### joule get

Retrieves details of a specific deployed assistant.

```bash
joule get my_assistant
joule get my_assistant --capability my_cap
```

| Option | Description |
|--------|-------------|
| `<assistant name>` | Name of the deployed assistant |
| `-c, --capability <name>` | Show details for a specific capability |

#### joule launch

Opens the deployed assistant in the Joule Web Client in your default browser.

```bash
joule launch my_assistant
```

#### joule delete

Deletes a deployed digital assistant.

```bash
joule delete my_assistant
```

#### joule update

Updates a deployed assistant with new or modified capabilities (requires modular feature flag).

```bash
joule update my_assistant --capability-file ./my-cap.daar
joule update my_assistant --capability-file ./capability.sapdas.yaml -b 3
joule update my_assistant --mcp-server-file ./mcp-server.json
```

| Option | Description |
|--------|-------------|
| `<assistant name>` | Name of the deployed assistant |
| `--capability-file <path>` | Path to `.daar` or `capability.sapdas.yaml` (repeatable) |
| `--mcp-server-file <path>` | Path to MCP server metadata JSON (repeatable, beta) |
| `--hide-warnings` | Suppress warnings |
| `-b, --batch-size <n>` | Batch size for compilation |

#### joule remove

Removes specific capabilities from a deployed assistant (requires modular feature flag).

```bash
joule remove my_assistant --capability com.example:my_capability
```

| Option | Description |
|--------|-------------|
| `<assistant name>` | Name of the deployed assistant |
| `--capability <namespace:name>` | Capability to remove (repeatable) |

---

### Testing & Quality

#### joule test

Executes BDD (Cucumber) test scenarios against a deployed assistant.

```bash
joule test my_assistant                              # run all tests
joule test my_assistant -t "@smoke"                  # filter by tag
joule test my_assistant --min-success 80             # allow up to 20% failures
joule test my_assistant --feature-path "tests/**/*.feature"
joule test my_assistant --use-env                    # auth from .env
joule test my_assistant -i ./my-cap.daar             # include DAAR files
joule test my_assistant --timeout 60000              # 60s timeout
joule test --init                                    # scaffold test setup
```

| Option | Description |
|--------|-------------|
| `[assistant name]` | Name of the deployed assistant |
| `--init` | Initialize test setup scaffolding |
| `-f, --format <fmt>` | Result formatter: `pretty` (default), `json`, `html` |
| `-t, --tags <expr>` | Cucumber tag expression to filter scenarios |
| `--use-env [path]` | Read credentials from env / .env file |
| `-i, --daar-input-file <files...>` | DAAR files to include |
| `--profile <profile...>` | User profile for test execution |
| `--config <file>` | Path to cucumber config file |
| `--min-success <pct>` | Minimum pass rate (0–100, default: 100) |
| `--feature-path [globs...]` | Glob patterns for `.feature` files (default: `tests/features/**/*.feature`) |
| `--published-capabilities` | Download remote DAAR files from deployed assistant |
| `--timeout <ms>` | Test execution timeout (also via `JOULE_TEST_TIMEOUT` env var) |
| `--joule-language <lang>` | Language for test execution |

**Cucumber configuration** is searched in this order: `cucumber.json`, `cucumber.yaml`, `cucumber.yml`, `cucumber.js`, `cucumber.cjs`, `cucumber.mjs`.

**Test step examples** (Gherkin syntax):
```gherkin
Given I am user "testuser@company.com"
  And I log in
  And I start a new conversation
 When I say "Show my leave balance"
 Then first message has type text
  And first message content contains "balance"
  And response has 2 messages
```

#### joule lint

Runs static lint checks on capability source files.

```bash
joule lint                                         # lint current directory
joule lint ./my-capability                         # lint specific path
joule lint "**/*.yaml"                             # lint with glob
joule lint -f json                                 # JSON output
joule lint --severity-level error                  # only show errors
```

| Option | Description |
|--------|-------------|
| `[file/dir/glob]` | Path or glob pattern to lint (default: current dir) |
| `-f, --format <fmt>` | Output format: `pretty` (default), `json`, `html`, `combined` |
| `--severity-level <level>` | Minimum severity: `info`, `warning` (default), `error` |

Exits with code 1 if errors are found. Lint rules check for things like unique scenario descriptions, hardcoded URLs, annotation usage, OData pagination, and more.

#### joule scenario-testing-to-feature

Converts legacy YAML test scenario files into Gherkin `.feature` files for the Cucumber test framework.

```bash
joule scenario-testing-to-feature
joule scenario-testing-to-feature --input-path "tests/scenarios/**/*.yaml"
```

| Option | Description |
|--------|-------------|
| `--input-path <glob>` | Glob for YAML scenario files (default: `tests/scenarios/**/*.yaml`) |

---

## Configuration Files

### da.sapdas.yaml (Digital Assistant Definition)

This is the main deployment descriptor. It defines which capabilities make up your assistant.

```yaml
schema_version: "3.4.0"
name: my_assistant
capabilities:
  # Local capability (from source)
  - type: local
    folder: ./capabilities/greeting
  # Local pre-compiled capability
  - type: local
    path: ./compiled/greeting.daar
  # Released capability from registry
  - type: release
    namespace: com.sap.example
    name: greeting
    version: "1.0.0"
  # Milestone (pre-release) capability
  - type: milestone
    namespace: com.sap.example
    name: greeting
    version: "1.0.0-SNAPSHOT"
```

**Name constraints:** 3–50 characters, pattern `^[a-zA-Z0-9]\w*[a-zA-Z0-9]$`.
**Namespace pattern:** `^(?!\.)[a-zA-Z0-9.]+$` (no dots at start/end).
**Version pattern:** `^([0-9]+)\.([0-9]+)\.([0-9]+)(-)?( SNAPSHOT)?$`

### ai_assistant.sapdas.yaml (AI Assistant Definition)

Used with `joule link` to define an AI Assistant that orchestrates capabilities.

```yaml
schema_version: "1.0.0"
metadata:
  namespace: com.example
  name: my_ai_assistant
  version: "1.0.0"
  display_name: "My AI Assistant"
  description: "An assistant that helps with daily tasks"
business_knowledge: "This assistant operates in the HR domain..."
capabilities:
  - namespace: com.example
    name: leave_management
    scenarios:
      - check_balance
      - request_leave
```

### capability.sapdas.yaml

Each capability lives in its own folder and must have this file. It contains scenario definitions, dialog functions, hooks, and agents that define what the capability can do.

## Common Workflows

### Full development cycle

```bash
# 1. Log in
joule login --sso

# 2. Compile your capability
joule compile ./capabilities/my-cap ./output

# 3. Deploy the assistant
joule deploy ./da.sapdas.yaml --compile

# 4. Launch in browser to verify
joule launch my_assistant

# 5. Run automated tests
joule test my_assistant -t "@smoke"

# 6. Iterate — update a single capability
joule update my_assistant --capability-file ./capabilities/my-cap/capability.sapdas.yaml
```

### CI/CD pipeline

```bash
# Login via env vars (no interactive prompts)
joule login --use-env

# Lint first
joule lint ./capabilities/ --severity-level error

# Compile + deploy in one step
joule deploy ./da.sapdas.yaml --compile -n my_assistant

# Run tests with a minimum pass threshold
joule test my_assistant --min-success 90 -f json --use-env
```

### Update a single capability without redeploying everything

```bash
joule update my_assistant --capability-file ./capabilities/updated-cap.daar
```

### Remove a capability from a deployed assistant

```bash
joule remove my_assistant --capability com.example:old_capability
```

## Troubleshooting

### Login Issues

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Login fails silently | Wrong auth URL | Double-check the URL pattern — XSUAA uses `.authentication.<landscape>.hana.ondemand.com`, IAS uses `.accounts.<domain>` |
| `AUTH_LOGIN_TIMEOUT` (error 17) | Browser didn't complete SSO | Retry with `joule login --sso-passcode` or use username/password flow |
| `AUTH_FETCH_TOKEN_FAILED` (error 14) | Invalid client credentials | Verify client ID and secret from your service key |
| `AUTH_UNSUPPORTED_AUTH_TYPE` (error 16) | Unrecognized auth URL format | Ensure the auth URL follows the XSUAA or IAS pattern |
| Keytar errors on Linux | Missing libsecret | Install `libsecret-1-dev` (Debian/Ubuntu) or `libsecret-devel` (RHEL) — or use `--unsecure-storage` |

### Compile/Deploy Issues

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `COMPILE_INVALID_SOURCE` (error 22) | No `capability.sapdas.yaml` in folder | Check you're pointing to the right directory |
| `DEPLOY_INVALID_SOURCE` (error 32) | No `da.sapdas.yaml` found | Ensure the file exists at the given path |
| `INVALID_ASSISTANT_NAME` (error 36) | Name doesn't match pattern | Use 3–50 chars, alphanumeric + underscores, must start/end with alphanumeric |
| `JOB_MAX_WAITING_TIME_EXCEEDED` (error 40) | Deploy took > 15 minutes | Retry; if persistent, check service health or reduce capability count |
| `LINK_INVALID_SOURCE` (error 172) | No `ai_assistant.sapdas.yaml` | Verify the AI assistant definition file exists |

### Test Issues

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| No tests found | Wrong feature path | Use `--feature-path` with the correct glob (default: `tests/features/**/*.feature`) |
| Tests timeout | Long-running scenarios | Increase with `--timeout <ms>` or `JOULE_TEST_TIMEOUT` env var |
| `CUCUMBER_CONFIGURATION_ERROR` (error 120) | Bad cucumber config | Check `cucumber.json` / `cucumber.yaml` syntax |
| Tests pass locally but fail in CI | Missing auth | Add `--use-env` and set `JOULE_*` environment variables |

### General Debugging

- Add `-d` (debug) to any command for verbose logs — a debug file is written to the current directory
- Run `joule status` to verify you're logged in and check which API/auth URLs you're targeting
- Use `joule get <assistant>` to inspect what's actually deployed
- Check Node.js version (`node -v`) — must be v20.12.0 – v24

## Key Concepts

| Term | Meaning |
|------|---------|
| **DTA** | Design Time Artifact — your capability source code (YAML, dialogs, scenarios, hooks) |
| **DAAR** | Digital Assistant Archive — compiled capability (output of `joule compile`) |
| **AIAAR** | AI Assistant Archive — linked AI assistant (output of `joule link`) |
| **RTA** | Runtime Artifact — full deployment package uploaded during `joule deploy` |
| **Capability** | A single unit of functionality, defined in `capability.sapdas.yaml` |
| **Digital Assistant** | A deployed instance bundling capabilities, defined in `da.sapdas.yaml` |
| **AI Assistant** | Orchestration layer with business knowledge, defined in `ai_assistant.sapdas.yaml` |
