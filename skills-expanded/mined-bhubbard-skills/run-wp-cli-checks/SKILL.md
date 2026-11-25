---
name: run-wp-cli-checks
description: Use the WP-CLI command from the Plugin Check plugin to validate WordPress plugins.
---

# Run Plugin Checks via WP-CLI

The Plugin Check (PCP) plugin provides a WP-CLI command to validate plugins against WordPress.org directory requirements.

## Basic Usage
To run static checks on a plugin file or directory:
```bash
wp plugin check /path/to/plugin
```

## Running Runtime Checks
To run runtime checks, you must load the `cli.php` file from the plugin-check directory before WordPress loads using the `--require` flag:
```bash
wp plugin check /path/to/plugin --require=./wp-content/plugins/plugin-check/cli.php
```

## Output Formatting
You can export results into various formats such as CSV, JSON, and Markdown. This is useful for CI/CD pipelines.
