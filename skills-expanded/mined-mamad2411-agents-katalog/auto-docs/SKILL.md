---
name: auto-docs
description: Creates structured technical documentation in /docs as markdown files, with Mermaid diagrams, usage examples, codebase references, and @docs back-reference tags that keep docs in sync when source files are later edited. Use when the user asks to create, write, or generate documentation for a feature, API, component, webhook, or flow.
---

# Auto-Docs

Creates technical docs in `/docs`, stamps source files with `@docs` back-references, and self-installs a sync rule so future edits to those files automatically trigger doc updates.

## Step 0 — Self-install the sync rule (once per project)

Before writing any documentation, check if `.cursor/rules/documentation-sync.mdc` exists in the project root.

If it does **not** exist, create it now by reading [rule-template.md](rule-template.md) and writing its contents to `.cursor/rules/documentation-sync.mdc`. Tell the user: "Installed documentation-sync rule for this project."

If it already exists, skip this step silently.

---

## Step 1 — Determine filename and topic

- Ask the user what is being documented if not already clear.
- Choose a kebab-case filename: `<short-topic-slug>.md`
- Save to `/docs/<filename>.md`

---

## Step 2 — Write the document

Use this exact structure:

```md
# <Title: clear, descriptive>

**Date:** YYYY-MM-DD
**Author:** Coding Assistant
**Status:** Draft | Active | Deprecated

---

## Summary

One or two sentences describing what this document covers and who it is for.

---

## Overview

Purpose, context, and scope of the feature, API, or system.

---

## Architecture / Flow

[Mermaid diagram — see Step 3]

---

## Key Concepts

Bullet-point list of important terms, types, or patterns.

---

## Usage Examples

\`\`\`typescript
// Concrete example
\`\`\`

---

## API Reference

Function signatures, parameters, return types, and side effects (omit if not applicable).

---

## Related Files

| File              | Role                                |
| ----------------- | ----------------------------------- |
| `path/to/file.ts` | What this file does in this context |

---

## References

Links to related `/docs/*.md` files or external documentation.
```

---

## Step 3 — Mermaid diagrams

Include a diagram whenever there is a flow, relationship, or state to describe. Choose the right type:

| Diagram           | Use when                                     |
| ----------------- | -------------------------------------------- |
| `flowchart TD`    | Data flow or processing steps                |
| `sequenceDiagram` | Request/response or service-to-service calls |
| `erDiagram`       | Database table relationships                 |
| `stateDiagram-v2` | Status transitions or state machines         |

---

## Step 4 — Write full JSDoc and add @docs back-reference to every related source file

For every file in the **Related Files** table:

1. **Read the full file** to understand its purpose, behaviour, key functions, dependencies, and any files that depend on it.
2. **Write or replace the file-level JSDoc block** at the top of the file. The JSDoc must describe the file broadly — not just in the context of the feature being documented — so it remains accurate as the codebase grows. Include:
   - `@description` — what the file does and its role in the overall system
   - `@behavior` — key steps, logic, or side effects (omit if trivial)
   - `@depends-on` — other files or services this file relies on (excluding standard library imports)
   - `@depended-by` — files that import or call into this file
   - `@example` — usage example for hooks, actions, utilities, or reusable modules
   - `@docs` — path to the linked documentation file
3. If the file already has a JSDoc, update it rather than replace it — preserve any existing tags that are still accurate and add missing ones.

**JSDoc template:**

```ts
/**
 * @description <What this file does and its role in the system.>
 *
 * @behavior
 * - <Key step or behaviour 1>
 * - <Key step or behaviour 2>
 *
 * @depends-on <path/to/dependency.ts>, <ExternalService>
 * @depended-by <path/to/consumer.ts>
 *
 * @example
 * // How to use this module
 * import { something } from './this-file'
 * something()
 *
 * @docs /docs/<filename>.md
 */
```

Omit any tag that is not applicable (e.g. skip `@example` for a page component, skip `@behavior` for a simple config file).

Confirm to the user which files were updated.

---

## Step 5 — Verification checklist

- [ ] Saved to `/docs/<filename>.md`
- [ ] Has title, date, and summary
- [ ] Mermaid diagram included (if warranted)
- [ ] Usage examples included
- [ ] Related Files table complete
- [ ] Every listed source file has a `@docs` tag in its JSDoc
- [ ] `documentation-sync.mdc` rule exists in `.cursor/rules/`
