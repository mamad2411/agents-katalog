---
name: blackbox-vuln-orchestrator
description: "授权黑盒 Web/API/CTF 漏洞研究的主入口：把范围、资产测绘、浏览器与 Burp 流量、JS/API 发现、技术栈/CVE 指纹和验证结果编排为可审计的下一步行动队列，并按证据加载现有专项漏洞 Skill。用于从零开始的黑盒测试、卡住后决定下一步、或把分散扫描结果转为验证计划；不用于无授权目标。"
---

# 黑盒漏洞编排器（主入口）

## 目的与边界

本 Skill 是**调度层**，不是大而全的 payload 集合：它用可复放证据决定下一步，随后才读取或激活适用的现有专项 Skill、项目 KB 和 MCP 工具。

仅在用户已声明授权范围的 Web/API/CTF/实验室任务中使用。把发现的新主机、第三方 SaaS、共享 IP 和历史资产视为**线索**，不是自动扩展的测试范围。默认目标是最小充分 PoC 与修复证据；不得把“系统 RCE”当作每个案例的默认成功条件。

## 必读资源与输入

1. 先读 `references/workflow.md`，执行范围、基线和状态门。
2. 读取 `references/tool-routing.md`，按 Chrome → Burp → Hunter → Kali 的顺序选工具；Kali/ARL 仅在环境预检确认可用时启用。
3. 使用 `assets/case_state.template.json` 建立或补全脱敏 case state；任何新信号、尝试、阻塞和证据路径都写入其中。
4. 先在接入/更新子 Skill 后运行离线维护检查：
   ```powershell
   python .agents/skills/blackbox-vuln-orchestrator/scripts/audit_skill_suite.py
   ```
   它校验路由、fixture、公共范围 gate 和私有历史值泄漏；不发网络请求。
5. 执行：
   ```powershell
   python .agents/skills/blackbox-vuln-orchestrator/scripts/next_action.py <case_state.json> --format markdown
   ```
   该脚本根据 `references/routing-rules.json` 生成候选路线、缺失前置条件和停止理由；它不发网络请求、不生成 payload。
6. 对排名最高且前置条件满足的**至多三条**路线，按 `references/routing-rules.json` 指向的现有专项 Skill / 项目 KB 推进。阅读相应专项 Skill 后，才可以执行该路线的验证。

## 工作流

### 0. Intake：锁定范围和成功条件

- 记录授权来源、目标、允许的主机/账户、速率限制、禁止操作和成功条件。
- 使用 Hunter scope/case 工具建立案例与范围；任何 scope 缺失、授权不明确、验证码/登录墙要求人工操作时停止自动化，转 `needs_operator`。
- 若要复用历史 CASE，先将其中的活体、凭据、token、第三方 URL 视为敏感且过期；不可将其自动带入新案例。

### 1. Baseline：先消灭误报

每个 host、身份态、路径深度至少记录：状态码、重定向链、响应长度/哈希、关键响应头、页面标题、软 404 对照和 WAF/验证码/限流分类。

没有 baseline，不得把目录枚举、扫描器命中、HTTP 200、CDN 错误页或历史 FOFA 记录视为有效端点。

### 2. 资产与攻击面：由广到窄

按 `references/tool-routing.md` 收集并关联：

- 被授权范围内的 host、端口、技术栈、公开文档、证书/被动资产线索；
- 浏览器抓到的请求、XHR/fetch、WebSocket、JS chunk、source map、OpenAPI/Swagger/GraphQL 线索；
- endpoint、HTTP 方法、参数、对象标识符、上传字段、回调 URL、认证态和权限边界。

测绘的产物必须进入 case state 的 `observations` / `surface`；发现越多不等于扫描越激进。每个新资产先过范围与 baseline 门。

### 3. 假设路由：信号决定专项 Skill

- 先运行 `stage_workplan.py`，统一确认当前阶段的工具顺序、最小产物与停止条件；它离线读取 case state，不执行目标请求。
- 运行 `next_action.py`，只选择满足前置条件且没有被证伪的候选项。
- 优先信息增益高、可回放、低副作用的路线；同一轮最多三个独立假设。
- 典型映射：对象 ID + 两身份 → `hunt-idor`；可控 URL + OAST → `hunt-ssrf`；可控 HTML/DOM sink → `hunt-xss`；版本确认 → CVE 非破坏性检测；JS/API 信号 → JS runtime/API discovery KB。
- SQLi、SSRF、文件上传、SSTI、反序列化、webshell/RCE 等高影响路线必须先有对应输入/输出链或产品指纹。它们不是默认扫描项。

### 线上目标的逆向循环

复杂线上靶场不按漏洞名称直接选 payload。先把页面、脚本、请求、响应、备用端口和错误页还原成可比较的攻击面图，再选择下一跳：

```text
FINGERPRINT → SURFACE_MAP → REVERSE → HYPOTHESIS → ENTRYPOINT
       ↑                                           ↓
       └──────── BACKTRACK ← DECISION ← PROBE ←───┘
```

`next_action.py` 的结果应优先回答：哪个 endpoint/parameter/state 是切入点、为什么它比其他入口信息增益高、第一处单变量 probe 是什么、什么响应会证伪假设、失败后 pivot 到哪里。允许的决策动作是 `DEEPEN`、`PIVOT`、`BACKTRACK`、`WAIT_FOR_SIGNAL`，而不是把 429、catch-all 302、传输超时混成“漏洞未发现”。

优先使用离线线上逆向工具：

- `scripts/online/response_diff.py`：响应分类与差异矩阵；
- `scripts/online/build_surface_graph.py`：从 case/evidence 建立 client→endpoint→parameter→auth hint 图；
- `scripts/online/hypothesis_engine.py`：从已观察 signal 生成可证伪假设；
- `scripts/online/next_pivot.py`：按信息增益排序切入点和 pivot。

统一入口可以调度 `hunt-client-reverse` 和 `hunt-api-reverse`，它们先恢复前端调用链、参数语义、token lifecycle、API schema 和状态机，再把证据交给 `hunt-*` 漏洞专项。CTF fixture 只用于规则回归；线上 case 的响应、脚本和服务差异是逆向判断的主要输入。

### 专项 Skill 的标准能力

每个专项都应具备：触发信号、入口点、所需上下文、第一探针、响应解释、DEEPEN/PIVOT/BACKTRACK 条件、误报排除、证据字段、handoff 和完成标准。XSS 先做 context/sanitizer/CSP/source-to-sink 逆向，API/IDOR 先做 schema/object/owner 差异，RCE 只能作为已确认输入链的终点。

### 4. 验证：一次实验只回答一个问题

每个实验遵循：`baseline → 受控 probe → post-baseline → oracle 比较`。

记录请求/响应的脱敏副本、时间、身份态、预期 oracle、实际结果和结论。WAF、验证码、限流、无身份对照或无 OAST 回连一律是 `INCONCLUSIVE`，不得升级为漏洞。

### 5. 链路复核与停止

确认一个 primitive 后，读取 `references/chain-review.md`，评估它可通向的**已证据支持**的凭据、数据、管理面或受控执行路径。只有链路的每一跳都有前置证据才可继续；否则创建“需要何种新信号”的待办。

把已否定的假设写入 `attempted_hypotheses`，并设置重新开启条件。所有可行候选都缺少前置条件时，输出 `WAIT_FOR_NEW_SIGNAL` / `NEEDS_OPERATOR` / `EXHAUSTED`，而不是反复扩大扫描或重复同一路径。

## CVE、外部实战库与子 Skill 的使用政策

- CVE 路由必须先确认产品、版本、暴露面和受影响版本范围；先用已有 Hunter/Nuclei 的非破坏性检测和厂商公告校验，再进入专项验证。
- GitHub、文章、案例库仅作为**参考来源**。不得整包复制未知来源的 Skill、payload、自动化脚本或绕过片段；来源、许可证、固定 revision、适用前置条件与回归 fixture 必须记录在 `references/upstream-sources.md`。
- 当前仓库已有的 `hunt-*`、`bb-methodology`、`ctf-web`、`recon-scope-triage`、`triage-validation`、`evidence-hygiene` 是首选子 Skill。缺失专题应先记录为“候选增量”，审核后才纳入路由规则。

## 资源索引

- `references/workflow.md`：状态机、证据门、输出契约。
- `references/stage-workplan.md`：阶段 → 工具顺序、产物与停止条件。
- `references/tool-routing.md`：工具预检和测绘/抓包/验证顺序。
- `references/routing-rules.json`：信号 → 专项 Skill / KB / 工具动作的可机读映射。
- `references/chain-review.md`：从已确认 primitive 到下一跳的证据审计。
- `references/upstream-sources.md`：已审计来源与接入规则。
- `references/specialist-catalog.md`：所有专项 Skill、触发门和维护 SOP。
- `references/coverage-matrix.md`：项目 KB 分类、当前覆盖和刻意不自动化的边界。
- `references/kb-coverage.json`：机读 KB 分类 → route ID 映射；审计器会验证分类、路由与本地目录同步。
- `references/technique-coverage.json`：每篇项目 Web/CTF KB 技术文件 → route ID / 状态映射；审计器会验证文件集合、路由与分类理由。
- `references/subskill-admission.md`：GitHub/案例/外部子 Skill 的准入与复审标准。
- `references/decomposition-audit.md`：独立漏洞类别与共享流程边界的定期拆分审计。
- `assets/case_state.template.json`：脱敏状态文件模板。
- `scripts/next_action.py`：离线候选路线排序器。
- `scripts/stage_workplan.py`：离线阶段工作计划输出器；不会接触目标。
- `scripts/audit_skill_suite.py`：离线路由/fixture/敏感值维护审计。
