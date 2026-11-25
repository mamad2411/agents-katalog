# Repo Ref
- source: https://github.com/softwareone-platform/mpt-extension-skills (path: skills/mpt-ext-task-fix-pre-commit-failures/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: Fix failures raised by the pre-commit hook during `git commit` (not standalone make/test runs). Reads hook output, fixes one failure at a time, reruns, and retries the commit; max 5 iterations.
