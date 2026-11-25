---
name: chrono-onboarding
description: Chrono AI 非技术团队 onboarding — 安装 NyxID CLI, 配置 AI 工具 MCP, 克隆战略仓库, 运行每日更新
version: 1.0.0
license: MIT
compatibility: Claude Code, Cursor, OpenAI Codex, Windsurf, any MCP-compatible AI tool
metadata:
  category: plain
  tag:
    - onboarding
    - nyxid
    - chrono-ai
    - team
    - mcp
---

# Chrono AI 团队 Onboarding

本技能引导 Chrono AI 非技术团队成员完成环境搭建, 让你可以用 AI 工具参与公司战略协作。

完成后你将拥有:
- NyxID CLI (公司的 Agent Connectivity Gateway)
- AI 工具通过 MCP 连接 NyxID
- 公司战略仓库 (chrono-ai-ceo), 可以运行 /daily 查看你的工作看板

## 使用方法

当用户说 "onboarding"、"设置环境"、"安装 NyxID" 时, 按下面的步骤引导。每一步完成后确认, 再进入下一步。

---

## Step 1: 检查基础环境

先检查用户的系统环境:

```bash
echo "=== 系统检查 ==="
echo "OS: $(uname -s)"
echo "Shell: $SHELL"
which git 2>/dev/null && echo "git: OK" || echo "git: 未安装"
which cargo 2>/dev/null && echo "cargo: OK" || echo "cargo: 未安装 (NyxID 需要)"
which gh 2>/dev/null && echo "gh: OK" || echo "gh: 未安装 (GitHub CLI)"
```

### 缺少工具时的安装指引

**git** (必须):
- macOS: `xcode-select --install`
- Windows: 下载 https://git-scm.com

**cargo** (NyxID 编译需要):
- 所有平台: `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
- 安装后重启终端, 运行 `cargo --version` 确认

**gh** (GitHub CLI, 用于 /daily):
- macOS: `brew install gh`
- Windows: `winget install GitHub.cli`
- 然后运行: `gh auth login`

## Step 2: 安装 NyxID CLI

```bash
cargo install nyxid-cli
```

安装完成后验证:

```bash
nyxid --version
```

应该显示 `nyxid 0.1.0` 或更高版本。

## Step 3: 注册并登录 NyxID

如果你还没有 NyxID 账号:

```bash
nyxid register
```

按提示输入邮箱和密码。注册后验证邮箱。

已有账号直接登录:

```bash
nyxid login
```

登录后确认身份:

```bash
nyxid whoami
```

## Step 4: 配置 AI 工具的 MCP 连接

NyxID 可以作为 MCP Server 连接到你的 AI 工具。根据你使用的工具选择:

### Claude Code (推荐)

```bash
nyxid mcp config --tool claude-code
```

这会自动写入 Claude Code 的 MCP 配置。重启 Claude Code 即可使用。

### Cursor

```bash
nyxid mcp config --tool cursor
```

配置会写入 Cursor 的 MCP settings。重启 Cursor 生效。

### 其他 MCP 兼容工具

```bash
nyxid mcp config --tool <tool-name>
```

运行 `nyxid mcp config --help` 查看支持的工具列表。

### 验证 MCP 连接

配置完成后, 在 AI 工具中确认 NyxID MCP 已连接。你应该能看到 NyxID 提供的工具 (如 proxy, service 管理等)。

## Step 5: 克隆战略仓库

```bash
cd ~
git clone https://github.com/ChronoAIProject/chrono-ai-ceo.git
cd chrono-ai-ceo
```

这是公司的战略仓库, 包含:
- `strategy/goals.md` — 公司北极星和里程碑
- `products/` — 每个产品线的战略文档
- `internal/` — 内部文档 (团队分配、运营)
- `team.yaml` — 团队成员和产品线映射

## Step 6: 确认你在 team.yaml 中

```bash
grep -A 5 "$(gh api user --jq '.login' 2>/dev/null)" team.yaml
```

你应该能看到你的名字、Lark ID、角色和产品线。如果找不到, 联系 CEO 添加。

## Step 7: 运行每日更新

在战略仓库目录下, 用你的 AI 工具运行:

```
/daily
```

这会生成你的个人化工作看板, 包含:
- 公司路线图 (所有人一致)
- 你的产品线状态
- 你的待办事项
- 建议优先级

## 常见问题

### NyxID 安装失败

如果 `cargo install nyxid-cli` 失败:
1. 确保 Rust 是最新版: `rustup update`
2. macOS 需要 Xcode CLI tools: `xcode-select --install`
3. 如果编译太慢, 耐心等待 (首次编译约 5-10 分钟)

### gh auth 失败

```bash
gh auth login --web
```

用浏览器完成 GitHub 认证。确保你的 GitHub 账号已加入 ChronoAIProject org。

### /daily 找不到我

确认 `gh api user --jq '.login'` 返回的用户名在 team.yaml 中。如果不在, 联系 CEO。

### MCP 连接不上

1. 确认 NyxID 已登录: `nyxid whoami`
2. 重新生成配置: `nyxid mcp config --tool <your-tool>`
3. 重启 AI 工具

## 完成

恭喜! 你现在可以:
- 用 AI 工具通过 NyxID 访问公司服务
- 在战略仓库中查看公司方向和你的工作安排
- 每天运行 /daily 保持战略对齐
