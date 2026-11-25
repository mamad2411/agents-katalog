---
name: docstring-and-typedoc
description: >
  Write effective Python docstrings and TypeScript/JavaScript TSDoc/TypeDoc comments:
  module/class/function contracts, parameters, returns, examples, and doc generation
  configs. Use when docstring style, Google/NumPy/Sphinx docstrings, TSDoc, TypeDoc,
  API docs from comments, or documenting public libraries for owned codebases — pair
  language style packs and code-quality-standards for non-doc concerns.
---

# Docstring and TypeDoc

## Scope And Authorization

- **In scope:** Codebases you maintain; public and internal API documentation.
- **Out of scope:** Documenting proprietary third-party code you may not redistribute; inventing inaccurate API behavior.
- Prefer documenting **public** surfaces thoroughly; keep private helpers concise.
- Do not put secrets, production URLs with credentials, or customer data in examples.
- Pair with `python-style-and-typing`, `typescript-style-and-eslint`, `api-documentation-writing`, `markdown-docs-style`, and `code-quality-standards`.

## When To Use

- Adding or standardizing Python docstrings (Google/NumPy/Sphinx).
- Adding TSDoc for TypeScript libraries consumed by others.
- Generating HTML docs (Sphinx, mkdocs-docstrings, TypeDoc).
- Reviewing PRs for missing parameter/return documentation on public APIs.
- Aligning IDE hover docs with real types.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full OpenAPI external docs | `api-documentation-writing` |
| README/contributor guides | `readme-and-contributing-docs` |
| Type system design | `python-style-and-typing` / TS style skills |
| Comment philosophy only | `comment-writing-standards` |
| Code quality baseline | `code-quality-standards` |

## What good API docs capture

| Element | Content |
| --- | --- |
| Summary | One line: what and why |
| Detail | Behavior, edge cases, side effects |
| Params | Name, type (if not in signature), constraints |
| Returns | Value meaning; empty/None cases |
| Raises/Throws | Expected failure modes |
| Examples | Minimal, copy-pasteable, tested when possible |
| Security | Auth requirements, injection notes if relevant |

## Workflow

### 1. Confirm scope and success criteria

1. Languages, public packages/modules, doc generator choice.
2. Success: public functions have complete docs; CI builds docs; style guide linked.
3. Decide Google vs NumPy vs Sphinx for Python; TSDoc tags for TS.

### 2. Inventory public surface

```bash
# Python packages
rg -n "^def |^async def |^class " -g '*.py' src/ | head
# TypeScript exports
rg -n "^export (async )?function|^export class|^export type" -g '*.ts' src/
```

1. Mark `public` vs `internal` (underscore, `@internal`, package exports map).
2. Prioritize documented exports used by other teams.

### 3. Python docstrings

```python
def fetch_user(user_id: str, *, include_deleted: bool = False) -> User:
    """Return a user by id.

    Looks up the user in the primary store. Deleted users are omitted unless
    ``include_deleted`` is True.

    Args:
        user_id: Stable external identifier (non-empty).
        include_deleted: When True, soft-deleted rows may be returned.

    Returns:
        The matching ``User`` model.

    Raises:
        UserNotFoundError: If no row matches the criteria.
        ValueError: If ``user_id`` is empty.

    Example:
        >>> fetch_user("usr_123").email  # doctest: +SKIP
        'a@example.com'
    """
```

1. Prefer types in signatures; do not duplicate uselessly unless generating Sphinx without napoleon types.
2. Document side effects (DB writes, network).
3. Module docstring: purpose + examples of primary entrypoints.

### 4. TypeScript TSDoc / TypeDoc

```typescript
/**
 * Fetch a user by id from the primary store.
 *
 * @param userId - Stable external identifier (non-empty)
 * @param options.includeDeleted - When true, soft-deleted rows may be returned
 * @returns The matching user
 * @throws {UserNotFoundError} When no row matches
 * @example
 * ```ts
 * const u = await fetchUser("usr_123");
 * console.log(u.email);
 * ```
 * @public
 */
export async function fetchUser(
  userId: string,
  options: { includeDeleted?: boolean } = {},
): Promise<User> {
  // ...
}
```

1. Use `@public` / `@internal` / `@alpha` for API levels.
2. Document generics and complex object params with `@typeParam` / `@param`.
3. Keep comments aligned with types—do not contradict signatures.

### 5. Generator config (sketch)

```json
// typedoc.json sketch
{
  "entryPoints": ["src/index.ts"],
  "out": "docs/api",
  "excludeInternal": true
}
```

```bash
# Python: mkdocs + mkdocstrings or sphinx-apidoc — per project
# CI: fail if docs build fails
```

1. Publish versioned docs with releases.
2. Link from README to API docs.

### 6. Review checklist for PRs

1. New public export has docstring/TSDoc.
2. Changed behavior updates docs same PR.
3. Examples still valid; no secrets.
4. Errors documented.

### 7. Hand off

1. Style choice recorded in CONTRIBUTING.
2. CI doc build + optional docstring lint (pydocstyle, eslint jsdoc rules carefully).
3. Apply `code-quality-standards` for the code itself.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Summary | “Return user by id” | “This function fetches” noise |
| Params | Constraints + units | Repeat names only |
| Types | Signature + short note | Wrong types in prose |
| Examples | Runnable minimal | Stale, untested, secretful |
| Scope | Public APIs deep | 50 lines on private `_tmp` |
| Drift | Docs change with code | Orphan comments |

## Output Checklist

- [ ] Style (Google/NumPy/TSDoc) chosen and documented
- [ ] Public surface inventoried
- [ ] Functions/classes documented with params/returns/errors
- [ ] Examples safe and current
- [ ] Generator config builds in CI
- [ ] `@internal`/private policy clear
- [ ] PR review checklist adopted
- [ ] README links to generated docs
- [ ] No secrets in comments
- [ ] `code-quality-standards` still applied to code

## Rules

- Document contracts, not line-by-line restatements of code.
- Prefer accurate types in signatures; comments add semantics.
- Update docs in the same change as behavior.
- No credentials in examples.
- Language formatting neighbors do not replace this skill for API doc content.
