# Module Scaffolding

## Purpose
Scaffolds feature modules and their internal components using generators.

## Role
Frontend Developer

## Phase
Development

## Triggered By
New feature/module needed within an existing webapp.

## Inputs
- Feature/module requirement from the task

## Rule
ALWAYS use generator — NEVER create module structure manually. Command: `bun turbo gen → select module/page/component/hook/usecase`.

## Process

### Module Structure (always)
```
apps/web/{app}/src/modules/{feature}/
├── index.ts              ← barrel export
├── pages/                ← file-based router pages
├── components/           ← feature-specific components
├── hooks/                ← feature-specific hooks
└── usecases/             ← feature-specific business logic
```

### Shared Structure (cross-module)
```
apps/web/{app}/src/shared/
├── components/           ← shared across modules
├── hooks/                ← shared across modules
└── helpers/              ← utility functions
```

### Import Rule
Never import directly from another module. Cross-module sharing goes through `shared/` only.

## Outputs
Scaffolded module structure ready for implementation.

## Quality Gates
- [ ] Generator used for module and all internal elements
- [ ] No cross-module direct imports
- [ ] Index.ts barrel export created

## References
- `.claude/skills/frontend-developer/webapp-scaffolding/SKILL.md`
- `.claude/skills/frontend-developer/component-development/SKILL.md`
