---
name: localwp-connect
description: Guidelines for managing LocalWP Connect to push and pull sites between local and remote environments.
---

# LocalWP Connect

This skill covers the use of LocalWP Connect, a feature designed to seamlessly pull and push sites between your local machine and supported hosting providers (WP Engine and Flywheel).

## Core Features

* **Pull from host**: Downloads a copy of the remote site to your local environment.
* **Push to host**: Uploads your local site changes (files and/or database) to the remote server.
* **MagicSync**: A file syncing engine that only transfers files that have changed, saving time and bandwidth.

## Supported Hosts

* WP Engine
* Flywheel

## Best Practices

### Before Pushing/Pulling
* Always create a backup of both your local and remote environments before initiating a sync.
* Ensure your local environment matches the remote environment (PHP version, web server) as closely as possible to prevent compatibility issues.

### Using MagicSync
* Review the list of files to be transferred carefully. Uncheck any files that shouldn't be synced (e.g., local configuration files).
* Ignore specific files or directories by using the built-in exclude settings if necessary.

### Database Syncing
* Use caution when pushing the database to a live production environment, as this will overwrite existing data (e.g., recent orders or comments).
* Consider pushing only the files and manually exporting/importing specific database tables if a full overwrite is risky.

## Troubleshooting

* **Authentication Errors**: Ensure your API credentials for WP Engine or Flywheel are up to date in the Local Connect settings.
* **Timeout Errors**: Large sites may time out during transfer. Check your internet connection or try syncing only specific components (e.g., just files, then just database).
