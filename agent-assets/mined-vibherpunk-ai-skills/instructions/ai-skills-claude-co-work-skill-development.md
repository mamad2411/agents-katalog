# Copilot Instructions: Claude Co Work Skill Development
Description: A comprehensive skill for developing, testing, and optimizing AI agent skills in Claude Co-Work, covering setup, project configuration, connector integration, and skill engineering best practices.

# Claude Co-Work Skill Development SOP

## Overview
This skill enables you to develop, test, and optimize AI agent skills within Claude Co-Work. It covers the full lifecycle from initial setup to advanced optimization techniques. Key concepts are explained in [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow

1. **Environment Setup**
   - Ensure Claude Pro/Enterprise account
   - Install desktop app
   - Enable co-work tab

2. **Project Configuration**
   - Create projects for different workflows
   - Connect relevant folders
   - Set project-specific instructions
   - Detailed steps in [Practical Guide](references/practical_guide.md)

3. **Connector Integration**
   - Prioritize native connectors
   - Search for MCP servers before using browser
   - Install custom MCP servers when needed (see [Code Examples](references/code_examples.md))

4. **Skill Development**
   - Define skill purpose and triggers
   - Gather reference files (style guides, examples, etc.)
   - Outline step-by-step process with human checkpoints
   - Add rules for edge cases

5. **Testing and Optimization**
   - Run initial functionality tests
   - Conduct focused evaluations on specific criteria
   - Perform AB tests between skill versions
   - Implement progressive updates

## Best Practices
- **Context Engineering**: Keep skill.md focused on process, offload details to reference files
- **Human-in-the-loop**: Use QA boxes for critical decisions
- **Variation Generation**: Request multiple options for human selection
- **Progressive Disclosure**: Structure skills to load context only when needed

## Common Pitfalls
1. **Overusing Browser**: Leads to token-heavy, expensive operations
   - Fix: Always check for MCP servers first

2. **Vague Skill Definitions**: Results in inconsistent outputs
   - Fix: Use precise process descriptions

3. **Testing Too Many Factors**: Makes optimization unclear
   - Fix: Focus on one improvement area per test

4. **Ignoring Reference Files**: Leads to generic outputs
   - Fix: Make file usage mandatory in skill rules

## Validation Steps
1. **Functional Testing**
   - Verify all process steps complete
   - Check output file generation

2. **Quality Evaluation**
   - Assess against style guides
   - Measure consistency with examples

3. **Performance Benchmarking**
   - Compare token usage
   - Time execution speed

4. **AB Testing**
   - Compare against baseline
   - Test different versions

Use the templates in [Code Examples](references/code_examples.md) for consistent testing.

## Reference Guides

### Code Examples

# Code and Prompt Examples for Claude Skills

## Skill Creation Prompt Template
```
Create a skill according to the following guidelines:

1. Name and Trigger:
- Name: [Skill Name]
- Trigger when: [description of when skill should activate]

2. Goal:
[Clear objective of what the skill accomplishes]

3. Connectors/APIs:
- [List required integrations]
- [Specify any special usage instructions]

4. Reference Files:
- [List required context files]
- [Explain their purpose]

5. Process Steps:
1. [First step with details]
2. [Second step with details]
...
[N. Final step and output]

6. Rules:
- [Edge case handling]
- [Quality controls]
- [Progressive improvement instructions]
```

## MCP Server Installation
For custom MCP servers:
1. Find documentation (search "[Tool] MCP server")
2. Either:
   - Add remote server URL via Connectors > +
   OR
   - Edit config file (Settings > Developer > Edit Config)
3. For config edits:
   - Paste JSON into Claude and ask for update
   - Insert new MCP configuration
   - Save and restart Claude

## Testing Prompt Example
```
Run an evaluation test for [Skill Name] with:
- Optimization focus: [specific aspect to improve]
- Test criteria:
  1. [Criterion 1]
  2. [Criterion 2]
  3. [Criterion 3]
- Test method:
  - Use [number] variations
  - Test on [specific input or range]
  - Compare against [baseline if applicable]
```

### Core Concepts

# Core Concepts of Claude Co-Work

## File Access and Projects
Claude Co-Work revolutionizes AI interaction by allowing persistent file access. When you grant Claude access to a folder, it can:
- Read all documents in that folder for context
- Create and edit files directly in the folder
- Maintain project-specific memory

Projects are organizational units that bundle:
- Connected folders
- Project-specific memory
- Organized chat history
- Scheduled tasks

Example: A YouTube project might include:
- A folder with transcripts, strategy docs, and ICP
- Memory rules about tone of voice
- Scheduled content generation tasks

## Connectors and Integration
Claude connects to external tools through:
1. Native connectors (pre-built integrations)
2. MCP servers (bundled API packages)
3. Browser access (fallback option)
4. Computer control (least efficient)

Best practices:
- Always prefer native connectors first
- Search for MCP servers before using browser
- Reserve computer control for special cases

## Skills Architecture
Skills are modular capabilities that include:
- skill.md (core process instructions)
- Reference files (context, examples, style guides)
- Code scripts (for API calls or functions)

Skills use progressive disclosure:
1. Only metadata (name/description) is in memory
2. skill.md loads when triggered
3. Reference files load only when needed

This allows one agent to access thousands of skills without context overload.

### Practical Guide

# Practical Guide to Building Claude Co-Work Skills

## Setting Up Projects
1. Create a new project from the sidebar
2. Choose between:
   - Starting from scratch
   - Importing from old Claude chat
   - Using an existing folder
3. For folder-based projects:
   - Select the relevant folder
   - Name the project
   - Add instructions for Claude
   - Specify context files
   - Set saving rules for generated assets

Example YouTube project setup:
```
You are my YouTube assistant. Help with:
- Video ideation
- Script writing
- Presentation creation

You have access to:
- Past YouTube transcripts
- YouTube strategy doc
- ICP document

Rules:
- Mimic my tone from transcripts
- Save all outputs to the folder
```

## Skill Development Process
1. Define the skill purpose and triggers
2. Gather necessary reference files
3. Outline the step-by-step process
4. Specify required connectors/APIs
5. Build human-in-the-loop checkpoints
6. Add rules and edge case handling

## Testing and Optimization
Use Skills 2.0 features for:
- Automated test case generation
- Performance benchmarking
- AB testing between skill versions

Key metrics to test:
- Output quality
- Style adherence
- Process completion
- Speed/token efficiency

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[CLAUDE COWORK FULL COURSE (2+ Hours)](https://www.youtube.com/watch?v=2HyBA-wkWsA)** by Ben AI