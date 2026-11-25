# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/mined-pmb2-hermes-starter/windows-cron-msys-path-fix/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: Fix .sh scripts in cron jobs that fail on Windows due to MSYS backslash stripping. Cron resolves relative paths to C:\... and passes them to bash, which strips backslashes as escape characters.
