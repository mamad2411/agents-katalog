# Repo Ref
- source: https://github.com/island-dev-crew/uncle-bob-skills (path: scripts/fixtures/bad-island/nonstring-metadata/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: text: This description is a YAML mapping, not a string. Its repr is long enough that a validator measuring len(str(desc)) reads it as a well-sized description and passes.
