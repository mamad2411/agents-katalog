---
name: supermap-jira-read
description: 读取 Supermap Jira 问题的详情。用于获取单个 Jira issue 的完整信息。使用方法：/supermap-jira-read <Jira URL 或 Issue Key>
---

# Supermap Jira Read

该技能用于读取 Supermap Jira 系统中单个问题的详细信息。

## 使用方法

### 通过 Claude Skill 调用

```
/supermap-jira-read <Jira URL 或 Issue Key>
```

### 直接运行脚本

```bash
node scripts/read_jira.js <Jira URL 或 Issue Key>
```

示例：
```bash
node scripts/read_jira.js ISVJ-11474
node scripts/read_jira.js "https://jira.supermap.work/browse/ISVJ-11474"
```

## 参数

- `Jira URL`: 完整的 Jira 问题链接，例如 `https://jira.supermap.work/browse/ISVJ-11474`
- `Issue Key`: Jira 问题 key，例如 `ISVJ-11474`

## 环境变量

- `SUPERMAP_JIRA_TOKEN`: Jira API 认证令牌

## 输出信息

- 基本信息（key、标题、状态、优先级等）
- 描述
- 报告人和负责人
- 组件和版本
- 附件列表
