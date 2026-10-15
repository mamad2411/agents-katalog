---
name: supermap-wiki-search
description: 搜索 Supermap wiki 查找文档。用于查找公司文档、流程或技术信息。使用方法：/supermap-wiki-search <搜索词>
disable-model-invocation: false
allowed-tools: Bash
---

# Wiki Search Skill

搜索 Supermap Confluence wiki 并以 markdown 表格格式返回结果。

## 使用方法

当用户想要搜索公司 wiki 文档时，使用此技能。

### 基本用法

```bash
/supermap-wiki-search <搜索词>
```

### 示例

- `/supermap-wiki-search API 文档` - 搜索 API 相关文档
- `/supermap-wiki-search 部署流程` - 搜索部署流程文档
- `/supermap-wiki-search 测试指南` - 搜索测试相关指南

## 工作原理

1. 从 `SUPERMAP_WIKI_TOKEN` 环境变量读取认证 token
2. 调用 `https://wiki.ispeco.com/rest/api/search` API
3. 解析 JSON 响应并格式化为 markdown 表格
4. 返回包含标题、命名空间、摘要和链接的结果

## 执行脚本

使用 Bash 工具运行 Node.js 脚本：

```bash
node .claude/skills/supermap-wiki-search/scripts/search_wiki.js "<搜索词>"
```

可选参数：
- `-l, --limit`: 限制返回结果数量（默认 20）

## 前置条件

必须设置 `SUPERMAP_WIKI_TOKEN` 环境变量：

**Linux/macOS:**
```bash
export SUPERMAP_WIKI_TOKEN='your-token-here'
```

**Windows (cmd):**
```cmd
set SUPERMAP_WIKI_TOKEN=your-token-here
```

**Windows (PowerShell):**
```powershell
$env:SUPERMAP_WIKI_TOKEN='your-token-here'
```

## 输出格式

结果以 markdown 表格形式返回：

| Title | Space | Excerpt |
|-------|-------|---------|
| [文档标题](链接) | 命名空间 | 摘要内容... |

## 错误处理

脚本会处理以下错误情况：

1. **缺少 token**: 提示用户设置 `SUPERMAP_WIKI_TOKEN`
2. **认证失败 (401)**: 提示检查 token 是否正确
3. **权限不足 (403)**: 提示用户可能没有搜索权限
4. **网络错误**: 提示检查网络连接
5. **无结果**: 显示"No results found."

## 故障排除

### 问题：提示"SUPERMAP_WIKI_TOKEN environment variable is not set"

**解决方案**: 确保已正确设置环境变量。可以在 shell 配置文件（如 `~/.bashrc` 或 `~/.zshrc`）中添加 export 语句使其持久化。

### 问题：认证失败

**解决方案**:
1. 确认 token 没有过期
2. 确认 token 有正确的权限
3. 从 wiki 设置中重新生成 token

### 问题：网络错误

**解决方案**:
1. 检查网络连接
2. 确认可以访问 https://wiki.ispeco.com
3. 检查是否需要 VPN 连接

## 技术细节

- **API 端点**: `GET https://wiki.ispeco.com/rest/api/search`
- **认证方式**: Bearer Token
- **返回格式**: Markdown 表格
- **依赖**: Node.js 内置模块（https），无需安装额外依赖
- **跨平台**: 支持 Linux、macOS、Windows