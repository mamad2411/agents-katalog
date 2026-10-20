---
name: find-crypto-entry
description: >-
  利用源码搜索和浏览器 DevTools/MCP 调试能力，定位 JS 请求里的加密参数、解密函数、签名参数、token、cookie 写入点或安全字段对应的关键脚本、函数入口和调用链。适合“用浏览器帮我找关键加解密 JS”“这个参数在哪生成”“请求头里的 xxx 哪来的”“这个 cookie 是哪个脚本写的”“帮我找 sign/token 的入口和调用路径”“定位 crypto/subtle/CryptoJS/wasm 加解密代码”这类请求，尤其适合用户明确要脚本 URL、行列号、函数名、调用链、入口类别或后续可接补环境的落点，而不是只要一段临时 hook 脚本、Node.js 补环境、Python + iv8 运行脚本或整文件 AST 解混淆时。对 challenge、动态 cookie、JSVMP、环境读取型签名场景，要先判断它是不是普通 `sign()` 入口问题；若出现瑞数/Ruishu/Rivers、`$_ts`、`r2mKa`、Cookie S/T 等证据且目标是固定项目结构、首跳材料缓存或最小 runtime/proxy 观察，转给 `rs-reverse`；Cookie T/basearr 纯算、r2mKa 字节码和 URL suffix AST 不由精简版 `rs-reverse` 接管。若用户只缺浏览器观察脚本，转给 `browser-hook-snippets`；若入口已知且目标是 Node.js 独立运行，转给 `env-patch`；若明确要 iv8/Python 脚本，转给 `iv8-web-reverse`。不要用于浏览器 hook 脚本生成、Node.js 补环境、普通抓包或整文件 AST 解混淆。
argument-hint: "[参数名]"
compatibility: "需要源码搜索能力；如需动态验证调用链，需浏览器调试能力。"
---

# find-crypto-entry

定位加密/解密逻辑 **$ARGUMENTS** 的生成或执行入口，并明确给出可继续分析的落点。

**目标**：找到关键加解密代码的函数位置（脚本 URL + 行列号 + 函数名 + 调用路径 + 入口类别），让后续补环境、AST 还原或算法分析可以直接接上。

## 使用方式

优先走成本最低的路径：

1. 先锁定真实请求、响应解密点或页面动作，再搜参数名、请求头名、密文字段、调用点和赋值位置。
2. 再读上下文，确认是业务代码、拦截器、外部 SDK、WebCrypto/CryptoJS、WASM、worker，还是 challenge 初始化链。
3. 静态路径不够时，再用浏览器调试验证调用链，优先围绕 Network initiator、XHR/fetch 断点、Event Listener、`crypto.subtle`、`CryptoJS.*`、`WebAssembly.instantiate`、Worker 构造和 SourceMap/pretty-print 入口定位。
4. 结束时只交付入口位置、调用链和最小运行时证据，不在本 skill 内继续做算法还原。

遇到复杂 header / cookie / verify / WebSocket 参数任务时，优先把问题压成这条链：

```text
最终请求 / 最终 cookie / 最终 verify / 最终 WebSocket 帧
-> writer
-> builder
-> entry
-> source
```

先证明当前卡在哪一层，再决定继续静态搜索、动态验证、转 AST 解混淆，还是进入补环境。

跨 skill 的阶段协议见 `references/js-reverse-workflow.md`。本 skill 主要覆盖 `Observe` 和轻量 `Capture`：先确认目标请求、脚本和入口类别，再把可继续补环境或解混淆的落点交给对应 skill。需要保存临时脚本、源码或证据时，按共享协议写入执行代码的工作区下的 `js_reverse_cache/`；不存在则先创建，不要写到工作区之外。

如果用户同时给了页面、抓包或报错，优先先确认一个真实请求：

1. 请求是在首页首跳、挑战页还是页面内 XHR / fetch 发出的。
2. 响应是正常业务数据，还是 `412` / `202` / `204` / 跳转链 / 挑战文档。
3. 如果只是“HTTP 200 但空 body / 空数据”，优先怀疑环境或注册路径没对上，而不是立刻认定入口没找到。

开始前先快速判断目标更像哪类：

1. **行为型签名**：页面能正常加载，参数出现在 XHR / fetch 请求里，常见于 `sign`、`token`、`a_bogus`、`X-Bogus`。
2. **首屏 challenge / 动态 cookie**：首页或前置请求先落到 `412`、`202`、`204`、跳转链或 challenge 文档。这类目标不要直接按“普通请求加签”思路深追入口，优先确认 challenge 脚本、cookie 写入点和初始化链路；如果命中瑞数证据且目标是固定项目骨架、首跳缓存或最小 runtime/proxy 观察，转给 `rs-reverse`。
3. **环境读取型 JSVMP / 环境即签名**：请求字段不是单一显式函数直接返回，而是依赖环境读取、副作用、解释器执行或初始化过程共同生成。这类目标不要强行寻找一个孤立的 `sign()` 函数。

如果已经确认是第二类或第三类，本 skill 只做局部定位，不承诺能单靠源码搜索直接找到最终 cookie 生成链或最终输出函数。

## 触发边界

下面这些需求通常应该触发本 skill：

1. “这个参数在哪生成”。
2. “请求头里的 Authorization / x-sign 是哪来的”。
3. “这个 cookie 是哪个脚本写的，给我调用链和脚本位置”。
4. “帮我找签名入口和调用链”。
5. “我要脚本 URL、函数名、行列号或调用路径”。
6. “用浏览器/DevTools/MCP 帮我找关键加解密 JS 代码”。
7. “定位 CryptoJS / WebCrypto / wasm / worker 里的加密或解密函数”。

下面这些需求通常不该由本 skill 单独处理：

1. “给我一个浏览器里能直接 hook 的脚本”。
2. “把浏览器代码补环境后放到 Node 里跑”。
3. “直接还原整个混淆文件”。
4. “我已经知道目标函数了，直接帮我补环境执行”。
5. “还不需要脚本位置或调用链，只想先判断题型、路线和检查点”。
6. “已经决定用 iv8/Python 跑防护页或动态 cookie 请求”。

## 转交提示

如果用户明确要的是“浏览器里能直接执行的 hook / 断点脚本”，转给 `browser-hook-snippets`。

如果用户只要任务分类、challenge/captcha 分线、writer-builder-entry-source 检查点或案例骨架，而不是脚本 URL、函数名、行列号和调用链，转给 `js-reverse-strategy`。

如果 challenge 证据明确指向瑞数/Ruishu/Rivers Security，如 `$_ts`、`r2mKa`、`Cookie S/T`、`meta[r=m]`，且任务目标是固定项目骨架、首跳材料缓存或最小 runtime/proxy 观察，转给 `rs-reverse`；如果用户要 Cookie T/basearr 纯算、r2mKa 字节码或 URL suffix AST，先说明当前精简版 `rs-reverse` 不覆盖该路线，不要继续按普通 sign 入口深追。本 skill 最多做未确认前的轻量定位。

如果用户在定位入口之后，下一步目标是“脱离浏览器在 Node.js 里独立运行”，转给 `env-patch`。

如果用户明确要的是“用 Python + iv8 跑浏览器 JS / 防护页 / 动态 cookie 后翻页请求”，转给 `iv8-web-reverse`。

如果入口已经找到，但 SDK 或目标文件本身高度混淆、需要源码级结构化还原，转给 `ast-deobfuscate`。

---

## 策略选择

根据信号选择策略，不要按固定顺序执行：

**优先静态搜索**：优先用 OpenCode 的搜索能力在源码里搜参数名。大多数情况下直接找到赋值位置，然后读上下文追溯来源。

**静态搜不到时再走浏览器侧定位**：在 DevTools 或可用的浏览器调试工具里围绕请求 URL、请求发起点和调用栈定位。断点命中后优先检查业务代码帧中的变量值。

**两种策略可以组合**：先静态搜索定位赋值位置，再在赋值处设断点动态验证。

### Browser-Assisted 关键 JS 定位

当用户的核心目标是“利用浏览器找关键加解密代码”时，优先按这条路径走：

1. **Network 入口**：锁定目标请求或密文字段，记录 URL、method、目标字段、initiator 和触发动作。
2. **断点入口**：按场景使用 XHR/fetch 断点、DOM/Event Listener 断点、WebSocket message/send 断点，先停在请求或数据出入口。
3. **调用栈筛选**：跳过框架、vendor、webpack runtime，优先看业务帧、SDK 帧、worker 脚本和动态脚本 URL。
4. **加解密 API 线索**：必要时围绕 `crypto.subtle.encrypt/decrypt/digest/sign/importKey`、`CryptoJS.AES/DES/TripleDES/RC4/MD5/SHA*`、`atob/btoa/TextEncoder/TextDecoder`、`WebAssembly.instantiate`、`Worker`、`postMessage` 做定点验证。
5. **源码落点**：记录脚本 URL、scriptId、行列号、函数名、模块 ID、chunk 名、是否 sourcemap/pretty-print 后定位。
6. **入口证据**：保存一次最小证据：入口入参、输出格式、调用前后关键状态、是否读取 cookie/storage/time/random/env。

如果浏览器里只能观察到 API 调用但还不能确定函数位置，可以临时借用 `browser-hook-snippets` 的最小 hook 采样调用栈；一旦目标变成“脚本 URL/函数/调用链”，回到本 skill 继续定位。

### Observe 完成判据

进入更重的 hook、补环境或解混淆前，至少能回答：

1. 目标请求 URL / 方法 / 参数位置是什么。
2. 请求由哪个页面动作触发。
3. 候选脚本 URL、scriptId 或文件路径是什么。
4. 参数更像业务直赋值、拦截器、外部 SDK、challenge 分支，还是环境读取型 JSVMP。
5. 当前证据来自静态搜索、网络 initiator、调用栈、hook，还是断点现场。
6. 当前链路已经证明到了哪一层：`writer`、`builder`、`entry`，还是 `source`。
7. 如果是解密任务，密文来自响应体、WebSocket 帧、localStorage、DOM 字段还是 worker message，明文第一次出现在哪个调用帧。

### Capture 最小样本

静态定位不够时，只采最小运行时样本：

1. 目标请求的 URL、method、headers/body 中的目标字段形态。
2. 入口函数的输入、输出、调用前后关键状态。
3. 影响入口是否注册或是否放行的初始化配置，如路径白名单、SDK 开关、token 预热状态。
4. 时间、随机数、cookie/storage 只记录键名、长度、格式和是否参与，不默认记录敏感原值。

完成后应能转交给 `env-patch` 或 `ast-deobfuscate`，不要在本 skill 中继续重写算法。

### 请求链记录

如果任务会跨多轮推进，或用户明确要求“继续上次结论”，优先把关键事实持续写入一个轻量请求链工件，例如 `reverse-records/请求链路.md` 或项目里的等价文件。至少记录：

1. 目标请求、目标字段、当前样本状态。
2. 样本编号和证据编号。
3. 写边界、来源链、去向链、上游请求。
4. 未闭环项和下一步最缺的证据。

这个工件用于续做和转交，不替代最终输出。

---

## 经验规则

逆向定位里最常见的误判如下：

更完整的入口架构、动态验证步骤和完成模板见 `references/entry-patterns.md`。当任务涉及拦截器、外部 SDK 或 challenge 分支时，先读该参考再开始追链。

### 加密参数的 5 种常见架构

1. **业务代码直接赋值** — 在请求函数中 `headers["x-sign"] = encrypt(data)`。静态搜索直接找到。
2. **请求拦截器统一加签** — axios interceptor 或 fetch wrapper 中统一添加。搜参数名可能只在拦截器中出现一次。
3. **外部安全 SDK** — 独立 JS 文件（通常混淆）挂载全局对象（如 `window.h5sign`），业务代码调用其方法。静态搜索能找到调用处，但 SDK 内部代码全被混淆。
4. **challenge / 动态 cookie 分支** — 参数或 cookie 来自首屏脚本副作用、跳转链或前置验证，不一定存在独立加密函数。
5. **环境读取型 JSVMP** — 输出依赖解释器执行时读取的环境、对象属性或宿主 API，不一定能抽象成单一业务函数。

### 行为型 SDK 的 2 个高价值线索

1. **初始化配置决定拦截器是否生效** — 某些 SDK 不是“找到 sign 函数就结束”，而是初始化时要注册目标路径或开关。除了参数名本身，也要搜初始化入参、路径表、配置对象。
2. **`cacheOpts` / `paths` / 请求白名单** — 字节系或同类 SDK 常把目标 API 路径挂在初始化配置里。静态搜索参数名搜不到时，改搜 `cacheOpts`、`paths`、目标 URL 片段、拦截器注册函数名，常能更快落到入口。

### 环境读取型目标的 3 个高价值线索

1. **请求发出前没有显式 sign 赋值** — 但会出现 cookie 变化、header 被统一注入、首屏脚本先运行一段解释器逻辑。
2. **请求是否放行取决于初始化配置** — 例如路径白名单、SDK 注册、解释器装载、cookie 预热、挑战脚本执行完成。
3. **环境读取比算法本身更关键** — 真正高价值的入口可能是 `document.cookie` 写入点、`createElement`/`canvas`/`navigator` 访问点、或 VMP 调度入口，而不是最终摘要函数。

### OB 混淆的影响

当加密逻辑在 OB 混淆的文件中（特征：`_0x` 前缀、大型字符串数组、RC4 解密函数），**所有字符串都被加密**，静态搜索在该文件内无法匹配任何明文。但调用该文件的业务代码通常未混淆，从业务代码侧搜索更高效。

### XHR 断点命中时的堆栈特点

XHR 断点命中在 `send()` 调用处，调用栈底部通常是框架代码（axios/fetch wrapper）。加密逻辑在栈的中上层。直接跳过底部框架帧，关注业务代码帧。

### 动态调试降噪

当暂停点总是落到框架、vendor 或 webpack runtime 时，先做调试降噪：

1. 如果调试器支持 blackbox，先黑盒 `jquery`、`react`、`vue`、`axios`、`lodash`、`node_modules`、`vendor`、通用 webpack runtime。
2. 优先用目标 URL 片段设置条件 XHR/fetch 断点，不要全局打断所有请求。
3. Watch expression 只盯当前问题需要的值：请求配置、最终 header、SDK 实例、时间种子、cookie/storage key、候选函数返回值。
4. Watch expression 要在目标调用帧里求值；只在顶层页面上下文求值容易误判。
5. 交互触发型签名可用事件断点辅助定位，例如 `click` / `submit`、timer instrumentation、WebSocket message/open。

这些只是入口定位辅助，不是本 skill 的最终交付物。

### 加密类型快速指纹

如果入口已定位但加密类型不清楚，用这些信号辅助填写“加密类型”：

1. `CryptoJS.AES/DES/TripleDES/RC4` 加第三个配置对象时，优先看 `mode`、`padding`、`iv`、salt。
2. `crypto.subtle.encrypt/sign/digest/importKey` 优先看第一个算法对象的 `name`、`hash`、`iv`、key usage。
3. 256 项 S-box/table、密集位运算、固定 block 循环，常指向对称加密或自定义 hash。
4. `modPow`、`modInverse`、`gcd`、素数检测，常指向 RSA/ECC 类大数逻辑。
5. MD5/SHA/AES 魔数只能帮助分类，不能替代入口链路验证。

---

## 反模式

- **不要反复 step_into** — 容易掉进框架响应式系统（Vue reactivity、React fiber）。优先直接检查当前调用帧里的变量，比盲目单步跟踪高效得多。
- **不要在 OB 混淆文件中搜字符串** — 所有明文都被加密了，搜不到。从非混淆的调用方搜。
- **不要频繁刷新页面** — 每次刷新所有 scriptId 失效。设好断点再刷新，一次到位。
- **断点命中时优先检查指定调用帧** — 如果调试工具支持按帧求值，优先查看目标业务帧，不要只看顶层上下文。

---

## 完成标准

找到以下信息即为完成：

```
入口位置：
- 参数：$ARGUMENTS
- 脚本：https://example.com/static/js/main.abc123.js
- 位置：第 X 行，第 Y 列
- 函数：functionName (或 anonymous)
- 调用路径：request → addSign → encrypt
- 加密类型：[标准算法名 | 外部SDK | 环境读取型 | 未知/需解混淆]
- 入口类别：[业务直赋值 | 拦截器统一加签 | 外部 SDK | challenge/动态 cookie 分支 | 环境读取型 JSVMP]
- 请求契约：method + url pattern + 参数所在位置
- 运行种子：cookie/storage/header/时间/随机数的键名、格式或参与状态
- 验证口径：参数长度/段数/编码特征，或服务端业务响应特征
```

如果目标不是普通函数加签，允许交付“初始化入口 / challenge 入口 / 环境访问链入口”，不强行伪造一个单点 `sign()` 结论。

只找入口，不做算法还原。

### 参数复现输出模板

需要沉淀给后续补环境时，优先补这份简表：

```text
requestSpec:
- method:
- urlPattern:
- paramLocation: query | body | header | cookie

paramContract:
- name:
- shape: length / segments / charset / encoding
- timeRelated: yes | no | unknown

runtimeSeedSchema:
- cookies:
- localStorage:
- sessionStorage:
- headers:

entryPoint:
- script:
- location:
- function:
- callPath:
- entryCategory:

handoff:
- nextSkill: rs-reverse | js-reverse-strategy | env-patch | ast-deobfuscate | browser-hook-snippets
- missingEvidence:
- artifact: reverse-records/请求链路.md | task-local equivalent
```

## 参考文件

1. `references/entry-patterns.md`：业务直赋值、请求拦截器、外部 SDK、challenge/dynamic cookie 分支的定位模式。
2. `references/js-reverse-workflow.md`：Observe/Capture/Rebuild/Patch/PureExtraction/Port 阶段协议。
3. `evals/evals.json`：入口定位、拦截器、challenge 转交和 hook 负例的回归测试集。
