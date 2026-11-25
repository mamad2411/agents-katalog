# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/mined-kjuhwa-skills-hub/chunked-resource-id-batch-fetch/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: Split large ID lists into ~1000-item chunks before querying DB or Elasticsearch to avoid bind-parameter limits (MSSQL 2100, Oracle 1000) and OOM on bulk responses
