# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/mined-NeverSight-learn-skills.dev/lazy-import-refactor/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: Refactor module-level imports of heavy native dependencies (torch, tensorflow, jax) to function-internal lazy imports. Use when a library import triggers SIGSEGV or slow startup in environments where 
