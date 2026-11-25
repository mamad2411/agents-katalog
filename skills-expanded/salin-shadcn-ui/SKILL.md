---
name: salin-shadcn-ui
description: 在 React、Next.js、Vite、TanStack、Tailwind 项目中安装、组合、定制或修复 shadcn/ui，并审查 CLI、组件源码、headless primitive、tokens、主题、variants 与组件行为。统一处理 components.json、表单、数据表、应用壳、响应式和无障碍。registry schema、创建与发布改用 shadcn-ui-registry；整体产品体验审查改用 salin-ui-quality-audit；与 shadcn 无关的普通 UI 方向改用 salin-product-ui-builder。
---

# Salin shadcn/ui

shadcn/ui 是“把组件源码带进项目”，不是一个不可修改的黑盒依赖。优先理解项目现状、沿用别名与 tokens，再用 CLI 获取基础组件，并把产品特定组合保留在功能层。

## 任务路由

| 任务 | 必读参考 |
|---|---|
| 初始化、添加、升级或排查组件 | [references/project-and-cli.md](references/project-and-cli.md) |
| 统一主题、颜色、圆角、密度、暗色 | [references/design-system.md](references/design-system.md) |
| 组合表单、数据表、应用壳、弹窗 | [references/component-patterns.md](references/component-patterns.md) |
| 响应式、键盘、焦点、状态与验收 | [references/accessibility-and-qa.md](references/accessibility-and-qa.md) |

创建或维护自定义 shadcn registry、registry item、schema 或分发源时，使用独立的 `shadcn-ui-registry`；消费端的预览、差异、本地源码保护和页面集成仍由当前 skill 负责。当前 skill 是 `shadcn-ui-builder`、`shadcn-ui-design-system` 与 shadcn/Tailwind 日常规则的合并替代入口；安装本合并版时不要同时把旧两项作为主入口。

审查按对象分流：CLI、底层 primitive、组件源码、tokens、主题和 Dialog/Popover 等组件行为由当前 skill 主责；整体流程、反模板化、跨页面一致性、通用无障碍和上线质量由 `salin-ui-quality-audit` 主责。

## 核心流程

1. **检查项目**：读 README、AGENTS/CLAUDE、Git 状态、package、锁文件、框架、Tailwind 版本、`components.json`、全局 CSS、路径别名、RTL 设置、实际 headless primitive 底座和现有 `components/ui`。通过当前 CLI 的 info/help 能力与源码 imports 交叉确认，不猜测。
2. **判断状态**：区分未初始化、已初始化、组件缺失、组件被本地修改、主题漂移或纯组合问题。
3. **先预览风险**：添加或更新组件前查看 CLI 帮助/差异；禁止在未审查的情况下覆盖项目已定制源码。
4. **获取基础组件**：使用项目包管理器和 shadcn CLI；保持现有 style、component base、base color、CSS variables、aliases 与 RSC 设置。已有项目禁止隐式迁移 Base UI、Radix 或 React Aria 等底层实现。
5. **按现有主题模式工作**：`cssVariables: true` 时维护 background、foreground、primary、muted、destructive、border 等语义 tokens 和亮暗配对；`false` 时沿用内联 utilities。只有用户明确要求主题迁移时才评估切换成本。
6. **组合产品界面**：通用原子留在 `components/ui`；业务表单、表格工具栏、页面壳和领域组合放到功能目录。
7. **补全状态与响应式**：覆盖键盘、焦点、触摸、加载、空、错误、禁用、长内容、窄屏与暗色。
8. **验证真实项目**：运行类型、lint、测试、构建和浏览器关键流程；检查控制台、hydration、主题闪烁与移动端。

## 强约束

- 不臆测 CLI 参数、组件路径或 Tailwind 版本；以本地项目与当前 CLI 输出为准。
- 不自动执行覆盖式更新；先确认将修改哪些文件并保留本地定制。
- 不把产品特定样式塞进通用 Button/Input；只有多处复用且语义稳定时才增加 variant。
- 不硬编码颜色替代语义 token，不混用 HSL、RGB、OKLCH 等颜色表示法。
- 不使用动态拼接的 Tailwind 类名；使用完整类名映射、`cn()` 和清晰 variants。
- 不用 div 伪造按钮、链接、复选框或对话框；保留项目当前 headless primitive 底座提供的语义、焦点、键盘与 Portal 行为。
- 触发器、Dialog、Sheet、Popover、DropdownMenu 的组合必须保留焦点管理、Escape 和可访问名称。
- 只需要产品设计方向时不要初始化 shadcn；先使用 `salin-product-ui-builder`。

## 输出契约

实现前简要说明：

```markdown
## shadcn 实施方案
- 项目状态：框架 / Tailwind / components.json / 包管理器 / component base / cssVariables / RTL
- 复用内容：现有组件 / tokens / 别名 / 主题
- 组件变化：新增 / 组合 / 修改 / 明确不覆盖
- 主题变化：语义 token / 亮暗色 / 圆角 / 密度
- 状态与响应式：键盘 / 触摸 / 移动 / 加载 / 空 / 错误
- 验证：类型 / lint / 测试 / 构建 / 浏览器
```

只做咨询时不运行初始化或安装。实现完成后列出 CLI 操作、修改文件、验证结果、未验证内容和风险。

## 完成前检查

- 是否沿用项目包管理器、路径别名、Tailwind 版本和 `components.json`。
- 是否保护了本地修改，避免无审查覆盖。
- tokens 是否语义化、亮暗成对且对比度足够。
- 业务组合是否与通用 `components/ui` 分层。
- 表单、浮层、数据表和应用壳是否有完整状态与移动端行为。
- 是否在真实浏览器检查主题、键盘、触摸和控制台错误。
