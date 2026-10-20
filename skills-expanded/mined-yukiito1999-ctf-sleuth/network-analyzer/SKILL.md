---
name: network-analyzer
description: pcap / live capture から protocol dissect・異常検出・credential 抽出を進める汎用 network 解析 skill。CTF forensics pcap 系、artifact_analysis BC の PCAP / PCAPNG、HTB の network 入口、DFIR で発火。
category: network
tags:
  - pcap
  - wireshark
  - tshark
  - protocol
  - credentials
  - anomaly
---

# Network Traffic Analyzer (general)

## When to Use

- pcap / pcapng / live capture が evidence で渡された
- protocol 種別を識別して攻撃 / exfil 痕跡を抽出
- credential / token / file の clear-text 漏洩確認
- 全 wireshark / tshark / zeek 系の pcap 解析の入口

**使わない場面**: C2 hunting / beaconing 解析のみ (→ network-hunter 系 skill — `network-hunter` / `hunting-for-*` 等。今後 `network-hunter` に統合予定)、Cobalt Strike beacon RE (→ `reverse-engineering`)。

tool / 観点別の深掘りは references/ を参照: 侵害 incident pcap からの flow / IOC 抽出 = `references/incidents.md`、wireshark の操作 quickstart = `references/wireshark-quick.md`、wireshark を中核に network forensics の deep workflow = `references/wireshark-deep.md`、tshark / pyshark の batch 解析 = `references/tshark.md`、Zeek (Bro) の metadata log 運用 = `references/zeek.md`。

## Approach / Workflow

### Phase 1 — triage

```bash
file capture.pcap
sha256sum capture.pcap
capinfos capture.pcap                  # 概要 (期間 / packet 数 / プロトコル)
tshark -r capture.pcap -q -z io,phs    # protocol hierarchy
tshark -r capture.pcap -q -z conv,tcp  # TCP conversation
tshark -r capture.pcap -q -z conv,udp
tshark -r capture.pcap -q -z conv,ip
tshark -r capture.pcap -q -z dns,tree
tshark -r capture.pcap -q -z http,tree
```

### Phase 2 — 異常 protocol / 急増

```bash
# protocol 比率
tshark -r capture.pcap -q -z io,phs | head -30

# top talker
tshark -r capture.pcap -q -z endpoints,ip
tshark -r capture.pcap -q -z endpoints,tcp
```

普段の baseline と比較し、過剰 ICMP / DNS / 不審 port 接続を highlight。

### Phase 3 — credentials / token 抽出

clear text を検出:

```bash
# HTTP basic auth
tshark -r capture.pcap -Y 'http.authorization' -T fields -e ip.src -e ip.dst -e http.authorization

# FTP / Telnet (legacy)
tshark -r capture.pcap -Y 'ftp.request.command in {USER, PASS}'
tshark -r capture.pcap -Y 'telnet'

# SMTP / IMAP / POP の AUTH LOGIN (base64)
tshark -r capture.pcap -Y 'smtp or imap or pop'

# SMB / NTLM / Kerberos
tshark -r capture.pcap -Y 'ntlmssp or kerberos'

# WPA/WPA2 handshake (要 monitor mode capture)
tshark -r capture.pcap -Y 'eapol'
```

`pcredz` / `credump` で自動抽出も。

### Phase 4 — file carving

HTTP / FTP / SMB に乗った file:

```
wireshark GUI:
  File → Export Objects → HTTP / SMB / IMF / TFTP / DICOM / ...

tshark で pcap 内 stream 抽出:
tshark -r capture.pcap -Y 'http.response_for.uri' --export-objects http,./out
```

抽出した file は SHA-256 + yara で family 同定 → `ioc-hunting`。

### Phase 5 — TLS / SSL

clear text にならない場合:

```
- SNI (Server Name Indication) は平文で見える
- JA3 / JA4 fingerprint で client identification
- pre-master secret が手元にある (SSLKEYLOGFILE 環境) なら wireshark で復号
```

### Phase 6 — 攻撃 pattern の検出

```bash
# port scan (SYN flood / SYN-ACK ratio)
tshark -r capture.pcap -Y 'tcp.flags.syn==1 and tcp.flags.ack==0' -T fields -e ip.src -e tcp.dstport | sort | uniq -c | sort -rn | head

# ARP poisoning
tshark -r capture.pcap -Y 'arp' -T fields -e arp.src.proto_ipv4 -e arp.src.hw_mac

# DNS exfil 兆候 (短時間に大量 / 長 query)
tshark -r capture.pcap -Y 'dns.qry.name' -T fields -e frame.time -e dns.qry.name | awk '{ if(length($NF)>50) print }'

# C2 beaconing (定間隔 outbound)
tshark -r capture.pcap -Y 'ip.dst==<dst>' -T fields -e frame.time_epoch | awk 'NR>1{print $1-prev}{prev=$1}' | sort | uniq -c | sort -rn
```

詳細は `network-hunter` / `reverse-engineering`。

### Phase 7 — 既知 family signature

```
- Cobalt Strike: x.509 default cert / GET /pixel.gif / POST /submit.php / sleep+jitter
- Metasploit: stage 起動の特徴 (短い 4 byte length + payload)
- Sliver: 自前 mTLS / DNS / HTTP profile
- Empire: PowerShell encoded payload
```

`reverse-engineering`、`network-hunter` で深掘り。

### Phase 8 — レポート / IOC

```
- 期間 / パケット数 / 主要 protocol
- 上位 talker (IP / domain)
- 不審 protocol / port
- 抽出 credential (件数 / redact)
- 抽出 file (hash / 推定種別)
- 推定攻撃 (port scan / ARP poisoning / DNS exfil / C2 beaconing)
- IOC (IP / domain / JA3 / 暗号化 client fingerprint)
```

## Tools

```
tshark / wireshark / tcpdump
zeek / suricata
pcredz / credump
yara
WebFetch
Bash (sandbox)
```

## Related Skills

- `reverse-engineering` (C2 protocol 再構成 / malware traffic)
- `network-hunter` (これらは `network-hunter` に統合予定)
- `replay-attack`, `performing-ssl-tls-security-assessment`
- `ioc-hunting`

## Rules

1. **read-only / copy** — pcap を直接 edit しない (mergecap や editcap は別 file に出力)
2. **integrity** — SHA-256 保持
3. **PII redaction** — credential / hostname / 個人 IP を共有 report で mask
4. **timezone** — tshark 出力を UTC で統一
