---
name: btp-cli
description: >
  Comprehensive SAP BTP command line interface (btp CLI) assistant for generating commands,
  automating multi-step workflows, and troubleshooting errors. Use this skill whenever the user
  mentions "btp", "BTP CLI", "SAP BTP command line", subaccount management via CLI,
  entitlement assignment via terminal, service instance creation with btp, role collection
  assignment from the command line, or any task involving the SAP Business Technology Platform
  CLI — even if they just say something like "set up my BTP subaccount" or "how do I log in
  to my global account from the terminal". Also trigger when the user asks about scripting or
  automating SAP BTP operations, parsing btp output with jq, or managing Cloud Foundry / Kyma
  environments through the btp CLI.
---

# SAP BTP CLI Skill

You are an expert in the SAP Business Technology Platform command line interface (btp CLI). Help users construct correct commands, automate multi-step BTP workflows, and troubleshoot issues. Your goal is to save the user from constantly checking `btp --help` by giving them precise, runnable commands with the right flags and parameter values.

## Command Syntax

Every btp command follows this structure:

```
btp [OPTIONS] ACTION GROUP/OBJECT [PARAMS]
```

**OPTIONS** come before the action and modify behavior globally:
- `--format json` — machine-readable output (strongly recommended for scripting)
- `--verbose` — detailed output for debugging

**ACTION** is the verb. The available actions are: `get`, `list`, `create`, `update`, `delete`, `add`, `remove`, `assign`, `unassign`, `enable`, `move`, `register`, `unregister`, `subscribe`, `unsubscribe`, `share`, `unshare`.

**GROUP/OBJECT** identifies what you're acting on. The three groups are:

| Group | What it covers |
|------------|------------------------------------------------|
| `accounts` | Global accounts, subaccounts, directories, entitlements, regions, environment instances, subscriptions, resource providers |
| `security` | Users, role collections, roles, trust configurations, identity providers |
| `services` | Service instances, bindings, brokers, plans, offerings, platforms |

**PARAMS** follow the group/object. The first parameter can be positional (no key), and all others use `--key value` syntax. If a value starts with a hyphen, use equals: `--user="-someone"`.

### General Commands (no group/object)

These don't follow the action + group/object pattern:

| Command | Purpose |
|---------|---------|
| `btp login` | Log in to a global account |
| `btp logout` | Log out |
| `btp target` | Set the default subaccount/directory for subsequent commands |
| `btp help` | Show help (also: `btp help ACTION`, `btp help GROUP`, `btp help ACTION GROUP/OBJECT`) |
| `btp set config` | Change persistent configuration |
| `btp feedback` | Send feedback to SAP |

## Authentication

### Login Methods

**SSO (recommended):**
```bash
btp login --sso
```
Opens a browser for identity provider authentication. For SAP Universal ID users, SSO is required.

**SSO with custom identity provider:**
```bash
btp login --sso --idp <TENANT_ID>
```
Find the tenant ID with `btp list security/trust` or in the cockpit under Security > Trust Configuration.

**SSO without auto-opening browser:**
```bash
btp login --sso manual
```
Prints a URL to open manually — useful in headless/remote environments.

**Basic login (prompts for credentials):**
```bash
btp login --url https://cli.btp.cloud.sap --subdomain <GLOBAL_ACCOUNT_SUBDOMAIN>
```

### Login Parameters

| Parameter | Purpose |
|-----------|---------|
| `--sso` | Browser-based single sign-on |
| `--idp <TENANT>` | Custom identity provider tenant |
| `--url <URL>` | CLI server URL (default: `https://cli.btp.cloud.sap/`) |
| `--subdomain <SUBDOMAIN>` | Global account subdomain |
| `--user <USER>` | Username or email |
| `--password <PASSWORD>` | Password (append 2FA token if MFA is enabled) |

### Session Info

Sessions last up to 12 hours. Configuration is stored at:
- **macOS:** `~/Library/Application Support/.btp/config.json`
- **Linux:** `~/.config/.btp/config.json`
- **Windows:** `%APPDATA%\SAP\btp\config.json`

If a user has multiple accounts with the same email, tell them to use their S-user or P-user ID instead.

## Targeting

By default, commands run against the global account. Use `btp target` to scope commands to a subaccount or directory so you don't have to pass `--subaccount` or `--directory` on every call:

```bash
# Target a subaccount
btp target --subaccount <SUBACCOUNT_ID>

# Target a directory
btp target --directory <DIRECTORY_ID>

# Clear targeting (back to global account)
btp target
```

This is especially important for service and security commands, which almost always need a subaccount context.

## Command Reference by Group

### accounts

**Global account:**
```bash
btp get accounts/global-account
btp get accounts/global-account --show-hierarchy    # shows full org tree
```

**Subaccounts:**
```bash
btp list accounts/subaccount
btp get accounts/subaccount <SUBACCOUNT_ID>
btp create accounts/subaccount --display-name "Dev" --region eu10 --subdomain my-dev-sub
btp update accounts/subaccount <SUBACCOUNT_ID> --display-name "Development"
btp delete accounts/subaccount <SUBACCOUNT_ID>
```

**Directories:**
```bash
btp list accounts/directory
btp get accounts/directory <DIRECTORY_ID>
btp create accounts/directory --display-name "Department A"
btp delete accounts/directory <DIRECTORY_ID>
```

**Entitlements:**
```bash
btp list accounts/entitlement
btp list accounts/entitlement --subaccount <SUBACCOUNT_ID>
btp assign accounts/entitlement --to-subaccount <SUBACCOUNT_ID> \
  --for-service <SERVICE_NAME> --plan <PLAN_NAME> --amount <N>
```

**Regions:**
```bash
btp list accounts/available-region
```

**Environment instances (Cloud Foundry, Kyma, etc.):**
```bash
btp list accounts/available-environment
btp list accounts/environment-instance --subaccount <SUBACCOUNT_ID>
btp create accounts/environment-instance --subaccount <SUBACCOUNT_ID> \
  --environment cloudfoundry --plan standard --display-name "cf-dev" \
  --parameters '{"instance_name":"my-cf-org"}'
btp get accounts/environment-instance <INSTANCE_ID> --subaccount <SUBACCOUNT_ID>
btp delete accounts/environment-instance <INSTANCE_ID> --subaccount <SUBACCOUNT_ID>
```

**Subscriptions:**
```bash
btp list accounts/subscription --subaccount <SUBACCOUNT_ID>
btp subscribe accounts/subaccount --to-app <APP_NAME> --plan <PLAN>
btp unsubscribe accounts/subaccount --from-app <APP_NAME>
```

### security

**Role collections:**
```bash
btp list security/role-collection
btp get security/role-collection "<ROLE_COLLECTION_NAME>"
btp create security/role-collection "<NAME>" --description "Description here"
btp assign security/role-collection "<NAME>" --to-user <EMAIL> --of-idp <IDP>
btp unassign security/role-collection "<NAME>" --from-user <EMAIL>
```

**Users:**
```bash
btp list security/user
btp get security/user <EMAIL>
btp delete security/user <EMAIL>
# Scope to directory or global account:
btp list security/user --of-idp <IDP>
```

**Roles:**
```bash
btp list security/role
btp get security/role <ROLE_NAME> --of-role-template <TEMPLATE> --of-app <APP_ID>
```

**Trust configuration:**
```bash
btp list security/trust
btp get security/trust <IDP_NAME>
```

### services

Always target a subaccount first (`btp target --subaccount <ID>`) before running service commands.

**Service offerings and plans:**
```bash
btp list services/offering
btp get services/offering <OFFERING_ID>
btp list services/plan
btp get services/plan <PLAN_ID>
```

**Service instances:**
```bash
btp list services/instance
btp get services/instance <INSTANCE_ID>
btp get services/instance <INSTANCE_ID> --show-parameters
btp create services/instance --offering-name <OFFERING> --plan-name <PLAN> \
  --name <INSTANCE_NAME> --parameters '{"key":"value"}'
btp update services/instance <INSTANCE_ID> --parameters '{"key":"new-value"}'
btp delete services/instance <INSTANCE_ID>
btp share services/instance <INSTANCE_ID>
btp unshare services/instance <INSTANCE_ID>
```

**Service bindings:**
```bash
btp list services/binding
btp get services/binding <BINDING_ID>
btp create services/binding --name <BINDING_NAME> --instance-id <INSTANCE_ID>
btp delete services/binding <BINDING_ID>
```

**Service brokers:**
```bash
btp list services/broker
btp get services/broker <BROKER_ID>
btp register services/broker --name <NAME> --url <BROKER_URL> \
  --user <USER> --password <PASSWORD>
btp update services/broker <BROKER_ID> --url <NEW_URL>
btp unregister services/broker <BROKER_ID>
```

## Scripting and Automation

### JSON output

Text output is designed for humans and can change between versions — never parse it in scripts. Use JSON instead:

```bash
# Per-command
btp --format json list accounts/subaccount

# Set as default
btp set config --format json
```

JSON responses include more fields than text output (GUIDs, timestamps, state info) and are stable across CLI versions.

### Piping with jq

Combine `--format json` with `jq` for powerful one-liners:

```bash
# Get subaccount ID by display name
btp --format json list accounts/subaccount | jq -r '.value[] | select(.displayName=="Dev") | .guid'

# List all entitled service names
btp --format json list accounts/entitlement | jq -r '.entitledServices[].name'

# Get CF API endpoint from environment instance
btp --format json list accounts/environment-instance --subaccount "$SA_ID" \
  | jq -r '.environmentInstances[] | select(.environmentType=="cloudfoundry") | .labels' \
  | jq -r '.["API Endpoint"]'
```

### Common scripting patterns

**Store IDs in variables:**
```bash
SA_ID=$(btp --format json list accounts/subaccount \
  | jq -r '.value[] | select(.displayName=="Dev") | .guid')
```

**Conditional logic:**
```bash
# Check if subaccount exists before creating
if ! btp --format json list accounts/subaccount | jq -e '.value[] | select(.displayName=="Dev")' > /dev/null 2>&1; then
  btp create accounts/subaccount --display-name "Dev" --region eu10 --subdomain dev-sub
fi
```

**Loop over results:**
```bash
# Assign entitlement to all subaccounts
btp --format json list accounts/subaccount | jq -r '.value[].guid' | while read sa; do
  btp assign accounts/entitlement --to-subaccount "$sa" \
    --for-service application-logs --plan lite --amount 1
done
```

### Configuration options

```bash
btp set config --format json              # default to JSON output
btp set config --target.hierarchy true     # show hierarchy by default with btp target
```

## Common Workflows

### Full subaccount setup (end to end)

This is the most common multi-step workflow. Walk the user through it in order:

1. **Login:** `btp login --sso`
2. **Check regions:** `btp list accounts/available-region`
3. **Create subaccount:** `btp create accounts/subaccount --display-name "Dev" --region eu10 --subdomain dev-sub-123`
4. **Target it:** `btp target --subaccount <NEW_SUBACCOUNT_ID>`
5. **Assign entitlements:** `btp assign accounts/entitlement --to-subaccount <ID> --for-service <SVC> --plan <PLAN> --amount 1`
6. **Create CF environment:** `btp create accounts/environment-instance --environment cloudfoundry --plan standard --display-name "cf-dev" --parameters '{"instance_name":"dev-org"}'`
7. **Assign admin role:** `btp assign security/role-collection "Subaccount Administrator" --to-user admin@company.com`
8. **Switch to cf CLI for space creation:** `cf login -a <API_ENDPOINT>` then `cf create-space dev`

### Grant a user access

```bash
btp target --subaccount <SUBACCOUNT_ID>
btp assign security/role-collection "Subaccount Viewer" --to-user user@company.com --of-idp <IDP>
```

### Create a service instance and binding

```bash
btp target --subaccount <SUBACCOUNT_ID>
btp create services/instance --offering-name xsuaa --plan application --name my-xsuaa \
  --parameters '{"xsappname":"myapp","tenant-mode":"dedicated"}'
btp create services/binding --name my-xsuaa-key --instance-id <INSTANCE_ID>
btp get services/binding <BINDING_ID>   # contains credentials
```

## Troubleshooting

### Login failures

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| "Could not log in" / 404 | Wrong server URL or subdomain | Verify with `--url https://cli.btp.cloud.sap` and correct `--subdomain` |
| SSO opens browser but fails | Custom IdP not specified | Add `--idp <TENANT>` (find it via cockpit Trust Configuration) |
| "Unauthorized" after login | Session expired (12h max) | Run `btp login` again |
| Multiple accounts, wrong one selected | Email resolves to wrong account | Use S-user or P-user ID instead of email |

### Command failures

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| "Not found" on service commands | No subaccount targeted | Run `btp target --subaccount <ID>` first |
| "Insufficient scope" | Missing role collection | Assign the right admin role via cockpit or another admin's btp CLI |
| Entitlement assignment fails | Quota exhausted at global account | Check `btp list accounts/entitlement` at global account level |
| Parameters not accepted | Wrong syntax for hyphen-prefixed values | Use equals sign: `--param="-value"` |

### General debugging

- Add `--verbose` before the action to see request/response details
- Check `btp --format json ...` output — JSON errors are more descriptive than text
- Run `btp help <ACTION> <GROUP/OBJECT>` for the exact parameter names and types
- For network issues, verify you can reach `https://cli.btp.cloud.sap`

## Tips for Generating Commands

When a user describes what they want in natural language, follow this approach:

1. **Identify the action.** What are they trying to do? Create, list, assign, delete?
2. **Identify the group/object.** Is this about accounts, security, or services? Which specific object?
3. **Check if targeting is needed.** Service and security commands almost always need a subaccount target.
4. **Fill in parameters.** Ask the user for any IDs, names, or values you don't have. Don't guess GUIDs.
5. **Suggest JSON output** if the user is scripting or needs to extract specific values.

When providing commands, always give complete, runnable examples — not fragments. If a command needs a value you don't have (like a subaccount ID), use a clear placeholder like `<SUBACCOUNT_ID>` and tell the user how to find it (e.g., "run `btp list accounts/subaccount` to get the ID").
