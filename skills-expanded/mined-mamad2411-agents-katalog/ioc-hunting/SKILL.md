---
name: ioc-hunting
description: malware sample から IOC (network / file / registry / mutex / certificate / yara pattern) を抽出し、多 source enrichment (VT / OTX / abuse.ch / TI feed) で context 強化、yara / sigma rule で hunting までを統合する。CTF DFIR / TI 開発 / blue team hunting で発火。enrichment / yara の深掘りは references/ 参照
category: intel
tags:
  - ioc
  - extraction
  - enrichment
  - yara
  - sigma
  - hunting
---

# IOC Hunting

## When to Use

- malware sample から network / file / registry IOC を抽出
- threat intel feed / SIEM rule の base material 作成
- 既知 family / variant の identification
- artifact_analysis BC で extract phase

**使わない場面**: malware の RE そのもの (→ `reverse-engineering`)、TI feed / actor 評価 (→ `threat-intel`)。

variant 別の深掘りは references/ を参照: 抽出 IOC を多 source (VT / OTX / abuse.ch / TI feed) で enrichment 自動化 = `references/enrichment.md`、YARA pattern matching で malware / 不審 file / memory / packet 内 signature を hunt = `references/yara.md`。

## Approach / Workflow

### Phase 1 — sample triage

```bash
file sample
sha256sum sample
exiftool sample
strings -n 8 sample | head -200
strings -e l sample | head -50
ssdeep -b sample
```

### Phase 2 — static IOC

```
network IOC:
  - URL / domain (http:// https:// ws://)
  - IP address (IPv4 / IPv6)
  - port
  - DGA seed / pattern
  - User-Agent / header signature

file IOC:
  - dropped file path / filename
  - 自身の hash
  - imphash (PE), TLSH, ssdeep
  - PDB path / build path

registry IOC:
  - HKCU / HKLM key / value (persistence)
  - explorer / scheduled task entries

mutex IOC:
  - 自プロセスが作る named mutex (重複起動防止)

certificate IOC:
  - signed binary なら signer / cert serial / fingerprint

config / encryption:
  - hardcoded AES / RC4 key
  - C2 暗号化 layer の magic bytes

string IOC:
  - 'campaign-id', 'X-Custom: Y'
  - 言語 / culture (pdb path / version)
```

### Phase 3 — 抽出 tool

```bash
# string / strings 系
strings -e l sample | grep -E '^https?://|^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$|^[a-z0-9-]+\.[a-z]{2,}$' | sort -u

# capa (Mandiant) — capability + IOC
capa sample

# floss (Mandiant) — obfuscated string deob
floss sample

# yara で 既知 ruleset を当てる
yara -r yara-rules/ sample

# pe-tree / pefile
python -c "import pefile; pe=pefile.PE('sample'); print(pe.dump_info())"

# manalyze
manalyze --plugins=all sample
```

### Phase 4 — dynamic IOC (隔離 sandbox)

```
- Cuckoo / ANY.RUN / Hybrid Analysis / VMRay
- 生成された file / registry / network call を観察
- DNS sinkhole (FakeDNS) で domain 抽出
- HTTP/HTTPS proxy で URL / payload 抽出
- mitmproxy で TLS 復号
```

### Phase 5 — config 抽出

family-specific config extractor:

```
- Cobalt Strike Beacon: CobaltStrikeParser / 1768.py / cs scan
- Emotet: emocheck / emotet-config-extractor
- TrickBot / IcedID: 専用 extractor
- AsyncRAT: rats-tools
- Lokibot: extract from binary に固有 logic
```

抽出 config から C2 / encryption key / mutex などを直接取得。

### Phase 6 — IOC 形式化

```
STIX 2.1:    {type:"ipv4-addr", value:"1.2.3.4"} ...
MISP event:  attribute / object
sigma:        process / network / file event
yara:         pattern / condition
```

```python
# STIX object 化
from stix2 import Indicator, IPv4Address
i = Indicator(pattern="[ipv4-addr:value = '1.2.3.4']", pattern_type="stix")
```

### Phase 7 — TI feed / SIEM 投入

```
- MISP event 化して community 共有
- threatfox / abuse.ch に submit
- 自社 SIEM の lookup table
- FW / proxy の dynamic blocklist
```

### Phase 8 — レポート

```
- sample identity (hash / family / arch)
- 抽出 IOC (種別 + 数)
- yara / sigma rule の draft
- TI feed 投入予定 / 共有先
- 推奨対応 (block / detection rule)
```

## Tools

```
strings / capa / floss / pefile / manalyze
yara / sigma / sigmatools
ssdeep / TLSH
Cuckoo / ANY.RUN / VMRay
mitmproxy / FakeDNS
WebFetch / WebSearch
Bash (sandbox)
```

## Related Skills

- `threat-intel` (TI feed / actor / report 系)
- `reverse-engineering` (malware RE)
- `dfir`, `blue-teamer`

## Rules

1. **隔離 sandbox**
2. **integrity** — sample SHA-256
3. **共有禁止** — sample の不正配布
4. **TLP** — IOC 共有時の LP color
