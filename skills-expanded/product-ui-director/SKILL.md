---
name: product-ui-director
license: MIT; see LICENSE and NOTICE.md
compatibility: Python 3.x. Browser acceptance should use ego-browser when available.
description: 何庆丰定制的产品 UI/UX 设计、实现与验收 Skill。凡是新建、改版、评审或迭代 Web、移动端、桌面端界面，设计系统、页面、组件、交互、响应式、可访问性、配色、字体、数据图表或视觉质量时必须使用。覆盖需求简报→设计系统→差异化视觉→代码实现→真实浏览器验收→迭代记录，内置可搜索 UI/UX 数据和项目级设计记忆。
metadata:
  owner: macistone71-jpg
  edition: heqingfeng-product-ui
  upstream: nextlevelbuilder/ui-ux-pro-max-skill@8bd29e7
---

# Product UI Director｜何庆丰定制版

把“做得好看”改成可复用的产品工程：**先理解产品，再建立设计系统；先形成差异，再写代码；最后必须在真实浏览器验收。**

## 必须使用的场景

- 新产品、页面、落地页、工作台、仪表盘、移动端或桌面端 UI；
- 修改布局、配色、字体、间距、导航、表单、动效、图表和响应式；
- 用户说“不专业、太像 AI、信息太乱、移动端崩、交互别扭”；
- UI 代码评审、上线前验收、竞品视觉分析和设计系统沉淀。

纯后端、数据库、部署或不改变界面体验的任务不加载本 Skill。

## 不可跳过的原则

1. **产品先于风格**：先确认目标用户、核心任务、使用频率、平台、内容密度和风险，再选风格。
2. **真实内容先于占位图**：不得用虚构指标、虚假评价、无意义 lorem 或装饰性数字冒充产品证据。
3. **差异化先于模板**：禁止无理由使用“AI 紫色渐变 + 三张玻璃卡 + 巨大圆角”的默认 AI 审美。
4. **一项目一套设计记忆**：已有 `design-system/<slug>/MASTER.md` 时先读，不得静默覆盖。
5. **功能正确优先**：视觉不得破坏业务链路、数据状态、错误恢复、键盘导航和移动端可用性。
6. **真实验收**：不能只看代码宣布完成；必须打开页面、操作核心链路并检查至少 390px 与桌面视口。
7. **保留来源**：本 Skill 基于 MIT 开源项目定制，许可证与上游归属不得删除。

## 六阶段工作流

### 0. 读取现场

- 读取 PRD、README、已有页面、品牌资产、技术栈和最近改动；
- 检测技术栈，不能硬猜；
- 查找并读取现有 `design-system/**/MASTER.md`、页面 override、UI 验收报告；
- 新产品需要浏览 3–5 个直接或邻近竞品的官方页面，记录结构与交互，不复制视觉皮肤。

### 1. 建立产品 UI Brief

至少明确：产品任务、受众、平台、首要 CTA、关键信息、风险、内容密度、品牌性格、无障碍要求、支持视口。信息可从项目推断时直接推进，不反复询问。

需要创建项目文档时运行：

```bash
python3 scripts/qf_project_init.py --project-root <项目根目录> --project-name "项目名" --product-type "产品类型" --platform web
```

脚本默认不覆盖已有文件。

### 2. 生成并持久化设计系统

新项目或系统级改版必须运行：

```bash
python3 scripts/search.py "<产品类型 行业 风格约束>" --design-system --persist -p "项目名" --output-dir "<项目根目录>"
```

可用调节器：`--variance 1-10`、`--motion 1-10`、`--density 1-10`。工作台通常提高 density；内容产品降低 density；motion 只服务状态与因果。

已有 MASTER 时先读；除非用户明确授权，不得 `--force`。

### 3. 建立“产品签名”

每个产品至少定义 3 项可识别但不妨碍使用的签名：

- 一个版式签名（如编辑部网格、制片时间线、纸张式阅读区）；
- 一个信息签名（如质量门禁、证据链、审核状态）；
- 一个交互签名（如排练模式、局部重做、渐进式预览）。

签名必须来自产品机制，不靠随机渐变、过量动效或装饰图形。

针对何庆丰现有产品类型，按需读取 `references/heqingfeng-product-patterns.md`。

### 4. 实现与针对性检索

只查询当前问题，不一次加载全部规则：

```bash
python3 scripts/search.py "keyboard focus modal" --domain ux
python3 scripts/search.py "dashboard dense filters" --domain style
python3 scripts/search.py "form error recovery" --domain ux
python3 scripts/search.py "responsive card grid" --stack <检测到的技术栈>
```

查询空结果时只缩窄重试一次；仍为空要明确使用通用规则，不能伪造数据库命中。

实现要求：

- 使用语义 token，不在组件中散落无意义颜色和间距；
- 正文移动端默认至少 16px，控件具备可见 label；
- Web 键盘焦点可见；触控目标按平台规范；
- 不依赖 hover 完成主任务；
- 异步流程有加载、成功、错误和恢复；
- 动画尊重 `prefers-reduced-motion`；
- 长中文、长英文、URL、数字和空数据都不破版。

### 5. 真实浏览器验收

页面可运行时必须使用浏览器完成核心任务。优先调用已安装的 `ego-browser` Skill：

1. 桌面视口约 1440px：首屏层级、核心链路、弹窗/表单/导出；
2. 移动视口 390px：确认 `scrollWidth === innerWidth`，无水平溢出；
3. 键盘操作：焦点可见、顺序合理、Esc/返回可恢复；
4. 状态：空、加载、错误、成功、禁用；
5. 可读性：对比度、长文本、缩放、减少动效；
6. 记录实际结果，不把“存在代码”写成“验收通过”。

Web/桌面验收读取 `references/quick-reference.md` 的 §1–§3；原生/移动端交付前读取 `references/pro-rules.md`。

可先运行静态预检：

```bash
python3 scripts/product_ui_audit.py <项目根目录> --format markdown
```

静态结果只是风险提示，不能替代浏览器验收。

### 6. 沉淀迭代记忆

交付时更新：

- `design-system/<slug>/MASTER.md`：稳定设计规则；
- `design-system/<slug>/pages/<page>.md`：页面差异；
- `design-system/<slug>/DECISIONS.md`：重要取舍与原因；
- `design-system/<slug>/UI-ACCEPTANCE.md`：视口、任务、状态、缺陷和证据。

只记录真实验证。灰度数据、转化率、采用率未采集时标记“待验证”。

## 质量优先级

1. Accessibility：对比、焦点、键盘、语义、替代文本；
2. Touch & Interaction：目标尺寸、反馈、错误恢复；
3. Performance：图片尺寸、CLS、字体、主线程；
4. Product Fit：风格是否匹配产品任务；
5. Responsive：移动优先、无水平溢出；
6. Typography & Color：字级、行高、语义颜色；
7. Motion：只表达因果，可中断、可减少；
8. Forms & Feedback；9. Navigation；10. Charts。

完整规则按需读取 `references/quick-reference.md`。

## 交付硬门禁

以下任一项存在，不得宣布 UI 完成：

- 主任务无法完成，或按钮只有视觉没有行为；
- 390px 产生水平滚动；
- 无来源却展示虚构用户数字、效果指标或评价；
- 表单没有 label、错误原因或恢复路径；
- 图标按钮无可访问名称，键盘焦点不可见；
- 文本/关键控件对比度明显不达标；
- 弹窗无法关闭，返回破坏状态，固定栏遮挡内容；
- 只检查了代码，没有运行和操作页面；
- 新项目没有设计系统，或擅自覆盖已有 MASTER。

## 本地知识库

本 Skill 保留上游可搜索数据：79 种风格、192 类产品与配色/推理、74 字体组合、119 UX 指南、图标、动效、图表和 22 类技术栈。`scripts/search.py` 与数据文件来自上游，定制工作流、项目模板和验收工具由本仓库新增。
