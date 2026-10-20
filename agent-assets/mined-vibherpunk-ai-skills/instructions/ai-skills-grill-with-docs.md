# Copilot Instructions: Grill With Docs
Description: A skill for AI-assisted development that combines the Grill Me technique with domain-driven design principles to establish and maintain a shared language between the developer and the AI. This skill leverages a context.md file to document shared language and an architectural decision record (ADR) to capture non-obvious decisions, ensuring concise and aligned communication.

# Grill with Docs Skill

## Overview

The Grill with Docs skill is designed to enhance AI-assisted development by establishing a shared language between the developer and the AI. This skill builds on the Grill Me technique, which involves the AI interviewing the developer to resolve ambiguities and dependencies. Grill with Docs extends this by incorporating domain-driven design principles, specifically the concept of ubiquitous language, to create a context.md file that documents the shared language used in the codebase. Additionally, it uses architectural decision records (ADRs) to capture non-obvious decisions that are hard to reverse.

## Step-by-Step Workflow

1. **Initialize the Session**: Start a grilling session with the AI, ensuring that the context.md file is present in the repository root.
2. **Define Shared Language**: During the session, the AI will challenge fuzzy language and ask for definitions of terms. Document these definitions in the context.md file.
3. **Capture Non-Obvious Decisions**: When encountering decisions that are hard to reverse, create an ADR to document the rationale and consequences.
4. **Update Context.md**: Continuously update the context.md file as new terms and definitions are agreed upon.
5. **Review and Refine**: Periodically review the context.md and ADRs to ensure they remain accurate and useful.

## Code Snippets and Prompt Templates

### Context.md Template
```markdown
# Context Documentation

## Entities
- **Course**: A structured series of lessons.
- **Lesson**: A single unit of instruction within a course.
- **Standalone Video**: A video not connected to a lesson or course.

## Relationships
- **Course** has many **Lessons**.
- **Standalone Video** can be associated with a **Pitch**.
```

### ADR Template
```markdown
# Architectural Decision Record

## Title
Use of Standalone Videos

## Status
Proposed

## Context
We need to define how standalone videos interact with pitches.

## Decision
Standalone videos can be associated with multiple pitches.

## Consequences
This allows for flexible video packaging but may complicate the UI.
```

## Best Practices and Common Pitfalls

### Best Practices
- **Consistent Language**: Ensure that all terms used in the codebase are defined in the context.md file.
- **Document Early**: Start documenting shared language and decisions early in the project to avoid confusion later.
- **Regular Reviews**: Periodically review and update the context.md and ADRs to keep them relevant.

### Common Pitfalls
- **Verbose Definitions**: Avoid overly verbose definitions that can confuse rather than clarify.
- **Undocumented Decisions**: Failing to document non-obvious decisions can lead to misunderstandings and technical debt.
- **Over-Documentation**: While documentation is important, avoid creating unnecessary documents that can clutter the repository.

## Validation and Testing Steps

1. **Check Context.md**: Verify that all terms used in the codebase are defined in the context.md file.
2. **Review ADRs**: Ensure that all non-obvious decisions are documented in ADRs.
3. **AI Alignment**: Test the AI's responses to ensure they align with the definitions in the context.md file.
4. **Code Consistency**: Check that variable names and file names in the codebase align with the shared language documented in context.md.

## References

- [Core Concepts](references/core_concepts.md)
- [Practical Guide](references/practical_guide.md)
- [Code Examples](references/code_examples.md)
- [Common Pitfalls](references/common_pitfalls.md)

## Reference Guides

### Code Examples

# Code Examples

## Context.md Example
```markdown
# Context Documentation

## Entities
- **Course**: A structured series of lessons.
- **Lesson**: A single unit of instruction within a course.
- **Standalone Video**: A video not connected to a lesson or course.

## Relationships
- **Course** has many **Lessons**.
- **Standalone Video** can be associated with a **Pitch**.
```

## ADR Example
```markdown
# Architectural Decision Record

## Title
Use of Standalone Videos

## Status
Proposed

## Context
We need to define how standalone videos interact with pitches.

## Decision
Standalone videos can be associated with multiple pitches.

## Consequences
This allows for flexible video packaging but may complicate the UI.
```

## Prompt Template
```markdown
# Grill with Docs Prompt

## Session Start
Start a grilling session to resolve ambiguities and dependencies in the code.

## Definitions
Define key terms and entities in the domain.

## Relationships
Document the relationships between entities.

## Decisions
Capture non-obvious decisions in ADRs.

## Updates
Continuously update the context.md and ADRs as new terms and decisions are made.
```

### Common Pitfalls

# Common Pitfalls

## Verbose Definitions
One common pitfall is creating overly verbose definitions in the context.md file. This can confuse rather than clarify. Ensure that definitions are clear and concise.

## Undocumented Decisions
Failing to document non-obvious decisions can lead to misunderstandings and technical debt. Always create ADRs for decisions that are hard to reverse.

## Over-Documentation
While documentation is important, avoid creating unnecessary documents that can clutter the repository. Focus on documenting key terms and decisions that have significant implications for the project.

## Inconsistent Language
Inconsistent language can lead to misunderstandings and misaligned code. Ensure that all terms used in the codebase are defined in the context.md file and used consistently.

## Lack of Reviews
Failing to regularly review and update the context.md and ADRs can lead to outdated and irrelevant documentation. Periodically review the documentation to ensure it remains accurate and useful.

### Core Concepts

# Core Concepts

## Domain-Driven Design (DDD)
Domain-Driven Design is a software development approach that emphasizes the importance of the domain model and the language used to describe it. The core idea is to create a shared language, known as ubiquitous language, that is used by developers, domain experts, and the codebase itself. This shared language ensures that everyone involved in the project has a clear understanding of the domain and its requirements.

## Ubiquitous Language
Ubiquitous language is a key concept in DDD. It refers to a shared language that is used consistently across the codebase, documentation, and communication between developers and domain experts. This language helps to reduce misunderstandings and ensures that everyone is on the same page.

## Architectural Decision Records (ADRs)
ADRs are documents that capture important architectural decisions made during the development process. They include the context of the decision, the decision itself, and the consequences of that decision. ADRs are particularly useful for documenting decisions that are hard to reverse and have significant implications for the project.

## Context.md
Context.md is a markdown file that documents the shared language used in a specific bounded context within the codebase. It includes definitions of key terms, relationships between entities, and any other relevant information that helps to clarify the domain model.

## Grill Me Technique
The Grill Me technique involves the AI interviewing the developer to resolve ambiguities and dependencies in the code. This technique helps to ensure that the developer and the AI have a shared understanding of the problem and its solution. Grill with Docs extends this technique by incorporating domain-driven design principles and documentation.

### Practical Guide

# Practical Guide

## Setting Up Grill with Docs
To set up Grill with Docs, follow these steps:

1. **Create Context.md**: Start by creating a context.md file in the root of your repository. This file will document the shared language used in your codebase.
2. **Define Key Terms**: Begin by defining the key terms and entities in your domain. Ensure that these definitions are clear and concise.
3. **Document Relationships**: Document the relationships between entities in your domain. This will help to clarify how different parts of the system interact.
4. **Create ADRs**: When making architectural decisions, create ADRs to document the context, decision, and consequences.

## Using Grill with Docs
When using Grill with Docs, follow these guidelines:

1. **Start a Grilling Session**: Begin a grilling session with the AI to resolve ambiguities and dependencies.
2. **Challenge Fuzzy Language**: During the session, challenge any fuzzy or ambiguous language. Ask the AI to clarify definitions and document them in context.md.
3. **Capture Decisions**: When encountering non-obvious decisions, create ADRs to document the rationale and consequences.
4. **Update Documentation**: Continuously update the context.md and ADRs as new terms and decisions are made.

## Maintaining Documentation
To maintain the documentation, follow these best practices:

1. **Regular Reviews**: Periodically review the context.md and ADRs to ensure they remain accurate and relevant.
2. **Consistent Language**: Ensure that all terms used in the codebase are defined in the context.md file.
3. **Avoid Over-Documentation**: While documentation is important, avoid creating unnecessary documents that can clutter the repository.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[I stopped using /grill-me for coding. Here’s what I use instead:](https://www.youtube.com/watch?v=6BB6exR8Zd8)** by Matt Pocock