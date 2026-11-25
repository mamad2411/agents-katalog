# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/s/sql-index-optimizer-multi-db/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 当用户希望“通过建表语句 + 慢 SQL 自动优化索引”时使用此 Skill，支持 MySQL、Oracle、PostgreSQL。脚本使用 Python，自动解析 DDL 与慢 SQL 中的 WHERE/JOIN/ORDER BY 列，生成候选索引及对应数据库的 CREATE INDEX 语句，并输出到文件。
