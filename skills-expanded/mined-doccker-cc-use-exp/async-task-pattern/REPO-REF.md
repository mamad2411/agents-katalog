# Repo Ref
- source: https://github.com/doccker/cc-use-exp (path: .gemini/skills/async-task-pattern/SKILL.md, branch: main)
- mined: 2026-09-20
- desc: 当 API/任务可能执行超过 10 秒（批量数据处理、远程 API 批量调用、全表扫描、跨租户聚合）时触发。防止同步接口被网关 30s 超时切断、用户重复点击触发并发、状态缓存内存泄漏等问题。提供异步任务状态机标准模板。
