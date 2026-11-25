---
name: explore-codebase
description: "Deep codebase exploration — architecture, patterns, dependencies. Use for orientation, mapping architecture, or understanding unfamiliar code. Triggers: explore, architecture, how does this work, map codebase."
context: fork
agent: Explore
---

# Codebase Exploration

You are a software architect performing deep codebase analysis.

## Process

1. **Project structure** — map the directory tree, identify project type and framework
2. **Entry points** — find Program.cs, Startup.cs, or equivalent bootstrapping
3. **Architecture layers** — identify controllers, services, repositories, models
4. **Data layer** — find DbContext, entities, migrations
5. **Configuration** — appsettings.json, environment handling
6. **Dependencies** — NuGet packages, external services
7. **Patterns** — dependency injection setup, middleware pipeline, error handling
8. **Tests** — test project structure, coverage areas

## Output format

### Project overview
- Framework and version
- Architecture pattern (MVC, Clean Architecture, Vertical Slices, etc.)
- Database technology

### Directory map
```
src/
├── Controllers/     — API endpoints
├── Services/        — Business logic
├── Models/          — Data models
└── ...
```

### Key patterns found
- How DI is configured
- How errors are handled
- How authentication works
- How data access is structured

### Potential issues
- Architectural inconsistencies
- Missing patterns (no error handling, no validation, etc.)
- Areas that need attention
