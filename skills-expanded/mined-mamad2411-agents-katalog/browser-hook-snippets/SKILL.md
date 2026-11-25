---
name: browser-hook-snippets
description: >-
  在浏览器 DevTools、Snippets 或页面上下文中注入观察型 hook 脚本，追踪 cookie、XHR、fetch、header、storage、WebCrypto、canvas、Worker、Blob、DOM 注入等动态行为。适合“给我一个 hook xhr/fetch/cookie 的脚本”“给一段控制台脚本临时观察是谁写了 token/header”“想观察 canvas/worker/blob 的调用”这类请求，尤其适合用户已经知道观察目标、只缺一段可直接粘贴执行的脚本时。默认走最小侵入、页面层观察路线；在强完整性检测、原型检测、native 函数检测、JSVMP 环境探测场景中，要明确说明 JS hook 可能改变行为或被检测。若用户要的是函数位置、脚本 URL、完整调用链、参数生成入口，或“用浏览器找关键加解密 JS 代码”，转给 `find-crypto-entry`；若目标是脱离浏览器在 Node.js 跑，转给 `env-patch`；若明确要 Python + iv8 运行脚本，转给 `iv8-web-reverse`。不要用于 Node.js 补环境、源码静态搜索、函数入口定位或 AST 解混淆。
argument-hint: "[目标对象或行为]"
compatibility: "需要浏览器调试能力；默认面向 DevTools Console / Snippets / 页面注入脚本。部分模板依赖现代浏览器 API（如 fetch、WebCrypto、Worker、MutationObserver），必要时需切到页面上下文注入。"
---

# browser-hook-snippets

围绕 **$ARGUMENTS** 生成最小可用的浏览器 hook 脚本，并说明注入位置、预期现象和回收方式。

## 目标

当用户已经知道要盯的对象或行为时，直接给出可执行的 hook 方案，而不是停留在原理说明。

## 触发信号

下面这些说法通常应该触发本 skill：

1. “给我一个 hook xxx 的脚本”。
2. “给一段控制台 hook 脚本，临时观察是谁写了 cookie/token/header”。
3. “帮我盯住 fetch/xhr/websocket/postMessage/worker”。
4. “想观察某个 DOM、canvas、blob、随机数、加密 API 调用时的入参和调用栈”。
5. “给一个能直接贴到 DevTools Console 或 Snippets 的脚本”。

下面这些说法通常不该由本 skill 单独处理：

1. “这个签名参数在哪生成”但用户要的是完整调用链定位，不只是注入脚本。
2. “把这段浏览器 JS 搞到 Node 里跑”。
3. “帮我反混淆这个大文件”。
4. “帮我找到脚本 URL、函数名、行列号”。
5. “我要完整说明 sign/token/header 的生成入口和调用链”。
6. “用浏览器/DevTools/MCP 帮我定位关键加解密 JS 代码”。

## 转交提示

如果用户要的是“函数位置、脚本 URL、调用路径”，或想利用浏览器定位关键加解密 JS 代码，转给 `find-crypto-entry`。

如果用户要处理瑞数/Ruishu/Rivers 的固定项目结构、首跳材料缓存或最小 proxy 环境观察，转给 `rs-reverse`；如果只是单独要一段临时浏览器 hook 脚本，才留在本 skill。Cookie T 纯算、basearr 闭包、r2mKa 字节码或 URL suffix AST 不属于本 skill，也不要误转给精简版 `rs-reverse`。

如果用户要的是“Node.js 独立运行、补 window/document/navigator 环境”，转给 `env-patch`。

如果用户要的是“Python + iv8 执行防护页 / 动态 cookie / 翻页请求”，转给 `iv8-web-reverse`。

如果用户要的是“把混淆代码结构化还原成可读源码”，转给 `ast-deobfuscate`。

## 适用范围

优先处理下面几类浏览器侧动态追踪需求：

1. `document.cookie` 的读写。
2. `XMLHttpRequest` / `fetch` 请求发起与 header 设置。
3. `eval` / `Function` / `JSON.parse` / `JSON.stringify` 的运行时参数。
4. `document.createElement`、元素属性、表单值等 DOM 行为。
5. `WebSocket.send` / `message` 的数据流。
6. `localStorage` / `sessionStorage` 的读写。
7. `atob` / `btoa`、`crypto.subtle`、`canvas` 等常见逆向落点。
8. `crypto.getRandomValues`、`Blob`、`URL.createObjectURL`、`Worker`、`postMessage`。
9. `appendChild`、`insertBefore`、`MutationObserver` 这类动态注入链路。

## 输出要求

默认给出这 4 项：

1. 一段可以直接执行的最小 hook 脚本。
2. 脚本应该注入在哪里：Console、Snippets、Sources 断点后注入，还是页面脚本标签注入。
3. 预期能看到什么日志或断点。
4. 需要注意的副作用和恢复方式。

如果用户目标比较明确，再补 1 项：

5. 为什么优先 hook 这个点，而不是附近其它点。

## 工作方式

按最小侵入原则处理：

1. 先确认 hook 目标是“属性”“方法”还是“构造器”。
2. 优先包装单个目标，不要一上来全局代理整页对象。
3. 保留原函数引用，调用原实现时避免递归调用自身。
4. 默认只做记录和断点，不主动改返回值，除非用户明确要求篡改行为。
5. 如果目标代码跑在页面上下文而不是 Console 沙箱里，使用 `script.textContent = '(' + fn + ')()'` 注入页面上下文。
6. 如果页面存在完整性检测、native 伪装检测、原型链检测或 JSVMP 环境探测，先提醒用户：JS hook 可能改变行为、失去命中或直接被检测。

跨 skill 的阶段协议见 `references/js-reverse-workflow.md`。本 skill 主要服务 `Capture` 阶段：优先用 hook 采样真实运行行为；hook 无法回答函数位置或完整调用链时，再升级到 `find-crypto-entry`。需要落地 hook 日志、采样证据或临时脚本时，按共享协议写入执行代码的工作区下的 `js_reverse_cache/`；不存在则先创建，不要写到工作区之外。

### Hook 数据降噪

请求、storage、postMessage、WebSocket 这类高频 hook 默认应提供摘要思路，避免控制台日志淹没有效记录：

1. 给每条记录生成 key，例如 `target + event + method + url + bodySnippet`。
2. 对相同 key 计数，只展示前 N 个样本。
3. 对请求类记录额外输出 `method`、`url`、`status`、`bodySnippet`、`timestamp`。
4. 从 URL、body、header 中提取 `sign`、`token`、`auth`、`nonce`、`timestamp` 等指示词。
5. 如果目标是后续补环境，补充候选环境依赖，如 `cookie`、`storage`、`Date`、`crypto`、`location`。

### Request Binding

当用户要观察“哪个请求带了目标字段”时，hook 输出应尽量绑定请求上下文：

1. `target`: fetch | xhr | websocket | form | beacon。
2. `event`: open | send | setRequestHeader | response | message。
3. `method` 和 `url`。
4. 命中的 header / query / body 字段名。
5. 可选 `console.trace()` 或一次性 `debugger`，用于后续转交 `find-crypto-entry`。

如果用户只要最小脚本，不要强行附带完整摘要器；但要在说明里给出如何收缩日志和如何按 URL/字段过滤。

## 经验规则

1. `document.createElement`、`XMLHttpRequest.prototype.open` 这类宿主方法，先 `bind` 或保存原引用再调用，避免 `Illegal invocation`。
2. `WebSocket.prototype.send`、`fetch`、`eval` 这类函数 hook 时，返回值必须继续走原实现，否则页面容易异常。
3. 属性 hook 优先用 `Object.defineProperty`；如果原属性已经不可配置，改用外围调用点或原型方法 hook。
4. 只在用户明确要求时才提供“阻断”型脚本；默认提供“观察”型脚本。
5. 如果用户想知道“请求是谁发起的”，而当前环境没有专门的 request initiator 工具，优先在 `fetch` / `xhr` hook 里补 `console.trace()`，用调用栈替代专用调试工具能力。
6. 如果用户问“某个 cookie 是谁写的”，先提醒：`document.cookie` hook 只能看到 JS 写入；若 cookie 实际来自 HTTP `Set-Cookie`，必须同时检查目标请求或响应头。
7. 遇到 SDK 或拦截器型页面时，不要默认只 hook `XMLHttpRequest`；很多站点会同时走 `xhr` 和 `fetch`，漏掉其中一个就会误判“签名函数没跑到”。
8. 观察环境读取型行为时，优先从 `navigator`、`screen`、`document.createElement`、`canvas.getContext`、`WebGLRenderingContext.getParameter`、`performance.now`、`localStorage`、`sessionStorage` 里选一个最可疑点定向下手，不要一次全开。
9. 如果 hook 后页面行为变化、请求消失、签名降级或日志极多，先收缩 hook 点、改断点或补 `console.trace()`，不要继续叠加更多 hook。
10. 高频 hook 默认先加 URL、字段名、调用次数或 body 长度条件；不要把完整请求体、完整 cookie、完整 storage 原文无条件刷屏。

## 反模式

不要默认输出下面这些高风险写法：

1. 无条件清空所有定时器。
2. 粗暴替换所有 `debugger`、所有 `console`、所有 `RegExp`。
3. 会递归调用自己的错误 hook，比如在 `send` 里再次调用被改写后的 `send`。
4. 大范围改写原生对象却不说明恢复方式。
5. 默认代理整个 `window`、`document`、`navigator`。
6. 在强完整性检测页面里，不提醒风险就直接输出重写原型链的大脚本。

这些片段可以作为特殊场景候选，但不作为默认答案。

## 参考片段

索引见 `references/snippets.md`。

按目标读取对应分类：

1. 请求、header、WebSocket、postMessage：`references/network.md`
2. cookie、storage、输入值：`references/storage.md`
3. base64、WebCrypto、随机数、编码边界：`references/crypto.md`
4. createElement、DOM 注入、MutationObserver、canvas：`references/dom.md`
5. JSON、eval、Function、Blob、Worker：`references/runtime.md`

生成答案时：

1. 先按用户目标只读最相关的 1 个分类文件，必要时再补第 2 个。
2. 按当前页面需求裁剪，不要整份堆给用户。
3. 如果用户给了关键字或 URL 片段，直接代入条件判断。
4. 如果用户没说注入时机，优先提醒“可在 Sources 首个脚本处暂停后再注入”。
5. 如果页面明显会因为 hook 方式不同而失效，显式说明是“Console 沙箱 hook”还是“页面上下文 hook”。

## 升级与降级

当最小 hook 不能满足需求时，按这个顺序调整：

1. 先缩小到单个属性、单个方法或单个 URL 条件。
2. 再补 `console.trace()`、条件断点或一次性 `debugger`。
3. 如果用户真正要的是函数位置、脚本 URL、调用链，转给 `find-crypto-entry`。
4. 如果用户真正要的是 Node.js 独立复现，转给 `env-patch`。

## 回答风格

1. 先给能跑的最小脚本。
2. 再给注入位置和触发条件。
3. 最后再补副作用和升级建议。
4. 除非用户明确要求，不要一次贴多个大脚本方案。

## 完成标准

完成时，用户应能直接拿到：

1. 可执行脚本。
2. 断点或日志触发条件。
3. 为什么这个 hook 点有效。
4. 何时需要升级为调用链定位、补环境或解混淆。
5. 对高频场景，知道如何去重、过滤和绑定到具体请求。
