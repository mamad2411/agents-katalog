---
name: write-typescript
description: TypeScript coding conventions for this codebase. Use when writing or modifying TypeScript or TSX files, when TypeScript type errors appear, or when asked about strict mode, type imports, naming conventions, return types, the no-any rule, async functions, floating promises, exhaustive switches, readonly properties, non-null assertions, control-flow style, test typing patterns, Node fs Dirent mock typing, formatting with oxfmt, import group order, enforced alphabetical ordering, the three-parameter limit, or JSDoc on public APIs.
license: MIT
---

# Write TypeScript

All TypeScript projects in this codebase use strict settings. This skill is the entry point and links to focused reference files so guidance stays organized and maintainable.

## When to Use This Skill

Use this skill when:

- Writing or refactoring `.ts` or `.tsx` files
- Fixing TypeScript compile or lint errors
- Reviewing strict-mode type-safety issues
- Standardizing naming, import style, or control-flow patterns
- Writing strict typed tests (including `fs.readdirSync` Dirent mocks)

## References

- [Strict typing](./references/strict-typing.md)
: strict flags, explicit return types, `any` avoidance, `unknown`, promises, exhaustive switches.
- [Naming and imports](./references/naming-and-imports.md)
: identifier naming, abbreviation rules, file naming, type imports, NodeNext `.js` extensions.
- [Class and control flow](./references/class-and-control-flow.md)
: readonly properties, braces, early returns, object shorthand, template literals.
- [Error handling and tests](./references/errors-and-tests.md)
: catch typing, guard-first test narrowing, Node Dirent mock typing pattern.
- [Formatting and ordering](./references/formatting-and-ordering.md)
: `oxfmt` settings, import groups, enforced alphabetical order, the 3-parameter
limit, JSDoc on public APIs.
- [Size limits](./references/size-limits.md)
: file length, function length, block nesting depth, parameter limits, complexity, comment block sizes.

## Related Skills

- [Handle error](../handle-errors/SKILL.md)
- [Write comment](../write-comments/SKILL.md)
- [Validate code](../validate-code/SKILL.md)

## Verification

After TypeScript changes:

```bash
pnpm exec nx run <project>:lint-code --configuration=write
pnpm exec nx run <project>:lint-code --configuration=check
```

## Notes

- Keep this `SKILL.md` concise and discovery-focused.
- Add detailed examples and larger workflows to files under `references/`.
- > ✅ **Best practice:** In NestJS class files such as `*.service.ts`, `*.command.ts`, `*.resolver.ts`, `*.dataloader.ts`, and `*.module.ts`, keep only imports and the class at top level. Move helper types and interfaces to `*.types.ts`, constants to `*.constants.ts`, and shared initialization logic into class members or dedicated modules.
- > ⚠️ **Warning:** Do not use top-level alias exports or type re-exports from NestJS class files. Import supporting symbols from their source `*.types.ts` or `*.constants.ts` file instead of re-exporting them through the class file.
