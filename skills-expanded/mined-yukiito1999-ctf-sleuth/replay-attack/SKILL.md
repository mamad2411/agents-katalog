---
name: replay-attack
description: 取得した token / session / API request / RFID / WiFi handshake / 認証 message を再送して認可を取る replay 攻撃を実証する。CTF / pentest / authorized engagement で発火。
category: network
tags:
  - replay
  - token
  - session
  - rfid
  - protocol
  - authorization
---

# Replay Attack

## When to Use

- 取得 token / session cookie / API request / RFID raw / WiFi 4-way handshake / Kerberos ticket / SAML assertion / OAuth code 等を再送する余地を評価
- 認証 protocol の nonce / timestamp / replay protection を評価
- CTF で SHA / HMAC / counter ベースの replay 系問題

**使わない場面**: 暗号方式そのものの解析 (→ `performing-cryptographic-audit-of-application`)、token forge (→ `testing-jwt-token-security`)。

## Approach / Workflow

### Phase 1 — capture / 取得

```
network: pcap で capture
mitmproxy / Burp で proxy intercept
RFID: Proxmark3 で raw dump
RF: HackRF / SDR で RF raw
SDR captured signal: rtl-sdr / GNU Radio で record
serial / IoT: USB / UART で capture
```

### Phase 2 — replay 試験対象

| 種別 | 試験 |
|---|---|
| HTTP request / API | curl / Burp Repeater で同 request 再送、認可成立確認 |
| Cookie / Session | 別 session で cookie 流用 |
| JWT / OAuth | 期限内であれば再使用、jti 検証無いか |
| Kerberos ticket | mimikatz / Pass-the-Ticket |
| SAML assertion | 同 assertion 再送、`InResponseTo` / `NotOnOrAfter` 検証 |
| WiFi 4-way handshake | aircrack-ng で WPA hash 抽出 (replay 自体ではないが capture を使う) |
| RFID UID | Proxmark3 で同 UID emulation |
| 433 / 868 MHz garage / car key | rtl_433 + rolling code 確認 |
| OTP / SMS code | 取得後 短時間に再使用、burn rate 試験 |
| 数字 PIN replay | 入力 form の event 解析 |

### Phase 3 — replay protection の評価

```
- nonce: 一意 challenge を server が発行し client が反映、再使用不能
- timestamp: 制限時間内のみ valid
- counter: monotonic increase、過去 counter 拒否
- HMAC: 秘密鍵で MAC、改竄不能
- TLS / mTLS: 暗号化通信路、外部からの replay 不能
- DPoP / mTLS bound: token が cert / key に紐付く
```

target が:

```
- nonce check 無し → replay 成立
- timestamp 緩い (±60 sec も) → 短時間 replay 成立
- counter なし → 過去 message 永久 replay
- HMAC なし → 改竄 + replay 両方成立
```

### Phase 4 — 影響評価

```
- 認証 bypass (login の form data replay)
- 認可越え (他人の transfer request replay)
- session 盗用 (cookie replay)
- 物理 access (RFID UID emulation で扉開錠)
- 車両 unlock (rolling code 不在の古い system)
```

### Phase 5 — 修正提案

```
- 認証 protocol に nonce / timestamp / counter 追加
- HMAC / 公開鍵署名 で 改竄防御
- TLS / mTLS で経路保護
- short-lived token + rotation
- DPoP / sender-constrained token
- replay-detection cache (jti / sid のサーバ側 dedup)
```

### Phase 6 — レポート

```
- 取得方法 / capture 環境
- replay 成立した protocol / message
- 影響 (認証 bypass / authorization 越え / 物理 access)
- 推奨修正
```

## Tools

```
mitmproxy / burp Repeater
curl
aircrack-ng (WiFi)
Proxmark3 / RFIDler (RFID)
HackRF / rtl-sdr / GNU Radio (RF)
WebFetch
Bash (sandbox)
```

## Related Skills

- `web-pentester`, `api-security`, `authentication`, `client-side`, `web-app-logic`
- `testing-jwt-token-security`, `testing-oauth2-implementation-flaws`
- `network-analyzer`
- `wifi-security`, `subghz-sdr`, `firmware-iot-security`
- `performing-cryptographic-audit-of-application`
- `system` (Kerberos PtT)

## Rules

1. **明示許可**
2. **最小実証 + cleanup**
3. **取得 token / RFID UID** — sealed area に
4. **物理 access 試験** — 委託契約に明記された場合のみ
