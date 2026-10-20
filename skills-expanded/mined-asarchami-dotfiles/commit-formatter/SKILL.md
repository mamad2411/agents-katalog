---
name: commit-formatter
description: Format and create git commits following Conventional Commits
---

When asked to commit (or when committing as part of your workflow), follow
this process:

1. Run `git diff --staged` to see what's staged. If nothing is staged, run
   `git add -A` to stage all changes, then diff again.

2. Determine the commit type from the changes:
   - `feat` — new functionality
   - `fix` — bug fix
   - `docs` — documentation only
   - `refactor` — code restructuring, no behavior change
   - `test` — adding or updating tests
   - `chore` — build, config, dependencies, tooling
   - `style` — formatting, whitespace, naming

3. Identify the scope — the primary area affected (a module name, component,
   or subsystem). Omit scope if changes span the whole project.

4. Write the commit message in this format:

   ```
   <type>(<scope>): <summary in imperative mood, ≤72 chars>

   What changed:
   - <concrete change 1>
   - <concrete change 2>

   Why:
   <1-2 sentences explaining the motivation, not restating the what>
   ```

5. Run `git commit` with the formatted message.

Rules:
- Summary line: imperative mood ("add", not "added"), no period at end
- Body: always include both What and Why sections
- Keep the summary under 72 characters
- If changes don't fit a single type, split into multiple commits
