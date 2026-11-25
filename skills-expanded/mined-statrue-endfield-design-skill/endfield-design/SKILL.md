---
name: endfield-design
description: "Design or restyle interfaces, websites, editorial graphics, and key visuals using the observable visual language of 《明日方舟：终末地》 / Arknights: Endfield. Use when the user explicitly requests 终末地风格 or Endfield style, supplies Endfield references to study or continue, or the project already uses this design system. Do not activate for generic sci-fi, industrial, black-yellow, or Hypergryph-inspired work without an Endfield-specific request."
---

# Endfield Design

Create work that belongs to the same visual world as 《明日方舟：终末地》 without reducing that world to a black-yellow skin or copying one official composition. Preserve the user's product, content, framework, and interaction requirements; this skill changes visual and structural decisions only within the requested scope.

This skill is self-contained: Build, Audit, and Redesign need no network access and no official images. The rules below were derived from official material whose sources are registered in `references/source-registry.md`. Study can use supplied material or explore official sources when the user asks for research.

## Verbs

Identify which job the user is actually asking for; each has a different deliverable and a different write permission.

- **Build**（默认）：为新内容设计。走完整工作流：先定家族与结构，再上母题。
- **Audit**：对照本系统检查已有界面或物料。产出按文件/位置定位的问题清单（结构、语义、克制、可用性），不主动改稿。
- **Redesign**：保留内容、数据、路由与信息架构，重构视觉与版式。先诊断旧结构为何失效，再选择新家族。
- **Study**：从用户提供的新终末地素材，或用户要求探索的官方渠道中提炼规律。**默认只输出观察报告**——区分反复出现的特征、主题专属特征、与现有规则冲突的证据，并给出置信度。用户明确要求"保存 / 更新 / 锁定"后，可修改 `references/evidence-map.md`、`references/source-registry.md` 与对应规则文件；修改前说明将改动哪些文件与章节。同一会话内已明确给出的探索/更新授权，在其声明的范围内对后续来源持续有效——换账号、换图不必重复请求；超出范围、换会话或触及 SKILL 核心规则时重新确认。新增全局规则需至少两个独立界面、主题或媒介交叉支持，或明确的官方设计规范；同一活动跨账号转发不算独立证据。单张画面只能进入家族、条件或主题层。渠道核验和采样方法见 `references/official-sources.md`。

If the project already contains an `endfield-design-context.md`, read it first; it records that project's approved families, theme, components, and exceptions (format in `references/project-context.md`). Project exceptions are never written back into this skill.

## Start with the job, not the motifs

Before designing:

1. Inspect the existing project, supplied references, real copy, assets, and implementation constraints. Reuse established tokens and components unless the user asked for a redesign.
2. Identify the artifact's audience, primary job, dominant content, and interaction density. Infer missing context when it is safe; ask only when different answers would materially change the result.
3. Pick one **surface family** from `references/surface-families.md`. A product may combine families, but each screen or section needs one dominant family.
4. Pick a theme anchor: default system yellow, a content-led event/operator/region color, or an existing brand color. Theme changes may also alter typography, texture, and graphic rhythm; do not treat them as color swaps.
5. Sketch the macro structure (zones, axes, focal anchor) before choosing any surface motif. State the decision briefly:

   `verb · family · visual anchor · theme · interaction stance · signature`

   **signature** is the one structural or interaction decision, produced by this content, that makes the piece memorable — e.g. "接管设施节点时拓扑与权限层级同时重排". It must not be a surface motif (yellow, slashes, grids, cut corners, outline type). For high-frequency utility surfaces (dashboards, bot images, dense tools) "清晰本身即记忆点" is a valid signature; do not invent novelty there.

## Stable design DNA

These principles survive across the official game UI, website, and editorial material.

### 1. Spatial hierarchy

- Use an off-center focal anchor: a character, map region, machine, large number, title block, or content cluster.
- Dock secondary information to edges, rails, bands, or shallow planes. Avoid surrounding every item with an equal card.
- Separate foreground action, primary content, and technical background into visibly different planes.
- Let composition follow the task; a diagonal wedge, fan, radial hub, or vertical rail can be the organizing structure itself, not decoration. Do not reuse a fixed hero, header, card grid, or footer merely because it looks on-brand.

### 2. Neutral material base, visible action

- Build on paper white, concrete gray, smoked charcoal, or near-black rather than pure white/black everywhere. Light and dark bases are both canonical; pick by content and context.
- Color has system roles, not one accent. This table is the single authoritative definition; `techniques.md` holds the tokens, `evidence-map.md` holds the supporting observations.
  - **黄**：默认导航、选中、系统行动、未读与新内容；也是**进度/完成度条**的填充色（任务、经验、通行证：灰轨 + 黄填充）；
  - **橙**：第二系统强调——通知菱形、倒计时、等级带、数量与折扣、稀有度上段；
  - **荧光黄绿**：增益与增量标签——“+6%”一类增益 chip、经验增量、新数值；不用于进度条填充（进度条归黄）；
  - **蓝**：量值图表与流程（产耗面积图、链路）、稀有度低段——官方产耗行图表与低稀有度实测为天蓝，不是青。区分：表达“完成了多少”的轨道条用黄，表达“数量有多少”的图表用蓝；
  - **青**：地区/机构主题色（地区建设、事项总览等同构换色；版本物料也随本版主地区换色，如雪山版本的日历与周边取冰蓝/青），不用作通用数据色；
  - **红**：危险、紧急、超支；也作身份权限强调与编辑物料的档案强调色；
  - **绿**：确认、充裕、通用标签；
  - **紫**：特殊与战术物品、高稀有度、特定角色主题；
  - **稀有度色阶**：蓝 → 紫 → 金黄 → 橙。
- Event, operator, and region themes may take over a whole surface (structure retained, palette/texture/typography swapped). Keep one dominant theme color plus a few semantic colors; never delete danger/success semantics.
- Multicolor registration strips are decorative print language. Do not use them as a universal header or as conflicting data semantics.

### 3. Shape follows meaning

- Angular cuts, wedges, brackets, corner hooks, and hard-edged bands communicate machinery, navigation, authority, or action.
- Circles and arcs suit instruments, skills, avatars, map radii, gauges, and targeting.
- Rounded rectangles and capsules suit conversation, filters, resources, transient status, and compact touch controls. White capsules with a circular icon chip are the canonical primary CTA on studio/tool surfaces; dark capsules carry secondary actions.
- Selection often speaks through **corner brackets, edge bars, or light/dark inversion** rather than a glow. Completed/celebration states may invert to dark ground with a yellow zone and giant outline word; pending states may drop to light gray.
- Do not maximize either angularity or roundness. Contrast between shape families is part of the language.

### 4. Typographic roles

- Functional UI defaults to a legible CJK sans with a geometric or semi-condensed Latin companion. Use tabular figures for dense numerical interfaces.
- Display and campaign material may use high-contrast, brush-like, condensed, expanded, handwritten, or rune-like decorative lettering when the subject supports it.
- English micro-labels, `//` breadcrumbs, indices, coordinates, keycap hints, and version strings create a technical secondary layer. They must support hierarchy or orientation; do not generate decorative pseudo-technical noise.
- Ghost typography (giant outline or low-contrast words/numerals) can index sections and phases; it must not fight the real title.
- Avoid fabricated metrics, meaningless English, fake legal copy, or arbitrary serial numbers presented as real data.

### 5. Technical texture with a budget

- Grids, contour lines, hatching, halftone, crop marks, measurement overlays, glitch slivers, pixel strips, and outline type are optional tools.
- Editorial material may add human traces — highlighter marks, red pen circles, stamps, tape, stickers — when the material is meant to read as an annotated document.
- Use two or three related texture systems in one view, normally at low contrast. Add more only for deliberately dense editorial material.
- Keep decorative layers subordinate to content and contained so they cannot create overflow or interaction interference.

### 6. Specificity over costume

- Derive the layout from the artifact's real content and task, then apply only the motifs that reinforce it.
- Preserve meaningful irregularity: unequal columns, interrupted grids, variable density, and asymmetric negative space.
- Reject generic sci-fi defaults such as indiscriminate neon glow, hexagons everywhere, fake telemetry, glass cards on every surface, or yellow borders around every component.

## Routing

Read only the references needed for the current task.

- Choose the visual structure → `references/surface-families.md`.
- Build an APP, desktop tool, dashboard, game-like UI, or individual interactive component → `references/app-ui.md`.
- Build a responsive website or landing page → `references/web.md`.
- Create a static poster, guide, calendar, report, or social long graphic → `references/infographic.md`.
- Compose an activity KV or write image-generation prompts → `references/imagegen.md`.
- Need a restrained motif or implementation technique → `references/official-motifs.md` and the relevant part of `references/techniques.md`.
- Render a fixed-width HTML artifact to PNG → `references/engineering.md` after the layout is decided.
- User asks to save this project's design decisions → `references/project-context.md` (never auto-create).
- Study new official material, or audit this skill's own rules → `references/evidence-map.md` and `references/source-registry.md`; do not load them for ordinary generation.
- Discover official websites, accounts, or recurring editorial series for Study → `references/official-sources.md`; browse only when the task calls for research.

This skill contains no universal page template or component gallery. Build structure from the chosen family and the user's actual content; do not recreate a query-result header, fixed brand strip, or report footer unless the requested product genuinely needs one.

## Build and verify

- Preserve existing routes, copy intent, data, accessibility, and component ownership unless the user requested changes to them.
- Implement states that the artifact actually needs: default, hover when applicable, keyboard focus, active/selected, disabled, loading, empty, error, and success.
- For responsive work, verify narrow phone, wide phone, tablet, and desktop behavior. Style must survive content wrapping and localization.
- For static graphics, verify reading order, minimum readable type, image fallback, crop safety, and export dimensions.

### Pre-emit gates

Before handoff, run these checks. **Any gate that fails → revise. Two or more gates that pass only marginally → revise.** Do not hand off with a known failing gate.

1. **换题测试**：换一种**内容类型或任务**（如把任务列表换成数据简报），这个结构还会一模一样吗？会 → 结构没有从内容推导。同家族、同内容类型的页面共享结构是预期行为（两张角色详情页理应同构），不算失败。
2. **脱皮测试**：去掉黄色与切角后，层级和主要行动是否仍然成立？
3. **家族测试**：能否一句话指出主家族、视觉锚与 signature？说不出 → 回到结构阶段。
4. **语义测试**：每个颜色、形状、状态变化是否表达含义？有无颜色与既定角色冲突（如把红当普通装饰）？
5. **克制测试**：技术纹理是否 ≤2–3 套且低于内容对比度？有没有无意义英文、伪数据、假编号？
6. **真实测试**：所有数字、日期、名称、素材来源是否真实或明确标注为占位？
7. **可用测试**：键盘焦点、触屏目标、长文案换行、加载/空/错误态是否可用？（静态物料改查阅读顺序与最小字号。）
8. **版权测试**：是否引入了用户未提供的官方 Logo、立绘、截图或专有字体？

### Report

State the verb, family, theme anchor, signature, and any official motif intentionally omitted. Report verification honestly with four levels — `verified`（实际打开检查过）/ `partial` / `blocked`（环境受限）/ `not tested` — separately for **visual**, **responsive**, and **interaction** where each applies. A screenshot that was generated but not inspected is not `verified`.

## Brand and source boundary

Treat official material as visual research, not as a license to copy assets. Do not introduce official logos, character art, screenshots, proprietary fonts, or brand claims unless the user supplied them and has chosen to use them. Prefer describing observable attributes in prompts and design notes. For public or commercial release, flag that the user must confirm rights to trademarks, artwork, fonts, and source images; do not make legal conclusions on their behalf.
