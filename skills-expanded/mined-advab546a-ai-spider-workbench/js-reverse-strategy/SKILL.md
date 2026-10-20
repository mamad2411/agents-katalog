---
name: js-reverse-strategy
description: JS 逆向策略层和路线规划 skill。Use ONLY when the user needs task classification, route selection, writer-builder-entry-source checkpoint design, captcha/challenge line splitting, or a reusable research-case scaffold. Do not use for exact sign/token/header function location, browser hook snippets, Node.js environment patching, AST deobfuscation, or Ruishu/Rivers fixed-project tasks; route those to find-crypto-entry, browser-hook-snippets, env-patch, ast-deobfuscate, or rs-reverse. Cookie T/basearr pure calculation and Ruishu URL suffix AST research are not covered by the simplified rs-reverse skill.
---

# JS Reverse Strategy

这项技能是 JS 逆向的策略层：先判断题型、阻塞点和证据闭环，再决定交给哪个执行型 skill 或落成哪种案例结构。

它不替代具体执行技能。需要实际定位脚本/函数时用 `find-crypto-entry`；只要浏览器 hook 脚本时用 `browser-hook-snippets`；入口已知且要 Node.js 复现时用 `env-patch`；目标是 AST 结构化解混淆时用 `ast-deobfuscate`；出现瑞数/Ruishu/Rivers 或 `$_ts`、`r2mKa`、Cookie S/T 等证据，且目标是固定项目结构、首跳材料缓存或最小 runtime/proxy 观察时用 `rs-reverse`。Cookie T/basearr 纯算、r2mKa 字节码或 URL suffix AST 深度研究不由精简版 `rs-reverse` 接管。

## Core Loop

先把任务压成这条闭环：

```text
最终请求 / 最终 cookie / 最终 verify / 最终 WS 帧
-> writer
-> builder
-> entry
-> source
```

然后固定 5 层检查点：

1. writer 检查点：最终 URL、header、body、cookie 或 WS 帧。
2. builder 输入：query、payload、token、challenge、distance、track、browser info。
3. 原始串或原始 payload。
4. 中间数组、中间对象或编码前字节流。
5. 最终输出。

## When To Use

使用本 skill 的典型场景：

1. 用户不知道当前题属于标准签名、混合加密、cookie/header、多参数联动、JSVMP、Wasm、协议还是验证码。
2. 用户需要先设计浏览器值与本地值的检查点，而不是马上写 hook 或补环境。
3. 用户要把一个站点逆向过程沉淀成可复盘案例、solver、SDK 或服务结构。
4. 用户明确要“路线”“打法”“题型判断”“先做什么”“检查点”“案例骨架”。
5. 用户面对 captcha、collect、w、pow_answer、verify、challenge 等多线任务，需要拆初始化、图像、参数、环境和 verify。

## Do Not Use

不要在这些场景触发本 skill：

1. 用户要脚本 URL、行列号、函数名、调用链、参数生成入口：使用 `find-crypto-entry`。
2. 用户只缺一段可粘贴的 fetch/XHR/cookie/storage/crypto/canvas hook：使用 `browser-hook-snippets`。
3. 用户已知入口，目标是在 Node.js/VM 中补 `window/document/navigator/crypto` 跑通：使用 `env-patch`。
4. 用户要对 `_0x`、sojson、obfuscator、while-switch 做 AST 解混淆并保留中间产物：使用 `ast-deobfuscate`。
5. 用户明确出现瑞数/Ruishu/Rivers，或 412/403 同时伴随 `$_ts`、`r2mKa`、Cookie S/T、meta[r=m]，且目标是固定项目结构、首跳材料缓存或最小 runtime/proxy 观察：使用 `rs-reverse`。如果目标是 Cookie T/basearr 纯算、r2mKa 字节码或 URL suffix AST，先说明当前精简版 skill 集不覆盖该执行路线。

## Triage

先回答 4 个问题：

1. 真正决定成败的是哪条请求、哪次 cookie 写入、哪次 verify 或哪帧 WebSocket。
2. 目标字段长什么样：`sign`、cookie、header、body、verify payload、track、collect、image result。
3. 当前题型属于哪类：标准签名、混合加密、Cookie/Header、JSVMP/VMP、Wasm/协议、验证码。
4. 当前阻塞点属于哪类：入口、原始串、中间态、环境、图像线、协议线。

如果这 4 个问题答不清，不要直接抄大文件，也不要直接补环境。

## Route By Family

### 标准签名 / 混合加密 / Cookie / Header / 国密

适用信号：

1. 输出长度规整。
2. 存在 `md5`、`sha1`、`hmac`、`aes`、`rsa`、`sm3`、`sm4`。
3. 存在 `token&t&appKey&data`、`params + encSecKey` 或类似分层。
4. 值写入 `document.cookie`，或多个字段共同收口成 header。

策略：先追最终 writer，再拆 normalize/stringify/sort、token/timestamp/cookie/UA 注入、hash/encrypt/encode。

### JSVMP / VMP / 多参数复杂纯算

适用信号：

1. 大数组、解释器、`for(;;)+switch`、寄存器式状态机。
2. 值逐位、逐段、逐数组构造。
3. `window._webmsxyw`、`byted_acrawler`、`__TENCENT_CHAOS_VM` 一类入口。

策略：不要从文件头正推。先找最终 writer 和返回值，再恢复中间数组、payload 和最终编码层。

### Wasm / Protobuf / WebSocket / 二进制协议

适用信号：

1. `WebAssembly.instantiate`。
2. `application/x-protobuf`、二进制 body、WebSocket 分段交互。
3. 需要区分首包、图片包、验证包或导出函数。

策略：先找加载点、URL、`instance.exports` 和固定输入输出样本，再决定是否反编译。

### 验证码 / 风控 / Challenge

永远先拆 5 条线：

1. 初始化 / challenge 线。
2. 图像或题面识别线。
3. 参数 builder 线。
4. 环境 / 指纹 / collect 线。
5. 最终 verify 线。

不要一边调识别距离，一边调签名参数。识别结果应作为 builder 的显式输入。

## Blocker Diagnosis

常见阻塞点和优先动作：

1. 入口没找对：回到最终请求或最终 sink，重建 `writer <- builder <- entry <- source`，暂停补环境和整体迁移。
2. 原始串没对齐：打印 hash/encrypt 前原文，固定时间戳和随机数，检查 token、cookie、UA、序列化格式。
3. 中间态没采到：对数组写入点插桩，对 builder 做输入输出 hook，用 logpoint 代替高频断点。
4. 运行时依赖没补齐：收缩到最小入口，记录真实访问属性，只补进入 builder 的必要对象。
5. 图像线和参数线没拆开：单独保存识别结果和 builder 输入对象。
6. 协议边界没证明：先数包或列导出函数，证明输入输出关系，再决定是否反编译或迁移。

## Debug Priority

优先级固定为：

1. Hook / logpoint。
2. 调用栈回溯。
3. 条件断点。
4. 普通断点。

最值钱的观察点：

1. 请求链：`fetch`、`XMLHttpRequest.open/send`、`setRequestHeader`、`JSON.stringify`。
2. 写出点：`document.cookie`、目标对象字段写入、已知 builder 函数。
3. 运行时代码：`eval`、`Function`、`Date.now`、`Math.random`、`crypto.getRandomValues`。

## Cache And Artifacts

逆向分析过程中如果需要产出临时文件、抓包证据、下载脚本、格式化源码、运行产物或中间数据，统一写入执行代码工作区下的 `js_reverse_cache/` 文件夹；不存在则先创建。

不要自行把逆向数据写到执行代码工作区之外的位置。

每个可复盘案例至少留下：

1. 最终请求或最终 sink。
2. 请求链闭环。
3. 入口定位路径。
4. 中间检查点。
5. 本地代码骨架。
6. 易错点和版本风险。

## Expected Output

使用本 skill 时，优先输出：

1. 题型判断。
2. `writer / builder / entry / source` 分层。
3. 当前阻塞点判断。
4. 必要检查点列表。
5. 是否需要 AST、插桩、补环境、图像识别或协议拆包。
6. 应该交给哪个执行型 skill。
7. 推荐落地结构：函数、solver、SDK 或服务。
8. 易错点与版本风险。

## References

1. `references/01-decision-tree.md`：题型判断、阻塞点判断、请求链定位。
2. `references/02-algorithm-families.md`：标准签名、混合加密、Cookie/Header、JSVMP、Wasm、国密、站点家族模式。
3. `references/03-captcha-families.md`：腾讯、极验、网易盾、百度旋转、阿里 v2、V5、拼多多、hCaptcha 等验证码/风控路线。
4. `references/04-debug-env-playbook.md`：hook、logpoint、最小补环境、浏览器/本地对齐、反调试与证据管理。
5. `references/05-training-routes.md`：学习顺序、训练阶段、案例如何带新人、视频资料怎么吸收。
6. `references/06-engineering-maintenance.md`：GitHub 项目怎么吸收、接口如何设计、扩库时怎么记主落点/补充落点/标签。
7. `scripts/new_case_scaffold.py`：新站点或新 challenge 的标准化案例目录脚手架。

## Case Scaffold

在执行代码的工作区里快速起一套案例骨架：

```powershell
python "<skill-dir>\\scripts\\new_case_scaffold.py" `
  "case-name" `
  --type captcha `
  --family tencent `
  --tags captcha,collect,pow `
  --sources "https://example-a,https://example-b" `
  --language py
```

默认输出到当前目录下的 `js_reverse_cache/research/<case-name>/`。如果显式传 `--output`，也应传执行代码工作区内的 `js_reverse_cache/` 子目录。

脚手架会生成：

1. `case-overview.md`
2. `request-chain.md`
3. `evidence-log.md`
4. `checkpoints.json`
5. `metadata.json`
6. `solver_stub.js` 或 `solver_stub.py`
7. `todo.md`
