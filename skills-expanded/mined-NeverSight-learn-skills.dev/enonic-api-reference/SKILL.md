---
name: enonic-api-reference
description: Enonic XP server-side JavaScript/TypeScript API reference for all /lib/xp/* libraries. Provides function signatures, parameters, return types, and usage examples for lib-content, lib-node, lib-auth, lib-portal, lib-context, lib-event, lib-task, lib-repo, lib-io, lib-mail, and lib-schema. Use when looking up Enonic XP library functions, parameter shapes, return types, or usage examples. Do not use for Guillotine GraphQL queries, content type schema definitions, Enonic CLI commands, or non-Enonic JavaScript APIs.
license: MIT
metadata:
  author: webmaxru
  version: "1.1"
---

# Enonic XP Server-Side API Reference

## Procedures

**Step 1: Identify the Target Library**

1. Determine which `/lib/xp/*` library the query relates to.
2. Map the library to the appropriate reference file:

   | Library | Reference File |
   |---------|---------------|
   | lib-content | `references/lib-content-reference.md` |
   | lib-node | `references/lib-node-reference.md` |
   | lib-auth | `references/lib-auth-reference.md` |
   | lib-portal | `references/lib-portal-reference.md` |
   | lib-context, lib-event, lib-task | `references/lib-context-reference.md` |
   | lib-io, lib-mail, lib-repo, lib-schema | `references/lib-utilities-reference.md` |

3. If the query spans multiple libraries or asks for a usage pattern, read `references/examples.md`.

**Step 2: Look Up the Function**

1. Read the identified reference file.
2. Locate the specific function by name.
3. Extract the following details:
   - **Signature:** Function name and import path.
   - **Parameters:** Name, type, required/optional, default value, description.
   - **Return type:** Type and shape of the returned value.
   - **Example:** Code snippet demonstrating correct usage.

**Step 3: Provide the Answer**

1. Present the function signature with its import statement.
2. Include the parameter table with types and descriptions.
3. Include the return type and shape.
4. Add a usage example. If the reference file includes one, use it. Otherwise, compose a minimal working example consistent with the documented signature.
5. Note any version requirements (e.g., "Requires XP 7.8.0+").

**Step 4: Handle Cross-Library Patterns**

1. If the query involves combining multiple libraries (e.g., "create content as admin"), read `references/examples.md` for established patterns.
2. If a pattern is not documented, compose it by combining individual function signatures from the relevant reference files.

**Step 5: Troubleshoot Common Issues**

1. If the query describes an error or unexpected behavior, read `references/troubleshooting.md`.
2. Match the error message or symptom to a known issue.
3. Provide the documented fix and any version-compatibility notes.

**Step 6: Generate Import Blocks**

1. If the user needs a reusable import block, read `assets/enonic-imports.template.ts`.
2. Uncomment only the libraries required for the user's controller.

## Error Handling

- If a function is not found in any reference file, report that it may belong to a community library or a newer XP version not yet documented, and suggest checking https://developer.enonic.com/docs/xp/stable/api.
- If the query relates to Guillotine/GraphQL, content type schemas, or Enonic CLI, indicate that this skill does not cover those topics.
- If a version mismatch is suspected, consult the version compatibility table in `references/troubleshooting.md`.
