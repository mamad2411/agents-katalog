---
name: detection-web
description: web の defender 視点で API gateway / WAF / OAuth audit log を統計検出する横断 skill。BOLA / IDOR / rate limit 突破 / credential scanning / SQLi WAF bypass / OAuth token 盗難 / 不審 OAuth consent grant を扱う。CTF DFIR / blue team SOC / 攻撃 visibility 評価で発火。観点別の深掘りは references/ 参照
category: defender
tags:
  - web-detection
  - api-gateway
  - waf
  - oauth
  - access-log
  - blue-team
---

# Web Detection

## When to Use

- API gateway / reverse proxy / WAF / OAuth provider の log から攻撃シグネチャや異常パターンを抽出する
- post-incident 調査で「侵入されたか」「列挙されたか」を log で確認
- bug bounty / pentest で防御 visibility の評価
- CTF DFIR で web 侵害の証拠抽出

**使わない場面**: 攻撃側の web 試験 (→ `web-pentester` / `injection` / `client-side` / `server-side`)、cloud 全般の anomaly hunting (→ `detection-cloud-anomalies`)、network 通信 hunting (→ `network-hunter`)。

観点別の深掘りは references/ を参照: SQLi 試行 / 成功 / WAF bypass を ModSecurity / AWS WAF / Cloudflare / Imperva log から抽出 = `references/sql-waf.md`、OAuth access / refresh token の窃取・replay を log と conditional access で検出 = `references/oauth-theft.md`、illicit consent grant 攻撃の不審 OAuth アプリ同意を Microsoft Graph / Entra audit log から検出 = `references/oauth-consent.md`。

## Approach / Workflow

### Phase 1 — log の取り込み

| ソース | 取得 |
|---|---|
| AWS API Gateway | CloudWatch Logs (JSON formatted access logs) |
| Kong | `/admin/log` / file `kong-access.log` |
| Nginx | combined / json_log format |
| ALB / CloudFront | S3 bucket への access log |

```python
import pandas as pd
df = pd.read_json('access.log', lines=True)
# 主要 column: timestamp, ip, method, path, status, latency, request_id, user_id (auth context)
```

### Phase 2 — 観点別の検出

#### BOLA / IDOR の徴候

```python
# 単一 user / IP が短時間に異なる resource_id を多数参照
g = df.groupby(['user_id', pd.Grouper(key='ts', freq='1min')])['resource_id'].nunique()
g[g > 50]  # 1 分間に 50 以上の異なる ID を触る user
```

#### rate limit bypass

```python
# 429 を返したのに同 IP / API key が継続して 200 も得ている → bypass
df.groupby('ip')['status'].value_counts()
```

#### credential scanning

```python
# 同 IP から /login 等への高頻度 401 → brute force
auth_paths = df[df['path'].str.contains('/login|/signin|/oauth/token', regex=True)]
auth_paths.groupby('ip')['status'].value_counts()
```

### Phase 3 — 注入 / payload 検出

```python
import re
SQLI = re.compile(r"(\bUNION\b|\bSELECT\b|\bSLEEP\(|\bWAITFOR\b|0x[0-9a-f]+|--)", re.I)
XSS  = re.compile(r"(<script|onerror=|javascript:|<svg|alert\()", re.I)
PATH = re.compile(r"(\.\./|%2e%2e|/etc/passwd|c:\\\\windows)", re.I)
SSRF = re.compile(r"(169\.254\.169\.254|metadata\.google\.internal|localhost|127\.0\.0\.1|gopher://|file://)", re.I)

for name, pat in [('sqli', SQLI), ('xss', XSS), ('traversal', PATH), ('ssrf', SSRF)]:
    hits = df[df['path'].str.contains(pat) | df['query'].str.contains(pat)]
    print(f"{name}: {len(hits)}")
```

### Phase 4 — 異常 baseline 検出

```python
from scipy import stats
z = stats.zscore(df.groupby('ip')['request_id'].count())
heavy_ips = df.groupby('ip')['request_id'].count()[z > 3]
```

```python
# user-agent 多様性 (botnet 兆候: 単一 IP で多数 UA)
df.groupby('ip')['ua'].nunique().sort_values(ascending=False).head()
```

### Phase 5 — geographic / ASN 分布

```python
import geoip2.database
reader = geoip2.database.Reader('GeoLite2-Country.mmdb')
df['country'] = df['ip'].map(lambda ip: reader.country(ip).country.iso_code)
df.groupby('country')['request_id'].count().sort_values(ascending=False).head(10)
```

### Phase 6 — 時系列可視化

```python
import matplotlib.pyplot as plt
df.set_index('ts')['status'].resample('5min').apply(lambda s: (s>=400).mean()).plot()
plt.title('error rate over time')
```

### Phase 7 — alert criteria（運用化）

```
- 1 user / API key で 1 分 50 IDs 超えの参照 → 監視
- 401 が 10 分で 50 超 → credential scanning
- 429 後の 200 増加 → rate limit bypass
- payload 系 regex hit → triage キュー
- 短時間に複数 country からの同 user_id → セッション窃取
```

### Phase 8 — レポート

```
- 期間 / 件数
- top suspicious IPs / users
- 推定攻撃カテゴリ (BOLA / brute / SQLi / SSRF)
- IOC (IP / UA / payload / URL pattern)
- 推奨対応 (block / WAF rule / app 側修正)
```

## Tools

```
pandas / numpy / scipy
GeoIP2 / MaxMind
jq
splunk / OpenSearch / Athena (大規模 log 用)
WebFetch / WebSearch
Bash (sandbox)
```

## Related Skills

- `web-pentester`, `api-security`, `web-app-logic` (offensive 視点)
- `detection-cloud-anomalies` (cloud 全般)
- `network-analyzer`, `network-hunter` (network 通信)
- `dfir`, `blue-teamer`

## Rules

1. **PII redaction** — 共有時は user_id / email を hash / mask
2. **保存期間** — engagement / incident scope 内のみ。期限後に削除
3. **誤検知耐性** — 内部 user / VA scanner / monitoring tool の活動を allowlist
4. **ベースライン取得** — 「平常時」の log との差分で語る
