# Copilot Instructions: Claude Co Work Mastery
Description: A comprehensive skill for mastering Claude Co-work, including setup, file management, persistent memory, connectors, skills creation, and scheduled tasks.

### Overview
Claude Co-work is a powerful AI tool that extends beyond the capabilities of Claude Chat by allowing direct interaction with local files, persistent memory, and integration with external tools. This skill will guide you through setting up Claude Co-work, managing files, leveraging persistent memory, connecting to external tools, creating custom skills, and setting up scheduled tasks.

### Step-by-Step Workflow
1. **Setup Claude Co-work**: Ensure the Co-work tab is selected and configure settings under the Co-work tab. Add instructions that apply to Co-work only.
2. **File Management**: Use Co-work to create, edit, and organize files directly on your computer. Ensure all files are within the Co-work Playground folder.
3. **Persistent Memory**: Leverage Co-work's ability to save memory to actual files on your computer. Use this feature to remember preferences and decisions across sessions.
4. **Connectors**: Connect Co-work to external tools like Gmail, Google Drive, and Notion. This allows Co-work to read from and work directly inside these tools.
5. **Skills Creation**: Create custom skills by teaching Co-work specific workflows. Use the skill creator by Anthropic skill to automate repetitive tasks.
6. **Scheduled Tasks**: Set up scheduled tasks to automate routine workflows, such as inbox triage.

### Code/Prompt Templates
```plaintext
Prompt Template for File Organization:
"I have 15 raw thumbnail photos in this folder. I need them organized into subfolders by topic with descriptive file names."

Prompt Template for Expense Report:
"Look, I need an expense report from the receipt photos in my receipts folder. Give me an Excel spreadsheet with a date, vendor, category, amount, and a totals row. If anything's blurry or unclear, mark it verify."
```

### Best Practices
- **Setup**: Always start by configuring Co-work settings and adding necessary instructions.
- **File Management**: Keep all files within the Co-work Playground folder to avoid access issues.
- **Persistent Memory**: Regularly update memory files to ensure Co-work remembers important preferences and decisions.
- **Connectors**: Connect Co-work to all relevant external tools to maximize its capabilities.
- **Skills Creation**: Start with simple skills and gradually move to more complex workflows.
- **Scheduled Tasks**: Regularly review and update scheduled tasks to ensure they remain effective.

### Common Pitfalls
- **File Access Issues**: Ensure all files are within the Co-work Playground folder to avoid access problems.
- **Memory Overload**: Regularly clean up memory files to prevent Co-work from becoming overwhelmed.
- **Skill Complexity**: Start with simple skills to avoid errors and ensure smooth operation.
- **Task Reliability**: Regularly test scheduled tasks to ensure they run as expected.

### Validation and Testing
- **File Management**: Verify that files are correctly organized and accessible.
- **Persistent Memory**: Test Co-work's ability to recall preferences and decisions across sessions.
- **Connectors**: Ensure Co-work can read from and work directly inside connected tools.
- **Skills Creation**: Test custom skills to ensure they perform as expected.
- **Scheduled Tasks**: Regularly review the output of scheduled tasks to ensure accuracy and reliability.

### References
For more detailed information, refer to the following documents:
- [Core Concepts](references/core_concepts.md)
- [Practical Guide](references/practical_guide.md)
- [Code Examples](references/code_examples.md)
- [Common Pitfalls](references/common_pitfalls.md)

## Reference Guides

### Code Examples

# Code Examples
This document provides concrete code snippets and prompt templates for using Claude Co-work.

## Prompt Templates
```plaintext
Prompt Template for File Organization:
"I have 15 raw thumbnail photos in this folder. I need them organized into subfolders by topic with descriptive file names."

Prompt Template for Expense Report:
"Look, I need an expense report from the receipt photos in my receipts folder. Give me an Excel spreadsheet with a date, vendor, category, amount, and a totals row. If anything's blurry or unclear, mark it verify."

Prompt Template for PDF Breakdown:
"I have a massive PDF. I need it broken into separate files, one per chapter or major section with descriptive file names so I can find what I need at a glance."
```

## Skills Creation
```plaintext
Prompt Template for Clear and Concise Skill:
"Turn what you just did into a clear and concise skill. This skill should apply to any text. It should rewrite and provide a change log so I can see what changed."

Prompt Template for Weekly Report Skill:
"Combine these three team updates into one formatted weekly marketing update I can send to leadership. Lead with three top-line metrics across all teams, then give me three highlights and three lowlights. Keep it within 300 words."
```

## Scheduled Tasks
```plaintext
Prompt Template for Inbox Triage Task:
"Produce a report and draft replies for all my emails. Map them against my inbox zero rules and what you know about me to draft contextually relevant replies."
```

For more detailed practical guidance, refer to the [Practical Guide](references/practical_guide.md).

### Common Pitfalls

# Common Pitfalls
This document highlights common pitfalls when using Claude Co-work and provides strategies to avoid them.

## File Access Issues
**Pitfall**: Files outside the Co-work Playground folder may not be accessible.
**Solution**: Ensure all files are within the Co-work Playground folder.

## Memory Overload
**Pitfall**: Memory files can become cluttered, causing Co-work to become overwhelmed.
**Solution**: Regularly clean up memory files to keep them relevant and useful.

## Skill Complexity
**Pitfall**: Starting with complex skills can lead to errors and inefficiencies.
**Solution**: Begin with simple skills and gradually move to more complex workflows.

## Task Reliability
**Pitfall**: Scheduled tasks may not run as expected.
**Solution**: Regularly test scheduled tasks to ensure they perform reliably.

## Connector Issues
**Pitfall**: Connectors may not function properly if not set up correctly.
**Solution**: Ensure all connectors are properly configured and regularly tested.

For more detailed practical guidance, refer to the [Practical Guide](references/practical_guide.md).

### Core Concepts

# Core Concepts
Claude Co-work extends the capabilities of Claude Chat by allowing direct interaction with local files, persistent memory, and integration with external tools. This document covers the fundamental concepts of Claude Co-work, including its differences from Claude Chat, file management, persistent memory, connectors, skills creation, and scheduled tasks.

## Differences from Claude Chat
Claude Co-work differs from Claude Chat in several key ways:
1. **File Access**: Co-work can access local files, allowing it to handle more files with larger sizes.
2. **Context Window**: Co-work has a larger context window, enabling more extensive work before triggering the compacting conversation function.
3. **Output Delivery**: Co-work delivers ready-to-use files directly in your folder, unlike Chat which provides responses in a chat window.

## File Management
Co-work can create, edit, and organize files directly on your computer. This includes tasks like organizing photos, creating expense reports, and breaking down large PDFs.

## Persistent Memory
Co-work saves memory to actual files on your computer, allowing it to remember preferences and decisions across sessions. This feature is crucial for maintaining consistency in workflows.

## Connectors
Connectors enable Co-work to integrate with external tools like Gmail, Google Drive, and Notion. This allows Co-work to read from and work directly inside these tools.

## Skills Creation
Skills are custom workflows that Co-work can automate. By teaching Co-work specific tasks, you can create skills that save time and improve efficiency.

## Scheduled Tasks
Scheduled tasks automate routine workflows, such as inbox triage. Co-work's scheduled tasks are highly reliable and can be customized to fit your needs.

For more detailed examples and practical applications, refer to the [Practical Guide](references/practical_guide.md).

### Practical Guide

# Practical Guide
This document provides practical guidance on using Claude Co-work, including setup, file management, persistent memory, connectors, skills creation, and scheduled tasks.

## Setup
1. **Select Co-work Tab**: Ensure the Co-work tab is selected in the settings.
2. **Add Instructions**: Under the Co-work tab, add instructions that apply to Co-work only. These instructions act as guardrails to prevent Co-work from making unwanted changes.
3. **Enable Memory Features**: Enable both memory features under settings to leverage persistent memory.
4. **Create Playground Folder**: Create a new subfolder called Co-work Playground in your documents folder to contain all Co-work activities.

## File Management
1. **Organize Files**: Use Co-work to organize files into subfolders with descriptive file names.
2. **Create Expense Reports**: Generate expense reports from receipt photos, ensuring clarity and accuracy.
3. **Break Down PDFs**: Break down large PDFs into smaller, more manageable files.

## Persistent Memory
1. **Save Preferences**: Save preferences and decisions in memory files to ensure Co-work remembers them across sessions.
2. **Update Memory Files**: Regularly update memory files to keep Co-work's memory relevant and useful.

## Connectors
1. **Connect External Tools**: Connect Co-work to external tools like Gmail, Google Drive, and Notion.
2. **Read and Work**: Use Co-work to read from and work directly inside connected tools.

## Skills Creation
1. **Create Simple Skills**: Start with simple skills to get familiar with the process.
2. **Automate Workflows**: Teach Co-work specific workflows to automate repetitive tasks.

## Scheduled Tasks
1. **Set Up Tasks**: Set up scheduled tasks to automate routine workflows.
2. **Review Output**: Regularly review the output of scheduled tasks to ensure accuracy and reliability.

For more detailed code examples, refer to the [Code Examples](references/code_examples.md).

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Learn 80% of Claude Cowork in Under 20 Minutes](https://www.youtube.com/watch?v=z9rdrNrkvDY)** by Jeff Su