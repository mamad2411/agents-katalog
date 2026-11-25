# Repo Ref
- source: https://github.com/kao273183/qa-claude-skill (path: skills/flaky-test-hunter/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 從 CI 跑歷史紀錄統計每個測試的失敗率，識別 flaky test（重跑就過的不穩定測試）、給出修復建議、自動標記到 quarantine（隔離區）讓 CI 不被假失敗阻擋。支援 GitHub Actions / GitLab CI / CircleCI / Jenkins JUnit XML / pytest-xdist 失敗紀錄。當使用者提到「flaky test / 不穩定測試 / 假失敗
