# Agentic Prompting Guide

General strategies for working effectively with AI coding assistants across all platforms (Claude, Gemini, GPT, etc.).

## Core Principles

### 1. Treat AI as a Collaborative Partner
- Share your thought process and constraints
- Ask for alternatives and trade-offs
- Build on AI suggestions iteratively

### 2. Provide Rich Context
- Include relevant code, error messages, and project details
- Mention your experience level and learning goals
- Specify your environment (frameworks, tools, constraints)

### 3. Think in Systems
- Break complex problems into smaller components
- Consider interactions between different parts
- Plan for scalability and maintainability

## Universal Prompting Patterns

### The STAR Method
**S**ituation - **T**ask - **A**ction - **R**esult

```
Situation: I'm building a React app with TypeScript
Task: Need to implement user authentication
Action: Show me how to create a login form with validation
Result: Should handle success/error states and redirect users
```

### The 5W+H Framework
Who, What, When, Where, Why, How

```
Who: Junior developer learning Node.js
What: Build a REST API for a blog
When: Need it working by end of week
Where: Using Express.js and MongoDB
Why: Portfolio project for job applications
How: Step-by-step implementation with explanations
```

### Chain of Reasoning
Ask the AI to show its thinking process:

```
"Think through this step by step:
1. What are the main challenges with this approach?
2. What are 3 different solutions?
3. What are the pros/cons of each?
4. Which would you recommend and why?"
```

## Advanced Agentic Techniques

### 1. Role Assignment
Give the AI specific expertise:

```bash
"Act as a DevOps engineer with 10 years of AWS experience. 
How would you set up CI/CD for this Node.js application?"
```

### 2. Perspective Taking
Ask for multiple viewpoints:

```bash
"From a security perspective... From a performance perspective... From a maintainability perspective..."
```

### 3. Socratic Method
Let the AI guide your learning:

```bash
"Instead of giving me the answer, ask me questions that will help me figure out why my React component isn't re-rendering."
```

### 4. Red Team/Blue Team
Challenge solutions:

```bash
"You just suggested using JWT tokens. Now argue against that approach - what are the vulnerabilities and alternatives?"
```

### 5. Rubber Duck Debugging
Use AI as a debugging partner:

```bash
"Let me walk you through my code line by line. Stop me when you see potential issues or have questions."
```

## Code-Specific Patterns

### Architecture First
```bash
"Before we write any code, let's design the architecture. What are the main components and how do they interact?"
```

### Test-Driven Thinking
```bash
"What would good tests for this function look like? Write the tests first, then implement the function."
```

### Performance Considerations
```bash
"Implement this feature, but also explain the performance implications and how to optimize it."
```

### Security Mindset
```bash
"What security vulnerabilities could this code introduce? How do we prevent them?"
```

## Debugging Workflows

### The Scientific Method
1. **Observe**: What exactly is happening?
2. **Hypothesize**: What might be causing it?
3. **Test**: How can we validate our hypothesis?
4. **Analyze**: What do the results tell us?
5. **Conclude**: What's the solution?

### Error Analysis Pattern
```bash
"I'm getting this error: [error message]
Here's my code: [code]
Here's what I expected: [expected behavior]
Here's what actually happened: [actual behavior]
What's the most likely cause and how do we fix it?"
```

## Learning Acceleration Techniques

### Explain Like I'm 5 (ELI5)
```bash
"Explain async/await in JavaScript like I'm 5 years old, then give me practical examples."
```

### Learn By Teaching
```bash
"I need to teach someone else about React hooks. Help me create a lesson plan with examples."
```

### Progressive Complexity
```bash
"Start with the simplest possible implementation, then show me how to add complexity step by step."
```

### Connect to Prior Knowledge
```bash
"I understand loops in Python. How are React's useEffect dependencies similar to loop conditions?"
```

## Quality Assurance Patterns

### Code Review Checklist
```bash
"Review this code for:
- Functionality correctness
- Security vulnerabilities  
- Performance bottlenecks
- Code style and readability
- Test coverage gaps"
```

### Documentation Standards
```bash
"Generate documentation that includes:
- Purpose and usage
- Input/output examples
- Error handling
- Performance considerations
- Related functions/components"
```

## Best Practices

### Do's
✅ Be specific about your environment and constraints  
✅ Ask for explanations of the reasoning  
✅ Request multiple approaches when possible  
✅ Iterate and refine based on feedback  
✅ Ask follow-up questions  
✅ Request code reviews and improvements  

### Don'ts
❌ Use vague or ambiguous language  
❌ Accept the first solution without exploring alternatives  
❌ Skip testing and validation steps  
❌ Ignore security and performance considerations  
❌ Copy code without understanding it  
❌ Forget to consider edge cases  

## Example Multi-Turn Conversation

```
You: "I need to build a user authentication system for my web app"

AI: "I'd be happy to help! Could you tell me more about your tech stack and requirements?"

You: "It's a Next.js app with TypeScript. I need login/logout, protected routes, and session management."

AI: "Great! Let's start with the architecture. We have several options..."

You: "I like the JWT approach. Can you show me how to implement it securely?"

AI: "Absolutely. Let's start with the authentication middleware..."

You: "This looks good, but how do I handle token refresh?"

AI: "Good question! Here's how to implement automatic token refresh..."
```

## Platform-Specific Adaptations

Remember to adapt these general principles to each platform's strengths:

- **Claude**: Excels at complex reasoning and code analysis
- **Gemini**: Great for creative solutions and explanations  
- **GPT**: Strong at following structured formats and templates
- **Codex**: Focused on code generation and completion

The key is to experiment and find what works best for your specific needs and working style.