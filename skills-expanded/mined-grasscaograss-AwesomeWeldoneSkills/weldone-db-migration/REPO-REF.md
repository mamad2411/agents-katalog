# Repo Ref
- source: https://github.com/grasscaograss/AwesomeWeldoneSkills (path: weldone-db-migration/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: Weldone 数据库迁移守护 skill；当拉取最新代码、实体/DbContext/配置出现数据库字段或表结构变化、运行时报缺列/缺表/模型快照不一致、或 AI 准备直接修改数据库/schema 来“补字段”时使用。强制先检查 EF Core 迁移状态并优先执行 just update-db；执行 just migrate 前必须先 dump PostgreSQL 到动态 APPDATA 备份目
