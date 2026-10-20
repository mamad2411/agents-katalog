---
name: security-platform-secrets
canonical_id: security.platform.secrets
aliases: [secrets-management, secrets-engineering, secret-handling]
version: 1.0.0
status: stable
created_date: 2026-05-25
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
forbidden-tools: WebFetch
manual_gate_required: false
disable-model-invocation: false
standards_versions:
  - OWASP Secrets Management Cheat Sheet: latest
  - OWASP ASVS: 5.0 (V11 Crypto, V13 Config)
  - NIST CSF: 2.0 (PR.DS-1, PR.DS-2)
  - GitHub OIDC: official docs
  - HashiCorp Vault: best practices
  - AWS Secrets Manager / GCP Secret Manager / Azure Key Vault: vendor docs
sensitive_data_rules:
  never_read: [".env*", "secrets/**", "*.pem", "*.key", "*.p12", "*.pfx", "credentials.json", "service-account*.json"]
  never_write: ["actual secret values", "real tokens", "real API keys"]
  redact_on_output: ["all token-shaped strings", "all key-shaped strings", "any base64 of credential material"]
upstream:
  - appsec-security-orchestrator
  - security-governance-threat-modeling  # 揭示 secrets 攻击面
downstream:
  - security-remediation  # 把发现的 leak / misconfig 转 finding
  - appsec-security-orchestrator  # 回 orchestrator
description: >-
  Secrets engineering review across the full lifecycle - central storage, distribution, rotation, audit, revocation, post-incident handling, OIDC short-lived credentials and leak detection. Running a secret scanner is the floor, not the scope.
trigger_phrases:
  - secrets / 凭证 / 密钥管理 / API key 管理
  - Vault / Secrets Manager / KMS
  - OIDC / federated identity / short-lived credentials
  - gitleaks / 密钥泄露 / credential leak
  - secrets rotation / 凭证轮换 / 密钥轮换
---

# Security Platform — Secrets

## 1. Mission

Secrets 管理不是"加密后放在配置文件里"。本 skill 覆盖完整生命周期：**集中存储 → 标准化分发 → 自动轮换 → 审计 → 撤销 → 泄漏响应**。

**职责边界**：
- 设计 / 审查 secrets 工程
- 检测泄漏（gitleaks history scan）
- 路由到 IAM / IaC / CI/CD 同类问题
- **不**碰真实凭证内容（§sensitive_data_rules 禁止）

---

## 2. Activation Triggers

| Trigger | Action |
|---|---|
| 项目初始化 | 设计 secrets 储存策略 |
| 引入新 secret（API key / DB / token） | 评估是否走 vault / OIDC |
| CI/CD 接入云 | 迁移到 OIDC short-lived credentials |
| 任何 credential leak 嫌疑 | 立即响应流程 |
| 定期轮换窗口（季度 / 年度） | 自动 / 手动轮换 |
| 事件后 | 凭证全量轮换 + history scan |
| 团队人员离开 | 撤销其专属凭证 |

---

## 3. Secrets Classification（按敏感度分级）

| Class | Examples | Storage | Rotation | Audit |
|---|---|---|---|---|
| **L0 Public** | Public API keys (Stripe publishable, Mapbox public) | env / config | manual on revoke | low |
| **L1 Service-to-service** | Internal API keys, OAuth client secrets | Vault / Secrets Manager | 90 天 | medium |
| **L2 Production credentials** | DB passwords, signing keys, encryption keys | Vault / KMS | 30-90 天 | high |
| **L3 Master** | Vault root token, KMS master keys, root CA | HSM / 离线保险 + 多人控 | strict policy | full |
| **L4 Customer / regulated** | Customer encryption keys, payment tokens, PHI keys | dedicated vault per tenant | regulatory | full + immutable |

---

## 4. Anti-patterns（绝对禁止）

- ❌ Secrets 入 git（含 .env、config.json、CI workflow yaml 内 inline）
- ❌ Secrets 入应用日志 / error message / stack trace
- ❌ Secrets 入 client-side bundle（next.js NEXT_PUBLIC_ 前缀含敏感值）
- ❌ Secrets 进容器镜像（build-time ARG / docker history）
- ❌ Secrets 写死在 ENV var 长期不轮换
- ❌ CI/CD 用长期云凭证（应改 OIDC short-lived token）
- ❌ Production secret 复用到 staging / dev
- ❌ 用对称加密 "保护" secret 后丢配置文件——key 也在同一处等于明文
- ❌ Service account 通用账号，跨服务复用
- ❌ 凭证轮换后旧凭证不撤销（attacker 仍可用）

---

## 5. Standard Workflow

```
Step 1  分类
        → 列项目所有 secret，按 §3 分级

Step 2  存储审查
        → L0: env 可以
        → L1+: 强制 Vault / Secrets Manager
        → L3+: HSM + 多人控制
        → 检查：是否有 secret 漂移到错误层（如 L2 还在 .env）

Step 3  分发审查
        → 应用读取 secret 路径：app boot → fetch from secret store
        → 短期凭证优先（OIDC token / IAM role）
        → 长期凭证必须有 rotation

Step 4  Leak 扫描（历史 + 当前）
        → gitleaks detect --source . --log-opts="--all" --redact
        → trufflehog filesystem .
        → 检查 issue / PR / wiki comment

Step 5  轮换审查
        → 每个 L1+ secret 有 rotation owner + cadence
        → 上次轮换日期 ≤ cadence
        → 轮换流程文档化（dry-run + verify + revoke old）

Step 6  Audit 审查
        → secret store access log 收集
        → 异常访问告警（off-hours / 大量 fetch / 非授权 actor）
        → SIEM 接入

Step 7  CI/CD 凭证迁移到 OIDC
        → GitHub Actions → AWS OIDC / GCP WIF / Azure federated
        → 替换长期 AWS_ACCESS_KEY_ID / GCP_SA_KEY 等长期凭证

Step 8  Pre-commit / pre-push hook
        → 安装 gitleaks pre-commit
        → 拦截 commit 含 secret-shaped string

Step 9  事件预案
        → leak 检测到 → 立即 revoke + 全量 history scan + IR 启动
        → 写到 incident-response-initial.md
```

---

## 6. Leak Detection Commands

```bash
# 全 git 历史 secret 扫描（首次 onboarding 必跑）
# --redact 强制：报告中的 secret 值被替换为 REDACTED，不留 raw 值
gitleaks detect --source . --log-opts="--all" --redact --report-format=json --report-path=.planning/security/gitleaks-report.json

# 增量扫描（pre-commit）
gitleaks protect --staged --redact

# 替代 / 补充工具（TruffleHog 必须配合 --no-verification + 输出 redirect 到受控目录）
trufflehog filesystem . --json --no-verification > .planning/security/trufflehog-report.json
trufflehog git file://. --since-commit HEAD~100 --json --no-verification > .planning/security/trufflehog-git-report.json

# 容器镜像 secret 扫描
trivy image --scanners secret <image>:<tag> --format json --output .planning/security/trivy-secrets-report.json

# CI workflow yaml secret 扫描
gitleaks detect --source .github/workflows --redact --report-format json --report-path=.planning/security/gitleaks-workflows.json
```

**Redaction rule（hard）**：
- ❌ 绝不把 secret 值（即使 redacted 形式）放进 chat / LLM context / SECURITY.md / 公开 report
- ❌ 绝不去掉 `--redact` 试图"看一眼真正的值"
- ✅ 所有 scan 报告写入 `.planning/security/` 受控目录，列入 `.gitignore`
- ✅ Scanner-only exception：扫描器进程本身可以读 secret-shaped 字符串以做检测，但**不输出 raw 值**；这是 detector tooling 的内部行为，与 LLM context 严格分离

**重要**：扫到结果 ≠ 解决问题。每条 leak 必须：
1. 立即 revoke 旧凭证
2. 发行新凭证
3. 评估实际被访问可能性（review access log）
4. 决定是否触发 incident-response
5. 添加 pre-commit hook 防再犯
6. git history 重写（如必要，但优先 revoke）

---

## 7. GitHub OIDC Migration（替代长期云凭证）

旧模式（不安全）：
```yaml
# .github/workflows/deploy.yml
env:
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}  # 长期凭证，泄漏代价大
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

新模式（OIDC short-lived）：
```yaml
# .github/workflows/deploy.yml
permissions:
  id-token: write   # 申请 OIDC token
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::${{ vars.AWS_ACCOUNT_ID }}:role/github-actions-deploy
          aws-region: us-east-1
          # 短期 token 自动续，无需长期 secret
```

类似机制：
- **GCP**: Workload Identity Federation
- **Azure**: Federated Credentials
- **Vault**: GitHub Actions auth method

---

## 8. Secret Store 推荐矩阵

| Scale / Need | 推荐 |
|---|---|
| 单项目 dev / 小团队 | doppler / 1Password CLI / direnv + .envrc.local（git ignored）|
| AWS-native | AWS Secrets Manager（auto-rotation 支持 RDS / Redshift / DocDB）+ Parameter Store |
| GCP-native | GCP Secret Manager + Workload Identity |
| Azure-native | Azure Key Vault + Managed Identities |
| 多云 / 自托管 | HashiCorp Vault（OSS or Enterprise）|
| K8s | External Secrets Operator + Vault / cloud KMS backend |
| 高合规（PCI / HIPAA）| HSM-backed（CloudHSM / Azure Dedicated HSM）|

---

## 9. Hard Rules

- ❌ **永不读 .env / secrets/** / *.pem / *.key 内容**——只读路径存在性
- ❌ **永不向 LLM 上下文 / 第三方传递 secret 值**
- ❌ **永不把 secret 写到本 skill 输出 / log / report**
- ❌ **永不**用 RSA-1024 / DES / MD5 等弱算法
- ❌ **永不**把 secret 长期暴露在 ENV——必须配合 rotation
- ❌ **永不**在 leak 响应里只 rotate 不评估 access log——必须双管齐下

---

## 10. Output Contract

> **v3.0 evidence sink**: machine-readable findings MUST be written via `appsec-sdk finding.add` (schema-validated against orchestrator §9, redacted first). Direct Write to `.appsec/findings/**` is blocked by the PreToolUse hook. The markdown report (vuln-report.md / SECURITY.md section) is the human-rendered view only.

每次 review 产出：

1. `SECURITY.md §11 Secret Management` 章节填充 / 更新
2. Secrets inventory（按 §3 分级）
3. 当前 rotation status（每个 L1+ secret）
4. Leak scan 结果（含 git history）
5. CI/CD 凭证迁移状态（是否已迁 OIDC）
6. Pre-commit hook 安装状态
7. 高危发现转 vuln-report.md → security-remediation

---

## 11. References

- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [GitHub OIDC docs](https://docs.github.com/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [gitleaks](https://github.com/gitleaks/gitleaks)
- [TruffleHog](https://github.com/trufflesecurity/trufflehog)
- [HashiCorp Vault docs](https://developer.hashicorp.com/vault/docs)
- [appsec-security-orchestrator](../appsec-security-orchestrator/SKILL.md)
- [templates/SECURITY.md §11](../../templates/planning/SECURITY.md)
- [templates/vuln-report.md](../appsec-security-orchestrator/templates/vuln-report.md)
