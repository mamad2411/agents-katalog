---
name: supermap-youtrack-search
description: 搜索 Supermap YouTrack 查找问题。用于查找 YouTrack issues、任务或缺陷报告。使用方法：/supermap-youtrack-search <搜索词>
---

# Supermap YouTrack 搜索技能

搜索 Supermap YouTrack 系统中的 issues，并以 markdown 表格格式返回结果。

## 使用方法

```
/supermap-youtrack-search <搜索关键词>
```

**示例：**
- `/supermap-youtrack-search test` - 搜索与 test 相关的 issues
- `/supermap-youtrack-search "bug fix"` - 搜索包含 "bug fix" 的 issues
- `/supermap-youtrack-search CS-4408` - 搜索特定编号的 issue
- `/supermap-youtrack-search project: CloudGIS` - 使用 YouTrack 查询语法搜索

## 前置要求

需要设置 `SUPERMAP_YOUTRACK_TOKEN` 环境变量：

```bash
# Linux/macOS
export SUPERMAP_YOUTRACK_TOKEN='your-youtrack-token-here'

# Windows (PowerShell)
$env:SUPERMAP_YOUTRACK_TOKEN='your-youtrack-token-here'

# Windows (Command Prompt)
set SUPERMAP_YOUTRACK_TOKEN=your-youtrack-token-here
```

## 输出格式

搜索结果以 markdown 表格形式呈现：

| 标题 | 链接 |
| --- | --- |
| iManager alpha 出包出镜像&测试包 | http://yt.ispeco.com:8099/issue/CS-4408 |

## 执行方式

Claude 应该使用 Bash 工具执行 Node.js 脚本：

```bash
node .claude/skills/supermap-youtrack-search/scripts/search_youtrack.js "<搜索词>"
```

脚本会：
1. 检查 `SUPERMAP_YOUTRACK_TOKEN` 环境变量
2. 调用 YouTrack API 进行搜索
3. 将结果格式化为 markdown 表格

## 错误处理

### Token 未设置
如果 `SUPERMAP_YOUTRACK_TOKEN` 未设置，脚本会提示用户设置该环境变量。

### 网络错误
如果无法连接到 YouTrack 服务器，会显示网络错误信息。

### 认证失败
如果 token 无效或已过期，会提示认证失败。

### 无结果
如果没有找到匹配的 issues，会显示 "No issues found."

## 技术细节

- **YouTrack 地址**: `http://yt.ispeco.com:8099`
- **API 端点**: `GET /api/issues`
- **认证方式**: Bearer Token
- **依赖**: Node.js 内置模块（http），无需安装额外依赖
- **跨平台**: 支持 Windows、macOS、Linux