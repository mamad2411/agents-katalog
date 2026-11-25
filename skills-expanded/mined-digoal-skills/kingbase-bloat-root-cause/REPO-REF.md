# Repo Ref
- source: https://github.com/digoal/skills (path: kingbase/kingbase-bloat-root-cause/SKILL.md, branch: main)
- mined: 2026-11-23
- desc: KingbaseES（金仓）表/索引膨胀根因诊断专家。当用户提供 KingbaseES 实例连接信息（主机、端口、用户名、密码）并希望排查表膨胀、索引膨胀、死元组过多、autovacuum 不生效、vacuum 卡住等问题时触发。KingbaseES 默认采用 PG 兼容模式，因此与 PostgreSQL 共享大量 `pg_stat_*` / `pg_catalog` 视图，但 KingbaseE
