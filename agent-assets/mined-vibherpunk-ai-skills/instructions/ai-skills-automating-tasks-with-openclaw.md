# Copilot Instructions: Automating Tasks With Openclaw
Description: This skill enables you to automate real-world tasks using OpenClaw, such as responding to sponsorship emails and scheduling meetings. It includes setup instructions, workflow automation, and integration with tools like Gmail, Google Drive, and Telegram.

# Automating Tasks with OpenClaw

## Overview
OpenClaw is a powerful AI tool that acts as a digital employee, automating tasks like email responses, meeting scheduling, and tool integrations. Unlike chatbots, OpenClaw performs end-to-end tasks autonomously. This skill teaches you how to set up OpenClaw on a Virtual Private Server (VPS), configure integrations, and automate workflows.

## Step-by-Step Workflow
1. **Set Up OpenClaw on VPS**: Use a VPS for easier setup and cost efficiency. Follow the steps in [Practical Guide](references/practical_guide.md) to configure OpenClaw.
2. **Configure Telegram Integration**: Set up Telegram to interact with OpenClaw. Use the BotFather to create a bot and link it to OpenClaw.
3. **Connect Gmail and Google Drive**: Enable two-factor authentication and create app passwords for Gmail. Follow the detailed steps in [Core Concepts](references/core_concepts.md) to integrate Google Drive.
4. **Automate Sponsorship Emails**: Use OpenClaw to read, filter, and respond to sponsorship emails. Attach media kits from Google Drive automatically.
5. **Schedule Meetings**: Integrate Google Calendar to allow OpenClaw to schedule meetings autonomously.

## Code/Prompt Templates
```plaintext
# Example prompt for automating sponsorship emails
"Read the emails today for sponsorship offers from EdTech company, decline for any other offer, send them a media kit."

# Example prompt for scheduling meetings
"Schedule a meeting with Karandeep tomorrow for a discussion on Boston project. Pick any 30-minute time between 9:00 to 12:00 noon."
```

## Best Practices
- **Use VPS**: Avoid local setup complexities by using a VPS. It’s cost-effective and easier to manage.
- **Detailed Prompts**: Provide clear and detailed instructions to OpenClaw to ensure accurate task execution.
- **Regular Testing**: Test integrations and workflows regularly to ensure they function as expected.

## Common Pitfalls
- **Incomplete Setup**: Missing steps in Gmail or Google Drive integration can cause failures. Double-check each step.
- **Ambiguous Prompts**: Vague instructions can lead to incorrect task execution. Be specific in your prompts.

## Validation Steps
1. **Test Telegram Integration**: Send a message to your Telegram bot and verify OpenClaw responds correctly.
2. **Check Email Automation**: Send a test sponsorship email and confirm OpenClaw responds appropriately.
3. **Verify Meeting Scheduling**: Schedule a test meeting and confirm it appears in your Google Calendar.

For more details, refer to the [Core Concepts](references/core_concepts.md) and [Practical Guide](references/practical_guide.md).

## Reference Guides

### Core Concepts

# Core Concepts of OpenClaw

OpenClaw is designed to function as a digital employee, automating tasks that traditionally require human intervention. Unlike chatbots that merely respond to queries, OpenClaw performs end-to-end tasks autonomously. This includes reading and responding to emails, scheduling meetings, and integrating with various tools like Gmail, Google Drive, and Telegram.

## Key Features
- **Task Automation**: OpenClaw can automate repetitive tasks such as email responses and meeting scheduling.
- **Tool Integration**: It seamlessly integrates with popular tools like Gmail, Google Drive, and Telegram.
- **Autonomous Operation**: Once set up, OpenClaw operates independently, reducing the need for manual intervention.

## Setup Options
- **Local Machine**: Setting up OpenClaw on a local machine is complex and requires a separate device for security reasons.
- **Virtual Private Server (VPS)**: Using a VPS simplifies the setup process and offers cost benefits. It also allows for easy environment reset if something goes wrong.

## Integration Details
- **Gmail**: Enable two-factor authentication and create app passwords to allow OpenClaw to access your emails.
- **Google Drive**: Configure Google Drive to enable OpenClaw to fetch and attach files like media kits.
- **Telegram**: Use the BotFather to create a bot and link it to OpenClaw for seamless interaction.

For a detailed guide on setting up and using OpenClaw, refer to the [Practical Guide](references/practical_guide.md).

### Practical Guide

# Practical Guide to Setting Up OpenClaw

This guide provides step-by-step instructions for setting up OpenClaw on a Virtual Private Server (VPS) and configuring integrations with Gmail, Google Drive, and Telegram.

## Setting Up OpenClaw on VPS
1. **Choose a VPS Provider**: Select a VPS provider like Hostinger. Use the provided coupon code for a discount.
2. **Deploy OpenClaw**: Follow the provider’s instructions to deploy OpenClaw on the VPS.
3. **Initial Setup**: Complete the initial bootstrap questions to configure OpenClaw’s personality and settings.

## Configuring Telegram Integration
1. **Create a Bot**: Use the BotFather in Telegram to create a new bot.
2. **Link Bot to OpenClaw**: Copy the bot’s access token and paste it into OpenClaw’s configuration.
3. **Test Integration**: Send a message to the bot and verify OpenClaw responds correctly.

## Integrating Gmail and Google Drive
1. **Enable Two-Factor Authentication**: Go to myaccount.google.com and enable two-step verification.
2. **Create App Passwords**: Generate an app password for OpenClaw to access Gmail.
3. **Configure Google Drive**: Follow the steps to enable Google Drive API and download the JSON file.
4. **Link Google Drive**: Paste the JSON file content into OpenClaw’s configuration.

## Automating Tasks
1. **Sponsorship Emails**: Use OpenClaw to read, filter, and respond to sponsorship emails. Attach media kits from Google Drive automatically.
2. **Meeting Scheduling**: Integrate Google Calendar to allow OpenClaw to schedule meetings autonomously.

For more detailed instructions and best practices, refer to the [Core Concepts](references/core_concepts.md).

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[OpenClaw Tutorial](https://www.youtube.com/watch?v=dgbdyxe435E)** by codebasics