---
name: web-reverse
author: null119
website: www.ztjun.fun
description: Web前端逆向工程技能：用于逆向网页前端 JS/WASM 逻辑、解混淆/脱壳、bundle 分析（Webpack/Vite/Rollup）、JS‑VM/自定义VM字节码还原、WebCrypto/自定义加密与 API 签名算法复现、source map 重建、浏览器反调试绕过、协议/请求重放与 CTF Web 题。凡用户提到“逆向某网站/还原签名或加密参数/恢复 JS 逻辑/抓包重放/VM/WASM/ob‑fuscator/JSFuck/eval‑pack”等都必须触发。本技能不用于前端开发/性能优化/通用加密教学/渗透扫描/Android 逆向。
---

# Web Reverse Engineering Skill (WEB)

> 核心原则：先定级再工具链；先事实后推断；先脱壳再分析；中文报告必须交付。

## § 目标与触发
- 本技能用于 **Web前端逆向与签名/加密复现**。
- 触发场景见前置 description；不满足则不要触发。

## § 任务输入（缺失即补充）
必须收集四字段：`target`、`objective`、`requirements`、`boundaries`。

### 通用字段
| 字段 | 说明 |
|---|---|
| `target` | URL 或文件路径；类型：WEB |
| `objective` | 密钥恢复 / 认证绕过 / 协议重建 / API签名逆向 / CTF flag / WASM反虚化 / JS-VM反虚化 |
| `requirements` | 深度：quick / standard / deep；输出格式；时间预算 |
| `boundaries` | 主动触发 Y/N；速率限制；禁止操作 |

### WEB 专属字段
| 字段 | 说明 |
|---|---|
| `url scope` | 基础URL、页面列表、登录态、所需角色 |
| `interface scope` | 目标API端点、HTTP方法/路径、API版本 |
| `runtime constraints` | 主动触发 Y/N；速率限制；禁止操作 |
| `evidence requirements` | Headers Y/N；载荷样本 Y/N；时序瀑布 Y/N；token/cookie溯源 Y/N |
| `js protection type` | 仅压缩 / 变量重命名 / 字符串加密 / CFG扁平化 / ob-fuscator.io / JSFuck / eval-pack / JS-VMP / 自定义VM / 未知 |
| `bundle system` | Webpack / Vite / Rollup / Parcel / Browserify / ESBuild / 未知 |
| `wasm present` | Y/N；如Y：独立.wasm / emscripten / wasm-pack / AssemblyScript |
| `source map available` | Y/N；内嵌 / 外部.map / Header中隐藏 |
| `anti-debug in browser` | DevTools检测 Y/N；时序检测 Y/N；debugger语句 Y/N |

### CTF 专属字段
| 字段 | 说明 |
|---|---|
| `CTF type` | web / crypto / rev |
| `flag format` | FLAG{...} / CTF{...} / 自定义正则 |
| `known hints` | 题目描述/提示 |
| `solver output` | flag字符串 / 可用exploit / 签名重放脚本 |

## § 安全与授权边界
- 仅在授权范围内逆向分析；不越权、不扩域。
- 禁止执行payload样本、触发在线漏洞利用、在沙箱外导出凭证。
- 外部平台/环境权限边界必须请求确认。

## § 输出要求（强制）
- 必须产出：`web_replay.js`、`Reverse_Report_CN.md`。
- 视情况追加：`deobf_clean.js`、`vm_opcodes.txt`、`wasm_analysis.wat`、`solver.py`、`crypto_params.json`、`token_flow.md`。

## § 证据与结论规则
- 高置信结论需 ≥2 种独立证据交叉验证。
- 单一工具结论标注 `LOW CONFIDENCE`。
- 每项结论附证据锚点：bundle chunk/行号、网络请求URL、JS函数名、xref。
- 输出必须分区：`FACTS`、`INFERENCES`、`UNKNOWNS`。

## § 防护等级（T0–T7）与处理策略
| 等级 | 模式 | 主要方法 |
|---|---|---|
| T0 | 仅压缩 | 美化 + 静态阅读 |
| T1 | 变量重命名 / 死代码注入 | AST重命名 + 静态阅读 |
| T2 | ob-fuscator.io / 字符串加密 / CFG扁平化 | 反混淆器 + 运行时hook |
| T3 | eval-packing / JSFuck / JJencode / aaencode | 解包 → T1/T2处理 |
| T4 | JS-VMP / 自定义VM | VM调度器映射 + opcode追踪 |
| T5 | WASM核心 | wasm-dis + IDA/Ghidra + 运行时hook |
| T6 | T4+T5混合 | 顺序：JS-VM反虚化 → WASM逆向 |
| T7 | 多重嵌套（T2+T4+T5） | 分层剥离：外层混淆→VM→WASM |

**强制：** 工具链选择前先完成T0–T7定级；未脱壳/未反混淆/未反虚化不得下结论。

## § 自动分流（JS Protection Triage）
1. DevTools → Sources：列出所有 .js/.mjs bundle
2. 单bundle >500KB → 疑似 Webpack/Rollup
3. 抽查可读性：可读变量名=仅压缩；_0x...=混淆/重命名
4. 搜索模式：debugger循环/JSFuck/eval pack/CFG扁平化
5. 检查 .wasm fetch / WebAssembly.instantiate
6. 检查大switch + opcode数组 → JS-VMP/自定义VM
7. 查找 sourceMappingURL
8. 识别框架指纹：React/Vue/Angular
9. 检查 Service Worker 注册
10. 检查 WebSocket 二进制帧

## § 工具编排
**首选：** `chrome-devtools-mcp`
- 网络捕获、JS source mapping、API重放、storage/token/WebSocket追踪、DevTools hook注入

**优先链**
- WEB基础：`chrome-devtools-mcp → 静态JS美化 → API重放`
- WEB混淆：`chrome-devtools-mcp → 反混淆 → 运行时hook → 静态验证`
- Webpack/Vite：`chrome-devtools-mcp → bundle拆分 → chunk映射 → 入口点追踪`
- JS-VMP/VM：`chrome-devtools-mcp → VM调度器定位 → opcode映射 → AST变换 → 运行时追踪`
- WASM：`chrome-devtools-mcp → wasm-dis/wasm2c → IDA/Ghidra → 运行时hook`
- **疑似题面/服务端漂移**：`线上资源指纹 → 历史题解入口对照 → 真实点击流验证 → 协议流验证`

**Fallback**
- DevTools不可用：声明阻塞 → 请求代理日志/HAR。

## § 标准流程（6步）
**Step 1 — 上下文拆解：** 评分路线（可行性/信号/风险 0-3）→ 选择主路径 + fallback。
**Step 2 — 环境检查：** DevTools可用、作用域/登录态/速率限制确认。
**Step 3 — 全局三角：** 定级T0–T7、识别bundle、枚举API、检查source map/WASM/SW/框架指纹。
**Step 4 — 关键路径：** 页面加载JS → 初始化 → 认证/加密模块 → sign() 调用点。
**Step 5 — 深度分析：** 反混淆/反虚化后数据流与参数生成逻辑。
**Step 6 — 动态验证：** hooks捕获 + 重放脚本验证签名一致性。

## § 专项流程：Drift Check
当用户提供历史题解、历史脚本路径，或你发现“当前线上行为与公开解法明显不一致”时，必须先跑一次漂移验证，再决定是否继续深挖客户端。

### Drift Check 最小动作集
1. 抓当前题页 HTML 指纹
2. 枚举当前加载的 script/link/API 资源
3. 直接请求历史题解常见入口与旧资源路径
4. 对照当前资源路径与历史文章/脚本路径是否一致
5. 跑真实点击流与协议流，确认当前线上实际失败点

### Drift Check 产物
- 当前题页 URL 与 HTML 哈希
- 当前 script/API 资源列表
- 旧入口可用性矩阵：`200 / 404 / 500 / redirect`
- 结论分级：
  - `NO DRIFT SIGNAL`
  - `POSSIBLE DRIFT`
  - `HIGH PROBABILITY DRIFT`

### Drift Check 判定规则
- 若旧入口 404/500，且真实点击流与历史公开解法期望不一致，至少标 `POSSIBLE DRIFT`
- 若客户端显式状态已压缩到最小仍无法解释失败，同时旧入口失效，标 `HIGH PROBABILITY DRIFT`

## § 参考资料（按需加载）
- `references/hooks.md`：网络/存储/反调试/WebCrypto/CryptoJS hook 代码
- `references/deobf.md`：T1–T3 反混淆与解包流程
- `references/vm_wasm.md`：JS-VM / WASM 反虚化步骤
- `references/replay.md`：协议重建与 `web_replay.js` 模板
- `references/ctf.md`：CTF 快速三角与交付物要求

## § 交付物模板
### Reverse_Report_CN.md 结构
1. 任务摘要
2. 核心发现（≤5项）
3. 证据表
4. 调用链
5. 风险与影响
6. FACTS / INFERENCES / UNKNOWNS
7. 下一步行动
8. 交付物清单
9. 复现步骤

### web_replay.js 要求
- 可直接 `node web_replay.js`
- 包含签名算法还原与请求重放
- 注明关键参数来源（key/token/nonce/ts）

## § 可复用实验模板

### 1. Signer Export + Minimal Trace
适用：已经定位到 runtime signer，但不确定它到底读了哪些输入。

动作：
- 对 `eval` / 动态 bundle 做最小 patch
- 导出 signer 入口与少量 helper
- 只记录：
  - signer 输入
  - signer 输出
  - 请求发出前的 cookie / URL / 少量动态全局
- 禁止一上来做全量 opcode 日志，优先做轻量 trace

产物：
- `trace_*.py`
- `trace_*.out.json`

### 2. Dynamic Global Injection Experiment
适用：服务端响应会下发 `k` / `nonce` / 动态全局名，怀疑这些值影响下一次请求。

动作：
- 收集真实点击流里每页响应下发的动态值
- 分别注入候选值
- 重新生成 fresh URL
- 记录请求结果矩阵

产物：
- `experiment_*_variants.py`
- `experiment_*_variants.out.json`

### 3. Scope Snapshot Diff
适用：`window` / storage / cookie 都看过了，怀疑还存在模块态或闭包态。

动作：
- 在运行时注入一个最小快照接口
- 快照范围：
  - 可访问的模块级 primitive / string / array 摘要
  - 关键闭包返回值摘要
- 只在关键请求前抓快照
- 自动比较相邻页面或相邻请求的差分

产物：
- `trace_scope_snap.py`
- `trace_scope_snap.out.json`

### 4. Browser / Protocol Consistency Matrix
适用：怀疑“浏览器里成功、协议层失败”或“自动化栈和真实点击流不一致”。

动作：
- 至少比较三条链路：
  - 真实点击流
  - browser-native `fetch`
  - 协议层 replay
- 若三者一致，则优先排除“网络栈差异”分支

结论要求：
- 必须明确写出哪几条链路一致，哪几条不一致
- 不得只凭单条链路下结论

## § 结果声明规则
- 未确认项写入 UNKNOWNS；给出下一步操作。
- 时间预算内空结果：声明空结果 + 已检查内容 + 次优路线。

## § 质量门槛（完成条件）
- 防护定级完成；关键层已脱壳/反混淆/反虚化。
- 重放脚本与浏览器签名一致。
- 证据锚点齐全，可复现。
- 若存在历史题解或旧入口，已明确完成一次 `Drift Check` 并给出分级结论。

