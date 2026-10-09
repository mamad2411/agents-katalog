---
name: review-fix-violations
description: "Use when architecture violations were found and need automated fixing by priority."
user-invocable: true
argument-hint: "[module]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Identify and fix `docs/ARCHITECTURE.md` violations in the specified module.

Module: $ARGUMENTS

## Steps

1. Run `/review-check-architecture` to find violations.

2. For each violation found, fix in priority order:

   **Critical (fix first):**
   - try/catch in services -> remove, move error handling to component/interceptor
   - Transformation in services -> move to adapter
   - innerHTML without sanitization -> remove or use DomSanitizer
   - Hardcoded secrets -> move to environment files

   **Important:**
   - NgModule -> migrate to standalone (`/migration-migrate-component`)
   - @Input/@Output decorators -> input()/output() signals
   - Constructor DI -> inject()
   - BehaviorSubject in stores -> signals
   - any types -> type correctly
   - Missing OnPush -> add ChangeDetectionStrategy.OnPush

   **Improvements:**
   - Components > 200 lines -> decompose
   - Console.log -> remove
   - TODO/FIXME -> resolve or create issue

3. Validate after each fix:
```bash
npx tsc --noEmit && ng build && ng test --watch=false
```

4. Report what was fixed and what remains.
