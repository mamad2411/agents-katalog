---
name: bug-bounter
description: bug bounty 全般の方法論。scope 定義 → 偵察 → 列挙 → 脆弱性評価 → triage → 報告 → 影響評価 → triagecycle までを体系化。OSINT CTF や bug bounty platform 利用で発火。
category: bug-bounty
tags:
  - bug-bounty
  - methodology
  - scope
  - triage
  - report
  - disclosure
---

# Bug Bounty Methodology

## When to Use

- HackerOne / Bugcrowd / Intigriti / YesWeHack 等の program に参加
- 認可された scope の web / api / mobile / cloud / OS が target
- OSINT CTF で 攻撃面網羅型問題

**使わない場面**: scope 外の active 試験、無認可の私的調査。

## Approach / Workflow

### Phase 1 — program / scope 確認

```
- scope 内 asset (subdomain wildcard / 特定 host / mobile app / API endpoint)
- out-of-scope (legacy / staging / 第三者 SaaS)
- in-scope vulnerability class (RCE / SQLi / XSS / 認可 / 機密漏洩)
- excluded vulnerability class (self-XSS / clickjacking on non-sensitive / theoretical)
- testing rules (rate limit / no DoS / no destructive)
- bounty range (Critical / High / Medium / Low)
- disclosure policy (vendor coordinated / public timeline)
```

### Phase 2 — 偵察 (passive 優先)

`reconnaissance` の手順:

```
- subdomain enum (amass / subfinder / crt.sh)
- DNS / TLS cert 履歴
- Wayback / archive
- GitHub OSINT (`github-workflow`)
- 技術 stack (`techstack-identification`)
```

### Phase 3 — 列挙 (active)

```
- web crawl (ffuf / katana)
- HTTP fingerprint / version
- API endpoint 発見 (sourcemap / swagger)
- mobile app の API 構造 (frida / objection)
```

### Phase 4 — 脆弱性 hunting

各 class に該当 skill を呼び出し:

```
web:        web-pentester / api-security / client-side / server-side / web-app-logic / injection / authentication / 各 specific exploit skill
mobile:     android-security / android-security / android-security / android-security / android-security / ios-security / ios-security / ios-security
cloud:      cloud-pentester / cloud-pentester / cloud-pentester / kubernetes-security / cloud-pentester
infra:      infrastructure / performing-ssl-tls-security-assessment / network-hunter
```

### Phase 5 — high-impact 候補に優先

```
P0 (critical):  RCE / 認証 bypass / 大規模 PII 漏洩 / 全アカウント乗取
P1 (high):       SQLi / SSRF / 任意 file upload / privilege escalation
P2 (medium):     XSS (stored on auth page) / IDOR (中規模)
P3 (low):        XSS (reflected) / CSRF on minor action / info disclosure
P4:              self-XSS / theoretical / no impact
```

### Phase 6 — 報告書

```markdown
# <脆弱性タイトル>

## Summary
<1 段落で何が起きるか>

## Severity
P0 (CVSS X.Y)

## Affected Asset
- URL / endpoint / app / API

## Reproduction Steps
1. ...
2. ...
3. ...

## Proof of Concept
\`\`\`
<最小 PoC>
\`\`\`

## Impact
<被害>

## Remediation
<修正提案>

## References
<RFC / OWASP>
```

screenshot / video を添付。production 影響なしで再現可能な手順を最優先。

### Phase 7 — triage / コミュニケーション

```
- triage に関する追加質問に短時間で返事
- duplicate / known issue は受け入れる
- triage 結果に異議があれば 公正な再評価依頼
- 公開 timeline (90 日 + α) を尊重
```

### Phase 8 — disclosure

```
- 修正完了 + program permission で writeup 公開可
- 一般化された learning として共有 (specific PoC を変える)
- CVE 申請が適切なら MITRE 経由で
```

## Tools

```
amass / subfinder / dnsx / shodan / censys
ffuf / katana / waybackurls / linkfinder
nuclei / dalfox / xsstrike
burp / mitmproxy
WebFetch / WebSearch
Bash (sandbox)
```

## Related Skills

- `web-bounty`, `hackerone`, `osint`, `reconnaissance`, `techstack-identification`, `github-workflow`
- `web-pentester`, `api-security`, `injection`, `client-side`, `server-side`, `web-app-logic`, `authentication`
- `injection`, `server-side`, `testing-jwt-token-security`, `testing-oauth2-implementation-flaws`, `client-side`
- `android-security`, `ios-security`
- `cloud-pentester`, `kubernetes-security`, `cloud-pentester`, `detection-cloud-anomalies`
- `cve-exploitation`, `source-code-scanning`
- `red-teamer`, `system`, `infrastructure`
- `essential-tools`, `coordination`, `script-generator`

## Rules

1. **scope 厳守**
2. **non-destructive default**
3. **PII 取扱** — 取得した user data の最小確認 + sealed report
4. **責任ある開示** — vendor 修正後に公開
5. **multiple bounty 重複報告禁止**
