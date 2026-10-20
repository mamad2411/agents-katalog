---
name: code-post
description: Run post-development actions script
---

Executes the post-dev-actions.bat script to run automated tasks after development work.

## Usage

```
/code-post
```

## Implementation

```bash
./code-post.sh
```

This command will:
- Execute the post-dev-actions.bat script from the current directory
- Show the output and exit status
- Handle any errors that occur during execution

Use this command after completing development tasks, code changes, or when you need to run automated post-development workflows like commits, testing, or cleanup.