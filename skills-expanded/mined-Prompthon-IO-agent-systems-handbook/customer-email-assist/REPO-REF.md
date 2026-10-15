# Repo Ref
- source: https://github.com/Prompthon-IO/agent-systems-handbook (path: zh-Hans/case-studies/examples/customer-email-assist-starter/skill/SKILL.md, branch: main)
- mined: 2026-10-14
- desc: 用 connector-first、最少 token 的方式审阅 Gmail 客户支持线程。适用于 Codex 需要通过 Codex Gmail connector 读取 Gmail、把清洗后的消息导入本地 SQLite 问题队列、先执行确定性的清洗和分类、只把模型调用保留给 JSON-only 的消息理解和草稿字段生成，并支持 dashboard 审阅、客户审批与排队回复处理的时候。
