---
name: supermap-wiki-writer
description: 向 Supermap Wiki 写入内容。支持创建新页面或修改现有页面，可指定模板页面保持样式一致。使用方法：/supermap-wiki-writer <操作> <参数>
disable-model-invocation: false
allowed-tools: Bash
---

# Wiki Write Skill

向 Supermap Confluence Wiki 写入内容，支持创建新页面或修改现有页面。可使用现有页面作为模板，自动保持样式一致。

## 使用方法

当用户需要向 wiki 写入内容时使用此技能。

### 基本用法

```bash
# 创建新页面
/supermap-wiki-writer create --space <空间key> --title <标题> --content <内容文件路径> --template <模板pageId>

# 修改现有页面
/supermap-wiki-writer update --pageId <pageId> --content <内容文件路径> --template <模板pageId>

# 使用模板创建页面（保持样式一致）
/supermap-wiki-writer create --space PDC --title "我的文档" --content ./content.md --template 215849520
```

### 参数说明

**create 命令（创建新页面）:**
- `--space`: 空间 key（如 PDC, ~liuxin1）
- `--title`: 页面标题
- `--content`: 内容文件路径（markdown 格式）
- `--template`: （可选）模板页面 pageId，将自动转换内容格式以匹配模板

**update 命令（修改现有页面）:**
- `--pageId`: 要更新的页面 ID
- `--content`: 内容文件路径（markdown 格式）
- `--template`: （可选）模板页面 pageId，将自动转换内容格式以匹配模板

### 示例

```bash
# 创建新页面
/supermap-wiki-writer create --space ~liuxin1 --title "季度总结" --content ./summary.md

# 使用模板创建页面（保持样式一致）
/supermap-wiki-writer create --space ~liuxin1 --title "季度总结" --content ./summary.md --template 215849520

# 更新现有页面
/supermap-wiki-writer update --pageId 210659947 --content ./summary.md

# 使用模板更新页面
/supermap-wiki-writer update --pageId 210659947 --content ./summary.md --template 215849520
```

## 功能特性

1. **创建新页面**: 在指定空间创建新 wiki 页面
2. **修改现有页面**: 更新已有页面的内容和标题
3. **模板样式保持**: 可指定模板页面，自动将内容转换为模板的 storage 格式
4. **自动版本管理**: 更新页面时自动递增版本号

## 工作原理

1. 从 `SUPERMAP_WIKI_TOKEN` 环境变量读取认证 token
2. 如指定了 `--template`，获取模板页面的 storage 格式作为参考
3. 将 markdown 内容转换为 Confluence storage XHTML 格式
4. 调用 Confluence REST API 创建或更新页面
5. 返回操作结果和页面链接

## 执行脚本

使用 Bash 工具运行 Node.js 脚本：

```bash
# 创建新页面
node .claude/skills/supermap-wiki-writer/scripts/write_wiki.js create --space <空间> --title <标题> --content <文件路径> [--template <pageId>]

# 更新现有页面
node .claude/skills/supermap-wiki-writer/scripts/write_wiki.js update --pageId <pageId> --content <文件路径> [--template <pageId>]
```

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

**创建成功:**
```
Page created successfully!
Title: {页面标题}
Page ID: {pageId}
Version: 1
Link: https://wiki.ispeco.com/pages/viewpage.action?pageId={pageId}
```

**更新成功:**
```
Page updated successfully!
Title: {页面标题}
Page ID: {pageId}
Version: {新版本号}
Link: https://wiki.ispeco.com/pages/viewpage.action?pageId={pageId}
```

## 错误处理

脚本会处理以下错误情况：

1. **缺少 token**: 提示用户设置 `SUPERMAP_WIKI_TOKEN`
2. **认证失败 (401)**: 提示检查 token 是否正确
3. **权限不足 (403)**: 提示用户可能没有写入权限
4. **页面不存在 (404)**: 更新时提示检查 pageId 是否正确
5. **空间不存在**: 创建时提示检查空间 key 是否正确
6. **参数错误**: 提示缺少必需参数

## 故障排除

### 问题：提示"SUPERMAP_WIKI_TOKEN environment variable is not set"

**解决方案**: 确保已正确设置环境变量。

### 问题：创建页面时提示空间不存在

**解决方案**:
1. 确认空间 key 正确（区分大小写）
2. 确认 token 有权限访问该空间
3. 个人空间 key 格式为 `~username`

### 问题：内容格式与模板不一致

**解决方案**:
- 确保正确指定 `--template` 参数
- 模板页面必须是有效的 wiki 页面
- 某些复杂宏可能无法完全复制

## 技术细节

- **API 端点**: `https://wiki.ispeco.com/rest/api/content`
- **认证方式**: Bearer Token
- **内容格式**: Confluence Storage XHTML
- **依赖**: Node.js 内置模块（https、fs、path），无需安装额外依赖
- **跨平台**: 支持 Linux、macOS、Windows

## Markdown 转 Storage 格式说明

脚本会自动进行以下转换：

| Markdown | Storage XHTML |
|----------|---------------|
| `# 标题` | `<h1><strong><span>标题</span></strong></h1>` |
| `## 标题` | `<h2><strong><span>标题</span></strong></h2>` |
| `**粗体**` | `<strong>粗体</strong>` |
| `*斜体*` | `<em>斜体</em>` |
| `- 列表项` | `<ul><li><span>列表项</span></li></ul>` |
| `\| 表格 \|` | `<table class="wrapped">...</table>` |
| 换行 | `<br/>` |

注意：指定 `--template` 时，会参考模板的实际 storage 格式，而非上述默认转换。
