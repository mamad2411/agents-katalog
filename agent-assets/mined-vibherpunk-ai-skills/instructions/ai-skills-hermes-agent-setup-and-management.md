# Copilot Instructions: Hermes Agent Setup And Management
Description: A comprehensive skill for setting up and managing Hermes Agent, an open-source AI assistant, including installation, configuration, skill development, and automation.

### Overview
Hermes Agent is a powerful, open-source AI assistant that grows with you through a self-improving loop of skills and automations. It runs on your own infrastructure and can be managed through various platforms like Telegram, Discord, and Slack. This skill will guide you through setting up Hermes Agent, configuring its core functionalities, and leveraging its capabilities for automation and skill development.

### Core Concepts
Hermes Agent operates on five main pillars: Memory, Skills, Soul, Cron, and Self-Improving Loop. These pillars enable Hermes to carry context across sessions, execute reusable tasks, shape its personality, schedule automations, and improve over time. For a deeper dive into these concepts, refer to [Core Concepts](references/core_concepts.md).

### Step-by-Step Workflow
1. **Set Up VPS**: Choose a virtual private server (VPS) provider like Hostinger and deploy Hermes Agent. For detailed instructions, see [Practical Guide](references/practical_guide.md).
2. **Install Hermes Agent**: Use the one-click Docker installation method for simplicity. Alternatively, install directly on the VPS root.
3. **Configure Hermes Agent**: Set up inference providers, messaging channels, and API keys. Use the following command to set an API key securely:
```bash
HERMES_CONFIG_SET GITHUB_TOKEN=<your_token>
```
4. **Develop Skills**: Create reusable playbooks for tasks. Example skill template:
```yaml
---
name: Generate Image
description: Generates an image based on a description.
steps:
  - description: Describe the image
    command: generate_image --description "{{ description }}"
---
```
5. **Set Up Cron Jobs**: Schedule automations using natural language commands. Example:
```bash
hermes cron create --name "Daily AI News Briefing" --time "06:00" --command "generate_news_briefing"
```
6. **Connect to GitHub**: Sync your Hermes Agent with a GitHub repo for backup and version control.

### Best Practices and Common Pitfalls
- **Best Practices**:
  - Use Docker containers for easy management.
  - Secure API keys by storing them in `.env` files.
  - Regularly back up your Hermes Agent to GitHub.
- **Common Pitfalls**:
  - Avoid storing secrets in conversation history.
  - Ensure proper permissions for GitHub tokens to avoid creation failures.

### Validation and Testing
1. **Test Connection**: Verify Hermes Agent responds to basic commands.
2. **Check Cron Jobs**: Ensure scheduled tasks execute as expected.
3. **Validate GitHub Sync**: Confirm that changes are pushed to the GitHub repo.

For more detailed examples and code snippets, refer to [Code Examples](references/code_examples.md).

### References
- [Core Concepts](references/core_concepts.md)
- [Practical Guide](references/practical_guide.md)
- [Code Examples](references/code_examples.md)

## Reference Guides

### Code Examples

### Code Examples for Hermes Agent
This document provides concrete code snippets and prompt templates for managing Hermes Agent.

1. **Setting API Keys**: Securely store API keys in `.env` files.
```bash
HERMES_CONFIG_SET GITHUB_TOKEN=<your_token>
```

2. **Skill Development**: Create reusable playbooks for tasks.
```yaml
---
name: Generate Image
description: Generates an image based on a description.
steps:
  - description: Describe the image
    command: generate_image --description "{{ description }}"
---
```

3. **Cron Jobs**: Schedule automations using natural language commands.
```bash
hermes cron create --name "Daily AI News Briefing" --time "06:00" --command "generate_news_briefing"
```

4. **GitHub Sync**: Sync Hermes Agent with a GitHub repo.
```bash
hermes github sync --repo <repo_name> --token <github_token>
```

5. **Terminal Commands**: Manage Hermes Agent via terminal.
```bash
hermes start
hermes stop
hermes status
```

These examples provide a foundation for managing Hermes Agent effectively. For a deeper understanding of core concepts, refer to [Core Concepts](references/core_concepts.md).

### Core Concepts

### Core Concepts of Hermes Agent
Hermes Agent is built on five main pillars that define its functionality and capabilities:

1. **Memory**: Hermes carries small, durable context across sessions using `user.md` and `memory.md` files. These files store user preferences, environments, and project contexts, ensuring Hermes wakes up with relevant information.

2. **Skills**: Skills are reusable playbooks for tasks. They are stored in `skill.md` files and invoked based on the task at hand. Skills ensure consistent execution of tasks, much like following a recipe.

3. **Soul**: The `soul.md` file shapes the personality of Hermes Agent. It allows customization of the assistant's tone and behavior, making it unique for different users or tasks.

4. **Cron**: Cron jobs turn Hermes from reactive to proactive by scheduling automations. These jobs run isolated sessions at specified times, executing tasks without inheriting current session context.

5. **Self-Improving Loop**: Hermes improves over time by persisting useful experiences as memory, skills, and searchable history. This loop ensures continuous enhancement based on user feedback and task execution.

Understanding these pillars is crucial for effectively managing and leveraging Hermes Agent's capabilities. For practical applications and examples, refer to [Practical Guide](references/practical_guide.md) and [Code Examples](references/code_examples.md).

### Practical Guide

### Practical Guide to Setting Up Hermes Agent
This guide provides step-by-step instructions for setting up and managing Hermes Agent on a virtual private server (VPS).

1. **Choose a VPS Provider**: Select a provider like Hostinger and deploy a VPS. Choose a plan based on your CPU and RAM needs.

2. **Install Hermes Agent**:
   - **One-Click Docker Installation**: Use the Docker manager in your VPS dashboard to install Hermes Agent in a containerized environment.
   - **Root Installation**: Alternatively, install Hermes directly on the VPS root using terminal commands.

3. **Configure Hermes Agent**:
   - **Inference Providers**: Set up inference providers like OpenAI Codex for model usage.
   - **Messaging Channels**: Configure messaging platforms such as Telegram for interaction.
   - **API Keys**: Securely store API keys in `.env` files using commands like `HERMES_CONFIG_SET GITHUB_TOKEN=<your_token>`.

4. **Develop Skills**: Create and manage skills using `skill.md` files. Example skill template:
```yaml
---
name: Generate Image
description: Generates an image based on a description.
steps:
  - description: Describe the image
    command: generate_image --description "{{ description }}"
---
```

5. **Set Up Cron Jobs**: Schedule automations using natural language commands. Example:
```bash
hermes cron create --name "Daily AI News Briefing" --time "06:00" --command "generate_news_briefing"
```

6. **Connect to GitHub**: Sync Hermes Agent with a GitHub repo for backup and version control. Ensure proper permissions for GitHub tokens to avoid creation failures.

For more detailed examples and code snippets, refer to [Code Examples](references/code_examples.md).

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Hermes Agent: Zero to Personal AI Assistant (1 Hour Course)](https://www.youtube.com/watch?v=gb5TlGw6Uks)** by Nate Herk | AI Automation