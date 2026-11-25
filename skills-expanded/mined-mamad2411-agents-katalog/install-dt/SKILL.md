---
name: install-dt
description: Install the Dovetail dt CLI via npm or npx, then run initial workspace setup.
license: MIT
metadata:
  author: dovetail
  version: "1.0"
---

# Install the Dovetail CLI (`dt`)

Installs `dt`, the Dovetail command-line tool for importing content from Notion, Confluence, Google Drive, Airtable, Marvin, Condens, EnjoyHQ, Productboard, local files, and more.

## Installation

### Option 1: Global install via npm (recommended)

```bash
npm install -g @heydovetail/dt
```

Verify:

```bash
dt --version
```

### Option 2: One-off use via npx

```bash
npx @heydovetail/dt <command>
```

Use this in CI/CD or when a global install is not possible.

## Initial setup

After installing, run the setup wizard to connect your Dovetail workspace:

```bash
export DOVETAIL_API_KEY="your-api-key"  # from your workspace Settings > API
dt init
```

`dt init` configures your workspace URL and API key, then walks you through adding your first data source.

Run a health check at any time:

```bash
dt doctor
```

## When to use

- Before running any `dt` commands for the first time
- When setting up a new machine or CI environment
- Use **global install** when `dt` will be called repeatedly
- Use **npx** for one-off or ephemeral environments

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `command not found: dt` after global install | Run `npm config get prefix` and ensure `<prefix>/bin` is on your `PATH` |
| Permission denied during global install | Use `sudo npm install -g @heydovetail/dt` or configure a user-writable npm prefix |
| `dt doctor` reports connectivity errors | Confirm `DOVETAIL_API_KEY` is set and your workspace URL is correct in `dt.json` |
