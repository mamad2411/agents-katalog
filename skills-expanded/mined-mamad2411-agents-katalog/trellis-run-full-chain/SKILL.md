---
name: trellis-run-full-chain
description: "Run full-chain behavior verification across UI + API + DB — cross-layer (browser driver + HTTP client + DB client), NOT frontend-only e2e like Playwright/Cypress test suites. Input is a 场景-路径-期望 scenario table; executes each row, logs pass/fail, and restores test data when feasible. Triggers: 「跑全链路」「全链路测试」「跨层验证」「跑E2E」「端到端验证」「自动化测试场景」「跑场景测试」「e2e test」. Not for lint/unit/spec-only (use trellis-check); not for frontend-only e2e suites."
---

# Run Full-Chain Verification — 跨层自动化验证

以"场景-路径-期望"三列表为输入，逐条跨层执行并验证：UI 驱动 + HTTP 调用 + DB 断言三种能力配合使用。最后汇总结果与**尽力而为**的数据恢复。

> **何时用**：PR 前 UAT、功能端到端验收、单测覆盖不到的跨层流程验证。
> **何时不用**：只跑 lint/typecheck/spec 合规（去 `trellis-check`）；只做 PRD↔代码静态对照（去 `trellis-check-all`）。

---

## 本 skill 的定位

skill 只描述**方法论骨架**：三列表场景设计、跨层交叉验证、Toast 观测、回滚边界、偏差立停。所有 URL / header / token 键名 / 表名 / 测试账号 / 可用测试数据等 **项目特定**信息应写在项目的 E2E playbook 里（见下节）。skill 执行时优先加载它；本次运行探测/学到的新条目会在 Step 5.5 以 diff 形式提交给用户确认后回写 playbook，**下次直接复用，无需再探测**。

---

## 项目 Playbook（自动沉淀）

固定位置：

```
.trellis/spec/guides/e2e-playbook.md
```

Playbook 内容范围（**跨任务可复用的环境常量**，不含具体场景）：

- **URL 模板**：前端 dev server、后端 API base、账号切换入口
- **Auth header 模板**：`authorization` 形式、是否需要自定义 header（如 dev-mode 开关）、token 存储键名（sessionStorage/localStorage/cookie）
- **测试数据指纹**：哪些项目/用户/租户可以用；哪些不能碰（生产数据、他人在用的数据）
- **表命名约定**：主要业务表、审计/流转日志表、幂等去重表
- **不可逆副作用清单**：哪些动作会触发外部通知 / 上链 / MQ 投递 / 缓存污染
- **常见数据重置方式**：有无 truncate-and-seed 脚本、快照恢复、savepoint 惯例

**沉淀机制**：

- **已有 playbook**：Step 0 加载；Step 0–4 执行中若发现 playbook 未记录或与实际不一致的条目，标记进"待沉淀缓存"；Step 5.5 汇总成 diff 让用户确认后增量写入（**append-only 心态**，默认不删旧条目；冲突项单列供人工裁决）
- **无 playbook**：按通用流程探测；Step 5.5 把整份探测结果作为"全新 playbook" diff 给用户，确认后创建文件

**不纳入 playbook 的内容**（避免污染）：

- 具体测试场景表、任务级一次性测试数据（如本次新建的项目 ID）、PRD 推导出的断言 — 这些留在任务目录 `.trellis/tasks/<task>/research/` 或任务报告里

---

## 能力矩阵（Step 0 自检用）

每一行是一种测试能力。**首选**不可用时逐级降级；**不可用时**仍应让 skill 能跑（哪怕只跑部分场景）。

| 能力 | 首选工具 | 备选 | 不可用时降级 |
|------|---------|------|-------------|
| UI 驱动 | Playwright MCP（`browser_*` 工具族） | Selenium / Puppeteer CLI；手动 Chrome DevTools 协议 | 让用户在浏览器里手点，把观察到的 toast/状态粘回对话 |
| HTTP 调用 | `curl` | HTTPie / Postman CLI | 让用户手调并粘贴响应 |
| DB 断言 | 对应数据库的 MCP（MySQL / PG / SQLite 等） | `mysql` / `psql` / `sqlite3` CLI | 让用户手查并粘贴结果；或 skill 只做 UI+API 层断言 |
| 抓 Auth 信息 | 浏览器里 `browser_evaluate` 读 storage / cookie | 让用户登录后手动粘贴 token | 同左 |
| 抓真实 header | `browser_network_requests` 观察一次真实 XHR | 浏览器 DevTools Network 截图 | 让用户粘贴任一 XHR 的请求头 |

**缺能力时的行为**：
- Step 0 把缺项列给用户，附推荐安装/启用方式（"首选 X，可参考 <官方链接>；不装也可以用 Y 替代；完全没有时我会让你手点并把结果粘回来"）
- 不要擅自跳过；让用户选"安装 / 降级 / 跳过该类场景"

---

## 执行步骤

### Step 0: 环境自检 + 加载 Playbook + 抓登录态

1. **读 playbook**（`.trellis/spec/guides/e2e-playbook.md`，若存在），拿到 URL/header/测试数据候选。同时**初始化"待沉淀缓存"**——后续 Step 0–4 探测到的"playbook 未记录的新条目 / 与 playbook 不一致的条目"都追加进来，Step 5.5 用
2. **能力矩阵自检**（上表），缺项时暂停
3. **前后端可达性**：`curl -sI <frontend-url>`、`curl -sI <backend-api-base>` — 若 URL 由探测得来（playbook 未覆盖或不一致），写入待沉淀缓存
4. **抓登录态 & header 模板**：通过浏览器驱动读 token（playbook 未指明则列出所有 storage keys 供识别），再触发一次真实业务 XHR，从 `browser_network_requests` 观察所需 header，作为后续 `curl` 模板。**确认后的 token 键名 / header 模板**写入待沉淀缓存

```js
// 通用 token 探测（不要猜键名）
() => ({
  sessionKeys: Object.keys(sessionStorage),
  localKeys: Object.keys(localStorage),
  cookies: document.cookie,
})
```

### Step 1: 构造/加载场景表

**首选**：用户已经整理好 "场景 / 路径 / 期望" 三列表。照抄即可。

**次选：列全候选后交用户抉择**

从任务 `prd.md` 列出**所有可端到端验证**的场景候选，来源包括但不限于：

- Goal / Requirements — 功能目标与需求项
- Acceptance Criteria — 验收标准（通常 1:1 映射为场景）
- Business Rules — 校验 / 容错 / 边界
- 实现决策（如 DEC 节）— 运行时有副作用的决策（数据迁移、文件生成、快照回写等）
- UI 交互细节 — Toast / 弹窗 / 状态流转 / 权限隐藏
- 跨层数据流 — 前端 → API → DB 链路
- 副作用点 — 外部通知 / 异步回写 / 幂等键

**不自行筛选**：不以"成本高"、"静态已验证"、"非核心"、"不好构造"为由提前裁掉候选。把所有可想到的场景都摆上桌。

输出完整场景表（模板如下）并**交用户抉择**：

| 场景 ID | 路径类型 | 操作 | 期望 |
|---------|---------|------|------|
| S1 | UI | 走页面 X → 点按钮 Y → 填 Z | 弹窗/状态/提示 A |
| S2 | API | POST <path> body `{...}` | 返回 code=0，DB 字段 X=Y |
| S3 | DB+API | 先查基线 → 调接口 → 再查 | 某字段从 X 变 Y + 新流转日志 `Z` |
| S4 | 跨层 | UI 触发 → 后端副作用 → DB 对账 | 所有层一致 |

每条必须有明确的**可观察信号**（UI 文案、HTTP code、DB 字段值），避免 "应该能跑"。

**可推荐**：附一份"建议跑 / 可选 / 可跳过"分级（附理由），供用户快速决策。但必须让用户明确圈选后才进 Step 2，不得替用户决定。

超过 10 条或需分批时尤其要问优先级或时间预算。

### Step 2: 识别测试数据 + 基线设计（可隔离优先）

**优先可隔离**：测试前就避免污染共享数据，而不是事后清理。依次尝试：

1. **独立测试数据 / 租户** — 用 playbook 里列出的"可用测试数据"，或为本次测试新建一条专用项目/任务/用户
2. **事务 savepoint / rollback** — 数据库支持时（PG、支持 BEGIN 的 MySQL 会话等）
3. **快照恢复** — 有 sandbox/snapshot 机制的环境
4. **共享数据 + 手动回滚**（底线） — 前提是场景改动有限、回滚步骤清晰

对每个场景：

1. **基线快照**：从 DB 查出被测目标的当前状态（状态、计数、外键引用），作为"Before"写入对话上下文
2. **回滚信息**：对每个会被改动的字段，记录原值 / 原关联 ID，便于 UPDATE 回去
3. **不可逆副作用清单**（见下节）必须在动手前**显式列出**

#### 不可逆副作用清单（执行前必检）

场景如果可能触发以下任一，**事前告知用户**，并问清楚"是否可接受"：

- 发送外部通知（邮件、IM、Webhook）
- 推送到 MQ / 事件总线（被其他系统消费）
- 写入流水账户 / 区块链 / 审计不可删表
- 调用第三方付费 API（短信、支付、邮件发送）
- 更新只读缓存的上游数据（缓存 TTL 内持续污染）
- 写入生产级日志存储（ELK、Datadog），不能擦除

**原则**：如果清单非空且用户未确认，不要跑该场景。

### Step 3: 逐场景执行

按 ID 顺序执行每个场景，每条遵循以下模板：

```markdown
#### Sx: <场景名>
- Path: <UI/API/DB/跨层>
- Pre: <基线>（从 DB 查到的 Before）
- Act:
  - UI: 浏览器驱动动作（snapshot → click/type → wait）
  - API: curl 带 header 调接口
  - DB: 用 DB 客户端预改数据（仅当场景要求，如临时改状态模拟某前置条件）
- Expect:
  - UI: 截图 / 文本快照 / Toast 观测
  - API: 返回体 code/msg 匹配
  - DB: 字段变化 + 审计/日志条目新增
- Result: ✅ / ❌ + 差异说明
- Restore: <必要的 UPDATE 恢复现场>
```

**UI 细节**：

- Toast 文案通常 2-3 秒自动消失，**别等**——先装 MutationObserver 抓文案，再触发点击：

  ```js
  window.__toasts = [];
  new MutationObserver(() => {
    for (const el of document.querySelectorAll('*')) {
      const t = el.textContent?.trim() || '';
      if (t.includes('<关键字>') && t.length < 200 && el.children.length < 3) {
        if (!window.__toasts.includes(t)) window.__toasts.push(t);
      }
    }
  }).observe(document.body, { childList: true, subtree: true });
  // 再触发按钮点击
  ```

- 下拉/autocomplete 可能依赖聚焦事件。先 click 让输入框聚焦，再 type，避免 fill 类 API 绕过 focus handler 而不触发下拉

**API 细节**：

- Header **完全对齐**前端抓到的真实请求（authorization、自定义开关头、trace ID）。401 多是 header 差一条，别去改服务端
- 回调/Webhook 类接口通常**不带用户 token**（外部系统身份），业务接口必须带
- 幂等键（requestId / externalNo / idempotency-key）**每次用新值**，否则被去重机制吞掉

**DB 细节**：

- 查询用 `SELECT ... AS <alias>` 让返回 key 可读
- 写 DML 前 `SELECT` 一次记录基线；写后 `SELECT` 一次对比
- 某些 MCP / 客户端不支持 multi-statement，**一次只发一条 SQL**

### Step 4: 发现偏差时暂停

任意一条 ❌：**立即暂停**，向用户说明：

- 场景 ID + 具体差异（文案差一个字 / 状态没变 / 日志没新增）
- **先排部署滞后再排代码 BUG**：若行为完全像旧代码，先核验部署版本（git hash / artifact timestamp / 健康检查版本端点），再改代码
- 建议下一步（改代码 / 重新部署 / 换测试数据 / 调整场景）

具体的"部署滞后"诊断命令因技术栈而异，见文末附录 B。

不要硬跑完再总结 — 早发现早暂停更省时间。

### Step 5: 尽力恢复 + 显式告知

> 回滚是**尽力而为**，不是充要条件。Step 2 的隔离设计做得越好，这一步越轻。

用前面备份的基线逐条 UPDATE 回去；结束后**再查一次**确认每条改动都复原。最终报告必须列出：

- ✅ 已恢复的改动（条数 + 影响表）
- ⚠️ 未能完全恢复 / 超出能力范围的项（外部通知、MQ、上链……）
- 🔧 用户需自行处理的善后（如通知接收方忽略测试记录）

**警告**：
- 别盲目 `UPDATE ... WHERE id=...` — 并发环境下别人可能已经改过，回滚反而破坏后续工作；先比对"当前值 vs 测试后值"再决定是否需要恢复
- 触发器 / 物化视图 / 异步 outbox 即便主表回滚，**下游可能已发出副作用**，需在报告里强调

### Step 5.5: Playbook 沉淀（diff 确认）

把 Step 0–4 收集的"待沉淀缓存"与现有 `.trellis/spec/guides/e2e-playbook.md` 做比对，以 diff 清单形式列给用户确认后再写入。**用户未确认之前不写文件。**

**diff 预览模板**：

```markdown
## 📒 Playbook 沉淀预览（待确认）

### ➕ 新增（playbook 无此条目）
- 前端 dev server: `http://localhost:5173`
- token 存储位置: `sessionStorage["iqs-token"]`
- 业务 XHR 必带 header: `authorization: Bearer …`, `x-dev-mode: 1`
- 流转日志表: `iqs_dispatch_log`
- 不可逆副作用 / 飞书审批: `POST /fs/approve` 会触发真实飞书通知

### ✏️ 变更（playbook 已有但与实测不一致）
- 后端 API base: `http://localhost:8080/api` → `http://localhost:8081/api`（旧值端口疑似过期）

### ⚠️ 冲突（需人工裁决，默认不写）
- playbook 记录 token 在 `localStorage`，本次实测在 `sessionStorage`。可能是环境差异，请判断是否覆盖

### ⏸️ 保持不变（已与 playbook 一致，仅列出确认）
- 测试账号列表、常见数据重置方式
```

**用户回应处理**：

- ✅ 全部接受 → 写入 `.trellis/spec/guides/e2e-playbook.md`（不存在则 Write 新建；存在则对应条目用 Edit 增补/修改，**不删除旧条目**）
- 🟨 部分接受 → 按用户圈选的条目写入
- ❌ 拒绝 / 跳过 → 不写文件，仅在 Step 6 汇总里标注"N 条新发现未沉淀"
- **diff 为空**（playbook 已完备） → 静默跳过本步，不打扰用户

**原则**：

- 沉淀的只能是**跨任务可复用**的环境常量；**任务级一次性数据**（新建的项目 ID、本次构造的用例、临时测试凭据）**不进 playbook**
- 冲突项（⚠️）不擅自覆盖 — 让用户判断是环境差异还是 playbook 过期
- append-only 心态：旧条目只增不删；用户明确要删才动

### Step 6: 汇总报告

```markdown
## 🎯 E2E 测试汇总

| 场景 | 路径 | 期望 | 结果 |
|------|------|------|:---:|
| S1 | UI | ... | ✅ |
| S2 | API+DB | ... | ✅ |
| S3 | 跨层 | ... | ❌：<差异说明> |

### 覆盖统计
- 通过：X / 总 N
- 失败：Y（需修复）
- 跳过：Z（未具备前置条件）

### 数据影响
- 已恢复：<N 条 / 涉及表>
- 未恢复 / 不可逆：<如果有>
- 需用户善后：<如果有>

### Playbook 同步
- 写入条目：<M 条 / 文件路径>（或"N 条新发现未沉淀（用户跳过）"，或"无变化"）
- 未解决冲突：<如果有，注明待用户裁决的项>

### 建议下一步
- <根据失败/跳过场景的具体建议>
```

---

## 核心原则

| 原则 | 为什么 |
|------|--------|
| **先对齐场景再动手** | "想当然测" = 白跑；文案/状态一个字都要写入期望 |
| **跨层交叉验证** | UI 看绿 ≠ DB 真的改了；只查 DB ≠ 用户能用 |
| **Header 与真实请求一致** | 401 大多是 header 差一个，不是服务端 bug |
| **隔离优先于回滚** | 事前设计可隔离 > 事后打扫现场 |
| **差异立即停** | 一条 ❌ 可能说明整批假设都错了，别继续堆无效结果 |

---

## 反模式（避免）

- ❌ 浏览器驱动只截图就下结论 — 文案可能已消失 / 被 overlay 遮挡，必须文本快照或 DOM 断言
- ❌ Toast 断言用 `sleep + screenshot` — 2-3s 够消失的，必须 MutationObserver 实时抓
- ❌ 跑完忘记恢复 — 污染后续测试，特别是状态类的"临时改成 X"
- ❌ 幂等键重用 — 被去重机制返回 success，但实际没执行任何逻辑
- ❌ 发现一处失败就假设整批代码错 — 先核验部署版本，再怀疑代码
- ❌ 场景表里写"大致正常" / "应该能用" — 没有可观察信号就无法判定通过
- ❌ 把 DB 写操作塞进一个 multi-statement string — 拆开更稳
- ❌ 跳过 Step 0 环境自检直接点按钮 — 浪费好几轮才发现 token 失效或未登录
- ❌ 跳过"不可逆副作用清单"— 测完才发现发了真的飞书通知，救不回来
- ❌ 习惯性跳过 Step 5.5 沉淀 — playbook 永远空白，下次还得从零探测
- ❌ 把任务级一次性数据（新建的项目 ID / 本次才构造的用例）塞进 playbook — 污染跨任务复用，下次用错数据

---

## 与其他入口的区别

| 入口 | 形态 | 用途 |
|------|------|------|
| `trellis-check` | skill | lint / typecheck / spec 规范 |
| `trellis-check-all` | skill | PRD→代码 静态对照 + 假设验证 |
| **`trellis-run-full-chain`** | skill（本技能）| **运行时行为跨层验证（UI+API+DB）** |
| `trellis-verify-prd` | skill | PRD↔源需求文档对账 |

---

## 附录 A：通用诊断片段

### A.1 MutationObserver 抓 Toast（已在 Step 3 给出，此处为参考）

见 Step 3 "UI 细节" 段。

### A.2 Playwright 聚焦后输入

```js
// 错：fill 可能绕过 focus handler
// await page.fill('#autocomplete', 'keyword');

// 对：先 click 聚焦，再 type 触发 input 事件
await page.click('#autocomplete');
await page.type('#autocomplete', 'keyword');
```

### A.3 API 通过浏览器抓出的 header 直接转 curl

```js
// browser_evaluate
() => {
  const req = performance.getEntriesByType('resource')
    .filter(e => e.name.includes('/api/'))[0];
  return req?.name;
}
```

Playwright `browser_network_requests` 直接给出已发的请求 header 列表，复制模板即可。

---

## 附录 B：部署滞后排查（按技术栈）

行为像旧代码时，先核对部署版本再改代码。以下按栈列常见诊断：

### Java / JVM

```bash
# 字节码是否含新逻辑
javap -c -p <class-file> | grep -A 2 <new-method-or-keyword>

# 进程启动时间 vs class 文件 mtime
ps -eo pid,lstart,cmd | grep <app>
stat <path-to-class-or-jar>
```

- IDE 热重载（JRebel / Spring DevTools）对 **lambda / method reference** 经常失败；让用户执行 IDE 的 "Rebuild Project" 或重启应用

### Node / 前端（Vite / Webpack / Next）

- Vite HMR 对部分改动（路由定义、全局 state 初始化）不触发重载，需要**强制刷新浏览器（Ctrl/Cmd + Shift + R）**
- DevTools Network 看 bundle/chunk 的 hash 是否变化；没变就是浏览器在用缓存
- Service Worker 缓存：Application → Service Workers → Unregister

### Go

```bash
# 进程编译时间
go version -m <binary> | grep build
# 对比 source mtime 看是否重编译
```

### Python / Ruby

- 解释型语言理论上重启即新，但 `gunicorn` / `uWSGI` 有 worker 预载；看进程启动时间、用 `kill -HUP` 重载

### 通用

- 部署流水线是否真的把你的 commit 推上了 — 看生产环境的版本端点（`/version` / `/health` / `/actuator/info`），对比 `git rev-parse HEAD`
- 容器化场景：容器镜像 tag 是否更新、pod 是否真的换了（`kubectl get pods -o wide` 看 `AGE` 和 `IMAGE`）
