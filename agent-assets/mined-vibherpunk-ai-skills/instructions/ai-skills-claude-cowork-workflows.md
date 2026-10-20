# Copilot Instructions: Claude Cowork Workflows
Description: A comprehensive skill for setting up and optimizing Claude Cowork workflows, including file access, projects, connectors, skills development, and testing methodologies.

# Claude Cowork Workflows Skill

## Overview
This skill enables you to implement and optimize Claude Cowork workflows for business automation. It covers [core concepts](references/core_concepts.md), [practical setup](references/practical_guide.md), and [skill development](references/skill_development.md) methodologies.

## Step-by-Step Workflow

1. **Initial Setup**
   - Ensure Claude Pro/Enterprise account
   - Install Claude Desktop app
   - Navigate to Co-work tab

2. **Configure File Access**
   - Select relevant folder for your project
   - Organize context documents (strategies, past work, templates)
   - Verify Claude can read/write files

3. **Create Projects**
   - Follow the [project setup guide](references/practical_guide.md)
   - Establish project-specific memory
   - Set default instructions and rules

4. **Implement Connectors**
   - Prioritize native integrations
   - For missing connectors:
     - Search for MCP servers
     - Consider building custom MCP
     - Use browser/computer control as last resort

5. **Develop Skills**
   - Use the [skill development framework](references/skill_development.md)
   - Start with simple skills
   - Gradually add reference files and complexity

6. **Test and Optimize**
   - Run initial evaluations
   - Focus optimization on one metric at a time
   - Implement AB testing for mature skills

## Best Practices
- **Context Management**: Always provide relevant reference files
- **Human-in-the-loop**: Identify critical decision points
- **Iterative Development**: Skills improve with use and feedback
- **Connector Hierarchy**: Always prefer native > MCP > browser > computer

## Common Pitfalls
1. **Overloading Context**
   - Symptom: Slow performance, high token usage
   - Fix: Use progressive disclosure in skills

2. **Inefficient Connectors**
   - Symptom: Slow responses, errors in tool usage
   - Fix: Always check for MCP servers first

3. **Vague Skill Instructions**
   - Symptom: Inconsistent outputs
   - Fix: Use the [structured prompt template](references/skill_development.md)

4. **Skipping Testing**
   - Symptom: Unreliable performance
   - Fix: Implement regular evals and AB tests

## Validation Steps
1. **Functional Testing**
   - Verify all process steps execute correctly
   - Check reference file usage

2. **Quality Evaluation**
   - Assess outputs against criteria
   - Gather human feedback

3. **Performance Benchmarking**
   - Measure speed and token usage
   - Compare against baseline

4. **Iterative Improvement**
   - Implement feedback loops
   - Document skill versions

## Implementation Example
```
// Sample skill creation prompt
Create a skill according to the following guidelines:

Name: Newsletter Writer
Trigger: When user requests newsletter creation

Goal: Transform content into polished newsletter following brand voice

Connectors: Google Docs, Mailchimp MCP

Reference Files:
- brand_voice.md: Tone and style guidelines
- newsletter_examples.docx: Past successful newsletters

Process:
1. Analyze input content
2. Suggest 3 angles using QA box
3. Draft newsletter following brand_voice.md
4. Format in Google Docs template
5. Send draft for approval

Rules:
- Must reference brand_voice.md for style
- Include at least one personal story
- Keep between 800-1200 words
```

For complete implementation details, consult the [reference documents](references/core_concepts.md).

## Reference Guides

### Core Concepts

# Core Concepts of Claude Cowork

## File Access
Claude Cowork allows direct access to folders on your computer, enabling persistent context for your projects. This means:
- Claude can read, create, edit, and update files directly in your designated folders
- No more manual copying and pasting of context documents
- Changes made by Claude are saved directly to your filesystem

Example: When working on YouTube content, you can give Claude access to a folder containing your YouTube strategy, past transcripts, and ICP documents. This provides automatic context for tasks like ideation, scripting, and research.

## Projects
Projects in Claude Cowork are containers for related tasks with shared context and memory. Each project can:
- Be connected to a specific folder
- Maintain project-specific memory (like tone of voice rules)
- Organize all related chats in one place
- Include scheduled tasks

Projects differ from standard chats by providing persistent, organized context that carries across multiple sessions.

## Connectors
Connectors enable Claude to interact with external software and services. There are several types:
1. Native connectors (built-in integrations)
2. MCP servers (bundled API calls for specific tools)
3. Browser access (less efficient fallback option)
4. Computer control (vision-based, token-heavy)

The hierarchy of preference is: native connectors > MCP servers > browser > computer control.

## Skills
Skills are instruction sets that teach Claude how to perform specific processes. They consist of:
- A skill.md file (core instructions)
- Optional reference files (context, examples, style guides)
- Optional code scripts (for API calls or functions)

Skills use progressive disclosure to manage context, only loading relevant parts when needed. This allows a single agent to access thousands of specialized skills.

## Testing and Optimization
Claude includes tools for skill evaluation and improvement:
- Eval Viewer agents for analyzing skill performance
- Benchmarking scripts
- AB testing capabilities

These tools help optimize skills for specific criteria like speed, token usage, or output quality.

### Practical Guide

# Practical Guide to Claude Cowork Implementation

## Setting Up Projects
1. Click "Create New Project" in the sidebar
2. Choose setup method:
   - From scratch (manual context)
   - Import from old Claude chat project
   - Use existing folder (recommended)
3. For folder-based projects:
   - Select the relevant folder on your computer
   - Name your project
   - Add instructions for Claude (role, scope, file usage)
   - Specify important context files
   - Set rules for asset creation/saving

Example YouTube project setup:
```
You are my YouTube assistant. Help with YouTube-related tasks including:
- Ideation
- Packaging
- Intro writing
- Script assistance
- Presentations

You have access to:
- Past YouTube transcripts (for tone/style)
- YouTube strategy doc
- ICP document

Rules:
- Save all created assets directly to the folder
- Mimic my tone from transcripts when writing scripts
```

## Working with Connectors
### For Native Integrations:
1. Go to Customize > Connectors
2. Browse available connectors
3. Click to connect and authenticate

### For MCP Servers:
1. Search "[Tool Name] MCP server" in Google
2. Follow documentation for setup instructions
3. Two setup methods:
   - Add remote server URL via "Add Custom Connector"
   - Edit config JSON file (Settings > Developer > Edit Config)

### When No MCP Exists:
1. Use the MCP builder skill:
   ```
   Claude, use the MCP builder skill to create an MCP server for [Tool Name]
   ```
2. Follow generated instructions to install

## Browser vs. Computer Control
Only use browser/computer control when:
- No connector or MCP exists
- You need one-time access
- Working with local software with specific workflows

Best Practice: Always prefer native connectors or MCP servers for efficiency.

### Skill Development

# Comprehensive Skill Development Guide

## Skill Components
Every skill should consider including:
1. skill.md - Core instruction file with:
   - Process steps
   - Human-in-the-loop points
   - Reference file usage instructions
   - Expected outputs
   - Rules

2. Reference Files (optional but recommended):
   - Text files (style guides, examples, ICP)
   - Assets (images, presentations for examples)
   - Code scripts (for API calls or functions)

## Building Process
1. Define the ideal step-by-step process
2. Identify needed knowledge sources
3. Determine required tools/connectors
4. Prepare good output examples

## Prompt Template for Skill Creation
```
Create a skill according to the following guidelines:

Name: [Skill Name]
Trigger: [When should the skill activate?]

Goal: [Clear objective for the skill]

Connectors: [List of required connectors/APIs/MCPs]

Reference Files:
- [File 1]: [Purpose]
- [File 2]: [Purpose]

Process:
1. [Step 1 description]
   - Human in the loop: [Yes/No]
   - Input: [What's needed]
   - Output: [Expected result]
2. [Step 2 description]
   ...

Rules:
- [Rule 1: Potential failure point to avoid]
- [Rule 2: Reference file usage requirement]

Progressive Updates:
- Automatically update rules when users specify "don't do X"
- Save approved outputs as good examples
```

## Testing and Optimization
### Evaluation Framework
1. Define optimization focus (one primary metric)
2. Set evaluation criteria (3-5 specific measures)
3. Specify test parameters:
   - Number of variations
   - Input consistency

Example test prompt:
```
Run a new test to optimize for [specific metric].

Criteria:
1. [Criterion 1]
2. [Criterion 2]
3. [Criterion 3]

Parameters:
- Use [specific input] for all tests
- Run [number] variations
- Focus on [specific aspect]
```

### AB Testing
Use for:
- Comparing skill versions
- Optimizing existing skills
- Testing against new model versions

AB Test Prompt:
```
Run an AB test on [Skill Name] to optimize for [metric].

Constraints:
- Must maintain [critical feature]
- Cannot compromise [important aspect]

Use [specific input] for testing.
```

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[CLAUDE COWORK FULL COURSE (2+ Hours)](https://www.youtube.com/watch?v=2HyBA-wkWsA)** by AI Experts