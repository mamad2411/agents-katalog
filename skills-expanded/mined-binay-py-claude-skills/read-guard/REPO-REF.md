# Repo Ref
- source: https://github.com/binay-py/claude-skills (path: skills/read-guard/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: Stop Claude Code from filling its context window with whole-file reads of huge files and log dumps. A PreToolUse hook that denies Read of files over ~800 lines / 80 KB without offset/limit, and `cat` 
