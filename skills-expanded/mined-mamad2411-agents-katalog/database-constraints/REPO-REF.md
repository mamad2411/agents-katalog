# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/mined-0xbb2b-bb-spec/database-constraints/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 关系型数据库 schema 与访问约定——UUIDv7 应用层主键；`deleted` 微秒时间戳软删 + UNIQUE 联合；created_at/updated_at 由 DB 管理；全链路 UTC。触发：编写/修改 .sql、migration、DDL；设计表结构或数据模型。跳过：非关系型存储（Redis/MongoDB/ES）、不动 schema 的查询调优、代码生成物。
