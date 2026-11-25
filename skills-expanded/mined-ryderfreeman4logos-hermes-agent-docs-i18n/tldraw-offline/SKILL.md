---
name: tldraw-offline
description: Drive and script tldraw offline canvases with an agent.
version: 1.0.0
author: Teknium + Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [tldraw, canvas, whiteboard, document-script, diagramming]
    category: creative
    related_skills: []
---

# tldraw offline 技能

该技能适用于与 tldraw offline 桌面应用（offline.tldraw.com）配合使用：读取已打开的画布、进行编辑，以及编写**文档脚本**——即嵌入在 `.tldraw` 文件中的 JavaScript 代码，这类代码会在文件加载时被执行，从而为文件赋予持久化功能。该应用会运行一个**本地 HTTP API**（默认地址为 `localhost:7236`），编程智能体可通过终端使用简单的 `curl` 命令来调用该 API——这正是该应用官网演示功能（实时编辑画布）的实现方式。智能体不会使用鼠标操作或 GUI 点击功能，也不会直接手动编辑 `.tldraw` 文件。在工作时请保持 tldraw offline 应用处于打开状态。

## 适用场景

- 用户已打开 tldraw offline 并要求你创建或修改画布内容（如图表、线框图、布局等）。
- 你希望通过嵌入的文档脚本为绘图内容添加持久化功能（如动态形状、交互式按钮、动画效果、连接逻辑等）。

请勿通过手动绘制形状来模拟绘图结果——应编写生成这些形状的代码。相比直接在画布上绘图，智能体在编写画布相关脚本方面表现更为出色。

## 先决条件

- **tldraw offline 已安装并正在运行，且当前有文档打开**。相关版本链接：
  https://github.com/tldraw/tldraw-offline/releases/latest（提供 macOS DMG 格式、Windows x64/Arm64 版本、Linux `x86_64`/`arm64` AppImage 格式以及 amd64/arm64 `.deb` 包）。
- **在应用中安装 Agent Skills**：可通过“开发 → 安装 Agent Skills”来完成。该应用会将自身的 tldraw 相关技能文件保存到 `~/.codex/skills/`、`~/.claude/skills/`、`~/.cursor/skills/` 和 `~/.gemini/skills/` 目录中，从而向对应 Agent 教授下述的 `curl` 命令用法。（此 Hermes Skill 的实现方式遵循 Hermes 的相关指导。）
- **本地控制 API**：应用启动时会将其配置目录（Linux 下为 `~/.config/tldraw/`，macOS 下为 `~/Library/Application Support/tldraw/`，Windows 下为 `%APPDATA%\tldraw\`）中的 `server.json` 文件写入端口信息（默认为 7236）、Bearer 令牌、进程 ID 以及启动时间。除 `GET /` 请求外，所有其他请求都需要在请求头中添加 `Authorization: Bearer <token>`。若正常退出，该文件会被删除；若文件存在但对应端口无响应，则表示应用已非正常退出，可视为未处于运行状态。
- **每次终端调用时都需重新读取端口和令牌**：由于每次打开终端都会启动一个新的 shell 环境，因此通过 `export` 设置的令牌不会持久保留——若尝试“仅设置一次后重复使用”，将会发送空令牌从而导致 401 错误。因此应在每次调用时直接在命令开头读取这些值：`PORT=$(jq -r .port <server.json>); TOKEN=$(jq -r .token <server.json>)`。
- 进行本地编辑无需账号或网络连接。

## 运行方式

共有两种不同的工作流程，可根据修改内容是否需要在应用重新加载后依然保留来选择合适的方式。

**A. 单次画布编辑（`/exec`）**——用于布局调整、图形生成以及画面清理。此类操作属于实时编辑，不会保存为脚本：

```bash
BASE=http://localhost:7236
TOKEN=$(python -c "import json;print(json.load(open('$HOME/.config/tldraw/server.json'))['token'])")
# find the focused document id
DOC=$(curl -s "$BASE/api/search" -X POST -H 'content-type: application/json' \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"code":"return (await api.getFocusedDoc()).id"}' | python -c "import sys,json;print(json.load(sys.stdin)['result'])")
# run code with the live `editor` + `helpers` in scope
curl -s "$BASE/api/doc/$DOC/exec" -X POST -H 'content-type: application/json' \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"code":"const {createShapeId,toRichText}=await import(\"tldraw\"); editor.createShape({id:createShapeId(),type:\"geo\",x:0,y:0,props:{geo:\"rectangle\",w:200,h:100,color:\"blue\",fill:\"solid\",richText:toRichText(\"hello\")}}); return editor.getCurrentPageShapes().length"}'
```

**B. 持久化行为（`script/main.js`）**——即那些在页面重新加载后仍需保持有效的响应式/交互式逻辑。只需修改磁盘上的该文件，应用的监视器便会自动应用这些更改：

```bash
# get the live script file path for the doc
curl -s "$BASE/api/doc/$DOC/script-workspace" -X POST \
  -H "Authorization: Bearer $TOKEN"          # -> result.mainJsPath, result.isDefaultScript
# edit result.mainJsPath with read_file / patch / write_file (see scripts/main.js)
# then confirm the watcher applied it:
curl -s "$BASE/api/doc/$DOC/script-status" -H "Authorization: Bearer $TOKEN"
```

可直接使用的文档脚本为 `scripts/main.js`。

## 快速参考

文档脚本的接口规范（已依据应用中打包的 `script-context.d.ts` 进行验证）：

```js
import { createShapeId, toRichText } from 'tldraw'   // primitives: import, not globals

export default function ({ editor, helpers, signal }) {
  editor.run(() => {                                 // batch = one undo step
    helpers.createShapeIfMissing({                   // idempotent furniture
      id: createShapeId('node-1'), type: 'geo', x: 0, y: 0,
      props: { geo: 'rectangle', w: 200, h: 100, richText: toRichText('hi') },
    })
  })

  const stop = editor.store.listen(() => { /* react */ })  // fires the tick AFTER a commit
  signal.addEventListener('abort', () => stop())           // REQUIRED cleanup on rerun/close
}
```

- `ctx.editor` — 实时 `Editor` 对象（提供 `createShape`、`updateShape`、`deleteShapes`、`getCurrentPageShapes`、`getShape`、`getBindingsFromShape`、`zoomToFit`、`on('tick'|'event', fn)` 以及 `run(fn, { history: 'ignore' })` 等方法）。  
- `ctx.helpers` — 包含 `createShapeIfMissing`、`createShapesIfMissing`、`createArrowBetweenShapes(from, to, { arrowheadEnd })`、`translateShapes`、`onShapeTranslate(id, fn, { signal })`、`richTextToPlainText`、`boxShapes`、`getLints` 等实用函数。  
- `ctx.signal` — `AbortSignal` 对象，可用于关联所有监听器及定时任务的清理操作。  
- `config.js`（独立文件）用于注册自定义的形状/工具/组件相关工具函数，并在编辑器初始化前执行；而 `main.js` 则在已初始化的编辑器上运行，并在内容保存时重新执行。

## 交互式用户界面（通过可点击按钮控制状态）

绘制的图形能够像真实应用程序一样运行——这是静态白板所无法实现的。完整示例见 `scripts/counter.js`（包含数字显示以及减号/重置/加号按钮）。

在确认交互功能是否正常之前，请先阅读相关验证说明。该应用的官方指南建议，通过 `/exec` 接口对可点击界面脚本进行验证，即“模拟一次点击并读取一次状态”（通过 `editor.dispatch` 发送指针事件，等待一次状态更新后读取图形的当前状态），而非使用真实鼠标操作。按照这一标准，计数器功能已得到验证：每次点击都会使数值依次变为 `0 → 1 → 2 → 1 → 0`。这里有两点需要注意：
- **该脚本仅会在应用程序的文件监控机制触发时运行。**在 Linux 系统中，该监控机制使用的是 inotify；如果系统的 `fs.inotify.max_user_instances` 参数已达到上限，就会出现“inotify_add_watch ... No space left on device”的错误信息，同时 `script-status` 的显示状态为“state: 'not-watching'”/“hasEntry: false”，此时脚本将永远无法执行。这是操作系统层面的限制，并非脚本本身的缺陷——普通桌面环境不会受到影响。  
- **由于需要通过计算机操作来驱动画布，因此必须采用前台模式而非后台模式进行操作。**cua-driver 的默认“后台”模式在遇到 Electron 的渲染器被遮挡时会导致“background_unavailable”的错误结果——但这只是初始障碍，并非无法解决的瓶颈。cua-driver 会给出“escalation: 'foreground'”的提示；将 `delivery_mode` 设置为“foreground”（并配合使用 `bring_to_front` 参数），即可让通过 X11 XTest 发送的点击指令成功执行——这样既能跳过“运行脚本”的确认对话框，又能直接点击到画布上。Cua 团队已在该版本的 v1.11.0 AppImage（Linux/X11 环境）上验证了这一方法。切勿因为认为“Electron 拒绝模拟点击”而放弃后台模式的尝试，应尝试切换到前台模式。（实际的操作路径仍然是通过 `/exec` 命令，而非直接点击；此说明仅针对基于计算机操作的测试场景。）

```js
export default function ({ editor, helpers, signal }) {
  // 1. Build buttons idempotently; tag each with meta so the handler finds them.
  //    Give buttons a visible label AND a meta.action.
  // 2. Hit-test pointer_down in PAGE coordinates against the button bounds:
  const inside = (b, p) => p.x >= b.x && p.x <= b.x + b.w && p.y >= b.y && p.y <= b.y + b.h
  function onEvent(info) {
    if (!info || info.name !== 'pointer_down') return
    let p = null
    try { if (info.point && editor.screenToPage) p = editor.screenToPage(info.point) } catch {}
    p = p ?? editor.inputs?.currentPagePoint
    if (!p) return
    const hit = editor.getCurrentPageShapes().find(
      (s) => s.meta?.ui === 'button' &&
        inside({ x: s.x, y: s.y, w: s.props.w, h: s.props.h }, p)
    )
    if (hit) runAction(hit.meta.action)   // mutate state; store it in a shape's meta
  }
  editor.on('event', onEvent)
  signal.addEventListener('abort', () => editor.off('event', onEvent))  // REQUIRED
}
```

- 通过 `meta` 字段来定位按钮（或通过 `helpers.richTextToPlainText` 获取可见标签），而非依赖硬编码的坐标。  
- **同一个脚本需同时负责按钮的生成与读取操作。** 如果图形是由某条代码路径生成的（且其 `meta.action: 'inc'`），而处理逻辑又采用另一种规则（如 `meta.action === 'PLUS'`），则点击操作将不会产生任何效果。应当由生成图形的同一脚本来负责读取这些按钮，或者提供空画布让该脚本重新生成按钮——绝不能将不匹配的图形预先存储到文件的数据库中。  
- 将应用状态保存在图形的 `meta` 字段中（例如 `meta.count`），并将其作为图形的 `richText` 标签进行渲染，这样状态就能在保存后依然保留，便于后续验证。  
- **在 `signal` 发生中断时务必解除监听器绑定。** 忽略这一点绝非无关紧要：在下一次保存时，旧的 `onEvent` 监听器会与新监听器一同存在，从而导致每次点击都会触发两次，计数器也会增加2而非1。  
- 对于连续运动效果，可使用 `editor.on('tick', fn)`；而对于带有附属部件的移动锚点，则应使用 `helpers.onShapeTranslate(id, fn, { signal })`。

### 发布可自动运行的脚本型 `.tldraw` 文件  

`.tldraw` 文件实际上是一个包含 `metadata.json`、`session.json`、`db.sqlite`、`assets/` 以及 `script/` 目录的压缩包（仅这些文件可被打包）。若要让脚本在无需出现“此文档包含脚本 → 运行脚本”确认对话框的情况下自动执行，需满足以下条件：

- `metadata.json` 文件必须包含一个 `script` 元数据项，格式为 `{ "sha256": "<digest>" }`，其中该哈希值是通过对每个排序后的 `script/` 路径应用 `sha256` 算法生成的，具体格式为 `` `${path}\0${sha256hex(bytes)}\n` ``。若哈希值不匹配，则视为文件已被篡改而被拒绝。
- 可通过将对应的哈希值添加到 `~/.tldraw/script-trust.json` 文件中来预先信任该哈希值（格式为 `{ "trusted": ["<digest>"] }`，或使用 `$TLDRAW_SCRIPT_TRUST` 作为快捷键）。当 `isScriptTrusted(digest)` 的返回值为真时，应用将跳过用户授权步骤。

## 操作步骤

1. 从 `server.json` 中读取当前的令牌/端口信息。使用 `api.getFocusedDoc()`（或 `api.getDocs()`）函数查找目标文档；如果同时打开了多个文档，则需明确指定目标文档。
2. 若需进行布局或内容生成，可使用 `/exec` 接口；若需实现持久化功能，则应通过 `/script-workspace` 接口来编辑 `script/main.js` 文件。
3. 需确保脚本具有可重复执行性：使用 `helpers.createShapeIfMissing` 函数创建持久化的图形对象，并为这些图形分配稳定的 `createShapeId('name')` 标识符。这样即使脚本在每次加载时都被重新执行，其状态也能保持一致。
4. 应将脚本自身进行的写入操作排除在用户的撤销历史记录之外：可使用 `editor.run(fn, { history: 'ignore' })` 函数来实现（或直接使用已具备此功能的 `helpers.translateShapes` 函数）。
5. 对于实现响应式功能，可使用 `editor.store.listen(cb)` 方法，在接收到 `signal` 中的终止信号时及时停止监听。对于处理用户交互，可使用 `editor.on('event', h)` 方法（例如检测页面坐标下的鼠标按下事件 `pointer_down`）；而对于动画效果，则可使用 `editor.on('tick', h)` 方法。
6. 对于仅包含一个移动锚点及其附属组件的场景，建议优先使用 `helpers.onShapeTranslate(anchorId, fn, { signal })` 方法，而非使用通用的存储监听器——因为通用监听器可能会导致用户的操作陷入反馈循环。

## 图形属性（需符合 tldraw SDK v5 的架构规范）

`editor.createShape` / `createShapeIfMissing` 函数允许传入部分属性（形状相关工具会自动填充默认值）。在为文件快照构建**原始记录**时，以下所有属性均为必填项（可运行 `scripts/validate_shapes.mjs` 进行验证）：

| 形状类型 | 必填属性 |
|---------|----------|
| `note`  | `richText`、`color`、`labelColor`、`size`、`font`、`align`、`verticalAlign`、`growY`、`fontSizeAdjustment`、`url`、`scale`、`textLastEditedBy` |
| `text`  | `richText`、`color`、`size`、`font`、`textAlign`、`w`、`scale`、`autoSize` |
| `frame` | `w`、`h`、`name`、`color` |
| `geo`   | `geo`、`w`、`h`、`color`、`fill`、`richText`（其余属性如虚线/大小等具有默认值） |

`richText` 属性的值必须是 `toRichText('...')` 的形式——纯字符串将被拒绝。`color` 属性为枚举类型，可选值包括：`black grey light-violet violet blue light-blue yellow orange green light-green light-red red white`。`font` 属性也为枚举类型，可选值包括：`draw sans serif mono`。

## 常见问题

- **`store.listen` 会在提交操作后的下一个计时周期触发，而非同步执行。** 如果你在创建形状后立即读取状态，期望监听器已触发，但实际上并未触发。实际测试表明：立即读取时触发次数为 0；等待一个 `setTimeout` 计时周期后触发次数变为 1。这也是应用中说明 `editor.dispatch` 是异步操作的原因——在验证之前需等待一个计时周期。
- **应使用 `ctx` 而非全局变量。** 相关代码的导出形式为 `export default function ({ editor, helpers, signal })`。在文档脚本中并不存在独立的 `editor` 全局变量。`createShapeId` / `toRichText` / `Vec` 等函数来自 `import ... from 'tldraw'` 的导入语句。
- **应使用 `richText` 而非 `text`。** 文本、注释和地理标签需通过 `richText: toRichText(s)` 来处理。  
- **原始记录需要所有属性；而 `createShape` 则不必。** 在应用内部只需传递所需属性；若手动生成 `.tldraw` 快照，则必须包含全部属性（即完整表格结构）。  
- **脚本会在每次加载时重新执行——因此需具备幂等性。** 建议使用带有稳定标识的 `createShapeIfMissing` 函数，否则会导致内容重复并覆盖用户的修改结果。  
- **需在信号触发时进行清理工作。** 对于每一个 `store.listen`、`editor.on` 或 `setInterval` 操作，都应添加 `signal.addEventListener('abort', () => stop())` 代码；该信号会在重新执行之前以及应用关闭时被触发。  
- **应将脚本的写入操作排除在撤销功能之外：** 可通过 `editor.run(fn, { history: 'ignore' })` 实现这一目标。  
- **当窗口被隐藏时，`editor.on('tick')` 会暂停执行**（因为它属于 RAF 循环）；而 `setInterval` 仍会持续触发，但 Electron 会在后台将其频率限制在约每秒一次。  
- **API 需要从 `server.json` 中获取令牌信息**；端口可以不是默认值（`server.listen(0)` 会自动选择合适端口）——务必从文件中读取配置，切勿硬编码 `7236`。  
- **仅允许导入 `tldraw`、`react` 和 `react-dom` 模块——本项目并非 Node 项目。**  

## 验证

- **形状模式（离线，无应用界面）：** 调用 `node scripts/validate_shapes.mjs` 脚本，该脚本会生成真实的 tldraw 模式，并对笔记、文本及框架内容进行验证。若验证通过，将输出 `3/3`。
- **实时画布编辑：** 在执行操作后，可通过 `/api/search` 获取当前状态 → 使用 `api.getShapes(docId)`（返回 `{ page, viewport, shapes }`）和 `api.getBindings(docId)`（返回数组）来查看生成的形状及绑定关系，确认它们与预期一致。随后可调用 `api.getScreenshot(docId)`（返回 `{ filePath, ... }`）获取截图，并使用 `vision_analyze` 工具对 PNG/JPEG 格式的图片进行分析。
- **持久化脚本应用状态查询：** 通过 `GET /api/doc/:id/script-status` 可查询脚本应用状态。若应用成功，状态将为 `state: "applied"`，此时需满足以下条件：`currentDiskDigest === lastAppliedDigest === manifestSha256`、`pendingApply === false` 且 `lastApplyError === null`。如果经过短暂重试后状态仍为 `"pending"`，则不应视为成功，而应上报该情况；若状态为 `"error"`，则表示应用失败，此时需查看 `errorLogPath` 文件以获取错误详情。
