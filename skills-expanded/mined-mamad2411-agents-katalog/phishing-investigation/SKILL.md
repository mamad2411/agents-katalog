---
name: phishing-investigation
description: phishing email の header 解析 (Received / SPF / DKIM / DMARC / ARC) と Certificate Transparency log 監視による typo-squatting / phishing 用ドメインの早期検出を統合する。CTF DFIR / phishing IR / OSINT で発火。CT log 監視の深掘りは references/ct-log.md
category: intel
tags:
  - phishing
  - email
  - header
  - certificate-transparency
  - dmarc
---

# Phishing Investigation

## When to Use

- 不審 email の header を解析して送信元を特定
- BEC (Business Email Compromise) 調査
- phishing campaign の actor 紐付け
- SPF / DKIM / DMARC / ARC の認証結果評価

**使わない場面**: 添付 PDF / Office malware の解析 (→ `reverse-engineering`)、mailbox 全体の forensic acquisition (→ `disk-forensics`)、SaaS storage の email / 共有 (→ `cloud-forensics`)。

CT log 監視の深掘りは `references/ct-log.md`: crt.sh / Certstream で phishing 用 typo-squatting / impersonation / 不正発行 cert を監視する手順。

## Approach / Workflow

### Phase 1 — header 取得

```
クライアント別:
  Gmail: メッセージを開く → 三点メニュー → "原文を表示"
  Outlook: ファイル → プロパティ → インターネットヘッダー
  Thunderbird: 表示 → メッセージのソース
  M365 admin: Message Trace
mbox / .eml / PST から抽出
```

`.eml` を保存し header 部 (RFC 5322) のみ抽出。

### Phase 2 — Received chain

最下位 (送信側) から最上位 (受信側) に時系列で並ぶ:

```
Received: from <claimed_hostname> (<actual_hostname> [actual_ip])
        by <our_mta> with <protocol>;
        <date>
```

`actual_ip` が真の送信源。`claimed_hostname` は偽装可能。internal infrastructure を経由している場合、最も外側の Received が真の起点。

### Phase 3 — 認証結果

`Authentication-Results:` header を確認:

```
spf=pass / fail / softfail / neutral / none / temperror / permerror
dkim=pass / fail / none
dmarc=pass / fail / quarantine / reject
arc=pass / fail
```

```
spf=pass + DKIM=pass + DMARC=pass → 多くの場合 legitimate
spf=fail / dkim=fail → spoofing 兆候
DMARC=reject なのに着信 → 受信側 policy が緩い (alignment 確認)
```

### Phase 4 — DKIM signature 検証

```
DKIM-Signature: v=1; a=rsa-sha256; d=domain.com; s=selector1;
                h=from:subject:date:to; b=<signature>;
```

selector の TXT record (`selector._domainkey.domain`) と DKIM signature を組合せて検証:

```
dkim-verify-tool / opendkim-testkey
```

`d=` (signing domain) と `From:` (visible domain) が一致しないと spoofing 兆候 (DMARC alignment 失敗)。

### Phase 5 — SPF 検証

```
Return-Path: <bounce@domain.com>
```

`bounce@domain.com` の domain の SPF (TXT record) で `actual_ip` が許可されているか:

```bash
dig +short txt domain.com | grep 'v=spf1'
```

`include:` を再帰的に展開し、actual_ip が含まれるか確認。

### Phase 6 — phishing 兆候

```
- From: 「会社名 <attacker@外部.com>」 風の display name 偽装
- Reply-To: が From: と異なり、attacker のものに
- Subject 行に urgency / fear / authority (「至急」「アカウント停止」「上司から」)
- attached file (xlsm / docm / html / iso / lnk / zip-in-zip / svg)
- short URL / typo-squat domain (paypa1.com)
- IP geolocation が actor の国 (TI feed と相関)
- BCC で大量 receiver
- DKIM 不一致
- ARC chain が壊れている
```

### Phase 7 — campaign attribution

```
- 送信 IP / ASN を VirusTotal / abuse.ch / OTX で検索
- DKIM selector 名で過去 campaign 検索
- Subject / 文言の TLSH / fuzzy match
- 添付 hash で family identification
```

詳細は `threat-intel`、`threat-intel`。

### Phase 8 — レポート / IOC

```
- 受信時刻 / from / to / subject
- 真の送信 IP / ASN / country
- 認証結果 (SPF / DKIM / DMARC)
- 推定 spoofing 手法
- 添付 hash + 推定 family
- IOC (IP / domain / hash / DKIM selector / SPF includes)
- 推奨 (DMARC=reject 強化 / mail filter rule / awareness)
```

## Tools

```
mailheaders parser (websites / CLI)
opendkim-testkey / dkim-verify
dig / host
whois / RDAP
WebFetch / WebSearch
Bash (sandbox)
```

## Related Skills

- `threat-intel` (campaign / actor / report)
- `ioc-hunting` (IOC enrichment)
- `disk-forensics` (Outlook PST / mailbox 全体)
- `osint`, `dfir`, `blue-teamer`, `social-engineering`
- `detection-web` (phishing → OAuth consent flow)

## Rules

1. **PII redaction** — 共有 report で recipient / 内容を redact
2. **integrity** — `.eml` の SHA-256 保持
3. **法令 / privacy** — 私信の取扱に注意
4. **誤検知耐性** — 正規 mail relay (Mailgun / Sendgrid) の chain を allowlist
