---
name: getting-started
description: "Use when pipelines CLI is not installed, authentication fails, or user needs to set up pipelines-cli for the first time."
license: Proprietary
compatibility: pipelines-cli>=1.x
metadata:
    category: onboarding
    author: Acquia
    version: "1.0.0"
    tags: "pipelines-cli, acquia-cloud, ci-cd, installation, authentication"
    software_requirements: "pipelines-cli>=1.x"
---

# Getting Started with Acquia Pipelines CLI

Use when:
- Installing the Pipelines CLI for the first time
- Configuring API credentials
- Verifying your connection to Acquia Cloud
- Updating the CLI to the latest version

## Tool Overview

Two separate CLIs exist for Acquia Cloud operations:

| Tool | Purpose |
|---|---|
| `pipelines-cli` | CI/CD pipeline operations: trigger builds, check job status, stream logs |
| `acli` | General Cloud management: applications, environments, IDEs, SSH keys, code/DB sync |

Use **pipelines-cli** for pipeline jobs. Use **acli** for everything else.

---

## Installation

### Download the binary

```bash
wget https://cloud.acquia.com/pipelines-client/download -O pipelines
chmod +x pipelines
sudo mv pipelines /usr/local/bin
```

### Verify installation

```bash
pipelines --version
pipelines help
```

---

## Authentication

### Configure credentials interactively

```bash
pipelines configure
```

You will be prompted for your **Acquia Cloud API key** and **API secret**:

```
Please enter your Acquia Cloud API key: <your-key>
Please enter your Acquia Cloud API secret: <hidden>
Configuration successful.
```

### Configure credentials non-interactively

Useful for CI/CD environments where interactive prompts are not available:

```bash
pipelines configure --key=YOUR_KEY --secret=YOUR_SECRET
```

### Configure with a custom endpoint

Only needed if you are not using the default Acquia Cloud endpoint:

```bash
pipelines configure --key=YOUR_KEY --secret=YOUR_SECRET --endpoint=https://your-custom-endpoint.com
```

### Reset credentials

If your credentials change or you need to reconfigure:

```bash
pipelines reset-credentials
```

Then run `pipelines configure` again.

---

## Verify Your Connection

After configuring, confirm your environment is set up correctly:

```bash
pipelines show-connection <application_id>
```

Output confirms whether the connection and application access are working.

To find your application ID first:

```bash
pipelines list-applications
```

---

## Common First Steps

### Step 1: Install

```bash
wget https://cloud.acquia.com/pipelines-client/download -O pipelines
chmod +x pipelines
sudo mv pipelines /usr/local/bin
```

### Step 2: Configure credentials

```bash
pipelines configure
```

### Step 3: Find your application

```bash
pipelines list-applications
```

### Step 4: Verify connection

```bash
pipelines show-connection <application_id>
```

### Step 5: Start your first pipeline

```bash
pipelines start --application-id=<application_id>
```

---

## Keeping the CLI Updated

```bash
pipelines self-update
```

Run this periodically to get bug fixes and new features.

---

## Getting Help

```bash
# List all available commands
pipelines

# Help for a specific command
pipelines help start
pipelines help configure

# Version (include in bug reports)
pipelines --version
```

---

## Troubleshooting

### "command not found: pipelines"

The binary is not in your `PATH`. Ensure you moved it to `/usr/local/bin` or another directory on your `PATH`:

```bash
which pipelines
export PATH="/usr/local/bin:$PATH"
```

### "Configuration failed. Please check your credentials and try again."

Your API key or secret is incorrect. Verify them in the Acquia Cloud UI under **API Keys**, then re-run:

```bash
pipelines configure
```

### "Non-interactive mode can only be used when key and secret are provided as cli options."

When using `--no-interaction`, you must pass both `--key` and `--secret`:

```bash
pipelines configure --no-interaction --key=YOUR_KEY --secret=YOUR_SECRET
```

---

## Next Steps

- **[Manage applications](../application-management/SKILL.md)** — Find application IDs, link repos
- **[Run pipeline jobs](../pipeline-operations/SKILL.md)** — Start, monitor, and manage builds
