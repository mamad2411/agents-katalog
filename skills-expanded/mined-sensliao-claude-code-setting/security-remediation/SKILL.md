---
name: security-remediation
canonical_id: security.app.remediation
aliases: [appsec-remediation, security-fix, vuln-remediation, security-app-remediation]
version: 1.1.0
status: stable
created_date: 2026-05-23
last_updated: 2026-05-25
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
forbidden-tools: WebFetch
manual_gate_required: false
disable-model-invocation: false
standards_versions:
  - OWASP ASVS: 5.0
  - NIST CSF: 2.0 (PR / RS)
  - CWE: latest
sensitive_data_rules:
  never_read: [".env*", "secrets/**", "*.pem", "*.key"]
  redact_on_output: ["tokens", "credentials", "PII"]
upstream:
  - appsec-security-orchestrator
  - appsec-reviewer (agent)
  - dast-baseline-scanning
  - authorized-pentest-validation
  - gsd-security-auditor (agent)
  - security-governance-threat-modeling
  - security-platform-secrets
  - security-platform-iac-cloud
downstream:
  - appsec-security-orchestrator (返回 Release Evidence)
  - gsd-verify-work
  - enterprise-qa-testing
description: >-
  Security finding remediation and regression workflow. Accepts any finding in the standardized schema (appsec-security-orchestrator section 9) from any upstream security skill or agent, and produces minimum-viable code fixes, security regression tests (RED to GREEN with stdout evidence) and an updated SECURITY.md. Use after any security review produces HIGH+ findings.
---

# SKILL: security-remediation

## 1. Mission

把安全发现（finding）转化为：
1. 实际代码修复（minimal, targeted）
2. Regression test（复现 vuln → 验证 fix）
3. 证据（test stdout）
4. SECURITY.md 更新记录

修复完成**必须有证据**，不能只说"fix 了"。

---

## 2. Inputs（接受来源）

**通用入口契约**：任何 `security-*` skill / `appsec-*` agent / `dast-*` skill / GSD 安全 auditor / 用户提交的 finding，只要符合 **standardized finding schema**（见 `appsec-security-orchestrator §9`），本 skill 即可消费。HIGH+ 强制路由进来。

| 来源 | 说明 | Schema 要求 |
|------|------|---|
| `appsec-reviewer` agent | SAST 审查输出 | 必须 |
| `dast-baseline-scanning` | ZAP baseline HIGH+ findings | 必须 |
| `authorized-pentest-validation` | 手动渗透测试漏洞 | 必须 |
| `gsd-security-auditor` agent | GSD 安全审计输出 | 必须 |
| `security-governance-threat-modeling` | Threat model control gap（已有 PoC 的项）| 必须 |
| `security-platform-secrets` | Secret leak / rotation gap / misuse | 必须 |
| `security-platform-iac-cloud` | IaC misconfig / cloud posture finding | 必须 |
| `appsec-security-orchestrator` | 任何 §7 workflow 产出的 finding | 必须 |
| 任何其他 `security-*` skill | 任何 HIGH+ finding | 必须 |
| 用户手动报告 | Bug report / CVE / 社区披露 | 建议（如格式不符，本 skill 帮 normalize 后处理）|

**Finding schema 是 canonical** — 完整定义在 `appsec-security-orchestrator §9`，本 skill 只引用，不 fork。关键字段速查：

- `schema_version: 1.0`
- `id: <YYYY-MM-DD>-<source>-<seq>`
- `source`: 完整 enum 见 orchestrator §9（含 sast / dast / sca / secret_scan / manual_review / pentest / external_disclosure / threat_model / iac_scan / container_scan / cloud_posture / secrets_engineering）
- `asvs_mapping: [v5.0.0-<chapter>.<sub>]` — version-pinned，例：`v5.0.0-6.2.1`
- `csf_function: GV | ID | PR | DE | RS | RC`
- `severity / confidence / computed_risk` — schema field values 是 lower-case（`critical|high|medium|low`）；UPPER-case 仅用于 human-display
- `verification_status: pending | red_confirmed | fix_applied | green_confirmed | regression_in_ci`
- `test_commands: [...]`
- `risk_acceptance: { approver, approval_date, compensating_controls, review_date }`（仅 status: accepted）

详见 [appsec-security-orchestrator §9](../appsec-security-orchestrator/SKILL.md#9-standardized-finding-schema)。

> **v3.0 evidence sink**: machine-readable findings MUST be written via `appsec-sdk finding.add` (schema-validated against orchestrator §9, redacted first). Direct Write to `.appsec/findings/**` is blocked by the PreToolUse hook. The markdown report (vuln-report.md / SECURITY.md section) is the human-rendered view only.

不符合 schema 的 finding 输入 → 本 skill 先用 normalize step 转格式（填默认值 + 推导 csf_function），再走 §3 workflow。绝不丢字段，绝不创建本 skill 私有的 schema 变体。

---

## 3. Remediation Workflow（7 步）

```
Step 1 — 解析 finding
          severity / location / category / CWE
          CVSS 是 optional，不是 schema 字段；schema 的 risk 字段是
          computed_risk / exploit_likelihood / business_impact

Step 2 — 评估修复方案（四选一）
          Fix      → 修代码，本 skill 负责
          Accept   → 记录接受风险，更新 SECURITY.md，结束
                     必须捕获 risk_acceptance{approver, approval_date,
                     compensating_controls, review_date} 并设 status: accepted
                     （orchestrator gate 要求这些字段才给 CONDITIONAL_PASS）
          Mitigate → 添加控制措施降低风险，非根因修复
          Transfer → 转给第三方（vendor / library upstream）

Step 3 — 写代码修复
          最小化改动，不引入新依赖，不顺手重构

Step 4 — 写 regression test
          RED：在未 fix 代码上测试失败（复现漏洞）
          GREEN：在 fix 后测试通过

Step 5 — 跑 regression test，收集 stdout

Step 6 — 更新 SECURITY.md
          记录：finding / severity / fix 位置 / verification evidence

Step 7 — 输出 remediation summary
          供 enterprise-qa-testing 接 release evidence
          供 gsd-verify-work 验证
```

---

## 4. Regression Test 模板

每个 fix 必须包含三层测试：

### 层 1：复现测试（RED）
```
// 描述：在 fix 前，此测试应失败（证明漏洞存在）
// 运行时注释掉 fix 或用旧实现
test('XSS: unescaped user input renders script tag', () => {
  const input = '<script>alert(1)</script>';
  const output = render(Component, { content: input });
  // 旧行为：script 标签出现在 DOM → 测试通过 = 漏洞存在
  expect(output).toContain('<script>');  // RED test
});
```

### 层 2：验证测试（GREEN）
```
// 描述：fix 后，此测试应通过（证明漏洞已修复）
test('XSS: user input is escaped, no script tag rendered', () => {
  const input = '<script>alert(1)</script>';
  const output = render(Component, { content: input });
  expect(output).not.toContain('<script>');
  expect(output).toContain('&lt;script&gt;');  // escaped
});
```

### 层 3：边界测试（相关攻击向量）
```
// 覆盖相似攻击向量
test.each([
  ['<img src=x onerror=alert(1)>'],
  ['javascript:alert(1)'],
  ['"><script>alert(1)</script>'],
])('XSS: attack vector %s is blocked', (payload) => {
  const output = render(Component, { content: payload });
  expect(output).not.toMatch(/<script|onerror|javascript:/i);
});
```

---

## 5. Fix 类型参考

| Finding 类型 | 典型修复 |
|-------------|---------|
| XSS | 转义输出；避免 innerHTML；用框架内置渲染 |
| CSRF | 添加 CSRF token；SameSite cookie 属性 |
| SQL Injection | 参数化查询；ORM 绑定参数 |
| 缺少安全头 | middleware 添加 HSTS / CSP / nosniff |
| Cookie 无 Secure/HttpOnly | Set-Cookie 属性补全 |
| 信息泄露（Server header）| 在服务器配置中移除版本信息 |
| 路径遍历 | 白名单路径；禁止 `../` 序列 |
| 硬编码密钥 | 移到环境变量；rotate 泄露的 key |

---

## 6. SECURITY.md 更新格式

每次修复在 SECURITY.md 追加：

```markdown
## [YYYY-MM-DD] Fix: <Finding Name> (CWE-XXX)

**Severity:** HIGH / MEDIUM / LOW
**Source:** dast-baseline-scanning | appsec-reviewer | manual report
**Location:** `src/components/Foo.tsx:42`
**Fix:** 描述修复方法（1-2 句）
**Regression Test:** `tests/security/foo-xss.test.ts`
**Verified:** ✅ regression test passing (stdout 附在 PR 中)
```

---

## 7. Hard Rules

- ❌ 不在没有 regression test 的情况下声称 fix 完成
- ❌ 不"过度修复"——只改 finding 涉及的代码，不顺手重构
- ❌ 不引入新的 HIGH severity 依赖来修一个 MEDIUM issue
- ❌ 不删除 / 隐藏 security log（修了要记录）
- ❌ 不"模糊修复"——必须修 root cause，不只 mitigate 表面
- ❌ 不 rotate 密钥时只改代码不通知用户（必须提醒 rotate 线上 secret）
- ❌ 不在未确认 finding 来源时盲目修复（先确认是真实漏洞）

---

## 8. 与 GSD 接口

| 接口方向 | Skill / Agent | 说明 |
|---------|--------------|------|
| 触发来源 | `gsd-secure-phase` | 安全阶段触发本 skill |
| 输入来源 | `dast-baseline-scanning` | DAST 报告中的 findings |
| 输入来源 | `appsec-reviewer` | SAST/代码审查 findings |
| 验收 | `gsd-verify-work` | 修复后验证 regression test 通过 |
| Release evidence | `enterprise-qa-testing` | 提供安全修复证据给 QA 关口 |

---

## 9. 修复证据输出格式

修复完成后输出：

```
## Remediation Summary

Finding: <name> (CWE-XXX, SEVERITY)
Source: <来源 skill>
Fix applied: <文件路径:行号>
Fix description: <1-2 句>

Regression tests:
  - tests/security/<test-file>.test.ts
  - Status: ✅ GREEN (3 tests passing)
  - Stdout: [附 test runner output]

SECURITY.md updated: ✅
Next step: gsd-verify-work → enterprise-qa-testing
```

---

## 10. 触发词

- "修复安全问题"
- "安全漏洞修复"
- "security fix"
- "regression test for vulnerability"
- "remediation"
- "fix XSS / CSRF / injection / security header"
