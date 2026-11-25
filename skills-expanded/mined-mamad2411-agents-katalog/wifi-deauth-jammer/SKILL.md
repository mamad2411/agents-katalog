---
name: wifi-deauth-jammer
version: 2.0.0
description: 'ESP32 Time-Division WiFi Killer v12 - Targeted deauth + nRF24 CW jamming
  alternating phases. v2.0: PhantomRF ESP32-S3 raw TX (esp_wifi_80211_tx) verified,
  BrakTooth 28 CVE BT Classic LMP exploits, ESPwn32 link-layer injection, cross-chip
  support (S3/C3/C6/H2).'
category: embedded-security
license: MIT
metadata:
  hermes_origin: import
tags:
- esp32
- nrf24
- wifi
- deauth
- jamming
- penetration-testing
- bt-classic
- ble-injection
related_skills:
- wifi-dualband-jammer
- rf-multi-protocol-jammer
- bluetooth-jammer-sweep
---

# ESP32 Time-Division WiFi Killer v12 (v2.0)

雙模式時分多工攻擊：
- **Phase A (WiFi ON, 500ms)**: Promiscuous sniff + Targeted deauth + Handshake/PMKID capture
- **Phase B (CW ON, 500ms)**: 雙 nRF24 PA+LNA 200mW @ 10kHz hop 全頻干擾

## 硬體需求

- ESP32 DevKit (WROOM-32)
- 2x nRF24L01+ PA+LNA 模組
- 接線：
  - VSPI: CE=26, CSN=25, SCK=18, MOSI=23, MISO=19
  - HSPI: CE=15, CSN=21, SCK=14, MOSI=13, MISO=12

## 檔案結構

```
esp32-wifi-killer-v12/
├── SKILL.md
├── firmware/
│   └── esp32_wifi_killer_v12.ino    # 主韌體
├── scripts/
│   ├── flash.sh                     # 一鍵燒錄腳本
│   └── monitor.sh                   # Serial monitor 腳本
└── references/
    └── wiring.md                    # 接線圖說明
```

## 快速開始

```bash
# 1. 進入 skill 目錄
cd ~/.hermes/profiles/trade/skills/esp32-wifi-killer-v12

# 2. 一鍵編譯燒錄
./scripts/flash.sh

# 3. 開啟監控
./scripts/monitor.sh
```

## 攻擊流程

1. **掃描階段** (Phase A): 掃描所有 2.4GHz channel，建立 AP/Client 資料庫
2. **攻擊階段** (Phase A): 對鎖定的 client 發送 targeted deauth (每輪 8 封包)
3. **干擾階段** (Phase B): 雙 nRF24 發射 200mW CW，10kHz 跳頻覆蓋全 ISM 頻段
4. **循環**: 每 500ms 切換一次，形成「踢下線 → 阻重連 → 踢下線」閉環

## 關鍵指標

| 指標 | 數值 |
|------|------|
| WiFi 階段 | 500ms |
| CW 階段 | 500ms |
| Deauth burst | 8 pkts/client/round |
| nRF24 功率 | 200mW (PA_MAX) |
| CW 跳頻率 | 10 kHz |
| 覆蓋通道 | 34 (Wi-Fi 1-13 + BLE + 補頻) |

## 適用目標

- ✅ 一般 2.4GHz Wi-Fi (WPA2, 無 PMF)
- ✅ IoT 裝置、舊手機、ESP8266 等
- ❌ WPA3 + PMF (802.11w) 強制開啟的 Mesh (Deco, Eero 等)
- ❌ 5GHz 頻段 (硬體限制)

## 進階用法

### 鎖定特定目標

編輯 `firmware/esp32_wifi_killer_v12.ino` 中的目標 BSSID：

```cpp
// 在 deauthAllClients() 中加入過濾
if (memcmp(clients[i].apBssid, targetBSSID, 6) != 0) continue;
```

### 調整時分比例

```cpp
#define PHASE_WIFI_MS  800   // 增加 WiFi 時間以抓更多 handshake
#define PHASE_CW_MS    200   // 減少 CW 時間
```

## 法律聲明

**僅供授權滲透測試、教學研究使用。未經授權攻擊他人網路屬違法行為。**

## Related to Umbrella Skill

This skill is the packaged implementation of the TDM v12 architecture documented in **`esp32-embedded-development`** → `references/time-division-multiplex-v12.md`. That reference contains the full architecture rationale, phase transition code, client tracking logic, EAPOL/PMKID capture, and hardware wiring details.

## Linked References (in esp32-embedded-development)

- `references/time-division-multiplex-v12.md` — Full TDM architecture documentation
- `references/nrf24-wifi-self-jamming.md` — Why CW + WiFi RX are mutually exclusive
- `references/wifi-targeted-deauth-architecture.md` — Phase A detail (targeted deauth + PMKID capture)
- `references/nrf24-only-jammer-v6.md` — Phase B detail (pure CW jammer)
- `references/ble-notification-flood-v12.md` — Alternative for Bluetooth disruption
- `references/si24r1-clone-detection.md` — Critical for verifying nRF24 modules are genuine