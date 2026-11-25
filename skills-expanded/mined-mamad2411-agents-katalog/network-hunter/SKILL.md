---
name: network-hunter
description: network metadata / pcap / log を統計分析し、C2 beaconing / Cobalt Strike beacon / DNS tunneling / DNS exfil / ARP poisoning など攻撃通信を hunting する横断 skill。CTF DFIR / blue team SOC / 継続 monitoring で発火。技法別の深掘りは references/ 参照
category: defender
tags:
  - network-hunting
  - beaconing
  - c2
  - dns-tunneling
  - cobalt-strike
  - arp-poisoning
---

# Network Hunter

## When to Use

- 既存 network capture / Zeek log / DNS log / NetFlow から不審通信を hunting
- 周波数解析 + payload size + protocol fingerprint + TI 突合で C2 beaconing を網羅検出
- Cobalt Strike beacon / DNS tunneling / ARP poisoning 等の専用検出 rule を策定
- 自社 network の継続 monitoring baseline + alerting

**使わない場面**: incident pcap の forensic chain 再構成 (→ `network-analyzer`)、Cobalt Strike beacon の binary RE / config 抽出 (→ `reverse-engineering`)、cloud control plane log (→ `detection-cloud-anomalies`)。

技法別の深掘りは references/ を参照:

- 周波数解析 (FFT / autocorrelation / inter-arrival statistics) で C2 beacon を識別: `references/frequency-analysis.md`
- Zeek conn.log 統計分析で beacon 検出: `references/beaconing-zeek.md`
- C2 beaconing の網羅 hunting (周波数 + payload + fingerprint + TI): `references/c2-beaconing.md`
- 既知 Cobalt Strike beacon の TLS / JA3 / URI / sleep / payload pattern matching: `references/cobalt-strike.md`
- Zeek dns.log 統計分析で DNS tunneling / iodine / dnscat2: `references/dns-tunneling.md`
- DNS query log の DGA / NXDOMAIN burst / exfil pattern 検出: `references/dns-exfil.md`
- ARPWatch / DAI / pcap での ARP poisoning / MITM 検出: `references/arp-poisoning.md`

## Approach / Workflow

### Phase 1 — log source の確保

```
- Zeek conn.log / dns.log / http.log / ssl.log / files.log
- pcap (live capture or stored)
- DNS query log (firewall / resolver / Cloud DNS)
- NetFlow / sFlow / IPFIX
- ARP table snapshot / DAI log
```

retention 期間 (最低 30-90 日) と signed integrity 確認。

### Phase 2 — baseline 構築

```
- 通常 outbound destination (top N domain / IP)
- 通常通信時間帯 / 周波数
- DNS query 量 / type 比率 (A / AAAA / TXT / NULL)
- 通常 ARP table の MAC ↔ IP mapping
```

### Phase 3 — hunting trigger

| 技法 | trigger |
|---|---|
| C2 beaconing | 一定間隔 (jitter 含む) outbound + 同一 SNI / URI / payload size |
| Cobalt Strike | TLS cert pattern / JA3 fingerprint / Malleable C2 URI / sleep & jitter |
| DNS tunneling | high entropy subdomain / 大量 TXT|NULL query / 短時間 burst |
| DNS exfil | 通常 query 量を超える burst / NXDOMAIN burst / DGA-like 名前 |
| ARP poisoning | 同 IP に対する複数 MAC / 突然の MAC 変更 / gateway MAC の偽装 |

### Phase 4 — TI 突合

```
- 検出した IP / domain / hash を TI feed (VT / OTX / abuse.ch) で確認
- C2 family の判別 (CS / Sliver / Empire / Mythic 等)
- campaign 帰属 (`threat-intel`)
```

### Phase 5 — alert / detection rule 策定

```
- Zeek script で per-flow detection
- Suricata / Snort signature
- Sigma rule
- SIEM (Splunk / OpenSearch / Sentinel) alert
```

### Phase 6 — レポート

```
- 期間 / 検出件数 (true positive / false positive 別)
- 攻撃 chain (initial outbound → C2 dwell → exfil)
- 関与した host / user / 外部 IP / domain
- 残存リスク (rule 改善余地 / 未対応 host)
- 推奨対応 (egress filtering / DNS sinkhole / EDR 連携)
```

## Tools

```
zeek (Bro)
suricata
tshark / tcpdump
RITA (Real Intelligence Threat Analytics)
arkime / moloch
splunk / OpenSearch / ELK
WebFetch
Bash (sandbox)
```

## Related Skills

- `network-analyzer` (incident pcap 解析)
- `reverse-engineering` (CS beacon RE / malware traffic 個別)
- `threat-intel`, `ioc-hunting`
- `dfir`, `blue-teamer`

## Rules

1. **read-only** — hunting 中は capture を read のみ
2. **誤検知耐性** — baseline + 例外 list で false positive を抑制
3. **PII redaction** — query 内容 / SNI / hostname に PII 含まれる、共有時 mask
4. **integrity** — pcap / log の SHA-256 を保持
