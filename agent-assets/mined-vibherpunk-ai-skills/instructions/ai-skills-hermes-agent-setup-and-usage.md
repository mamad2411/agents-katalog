# Copilot Instructions: Hermes Agent Setup And Usage
Description: A comprehensive guide to setting up and using the Hermes AI Agent locally on your machine, including Telegram integration, skill management, and cron job setup.

# Hermes Agent Setup and Usage

## Overview
Hermes Agent is a powerful, open-source AI agent that runs locally on your machine. It features a curator for self-improvement, bounded memory for consistent performance, and integrates with Telegram for easy interaction. For a detailed breakdown of its core concepts, see [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow
1. **Download and Install**:
   - Visit hermesagent.newsresearch.com and download the app for your OS.
   - Install it by dragging to Applications (Mac) or running the installer (Windows).

2. **Initial Setup**:
   - Launch Hermes and click "Install Hermes" to download dependencies.
   - Configure the AI model using a free Google AI Studio API key. See [Practical Guide](references/practical_guide.md) for details.

3. **Telegram Integration**:
   - Create a bot via @BotFather in Telegram.
   - Paste the bot token and your user ID into Hermes. Restart the messaging gateway.

4. **Agent Context**:
   - Start a chat session and provide context about yourself. Example prompts are in [Code Examples](references/code_examples.md).

5. **Cron Jobs and Skills**:
   - Set up cron jobs for automated tasks like morning news briefs.
   - Manage skills via the Skills section in the sidebar.

6. **Maintenance**:
   - Regularly run the curator (`Hermes curator run`) to optimize skills.
   - Use `Hermes doctor` for diagnostics.

## Best Practices
- **Calibration**: Regularly check and update your agent's knowledge about you.
- **Security**: Only whitelist trusted Telegram IDs.
- **Memory Management**: Avoid overloading the agent with redundant skills.

For common pitfalls and how to avoid them, see [Common Pitfalls](references/common_pitfalls.md).

## Validation Steps
1. **Telegram Test**: Send a message to your bot to ensure it responds.
2. **Cron Job Test**: Verify that scheduled tasks execute as expected.
3. **Curator Test**: Run the curator and check the skill library for optimizations.

By following this guide, you'll have a fully functional Hermes Agent tailored to your needs.

## Reference Guides

### Code Examples

# Code Examples and Prompt Templates

## Setting Up a Cron Job
To set up a morning AI news brief, use the following prompt in the Hermes chat:
```
Set up a cron job that runs every morning at 7:00 a.m. Search for the top three AI news stories and send me a summary in Telegram.
```

## Skill Management
To check available skills, ask:
```
What tools do you have available right now?
```

To enable or disable skills, navigate to the Skills section in the left sidebar and toggle them as needed.

## Curator Command
To manually trigger the curator, open the built-in terminal in Hermes and run:
```
Hermes curator run
```

## Diagnostics
To check the agent's status, run:
```
Hermes doctor
```

For more details on core concepts and best practices, see [Core Concepts](references/core_concepts.md) and [Practical Guide](references/practical_guide.md).

### Common Pitfalls

# Common Pitfalls and Best Practices

## Pitfalls
1. **Fake Downloads**: Ensure you download Hermes from the official site (hermesagent.newsresearch.com) to avoid fake versions.
2. **Cron Jobs**: Cron jobs only run while your computer is on. For 24/7 operation, leave your machine running or use a dedicated device.
3. **Memory Issues**: Hermes uses bounded memory. Avoid overloading it with redundant skills or excessive context.
4. **API Limits**: The free-tier Gemini 2.5 Flash has a limit of 1,500 requests per day. Monitor usage to avoid hitting limits.

## Best Practices
1. **Regular Calibration**: Periodically ask your agent what it knows about you and correct any inaccuracies.
2. **Skill Optimization**: Let the curator run regularly to merge and optimize skills.
3. **Security**: Only whitelist trusted Telegram chat IDs to prevent unauthorized access.
4. **Model Switching**: If you need more capacity, consider switching to a paid model via OpenRouter.

For practical examples and setup guides, refer to [Practical Guide](references/practical_guide.md) and [Code Examples](references/code_examples.md).

### Core Concepts

# Core Concepts of Hermes Agent

Hermes Agent is an open-source AI agent that runs locally on your machine (Mac, Windows, or Linux). Unlike other agents, it features a curator that periodically reviews and optimizes its own skills, bounded memory to maintain performance, and works with free-tier AI models like Gemini 2.5 Flash through Google AI Studio.

## Key Features
1. **Curator System**: Automatically reviews and optimizes skills, merging redundant ones and rewriting stale ones.
2. **Bounded Memory**: Enforces a memory budget to keep the agent fast and predictable over time.
3. **Cost-Effective**: Uses free-tier AI models, requiring no paid subscriptions for basic use.
4. **Local Execution**: Runs entirely on your machine, no cloud server needed.
5. **Telegram Integration**: Allows interaction via Telegram, with whitelisting for security.

## Use Cases
- Morning AI news briefs
- Competitor research
- Daily check-ins
- Home Assistant integration
- Kanban task management

For more details on setting up and using these features, see [Practical Guide](references/practical_guide.md).

### Practical Guide

# Practical Guide to Hermes Agent

## Installation
1. Download the Hermes Agent from the official site (hermesagent.newsresearch.com).
2. For Mac, drag the app to your Applications folder. For Windows, run the installer.
3. Open the app and click "Install Hermes" to download dependencies.

## Initial Setup
1. **Model Configuration**:
   - Go to Google AI Studio (aastudio.google.com) and get an API key.
   - In Hermes, select Google as the provider and paste the API key.
   - Choose Gemini 2.5 Flash from the model list.
2. **Agent Context**:
   - Start a chat session and provide context about yourself. Example:
     ```
     Your name is Master Agent. I'm [Your Name]. I run [Your Role]. I'm interested in [Your Interests]. I prefer concise updates. My time zone is [Your Time Zone]. When you're unsure, ask me rather than guessing.
     ```

## Telegram Integration
1. In Telegram, search for @BotFather and create a new bot.
2. Copy the bot token and paste it into Hermes under Messaging > Telegram.
3. Get your Telegram user ID by messaging @userinfobot and paste it into Hermes.
4. Restart the messaging gateway in Hermes.

For more examples and troubleshooting, see [Code Examples](references/code_examples.md).

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Hermes Agent Tutorial: How to Setup & Use Open Source AI Agent for Beginners](https://www.youtube.com/watch?v=uSdVgSY7ryU)** by AI Master