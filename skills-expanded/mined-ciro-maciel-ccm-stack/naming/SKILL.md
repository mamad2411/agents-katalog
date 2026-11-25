---
name: naming
description: Name code, files, routes and commits the same way everywhere, screens in the reader's language, and rename without collisions. Use when naming or renaming.
---

# Names and language

## The boundary is who reads it

Identifiers, file names, routes, comments and commit messages are in **English**: their readers are developers and tools. Everything a person reads on screen, in an e-mail or in a notification is in **that person's language**. The line is the audience, not "string or not string".

Renaming by search-and-replace cannot see that line. Replacing `search` across a codebase once turned `aria-label="Limpar busca"` into `aria-label="Limpar search"`. After any rename, search for mixed-language phrases in user-facing text.

## Casing

| Kind | Style | Example |
|---|---|---|
| Variable, function, JSON field | camelCase | `userId`, `loadPosts()` |
| Class, component | PascalCase | `PostEditor` |
| Module constant | SCREAMING_SNAKE | `MAX_RETRIES` |
| File | kebab-case | `post-editor.js` |
| Route segment | kebab-case, English | `/posts/{id}/edit` |

- **`Id`, never `ID`**: `userId`, `getById`.
- **Booleans ask a yes/no question and are affirmative**: `isOpen`, `hasAccess`, `canEdit`, `shouldRetry`. Never `notReady` or `disabled` as a boolean name.

## Records are addressed by their stable id

Routes, API paths, webhooks and public links use the record's UUID: `/posts/0b5c…/edit`, never `/post/12`. A per-account counter is a display label. A slug the customer chooses is fine for public pages.

## Commits

[Conventional Commits](https://www.conventionalcommits.org): `type(scope): summary in the imperative, lower case, no final period`. Types: `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `build`, `ci`, `chore`, `style`, `revert`. A hook checks the subject line of every `git commit -m`.

## Before a bulk rename

1. List every occurrence of the old name, and every existing occurrence of the new name.
2. Where the new name already exists with another meaning, stop and pick a different one.
3. Rename object keys at the call sites together with the function signature: a renamed parameter with old keys at the call site breaks only at runtime.
4. Run the tests and search for mixed-language text before you commit.
