# TypeScript Style

- Prefer `const` for values that are never reassigned.
- Use `interface` for public object shapes, `type` for unions and primitives.
- Never use `any` in public function signatures; use `unknown` and narrow.
- Avoid default exports in library code.
- Use `import type { Foo } from 'bar'` for type-only imports.
