---
name: blue-teamer
description: Blue team / SOC 方法論。監視 / 検出 engineering / triage / response の運用とそのための rule (Sigma / YARA / Suricata) 開発を扱う。CTF blue team / SOC 演習で発火。
category: dfir
tags:
  - blue-team
  - soc
  - detection
  - sigma
  - hunting
  - response
---

# Blue Team / SOC Methodology

## When to Use

- SOC analyst の trigger 対応 / triage
- detection rule (Sigma / Yara / Suricata / Snort / KQL / SPL) の設計と検証
- threat hunting (構造化 / 仮説駆動)
- IR の playbook 提案

**使わない場面**: 攻撃側 (→ `red-teamer`)、specific incident の forensic deep dive (→ `dfir` の各 individual skill)。

## Approach / Workflow

### Phase 1 — visibility 確認

```
log source:
  - endpoint EDR / Sysmon
  - Windows / Linux / macOS auth log
  - firewall / proxy / IDS
  - cloud audit (CloudTrail / Activity Log / Audit Logs)
  - SaaS log (M365 / Workspace / Github / Slack / Jira)
  - DNS / DHCP / VPN
  - identity provider (Okta / Auth0 / Entra)
  - mail gateway

retention:
  - 90+ 日 / regulatory 1+ 年
  - critical alert は raw evidence を sealed area に
```

### Phase 2 — alert 来源と triage

```
- EDR / antivirus
- SIEM correlated alert
- 自前 detection rule
- threat intel feed
- user 報告
- vulnerability scanner

triage:
- IOC 検証 (TI feed / VT lookup)
- baseline 比較 (false positive 候補)
- multi-source corroboration
- severity assignment + escalation
```

### Phase 3 — detection engineering

```
Sigma:        汎用 detection 言語、convert で SIEM 別 query
YARA:         file / memory pattern
Suricata:     network signature
Snort:        legacy network IDS
KQL / SPL:    Sentinel / Splunk 専用
Falco / OPA:  runtime / k8s policy
```

rule 設計:

```
1. attack technique を identify (MITRE ATT&CK)
2. 検出に使う observable を選ぶ (process / file / network / registry)
3. baseline (legitimate) と比較し false positive を minimize
4. 細分化 (technique → specific behavior)
5. test (atomic-red-team / 自前 emulation)
6. deploy + tune
```

### Phase 4 — atomic-red-team / emulation

```
- atomic-red-team で specific TTP の動作再現
- caldera / vectr で 自動 emulation
- purple team exercise でルール改善
```

### Phase 5 — threat hunting (仮説駆動)

```
hypothesis:    "もし actor X が侵入していたら observable Y が出る"
hunt:          log / artefact から Y を探す
result:        positive (incident) / negative (rule 改善 / hypothesis 棄却)
```

```
例:
- Cobalt Strike default URI / cert / sleep が ある? → network-hunter
- DNS tunnel pattern? → network-hunter
- 不審 OAuth consent? → detection-web
```

### Phase 6 — IR playbook

各 incident class に対応:

```
malware infection:    isolate → image → vendor / EDR で清掃
phishing:             quarantine → user reset → awareness
data exfil:           network egress filter → forensic → 法的助言
account takeover:     password / MFA reset → session revoke → audit
ransomware:           isolate ASAP → backup restore / decryptor → law-enforcement
DDoS:                 upstream / CDN mitigation
insider threat:       legal / HR 連絡 → 慎重な evidence 収集
cloud compromise:     credential rotate → role audit → cloud forensics
```

### Phase 7 — TI / sharing

```
- IOC を SIEM / FW に投入
- TI feed (MISP / OTX) と共有
- ISAC / sector partner 共有 (TLP)
- regulatory 報告 (法定義務)
```

### Phase 8 — レポート / metric

```
- MTTD (mean time to detect) / MTTR (mean time to respond)
- triage queue size / age
- false positive ratio
- detection coverage (ATT&CK Navigator)
- incident lessons-learned
- improvement plan
```

## Tools

```
SIEM: splunk / Elastic / Sentinel / OpenSearch
EDR: defender / crowdstrike / sentinelone
sigma / yara / suricata / snort / falco
atomic-red-team / caldera / vectr (emulation)
MISP / OpenCTI / VirusTotal / abuse.ch (TI)
WebFetch / WebSearch
Bash (sandbox)
```

## Related Skills

- `dfir`, 各 forensics / network / cloud / memory / disk / log / endpoint skill 群
- `ioc-hunting`
- `threat-intel`
- `detection-cloud-anomalies`, `detection-web`, `detection-cloud-anomalies`
- `network-hunter`, `rootkit-analysis`, `detecting-kerberoasting-attacks`, `detection-web`
- `red-teamer` (defensive understanding of offensive techniques)

## Rules

1. **rule の信頼性** — false positive を測定 + tuning
2. **TLP** — TI 共有規約
3. **PII redaction**
4. **continuous improvement** — atomic-red-team / purple team で rule 改善
