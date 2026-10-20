---
description: "Generate conventional commit message based on staged changes"
allowed-tools: ["Bash", "Read", "Grep"]
---

Analyze the current git staged changes and generate a conventional commit message following these steps:

1. Run `git status` and `git diff --cached` to understand what changes are staged
2. Analyze the nature of changes (feat/fix/docs/style/refactor/test/chore)
3. Generate a concise, descriptive commit message following conventional commits format:
   - Format: `type(scope): description`
   - Types: feat, fix, docs, style, refactor, perf, test, chore
   - Keep description under 50 characters
   - Use imperative mood ("add" not "added")

4. If there are multiple types of changes, suggest splitting into separate commits
5. Present the suggested commit message and ask for confirmation before committing

Example output:
```
feat(auth): add OAuth2 login integration
```

After generating the message, ask if you should proceed with the commit using this message.