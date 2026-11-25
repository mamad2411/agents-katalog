# Reddit Intel

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://docs.anthropic.com/en/docs/claude-code)
[![Powered by Trellis](https://img.shields.io/badge/Powered%20by-Trellis-blue)](https://github.com/mindfold-ai/Trellis)

一套 Claude Code skill，帮你从 Reddit 挖掘竞品情报和用户痛点。直接、高效、数据驱动。

## 它能做什么

这套工具包含 5 个独立的 Claude Code skill，通过 Exa 搜索 Reddit，将用户语言、社区、帖子、评论转化为结构化的 JSONL 数据流，最终生成一份可操作的产品竞争分析报告。

```
/reddit-kw           /reddit-sub          /reddit-fp           /reddit-ac
keywords.jsonl  -->  subreddits.jsonl --> posts.jsonl     -->  comments.jsonl
```

## 核心命令

| 命令 | 功能 |
|------|------|
| `/reddit-intel-init` | 首次初始化：创建目录、配置文件、产品上下文模板 |
| `/reddit-kw` | 从 Reddit 用户语言中发现痛点关键词 |
| `/reddit-sub` | 找到目标用户活跃的社区 |
| `/reddit-fp` | 搜索匹配关键词的痛点帖子（支持传参如 `/reddit-fp context loss`） |
| `/reddit-ac` | 分析评论区：竞品提及、用户原话、未满足需求 |

## 数据示例

**keywords.jsonl**
```json
{"keyword": "context loss", "category": "pain", "reddit_usage": "Claude keeps forgetting my project context", "source": "r/ClaudeAI"}
```

**subreddits.jsonl**
```json
{"name": "r/ClaudeAI", "tier": 1, "members": "451K", "promo_policy": "discussion OK", "strategy": "Pain-point replies"}
```

**posts.jsonl**
```json
{"title": "200K context just ain't cutting it", "subreddit": "r/ClaudeAI", "upvotes": 85, "pain_category": "context_loss", "product_solution": "Layered context architecture"}
```

**comments.jsonl** (三种类型)
```json
{"type": "competitor", "content": "I switched to Cursor when hitting token limits", "competitor": "Cursor", "sentiment": "positive"}
{"type": "language", "content": "compacting process straight-up nukes crucial context"}
{"type": "need", "content": "Need persistent memory across sessions"}
```

## 安装

### 前置条件
- Claude Code
- Exa MCP server（Reddit 屏蔽了 Anthropic 爬虫）

Exa MCP 配置示例（添加到 `~/.claude.json` 或 `.claude/settings.json`）：
```json
{
  "mcpServers": {
    "exa": {
      "command": "npx",
      "args": ["-y", "exa-mcp-server"],
      "env": { "EXA_API_KEY": "去 exa.ai 申请" }
    }
  }
}
```

### 安装 skill
```bash
git clone https://github.com/SamCuipogobongo/reddit-intel ~/.claude/skills/reddit-intel
for cmd in reddit-intel-init reddit-kw reddit-sub reddit-fp reddit-ac; do
  ln -s ~/.claude/skills/reddit-intel/commands/$cmd ~/.claude/skills/$cmd
done
```

## 配置

初始化后会在项目根目录生成 `.reddit-intel.json`：

```json
{
  "data_dir": "./reddit-intel/data",
  "product_name": "YourProduct",
  "product_context": "./reddit-intel/product-context.md",
  "language": "zh"
}
```

字段说明：
- `data_dir`: JSONL + Markdown 文件存放目录
- `product_name`: 渲染 Markdown 标题时使用
- `product_context`: 你填写好的产品上下文文件路径
- `language`: `en` 或 `zh`，所有输出标签自动切换

## 快速上手

1. `/reddit-intel-init` 初始化项目
2. 填写 `product-context.md`（描述你的产品、目标用户、核心价值）
3. 依次运行：
   - `/reddit-kw` 发现关键词
   - `/reddit-sub` 定位社区
   - `/reddit-fp` 收集痛点帖子
   - `/reddit-ac` 分析评论洞察

## 真实案例：Trellis

`examples/trellis/` 包含为 [Trellis](https://github.com/mindfold-ai/Trellis)（开源 AI 开发框架）收集的真实数据：

- **45 个关键词**：发现了 "context rot"、"AI amnesia"、"compacting nukes context" 等用户真实用语
- **53 个社区**：r/ClaudeAI, r/ClaudeCode, r/ChatGPTCoding 为 tier 1；r/LocalLLaMA, r/cursor 为 tier 2
- **44 个帖子**：context_loss 是 #1 痛点分类；1M context window 并没有解决问题
- **54 条评论洞察**：竞品包括 Cursor、Obsidian vaults、devctx MCP、Ember MCP；"250-500K token 后质量下降"

完整案例见 [`examples/trellis/product-context.md`](examples/trellis/product-context.md)。

## 仓库结构

```
reddit-intel/
├── commands/                          # 5 个独立 Claude Code skill
│   ├── reddit-intel-init/SKILL.md     # /reddit-intel-init
│   ├── reddit-kw/SKILL.md            # /reddit-kw
│   ├── reddit-sub/SKILL.md           # /reddit-sub
│   ├── reddit-fp/SKILL.md            # /reddit-fp
│   └── reddit-ac/SKILL.md            # /reddit-ac
├── scripts/
│   └── jsonl_ops.py                   # 共享脚本：append, render, stats, init
├── references/
│   ├── step-details.md                # 每个 step 的详细搜索策略
│   ├── product-context.template.md    # 英文模板
│   └── product-context.template.zh.md # 中文模板
├── examples/
│   └── trellis/                       # 真实案例
│       ├── product-context.md
│       ├── keywords.jsonl             # 45 keywords
│       ├── subreddits.jsonl           # 53 subreddits
│       ├── posts.jsonl                # 44 posts
│       └── comments.jsonl             # 54 comments
├── SKILL.md                           # 完整参考
└── LICENSE                            # MIT
```

## Built with Trellis

<p align="center">
  <img src="https://raw.githubusercontent.com/mindfold-ai/Trellis/main/assets/trellis.png" alt="Trellis" width="600">
</p>

reddit-intel 是使用 [Trellis](https://github.com/mindfold-ai/Trellis) 开发的 —— 一个开源的 AI 开发框架，让 Claude Code 和 Cursor 真正理解你的代码库。

如果你喜欢 reddit-intel 的 skill 架构，Trellis 可以帮你构建更多类似的自动化工作流。

```bash
npm install -g @mindfoldhq/trellis@latest
```

## License

MIT — Sam Cui, 2026
