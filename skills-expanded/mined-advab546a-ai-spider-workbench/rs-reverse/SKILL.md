---
name: rs-reverse
description: >-
  瑞数/Ruishu/Rivers Security 轻量项目骨架 skill。仅在有明确瑞数证据（如 $_ts.nsd/cd/l__、r2mKa、meta[r=m]、Cookie S/T/P、hasDebug、瑞数/Rivers 412/403）且任务目标是创建或维护固定本地项目结构、把首跳挑战材料缓存到 js_reverse_cache/、运行基础 Node cookie/runtime 检查、或使用最小浏览器 proxy 模板观察环境读取时触发。不要用于 Cookie T/P 纯算、basearr 拟合、sdenv/jsdom 框架补环境、browser-rpc/JsRpc、URL suffix AST 研究、普通 sign/token 定位或 Python + iv8 请求脚本。
---

# RS Reverse Skill

本 skill 已精简为瑞数轻量项目骨架 skill，只保留固定项目结构、`js_reverse_cache/` 缓存规则、基础 Node runtime 检查，以及最小浏览器环境 proxy 观察模板。

本 skill 不提供、不引导以下路线：Cookie T/P 纯算、basearr 拟合、sdenv/jsdom 框架补环境、browser-rpc/JsRpc 框架、URL suffix AST 研究、r2mKa 字节码研究。

## 硬性约束

- 自动采集或下载得到的目标站点动态材料、挑战源码、session 样本、临时 runtime 文件、运行报告和分析记录，统一写入当前工作区的 `js_reverse_cache/`。
- 如果当前工作区没有 `js_reverse_cache/`，先创建它。
- 不要把目标站点动态素材写入本 skill 目录。
- 固定瑞数项目结构必须保留，不能被通用 demo 结构替代。
- 根目录 `challenge_payload_bootstrap.js` 和 `challenge_payload_runner.js` 是用户手动维护的固定样本，用于本地环境观察和缺失环境定位；除非用户明确要求，不要覆盖它们。
- `rs_reverse.js` 只放占位符模板，不写入真实动态挑战源码；真实 runtime 源码只写入 `js_reverse_cache/<run>/rs_reverse_runtime.js` 这类临时文件。
- 同一条验证链路必须使用同 session 的首跳 Cookie、挑战 payload、Node 生成 Cookie、业务参数/sign/timestamp 和回放请求；不要混用旧 Cookie、旧 runtime、旧 suffix 或旧签名。
- 不要因为浏览器网络里出现 suffix 就默认复用 suffix。本精简 skill 不做 suffix 研究或生成；如果请求可用性依赖 suffix，转交 `iv8-web-reverse`。

## MCP 工具选择

- 需要浏览器侧定位、源码搜索、XHR/fetch 断点、请求发起栈、WebSocket 消息或 runtime 调试时，先检查是否存在 `js-reverse-mcp_*` 工具。
- 如果存在 `js-reverse-mcp_*`，优先用它完成页面选择、源码搜索、断点、调用栈和网络分析。
- 只有当前会话没有 `js-reverse-mcp_*`，或该工具无法完成所需浏览器交互时，才回退到 `chrome-devtools-mcp_*`。
- 同一条调试链路尽量不要混用两套 MCP 页面上下文；确需切换时，先重新确认当前 page、frame 和请求证据。

## 固定项目结构

当用户要把瑞数材料、Cookie 检查或本地环境观察落到项目中时，使用以下根目录结构：

```text
challenge_payload_bootstrap.js  # 用户手动固定的 $_ts inline/bootstrap 样本；自动采集不要覆盖
challenge_payload_runner.js     # 用户手动固定的 mainjs/r2mKa runner 样本；自动采集不要覆盖
mod.js                          # 最小浏览器 proxy / logging 模板
main.js                         # 本地 runner：require mod/bootstrap/runner 后输出 document.cookie
main.py                         # 首跳采集 + 临时 runtime 执行 + 同 session 回放
rs_reverse.js                   # 只含占位符的 runtime 模板
js_reverse_cache/               # 自动缓存：源码、样本、临时 runtime、报告
```

本 skill 提供的模板文件：

- `project-templates/minimal-proxy-env-template.js`：创建 `mod.js` 的默认起点。
- `project-templates/rs-runtime-placeholder-template.js`：创建 `rs_reverse.js` 的占位符模板。
- `project-templates/node-cookie-runner-template.js`：创建 `main.js` 的本地 runner 模板。
- `project-templates/python-session-request-template.py`：创建 `main.py` 的首跳/session/runtime 模板。

根目录 `challenge_payload_*` 文件由用户手动维护。自动采集流程只把新鲜材料写入 `js_reverse_cache/<run>/`，再基于缓存材料构造临时 runtime 文件。

## 触发范围

使用本 skill 当：

- 用户明确说瑞数、Ruishu、Rivers Security、瑞数 4/5/6 或 Rivers 动态安全防护，并且目标是固定项目结构、首跳材料缓存、基础 Node runner 或最小 proxy 观察。
- `412` / `403` challenge 有明确瑞数证据：`$_ts`、`$_ts.nsd`、`$_ts.cd`、`$_ts.l__`、`r2mKa`、`meta[r=m]`、Cookie `S/T/P` 或 `hasDebug`。
- 用户要创建或修复固定本地瑞数项目结构。
- 用户要把首跳 challenge HTML / 外链 JS 缓存到 `js_reverse_cache/`，且不覆盖根目录 payload 文件。
- 用户要一个基础 Node runner，加载 `mod.js`、`challenge_payload_bootstrap.js`、`challenge_payload_runner.js`，观察 `document.cookie` 或缺失环境读取。
- 用户要最小 proxy 版浏览器环境观察模板。

不要使用本 skill 当：

- 用户要 Cookie T/P 纯算、basearr 拟合、type=2 映射、混合验证或端到端纯算。本精简 skill 不再包含这些路线。
- 用户要 sdenv/jsdom、JsRpc/browser-rpc 或任何框架型浏览器环境补齐。
- 用户要 URL suffix AST 研究、r2mKa 字节码反汇编、session49、child[29]/child[40] 或 VM opcode 工具链。
- 任务是普通 `sign`、`token`、`x-sign`、动态 header 或业务参数入口定位。交给 `find-crypto-entry`。
- 任务只是要可粘贴的浏览器 hook snippet 来观察 cookie/fetch/xhr/header。交给 `browser-hook-snippets`。
- 任务是非瑞数浏览器 JS 的通用 Node.js 补环境。交给 `env-patch`。
- 任务是通用 AST 解混淆。交给 `ast-deobfuscate`。
- 用户明确要紧凑 `Python + iv8 + requests`、iv8 翻页请求，或通过浏览器式页面执行解决 suffix 请求可用性。交给 `iv8-web-reverse`。
- 页面只有普通 403/412，但没有瑞数证据。先交给 `find-crypto-entry` 或 `js-reverse-strategy` 判断题型。

## 跨 skill 交接

- 未确认瑞数，且目标是参数/header/cookie 来源定位：交给 `find-crypto-entry`。
- 只要 DevTools 临时观察 hook：交给 `browser-hook-snippets`。
- 通用 Node.js 补环境或 sdenv/jsdom 框架工作：交给 `env-patch`。
- 单个混淆文件结构化还原：交给 `ast-deobfuscate`。
- 紧凑 Python + iv8 runtime 复现或请求可用性：交给 `iv8-web-reverse`。
- 没有明确瑞数证据，只要路线判断和检查点设计：交给 `js-reverse-strategy`。

## 任务状态块

仅当任务需要多步执行、跨会话续做或会产出本地工件时，先输出一个简短状态块；简单问答、目录检查、轻量 review 或用户明确只要结论时不要强制输出。

```text
Complexity: L3
Current stage:
Why this stage now:
Read now:
Required artifact:
Exit condition:
```

阶段含义：

- `locate`：确认瑞数证据、首跳页面、runner 脚本、可见 cookie 和目标业务请求。
- `scaffold`：创建或修复固定项目结构和模板文件。
- `runtime`：用同 session 缓存材料构造临时 runtime，并运行本地 Node 检查。
- `validation`：同 session 回放检查和 artifact/report 清理。

## 工作流程

1. 从页面 HTML、Cookie、script 标签或网络响应确认瑞数证据。
2. 确保当前工作区存在 `js_reverse_cache/`。
3. 如果固定项目文件缺失，只从 `project-templates/` 创建缺失文件。
4. 不覆盖根目录 `challenge_payload_bootstrap.js` 或 `challenge_payload_runner.js`，除非用户明确要求。
5. 把首跳 HTML、首跳 Cookie、runner URL、runner JS 写入带时间戳的 `js_reverse_cache/<run>/` 目录。
6. 基于根目录 `rs_reverse.js` 的占位符，在缓存 run 目录里生成临时 `rs_reverse_runtime.js`。
7. 只运行临时 runtime，不把真实挑战源码写回 `rs_reverse.js`。
8. 如果 Node 输出中能解析到生成 Cookie，写回同一个 Python `requests.Session`。
9. 用同一个 session 回放页面或业务请求。
10. 如果失败原因是业务参数、sign 或 timestamp，离开本 skill 修业务逻辑。
11. 如果失败需要 suffix 生成或高保真页面执行，停止本 skill 路线并转交 `iv8-web-reverse`。

## 最小浏览器 Proxy 模板

本 skill 只保留一个浏览器环境辅助：基础 proxy/logging 模板，用来观察目标瑞数 JS 在本地运行时读取、写入或调用了哪些浏览器全局对象。

用 `project-templates/minimal-proxy-env-template.js` 创建 `mod.js`。

不要在本 skill 内把 `mod.js` 扩展成完整浏览器框架。如果目标需要大量 DOM、navigator、canvas、WebGL、Worker、crypto 或 XHR 仿真，根据交付目标转交 `env-patch` 或 `iv8-web-reverse`。

## 已移除范围

- Cookie T/P 纯算。
- basearr 数据驱动拟合和 type=2 映射。
- sdenv/jsdom 框架工作。
- browser-rpc/JsRpc 框架工作。
- URL suffix AST 研究和 r2mKa 字节码工具链。
- 上游纯算参考资源。

本精简 skill 只用于项目骨架、同 session 材料缓存、最小本地 runtime 检查和 proxy 环境观察。

## 完成报告

完成后简短报告：

- 触达的项目根目录。
- 是否创建了 `js_reverse_cache/`。
- 创建或保留了哪些固定项目文件。
- 根目录 `challenge_payload_*` 是否保持未覆盖。
- 如果发生采集，缓存 run 目录路径是什么。
- 本地 Node runtime 是否生成 cookie，或卡在哪个缺失环境读取。
- 是否尝试了同 session 回放，以及观察到的 HTTP 状态码。
