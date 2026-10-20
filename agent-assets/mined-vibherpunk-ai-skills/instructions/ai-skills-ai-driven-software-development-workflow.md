# Copilot Instructions: Ai Driven Software Development Workflow
Description: A comprehensive skill for AI agents to assist in software development workflows, including planning, specification, implementation, and code review.

## Overview
This skill guides AI agents through a structured software development workflow, from initial planning to final implementation and code review. The workflow includes steps for creating specifications, breaking down tasks into tickets, implementing features, and reviewing code for quality and adherence to standards.

## Step-by-Step Workflow
1. **Grill the User**: Start by grilling the user to gather detailed requirements. Use the `grill_me` skill to ask one question at a time and ensure a shared understanding before proceeding.
2. **Create Specifications**: Convert the gathered requirements into a detailed specification using the `to_spec` skill. This document should outline the technical and non-technical aspects of the project.
3. **Break Down Tasks**: Use the `to_tickets` skill to break down the specification into individual tickets. Each ticket should represent a manageable task that can be completed in a single agent session.
4. **Implement Features**: Implement each ticket using the `implement` skill. Follow Test-Driven Development (TDD) practices where possible and run type checking and tests regularly.
5. **Code Review**: Review the implemented code using the `code_review` skill. Check for adherence to coding standards and ensure the code faithfully implements the originating specification.
6. **Commit Work**: Once the code review is complete, commit the work to the current branch.

## Code Snippets
```javascript
// Example of using the implement skill
const implementSkill = require('skills/implement');
implementSkill.execute({
  spec: 'path/to/spec.md',
  ticket: 'path/to/ticket.md',
  tdd: true,
  typeChecking: true,
  testSuite: true
});
```

## Best Practices
- **Ask One Question at a Time**: Avoid overwhelming the user with multiple questions simultaneously.
- **Use TDD**: Implement features using Test-Driven Development to ensure code quality.
- **Regular Type Checking**: Run type checking regularly to catch errors early.
- **Full Test Suite**: Run the full test suite at the end of the implementation to ensure all tests pass.

## Common Pitfalls
- **Multiple Questions**: Asking multiple questions at once can confuse the user and lead to incomplete or incorrect requirements.
- **Skipping Code Review**: Skipping the code review step can result in code that does not adhere to standards or fully implement the specification.
- **Ignoring TDD**: Not using TDD can lead to poorly tested code and increased technical debt.

## Validation and Testing
- **Shared Understanding**: Ensure the user confirms a shared understanding before proceeding with implementation.
- **Code Standards**: Verify that the code adheres to the repository's documented coding standards.
- **Specification Adherence**: Check that the code faithfully implements the originating specification.

For more detailed information, refer to the following documents:
- [Core Concepts](references/core_concepts.md)
- [Practical Guide](references/practical_guide.md)
- [Code Examples](references/code_examples.md)
- [Common Pitfalls](references/common_pitfalls.md)

## Reference Guides

### Code Examples

# Code Examples

## Overview
This document provides code examples for implementing the AI-driven software development workflow. These examples illustrate how to use the various skills in practice.

## Example: Using the Implement Skill
```javascript
// Example of using the implement skill
const implementSkill = require('skills/implement');
implementSkill.execute({
  spec: 'path/to/spec.md',
  ticket: 'path/to/ticket.md',
  tdd: true,
  typeChecking: true,
  testSuite: true
});
```

## Example: Using the Code Review Skill
```javascript
// Example of using the code review skill
const codeReviewSkill = require('skills/code_review');
codeReviewSkill.execute({
  code: 'path/to/code.js',
  standards: 'path/to/coding_standards.md',
  spec: 'path/to/spec.md'
});
```

## Example: Using the Grill Me Skill
```javascript
// Example of using the grill me skill
const grillMeSkill = require('skills/grill_me');
grillMeSkill.execute({
  questions: [
    'What is the primary goal of this project?',
    'What are the key features you want to implement?',
    'Are there any specific technologies you want to use?'
  ],
  confirmUnderstanding: true
});
```

## Best Practices
- **Ask One Question at a Time**: Avoid overwhelming the user with multiple questions simultaneously.
- **Use TDD**: Implement features using Test-Driven Development to ensure code quality.
- **Regular Type Checking**: Run type checking regularly to catch errors early.
- **Full Test Suite**: Run the full test suite at the end of the implementation to ensure all tests pass.

## Common Pitfalls
- **Multiple Questions**: Asking multiple questions at once can confuse the user and lead to incomplete or incorrect requirements.
- **Skipping Code Review**: Skipping the code review step can result in code that does not adhere to standards or fully implement the specification.
- **Ignoring TDD**: Not using TDD can lead to poorly tested code and increased technical debt.

## Validation and Testing
- **Shared Understanding**: Ensure the user confirms a shared understanding before proceeding with implementation.
- **Code Standards**: Verify that the code adheres to the repository's documented coding standards.
- **Specification Adherence**: Check that the code faithfully implements the originating specification.

### Common Pitfalls

# Common Pitfalls

## Overview
This document outlines common pitfalls encountered when using the AI-driven software development workflow. Understanding these pitfalls can help you avoid them and ensure a smoother development process.

## Common Pitfalls

### Multiple Questions
Asking multiple questions at once can confuse the user and lead to incomplete or incorrect requirements. Always ask one question at a time to ensure clarity and completeness.

### Skipping Code Review
Skipping the code review step can result in code that does not adhere to standards or fully implement the specification. Always perform a thorough code review to ensure quality and adherence.

### Ignoring TDD
Not using Test-Driven Development (TDD) can lead to poorly tested code and increased technical debt. Always follow TDD practices to ensure high-quality, well-tested code.

### Overloading Implementation
Overloading the implementation phase with too many tasks can lead to errors and inefficiencies. Break down tasks into manageable tickets and implement them one at a time.

### Ignoring Type Checking
Ignoring type checking can result in undetected errors and bugs. Run type checking regularly to catch errors early and ensure code quality.

### Skipping Full Test Suite
Skipping the full test suite can result in untested code and potential bugs. Always run the full test suite at the end of the implementation to ensure all tests pass.

## Best Practices
- **Ask One Question at a Time**: Avoid overwhelming the user with multiple questions simultaneously.
- **Use TDD**: Implement features using Test-Driven Development to ensure code quality.
- **Regular Type Checking**: Run type checking regularly to catch errors early.
- **Full Test Suite**: Run the full test suite at the end of the implementation to ensure all tests pass.

## Validation and Testing
- **Shared Understanding**: Ensure the user confirms a shared understanding before proceeding with implementation.
- **Code Standards**: Verify that the code adheres to the repository's documented coding standards.
- **Specification Adherence**: Check that the code faithfully implements the originating specification.

### Core Concepts

# Core Concepts

## Overview
This document outlines the core concepts behind the AI-driven software development workflow. Understanding these concepts is crucial for effectively using the skills provided.

## Key Concepts

### Grilling
Grilling involves asking the user detailed questions to gather comprehensive requirements. The `grill_me` skill ensures that questions are asked one at a time to avoid overwhelming the user.

### Specifications
Specifications (`to_spec` skill) are detailed documents that outline the technical and non-technical aspects of a project. They serve as the blueprint for development.

### Tickets
Tickets (`to_tickets` skill) break down the specification into manageable tasks. Each ticket represents a task that can be completed in a single agent session.

### Implementation
Implementation (`implement` skill) involves coding the features described in the tickets. Following Test-Driven Development (TDD) practices ensures high-quality code.

### Code Review
Code review (`code_review` skill) checks the implemented code for adherence to coding standards and ensures it faithfully implements the specification.

### Committing Work
Once the code review is complete, the work is committed to the current branch, marking the completion of the task.

## Best Practices
- **Ask One Question at a Time**: Avoid overwhelming the user with multiple questions simultaneously.
- **Use TDD**: Implement features using Test-Driven Development to ensure code quality.
- **Regular Type Checking**: Run type checking regularly to catch errors early.
- **Full Test Suite**: Run the full test suite at the end of the implementation to ensure all tests pass.

## Common Pitfalls
- **Multiple Questions**: Asking multiple questions at once can confuse the user and lead to incomplete or incorrect requirements.
- **Skipping Code Review**: Skipping the code review step can result in code that does not adhere to standards or fully implement the specification.
- **Ignoring TDD**: Not using TDD can lead to poorly tested code and increased technical debt.

## Validation and Testing
- **Shared Understanding**: Ensure the user confirms a shared understanding before proceeding with implementation.
- **Code Standards**: Verify that the code adheres to the repository's documented coding standards.
- **Specification Adherence**: Check that the code faithfully implements the originating specification.

### Practical Guide

# Practical Guide

## Overview
This guide provides practical steps for implementing the AI-driven software development workflow. Follow these steps to ensure a smooth and efficient development process.

## Step-by-Step Workflow
1. **Grill the User**: Start by grilling the user to gather detailed requirements. Use the `grill_me` skill to ask one question at a time and ensure a shared understanding before proceeding.
2. **Create Specifications**: Convert the gathered requirements into a detailed specification using the `to_spec` skill. This document should outline the technical and non-technical aspects of the project.
3. **Break Down Tasks**: Use the `to_tickets` skill to break down the specification into individual tickets. Each ticket should represent a manageable task that can be completed in a single agent session.
4. **Implement Features**: Implement each ticket using the `implement` skill. Follow Test-Driven Development (TDD) practices where possible and run type checking and tests regularly.
5. **Code Review**: Review the implemented code using the `code_review` skill. Check for adherence to coding standards and ensure the code faithfully implements the originating specification.
6. **Commit Work**: Once the code review is complete, commit the work to the current branch.

## Code Snippets
```javascript
// Example of using the implement skill
const implementSkill = require('skills/implement');
implementSkill.execute({
  spec: 'path/to/spec.md',
  ticket: 'path/to/ticket.md',
  tdd: true,
  typeChecking: true,
  testSuite: true
});
```

## Best Practices
- **Ask One Question at a Time**: Avoid overwhelming the user with multiple questions simultaneously.
- **Use TDD**: Implement features using Test-Driven Development to ensure code quality.
- **Regular Type Checking**: Run type checking regularly to catch errors early.
- **Full Test Suite**: Run the full test suite at the end of the implementation to ensure all tests pass.

## Common Pitfalls
- **Multiple Questions**: Asking multiple questions at once can confuse the user and lead to incomplete or incorrect requirements.
- **Skipping Code Review**: Skipping the code review step can result in code that does not adhere to standards or fully implement the specification.
- **Ignoring TDD**: Not using TDD can lead to poorly tested code and increased technical debt.

## Validation and Testing
- **Shared Understanding**: Ensure the user confirms a shared understanding before proceeding with implementation.
- **Code Standards**: Verify that the code adheres to the repository's documented coding standards.
- **Specification Adherence**: Check that the code faithfully implements the originating specification.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[New Skills! v1.1 brings /wayfinder, /research, /implement, /to-spec, /to-tickets](https://www.youtube.com/watch?v=A8mokin_YOs)** by Matt Pocock