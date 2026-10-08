# 起手 Prompt — Step 1：建立全新设计系统

**怎么用**：截完那 4 张关键截图后，新开一个 Claude Design session，把下面 `===` 之间整段**复制粘贴**进去，并把 `01_REDESIGN_BRIEF.md`（第 1–3 节）+ 4 张截图 + `02/03` 文案文件一起拖进去。先**只建设计系统**，确认满意后存为 Design System，再进 Step 2 按 flow 做屏。

文末附 **Step 2 每个 flow 的可复用模板**。

---

## Step 1 Prompt（复制这段）

```
我要为一款留学申请 App 做全新视觉设计。这一步只建立设计系统，先不做所有页面——
请产出一套完整的视觉语言 + design token，并用 1 个最复杂的屏（Home 仪表盘）验证落地效果。

【产品背景】
- 留学申请一站式 App。核心功能：选校、录取概率预测、AI 文书助手、真实录取案例库、申请时间线、社区。
- 用户：中国高中生（主申美本）+ 他们的家长。高风险、高决策（家长付费）、信息密度高
  （GPA、SAT、录取率、概率、deadline 满屏数据）。
- 双语：中文 + 英文，中文更长更密，排版要同时兼容。
- iOS + Android；必须同时支持浅色 + 深色。

【情绪目标】
既要让家长信任（专业、可靠、有学术分量），又要让学生向往（年轻、有抱负、不土气）。
关键词：可信 / 抱负 / 清晰 / 高级。避免：幼稚卡通、廉价感、过度花哨。

【第一步：先给我 2–3 个视觉方向（mood board 级别的小预览）让我选】
可参考以下方向，也可自由发挥或融合：
  A.「学术常春藤」沉稳深色主调 + 克制的金/铜点缀，像高端教育品牌。
  B.「现代抱负」干净中性底 + 一个有活力的主色（蓝/紫/青），数据可视化亮眼。
  C.「温暖陪伴」柔和暖色、圆润、亲和，降低申请焦虑感。
每个方向各给一个小预览（主色 + 一张卡片示例）。我选定一个之后你再展开完整系统。

【第二步：选定方向后，产出完整设计系统】
1. Color：浅色 + 深色两套。语义色板（background / surface / card / foreground / muted /
   border / primary / secondary / accent / success / warning / danger / info），
   外加数据可视化专用色（图表色、概率高/中/低、选校 tier 的 reach/match/safety）。
2. Typography：字号阶梯（最小 12px，符合 WCAG），中英文都要好看；
   标题 / 正文 / caption / 大号统计数字 各级样式。
3. Spacing / Radius / Elevation：间距阶梯、圆角阶梯、阴影与层级。
4. Iconography：图标风格基调（线性/面性、粗细、圆角）。
5. 核心组件（每个都要 default + 关键状态 + 浅色/深色两版）：
   Button(primary/secondary/danger/ghost)、Card、Input/TextArea、Select、RadioGroup、
   Checkbox、Switch、Slider、Badge(status/result/ranking/count)、Avatar、
   Tabs/Segmented control、Bottom sheet、Modal、ConfirmDialog、FAB、SearchBar、
   Chip/filter chip、Progress bar、Circular progress(完成度/概率环)、Stat card、
   List item、EmptyState、Skeleton、Toast、底部 Tab bar(6 个 tab)。

【第三步：用 Home 屏验证设计系统】
把这套系统应用到 Home 仪表盘，内容见我提供的 brief（渐变 Hero + 3 项统计、快捷入口网格、
完成度等级卡、选校 Tier 分布、即将截止倒计时、Top Schools 横滑、最近案例列表）。
给出浅色 + 深色两版。

【硬约束】
- 数据密度高：卡片和列表要能塞下大量字段还保持清爽，请参考我提供的截图里的真实密度。
- 触控目标 ≥ 44pt；注意刘海与底部安全区留白。
- 中文文案普遍比英文长，组件不要写死宽度，避免溢出/截断。
- 这是全新视觉：截图只作内容/密度参考，不要沿用旧样式。
```

---

## Step 2 Prompt 模板（每个 flow 重复用）

确认设计系统后，按 brief 第 5 节的 flow 分批做屏。每批粘贴这段、替换 `{}`：

```
继续用我们刚定的设计系统。现在设计 {Flow 名，如 "School Discovery"} 这一组屏：
{从 brief 第 5 节复制该 flow 的屏清单 + 每屏的内容块/数据/操作/状态}

要求：
- 严格复用已建立的设计系统组件与 token，保持与 Home 一致。
- 每屏都给出这些状态：默认 / loading(skeleton) / empty / error / 浅色 / 深色；
  受保护屏额外给"未登录"态。
- 截图仅作内容与密度参考，视觉全新设计。
- 我附了该 flow 的当前截图和 i18n 文案文件，文字以文案文件为准。
```

> ⚠️ 5 个空壳屏（Peer Review / Resume / Vault / Points / Verification）没有截图，
> 直接按 brief 里写的「intended content」设计。
