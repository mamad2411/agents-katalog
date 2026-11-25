# ego-ops-to-skill：把浏览器操作沉淀为可复用 Skill

---
name: ego-ops-to-skill
description: 把用户或 Agent 在 Ego Lite 浏览器里刚完成的操作序列，转化为结构化的 WorkBuddy Skill（SKILL.md + 可选脚本 + 登记项）。触发词：把这个操作做成 skill、沉淀成 skill、转成技能、操作转 skill、make this a skill。
---

## 目标

把「AI + 用户摸出来的浏览器操作路径」一键固化为可分发 skill，让其他同事**只装 Ego Lite、扫码登录一次**就能复现整条流程。

## 工作流（五步，必须按序）

### Step 1 — 捕获操作轨迹

在 ego-browser 会话仍在时，收集以下素材（缺失则询问用户）：

1. **目标站点与页面路由**（URL hash 路由，如 `app.qian-gua.com/#/material/note/关键词`）
2. **操作序列**：每一步的动作（点击/填写/滚动/等待/下载）+ 定位方式（优先 CSS/文本，禁用裸坐标）
3. **验证点**：每步怎么判断成功（计数+1、文件落盘、URL 变化、单元格值）
4. **踩坑记录**：过程中绕过的坑（弹窗、双发、僵尸流、坐标缩放等）
5. **输入参数化清单**：哪些值每次会变（关键词、日期范围、条数、导出文件名），收敛为 skill 的入参

### Step 2 — 设计 skill 骨架

按 `references/workflow.md` 的格式生成：

```
~/.workbuddy/skills/<skill-name>/
├── SKILL.md          # 主文档：frontmatter(name/description) + 工作流 + 验证点 + 踩坑
├── references/       # 可选：详细分步说明、字段映射表
└── scripts/          # 可选：辅助脚本（清洗、合并、上传）
```

**硬性要求**：
- 所有元素定位用 CSS/文本/ref，**禁止像素坐标**（屏幕尺寸因人而异）
- 下载类操作写「武装事件 + 文件系统落盘验证」双保险
- 写入飞书/外部系统的步骤必须带校对环节（AI 数据标黄、逐字段核对）
- 涉及平台额度的步骤写明额度模型与确认时机

### Step 3 — 生成文件

- SKILL.md frontmatter 必须含 `name` 和 `description`（description 写清触发词，用户一句话能命中）
- 操作序列写成带代码块的步骤（ego-browser nodejs heredoc 形式，可直接复制运行）
- 把 Step 1 的踩坑写进 SKILL.md 的「踩坑与自愈」节，并同步追加到对应站点的 learnings（见 ego-site-learnings skill）

### Step 4 — 验证（不可跳过）

1. fresh 会话按 SKILL.md 从零跑一遍（可用测试参数，如导出 10 条而非 1000 条）
2. 逐个验证点打勾；失败的步骤回炉修改，不许带病发布
3. 确认 skill 在无人工干预下能跑完主流程（扫码/验证码等人工步骤除外，需显式标注「人工介入点」）

### Step 5 — 登记

在 `~/.workbuddy/skills/ego-ops-to-skill/REGISTRY.md` 追加一行（本 skill 自带登记表）：

```
| 日期 | skill 名 | 站点 | 触发词 | 验证人 |
```

## 何时不要做成 skill

- 一次性任务（无复用预期）
- 依赖特定账号权限且无法泛化的（如仅管理员可见页面）——除非明确标注适用范围
- 操作路径尚未稳定的（改版概率高的灰色地带）——先跑 3 次手工确认稳定再固化

## 参考

- `references/workflow.md`：index.json 元数据 schema、SKILL.md 模板、merge 登记
- `ego-site-learnings`：站点踩坑知识库（skill 引用的自愈层）
