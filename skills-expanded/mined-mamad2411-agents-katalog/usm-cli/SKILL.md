---
name: usm-cli
description: Manage UniFi sites via the cloud-based Site Manager API using the usm CLI. Use when working with multiple sites, cloud controllers, or UniFi cloud infrastructure.
---

# Skill: usm-cli

# UniFi Site Manager CLI

This skill provides guidance for the `usm` CLI tool, a command-line interface for the UniFi Site Manager API.

## Overview

`usm` provides cloud-based management of UniFi sites via the official Site Manager API at `api.ui.com`. For local controller APIs (Network, Protect), see the separate `unifi` CLI.

## Installation

### Homebrew
```bash
brew tap dl-alexandre/tap
brew install usm
```

### Manual
Download from GitHub Releases:
```bash
# macOS (Apple Silicon)
curl -L https://github.com/dl-alexandre/UniFi-Site-Manager-CLI/releases/latest/download/usm-darwin-arm64 -o usm
chmod +x usm
sudo mv usm /usr/local/bin/
```

## Quick Start

1. Get API Key from unifi.ui.com → Settings → Control Plane → Integrations → API Keys

2. Configure:
```bash
usm init
# Or: export USM_API_KEY="your-api-key"
```

3. Verify:
```bash
usm whoami
```

4. List sites:
```bash
usm sites list
```

## Available Commands

### usm init
Interactive configuration setup. Creates `~/.config/usm/config.yaml`.

**Use when:**
- First-time setup
- Changing default settings (base URL, output format, color mode)

**Flags:**
- `--force` - Overwrite existing config

### usm sites list
List all sites with pagination and filtering.

**Use when:**
- Getting an overview of all UniFi sites
- Finding a specific site by name
- Exporting site data

**Flags:**
- `--page-size=N` - Number of sites per page (default: 50, 0 = fetch all)
- `--search=<term>` - Filter by name/description
- `--output=json|table` - Output format
- `--no-headers` - Table without headers (for scripts)

**Examples:**
```bash
usm sites list                          # Default: 50 sites
usm sites list --page-size 0            # Fetch all sites
usm sites list --search "office"        # Filter by name
usm sites list --output json            # JSON output
usm sites list --no-headers             # For piping to other tools
```

### usm sites get <site-id>
Get detailed information about a specific site.

**Use when:**
- You need details about one specific site
- You have a site ID and want to verify it exists

**Examples:**
```bash
usm sites get 60abcdef1234567890abcdef
usm sites get 60abcdef1234567890abcdef --output json
```

### usm whoami
Show authenticated user account information.

**Use when:**
- Verifying API key is working
- Checking which account you're authenticated as

**Examples:**
```bash
usm whoami
usm whoami --output json
```

### usm version
Show version information.

**Use when:**
- Checking installed version
- Checking for updates (with `--check`)

**Flags:**
- `--check` - Check GitHub for latest release

## Configuration

Config file: `~/.config/usm/config.yaml`

**Note:** API keys are NOT stored in config. Use environment variables or flags.

```yaml
api:
  base_url: https://api.ui.com
  timeout: 30

output:
  format: table      # table, json
  color: auto        # auto, always, never
  no_headers: false
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `USM_API_KEY` | API key for authentication (required) |
| `USM_BASE_URL` | API base URL (default: https://api.ui.com) |
| `USM_TIMEOUT` | Request timeout in seconds |
| `USM_FORMAT` | Default output format |
| `USM_COLOR` | Color mode |
| `USM_NO_HEADERS` | Disable table headers |
| `USM_CONFIG` | Path to config file |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Authentication failure |
| 3 | Permission denied |
| 4 | Validation error |
| 5 | Rate limited |
| 6 | Network error |

## API Reference

- [Site Manager API Documentation](https://developer.ui.com/site-manager/v1.0.0/gettingstarted)

## Related Tools

- `unifi` CLI - For local UniFi Network and Protect APIs

## Common Workflows

### List all sites and export to JSON
```bash
usm sites list --page-size 0 --output json > sites.json
```

### Find a site by name and get its details
```bash
SITE_ID=$(usm sites list --search "Office" --output json | jq -r '.[0]._id')
usm sites get "$SITE_ID"
```

### Check authentication in CI/CD
```bash
usm whoami || exit 1
```

### Table output for reports
```bash
usm sites list --no-headers | column -t
```
