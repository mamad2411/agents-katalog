---
name: hermes-desktop-plugins
description: Write desktop app plugins that add UI panes and commands.
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [desktop, plugins, ui, extension]
    category: productivity
    related_skills: []
---

# Hermes 桌面端插件技能

为 Hermes 桌面应用编写插件：状态栏项目、布局面板、命令面板命令、键绑定、路由以及主题。插件是一个纯 JavaScript ESM 文件，可在运行时被应用加载——无需构建步骤，也无需修改代码仓库。插件还可以与其自身的 Python 后端命名空间进行通信（通过 `ctx.rest`/`ctx.socket` 访问 `/api/plugins/<id>`）；而通用的 Python 插件系统（位于 `~/.hermes/plugins/`）则有单独的文档说明。

完整参考资料（包括所有导出项、区域载荷、后端及安全相关内容）：  
`website/docs/developer-guide/desktop-plugin-sdk.md`。

## 适用场景

- 用户希望添加新的桌面 UI 元素（如面板、状态栏控件、仪表板或命令），但不想修改应用本身。
- 您希望将通过网关 RPC 计算得到的数据展示在应用内部。

## 先决条件

- Hermes 桌面应用（它能加载插件，而仅 CLI 或网关无法做到）。
- 对 `$HERMES_HOME/desktop-plugins/` 目录的写入权限（通常为 `~/.hermes/desktop-plugins/`）。

## 运行步骤

1. 根据本技能目录下的 `templates/plugin.js` 文件创建 `$HERMES_HOME/desktop-plugins/<name>/plugin.js` 文件——默认路径为 `~/.hermes/...`，若使用了命名配置文件，则路径为 `~/.hermes/profiles/<profile>/...`。请确保 `<name>` 与插件 ID 相同。
2. 桌面应用会持续监控该目录：文件保存后几秒内插件就会加载，后续的保存操作会实现热重载，无需手动重新加载。（若插件未出现，可按 ⌘K 调用 **Reload desktop plugins** 重新加载。）
3. 若加载失败，应用会显示包含错误信息的提示框——请修复文件后再次保存。

## 快速参考

唯一需要导入的模块是 `@hermes/plugin-sdk`（此外还有 `react` / `react/jsx-runtime`，它们实际上指向应用自带的 React 实现——应使用 `jsx()` 函数编写 UI，而非 JSX 语法；该文件不会被编译）。

- `host.state.*` —— 只读的反应式原子：`activeSessionId`、`cwd`、`gateway`、`model`、`profile`、`viewport`。在处理函数中可通过 `.get()` 读取，在组件中可通过 `useValue(atom)` 读取。
- `host.request(method, params)` —— 用于调用网关的 JSON-RPC 接口（支持会话、配置、技能、定时任务等应用所需的所有功能）。
- `host.onEvent(type, fn)` —— 监听网关实时事件（使用 `'*'` 可监听所有事件）。该方法会返回一个销毁函数。
- `host.notify({ kind, message })`、`host.navigate(path)`、`host.logs()`、`host.status()`、`haptic('tap')`。
- `ctx.register({ id, area, order?, render?, data? })` —— 用于添加 UI 元素。常用区域包括：`'statusBar.right'`/`'statusBar.left'`（用于显示芯片状图标）、`'panes'`（布局区域——可设置 `title` 以及 `data: { placement, dock?, width?, height? }`；面板会自动加入对应的区域）、`PALETTE_AREA`（用于 ⌘K 命令）、`KEYBINDS_AREA`（用于重新绑定操作）。
- 面板放置方式：`placement: 'left'|'right'|'bottom'|'main'` 表示语义角色——面板会与该角色下的其他面板堆叠（类似标签页）。若希望面板固定在特定边缘，可添加 `dock: { pane, pos }` 参数——其操作方式与将元素拖放到面板的放置芯片上相同。`pane` 可以是任何面板 ID（如 `workspace` 表示主线程，还有 `sessions`、`terminal`、`files`、`review`、`logs` 等）；`pos` 的取值为 `'top'|'bottom'|'left'|'right'|'center'`。例如，“放在对话内容下方”可表示为 `dock: { pane: 'workspace', pos: 'bottom' }`，同时还需指定高度（如 `'200px'`），以避免占据整个区域的一半空间。
- 完整页面：可通过注册 `area: ROUTES_AREA` 并设置 `data: { path: '/my-page' }` 以及对应的渲染函数来创建页面——该页面会像内置视图一样显示在主工作区面板中。若希望通过侧边栏导航访问该页面，可执行如下操作：`ctx.register({ id: 'nav', area: SIDEBAR_NAV_AREA, data: { path: '/my-page', label: '我的页面', codicon: 'project' } })`（该元素会显示在“Artifacts”下方，并在对应路由激活时高亮显示）——或者通过 `PALETTE_AREA` 中的命令调用 `host.navigate('/my-page')`。
- `ctx.storage.get/set/remove` —— 用于实现插件自身的持久化存储。
- `ctx.i18n.register({ en, ja, ... })` —— 允许您上传属于自己的本地化语言包，这些语言包仅对当前插件生效（切勿修改核心的 `en.ts` 文件）。语言值可以是字符串或插值函数；嵌套结构可通过点号路径访问。在组件中可使用 `usePluginI18n(id)` 函数以反应式方式读取这些值，该函数会返回 `t('key', ...args)` 的形式（当语言切换时组件会重新渲染），或在处理函数/存储模块中使用 `ctx.i18n.t` 函数。解析顺序为：先根据应用当前激活的语言查找，若未找到则依次查找您定义的 `en` 语言包，最后才是原始键值。
- 数据处理：可使用 `useQuery`/`useMutation`/`useQueryClient`/`queryClient`（这是应用唯一的 React Query 客户端——具备缓存、去重、`refetchInterval` 设置以及与核心功能相同的无效化功能；切勿自行实现轮询逻辑），此外还可使用 `atom`/`computed` 函数来管理插件内部的本地状态。
- 后端通信：如果插件包含了 Python 文件 `plugin_api.py`（位于 `~/.hermes/plugins/<id>/dashboard/` 目录下，且文件中声明了 `"api": "plugin_api.py"`），则可通过 `ctx.rest('/path', { method?, body?, timeoutMs? })` 调用该接口，以及通过 `ctx.socket('/events', onMessage)` 调用其实时事件接口——这两者均被限制在 `/api/plugins/<id>` 路径下，无法跨路径访问。在基于 OAuth 的远程环境中，`ctx.socket` 为无操作函数，因此务必保留轮询作为备用方案。只有当插件被列入 `config.yaml` 文件中的 `plugins.enabled` 列表时，才会加载对应的 Python 后端（此设置与应用内的开关功能是独立的）。若需要访问全网关范围的数据，则应使用 `host.request` / `host.onEvent`。
- `Contribute`（挂载级功能）：在组件内部使用 `jsx(Contribute, { area, id, children })` 语法，这样当页面被卸载时，属于该页面的 UI 元素（例如位于 `TITLEBAR_AREAS.center` 区域的标题栏控件）也会随之消失——而 `ctx.register` 用于创建永久性的 UI 元素。
- 若在默认导出处设置 `defaultEnabled: false`，则表示该插件为可选启用类型：它会在“设置 → 插件”页面中列出，用户需手动开启才能使用。
- 用户可在“设置 → 插件”页面管理插件（启用/禁用实时功能以及显示对应文件夹）。已被禁用的插件在重启后仍会保持禁用状态——无需强行启用，因为是用户主动关闭的。
- UI 组件：应用提供了统一的设计语言，可直接导入使用，包括 `Button`、`Input`、`Textarea`、`Select*`、`Switch`、`Checkbox`、`SegmentedControl`、`Tabs*`、`Dialog*`、`ConfirmDialog`、`DropdownMenu*`、`ContextMenu*`、`Popover*`、`Tip`/`Tooltip*`、`Badge`、`Kbd`/`KbdGroup`、`SearchField`、`ScrollArea`、`Separator`、`Skeleton`、`GlyphSpinner`、`EmptyState`、`ErrorState`、`CopyButton`、`StatusDot`、`LogView`、`Codicon`、`DecodeText`，此外还有 `cn` 以及各类 `icons.*` 组件。建议优先使用这些预定义组件，而非自行编写元素，这样插件才能保持原生外观；样式应通过主题变量设置，切勿硬编码颜色值。

## 实施步骤

1. 选择一个简短的 kebab-case 格式的 ID，文件夹名称必须与之一致。
2. 以 `templates/plugin.js` 为模板，保持其默认导出结构（即 `{ id, name, register(ctx) }`）。
3. 若要创建面板，需注册 `area: 'panes'`，并指定放置位置以及返回对应组件的渲染函数——应用会自动将该面板放入合适的区域，之后用户可自由拖动面板。
4. 使用 `host.request` 获取数据，或使用 `host.onEvent` 订阅事件；切勿频繁轮询，间隔应至少几秒。
5. 使用文件编辑工具完成文件编写后，让用户按 ⌘K 调用 **Reload desktop plugins** 重新加载插件。

## 常见问题与注意事项

- 绝对不要硬编码颜色或背景色值（如 `#000`、`black`、`rgb(...)`）。面板本身已位于应用的编辑器背景之上，无需更改背景色，其他所有元素都应使用主题变量来设置，例如 `var(--ui-text-secondary)`、`var(--ui-text-quaternary)`、`var(--ui-stroke-secondary)`、`var(--ui-accent)`。若需要在画布上绘制，可先通过 `getComputedStyle(canvas).getPropertyValue('--ui-accent')` 获取对应的颜色值。
- 仅能使用已导入的组件——若遗漏了某个组件的导入（例如 `StatusDot`），则在渲染时会触发 `ReferenceError` 错误。请仔细检查 `jsx()` 函数中的所有标识符是否都已出现在导入语句中。
- 画布面板必须通过 `ResizeObserver` 监听其容器尺寸变化，并动态调整画布的宽高属性（而非仅依赖 CSS），因为面板会不断因用户操作而改变大小（如拖动边框、切换布局）；仅在初始化时设置一次尺寸会导致空白区域或模糊的缩放效果。
- JSX 语法不会被解析，因此文件会以未编译的形式加载。应使用 `react/jsx-runtime` 提供的 `jsx('div', { children: ... })` 函数来编写代码。
- 除 `@hermes/plugin-sdk`、`react` 以及 `react/jsx-runtime` 外，切勿导入其他任何模块；否则会导致解析失败。
- 处理函数必须以命令式方式读取状态（通过 `$atom.get()`），绝不能从渲染闭包中读取状态——否则在快速连续触发事件时可能会获取到过时的数据。
- 组件应保持简洁，仅在真正需要使用该值的组件中调用 `useValue` 进行订阅。

## 验证方法

- 执行 **Reload desktop plugins** 后，插件的 UI 元素应正常显示。
- 不会出现任何错误提示（如“插件 <name> 加载失败”）；如果出现错误提示，会明确指出故障原因——请修复问题后再次重新加载。
- 对于面板而言，新的区域应能够像普通核心面板一样被看到且可拖动。
