---
name: dead-code-analysis
description: Find unused files, exports, types, and package dependencies using knip. Use when asked to find dead code, unused exports, or files that can be deleted.
compatibility: Requires pnpm and Node 20+. Works with TypeScript/JavaScript projects.
metadata:
  author: kylebrodeur
  version: "1.0"
---

# Dead Code Analysis

Use knip to find unused files, exports, types, and package.json dependencies.

## Supported Projects

This skill works with any TypeScript/JavaScript project:
- **Node.js** backends
- **Next.js** applications
- **React** libraries
- **shadcn/ui** component libraries
- **Generic** monorepos

## Commands

```bash
# Dead code analysis
pnpm analyze:dead

# Exports and types only (less noise)
pnpm analyze:dead:exports

# Dependencies only
pnpm analyze:dead:dependencies
```

## Example output

knip exits code 1 when issues are found — this is expected, not a tool error.

```
Unused files (1)
src/config.ts

Unused dependencies (2)
some-package        package.json:12
another-package     package.json:18

Unused exports (3)
processItem         function  src/services/processor.ts:42:23
CONFIG              const     src/config/settings.ts:5:14
helperFn            function  src/utils/helpers.ts:18:17

Unused exported types (2)
ProcessOptions      interface  src/services/processor.ts:10:18
ResultShape         interface  src/utils/helpers.ts:4:18
```

## Interpreting results

| Output section | What it means |
|---|---|
| Unused files | Entire file has no importer anywhere in the project |
| Unused exports | Symbol is exported but not imported by any other module |
| Unused types | Type/interface exported but never imported externally |
| Unused dependencies | `package.json` dependency with no `import` in `src/` |

## Critical: unused exports ≠ delete

**Do not default to removing unused exports.** An unused export is a question that needs investigation before any action.

## Investigation workflow for each unused export

**Step 1 — Is it called within its own file?**

```bash
grep -n "symbolName" src/path/to/file.ts
```

If yes: the `export` is preemptive. The function is used — just not externally.

**Step 2 — Is there another piece of code doing the same job?**

```bash
grep -rn "similarFunctionName\|keywordFromImplementation" src/ --include="*.ts"
```

If you find code elsewhere doing the same thing without calling this function: a parallel implementation exists.

**Step 3 — Is there a consumer that SHOULD exist but doesn't?**

Check whether there is a route, handler, or caller that logically belongs to this function.

**Step 4 — Does the surrounding code suggest a changed direction?**

Read the function and its neighbors. If the type signatures suggest a workflow that was replaced by a different approach, the function is orphaned.

## Export categories

| Category | Description | Action |
|---|---|---|
| **A** — Preemptive export | Called within its own file; `export` added for a future caller | Safe to remove `export` keyword when ready |
| **B** — Wiring gap | Complete, correct, but no external caller exists yet | Identify what should be calling it and wire it up |
| **B (bypassed)** | Another piece of code does the same job without calling this | Consolidate — replace inline code with a call to this function |
| **C** — Changed direction | Built for a feature that moved differently; genuinely orphaned | Document and either delete or preserve |

## Generic example: bypassed utility

```ts
// utils/validation.ts — exported but knip says unused
export function validateRequiredFields(data: Record<string, unknown>, required: string[]): string | null {
  for (const field of required) {
    if (!data[field]) return `Missing required field: ${field}`;
  }
  return null;
}

// handlers/items.ts — does NOT import validateRequiredFields
if (!req.body.name || !req.body.type) {
  return res.status(400).json({ error: "Missing required fields" });
}
```

This is a bypassed utility — the handler reimplements inline what the utility was built to do.

## Known false positives to consider

- **ESLint plugins** — used in `eslint.config.js` outside `src/`
- **CSS toolchain** (`clsx`, `tailwind-merge`, `cn()` utilities) — used via config or theme files that knip doesn't trace
- **shadcn/ui components** — auto-generated, intentionally duplicated boilerplate
- **Next.js routes** — files in `app/` or `pages/` may be used via file-system routing, not imports

## Project-Specific Notes

### Next.js (App Router)

In Next.js with App Router, knip may flag files as unused that are actually entry points via routing:

| File | Why it may be flagged | Is it safe to delete? |
|---|---|---|
| `app/page.tsx` | No explicit import | **No** - used by Next.js router |
| `app/layout.tsx` | No explicit import | **No** - used by Next.js router |
| `app/error.tsx` | No explicit import | **No** - used by Next.js router |
| `app/not-found.tsx` | No explicit import | **No** - used by Next.js router |
| `app/route.ts` | No explicit import | **No** - used by Next.js router |

**Configuration**:
```json
{
  "entry": ["app/page.tsx", "app/layout.tsx", "app/router.ts", "app/route.ts"]
}
```

### Next.js (Pages Router)

For older projects using `pages/`:

| File | Why it may be flagged | Is it safe to delete? |
|---|---|---|
| `pages/_app.tsx` | No explicit import | **No** - Next.js entry |
| `pages/_document.tsx` | No explicit import | **No** - Next.js entry |
| `pages/api/*.ts` | No explicit import | **No** - API routes |

### shadcn/ui Component Libraries

When building a design system with shadcn/ui:

- **`components/ui/`** - All files are intentionally similar (boilerplate). knip won't flag these as duplicates, but jscpd will. **Add to jscpd ignore list.**
- **`lib/utils.ts`** (cn utility) - Used via string concatenation. Add to knip `ignoreDependencies`.
- **`components.json`** - No imports but defines component configuration.

### React Component Libraries

For libraries without Next.js routing:

- `index.ts` exports all components - this is the entry point
- `stories/*.tsx` files may be unused but are for Storybook development

### Tailwind CSS Projects

If using Tailwind without PostCSS processing in knip:

```json
{
  "ignoreDependencies": ["tailwindcss", "clsx", "tailwind-merge"]
}
```

The `cn()` function in `lib/utils.ts` is used via template strings which knip cannot trace.

## Project-Specific knip.json Templates

### Next.js App Router (Recommended)
```json
{
  "entry": ["app/page.tsx", "app/layout.tsx", "app/router.ts"],
  "project": ["app/**/*.ts", "app/**/*.tsx", "components/**/*.ts", "components/**/*.tsx", "lib/**/*.ts"],
  "ignore": [
    "app/**/page.tsx",
    "app/**/layout.tsx",
    "app/**/not-found.tsx",
    "app/**/error.tsx",
    "components/ui/**",
    "**/__tests__/**",
    "**/*.test.ts",
    "**/*.test.js"
  ],
  "ignoreDependencies": ["clsx", "tailwind-merge", "class-variance-authority"],
  "ignoreExportsUsedInFile": true
}
```

### Next.js Pages Router
```json
{
  "entry": ["pages/_app.tsx", "pages/_document.tsx"],
  "project": ["pages/**/*.ts", "pages/**/*.tsx", "components/**/*.ts", "lib/**/*.ts"],
  "ignore": ["components/ui/**", "**/__tests__/**"],
  "ignoreDependencies": ["clsx", "tailwind-merge"],
  "ignoreExportsUsedInFile": true
}
```

### React Library / Component Library
```json
{
  "entry": ["src/index.ts"],
  "project": ["src/**/*.ts", "src/**/*.tsx"],
  "ignore": ["src/components/ui/**", "src/stories/**", "**/*.test.ts"],
  "ignoreDependencies": ["clsx", "tailwind-merge"],
  "ignoreExportsUsedInFile": true
}
```

### Node.js Backend
```json
{
  "entry": ["src/index.ts"],
  "project": ["src/**/*.ts"],
  "ignore": ["src/**/__tests__/**", "src/**/*.test.ts"],
  "ignoreExportsUsedInFile": false,
  "rules": {
    "files": "error",
    "exports": "error",
    "dependencies": "warn"
  }
}
```

## Cross-tool interpretation

Dead code findings gain more meaning when combined with jscpd results.

**Knip reports an unused export + jscpd reports that same code is duplicated elsewhere = bypassed utility**

This combination means: the utility exists, nobody imports it, AND the logic was written again inline somewhere.
