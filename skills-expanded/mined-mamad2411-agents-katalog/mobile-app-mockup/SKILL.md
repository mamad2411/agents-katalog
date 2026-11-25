---
name: mobile-app-mockup
description: 从 PRD 文档或产品描述自动生成高保真移动端 App 原型 HTML 页面。Use when the user provides a PRD, product requirements doc, feature description, or app idea and wants to generate high-fidelity mobile app prototypes, create UI mockups, visualize product features as mobile screens, or build interactive HTML prototypes. Also triggers on "原型图", "高保真原型", "mockup", "app prototype", "UI 设计稿", "手机界面", "移动端原型", or when user pastes product requirements and asks for visual output. Covers the full pipeline — UX analysis, interface planning, UI design, HTML implementation with iPhone 15 Pro device frames.
---

# 移动端 App 高保真原型生成

从 PRD 文档或产品描述出发，经过用户体验分析、界面规划、UI 设计，最终生成一套可在浏览器中直接查看的高保真移动端 HTML 原型。

## 核心原则

- **结构化渐进**：必须按顺序完成四个阶段（分析→规划→设计→实现），每个阶段的输出作为下一阶段的输入。
- **真实感优先**：所有原型必须模拟真实 iOS App 体验。使用真实图片、iOS 风格组件、iPhone 15 Pro 尺寸和圆角边框。
- **独立可运行**：每个页面是独立的 HTML 文件，可在浏览器中单独打开；index.html 通过 iframe 统一展示所有页面。
- **以 App 设计规范为准**：遵循 iOS 原生设计语言，包括 SF 风格字体层级、iOS 标准的间距和圆角、系统级交互模式。

## 工作流程

### 阶段一：读取并理解 PRD

根据用户输入方式获取 PRD 内容：

- 用户提供文件路径 → 读取该文件
- 用户直接粘贴文本 → 直接使用
- 用户给出产品名称和简要描述 → 据此展开分析

从 PRD 中提取以下关键信息，并在后续分析中明确列出：

1. **产品名称与定位**：一句话描述产品是什么、为谁解决什么问题
2. **目标用户**：主要用户角色及其特征
3. **核心功能列表**：按优先级排列（P0 必须有，P1 锦上添花）
4. **关键用户场景**：用户使用这个 App 完成什么任务
5. **数据实体**：涉及的核心数据对象及其关系

### 阶段二：用户体验分析

基于 PRD 分析，输出用户体验分析报告：

**用户核心任务**：
- 列出用户使用 App 要完成的 2-4 个核心任务
- 每个任务对应一条关键用户路径

**关键用户路径**：
- 用步骤序列描述每条路径（如：打开 App → 浏览列表 → 点击详情 → 下单 → 支付）
- 标注每个步骤所在的页面

**页面跳转关系**：
- 以文字描述页面之间的导航关系
- 区分 Tab 主页面（一级）和详情/子页面（二级/三级）
- 标注页面间数据传递关系（如：列表页传递 id → 详情页）

**核心交互元素**：
- 每个页面的关键操作按钮、输入区域、可点击元素

### 阶段三：产品界面规划

作为产品经理，定义所有关键界面：

**页面清单**：
列出所有需要创建的页面，包含：
- 页面名称（中文 + 英文文件名）
- 页面类型（Tab 主页 / 二级页面 / 弹窗/模态）
- 页面核心内容和功能

通常需要 4-8 个页面，覆盖核心用户路径。

**Tab Bar 配置**：
- 定义底部 Tab 数量和图标（使用 FontAwesome 图标名）
- 常见配置：3-5 个 tab，每个 tab 对应一个主要功能入口
- 示例：首页(home) + 发现(compass) + 消息(comment) + 我的(user)

**信息架构**：
- 用缩进文本表示页面层级：
  ```
  Tab: 首页
    ├── 搜索页
    ├── 详情页
    │   └── 下单页
    └── 通知页
  Tab: 我的
    ├── 设置页
    └── 编辑资料页
  ```

### 阶段四：高保真 UI 设计

为整个 App 定义统一的设计规格：

**配色方案**：
```css
--color-primary: #主色调（用于按钮、选中状态、关键交互元素）;
--color-primary-light: #主色调浅色变体（背景、卡片）;
--color-secondary: #辅助色（用于次要按钮、标签）;
--color-bg: #F2F2F7（iOS 标准背景灰）;
--color-card: #FFFFFF（卡片白）;
--color-text-primary: #000000;
--color-text-secondary: #8E8E93;
--color-text-tertiary: #C7C7CC;
--color-separator: #E5E5EA;
--color-danger: #FF3B30;
--color-success: #34C759;
```

主色调需根据产品调性选择：电商类用暖色（橙/红）、工具类用蓝/青、社交类用紫/蓝、健康类用绿、金融类用深蓝。

**字体层级**（模拟 iOS SF 字体）：
| 用途 | 字号 | 字重 | 行高 |
|------|------|------|------|
| 大标题 | 34px | 700 | 41px |
| 标题1 | 28px | 700 | 34px |
| 标题2 | 22px | 600 | 28px |
| 标题3 | 20px | 600 | 25px |
| 正文 | 17px | 400 | 22px |
| 副文本 | 15px | 400 | 20px |
| 辅助文字 | 13px | 400 | 18px |
| 小标签 | 11px | 400 | 13px |

**间距体系**（基于 4px 网格）：
- 页面左右边距：16px
- 卡片圆角：12px
- 按钮圆角：12px
- 卡片之间间距：12px
- 列表项高度：44px（标准点击目标）
- Section 上下间距：24px

**组件样式**：
- **主按钮**：`bg-[--color-primary] text-white rounded-xl h-12 font-semibold text-[17px]`
- **次要按钮**：`bg-transparent border border-[--color-primary] text-[--color-primary] rounded-xl h-12`
- **卡片**：`bg-white rounded-xl shadow-sm p-4`
- **列表项**：`flex items-center h-11 px-4 bg-white border-b border-[--color-separator]`
- **输入框**：`bg-[--color-bg] rounded-lg h-11 px-4 text-[17px]`

### 阶段五：HTML 原型实现

按照以下严格规范生成 HTML 文件。**必须使用 `templates/screen-template.html` 和 `templates/index-template.html` 作为起点**。

#### 文件输出结构

```
output/
├── index.html              # 主入口，iframe 平铺展示所有页面
└── screens/
    ├── home.html           # 首页
    ├── discover.html       # 发现页
    ├── post.html           # 发布页
    ├── messages.html       # 消息页
    ├── profile.html        # 我的/个人中心
    ├── detail.html         # 详情页（按需）
    ├── settings.html       # 设置页（按需）
    └── ...                 # 其他按 PRD 定义的页面
```

#### 每个页面 HTML 文件规范

每个 `screens/*.html` 文件必须是一个完整的、独立可打开的 HTML 文档，包含：

1. **iPhone 15 Pro 模拟容器**（`.iphone-frame`）：
   - 宽度 393px，高度 852px（iPhone 15 Pro 逻辑分辨率）
   - `border-radius: 44px` 模拟设备圆角
   - 黑色边框 `3px solid #1a1a1a` 模拟金属边框
   - `box-shadow` 模拟设备阴影
   - `overflow: hidden` 确保内容不溢出圆角

2. **iOS 状态栏**（`.status-bar`，54px）：
   - 左侧：时间文字 "9:41"
   - 右侧：信号 + 电池图标（用 SVG 或 FontAwesome）
   - 背景色与页面内容协调（浅色页面用白色或浅灰，深色页面用深色背景+白色文字）
   - 动态岛区域留白

3. **页面内容区域**（`.content-area`）：
   - 高度：`852px - 54px(状态栏) - 84px(底部安全区+TabBar) = 714px`
   - `overflow-y: auto` 支持内容滚动
   - 对于 Tab 主页面，内容底部预留 tab bar 空间
   - 对于二级页面（无 tab bar），去掉底部 tab bar，内容高度延伸到 798px

4. **底部 Tab Bar**（`.tab-bar`，仅 Tab 主页面）：
   - 高度 50px + `padding-bottom: 34px`（安全区），总计 84px
   - 半透明背景 `rgba(255,255,255,0.92)` + `backdrop-filter: blur(20px)`
   - 每个 tab：图标（FontAwesome）+ 文字标签（11px）
   - 当前选中 tab 的图标和文字使用主色调，其余用灰色 `#8E8E93`

5. **内容实现要求**：
   - 使用 Tailwind CSS Play CDN：`<script src="https://cdn.tailwindcss.com"></script>`
   - 使用 FontAwesome 6：`<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">`
   - 所有 CSS 变量在 `<style>` 中定义
   - 页面内容要**丰富真实**，包含模拟数据、多张卡片、列表项，而非仅占位符

#### 图片使用规范

**非常重要：不要使用占位符图片。** 每张图片必须来自真实可访问的源。

1. **Unsplash 图片**（用于背景、商品图、内容图）：
   ```
   https://images.unsplash.com/photo-{photo_id}?w={width}&h={height}&fit=crop
   ```
   常用 photo_id 参考：
   - 食物：1504674900247-0877df9cc836, 1546069901-ba9599a7e63c
   - 风景：1506744038136-46273834b3fb, 1469474968028-56623f02e42e
   - 城市：1477959858617-67f85cf4f2df, 1449824913934-46aed80d943b
   - 人物：1535713875002-d1d0cf377fde, 1507003211169-0a1dd7228f2d
   - 产品：1523275335684-37898b5baf30, 1542291026-7eec264c27ff
   - 科技：1518770660439-4636190af475, 1555066931-4365d14bab8c

   根据 App 主题选择合适的图片类别，不要随机使用。例如电商 App 用产品/商品图，旅游 App 用风景图，社交 App 用人物图。

2. **头像图片**：
   使用 UI Avatars API：
   ```
   https://ui-avatars.com/api/?name={姓名}&background=random&size=100
   ```

3. **图标**：
   统一使用 FontAwesome 6 Free 图标，按语义选择：
   - 首页：`fa-house`
   - 搜索：`fa-magnifying-glass`
   - 发布：`fa-plus-square`
   - 通知/消息：`fa-comment` 或 `fa-bell`
   - 用户/我的：`fa-user`
   - 设置：`fa-gear`
   - 返回：`fa-chevron-left`
   - 分享：`fa-share-nodes`
   - 收藏：`fa-heart`
   - 更多：`fa-ellipsis`
   - 位置：`fa-location-dot`
   - 时间：`fa-clock`
   - 电话：`fa-phone`
   - 消息：`fa-envelope`

#### index.html 规范

`index.html` 作为主入口，**不直接写入任何页面的 HTML 内容**，而是：

1. 使用 `iframe` 嵌入每个 `screens/*.html` 文件
2. 所有页面**平铺展示**在 index 页面中（不是链接跳转）
3. 采用响应式网格布局（根据屏幕宽度自动排列）
4. 每个 iframe 外层包裹 iPhone 设备容器，形成设备展示墙

具体实现参考 `templates/index-template.html`。

## 质量检查清单

完成所有页面生成后，逐项确认：

- [ ] 所有页面文件已生成，可在浏览器中独立打开
- [ ] index.html 可正确加载并展示所有页面
- [ ] 每个页面使用 iPhone 15 Pro 尺寸（393x852）
- [ ] 设备圆角（44px）和阴影正确显示
- [ ] iOS 状态栏（时间、信号、电池）在每个页面顶部
- [ ] 底部 Tab Bar 仅在 Tab 主页面显示
- [ ] 所有图片来自真实的 Unsplash/UI Avatars URL，无灰色占位符
- [ ] 配色方案统一，主色调在全局一致使用
- [ ] 字体层级遵循规范（标题/正文/辅助文字大小正确）
- [ ] Tailwind CSS 和 FontAwesome 正确加载
- [ ] 每个页面有充足的模拟数据，看起来像真实的 App 截图
- [ ] 页面内容支持滚动（内容超出可视区域时可滚动）
- [ ] 没有未定义的 CSS 类或变量
- [ ] iframe 尺寸与设备尺寸匹配

## 参考资源

| 文件 | 何时查阅 |
|------|----------|
| `templates/screen-template.html` | 生成每个页面 HTML 时，以此为代码骨架 |
| `templates/index-template.html` | 生成 index.html 时，以此为代码骨架 |
| `references/ios-design-guidelines.md` | 需要确认 iOS 设计规范细节时 |
