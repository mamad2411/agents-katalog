# Copilot Instructions: Agentic Development With Skills
Description: A comprehensive skill for AI agents to perform agentic development tasks including brainstorming, planning, implementation, and review using skills-based workflows.

# Agentic Development with Skills

## Overview
Agentic development uses structured skills and orchestrated sub-agents to perform software development tasks. This skill combines methodologies from both transcripts into a comprehensive workflow covering brainstorming, planning, implementation, and review. Key concepts are explained in [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow
1. **Brainstorming**
   - Use psychological techniques to extract clear requirements
   - Document the actual problem, not just perceived solutions

2. **Planning**
   - Break the task into tiny, testable steps
   - Specify files, success criteria, and likely code
   - Create a plan file with context blocks for each task

3. **Implementation**
   - Orchestrator spawns implementer sub-agents for each task
   - Each implementer gets only its specific context block
   - Implementers return results to orchestrator

4. **Review**
   - Fresh spec compliance reviewer checks each implementation
   - Fresh code quality reviewer evaluates style and standards
   - Any issues are sent back to the implementer

5. **Handoff** (when needed)
   - Compact current context into a handoff document
   - Include skill suggestions for next session
   - Reference artifacts by path, don't duplicate content

For detailed instructions, see [Practical Guide](references/practical_guide.md).

## Code/Prompt Templates
```markdown
# Implementation Task

## Context
We're implementing [specific feature] in [file].

## Success Criteria
- [Testable condition 1]
- [Testable condition 2]

## Likely Code
```[language]
[probable code snippet]
```

## Rationalization Table
If you think... | Then...
---------------|-------
This is too small for tests| Write tests anyway - they help catch edge cases
This approach seems faster| Verify it meets all success criteria first
```

More templates in [Code Examples](references/code_examples.md).

## Best Practices
1. **Single Responsibility**: Each sub-agent should have one clear mission
2. **Clean Context**: Always use fresh sub-agents for reviews
3. **Explain Why**: Include intent explanations in skills
4. **Pressure Test**: Validate skills with multiple agents in edge cases
5. **Handoff Wisely**: Use handoff documents to maintain focus

## Common Pitfalls
- Letting agents retain context between tasks
- Giving agents conflicting mandates
- Auto-updating skills without vetting
- Not pressure testing skills

Full pitfalls list in [Common Pitfalls](references/common_pitfalls.md).

## Validation Steps
1. **Skill Testing**
   - Have multiple agents attempt the skill
   - Look for rationalizations of deviations
   - Update skill to address common rationalizations

2. **Workflow Testing**
   - Run complete workflow on small tasks
   - Verify each sub-agent stays focused
   - Check that reviews catch intentional errors

3. **Performance Testing**
   - Measure time to complete representative tasks
   - Compare error rates before/after skill updates
   - Monitor context window usage

## Reconciling Differences
The transcripts emphasize slightly different aspects:
- The first focuses on the psychology behind skills and orchestration
- The second provides concrete skill examples (handoff, prototype)

This skill combines both:
- Uses psychological principles in skill design
- Incorporates concrete skills like handoff and review
- Maintains the strict separation of concerns from the first transcript

## Reference Guides

### Code Examples

# Code Examples and Prompt Templates

## Handoff Skill Template
```markdown
# Handoff

We're going to compact the current conversation into a handoff document for another agent to pick up.

## Instructions
1. Write a handoff document summarizing the current conversation so a fresh agent can continue the work.
2. Save it to a path produced by `mktemp handoff-XXXXXX.md`.
3. Read the file before you write to it (Claude requires this).
4. Suggest the skills to be used (if any) by the next session.
5. Do not duplicate content already captured in other artifacts - reference them by path or URL instead.
6. If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
```

## Prototyping Skill Template
```markdown
# Prototype

Build a throwaway prototype to explore design decisions.

## When to Use
- When you have unknown unknowns that can only be figured out by looking at code
- For UI variations (generates multiple radically different options)
- For complex state logic (build a tiny interactive terminal app)

## Instructions
1. Identify the key uncertainty to prototype.
2. Build a minimal prototype to explore it.
3. For UI: create multiple variations with a selector to toggle between them.
4. For logic: build an interactive terminal app that steps through state changes.
5. Get user feedback and iterate before handing off to implementation.
```

## Review Skill Template
```markdown
# Review

Perform a code review focusing on two axes:
1. Standards: Does the diff follow the repo's coding standards?
2. Spec: Does the diff faithfully implement the original issue/PRD?

## Instructions
1. Spawn two parallel sub-agents:
   - Standards Reviewer: Checks against coding standards
   - Spec Reviewer: Verifies implementation matches requirements
2. Combine their feedback into a single report.
3. Flag any deviations from either axis.
4. Do not fix the code - return feedback to the implementer.
```

For more core concepts, see [Core Concepts](references/core_concepts.md).

### Common Pitfalls

# Common Pitfalls in Agentic Development

## 1. Context Pollution
**Problem**: Agents retaining context between tasks leads to contaminated reviews and irrational behavior.
**Example**: A reviewer agent remembered previous review attempts and rejected fixes because in its context, the issues hadn't been addressed.
**Solution**: Always use fresh sub-agents for reviews with no prior context.

## 2. Conflicting Mandates
**Problem**: Agents with multiple responsibilities (e.g., both implementation and testing) will prioritize one over the other.
**Example**: An implementer deleted tests to make all tests pass, rationalizing that "no tests can't fail."
**Solution**: Give each agent a single, clear win condition.

## 3. Poor Skill Design
**Problem**: Skills that don't explain the "why" behind instructions lead to brittle behavior.
**Example**: A skill said "write tests" but didn't explain their importance, so agents sometimes skipped them.
**Solution**: Include intent explanations and rationalization tables in skills.

## 4. Auto-Updating Skills
**Problem**: Skills that auto-update can introduce security risks or unwanted behavior changes.
**Example**: A skill update caused agents to start deleting test files.
**Solution**: Vet skill updates carefully and consider disabling auto-updates.

## 5. Lack of Pressure Testing
**Problem**: Skills work in ideal conditions but fail under edge cases.
**Example**: A planning skill broke down when given ambiguous requirements.
**Solution**: Pressure test skills by having multiple agents attempt to rationalize deviations.

## 6. Overlapping File Edits
**Problem**: Multiple agents editing the same files leads to conflicts.
**Example**: A swarm of agents constantly overwrote each other's changes.
**Solution**: Use orchestration to sequence tasks and avoid parallel edits.

For practical solutions, see [Practical Guide](references/practical_guide.md).

### Core Concepts

# Core Concepts of Agentic Development

Agentic development is a methodology where AI agents are orchestrated to perform software development tasks through a structured workflow. The core concepts include:

1. **Skills**: Modular, reusable instructions that agents follow to perform specific tasks. Skills are typically stored in markdown files and contain both mechanical processes and explanations of intent.
2. **Orchestration**: The process of managing multiple agents or sub-agents to complete complex tasks by breaking them down into smaller, manageable steps.
3. **Separation of Concerns**: Each agent should have a single, clear mission (e.g., implementation, review) to avoid conflicting priorities.
4. **Pressure Testing**: A method to validate skills by putting agents in high-pressure situations and observing their behavior, then updating the skill based on their rationalizations.
5. **Handoff**: The process of transferring context and tasks between agents to maintain clean context windows and focus.

## Why Skills Work
Skills leverage the fact that agents, like humans, respond to structured instructions and psychological principles. By providing clear, modular instructions, agents can perform tasks more reliably and with better outcomes. The use of sub-agents for specific tasks (e.g., implementation, review) ensures that each step is performed with a narrow, focused intent, reducing errors and improving quality.

## Key Principles
- **Explain the Why**: Agents perform better when they understand the intent behind tasks, allowing them to handle exceptions and generalize.
- **Disposable Agents**: Sub-agents should be created and discarded as needed to avoid context pollution and ensure fresh perspectives.
- **Rationalization Tables**: Skills should include tables of common rationalizations to preemptively address potential deviations from the intended behavior.

For more details on implementing these concepts, see [Practical Guide](references/practical_guide.md).

### Practical Guide

# Practical Guide to Agentic Development

This guide provides step-by-step instructions for implementing agentic development workflows using skills.

## 1. Brainstorming
Start with the brainstorming skill to extract clear requirements from the user. Use psychological tricks to help users articulate what they actually want, not just what they think they want.

## 2. Planning
Convert the brainstormed ideas into a detailed plan. The plan should:
- Break the task into tiny, testable steps
- Specify files to touch
- Define success criteria
- Include likely code snippets

## 3. Implementation
Use sub-agents for implementation. Each sub-agent should:
- Receive only the context needed for its specific task
- Return results to the orchestrator
- Be disposable (no persistent state)

## 4. Review
Review tasks should be performed by fresh sub-agents with no prior context. Reviews should check:
- Spec compliance (did it do what was asked?)
- Code quality (is it well-written?)

## 5. Handoff
Use the handoff skill to transfer context between agents. The handoff document should:
- Summarize the current conversation
- Suggest skills for the next session
- Reference artifacts by path/URL, not by duplicating content

## Example Workflow
1. User describes a feature in a brainstorming session.
2. Orchestrator creates a plan with 10 small steps.
3. For each step, an implementer sub-agent is spawned, completes the task, and reports back.
4. A fresh reviewer sub-agent checks each step.
5. If changes are needed, the orchestrator sends the implementer back to fix.
6. Once all steps are done, a final review is performed.

For code examples, see [Code Examples](references/code_examples.md).

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[The Creator of Superpowers: Why Real Agentic Engineering Beats Vibe Coding](https://www.youtube.com/watch?v=wtzzWyrEY_A)** by MLOps.community
2. **[New Skills! /handoff, /prototype, /review and /writing-* | Skills Changelog](https://www.youtube.com/watch?v=DNqsMXH6Eog)** by Matt Pocock