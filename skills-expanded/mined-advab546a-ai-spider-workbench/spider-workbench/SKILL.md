---
name: spider-workbench
description: >-
  爬虫/逆向统一工作台入口（编排层，不替代具体执行 skill）。当用户开启新的爬虫/逆向任务、需要
  选择工具链、或要求"整合/统一"爬虫能力时使用：先做任务分类和工具路由，再初始化标准输出目录，
  然后按需调用具体 skill（find-crypto-entry / js-reverse-strategy / env-patch / ast-deobfuscate /
  iv8-web-reverse / web-protocol-recovery / rs-reverse / browser-hook-snippets）或 MCP
  （js_reverse_mcp_local_cloak / camoufox_reverse_mcp / proxy_mcp / miniapp_reverse_mcp /
  android_re_* / frida_mcp / mobile_pentest）。不要用它代替具体执行 skill。
---

# Spider Workbench

统一爬虫/逆向工作台的入口。目标：任何新任务都能在 3 分钟内确定"用什么工具、产出放哪、怎么验证"。

## 1. 任务分类（先回答这三个问题）
- **目标载体**：网页 Web / 小程序 / Android App / 纯协议接口？
- **主要障碍**：加密参数(sign/token) / 动态 cookie / 风控挑战(412/403/JSVMP/瑞数) / 抓包困难(SSL pinning) / 反调试？
- **交付物**：浏览器能跑通即可 / Node.js 独立脚本 / Python + iv8 采集器 / App 抓包证据？

## 2. 工具路由（决策表）
| 场景 | 执行 skill / MCP |
|---|---|
| 不确定怎么切入 | `js-reverse-strategy`（策略规划，先压"最终请求→writer→builder→entry→source"闭环） |
| 定位加密参数/签名/cookie 写入点 | `find-crypto-entry` |
| 浏览器动态调试、断点、发起栈 | `js_reverse_mcp_local_cloak`（CloakBrowser）/ `camoufox_reverse_mcp` |
| 只要观察型 hook 脚本 | `browser-hook-snippets` |
| 已知入口，跑通到 Node 沙箱 | `env-patch` |
| 混淆 JS 结构化还原 | `ast-deobfuscate` |
| 交付 Python+iv8 采集器 | `iv8-web-reverse` |
| 浏览器无关协议还原 | `web-protocol-recovery` |
| 瑞数/Rivers（$_ts/r2mKa/Cookie S/T） | `rs-reverse` |
| HTTPS 抓包/MITM/重放 | `proxy_mcp`（启动后 browser/android 全端拦截） |
| 小程序 | `miniapp_reverse_mcp` |
| Android App | `android_re_static`（静态）→ `android_re_dynamic`（动态）→ `frida_mcp` / `mobile_pentest` / `android_pentest`（hook/抓包）→ `android_re_triage`（汇总） |
| 跑 JS 验证算法 | `node_repl` |

## 3. 标准工作流（五阶段）
1. **recon 侦察**：拿到目标请求/页面，记录 URL、headers、body、cookie、生成时机。
2. **locate 定位**：用 find-crypto-entry + 浏览器 MCP 找到入口函数与调用链，固定检查点。
3. **restore 还原**：env-patch / ast-deobfuscate / iv8 把算法跑通，输出与浏览器一致的参数。
4. **collector 落地**：web-protocol-recovery / iv8-web-reverse 产出浏览器无关的 Python 采集器。
5. **verify 验证**：离线样本对拍（verify_signer_offline / 样本对比），再实测请求通过。

## 4. 输出目录约定
- 项目根：用户当前工作区（如 `D:\Documents\Spider`）。
- 统一结构：`Output/<target>/<stage>/`，stage ∈ recon|locate|restore|collector|verify。
- 中间产物（脚本、抓包、还原代码、证据）都落在这棵树里，禁止散落根目录。

## 5. 环境脚本（Windows）
- 项目 `workbench/check-env.ps1`：一键检查 runtimes / MCP 二进制 / 2828 端口 / adb / 代理端口。
- `workbench/start-firefox-reverse.ps1`：手动最小化启动 Firefox Reverse（MCP 已配 FRX_AUTOLAUNCH=0，不会自动弹窗）。
- `workbench/stop-firefox-reverse.ps1`：关闭 Firefox Reverse。

## 6. 注意事项
- 多浏览器并存：CloakBrowser / Camoufox / Firefox Reverse 是独立实例，不要混用会话。
- 抓包优先走 proxy_mcp 的规则引擎（mock/rewrite/headers），少用一次性的临时拦截脚本。
- 每次任务结束把关键证据链接到 `Output/<target>/verify/` 或 triage，便于回溯。
