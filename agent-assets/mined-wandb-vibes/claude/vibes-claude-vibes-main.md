# Claude Code Prompting Guide

## Basic Usage

```bash
claude
claude "Your prompt here"
```

## Claude Code Specific Features

### Slash Commands
Claude Code supports custom slash commands. Create them in your project root:

```bash
# Example: Add to your project's .claude/commands/
/slides - Regenerate presentation slides
```

### Memory Management
Claude Code maintains context across conversations. Use `CLAUDE.md` files to provide persistent context.

## Agentic Prompting Techniques

### 1. Multi-Step Planning
Claude excels at breaking down complex tasks:

```bash
claude "I need to implement user authentication. First, create a plan with all the necessary steps."
```

### 2. Code Analysis and Refactoring
Leverage Claude's code understanding:

```bash
claude "Analyze this codebase structure and suggest architectural improvements: [paste code or file paths]"
```

### 3. Interactive Development
Build solutions iteratively:

```bash
claude "Start building a React component for user profiles. Begin with the basic structure."
# Then: "Add form validation to the profile component"
# Then: "Add state management with useReducer"
```

### 4. Documentation Generation
Claude is excellent at creating comprehensive docs:

```bash
claude "Generate API documentation for this Express.js router: [code]"
```

### 5. Test-Driven Development
Use Claude to guide TDD workflows:

```bash
claude "Write failing tests for a user authentication service, then implement the service to make them pass"
```

## Advanced Techniques

### System Thinking
```bash
claude "Think like a system architect. How would you design a scalable microservices architecture for an e-commerce platform?"
```

### Code Review Partner
```bash
claude "Act as a senior code reviewer. What potential issues do you see in this implementation? Consider security, performance, and maintainability."
```

### Debugging Assistant
```bash
claude "I'm getting this error: [error message]. Here's my code: [code]. Walk me through debugging this step by step."
```

### Learning Mentor
```bash
claude "I'm learning TypeScript. Explain generics with practical examples I can use in my current project."
```

## File Operations

Claude Code can work with your entire codebase:

```bash
# Analyze multiple files
claude "Review all components in src/components/ for consistency"

# Generate based on existing patterns
claude "Create a new API endpoint following the pattern in src/routes/users.js"

# Cross-file refactoring
claude "Rename the User interface to UserProfile across all TypeScript files"
```

## Best Practices

1. **Provide Context**: Share relevant files, error messages, and project details
2. **Ask for Explanations**: Request reasoning behind suggestions
3. **Iterate Incrementally**: Build solutions step by step
4. **Use Memory**: Reference previous conversations and decisions
5. **Be Specific**: Include exact requirements and constraints

## Example Workflows

### Feature Development
```bash
# 1. Requirements analysis
claude "I need to add real-time notifications. What are the technical considerations?"

# 2. Architecture planning
claude "Design the notification system architecture using WebSockets and Redis"

# 3. Implementation
claude "Implement the WebSocket server for notifications"

# 4. Testing
claude "Create integration tests for the notification system"

# 5. Documentation
claude "Document the notification API for other developers"
```

### Bug Investigation
```bash
# 1. Error analysis
claude "This error occurs intermittently: [error]. Here's the relevant code: [code]"

# 2. Hypothesis testing
claude "What are the most likely causes? How can we test each hypothesis?"

# 3. Solution implementation
claude "Implement logging and error handling to prevent this issue"

# 4. Verification
claude "Review this fix and suggest additional safeguards"
```

### Code Quality Improvement
```bash
# 1. Assessment
claude "Analyze this module for code quality issues: [file path]"

# 2. Refactoring plan
claude "Create a refactoring plan to improve this code's maintainability"

# 3. Implementation
claude "Refactor this function to be more testable and readable"

# 4. Documentation
claude "Update the documentation to reflect these changes"
```

## Project-Specific Context

Use your project's `CLAUDE.md` file to provide persistent context:

```markdown
# Project Context
- Framework: Next.js 14 with TypeScript
- Database: PostgreSQL with Prisma ORM
- State Management: Zustand
- Testing: Jest + React Testing Library
- Deployment: Vercel

## Coding Standards
- Use functional components with hooks
- Prefer server components when possible
- Follow the existing file structure in src/
```

This helps Claude provide more relevant and consistent suggestions throughout your project.