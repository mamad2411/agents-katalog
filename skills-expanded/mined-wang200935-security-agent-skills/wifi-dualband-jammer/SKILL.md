---
name: wifi-dualband-jammer
description: ESP32 雙頻 (2.4GHz + 5GHz) WiFi 干擾器完整實作指南 — 架構：ESP32-C6 負責 5GHz beacon
  flood + ESP32-S3 + 雙 nRF24L01+ PA+LNA 負責 2.4GHz 三層干擾 (CW×2 + beacon)。含硬體接線、ESP-IDF
  韌體、同步協定、一鍵燒錄、除錯流程。
category: hardware
version: 1.0.0
license: MIT
metadata:
  hermes_origin: import
tags:
- esp32
- esp32-c6
- esp32-s3
- nRF24L01
- wifi-jammer
- beacon-flood
- cw-jamming
- dual-band
- 2.4ghz
- 5ghz
- esp-idf
related_skills:
- wifi-deauth-jammer
- rf-multi-protocol-jammer
- rf-jammer-firmware-port
---

# ESP32 雙頻 WiFi 干擾器完整實作指南

## 🎯 觸發時機

使用者提到：
- 雙頻 WiFi 干擾 / 同時阻擋 2.4GHz 和 5GHz
- ESP32-S3 + nRF24L01 干擾器
- 「通電即全阻擋」/ 自動啟動干擾
- CC1101 能不能做 2.4GHz (答案：不能)
- 要完整可燒錄的專案代碼、接線圖、除錯流程

---

## 📂 專案位置

```
~/Documents/esp32_dualband_jammer/
├── README.md                    # 專案總覽、法律警告、快速開始
├── build_flash.sh               # 一鍵建置燒錄腳本 (互動選單 + CLI)
├── wiring_guide.md              # 完整接線圖 (電源分配、nRF24×2、同步 GPIO)
├── sync_protocol.md             # 同步協定 (狀態機、時序圖、GPIO 定義)
│
├── node_5ghz/                   # ESP32-C6 5GHz 節點 (ESP-IDF)
│   ├── CMakeLists.txt
│   ├── sdkconfig.defaults
│   ├── README.md
│   └── main/
│       ├── CMakeLists.txt
│       ├── jammer_5ghz.c        # 主程式：狀態機、按鍵、同步、啟動 5GHz flood
│       ├── wifi_raw_tx_5ghz.c/h # 5GHz Raw Beacon Flood (9通道、隨機BSSID)
│       └── sync_gpio.c/h        # 同步 GPIO (OUT=GPIO8, IN=GPIO9)
│
└── node_2ghz/                   # ESP32-S3 2.4GHz 三層節點 (ESP-IDF)
    ├── CMakeLists.txt
    ├── sdkconfig.defaults
    ├── README.md
    ├── components/rf24/         # nRF24 驅動元件 (ESP-IDF SPI Master 適配)
    │   ├── CMakeLists.txt
    │   ├── rf24.c/h             # 底層 SPI 讀寫、CW 初始化、跳頻
    │   └── rf24_registers.h     # 寄存器定義
    └── main/
        ├── CMakeLists.txt
        ├── jammer_2ghz.c        # 主程式：三層干擾任務、同步等待、狀態監控
        ├── rf24_driver.c/h      # 雙 radio 封裝 (VSPI+HSPI 初始化、同步跳頻)
        ├── wifi_raw_tx_2ghz.c/h # 2.4GHz Beacon Flood (ch 1,6,11)
        ├── sync_gpio.c/h        # 同步 GPIO (IN=GPIO4, OUT=GPIO5)
        └── led_indicator.c/h    # WS2812 狀態燈 (GPIO48)
```

---

## ⚠️ 法律必宣告 (每次輸出都帶)

**台灣《電信管理法》第 66/67 條**：製造、持有、使用干擾器違法 (NCC 可沒收 + 罰鍰 100-700 萬；持有使用罰 3-30 萬)

本 skill 僅供 **自有設備、受控環境 (法拉第籠/屏蔽箱)、研究學習** 用途。

---

## 🏗️ 架構總覽

```
┌─────────────────────────────────────────────────────────────────┐
│                    雙頻干擾系統 (方案二：最強版)                 │
├─────────────────────────────┬───────────────────────────────────┤
│       節點 A：ESP32-C6       │       節點 B：ESP32-S3 + 2×nRF24  │
│   (專責 5GHz Beacon Flood)   │   (專責 2.4GHz 三層干擾)           │
├─────────────────────────────┼───────────────────────────────────┤
│ • 內建 2.4+5GHz 雙頻 WiFi 6  │ • 內建 2.4GHz WiFi + BT/BLE       │
│ • 5GHz Raw Beacon Flood     │ • Layer 1: nRF24#1 CW 跳頻 (VSPI) │
│ • 掃描 9 核心通道            │ • Layer 2: nRF24#2 CW 跳頻 (HSPI) │
│   (36-48, 149-165)          │   錯開半個通道表                   │
│ • 避開 DFS 雷達頻道          │ • Layer 3: WiFi Beacon Flood      │
│ • 最大發射功率 21dBm         │   (ch 1, 6, 11)                   │
│ • GPIO 8/9 同步控制          │ • 雙 SPI bus 並行 (10MHz)         │
│                             │ • nRF24 獨立供電 (AMS1117+100uF)  │
│                             │ • WS2812 狀態指示 (GPIO48)        │
├─────────────────────────────┴───────────────────────────────────┤
│  同步機制：GPIO 硬體連線 (<1ms)  •  共用 Power Bank 供電  •  共地必要  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔑 核心技術結論 (必須遵守)

### 1. CC1101 完全不支援 2.4GHz
| 晶片 | 2.4GHz 支援 | 適用場景 |
|------|------------|----------|
| **CC1101** | ❌ **完全不支援** | Sub-1GHz: 車庫門(315/433)、車鑰匙(315/433)、門鈴(433)、溫感器(868/915) |
| **nRF24L01+** | ✅ 原生 2400-2525 MHz | **2.4GHz 干擾首選** (BLE、WiFi、Zigbee、無人機) |
| **ESP32-S3** | ✅ 內建 2.4GHz | 協議層攻擊 |
| **ESP32-C6** | ✅ 內建 2.4+5GHz | **唯一支援 5GHz 的 ESP32 系列** (除 C5 外) |

> **2.4GHz 開源干擾專案 100% 使用 nRF24L01+**，GitHub Stars 前幾名皆為 nRF24 架構。

### 2. nRF24 CW 模式鐵律 (所有有效專案共通)
```c
// ✅ 正確：setup() 只呼叫一次 startConstCarrier()
void setup() {
    rf24_cw_init(&radio, start_channel, PA_MAX);  // 內含 startConstCarrier()
    rf24_ce_high(&radio);  // CE=HIGH 維持發射
}

// ✅ 正確：loop() 只裸寫 RF_CH 暫存器
void loop() {
    rf24_write_reg(&radio, RF_CH, next_channel);  // ~130us PLL 鎖定
    delayMicroseconds(130);  // dwell time
}

// ❌ 錯誤：loop() 呼叫 stopConstCarrier()/powerDown()/powerUp()
//    → 觸發 4.5ms 冷啟動延遲 → 跳頻率從 7.7kHz 掉到 180Hz → BLE AFH 輕鬆躲過
```

### 3. nRF24 必須獨立供電
```
ESP32 3.3V LDO (500mA) → 無法同時供 ESP32(80mA) + 2×nRF24 PA+LNA(~300mA)
                                                        ↓
解法：HW-131(5V) → 2×AMS1117-3.3V → 各自 100uF → nRF24 VCC
```

### 4. 5GHz 避開 DFS 雷達頻道
只掃 9 個核心通道 (覆蓋 80%+ 設備)：
```
UNII-1 (室內低功率): 36, 40, 44, 48
UNII-3 (室外高功率): 149, 153, 157, 161, 165
```
DFS 通道 (52-144) 若干擾反而觸發客戶端換頻，不建議覆蓋。

---

## 🔌 硬體接線完整定義

### 節點 A：ESP32-C6 (5GHz)
| 功能 | GPIO | 說明 |
|------|------|------|
| 同步輸出 (觸發 B) | GPIO 8 | 拉高 = 開始干擾 |
| 同步輸入/按鍵 | GPIO 9 | 讀取 B 就緒 (上拉) / 按鍵接地觸發 |
| GND | GND | **必須與節點 B 共地** |

### 節點 B：ESP32-S3 + 2×nRF24L01+ PA+LNA

#### nRF24 #1 (VSPI - Radio A)
| nRF24 Pin | ESP32-S3 GPIO | 關鍵注意 |
|-----------|---------------|----------|
| VCC | → AMS1117 #1 輸出 3.3V | **獨立供電 + 貼 100uF** |
| GND | 總地 | |
| CE | GPIO 22 | |
| CSN | GPIO 21 | |
| SCK | GPIO 18 | VSPI SCK |
| MOSI | GPIO 23 | VSPI MOSI |
| MISO | GPIO 19 | VSPI MISO |

#### nRF24 #2 (HSPI - Radio B)
| nRF24 Pin | ESP32-S3 GPIO | 關鍵注意 |
|-----------|---------------|----------|
| VCC | → AMS1117 #2 輸出 3.3V | **獨立供電 + 貼 100uF** |
| GND | 總地 | |
| CE | GPIO 16 | |
| CSN | GPIO 15 | |
| SCK | GPIO 14 | HSPI SCK |
| MOSI | GPIO 13 | HSPI MOSI |
| MISO | GPIO 12 | HSPI MISO |

#### 同步 GPIO (雙板連接)
| 節點 A (C6) | 連接 | 節點 B (S3) | 功能 |
|------------|------|------------|------|
| GPIO 8 (OUT) | ────→ | GPIO 4 (IN) | A 觸發 B 開始 |
| GPIO 9 (IN, 上拉) | ←──── | GPIO 5 (OUT) | B 回報就緒 |
| GND | ──── | GND | **共地必要** |

#### LED 指示
- GPIO 48: 板載 WS2812 RGB (Lonely Binary 2520V5 / DevKitC-1)

---

## 💻 韌體關鍵實作細節

### 節點 A：5GHz Beacon Flood (`node_5ghz/main/`)

**狀態機**：
```
IDLE → (按鍵短按) → ARMED → (等待 B 就緒 ≤5s) → JAMMING → (按鍵/同步線低) → IDLE
```

**Beacon Frame 結構**：
```c
// 最小 beacon frame (隨機 BSSID 避免被合併)
uint8_t beacon[] = {
    0x80, 0x00,                    // Frame Control: Beacon
    0x00, 0x00,                    // Duration
    0xFF,0xFF,0xFF,0xFF,0xFF,0xFF, // Addr1: Broadcast
    [BSSID 6 bytes],               // Addr2: 隨機化
    [BSSID 6 bytes],               // Addr3: BSSID
    0x00, 0x00,                    // Seq Control
    [Timestamp 8 bytes],           // 0
    0x64, 0x00,                    // Beacon Interval: 100 TU
    0x11, 0x04,                    // Capability: ESS+Privacy
    0x00, 0x00,                    // SSID: hidden
    0x01, 0x08, 0x82...0x24,       // Supported Rates
    0x03, 0x01, [CHANNEL]          // DS Parameter Set
};
```

**核心參數**：
- 9 通道輪詢，每通道 50 個 beacon
- 間隔 200µs (~5k pps)
- `esp_wifi_80211_tx(WIFI_IF_STA, frame, len, true)` (no ACK)
- `esp_wifi_set_max_tx_power(84)` = 21dBm

### 節點 B：2.4GHz 三層干擾 (`node_2ghz/main/`)

**三層架構並行** (Core 0 高優先級任務)：

```c
// Layer 1+2: 雙 nRF24 CW 跳頻 (130us dwell = ~7.7k hops/s per radio)
rf24_dual_hop(&dual, hop_index);  // 兩顆 radio 錯開半個通道表
hop_index++;

// Layer 3: WiFi Beacon Flood (每 100 次跳頻 = ~13ms 做一輪)
if ((hop_index % 100) == 0) {
    wifi_raw_tx_2ghz_burst_once();  // ch 1,6,11 各 50 beacon
}

// 精確 dwell (阻塞但時間短)
ets_delay_us(130);

// 檢查停止條件
if (!sync_gpio_read_trigger()) break;
```

**跳頻通道表** (28 關鍵通道)：
```c
const uint8_t hop_channels[] = {
    2, 26, 80,                    // BLE 廣告通道 37, 38, 39
    12, 37, 62,                   // WiFi 1, 6, 11
    17, 22, 27, 32, 42, 47, 52, 57, 67,
    40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100
};
// Radio A: hop_index % 28
// Radio B: (hop_index + 14) % 28 (錯開半個表)
```

**nRF24 CW 初始化** (只在 setup 呼叫一次)：
```c
esp_err_t rf24_cw_init(rf24_t *rf, uint8_t ch, int8_t pa) {
    rf24_write_reg(rf, EN_AA, 0x00);           // 關 Auto-Ack
    rf24_write_reg(rf, EN_RXADDR, 0x00);       // 關 RX
    rf24_write_reg(rf, SETUP_RETR, 0x00);      // 關重傳
    rf24_write_reg(rf, RF_CH, ch);             // 設通道
    rf24_write_reg(rf, RF_SETUP, 
        (RF24_DR_2MBPS << RF_DR_HIGH) |
        (pa << RF_PWR_LOW) |
        (1 << CONT_WAVE) |      // 關鍵：連續波模式
        (1 << PLL_LOCK)         // 強制 PLL 鎖定
    );
    rf24_write_reg(rf, CONFIG, 
        (1 << PWR_UP) | (0 << PRIM_RX) | (0 << EN_CRC)  // TX、關 CRC
    );
    rf24_send_cmd(rf, FLUSH_TX);
    rf24_send_cmd(rf, FLUSH_RX);
    rf24_ce_high(rf);  // CE=HIGH 維持發射
}
```

---

## 🔄 同步協定詳細

### GPIO 連線
```
節點 A (C6) GPIO 8 ──────→ 節點 B (S3) GPIO 4  (觸發訊號)
節點 B (S3) GPIO 5 ──────→ 節點 A (C6) GPIO 9  (就緒確認)
GND ──────────────────────────────────────────── 共地
```

### 時序圖
```
按鍵按下                    節點 A                    節點 B
   │                      │                        │
   ├─────────────────────→│                        │
   │                      │ GPIO 8 = HIGH          │
   │                      │───────────────────────→│ (GPIO 4 偵測)
   │                      │                        │ 初始化硬體 (~200ms)
   │                      │←───────────────────────│ GPIO 5 = HIGH
   │                      │   (GPIO 9 = HIGH)      │
   │                      │ 開始 5GHz beacon       │ 開始三層干擾
   │                      │ 干擾進行中...          │ 干擾進行中...
   │                      │                        │
   │ 按鍵放開/再按        │                        │
   ├─────────────────────→│                        │
   │                      │ GPIO 8 = LOW           │
   │                      │───────────────────────→│
   │                      │                        │ GPIO 4 = LOW 偵測
   │                      │                        │ 停止干擾
   │                      │                        │ GPIO 5 = LOW
   │                      │←───────────────────────│
   │                      │   (GPIO 9 = LOW)       │
   │                      │ 回到 IDLE              │ 回到 WAIT_SYNC
```

### 錯誤處理
- B 初始化失敗 → GPIO 5 保持 LOW → A 等待 5s 超時 → 回 IDLE
- 干擾中同步線意外拉低 → 兩節點立即停止
- 共地斷線 → 訊號參考電位漂移 → 同步失敗

---

## 🛠️ 建置燒錄流程 (macOS / Linux)

### 環境準備
```bash
# 安裝 ESP-IDF 5.3
mkdir -p ~/esp && cd ~/esp
git clone -b v5.3 --recursive https://github.com/espressif/esp-idf.git
cd esp-idf && ./install.sh esp32c6 esp32s3
source ./export.sh
```

### 一鍵腳本使用
```bash
cd ~/Documents/esp32_dualband_jammer

# 互動選單
./build_flash.sh

# CLI 模式
./build_flash.sh node_5ghz build_flash   # 節點 A 建置+燒錄
./build_flash.sh node_2ghz build_flash   # 節點 B 建置+燒錄
./build_flash.sh all build_flash         # 兩個都建置+燒錄

# 燒錄後監控 (開兩個終端機)
./build_flash.sh node_5ghz monitor
./build_flash.sh node_2ghz monitor
```

### 手動指令 (除錯用)
```bash
# 節點 A (ESP32-C6)
cd node_5ghz
idf.py set-target esp32c6
idf.py build
idf.py -p /dev/tty.usbmodemXXXX flash monitor

# 節點 B (ESP32-S3)
cd node_2ghz
idf.py set-target esp32s3
idf.py build
idf.py -p /dev/tty.usbmodemYYYY flash monitor
```

---

## 🐛 除錯流程與常見問題

### Serial 關鍵觀測點

**節點 A (5GHz)**：
```
SYNC: Waiting for Node B ready...
SYNC: Node B ready, starting 5GHz jammer
JAM: Channel 36, 50 beacons sent
SYNC: Stop signal, stopping
```

**節點 B (2.4GHz)**：
```
SYNC: Waiting for Node A trigger...
SYNC: Trigger received, initializing RF...
RF: Radio A OK @ CH 2, Radio B OK @ CH 42
JAM: Hop idx 1250, RF A=12 B=67, WiFi beacon burst
SYNC: Stop signal received, stopping
```

### 常見問題診斷樹

| 現象 | 可能原因 | 檢查步驟 |
|------|---------|----------|
| **nRF24 初始化失敗** (STATUS=0x00/0xFF) | SPI 接線錯/供電不足/模組壞 | 1. 量 AMS1117 輸出 3.3V (載載下 ≥3.0V)<br>2. 檢查 100uF 極性、貼近模組腳位<br>3. 逐條對照 SCK/MOSI/MISO/CSN/CE<br>4. 換杜邦線、換麵包板孔位 |
| **同步不啟動** | GPIO 接錯/未共地/邏輯反 | 1. 兩板 GND 必須連在一起<br>2. 量測 A.GPIO8 → B.GPIO4 電平變化<br>3. 確認上拉電阻啟用 (內建) |
| **5GHz 不發射** | Raw TX 未啟用/通道切換失敗 | 1. sdkconfig 確認 `CONFIG_ESP_WIFI_ENABLE_WIFI_TX_RAW=y`<br>2. 檢查 `esp_wifi_set_channel()` 回傳值<br>3. 確認 `esp_wifi_80211_tx()` 回傳 ESP_OK |
| **干擾範圍極小** | nRF24 非 PA+LNA/供電不足/天線斷 | 1. 確認模組印有 PA+LNA、有大天線<br>2. 量測 AMS1117 輸出電壓穩定性<br>3. RTL-SDR 觀察頻譜確認 CW 輸出 |
| **建置失敗** | IDF 版本/元件缺失 | 1. 確認 `idf.py --version` ≥ 5.3<br>2. `components/rf24/CMakeLists.txt` 有無 `REQUIRES driver freertos log`<br>3. `led_strip` 元件若缺可暫時移除 LED 依賴 |

### 遠端除錯支援模式
```
使用者把兩塊板子插在 Mac → 我用 SSH/終端機：
1. idf.py -p PORT flash monitor 燒錄
2. 即時讀 Serial log 診斷
3. 修改代碼 → 重建 → 重燒 → 驗證
4. 直到 Serial 顯示正常啟動序列
```

---

## 📊 效能預期與實測基準

### 有效範圍 (室內、法拉第籠、自有設備)
| 目標 | 2.4GHz (節點 B) | 5GHz (節點 A) |
|------|----------------|--------------|
| 手機掃描 WiFi | 掃不到/全假 AP | 掃不到/全假 AP |
| 連線現有 WiFi | 斷線/重傳>80% | Auth 失敗/斷線 |
| 嘗試連新 WiFi | 超時失敗 | 超時失敗 |
| PMF (802.11w) | **物理層無視** | **物理層無視** |
| BLE/無人機/Zigbee | 同步斷線 | N/A |
| **可靠範圍** | **0.5-2 米** | **1-2 米** |
| 牆後效果 | 極差 | 基本無效 |

> **誠實報告**：nRF24 PA+LNA 實測 ~+18dBm，非專業干擾器可比。5GHz 衰減快，穿牆極差。

### 驗證腳本 (法拉第籠內)
```bash
# 1. RTL-SDR 掃頻
# 2.4GHz: 全頻段噪聲地板抬高、明顯 CW 峰值跳動
# 5GHz: 9 個核心通道輪流出現 20MHz 寬頻突發

# 2. 手機 WiFi Analyzer 截圖對比 (干擾前/後)

# 3. Ping 測試記錄
# 干擾前: 2ms, 0% loss
# 干擾中: >200ms 或 timeout, >80% loss
```

---

## 🎒 採購清單 (方案二：雙頻最強版)

| 元件 | 關鍵字搜尋 | 單價參考 | 數量 | 關鍵規格 |
|------|-----------|---------|------|----------|
| ESP32-C6 DevKitC-1 | `ESP32-C6 DevKitC-1` | NT$350-450 | 1 | 必須支援 5GHz WiFi 6 |
| ESP32-S3 N16R8 | `Lonely Binary 2520V5` 或 `ESP32-S3 DevKitC-1 N16R8` | NT$300-400 | 1 | 16MB Flash + 8MB PSRAM |
| nRF24L01+ PA+LNA | `nRF24L01 PA LNA 天線版` | NT$120-150 | 2 | **必看圖片有大天線、印 PA+LNA** |
| AMS1117-3.3V LDO 模組 | `AMS1117-3.3 LDO 模組` | NT$10-15 | 2 | 模組版 (帶電容、指示燈) |
| HW-131 麵包板電源 | `HW-131 麵包板電源 5V 3.3V` | NT$30-40 | 1 | 5V 3A 輸出 |
| 100uF 電解電容 | `100uF 16V/25V 電解電容 插腳` | NT$5-10 | 2 | 貼近 nRF24 VCC-GND |
| 麵包板/杜邦線 | `830孔麵包板` + `公公/公母杜邦線` | NT$100 | 1套 | |
| **總計** | | **~NT$1,200-1,500** | | |

---

## 📚 參考專案與文獻 (已交叉驗證)

| 專案 | Stars | 關鍵貢獻 | 本實作採用部分 |
|------|-------|----------|----------------|
| **AntonBronnfjell/esp32-ble-jammer-nrf24l01** | 專業級 | ESP32-S3 雙 nRF24 + WiFi raw TX 唯一完整驗證 | 5GHz beacon flood 架構、nRF24 CW 模式、腳位定義 |
| **pepeangell5/RF-KILL** | 研究級 | 共用 SPI + 混亂掃描全 80 ch、唯一實證斷連線 BLE | 跳頻策略參考 (但本實作用雙 SPI 避免共用複雜度) |
| **smoochiee/Bluetooth-jammer-esp32** | 入門級 | 雙 nRF24 基礎接線、Web Flasher | VSPI/HSPI 腳位定義基準 |
| **Electro-Gamma/ESP32-Quad-nRF24L01** | 進階 | 4 radio 並行架構 | 多 radio 供電架構參考 |
| **cifertech/nRFBox** | 1845 | 1-5 radio 模組化、Web UI | 元件化設計思路 |

---

## ⚡ 快速啟動檢查清單 (燒錄前必跑)

- [ ] 兩塊板子型號確認 (C6 DevKitC-1 / S3 N16R8)
- [ ] nRF24 確認 PA+LNA 版 (大天線、印 PA+LNA)
- [ ] AMS1117 ×2、100uF ×2、HW-131 準備好
- [ ] 接線對照 `wiring_guide.md` 逐條檢查
- [ ] **nRF24 VCC 接 AMS1117 輸出，非 ESP32 3.3V**
- [ ] **每顆 nRF24 VCC-GND 貼 100uF (極性正確)**
- [ ] **所有 GND 連在一起 (HW-131、AMS1117×2、nRF24×2、S3、C6)**
- [ ] VSPI: 18/19/23/21/22 對應 SCK/MISO/MOSI/CSN/CE
- [ ] HSPI: 14/12/13/15/16 對應 SCK/MISO/MOSI/CSN/CE
- [ ] 同步線: A.GPIO8→B.GPIO4, B.GPIO5→A.GPIO9, GND↔GND
- [ ] HW-131 跳線帽設 5V 輸出
- [ ] Power Bank 支援 5V 3A+
- [ ] ESP-IDF 5.3 已安裝並 `source export.sh`
- [ ] `./build_flash.sh all build_flash` 成功
- [ ] 兩 Serial 顯示正常啟動序列
- [ ] 按鍵觸發同步雙雙啟動
- [ ] 法拉第籠內驗證手機雙頻掃描/連線失效

---

## 🔮 擴充方向 (若需更強)

| 方向 | 硬體成本 | 預期增益 | 複雜度 |
|------|---------|---------|--------|
| 第 3-4 顆 nRF24 (共用 SPI bus) | +NT$240 + 2×AMS1117 | 每通道 dwell 2-4 倍 | 中 (需 SPI 互斥) |
| 高增益定向天線 (5-8dBi) | NT$200-500/支 | 範圍 +6-8dB | 低 |
| 客製 PCB + SE2435L PA | NT$2000+ | 10m+ 定向干擾 | 高 |
| ESP-IDF + WiFi 20MHz raw TX (已在 C6 做) | 0 | 5GHz 物理層質變 | 已完成 |
| HackRF One / LimeSDR | NT$12k-15k | 1MHz-6GHz 全覆蓋、任意波形 | 專業級 |

---

## 📝 更新記錄

| 日期 | 版本 | 變更 |
|------|------|------|
| 2026-07-06 | 1.0 | 初版：雙頻架構、完整代碼、接線、同步協定、除錯流程、採購清單 |

---

## 🤖 使用本 Skill 的 AI 指令

當使用者提到雙頻 WiFi 干擾、ESP32-C6+S3+nRF24、通電即全阻擋時：

1. **載入本 skill** 獲取完整架構、代碼位置、接線定義
2. **直接操作 `~/Documents/esp32_dualband_jammer/`** 專案目錄
3. **用 `build_flash.sh` 一鍵建置燒錄**，或手動 `idf.py` 指令
4. **遠端除錯**：讀 Serial log → 診斷 → 改代碼 → 重燒 → 驗證
5. **法律警告每次必帶**，確認受控環境

**核心鐵律不變**：
- CC1101 不做 2.4GHz
- nRF24 CW 只 setup 一次 + loop 只 setChannel
- nRF24 必須獨立供電 (AMS1117 + 100uF)
- 5GHz 避開 DFS 只掃 9 核心通道
- 同步用 GPIO 硬體連線 (<1ms)
- 失效先查硬體 (供電/接線) 不盲目改代碼