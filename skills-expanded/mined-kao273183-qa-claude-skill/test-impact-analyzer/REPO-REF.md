# Repo Ref
- source: https://github.com/kao273183/qa-claude-skill (path: skills/test-impact-analyzer/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: Test Impact Analysis（TIA）——從 git diff 算出這次改動影響到哪些測試，PR 時只跑受影響的子集，大幅砍 CI 時間。支援 coverage-based（pytest-testmon / xccov / JaCoCo / jest --findRelatedTests）、dependency-graph（nx affected / Gradle / Bazel）、p
