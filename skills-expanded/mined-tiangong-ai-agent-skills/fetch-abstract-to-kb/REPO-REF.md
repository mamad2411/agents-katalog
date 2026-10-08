# Repo Ref
- source: https://github.com/tiangong-ai/agent-skills (path: fetch-abstract-to-kb/SKILL.md, branch: main)
- mined: 2026-09-20
- desc: Fetch DOI candidates from PostgreSQL `journals` and batch write `abstract` by DOI. Use when you need DB-only backfill workflow: (1) select newest rows where doi is not empty, author is not empty, and 
