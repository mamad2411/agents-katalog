# Repo Ref
- source: https://github.com/eosphoros-ai/DB-GPT (path: assets/retired-suites/db-ops/skills/safe-ddl-review/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 受控 DDL 评审技能。对任何结构变更（ADD/DROP INDEX、ADD COLUMN、改主键、OPTIMIZE、分区、归档搬迁）做破坏性分级 L0-L3、锁影响与耗时预估、复制延迟风险评估、在线 DDL 方案选型（INPLACE/LOCK=NONE、gh-ost、pt-online-schema-change）、回滚预案与审批要求判定；生产环境 DDL 默认拒绝，仅输出提案。触发词包括"DD
