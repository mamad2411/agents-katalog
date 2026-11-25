---
name: hash-design
description: Use when building or redesigning any web page, landing page, one-page site, slide deck, mobile app screen, dashboard, poster / social card or HTML email where the result must have real design character and must NOT look AI-generated (no Inter, purple gradients, centered hero with two buttons, three identical cards). Rolls true-random hashes through the hash-design MCP server (each hash is one design direction: its bytes set the palette, faces, grid, motif, motion, voice and twist directly, with no style library), freezes N design briefs (default 5, up to 12; scenario web, deck, app, dashboard, poster or email), replies with one line per direction and waits; on request renders independent HTML previews plus a side-by-side compare page; then builds the picked one and self-critiques it. Triggers - "做个页面/官网/落地页/一页站", "做个 PPT/幻灯片", "App 界面", "数据看板", "海报", "去 AI 味", "要有设计感", "landing page", "slide deck", "make it not look like AI", "give me design options".
---

# hash-design：用外部随机打破默认审美

LLM 做页面会塌缩到众数审美。这个 Skill 的做法是：**风格不由你选**。先用真随机哈希掷骰：**哈希本身就是设计方向**，它的每个字节按固定规则直接决定一个参数（配色的色相与明度、标题和正文字体、栅格、首屏锚点、母题、材质、动效、文案语气、变数），没有任何风格库可选。N 个哈希（默认 5 个）就是 N 份 brief，你只负责**忠实执行** brief，把选择权交还给用户。

## 何时使用

- 用户要做/重做一个网页、落地页、一页站、活动页、作品集首页、UI 视觉稿；或幻灯片/PPT、手机 App 界面、数据看板、海报/社交卡片、HTML 邮件。
- 用户说"要有设计感""别像 AI 做的""给我几个方向"。
- 不适用：纯后端、已有严格设计系统且用户要求遵守的改动（此时只用 `critique_page` 自检即可）。

## 前置条件

- 已连接 MCP server `hash-design`（工具：`roll_designs`、`get_brief`、`critique_page`、`build_compare_page`）。
- 没有 MCP 时用 CLI，参数相同（见文末对照表）：`npx -y hash-design roll …`、`npx -y hash-design critique …`、`npx -y hash-design compare …`；在源码目录里是 `node packages/core/dist/bin.js …`。`skill install` 安装后会打印当前可用的 CLI 和 MCP 命令。

## 工作流（严格按顺序）

### 0. 收集事实

向用户要（或从仓库/上下文里找）**事实清单**：名称、地址、时间、价格、产品、联系方式、真实卖点。页面上只能出现这些事实。缺的就在页面里留"【待补：…】"，**绝不编造**数字、评价、客户、奖项。

### 1. 掷骰（不要自己挑风格）

调用 `roll_designs`：

```json
{ "subject": "第四巷面包店 一页站", "facts": ["…", "…"], "count": 5, "out_dir": "design/hash-design" }
```

- **不要传 `seed`**。seed 只用于复现示例；真实使用必须用系统随机。
- **方向数 N** → `count`：用户说了数量就用（"3 个方向""give me 8 options""/hash-design 3 deck"；Claude Code 里斜杠命令的参数会以 `ARGUMENTS: 3 deck` 出现），否则 5。范围 1–12：每个方向各是一个独立的哈希，约束不影响上限；上限是为了让一次掷骰还能逐个看完。参数里的场景词（deck/app/dashboard/poster/email，幻灯片/App/看板/海报/邮件）就是下面的 `scenario`。
- **场景** `scenario`：做的不是网页时传 `deck`（16:9 幻灯片）/ `app`（手机界面）/ `dashboard`（看板）/ `poster`（海报、社交卡片）/ `email`（HTML 邮件）；网页不传（默认 `web`）。它和其他约束一样是设计身份的一部分，复现时要再传一次。
- 用户的硬约束才写进约束：`light_only` / `dark_only` / `reduced_motion` / `brand_colors`（品牌色，最多 2 个，第一个同时决定色相）。不要为了"安全"擅自加约束。
- **不要因为不喜欢结果而重掷。** 只有用户要求时才重掷。

### 2. 回复用户，然后停下（回复协议）

`roll_designs` 会返回一段 reply（CLI：`roll … --format reply`）。**原样发给用户**（用户用别的语言就翻译），前后不加别的话，然后**停下**。它的形状固定（中文 roll 的 reply 是中文）：

```
**hash-design** · N directions for “<subject>” · <scenario> · true-random

1. **<Display face>** / <Body face> — <light|dark> paper, hue <H>° · <C>-column grid · anchor: <subject>[ · <format>] · `<short ref>`
…
N. …

Reply with a number to build that direction as the final <page|deck|app screens|dashboard|poster|email>, **render** to see all N as previews side by side first, or **reroll** for a new set.
```

- 不贴 brief 内容，不写长段解释，不推荐（用户问了才说）。
- 用户回复**编号** → 第 7 步，直接按那份 brief 做正式产物；**render / 预览** → 第 4–6 步；**reroll / 重掷** → 回到第 1 步重新掷；混搭（"#2 的版式 + #4 的配色"）→ 第 7 步，并注明来源 ref。

### 3. 冻结 brief

`out_dir` 会写出 `roll.json`、`ROLL.md` 和 `briefs/01-<短哈希>.md … NN-<短哈希>.md`。从这一刻起 brief 是**冻结的规格**：

- 字体、色值、版式结构、首屏锚点（anchor）、密度、动效、母题、材质、文案语气（voice）、变数（twist）都按 brief 执行。
- 不允许"顺手优化"成你习惯的样子（换成 Inter、加渐变、加圆角阴影卡片、把首屏改成居中双按钮……）。
- 需要复现某个 brief：`get_brief`，传 `ref` 和**同样的约束**。

### 4. 逐个渲染 N 个独立 HTML 预览（用户回复 render 时）

对每个 brief **单独**做一个预览，保存为 `design/hash-design/previews/<与 brief 同名>.html`，例如 `previews/01-4e60ca25.html`。

独立性要求（这是方法能生效的关键）：

- 做第 N 个时，**只看第 N 份 brief**；不要参考前面预览的代码，不要复用 CSS，不要统一组件。能开子 Agent 就每个预览开一个独立子 Agent，只给它那一份 brief + 事实。
- 每个预览是**单文件**：内联 `<style>`，用 brief 里的 Google Fonts `<link>`，粘贴 brief 的 `tokens.css` 并只用这些变量取色；不用 Tailwind CDN、不用 UI 框架、不引入图标库。
- 首屏必须是 brief 的 **anchor**（主体、宽度、位置、旋转都按数值）；栅格用 brief 的列数和间距，文本块放在 brief 指定的列，区块数和分隔方式照做；文案按 **voice** 的人称、标题形式、句长和语域写；**twist** 要看得出来。
- 图片：没有真实素材就不用照片，用排版、色块、自绘 SVG、brief 母题完成视觉。
- 必须响应式（至少 390px 手机宽度可读），`<html lang>`、`<meta viewport>` 齐全，尊重 `prefers-reduced-motion`。
- 文件顶部写注释：`<!-- hash-design #N · <短哈希> · ref <ref> -->`。
- **非 web 场景**：按 brief 的「场景 Scenario」一节交付（格式、画布尺寸、文件结构、数量、场景规则与禁忌），它优先于上面针对网页的要求。固定画布（幻灯片、海报）整体等比缩放，不重排；邮件不用脚本，用表格布局并内联样式。

### 5. 自检每个预览

对每个预览调用 `critique_page`：

```json
{ "path": "design/hash-design/previews/01-4e60ca25.html", "roll_path": "design/hash-design/roll.json", "pick": 1 }
```

- 所有 **critical / major** 必须修掉；minor 尽量修，保留的要能说出理由。
- `adherence`（对 brief 的遵守度）应 ≥ 80。低于就是你偏离了 brief，回去对照 brief 改。
- 静态检查抓不到一切：再自己对照 brief 的「交付前自检」清单过一遍。

### 6. 并排对比页，回复，再停下

调用 `build_compare_page`（`{"roll_path": "design/hash-design/roll.json"}`），得到 `compare.html`：N 个预览缩放后并排，带方向编号、配色色块、字体、栅格、语气、变数，支持桌面/手机切换和单张放大。它返回第二段 reply（对比页路径 + 同样的列表 + "回复编号"），原样发给用户（能打开 compare.html 就打开），然后**停下，等用户回复编号**。不要替用户选，不要说"我推荐 #3"，除非用户明确问你意见。

### 7. 按选中的 brief 落地正式产物

- 只读选中的那一份 brief（及其预览，如果做过）。预览可以作为起点，但正式页面要把**全部事实**组织进去，补齐所有区块、交互和移动端。
- 仍然遵守 brief 的全部 token 和全局禁令；用户要求的修改优先于 brief，但不要借机回到默认审美。
- 用户如果明确要求混搭（"#2 的版式 + #4 的配色"），照做，并在页面注释里写明来源 ref。

### 8. 最终自检并交付

对正式页面调用 `critique_page`（带 `roll_path` + `pick` 或 `brief_ref`），修到没有 critical/major。交付时说明：用了哪个 ref、做了哪些取舍、还有哪些"待补"事实。

## 硬性规则

1. 风格来自骰子，不来自你。你的品味只用于**执行质量**：对齐、节奏、细节、可读性。
2. 一个 brief 一个独立预览；预览之间不共享代码。
3. 只用事实；不编造社会证明。
4. 全局禁令高于一切（见下方，自动生成，与数据同步）。
5. 掷骰后、对比页后都必须按回复协议回复并停下，等用户选择。

<!-- BEGIN GENERATED: bans (npm run sync) -->
### 全局禁令（14 条，与 hash-design 数据同步）

- **禁用 Inter 及同类默认无衬线** (`generic-sans`, critical)
- **禁用紫蓝渐变** (`purple-blue-gradient`, critical)
- **禁用居中 hero + 双按钮** (`centered-hero-two-buttons`, critical)
- **禁用三张同款卡片** (`identical-cards`, major)
- **禁用玻璃态** (`glassmorphism`, major)
- **禁用 emoji 当图标** (`emoji-icons`, major)
- **禁用空洞营销文案** (`buzzword-copy`, major)
- **禁用"圆角 + 柔和大阴影"一切** (`soft-shadow-rounded`, major)
- **禁止编造事实与社会证明** (`invented-facts`, critical)
- **禁用框架默认色板** (`tailwind-default-palette`, major)
- **禁用"每段都淡入上浮"** (`scroll-fade-everything`, minor)
- **禁用标题上方的胶囊徽标** (`pill-badge-sparkle`, minor)
- **禁用占位内容** (`placeholder-content`, major)
- **禁用 SaaS 模板分节** (`template-sections`, minor)

禁用字体：Inter, Inter Tight, Inter Display, Roboto, Roboto Flex, Open Sans, Lato, Poppins, Montserrat, Nunito, Nunito Sans, Plus Jakarta Sans, Manrope, DM Sans, Outfit, Figtree, Geist, Urbanist, Sora, Lexend, Raleway, Work Sans, Space Grotesk。

字体池：98 个标题字体 × 62 个正文字体，由哈希字节直接选，没有风格分类。
<!-- END GENERATED: bans -->

## MCP 工具 ↔ CLI 对照

| MCP 工具 | CLI |
|---|---|
| `roll_designs` | `hash-design roll --subject "…" --facts-file facts.md [--count N] [--scenario deck] --out design/hash-design --format reply` |
| `get_brief` | `hash-design brief <ref> [约束参数]` |
| `critique_page` | `hash-design critique page.html --roll design/hash-design/roll.json --pick 1` |
| `build_compare_page` | `hash-design compare --roll design/hash-design/roll.json`（预览齐全时打印第二段 reply） |

MCP 资源：`hash-design://bans`、`hash-design://workflow`（本文件）；MCP prompt：`hash-design`。

## 目录约定

```
design/hash-design/
  roll.json            # 哈希、约束、事实、每个 brief 的 JSON
  ROLL.md              # 概览表 + refs
  briefs/01-<短哈希>.md … NN-<短哈希>.md
  previews/01-<短哈希>.html … NN-<短哈希>.html
  compare.html         # 并排对比页
```
