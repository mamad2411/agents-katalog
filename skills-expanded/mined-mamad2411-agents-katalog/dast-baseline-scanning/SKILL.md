---
name: dast-baseline-scanning
canonical_id: security.app.dast.baseline
aliases: [dast-baseline, zap-baseline, security-app-dast-baseline]
version: 1.1.0
status: stable
created_date: 2026-05-23
last_updated: 2026-05-25
allowed-tools: Read, Write, Bash, Grep, Glob
forbidden-tools: WebFetch
manual_gate_required: false
disable-model-invocation: false
standards_versions:
  - OWASP ZAP Baseline: latest
  - OWASP ASVS: 5.0 (V13 Configuration, V3 Web Frontend, V12 Secure Communication)
  - OWASP API Security Top 10: 2023
sensitive_data_rules:
  never_read: [".env*", "secrets/**", "*.pem", "*.key", "production credentials"]
  redact_on_output: ["session cookies from scan", "auth headers", "PII in responses"]
upstream:
  - appsec-security-orchestrator
  - enterprise-qa-testing (release readiness)
downstream:
  - security-remediation (HIGH+ findings)
  - authorized-pentest-validation (manual upgrade path if active needed)
description: >-
  Passive DAST baseline scanning — configures and runs an OWASP ZAP Baseline scan (spider + passive only, NO active attacks) against authorized local / lab / staging / preview targets, then reports, explains alerts and proposes remediation. No active scan, full scan, exploitation or any attack on production or unauthorized targets; wrapper-based, raw ZAP CLI invocation forbidden. Active validation is gated by `authorized-pentest-validation`. NEVER rename this skill — the wrapper safety boundary depends on this exact name. Triggers: "DAST baseline / ZAP baseline / passive 安全扫描 / preview 安全检查 / staging security scan".
---

# SKILL: dast-baseline-scanning

## 1. Mission

运行 OWASP ZAP **Baseline** scan（passive only）：spider 爬取目标 + passive 规则检测 + 生成报告 + 解释 alerts + 路由到修复。

**永不**做以下任何一项：
- 跑 active scan / full scan
- 对 production / 未授权目标扫描
- 直接调用 raw ZAP 命令（必须走 wrapper）
- 自动升级为 active 测试（升级路径需用户手动调用 `authorized-pentest-validation`）

---

## 2. ZAP Baseline vs Full Scan（关键区分）

| 模式 | 行为 | 本 skill 是否涵盖 |
|------|------|------------------|
| **Baseline** | spider + passive scan + 报告 passive 发现 | ✅ 涵盖 |
| **Full Scan** | spider + ajax spider + **active scan**（实际攻击）+ 长耗时 | ❌ 路由 `authorized-pentest-validation`（手动） |

ZAP 官方说明：Baseline 设计为 CI/CD 友好，只做 passive 检测，不发送攻击 payload；Full Scan 会执行 actual attacks（SQL injection probe, XSS probe 等）。两者行为和风险完全不同。

---

## 3. Authorization Pre-check（强制，跑之前必须全部确认）

- [ ] Target URL 是用户自有或被书面授权
- [ ] Target 不是 production（除非用户明确授权 + 本地代理隔离）
- [ ] ROE（Rules of Engagement）已确认（baseline 简化版：授权 scope + 时间窗口）
- [ ] 报告输出路径已确定
- [ ] 速率：ZAP baseline 默认低速，若调整须确认
- [ ] 紧急终止条件（超时 / 意外流量触发告警时停止）

如任一项未确认 → 停止，询问用户，不继续。

---

## 4. Wrapper 设计

**不直接调用 raw ZAP 命令。** 项目必须自带 wrapper：

```bash
# 推荐路径
npm run security:baseline -- --target=<URL> --report=./security/baseline-report.html

# 或
scripts/security/zap-baseline.sh --target=<URL>
```

**Wrapper 必须强制：**
- Target allowlist（只允许 .env / config 中声明的 URL）
- Non-production 确认标志
- Report output directory（不输出到项目 src 内）
- Timeout cap（建议 10 分钟）

**settings.json 权限配置：**

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run security:baseline *)",
      "Bash(bash scripts/security/zap-baseline.sh *)"
    ],
    "deny": [
      "Bash(*zap-full-scan.py*)",
      "Bash(*zap-api-scan.py*)",
      "Bash(docker run *zap*full*)",
      "Bash(docker run *zap*api*)"
    ]
  }
}
```

旧的 path-prefix 形式（`Bash(zap-full-scan.py *)`）可被路径前缀绕过，且 `zap-full-scan.py` / `zap-api-scan.py` **本身就是 active-by-default**，所以 `*--active*` 之类的 matcher 永远不会命中——改用上面的 name-based 形式，无论路径如何都能匹配。This deny-list is best-effort defense-in-depth; the real control is the wrapper allowlist + the §3 authorization pre-check. zap-baseline.py (passive) stays in `ask`, not deny.

---

## 5. 工作流（7 步）

```
Step 1 — 确认 §3 Authorization Pre-check（逐条）
Step 2 — 收集 target（local dev / staging / preview URL）
Step 3 — 调用 wrapper：npm run security:baseline -- --target=<URL>
Step 4 — 等待完成，收集报告（HTML + JSON）
Step 5 — 解释 alerts（按 severity 分类：CRITICAL / HIGH / MEDIUM / LOW / INFO）
Step 6 — 路由修复：每条 HIGH+ finding 路由到 `security-remediation`
Step 7 — 输出 baseline summary（附 report 路径 + finding 计数）
```

---

## 6. Alert 解释模板

每条 alert 输出格式：

```
[SEVERITY] Alert Name (CWE-XXX)
位置：<URL + 参数>
被动发现理由：<ZAP 为何报告此项>
风险说明：<实际风险是什么>
建议修复：路由到 security-remediation
```

---

## 7. 与上下游接口

| 方向 | Skill / Agent | 说明 |
|------|--------------|------|
| 上游 | `appsec-security-orchestrator` | 决定是否触发 DAST baseline |
| 下游 | `security-remediation` | 处理每条 HIGH+ finding 的代码修复 |
| 升级路径 | `authorized-pentest-validation` | 需要 active validation 时，用户手动调用 |

---

## 8. Hard Rules

- ❌ 不跑 active scan（zap-full-scan / zap-api-scan）
- ❌ 不跑 full scan
- ❌ 不对 production 目标扫描（未授权）
- ❌ 不直接调用 raw ZAP CLI 命令
- ❌ 不在 CI 默认对外部 URL 扫描（必须 staging/preview 受控环境）
- ❌ 不在用户未确认 authorization pre-check 时继续
- ❌ 不自动将 baseline 发现升级为 active exploitation 尝试

---

## 9. 常见 Baseline Alerts 参考

| Alert | 类型 | 说明 |
|-------|------|------|
| Missing Anti-CSRF Tokens | MEDIUM | 表单缺少 CSRF token |
| X-Content-Type-Options Header Missing | LOW | 缺少 nosniff 头 |
| Content Security Policy (CSP) Header Not Set | MEDIUM | 缺少 CSP |
| Strict-Transport-Security Header Not Set | LOW/MEDIUM | 缺少 HSTS |
| Information Disclosure - Server Info | LOW | Server header 暴露版本 |
| Cookie Without Secure Flag | MEDIUM | Cookie 未设 Secure |

以上均为 passive 观察，无实际攻击 payload。

---

## 10. 触发词

- "DAST baseline"
- "ZAP baseline"
- "passive 安全扫描"
- "preview / staging security scan"
- "安全检查（staging 或 preview）"

**不触发：** "active 安全测试" / "渗透测试" / "exploit" → 路由 `authorized-pentest-validation`
