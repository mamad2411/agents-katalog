---
name: organize-imports
description: Sorts, groups and prunes imports in your changed files to match the project convention, then proves nothing broke.
disable-model-invocation: true
---

Organize the imports in the changed files. Scope or extra rules: $ARGUMENTS

1. Run `git diff --name-only HEAD` to get the files. Limit yourself to source files in that list.
2. Find the project's convention: look for an ESLint import/order rule, isort or ruff config, goimports, a Prettier plugin, or `.editorconfig`. If a tool exists, run it in fix mode on those files only. Otherwise infer the order from three untouched files.
3. Typical order: standard library, third-party, project aliases, relative paths, with a blank line between groups and alphabetical inside each.
4. Remove imports that nothing uses. Check for side-effect imports and type-only imports before deleting.
5. Never reorder imports whose order matters, such as polyfills or CSS that must load first. Leave a comment-marked block alone.

Run the type checker or build and the tests. Show `git diff --stat` and mention any file you skipped and why. Do not commit.
