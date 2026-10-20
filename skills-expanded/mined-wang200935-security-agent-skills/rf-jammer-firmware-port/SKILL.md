---
name: rf-jammer-firmware-port
description: RF Jammer v2 完整移植技術手冊 — 從 RF Jammer 3×nRF24 原始碼深度分析、 sigkill 交叉比較、到 Wang
  現有雙 nRF24 硬體的移植方案。包含完整硬體腳位對照、firmware 逐行架構分析、UI 動畫系統、頻道協議映射、編譯燒錄 SOP、以及所有已踩過的 Pitfall。當
  user 要製作 OLED 選單多協議干擾器、或移植 RF Jammer/ 到 Wang 硬體時載入。
version: 1.0.0
license: MIT
metadata:
  hermes_origin: import
tags:
- RF Jammer
- esp32
- nrf24
- jammer
- multi-protocol
- oled
- 移植
related_skills: []
---

# RF Jammer v2 完整移植技術手冊

## 🎯 觸發時機

- user 提到「RF Jammer」「」「多協議干擾器」「OLED 選單 jammer」
- user 要移植 RF Jammer 到 Wang 現有硬體（雙 nRF24 + OLED + 按鈕）
- user 問 RF Jammer 內部架構、UI 動畫、頻道定義、nRF24 初始化策略

---

## 📊 RF Jammer v2 vs  深度對比

| 特徵 | RF Jammer v2 |  |
|------|-----------|---------|
| GitHub | cifertech/RF Jammer ★1,721 | jbohack/ ★547 |
| 框架 | Arduino IDE (.ino) | PlatformIO (src/include) |
| nRF24 數量 | **3** (GT24 Mini) | **3** |
| 按鈕 | **3** (L=27,R=25,S=26) | **5** (UP=26,DOWN=33,CENTER=32,LEFT=25,RIGHT=27) |
| OLED | SSD1306 128×64 I²C (SCL=22,SDA=21) | SSD1306 128×64 I²C |
| 狀態 LED | NeoPixel GPIO14 | NeoPixel GPIO14 |
| 協議數量 | **8** (WiFi/VideoTX/RC/BLE/BT/USB/Zigbee/NRF24) | **9** (+All mode) |
| 按鈕處理 | HW interrupt FALLING + 200ms millis debounce | digitalRead polling + 200ms millis debounce |
| UI 風格 | **動畫卡片滑動 + Pill Toggle** | 文字選單 + 捲軸 |
| 模式切換 | L/R 按鈕切模式 + S 按鈕 ON/OFF toggle | UP/DOWN 切選項 + RIGHT 啟動 + LEFT 返回 |
| ESP32 core | **1.0.5** (Arduino IDE 舊版) | 未知 (PlatformIO) |
| nRF24 SPI | **3 顆共用 default SPI** (只用 VSPI 硬體腳) | 3 顆獨立 SPI? (pindefs 只列 CE/CSN) |
| 開源程度 | **完整** (.ino + config.h + setting.cpp/h + neopixel.cpp) | **legacy-src 完整** (PlatformIO) |
| PCB | **已釋出** Gerber+BOM+Pick&Place+示意圖 | 商業產品，無 PCB |

---

## 🔌 RF Jammer v2 完整腳位定義 (config.h)

```cpp
// 按鈕
#define PIN_BTN_L  27  // 左鍵 = 上一個模式
#define PIN_BTN_R  25  // 右鍵 = 下一個模式
#define PIN_BTN_S  26  // 中鍵 = ON/OFF toggle

// nRF24 (3 顆共用 default SPI = VSPI 硬體腳)
#define NRF_CE_PIN_A    5
#define NRF_CSN_PIN_A   17
#define NRF_CE_PIN_B    16
#define NRF_CSN_PIN_B   4
#define NRF_CE_PIN_C    15
#define NRF_CSN_PIN_C   2
// SCK=18, MOSI=23, MISO=19 (default VSPI pins)

// NeoPixel
// pixels(1, 14, NEO_GRB + NEO_KHZ800) — 1 顆 LED @ GPIO14

// OLED
// U8G2_SSD1306_128X64_NONAME_F_HW_I2C — SCL=22, SDA=21, 400kHz
```

---

## 🏗 RF Jammer 完整 firmware 架構逐行分析

### 檔案結構

```
rf-jammer/
├── rf-jammer.ino     ← 主程式 (407 行)
├── config.h        ← 所有 define + include + 頻道陣列 (98 行)
├── setting.h       ← 函式宣告 + extern + OLED 字型 (55 行)
├── setting.cpp     ← nRF24 init + OLED 文字 + 開機畫面 (51 行)
└── neopixel.cpp    ← NeoPixel 顏色設定 + 閃爍 (54 行)
```

### config.h 核心定義

```cpp
// --- 枚舉 ---
enum OperationMode {
  WiFi_MODULE,         // 0
  VIDEO_TX_MODULE,     // 1
  RC_MODULE,           // 2
  BLE_MODULE,          // 3
  Bluetooth_MODULE,    // 4
  USB_WIRELESS_MODULE, // 5
  ZIGBEE_MODULE,       // 6
  NRF24_MODULE         // 7
};

enum Operation {
  DEACTIVE_MODE,       // 0 = 待機
  ACTIVE_MODE          // 1 = 干擾中
};

// --- 頻道群組 (三 radio 各鎖一群) ---
byte channelGroup_1[] = {2, 5, 8, 11};
byte channelGroup_2[] = {26, 29, 32, 35};
byte channelGroup_3[] = {80, 83, 86, 89};

// --- 各協議頻道陣列 ---
const byte bluetooth_channels[] =        {32,34,46,48,50,52, 0,1,2,4,6,8, 22,24,26,28,30, 74,76,78,80};  // 21 個
const byte ble_channels[]       =        {2, 26, 80};                                                      // 3 個 (廣告通道)
const byte WiFi_channels[]      =        {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12};                         // 12 個
const byte usbWireless_channels[] =      {40, 50, 60};                                                      // 3 個
const byte videoTransmitter_channels[] = {70, 75, 80};                                                      // 3 個
const byte rc_channels[]        =        {1, 3, 5, 7};                                                      // 4 個
const byte zigbee_channels[]    =        {11, 15, 20, 25};                                                  // 4 個
const byte nrf24_channels[]     =        {76, 78, 79};                                                      // 3 個
```

### nRF24 初始化流程 (setting.cpp)

```cpp
// 全域 radio 物件
RF24 RadioA(NRF_CE_PIN_A, NRF_CSN_PIN_A);  // CE=5, CSN=17
RF24 RadioB(NRF_CE_PIN_B, NRF_CSN_PIN_B);  // CE=16, CSN=4
RF24 RadioC(NRF_CE_PIN_C, NRF_CSN_PIN_C);  // CE=15, CSN=2

// 中性狀態 (DEACTIVE_MODE 時呼叫)
void setRadiosNeutralState() {
  RadioA.stopListening(); RadioA.setAutoAck(false);
  RadioA.setRetries(0, 0); RadioA.powerDown(); digitalWrite(NRF_CE_PIN_A, LOW);
  // RadioB, RadioC 同上
}

// 通用設定 (所有 radio 共用)
void configureNrf(RF24 &radio) {
  radio.begin();                             // default SPI
  radio.setAutoAck(false);
  radio.stopListening();                     // TX mode
  radio.setRetries(0, 0);
  radio.setPALevel(RF24_PA_MAX, true);       // +20dBm (PA+LNA)
  radio.setDataRate(RF24_2MBPS);
  radio.setCRCLength(RF24_CRC_DISABLED);     // 純 CW 不需 CRC
}
```

### 干擾核心 — configure_Radio() + loop()

```cpp
// 每個 radio 對其 channelGroup 逐一 startConstCarrier
// ⚠ 最後一個 channel 的 startConstCarrier 覆蓋前面的
void configure_Radio(RF24 &radio, const byte *channels, size_t size) {
  configureNrf(radio);
  radio.printPrettyDetails();  // debug
  for (size_t i = 0; i < size; i++) {
    radio.setChannel(channels[i]);
    radio.startConstCarrier(RF24_PA_MAX, channels[i]);  // 每個都叫，最後保留
  }
}

// ACTIVE_MODE: 三 radio 各自 configure_Radio(channelGroup_N)
// DEACTIVE_MODE: 三 radio powerDown() + delay(100)
void initialize_Radios() {
  if (current == ACTIVE_MODE) {
    if (RadioA.begin()) configure_Radio(RadioA, channelGroup_1, sizeof(channelGroup_1));
    if (RadioB.begin()) configure_Radio(RadioB, channelGroup_2, sizeof(channelGroup_2));
    if (RadioC.begin()) configure_Radio(RadioC, channelGroup_3, sizeof(channelGroup_3));
  } else {
    RadioA.powerDown(); RadioB.powerDown(); RadioC.powerDown(); delay(100);
  }
}
```

### loop() — 只做 setChannel() 裸調

```cpp
void loop() {
  checkMode();  // 處理 interrupt flag

  // 偵測模式變化 → 播放動畫
  static Operation     lastActivity = current;
  static OperationMode lastFocus    = current_Mode;
  if (current_Mode != lastFocus) {
    animateToMenu(menuIndexFromMode(lastFocus), menuIndexFromMode(current_Mode));
    lastFocus = current_Mode; return;
  }
  if (current != lastActivity) {
    initialize_Radios();
    animateToggleKnobForFocus(focus, wasActive, nowActive);
    lastActivity = current; return;
  }

  // 干擾中：依目前模式隨機挑頻道 → 三 radio 同步 setChannel(random)
  if (current_Mode == BLE_MODULE) {
    byte channel = ble_channels[random(3)];
    RadioA.setChannel(channel);
    RadioB.setChannel(channel);
    RadioC.setChannel(channel);
  }
  // ... 其他 7 種模式同理，各有自己的頻道陣列
}
```

### 🔥 關鍵設計模式

1. **startConstCarrier 只在 initialize_Radios() 裡叫**，loop() 內絕不重新叫
2. **三 radio 在同一模式內同步跳到同一個頻道**（功率疊加，而非分散）
3. **從不呼叫 stopConstCarrier() / powerDown() / powerUp() 在 loop 內**
4. **模式切換時先 powerDown() 全部 radio，再重新 init**
5. **頻道群組設計**: radioA 鎖低頻 (2-11), radioB 鎖中頻 (26-35), radioC 鎖高頻 (80-89)

---

## 🎨 UI 動畫系統完整架構

### 佈局

```
┌──────────────────────────┐ y=0
│ ████████ RF Jammer v2.0.0 │ HEADER_H=12 (黑底白字)
├──────────────────────────┤ y=12
│                          │
│  ┌──────────────────┐    │ y=16 (HEADER_H + 4)
│  │ WiFi         ⬤━⬤ │    │ CARD_H=36 (RFrame + Pill Toggle)
│  │ DEACTIVE          │    │
│  └──────────────────┘    │ y=52
│                          │
│  ● ○ ○ ○ ○ ○ ○ ○        │ y=58 (DOT_Y=64-6, PaginationDots)
└──────────────────────────┘ y=64
```

### 動畫函式

| 函式 | 用途 | 步數 | 時間 | 緩動 |
|------|------|------|------|------|
| `animateToMenu(from, to)` | 卡片左/右滑動切換 | 14 steps × 10ms = 140ms | CubicEaseInOut |
| `animateToggleKnobForFocus(focus, wasActive, nowActive)` | Pill 開關切換動畫 | 10 steps × 12ms = 120ms | QuadraticEaseInOut |
| `renderStaticMenu(focus)` | 直接渲染 (無動畫) | — | — | — |
| `spectrum()` | 背景頻譜視覺化 | — | — | 隨機柱狀+慣性衰減 |

### 動畫數學

```cpp
// CubicEaseInOut (卡片滑動)
float t = (float)s / (float)STEPS;
float e = (t < 0.5f) ? 4.0f*t*t*t : 1.0f - powf(-2.0f*t + 2.0f, 3)/2.0f;

// QuadraticEaseInOut (Pill knob)
float t = (float)s / (float)STEPS;
float e = (t < 0.5f) ? 2.0f*t*t : 1.0f - powf(-2.0f*t + 2.0f, 2)/2.0f;
```

### Pill Toggle 幾何

```cpp
// Pill = 圓角矩形 + 圓形 knob
// drawPillOutline: drawRFrame(x, y, w, h, h/2) — 半徑 = 半高
// drawPillKnob: drawDisc(cx, cy, max(2, r-3)) — knob 半徑比 pill 小 3px
// pos: 0.0f = 左 (ON), 1.0f = 右 (OFF)
int cxL = x + r;            // knob 左極限位置
int cxR = x + w - r - 1;    // knob 右極限位置
int cx  = cxL + (cxR - cxL) * pos;  // 插值
```

---

## 🔄 移植到 Wang 硬體 (雙 nRF24 + 6 鍵 + 4pin LED)

### Wang 現有硬體 vs RF Jammer 差異

| 項目 | RF Jammer | Wang 現有 | 移植動作 |
|------|----------|----------|---------|
| nRF24 數量 | 3 顆 | **2 顆** | 砍掉 RadioC、channelGroup_3 |
| nRF24 CE/CSN | {5,17, 16,4, 15,2} | **VSPI {22,21} / HSPI {16,15}** | 改 config.h 腳位 |
| SPI bus | 3 顆共用 default SPI (VSPI) | **VSPI+HSPI 獨立** (Wang 現有接法) | RadioA 用 VSPI, RadioB 用 HSPI |
| OLED | SSD1306 128×64 I²C (22/21) | **SSD1306 128×64 I²C (21/22)** | 腳位一致 ✅ |
| 按鈕 | 3 鍵 {27,25,26} | **6 鍵** | 映射: L=34, R=35, S=36 (或上/下/左/右/中/退) |
| 狀態 LED | NeoPixel GPIO14 | **4pin LED 螢幕模組** | 砍掉 NeoPixel，直接 GPIO 控制 LED |

### 移植步驟

1. **修改 config.h**：
```cpp
// nRF24 GPIO → Wang 硬體
#define NRF_CE_PIN_A    22   // VSPI
#define NRF_CSN_PIN_A   21
#define NRF_CE_PIN_B    16   // HSPI
#define NRF_CSN_PIN_B   15

// 按鈕 GPIO → Wang 硬體
#define PIN_BTN_L  34   // 上/左
#define PIN_BTN_R  35   // 下/右
#define PIN_BTN_S  36   // 確認/啟動

// 砍掉 RadioC 相關
// 砍掉 channelGroup_3
// 頻道群組改為雙 radio 分工:
byte channelGroup_1[] = {2, 5, 8, 11, 26, 29, 32, 35};  // radioA 鎖低+中頻
byte channelGroup_2[] = {80, 83, 86, 89};                  // radioB 鎖高頻
```

2. **移植 nRF24 初始化**：RF24 建構子用 VSPI/HSPI 獨立 SPI bus
```cpp
#include <SPI.h>
SPIClass *vspi_bus = nullptr;
SPIClass *hspi_bus = nullptr;

void configure_Radio(RF24 &radio, SPIClass *bus, const byte *channels, size_t size) {
  radio.begin(bus);  // 傳入 SPI bus pointer
  radio.setAutoAck(false);
  // ... 其他設定同上
  for (size_t i = 0; i < size; i++) {
    radio.setChannel(channels[i]);
    radio.startConstCarrier(RF24_PA_MAX, channels[i]);
  }
}

void initialize_Radios() {
  if (current == ACTIVE_MODE) {
    vspi_bus = new SPIClass(VSPI);
    vspi_bus->begin(18, 19, 23, -1);  // SCK=18, MISO=19, MOSI=23
    hspi_bus = new SPIClass(HSPI);
    hspi_bus->begin(14, 12, 13, -1);  // SCK=14, MISO=12, MOSI=13

    if (RadioA.begin(vspi_bus))
      configure_Radio(RadioA, vspi_bus, channelGroup_1, sizeof(channelGroup_1));
    if (RadioB.begin(hspi_bus))
      configure_Radio(RadioB, hspi_bus, channelGroup_2, sizeof(channelGroup_2));
  } else {
    RadioA.powerDown(); RadioB.powerDown(); delay(100);
    if (vspi_bus) { vspi_bus->end(); delete vspi_bus; vspi_bus = nullptr; }
    if (hspi_bus) { hspi_bus->end(); delete hspi_bus; hspi_bus = nullptr; }
  }
}
```

3. **砍掉 NeoPixel** — 改用 4pin LED：
```cpp
#define LED_PIN 2  // ESP32 內建 LED 或自訂 GPIO
// 代替 setNeoPixelColour():
void setStatusLED(bool on) {
  digitalWrite(LED_PIN, on ? HIGH : LOW);
}
```

4. **UI 保留** — OLED 128×64 U8g2 完整保留，只改 kMenuLabels (砍掉 NRF24_MODULE? 或保留 8 種全上)

---

## ⚠️ 移植 Pitfall 清單

### P1: ESP32 core 版本差異 (1.0.5 → 3.3.10)

RF Jammer 用 ESP32 core **1.0.5**。Wang 環境用 **3.3.10**。

| API | core 1.0.5 | core 3.3.10 |
|-----|-----------|-------------|
| `esp_bt_controller_deinit()` | ✅ | ✅ (仍可用) |
| `esp_wifi_stop/deinit/disconnect()` | ✅ | ✅ |
| `ieee80211_raw_frame_sanity_check` | 弱符號 | **強符號 → linker 會要求 `__wrap_`** |
| `WiFi.scanNetworks()` | 正常 | 正常 |

**解法**: 任何 ESP32 core 3.3.10 的 .ino 都要加：
```cpp
extern "C" int __wrap_ieee80211_raw_frame_sanity_check(int32_t arg, int32_t arg2, int32_t arg3) {
  return 1;
}
```
(即使完全不碰 WiFi raw TX，linker 也強制要求)

### P2: RF24 ≥1.6 startConstCarrier 回 void

RF Jammer 寫的時候可能是 RF24 1.4.x（`startConstCarrier` 回 `bool`）。
Wang 環境是 RF24 1.6.1（回 `void`）。

**移植時不需要改** — RF Jammer 原始碼的 `configure_Radio()` 沒有檢查回傳值（直接 `radio.startConstCarrier(...)`），所以相容 ✅。但如果自己加的 code 有 `if (!radio.startConstCarrier(...))` 就會編譯失敗。

### P3: ESP32-D0WD-V3 需要 FlashMode=dio

Wang 的 ESP32 是 D0WD-V3 rev3.0，不支援 QIO flash。編譯時必須加：
```bash
arduino-cli compile --fqbn esp32:esp32:esp32:FlashMode=dio <sketch_dir>
```

### P4: Arduino sketch 目錄必須等於 .ino 檔名

`rf-jammer_multi.ino` 必須在 `rf-jammer_multi/rf-jammer_multi.ino`

### P5: 分次燒錄 @230400 baud 最可靠

```bash
# Step 1: bootloader (保持 stub)
esptool.py --chip esp32 --port $PORT --baud 230400 --before default-reset --after no-reset \
  write-flash 0x1000 <sketch>.ino.bootloader.bin

# Step 2: partitions + app (從 stub 繼續，最後 hard-reset)
esptool.py --chip esp32 --port $PORT --baud 230400 --before default-reset --after hard-reset \
  write-flash 0x8000 <sketch>.ino.partitions.bin 0x10000 <sketch>.ino.bin
```

### P6: INPUT_PULLUP vs 外部上拉電阻

RF Jammer 用 `pinMode(PIN_BTN_L, INPUT_PULLUP)` — ESP32 內建上拉，不用外部電阻。
移植時直接用 INPUT_PULLUP（省零件）。**但 GPIO 34/35/36/39 是 input-only，沒有內部 pull-up** — 如果按鈕接這些腳，必須外加 10kΩ 上拉電阻到 3.3V。

### P7: SPI 三線 (SCK/MOSI/MISO) 接錯 = 最常見 ERR

nRF24 `begin()` 失敗 90% 是 SPI 線接錯。遠端診斷時叫 user 逐條唸出接線對照檢查。

### P8: 每顆 nRF24 VCC-GND 必並 10µF 電容

不加電容 → nRF24 在 CW 模式隨機 reset 或 power drop → `begin()` 成功但干擾時有時無。

### P9: 三 radio 共用 SPI vs 獨立 SPI

RF Jammer 用 3 顆 nRF24 共用 default SPI（VSPI 硬體腳）。Wang 硬體目前用 **VSPI+HSPI 獨立**。
移植時兩種做法都可以：
- **A) 保持獨立** (不改線)：`RadioA.begin(vspi_bus)` + `RadioB.begin(hspi_bus)`
- **B) 共用 VSPI** (改線，像 RF-KILL)：把 nRF24 #2 的 SCK/MOSI/MISO 改接到 VSPI GPIO (18/23/19)

推薦 **A** (不改線，直接移植) — Wang 硬體已經有穩定的獨立 SPI 接法。

### P10: 兩顆 nRF24 vs 三顆 nRF24 頻道策略

RF Jammer 用三顆 radio 各有固定頻道群組。移植到兩顆時：
- **方案 A**：radioA 鎖廣告通道 (2/26/80)，radioB 做 RF-KILL 混亂掃描 (全 0-79)
- **方案 B**：雙 radio 同步隨機跳頻，像  sigkill 做法（每模式各有頻道陣列）
- **方案 C**：照 RF Jammer 原設計，砍掉 RadioC，RadioA/B 各自鎖一半頻道群組

推薦 **方案 B** ( 風格) — 最簡單、最符合 user 描述的多協議選單行為。

---

## 🔧 編譯燒錄 SOP (macOS, 2026-07)

### 環境確認

```bash
arduino-cli version      # ≥1.5.1
arduino-cli core list    # esp32:esp32 3.3.10
arduino-cli lib list     # RF24 ≥1.6.1, U8g2
```

### 編譯

```bash
arduino-cli compile \
  --fqbn esp32:esp32:esp32:FlashMode=dio \
  --build-path bin/build \
  --output-dir bin \
  rf-jammer_multi/rf-jammer_multi.ino
```

### 燒錄

```bash
ESPPORT=$(ls /dev/cu.usbserial-* | head -1)

# bootloader
~/.hermes/hermes-agent/venv/bin/python3 -m esptool \
  --chip esp32 --port $ESPPORT --baud 230400 \
  --before default-reset --after no-reset \
  write-flash 0x1000 bin/rf-jammer_multi.ino.bootloader.bin

# partitions + app
~/.hermes/hermes-agent/venv/bin/python3 -m esptool \
  --chip esp32 --port $ESPPORT --baud 230400 \
  --before default-reset --after hard-reset \
  write-flash 0x8000 bin/rf-jammer_multi.ino.partitions.bin \
  0x10000 bin/rf-jammer_multi.ino.bin
```

### Serial 驗證

```bash
python3 -c "
import serial, time
s = serial.Serial('$ESPPORT', 115200, timeout=1)
deadline = time.time() + 10
while time.time() < deadline:
    data = s.read(1024)
    if data: print(data.decode('utf-8', errors='replace'), end='', flush=True)
    else: time.sleep(0.1)
s.close()
"
```

---

## 📡 各協議 nRF24 channel 對照總表

| 協議 | 頻道陣列 | 數量 | nRF24 channel → 實際頻率 |
|------|---------|------|-------------------------|
| BLE 廣告通道 | {2, 26, 80} | 3 | 2402MHz / 2426MHz / 2480MHz |
| Bluetooth Classic | {32,34,46,48,50,52, 0,1,2,4,6,8, 22,24,26,28,30, 74,76,78,80} | 21 | 分散 2400-2480MHz |
| WiFi 2.4GHz | {1..12} | 12 | 2412-2484MHz |
| Video TX (FPV) | {70, 75, 80} | 3 | 2470/2475/2480MHz |
| RC (遙控器) | {1, 3, 5, 7} | 4 | 2401/2403/2405/2407MHz |
| USB Wireless | {40, 50, 60} | 3 | 2440/2450/2460MHz |
| Zigbee | {11, 15, 20, 25} | 4 | 2411/2415/2420/2425MHz |
| NRF24 通用 | {76, 78, 79} | 3 | 2476/2478/2479MHz |

nRF24 channel → 頻率公式：**2400 + channel (MHz)**

---

## 🛡 操作守則（必讀）

1. **只在法拉第籠內操作**（鋁箔紙箱即可）
2. **只用電池供電**（鋰電 + TP4056，不要一邊充電一邊用）
3. **只測自有舊設備**
4. **連續不超過 5 分鐘**（nRF24 PA 發燙）
5. **絕不在公共空間開機**

台灣「電信管理法」第 66/67 條：製造、持有、使用干擾器均違法。本 skill 僅供**自有設備、受控實驗室環境、學術研究**用途。

---

## 📁 專案位置

- RF Jammer 完整 clone: `~/projects/RF Jammer-study/`
- 研究報告: `~/projects/multi-protocol-jammer-guide/RESEARCH.md`
- Wang 現有 jammer 專案: `~/projects/esp32-nrf24-jammer/` (esp32-nrf24-jammer-builder skill)

---

## 📚 來源

- cifertech/RF Jammer (GitHub, ★1,721): https://github.com/cifertech/RF Jammer
- jbohack/ (GitHub, ★547): https://github.com/jbohack/
- RF Jammer 官方文件: https://cifertech.net/RF Jammer-your-portable-ble-bluetooth-jamming-tool/
-  商店: https://nyandevices.com