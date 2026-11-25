---
name: inspecting-hermes-desktop-dom
description: "Read the live Hermes desktop DOM/CSS over CDP."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [desktop, electron, cdp, dom, ui-verification, self-inspection]
    related_skills: [node-inspect-debugger, systematic-debugging, dogfood]
---

# 查看实时的 Hermes 桌面端 DOM

## 概述

在开发 `apps/desktop` 应用且用户正在运行该应用时（通过 `hgui` 或 `npm run dev`），你可以直接读取用户当前查看窗口的**实时渲染 DOM**——包括计算后的样式、几何信息、实际生效的 CSS 规则以及控制台输出——而无需从 `.tsx` 文件中推断，从而避免出错。

开发服务器会自动在 `127.0.0.1:9222` 端口开启 Chrome DevTools Protocol 接口。由于渲染器基于 Chromium 页面，因此 DevTools 能读取的一切内容，脚本也同样可以获取。

**但这并不能替代直接查看。** CDP 能回答*事实性*问题（如“计算后的内边距是多少”、“该元素是否已渲染”、“哪个选择器匹配”）。它无法判断视觉效果是否良好——色彩平衡、间距感受以及“设计是否美观”等问题仍需依靠用户肉眼或截图来判断。用 CDP 回答事实问题，而将审美判断留给用户。

## 适用场景

- 验证 UI 变更是否已在运行的应用中生效
- 当遇到“为什么这个元素的值仍是 X？”的情况时——在修改任何内容之前先找出生效的规则
- 为即将修改的组件寻找稳定的选择器
- 在真实节点上查看设计令牌的计算值
- 读取用户提及但无法复制的渲染器控制台错误信息

**不适用于：** 性能分析或堆内存调试（如 `node-inspect-debugger`、`debugging-hermes-desktop`），以及那些核心问题是“看起来对不对”的场景。

## 端口地址

任何运行中的开发服务器均会在 `127.0.0.1:9222` 端口上开启。仅在以下两种情况下会关闭该端口（位于 `apps/desktop/electron/dev-cdp.ts` 文件中）：

- **已打包的应用**——始终处于关闭状态，且任何环境变量设置都无法改变这一规则；
- **未定义 `HERMES_DESKTOP_DEV_SERVER`**——此时会使用未打包的 `electron .` 版本针对 `dist/` 目录进行测试，因此其行为与已打包应用一致。

`HERMES_DESKTOP_CDP_PORT` 用于指定端口号（默认值为 `9333`）或将其禁用（设置为 `off`）。

在执行其他操作之前，请先确认以上设置。

```bash
curl -s --max-time 3 http://127.0.0.1:${HERMES_DESKTOP_CDP_PORT:-9222}/json/version
```

为空 → 无端口。切勿擅自猜测其他端口。

**绝不要通过重启用户的应用程序来获取端口**，这会破坏用户的会话及状态。应改为启动您自己的独立实例（见下文）。

## 读取 DOM

`apps/desktop/scripts/eval.mjs` 即为相关的一行代码：

```bash
cd apps/desktop
node scripts/eval.mjs "document.querySelectorAll('[data-slot]').length"
```

对于多步骤任务，请使用共享客户端——它具备目标发现功能以及基于承诺值的评估机制。

```js
import { CDP, SELECTORS } from './scripts/perf/lib/cdp.mjs'

const cdp = await CDP.connect({ port: 9222, match: '5174' })
const out = await cdp.eval(`JSON.stringify({
  radius: getComputedStyle(document.documentElement).getPropertyValue('--radius-scalar').trim(),
  composer: !!document.querySelector('[data-slot="composer-rich-input"]')
})`)
cdp.close()
```

`scripts/perf/lib/cdp.mjs` 文件中的 `SELECTORS` 定义了稳定的 `data-slot` 钩子（包括 composer、thread viewport、assistant message、turn pair、profile rail 等）。建议优先使用这些预定义的钩子，而非自行编写 `querySelector` —— 当组件位置发生变化时，它们会作为一个整体一同更新。

## 这个方法最适用于判断：哪条规则生效了？
因为样式“没有应用”就逐一修改调用代码，是典型的浪费时间行为。请先查看实际的节点结构：

```js
const el = document.querySelector('[data-slot="aui_assistant-message-root"] a')
JSON.stringify({
  ownClasses: el.className,
  weight: getComputedStyle(el).fontWeight,
  parents: (() => {
    const out = []
    let n = el
    while ((n = n.parentElement) && out.length < 6) out.push(n.className)
    return out
  })()
})
```

如果节点没有自身的样式类，该属性值将会**被继承**——简单的遍历调用方式无法解决此问题，此时就需要使用父级规则。通常情况下，插件样式表（例如 `@tailwindcss/typography` 中的 `prose a { font-weight: 500 }`）会比通用样式类更有效；应直接在共享的样式类上进行覆盖，而无需在每次使用时都重复操作。

## 自有的独立实例

当不存在端口，或者必须避免干扰用户窗口时：

```bash
cd apps/desktop
HERMES_HOME=/tmp/cdp-probe-home \
HERMES_DESKTOP_DEV_SERVER=http://127.0.0.1:5174 \
HERMES_DESKTOP_CDP_PORT=9333 \
  npx electron . --user-data-dir=/tmp/cdp-probe-userdata
```

通过使用独立的 `--user-data-dir` 参数，可以避开 Electron 的单实例锁定机制，从而避免与正在运行的 `hgui` 发生冲突；而独立的 `HERMES_HOME` 设置则能将其与真实会话隔离开来。出于同样的原因，选择 9222 号端口之外的端口进行运行，并在任务完成后终止该进程。

如果您同时也需要性能测试工具包，执行 `npm run perf:serve` 即可，该命令会内置一个临时的 `HERMES_HOME` 环境来实现相同的功能。

## 常见问题

- **切勿为“释放资源”而强制关闭用户的开发服务器或应用程序。**在服务运行过程中强行终止进程会破坏 Chromium 的套接字池，进而引发 `ERR_NETWORK_CHANGED` 错误，而该错误往往会被误认为是由你刚刚进行的操作所导致的。
- **临时使用的 `HERMES_HOME` 环境变量不支持后端功能。**应用程序会针对 `hermes:api` 报出 `ECONNREFUSED` 错误，甚至可能自动退出。不过渲染器依然会正常加载，DOM 信息也可读取——请及时获取数据，切勿将应用程序的自动退出误认为是端口故障。当 Chromium 绑定到指定端口时，会在日志中显示 `DevTools listening on ws://127.0.0.1:<port>/…`，这条日志便是端口已打开的证明。
- **应采用轮询方式，而非仅执行一次探测操作。**新启动的应用程序需要一两秒钟的时间，端口才会响应请求。
- **切勿一次性获取整个 DOM 结构。**桌面端应用会渲染数百个节点，使用 `outerHTML` 读取时会淹没你需要的关键信息。建议将数据范围缩小到计算结果中的某个小型 JSON 对象。
- **在调用 `CDP.connect` 时需传入 `match` 参数。**如果不提供该参数，连接可能会被附加到侧边栏、快速入口窗口或开发者工具的目标对象上，而非主窗口。
- **`cdp.eval` 会直接返回计算结果；而原始的 `Runtime.evaluate` 方法则需要通过双重嵌套访问结果（即 `.result.result.value`）。建议使用封装好的方法。**
- **在本项目中的 `vite dev` 模式下，`import.meta.env.DEV` 的值为 `true`**。`apps/desktop/scripts/profile-typing-lag.md` 文件中声称该值为空的说法已经过时。
