---
name: always-apply-standards
description: Ensures coding standards, best practices, and quality principles are applied to all code written. Use when writing code, creating functions, implementing features, refactoring, or performing any development task. This skill ensures consistency, maintainability, and quality across all projects and codebases.
---

# Always Apply Standards

This skill ensures that all code follows established standards and best practices. Apply these principles to every piece of code you write or modify.

## Core Principles

When writing or modifying code, always:

1. **Improve bad code, don't perpetuate it** - If you encounter poorly written code, suggest refactoring or a better approach instead of copying the bad pattern
2. **Follow existing patterns** - Match the style and patterns already in the codebase (but only if they're good patterns)
3. **Apply relevant skills** - Consider and apply other available skills (DRY/SOLID, TypeScript best practices, error handling, security, etc.)
4. **Maintain consistency** - Use consistent naming, structure, and organization
5. **Handle errors properly** - Include appropriate error handling and validation
6. **Write maintainable code** - Prioritize readability and maintainability
7. **Modern delivery habits** - Small reviewable diffs, committed lockfiles where the stack uses them, structured logging for services, and accessibility considered by default for UI work (see **modern-development-practices** for cross-cutting norms)

## Before Writing Code

1. **Check existing code patterns** - Review similar files/functions in the codebase
2. **Evaluate code quality** - If existing code is poorly written, suggest improvements rather than copying bad patterns
3. **Identify relevant skills** - Consider which specialized skills apply (TypeScript, Vue, React Native, API design, etc.)
4. **Follow project structure** - Respect existing directory organization and file naming conventions
5. **Use existing utilities** - Check for existing helper functions, utilities, or shared code before creating new ones

## When Encountering Bad Code

**CRITICAL**: If you find poorly written code, do NOT simply maintain or copy it. Instead:

1. **Identify the problems** - What makes this code bad? (duplication, poor structure, missing error handling, etc.)
2. **Suggest refactoring** - Propose a better approach or refactoring plan
3. **Explain the benefits** - Why is the suggested approach better?
4. **Implement improvements** - When modifying or extending bad code, improve it as part of your changes

**Examples of bad code patterns to improve:**
- Duplicated logic that should be extracted
- Functions that do too many things (violate single responsibility)
- Missing error handling or validation
- Poor naming or unclear structure
- Security vulnerabilities
- Performance issues
- Type safety problems

**Never say**: "I'll keep it as-is because that's how it was written"
**Always say**: "I notice this code has [issue]. Let me refactor it to [better approach]"

## Code Quality Checklist

Apply these checks to all code:

- [ ] Follows TypeScript strict mode best practices
- [ ] Uses consistent naming conventions (camelCase for variables/functions, PascalCase for types/components)
- [ ] Includes proper error handling
- [ ] Validates inputs where appropriate
- [ ] Follows DRY principles (no unnecessary duplication)
- [ ] Functions are focused and single-purpose
- [ ] Code is readable and well-structured
- [ ] Security best practices are followed
- [ ] Performance considerations are addressed

## Integration with Other Skills

This skill works alongside your other skills. When writing code:

- **TypeScript code** → Apply TypeScript best practices skill
- **Vue components** → Apply Vue frontend patterns skill
- **API endpoints** → Apply API design RESTful skill
- **Database operations** → Apply database data modeling skill
- **Error scenarios** → Apply error handling and logging skill
- **Security features** → Apply security best practices skill
- **Performance issues** → Apply performance optimization skill
- **Current engineering defaults** (AI-assisted workflow, observability, supply chain, API contracts) → Apply modern-development-practices skill

## Project-Specific Considerations

- **React Native app**: Follow React Native patterns, use TypeScript strictly, maintain RTL support
- **Vue dashboard**: Follow Vue 3 patterns, use composables appropriately, maintain Pinia store structure
- **Node.js API**: Follow RESTful conventions, use proper error handling, validate all inputs

## Remember

This skill ensures quality and consistency. Every line of code should reflect these standards. When in doubt, prioritize:
1. **Code quality over blind consistency** - Improve bad code rather than copying bad patterns
2. Maintainability
3. Type safety
4. Error handling
5. Security

**Key principle**: If you see bad code, improve it. Don't perpetuate bad patterns just because they exist.
