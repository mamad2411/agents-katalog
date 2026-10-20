---
name: follow-best-practice
description: Write according to best practices for the given context
argument-hint: "[topic]"
related:
  - learn
  - deep-research

---

## Goal

Write according to best practices for the given context

## Scope

Apply to every workspace and every kind of work (code, workflow, config, documentation) so results are high quality and follow standards

## Execute

### 1. Analyze Context

> Goal: Identify the context and tech stack where the best practices will apply

1. Identify the context of the work (code, workflow, config, documentation, etc.)
2. For code: read `package.json`, `Cargo.toml`, or the relevant package manifest
3. For code: identify the language, runtime, and libraries in use
4. Summarize the tech stack or tools relevant to that context

### 2. Research Best Practices

> Goal: Research current best practices from credible sources

1. Identify the library, framework, or tool whose best practices to learn
2. Follow `/learn-from-web` for systematic learning from web sources
3. Follow `/deep-research` when deep information from multiple sources is needed
4. Verify the information is current

### 3. Apply Best Practices

> Goal: Apply the learned best practices to improve files per context

1. Read all files that need improvement
2. Analyze what these files need per the best practices of that context
3. Edit the files according to the learned best practices
4. Check consistency with what already exists
5. Update the relevant configuration and settings
6. Document the recommended patterns and conventions

### 4. Verify Implementation

> Goal: Confirm the best practices are fully applied with no regressions

1. Run linter and typecheck to verify
2. Run tests to confirm no regressions
3. Verify the best practices have been fully applied
4. Update documentation if needed
5. Try out the usage per the best practices
6. Record lessons learned

## Rules

### 1. Research Sources

Use reliable sources for best practices

- Official documentation as the primary source
- Community guidelines and style guides
- Well-known blogs and articles
- Widely used GitHub repositories
- Stack Overflow for common issues
- Use `/learn-from-web` as the primary workflow for learning
- Use `/deep-research` when deep information from multiple sources is needed

### 2. Language-Specific Conventions

Follow each language's conventions

- TypeScript: follow TypeScript best practices
- Rust: follow Rust guidelines
- Go: follow Go conventions
- Python: follow PEP 8 and best practices
- Use linters suited to each language

### 3. Library-Specific Patterns

Use patterns suited to each library

- React: use hooks patterns and component patterns
- Vue: use the composition API and best practices
- Prisma: use schema best practices and queries
- Read each library's documentation thoroughly
- Check examples from official sources

### 4. Runtime Considerations

Consider the characteristics of the runtime in use

- Node.js: use async patterns and event loop best practices
- Bun: use Bun-specific APIs and native features
- Deno: follow Deno security and module patterns
- Browser: consider performance and compatibility
- Server: consider security and scalability

### 5. Consistency Maintenance

Keep consistency across the codebase

- Use consistent naming conventions
- Use consistent code style
- Use consistent patterns
- Configure automatic linter and formatter
- Do code review to verify

## Expected Outcome

- Results written per the best practices of the context
- High quality and maintainable
- Consistency across the project
- Correct and up-to-date best practices
- Suitable patterns and conventions