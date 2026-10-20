---
globs: "**/*.md"
alwaysApply: false
---

Before generating content for any *.md file, validate all claims against the repository's actual files using tools like `read_file`, `grep_search`, or `file_glob_search`. If a fact cannot be verified against the repo's state, refuse to generate content for that file.
