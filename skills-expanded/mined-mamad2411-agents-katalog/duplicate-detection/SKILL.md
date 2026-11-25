---
name: duplicate-detection
description: Find copy-pasted code blocks and similar patterns using jscpd. Use when asked to find duplicate code, identify refactoring targets, or check if a utility should be extracted because it appears in multiple places.
compatibility: Requires pnpm. Generates HTML reports at /tmp/jscpd-report/html/index.html.
metadata:
  author: kylebrodeur
  version: "1.0"
---

# Duplicate Code Detection

Use jscpd to find copy-pasted code blocks using token comparison.

## Supported Projects

- **Node.js** backends
- **Next.js** applications (App Router & Pages Router)
- **React** libraries
- **shadcn/ui** component libraries
- **Generic** TypeScript/JavaScript projects

## Commands

```bash
# Run detection + generate HTML report
pnpm analyze:dupes

# Open the HTML report (side-by-side diff per clone group)
open /tmp/jscpd-report/html/index.html
```

## Configuration

Create a `.jscpd.json` file at project root:

```json
{
  "threshold": 5,
  "reporters": ["html", "console"],
  "ignore": [
    "**/__tests__/**",
    "**/*.test.ts",
    "**/*.test.js",
    "**/dist/**",
    "**/node_modules/**"
  ],
  "gitignore": true,
  "minLines": 8,
  "minTokens": 50,
  "format": ["typescript", "javascript"],
  "output": "/tmp/jscpd-report"
}
```

## Clone Classification Guide

### False positive: uniform structural patterns

When a codebase enforces consistent shape across similar files (e.g., action file entry points, component definitions), jscpd will report them as duplicates even though the duplication is intentional.

**Example** — action file entry points:

```ts
// actions/createItem.ts
export const createItemAction: ActionConfig = {
  id: "create-item",
  label: "Create Item",
  schema: createItemSchema,
  execute: async (params, api) => { ... }
};

// actions/deleteItem.ts
export const deleteItemAction: ActionConfig = {
  id: "delete-item",
  label: "Delete Item",
  schema: deleteItemSchema,
  execute: async (params, api) => { ... }
};
```

The outer shell is identical. jscpd flags it. But this uniformity is the point — every action follows the same contract, which makes adding new actions predictable and safe. **Do not refactor.**

### False positive: protocol/shape boilerplate

When a response type or protocol requires the same fields to be assembled in every consumer, the assembly code will look duplicated.

**Example** — response builders with the same shape:

```ts
// In handlerA
return { processed: results.length, skipped: skipped.length, errors, dryRun };

// In handlerB
return { processed: results.length, skipped: skipped.length, errors, dryRun };
```

The contents differ per handler — only the shape is shared.

### False positive: parallel strategy implementations

When two code paths implement the same *kind* of operation but for different *cases*, jscpd will flag the retry/fallback scaffold as a duplicate.

**Example** — lookup strategies:

```ts
// lookupByCode
async function lookupByCode(code: string): Promise<User | null> {
  for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
    try {
      const result = await api.findByCode(code);
      if (result) return result;
    } catch (err) {
      if (attempt === MAX_RETRIES) throw err;
      await delay(RETRY_DELAY);
    }
  }
  return null;
}

// lookupById
async function lookupById(id: string): Promise<User | null> {
  for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
    try {
      const result = await api.findById(id);
      if (result) return result;
    } catch (err) {
      if (attempt === MAX_RETRIES) throw err;
      await delay(RETRY_DELAY);
    }
  }
  return null;
}
```

Investigate before accepting. Ask: should there be a single `findUser(identifier, method)` function?

### Genuine target: same logic duplicated across feature modules

When two *different* feature areas contain the same block of logic, that logic belongs in `shared/utils/`.

## What is excluded

- Auto-generated component library files (would produce false positives)
- All `__tests__/` directories and `*.test.ts` / `*.spec.ts` files
- Build output (`dist/`, `build/`, `lib/`)

## Interpreting results

jscpd reports "clone groups" — sets of code blocks that are structurally near-identical based on token comparison. It detects structural similarity even when variable names differ.

**Important**: jscpd cannot determine intent. It reports *what looks similar*, not *whether it should be different*. Every clone group requires manual review.

## Act on clone groups

1. **Extract a utility** — If `services/A.ts` and `services/B.ts` share logic, create `shared/utils/sharedHelper.ts`
2. **Create a higher-order function** — If two functions share an outer retry/error-handling shell
3. **Enforce via TypeScript** — If two blocks share a *shape*, create a shared interface or builder
4. **Accept and suppress** — If structural/intentional, add the path to `"ignore"` in `.jscpd.json`

## Project-Specific Notes

### Next.js (App Router)

Configure jscpd to analyze the `app/` directory. Pages and layouts often have similar structure — focus on finding duplicate business logic, not layout patterns.

### shadcn/ui Component Libraries

Components in `components/ui/` are intentionally similar — each is a self-contained primitive. Don't try to consolidate them.

### Tailwind CSS / shadcn/ui

- Component files often have similar JSX structure (intentional)
- Focus on finding duplicate **logic**, not **styles**

## Cross-tool interpretation

jscpd findings gain more meaning when combined with knip results.

**jscpd flags two blocks as duplicates + knip flags one of them as an unused export = strong signal of a bypassed utility**

```
jscpd: src/utils/validator.ts:14-28 clones src/handlers/items.ts:67-81
knip:  "validateItemInput" — unused export in src/utils/validator.ts
```

This means: a utility exists for this validation, nobody imports it, and the validation logic was written inline. The fix is to replace the inline code with a call to the utility — not to delete either.
