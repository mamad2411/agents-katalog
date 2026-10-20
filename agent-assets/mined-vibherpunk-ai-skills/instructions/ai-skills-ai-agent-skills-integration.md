# Copilot Instructions: Ai Agent Skills Integration
Description: A comprehensive skill for integrating and utilizing various AI agent skills and plugins to enhance productivity, design, and research capabilities.

# AI Agent Skills Integration

## Overview
This skill enables AI agents to integrate and utilize a variety of pre-built skills and plugins to enhance their capabilities. These skills range from design and research to code review and animation generation. The core concept revolves around reusable instruction files (skills) and bundled functionalities (plugins) that provide consistent, repeatable behaviors.

For a deeper dive into the core concepts, see [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow
1. **Identify the Skill/Plugin**: Determine the functionality you need (e.g., design, research, code review).
2. **Install the Skill/Plugin**: Use the GitHub URL to install the skill/plugin in your AI harness (e.g., CodeX, Claude Code).
   ```
   install this for me, please <GitHub_URL>
   ```
3. **Activate the Skill**: Use the appropriate command to activate the skill (e.g., `/graphify`, `/understand`).
4. **Provide Input**: Give the necessary input or prompt to the skill (e.g., a paragraph to improve, a codebase to review).
5. **Review Output**: Analyze the output and iterate if necessary.

For detailed installation and usage examples, refer to [Practical Guide](references/practical_guide.md).

## Code/Prompt Templates
### Installing a Skill
```
install this for me, please https://github.com/garytan/gstack
```
### Using the Stop Slop Skill
```
use the Stop Slop skill to improve this paragraph: <paste_paragraph_here>
```
### Using the Graphify Skill
```
/graphify .
```

For more code examples, see [Code Examples](references/code_examples.md).

## Best Practices
- **Start Simple**: Begin with basic skills like Stop Slop before moving to complex ones like Graphify.
- **Validate Outputs**: Always review the outputs for accuracy and relevance.
- **Combine Skills**: Some skills work better when combined (e.g., front-end design and taste skills).

## Common Pitfalls
- **Overloading Tokens**: Complex skills like Graphify can be token-heavy. Monitor usage.
- **Skill Conflicts**: Combining incompatible skills can lead to suboptimal results (e.g., mixing design skills without clear objectives).

## Validation and Testing
1. **Test in Isolation**: Use each skill individually to understand its capabilities.
2. **Compare Outputs**: Run the same prompt with different skills to compare results.
3. **Iterate**: Refine prompts and inputs based on initial outputs.

For a comprehensive list of pitfalls and how to avoid them, see [Common Pitfalls](references/common_pitfalls.md).

## Reconcile Differences
- **Design Skills**: The front-end design skill (Anthropic) and taste skill (Leon XLNX) serve similar purposes but produce different outputs. Test both to determine which suits your needs.
- **Animation Skills**: Remotion and Hyperframes both generate animations but with varying quality. Hyperframes generally produces more polished results.


## Reference Guides

### Code Examples

# Code Examples

## Installing a Skill
```
install this for me, please https://github.com/garytan/gstack
```

## Using the Stop Slop Skill
```
use the Stop Slop skill to improve this paragraph: Humanoid robots are designed to mimic human movements and interactions. They are used in various fields, including healthcare, entertainment, and manufacturing.
```

## Using the Graphify Skill
```
/graphify .
```

## Using the Front-End Design Skill
```
use the front-end design skill to redesign this homepage: <paste_current_design>
```

## Using the Hyperframes Skill
```
use the Hyperframes skill to create an animation of a text conversation on an iPhone: <paste_dialogue>
```

For best practices and pitfalls, see [Common Pitfalls](references/common_pitfalls.md).

### Common Pitfalls

# Common Pitfalls

## Overloading Tokens
Complex skills like Graphify can consume a significant number of tokens, leading to high costs and slower performance. Always monitor token usage and optimize queries.

## Skill Conflicts
Combining incompatible skills can result in suboptimal outputs. For example, using both the front-end design and taste skills without clear objectives may produce conflicting designs.

## Installation Issues
Some skills may not be available in all AI harnesses. For instance, G Stack is not listed in the CodeX marketplace and must be installed manually via GitHub.

## Output Validation
Always validate the outputs of skills. For example, the Stop Slop skill may not always remove all AI-isms, requiring manual review.

## Design Subjectivity
Design skills like front-end design and taste produce subjective results. Test multiple variations to find the most suitable design.

For more on core concepts, see [Core Concepts](references/core_concepts.md).

### Core Concepts

# Core Concepts

## What are AI Agent Skills?
AI agent skills are reusable instruction files, typically written as detailed prompts in a `skill.md` file. These files are designed to provide consistent results when called upon by an AI agent. They may also include additional references, scripts, examples, or assets to enhance functionality.

## What are Plugins?
Plugins are bundles that package multiple skills, agents, hooks, MCP servers, commands, or other configurations. They allow users to install a comprehensive set of functionalities without manually copying individual components.

## Key Benefits
- **Consistency**: Skills provide repeatable behaviors, ensuring consistent outputs.
- **Efficiency**: Plugins bundle related functionalities, saving setup time.
- **Enhanced Capabilities**: Skills and plugins extend the native capabilities of AI agents.

## Examples
- **G Stack**: A bundle of 23 specialists and 8 power tools for virtual engineering teams.
- **Graphify**: Turns codebases and docs into queryable knowledge graphs.
- **Stop Slop**: Removes AI-isms from written content.

For practical applications, see [Practical Guide](references/practical_guide.md).

### Practical Guide

# Practical Guide

## Installation
1. **Locate the Skill/Plugin**: Find the GitHub repository for the skill/plugin you want to install.
2. **Install in AI Harness**: Use the command `install this for me, please <GitHub_URL>` in your AI harness (e.g., CodeX, Claude Code).
3. **Verify Installation**: Check the plugins/skills section to ensure the skill/plugin is installed.

## Usage
### G Stack
1. **Activate**: Use `/gstack office hours` to start a session.
2. **Provide Input**: Describe your project or idea.
3. **Review Output**: Analyze the stress test results or code reviews.

### Graphify
1. **Activate**: Use `/graphify .` in your project folder.
2. **Select Components**: Choose which parts of your project to graphify (e.g., wiki, journal).
3. **Query the Graph**: Ask questions like "What are the biggest recurring themes in my notes?"

### Stop Slop
1. **Activate**: Use `use the Stop Slop skill to improve this paragraph: <paste_paragraph_here>`.
2. **Review Output**: Compare the improved paragraph with the original.

For code snippets, see [Code Examples](references/code_examples.md).

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[9 Free AI Skills That Feel Like Cheat Codes](https://www.youtube.com/watch?v=STH929HARLo)** by Matt Wolfe