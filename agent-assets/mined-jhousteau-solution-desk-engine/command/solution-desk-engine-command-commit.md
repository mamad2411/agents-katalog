---
name: commit
description: Create a git commit using genesis commit with smart commit validation
---

<role>
You are a helpful assistant creating clean, well-structured git commits using Genesis's smart commit system.
</role>

<instructions>
When the user asks you to commit changes, follow these steps:

1. **Check git status** to see what files have been modified
2. **Review the changes** using git diff to understand what was done
3. **Check recent commits** to follow the repository's commit message style
4. **Create a commit** using `genesis commit -m "<message>"`

The Genesis smart commit system will automatically:
- Run code formatting (black)
- Run linting checks (ruff)
- Run type checking (mypy)
- Run pre-commit hooks
- Validate file counts for AI safety
- Ensure tests pass
- Detect secrets
</instructions>

<process>
1. First, check the current status:
   ```bash
   git status
   ```

2. Review the changes to understand what was modified:
   ```bash
   git diff --stat
   git diff HEAD~1 --stat  # If some files were already staged
   ```

3. Look at recent commits to match the style:
   ```bash
   git log --oneline -5
   ```

4. Stage files if needed:
   ```bash
   git add <files>  # Only if there are untracked files that should be included
   ```

5. Create the commit using Genesis:
   ```bash
   genesis commit -m "<descriptive message>"
   ```

   The message should:
   - Start with a verb (Add, Update, Fix, Refactor, etc.)
   - Be concise but descriptive
   - Follow the repository's existing style
   - Focus on the "what" and "why", not the "how"
</process>

<examples>
**Example 1: Feature addition**
```bash
genesis commit -m "Add SOLVE interaction monitoring system for pipeline analysis"
```

**Example 2: Bug fix**
```bash
genesis commit -m "Fix validation error in scaffold phase orchestrator"
```

**Example 3: Refactoring**
```bash
genesis commit -m "Refactor monitoring module to use pre/post hooks pattern"
```

**Example 4: Documentation**
```bash
genesis commit -m "Update SOLVE monitoring documentation with usage examples"
```

**Example 5: Configuration change**
```bash
genesis commit -m "Configure monitoring to use native Genesis logging"
```
</examples>

<best-practices>
- Always review changes before committing
- Use genesis commit, not git commit directly
- Let smart-commit handle formatting and validation
- Don't commit if tests are failing
- Keep commits focused on a single logical change
- Write messages that will be helpful to future developers
</best-practices>

<notes>
- Genesis commit will run quality checks automatically
- If pre-commit hooks fail, fix the issues and retry
- The smart commit system ensures AI-safe file counts
- Commits are automatically signed if configured
</notes>
