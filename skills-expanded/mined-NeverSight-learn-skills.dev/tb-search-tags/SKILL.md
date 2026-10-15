---
name: tb-search-tags
description: 搜索组织标签
allowed-tools: Bash(node *)
---

# 搜索标签

## 执行步骤

1. 用 `AskUserQuestion`（单选，2 个 option：查看全部 / 按关键词搜索）询问用户
2. 如果选择"按关键词搜索"，在对话中问用户"请输入搜索关键词"，等用户回复
3. 执行：
```bash
node ${CLAUDE_SKILL_DIR}/scripts/tb-api.mjs search-tags [--keyword <关键词>]
```
4. 以表格展示：标签ID(id)、名称(name)、颜色(color)
