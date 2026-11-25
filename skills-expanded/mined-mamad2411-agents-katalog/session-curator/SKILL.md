---
name: session-curator
description: Use near session end or when the user asks to curate durable project knowledge, reconcile docs and memory, reduce documentation rot/bloat, or update README.md, AGENTS.md, CLAUDE.md, docs, CONTEXT/MEMORY, or project memory after a confirmed edit plan.
version: 0.1.0
---

# Session Curator

像知识库编辑一样从当前会话中提炼可复用、长期有效、可验证的项目知识，审查文档与记忆是否过期、膨胀或冲突，并在用户确认修改计划后更新项目文档或记忆文档。

## 进入边界

使用本 skill 的前提是用户明确要求整理会话、沉淀记忆、更新项目文档、修正文档腐烂，或 `workflow-router` / 上一轮 `Natural Handoff` 推荐本 skill 且用户确认。会话接近结束、完成实现或看到可整理内容都不是静默写文档的授权。

适用：

- 从当前会话或指定材料中提炼长期有效的 workflow、项目约定、验证命令、架构决策、术语或用户偏好。
- 检查并修正 README、AGENTS、CLAUDE、docs、CONTEXT/MEMORY 或项目记忆里的过期、重复、冲突和膨胀。
- 在用户批准具体计划后同步项目文档、agent 规则或记忆文件。

不适用：

- 只需要跨会话交接给下一位 agent 时，使用 `$handoff`。
- 只需要回答问题、解释代码或总结当前结果时，不写持久文档。
- 用户没有确认修改计划时，不进入文件编辑阶段。

## Language Contract

语言契约：生成的文档和聊天输出默认以中文优先；代码、命令、API 名称、契约字段、ID、专有名词以及必要的技术术语保留英文。用户或目标项目明确要求英文时可以例外，但必须记录原因。

## Pressure Scenarios

1. User says: "把这次会话里值得长期保留的东西整理一下。"
   - Expected skill trigger: 先区分可沉淀内容和一次性过程，再给修改计划。
   - Common failure without skill: 把完整聊天摘要、临时调试过程或过期计划写进项目文档。
   - Behavior this skill must force: 只保留长期有效、可复用、可验证的信息。
2. User says: "这个规则以后都要记住，写到 AGENTS 或 memory。"
   - Expected skill trigger: 先判断受众层级和已有落点，再计划最小 diff。
   - Common failure without skill: 同一事实同时塞进 README、AGENTS 和 memory，制造重复来源。
   - Behavior this skill must force: 选择单一权威落点；能更新旧条目就不追加新条目。
3. User says: "文档有点乱，帮我收一收。"
   - Expected skill trigger: 做尺寸和腐烂体检，优先精简、合并或删除过期内容。
   - Common failure without skill: 继续追加新 section，让文档更臃肿。
   - Behavior this skill must force: 减优于加；无法证明长期价值时报告无需修改。

## 核心规则

- 修改任何文件前，必须先列出具体修改计划并等待用户确认。
- 只沉淀通用部分：稳定约定、重复出现的 workflow、项目结构知识、验证命令、长期决策、术语、用户明确偏好的项目级规则。
- 不沉淀一次性过程、临时调试细节、过期计划、聊天寒暄、未验证猜测、隐私信息、secrets、tokens、passwords 或完整对话转录。
- 优先更新已有文档和已有 section；只有用户确认且没有合适落点时才创建新记忆文档。
- 保留项目既有写作风格、语言约定和 heading 层级；不要把文档改成另一套体系。
- 减优于加，合并优于追加，删除过期内容优于保留历史包袱。
- 如果没有值得沉淀的通用内容，明确报告“无需修改”，不要为了产出而改文档。

## References

- 选择文档受众、候选文件和跨文档影响时，使用 `references/document-targets.md`。
- 过滤沉淀内容、检查文档腐烂、控制膨胀和敏感信息时，使用 `references/curation-quality.md`。

## 工作流程

1. 明确整理范围。
   - 默认范围是当前对话。
   - 如果用户指定了某段会话、某些文件或某个主题，只整理指定范围。

2. 盘点候选文档。
   - 先列目录再判断：项目根、`docs/`、根目录 Markdown、ADR/decision 目录、项目已有记忆文件。
   - 按 `references/document-targets.md` 选择候选文件和受众层级。
   - 只读取和候选内容相关的文档；不要批量重写所有文档，也不要漏掉明显受影响的文档。
   - 如果项目有 git，先记录 `git status --short`，避免覆盖用户已有改动。
   - 做尺寸体检：如果项目规则或记忆文件已接近臃肿，计划优先精简、迁移或合并，再考虑新增内容。

3. 提炼候选内容。
   - 将会话内容分类为 `workflow`、`project convention`、`architecture/domain decision`、`setup/verification`、`terminology`、`user preference` 或 `skip`。
   - 对每个可沉淀候选写明来源依据、适用范围、目标读者和为什么它不是一次性信息。
   - 按 `references/curation-quality.md` 对不沉淀内容写 skip 原因，特别是敏感信息、临时实验、未确认决策和相对时间。
   - 用 `references/document-targets.md` 的影响矩阵检查是否需要同步上下游文档，或是否应只更新一个权威落点。

4. 输出修改计划并停止等待确认。
   - 不要在确认前调用编辑工具。
   - 如果计划包含多个文件，允许用户选择部分执行。
   - 如果用户修改计划，先复述新的批准范围再编辑。

5. 执行已确认的修改。
   - 只修改用户批准的文件、section 和内容类型。
   - 使用最小 diff；不要顺手整理无关段落。
   - 优先顺序：先更新面向外部读者的 `docs/` / `README.md`，再更新 `AGENTS.md` / `CLAUDE.md`，最后整理记忆。
   - 新信息更新旧条目时直接改旧条目；新增条目前先搜索同义内容，能合并就不追加。
   - 删除已完成临时计划、被新版本取代的事实、重复记忆和相对时间表达。
   - 如果编辑过程中发现新风险或需要新增文件，停止并重新确认。

6. 验证和报告。
   - 运行项目已有的文档或 skill validator；没有专用验证时至少运行 `git diff --check` 并检查 links/headings/metadata。
   - 按 `references/curation-quality.md` 做最终自检。
   - 汇总实际修改、验证命令、跳过项和残留风险。

## 修改计划格式 (Curation Plan)

```markdown
## 会话整理计划 (Session Curation Plan)

- Scope:
- Candidate docs checked:
- Recommendation: edit / no changes / needs user decision
- Size/bloat check:

| ID | Candidate | Audience layer | Target file/section | Change type | Why durable | Risk |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | ... | agent rules / docs / memory | ... | add/update/remove | ... | ... |

## 不沉淀内容 (Skipped)

- ...

请确认要执行的 ID；确认前我不会修改文件。
```

## 完成报告格式

```markdown
## 会话整理结果 (Session Curation Result)

- Approved scope:
- Changed:
- Verified:
- Skipped:
- Residual risk:
```

## 完成标准

- 用户明确调用了本 skill，或通过 `workflow-router` / `Natural Handoff` 推荐后确认进入。
- 文件修改前已给出修改计划，并收到用户确认。
- 只写入长期有效、可复用、可验证的项目知识。
- 已区分 agent 记忆、项目规则和项目文档的不同受众。
- 已优先处理过期、重复、膨胀和相对时间问题。
- 没有泄露敏感信息或转录完整对话。
- 修改范围与用户批准范围一致。
- 已运行可用验证，或说明跳过原因。
