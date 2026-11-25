---
name: apply-navigation
description: >-
  Inject navigation links into all book files by replacing placeholders with
  resolved prev/next links. Use when applying navigation to book chapters,
  after all drafting is complete, or when fixing navigation links.
---

# Apply Navigation

Replace `{{NAV_HEADER}}` and `{{NAV_FOOTER}}` placeholders in every generated file with fully resolved navigation links. Runs after all files have been drafted.

For the full navigation format specification (link format, placement, edge cases, path resolution), see [references/navigation-config.md](references/navigation-config.md).

## When to Use

- After all chapters, front matter, and back matter have been drafted
- When fixing or regenerating navigation links
- As part of the book finalization process

## Process

1. **Build ordered file list.** From `structure.md` and feature flags, construct the navigation sequence:
   - `preface.md` (when enabled)
   - `introduction.md` (when enabled)
   - Each chapter file in ascending chapter number order
   - `conclusion.md` (when enabled)

2. **For each file**, determine:
   - **Previous**: preceding entry, or `null` for first file
   - **Next**: following entry, or `null` for last file
   - **Outline path**: relative path to `book-outline.md`

3. **Compute relative paths** using the resolution rules in `references/navigation-config.md`:
   - Same directory → just the filename
   - Chapter → book root → prefix `../`
   - Book root → chapters → prefix `chapters/`

4. **Build the navigation line** using the fixed format:
   - Full: `*[← Previous: {{title}}]({{path}}) | [↑ Book Outline]({{outline_path}}) | [Next: {{title}} →]({{path}})*`
   - First file: omit previous link and its trailing separator
   - Last file: omit next link and its leading separator

5. **Inject into each file.**
   - Replace `{{NAV_HEADER}}` with the navigation line
   - Replace `{{NAV_FOOTER}}` with the same navigation line

6. **Write each file** back to its path.

## Output

All generated files updated in place with resolved navigation. No new files created.

## Constraints

- All format details are fixed in `references/navigation-config.md` — this skill does not make formatting decisions.
- Idempotent: running twice produces the same result (R-SYS-7).
- `book-outline.md` does not receive navigation.
