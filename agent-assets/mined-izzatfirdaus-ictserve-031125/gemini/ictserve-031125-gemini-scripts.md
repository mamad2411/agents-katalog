# scripts Directory - GEMINI Instructions

This file provides instructions for the Gemini AI related to the `scripts` directory of the ICTServe project.

## Directory Overview

The `scripts` directory contains utility scripts for development, deployment, and maintenance tasks. These are typically shell scripts or other executable files that automate common operations.

## Instructions

* **Script Permissions:** All scripts should be executable. Use `chmod +x script-name.sh` to make a script executable.
* **Error Handling:** Use `set -e` at the beginning of bash scripts to exit immediately if any command fails.
* **Documentation:** Add comments explaining what each script does and any prerequisites or environment variables required.
* **Shebang:** Start shell scripts with the appropriate shebang line (e.g., `#!/bin/bash` or `#!/usr/bin/env bash`).
* **Cross-Platform:** When possible, write scripts that work on both Linux/Mac and Windows (or provide both versions).

## Common Script Types

* **Deployment Scripts:** Automate deployment tasks like pulling code, installing dependencies, running migrations
* **Setup Scripts:** Initialize development environments, set up databases, create test data
* **Utility Scripts:** Helper scripts for common tasks like clearing caches, optimizing assets, backing up data
* **CI/CD Scripts:** Scripts used in continuous integration and deployment pipelines

## Best Practices

* Use descriptive names that clearly indicate the script's purpose
* Add usage information or help text for scripts that accept arguments
* Log important steps with `echo` statements for visibility
* Test scripts in a safe environment before running in production
* Use environment variables for configuration instead of hardcoded values
* Include error messages that help diagnose problems
* Clean up temporary files or resources before exiting

## Example Script Structure

```bash
#!/bin/bash
set -e

# Script description
# Usage: ./script-name.sh [options]

echo "--> Step 1: Description"
# commands here

echo "--> Step 2: Description"
# more commands

echo "--> Complete!"
```

## Security Considerations

* Never commit sensitive credentials or API keys in scripts
* Use environment variables or .env files for sensitive data
* Validate and sanitize any user input
* Be cautious with destructive operations (deletions, database drops)
* Review scripts for potential security vulnerabilities before using in production
