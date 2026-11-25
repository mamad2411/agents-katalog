---
name: idea-foundry
description: |
  创建 构建 设计 开发 搭建 实现 编写 制作 重构 新建 生成 做项目 写工具 做App 做网站 写服务 搭框架 从零开始 技术方案 架构设计 产品设计 帮我做 帮我写 帮我设计 帮我开发 帮我搭建 帮我规划 帮我实现 新项目 工具开发 完整系统。TRIGGER INTENT: CREATE, BUILD, DESIGN, IMPLEMENT. BEHAVIOR: role=orchestrator stage=dispatch TAKES OVER workflow. No other engine may preempt.
triggers:
  - 帮我做
  - 开发一个
  - 搭建
  - 构建
  - 从零开始
  - 做项目
  - 新项目
  - 工具开发
  - 写一个
  - 做一个
  - 设计一个
  - 实现一个
  - 创建一个
  - 重构
  - 架构设计
  - 技术方案
  - 产品设计
  - 做一个App
  - 做一个网站
  - 写一个服务
  - 搭一个框架
  - 工具构思
  - 帮我设计
  - 帮我规划
  - 帮我实现
  - 帮我搭建
negative_triggers:
  - 查一下
  - 这个命令
  - 文档
  - 什么意思
  - 怎么用
  - 单行
  - 小修改
  - 改一行
  - 修bug
  - 配置修改
version: 9.1.0
role: orchestrator
stage: dispatch
author: Hermes Agent
license: MIT
---

# 创意锻造 · Idea Foundry v9.1.0 — 方法集

> **角色声明:** v9 正式废除数字优先级。调度权来自 `role: orchestrator, stage: dispatch`。

## 架构全景（最终形态）

```
                         「用户需求」
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
## 🚨 触发规则 — 意图识别

### 触发意图（CREATE / BUILD / DESIGN / IMPLEMENT）

当用户表达的**核心意图**是以下之一，直接接管：

| 意图 | 典型表达 | 本质 |
|------|---------|------|
| **CREATE** | 「做一个」「写一个」「建一个」「搞一个」「搭一个」 | 从无到有创造 |
| **BUILD** | 「帮我开发」「实现这个功能」「构建系统」 | 工程实现 |
| **DESIGN** | 「帮我设计」「技术方案」「架构怎么弄」 | 方案设计 |
| **REFACTOR** | 「重构」「重写」「翻新」「升级架构」 | 大规模改造 |
| **PLAN** | 「规划一下」「怎么入手」「分几步」 | 工程规划 |

### 排除意图（QUERY / CHAT / TWEAK / REVIEW）

以下意图**不走完整流水线**，但部分场景可用精简路径：

| 意图 | 典型表达 | 处理方式 |
|------|---------|---------|
| **QUERY** | 「这个命令是什么意思」「X 和 Y 有什么区别」 | 直接回答 |
| **LOOKUP** | 「帮我查一下文档」「这个 API 怎么用」 | 查阅检索 |
| **TWEAK** | 「改一行」「修个 bug」「配置调一下」 | 微调修改 |
| **CHAT** | 「你觉得呢」「讨论一下」「随便聊聊」 | 对话交流 |
| **REVIEW** | 「过一遍 IF 逼问」「用 IF 审查」「跑 IF 质询」 | **精简路径：** 策略选择→直接逼问→记录决策。不跑 Phase -3/-2/-1/-0.5。详见 `references/using-if-for-design-review.md` |

### 意图识别规则

```
1. 核心判断: 「用户要我产出东西，还是回答东西？」

   产出 → 🚨 Foundry 接管
   回答 → 直接回答

2. 产出量判断: 「产出物是 单行/几行 还是 多文件/多模块？」

   ≤3 行改动 → 直接回答
   ≥4 行或 多文件 → 🚨 Foundry 接管

3. 模糊判断: 「用户没说要产出，但意图隐含了要产出」

   「我想做一个...但不知道怎么做」 → 🚨 Foundry
   「帮我分析一下这个方案」 → 判断产出物大小决定
```

### 无需询问，直接接管

满足以下**任意一个**→ 立即接管，不弹出询问：

- 用户意图 = CREATE / BUILD / DESIGN / REFACTOR / PLAN
- 预期产出物 ≥ 多文件或多模块
- 用户明确说「帮我做/开发/搭建/设计/实现」

### 模糊意图 → 一句话确认

满足以下 → 问一句就走：

- 用户说「有个想法」但未描述产出物
- 边界场景（可能是查询也可能是构建）

确认语: 「检测到构建意图，是否进入锻造流程？」

### 排除场景 → 直接回答

- 意图 = QUERY / LOOKUP / TWEAK / CHAT
- 预期产出 ≤ 3 行或纯文本

### ⚠️ 反模式：表面匹配 Skill 干扰

**陷阱场景：** 用户说「帮我做一个AI筛图工具」，Agent 发现已有 `photo-organizer-pro`（AI照片评分/整理），直接加载 brainstorming + photo-organizer-pro 开始设计，跳过了 idea-foundry。

**为什么错：** 用户说的是「**做**一个工具」→ 命中「帮我做一个」触发词，属于**新项目开发**，不是「用现有工具整理照片」。现有 Skill 的话题相似性不等于任务类型匹配。

**正确行为：** 任何包含「帮我做/开发/搭建/创建/构建/写一个」的请求，**无论是否存在话题相似的现有 Skill**，idea-foundry 必须最先触发。先走 Phase -4 策略选择，再决定是否将现有 Skill 作为能力匹配项注入流水线。

**区分规则：**
| 用户说 | 正确入口 |
|--------|---------|
| 「帮我做一个AI筛图工具」 | idea-foundry（新项目开发） |
| 「用 photo-organizer 整理我的照片」 | 直接加载 photo-organizer-pro |
| 「这个筛图功能加个批量导出」 | 直接改代码（已有项目的增量修改） |

---

## 🆕 自进化机制

**Phase -2 检测到未知领域时自动触发。** 这是 v5 承诺的能力，v8.3 正式激活。

### 触发条件

多领域识别完成后，任一领域标签不在 `tag-pool.json` 中。

### 进化流程

```
1. 标记未知领域 → 分析特征（6维）
2. 判断类型: 工程主干 or 行业垂直
3. 生成最小插件包:
   ├── 标签名（英文slug）
   ├── 1-2个行业校验规则
   ├── 0-1个专属阶段
   └── 必要声明/免责
4. 追问用户一次: 「检测到新领域『XXX』，是否注册？」
   ├── 是 → 写入 tag-pool.json → 记录 evolution_log → 继续执行
   └── 否 → 跳过自进化，本次用通用主干
```

### 进化日志

`tag-pool.json` 的 `evolution_log` 字段记录每次进化:

```json
{"ts": "2026-05-19T12:00:00Z", "domain": "astronomy", "type": "industry", "plugins": ["data-accuracy", "unit-conversion"]}
```

### 安全约束

- 生成的新标签不得覆盖已有标签
- 插件规则不得包含 `rm -rf` / `sudo` / 网络请求等危险操作
- 用户可随时「删除标签 XXX」移除误注册的领域

---

## Phase -4: 全局策略选择 · Strategy Selector  ← 用户决策层
│                                                                  │
│    极致成品   不惜Token,全Skill,剔除冗余,完美交付                    │
│    均衡性价比  核心Skill,砍低收益步骤,质量够用                        │
│    极速省Token 最小Skill链路,最快出结果                              │
│                                                                  │
│   策略决定: 能力优先级分布 / 去重激进程度 / 冗余注入 / 降级行为           │
└───────────────────────────────┬──────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│ Phase -3: Skill 发现扫描器                                         │
│   扫描本地 → 构建能力映射表 → 按策略模式标记可用Skill                    │
└───────────────────────────────┬──────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│ Phase -2: 多领域识别 & 权重计算                                     │
└───────────────────────────────┬──────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│ Phase -1: 主干+插件 拼接                                            │
└───────────────────────────────┬──────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│ Phase -0.5: 策略感知动态匹配（策略层驱动裁剪）                          │
│                                                                  │
│   根据策略模式:                                                      │
│   ├── 决定哪些能力激活(critical/important/nice-to-have)               │
│   ├── 决定去重激进程度(互补都留 vs 只留最优)                             │
│   ├── 决定冗余Skill是否注入                                          │
│   └── 决定降级时自动接受 or 弹窗询问用户                                │
└───────────────────────────────┬──────────────────────────────────┘
                                │
                                ▼
                         执行 + 日志
```

 直接回答 → 不接管

> 意图识别设计模式详见 `references/intent-based-triggering.md`

## Phase -4: 全局策略选择

### 三种模式

| |  极致成品 |  均衡性价比 |  极速省Token |
|---|---|---|---|
| **目标** | 交付完美无瑕疵 | 质量够用，Token适中 | 最快出结果 |
| **能力范围** | critical + important + nice-to-have + 行业 | critical + important | critical only |
| **去重策略** | 互补都留，纯冗余才剔除 | 每能力只留最优1个 | 每能力只留最优1个 |
| **冗余注入** | 注入所有相关多余Skill | 仅注入直接相关的 | 不注入 |
| **降级行为** | 缺Skill→弹窗: 「当前环境无法达到S级，接受降级?」 | 静默降级 | 自动接受任何降级 |
| **行业插件** | 全部注入 | 仅高权重(>0.5)注入 | 不注入 |
| **审查轮次** | 全量(设计+架构+DX+代码+安全) | 设计+代码+安全 | 仅代码 |
| **复盘** | 完整(retro+learn+context-save) | context-save only | 跳过 |
| **错误处理** | 全量 debug+investigate | debug only | 快速修复 |

## 环境自适应 UI

工作流自动检测运行环境，切换交互模式：

```
检测环境:
  ├── CLI终端 (Hermes CLI / Terminal) → 🖥️ 终端交互式
  │   ├── clarify 工具 → 方向键菜单
  │   ├── ANSI颜色 → 进度条/等级标识
  │   └── 质量报告 → 彩色表格
  │
  └── 网页/消息平台 (OpenWebUI/飞书/微信) → 📱 纯文本降级
      ├── 1/2/3 数字选择
      ├── 纯ASCII进度条 [====>     ]
      └── 纯文本表格
```

### 终端交互式 (CLI)

**策略选择 — 方向键菜单:**
```
clarify(question="选择执行策略", choices=[
  "极致成品 — 完美交付, 不惜Token",
  "均衡性价比 — 质量够用, Token适中(推荐)",
  "极速省Token — 最小链路, 最快出结果",
  "学术论文 — 纯学术链路",
  "金融风控 — 强制合规回测",
  "自定义 — 逐项调整"
])
```

**质量预检 — 彩色进度条:**
```
质量预检报告 · 极致成品模式
────────────────────────────────
critical(6):    ████████████ 6/6  ✅ 全匹配
important(11):  ██████████░░ 10/11 ⚠️ 缺1
nice-to-have:   ██████░░░░░░ 4/6   ❌ 缺2
行业插件:       ████████████ 10/10 ✅

目标: S级 → 实际可达: A级 ⚠️

[执行] [切换均衡] [查看缺失] [取消]
```

颜色规则: S/A=绿色, B=黄色, C=橙色, D=红色

### 纯文本降级 (Web/消息)

**策略选择 — 数字回复:**
```
选择执行策略:
1. 极致成品 — 完美交付
2. 均衡性价比 — 质量够用(推荐)
3. 极速省Token — 最快出结果
回复数字选择
```

**质量预检 — ASCII进度条:**
```
质量预检报告 · 极致成品模式
critical(6):    [████████████] 6/6 OK
important(11):  [██████████--] 10/11 缺1
实际可达: A级 (目标S级, 建议切换均衡模式)
回复: A-接受 B-切换均衡 C-查看缺失
```

```
用户需求输入
    │
    ▼
检测用户是否明确指定模式？
    ├── 是 → 直接使用(含自定义/预设)
    └── 否 → 根据需求特征推荐:
              ├── 「帮我做产品/正式项目」→ 推荐 
              ├── 「帮我快速做一个原型」→ 推荐 
              ├── 「写论文/学术」→ 推荐 学术论文模式
              ├── 「金融分析/量化」→ 推荐 金融风控模式
              └── 其他 → 默认 

展示推荐 + 确认:
  「检测到正式项目需求，推荐极致成品模式。
   预计消耗: ~500K tokens, 25+ Skill, 11-12阶段。
   
   可选:
    极致成品 — 完美交付
    均衡性价比 — 质量够用(推荐)
    极速省Token — 最快出结果
    学术论文 — 只走学术链路
    金融风控 — 强制合规回测
    自定义 — 逐项调整」
```

### 自定义模式

用户可逐项调整策略参数，生成个性化配置：

```
可调参数:
  能力范围:     [全量/仅critical+important/仅critical/自定义勾选]
  去重激进度:   [互补都留/每能力最优/单一最优]
  冗余注入:     [全注入/相关注入/不注入]
  降级行为:     [弹窗确认/静默降级/自动接受]
  行业插件深度: [全量/高权重/不注入]
  审查深度:     [全量/设计+代码+安全/仅代码]
  复盘:         [完整/仅上下文保存/跳过]

触发: 「自定义模式」「手动调整策略」「我要自己配」
```

### 预设领域模式

针对高频场景提供开箱即用的策略预设:

** 学术论文模式:**
```
能力范围: 学术12阶段(选题→文献→研究→方法论→数据→初稿→论证→格式→查重→终稿→提交→复盘)
跳过: 所有工程开发流程(TDD/代码审查/QA/浏览器测试/Ship)
强制启用: humanizer-zh(去AI味), 格式规范检查
行业插件: academic(文献综述/查重/格式)
策略: 基于均衡裁剪
```

** 金融风控模式:**
```
能力范围: 金融10阶段(需求→合规→风控→数据→建模→回测→报告→合规复审→交付→复盘)
强制启用: 合规审查, 风控评估, 回测验证
强制注入: 风险提示免责声明
跳过: UI设计/浏览器测试/前端开发
行业插件: finance(合规/风控/回测)
策略: 基于极致裁剪(金融不省)
```

**🎨 纯创作模式:**
```
能力范围: 创作9阶段(灵感→收敛→初稿→风格→受众→精修→审定→发布→复盘)
强制启用: humanizer-zh, brainstorming(发散模式)
跳过: 所有工程开发流程
行业插件: creative(灵感/风格/受众)
策略: 基于均衡裁剪
```

### 策略 vs 环境匹配检测 (前置质量预检)

**Phase -4 策略选择后，Phase -3 扫描完成后，立刻执行质量预检。**

```
1. 用户选择策略模式(如极致成品)
2. Phase -3 扫描本地Skill池
3. 质量预检: 当前Skill池 vs 策略模式需求
4. 输出质量匹配报告 → 强制用户确认
5. 确认后 → 继续执行
```

**质量评估等级:**

```
S级: 所有critical+important+nice-to-have+行业能力 全匹配 → 完美执行
A级: critical+important 全匹配，nice-to-have ≥70% → 良好执行
B级: critical 全匹配，important ≥60% → 可行但存缺口
C级: critical ≥80%，大量降级 → 勉强执行
D级: critical <80% → 不建议执行此策略
```

**弹窗格式:**

```
「质量预检报告 · 极致成品模式
 ─────────────────────────────
 当前环境: 273 Skill
 目标等级: S级
 实际可达: S级 ✅
 
 能力覆盖:
   critical(6):     ✅ 全匹配
   important(11):   ✅ 全匹配
   nice-to-have(6): ✅ 全匹配
   行业插件:         ✅ 可用(10/10)
 
 预计降级: 0处
 预计注入: 3处
 ─────────────────────────────
 确认执行?  [执行] [切换模式] [取消]」

─────────────────────────────────

「质量预检报告 · 极致成品模式
 ─────────────────────────────
 当前环境: 50 Skill
 目标等级: S级
 实际可达: ⚠️ B级 (无法达到S级)
 
 能力覆盖:
   critical(6):     ✅ 5/6 (缺 CAP:SHARPEN)
   important(11):   ⚠️ 7/11 (缺 DESIGN_REVIEW, DX_REVIEW, SECOND_OPINION, CODE_HEALTH)
   nice-to-have(6): ❌ 2/6 (缺 DOCUMENT, RETRO, LEARN, CODE_HEALTH)
   行业插件:         ⚠️ 4/10
 
 预计降级: 5处
 预计人工兜底: 2处
 ─────────────────────────────
 ⚠️ 当前环境无法达到S级成品质量。
 
 A) 接受降级到B级(继续执行)
 B) 切换到均衡模式(推荐 — 当前环境可达A级)
 C) 查看缺失Skill清单并安装
 D) 强制继续(标记为降级执行)」
```

### Skill Gap 报告（质量预检降级时自动触发）

质量预检降级时（实际可达 < 目标等级），在质量预检报告后追加输出：

```
🎯 Skill 缺口分析
─────────────────────────────
降级项:
  CAP:BROWSER_TEST → qa 缺失 → 降级为 playwright-skill（功能受限）
  CAP:SECOND_OPINION → codex 缺失 → 跳过（无双审）

补充可恢复:
  1. qa → 恢复 CAP:BROWSER_TEST → 安装: npx skills add qa
  2. codex → 恢复 CAP:SECOND_OPINION → 安装: npx skills add codex

补充后可达: A级（当前 B级）
一键安装全部? [Y/n]
```

**规则：**
1. **降级项明细**：遍历 capability 表，找出「已激活但实际不可用」的能力，记录 {能力标签, 首选 Skill, 安装命令}
2. **补充后等级**：假设缺失 Skill 全部安装 → 重算等级 → 输出「补充后可达 X 级（当前 Y 级）」
3. **排序**：按重要性排序（critical > important > nice-to-have），每条含 Skill 名 / 恢复的能力 / 安装命令
4. **一键安装**：用户选 Y → 依次执行安装命令 → 重跑 Phase -3 → 新质量预检
5. **安装命令来源**：从 skills_list 查询安装源（如 `npx skills add <name>`）

**强制确认规则（可配置阈值）:**

阈值配置在 strategy-config.json 的 `confirmation_policy` 字段:

```json
{
  "confirmation_policy": {
    "thresholds": {
      "silent_execute": 0,       // 实际≥目标 → 不弹窗(默认)
      "suggest_switch": 1,        // 比目标低1级 → 弹窗建议切换
      "force_confirm": 2          // 比目标低≥2级 → 强制弹窗
    },
    "strict_mode": false          // true=所有降级都弹窗
  }
}
```

| 预检结果 | 默认行为 | strict_mode 行为 |
|---------|---------|-----------------|
| 实际≥目标 | 直接执行 | 弹窗确认 |
| 实际比目标低1级 | 弹窗建议切换 | 强制弹窗 |
| 实际比目标低≥2级 | 强制弹窗 | 强制弹窗+阻止执行 |

用户自定义:
```
「弹窗严格一点」→ strict_mode: true
「弹窗宽松一点」→ suggest_switch: 2, force_confirm: 3
「不要弹窗」→ force_confirm: 999
```

### 策略驱动的能力裁剪

```
能力标签           极致    均衡    极速
────────────────  ──────   ──────   ──────
CAP:VALIDATE       ✅        ✅        ✅
CAP:SHARPEN        ✅        ✅        ❌
CAP:DESIGN         ✅        ✅        ❌
CAP:DESIGN_REVIEW  ✅        ❌        ❌
CAP:ARCH_REVIEW    ✅        ✅        ❌
CAP:DX_REVIEW      ✅        ❌        ❌
CAP:PLAN           ✅        ✅        Lite
CAP:BREAKDOWN      ✅        ✅        ❌
CAP:IMPLEMENT      ✅        ✅        ✅
CAP:TDD_ENFORCE    ✅        ✅        ❌
CAP:DEBUG          ✅        ✅        ❌
CAP:CODE_REVIEW    ✅        ✅        ✅
CAP:SECOND_OPINION ✅        ❌        ❌
CAP:SECURITY_SCAN  ✅        ✅        ❌
CAP:BROWSER_TEST   ✅        ✅        ❌
CAP:SECURITY_AUDIT ✅        ✅        ❌
CAP:CODE_HEALTH    ✅        ❌        ❌
CAP:VERIFY         ✅        ✅        ✅
CAP:SHIP           ✅        ✅        ✅
CAP:DOCUMENT       ✅        ❌        ❌
CAP:RETRO          ✅        ❌        ❌
CAP:LEARN          ✅        ❌        ❌
CAP:CONTEXT_SAVE   ✅        ✅        ❌
行业能力           全量注入   高权重    不注入
```

### Skill 组合策略（解决「同类Skill太多」的困扰）

** 极致成品模式下的互补Skill自动搭配:**

```
CAP:DESIGN → brainstorming (主) + design-consultation (辅,设计系统)
            → 互补: 一个做方案,一个出设计tokens,不冲突

CAP:BROWSER_TEST → qa (主) + playwright-skill (辅,自动化脚本)
                 → 互补: 一个交互测试,一个脚本自动化

CAP:TDD_ENFORCE → tdd (主,Matt Pocock) + test-driven-development (后备铁律)
                → 互补: 一个教术,一个教律,双重保障

CAP:CODE_REVIEW → review (主,gstack) + codex (辅,第二意见)
                → 互补: 一个审代码,一个出挑战

去重: 纯重叠的只留最优(如两个同功能Skill取加权分高的)
```

** 极速模式下的裁剪:**

```
CAP:DESIGN → brainstorming (仅1个,跳过design-consultation)
CAP:BROWSER_TEST → Hermes内置browser (最轻)
CAP:CODE_REVIEW → review (仅1个,跳过codex)
所有nice-to-have能力 → 全跳过
行业插件 → 全跳过
复盘 → 全跳过
```

---

## 环境感知 & 主动提示

### 策略 vs 环境匹配检测

Phase -3 扫描后，评估当前Skill池能否满足所选策略的质量目标：

```
扫描结果: 273 Skill → 极致成品: ✅ 可达S级
扫描结果: 50 Skill  → 极致成品: ⚠️ 仅可达B级
扫描结果: 10 Skill  → 极致成品: ❌ 仅可达C级
```

**当环境不满足策略目标时，主动弹窗:**

```
「当前环境 Skill 池(50个)无法达到极致成品S级标准。
 缺失能力: CAP:DESIGN_REVIEW, CAP:SECOND_OPINION, CAP:DX_REVIEW...
 
 选择:
 A) 接受降级到B级(继续执行)
 B) 切换到均衡模式(推荐 — 当前环境可达到均衡A级)
 C) 安装缺失Skill后再执行(列出建议安装清单)
 D) 强制继续(标记为降级执行)」
```

### 别人使用时的自动适配

```
场景: 用户B有30个Skill，选均衡模式

Phase -3扫描 → 发现缺 qa, codex, cso
Phase -0.5匹配 → 自动裁剪:
  CAP:BROWSER_TEST → 降级 playwright-skill
  CAP:SECOND_OPINION → 静默跳过(均衡模式不激活)
  CAP:SECURITY_AUDIT → 降级 requesting-code-review安全扫描部分

结果: 不弹窗,不报错,静默适配出B的专属流水线
```

---

## 能力抽象标签体系

```
critical:     VALIDATE SHARPEN DESIGN PLAN IMPLEMENT VERIFY
important:    DESIGN_REVIEW ARCH_REVIEW BREAKDOWN TDD_ENFORCE DEBUG 
              CODE_REVIEW SECURITY_SCAN BROWSER_TEST SECURITY_AUDIT SHIP CONTEXT_SAVE
nice_to_have: DX_REVIEW SECOND_OPINION CODE_HEALTH DOCUMENT RETRO LEARN
industry:     ACADEMIC_REVIEW FINANCE_COMPLY LEGAL_REVIEW CREATIVE_POLISH PHOTO_CHECK
```

---

## 加权仲裁（多Skill竞争）

| 维度 | 权重 | 评分规则 |
|------|------|---------|
| 同生态优先 | 30% | gstack系+1.0 / matt-pocock+0.8 / superpowers+0.6 / 无关0 |
| 专用>通用 | 25% | 精确命中+1.0 / 模糊覆盖+0.3 / 兜底0 |
| 版本优先 | 20% | 最新+1.0 / 次新+0.5 / 无版本号0 |
| 安全评级 | 15% | Safe+1.0 / Low+0.7 / Med+0.4 / High+0.1 / Critical 0 |
| 历史成功率 | 10% | 该Skill在此能力上的实际成功率（默认0.5，执行后动态更新） |

### 历史成功率追踪

每次委派执行后，记录结果到 `~/.hermes/ideas/success-rates.json`：

```json
{
  "brainstorming": {"CAP:DESIGN": {"success": 12, "total": 14}},
  "tdd": {"CAP:IMPLEMENT": {"success": 20, "total": 20}},
  "review": {"CAP:CODE_REVIEW": {"success": 8, "total": 11}}
}
```

成功率 = success / total（无记录→默认0.5）。每 10 次委派后重新计算一次权重，写入日志 `WEIGHT_UPDATE` 事件。

---

## 降级链 + 兜底

```
CAP:VALIDATE → office-hours → plan-ceo-review → brainstorming → 🧑人工引导
CAP:DESIGN → brainstorming → design-consultation → idea-superpowers-suite → 🧑人工填写
CAP:BROWSER_TEST → qa → playwright-skill → Hermes browser → 🧑人工测试清单
CAP:IMPLEMENT → tdd → test-driven-development → 通用coding → 🧑人工编码引导
CAP:CODE_REVIEW → review → codex → requesting-code-review → 🧑人工审查清单
CAP:SECURITY_AUDIT → cso → requesting-code-review → 🧑OWASP自查清单
CAP:RETRO → retro → context-save → 🧑人工复盘模板
```

🧑 兜底 = 人工引导模式: Agent出结构化问卷→用户逐项回答→最多3轮→标记继续。

降级失败自动重试3次，仍失败→标记为「待人工决策」。

---

## 全局可观测日志

`~/.hermes/ideas/logs/<timestamp>-<slug>.jsonl`

```
PHASE_START / CAP_MATCH(选什么+评分+原因) / CAP_DEGRADE(降级原因)
CAP_SKIP / CAP_FALLBACK(人工引导) / SURPLUS_INJECT(冗余注入)
PHASE_END / PIPELINE_DONE(总执行/跳过/降级/人工占比) / STRATEGY_SELECTED
```

日志保留 90 天，自动清理。

**自动Skill补全推荐（每次执行结束触发）:**

执行结束后，自动分析日志，生成Skill补全清单:

```
「📊 执行复盘 & Skill补全建议
 本次执行: 极致成品模式 → 实际: B级(降级)
 降级统计:
   CAP:BROWSER_TEST → qa缺失 → 降级 playwright-skill (3次)
   CAP:SECOND_OPINION → codex缺失 → 跳过 (2次)
 🎯 推荐安装:
   1. qa — 消除浏览器测试降级, 提升至A级
   2. plan-design-review — 恢复设计审查能力
 一键安装? [安装全部] [选择性安装] [跳过]」
```

推荐算法: 降级频率 × 能力优先级权重 → Top 5 → 附安装命令。

---

## 跨平台兼容

### 路径规范

所有路径使用 Hermes 内置变量，不硬编码：

```
${HERMES_HOME}/skills/              ← ~/.hermes/skills/ (Mac/Linux) 或 %USERPROFILE%/.hermes/skills/ (Win)
${HERMES_HOME}/ideas/               ← 工作流数据目录
${HERMES_HOME}/ideas/logs/          ← 日志目录
${HERMES_HOME}/ideas/tag-pool.json
${HERMES_HOME}/ideas/strategy-config.json
${HERMES_HOME}/ideas/capability-registry.json
${HERMES_HOME}/ideas/global-priority.json
```

### 命令兼容

```
文件列表:  search_files(target='files') 替代 ls/dir
文件搜索:  search_files(pattern=...) 替代 grep/findstr
文件读写:  read_file / write_file 替代 cat/echo
路径拼接:  os.path.join / pathlib 替代字符串拼接
编码:     UTF-8, LF换行, BOM头不写
```

### 平台检测

```
Mac:     sys.platform == 'darwin'
Linux:   sys.platform == 'linux'
Windows: sys.platform == 'win32'
```

## 调试模式

```
触发: 「foundry debug」「--debug」「调试模式」
效果:
  ├── 每阶段输出完整决策链路(为什么选这个Skill, 评分明细)
  ├── 降级/跳过/注入详细原因
  ├── 能力匹配候选列表+得分
  └── 不压缩日志, 输出完整内部状态

关闭: 「关闭调试」「--debug off」
```

## 版本查询

```
触发: 「foundry version」「版本号」「什么版本」
输出: Idea Foundry v9.1.0 · 方法集 · role: orchestrator
```

## 交互控制

```
触发: 「foundry hold」      → 暂停, 保存当前状态
触发: 「foundry resume」    → 恢复暂停的流程
触发: 「foundry restart」   → 重置, 清除进度从头开始
```

**所有 `clarify()` 菜单末尾自动追加 `← 上一步` 选项。** 用户选中后回退到上一个交互节点重选。CLI 环境用方向键 ↑↓ 导航，Web 环境用数字回复。

## 自检命令

```
触发: 「foundry test --self」「自检」「跑一遍自检」

执行流程:
  ① 自进化链路: 模拟一个不存在的领域标签 → 验证特征分析 → 验证追问弹窗 → 验证写入 tag-pool
  ② 成功率回写: 模拟一次委派 → 验证 success-rates.json 可读写 → 验证权重重新计算
  ③ careful 开关: 模拟 Phase 8 → 验证 careful 启用 → 模拟 Phase 11 → 验证 careful 关闭
  ④ 能力扫描: 扫描本地 Skill 池 → 验证能力映射表构建 → 列出缺失的关键能力

输出格式:
  自进化链路    ████████████ ✅ 通过
  成功率回写    ████████████ ✅ 通过
  careful 开关  ████████████ ✅ 通过
  能力扫描      ██████████░░ ⚠️ 缺 CAP:DESIGN_REVIEW
  ────────────────────────────
  3/4 通过, 1 警告
```

**纯只读验证，不修改任何状态文件。** 模拟写操作使用临时文件，验证后删除。

## 配置文件重载

```
触发: 「foundry reload」「重载配置」
效果:
  ├── 重新读取 tag-pool.json
  ├── 重新读取 strategy-config.json
  ├── 重新扫描本地Skill池
  └── 无需 /reset, 实时生效
```

## 错误处理

| 错误场景 | 友好提示(非堆栈) |
|---------|----------------|
| tag-pool.json 损坏 | 「⚠️ 标签池配置损坏, 已使用内置默认标签。修复: 删除后重启自动重建。」 |
| strategy-config.json 缺失 | 「⚠️ 策略配置未找到, 已使用默认三模式。创建: foundry init」 |
| Skill目录不存在 | 「⚠️ Skill目录未找到, 能力扫描跳过。检查: ${HERMES_HOME}/skills/」 |
| 日志目录不可写 | 「⚠️ 日志目录不可写, 本次不记录日志。检查权限: ${HERMES_HOME}/ideas/logs/」 |
| 网络超时(扫描时) | 「⚠️ Skill扫描超时, 使用缓存的能力映射表。上次扫描: <timestamp>」 |

## 多语言

预设模式的提示文本支持中英文自动切换。

### 自动检测

工作流启动时读取系统语言环境，自动切换：

```
检测顺序:
  1. 用户显式设置(如「切成中文」)
  2. 环境变量 $LANG / $LC_ALL
  3. Hermes 配置 display.language
  4. 默认: en_US

语言代码映射:
  zh_CN / zh_TW / zh_* → 中文
  en_US / en_GB / en_* → English
  其他 → English (fallback)
```

### 手动切换

```
触发: 「foundry lang zh」「foundry lang en」「切换到英文」
效果: 立即切换, 写入 ~/.hermes/ideas/.lang 持久化
```

### 提示文本示例

```
zh_CN → 「 极致成品 — 完美交付, 不惜Token」
en_US → 「 Perfection — Maximum quality, full pipeline」

zh_CN → 「质量预检报告 · 当前环境可达 A级」
en_US → 「Quality Check · Environment can reach Grade A」

zh_CN → 「⚠️ 标签池配置损坏, 已使用内置默认标签」
en_US → 「⚠️ Tag pool config corrupted, using built-in defaults」
```

```
实例A (273Skill) + 极致 → S级完整流水线
实例B (50Skill)  + 极致 → ⚠️弹窗: 仅可达B级,接受降级?
实例B (50Skill)  + 均衡 → A级,静默适配,不弹窗
实例C (10Skill)  + 极速 → 自动用最简链路,不弹窗
实例D (任意Skill) + 任意策略 → 先读池→后匹配→出专属流程
```

---

## 成功案例

- [计划文档写作标准](references/plan-writing-standards.md) — 每步必带「为什么」，交付物必须解释存在理由（2026-06-24）
- [计划质量规范](references/plan-quality-standards.md) — 计划四要素：目的 / 每步「为什么」/ 验收标准 / 自查清单（2026-06-26）
- **Hermes 自省引擎（2026-05-19）** —— 完整 极致成品 流水线：Phase -4→-3→-2→-1→-0.5→brainstorming→writing-plans→execution。产出 v2.2.0 Skill + GitHub 开源。详见 `references/case-self-reflection-engine.md`。
- **skill-matcher 插件设计逼问（2026-06-04）** —— 用 8 维逼问法审查 A+B 混合架构，暴露 8 个盲区并全部决策落地。方法论见 `references/design-grill-methodology.md`。
- **教育学会论文需求逼问（2026-06-05）** —— 8 维逼问法适配论文写作场景，暴露素材来源、多篇差异化、格式规范等盲区并全量决策。方法论见 `references/paper-grill-methodology.md`。
- **金融子 Agent 分析深度增强（2026-05-18）** —— 金融领域专用流程，详见 brainstorming 技能内的 `brainstorming-case-finance-enhancement.md`。
- **Go CLI → HTTP 封装模式（2026-06-24）** —— main() 替换法：算法代码不动、只换入口。Go CLI 封装为 REST API 供 Agent 调用。详见 `references/go-cli-to-http-wrapper.md`。
- **心理物理检测系统（2026-06-24）** —— 完整 Ph-4→brainstorming→设计文档。Go QUEST+ 算法 + Hermes + MCP + REST API 四层架构，Mac Mini 局域网部署。产出设计文档 `~/.hermes/plans/psychophysics-test/design.md`。

## 全局调度机制（角色声明制）

**Idea Foundry 以 `role: orchestrator, stage: dispatch` 定位为全局调度中枢。**

> **角色声明制 (v9):** 废除数字优先级。CMG 以 `role: guard, stage: pre_action` 在 Foundry 之前执行护栏检查，Foundry 以 `role: orchestrator, stage: dispatch` 接管调度。通过阶段分离协作，非数字竞争。

### 调度层级（角色声明制）

```
role: orchestrator, stage: dispatch   Idea Foundry (本引擎)  ← 全局调度中枢
    │
    ├── 领域子流程                    ← Foundry 内部路由
    ├── 能力匹配的 Skill (主)         ← Foundry 调度执行
    ├── 能力匹配的 Skill (辅)         ← 互补注入
    ├── 降级替代 Skill                ← 缺失时启用
    ├── 外部原生工作流                ← 仅作备选降级
    └── 人工引导模式                  ← 最后兜底
```

### 调度规则

**1. 全局接管**

当用户需求触发工作流时，无论环境中有多少工作流引擎（Superpowers、Idea Workflow、原生 brainstorming/TDD 链路等），Idea Foundry **始终最先触发**，接管全局控制权。

```
用户需求
    │
    ▼
Idea Foundry (orchestrator) ← 最先触发，抢占控制权
    │
    ├── 领域识别 → 策略选择 → 能力匹配
    │
    ├── 调度 Brainstorming (作为 CAP:DESIGN 的匹配Skill)
    ├── 调度 TDD (作为 CAP:IMPLEMENT 的匹配Skill)
    ├── 调度 Superpowers writing-plans (作为 CAP:PLAN 的匹配Skill)
    └── ...
    
外部原生工作流 → 仅当 Foundry 降级链耗尽时作为备选启用
```

**2. 内部择优调度**

Foundry 接管后，不直接执行——而是作为调度中枢，根据能力需求和加权仲裁规则，将每个阶段**委派**给最匹配的子 Skill：

```
Phase 3: 方案设计 → CAP:DESIGN → 加权仲裁 → 委派 brainstorming (0.785)
Phase 5: 架构评审 → CAP:ARCH_REVIEW → 加权仲裁 → 委派 plan-eng-review (0.820)
Phase 8: 开发实现 → CAP:IMPLEMENT → 加权仲裁 → 委派 tdd (0.910)
```

**🛡️ 实现阶段安全保护:** 进入 CAP:IMPLEMENT 时自动启用 `careful`，Phase 11 交付后自动关闭。借用已有安全网，不新增拦截。

**3. 外部工作流降级**

其他原生工作流（Superpowers 完整链路、brainstorming→writing-plans→TDD 原生链）**不作为主流程运行**，仅在 Foundry 能力匹配全部失败时作为降级备选：

```
CAP:DESIGN 缺 brainstorming, design-consultation, idea-superpowers-suite
  → 降级链耗尽
  → 启用备选: 外部原生 brainstorming 工作流
  → 🧑 人工引导 (最后兜底)
```

**4. 调度冲突解决**

当多个 Skill 同时注册为「全局调度引擎」时：

| 优先级 | 引擎 | 处理 |
|--------|------|------|
| 调度中枢 | Idea Foundry | 始终优先（role: orchestrator） |
| 外部引擎 | Superpowers (idea-superpowers-suite) | 降级为Foundry的CAP:PLAN匹配Skill |
| 外部引擎 | GStack (autoplan) | 降级为Foundry的CAP:SHARPEN+DESIGN_REVIEW+ARCH_REVIEW匹配Skill |
| 原生链路 | 原生 brainstorming→TDD链路 | 降级为Foundry的独立能力Skill |

**同优先级仲裁规则：** 当多个引擎声明相同优先级时，按以下顺序自动排序：

```
版本号(降序) → 发布时间(降序) → 名称哈希(升序)
```

Idea Foundry 内置 `force_primary: true` 标记，**同优先级下依然抢占调度权**。

**调度排他开关：** 用户可一键开启独占全局调度，所有其他引擎强制降级为能力Skill，不参与调度竞争。

```
触发: 「独占调度」「只走Foundry」「锁定Foundry」
关闭: 「取消独占」「允许其他引擎」「解锁Foundry」
```

**修改本 Skill 前必须加载 `writing-skills` 走 TDD 流程，发布前必须加载 `hermes-agent-skill-authoring` 跑 PRE-RELEASE GATE。已在 CMG rules/ban/ 下永久记录违规。**

Foundry 自身不可用时（Skill文件损坏/缺失），自动退化为直接能力匹配模式，不阻断流水线。

---

## ⛔ 检查点铁则（不可跳过）

以下节点**必须**执行对应行为，跳过即违规，需回退重来：

| 节点 | 必需行为 | 跳过后果 |
|------|---------|---------|
| 加载时 | 判断「跑/过/走一遍」→ 是执行workflow不是读文档 | 读文档停住 = 违规 8（不理解意图） |
| Phase -4 策略选择后 | `clarify()` 让用户选策略 | 未选策略 = 流水线不可启动 |
| 质量预检完成后 | `clarify()` 确认等级/是否继续 | 降级决策无据可查 |
| Phase -3/-2/-1/-0.5 每阶段 | 输出 ≥8 行 + `clarify()` 确认 | 输出不足 = 违规 1（黑箱操作） |
| 用户中途切换模式 | 重跑 Phase -3 + -0.5 + 新质量预检 | 不重扫 = 违规 5（旧裁剪表跑新模式） |
| 设计分段确认 | 每段设计展示后 `clarify()` | 纯文本问 = 违规 2 |
| Brainstorming 阶段 | 每段设计确认用 `clarify()` 选择题 | 纯文本 = 违规 4 |
| Phase -1 拼接后 | 排查误标的「参考类」依赖 | 注入仅参考 Skill = 违规 6 |

这些不是「自检建议」，是「Phase 步骤的一部分」。Agent 加载本 Skill 后**立即读取本表**，逐条对应当前 Phase。

## 🚨 常见执行违规（来自真实教训）

以下是我（Agent）在执行 idea-foundry 时**实际犯过的错误**，每次加载此 Skill 时必须自检：

### 违规 1：跳过 Phase 输出

**症状：** Phase -4 策略选择后，Phase -3/-2/-1/-0.5 只给一句"扫描通过，S级可达"，不展示完整的能力映射表、领域权重、主干拼接、策略匹配。

**为什么错：** 用户看不到决策过程，无法验证能力匹配是否正确。Foundry 的价值一半在**可观测**，跳过输出等于黑箱操作。

**正确行为：**
```
Phase -3 → 完整列出每个能力标签匹配的 Skill + 评分
Phase -2 → 列出领域分类 + 权重
Phase -1 → 列出主干流水线 + 插件注入
Phase -0.5 → 列出每个能力的激活/跳过决策 + 原因
质量预检 → 完整彩色进度条报告
```

每阶段至少 8-10 行输出，不可压缩成一行。

### 违规 2：用纯文本代替 clarify() 选择题

**症状：** 设计呈现后问"这部分 OK 吗？继续讲 Skill 行为定义？"——纯文本，没有用 clarify()。

**为什么错：** CLI 环境下用户期望方向键菜单。纯文本问题让用户不知道该选什么、怎么回应。Foundry 文档明确规定 CLI 用 `clarify()` 做方向键菜单。

**正确行为：** 任何需要用户确认/选择的节点，**必须**使用 clarify()：
- 策略选择 → clarify(choices=[...])
- 质量预检确认 → clarify(choices=[...])
- 设计分段确认 → clarify(choices=[...])
- 方案选择 → clarify(choices=[...])

**唯一例外：** 信息收集型问题（"你的源目录是什么？"）可用纯文本。

### 违规 3：被现有 Skill 话题相似性误导

**症状：** 用户说「帮我做一个AI筛图工具」，Agent 发现了 photo-organizer-pro（AI照片评分），直接加载 brainstorming + photo-organizer-pro 开始设计，跳过了 idea-foundry。

**为什么错：** 已记录在反模式章节，但仍是高频违规。关键判断：用户说的是「做」还是「用」。

### 违规 4：Brainstorming 阶段不用 clarify()

**症状：** 进入 brainstorming 后，每段设计确认都用纯文本，不用 clarify 选择题。

**为什么错：** Brainstorming 规范明确要求「Multiple choice preferred」。即使是子 Skill，也必须遵守自身的交互规范。

### 违规 5：中途切换模式不重走 Phase -3 扫描

**症状：** 用户从极速切到极致，Agent 直接改了模式标签继续，没有重新执行 Phase -3 Skill 扫描和 Phase -0.5 策略裁剪。

**为什么错：** 不同模式的能力激活表完全不同（极速只走 critical，极致走全量）。不重扫 = 用极速的裁剪表跑极致模式，nice-to-have 全漏。

**正确行为：**
```
用户说「我要质量优先」/「换极致模式」/「切」
  → 确认切换
  → 重跑 Phase -3 (Skill 扫描) + Phase -0.5 (策略裁剪)
  → 重新输出质量预检报告
  → clarify() 确认
  → 继续
```

### 违规 6：Phase -3 注入「参考类」Skill 标为「互补」

**症状：** 在能力匹配表中把 `memory-system-rules`、`hermes-memory-optimization` 标为「互补注入」，但实际它们仅供设计参考，不是运行时依赖。

**为什么错：** 「互补注入」意味着 Foundry 会主动调度它们，增加不必要的 token 消耗和依赖风险。参考类 Skill 应标为「仅参考」，不进入调度链。

**区分规则：**
| 标注 | 含义 | 调度？ |
|------|------|--------|
| 「互补保留」 | 两个 Skill 互补，都进入调度链 | ✅ |
| 「仅参考」 | 设计灵感来源，不进入调度链 | ❌ |
| 「本次新建」 | 当前项目产出 | ❌ (产出物) |

### 违规 8：加载文档 ≠ 执行 Workflow（"跑" vs "读"）— 2026-05-28 三次重犯

**症状：** 用户说「跑/过/走一遍IF」→ Agent 加载 SKILL.md 提取设计模式 → 停在"已加载，提取了X个设计模式" → 不进 Phase 流程。

**为什么错：** "跑IF" = 执行完整 Phase -4→-3→-2→-1→-0.5→质量预检→每阶段 clarify()。读文档 = 不是跑工作流。三次才做对：第一次读文档提取模式→写三文件声称"产出完毕"→用户拆穿；第二次 redo 直接写三文件仍不 clarify→用户骂"闷头干"；第三次才真正走 Phase。

**正确行为：**
```
用户说「跑一遍IF」→
  ① 加载 SKILL.md
  ② 立即进入 Phase -4：clarify() 策略选择
  ③ Phase -3→-2→-1→-0.5：每阶段 ≥8行 + clarify()
  ④ 质量预检 + clarify()
  ⑤ 最终输出 → 用户确认后才写入文件，禁止直接写好交差
```

**区分规则：**
| 用户说 | 正确行为 |
|--------|---------|
| 「跑一遍IF」「走IF流程」 | 执行完整 Phase + clarify |
| 「IF有什么设计模式」 | 读文档回答即可 |

### 违规 8：「跑/走/过一遍」≠「加载SKILL.md」

**症状：** 用户说「跑一遍 IF」「过一遍 brainstorming」，Agent 加载 SKILL.md → 提取设计模式 → 宣称"跑完了"。实际连 Phase -4 都没进。

**为什么错：** 「跑」= 执行完整 workflow（Phase -4 → -3 → -2 → -1 → -0.5 → 质量预检 + clarify），不是只读文档。用户连说三遍才执行正确，说明这是高频误解。

**正确行为：**
- 加载 SKILL.md 后 → **立即进入 Phase -4 策略选择**
- 不可停在「已加载，提取了设计模式」——那是读，不是跑
- 每阶段必须 clarify() 交互

**区分：**
| 用户说 | 正确行为 |
|--------|---------|
| 「跑一遍 IF」 | 执行 Phase -4 → 质量预检（完整 workflow） |
| 「IF 是怎么设计的」 | 读文档，解释架构 |
| 「提取 IF 的设计模式」 | 只读，不执行 |

### 违规 9：逼问时一次抛出全部维度（2026-06-05 论文逼问实战）

**症状：** 用户说"用IF逼问"，Agent 把8个维度全部展开成一大段文字一次性输出。用户两次喊"暂停"，然后说"重新用选择方式给我选项"。

**为什么错：** 逼问的本质是交互式——每个维度需要用户消化、思考、选择。8维一次性输出=阅读负担+决策疲劳。用户实际需要的是：**每次一个 clarify()，选完就下一个**，像问答通关。

**正确行为：**
```
维度 1 → clarify(choices=[...]) → 用户选 → 
维度 2 → clarify(choices=[...]) → 用户选 → 
...
维度 8 → clarify(choices=[...]) → 用户选 → 汇总
```

每个 clarify() 标注进度（如"维度 3/8"），让用户知道进度。选项控制在4-5个以内。

**适用场景：** 不仅是 8 维逼问法——任何"逐项审查"类流程（需求确认、方案评审、格式检查）都应按此节奏。用户说"暂停"=节奏太快了。

### 违规 11：稳定项目过度迭代（2026-06-09 DeepSeek 评审）

**症状：** DeepSeek 评审提了依赖预检、超时控制等建议，Agent 立刻规划 IF v9.1.0。用户制止：「IF算是迭代过度吗？现在已经很稳定了。」

**为什么错：** IF v9.0.1 降级链已兜底所有缺失场景。依赖预检（提前报错 vs 运行时降级）是 polish 级改进，不是 gap。升版前自问三问：①有重大新功能？②有重大bug？③有重大体验优化？三问全否→不做。

**正确行为：**
- 外部评审建议 → 逐条分析是否解决真实痛点 → 区分 polish vs gap
- 稳定项目的改动门槛高于新项目——不是不做，是必须证明必要性
- 用户说「已经很稳定」= 不要为了改而改

### 违规 13：计划文档缺少「为什么」和「完成标准」（2026-06-26 实战）

**症状：** 写了一份详细的实施计划——任务列表、交付物清单、架构图全有。用户反复追问：「为什么用 Mac Mini？」「为什么改 main()？」「为什么做公网访问？」「写了目的吗？」。计划是「做什么」的清单，不是「为什么做」的解释。

**为什么错：** 计划文件有双重读者——执行者（需要知道怎么做）和介绍对象（需要知道为什么）。只写怎么做，不给原因，别人看不懂也说服不了自己投入。

**正确做法：**
1. 计划必须有「目的」章节——这个阶段要验证什么核心假设？（2-3 句）
2. 每一步/每个交付物附带「为什么」——不是技术原因，是决策逻辑
3. 完成标准必须量化可验证（不是「API 能跑」，是「外部开发者从公网调通一次完整测试」）
4. 文档风格：专业度不减，但小白也能跟读——两种读者都能受益
5. 把讨论中你举例的参考模型（和风天气/高德）放计划里

**交付物对比：**
```
❌ | 交付物 | 说明 |
   | server.go | Go HTTP 代码 |
   
✅ | 交付物 | 为什么要这个 |
   | server.go | 当前 Go 程序是 CLI 交互（等键盘输入）。API 服务需要等 HTTP 请求。改 main() 不改算法——算法已经是对的，只换入口 |
```

### 违规 12：clarify() choices 用 emoji 导致终端框对不齐（2026-06-09 修复）

**症状：** clarify() 选项含 🏆⚖️⚡ 等 emoji → 终端宽度计算错误 → 选择框错位、框不住文字。

**根因：** emoji 在不同终端实现中列宽不同（1 或 2），Hermes CLI 宽度计算假设固定列宽。

**修复：** IF 全量清除 62 处 emoji（🏆⚖️⚡📝💰✏️），改用纯文本。

### 违规 13：用户喊停后继续推进（2026-06-24 单次会话 2 次）

**症状：** clarify() 超时或用户说"停"，Agent 未等确认就跳到下一阶段——直接说「继续。下一层——」或跳到下一设计节点。

**为什么错：** 「停」= 用户需要更多时间、想回头看上一个问题、或在外部参考分析。超时不等于同意。未经确认推进 = 替用户做决定。

**正确行为：**
- 用户说「停」→ 立即停止当前流程，问「哪里需要重新讨论？」
- clarify() 超时 → **重发同一个 clarify()**，附「等你决定」
- 绝不在未确认状态跳到下一阶段
- 如果用户说「先继续别的」→ 标记当前节点未决
- 节奏由用户掌控

**本会话两次触发：** ① clarify() 超时直接跳过 MCP 确认 → 用户喊停 ② 用户说「停我都没决定呢。之前也是」——累计效应，第一次就该修正。

**自检清单追加项：** `[ ] clarify() 超时 → 重发，不跳步？`

### 违规 14：clarify() 超时自动跳下一步（2026-06-24 心理物理检测实战）

**症状：** clarify() 发出后用户未在时限内选择，Agent 直接说「继续。下一层——」跳过未确认的设计节点，进入下一阶段。用户喊停：「停我都没决定呢。之前也是」。

**为什么错：** clarify() 超时不等于用户同意。用户可能在思考、在看豆包分析、在忙别的事。未收到明确确认就往前推进 = 替用户做决定。

**正确行为：**
- clarify() 超时 → 重新发出同一个 clarify()，附「等你决定」
- 绝不在未确认状态下跳到下一阶段
- 如果用户明确说「先继续别的」→ 标记当前节点未决，后续回来补确认
- 节奏由用户掌控，Agent 只负责等待

**症状：** IF Phase -3 能力映射时，根据 skills_list 返回的索引推荐了多个 skill。用户要求「确认全都真实存在？不是你瞎编自己造的？」→ skill_view 验证发现其中 2 个加载失败（SKILL.md 缺失/损坏）。

**为什么错：** skills_list 返回的是名称索引，不保证每个 skill 的 SKILL.md 完整可用。在列表 ≠ 能加载。

**正确行为：**
- Phase -3 能力映射时，对每个候选 skill 调用 skill_view() 确认加载成功
- 加载失败 → 标注「❌ 不可用」+ 提供替代方案
- 禁止仅凭 skills_list 推荐 skill

**区分规则：**
| 数据源 | 可信度 | 用途 |
|--------|:---:|------|
| skills_list | 索引级 | 发现候选 skill |
| skill_view() 成功 | 验证级 | 确认可用，方可推荐 |
| skill_view() 失败 | 不可用 | 标注替代方案 |

### 违规 7：设计阶段未排查外部依赖

**症状：** 设计自省引擎防偷懒清单时，直接把 `ralph-loop` 写入架构，「checklists/ 依赖 ralph-loop skill」。

**为什么错：** 「借鉴设计灵感」≠「声明为依赖」。用户一句话拆穿——「这不就锁死绑定 ralph-loop 这个 skill 了吗？又不是我独有的，使用率就大大降低了，还有侵权风险。」

**正确行为：**
- Phase -1 拼接时，对每个注入的 Skill 做依赖审核：
  - 被调度执行（互补）？→ 保留
  - 设计灵感/方法论（仅参考）？→ 摘除依赖，内置实现
- 最终产出必须零外部依赖
- 灵感来源在 spec 注明即可，不进入运行时依赖链

### 自检清单（每次加载 idea-foundry 时过一遍）

```\n[ ] 用户请求是否触发接管？→ 是 → 继续，否 → 退出\n[ ] 用户说「跑/走/过一遍」→ 是执行完整workflow，不是读文档？→ 是<br>[ ] Phase -4 是否用了 clarify() 选择策略？→ 是\n[ ] Phase -3/-2/-1/-0.5 是否完整输出了 ≥8 行/阶段？→ 是\n[ ] Phase -1 拼接时是否排查了误标的「参考类」依赖？→ 是\n[ ] 质量预检是否完整展示？→ 是\n[ ] 质量预检确认是否用了 clarify()？→ 是\n[ ] 所有后续用户确认是否用了 clarify()？→ 是\n[ ] 是否有被话题相似的现有 Skill 误导？→ 否\n[ ] 用户切换模式时是否重跑了 Phase -3 + Phase -0.5？→ 是\n[ ] Skill 匹配表中是否有误标为「互补」的「仅参考」Skill？→ 否
[ ] clarify() 超时/用户喊停 → 重发，不跳步？→ 是
[ ] 用户说「停」→ 立即停止推进，问「哪里需要重新讨论」？→ 是\n```

---

## 后续版本规划（v10+）

> 以下方向来自外部评审（豆包 AI）与实战反馈。非紧急，积累至下个大版本统一发布。

| # | 方向 | 说明 | 涉及 |
|---|------|------|------|
| F1 | 循环依赖检测 | Phase -1 拼接时检测 A→B→A 环路，警告用户 | Phase -1 |
| F2 | 超时控制 | 委派子 Skill 执行超时（如 600s）→ 自动降级下一候选 | Phase 执行 |

### 已排除

| 建议 | 排除原因 |
|------|---------|
| 事务性/回滚 | 跨 Skill 事务在 Hermes 架构下不现实 |
| 数据适配层 | 复杂的输入输出规范化不属于调度器职责 |
| 崩溃恢复 | Hermes 会话级恢复已覆盖，IF 无需重复实现 |

### 已知缺口

| # | 缺口 | 影响 | 优先级 |
|---|------|------|:---:|
| G1 | `idea-superpowers-suite` 子 skill 未安装 | CAP:DESIGN 降级链第三级断档（前两级 brainstorming/design-consultation 已兜底，非阻塞） | 低 |
| G2 | `priority: 110` 数字优先级已从 frontmatter 移除 | v9 已清理 | - |
