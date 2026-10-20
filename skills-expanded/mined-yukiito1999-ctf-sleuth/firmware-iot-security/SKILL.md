---
name: firmware-iot-security
description: IoT device の総合 security assessment。firmware extraction / 内部 malware は references/ で深掘り、network / hardware port は本体 phase で扱う、companion app は android-security/ios-security へ、radio (subGHz / WiFi) は subghz-sdr / wifi-security へ offload。CTF hardware / pentest / 製品 audit で発火
category: hardware
tags:
  - iot
  - firmware
  - binwalk
  - radio
  - companion-app
  - hardware
---

# Firmware / IoT Security

## When to Use

- 認可済 IoT device (camera / lock / lighting / sensor / industrial) の包括 audit
- companion mobile app + cloud backend を含めた評価
- hardware port (UART / JTAG / SWD) の試験

**使わない場面**: 特定 RF (→ `subghz-sdr`、`wifi-security`)、companion mobile アプリ深掘り (→ `android-security` / `ios-security`)。

variant 別の深掘りは references/ を参照: binwalk / unblob で firmware image (router / IoT / camera) を解析し内部 file system / kernel module / 隠 file を抽出 = `references/binwalk-extract.md`、取得 firmware の中の malware / backdoor / unauthorized binary 解析 = `references/firmware-malware.md`。

## Approach / Workflow

### Phase 1 — surface 列挙

```
1. companion mobile app (Android APK / iOS IPA)
2. cloud API / web admin
3. local Wi-Fi / Bluetooth / Zigbee / Z-Wave / Thread / 4G モジュール
4. RF (433 / 868 / 915 MHz)
5. hardware: UART / JTAG / SWD / SPI flash / I2C
6. firmware update mechanism
7. 各種 service (ONVIF / RTSP / MQTT / CoAP / Modbus / OPC UA)
```

### Phase 2 — companion app

```
- Android: android-security / android-security / android-security
- iOS: ios-security / ios-security / ios-security
- pinning bypass で API endpoint を観察
- API 認証 / token / device pairing 流れ
```

### Phase 3 — cloud API

```
- REST / GraphQL / MQTT broker / WebSocket
- 認証: token / device cert / mTLS
- AWS IoT / Azure IoT Hub / GCP IoT Core (deprecated) の典型
- bug bounty: device-to-cloud trust の操作
```

`web-pentester` / `api-security` / `authentication` の手順を流用。

### Phase 4 — local network

```
nmap target_iot_ip
- TCP: 80 / 443 / 22 / 23 / 8080 / 8443 / 554 (RTSP) / 1935 (RTMP) / 1883 (MQTT) / 5683 (CoAP)
- UDP: 5353 (mDNS) / 1900 (SSDP) / 5683 (CoAP) / 502 (Modbus) / 47808 (BACnet)
```

```
ssrf / mDNS amplification / UPnP misuse / Telnet default credential
```

### Phase 5 — Wi-Fi / Bluetooth

`wifi-security` の手順 (WPA handshake / pixie dust / KARMA evil twin)。

```
Bluetooth:
  - btsnoop log
  - bluez を使った scan / pair / 認証 bypass
  - BLE: gatttool / nRF Connect で characteristic 列挙
  - pairing protocol (Just Works / Passkey / OOB)
  - DH MitM (CVE-2018-5383 KNOB)
```

### Phase 6 — RF (sub-GHz)

`subghz-sdr` の手順:

```
HackRF / RTL-SDR で 433 / 868 / 915 MHz 帯 capture
GNU Radio / urh / Universal Radio Hacker で demodulate
rolling code 不在の 古い key fob を replay
```

### Phase 7 — hardware port

```
UART:    115200 8N1 / 9600 8N1 周辺の baud rate を試行 → console 取得
JTAG:    OpenOCD で device 制御 / memory dump
SWD:     ARM Cortex の debug interface
SPI flash: chip-off + bus pirate / Flashrom / soldering / ZIF socket
I2C:     EEPROM / sensor の dump
microSD: bootloader / config が外部 SD で実装される device
```

```bash
# Bus Pirate / FT232H 経由で SPI flash dump
flashrom --programmer ft232h --read flash.bin
```

### Phase 8 — firmware update

```
- update server URL の hardcoded
- TLS pinning 無し → 偽 update server
- signature verification 不在 → 任意 firmware 投入
- update file が暗号化されない / 弱 key
- rollback prevention 無し (古い vulnerable firmware に戻せる)
```

### Phase 9 — レポート

```
- device 情報 (vendor / model / firmware version / hardware revision)
- attack surface map
- 検出脆弱性 (severity 別)
- 推奨修正 (vendor 通報 / 自社運用ならパッチ計画)
- 修正できない場合の workaround (network segment / IDS rule)
```

## Tools

```
binwalk / unblob
android-security / mobsf / frida / objection (companion app)
nmap / mqtt-tools / coapthon
HackRF / RTL-SDR / GNU Radio / Universal Radio Hacker
OpenOCD / Bus Pirate / FT232H / Flashrom
WebFetch / WebSearch
Bash (sandbox)
```

## Related Skills

- `subghz-sdr`, `wifi-security`
- `web-pentester`, `api-security`, `authentication`, `client-side`
- `android-security`, `ios-security`
- `network-analyzer`, `replay-attack`, `performing-ssl-tls-security-assessment`
- `bug-bounter`, `web-bounty`, `hackerone`
- `red-teamer`, `infrastructure`, `cloud-pentester`

## Rules

1. **明示許可** — 自分が所有 or vendor / customer engagement の認可必須
2. **物理破壊リスク** — chip-off / 半田作業は device を壊す
3. **法令** — 一部 RF 帯は許認可必要
4. **vendor 連携** — coordinated disclosure を進める
