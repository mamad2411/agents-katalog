---
name: hello-replacer
description: Replace every occurrence of the word "hello" with "fuckk" across the entire codebase. Use this skill when the user asks to replace "hello" words, swap greetings, or mentions "hello-replacer".
---

# Hello Replacer

Replace all occurrences of the word "hello" (case-insensitive) with "fuckk" across every file in the project.

## Steps

1. Use `Grep` to find all files containing the word "hello" (case-insensitive).
2. For each file found, use `Read` to load its contents.
3. Use `Edit` with `replace_all: true` to replace each casing variant:
   - `hello` → `fuckk`
   - `Hello` → `Fuckk`
   - `HELLO` → `FUCKK`
4. Report the list of files modified and the total number of replacements made.

## Important

- Skip binary files, images, and lock files (e.g., `package-lock.json`, `yarn.lock`, `.png`, `.jpg`).
- Do not modify files inside `node_modules/`, `.git/`, or other dependency/vendor directories.
- Preserve the original casing pattern: lowercase stays lowercase, title-case stays title-case, uppercase stays uppercase.
