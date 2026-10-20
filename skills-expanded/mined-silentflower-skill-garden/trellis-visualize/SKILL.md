---
name: trellis-visualize
description: "把架构、流程、业务逻辑、状态流转和旧 UML / 活动图诉求可视化为离线 HTML/SVG 图解。触发：画架构图、系统图、流程图、业务流程图、梳理流程、解释逻辑、状态流转、画活动图、draw UML、diagram、visualize。用于编码或决策前生成可复核视觉模型；生成图时必须优先使用随 skill 分发的 templates/template.html 作为结构和视觉参考；不用于 PRD 提取、任务规格校验或全链路测试。"
---
# Trellis 可视化图解

把架构、流程、业务规则和复杂逻辑转成可复核的离线 HTML/SVG 图解。这个 skill 继承 `architecture-diagram` 的设计范式，不是松散重写：生成图前必须先建立图模型，并在需要生成 HTML/SVG 时读取本 skill 自带的 `templates/template.html`。

## 资源

- `templates/template.html`：从原 `architecture-diagram` 保留下来的 HTML/SVG 结构模板，包含暗色网格、SVG defs、箭头 marker、组件样式、边界、图例和说明卡片示例。

使用规则：

- 生成任何 HTML/SVG 图解前，先读取 `templates/template.html`。文件路径相对本 `SKILL.md` 所在目录。
- 技术架构、云架构、基础设施图必须以该模板作为结构基准，替换标题、节点、连线和说明卡片，不要从零另写一套视觉系统。
- 流程图、逻辑图、状态图也要复用该模板的页面结构、暗色网格、SVG defs、卡片区和排版约束；只扩展节点语义，不换掉整体设计范式。
- 如果当前平台不能直接读取 bundled resource，明确说明模板不可用，并用本文件中的硬约束近似复刻；不要假装已经使用模板。

## 适用范围

优先使用本 skill：

- 架构图：系统、服务、组件、部署、依赖关系、数据流、云资源、网络边界。
- 流程图：角色、触发、主路径、分支、异常、终态、泳道。
- 逻辑图：规则链路、判断条件、因果关系、策略选择。
- 状态图：状态流转、事件触发、失败、取消、超时、回滚。
- 旧意图兼容：用户说“画活动图”、“业务流程图”、“梳理流程”、“draw UML”时，也使用本 skill。

不要用于：

- 正式需求提取：使用 `trellis-extract-prd`。
- 三件套校验：使用 `trellis-verify-task`。
- 开发后质量检查：使用 `trellis-check-all`。
- 跨层自动化验证：使用 `trellis-run-full-chain`。

## 不可弱化的原始约束

以下约束来自原 `architecture-diagram`，必须按硬约束执行，不要翻译成可选建议：

- 产物是 standalone HTML file with inline SVG graphics。
- 不需要外部工具、API key 或渲染库；浏览器离线打开即可查看。
- CSS 和 SVG 必须内联；不得依赖外部渲染服务。
- 不使用 JavaScript；允许纯 CSS 动效。
- 模板里的 Google Fonts 可保留，也可以替换成系统字体栈；如果保留，要知道离线时会降级。
- 连线要在 SVG 中早于节点绘制，让箭头位于节点盒子后方。
- 半透明节点要使用 double-rect masking technique：先画不透明背景矩形，再画半透明样式矩形，避免箭头透出来。
- 图例位置必须计算，不得遮挡边界、节点或连线；有边界框时，图例放到最低边界下方至少 20px，或放在明确不遮挡的位置。
- Message bus / 异步事件 / 队列必须放在服务之间的间隙，不得压在节点上。

## 工作流

### 1. 判断图类型

从用户描述中判断主图类型：

| 用户意图 | 图类型 |
| --- | --- |
| 系统、服务、组件、部署、调用链、云资源 | 架构图 |
| 业务办理、审批、操作步骤、泳道 | 流程图 |
| 规则、判断、因果、策略 | 逻辑图 |
| 状态、事件、流转、回滚 | 状态图 |

如果请求同时包含多种图，先选择最能回答当前问题的一张主图；其他图作为待确认或后续迭代。

### 2. 整理图模型

输出图之前，先整理图模型：

- 图名：本图要解释的问题。
- 主体：角色、系统、组件、服务、外部依赖。
- 关系：调用、依赖、流转、触发、判断、异常、回滚。
- 边界：系统边界、组织边界、阶段边界、权限边界、云区域、安全组。
- 终态：成功、失败、取消、超时、回滚等结束状态。
- 事实 / 假设 / 待确认：明确区分用户已给出的事实和仍需确认的信息。

不要虚构角色、系统、字段、规则、状态、分支或异常路径。能从仓库、文档、任务文件中查到的事实不要问用户。

### 3. 澄清规则

当缺失信息会影响图结构时，先问再画。一次最多问 3 个关键问题，并给出推荐答案或取舍。

优先澄清：

- 主体是谁：用户、运营、审批人、系统、第三方。
- 入口是什么：触发事件、页面入口、API 调用、定时任务。
- 分支条件是什么：判断字段、阈值、权限、状态。
- 异常怎么处理：失败、拒绝、超时、重复提交、回滚。
- 终态是什么：成功状态、失败状态、是否通知、是否留痕。

如果信息不足但可以画“待确认版”，必须在图模型和说明卡片里标出待确认项。

## 输出契约

默认输出：

- 主图：`doc/visualize/<slug>.html`
- 截图：`doc/visualize/<slug>.png`，仅在用户需要对话内预览或明确要求截图时生成。

规则：

- **输出语言必须跟随用户语言**：中文对话生成中文标题、中文节点、中文图例、中文卡片和中文说明；英文对话才生成英文可见文案。
- 技术 token 可以保留原文，例如命令、文件名、包名、函数名、tag、环境变量、API 名：`npm run sync`、`release.yml`、`vX.Y.Z-beta.N`、`MANIFEST.sourceCommit`。
- 模板里的示例文案不是输出文案来源；不得残留 `Legend`、`Users`、`Backend`、`Channel check`、`Card Title` 等与当前语境无关的英文示例标签。
- 图模型中明确记录：`输出语言：<中文 / English / 用户指定语言>；技术 token 保留原文`。
- `slug` 使用英文小写和连字符，例如 `order-approval-flow`。
- 无法安全命名时，向用户确认 `slug`。
- 同名文件可以覆盖；HTML 是当前真源。
- 旧 `doc/uml/` 不再作为默认目录。

最终答复包含：

```markdown
## 可视化图解：<图名>

### 图类型
- <架构图 / 流程图 / 逻辑图 / 状态图>

### 产物
- HTML：`doc/visualize/<slug>.html`
- PNG：`doc/visualize/<slug>.png`（如已生成）

### 图模型
- **输出语言**：<中文 / English / 用户指定语言；技术 token 保留原文>
- **主体**：<角色 / 系统 / 组件>
- **关系**：<调用 / 流转 / 判定 / 异常>
- **边界**：<系统边界 / 阶段 / 权限>

### 关键说明
- <关键节点或路径>
- <关键判定>
- <异常 / 回滚>

### 待确认
- [ ] <仍未确认但不阻塞当前图的问题>
```

## HTML/SVG 生成规则

生成 HTML 时，以 `templates/template.html` 的四段式结构为基准：

1. Header：标题、状态点、简短副标题。
2. Main SVG：带暗色网格背景的主图区域。
3. Summary Cards：图下方说明卡片，至少覆盖关键节点、关键判定、异常 / 风险、待确认项中的三类。
4. Footer：产物元信息。

SVG 必须包含：

- `defs` 中的 arrow marker。
- `pattern id="grid"` 的 40px 网格背景。
- 先画背景和连线，再画边界和节点。
- 节点文本短句化；细节放在副标题或说明卡片。
- 复杂节点使用不透明底层矩形 + 半透明样式层。

### 模板替换规则

复制或参考 `templates/template.html` 后，必须逐项替换所有可见文案：

- HTML `<title>`、`h1`、subtitle、footer。
- SVG 中所有 `<text>`：节点标题、节点副标题、连线标签、边界标题、图例。
- Summary Cards：卡片标题、列表项、状态点语义。
- 示例节点、示例云资源、示例技术栈和示例图例都必须替换成当前图模型中的真实主体和关系。

允许保留的英文只限技术 token。普通说明性 UI 文案必须翻译或改写成用户语言，例如：

- `Legend` → `图例`
- `Maintainer` → `维护者`
- `Channel check` → `通道判定`
- `Release notes` → `Release 说明` 或 `发布说明`
- `same args` → `参数一致`
- `trigger CI` → `触发 CI`

不要为了保留模板风格而保留英文示例文案。

## 语义映射

模板原生颜色用于技术架构：

| 类型 | 填充 | 描边 | 用途 |
| --- | --- | --- | --- |
| Frontend | `rgba(8, 51, 68, 0.4)` | `#22d3ee` | 前端、入口、人工动作 |
| Backend | `rgba(6, 78, 59, 0.4)` | `#34d399` | 后端服务、系统动作、任务执行 |
| Database | `rgba(76, 29, 149, 0.4)` | `#a78bfa` | 数据库、缓存、文件、状态记录 |
| AWS/Cloud | `rgba(120, 53, 15, 0.3)` | `#fbbf24` | 云资源、平台边界、业务阶段 |
| Security | `rgba(136, 19, 55, 0.4)` | `#fb7185` | 安全、异常、拒绝、超时、回滚 |
| Message Bus | `rgba(251, 146, 60, 0.3)` | `#fb923c` | 队列、事件、异步、判定规则 |
| External | `rgba(30, 41, 59, 0.5)` | `#94a3b8` | 外部参与者、第三方系统 |

扩展到流程 / 逻辑 / 状态图时按同一色板映射，不新增一套不兼容色板：

- 外部参与者 / 第三方系统：External。
- 人工动作 / 用户操作 / 审批：Frontend。
- 系统动作 / 服务处理 / 定时任务：Backend。
- 数据 / 状态记录 / 审计日志：Database。
- 阶段 / 组织 / 平台边界：AWS/Cloud boundary。
- 判定 / 策略 / 异步事件：Message Bus。
- 异常 / 拒绝 / 超时 / 回滚：Security。
- 成功终态：Backend 或 Database 色系，并在文本中标明终态。

## 连线规则

- 普通调用、主流程：实线箭头。
- 鉴权、安全、拒绝、失败、回滚：玫红色虚线。
- 异步、事件、队列：橙色或琥珀色，并标注“异步”、“事件触发”或队列名。
- 条件分支必须在线上或节点旁标注条件，不允许只靠箭头颜色表达。
- 回到前置状态的路径必须明确标注原因，例如“补充材料”、“重试”、“人工复核”。

## PNG 渲染

生成 HTML 后，只有在用户需要预览时才生成 PNG。优先用本地浏览器 / Playwright 截图：

```bash
node - <<'JS'
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const input = path.resolve('doc/visualize/<slug>.html');
  const output = path.resolve('doc/visualize/<slug>.png');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 2 });
  await page.goto('file://' + input);
  await page.screenshot({ path: output, fullPage: true });
  await browser.close();
  console.log(`saved: ${output}`);
})();
JS
```

如果 Playwright 或浏览器不可用，保留 HTML 主产物并说明 PNG 未生成的原因；不要假装截图成功。

## 生成后自检

交付前必须检查 HTML：

- 确认 `templates/template.html` 的结构已被业务内容替换，不存在 `Card Title`、`Users`、`Frontend`、`Backend`、`Database` 等无关示例残留；如果这些词本身就是业务真实名称，必须在说明中可解释。
- 对中文用户，用 `rg -n "[A-Za-z]{3,}" doc/visualize/<slug>.html` 扫描可见英文。保留命令、文件名、包名、tag、API 名、CSS/HTML 属性等技术 token；把普通 UI 标签、状态说明、图例、节点标题和连线说明改成中文。
- 确认图中每个节点和说明卡片都来自图模型，不从模板示例继承。
- 自检不通过时，先修 HTML，再向用户报告产物。

## 迭代规则

- 用户反馈后，只改被指出的部分，保持其他节点和关系稳定。
- 大幅改图类型、版式或主流程前，先确认修改范围。
- 修改后必须同步更新 HTML；如果已经生成 PNG，也要重新截图。

## 禁止事项

- 不要不读 `templates/template.html` 就直接生成最终 HTML/SVG。
- 不要把原 `architecture-diagram` 的硬约束弱化为“可选建议”。
- 不要让模板英文示例文案泄漏到最终图中；除技术 token 外，可见文案必须跟随用户语言。
- 不要跳过澄清直接画复杂分支图。
- 不要虚构角色、系统、字段、状态、规则、异常路径。
- 不要只输出文字说明而不生成图。
- 不要只给 Mermaid 代码作为最终产物。
- 不要把旧 UML 诉求继续写入 `doc/uml/`。
- 不要在 PNG 生成失败时假装成功。
