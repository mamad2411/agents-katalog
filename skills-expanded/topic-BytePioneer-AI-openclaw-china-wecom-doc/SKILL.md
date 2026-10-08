---
name: wecom-doc
description: 当用户提到企业微信文档、智能表格、创建文档、编辑文档、写文档时启用。优先复用 wecom channel 自动写入的文档 MCP 配置，并通过 mcporter 调用文档能力。
metadata:
  {
    "openclaw":
      {
        "emoji": "📄",
        "always": true,
        "requires":
          {
            "bins": ["mcporter"],
          },
        "install":
          [
            {
              "id": "mcporter",
              "kind": "node",
              "package": "mcporter",
              "bins": ["mcporter"],
              "label": "Install mcporter (npm)",
            },
          ],
      },
  }
---

# 企业微信文档 MCP

这个 skill 只负责通过 `mcporter` 调用企业微信文档 MCP，不要直接调用企业微信 Wedoc API。

## 使用时机

- 用户要创建企业微信文档
- 用户要创建企业微信智能表格
- 用户要编辑机器人创建的企微文档或智能表格

## 前置检查

### 1. 检查 mcporter

先确认 `mcporter` 可执行。若未安装，提示用户安装；用户同意后执行：

```bash
npm install -g mcporter
```

安装完成后继续后续步骤，不要停在中间。

### 2. 确认 wecom-doc MCP 已配置

先执行：

```bash
mcporter list wecom-doc --output json
```

如果已经能正常返回 tool 列表，直接进入调用阶段。

如果返回 `server not found`、`unknown server` 或类似错误，读取：

```bash
~/.openclaw/wecomConfig/config.json
```

检查是否存在 `mcpConfig.doc.type` 和 `mcpConfig.doc.url`。若存在，执行：

```bash
mcporter config add wecom-doc --type "<type>" --url "<url>"
```

添加完成后再次执行 `mcporter list wecom-doc --output json` 进行验证。

### 3. 自动配置失败时的引导

如果本地没有 `mcpConfig.doc`，说明当前 wecom 长连接还没成功拉到文档 MCP 配置。此时：

- 如果能读取到 `channels.wecom.botId`，提示用户去企业微信授权当前机器人文档权限
- 或让用户直接发送 `StreamableHttp URL` / `JSON Config`

当用户提供 URL 或 JSON Config 后，提取 `url` 并执行：

```bash
mcporter config add wecom-doc --type streamable-http --url "<url>"
```

配置完成后重新执行 `mcporter list wecom-doc --output json`，然后继续用户原始请求。

## 调用规则

- 所有请求必须通过 `mcporter call wecom-doc.<tool> --args '{...}' --output json` 执行
- 先用 `mcporter list wecom-doc --output json` 读取实际 tool 列表，不要硬编码 tool 名称和参数结构
- `create_doc` 返回的 `docid` 要保存在当前会话里，后续编辑操作依赖它
- 如果用户要编辑已有文档，但当前会话里没有机器人创建时返回的 `docid`，直接输出：

> 仅支持对机器人创建的文档进行编辑

## 文档工作流

### 新建普通文档

1. 调用 `create_doc`，传 `doc_type: 3`
2. 保存返回的 `docid`
3. 如需写内容，调用 `edit_doc_content`

### 新建智能表格

1. 调用 `create_doc`，传 `doc_type: 10`
2. 保存返回的 `docid`
3. 根据需要继续调用智能表格相关 tool

## 错误处理

- 如果 `mcporter call` 返回 `help_message`，优先把其中面向用户的说明直接输出给用户
- 如果返回 `850001`，说明还需要用户提供配置或授权，按上面的配置引导继续处理
- 如果返回 `daemon not running` 或 `connection refused`，提示用户先执行：

```bash
mcporter daemon start
```
