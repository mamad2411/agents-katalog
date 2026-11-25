---
name: damc
description: |
  AI时代个人价值评估器（DAMC模型）。自动扫描用户的 AI Agent 环境（Claude Code、Codex、Cursor、Windsurf、Continue、Aider 等），
  量化评估四个维度：蒸馏价值(D)、抗蒸馏指数(A)、AI驾驭能力(M)、职业适配(C)，生成可分享的可视化 HTML 报告。
  兼容所有能运行 Shell 命令的 AI Agent。
  触发条件：用户提到"评估我的价值"、"DAMC"、"distill score"、"蒸馏评估"、"AI能力评估"、
  "我会被AI取代吗"、"我的AI水平"、"蒸馏我"、"值不值得蒸馏"。
---

# DAMC — AI 时代个人价值评估器

> 不是恐吓你会被取代，而是帮你看清自己在 AI 时代的真实坐标。

## 兼容 Agent

DAMC 支持扫描以下 AI Agent 环境（自动检测，无需配置）：

| Agent | 配置目录 | 检测信号 |
|-------|---------|---------|
| Claude Code | `~/.claude/` | skills, hooks, MCP, memory |
| OpenAI Codex | `~/.codex/` | agents, config, sessions |
| Cursor | `~/.cursor/` | rules, extensions, settings |
| Windsurf | `~/.codeium/windsurf/` | rules, cascade config |
| Continue | `~/.continue/` | config, models, rules |
| Aider | `~/.aider*` | config, model settings |
| GitHub Copilot | `~/.config/github-copilot/` | settings, instructions |
| WorkBuddy | `~/.workbuddy/` | config, skills |
| Trae (ByteDance) | `~/.trae/` | rules, extensions, settings |
| 通义灵码 (Lingma) | `~/.lingma/` | config, rules, extensions |
| 豆包 MarsCode | `~/.marscode/` | config, rules, extensions |
| CodeGeeX (智谱) | `~/.codegeex/` | config, chat history |
| Baidu Comate | `~/.comate/` | config, extensions |
| DevChat | `~/.chat/` | config, workflows |

如果用户环境中安装了多个 Agent，则合并扫描，取最高分。

## DAMC 模型

| 维度 | 全称 | 核心问题 |
|------|------|---------|
| **D** | Distillation Value | 你的经验值得被蒸馏成 AI Skill 吗？ |
| **A** | Anti-Distillation | 你的哪些能力是 AI 拿不走的？ |
| **M** | AI Mastery | 你驾驭 AI 工具的水平如何？ |
| **C** | Career Compass | 基于以上三维，你该往哪走？ |

## 执行流程

### Phase 0: 隐私告知（必须，第一步）

**触发后立刻显示，等用户确认后才能扫描：**

```
🔒 DAMC 隐私承诺（请阅读）

我即将扫描你的本地环境来生成 Agent 体检报告，包括：
  ~/.claude/ 配置 · git 历史 · 已安装开发工具

数据流向（透明承诺）：
  ✅ 所有原始内容仅在你本地处理，永远不上传
  ✅ 仅评分数字（D/A/M/C 总分 + 22 个子维度）会上传到
     damc.ai 用于生成你的可分享报告
  ✅ 数据只用于生成你的报告，绝不用于训练 AI / 卖广告 /
     分享给第三方
  ✅ 任何时候 damc.ai/account/delete 一键清空所有数据

❌ 永不上传：CLAUDE.md 全文、MEMORY.md 内容、git commit
   原文、skill 名称列表、项目路径、邮箱

→ 输入 "同意" 继续
→ 输入 "本地模式" 仅生成本地报告（不上传，不能用平台功能）
→ 输入 "取消" 退出
```

**用户回答后路由：**
- "同意" / "yes" / "ok" → Phase 1-5 扫描评估上传 + Phase 6 Skills 上架 + 显示完整汇总
- "本地模式" / "local" → Phase 1-4 扫描评估 + 跳过 Phase 5/6，仅生成 ~/Desktop/HTML
- "取消" / "no" → 直接退出

### Phase 1: 自动扫描（核心 — 不依赖问卷）

**扫描所有检测到的 AI Agent 环境，静默执行，不需要用户参与。**

#### 1.0 Agent 环境检测

```bash
echo "=== DAMC Agent Detection ==="
[ -d "$HOME/.claude" ] && echo "DETECTED: Claude Code"
[ -d "$HOME/.codex" ] || command -v codex >/dev/null 2>&1 && echo "DETECTED: Codex"
[ -d "$HOME/.cursor" ] && echo "DETECTED: Cursor"
[ -d "$HOME/.codeium/windsurf" ] && echo "DETECTED: Windsurf"
[ -d "$HOME/.continue" ] && echo "DETECTED: Continue"
[ -f "$HOME/.aider.conf.yml" ] || [ -d "$HOME/.aider" ] && echo "DETECTED: Aider"
[ -d "$HOME/.config/github-copilot" ] && echo "DETECTED: GitHub Copilot"
[ -d "$HOME/.workbuddy" ] && echo "DETECTED: WorkBuddy"
[ -d "$HOME/.trae" ] && echo "DETECTED: Trae"
[ -d "$HOME/.lingma" ] && echo "DETECTED: 通义灵码"
[ -d "$HOME/.marscode" ] && echo "DETECTED: MarsCode"
[ -d "$HOME/.codegeex" ] && echo "DETECTED: CodeGeeX"
[ -d "$HOME/.comate" ] && echo "DETECTED: Comate"
[ -d "$HOME/.chat" ] && echo "DETECTED: DevChat"
```

将检测结果记录下来，用于 Phase 3 多 Agent 合并评分。

#### 1.1 Claude Code 环境扫描（如果检测到 `~/.claude/`）

```
扫描目标 → 评估信号
──────────────────────────────────────────
~/.claude/CLAUDE.md
  → 文件是否存在、行数、自定义规则数量、是否有工作流定义

~/.claude/settings.json
  → hooks 配置数量和类型、权限模式、MCP servers 列表

~/.claude/skills/
  → skill 总数、自建 vs 安装(检查是否为 symlink)、类别分布

~/.claude/memory/
  → MEMORY.md 是否存在、memory 文件数量、类型分布

~/.claude/keybindings.json
  → 是否存在、自定义快捷键数量

~/.claude/projects/
  → 项目数量、项目级 CLAUDE.md 深度
```

#### 1.2 Codex 环境扫描（如果检测到 `~/.codex/` 或 codex CLI）

```
扫描目标 → 评估信号
──────────────────────────────────────────
~/.codex/
  → 目录结构和文件数量

~/.codex/generated_images/
  → session 数量（代表使用频率）、图片生成总数

项目级 AGENTS.md 或 codex 配置
  → 是否为 Codex 定制了项目指令

codex --version
  → 版本号
```

#### 1.3 Cursor 环境扫描（如果检测到 `~/.cursor/`）

```
扫描目标 → 评估信号
──────────────────────────────────────────
~/.cursor/rules/
  → 自定义规则文件数量和大小

项目级 .cursorrules 或 .cursor/rules/
  → 规则复杂度（行数、是否分文件）

~/.cursor/extensions/
  → 已安装扩展数量
```

#### 1.4 Windsurf 环境扫描（如果检测到 `~/.codeium/windsurf/`）

```
扫描目标 → 评估信号
──────────────────────────────────────────
~/.codeium/windsurf/
  → 配置深度

项目级 .windsurfrules
  → 是否自定义了 Windsurf 规则

Cascade 配置
  → 是否使用了 Cascade agentic 模式
```

#### 1.5 Continue 环境扫描（如果检测到 `~/.continue/`）

```
扫描目标 → 评估信号
──────────────────────────────────────────
~/.continue/config.json
  → 模型配置数量、自定义 provider、context providers

~/.continue/config.ts
  → 是否有高级 TypeScript 配置

~/.continue/.continuerules
  → 自定义规则
```

#### 1.6 Aider 环境扫描（如果检测到）

```
扫描目标 → 评估信号
──────────────────────────────────────────
~/.aider.conf.yml
  → 配置复杂度

.aider* 项目级配置
  → 是否自定义了模型、lint 命令等

aider --version
  → 版本号
```

#### 1.7 GitHub Copilot 扫描

```
扫描目标 → 评估信号
──────────────────────────────────────────
~/.config/github-copilot/
  → 配置是否存在

.github/copilot-instructions.md
  → 项目级指令文件
```

#### 1.8 WorkBuddy 环境扫描（如果检测到 `~/.workbuddy/`）

```
扫描目标 → 评估信号
──────────────────────────────────────────
~/.workbuddy/
  → 目录结构、配置文件数量、skill/插件数量
```

#### 1.9 Trae 环境扫描（如果检测到 `~/.trae/`）

```
扫描目标 → 评估信号
──────────────────────────────────────────
~/.trae/
  → 目录结构、配置文件

~/.trae/rules/ 或项目级 .trae/rules/
  → 自定义规则数量和复杂度

~/.trae/extensions/
  → 已安装扩展数量
```

#### 1.10 通义灵码环境扫描（如果检测到 `~/.lingma/`）

```
扫描目标 → 评估信号
──────────────────────────────────────────
~/.lingma/
  → 配置目录结构

~/.lingma/config 或 settings
  → 自定义配置深度（模型选择、代码补全偏好等）

项目级 .lingma 配置
  → 是否有项目级定制
```

#### 1.11 MarsCode 环境扫描（如果检测到 `~/.marscode/`）

```
扫描目标 → 评估信号
──────────────────────────────────────────
~/.marscode/
  → 配置目录结构

项目级 .marscode/ 或自定义规则
  → 是否有项目定制

MarsCode IDE 扩展
  → 已安装扩展数量和类型
```

#### 1.12 CodeGeeX / Comate / DevChat 环境扫描

```
扫描目标 → 评估信号
──────────────────────────────────────────
~/.codegeex/ / ~/.comate/ / ~/.chat/
  → 目录存在 = 使用过该工具
  → 配置文件复杂度
  → 对话历史数量（如果有）
  → 项目级配置存在
```

#### 1.13 Git 历史扫描（通用）

```
git log --oneline -100
  → AI 协作提交数（含 Co-Authored-By / Cursor / Copilot / Codex 标记）
  → 总提交频率

git log --all --author 过滤
  → 用户活跃度
```

#### 1.10 工作环境信号（通用）

```
检查已安装的开发工具
  → node/python/go 等（技术栈广度）
  → docker/k8s（DevOps 能力信号）

检查 AI Agent 总数
  → 安装的 Agent 数量本身就是 M 维度信号（多 Agent 加分）
```

### Phase 2: 快速画像（仅问 3 个问题）

扫描完成后，**只问用户 3 个问题**（不是问卷，是对话）：

1. **你的职业角色是什么？**（如：前端开发、产品经理、SEO专家、设计师、运营）
2. **你最核心的工作产出是什么？**（如：代码、文档、设计稿、决策、沟通协调）
3. **你的 MBTI 类型？**（可选，输入"跳过"则不纳入分析）

### Phase 3: 评分计算

读取 `references/scoring-framework.md` 获取详细评分算法。

**核心原则：**
- M 维度（AI 驾驭）100% 基于自动扫描数据，客观量化
- D 维度（蒸馏价值）70% 自动扫描 + 30% 用户画像推断
- A 维度（抗蒸馏）40% 自动扫描 + 60% 基于角色/产出类型推断
- C 维度（职业适配）= f(D, A, M) + MBTI 调整

**读取 `references/career-archetypes.md` 匹配用户的 8 种画像之一。**

### Phase 4: 生成可视化报告（本地 LITE 版）

1. 读取 `templates/report.html` 模板
2. 将评分数据填入模板中的 `window.DAMC_DATA` 对象
3. 将 LITE 版 HTML 保存到 `~/Desktop/DAMC-Report-{YYYY-MM-DD}.html`
   - LITE 版只含 4 维总分和画像，不含子维度详情、可蒸馏清单、护城河识别、行动建议
4. 完整版需在 damc.ai 平台解锁（见 Phase 5）

### Phase 5: 上传分数 + 生成平台链接（仅同意上传时）

**核心规则：只上传数字，永不上传原文。**

```python
# 仅以下数据会通过 HTTPS POST 到 damc.ai
upload_payload = {
    "scores": {
        "D": 78,                          # 总分
        "A": 62,
        "M": 85,
        "C": 65,
        "subs": {                          # 22 个子维度数字
            "expertise": 82, "methodology": 65, ...
        }
    },
    "archetype": "AI架构师",                # 画像名
    "role": "前端开发",                     # 用户输入
    "mbti": "INTJ",                        # 可选
    "env": {"os": "darwin", "shell": "zsh"}, # 桌面环境
    "agents_detected": ["Claude Code", "Codex", "Cursor"],
    "scan_summary": {                       # 仅数字摘要
        "agentsCount": 3,
        "totalSkills": 83,
        "customSkills": 5,
        "mcpServers": 8,
        "memoryFiles": 12,
        "claudeMdLines": 150,
        "cursorRulesFiles": 3,
        "codexSessions": 15,
        "aiCommits": 45,
        "totalCommits": 200
    }
}
# ❌ 不上传任何原始内容
```

接收 `{ token, url }` 响应后，在终端显示：

```
📊 你的 Agent 体检 · 部分结果

  检测到 AI Agent: Claude Code, Codex, Cursor

  D ████████░░ 78  M █████████░ 85
  A ██████░░░░ 62  C ██████░░░░ 65

  画像：🏆 AI 架构师

  ⚠️  Top 风险：你的 [跨域思维] 评分较低

  🔓 解锁完整分析（22 子维度 + 可蒸馏清单 +
     护城河识别 + 90 天行动路径）：

  https://damc.ai/r/{token}

  📄 本地 LITE 版已保存：~/Desktop/DAMC-Report-{date}.html
```

**API 端点（MVP 阶段使用 vibergo.space 域名）：**
```
POST https://vibergo.space/api/scan
Content-Type: application/json
Body: <upload_payload 见上>
Response: { "token": "aB7xK9", "url": "https://vibergo.space/r/aB7xK9" }
```

如果 API 调用失败（网络/服务不可用），降级为本地模式：
- 终端只显示 LITE 摘要
- 告知用户：「平台暂不可达，已生成本地报告」

### Phase 6: Skills 扫描与上架（仅同意上传时）

**在 Phase 5 完成后执行。扫描用户本地已创建的 Skills，分析其价值，让用户选择是否上架到 DAMC 技能商城。**

#### 6.1 扫描用户 Skills

扫描以下目录中**用户自己创建的** Skills（排除通过 `npx skills add` 安装的第三方 skill）：

```bash
# Claude Code skills — 用户自建的 slash commands
ls -la ~/.claude/commands/ 2>/dev/null

# 已安装的 skills（区分自建 vs 第三方）
# 自建信号：非 symlink、有个人特征、在 commands/ 下
ls -la ~/.claude/skills/ 2>/dev/null

# 项目级 skills
find . -maxdepth 2 -name "SKILL.md" -o -name "*.skill.md" 2>/dev/null
```

**判断"用户自建"的信号：**
- 文件不是 symlink（symlink 通常是 `npx skills add` 安装的）
- 文件内容有个人特征（作者名、自定义逻辑）
- `.claude/commands/` 下的文件默认视为用户自建

#### 6.2 分析 Skill 价值

对每个检测到的自建 Skill，快速分析：
- **名称和功能**：从文件内容提取 name 和 description
- **类别**：automation / content / dev-tools / seo / design / data / productivity
- **商业价值**：基于功能复杂度和通用性判断
- **建议可见性**：`public`（免费公开）或 `premium`（付费，后续上线）

#### 6.3 展示并让用户选择

```
🧩 Skills 扫描结果

检测到 {N} 个你创建的 Skills：

  1. ✅ seo-pipeline      — SEO 全流程自动化      建议: Premium
  2. ✅ deploy-check      — 部署前检查清单        建议: 公开（免费）
  3. ❌ my-test-script    — 个人测试脚本          建议: 不上架（过于个人化）
  4. ✅ content-rewriter  — AI 内容改写器         建议: Premium

→ 输入要上架的编号（如 "1,2,4"）
→ 输入 "全部" 上架所有推荐的（标 ✅ 的）
→ 输入 "跳过" 不上架任何 Skill
```

#### 6.4 上传到平台草稿箱

对用户选择的每个 Skill，调用 API 上传到草稿箱：

```
POST https://vibergo.space/api/skills
Content-Type: application/json

Body: {
  "name": "seo-pipeline",
  "displayName": "SEO Pipeline Pro",
  "description": "从 Skill 文件中提取的功能描述",
  "category": "seo",
  "installCommand": "npx skills add username/seo-pipeline",
  "iconEmoji": "🔍",
  "tags": ["SEO", "Automation"],
  "features": ["feature1", "feature2", "feature3"],
  "visibility": "premium",
  "valuation": {
    "score": 85,
    "reasoning": "基于 DAMC 分析的估值理由",
    "marketFit": "市场适配度分析",
    "uniqueness": "独特性分析"
  }
}
Response: { "id": "uuid", "slug": "seo-pipeline", "url": "/marketplace#seo-pipeline" }
```

**注意：**
- 上传需要用户已通过 GitHub 登录平台（未登录则提示先去 damc.space 登录绑定账号）
- 上传的 Skill 默认进入**草稿箱**（status=draft），需要用户在网页端确认后才会正式上架
- 如果 API 调用失败，告知用户稍后可以手动在 Dashboard 上架

#### 6.5 上传后提示

```
✅ 已提交 {N} 个 Skills 到草稿箱

  📋 seo-pipeline       → 草稿箱 (Premium)
  📋 deploy-check       → 草稿箱 (公开)
  📋 content-rewriter   → 草稿箱 (Premium)

⚠️  Skills 需要在网页端确认后才会正式上架
```

**`window.DAMC_DATA` 结构：**

```javascript
window.DAMC_DATA = {
  userName: "用户角色",
  date: "2026-04-08",
  mbti: "INTJ", // 或 null
  agents: ["Claude Code", "Codex", "Cursor"], // 检测到的 Agent 列表
  archetype: { name: "AI架构师", emoji: "🏆", tagline: "一句话定位" },
  overall: 72,
  scores: {
    D: { total: 78, subs: { expertise: 82, methodology: 65, codifiability: 88, standardization: 72, demand: 83 } },
    A: { total: 62, subs: { creativity: 70, eq: 55, crossDomain: 68, ambiguity: 60, physical: 40, trust: 75 } },
    M: { total: 85, subs: { environment: 18, skills: 22, automation: 16, memory: 12, advanced: 17 } },
    C: { total: 65, fit: "AI-Augmented Expert", paths: ["推荐路径1", "推荐路径2"] }
  },
  insights: {
    distillTargets: ["值得蒸馏的能力1", "值得蒸馏的能力2"],
    moats: ["护城河1", "护城河2"],
    risks: ["风险点1"],
    actions: ["行动建议1", "行动建议2", "行动建议3"]
  },
  scanSummary: {
    totalSkills: 83,
    customSkills: 5,
    hooksCount: 3,
    mcpServers: 8,
    memoryFiles: 12,
    claudeMdLines: 150,
    aiCommits: 45,
    totalCommits: 200
  }
};
```

## 输出规范

### 在终端显示的摘要

**所有 Phase 执行完毕后，统一输出最终汇总（覆盖此前的中间输出）：**

```
📊 DAMC 评估完成

  D 蒸馏价值  ████████░░  78
  A 抗蒸馏    ██████░░░░  62
  M AI驾驭   █████████░  85
  C 职业适配  ██████░░░░  65

  画像：🏆 AI架构师
  "你有值得蒸馏的深度经验，且善用 AI 放大自己的价值"

---
报告输出汇总：

  📄 完整报告：~/Desktop/DAMC-Report-2026-04-08.html
  🔗 在线报告：https://vibergo.space/r/{token}
  📋 Skills 草稿：{N} 个已提交到草稿箱
  🏢 团队码：{code}（已有则显示，没有则不显示）

  🔓 登录 damc.space/dashboard 解锁完整分析：
     · 22 子维度详情 + 可蒸馏清单 + 护城河识别 + 行动路径
     · 管理你的 Skills 草稿（确认上架、设置价格）
     · 查看团队排行和个人历史趋势
```

**如果用户选择了"本地模式"，则不显示在线报告、Skills 草稿和 Dashboard 相关的行。**

### 报告输出路径

- 默认保存到 `~/Desktop/DAMC-Report-{YYYY-MM-DD}.html`
- 如果用户指定路径则按用户指定

## 评分时的注意事项

- M 维度的评分必须基于实际扫描到的数据，不要凭感觉打分
- D 和 A 维度中基于推断的部分，要在报告中标注"基于角色推断"
- 整体评分 = D×0.25 + A×0.30 + M×0.25 + C×0.20
- A 维度权重最高，因为抗蒸馏能力是 AI 时代最核心的竞争力
