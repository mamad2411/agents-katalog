---
description:
globs:
alwaysApply: false
---
# Roo Code's Memory Bank

I reset between sessions. My effectiveness depends entirely on the `memory-bank/` folder.

## Required Core Files

```mermaid
flowchart TD
    PB[projectbrief.md] --> PC[productContext.md]
    PB --> SP[systemPatterns.md]
    PB --> TC[techContext.md]

    PC --> AC[activeContext.md]
    SP --> AC
    TC --> AC

    AC --> P[progress.md]
```

## Memory Bank Workflow

### Read Phase
1. Read all memory bank files before any task
2. Cross-reference with existing `.roo/rules/` files
3. Identify current project state and patterns

### Update Phase
Update memory bank on:
- New patterns discovered
- Major changes to architecture
- User request: "update memory bank"
- Completion of significant features
- Integration of new components or libraries

### Integration with Existing Rules
- **Taskmaster Integration**: Reference `taskmaster.md` for task management patterns
- **Development Workflow**: Align with `dev_workflow.md` processes
- **UI Patterns**: Maintain consistency with `styling-guidelines.md` and ShadCN usage
- **Security**: Follow patterns from `security.md`
- **Performance**: Apply optimizations from `performance_optimization.md`

### File Hierarchy
```
memory-bank/
├── projectbrief.md      # Mission and core goals
├── productContext.md    # Why project exists, problems solved
├── techContext.md       # Tech stack, architecture decisions
├── systemPatterns.md    # Design patterns, conventions
├── activeContext.md     # Current focus, recent changes
└── progress.md          # Milestones, completed features
```

### Maintenance Rules
- Update `activeContext.md` after each significant change
- Append to `progress.md` when features are completed
- Modify `systemPatterns.md` when new patterns emerge
- Keep `techContext.md` current with stack changes
- Review and update `productContext.md` when scope evolves

### Cross-Reference Points
- **Project Structure**: Align with `project_structure_and_organization_rules.md`
- **Communication**: Follow `communication_Documentation_rules.md`
- **Testing**: Reference `testing_and_quality_assurance_rules_code.md`
- **Error Handling**: Apply `error_handling_Debugging.md` patterns
