---
name: style-fix
description: 修复 CSS、Tailwind CSS、CSS Module、Ant Design 样式覆盖、className、主题 token、布局和视觉样式问题。用户提到样式问题、CSS 报错、Missing comma、选择器、@apply、Tailwind v4 canonical class、颜色、间距、圆角、表格样式、AntD 覆盖，或功能改动触碰样式代码时使用。
---

# Style Fix

最小范围修正样式写法。只处理 CSS、Tailwind、CSS Module、Ant Design 覆盖、className 和主题 token；不重构业务逻辑、不重新设计 UI、不顺手做类型治理。

```text
输入 -> 识别范围 -> 只读审查 -> 分级 -> 修改必须修复项 -> 最小验证 -> 汇报
```

## 读取与范围

先读：

1. `AGENTS.md`：确认高风险文件、联动规则和项目边界。
2. 当前仓库实际存在的样式入口、Tailwind 版本、格式化配置和 lint 配置；路径不存在时不要沿用历史路径。
3. 功能名范围涉及的模块文档和路由配置，例如 `docs/modules/module-map.md`、`docs/modules/`、`src/config/router.config.ts`、`src/router/routers.ts`。
4. 颜色、阴影、动画、尺寸、主题类或 Ant Design 覆盖相关入口，例如 `src/styles/global.css`、`src/styles/theme-config.css`、`src/styles/theme.css`、`src/styles/custom-antd.css`、`src/components/StyleProviderClient.tsx`。
5. 当前安装的 `antd` 类型定义或源码；只在需要判断 `classNames` / `styles` 槽位时读取。

只使用已在当前代码或样式入口中确认存在的 token / utility，不凭记忆猜 token 名。

```text
用户输入
  +-- 目录/文件 -> 只处理该路径下样式相关内容
  +-- 功能名   -> 走“功能模块定位”
  +-- 暂存区   -> git diff --cached --name-only --diff-filter=ACMR
  +-- 无范围   -> 询问目录、功能模块、文件或暂存区
```

如果用户同时给目录、功能名和“暂存区”，以显式指定范围为准。

### 功能模块定位

```text
功能名
  -> docs/modules/module-map.md、docs/modules/
  -> router.config.ts、routers.ts
  -> 中文名 / 英文名 / 路由片段 / API 名 / i18n key 搜索
  -> 候选清楚：只处理该模块内样式相关文件
  -> 候选过多：列 2~4 个入口和依据；无法判断才追问
```

定位后不要因为同名词出现在其他模块就跨范围修改。

### 暂存区模式

```text
git status --short
  -> 识别 staged / unstaged / 同文件混合状态
  -> git diff --cached --name-only --diff-filter=ACMR
  -> 只审查暂存范围内样式相关文件
  -> 需重新暂存且无混合风险：git add <具体文件>
  -> 同文件混合状态有带入风险：说明风险，让用户决定
```

不要使用 `git add -A` 或 `git add .`。

## 修复门槛

```text
候选问题
  -> 是否违反 AGENTS.md、本 Skill 或当前项目已确认样式规则？
     +-- 否：建议确认或无需处理
     +-- 是：是否能在用户范围内无损修正？
             +-- 是：必须修复
             +-- 否：建议确认或列为未处理
```

| 分类     | 处理                                                                                                                                                                                                            |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 必须修复 | Tailwind v3 写法、Tailwind v4 canonical class、可无损替换的 arbitrary value、已有 token 却使用裸值、应随主题变化却写死固定色、CSS Module 命名不符合约定、无边界 Ant Design 覆盖、增加维护负担的一次性样式抽象。 |
| 建议确认 | 视觉表达重做、历史样式统一、可内联可保留的 className、新增全局 token / 覆盖、会扩大到非本次范围的项。                                                                                                           |
| 无需处理 | 没有必须修复项时，不为体现使用本 Skill 而改 className、搬 CSS Module 或替换视觉写法；只汇报范围和依据。                                                                                                         |

本 Skill 被新功能或旧功能修改顺带触发时，只处理与当前改动直接相关的必须修复项。

## 文件边界

优先关注：

- `*.tsx` / `*.jsx`：`className`、条件类名、CSS Module import、局部 `ConfigProvider`。
- `*.ts`：只服务样式的 `xxxClassName`、`xxxClassNames`、`classNameMap`、组件配置或 className 组合。
- `*.module.css`、`src/styles/*.css`：Tailwind `@apply`、`@reference`、Ant Design 覆盖和主题样式。

默认跳过：

- 业务逻辑、接口、状态、路由注册等非样式改动。
- 生成文件、依赖目录、构建产物和第三方源码。
- 与本次范围无关的历史 `style.module.css` 大迁移。

## 修改规则

### className 与样式常量

```text
样式写法
  +-- 单次使用/简单静态样式 -> 直接写 JSX className
  +-- 条件组合              -> 用现有 cn / clsx / classnames 在 className 中组合
  +-- 三次以上复用/稳定语义/第三方配置限制/复杂条件
                              -> 保留样式常量，命名表达稳定语义
```

不要为了缩短字符串保留只使用一次或简单组合的样式变量；一次性组合样式不要再抽一层变量。

### Tailwind 与主题 token

```text
待处理值或 class
  +-- 已有 token / utility -> 改为 token utility
  +-- Tailwind v3/旧写法  -> 改为 v4 canonical class
  +-- arbitrary value
        +-- spacing/字号/行高/圆角可无损表达 -> 改为标准 utility
        +-- calc()/CSS 变量/%/非 4px 整数倍/运行时拼接/第三方约束 -> 保留
```

规则：

- 颜色、背景、边框、填充、描边、占位符和透明度优先转成主题 token utility，例如 `text-brand-wzj6`、`bg-brand-wzj1`、`border-gray-wzj3`、`fill-brand-wzj6`、`bg-brand-wzj6/10`。
- 避免把已有 token 写成裸 hex、`[]` arbitrary value、`text-[var(--xxx)]`、`bg-(--brand-wzj6)` 或 `text-(color:--brand-wzj6)`。
- Tailwind v4 重要性写法使用后缀：`!text-font-wzj1` -> `text-font-wzj1!`，`disabled:!bg-gray-f0` -> `disabled:bg-gray-f0!`。
- `bg-gradient-to-r` -> `bg-linear-to-r`；同宽高优先 `size-*`。
- spacing scale 按 `1 = 4px` 换算，支持 Tailwind 已存在的 0.25 步进；不要只按 4px 整数倍判断。例如 `min-w-[1180px]` -> `min-w-295`、`w-[360px]` -> `w-90`、`max-w-[720px]` -> `max-w-180`、`ml-[5px]` -> `ml-1.25`。
- 默认 token 可无损表达时才替换：`text-[14px]` -> `text-sm`、`text-[16px]` -> `text-base`、`leading-[20px]` -> `leading-5`、`leading-[22px]` -> `leading-5.5`、`rounded-[8px]` -> `rounded-lg`、`rounded-[12px]` -> `rounded-xl`、`rounded-[16px]` -> `rounded-2xl`。
- `rounded-[10px]`、`rounded-[14px]` 这类没有无损等价的写法先保留或列为建议确认，不要近似替换。
- 编辑器 / linter 提示的 canonical class 要一并处理，例如 `break-words` -> `wrap-break-word`，并按项目 class 排序规则调整顺序。

### CSS Module

```text
样式需求
  -> JSX className 是否足够表达？
     +-- 是：不新增 CSS Module
     +-- 否：伪元素/复杂后代选择器/第三方内部结构/@keyframes/打印样式
             -> 保留或新增 CSS Module
             -> 新文件 styles.module.css，导入名 styles
             -> 顶部优先 @reference '#global-css';，声明优先 @apply
```

修改历史 CSS Module 时，只在本次触碰且引用范围清楚时迁移命名。

### Ant Design 覆盖

```text
AntD 样式问题
  -> 全局 ConfigProvider / custom-antd.css / theme.css 是否已有表达？
     +-- 是：复用现有全局配置或 token
     +-- 否：查当前 antd 类型定义或源码确认槽位
             +-- 有 classNames 语义槽位 -> classNames
             +-- 需要运行时值或无稳定语义槽位 -> styles / style
             +-- 需要选择内部结构 -> 父级作用域 + 局部选择器
```

局部覆盖必须有父级作用域，不新增无边界 `:global(.ant-*)`。项目尚未安装 `antd` 时，不新增依赖未确认槽位名的规则。

### Missing comma 与选择器误报

```text
CSS Missing comma / 选择器解析错误
  -> 是否是长后代选择器换行导致工具链兼容问题？
     +-- 是：缩短选择器 / 改直接子级 / 单行表达
     +-- 否：按真实 CSS 语法问题修复
  -> 运行格式化和 git diff --check
```

不要为了消除报错添加无意义逗号；保持原语义。

## 类型处理边界

样式规范调整不承担类型治理职责。

- 不主动新增、迁移、重命名类型文件。
- 不在本 Skill 中决定 `types.ts`、`types.d.ts`、`*.types.ts` 等命名策略；以当前仓库类型规范文档和现有代码为准。
- 样式修正不可避免触碰 Props 或类型声明时，只做与本次样式改动直接相关的最小调整。
- 发现类型定义放置问题但与样式修正无直接关系时，列为未处理项或建议交给类型处理 Skill。

## 示例

| 场景             | 调整前                                                   | 调整后                                            |
| ---------------- | -------------------------------------------------------- | ------------------------------------------------- |
| 主题 token       | `border-[#02A999] bg-[#E8FFF9] text-[var(--brand-wzj6)]` | `border-brand-wzj6 bg-brand-wzj1 text-brand-wzj6` |
| v4 重要性写法    | `!text-font-wzj1 disabled:!bg-gray-f0`                   | `text-font-wzj1! disabled:bg-gray-f0!`            |
| spacing scale    | `min-w-[1180px] w-[360px] max-w-[720px] ml-[5px]`        | `min-w-295 w-90 max-w-180 ml-1.25`                |
| 字号、行高、圆角 | `rounded-[12px] text-[14px] leading-[22px]`              | `rounded-xl text-sm leading-5.5`                  |
| canonical class  | `ml-1 break-words`                                       | `wrap-break-word ml-1`                            |

Ant Design 槽位示例：

```tsx
// 调整前
<Tooltip overlayClassName="text-[var(--font-wzj1)]" />

// 调整后
<Tooltip classNames={{ root: 'text-font-wzj1!' }} />
```

处理前必须查当前安装版本的类型定义或源码。以 Ant Design 5.26.2 的浮层组件为例，`overlayClassName` 对应 `classNames.root`，`overlayStyle` 对应 `styles.root`，`overlayInnerStyle` 对应 `styles.body`；当前安装版本不同，以本地类型和源码为准。

Missing comma 示例：

```css
/* 调整前 */
.wenshu-markdown
  [data-streamdown='table-body']
  [data-streamdown='table-row']:last-child
  [data-streamdown='table-cell'] {
  @apply border-b-0;
}

/* 调整后 */
.wenshu-markdown [data-streamdown='table-body'] > :last-child > [data-streamdown='table-cell'] {
  @apply border-b-0;
}
```

## 不做什么

- 不改业务行为、请求逻辑、权限逻辑或状态结构。
- 不擅自新增局部 `ConfigProvider`。
- 不为少量局部样式新增包装组件或平行组件。
- 不因为发现历史命名不统一而扩大到全仓库迁移。
- 不新增全局 token 或全局 Ant Design 覆盖，除非已有规范无法表达且用户明确同意。
- 不替换图标、不改交互、不把透明、渐变、玻璃态等设计效果扁平化成实色背景。

## 验证

```text
完成改动
  -> git diff --check -- <处理过的文件>
  -> 修改 TS/TSX：运行项目已有 lint 或类型检查中与范围匹配的命令
  -> 修改可见 UI：能运行页面就验证目标页面；不能验证时说明原因
  -> 暂存区模式：再看 git status --short，并说明重新暂存情况
```

不确定项目命令时，建议 `npm run lint` 和 `npm run check-types`。

## 输出格式

```md
## 样式规范调整结果

- 范围：<目录 / 功能模块 / 文件 / Git 暂存区>
- 定位依据：<模块文档 / 路由配置 / 关键词 / 暂存文件列表>
- 已调整：<文件和关键改动>
- 未处理：<有意保留或需要确认的项，没有则写“无”>
- 联动影响：<是否涉及全局主题、Ant Design、路由或 Provider>
- 验证：<已运行命令和结果，或未运行原因>
```
