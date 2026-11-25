---
name: design-spec
description: Web 设计规范生成器——读 PRD/03-design-handoff.md（设计交接清单）+ PRD/04-pages-components.md（页面组件清单），产出包含完整 hex 色板/字体/间距/动效/组件样式的 DESIGN.md。0→1 流程中必须在 PRD 完成后才跑。当用户说"做一份设计规范""定一下视觉风格""帮我写 DESIGN.md""参考 XX 出一套设计 token""按 PRD 设计页面"时触发。本 SKILL 只产规范文档,不写实现代码——代码由下游(Claude Code 默认能力)按 DESIGN.md + PRD/ 落地。
---

# Design Spec — 设计规范生成器

只做一件事:产出一份高质量的 `DESIGN.md`。

代码落地不归本 SKILL 管——交给下游 Claude Code 读 DESIGN.md + PRD.md 自己实现。

---

## 与其他 Skill 的衔接关系

```
/mrd → 从数据分析市场需求 → MRD.md
  ↓
/brd → 判断商业可行性 → BRD.md
  ↓
/prd-writing → 定义产品结构 → PRD/ 文件夹（含 PRD/03-design-handoff.md 设计交接清单）
  ↓
/design-spec → 读 PRD/03-design-handoff.md + PRD/04-pages-components.md → 产出 DESIGN.md（本 Skill）
  ↓
Claude Code 默认能力 → 基于 PRD/ + DESIGN.md 实现 MVP 代码
```

设计规范是**规格层**,代码实现是**执行层**——两层分离,互不污染。

### 🔒 PRD 必须先于 DESIGN（教学场景的硬性顺序）

本 skill **必须在 PRD 完成后才运行**。如果当前目录没有 `PRD/` 文件夹（或没有 `PRD/03-design-handoff.md`），告诉用户先跑 `/prd-writing`，不要硬上。

**为什么这样划线**：
0→1 项目还没有"已存在的设计系统"作为约束，必须先定结构（页面/组件/路由）才能定皮肤（颜色/字体/动效）。如果反过来（先 DESIGN 再 PRD），DESIGN 阶段不知道有哪些组件要被定规范，做出的设计是空中楼阁。这条流程顺序在教学场景里是绝对的。

---

## 核心原则

1. **DESIGN.md 是显式产物**,保存到项目根目录,可手动改、可被任何工具消费
2. **不写页面代码**,代码由 Claude Code 读 DESIGN.md + PRD/ 自己生成
3. **PRD 是上游,本 skill 是下游**——0→1 项目必须先有 PRD/ 文件夹,本 skill 读 `PRD/03-design-handoff.md` 作为输入
4. **能继承就继承**:有 03-design-handoff.md 就读它,有参考 URL/截图就提取
5. **有数据就用数据,没数据用对话**——不要一上来就给问卷
6. **MVP 优先**——规范服务于「先把核心功能跑起来」,不要为「将来可能用到」加复杂度
7. **默认 Web 端响应式网页**,除非用户明确说要做 App

---

## 启动检测(按优先级)

按以下顺序判断从哪里起步:

1. 项目根目录已有 `DESIGN.md`?→ 问用户:**沿用 / 修改 / 重建**
2. **项目根目录有 `PRD/03-design-handoff.md`?**（推荐路径，0→1 教学流程的标准入口）
   → 读它的 7 个小节（产品调性 / 目标用户视觉感受 / 目标市场与语言 / 参考竞品 / 视觉约束 / 组件密度提示 / 输出契约），作为主要输入
   → **同时读 `PRD/04-pages-components.md`** 拿到完整页面/组件清单（决定要为哪些组件定样式）
3. 项目根目录有旧版 `PRD.md`（单文件版）?→ 读末尾的「设计交接区」字段（兼容历史版本）
4. 用户给了参考 URL / 截图 / 关键词?→ 直接进入 Phase 1 提取
5. 啥都没有 → 询问"你跑过 /prd-writing 吗？没跑过的话 0→1 项目建议先跑，本 skill 的输入来源就是 PRD/03-design-handoff.md。如果你坚持跳过 PRD，我可以用 Phase 1 对话兜底引导（最多 3 个问题），但效果会差很多。"

### PRD 完成度门禁（情况 2 触发）

读到 `PRD/03-design-handoff.md` 后，**先做 3 项门禁检查再开始设计**：

- [ ] 03-design-handoff.md 的 §3.1（产品调性关键词）有内容
- [ ] 03-design-handoff.md 的 §3.6（组件清单视觉密度提示）至少列了 1 个页面/组件
- [ ] 04-pages-components.md 存在且能读到组件清单

任何一项不通过，告诉用户：

> ⚠️ 我读了 PRD/03-design-handoff.md，发现 [具体缺什么]。建议你回 prd-writing 把 03-design-handoff.md 补完再跑本 skill——否则我做出来的设计会和你的页面/组件清单脱节。

读取通过时告诉用户:

> "我读到了 PRD/03-design-handoff.md，产品调性是 [§3.1 关键词]，目标市场是 [§3.3]，要为 [§3.6 列出的页面] 定设计。我基于这些直接出设计规范，只补问 1-2 个 handoff 没覆盖的关键点（比如交互档位、明暗偏好）。"

---

## Phase 1: 收集设计输入(最多 3 个问题)

不强制走问卷,**有什么用什么**:

| 用户给的 | 你做的 |
|---------|--------|
| 参考 URL | 用 WebFetch 抓页面,提取色彩 / 字体 / 间距气质 |
| 截图 | 从图里读视觉气质(色温、密度、字体风格) |
| 关键词("暗色克制衬线") | 直接转 token |
| 品牌名("像 Linear 那样") | 描述该品牌的设计语言并提取 token |
| PRD 设计交接区 | 直接继承产品调性、目标用户、技术栈、语言 |

**对话兜底**(用户什么都没给时,问最多 3 个,**一次只问一个**):

1. 亮色 / 暗色 / 跟内容走?
2. 风格关键词?(克制 / 活泼 / 极简 / 编辑感 / 科技感 任选 1-2 个)
3. 有没有喜欢的网站?(可选,用户能想起就说)

### 交互档位确认(必问一次)

| 档位 | 体验 | 适用场景 |
|------|------|----------|
| **L1 静态优雅**(默认) | hover + 柔和入场动画 | MVP 阶段、内容型站点 |
| **L2 流畅交互** | 滚动 reveal、视差、导航变化 | 有充足实现时间 |
| **L3 沉浸体验** | pin 动画、光标跟随、3D / WebGL | 用户明确要求"电影感" |

**MVP 默认 L1**——先把核心功能跑通再考虑加动效。L2/L3 仅在用户明确要求时启用。

---

## Phase 2: 生成 DESIGN.md

按下面 7 个章节产出。**每个章节都要有实质内容,严禁占位符或"TODO"**。

### DESIGN.md 模板

```markdown
# [项目名] — 设计规范 (DESIGN.md)

> 最后更新:[日期]
> 上游来源:[PRD.md / 参考 URL / 用户对话]
> 交互档位:L1 / L2 / L3
> 证据等级:🟢 充分 / 🟡 有限,标注待验证项 / 🔴 探索性,结论仅供假设

---

## 1. 设计基调

- **氛围关键词**:3-5 个词(如「克制、编辑感、暖色、留白」)
- **一句话定调**:[这个产品给人什么感觉,一句话]
- **目标用户视角**:[这套设计在向哪类用户说话]
- **目标地区/语言**:[继承自 PRD,如「泰国 / 泰语主 + 英语切换」]

## 2. 色彩系统

```css
:root {
  /* 主色 */
  --color-bg: #...;          /* rgb: ...,...,... */
  --color-surface: #...;
  --color-text: #...;
  --color-text-muted: #...;
  --color-border: #...;

  /* 强调色 */
  --color-accent: #...;
  --color-accent-hover: #...;

  /* 语义色 */
  --color-success: #...;
  --color-warning: #...;
  --color-danger: #...;
}
```

每个变量必须有 RGB 辅助值(便于做 rgba 透明)。

## 3. 字体系统

- **字体引入**:`@import url('https://fonts.googleapis.com/...')`
- **中文/泰语等非拉丁字族**(对应市场必备):Noto Sans SC / Noto Sans Thai / LXGW WenKai 等
- **字号层级**:

| 用途 | 字号 | 行高 | 字重 |
|------|------|------|------|
| H1   | ...  | ...  | ...  |
| H2   | ...  | ...  | ...  |
| Body | ...  | ...  | ...  |

非拉丁文页面规则:行高 ≥ 1.7,字距 `0.02em`,正文 ≥ 15px。

## 4. 组件样式(核心 4 类)

按钮 / 卡片 / 输入框 / 导航,每个都给完整 CSS,**包含 default / hover / focus / disabled 全部状态**。

## 5. 布局原则

- **断点**:Mobile (≤640px) / Tablet (641-1024px) / Desktop (≥1025px)
- **容器宽度**:max-width: ...,padding: ...
- **间距梯度**:4 / 8 / 16 / 24 / 32 / 48 / 64
- **栅格**:[使用什么栅格系统,几列]

## 6. 动效与交互(按档位填,默认 L1)

**L1**(MVP 默认):
- 按钮 hover:transition 200ms ease-out,色彩变化
- 入场:fadeInUp,持续 400ms

**L2**(在 L1 基础上加,用户明确要求时):
- 滚动 reveal:IntersectionObserver,可见时触发
- 导航滚动变化:scroll > 100px 加背景

**L3**(在 L2 基础上加,用户明确要求"电影感"时):
- 允许的库:GSAP / ScrollTrigger / Lenis
- pin / 光标跟随 / 3D / WebGL 选用

**必备**:`prefers-reduced-motion` 降级路径。

## 7. Do's & Don'ts(各 ≥ 4 条)

**Do:**
- ...

**Don't:**
- ❌ 给 MVP 阶段塞超出 PRD 范围的视觉花活
- ...

---

## 📎 实现交接(供下游 Claude Code 读取)

```yaml
design_status: ready
theme: [关键词]
interaction_level: L1 / L2 / L3
color_system: 见第 2 节 CSS 变量
font_system: 见第 3 节
core_components: [button, card, input, nav, ...]
breakpoints: mobile / tablet / desktop
motion_libs: [若 L3 列出 gsap / lenis 等]
language_default: zh-CN / en / th 等
mvp_scope: [继承自 PRD.md 的 V1 功能列表,本规范服务于这些功能]
```

---

## 📎 给 Claude Code 的实现指令(MVP 落地)

> 本节是 DESIGN.md 的最后一节,目的是把"规格"和"实现"无缝衔接。
> Claude Code 拿到 PRD.md + DESIGN.md 后,**严格按下面规则写代码**。

### 实现纪律(MVP 优先,不可破)

1. **只实现 PRD 中列出的 V1 功能**——PRD 的「不做清单」就是不做,不要"顺手"加
2. **每个页面先跑通再美化**——HTML 结构 + 文案 + 基础样式 → 跑通 → 再加动效
3. **不引入 PRD 技术栈外的依赖**——除非 DESIGN.md 第 6 节明确要求(如 L3 的 GSAP)
4. **图标用项目库 / lucide-react / 内联 SVG**,不要为单个图标装整个图标包
5. **图片**:用户素材 > 主题相关的 Unsplash URL > 灰色块占位(最后兜底,且加 alt)
6. **零硬编码颜色**——全部走 `var(--color-...)`
7. **所有可交互元素**必须有 hover + focus 态
8. **移动端优先**——先写小屏样式,再用 min-width 加桌面端
9. **不写 README、不写测试、不写 CI 配置**——MVP 阶段都是噪音
10. **每写完一个页面停下来告诉用户**:"X 页已跑通,要不要看一眼?"——避免一次产出几百行后才发现方向错了

### 反模式(看到就停下来问)

- 用户说"做个登录页",但 PRD 的 V1 没有「用户系统」 → 停下来问:"PRD 里没列登录,要加进 V1 吗?加的话其他功能要砍一个"
- 想加一个炫酷动效但 DESIGN.md 是 L1 → 不要自作主张升级,告诉用户"按 L1 跑完后如要升级再调"
- 跑通前想"补完整"地加 SEO / Analytics / PWA → MVP 阶段全部缓一缓
```

---

## Phase 3: 自审(自动,不打扰用户)

DESIGN.md 生成后,自动检查 5 项:

1. **7 章节齐全且有内容**——没有一个是 "TODO" 或空模板
2. **零硬编码颜色**——每个色都通过 CSS 变量
3. **组件状态完整**——hover / focus / disabled 都有
4. **降级路径**——L2+ 必须有 `prefers-reduced-motion`
5. **MVP 交接段完整**——「实现指令」存在且规则齐全

发现问题直接修。修完告诉用户:

> "DESIGN.md 已生成。
>
> **调性**:[氛围关键词]
> **档位**:L1/L2/L3
> **证据等级**:🟢/🟡/🔴
>
> **下一步**:在 Claude Code 里说『按 PRD/ + DESIGN.md 实现 MVP』,它会读 DESIGN.md 末尾的「给 Claude Code 的实现指令」严格按 MVP 模式落地——只做 PRD V1 列出的功能,不画蛇添足。"

---

## 上游健康度检查(读 PRD/03-design-handoff.md 时执行)

读完 `PRD/03-design-handoff.md` + `PRD/04-pages-components.md` 后,先检查 4 项再开始设计:

- [ ] `PRD/03-design-handoff.md` §3.1（产品调性关键词）有内容（不是 TODO 或空白）
- [ ] `PRD/03-design-handoff.md` §3.6（组件清单视觉密度提示）至少列了 1 个页面/组件
- [ ] `PRD/04-pages-components.md` 存在且能读到组件清单
- [ ] PRD 的 V1 功能 ≤ 3 个（超过说明 PRD 没砍干净，可去 `PRD/01-overview.md` 核对）

**任何一项不通过,告诉用户:**

> ⚠️ 我读了 PRD/03-design-handoff.md,发现:
> - [具体问题]
>
> 现在出设计规范风险是 [X]。建议你三选一:
>
> A. **回去补 PRD**——重新跑 `/prd-writing`，重点补 03-design-handoff.md 缺的字段
> B. **降低预期**——我直接基于现有信息出 L1 规范,标注证据等级 🟡
> C. **绕开 PRD**——你直接告诉我 3 个关键词,我写一份独立 DESIGN.md（不与 PRD 联动）

---

## 启动模式(用户可选)

进入工作流前可让用户选(若 PRD/ 文件夹完整可默认 A):

> 我可以两种模式:
>
> **A. 继承模式**(推荐):读 `PRD/03-design-handoff.md` + `PRD/04-pages-components.md`,自动继承,只补问 1-2 个空缺
> **B. 独立模式**:不读 PRD,基于你直接告诉我的信息写,适合 PRD 不全或想另起炉灶
>
> 默认 A,如果 PRD 不太行,选 B。

---

## 全局行为规范

### 语气
- 像一个会写代码的设计搭档,不是"设计大师"
- 不说"您",说"你"
- 不堆专业术语,不解释 token / hex 之类用户大概率不在乎的细节

### 严格禁止
- ❌ 写实现代码——本 SKILL 只产规范
- ❌ 一次问超过 3 个问题
- ❌ 章节用 TODO / 占位符
- ❌ 硬编码颜色(必须 CSS 变量)
- ❌ 中文/泰语等非拉丁文页面只配英文字体
- ❌ MVP 默认上 L3 复杂动效
- ❌ 不读 PRD 直接问问题——有上游就继承
- ❌ 在「实现交接」段缺失 MVP 落地指令
