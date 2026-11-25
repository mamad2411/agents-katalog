---
name: supermap-wiki-read
description: 完整阅读 Supermap wiki 页面内容。包括页面文字、图片列表、评论，并递归解析引用的其他 wiki 页面。使用方法：/supermap-wiki-read <wiki URL 或 pageId>
disable-model-invocation: false
allowed-tools: Bash
---

# Wiki Read Skill

完整阅读 Supermap Confluence wiki 页面内容，包括页面文字、图片列表、评论，并递归解析引用的其他 wiki 页面。

## 使用方法

当用户想要完整阅读 wiki 页面内容时，使用此技能。

### 基本用法

```bash
/supermap-wiki-read <wiki URL 或 pageId>
```

### 示例

- `/supermap-wiki-read https://wiki.ispeco.com/pages/viewpage.action?pageId=210641700` - 读取指定 wiki 页面
- `/supermap-wiki-read 210641700` - 使用 pageId 直接读取
- `/supermap-wiki-read https://wiki.ispeco.com/pages/viewpage.action?pageId=210641700 --depth 2` - 限制递归深度为 2 层

## 功能特性

1. **页面内容获取**: 获取完整的页面文字内容并转换为 markdown
2. **图片提取**: 提取页面中实际显示的图片（不包括附件列表中的其他文件）
3. **评论获取**: 获取页面的所有评论，包括作者和时间
4. **递归解析**: 自动解析页面中引用的其他 wiki 页面

## 工作原理

1. 从 `SUPERMAP_WIKI_TOKEN` 环境变量读取认证 token
2. 调用 Confluence REST API 获取页面内容
3. 解析 HTML 提取图片和 wiki 链接
4. 获取页面评论
5. 递归处理引用的 wiki 页面（最大深度可配置）
6. 输出格式化的 markdown 内容

## 执行脚本

使用 Bash 工具运行 Node.js 脚本：

```bash
node .claude/skills/supermap-wiki-read/scripts/read_wiki.js "<wiki URL 或 pageId>"
```

可选参数：
- `-d, --depth`: 递归解析的最大深度（默认 3）
- `--no-comments`: 不获取评论
- `--no-images`: 不提取图片

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

```markdown
# {页面标题}

**空间**: {space名称}
**链接**: {wiki URL}

---

## 页面内容

{清理后的 markdown 内容}

## 页面图片

| # | 文件名 | 下载链接 |
|---|--------|----------|
| 1 | xxx.png | https://... |

## 评论 ({数量}条)

### 评论 1
**作者**: xxx
**时间**: xxx
**内容**: xxx

---

## 引用页面

### {引用页面标题}

{递归内容...}
```

## API 端点

- **页面内容**: `GET /rest/api/content/{pageId}?expand=body.storage,space,version`
- **评论**: `GET /rest/api/content/{pageId}/child/comment?expand=body.storage,history`
- **图片下载**: `GET /download/attachments/{pageId}/{filename}`

## 错误处理

脚本会处理以下错误情况：

1. **缺少 token**: 提示用户设置 `SUPERMAP_WIKI_TOKEN`
2. **认证失败 (401)**: 提示检查 token 是否正确
3. **权限不足 (403)**: 提示用户可能没有访问权限
4. **页面不存在 (404)**: 提示检查 pageId 或 URL 是否正确
5. **网络错误**: 提示检查网络连接
6. **无效 URL**: 提示 URL 格式错误

## 故障排除

### 问题：提示"SUPERMAP_WIKI_TOKEN environment variable is not set"

**解决方案**: 确保已正确设置环境变量。可以在 shell 配置文件（如 `~/.bashrc` 或 `~/.zshrc`）中添加 export 语句使其持久化。

### 问题：认证失败

**解决方案**:
1. 确认 token 没有过期
2. 确认 token 有正确的权限
3. 从 wiki 设置中重新生成 token

### 问题：页面内容不完整

**解决方案**:
1. 检查是否有权限访问该页面
2. 某些内容可能需要特殊权限才能查看

### 问题：递归解析过深

**解决方案**: 使用 `--depth` 参数限制递归深度，例如 `--depth 1` 只解析直接引用的页面。

## 技术细节

- **API 端点**: `https://wiki.ispeco.com/rest/api/content`
- **认证方式**: Bearer Token
- **返回格式**: Markdown
- **依赖**: Node.js 内置模块（https），无需安装额外依赖
- **递归深度**: 默认最大 3 层，可配置
- **跨平台**: 支持 Linux、macOS、Windows