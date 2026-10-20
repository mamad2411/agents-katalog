---
name: security-app-websocket
canonical_id: security.app.websocket
aliases: [websocket-security, ws-security, realtime-security, sse-security]
version: 1.0.0
status: stable
created_date: 2026-05-25
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
forbidden-tools: WebFetch
manual_gate_required: false
disable-model-invocation: false
standards_versions:
  - OWASP WebSocket Security Cheat Sheet: living reference, checked 2026-05-25
  - OWASP ASVS: 5.0 (V17 WebRTC + V4 API + V8 Authorization)
  - RFC 6455: 2011 (WebSocket Protocol)
  - RFC 8441: 2018 (Bootstrapping WebSockets with HTTP/2)
sensitive_data_rules:
  never_read: [".env*", "secrets/**", "*.pem", "*.key"]
  redact_on_output: ["session tokens", "WS frame payload PII", "real user ids"]
upstream:
  - appsec-security-orchestrator
  - security-governance-threat-modeling
downstream:
  - security-remediation
  - appsec-security-orchestrator (back with findings)
description: >-
  WebSocket and Server-Sent Events security overlay - handshake authentication, origin verification, message-level validation, rate limiting, channel authorization, heartbeat handling, frame size limits, disconnect semantics, and frame-level log discipline (HTTP access logs cover only the upgrade request).
trigger_phrases:
  - WebSocket security / WS security / 长连接安全
  - SSE security / server-sent events
  - Socket.IO / SignalR / Phoenix Channels / ActionCable security
  - realtime channel auth / message validation
  - WebSocket DoS / message rate limit / frame size
---

# Security App — WebSocket and Realtime Channels

## 1. Mission

HTTP access log 只覆盖 **upgrade request**，不覆盖后续 frames。所以传统 WAF / IDS / rate limit 对 WebSocket 失效。本 skill 覆盖：handshake auth / origin / message validation / rate / channel authz / heartbeat / frame size / disconnect / 专项日志。

**职责边界**：
- **owns**: WebSocket / SSE / Socket.IO / SignalR specific concerns
- **不做**: 一般 web auth（归 orchestrator V6/V7/V8）；不做协议层加密（TLS 走 V12）

---

## 2. Activation Triggers

| Trigger | Action |
|---|---|
| 项目用 ws:// / wss:// | 默认激活 |
| 项目用 Socket.IO / SignalR / Phoenix Channels / Action Cable | 激活 + 框架特定 |
| 项目用 Server-Sent Events (EventSource) | 激活 SSE-specific section |
| 项目用 long-polling 模拟 realtime | 激活 polling-specific |
| Chat / collaboration / live trading / notification feed | 升级深度审 |

---

## 3. Standard Workflow

```
Step 1  连接 inventory
        → 列所有 ws:// / wss:// endpoint
        → 列 channel / topic / room 设计
        → 列 message types + payload schema
        → 列 expected concurrent connections + per-user limit

Step 2  Handshake authentication review
        → Auth via cookie (with Secure + HttpOnly + SameSite=Strict)? ← 默认推荐
        → Auth via subprotocol header? ← 可，但避免 token in URL
        → Auth via custom message after open? ← 必须 immediate enforced + close on fail
        → 禁止：token in URL query string（会进 HTTP log + browser history + referer）

Step 3  Origin verification
        → 服务端必须验证 Origin header
        → Origin allowlist（不接受 wildcard 除非有意）
        → CSWSH (Cross-Site WebSocket Hijacking) 防护
        → 注意：non-browser client（CLI / mobile native）没有 Origin，需替代凭证

Step 4  Channel / room authorization
        → 每个 subscribe 操作 server-side 校验：user has access to channel?
        → Channel naming 不依赖 hard-to-guess pattern（不是 security）
        → Wildcard subscribe（"subscribe to all rooms"）需 explicit admin role
        → Channel join 失败 close connection 或 send error frame（按设计）

Step 5  Message-level validation
        → 每条 inbound frame 按 schema validate（如 JSON Schema / Zod / proto）
        → Validate message type + actor + target + content
        → 不允许 client 自报 user_id；用 session-derived
        → SQL injection / XSS / command injection in frame payload 同 HTTP 一致

Step 6  Rate limiting (frame-level, not connection-level)
        → Per-connection: msg/sec cap（如 10/sec）
        → Per-user: msg/sec across all connections
        → Per-channel: msg/sec broadcast cap
        → Per-IP: max concurrent connections
        → 超 cap 行为：drop frame / close connection / temp ban

Step 7  Frame size limits
        → Max single frame size（如 64 KB default，业务大数据走 HTTP）
        → Max queued unsent frames（防慢消费者 DoS）
        → Reject oversized frames immediately（不 buffer）

Step 8  Idle / heartbeat / timeout
        → Server-side idle timeout（如 60s no message）
        → Heartbeat / ping-pong cadence（detect dead connection）
        → Max connection lifetime（force re-auth after N 分钟）

Step 9  Disconnect semantics
        → On auth expiry: close connection + 客户端 reconnect with fresh token
        → On user logout: server actively close all user 的 connections
        → On tenant switch / privilege change: revoke + close

Step 10 Logging discipline（HTTP access log 不够）
        → Connection open log: user / IP / Origin / subprotocol / time
        → Connection close log: reason / duration / bytes sent/received / frame count
        → Auth fail log: detailed
        → Rate limit hit log: connection + user + cap exceeded
        → Frame schema fail log: redacted snippet
        → 注意：log 不含 raw frame body（除非 redact 后用于 debugging）

Step 11 Backpressure & memory
        → Slow consumer detection（client 不 ACK / 不读）→ close
        → Per-connection buffer limit
        → Server memory total cap for WS subsystem

Step 12 Framework-specific
        → Socket.IO: namespace + room + middleware order
        → SignalR: Hub authorization attribute + connection lifetime
        → Phoenix Channels: join authorize callback + intercept
        → Action Cable: identified_by + channel authorization

Step 13 SSE-specific
        → SSE 是 HTTP，所以 access log 部分覆盖
        → 但 `text/event-stream` 长连接 → 同样需 idle timeout / rate / per-connection limit
        → SSE 是单向（server → client）；client 用 HTTP POST 走另一条 channel
        → SSE auth = HTTP auth + 同 origin policy

Step 14 输出 + 路由（权威契约见 §7 Output Contract + §7.1 Overlay Evidence Contract）
        → Findings 全部走 `appsec-sdk finding.add`（canonical；不直写 .appsec/findings/**）→ security-remediation
        → `appsec-sdk overlay.activate <tag> websocket` + 写 overlay-websocket/checklist.yaml（§7.1，缺则 release BLOCK）
        → 更新 SECURITY.md WebSocket section + AppSec Release Evidence §12 叠加层
```

---

## 4. CSWSH (Cross-Site WebSocket Hijacking) 详解

WebSocket handshake 是 HTTP upgrade，**不**受 CORS 保护。如果 server 仅靠 cookie auth 且不验 Origin：

```
attacker.com → JavaScript → new WebSocket('wss://victim.com/api')
              → browser 自动带 victim.com 的 cookie
              → server 看到合法 cookie，开 connection
              → attacker.com 现在能 send/receive frames as victim user
```

**Defense**（必须组合）：
1. Server 校验 `Origin` header against allowlist
2. CSRF-token-in-subprotocol（额外保险）
3. Connection-level token（不只 cookie）

---

## 5. Hard Rules

- ❌ **不**把 token 放 URL query string（会进 access log / browser history / referer）
- ❌ **不**信任 client-reported user_id / tenant_id（永远 session-derived）
- ❌ **不**忽略 Origin 验证（CSWSH 默认开）
- ❌ **不**让 frame size unbounded（DoS）
- ❌ **不**让 idle connection 永久挂着（资源耗尽）
- ❌ **不**让 channel subscribe wildcard 无 admin 校验
- ❌ **不**靠 HTTP access log 监控 WS frame activity
- ❌ **不**让 frame schema validation 失败时只 log 不 close（attacker 会继续探测）
- ❌ **不**log raw frame payload（PII / token / 凭证泄露风险）
- ❌ **不**让 logout 留下未 close 的 WS connections

---

## 6. Anti-patterns

- ❌ "WSS = secure" — 加密是 baseline，认证/授权/校验都要
- ❌ "Cookie auth 够了" — CSWSH 攻击专门绕过
- ❌ "Origin 容易伪造" — 浏览器 client Origin 强制；非浏览器 client 需替代 token
- ❌ "Channel naming 用 UUID 就不被发现" — security through obscurity，不是 authz
- ❌ "Rate limit 在 connection 层就行" — 每 connection 可发无限 frame
- ❌ "Frame schema 用 JSON.parse 接住即可" — 必须 schema validate + business rule check
- ❌ "Idle 不关，省 reconnect cost" — 内存 + connection 资源 + auth 过期问题
- ❌ "WS 就是 fire and forget" — slow consumer 也会拖死 server
- ❌ "Socket.IO 自动处理" — middleware 顺序错误会留缺口
- ❌ SSE 安全等于 WebSocket — 它是单向 HTTP，关注点子集，但 idle / rate 同样要

---

## 7. Output Contract

每次 review 产出：

1. Connection inventory（endpoint / channel / message types）
2. Auth + Origin verification matrix（per-endpoint）
3. Authorization matrix（per-channel）
4. Rate limit policy（per-conn / per-user / per-channel / per-IP）
5. Frame size + idle timeout config
6. Logging schema（含 frame-level event types）
7. CSWSH defense verification
8. Framework-specific config audit
9. SSE-specific config（如适用）
10. SECURITY.md WebSocket section + AppSec Release Evidence §12 叠加层
11. **Findings** —— 全部经 `appsec-sdk finding.add <file>`（canonical path，redact-first）落 `.appsec/findings/<tag>/`，符合 orchestrator §9 finding schema v1.0：
    - `source`（`manual_review` 或扫描命中）；`severity` **小写**；`cwe`（CSWSH 常为 `CWE-352` / 缺 origin 校验 `CWE-346`）；`reproduction_steps`（**禁含 raw session token / frame payload PII / 真实 user id**——脱敏）
    - `asvs_mapping` 用版本化三段 `v5.0.0-<ch>.<sec>.<req>`（正则 `^v5\.0\.0-\d+\.\d+\.\d+$`；WebSocket/realtime 用 ASVS V17，授权用 V8），不用 4.x 旧标签
    - **绝不** Write 直写 `.appsec/findings/**`（orchestrator hook §18.5a 拦 Write/Edit/MultiEdit）；只走 sdk
    - high+ finding → `security-remediation`（fix → 回归测试）

### 7.1 Overlay Evidence Contract（满足 release gate — 不可省）

> 起因：appsec-evidence-validator（orchestrator §16.9 check #3）对**每个激活的 overlay** HARD-REQUIRE `.appsec/evidence/<tag>/overlay-<name>/checklist.yaml`，缺一即 release **BLOCKED**。本 overlay 的 `<name>` = `websocket`。

每次 review 结束，**两步落盘**（按序）：

1. **标记 overlay active**：
   ```bash
   appsec-sdk overlay.activate "<release-tag>" websocket
   # → 建 .appsec/evidence/<tag>/overlay-websocket/ + 写 .activated 标记
   ```
2. **写 overlay checklist evidence**（validator 真正校验的文件）：
   - 写 `.appsec/evidence/<release-tag>/overlay-websocket/checklist.yaml`
   - 直接 Write 即可（evidence 路径不被 hook 拦；只有 `.appsec/findings/**` + `.appsec/decisions/**` 被 §18.5a 拦）
   - 内容：把 §3 Standard Workflow 的 Step 2-13 关键控制（含 §4 CSWSH defense）逐项转成 `items[]`（每项 `id` / `requirement` / `asvs_ref`（`v5.0.0-17.x.x`）/ `status: pass|fail|na|not_tested` / `evidence_ref` / `notes`）+ `summary{total, pass, fail, na}`
   - 任何 `status: fail` 在 `evidence_ref`/`notes` 引用对应 `finding.add` 出的 finding id（finding 本体走 sdk，不塞 checklist）
   - 模板：[`appsec-security-orchestrator/templates/overlay-checklist.template.yaml`](../appsec-security-orchestrator/templates/overlay-checklist.template.yaml)（含 websocket 示例 items：origin check / auth on upgrade / message rate limit / message schema validation / frame size + idle timeout）

无此 checklist.yaml → §16.9 validator BLOCK 整个 release。

---

## 8. References

- [OWASP WebSocket Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/WebSocket_Security_Cheat_Sheet.html)
- [RFC 6455 The WebSocket Protocol](https://datatracker.ietf.org/doc/html/rfc6455)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [Socket.IO Security](https://socket.io/docs/v4/middlewares/)
- [SignalR Security](https://learn.microsoft.com/en-us/aspnet/core/signalr/security)
- [appsec-security-orchestrator](../appsec-security-orchestrator/SKILL.md) — §9 finding schema / §16.3 overlay activation / §16.9 evidence validation / §18.5a finding-path hook
- [overlay-checklist.template.yaml](../appsec-security-orchestrator/templates/overlay-checklist.template.yaml) — overlay-websocket/checklist.yaml 模板
