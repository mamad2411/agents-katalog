---
name: frontend-templates
description: "新前端项目起步、给现有项目注入设计体系、或写控制台/后台/数据密集界面/内容编辑向界面/创作影视工具之前必读。把「要做什么」映射到模版库 <~/frontier> 的具体模版：读声明、按 MANIFEST 复制骨架、按声明定制、跑护栏验收。当前模版：graphite(软性单色开发者控制台)、tape(纸墨新粗野内容/编辑向骨架)、ember(琥珀影视控制台/暖色叙事极)。"
---

# frontend-templates · 前端设计体系入口

## Mandate

把「要做什么界面」映射到模版库里**具体的模版与声明**，然后按 MANIFEST 复制、按声明定制、跑护栏验收——不要凭记忆手搓设计体系，也不要把某个模版硬套到不适用的产品形态上。

- 库根：`~/frontier`（模版根 `~/frontier/templates/<name>/`）。
- 当前三个模版：**graphite** = 软性单色（zero-chroma 中性灰）开发者控制台，适用后台 / 控制台 / 数据密集工具；**tape** = 纸墨新粗野（paper-and-ink neo-brutalist），适用内容 / 编辑向产品与高能量落地页；**ember** = 琥珀影视控制台（暖色叙事极，chroma 0 中性基座 + 恒定琥珀 primary + 胶片监视器/涟漪网格/编辑风母题），适用创作 / 影视 / AI 工具类产品。
- 取值与规范全部沉淀在四份声明里，agent 只读声明即可正确使用，无需回看组件源码。

**何时触发本 skill**：开新前端项目、给现有前端注入设计体系、要写控制台 / 后台 / 数据密集界面 / 创作影视工具、或换品牌配色之前。
**不替代什么**：本 skill 只做「选模版 → 复制 → 定制 → 验收」的调度；具体取值规范在四份声明里，业务功能定义在消费方自写的 `spec.md` / `domain.md` 里，各有归属，不在此重复。

## 库缺失时的行为（先确认这一步）

若 `~/frontier` 不存在：**停下来问用户库的位置**（本地路径或 git 地址），不要自行猜测路径、不要跳过、不要临时另起一套体系。拿到位置后把下文所有 `~/frontier` 替换为实际库根再继续。

## 五步工作流

每步给出「判断依据」与「产出」，逐步推进，不跳步。

### 1. 定位场景

- **判断依据**：确认要做的页面类型。控制台 / 管理后台 / 数据密集工具（Product Console 类，导航项成十上百条需分组折叠）→ 走 graphite；内容 / 编辑向产品（信息流、发布台账、知识库）或需要高能量视觉签名的营销落地页、导航项扁平（个位数到十余项）的轻量控制台 → 走 tape；创作 / 影视 / AI 工具类产品（拍摄台账、渲染队列、素材审阅）或需要暖色叙事感的内容/编辑向产品、导航项扁平的轻量控制台 → 走 ember；单屏产品 landing → graphite（软性单色）/ tape（高能量新粗野）/ ember（暖色叙事）均可，按品牌调性三选一；内容型营销站 / 多页官网 / 文档站、单页表单产品 → **目前无对应模版**，明确告知用户「graphite/tape/ember 都是后台或编辑向骨架，不适用该形态」并停止，不要硬套 AppShell。判据的事实源：`~/frontier/templates/{graphite,tape,ember}/declarations/templates.md` 各自的「适用与不适用场景」表。
- **产出**：一句场景判定结论——「适用 graphite」/「适用 tape」/「适用 ember」/「无匹配模版，已告知用户」。

### 2. 选模版

- **判断依据**：按场景匹配表路由到对应模版，再读对应速查卡复核。

  | 场景特征 | 模版 | 速查卡 |
  | --- | --- | --- |
  | 数据密集、导航项多需分组折叠、界面层次靠灰面明度台阶、低调效率优先 | graphite | `~/frontier/skills/frontend-templates/references/graphite.md` |
  | 内容 / 编辑向、导航项扁平、需要高能量视觉签名（硬描边+硬偏移阴影+巨字标题）、中文重字是签名一部分 | tape | `~/frontier/skills/frontend-templates/references/tape.md` |
  | 创作 / 影视 / AI 工具类、导航项扁平、需要暖色叙事母题（胶片监视器/涟漪网格/编辑风玻璃描边巨字）、卡片描边形状语言 | ember | `~/frontier/skills/frontend-templates/references/ember.md` |

  三者是同一套 create-vite + Tailwind v4 + radix-ui + motion 工具链下的平行模版，选错会导致后续「按声明定制」错读取值——拿不准时用速查卡的「一句话签名 + 适用/不适用」复核第 1 步结论，而非凭印象二选一。ember 与 tape 都是顶栏型骨架、导航都扁平，别只看结构混淆：tape 是新粗野高能量视觉签名（零圆角+硬偏移阴影+恒定电光蓝），ember 是暖色叙事母题签名（描边+圆角+柔和阴影+恒定琥珀+胶片监视器）。
- **产出**：确定所选模版（graphite / tape / ember）及其模版根路径。

### 3. 按 MANIFEST 复制骨架

- **判断依据**：严格按 `~/frontier/templates/graphite/MANIFEST.md` 从上到下执行六步，**不要凭记忆挑文件或跳步**；`.example.` / `-ui.mjs` 后缀件是「参考合入」（把内容并进消费方对应文件），不是「直接覆盖」。六步概览：
  1. 复制文件（复制清单表：`index.css` 整覆盖、`lib/` 五件全拿、`hooks/`、`components/ui/` 整目录、`components/shell/` 后台类全拿、`locales/`、`scripts/`、`config/`）。
  2. tsconfig 接线：只加 `paths: { "@/*": ["./src/*"] }`（消费方是 `./src/*`，**不是** demo 的 `../skeleton/src/*`；**不要加 `baseUrl`**——现行 TypeScript 已弃用，`tsc -b` 会报 TS5101）。
  3. vite + main 接线：`resolve.alias` `@` + `react/motion/overlay` 三 vendor 分包 + overlay preload 过滤；`main.tsx` 用 `ThemeProvider` + `<MotionConfig reducedMotion="user">` + `initI18n`。
  4. eslint 接线：引 `config/eslint-ui.mjs` 的 `nativeControlRestrictions()` + `vendoredUiOverrides()`。
  5. package.json 脚本：`build` 末尾挂 `check-bundle-budget.mjs`、`lint` 串 `check:ui`（零参数即消费方默认布局）。
  6. test-setup：复制**内容**到 `src/test/setup.ts`，勿跨包引用（见坑位沉淀末条）。
- **产出**：在一个空的 `create-vite react-ts` 工程上叠加出可 `lint` / `build` 通过的 graphite 骨架。

### 4. 按声明定制

按需求读对应声明，不要四份全读、也不要一份不读：

| 要做的事 | 先读哪份声明（完整路径） |
| --- | --- |
| 换品牌 / 改配色 · 密度 · 字体等取值 | `~/frontier/templates/graphite/declarations/design.md`（尤其 V7 的**必填 / 可调 / 勿改**三类分级与「换品牌操作序列」） |
| 写页面 · 搭页面骨架 | `~/frontier/templates/graphite/declarations/templates.md`（AppShell / AuthShell、页面三段式、四类场景默认骨架） |
| 选组件拿不准（Badge? Dialog? Sheet?） | `~/frontier/templates/graphite/declarations/components.md`（全组件清单 + 语义边界） |
| 动效 · 加载态 · 密度 · 无障碍 | `~/frontier/templates/graphite/declarations/craft.md` |

- **判断依据**：换品牌只动 `index.css` 顶部两块 token（`:root` 与 `[data-theme='dark']` 都给值），组件零改动；品牌标识走 `brand.tsx` 单通道（**AppShell 无 `brand` prop**）。同时引导用户为本项目写 `spec.md`（功能定义）与 `domain.md`（业务领域语义）——声明只给空骨架，业务字段由消费方自写；写法见库级 `~/frontier/docs/writing-spec-and-domain.md`（Task 19 落地后可用）。
- **换品牌操作序列**（design.md V7，只动 `index.css`）：
  1. 在 `:root` 与 `[data-theme='dark']` 两块各重定义「必填」token（`--primary` 三件套、`--background`、`--foreground`、三语义色），每个都给该主题下的值，不留空。
  2. 保留 soft monochrome 则灰面继续用 `oklch(L 0 0)`（色度 `0`）；只微调明暗改「可调」的 `--surface* / --muted`。
  3. 不碰 `@theme inline` 映射键（除非换字体栈——那必须改在 `@theme inline` 内的 `--font-sans` / `--font-mono` 行）。
  4. 跑验收清单前四条；对比不足或语义色变实心即回退。
- **产出**：品牌 token 落到 `index.css` 两块、按场景骨架搭好的页面；`git diff --stat` 应只见 `index.css` 变更。

### 5. 验收

- **判断依据**：两道机器护栏全绿 + 四份声明末尾的验收清单逐条核对。护栏命令（消费方项目根）：
  - `pnpm lint`（串 `check-ui.mjs`：拦业务层原生控件 / emoji / 裸色值）
  - `pnpm build`（末尾跑 `check-bundle-budget.mjs`，超预算 `exit 1`）
  - 四份声明各自的「验收清单」小节逐条 grep 或肉眼核对（汇总见速查卡）。
- **产出**：护栏结果 + 四清单核对结论的输出；有缺口按 design.md V7 记 `gaps.log`，不私自绕过。

## 坑位沉淀（体系性不可犯的错）

初始条目如下，随仓库演进增补：

- **字体**：Tailwind v4 接字体走 `@theme inline` 直写字体栈；只在 `:root` 覆盖 `--font-sans` **不会**被 `font-sans` 工具类采纳（会静默回退默认栈，无报错）。团队踩过。
- **焦点环**：`outline` 焦点环不可删、不可换成 `outline: none`——键盘用户底线（craft.md 勿改类）。
- **裸值**：业务层禁 hardcode 色值 / `px` 阴影 / `ms` 时长；缺 token 记 `gaps.log`，不私自绕过。
- **demo 展柜页别抄**：`demo/src/pages/{tokens,components,motion,overview}-page.tsx` 是文档不是生产骨架；`patterns` / `auth-sample` 可抄布局但**必换样例数据与文案**。
- **语义色不实心填充**：`success/warning/danger` 一律「淡底 + 实色文字」；除 `--primary` 外禁实心彩色填充。
- **禁 emoji**：前端工程全源码不得出现 emoji，`check-ui` 会硬拦。
- **品牌单通道**：`AppShell` / `AuthShell` 都**无 `brand` prop**，换品牌标识只改 `brand.tsx`（保留 focus ring 与尺寸结构），让移动顶栏 / 侧栏 / 抽屉 / 认证页永远一致；双控制台（用户台 / 管理台）由调用方按 `location.pathname` 传不同 `navigation`，AppShell 本身无 `admin` 概念。
- **磨砂玻璃只用于 sticky chrome**：只有顶栏与侧栏有 `backdrop-blur`，普通卡片实心不透；满铺 `backdrop-blur` 是 AI Slop 起手，review 会打回。
- **`@/` alias 两处都要接**：skeleton 源码的 `@/` 依赖消费方 `@ -> src` 别名（tsconfig `paths` + vite `resolve.alias`），复制后先确认两处 alias 再排查 `Cannot find module`。
- **test-setup 是复制内容、不是跨包引用**（执行期教训）：把 `config/test-setup.ts` 的**内容**落到消费方 `src/test/setup.ts`，**不要**写 `import '.../skeleton/config/test-setup'`——`@testing-library/jest-dom` 只装在消费方，跨包 bare specifier 会解析失败（本库 demo 就地留了独立副本正因如此）。
- **别把 graphite 与 tape 的 token 心智混用**（tape 专有坑）：tape 的 `--primary` 是恒定电光蓝、不随主题反相，`--border`/`--border-strong` 恒等前景色不做透明度分级，`outline` 按钮反而是「真描边」而 `ghost`/`link` 才零描边——这几条与 graphite 方向相反，照抄 graphite 心智会做错，换模版时先看 `references/tape.md`「token 分级速记」与「组件语义速记」两节。
- **tape 圆角是勿改档**：`--radius` 恒 `0px`，零圆角是 neo-brutalist 签名的一部分，不像 graphite 有密度档位可调。
- **tape 自托管 CJK 字体是有意的 bundle 代价**：4 个 `@fontsource` 包（含中文 700/900 两档）使关键 CSS 预算定在 `128KB`（非 graphite 的 `16KB`），预算敏感或纯拉丁内容消费方按 `templates/tape/MANIFEST.md`「定制指引」的去 CJK opt-in 步骤降级，不要直接改小预算常量了事。
- **ember 的 chroma 0 中性基座别称「暖灰」**（ember 专有坑，verifier 已纠）：`index.css` 的灰阶 token 写法是 `oklch(L 0 95.33)`——`hue` 位保留 `95.33` 是忠于 actionow 源码的写法，但 `chroma`（第二位）恒为 `0`，OKLCH 下 chroma=0 时 hue 无视觉效果，渲染结果与 graphite 的 `oklch(L 0 0)` 像素等价；ember 的差异化全部压在琥珀 primary + 三件母题装饰层 + 卡片描边形状 + 编辑风 landing 四条结构性差异上，不靠基座换色，文档与对话里不得称基座为「暖灰」。
- **ember 的主色恒定不反相，`--ring` 恒等 `--primary`**（与 graphite 相反）：`--primary: oklch(88.68% 0.1822 95.33)` 浅暗两套完全相同，焦点环颜色因此恒为琥珀，换品牌只需重定义 `--primary` 三件套，`--ring` 自动联动，不需要单独改。
- **ember 母题件是纯装饰，别塞业务数据**：`MonitorBackground`/`RippleGrid`/`GlassText` 三件专有组件只接受视觉开关（`showRec`/`columns`/`className` 等），不接受业务数据 prop；需要展示业务状态时用 `Badge`/`StatCard`/`ApiErrorNotice` 叠加在母题层之上，且接入前先给一个 `relative` 定位容器再叠加（专展页整屏铺陈是唯一例外，见 `references/ember.md`「母题克制原则」）。
- **ember 是变量字体包，别照抄静态逐权重写法**：依赖是 `@fontsource-variable/plus-jakarta-sans` + `@fontsource-variable/jetbrains-mono`（`wght.css` 变量轴单文件覆盖全部字重），family 名 `'Plus Jakarta Sans Variable'`/`'JetBrains Mono Variable'`，CJK 走系统回退不自托管；CSS 预算与 graphite 平价 `16KB`（实测约 12.9KB），不要照抄 tape 的 `128KB`。

## 报告契约

完成一轮接入 / 定制后，向用户汇报三点，别只说「做完了」：
- **选了哪个模版、为什么**（场景判定结论）；若判定「无匹配模版」，说清原因并停在第 1 步。
- **改了哪些文件**：换品牌应只有 `index.css` 两块 token 变更（`git diff --stat` 佐证），组件零 diff。
- **验收结果**：`pnpm lint && pnpm build` 是否全绿、四份声明验收清单逐条核对结论、`gaps.log` 是否有未闭环缺口。

## 库内导航

- **graphite**（软性单色开发者控制台）：
  - 模版速查卡：`~/frontier/skills/frontend-templates/references/graphite.md`（先读这份）
  - 复制清单：`~/frontier/templates/graphite/MANIFEST.md`
  - 四份声明：`~/frontier/templates/graphite/declarations/{design,craft,components,templates}.md`
  - 展柜（跑起来看）：`pnpm --filter graphite-demo dev` → http://localhost:4373
- **tape**（纸墨新粗野内容/编辑向骨架）：
  - 模版速查卡：`~/frontier/skills/frontend-templates/references/tape.md`（先读这份）
  - 复制清单：`~/frontier/templates/tape/MANIFEST.md`
  - 四份声明：`~/frontier/templates/tape/declarations/{design,craft,components,templates}.md`
  - 展柜（跑起来看）：`pnpm --filter tape-demo dev` → http://localhost:4375
- **ember**（琥珀影视控制台/暖色叙事极）：
  - 模版速查卡：`~/frontier/skills/frontend-templates/references/ember.md`（先读这份）
  - 复制清单：`~/frontier/templates/ember/MANIFEST.md`
  - 四份声明：`~/frontier/templates/ember/declarations/{design,craft,components,templates}.md`
  - 展柜（跑起来看）：`pnpm --filter ember-demo dev` → http://localhost:4376
