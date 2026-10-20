# SCALE Engine 治理规则（自动生成）

本项目由 SCALE Engine 治理。AI 行为受以下约束：

1. **Role 必须激活**：执行任务前先 `scale role activate <role>`
2. **Artifact 必须有上游**：创建 Plan 前 Spec 必须 FROZEN
3. **声称完成前必须验证**：修代码后必须跑 test/lint
4. **不准甩锅**：说"环境问题"前必须有 ≥2 个验证证据

## 可用 Roles
- Explorer / SpecWriter / Planner / Implementer / Verifier / Releaser

## 关键命令
- `scale create <type> <title>` - 创建 Artifact
- `scale transition <id> --to <action>` - 状态迁移
- `scale role activate <name>` - 切换 Role
- `scale lesson recall "查询"` - 召回历史经验
