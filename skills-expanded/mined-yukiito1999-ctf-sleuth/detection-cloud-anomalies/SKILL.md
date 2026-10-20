---
name: detection-cloud-anomalies
description: AWS / Azure / GCP / Kubernetes の log を統計的 baseline + behavioral 分析し、credential 侵害 / 権限昇格 / 横展開 / cryptomining / storage 公開 / WAF / OAuth 異常を検出する横断 skill。CTF DFIR / cloud SOC / 自社 cloud の継続 hunting で発火。provider / 観点別の深掘りは references/ 参照
category: defender
tags:
  - cloud
  - detection
  - hunting
  - aws
  - azure
  - gcp
  - kubernetes
  - anomaly
---

# Cloud Anomaly Detection / Hunting

## When to Use

- AWS / Azure / GCP / Kubernetes 環境で、不審 API 呼出 / 横展開 / 権限昇格 / 大量 storage 取得 / cryptomining 兆候を検出する
- 既存 GuardDuty / Defender / SCC / Falco / Sentinel の上位 hunting layer
- 自社 cloud account の継続 baseline + behavioral monitoring

**使わない場面**: cloud 攻撃側 (→ `cloud-pentester`)、cloud 侵害事後の forensic chain 再構成 (→ `cloud-forensics`)、container 内部 syscall (→ `cloud-forensics/references/k8s-runtime-falco.md`)。

provider / 観点別の深掘りは references/ を参照:

- AWS CloudTrail anomaly detection: `references/aws-cloudtrail.md`
- AWS Athena 経由の log forensics: `references/aws-athena.md`
- AWS Detective の behavior graph hunting: `references/aws-detective.md`
- AWS credential 漏洩検出 (TruffleHog 等): `references/aws-credential-exposure.md`
- GCP project / org の IAM / SA key / 大量 storage access / cryptomining / log sink 改竄 hunting: `references/gcp.md`
- Azure Activity / Sign-In Log 解析: `references/azure-activity.md`
- Azure 横展開 (token theft / cross-tenant pivot): `references/azure-lateral.md`
- Azure service principal abuse: `references/azure-sp-abuse.md`
- Azure Storage account misconfiguration: `references/azure-storage.md`
- cross-cloud storage access pattern (S3 / Blob / GCS): `references/storage-access.md`
- cloud cryptomining 兆候: `references/cryptomining.md`
- Kubernetes pod 権限昇格検出: `references/k8s-priv-esc.md`

## Approach / Workflow

### Phase 1 — log source の確保

```
AWS:    CloudTrail (mgmt + data events) → CloudWatch / S3 / Athena / OpenSearch
Azure:  Activity Log + Sign-In + Audit (Entra ID) → Log Analytics / Sentinel KQL
GCP:    Cloud Audit Logs (Admin / Data / System / Policy Denied) → BigQuery
K8s:    audit log (RequestResponse) → 集中 SIEM
```

trail / log の有効化と保存先 access policy / 暗号化を確認。`StopLogging` / `DeleteTrail` 等の隠蔽兆候も hunting 対象。

### Phase 2 — baseline の構築

```
- API 呼出回数 / 種別の per-actor baseline (7-30 日)
- source IP の通常 ASN / geo
- 通常 working hour / 時間帯
- 通常使用される resource scope (service / region / account)
```

deviation を hunting trigger に使う。

### Phase 3 — behavioral hunting

| 観点 | 検出 |
|---|---|
| credential 異常 | 同 user の MFA 未使用 console login + 直後 access key 作成 |
| 権限昇格 | AssumeRole の wildcard / IAM policy attach 連鎖 |
| 横展開 | role A → role B → role C の chained AssumeRole |
| storage exfil | 短時間に大量 GetObject / 大型 download / public 化 (PutBucketPolicy) |
| snapshot exfil | CreateSnapshot + ModifySnapshotAttribute (Add) で別 account に共有 |
| cryptomining | 突然の compute 使用量増 + 不審 image / GPU 起動 + 既知 mining pool DNS |
| OAuth 異常 | 非 admin による illicit consent grant / suspicious app registration |
| SP abuse | service principal の credential 追加 / role 変更 |
| storage misconfig | public access enable / SAS 弱化 / encryption 解除 |

### Phase 4 — alert correlation

複数 source の alert を timeline で相関:

```
時刻       provider event              actor                 影響
HH:MM:SS   ConsoleLogin (no MFA)      compromised-user      foothold
HH:MM:SS   AttachUserPolicy admin     compromised-user      privesc
HH:MM:SS   AssumeRole admin-role      compromised-user      lateral
HH:MM:SS   GetSecretValue x100        compromised-user      exfil
HH:MM:SS   StopLogging                compromised-user      隠蔽
```

### Phase 5 — alert 化 / detection rule

```
- IaC / GuardDuty rule に baseline 化
- Sentinel KQL / Splunk / OpenSearch rule
- IR runbook の trigger 化
- Falco / OPA rule の補強
```

### Phase 6 — レポート

```
- 検知 rule / 期間 / hit 件数 (true positive / false positive 別)
- 攻撃 chain の timeline (MITRE ATT&CK Cloud Matrix)
- 残存リスク (key rotation 必要 / role 縮小 / public bucket)
- 推奨対応 (rule 強化 / IAM policy / encryption / monitoring)
```

## Tools

```
AWS: CloudWatch / Athena / Detective / GuardDuty / Macie
Azure: Sentinel KQL / Defender for Cloud / Log Analytics
GCP: BigQuery / SCC / Chronicle
K8s: Falco / kubectl-who-can / OPA / kyverno
generic: Splunk / OpenSearch / ELK / SIEM
WebFetch
Bash (sandbox)
```

## Related Skills

- `cloud-pentester` (offensive 視点)
- `cloud-forensics` (post-incident)
- `container-forensics` (k8s audit log)
- `kubernetes-security` (cluster offensive 評価)
- `dfir`, `blue-teamer`

## Rules

1. **read-only credentials** — hunting 中は read のみ
2. **PII / secret redaction** — log / IOC / token を共有 report で mask
3. **多 region / 多 account 確認** — 1 region で結論しない
4. **rule の継続改善** — false positive 高い rule は条件強化
