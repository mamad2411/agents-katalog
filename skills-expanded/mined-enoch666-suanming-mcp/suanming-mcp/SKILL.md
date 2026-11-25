---
name: suanming-mcp
description: 玄机阁算命 — 八字排盘、六爻起卦、灵签抽签、姓名打分、起名、程序员黄历。传统中国风水墨 HTML 命理报告，Claude Code / Codex / Cursor / Windsurf 通用 MCP Server。
metadata:
  type: skill
  provider: MCP Server
  package: suanming-mcp
  topics:
    - fortune-telling
    - bazi
    - chinese-metaphysics
    - mcp-server
    - claude-code
    - programmer-humor
---

# 玄机阁算命 MCP Server (suanming-mcp)

传统中国风 × 程序员整活风 MCP Server，六大算命功法，每算必出水墨 HTML 命理报告。

## 六大功法

| Tool | 功能 | 输入 | 风格 |
|------|------|------|------|
| `fortune_bazi` | 八字排盘 | 出生年月日时 + 性别 | 传统 |
| `fortune_liuyao` | 六爻起卦 | 心中问题（可选） | 传统 |
| `fortune_qian` | 灵签抽签 | 心中问题（可选） | 传统 |
| `fortune_name` | 姓名打分 | 姓名（2-4字） | 传统 |
| `fortune_mingming` | 起名 | 姓氏 + 生辰 | 传统 |
| `fortune_coder` | 程序员黄历 | 编程语言 | 整活 |

## 快速开始

### 安装

```bash
npm install -g suanming-mcp
```

### 配置 Claude Code

在 `.mcp.json` 或 `~/.claude/.mcp.json` 中添加：

```json
{
  "mcpServers": {
    "suanming": {
      "command": "npx",
      "args": ["-y", "suanming-mcp"]
    }
  }
}
```

### 使用

直接用自然语言对话触发：

- "帮我算个八字，1990年5月20日上午10点出生，男"
- "起个卦问问事业前程"
- "抽个签看看财运"
- "分析一下'张三'这个名字"
- "姓李，2024年3月15日生，帮我起几个名字"
- "今天适合写Python吗"

## 视觉特色

每次算命结果生成**水墨风格 HTML 页面**：
- 宣纸纹理背景（CSS 噪点叠加）
- 毛笔书法标题（Google Fonts 马山正）
- 朱砂印章（"玄机阁印"）
- 八卦符号（Unicode ☰☱☲☳☴☵☶☷）
- 竖排签文、淡入动画

## 使用场景

| 场景 | 适用程度 | 说明 |
|------|----------|------|
| 学习传统命理 | 很适合 | 从八字排盘、六爻、签文多角度了解 |
| 程序员日常整活 | 很适合 | 程序员黄历宜忌幽默、Bug率/摸鱼指数 |
| 起名参考 | 适合 | 八字五行补缺生成候选名、五格打分 |
| 娱乐消遣 | 很适合 | 抽签、黄历轻松有趣 |
| 专业命理 | 不适合 | 仅供娱乐参考，不提供个人化命理建议 |
| 医疗诊断 | 绝对不适合 | 算命 ≠ 医疗行为 |

## 安全与免责

本项目仅供娱乐参考，不作为个人化命理建议。涉及医疗、投资、法律等重要决策，请咨询相关专业人士。详见 [USE_AND_RISK_NOTICE.md](./docs/USE_AND_RISK_NOTICE.md)。

## 开发

```bash
git clone https://github.com/Enoch666/suanming-mcp.git
cd suanming-mcp
npm install
npm run build
```

## License

MIT © 2026
