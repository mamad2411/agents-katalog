---
name: agent-browser
description: AI 浏览器自动化工具 - 无头浏览器 + 元素分析 + 自动化操作
metadata:
  {
    "openclaw":
      {
        "emoji": "🌐",
        "requires": { "bins": ["agent-browser"] },
        "install":
          [
            {
              "id": "install-agent-browser",
              "kind": "npm",
              "pkg": "agent-browser",
              "label": "Install Agent Browser",
            }
          ],
      },
  }
---

# Agent Browser

AI 浏览器自动化工具，基于 Playwright 的 CLI，支持元素分析、截图、自动化操作。

## 环境要求

- Node.js + npm
- 已安装 Playwright 浏览器 (首次运行自动下载)

## 安装

```bash
npm install -g agent-browser
agent-browser install  # 下载 Chromium
```

## 使用方法

### 基本命令

| 命令 | 说明 |
|------|------|
| `agent-browser open <url>` | 打开网页 |
| `agent-browser snapshot` | 获取页面元素树 (带 AI 引用) |
| `agent-browser click <ref>` | 点击元素 (@e1, @e2...) |
| `agent-browser fill <ref> <text>` | 填写表单 |
| `agent-browser type <ref> <text>` | 输入文本 |
| `agent-browser screenshot` | 截图 |
| `agent-browser find <role> <name>` | 查找元素 |
| `agent-browser press <key>` | 按键 (Enter, Tab, Escape...) |
| `agent-browser scroll <dir>` | 滚动 (up/down/left/right) |
| `agent-browser wait <selector\|ms>` | 等待元素或时间 |
| `agent-browser eval <js>` | 执行 JavaScript |
| `agent-browser pdf <path>` | 保存为 PDF |

### 常用参数

| 参数 | 说明 |
|------|------|
| `--session-name <name>` | 保存/恢复会话状态 |
| `--profile <path>` | 浏览器配置文件 |
| `--color-scheme dark` | 暗色模式 |
| `--full` | 完整页面截图 |
| `--annotate` | 带标注的截图 |
| `-i` | 仅交互元素 |

### 命令链式调用

用 `&&` 链式调用（浏览器状态保持）：

```bash
# 打开页面 + 等待加载 + 截图分析
agent-browser open example.com && agent-browser wait --load networkidle && agent-browser snapshot

# 登录示例
agent-browser open login.example.com && agent-browser fill @e1 "user@email.com" && agent-browser fill @e2 "password" && agent-browser click @e3

# 滚动 + 截图
agent-browser open example.com && agent-browser scroll down 500 && agent-browser screenshot
```

## 输出示例

### snapshot 输出

```
# 页面: Example Domain

@example1 [link] Example Domain
@example2 [heading] Example Domains
@example3 [paragraph] This domain is for use in illustrative examples in documents...
...
```

### find 示例

```bash
agent-browser find role button --name Submit
# 输出: @e5 [button] Submit
```

## 会话管理

```bash
# 保存会话
agent-browser --session-name mytask open example.com

# 恢复会话
agent-browser --session-name mytask snapshot

# 删除会话
agent-browser session delete mytask
```

## 完整工作流示例

```bash
# 1. 打开网页
agent-browser open https://www.example.com

# 2. 等待加载
agent-browser wait --load networkidle

# 3. 获取页面元素
agent-browser snapshot

# 4. 点击登录按钮
agent-browser click @e5

# 5. 填写表单
agent-browser fill @e1 "username"
agent-browser fill @e2 "password"

# 6. 提交
agent-browser press Enter

# 7. 截图确认
agent-browser screenshot result.png
```

## 注意事项

1. **元素引用时效**：每次 snapshot 后元素引用可能变化，需重新获取
2. **等待加载**：动态内容建议用 `wait --load networkidle`
3. **会话复用**：复杂流程用 `--session-name` 保存状态，中断后可恢复

---

*基于 agent-browser CLI*
