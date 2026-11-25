# Repo Ref
- source: https://github.com/milodule3-debug/aura-code (path: .qwen/skills/en/silent-require-failure-in-electron-ai/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: When Electron main-process AI features fail with "Offline" despite valid API keys, check whether the `openai` npm package is installed — a silent `require('openai')` inside try/catch returns null and 
