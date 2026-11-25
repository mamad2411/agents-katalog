---
name: agentic-html-editor
description: |
  AI 编辑/生成 HTML 页面工具（HTML Anything 工作流）：「Markdown 是草稿，HTML 是读者最终读到的形态」——
  检测本地已登录的 coding-agent CLI，把 Markdown/CSV/Excel/JSON/SQL/纯文本输入转成 ship-ready 的
  单文件 HTML 成品，覆盖杂志文章、keynote、简历、海报、小红书/X 卡片、web 原型、数据报告等 9 类版面，
  并一键导出微信/X/知乎或下载 .html/.png。
  当用户说「把这篇 md 转成能直接发公众号的排版」「生成一个 SaaS 落地页原型」「把 CSV 变成可视化报告页」
  时使用。
  不适用于：在编辑器里实时预览自己写的 .md 文件（转 markdown-preview-enhanced）。
source_project: nexu-io/html-anything
tags: [agentic-html-editor, html-anything, html-generation, 微信排版, agent-cli, 蒸馏技能]
---

# Agentic HTML Editor · AI 编辑/生成 HTML 页面工具

## R (Reading) — 上游原文

> "Markdown is the draft. HTML is what humans read. Your local agent writes it. … Local-first, zero API key, reuses the CLI session you already have logged in — **9 coding-agent CLIs** auto-detected on your PATH … driven by **75 composable skill templates** across **9 deliverable surfaces** (magazine articles · keynote decks · résumés · posters · Xiaohongshu cards · tweet cards · web prototypes · data reports · Hyperframes videos). One-click export to WeChat / X / Zhihu, or download `.html` / `.png`."
>
> — 上游 README.md（nexu-io__html-anything）

上游还写明反 AI 味硬约束的出处：「The discipline is lifted from alchaincyf/huashu-design's Junior-Designer mode + anti-AI-slop checklist. Constraints belong in the prompt — every SKILL.md writes them in.」（README.md §Six load-bearing ideas）

cli/README.md 描述 auto 命令的三层匹配：「第一层：强信号关键词匹配（零 token，毫秒级，命中即定）→ 第二层：规则打分匹配（内容 × 全部模板 metadata）→ 第三层：AI Summary 兜底（仅在规则失配时）」，全败时回退 deck-swiss-international 通用模板。

## I (Interpretation) — 方法论骨架

1. **读者优先的格式观**：Markdown 服务写作者，HTML 服务读者；交付给「人看」的东西应该是排版完成的 HTML 而非待渲染源码。「ship-ready 是底线」——生成结束即成品，不留「回头再修」的二手加工。
2. **不自带模型，复用本地 agent**：启动时扫描 PATH（含 GUI 进程常漏的 ~/.local/bin 等目录）检测 claude/codex/cursor-agent/gemini/copilot/opencode/qwen/aider/bob 九种 CLI；每个 CLI 一个薄适配器（argv + stdin 协议 + JSON-line 流解析），零 API key，直接吃用户已有订阅。
3. **模板即文件夹**：75 个 skill 模板遵循 Claude Code SKILL.md 约定（SKILL.md + example.html，frontmatter 含 mode/scenario/surface/preview/design_system 五字段）；mode（prototype/deck/frame/social/office）× scenario（design/marketing/engineering…）双轴组织选择器。
4. **模板匹配三层漏斗**（auto 命令）：强信号关键词规则（约 80 条，毫秒级命中，如简历→resume-modern）→ 全模板 tags/名称/描述打分 → 前 800 字 AI summary 兜底；全败回退 deck-swiss-international。
5. **反 AI 味硬约束写进每个模板**：CJK 优先字体栈（中文 Noto Sans/Serif SC、西文 Inter/Manrope）、8px 基线网格（所有间距/行高/字号为 8 的倍数）、圆角+软阴影+不用纯黑纯白、对比度 ≥4.5 且交互元素有 :focus 态、必须用用户真实数据禁止 lorem ipsum。
6. **流式渲染与沙箱**：POST /api/convert 走 SSE，agent stdout JSON-line 增量解析进 iframe srcdoc 实时可见，可随时中断重提示；用户 HTML 一律渲染在 `<iframe sandbox="allow-scripts allow-same-origin">` 内，cookie/localStorage 与宿主隔离。
7. **一键导出消灭二次排版**：微信=juice 内联 CSS 后整段可贴；X/微博/小红书=modern-screenshot 渲染 2× PNG 进剪贴板；知乎=mjx-container 转 data-eeimg 图片占位让公式上传后可见；另有 .html/.png 直接下载。
8. **本地安全边界**：/api/* 有 Host 头白名单中间件防 DNS rebinding（默认仅接受 loopback，可用 HTML_ANYTHING_ALLOWED_HOSTS 放开局域网），因为 convert 路由会以宽权限 flag 拉起本机 CLI。

## A1 (Past Application) — 源项目典型应用

### 案例: Markdown 长文转微信公众号成品
- **输入**: 一篇项目总结 Markdown，目标平台微信公众号
- **做法**: `html-anything auto article.md` 自动匹配 doc-kami-parchment 羊皮纸文档模板 → 本地 CLI 按 CJK 字体栈与 8px 网格生成单文件 HTML → juice 内联 CSS 导出
- **结果**: 粘贴进公众号编辑器样式完整保留，零二次排版

### 案例: CSV 变数据报告页
- **输入**: 一份业务数据 CSV
- **做法**: 格式自动探测（papaparse/xlsx 浏览器端解析不上传）→ 匹配 data-report 模板 → SSE 流式生成中随时打断调整
- **结果**: 沙箱 iframe 内实时预览的可视化数据报告，可导出 .html 或 2× PNG

### 案例: 产品发布的多形态产物
- **输入**: 同一套产品介绍素材
- **做法**: 分别套 deck-swiss-international（瑞士网格 keynote）、social-x-post-card（1600×900 引用卡）、prototype-web（SaaS landing 原型）三个模板各生成一次
- **结果**: 一份素材产出演讲、社媒、落地页三种 ship-ready 形态

## A2 (Future Trigger) ★ 触发场景

### 用户会在什么情境下需要
1. 写完 Markdown/笔记想直接获得「能发出去」的成品页面——公众号长文、知乎文章、博客排版
2. 需要快速产出设计感交付物：keynote 幻灯、海报、简历、小红书图文卡、产品原型、数据报告页
3. 手上有 CSV/JSON/SQL 数据想要一页可视化报告，且不想手写 CSS/栅格/响应式

### 语言信号
- "把这篇 markdown 转成能直接粘贴到公众号的排版"
- "帮我生成一个 SaaS 产品的落地页原型，要好看"
- "这份 CSV 做成一页数据报告，可以导出图片发 X"
- "用 html-anything 把我的简历排成 A4 单页"
- "这篇知乎回答帮我排个版，公式别丢"

### 与同 agent 兄弟 skill 的区分
- 与 `markdown-preview-enhanced` 的区别一句话：本 skill 让 AI **生成/编辑面向读者的成品 HTML 页面**（设计模板+一键分发导出），markdown-preview-enhanced 只是在编辑器里**实时预览增强你自己写的 Markdown**（数学/图表/代码块渲染），不负责设计与再创作。

## E (Execution) — 可执行步骤

1. **确认输入与目标版面** — 完成标准: 已识别输入格式（md/csv/json/text 自动探测）并确定 9 类 surface 中的一类；歧义时列出候选模板供选或走 auto 三层匹配
2. **选定模板与 agent** — 完成标准: 模板 ID 已锁定（auto 命中需说明匹配层级），且本机至少一个 coding-agent CLI 已登录可用（agents 列表 ✓）
3. **按硬约束生成** — 完成标准: 产出的 HTML 通过反 AI 味检查——CJK 字体栈、8px 基线、对比度 ≥4.5、有 :focus 态、内容全部来自用户真实数据无占位文
4. **流式预览与迭代** — 完成标准: 沙箱 iframe 内预览正常渲染第三方 CDN 资源；不满意处通过追加提示增量修正而非整体重生成
5. **按平台导出** — 完成标准: 目标平台对应管线执行成功——微信 juice 内联、社媒 2× PNG 剪贴板、知乎公式图片占位、或 .html/.png 下载，粘贴后无需手工修补
6. **安全收尾** — 完成标准: 未在公网暴露 /api/*（Host 白名单未被放开为 any，除非确有可信反代）；生成的文件不含用户未要求的密钥或本机路径泄露

## B (Boundary) — 边界

### 不适用场景
- 在 VSCode 里边写边预览自己的 .md 笔记（数学公式/mermaid/代码块渲染）→ 转 `markdown-preview-enhanced`
- 需要像素级品牌规范管控的专业设计交付（Figma 设计系统流程），模板化 HTML 只是近似而非替代
- 服务端多租户部署：convert 路由以宽权限拉起本机 CLI，架构假设单操作者单机，不适合当在线服务开放
- 需要长期维护的多页站点/组件化前端工程——产出是单文件 HTML 成品，不是可演进的代码库

### 已知局限 / 失败模式
- 依赖本机已登录的 coding-agent CLI，全部未安装/未登录时无法生成；CLI 升级导致 argv 协议变化时对应适配器需跟进修复
- 多模板对比预览、Hyperframes 一键转 mp4 尚属 in progress；部分模板经 CDN 加载字体/Tailwind，离线打开可能降级
- GUI 启动的 Node 进程可能漏扫 PATH 目录，检测不到 CLI 时需手动补环境变量
- 微信导出依赖 juice 对内联样式的支持，极复杂的 CSS（grid/flex 高级特性）在公众号编辑器内仍可能被平台二次过滤

## 相关 skills

- contrasts-with: markdown-preview-enhanced（AI 生成成品 HTML vs 编辑器内 Markdown 实时预览）
- composes-with: markdown-preview-enhanced（先用 MPE 校对稿子，再用本 skill 出成品排版）

---

## 审计信息

- **验证**: V1 ✓（README.md 与 cli/README.md 在九类 surface、75 模板、三层匹配漏斗、导出管线上互证）/ V2 ✓（可回答「为什么不需要 API key」「微信粘贴为何不掉样式」「如何防 DNS rebinding」等新问题）/ V3 ✓（读者优先格式观、模板即文件夹协议、反 AI 味五条硬约束是非常识性工作流）
- **蒸馏时间**: 2026-08-25
- **来源文件清单**: vendor/nexu-io__html-anything/{README.md, cli/README.md}
