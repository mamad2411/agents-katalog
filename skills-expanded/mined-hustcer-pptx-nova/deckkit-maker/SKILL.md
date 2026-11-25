---
name: deckkit-maker
description: >
  从参考 .pptx、HTML 模板，或 design.md + 参考图为 pptx-nova 创建或迁移 DeckKit
  （开发者侧 skill，操作 pptx-nova/ 源码）。用户提供设计规范、截图/风格板并要求
  创建套件、迁移皮肤或扩展设计语言时适用；也支持 PPTX/HTML 风格重建。两阶段工作流：
  第一阶段建立视觉基线（PPTX/HTML 按约定范围重建；设计规范与图片提取身份、构图并修正不合理设计），
  第二阶段组件化抽象为 id.kit.mjs +
  schema + catalog + benchmark 并走 readiness
  流程。不要把本 skill 用于普通交付型 deck 生成——那是 pptx-nova 的 DeckKit 模式。
---

# deckkit-maker

从参考 `.pptx`、HTML 模板，或 `design.md + 参考图` 出发，为 pptx-nova 创建新的 DeckKit。目标是让以后的 Agent
能用 `content.json → DeckKit → patch → xdoc` 稳定高效地产出同主题、同质量的 PPTX。

本 skill 是 **开发者侧** skill：它修改 `pptx-nova/` 源码，可以使用仓库根
`tools/`、`Justfile` 等 developer-only 工具链；但写进 pptx-nova 的任何用户路径
（kit、schema、scripts、references）必须保持 skill 自包含，不得依赖 skill 目录外文件。
本 skill 自带的 `scripts/` 只服务 DeckKit 创建流程，不会随 pptx-nova 发布。

## 输入

用户会提供：

1. **参考源** —— `.pptx`、HTML template 文件/目录，或 `design.md + 一张/多张参考图`。参考文件只读。
2. **新 DeckKit 的名字** —— kebab-case id（如 `swiss-grid`、`consulting-dark`）。

新建 DeckKit 时如果两者缺一，先向用户索取，不要自己猜测或挑选文件。已有 kit 修复、skill
维护或兼容性评估按用户指定范围开展，不需要虚构新 id 或索取无关参考文件。若参考源是 HTML 目录，优先确认其中
的入口文件（通常是 `template.html`）和元数据文件（如 `template.json` / `design.md`）。

输入为设计规范和图片时，先读 [references/design-source-migration.md](references/design-source-migration.md)。
迁移已有 DeckKit（包括 HTML/PPTX 来源）时，先读
[references/legacy-deckkit-migration.md](references/legacy-deckkit-migration.md)，再沿原参考类型完成两个阶段。
文档约束、图片布局和领域政策可能冲突，先记录来源与优先级；截图不自动成为业务数据来源。
用户允许设计优化时，以身份一致、可读性和内容表达为验收目标，主动修正不合理参考，不要求逐像素复刻。
该路线采用 `design.json + intent.md + 已注册执行组件`，复用现有合同门禁；不要给新风格复制一整套生成器。

## xdoc transport 边界

本 skill 默认使用一次性 CLI 或 CLI `--daemon`，因为完整 DeckKit 流程还需要
`convert`、`vision-check`、benchmark 等命令。每次任务先记录 `xdoc --version`，用
`node pptx-nova/scripts/cli/runtime/probe.mjs --json` 保存当前 runtime 的 capability snapshot。
新增或修改 op 前按 `pptx-nova/references/edit/patch-ops-cheatsheet.md` 查询 focused schema；不要从
旧示例推断字段、enum 或能力。宿主若已配置 xdoc MCP，只有
`capabilities.agentTransports.mcp.status == "disclosed"` 且合同版本被宿主识别时，才可按
完整 `capabilities.agentTransports.mcp.contract` 使用它。

- `xdoc_schema` 只能替换对应 schema discovery，`pptx_inspect` / `pptx_apply` 只能替换
  对应的 inspect/apply 调用；其余 xdoc 命令继续走 CLI。
- 所有文件路径传绝对路径；`overwrite` 默认 false，不能把 client 工作目录当成项目目录。
- MCP 只替换调用 adapter，不能跳过 dry-run → apply → post-apply inspect、vision-check、
  benchmark、人工 PNG 对比或 evidence gate。
- MCP 未安装、未公开或合同不兼容时回退 CLI，不阻塞 DeckKit 创建或修复流程。

### 当前合同与按需阅读

能力以本次可执行文件的 schema、报告和实际产物为准；支持写入、保留、渲染与播放是不同能力，
不能互相推导。维护者文档只提供线索，不把私有构建方式或库 API 写成公开集成路径。
长任务还须记录可执行文件 SHA256，并在正式重生成前比对；若全局二进制被替换，固定本轮
可执行文件并重验旧基线，不能只因版本号相同就混用证据。保留旧报告与本次兼容性结论。

| 涉及内容                                                   | 必须核对的依据                                                                                                                                                             |
| ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| OPC/Strict 包、非标准 part 名、继承主题、group/placeholder | `references/analyze-reference.md`；按关系解析，有效样式与局部 XML 分开记录                                                                                                 |
| freeform、自定义路径、gradient、group 几何                 | `pptx-nova/references/edit/patch-ops-cheatsheet.md` 与 focused schema；检查最终 slide 坐标和 PNG                                                                           |
| CJK/RTL、项目符号、rich text、autofit                      | `pptx-nova/references/create/deck-generator-workflow.md`；以新 runtime 的实际字体/换行复核旧补偿，不重复加大旧 workaround                                                  |
| 原生图表、极小数/百分比、数据标签                          | `pptx-nova/references/content/charts.md`；保留原始数值，显示精度单独设格式，转换为 JSON 回读                                                                               |
| 原生源稿编辑、3D、动画/transition/Morph                    | `pptx-nova/SKILL.md` 对应路由；按 schema 中各能力轴评估，不能把静态 PNG 或 generator kit 视为保留/播放证明                                                                 |
| 视觉漂移与质量放行                                         | `pptx-nova/references/review/fidelity-diagnosis.md`、`pptx-nova/references/create/create-runner.md`；同一 PPTX 字节、冻结 field date、canonical evidence 与人工逐页 review |

修复现有 PPTX 的对象时遵循主 skill 的 inspect → 精确 selector/guard → dry-run → apply →
inspect 回读；DeckKit 新建 patch 不能混入已有文件的 stale selector/source guard。

## 修复或扩展已有 DeckKit

当用户要求“修一下现有 DeckKit / 重新走一遍 broadside / 对照参考源修几页”时，按
**existing DeckKit repair** 处理，而不是新建 DeckKit：

- `catalog.json` 已注册该 id、`<id>.kit.mjs`、schema、examples 和 benchmark case 已存在是
  预期状态，不要按“目标文件已存在”判定为阻塞；只需确认这些文件确实属于本次要修的 DeckKit。
- 选择新的 `.tmp/deckkit-<id>-<run>/`；仅明确续做同一任务时复用其状态文件。
  每次迭代写新的 `iterations/01/`、`iterations/02/` 等目录；旧 benchmark、PNG 和报告只读保留。
  不以“已记录覆盖原因”代替授权，不清空旧目录，也不让 readiness 读取其他 run 的证据。
- 修复流程应以参考源和现有 benchmark 为事实来源：先复现/查看当前 PNG，再改 kit/test，最后跑
  validation、目标 benchmark、必要时全量 benchmark 和 showcase 更新。不要重新执行新建 DeckKit
  的 catalog/schema 初始化步骤。

## 新建 DeckKit preflight（必做）

先定位真实源码根目录：安装的 skill 可能是符号链接，当前工作目录也可能是 xdoc 维护者仓库。
解析本 SKILL.md 的真实路径，找到同时包含 `deckkit-maker/` 和 `pptx-nova/` 的仓库，
读取该仓库 AGENTS.md 并检查其工作区。下文相对路径都以这个源码仓库为基准；不要因为
当前目录没有 `pptx-nova/SKILL.md` 就初始化另一份套件。维护者仓库的文档和可选工具用其
独立绝对路径访问。运行会创建系统临时目录的维护者测试时，将支持的临时根显式指向当前 run。

`design.md + 参考图` 路线用设计文档/图片的存在性、source manifest 和目标 id 检查替代下例的
PPTX/HTML 输入检查；不要求不存在的二进制参考源。其他身份、目标路径、输出隔离检查仍适用。

新建 DeckKit 时，在读取参考 deck 或创建 run 目录前，先完成这些检查并把结果写进
`.tmp/deckkit-<id>/progress.md`；若 run 目录已存在，改用带时间戳的目录或先询问用户，
不要覆盖旧分析产物。

```bash
git status --short
node -e "const id=process.argv[1]; if(!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(id)) process.exit(1)" <id>
test -f <ref.pptx-or-template.html>   # HTML 目录输入时检查入口 template.html
test ! -e .tmp/deckkit-<id>
node -e "const c=require('./pptx-nova/assets/deckkits/catalog.json'); const id=process.argv[1]; if ((c.entries||[]).some(e=>e.id===id)) process.exit(1)" <id>
test ! -e pptx-nova/assets/deckkits/<id>
test ! -e pptx-nova/benchmarks/visual/cases/<id>
test ! -e pptx-nova/assets/examples/deckkits/<id>
```

如果任一目标文件或目录已存在，先确认是继续扩展、接管未完成工作，还是换新 id。不要删除或覆盖
不是本次任务创建的内容。参考 `.pptx` / HTML 模板必须只读；除 Phase 2 正式产物写入
`pptx-nova/` 外，任何导出、解包、截图、patch、PPTX、PNG、benchmark、审计和草稿文件
都必须写入当前 run 目录，不得散落到仓库根目录、`.tmp/` 其他子目录或临时的一次性目录。

## 前置阅读（必读，按序）

1. `pptx-nova/SKILL.md` —— pptx-nova 路由与红线
2. `references/componentize.md` 与 `pptx-nova/references/create/design-contracts.md` ——
   DeckKit/content 契约、字符串分层、组件化、benchmark 与 readiness
3. `pptx-nova/assets/deckkits/README.md` —— core-primitives 职责边界、冻结准入
4. `pptx-nova/references/create/deck-generator-workflow.md` —— 探索生成器方法与避坑

额外的维护者指南仅在可用时作为补充，不是本 skill 的必需输入。外部指南可能仍含旧的
扁平目录或 CLI 名称；目录、发布边界与当前命令以本仓库 AGENTS.md、skill 和真实
CLI `--help` 为准，记录冲突，不照搬旧路径，也不要为兼容旧示例添加 wrapper。

已有先例：`swiss-grid` DeckKit 即从 xdoc 维护者仓库的 `demos/67-swiss-grid-systems.pptx` 复刻而来，
`broadside` / `cartesian` / `biennale-yellow` 则来自 HTML 模板（见 catalog `knownLimits`），
本 skill 把这条路径固化为标准流程。

## 正式文件目录约定（必做）

每个套件的正式文件集中在 `pptx-nova/assets/deckkits/<id>/`：

```text
<id>/
├── <id>.kit.mjs       # 稳定入口；catalog.path = <id>/<id>.kit.mjs
├── design.json        # catalog.designContract = <id>/design.json
├── intent.md
├── layouts.mjs
├── components.mjs     # 需要套件专属执行器时提供
├── registry.mjs       # 需要注册视觉族时提供
├── schemas/           # <slideType>.schema.json
└── examples/
    ├── content.json   # 主示例
    ├── build.mjs      # 开发和 benchmark 胶水
    └── <variant>-content.json
```

套件内使用职责文件名，不创建根目录 `<prefix>-components.mjs` 等文件，不再使用全局
`deckkits/examples/` 或 `deckkits/schemas/<id>/`。catalog 的路径以 `assets/deckkits/`
为基准，benchmark index 的路径以 `benchmarks/visual/` 为基准。真正跨套件复用的 helper
放在 `shared/`；套件不得直接导入其他套件的实现。统一注册和合同/校验调度模块可以导入
套件的公开注册或解析接口。共享资源定位复用 `shared/deckkit-paths.mjs`，不得依赖运行 cwd。

公共 `content.schema.json`、`design.schema.json` 继续位于 `deckkits/schemas/`；
用户可见 showcase 仍位于 `assets/examples/deckkits/<id>/`，视觉回归资料仍位于
`benchmarks/visual/cases/<id>/`。每次新增或修改套件后运行：

```bash
node --test tools/tests/maintenance/deckkit-layout.test.mjs
node tools/pptx-nova-audit-public.mjs --strict
```

目录规则由公共审计强制检查；不要用旧路径 wrapper、复制文件或双份 schema 绕过检查。

## 两阶段总览

参考含新字体字重、CSS 固定圆角或未验证的原生对象组合时，先在当前 run 做一页最小探针，
再展开全量基线。用实际字号测试 Latin/CJK 常规与粗体、所需真实斜体，并比较 canonical 与
适用原生宿主；字体名可写、系统查询命中或预设形状名相同，都不证明实际字重／几何相同。
保留探针和裁决，复用本轮已证明的组合，不为每页重复探测。细节见
[HTML 视觉语义](references/html-template-reference.md) 和 [逐页验收](references/visual-acceptance.md)。

```text
参考 .pptx / HTML template / design.md + 参考图 + 新 DeckKit 名字
  │
  ├─ Phase 0  分析参考 deck/template   → references/analyze-reference.md
  │    pptx: unpack → 参考 PNG 基准
  │    html: browser screenshots → DOM/CSS/token extraction
  │    design + image: provenance → page/signature inventory → conflict decisions
  │    → style-spec.md + slide-inventory.md + fidelity-scope.md
  │
  ├─ Phase 1  高保真重建（第一交付物）  → references/rebuild-high-fidelity.md
  │    探索生成器 generate.mjs → 按 fidelity-scope 重建 → 逐页与参考 PNG 对比
  │    门禁：dry-run → apply → inspect → vision → canonical Create → 范围内逐页人工对比
  │
  └─ Phase 2  组件化抽象（第二交付物）  → references/componentize.md
       抽 <id>.kit.mjs + schemas + content.json + catalog 注册
       → slots/slot-consistency → benchmark(golden 入库；stress/mixed-language 在 .tmp 审查)
       → validation tests + content leak regression → readiness audit
```

**先完成并验收 Phase 1，再开始 Phase 2。** 高保真重建是组件化的证据基础：没有约定
范围内逐页对比通过的重建产物，就没有资格冻结 kit。这里的高保真指无 hard defect 的
视觉/结构基线，不要求像素级一致；最终 kit 只保留可复用视觉系统，不保留业务内容。
两阶段的产物都保留在 run 目录中。

## Skill 反馈闭环（必做）

每次使用本 skill 创建、修复或扩展 DeckKit 时，都要把 **deckkit-maker 自身的流程问题**
当作显式观察对象，而不是只关注目标 DeckKit。过程中持续记录：

- 文档不清、前后矛盾、路径/命令过期、示例不可直接运行。
- 脚本参数、退出码、输出格式、错误信息或默认行为影响效率。
- xdoc、browser、benchmark、readiness、content leak audit 等工具链的误报、漏报或需要人工绕行的地方。
- HTML/PPTX 迁移中反复踩到、但当前 skill 尚未覆盖的视觉、资产、schema、测试或目录管理问题。
- 可以通过补脚本、补模板、补检查项、改文档顺序来让下一个 Agent 更快完成的机会。

这些记录应追加到 run 目录的 `skill-feedback.md`，或在 `findings.md` 中单独开
`## deckkit-maker feedback` 小节；不要等任务结束后凭记忆回想。完成 DeckKit 后，最终回复
必须包含“deckkit-maker 改进意见和反馈”：列出本次发现的问题、影响、建议改法和是否已在本次
顺手修复。若本次没有发现新问题，也要明确说明“未发现新的 deckkit-maker 改进项”。

### HTML 模板输入补充流程

HTML 模板不是 PPTX，不能走 `xdoc inspect` / `xdoc convert <ref.pptx>` 作为事实源。遇到
`template.html`、网页 URL、本地 HTML 模板目录或 `beautiful-html-templates` 类素材时：

1. 读取 `template.json`、`design.md`、入口 HTML 的 CSS token、slide section 和脚本。记录
   HTML 元数据与实际 DOM 的不一致（如 `slide_count` 与 `.slide` 数量不同）。
2. 使用 agent-browser 或等效浏览器工具，以 16:9 viewport（建议 1440×810）逐页截图到
   `ref-previews/`，并生成 contact sheet。截图前冻结动画，隐藏网页导航控件、圆点、浏览器
   slide counter、hover-only UI 等 PPTX 不应复刻的交互元素。截图流程必须可复现：
   记录 `agent-browser set viewport 1440 810`、注入的 capture CSS、slide 切换方式，以及
   绝对 screenshot path；不要只留下手工点击后的散图。优先使用
   `node deckkit-maker/scripts/capture-html-slides.mjs --url <template.html-or-url> --out .tmp/deckkit-<id>/ref-previews`
   生成逐页 PNG 与 `capture-manifest.json`（ImageMagick 可用时另有 contact sheet）；输出目录必须新建或为空。
   脚本默认独立 session，逐页等待字体、图片解码与布局，保存截图 hash/几何；具体限制见 HTML reference。
   非 `.slide` 模板通过
   `--selector` 调整，只有
   模板用 `.is-active` 等激活类时传 `--active-class is-active`；脚本将有限入场动画推进终态，
   并拒绝仍透明的 `data-anim` 文字。不要用 `animation:none` 冻结初始透明态后把空页当成功。
   slide 原本是 `display:none` 且无法靠激活类恢复时才传 `--active-display`，避免破坏
   源 HTML 的 grid/flex 布局。macOS 上 ImageMagick 可能找不到默认字体；脚本会优先使用
   `DECKKIT_CONTACT_SHEET_FONT` / `--contact-sheet-font`，否则回退到系统 Arial/Helvetica
   路径，避免 contact sheet 因空字体失败。
3. `style-spec.md` 必须同时引用 CSS token 与浏览器截图；字号从 CSS `vw/vh/rem/px`
   映射为 PPTX pt，间距从 viewport 比例映射到 13.333×7.5in。
4. `slide-inventory.md` 以真实 DOM slide 顺序为准，不以元数据声明为准；把 CSS class
   映射为 DeckKit page type。文案抽取建议用 `xdoc html2md <template.html>` 做交叉校验；
   对隐藏 slide、off-screen slide 或当前未激活的 slide，用 DOM `textContent` 抽取，不要只用
   `innerText`，否则会漏掉 `display:none` 页面。
5. HTML 的 motion、keyboard handlers、pagination dots、scroll transforms、hover states
   只记录为"不迁移"决策；DeckKit 只冻结静态演示视觉系统、可编辑 shape/text、asset slot
   和可复用 chart/diagram 结构。
6. 图片/截图区域默认转为 asset slot 或占位框；不把 HTML 模板中的一次性位图、远程图、CSS
   背景图直接写入 kit。
7. CSS texture、SVG pattern、全页背景 SVG/bitmap 默认不要直接迁移为整页 `add-image`。
   优先用 flat fill、线条、重复 shape 或低密度 hatch 表达纹理语气。若必须用图片背景，先在 run
   目录以当前 runtime 做最小实验，核对同一 PPTX 的 layer order、PNG 和 PowerPoint 打开效果；
   不沿用旧版 renderer 的占位覆盖层假设，实际限制再写入 knownLimits。
8. Phase 1 对比时用浏览器截图作为参考 PNG；Phase 2 benchmark 仍必须用 xdoc 生成 PPTX
   PNG，并走下文完整视觉门禁；benchmark 不能替代 canonical Create 和逐页 review。

### HTML 到 PPTX 视觉语义避坑

HTML/CSS 的视觉语义不能逐字搬到 PPTX patch，尤其是透明色和自定义图形：

- **CSS alpha 颜色要折算并过门禁**：PowerPoint 文本 font color 通常是实体色，不能直接表达
  `rgba(...)` 的网页透明感。把 CSS token 折算到目标背景色上后，还要跑 `vision-check`；
  若可读正文、label、页眉页脚触发低对比 high/medium，就区分“可读 muted token”和“装饰 muted token”。
  大号背景编号、装饰 slash、非关键信息可以更淡；正文和小号 chrome 必须满足交付门禁。
- **不要为了贴近参考而接受不可读色**：参考 HTML 里的 `rgba(17,17,17,.45/.55/.60)` 在橙底上
  可能只有 2-3:1 对比度。DeckKit 要服务后续交付，优先级是参考视觉语气 + PPT 可读性 +
  `vision high/medium = 0`，而不是像素级复制网页透明度。
- **小号透明/白色文本允许可读性适配**：HTML 中的小号透明黑、透明白或低 alpha chrome
  在 PPTX 门禁中可能触发低对比。正文、小号 label、页眉页脚、来源和按钮文字可以加深为
  同色系高对比实体色；在 `compare-notes.md` 标记为可读性适配即可。
- **freeform 使用当前 canonical path 合同**：`add-freeform` 的 `x/y/w/h` 是显式形状框，
  `path.width/height` 是正整数局部 viewport，`path.commands` 使用 `move/line/cubic/close`。
  旧 `points/originX/originY/xScale/yScale` 写法已不适用。先读 cheatsheet 的 freeform 示例与
  当前 focused schema，再用 inspect 回读 `freeform.path`、真实尺寸和 PNG 验证；控制点可以超出
  viewport，不能假设形状框会自动裁剪或扩张。遇到 `preserve-only` 不重建成空路径。

### 门禁与 benchmark 判读

- **vision 字段不同于 dry-run**：`vision.json` 的定位字段是 `issues[].slideIndex` 和
  `issues[].shapeName`，不是 dry-run 的 `target.name`。汇总 high/medium 时用：

  ```bash
  VISION_JSON=.tmp/deckkit-ID/vision.json
  node -e 'const fs=require("fs"); const r=JSON.parse(fs.readFileSync(process.argv[1],"utf8")); const xs=(r.issues||[]).filter(i=>["high","medium"].includes(i.severity)); console.log(xs.map(i=>`${i.severity}\tslide ${(i.slideIndex??-1)+1}\t${i.shapeName||i.shapeId}\t${i.kind||""}\t${i.message||""}`).join("\n")||"vision high/medium: 0"); process.exit(xs.length?1:0)' "$VISION_JSON"
  ```

- **candidate readiness warning 是预期状态**：新 kit 推到 `candidate` 时，
  `validate-content --mode delivery` 可能仍提示 readiness 相关 warning。只要没有 schema、
  slot 或 content-contract error，并且 benchmark/readiness audit 通过，不要把这类 warning
  当作交付阻塞。
- **golden benchmark 之外的韧性覆盖**：新 kit 必须审查 golden、stress-density 和
  mixed-language 三类输入，但默认只有 golden 视觉 benchmark 落进 git。stress-density 和
  mixed-language 的临时 content、patch、PNG、contact sheet、结论写入
  `.tmp/deckkit-<id>/benchmark/`，不登记 `benchmarks/visual/index.json`，除非它们确实提供
  长期回归价值。长标题、密度、多语言和边界长度优先放进 schema slot budget、validation tests、
  content leak regression 或有针对性的非视觉单测。真实合理内容仍失败时再改 kit 几何或容量策略。

### 高保真范围决策

默认做全量重建：参考 deck 每一页都有对应重建页。若参考 deck 页数很多、重复页占比高，
或包含大量一次性/低复用页面，Phase 0 必须在 `fidelity-scope.md` 中先做范围决策：

- `full`：默认模式，全量重建全部 slides。
- `scoped`：只在用户确认后使用；必须覆盖每种页型、每个 signature visual element、
  每类图表/表格/资产形态和所有可复用 chrome；未重建页逐页记录归属页型、省略原因与
  Phase 2 影响。

`scoped` 只能降低一次性页面的重建成本，不能跳过风格证据、页型证据、资产决策或
benchmark 覆盖；最终 catalog 必须把未覆盖内容写入 `knownLimits` 或 coverage 说明。

### 图片资产原则

当前新增图片式视觉统一走 [原生 PowerPoint 组合](../pptx-nova/references/create/native-visuals.md)。
空外壳只可用于开发时登记资产职责，不能作为交付完成态。复用主体相关的 shape/path、连接线、
分组、文字、已注册图标及有真实数据依据的原生对象，维护对应套件合同和测试；保留用户提供的真实素材。

DeckKit 复刻视觉语法，不复刻一次性素材。图片主导页（照片、截图、插画、产品界面图、
背景位图占主要表达价值）默认不进入 Phase 1 高保真 rebuild set；只登记其页型、图片角色、
裁切/边框/callout/caption 等可复用外壳。若该页贡献了新的可复用页型，重建外壳和
`asset` 槽位，用占位框、语义相关的原生 shape、Tabler icon、图表/表格或 SmartArt-like
组合替代，不搬参考图片。

替代元素必须和原页表达含义相关；禁止为填充画面而塞入无关图标、装饰或抽象形状。参考 deck
提取出的图片不得写入 `.kit.mjs`，默认也不得进入 DeckKit examples/assets；只有授权明确、
跨 deck 可复用且用户确认的品牌资产才可例外纳入。

## 不可跳过的红线

- **core-primitives 只读为默认**。`shared/core-primitives.kit.mjs` 不承担任何 DeckKit 专属
  风格。只有当一段逻辑"换了主题色/间距后仍然正确"且至少有跨 kit 复用证据时，才考虑
  下沉；下沉前必须与用户确认，并跑全部现有 DeckKit 的 validation tests。
- **参考 pptx / HTML 只读**。所有解包、DOM/CSS 抽取和分析副本都放进
  `.tmp/deckkit-<id>/ref-unpack/` 或同一 run 目录下的对应子目录。
- **content leak 防线**（细节见 `references/componentize.md` 的字符串分层与审计）：
  `.kit.mjs` 只冻结视觉语言、几何、chrome、结构标签；参考 deck 的业务文案
  （标题、观点、指标、实体、年份、来源、callout 强调词）最终只能进入
  `content.json` / examples / benchmark fixture。Phase 1 的探索生成器里可以暂时
  内联内容，Phase 2 抽取时必须全部移出。反例教训：swiss-grid 早期把
  `'Aa'`、`'所有距离的最小公因子'` 等示例内容硬编码进页型，导致三个版型跨主题不可复用。
- **坐标必须推导**：所有 op 坐标走 primitives（`nm()`/`grid()`/`txH()`）或显式
  bounds 计算，不凭目测摆放。幕布 13.333in × 7.5in。
- **图标只用 pptx-nova 现有 Tabler pack**：用
  `node pptx-nova/scripts/cli/assets/icons.mjs search <query> --json` 查询、
  `createOps().icon()` 内联。参考 deck 中的图标/装饰图找最接近的 Tabler 替代；
  不联网取图，不把参考 deck 的位图直接打进 kit。替代图标/shape 必须语义相关。
- **视觉门禁**：每次 build 走
  `dry-run → apply → inspect → vision-check(high/medium=0) → canonical Create → 人工逐页 PNG review`。
  dry-run 与 vision-check 的溢出估算阈值不同，两个都要跑。benchmark 的历史 low 基线不等于
  canonical Create 放行；仍须通过当前交付门禁，不能用 qualityProfile 覆盖它。
  现有 benchmark 的 vision/PNG 成功也不能代替 canonical PDF 最终布局检查。
  手动探索循环在完整渲染前运行 `deckkit-maker/scripts/check-build-evidence.mjs --dir <iteration>`，
  先拒绝缺失语义证据和已知 high/medium 风险，再调用 canonical；不要把命令顺序当作门禁判定。
  至少对完整 golden 示例执行一次当前 runtime 的 canonical 检查。替换下例路径和冻结日期：

  ```sh
  xdoc pptx visual-audit --candidate ./deck.pptx \
    --visual-mode create --field-date 2026-10-22 \
    --output-dir ./iteration/canonical --json
  ```

  读取 manifest 的 required checks、findings 和 decision；若运行时未披露该路线，
  按 `create-runner.md` 的兼容路径处理并记录边界。
  参考、candidate、benchmark 使用同一冻结日期；按 manifest/artifact path 定位产物，不猜文件名。
  exit code 0、PNG 存在或旧 baseline 通过均不足以单独证明放行。

- **逐页与局部验收**：首次走查前读 [references/visual-acceptance.md](references/visual-acceptance.md)。
  对准备接受的 golden、构图变体、压力、多语言样例逐张检查实际 canonical PNG，并记录每页结果。
  圆形编号、带底色标签、密集数值与表格底部说明须放大复核；重点防止圆内数字偏心、文字超出底条、
  附注贴线。机器零 findings 不能替代视觉验收；用户指出漏检后撤回受影响结论，复查全部同类组件。
- **常规 shape 也必须高保真**：不要只复刻版式语义而放松基础元素。人工 PNG 对比时逐页检查
  文本字号、字色、大小写、对齐、行高、圆形/方块尺寸、圆内文字颜色与居中、斜线/纹理方向、
  裁切边界和是否越界。除非为了通过可读性门禁并在 compare notes 中说明，PPTX 字号不应小于
  参考源；圆形、badge、编号、标题这类高识别元素必须优先按参考截图尺寸还原。
- **字号下限**：正文 ≥10.5pt；label/badge/chart/table 和页脚/来源须满足当前 canonical
  可读性门禁（默认 10pt）。若参考源使用更小字号，优先增高或加宽文字框并调整内容预算，
  在 compare notes 记录可读性适配；同步 schema slot budget 和 catalog，不能仅声明小字号例外。
- **readiness 不跳级**：新 kit 从 `experimental` 起步，benchmark 通过后
  `candidate`；`production` 必须 benchmark + 人工 PNG review +
  `--confirm-manual-png-review`。本 skill 默认推进到 `candidate`，
  promotion 到 `production` 需用户确认。

## 长任务管理

本任务通常跨 50+ 工具调用，必须有可恢复的状态文件。若 planning-with-files SKILL
可用，开工即使用它；否则在 run 目录手动创建并持续维护：

- `task_plan.md`：Phase 0/1/2 分阶段 checklist，阶段完成时更新状态。
- `findings.md`：风格提取、XML 证据、字体/资产风险、用户确认事项。
- `progress.md`：已执行命令、产物路径、失败与修复、下一步。
- `skill-feedback.md`：deckkit-maker 自身的问题、摩擦点、误报/绕行、改进建议和已修复项。

每看完 1–2 页参考 PNG、每轮重建对比、每次 benchmark/readiness 后都要落盘。需要深入读取
参考 pptx 内部 XML 之外的内容（如嵌入对象）时，可借助 pptx SKILL。

## Run 目录约定

以下 `.tmp/deckkit-<id>/` 均代表本次唯一 run；目录已存在时使用
`.tmp/deckkit-<id>-<run>/`，并统一替换所有命令路径。不要混用新旧 run 的报告。

```text
.tmp/deckkit-<id>/
├── ref-previews/          # 参考 deck PNG 基准（contact-sheet + 逐页）
├── ref-unpack/            # 参考 PPTX 解包、HTML DOM/CSS 抽取等只读分析副本
├── ref-inspect.json       # xdoc inspect / DOM inspect 结构化输出
├── style-spec.md          # Phase 0 风格提取结论
├── slide-inventory.md     # Phase 0 逐页清单与页型归并
├── fidelity-scope.md      # Phase 0 高保真范围决策（full/scoped）
├── task_plan.md / findings.md / progress.md / skill-feedback.md
├── generate.mjs           # Phase 1 探索生成器
├── render-context.json    # 本次 runtime/build、源文件 hash、冻结 fieldDate
├── iterations/01/         # patch、PPTX、dry-run、inspect、vision、canonical manifest/PNG/PDF
├── benchmark/01/          # benchmark/readiness/catalog-update 共同 --out，旧轮次保留
├── compare-notes.md       # Phase 1 逐页对比记录
└── audit/                 # Phase 2 content leak / text extraction / slot audit 产物
```

`.tmp/deckkit-*` 均不提交。Phase 2 的正式产物写入
`pptx-nova/`（kit、schema、catalog、examples、benchmark、tests）。

不要再创建 legacy 根目录 run 目录、散落的截图/解包目录、根目录 JSON，或按脚本名临时拼出来的
目录。若外部工具默认输出到别处，显式传 `--out` / `-o` / 输出路径，把结果收束到
`.tmp/deckkit-<id>/` 下；需要保留的错误日志、CLI stdout JSON、截图和对比图也放在这里。旧任务
留下的 legacy 目录可以只读参考，但新任务和新产物一律使用 `.tmp/deckkit-<id>/`。

## 完成摘要

任务结束时最终回复必须列出：

- 新 DeckKit id、版本、readiness 结论与 catalog 路径
- Phase 1 重建 deck 路径与逐页对比结论（保留页数 / 参考页数）
- Phase 2 落盘文件清单（kit / schemas / content / catalog / benchmark / tests）
- 验证结果：validate-content、dry-run、vision-check、slot-consistency、
  content leak audit、benchmark summary、readiness audit
- 与参考 deck 的已知差异（字体替代、图标替代、未还原元素）逐条披露
- 是否动了 core-primitives；若动了，列出改动与全量 DeckKit 回归结果
- deckkit-maker 改进意见和反馈：本次发现的问题、影响、建议改法、已修复项；若无新问题则明确说明

## Reference 索引

| 文件                                     | 用途                                                |
| ---------------------------------------- | --------------------------------------------------- |
| `references/analyze-reference.md`        | Phase 0：解包、PNG 基准、风格提取、页型归并         |
| `references/html-template-reference.md`  | Phase 0 补充：HTML 模板截图、DOM/CSS 分析、交互过滤 |
| `references/rebuild-high-fidelity.md`    | Phase 1：探索生成器、逐页重建与对比循环、避坑清单   |
| `references/componentize.md`             | Phase 2：抽 kit/schema/catalog/benchmark/readiness  |
| `references/design-source-migration.md`  | design.md + 参考图：来源、设计裁决、合同与复用验证  |
| `references/legacy-deckkit-migration.md` | 已有套件：调用清单、合同切换、验收与旧资产退役      |
| `references/visual-acceptance.md`        | 逐页验收、局部放大、居中/标签/附注反例              |
