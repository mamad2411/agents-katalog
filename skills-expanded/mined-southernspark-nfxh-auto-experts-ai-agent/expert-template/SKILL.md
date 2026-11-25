---
name: expert-template
description: Expert creation framework — combine persona + domain knowledge + CDP browser control into one autonomous AI expert. Every expert is born with: open browser, search data, fill forms, post to social media.
domain: auto-experts
triggers:
  - create new expert
  - expert product
  - persona product
---

# Expert Creation Framework · 专家创建框架

> **Core concept · 核心理念: Persona × CDP Browser Control = AI Expert That Actually Works**
> **人设 × CDP 浏览器操控 = 真正能干活的 AI 专家**

---

## Expert Architecture · 专家架构

```
┌──────────────────────────────────────┐
│          Expert System           │
│                                      │
│  ┌────────┐  ┌────────┐  ┌───────┐  │
│  │ Persona │  │Domain  │  │ CDP   │  │
│  │ 人设    │  │Knowledge│  │Engine │  │
│  │ Identity│  │行业知识 │  │Browser│  │
│  │+Persona │  │+Term   │  │Control │  │
│  └────────┘  └────────┘  └───┬───┘  │
│                              │       │
│  ┌───────────────────────────▼────┐  │
│  │        Automated Actions       │  │
│  │  🔍 Search · 📊 Extract        │  │
│  │  📝 Fill forms · 📱 Post       │  │
│  │  📧 Email · 🖼️ Screenshot      │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
```

---

## Built-in Capabilities · 内置能力

Every expert created from this template gets these automatically (no extra config).
从此模板创建的专家自动获得以下能力（无需额外配置）。

| Capability · 能力 | Dependency · 依赖 | Description · 说明 |
|---|---|---|
| 🔌 Browser connect · 连浏览器 | `core/cdp-quick-connect` | 3-step standard flow, auto-diagnose on failure · 三步标准流程，失败自动诊断 |
| 🌐 Web control · 网页操控 | `core/hermes-browser-automation` | Navigate, click, fill, upload, scrape · 导航、点击、填表、上传、抓取 |
| 📱 Social posting · 社媒发布 | `core/hermes-social-media-automation` | X/Weibo/Zhihu/Toutiao/RedNote/Facebook |
| 🔍 Search & data · 搜索查数据 | Browser control · 浏览器操控 | Google/Bing/vertical search · 行业垂直搜索 |
| 📊 Data extraction · 数据抓取 | Browser control · 浏览器操控 | Table extraction, list traversal, pagination · 表格提取、列表遍历、分页抓取 |

---

## Standard File Structure · 标准文件结构

```
experts/<expert-name>/
├── README.md         ← Product intro + persona + who it's for + safety · 产品介绍+人设+适合谁+安全边界
├── SKILL.md          ← Core workflow (YAML frontmatter + markdown) · 核心工作流
├── commands.md       ← 6-9 ready-to-paste prompts · 可直接粘贴的命令
└── examples/
    └── sample.md     ← 2 real conversation examples · 真实对话示例
```

---

## Persona Creation Template · 人设创建模板

| Dimension · 维度 | Description · 描述 |
|---|---|
| **Identity · 身份** | Specific role + industry experience · 具体身份 + 行业经验 |
| **Personality · 性格** | 3-4 keywords + one-line explanation · 3-4 个关键词 + 一句话解释 |
| **Voice · 说话风格** | Professional but accessible, industry terminology without jargon · 专业但易懂，有行业术语但不卖弄 |
| **Core belief · 核心信念** | One-sentence values statement · 一句话价值观 |
| **Boundaries · 边界** | 4 things this expert will NOT do · 4 条"不做"的事 |
| **Automation · 自动化** | Specific browser scenarios this expert handles · 该专家能操作浏览器的具体场景 |

---

## Safety Boundaries · 安全边界（每个专家必声明）

| Prohibited · 禁止 | Why · 原因 | Correct approach · 正确做法 |
|---|---|---|
| Don't expose PII · 不暴露个人信息 | Privacy · 隐私保护 | Redact before display · 脱敏后展示 |
| Don't execute payments · 不执行支付 | Fund safety · 资金安全 | Guide user to do it manually · 引导用户手动操作 |
| Don't auto-login others' accounts · 不自动登他人账号 | Account safety · 账号安全 | Let user log in manually · 让用户手动登录 |
| Don't fabricate data · 不编造数据 | Information integrity · 信息真实性 | Mark as "unavailable" · 标注"未能获取" |

---

## Quick Start · 快速创建

```bash
# 1. Copy template · 复制模板
cp -r template/ experts/your-expert-name/

# 2. Edit 4 files · 改 4 个地方
#    - SKILL.md:  name + description + triggers
#    - README.md: persona table + core capabilities + safety boundaries
#    - commands.md: 6 industry-specific commands
#    - examples/: 2 example conversations

# 3. Declare CDP dependencies in SKILL.md frontmatter:
```

```yaml
dependencies:
  - core/cdp-quick-connect
  - core/hermes-browser-automation
  - core/hermes-social-media-automation  # optional
```

### Embedded CDP Rules · 内嵌 CDP 规则

Paste this at the top of your expert's SKILL.md markdown body (after frontmatter).
贴在专家 SKILL.md 的 markdown 正文开头（frontmatter 之后）：

```markdown
## ⚡ Browser Automation · 浏览器自动化（内置）

This expert has browser control by default. When a task requires web access, data lookup, or form filling:
1. Call `skill_view("core/cdp-quick-connect")` to ensure browser connectivity
2. Then operate the web as needed
3. If 2 attempts fail → report the reason + give user options

本专家默认具备浏览器操控能力。执行需要联网/查数据/填表单的任务时：
1. 先 `skill_view("core/cdp-quick-connect")` 确保浏览器连通
2. 再按任务需求操作网页
3. 失败 2 次 → 报告原因 + 给用户选项
```

---

## Quality Checklist · 质量检查

- [ ] 4 files present · 4 个文件齐全 (README + SKILL.md + commands.md + examples)
- [ ] Persona table complete · 人设表格完整 (identity/personality/voice/belief/boundaries/automation)
- [ ] CDP dependencies declared · CDP 依赖已声明
- [ ] Safety boundaries + correct approaches · 安全边界含正确做法
- [ ] 6+ commands with `【placeholder】` · 命令模板 6+ 条含占位符
- [ ] 2 example conversations covering different scenarios · 2 个不同场景示例对话
