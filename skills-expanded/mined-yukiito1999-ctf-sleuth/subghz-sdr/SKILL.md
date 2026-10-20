---
name: subghz-sdr
description: 1 GHz 未満の RF (433 / 868 / 915 MHz の garage / IoT / key fob 等) を SDR で capture / demodulate / replay / fuzz する。CTF hardware / IoT 評価で発火。
category: hardware
tags:
  - sdr
  - sub-ghz
  - rf
  - replay
  - rolling-code
  - flipper
---

# Sub-GHz RF Analysis with SDR

## When to Use

- 433 / 315 / 868 / 915 MHz 帯の RF protocol を解析
- garage / car key / smart meter / weather station / IoT remote の評価
- CTF hardware で sub-GHz signal capture が必要
- Flipper Zero / HackRF / RTL-SDR を持っている

**使わない場面**: WiFi / Bluetooth (→ `wifi-security`)、cellular / 衛星 (規制範囲)。

## Approach / Workflow

### Phase 1 — hardware

```
HackRF One        : 1 MHz ~ 6 GHz, full duplex
RTL-SDR           : 24 MHz ~ 1.7 GHz (DVB-T tuner) — 受信のみ、安価
LimeSDR           : 100 kHz ~ 3.8 GHz, full duplex, 高性能
BladeRF           : 47 MHz ~ 6 GHz
Flipper Zero      : 300-928 MHz 内一部許可帯 (国別制限)
YARD Stick One   : <1 GHz, RfCat
```

帯域 / 国 / 許認可を必ず確認。送信は受信より厳しい。

### Phase 2 — capture

```bash
# RTL-SDR で 433.92 MHz 受信
rtl_sdr -f 433920000 -s 2400000 -g 40 capture.iq

# HackRF
hackrf_transfer -f 433920000 -s 8000000 -r capture.iq

# GQRX / SDR# / SDRplus / CubicSDR で GUI 観察 (waterfall)
```

```
- center frequency の周辺 ±1 MHz を探索
- 信号の幅 / 周期 / sidelobe を見る
- recorded IQ file を後段 demod に渡す
```

### Phase 3 — modulation 同定

```
ASK / OOK (on-off keying)            garage / 車両 key / weather station
FSK 2 / 4                             IoT 仰々しい
GFSK                                   Bluetooth / Zigbee 風 (sub-GHz でも)
ASK + Manchester encoding             RFID 系
LoRa CSS                               LoRaWAN (extracted via 専用 demod)
```

`urh` (Universal Radio Hacker) で modulation 自動判定 + protocol decode。

### Phase 4 — protocol decode

```
- preamble / sync word
- bit / symbol rate
- field 構造 (addr / cmd / data / CRC)
- encoding (NRZ / Manchester / 4b6b / ...)
- error correction (CRC-8 / CRC-16 / Reed-Solomon)
```

`rtl_433` は 200+ device protocol を decode し JSON 出力:

```bash
rtl_433 -F json -G 4
```

### Phase 5 — replay

```
hackrf_transfer -f 433920000 -s 8000000 -t capture.iq -a 1 -x 47
```

簡単な fixed-code remote (古い garage / RF 玩具) は capture → re-transmit で動作。

### Phase 6 — rolling code / 暗号化

```
- KeeLoq (HCS200 系): 64bit key + counter
- AES-CCM / 自前 暗号化
- one-time code (OTP)
- challenge-response
```

rolling code は単純 replay 不可。攻撃手法:

```
- 'rolljam': victim の使用を妨害して code を奪う
- 過去 code 復元 (公開 key 漏洩 + counter 推定)
- vendor 設計の bug
```

法的 / 倫理的に厳格な制限。CTF / 自分の device / 演習でのみ。

### Phase 7 — fuzz / replay tool

```
urh で macro 化
flipper-zero apps (sub-ghz)
flpr / flipper-firmware 改造
pyrtlsdr で Python 自動化
```

### Phase 8 — レポート

```
- 対象 device / 周波数 / modulation / encoding
- protocol structure
- 検出脆弱性 (rolling code 不在 / 弱 key / replay 可能)
- 法令 / 規制範囲の確認
- 修正 (firmware update / vendor 報告)
```

## Tools

```
HackRF One / RTL-SDR / LimeSDR / BladeRF / Flipper Zero / YARD Stick One
GQRX / SDR# / SDRplus / CubicSDR
GNU Radio / urh / inspectrum
rtl_433 / rfcat
WebFetch / WebSearch
Bash (sandbox)
```

## Related Skills

- `wifi-security`, `firmware-iot-security`
- `replay-attack`, `network-analyzer`
- `red-teamer`, `infrastructure`, `bug-bounter`
- `essential-tools`

## Rules

1. **電波法 / 各国規制** — 送信は許認可帯のみ
2. **scope 厳守** — 自分の device / 認可済 演習のみ
3. **隣人 device に影響を出さない**
4. **rolling code 攻撃は engagement 内で**
