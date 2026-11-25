---
name: simple-history-wp-cli
description: Managing and querying the Simple History audit log via the command line using WP-CLI.
---

# Simple History & WP-CLI

Simple History comes with built-in support for WP-CLI. This is incredibly useful for system administrators and agencies who need to audit multiple sites without logging into the WordPress admin panel.

## 1. Viewing Logs (`list`)
The primary command is `wp simple-history list`. This outputs a formatted table of recent events.

```bash
# List the 10 most recent events
wp simple-history list

# List 50 events
wp simple-history list --count=50
```

## 2. Searching and Filtering
You can pass various arguments to filter the log output.

```bash
# Search for events containing a specific keyword
wp simple-history list --search="plugin"

# Filter by log level (info, warning, error, critical)
wp simple-history list --level="warning"
```

## 3. Formatting and Exporting
By default, the output is a human-readable table. You can change the format for scripting or exporting.

```bash
# Export the log to a CSV file
wp simple-history list --format=csv > audit_log.csv

# Output as JSON for integration with other tools
wp simple-history list --format=json
```

## 4. Useful Subcommands
Starting with version 5.27.0, you can run `wp simple-history info` to see the installed version, premium add-on status, and a list of useful subcommands.

```bash
wp simple-history info
```

You can also use `--fields=` with the `list` command to extract very specific information, such as `date_relative` or `ai_agent` to track if an action was initiated by an AI tool like Claude Code or ChatGPT.
