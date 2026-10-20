---
description: Apply this rule when working with configuration files (e.g.,
  `.flake8`, `pyproject.toml`) to avoid overwriting existing content or
  misidentifying file paths.
alwaysApply: false
---

Always verify file paths using read-only tools (e.g., `ls`, `find`, or `grep`) before making any edits. When modifying configuration files, append new content instead of overwriting existing data. Use tools like `echo`, `sed`, or `read_file` to ensure minimal, atomic changes. If the user clarifies file locations (e.g., 'Files are in the root'), adjust the plan immediately without asking for further confirmation.