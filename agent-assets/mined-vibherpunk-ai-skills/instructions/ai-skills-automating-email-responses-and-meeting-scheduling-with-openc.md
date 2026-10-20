# Copilot Instructions: Automating Email Responses And Meeting Scheduling With Openclaw
Description: A comprehensive skill for setting up OpenClaw as a digital assistant to automate email responses and meeting scheduling, including integration with Gmail, Google Drive, and Google Calendar.

# Automating Email Responses and Meeting Scheduling with OpenClaw

## Overview
OpenClaw is a digital assistant that automates tasks like email responses and meeting scheduling. This skill covers setting up OpenClaw on a VPS, integrating it with Gmail, Google Drive, and Google Calendar, and creating autonomous workflows. For core concepts, see [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow
1. **Set Up OpenClaw on a VPS**:
   - Choose a VPS provider (e.g., Hostinger) and deploy OpenClaw using the one-click setup.
   - Configure initial settings, including the assistant's personality and communication channels (Telegram/WhatsApp).

2. **Integrate Gmail**:
   - Enable two-factor authentication and generate an app password.
   - Provide the email and password to OpenClaw for authentication.

3. **Integrate Google Drive**:
   - Create an OAuth client ID and download the JSON file.
   - Provide the JSON file to OpenClaw and authorize access.

4. **Integrate Google Calendar**:
   - Enable the Google Calendar API and authenticate OpenClaw.
   - Test by scheduling a meeting via Telegram.

5. **Create Autonomous Workflows**:
   - Set up cron jobs for daily email checks and responses.
   - Use natural language commands to automate tasks (e.g., "Schedule a meeting with Karan tomorrow").

For detailed steps, refer to the [Practical Guide](references/practical_guide.md).

## Code Snippets and Prompt Templates
```plaintext
Read the emails today for sponsorship offers from EdTech companies.
```
```plaintext
Schedule a meeting with Karandeep tomorrow for a discussion on the Boston project. Pick any 30-minute time between 9:00 to 12:00 noon.
```
More examples can be found in [Code Examples](references/code_examples.md).

## Best Practices and Pitfalls
- **Best Practices**:
  - Use a VPS for easier setup and maintenance.
  - Interact with OpenClaw using natural language.
  - Monitor tool calls to understand and troubleshoot workflows.

- **Pitfalls**:
  - Avoid local setup due to complexity and security risks.
  - Double-check authentication settings to prevent errors.
  - Handle broken links during integration by pasting them back to OpenClaw.

For more details, see [Common Pitfalls](references/common_pitfalls.md).

## Validation and Testing
1. **Test Email Automation**:
   - Send a test sponsorship email and verify OpenClaw's response.
   - Check the sent folder to ensure the response and attachments are correct.

2. **Test Meeting Scheduling**:
   - Schedule a test meeting via Telegram and verify it appears in Google Calendar.
   - Confirm the meeting details (time, participants) are accurate.

3. **Test Cron Jobs**:
   - Verify the cron job is set up correctly and runs at the specified time.
   - Check logs to ensure the job executes as expected.

By following these steps, you can ensure OpenClaw is functioning correctly and efficiently automating your tasks.

## Reference Guides

### Code Examples

# Code Examples and Prompt Templates

This document provides concrete examples of commands and prompts used to interact with OpenClaw for email automation and meeting scheduling.

## Email Automation
1. **Reading Emails**:
   ```plaintext
   Read the emails today for sponsorship offers from EdTech companies.
   ```
2. **Responding to Emails**:
   ```plaintext
   For any offers, respond by attaching the media kit. You can find the media kit in Google Drive.
   ```

## Meeting Scheduling
1. **Scheduling a Meeting**:
   ```plaintext
   Schedule a meeting with Karandeep tomorrow for a discussion on the Boston project. Pick any 30-minute time between 9:00 to 12:00 noon.
   ```
2. **Setting Up Cron Jobs**:
   ```plaintext
   Set up a daily job at 4:00 PM to check for sponsorship emails and respond accordingly.
   ```

These examples demonstrate how natural language commands can be used to automate complex tasks. For more details on setup, refer to the [Practical Guide](references/practical_guide.md).

### Common Pitfalls

# Common Pitfalls and Best Practices

## Pitfalls
1. **Local Setup Complexity**: Setting up OpenClaw on a local machine is complex and not recommended due to security and maintenance issues.
2. **Authentication Errors**: Incorrectly configuring OAuth client IDs or app passwords can lead to authentication failures. Always double-check the settings.
3. **Broken Links**: During Google Drive or Calendar integration, you may encounter broken links. Copy and paste the entire URL back to OpenClaw for resolution.

## Best Practices
1. **Use VPS**: A virtual private server simplifies setup and maintenance, offering benefits like disposability and one-click deployment.
2. **Natural Language Commands**: Interact with OpenClaw as if it were a human assistant. For example, "Help me connect to Gmail" is more effective than technical jargon.
3. **Monitor Tool Calls**: Review the tool calls and outputs to understand what OpenClaw is doing behind the scenes. This helps in troubleshooting and optimizing workflows.

For example, in the transcript, the user initially faced issues with Google Drive integration due to selecting the wrong app type (web vs. desktop). This highlights the importance of carefully following setup instructions. Refer to the [Practical Guide](references/practical_guide.md) for detailed setup steps.

### Core Concepts

# Core Concepts of OpenClaw Automation

OpenClaw is a powerful AI tool that functions as a digital employee, capable of performing end-to-end tasks such as reading and responding to emails, scheduling meetings, and integrating with various tools like Gmail, Google Drive, and Google Calendar. Unlike traditional chatbots, OpenClaw executes tasks autonomously, reducing manual effort and increasing efficiency.

Key concepts include:
1. **Digital Employee**: OpenClaw acts as a virtual assistant, handling tasks that would typically require human intervention.
2. **Tool Integration**: OpenClaw connects with various APIs (e.g., Gmail, Google Calendar) to perform tasks seamlessly.
3. **Autonomous Workflows**: Once set up, OpenClaw can run predefined workflows (e.g., daily email checks) without manual triggers.
4. **Natural Language Interaction**: Users can interact with OpenClaw via natural language commands, making it accessible to non-technical users.

For example, in the transcript, OpenClaw automates the process of responding to sponsorship emails by reading the email content, determining the appropriate response, and attaching relevant documents from Google Drive. This demonstrates its ability to handle complex workflows autonomously.

### Practical Guide

# Practical Guide to Setting Up OpenClaw

This guide provides step-by-step instructions for setting up OpenClaw on a VPS and configuring it for email automation and meeting scheduling.

## VPS Setup
1. **Choose a VPS Provider**: Hostinger is recommended for its ease of use and cost-effectiveness. Use the provided coupon code for a discount.
2. **Select a Plan**: The KVM 2 plan offers the best price-to-performance ratio.
3. **Deploy OpenClaw**: Follow the one-click setup process provided by the VPS provider.

## Initial Configuration
1. **Bootstrap OpenClaw**: Answer initial setup questions to define the assistant's personality (e.g., "You are ClawBuddy, a friendly AI with a warm and funny vibe").
2. **Configure Communication Channels**: Set up Telegram or WhatsApp for interacting with OpenClaw on the go.

## Tool Integrations
1. **Gmail Integration**: Enable two-factor authentication and generate an app password for OpenClaw.
2. **Google Drive Integration**: Create an OAuth client ID and download the JSON file for authentication.
3. **Google Calendar Integration**: Enable the Google Calendar API and authenticate OpenClaw to access your calendar.

For detailed steps, refer to the [Core Concepts](references/core_concepts.md) document.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[OpenClaw Tutorial](https://www.youtube.com/watch?v=dgbdyxe435E)** by codebasics