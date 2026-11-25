---
name: security-compliance-payment
canonical_id: security.compliance.payment
aliases: [pci-dss, payment-security, card-data-security]
version: 1.0.0
status: stable
created_date: 2026-05-25
allowed-tools: Read, Write, Edit, Grep, Glob
forbidden-tools: Bash, WebFetch
manual_gate_required: false
disable-model-invocation: false
standards_versions:
  - PCI DSS: 4.0.1
  - PCI SAQ: A / A-EP / D-Merchant / D-SP
  - NIST CSF: 2.0
  - OWASP ASVS: 5.0
sensitive_data_rules:
  never_read: ["**/PAN*", "**/cardholder*", "**/CVV*", "**/track_data*", ".env*", "secrets/**", "*.pem", "*.key"]
  never_write: ["actual PAN", "actual CVV", "actual track data", "actual PIN"]
  redact_on_output: ["PAN (only show last 4)", "any 13-19 digit string in card-format", "any 3-4 digit CVV-format string"]
upstream:
  - appsec-security-orchestrator
  - security-governance-threat-modeling
downstream:
  - security-remediation
  - security-platform-secrets (payment provider API keys)
  - compliance.audit (planned)
description: >-
  PCI DSS 4.0.1 overlay - determines SAQ scope, minimizes PCI surface via redirect / iframe / hosted-fields patterns, avoids storing PAN, CVV or track data, enforces PSP tokenization and prepares QSA evidence. A developer-facing baseline, not a formal QSA audit.
trigger_phrases:
  - PCI DSS / 支付安全 / payment security / 卡数据安全
  - cardholder data / CHD / PAN / CVV
  - SAQ A / SAQ A-EP / SAQ D
  - Stripe / Adyen / PayPal / Square security
  - 3-D Secure / SCA / Strong Customer Authentication
  - tokenization / payment token
---

# Security Compliance — Payment (PCI DSS 4.0.1)

## 1. Mission

支付场景的核心原则：**不让自己 in scope 比 in scope 后合规更便宜**。本 skill 帮你判断 SAQ 类型，最小化 PCI surface，正确使用 PSP 的 tokenization / hosted fields / redirect，避免存 PAN / CVV / track data，准备 evidence。

**职责边界**：
- **owns**: PCI DSS scope 决策 + SAQ 选择 + 应用层 control 验证 + dev-facing baseline
- **不做**: 替代 QSA (Qualified Security Assessor) 正式审计；本 skill 是工程基线，最终 attestation 走 QSA / ASV 流程
- **不做**: 处理真实卡数据（hard rule，see §sensitive_data_rules）

---

## 2. Activation Triggers

| Trigger | Action |
|---|---|
| 项目接收 / 处理 / 传输 / 存 cardholder data | 强制激活 |
| 项目集成 Stripe / Adyen / Braintree / PayPal / Square / 国内支付（支付宝 / 微信）| 激活 + 评估 SAQ |
| 项目自建 payment form 直接收 PAN | 激活 + **强烈建议改架构** to redirect / hosted fields |
| 项目走 subscription / recurring billing | 激活 + tokenization |
| 项目处理 refund / partial-capture / pre-auth | 激活 + transaction integrity |
| 项目对接 acquirer / processor 直接（非 PSP）| 激活 + 完整 SAQ D + QSA 准备 |

---

## 3. SAQ Selection Decision Tree

| 你的架构 | 适用 SAQ | 复杂度 | 推荐 |
|---|---|---|---|
| **完全 redirect 到 PSP（Stripe Checkout / PayPal redirect）— 服务端永不看 PAN** | SAQ A | 最低（order-of-magnitude — verify against the current PCI DSS 4.0.1 SAQ documents）| ⭐⭐⭐ 首选 |
| **TPSP-hosted iframe — payment form elements 100% 由 validated TPSP 提供，merchant 满足 script 条件** | **可能 SAQ A**（按 PCI SSC FAQ + acquirer/QSA 确认）| 低-中 | ⭐⭐⭐ 推荐（确认后）|
| **PSP iframe / hosted fields（Stripe Elements / Adyen Drop-in）— 浏览器直传 PSP but merchant 部分控制 script/form** | SAQ A-EP（部分情形可 SAQ A，按 PCI SSC FAQ 判断）| 中（order-of-magnitude — verify against the current PCI DSS 4.0.1 SAQ documents）| ⭐⭐ 次选（确认后）|
| **Merchant page 控制 payment form / direct post / 自建 JS 收集** | SAQ A-EP 或 D-Merchant | 高（order-of-magnitude — verify against the current PCI DSS 4.0.1 SAQ documents）| ❌ 避免 |
| **自托管支付，直对接 acquirer** | SAQ D-Service Provider | 最高（order-of-magnitude + ROC — verify against the current PCI DSS 4.0.1 SAQ documents）| 仅大型 / 战略需要 |

**Iron rule**: 选择能让你走 SAQ A 的架构，除非业务确实需要 D。SAQ A vs D 工作量差 10-100x。

**iframe / hosted fields ≠ 必然 SAQ A-EP**：PCI SSC 2024 FAQ（"How does an e-commerce merchant meet the SAQ A eligibility criteria for scripts"）明确：当 TPSP-hosted iframe 中所有 payment form element 100% 来自 validated TPSP、且 merchant 满足 script 治理条件时，SAQ A 仍适用。**最终 scope 决定权在 acquirer / QSA**，不能由架构图独自定。

---

## 4. Standard Workflow

```
Step 1  Scope determination
        → 列所有 system 接触 cardholder data（含 transmit / process / store）
        → 画 CDE (Cardholder Data Environment) boundary
        → 列 segmentation controls（网络 / 应用 / 数据）
        → 决定：能否缩减 CDE？

Step 2  SAQ selection
        → 按 §3 decision tree 选 SAQ type
        → 评估改架构 cost vs 持续 compliance cost
        → 强烈推荐：scope reduction first

Step 3  Cardholder data inventory
        → 是否任何 system 接触 PAN / CVV / track / PIN？
        → PAN truncation: 只存 first 6 + last 4（如展示需要）
        → CVV: 永不存（PCI DSS 3.2.2 + 4.0.1）
        → Track data: 永不存（even temporarily after auth）
        → PIN / PIN block: 永不存

Step 4  Tokenization
        → 所有 recurring / refund / partial-capture 用 PSP token，不存 PAN
        → Token 应 random / unique / non-reversible
        → Token detokenization 只在 PSP，本系统永不

Step 5  Payment flow architecture review
        → 是否 redirect / hosted fields / iframe（SAQ A friendly）?
          - 严格按 §3 SAQ decision tree 确定 — iframe ≠ 必然 A-EP
        → PCI DSS 6.4.3 完整治理（不只 SRI）:
          - payment-page-script-inventory.md（每 script: 来源/用途/owner/integrity）
          - business justification per script
          - authorization process documented
          - integrity method per script (SRI / CSP nonce / vendor sig)
          - exception handling workflow
        → PCI DSS 11.6.1 完整 tamper detection:
          - tamper-detection-config.md（browser-side detection mechanism）
          - 监控 receivedHTTP headers + page content + script content (consumer browser)
          - 初始 baseline 记录
          - alert destination
          - cadence: ≥ weekly OR per TRA-11.6.1-frequency.md
          - 响应 workflow per alert
        → 输出 3 个新证据文件：
          - .planning/security/payment-page-script-inventory.md
          - .planning/security/tamper-detection-config.md
          - .planning/security/TRA-11.6.1-frequency.md

Step 6  Cryptography
        → TLS 1.2+ for any CHD transmission
        → 不存 PAN 优先；如存，必须 strong cryptography（AES-256 + KMS）
        → Key management 走 §security-platform-secrets
        → Key rotation 按 PCI DSS 3.5 / 3.6

Step 7  Access control
        → CDE 系统最小权限
        → MFA for any access to CDE
        → Privileged access audit
        → Vendor / 3rd party access 单独 controls

Step 8  Logging & monitoring
        → CDE 系统 audit log 必收 + SIEM
        → Daily review of CDE log
        → Quarterly ASV scan（external, PCI 11.3.2）
        → Annual penetration test（PCI 11.4）→ 走 pentest-scope-and-roe + authorized-pentest-validation

Step 9  Strong Customer Authentication (SCA)
        → EU PSD2: 3-D Secure 2.x for in-scope transactions
        → Other regions: per local rules
        → Exemption logic（low value / trusted device / corporate）

Step 10 Vendor management
        → PSP attestation (PCI AoC) 备档
        → 4 partner due diligence
        → Service Provider responsibility matrix

Step 11 Incident response (PCI 12.10)
        → IR plan 含 CHD breach response
        → Card brand notification（Visa / Mastercard / Amex 各有要求）
        → 走 security-response-incident-response + 补 PCI-specific notification

Step 12 输出 + 路由
        → Scope reduction recommendations
        → SAQ readiness report
        → Findings → security-remediation
        → 更新 SECURITY.md Payment section + AppSec Release Evidence §12 叠加层
        → Evidence package for QSA / ASV (annual)
```

---

## 5. PCI DSS 4.0.1 关键新变化（vs 3.2.1）

| 控制 | 新要求 |
|---|---|
| **6.4.3** | **Payment page scripts 全生命周期治理**（防 Magecart）— 必须：(1) **inventory** 每个 payment page script，(2) **business justification** 每个 script 的存在理由，(3) **authorization method**（谁批准 / 何时 / 何种 process），(4) **integrity method**（SRI / CSP nonce / vendor signature / 等），(5) **owner / responsible party**，(6) **source provenance**（first-party / TPSP / CDN），(7) **change review process**，(8) **exception handling**。CSP + SRI 是工具，不是合规本身——治理流程必须文档化。 |
| **11.6.1** | **Tamper detection on consumer browser as received**（不只 server-side file integrity）— 必须监控：(1) **HTTP security headers** 实际抵达浏览器时的状态，(2) **payment page content** 浏览器渲染时的内容，(3) **script content** 实际执行时的内容。监控位置：browser-side beacon / synthetic monitoring / 等。Cadence：**至少 7 天一次**或按 PCI DSS 12.3.1 **targeted risk analysis (TRA)** 定义的频率（更频繁可以，更少必须有 TRA 支持）。Alert destination + 初始 baseline + 响应 workflow 必须文档化。 |
| **8.3.6** | MFA for all access to CDE（不只 admin） |
| **3.5.1** | PAN encryption + tokenization 替代方案明确 |
| **A3.x** | Service Provider 责任分担 attestation 形式化 |
| **12.5.2.1** | 持续 scope verification（不只年度） |

---

## 6. Critical "Never Store" List

| 数据 | 可否存 |
|---|---|
| PAN (Primary Account Number) | ⚠️ 仅当业务必须 + 强加密 + 最小化 — 首选不存 |
| Truncated PAN (first 6 + last 4) | ✅ OK |
| Cardholder name | ✅ OK |
| Service code | ✅ OK |
| Expiration date | ✅ OK |
| **CVV / CVV2 / CVC2 / CID** | ❌ **永不存** (PCI 3.2.2) |
| **Full track data (magnetic stripe / chip)** | ❌ **永不存** |
| **PIN / PIN block** | ❌ **永不存** |

---

## 7. Hard Rules

- ❌ **永不**存 CVV / track data / PIN（PCI 3.2.2 / 4.0.1）
- ❌ **永不**log PAN（even partial 也要小心）
- ❌ **永不**写真实卡数据到 test fixture / dev DB
- ❌ **永不**在 SAQ A 项目让服务端看到 PAN（自然破坏 SAQ A scope）
- ❌ **永不**用 disabled 3-D Secure 处理 EU 交易（PSD2 违规）
- ❌ **永不**忽略 ASV quarterly scan（PCI 11.3.2）
- ❌ **永不**忽略 annual pentest（PCI 11.4）
- ❌ **永不**让 CDE 系统 access 不开 MFA（PCI 8.3.6）
- ❌ **永不**用 disabled JS integrity check on payment page（PCI 6.4.3 / 11.6.1）
- ❌ **永不**假设"PSP 处理了 PCI" — 你仍 in scope（至少 SAQ A）

---

## 8. Anti-patterns

- ❌ "我们用 Stripe，所以 PCI 不关我们事" — 仍 in scope 至少 SAQ A
- ❌ "自己做 payment form 体验好" — 让自己进 SAQ D + QSA + ROC 很多倍工作
- ❌ "Token 等于 PAN，要加密存储" — token 不是 CHD（按 PSP 定义），可放普通 DB
- ❌ "CVV 临时存 30 秒做 retry 就行" — 永不存，即使临时
- ❌ "Test card 上线" — 测试卡号写死在代码 = 上线后真的 charge 失败 + 暴露体系
- ❌ "我们 dev 用真实卡做测试方便" — 一旦泄露 + 你也违 PCI
- ❌ "PCI 是 ops 的事" — 4.0.1 强调 dev secure-by-design
- ❌ "Pentest 找朋友帮跑" — 必须 PCI-approved + 完整 ROE
- ❌ "Magecart 攻击不会发生我们" — payment page JS integrity 是 4.0.1 强制要求
- ❌ "国内不走 Visa/MC，PCI 不适用" — 接受国际卡就 in scope，国内卡有 自己规则（央行 + UnionPay）

---

## 9. Output Contract

每次 review 产出：

1. SAQ type 决定 + rationale
2. CDE boundary diagram + segmentation
3. Cardholder data inventory（什么 / 哪里 / 为什么）
4. Tokenization strategy
5. Payment flow architecture + JS integrity controls
6. Cryptography + key management plan
7. Access control + MFA coverage
8. Logging + monitoring + ASV scan + pentest schedule
9. SCA / 3DS strategy（区域）
10. Vendor AoC inventory
11. IR plan PCI addendum
12. Findings → security-remediation
13. SECURITY.md Payment section + AppSec Release Evidence §12 叠加层
14. Evidence package readiness for QSA / SAQ self-attestation

---

## 10. References

- [PCI DSS 4.0.1](https://www.pcisecuritystandards.org/standards/pci-dss/)
- [PCI Self-Assessment Questionnaires](https://www.pcisecuritystandards.org/document_library/?category=saqs)
- [PCI DSS 4.0 Transition Guide](https://blog.pcisecuritystandards.org/pci-dss-4-0-transition-overview)
- [PSD2 SCA](https://www.eba.europa.eu/regulation-and-policy/payment-services-and-electronic-money)
- [Stripe PCI compliance guide](https://stripe.com/docs/security/guide)
- [appsec-security-orchestrator](../appsec-security-orchestrator/SKILL.md)
- [security-platform-secrets](../security-platform-secrets/SKILL.md) — payment provider API keys
- [authorized-pentest-validation](../authorized-pentest-validation/SKILL.md) — annual PCI pentest
