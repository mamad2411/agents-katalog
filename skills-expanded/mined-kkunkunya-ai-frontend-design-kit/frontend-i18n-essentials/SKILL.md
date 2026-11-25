---
name: frontend-i18n-essentials
description: 前端国际化（i18n）的综合规划与执行指南——做国际性网站、多语言架构、补多语言、翻译质量验证、字体跨语言统一、路由 / SEO / 字符串提取 / 动态切换等 i18n 相关任务时用。本 skill 按"运行时 / 翻译内容 / 视觉"三层正交模型路由：先定位用户的 i18n 痛点在哪一层，再走对应决策流；翻译内容层默认走三段流水线（机翻 → AI 本地人审 → 人工兜底）+ subagent 并行化（locale × persona × domain）。触发：用户说"做国际性网站""加多语言""补英文版""做 i18n""多语言网站的 SEO""路由用子路径还是子域名""本地化翻译""文化陷阱""AI 扮演当地人审翻译""字体跨语言不统一""语言切换器怎么做""字符串提取"。不用于纯单语言产品（没有国际化意图的就别套）、不用于纯翻译任务不涉及前端（那是纯文案）、不用于 RTL 排版深度实现（附录里有清单但不是本 skill 主场，目标市场不含中东时直接跳过）。
---

<!-- PACKAGED_KNOWLEDGE_START -->
## Packaged Knowledge Snapshot

This packaged copy includes local note snapshots for portability.
When the original Obsidian absolute path is unavailable, use the packaged snapshot instead:

- `/Users/kunkun/note/11-前端工程/前端国际化（i18n）认知对齐.md` -> `references/packaged-knowledge/前端国际化（i18n）认知对齐.md`
<!-- PACKAGED_KNOWLEDGE_END -->

# Frontend i18n Essentials

## 这个 skill 在做什么

**做国际性网站时的 i18n 规划与执行路由器**。用户要做多语言、补多语言、或 i18n debug 时，本 skill 干两件事：

1. **按三层正交模型诊断**用户的痛点在哪一层（运行时 / 翻译内容 / 视觉），避免把不同层的问题混着解
2. **按三场景分流**（新搭 / 补多语言 / debug）输出对应决策 + 执行资产（prompt 模板 / subagent 编排 / checklist / glossary 骨架）

本 skill **不替用户做具体库选型**（next-intel vs i18next vs react-intl 让 AI 按项目栈判断），**不跑完整开发流程**（执行交给开发实现剧本）——它只管"i18n 相关决策的判断方向"和"翻译质量流水线的编排"。

## 核心赌局

**i18n 最常见的失败是把三件正交的事混成一件**：

- 用户抱怨"网站不地道"——问题在翻译内容层（机翻味）、视觉层（字体塌）、还是运行时层（切语言把表单清空了）？
- 模型默认倾向把这些症状堆在一起开一个大药方，结果哪一层都没治好

本 skill 的硬约束：**先定位层，再开方**。三层各自独立评审、独立优化。

## 何时进入本 skill

**要进**：

- 用户说"做国际性网站 / 做国际化 / 做多语言 / 加英文版 / 加日文版 / i18n / 本地化 / localization"
- 老项目要补多语言，问"怎么开始 / 架构怎么搭 / 翻译怎么搞"
- 讨论 i18n 相关具体决策：路由用子路径还是子域名 / SEO hreflang 怎么配 / 语言切换器放哪 / 切语言要不要刷新 / 复数怎么处理 / 字符串提取 / 字体跨语言
- 翻译质量问题：机翻味重、当地人读着古怪、文化陷阱
- i18n 相关 debug：SEO 流量异常、语言切换后状态错乱、缺翻译页面 404

**不要进**：

- 项目是纯单语言（无国际化意图，用户没说要扩展）→ 跳过本 skill
- 纯翻译任务不涉及前端（纯文案翻译）→ 不是本 skill 范畴
- RTL 排版深度实现（目标市场不含中东 / 希伯来 / 波斯 / 乌尔都时直接跳过，附录里有清单但不是主场）
- UI 设计 / 视觉规划 / 动效 / 组件库（那是 frontend-suite 其他 skill 的活）

## 知识库依赖

本 skill 的认知底座**住在 Obsidian**，本文件只放执行层的路由 + 模板。决策前必读底座：

| 文件 | 用途 | 何时读 |
|------|------|--------|
| `/Users/kunkun/note/11-前端工程/前端国际化（i18n）认知对齐.md` | 三层正交模型 + 四条元原则 + 8 题原则 + 三场景速查 | **启动必读** |

**重要分工**：
- 认知层（Obsidian 笔记）：**原则 + 判断标准 + 禁区**——回答"为什么这么做"
- skill 层（本文件）：**执行流程 + prompt 模板 + 决策树**——回答"怎么做"

两者互补不重复。认知笔记更新优先，skill 同步引用。

## 执行顺序

```
步骤 0 读认知层 + 场景路由
  ↓
步骤 1 三层诊断（运行时 / 翻译内容 / 视觉）
  ↓
步骤 2 按层 × 场景输出决策 + 落地方案
  ↓
步骤 3 翻译内容层：subagent 并行化编排（按需）
  ↓
步骤 4 输出结构化结论 + handoff 给执行者
```

---

## 步骤 0：读认知层 + 场景路由

**先 Read 认知底座**（一次即可，后续按章节回读）：
`/Users/kunkun/note/11-前端工程/前端国际化（i18n）认知对齐.md`

**场景路由**（一次问答定档）：

问用户（或从上下文推断）：
> 你的项目是 A）全新国际化项目从零搭 / B）已有项目补多语言 / C）i18n 相关 debug？

| 场景 | 核心诊断点 | 跳过什么 |
|---|---|---|
| **A 新搭** | 架构决策前置（路由 / 库 / 字体栈 / ESLint 防御） | 字符串提取（新项目第一天包裹不需要这步） |
| **B 补多语言** | 老项目适配 + 一次性大工程 | 可能跳 RTL、简化路由策略（保持老 URL） |
| **C Debug** | 精确定位现象 → 三层哪一层 → 具体诊断清单 | 架构决策、翻译流水线设计 |

场景确定后进入步骤 1。

---

## 步骤 1：三层诊断

**不管三种场景哪个，都要先定位**在哪一层：

### 运行时层

涉及：库选型、复数/插值语法、路由、字符串提取、动态切换、fallback、SEO、语言包管理

诊断问题：
- 架构要不要做、做什么形态？
- 哪些老代码要改？
- 有没有"刷新状态错乱 / SEO 异常 / 缺翻译 404"这类症状？

### 翻译内容层

涉及：翻译质量、当地人视角、文化适配

诊断问题：
- 翻译由谁出？（AI / 机翻 / 人工 / 混合）
- 审校流水线要不要搭？
- 有没有"机翻味重 / 当地人看着别扭 / 踩文化禁忌"这类反馈？

### 视觉层

涉及：字体跨语言一致、布局（含 RTL）、视觉量感

诊断问题：
- 品牌调性有没有要求字体一致？
- 中英日韩并排视觉会不会塌？
- 目标市场含不含 RTL 语言？

**多层交叠时**：按"严重度 × 易解度"优先级排，一次解一层，不要同时开三张药方。

---

## 步骤 2：按层 × 场景输出决策

### 运行时层决策清单

按认知笔记的相关章节回读 + 组合输出。常见决策：

| 决策点 | 推荐方案 |
|---|---|
| URL 结构 | 子路径 `site.com/zh/`，默认语言不带前缀 |
| 首次访问 | 默认语言 + `Accept-Language` 浮条提示，禁止静默自动跳转 |
| 切换刷新 | SPA 软切换（router.push + 懒加载 + re-render），保留路径 |
| 语言持久化 | cookie 优先（SSR 首屏需要），1 年过期 |
| 复数 / 插值 | 用库原生 ICU MessageFormat，不自拼不绕开 |
| fallback 分层 | 生产回退默认语言 + 开发显示 key + CI 核心语言 block |
| hreflang | 双向 + self-reference + x-default，locale 严格 ISO 码 |
| 字符串提取 | AI + subagent 扫 + 人审 + ESLint 永久兜底 |
| 切换器位置 | 右上角 + 目标语言本土文字显示 + 国旗图标可选 |
| key 命名 | 业务语义（`user.profile.saveSuccess`），禁止 hash |

**每条背后的"为什么"回查认知笔记对应章节**。

### 翻译内容层决策清单

默认走三段流水线（跳到步骤 3 详细展开）。

### 视觉层决策清单

| 决策点 | 推荐方案 |
|---|---|
| 调性优先级 | 调性 > 一致量感 > 性能 |
| 字体栈 | Noto Sans / Serif 家族或 Apple 系统栈，**禁止手工拼 fallback** |
| CJK / Latin 混排 | `font-family: "Noto Sans", "Noto Sans SC"`（Latin 优先，CJK fallback） |
| 调性字体 | 像素风 / 复古 / 手写等必须所有语言贯彻同调性，**禁止某语言找不到就降级** |
| webfont | 要用就必须子集化（Google `&text=` 或 `fonttools subset`），禁止整包加载 CJK |
| 系统字体 | 仅"调性不强 + 性能要求极高"时可默认 `system-ui` |
| CSS 逻辑属性 | 无论是否做 RTL 都用 `margin-inline-start` 取代 `margin-left` |

---

## 步骤 3：翻译内容层 Subagent 并行化编排

**本步骤专门处理翻译 / 审校任务**。架构 / 路由 / 字体场景跳过。

### 三段流水线总览

```
第一段：机翻 / AI 直译
  ↓
第二段：AI 本地人审（核心，subagent 并行）
  ↓
第三段：人工兜底（只审敏感文案清单）
```

### Subagent 切分策略

| 模式 | 切分 | 何时用 |
|---|---|---|
| **A. 翻译初稿** | 按目标语言（1 subagent × 1 locale） | 从源语言批量产出 N 份目标语 json |
| **B. 本地化审校** | 按 `locale × persona`（3-5 persona × 每种语言） | 质量验证阶段 |
| **C. 业务域并行** | 按 `locale × domain` | 大项目（多业务 json × 多语言） |

实战中 ABC 可叠加：**5 语言 × 8 业务域 × 3 persona = 120 subagent 任务**。

### 主 agent 必兜底的三件事

1. **glossary 前置**：主 agent 先和用户定核心术语表 `glossary.json` 下发每个 subagent 作为硬约束。例：

```json
{
  "Login": {
    "zh": "登录",
    "ja": "ログイン",
    "ar": "تسجيل الدخول"
  },
  "Dashboard": {
    "zh": "控制台",
    "ja": "ダッシュボード",
    "ar": "لوحة القيادة"
  }
}
```

禁止 subagent 自由译 glossary 内的术语。

2. **key 完整性校验**：subagent 返回后，主 agent schema diff 对照源语言 json 的 key 树，漏 key / 错嵌套回发补。

3. **文化 checklist 强制注入**：spawn 每个 subagent 时 prompt 里必带：

```
审校时必须显式 check 以下文化陷阱：
- 颜色（红色在不同文化含义反转）
- 数字（4 / 13 / 666 / 7 的文化含义）
- 手势图标（OK / 大拇指在不同文化含义反转）
- 宗教（食物成分、节日祝福、图像敏感）
- 政治（地图、国名、争议区域）
- 幽默（笑话 / 双关语跨文化失效）
```

### Subagent prompt 模板（翻译初稿 - 模式 A）

```
你是专业翻译，将下面的 json 语言包从 [源语言] 翻译到 [目标 locale]。

输入：[源 json]
术语表（强制遵循）：[glossary.json 对应 locale 段]

输出要求：
1. 严格保留 json 结构、key 名不变，只译 value
2. 术语表内的词必须按表中目标语译法，不自由发挥
3. ICU MessageFormat 语法保留（如 `{count, plural, ...}` 中的 case 名不译）
4. 直译即可，不追求地道——地道化在下一段审校做
5. 输出纯 json，不加任何解释

源 json:
[...]
```

### Subagent prompt 模板（本地化审校 - 模式 B）

```
你是一名 [国籍] 用户，[年龄段]、[职业/身份]、[教育程度]、
[对本产品领域的熟悉度]。请以该身份读下面这段译文，按下述四段结构输出审校意见。

审校时必须显式 check 以下文化陷阱：
- 颜色 / 数字 / 手势图标 / 宗教 / 政治 / 幽默（详见上文清单）

输出格式（对每个有问题的条目）：
【别扭处】原文"[片段]"
【严重度】高/中/低（高=误解风险，中=不地道但能懂，低=语气偏好）
【建议】建议改成"[新译]"
【理由】当地人通常这么说因为...

译文：
[...]

源文（参考）：
[...]
```

**每种语言至少跑 3 个 persona**（主力用户 + 边缘用户 + 高龄/低教育），取并集。

### 人工兜底清单（主 agent 标注、人工兜底）

以下类型的 key 由主 agent 在 glossary 或单独 flag 文件中标记 `needs-human-review: true`，AI 审完仍要人工过一遍：

1. 法律 / 合规：`legal.*` / `privacy.*` / `terms.*`
2. 错误提示：`error.*` / `warning.*`
3. 品牌 slogan / 首页主标题：`marketing.hero.*` / `brand.*`
4. 支付 / 结账链路：`checkout.*` / `payment.*`
5. 客服话术：`support.*` / `help.*`

---

## 步骤 4：输出结构化结论 + handoff

最终输出给用户的三件事：

1. **诊断小结**（一句话）：本次任务落在哪一层 × 哪个场景
2. **决策清单**（分层表格）：每条决策 + 理由 + 认知笔记的对应段落锚
3. **执行 handoff**：
   - 运行时层决策 → 交给开发实现剧本 / 具体框架文档
   - 翻译任务 → subagent 编排已就位，主 agent 直接 spawn
   - 视觉字体决策 → 交给 `frontend-visual-reference` 或设计资产生成 skill

示例输出：

```
【诊断】本次任务：场景 B（补多语言）× 三层均涉及

【运行时层决策】
- 路由：子路径 + 默认语言不带前缀（不改老 URL）
- hreflang：HTML head 模式（项目 < 500 页）
- 字符串提取：AI + subagent 并行 + ESLint 兜底
- 切换器：右上角下拉 + 本土文字显示 + cookie 持久化
（每条理由 → 参见 Obsidian 笔记 §运行时层）

【翻译内容层决策】
- 走三段流水线
- Glossary 待用户确认 10 个核心术语
- Subagent 切分按 locale × 3 persona 并行
- 人工兜底：legal / error / checkout / brand 四类 key
（prompt 模板已就位见步骤 3）

【视觉层决策】
- 项目调性：[待用户确认]
- 字体栈：先按 Noto 家族方案落地，调性确认后再定制
（参见 Obsidian 笔记 §视觉层）

【Handoff】
- 运行时层 → 开发实现剧本 + 框架文档（next-intl / i18next 选型）
- 翻译任务 → 待 glossary 确认后主 agent spawn subagents
- 视觉层 → 待调性确认后 frontend-visual-reference 出字体方案
```

---

## 三场景详细速查

### 场景 A 新搭项目

关键动作：
1. 第一天就用框架原生 i18n（Next.js / Nuxt / Astro 内置）
2. URL 策略定好（子路径 + 默认语言不带前缀）
3. ESLint i18n 插件接好（防硬编码回归）
4. 字体调性前置决策（含目标语言配套字体栈）
5. hreflang 中间件自动生成
6. 翻译流水线搭起来（glossary + subagent 编排模板）

### 场景 B 补多语言

关键动作：
1. **绝不改老 URL**（原路径 = 默认语言，新加 `/xx/` 前缀）
2. 字符串提取：AI + subagent 并行 + 人审 + 批量改 + ESLint 兜底
3. 每加一种语言，所有页面 hreflang 批量更新（subagent 并行改模板）
4. 语言切换器首次接入（右上角 + cookie 持久化）
5. 调性字体栈若已存在，评估是否覆盖目标语言

### 场景 C Debug 常见症状

| 症状 | 诊断入口 | 常见根因 |
|---|---|---|
| SEO 流量下降 / 被错误语言索引 | Search Console 国际定位报告 | hreflang 双向不一致 / canonical 冲突 / 静默自动跳转 |
| 切语言后状态错乱 | 查派生状态 | 缓存 / 格式化 state 没监听 locale 变化 |
| 切语言后跳回首页 | 查路由实现 | 没保持路径，`router.push('/zh/')` 而非 `/zh/{currentPath}` |
| 缺翻译页面 404 | 查 fallback 配置 | 没配回退默认语言 |
| 某处文案没翻（残留原语言） | ESLint + 搜硬编码 | 字符串提取漏抽 / 缺 `t()` 包裹 |
| 切语言表单丢失 | 查组件是否 unmount | SPA 软切换实现错误导致 re-mount |
| 中英混排字体塌 | 查 font-family 链 | CJK 字体在前导致英文字母质量差 |

---

## 成熟度与演化计划

**当前成熟度**：0.5（基于 2026-04-23 认知采访沉淀，未经实战验证）

**演化节奏**（参考 git-workflow 的 3-5 次实战再固化原则）：

- **0.5 → 0.7**：跑过 3 次真实 i18n 项目后，字段 / prompt 模板 / glossary 骨架按实战反馈微调
- **0.7 → 0.9**：跑过 5+ 次后，评估是否拆分为 `i18n-setup`（架构 / 路由 / 提取）+ `i18n-localize`（翻译 / 审校 / subagent 编排）两个 skill
- **0.9 → 1.0**：拆分后稳定运行、考虑升格为独立 `i18n-suite` plugin（3-4 skill 语义内聚）

## Deletion-spec

- **触发删除条件**：当 i18n 相关认知已被模型默认稳定吸收（无需本 skill 做路由就能按三层模型分析任务）、或本 skill 的价值被独立 `i18n-suite` plugin 完全覆盖后，本 skill 可降级
- **禁用方式**：删除本目录 `skills/frontend-i18n-essentials/`；frontend-suite 的 plugin.json description 同步移除 i18n 段；README 同步
- **卸载清单**：
  - `~/.agents/plugins/frontend-suite/.claude-plugin/plugin.json`（description 段）
  - `~/.agents/plugins/frontend-suite/.codex-plugin/plugin.json`（description 段）
  - `~/.agents/plugins/.claude-plugin/marketplace.json`（frontend-suite description）
  - `~/.agents/plugins/frontend-suite/README.md`（i18n 段）
  - `/Users/kunkun/note/11-前端工程/前端国际化（i18n）认知对齐.md`（认知笔记——是否同步删除视是否还有其他引用）