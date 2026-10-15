---
name: setup-team-config
description: Setup team-shared coding agent configuration from a git repository. Use when the user wants to install or configure team-shared settings for opencode or other coding agents. Triggers include "setup team config", "install team configuration", "configure team settings", or "set up shared agent config".
allowed-tools: Bash(npx @tothemax/agent-config-cli:*), AskUserQuestion
---

# setup-team-config

Install team-shared coding agent configuration from a git repository (GitLab, GitHub, or any git server).

## How to use

When this skill is invoked:

1. **Determine the repository URL** - Ask the user for the team config repository. The user may provide:
   - A **full URL** (e.g., `https://gitlab.example.com/team/configs.git`, `git@gitlab.example.com:team/configs.git`) → use it directly
   - A **short path / repo name** (e.g., `team/coding-agent-configs`) → infer the full URL

   **URL inference rules:**
   - If the input contains `://` or `@` → it is a full URL, pass it directly to CLI
   - If the input does NOT contain `://` or `@` → it is a short path. Ask the user:
     > "Is this repository on GitHub, or on another platform (e.g., your team's GitLab)? If it's on GitHub, I'll use https://github.com/<name>. Otherwise, please provide the full URL."

   - If the user confirms GitHub → prepend `https://github.com/` to form the full URL
   - If the user says another platform → ask for the full URL

   If the user does not provide any URL at all, ask them:
   > "What is the repository URL for your team's shared coding agent configuration? You can provide a full URL (e.g., https://gitlab.example.com/team/configs.git) or a short repo name (e.g., team/configs)."

2. **Ask which agent to configure** (optional) - If the user wants to configure a specific agent:
   > "Which agent do you want to configure? Available agents: opencode. Leave empty to configure all."

3. **Ask for custom config directory** (optional) - If the user wants a custom installation path:
   > "Do you want to specify a custom config directory? If so, provide the path. Otherwise the default path will be used."

4. **Call the CLI to perform setup** - Once you have the parameters, execute:

   ```bash
   npx @tothemax/agent-config-cli setup --repo "<resolved-url>" -a <agent-name> --config-dir <custom-path>
   ```

   Examples:
   ```bash
   # Full URL from GitLab
   npx @tothemax/agent-config-cli setup --repo "https://gitlab.example.com/team/configs.git" -a opencode

   # Full URL from GitHub (after inference from short path "team/configs")
   npx @tothemax/agent-config-cli setup --repo "https://github.com/team/configs" -a opencode

   # Setup all agents with default paths
   npx @tothemax/agent-config-cli setup --repo "https://github.com/team/configs"

   # Setup opencode with custom directory
   npx @tothemax/agent-config-cli setup --repo "https://gitlab.example.com/team/configs.git" -a opencode --config-dir ~/my-team-configs
   ```

5. **Handle clone failures** - If the CLI clone fails after URL inference:
   > "The clone failed. The repository may not be on GitHub. Please provide the full URL (e.g., https://gitlab.example.com/team/configs.git)."

6. **Report results** - Relay the CLI's output to the user. If the CLI returns a non-zero exit status, show the error and suggest troubleshooting steps.

## What this does

- Clones the team config repository from the resolved URL
- Installs agent configuration files to the target directory (default: `~/.config/team-agent-config/<agent-name>/`, or custom path if `--config-dir` is provided)
- Sets the agent's config directory environment variable in the user's shell profile (opencode uses `OPENCODE_CONFIG_DIR`)
- The user needs to restart their shell or source their profile for changes to take effect

## Update existing config

To update an already-installed team config:

```bash
npx @tothemax/agent-config-cli update --repo "<resolved-url>" -a <agent-name> --config-dir <custom-path>
   ```

Same URL inference rules apply for update.

## Notes

- The repository URL is dynamic and must be provided by the user each time
- Short paths (without `://` or `@`) default to GitHub; ask the user if they prefer another platform
- `-a` / `--agent` targets a specific agent; omit to configure all registered agents
- `--config-dir` requires `-a` because different agents need different directories
- The CLI assumes the user has git access (SSH key or HTTPS credentials) to the repository
- Currently only opencode is registered; more agents will be added in future versions