---
name: bundled-skill-file-extraction
description: "Lazily extract referenced files for bundled skills so large prompts stay offline until needed."
metadata:
  author: ychampion
---

# SKILL: Bundled Skill File Extraction
**Domain:** command-surfaces  
**Trigger:** Use whenever a bundled skill needs reference files extracted on demand while keeping startup fast.
**Source Pattern:** Distilled from reviewed command-surface and listing-control patterns.

## Core Method
When a bundled skill defines `files`, memoize an extraction promise and write each file under a secure directory (with O_NOFOLLOW / 0o700+ permissions). Cache the extraction path so the same directory can be reused across invocations, and wrap the skill prompt with `Base directory for this skill: <dir>` so the agent can Read/Grep as needed without bloating the inline instructions.

## Key Rules
- Group requested files by parent directory when writing so mkdir/disk writes happen per subtree.
- Allocate per-process directories under the locked `getBundledSkillsRoot()` and avoid overwriting by using `O_EXCL`/`SAFE_WRITE_FLAGS`.
- Memoize the extraction promise (not just the result) so concurrent invocations await a single write.
- Prepend `Base directory ...` to the skill prompt only when the extraction succeeded; otherwise continue without the prefix to keep the skill usable.

## Example Application
When packaging a bundled “project review” skill with large README snippets, add `files` entries for the README, let this method extract them lazily, and cite the base directory in the prompt so the agent can `Read` the files only when it actually runs the skill.

## Anti-Patterns (What NOT to do)
- Don’t write the files directly during startup—delay until the first invocation, using memoized promises to avoid race conditions.
- Don’t forget to guard against traversal (`resolveSkillFilePath`) so bad relpaths cannot escape the extraction dir.
