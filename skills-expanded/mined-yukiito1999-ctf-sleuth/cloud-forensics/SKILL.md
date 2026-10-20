---
name: cloud-forensics
description: AWS / Azure / GCP / SaaS / 云原生 runtime の log・snapshot・metadata を統合して cloud 環境侵害を解析する。control plane log / EBS snapshot / VPC flow / IAM 改竄 / Falco runtime / SaaS storage 取得を扱う。CTF DFIR や cloud incident response で発火。AWS CloudTrail / Falco / SaaS storage の深掘りは references/ 参照
category: forensics
tags:
  - cloud-forensics
  - aws
  - azure
  - gcp
  - control-plane
  - snapshot
  - falco
  - saas
---

# Cloud Forensics

## When to Use

- AWS / Azure / GCP のいずれかで侵害が疑われ、cloud 固有の evidence を集約解析する必要
- snapshot / log / IAM を統合して timeline 化したい
- live host にアクセスできない、または cloud control plane 経由で evidence を集める運用

**使わない場面**: cloud service log の hunting (anomaly detection / behavioral hunt) (→ `detection-cloud-anomalies`)、container forensic 単独 (→ `container-forensics`)。

variant の深掘りは references/ を参照: AWS CloudTrail から侵害 chain を再構成 = `references/aws-cloudtrail.md`、Azure Activity / Audit / Sign-In log の triage = `references/azure.md`、GCP Cloud Audit Logs / IAM 改竄 = `references/gcp.md`、Falco runtime での container syscall hunt = `references/k8s-runtime-falco.md`、Google Drive / OneDrive / Dropbox / Box の SaaS storage acquisition = `references/saas-storage-acquisition.md`。

## Approach / Workflow

### Phase 1 — IR 体制と権限

```
- IR 用 read-only role (AWS: SecurityAudit + ReadOnlyAccess; Azure: Reader; GCP: Viewer)
- evidence 保存先の隔離 bucket / storage account / GCS bucket
- access log 取得経路 (CloudTrail / Activity Log / Cloud Audit Logs が有効か確認)
- 関連 region 全て見る (region 跨ぎ攻撃)
```

### Phase 2 — control plane log

```
AWS:    CloudTrail (management + data events)
        → S3 bucket / CloudWatch Logs / Athena query
Azure:  Activity Log + Sign-In Logs + Audit Logs (Entra ID)
        → Log Analytics workspace / Sentinel
GCP:    Cloud Audit Logs (Admin Activity / Data Access / System Event / Policy Denied)
        → Cloud Logging / BigQuery
```

各 provider の最低限取得:

```bash
# AWS
aws cloudtrail lookup-events --start-time '2024-01-01T00:00:00Z' --end-time '2024-01-02T00:00:00Z' --region us-east-1
# Azure (PowerShell)
Get-AzActivityLog -StartTime '2024-01-01' -EndTime '2024-01-02'
# GCP
gcloud logging read 'resource.type="audited_resource"' --freshness=2d
```

### Phase 3 — workload snapshot

```
AWS:    EBS snapshot (前後), AMI 作成, EFS バックアップ
Azure:  VM snapshot, Managed Disk snapshot
GCP:    persistent disk snapshot
```

```bash
# AWS 例
aws ec2 create-snapshot --volume-id vol-xxx --description "IR-2024-001"
aws ec2 modify-snapshot-attribute --snapshot-id snap-xxx --create-volume-permission '{"Add":[{"UserId":"<ir-account>"}]}'
```

snapshot を IR account の volume にアタッチして read-only mount → 通常の disk forensics (→ `disk-forensics`)。

### Phase 4 — network log

```
AWS:    VPC Flow Logs / Route 53 Resolver query log / GuardDuty findings
Azure:  NSG flow log / Azure Firewall log / DNS Analytics
GCP:    VPC Flow Logs / Firewall Rules Logging / Cloud DNS log
```

外部 IP 接続・cloud metadata 取得・横展開の証跡。

### Phase 5 — IAM 改竄チェック

```
AWS CloudTrail:
  CreateUser / CreateAccessKey / AttachUserPolicy / PutUserPolicy
  CreateRole / AttachRolePolicy / UpdateAssumeRolePolicy
  CreateLoginProfile (root)
  ConsoleLogin (MFA used or not)

Azure:
  Add member to role / Update conditional access / Disable MFA / Add OAuth app

GCP:
  google.iam.admin.v1.SetIamPolicy / google.iam.v1.IAMPolicy.SetIamPolicy
```

短時間に user / role / policy が増減していたら高リスク。

### Phase 6 — storage / data access

```
AWS S3 data events (要 data event 有効化)
Azure Storage Blob log (Diagnostic Setting)
GCS audit log (DATA_READ / DATA_WRITE)
```

data exfil の痕跡 (大量 GetObject / 巨大 download) を検出。

### Phase 7 — secret 系の改竄

```
AWS Secrets Manager / Parameter Store: GetSecretValue 連発
Azure Key Vault: SecretGet / KeyGet
GCP Secret Manager: AccessSecretVersion
```

侵害された service account / role が大量に secret を取りに行っているか確認。

### Phase 8 — timeline 化と cross-reference

```
1. 各 source を共通 schema (timestamp / actor / verb / resource) に正規化
2. timestamp 順に統合
3. actor (user / role / SA) 別に grouping
4. resource 別 (どの S3 bucket / VM / role が触られたか)
```

### Phase 9 — レポート

```
- 環境 (AWS account / Azure tenant / GCP project)
- 期間
- 攻撃 chain (initial access → persistence → privesc → exfil)
- 関与した actor (compromised credentials / role)
- 影響範囲 (data / service / cost)
- 残存リスク (key / role / policy が直されたか)
- 推奨 (key rotation / role 縮小 / detection rule)
```

## Tools

```
AWS CLI / Athena / Detective / GuardDuty / Macie
Azure CLI / PowerShell / Sentinel KQL
gcloud / BigQuery
jq
WebFetch
Bash (sandbox)
```

## Related Skills

- `detection-cloud-anomalies` (anomaly hunting / behavioral)
- `container-forensics` (Docker / k8s audit log)
- `disk-forensics`, `endpoint-forensics`
- `dfir`, `blue-teamer`

## Rules

1. **read-only credentials** — IR 中に書込権限を使わない
2. **chain of custody** — snapshot id / log export の hash を保持
3. **PII / secret redaction** — log / secret を共有 report に入れる場合は mask
4. **多 region 確認** — 1 region の log だけで結論しない
