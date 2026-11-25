---
name: supermap-jira-search
description: 搜索 Supermap Jira 查找问题。用于查找 Jira issues、bug 报告或任务。使用方法：/supermap-jira-search <搜索词>
---

# Supermap Jira 搜索技能

搜索 Supermap Jira 系统中的 issues，并以 markdown 表格格式返回结果。

## 使用方法

```
/supermap-jira-search <搜索关键词>
```

**示例：**
- `/supermap-jira-search iServer` - 搜索与 iServer 相关的 issues
- `/supermap-jira-search "bug fix"` - 搜索包含 "bug fix" 的 issues
- `/supermap-jira-search DSG-123` - 搜索特定编号的 issue

## 前置要求

需要设置 `SUPERMAP_JIRA_TOKEN` 环境变量：

```bash
# Linux/macOS
export SUPERMAP_JIRA_TOKEN='your-jira-token-here'

# Windows (PowerShell)
$env:SUPERMAP_JIRA_TOKEN='your-jira-token-here'

# Windows (Command Prompt)
set SUPERMAP_JIRA_TOKEN=your-jira-token-here
```

## 输出格式

搜索结果以 markdown 表格形式呈现：

| 标题 | 链接 |
| --- | --- |
| 问题标题 | https://jira.supermap.work/browse/ISSUE-123 |

## 执行方式

Claude 应该使用 Bash 工具执行 Node.js 脚本：

```bash
node .claude/skills/supermap-jira-search/scripts/search_jira.js "<搜索词>"
```

脚本会：
1. 检查 `SUPERMAP_JIRA_TOKEN` 环境变量
2. 调用 Jira API 进行搜索
3. 过滤只显示 issue 结果（忽略项目等其他结果）
4. 将结果格式化为 markdown 表格

## 错误处理

### Token 未设置
如果 `SUPERMAP_JIRA_TOKEN` 未设置，脚本会提示用户设置该环境变量。

### 网络错误
如果无法连接到 Jira 服务器，会显示网络错误信息。

### 认证失败
如果 token 无效或已过期，会提示认证失败。

### 无结果
如果没有找到匹配的 issues，会显示 "No issues found."

## 技术细节

- **API 端点**: `https://jira.supermap.work/rest/quicksearch/1.0/productsearch/search`
- **认证方式**: Bearer Token
- **结果过滤**: 只返回 `id == "quick-search-issues"` 的结果
- **依赖**: Node.js 内置模块（https），无需安装额外依赖
- **跨平台**: 支持 Windows、macOS、Linux