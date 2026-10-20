# Copilot Instructions: Claude Cowork System Setup
Description: A comprehensive skill for setting up and managing a Claude Cowork system, enabling persistent memory, context-aware responses, and efficient task management.

## Overview

The Claude Cowork system is a structured approach to leveraging AI for task management, persistent memory, and context-aware responses. By organizing your workspace with markdown files (`claude.md`, `memory.md`, and `voice_principles.md`), you can create a system that remembers past interactions, maintains your tone of voice, and efficiently manages tasks. This skill will guide you through setting up this system, including creating the necessary files, organizing your workspace, and optimizing for low token usage.

For a deeper understanding of the core concepts, refer to [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow

1. **Create the Root Folder**: Start by creating a folder named `Co-work OS` in your documents.
2. **Download Starter Templates**: Download the `claude.md`, `memory.md`, and `voice_principles.md` templates provided in the transcript.
3. **Organize Files**: Place `claude.md` and `memory.md` in the root folder. Create a `00_resources` folder and move `voice_principles.md` into it.
4. **Set Up Obsidian**: Install Obsidian and open the `Co-work OS` folder as a vault to view the markdown files in a readable format.
5. **Configure `claude.md`**: Ensure `claude.md` includes instructions to read `memory.md` at the start of each session and to write to `memory.md` when told to remember something.
6. **Build Workstations**: Create workstation folders (e.g., `email HQ`, `personal finances`) each with their own `claude.md`, `memory.md`, and `resources` folder.
7. **Optimize Token Usage**: Keep the root `claude.md` file lean by pointing to other resource files only when necessary.

For detailed instructions and code snippets, refer to [Practical Guide](references/practical_guide.md).

## Code Snippets and Prompt Templates

### Prompt Template for Voice Principles
```markdown
Option 1: Gmail Connected
Paste this prompt into a new session within Co-work:
"Extract writing patterns from my last 30 sent emails to build my voice profile."

Option 2: No Gmail Connected
Paste this prompt into a new session within Co-work:
"Analyze these five writing samples to build my voice profile."
```

### Session Audit Prompt
```markdown
{forward slash} session audit
```

For more examples, refer to [Code Examples](references/code_examples.md).

## Best Practices and Common Pitfalls

### Best Practices
- **Keep Files Lean**: Avoid repeating rules in multiple files to reduce token usage.
- **Use Sonnet Model**: Default to the Sonnet model for most tasks to save costs.
- **Session Audits**: Regularly audit sessions to capture unsaved principles and preferences.

### Common Pitfalls
- **Overloading Root File**: Avoid adding too many rules to the root `claude.md` file, as it is loaded by default in every session.
- **Misclassification**: Correct any misclassifications (e.g., categorizing Canva as freelancer instead of software) to ensure accurate future classifications.

For more best practices and pitfalls, refer to [Common Pitfalls](references/common_pitfalls.md).

## Validation and Testing

1. **Test Memory**: Start a new session and ask Co-work about recent entries in `memory.md` to verify persistence.
2. **Check Voice Principles**: Review the `voice_principles.md` file to ensure it accurately reflects your tone of voice.
3. **Workstation Functionality**: Test workstation-specific tasks (e.g., drafting emails) to ensure rules are correctly applied.

## References

```json
[
  {
    "filename": "core_concepts.md",
    "content": "## Core Concepts\n\nThe Claude Cowork system revolves around three core concepts: persistent memory, context-aware responses, and efficient task management. Persistent memory is achieved through the `memory.md` file, which stores information between sessions. Context-aware responses are enabled by the `claude.md` file, which acts as the instruction manual for Co-work. Efficient task management is facilitated by organizing workstations, each with its own set of rules and resources.\n\n### Persistent Memory\nThe `memory.md` file is crucial for maintaining continuity between sessions. It contains sections for active projects and general memory entries. When you tell Co-work to remember something, it writes that information to `memory.md`, ensuring it can be recalled in future sessions.\n\n### Context-Aware Responses\nThe `claude.md` file governs how Co-work behaves. It includes instructions for reading `memory.md` at the start of each session and for routing tasks to the appropriate workstation. This ensures that Co-work always has the necessary context to provide relevant responses.\n\n### Efficient Task Management\nWorkstations are specialized folders that handle specific areas of your life (e.g., email, personal finances). Each workstation has its own `claude.md`, `memory.md`, and `resources` folder, allowing for task-specific rules and resources. This modular approach keeps the system organized and efficient."
  },
  {
    "filename": "practical_guide.md",
    "content": "## Practical Guide\n\n### Setting Up the Root Folder\n1. Create a folder named `Co-work OS` in your documents.\n2. Download the `claude.md`, `memory.md`, and `voice_principles.md` templates.\n3. Place `claude.md` and `memory.md` in the root folder.\n4. Create a `00_resources` folder and move `voice_principles.md` into it.\n\n### Configuring `claude.md`\n1. Open `claude.md` in a text editor.\n2. Ensure it includes the following instructions:\n   - At the start of every session, read `memory.md` before responding.\n   - When told to remember something, write the information to `memory.md`.\n3. Add a routing map section to direct tasks to the appropriate workstation.\n\n### Building Workstations\n1. Create a new folder for each workstation (e.g., `email HQ`, `personal finances`).\n2. Inside each workstation folder, create `claude.md`, `memory.md`, and `resources` folders.\n3. Configure the `claude.md` file in each workstation to include task-specific rules.\n\n### Optimizing Token Usage\n1. Keep the root `claude.md` file lean by pointing to other resource files only when necessary.\n2. Avoid repeating rules in multiple files.\n3. Default to the Sonnet model for most tasks to save costs."
  },
  {
    "filename": "code_examples.md",
    "content": "## Code Examples\n\n### Prompt Template for Voice Principles\n```markdown\nOption 1: Gmail Connected\nPaste this prompt into a new session within Co-work:\n\"Extract writing patterns from my last 30 sent emails to build my voice profile.\"\n\nOption 2: No Gmail Connected\nPaste this prompt into a new session within Co-work:\n\"Analyze these five writing samples to build my voice profile.\"\n```\n\n### Session Audit Prompt\n```markdown\n{forward slash} session audit\n```\n\n### Email HQ Prompt\n```markdown\nSearch my Gmail sent folder for the last 4 weeks of emails, then analyze and extract only email-specific patterns that aren't covered by my root voice principles.\n```\n\n### Personal Finances Prompt\n```markdown\nRead every transaction across my statements, break down the spending by category, and build a master spending tracker spreadsheet.\n```"
  },
  {
    "filename": "common_pitfalls.md",
    "content": "## Common Pitfalls\n\n### Overloading the Root File\nOne common mistake is adding too many rules to the root `claude.md` file. Since this file is loaded by default in every session, keeping it lean is crucial to avoid unnecessary token usage. Instead, point to other resource files only when the situation calls for it.\n\n### Misclassification\nAnother pitfall is misclassifying transactions or tasks. For example, categorizing Canva as freelancer instead of software can lead to inaccurate spending trackers. Correcting these misclassifications ensures accurate future classifications.\n\n### Repeating Rules\nAvoid repeating the same rule in multiple files. For example, if your root `voice_principles.md` file includes rules like 'no corporate jargon,' do not restate those rules in workstation-specific `claude.md` files. Instead, focus on task-specific preferences.\n\n### Ignoring Session Audits\nFailing to regularly audit sessions can result in unsaved principles and preferences. Use the `{forward slash} session audit` prompt to scan the conversation and capture any unsaved information."
  }
]


## Reference Guides

### Code Examples

## Code Examples

### Prompt Template for Voice Principles
```markdown
Option 1: Gmail Connected
Paste this prompt into a new session within Co-work:
"Extract writing patterns from my last 30 sent emails to build my voice profile."

Option 2: No Gmail Connected
Paste this prompt into a new session within Co-work:
"Analyze these five writing samples to build my voice profile."
```

### Session Audit Prompt
```markdown
{forward slash} session audit
```

### Email HQ Prompt
```markdown
Search my Gmail sent folder for the last 4 weeks of emails, then analyze and extract only email-specific patterns that aren't covered by my root voice principles.
```

### Personal Finances Prompt
```markdown
Read every transaction across my statements, break down the spending by category, and build a master spending tracker spreadsheet.
```

### Common Pitfalls

## Common Pitfalls

### Overloading the Root File
One common mistake is adding too many rules to the root `claude.md` file. Since this file is loaded by default in every session, keeping it lean is crucial to avoid unnecessary token usage. Instead, point to other resource files only when the situation calls for it.

### Misclassification
Another pitfall is misclassifying transactions or tasks. For example, categorizing Canva as freelancer instead of software can lead to inaccurate spending trackers. Correcting these misclassifications ensures accurate future classifications.

### Repeating Rules
Avoid repeating the same rule in multiple files. For example, if your root `voice_principles.md` file includes rules like 'no corporate jargon,' do not restate those rules in workstation-specific `claude.md` files. Instead, focus on task-specific preferences.

### Ignoring Session Audits
Failing to regularly audit sessions can result in unsaved principles and preferences. Use the `{forward slash} session audit` prompt to scan the conversation and capture any unsaved information.

### Core Concepts

## Core Concepts

The Claude Cowork system revolves around three core concepts: persistent memory, context-aware responses, and efficient task management. Persistent memory is achieved through the `memory.md` file, which stores information between sessions. Context-aware responses are enabled by the `claude.md` file, which acts as the instruction manual for Co-work. Efficient task management is facilitated by organizing workstations, each with its own set of rules and resources.

### Persistent Memory
The `memory.md` file is crucial for maintaining continuity between sessions. It contains sections for active projects and general memory entries. When you tell Co-work to remember something, it writes that information to `memory.md`, ensuring it can be recalled in future sessions.

### Context-Aware Responses
The `claude.md` file governs how Co-work behaves. It includes instructions for reading `memory.md` at the start of each session and for routing tasks to the appropriate workstation. This ensures that Co-work always has the necessary context to provide relevant responses.

### Efficient Task Management
Workstations are specialized folders that handle specific areas of your life (e.g., email, personal finances). Each workstation has its own `claude.md`, `memory.md`, and `resources` folder, allowing for task-specific rules and resources. This modular approach keeps the system organized and efficient.

### Practical Guide

## Practical Guide

### Setting Up the Root Folder
1. Create a folder named `Co-work OS` in your documents.
2. Download the `claude.md`, `memory.md`, and `voice_principles.md` templates.
3. Place `claude.md` and `memory.md` in the root folder.
4. Create a `00_resources` folder and move `voice_principles.md` into it.

### Configuring `claude.md`
1. Open `claude.md` in a text editor.
2. Ensure it includes the following instructions:
   - At the start of every session, read `memory.md` before responding.
   - When told to remember something, write the information to `memory.md`.
3. Add a routing map section to direct tasks to the appropriate workstation.

### Building Workstations
1. Create a new folder for each workstation (e.g., `email HQ`, `personal finances`).
2. Inside each workstation folder, create `claude.md`, `memory.md`, and `resources` folders.
3. Configure the `claude.md` file in each workstation to include task-specific rules.

### Optimizing Token Usage
1. Keep the root `claude.md` file lean by pointing to other resource files only when necessary.
2. Avoid repeating rules in multiple files.
3. Default to the Sonnet model for most tasks to save costs.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[My Simple Claude Cowork System (for normal people)](https://www.youtube.com/watch?v=0_dSWLOHKng)** by Jeff Su