# Copilot Instructions: Handoff Skill
Description: Compact the current conversation into a handoff document for another agent to pick up, summarizing the conversation and suggesting next steps.

# Handoff Skill Documentation

## Overview
The Handoff Skill enables smooth transitions between AI agents by creating a temporary summary document. This is particularly useful when:
- The current context window is becoming too large
- A different type of agent would be better suited for the next phase
- You need to parallelize work across multiple agents

For core concepts, see [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow
1. **Initiate Handoff**: Trigger the skill with `/handoff` or `/handoff "focus description"` if you want to specify the next session's focus.
2. **Document Creation**: The agent will:
   - Summarize the current conversation
   - Capture the current state of work
   - Suggest next steps and recommended skills
   - Reference relevant artifacts
3. **File Handling**: The document is saved to a temporary location (see [Practical Guide](references/practical_guide.md) for details).
4. **Transfer**: The path to the document is provided for use in a new agent session.
5. **Continuation**: The new agent loads the handoff document and continues the work.

## Best Practices
1. **Content Selection**:
   - Focus on key decisions and current state
   - Avoid duplicating content available in other artifacts
   - Include enough context for effective continuation
2. **Skill Suggestions**:
   - Recommend skills that match the next phase of work
   - Consider the 'vibe' of the current session
3. **Temporary Nature**:
   - Remember these are transitional documents
   - Important information should be saved elsewhere

## Common Pitfalls
1. **Over-summarizing**: Losing important nuances in the handoff
2. **Under-summarizing**: Creating documents that are too verbose
3. **Missing References**: Forgetting to link to relevant artifacts
4. **Skill Mismatch**: Suggesting inappropriate skills for continuation

## Validation Steps
1. **Content Check**: Verify the document contains:
   - Clear summary
   - Current state
   - Next steps
   - Skill suggestions
   - Artifact references
2. **File Check**: Confirm the file exists at the specified path
3. **Continuation Test**: Start a new agent with the document and verify it can continue the work effectively

For complete code examples and templates, see [Code Examples](references/code_examples.md).

## Reference Guides

### Code Examples

# Code Examples and Templates

## Basic Handoff Command
```
/handoff
```
This creates a standard handoff document summarizing the current conversation.

## Focused Handoff with Arguments
```
/handoff "Continue with the prototype implementation focusing on the user authentication flow"
```
The argument becomes the focus description for the next agent.

## Handoff Document Structure Example
```markdown
# Handoff Document

## Conversation Summary
[Brief summary of key points from the conversation]

## Current State
[Description of where the work currently stands]

## Suggested Next Steps
1. [First recommended action]
2. [Second recommended action]
3. [Etc.]

## Recommended Skills
- /prototype
- /grill
- /implement

## Artifact References
- [path/to/relevant/file1]
- [path/to/relevant/file2]
```

## File Handling Pseudocode
```python
def create_handoff(content):
    temp_dir = get_temp_directory()
    file_path = os.path.join(temp_dir, 'mic_temp_t_handoff.md')
    
    # Claude requires reading before writing
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            existing_content = f.read()
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    return file_path
```

### Core Concepts

# Core Concepts of Handoff Skill

The Handoff Skill is designed to facilitate seamless transitions between AI agents by creating a temporary document that captures the essence of the current conversation. This document serves as a bridge, allowing a fresh agent to continue work without losing context.

Key concepts:
1. **Temporary Nature**: The handoff document is not meant for long-term storage. It exists in a temporary directory with a standardized naming convention (e.g., mic_temp_t_handoff).
2. **Context Preservation**: The document must capture not just the content, but also the 'vibe' and intent of the original conversation.
3. **Skill Suggestion**: The handoff should recommend which skills the next agent should use to continue the work effectively.
4. **Artifact Referencing**: Instead of duplicating content, the handoff should reference existing artifacts by path or URL.
5. **Argument Handling**: If the user provides arguments, these should be treated as focus areas for the next session and the document should be tailored accordingly.

Example Use Cases:
- Moving from a planning session to implementation
- Transitioning between different types of work (e.g., from design to coding)
- Creating sub-agent workflows where specialized agents handle specific tasks

### Practical Guide

# Practical Guide to Using Handoff Skill

## When to Use Handoff
1. **Context Window Management**: When you're approaching context window limits in a long-running session.
2. **Specialization Needs**: When a different type of agent would be better suited for the next phase of work.
3. **Parallel Workflows**: When you need to split work between multiple agents working simultaneously.

## Implementation Details
1. **File Handling**: The skill creates files in a temporary directory. Ensure your system has proper permissions for this location.
2. **Content Structure**: The handoff document should include:
   - Conversation summary
   - Current state of work
   - Suggested next steps
   - Recommended skills for continuation
   - References to any relevant artifacts
3. **Error Handling**: Some AI models (like Claude) require reading a file before writing to it. The skill includes this as a necessary step.

## Common Patterns
1. **Fire-and-Forget**: When you need to quickly spin up a new agent to handle a specific task without maintaining the original context.
2. **DIY Sub-Agent**: When you want to maintain control over a sub-process while giving it full context window capacity.

## Best Practices
- Keep handoff documents concise but comprehensive
- Clearly mark transitions between different phases of work
- Include enough context for the next agent to be effective, but avoid unnecessary duplication

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[New Skills! /handoff, /prototype, /review and /writing-* | Skills Changelog](https://www.youtube.com/watch?v=DNqsMXH6Eog)** by Matt Pocock