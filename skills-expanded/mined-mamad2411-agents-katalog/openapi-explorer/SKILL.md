---
name: openapi-explorer
description: OpenAPI/Swagger 文档解析工具。当用户询问 API 文档、接口定义、需要根据 Swagger 生成代码时激活。支持按模块、路径精准提取接口信息，避免加载大文档导致上下文溢出。
license: MIT
metadata:
  author: nnnnzs
  version: "1.0.0"
---

# OpenAPI Explorer

OpenAPI/Swagger 文档解析工具，专为 AI 代理设计，支持按需精准提取接口信息，避免上下文溢出。

## 脚本路径

所有脚本位于本技能目录下的 `scripts/` 子目录。代理应使用相对于 SKILL.md 所在目录的路径调用：
```
{SKILL_DIR}/scripts/{script-name}.py
```
其中 `{SKILL_DIR}` 为本文件所在目录的绝对路径。

## 何时激活此技能

当用户提到以下内容时激活：
- "swagger"、"openapi"、"api 文档"
- "根据文档生成 API 调用代码"
- "查询接口定义"、"获取接口信息"
- "查看某个模块的接口"
- 提供了 swagger/openapi URL

## 核心策略

OpenAPI 文档通常很大（可能数 MB），直接读取会导致上下文溢出。采用以下策略：

### 1. 分块读取
- 只读取需要的部分（paths、components、tags）
- 使用 JSON 路径过滤，避免加载整个文档
- 按 tag 或 path 精准定位

### 2. 渐进式披露
- 先获取概览（tags、paths 列表）
- 根据用户需求逐步获取详情
- 遇到 $ref 再解析引用的 schema

### 3. 按需加载
- 不一次性读取所有接口
- 只读取用户明确需要的接口定义
- 批量获取相关 schemas 时限制数量

### 4. 零依赖
- 使用 Python 标准库（urllib），无需安装额外依赖
- 跨平台兼容，Python 3 通常已预装
- Claude Code CLI 可以直接调用，无需配置环境

## 工作流程

### 第一步：获取文档概览

当用户首次询问 Swagger 文档时，先获取基本信息：

**使用 Python 脚本**（无需安装依赖）：
```bash
python3 scripts/fetch-tags.py {swagger-url}
```

**预期输出**：
```json
{
  "title": "API 文档标题",
  "version": "1.0.0",
  "tags": ["user", "order", "product"]
}
```

向用户展示可用的模块（tags），让用户选择。

### 第二步：按需获取接口

根据用户选择的模块或具体路径，获取接口列表：

**按模块获取**：
```bash
python3 scripts/fetch-by-tag.py {swagger-url} {tag-name}
```

**按路径获取**：
```bash
python3 scripts/fetch-endpoint.py {swagger-url} "{path}"
```

### 第三步：获取接口详情

获取具体接口的完整定义（parameters、requestBody、responses）：

```bash
python3 scripts/fetch-endpoint.py {swagger-url} "{path}" {method}
```

### 第四步：解析引用

如果接口定义中包含 `$ref`，提取并获取相关的 schema：

```bash
# 先将接口定义保存到临时文件
echo '{...endpoint_json...}' > /tmp/endpoint.json

# 解析所有 $ref
cat /tmp/endpoint.json | python3 scripts/resolve-refs.py {swagger-url}
```

### 第五步：生成代码

根据获取到的接口定义，生成相应的代码：
- TypeScript/JavaScript (fetch/axios)
- Python (requests)
- cURL 命令
- 其他语言

## 输出格式

向用户展示接口信息时，使用以下格式：

```markdown
## 接口：{summary}

**路径**: `{method} {path}`
**描述**: {description}
**标签**: {tags}

### 请求参数
| 参数名 | 类型 | 位置 | 必填 | 说明 |
|--------|------|------|------|------|
| ... | ... | ... | ... | ... |

### 请求体
{request body 示例}

### 响应
| 状态码 | 说明 |
|--------|------|
| 200 | {description} |

### 数据结构
{相关 schema 的说明}
```

## 重要注意事项

1. **避免读取整个文档**：永远不要使用 `fetch(swaggerUrl).then(r => r.json())` 然后读取整个 doc
2. **优先使用脚本**：使用提供的 Python 脚本，它们已经实现了分块读取
3. **限制输出大小**：如果某个接口的返回值过大，询问用户需要哪些具体字段
4. **缓存策略**：如果用户查询多个接口，可以缓存文档到 `/tmp/swagger-{timestamp}.json`
5. **错误处理**：如果脚本执行失败，检查 URL 是否正确、是否有网络问题

## 常见命令速查

```bash
# 获取所有模块
python3 scripts/fetch-tags.py {url}

# 获取模块下的接口列表
python3 scripts/fetch-by-tag.py {url} {tag}

# 获取接口详情
python3 scripts/fetch-endpoint.py {url} {path} {method}

# 获取 schema 定义
python3 scripts/fetch-schema.py {url} {SchemaName}

# 解析 $ref 引用
echo '{...}' | python3 scripts/resolve-refs.py {url}
```

## 参考文档

遇到问题或需要代码模板时，按需查阅：

- **故障排除** - 见 [references/troubleshooting.md](references/troubleshooting.md)
- **代码生成示例** - 见 [references/code-examples.md](references/code-examples.md)
- [OpenAPI 3.0 规范](https://spec.openapis.org/oas/v3.0.0)
