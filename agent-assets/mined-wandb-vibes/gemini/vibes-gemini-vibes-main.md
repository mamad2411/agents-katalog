# Gemini Instructions

This repo contains a presentation defined in slides.md.  We use marp to render it.  After making any changes you can run `pnpm slides` to regenerate the presentation at index.html.

The below information is less for you and more for users of the repo so please disregard instructions below this line.

=================================

# Gemini CLI Prompting Guide

## Basic Usage

```bash
gemini "Your prompt here"
```

## Agentic Prompting Techniques

### 1. Task Decomposition
Break complex tasks into smaller, manageable steps:

```bash
gemini "I need to build a web scraper. First, help me understand what libraries I should use for Python web scraping."
```

### 2. Role-Based Prompting
Assign specific roles to get targeted responses:

```bash
gemini "Act as a senior software engineer. Review this code and suggest improvements: [paste code]"
```

### 3. Chain of Thought
Ask Gemini to show its reasoning:

```bash
gemini "Think step by step: How would you debug a memory leak in a Node.js application?"
```

### 4. Context Setting
Provide relevant context for better responses:

```bash
gemini "I'm working on a React TypeScript project using Vite. How should I configure environment variables for different deployment environments?"
```

### 5. Iterative Refinement
Build on previous responses:

```bash
gemini "Based on your previous suggestion about using React Query, show me how to implement error handling for API calls."
```

## Code-Specific Prompts

### Code Review
```bash
gemini "Review this function for potential bugs, performance issues, and best practices: [code]"
```

### Documentation
```bash
gemini "Generate comprehensive JSDoc comments for this TypeScript class: [code]"
```

### Testing
```bash
gemini "Create unit tests for this function using Jest: [code]"
```

### Refactoring
```bash
gemini "Refactor this code to use modern JavaScript features and improve readability: [code]"
```

## Best Practices

1. **Be Specific**: Include file types, frameworks, and constraints
2. **Provide Context**: Mention your project structure and requirements
3. **Ask for Alternatives**: Request multiple approaches when possible
4. **Request Explanations**: Ask "why" to understand the reasoning
5. **Iterate**: Build on responses to refine solutions

## Example Workflows

### Building a New Feature
```bash
# 1. Plan the feature
gemini "I need to add user authentication to my Express.js app. What's the best approach?"

# 2. Get implementation details
gemini "Show me how to implement JWT authentication middleware in Express"

# 3. Handle edge cases
gemini "What security considerations should I keep in mind with JWT tokens?"
```

### Debugging Issues
```bash
# 1. Describe the problem
gemini "My React component is re-rendering infinitely. Here's the code: [code]"

# 2. Get specific solutions
gemini "How can I use React.memo and useMemo to prevent unnecessary re-renders?"

# 3. Verify the fix
gemini "Review this optimized component and confirm it addresses the re-rendering issue: [code]"
```