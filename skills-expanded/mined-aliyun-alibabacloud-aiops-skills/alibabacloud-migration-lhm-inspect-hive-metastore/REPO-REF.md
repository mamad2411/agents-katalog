# Repo Ref
- source: https://github.com/aliyun/alibabacloud-aiops-skills (path: skills/playbooks/wadaps/alibabacloud-migration-lhm-inspect-hive-metastore/SKILL.md, branch: master)
- mined: 2026-09-20
- desc: 执行 Hive 数据表探查任务，支持全量探查和增量探查，提供两种连接方式：DB 直连（通过 Metastore MySQL/PostgreSQL 数据库）和 Thrift 直连（通过 HMS Thrift API 端口 9083）。全量探查导出所有表的元数据、存储大小和 DDL；增量探查识别指定时间节点之后的表创建、结构变更、数据变更和分区变更。使用场景：用户提到"Hive 探查"、"全量探查"、
