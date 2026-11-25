---
name: node-inspect-debugger
description: "Debug Node.js via --inspect + Chrome DevTools Protocol CLI."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [debugging, nodejs, node-inspect, cdp, breakpoints, ui-tui]
    related_skills: [systematic-debugging, python-debugpy]
---

# Node.js 检查调试器

## 概述

当 `console.log` 已无法满足需求时，您可以通过终端以编程方式调用 Node 内置的 V8 检查工具。该工具支持真正的断点设置、单步执行/跳过/退出、调用栈遍历、局部变量/闭包作用域查看，以及在对当前帧进行暂停时评估任意表达式。

您可以从以下两种工具中选择一种：

- **`node inspect`** —— 内置工具，无需安装，基于 CLI REPL，适合快速调试。
- **`ndb` / 通过 `chrome-remote-interface` 的 CDP** —— 可从 Node/Python 脚本中调用，适用于需要设置大量断点、在多次运行间收集状态，或通过代理循环进行非交互式调试的场景。

**建议优先使用 `node inspect`**。它始终可用，且 REPL 的响应速度很快。

## 适用场景

- Node 测试失败，需要查看中间状态
- ui-tui 发生崩溃或行为异常，需要检查预渲染前的 React/Ink 状态
- tui_gateway 的子进程（如 `_SlashWorker`、PTY 桥接进程）行为异常
- 需要查看闭包中的某个值，而 `console.log` 无法直接获取（除非进行代码修改）
- 性能分析：附加到正在运行的进程上以捕获 CPU 使用情况或堆内存快照

**不推荐用于**：那些 `console.log` 即可在一分钟内解决的问题。基于断点的调试方式较为繁琐，只有当其能带来显著收益时才应使用。

## `node inspect` REPL 快速参考

首次启动时会自动暂停在代码的第一行：

```bash
node inspect path/to/script.js
# or with tsx
node --inspect-brk $(which tsx) path/to/script.ts
```

`debug>` 提示符支持以下命令：

| 命令 | 功能 |
|---|---|
| `c` 或 `cont` | 继续执行 |
| `n` 或 `next` | 跳过当前行 |
| `s` 或 `step` | 进入函数内部 |
| `o` 或 `out` | 退出函数 |
| `pause` | 暂停正在运行的代码 |
| `sb('file.js', 42)` | 在 file.js 的第 42 行设置断点 |
| `sb(42)` | 在当前文件的第 42 行设置断点 |
| `sb('functionName')` | 在函数被调用时触发断点 |
| `cb('file.js', 42)` | 删除指定位置的断点 |
| `breakpoints` | 列出所有断点 |
| `bt` | 显示调用堆栈 |
| `list(5)` | 显示当前位置周围的 5 行代码 |
| `watch('expr')` | 每次暂停时计算 expr 的值 |
| `watchers` | 显示已监控的表达式 |
| `repl` | 进入当前作用域的 REPL 模式（按 Ctrl+C 可退出 REPL） |
| `exec expr` | 一次性计算表达式的值 |
| `restart` | 重新启动脚本 |
| `kill` | 终止脚本运行 |
| `.exit` | 退出调试器 |

**在 `repl` 子模式下：** 可输入任意 JS 表达式，包括访问局部变量/闭包变量。按 `Ctrl+C` 可返回到 `debug>` 模式。

## 连接到正在运行的进程

当进程已经处于运行状态时（例如长期运行的开发服务器或 TUI 网关）：

```bash
# 1. Send SIGUSR1 to enable the inspector on an existing process
kill -SIGUSR1 <pid>
# Node prints: Debugger listening on ws://127.0.0.1:9229/<uuid>

# 2. Attach the debugger CLI
node inspect -p <pid>
# or by URL
node inspect ws://127.0.0.1:9229/<uuid>
```

从初始状态开始使用检查器启动流程：

```bash
node --inspect script.js           # listen on 127.0.0.1:9229, keep running
node --inspect-brk script.js       # listen AND pause on first line
node --inspect=0.0.0.0:9230 script.js   # custom host:port
```

通过 tsx 使用 TypeScript 时：

```bash
node --inspect-brk --import tsx script.ts
# or older tsx
node --inspect-brk -r tsx/cjs script.ts
```

## 基于脚本的CDP（终端编程方式）

当您需要实现自动化操作——例如设置多个断点、捕获作用域状态或编写可复现的操作脚本时，可使用 `chrome-remote-interface`：

```bash
npm i -g chrome-remote-interface        # or project-local
# Start your target:
node --inspect-brk=9229 target.js &
```

驱动脚本（保存为 `/tmp/cdp-debug.js`）：

```javascript
const CDP = require('chrome-remote-interface');

(async () => {
  const client = await CDP({ port: 9229 });
  const { Debugger, Runtime } = client;

  Debugger.paused(async ({ callFrames, reason }) => {
    const top = callFrames[0];
    console.log(`PAUSED: ${reason} @ ${top.url}:${top.location.lineNumber + 1}`);

    // Walk scopes for locals
    for (const scope of top.scopeChain) {
      if (scope.type === 'local' || scope.type === 'closure') {
        const { result } = await Runtime.getProperties({
          objectId: scope.object.objectId,
          ownProperties: true,
        });
        for (const p of result) {
          console.log(`  ${scope.type}.${p.name} =`, p.value?.value ?? p.value?.description);
        }
      }
    }

    // Evaluate an expression in the paused frame
    const { result } = await Debugger.evaluateOnCallFrame({
      callFrameId: top.callFrameId,
      expression: 'typeof state !== "undefined" ? JSON.stringify(state) : "n/a"',
    });
    console.log('state =', result.value ?? result.description);

    await Debugger.resume();
  });

  await Runtime.enable();
  await Debugger.enable();

  // Set a breakpoint by URL regex + line
  await Debugger.setBreakpointByUrl({
    urlRegex: '.*app\\.tsx$',
    lineNumber: 119,       // 0-indexed
    columnNumber: 0,
  });

  await Runtime.runIfWaitingForDebugger();
})();
```

运行它：

```bash
node /tmp/cdp-debug.js
```

针对 Hermes 的特别说明：`ui-tui/package.json` 中并未包含 `chrome-remote-interface`。如果您不想污染项目文件，可将其安装到临时目录中。

```bash
mkdir -p /tmp/cdp-tools && cd /tmp/cdp-tools && npm i chrome-remote-interface
NODE_PATH=/tmp/cdp-tools/node_modules node /tmp/cdp-debug.js
```

## 调试 Hermes ui-tui

该 TUI 是使用 Ink 和 tsx 构建的。常见有以下两种场景：

### 在开发模式下调试单个 Ink 组件

`ui-tui/package.json` 文件中已定义了 `npm run dev`（即 `tsx --watch` 命令）。若需直接运行 tsx 进行调试，可添加 `--inspect-brk` 参数：

```bash
cd <hermes-agent-repo>/ui-tui
npm run build    # produce dist/ once so transpile isn't needed on first load
node --inspect-brk dist/entry.js
# In another terminal:
node inspect -p <node pid>
```

接着在 `debug>` 命令下：

```
sb('dist/app.js', 220)     # or wherever the suspect render is
cont
```

当程序暂停时，可通过 `repl` 命令来查看 `props`、状态引用、`useInput` 处理器的值等信息。

### 调试正在运行的 `hermes --tui` 程序

TUI 会通过 Python CLI 启动 Node 进程。最简便的调试方法为：

```bash
# 1. Launch TUI
hermes --tui &
TUI_PID=$(pgrep -f 'ui-tui/dist/entry' | head -1)

# 2. Enable inspector on that Node PID
kill -SIGUSR1 "$TUI_PID"

# 3. Find the WS URL
curl -s http://127.0.0.1:9229/json/list | jq -r '.[0].webSocketDebuggerUrl'

# 4. Attach
node inspect ws://127.0.0.1:9229/<uuid>
```

通过 TUI 进行交互（在其实时输入窗口中输入指令）可持续推动程序执行；您的调试器可在任意 `sb(...)` 语句处的断点处暂停执行。

### 调试 `_SlashWorker` / PTY 子进程

这类进程为 Python 编写，而非 Node —— 应使用 `python-debugpy` 技能进行调试。仅有 Node 相关部分（如 Ink UI、tui_gateway 客户端，以及 `ui-tui/` 目录下的 tsx-run 测试）才适用该技能。

## 在调试器环境下运行 Vitest 测试

```bash
cd <hermes-agent-repo>/ui-tui
# Run a single test file paused on entry
node --inspect-brk ./node_modules/vitest/vitest.mjs run --no-file-parallelism src/app/foo.test.tsx
```

在另一个终端中执行：`node inspect -p <pid>`，随后输入 `sb('src/app/foo.tsx', 42)`，最后输入 `cont`。

建议使用 `--no-file-parallelism`（vitest）或 `--runInBand`（jest）选项以确保仅存在一个工作进程——调试多个工作进程的过程十分繁琐。

## 堆快照与 CPU 分析（非交互模式）

在上述 CDP 驱动程序中，将 Debugger 替换为 `HeapProfiler` / `Profiler` 即可：

```javascript
// CPU profile for 5 seconds
await client.Profiler.enable();
await client.Profiler.start();
await new Promise(r => setTimeout(r, 5000));
const { profile } = await client.Profiler.stop();
require('fs').writeFileSync('/tmp/cpu.cpuprofile', JSON.stringify(profile));
// Open /tmp/cpu.cpuprofile in Chrome DevTools → Performance tab
```

```javascript
// Heap snapshot
await client.HeapProfiler.enable();
const chunks = [];
client.HeapProfiler.addHeapSnapshotChunk(({ chunk }) => chunks.push(chunk));
await client.HeapProfiler.takeHeapSnapshot({ reportProgress: false });
require('fs').writeFileSync('/tmp/heap.heapsnapshot', chunks.join(''));
```

## 常见问题

1. **TypeScript 源文件中的行号错误。** 断点实际上作用于生成的 JavaScript 文件，而非 `.ts` 文件。解决方案为：(a) 在编译后的 `dist/*.js` 文件中设置断点；或 (b) 启用源映射功能（使用 `node --enable-source-maps`），并通过 `sb('src/app.tsx', N)` 设置断点——但仅适用于支持源映射的 CDP 客户端，`node inspect` CLI 不支持此功能。

2. **`--inspect` 与 `--inspect-brk` 的区别。** `--inspect` 仅启动调试器而不暂停脚本执行，若在过晚时附加调试器，脚本会直接跳过第一个断点。当需要在代码运行之前就设置断点时，请使用 `--inspect-brk`。

3. **端口冲突问题。** 默认端口为 `9229`。如果有多个 Node 进程正在使用该端口进行调试，可指定 `--inspect=0` 以随机选择端口，并通过 `/json/list` 获取实际的端口号。
   ```bash
   curl -s http://127.0.0.1:9229/json/list   # lists all inspectable targets on the host
   ```

4. **子进程。** 在父进程上使用`--inspect`选项并不会对其子进程进行检测。若需对所有子进程生效，应使用`NODE_OPTIONS='--inspect-brk' node parent.js`命令；需要注意的是，这些子进程需要使用不同的端口（当继承了`NODE_OPTIONS='--inspect'`选项时，Node会自动为每个进程分配递增的端口）。

5. **后台终止操作。** 如果在目标进程处于暂停状态时通过`node inspect`退出程序，目标进程仍会保持暂停状态。此时要么先使用`cont`命令继续执行，要么直接对目标进程发送`kill`指令。

6. **通过Agent终端运行`node inspect`。** 它是一个兼容伪终端（PTY）的REPL环境。在Hermes中，可通过`terminal(pty=true)`或`background=true`结合`process(action='submit', data='...')`来启动它。非PTY的前台模式适用于一次性命令，但不支持交互式调试步骤执行。

7. **安全性。** 使用`--inspect=0.0.0.0:9229`选项会带来任意代码执行的风险。除非处于隔离网络环境中，否则应始终将监听地址设置为默认值`127.0.0.1`。

## 验证清单

设置完调试会话后，请进行以下验证：

- [ ] 执行`curl -s http://127.0.0.1:9229/json/list`命令后，返回的结果确实为预期的目标进程。
- [ ] 第一个断点能够成功触发（若无法触发，很可能是遗漏了`--inspect-brk`选项，或是在程序执行完成后才进行连接）。
- [ ] 程序暂停时显示的源代码列表为正确的文件（若不一致，则属于源码映射问题，详见注意事项1）。
- [ ] 在REPL环境中执行`exec process.pid`命令后，返回的进程ID即为原本打算连接的进程ID。

## 一次性使用方案

**“为什么在X行这个变量是未定义的？”**
```bash
node --inspect-brk script.js &
node inspect -p $!
# debug>
sb('script.js', X)
cont
# paused. Now:
repl
> myVariable
> Object.keys(this)
```

**“调用该函数的路径是什么？”**
```
debug> sb('suspectFn')
debug> cont
# paused on entry
debug> bt
```

**“这个异步链卡住了——问题出在哪里？”**
```
# Start with --inspect (no -brk), let it run to the hang, then:
debug> pause
debug> bt
# Now you see the stuck frame
```
