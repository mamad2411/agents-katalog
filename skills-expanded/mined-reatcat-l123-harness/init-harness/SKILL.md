---
name: init-harness
description: 在当前项目初始化 L1-L2-L3 三级记忆骨架（CLAUDE.md 常驻层、.agents/INDEX.md 索引、.agents/ 详情目录、门禁清单、模板）。当用户说"初始化 harness"、"装上三级记忆"、"init harness"、"给这个项目上记忆系统"，或新项目希望启用本插件方法论时使用。
---

# Init Harness —— 装机程序

把 L1-L2-L3 方法论骨架装进当前项目。骨架是**引擎生成的数据**：装完后项目自己积累知识，插件不再参与。

## 步骤

### 1. 前置检查
- 确认当前工作目录就是目标项目根（用户没指定就用 cwd）。
- 如果项目已有 `CLAUDE.md` 或 `.agents/`，**不要覆盖**：脚本本身永不覆盖已存在文件，但你要先看一眼现状，向用户说明哪些会新建、哪些会跳过。

### 2. 执行装机脚本

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/init-harness/init.sh" "<项目根绝对路径>"
```

脚本会创建（不覆盖）：
- `CLAUDE.md` —— L1 常驻层模板
- `.agents/INDEX.md` —— L2 索引模板
- `.agents/gate.conf` —— 门禁保护清单
- `.agents/{current,inbox,events,knowledge,pitfalls,runbooks,templates,archive}/`
- `.agents/templates/` —— spec/plan/pitfall/knowledge/runbook 模板
- `.agents/README.md`、`.agents/inbox/README.md`

### 3. 陪同用户完成三件事（不要跳过）

1. **审 L1 安全底线**：打开新生成的 `CLAUDE.md`，把「安全底线」一节逐条读给用户，按项目实际补充专有红线（例如：专用设备、禁止触碰的分支、数据不可编造的具体口径）。
2. **审门禁清单**：展示 `.agents/gate.conf` 默认保护项，问用户要不要增删。
3. **建议首个 git 提交**：骨架应入库，建议 `git add CLAUDE.md .agents` 并提交（提交信息由用户确认）。

### 4. 说明日常循环（一段话讲完即可）

- 干活：读 L2 索引按指针走；过程状态写 `.agents/current/notes.md`。
- 踩坑：修完用 `.agents/templates/pitfall-template.md` 记录，**提议**加入 L2 索引（需审批，改受保护文件要门禁令牌）。
- 提炼：定期跑 `event-review` 技能（/l123-harness:event-review）做周审。

## 纪律
- 绝不覆盖已有文件；冲突一律报告给用户裁决。
- 不在骨架里预填任何项目知识——空的表头就是对的。
