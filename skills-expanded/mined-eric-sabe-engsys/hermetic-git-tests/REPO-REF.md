# Repo Ref
- source: https://github.com/eric-sabe/engsys (path: core/skills/hermetic-git-tests/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: Keep tests and tools that shell out to git from touching the enclosing repository when run from a git hook. A pre-push hook exports GIT_DIR, so a child `git init` or `git config` inside a test rewrite
