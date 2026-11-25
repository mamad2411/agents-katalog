---
name: ht9045-secsgem
description: HT9045 SECS/GEM 通訊模組知識庫。當使用者詢問 SECS/GEM、SVID、ECID、CEID、Report、S1F1、S2F15、SV 變數、EC 變數、SetSVDataPointer、SetECDataPointer、AddSV、AddEC、AddCEID、AddReport、HT9045Gem、uHGemHT9045、SECS Alarm、Event Report、溫度 SECS 回報等相關問題時，應先載入此技能。關鍵字：SECS, GEM, SVID, ECID, CEID, SV, EC, Report, SetSVDataPointer, SetECDataPointer, AddSV, AddEC, uHGemHT9045, HT9045Gem, S1F1, S2F15, S7F23, SEMI。
---

# HT9045 SECS/GEM 模組知識庫

## 完整 SV / EC 對照表（逐筆查詢）

> 逐筆 SVID/ECID → 名稱/型態/資料來源/註解的對照表已自動產生，查特定 ID 或變數時用這份，
> 不要只看下方的「範圍區段」概覽。
>
> - 說明：`references/SECS_SV_EC_Reference.md`
> - SV（772 筆）：`references/sv_table.csv`
> - EC（1671 筆）：`references/ec_table.csv`
> - 重新產生：`python scripts/extract_secs_sv_ec.py`

## 檔案結構

| 檔案 | 說明 |
|------|------|
| `SECSGEM/uHGemHT9045.h` | HT9045Gem 類別宣告、CEID enum (ETypeStruct)、Report 結構 |
| `SECSGEM/uHGemHT9045.cpp` | CEID 註冊 (AddCEID)、Report 註冊 (AddReport)、SECS 訊息處理 |
| `SECSGEM/uHGemHT9045_SV.cpp` | SV 變數註冊 (AddSV) |
| `SECSGEM/uHGemHT9045_EC.cpp` | EC 變數註冊 (AddEC) |
| `SECSGEM/uHGemClass.h` | HTGem 基類，定義 SECS 訊息處理虛擬函式 |
| `SECSGEM/uHGemClass.cpp` | HTGem 基類實作 |
| `SECSGEM/uHGemEquipment.h/.cpp/.dfm` | THGem 底層元件，提供 SetSVDataPointer/SetECDataPointer API |
| `SECSGEM/uHGemHT9045_EC.cpp` | EC 變數註冊 |
| `SECSGEM/UsecegemMainFrom.cpp/.h/.dfm` | SECS GEM 主畫面 |
| `SECSGEM/SECSGEM.cpp` | SECS/GEM 系統初始化 |
| `SECSGEM/TasmInfo.cpp/.h` | SECS 訊息解析/組裝 |

## API 格式

### SV 註冊（Status Variable，唯讀）
```cpp
HGemPtr->SetSVDataPointer(
    SVID,                    // int: 唯一識別碼
    HType.ASCII_TYPE,        // 資料型態
    "Variable Name",         // 變數名稱（SECS 可見）
    "Unit",                  // 單位（可為 ""）
    &DataPointer,            // 資料來源指標（變數、TEdit*、TLabel*、TPanel* 等）
    "Description"            // 註解
);
```

### EC 註冊（Equipment Constant，可讀寫）
```cpp
HGemPtr->SetECDataPointer(
    ECID,                    // int: 唯一識別碼
    HType.FT_8_TYPE,         // 資料型態
    "Variable Name",         // 變數名稱（SECS 可見）
    "Unit",                  // 單位
    &DataPointer,            // 資料來源指標
    "Max",                   // 最大值（字串）
    "Min",                   // 最小值（字串）
    "Default",               // 預設值（字串）
    "Description"            // 註解
);
```

### 支援資料型態
| 型態常數 | 說明 |
|---------|------|
| `HType.ASCII_TYPE` | 字串（AnsiString、TEdit*、TLabel*、TPanel*） |
| `HType.INT_4_TYPE` | 32-bit 整數 |
| `HType.FT_8_TYPE` | 64-bit 浮點數（double） |
| `HType.BOOLEAN_TYPE` | 布林值 |

## SVID 編號分配

| 範圍 | 用途 |
|------|------|
| 1000–1050 | 機台基本資訊（Machine ID/Version/State/UPH/Time） |
| 1051–1098 | 溫度即時值（tcHotPlate1~tcBh2, HeatGun, DUT, Socket） |
| 1100–1420 | Bin Count、Test Result、Site Count |
| 1430–1468 | Contact Count、Bin Assignment |
| 1470–1473 | CCD2/2DID/LB/ESD Temperature |
| 1700–1707 | Auto car Count |
| 2001–2106 | Contact Force/Height |
| 2631–2756 | Height Calibration/Tray Alias |
| 6001–6002 | Total Contact Count |
| 9001–9004 | Auto Clean |
| 15500 | Pre Alarm |
| 16200–16215 | Site Bin Total |
| 37501–37508 | ATC Power Supply Info |

## ECID 編號分配

| 範圍 | 用途 |
|------|------|
| 1006–1007 | Lot/Operator ID |
| 1191 | RFID Reader |
| 1430–1431 | Contact Alarm Setting |
| 1501–1531 | Recipe/User/Tester/Temp/Site |
| 1581–1595 | Lot Information（SPIL） |
| 1600–1649 | Individual Temperature |
| 1701 | 2DID Allow List |
| 2001–2023 | Contact Force/Dimension/Kit |
| 3640–3655 | Bin Type |
| 4901–4925 | Temperature Mode/LB Boost |
| 6501–6599 | Single Temp Limit（6551+tcIndex） |

## CEID 事件（ETypeStruct enum）

主要事件（共 ~190+ 個）：
- 1~10: 操作按鈕（Start/Pause/LotStart/LotEnd）
- 11~25: 模式切換（Production/Engineer/Temperature）
- 26: GetTestResult
- 27: RunStatus（Machine State Change）
- 43: DownloadRecipe
- 77: ReadCurrentESDData（Time Event）
- 80~83: 即時數據讀取（Handler/ATC/EP）
- 89: PreAlarmMessage
- 91~93: SECS Online/Offline
- 94~118: Transfer/Cassette 事件
- 141: GemControlStateChange

## 溫度 SV 變數結構

溫度即時值統一使用 `RunInfo.ShowTempComp[tcXxx]` 作為資料來源：
```cpp
HGemPtr->SetSVDataPointer(SVID, HType.ASCII_TYPE, "Name", "", &RunInfo.ShowTempComp[tcXxx], "Comment");
```

溫度上下限使用 EC 透過 `Temperature.xxx` 或 `IniConfig.dSingleTempLimit[tcXxx]`：
```cpp
HGemPtr->SetECDataPointer(ECID, HType.FT_8_TYPE, "Name", "Celsius", &Temperature.xxx, "Max", "Min", "Default", "Comment");
```

### 溫控元件 enum（eTempControll in MachineType.h）

| enum | 值 | 說明 |
|------|---|------|
| tcHotPlate1~tcHotPlate4 | 0,1,63,64 | 加熱板 |
| tcShuttle1~tcShuttle4 | 2,3,65,66 | 飛梭 |
| tcHead1~tcHead4 | 4,5,6,7 | Index Head |
| tcSocket | 8 | Socket |
| tcChamber | 9 | Chamber |
| tcCCD, tcCCD_2 | 10, 52 | CCD |
| tcAa1~tcBh2 | 11~48 | Index Heater |
| tc2D | 49 | 2D Scanner |
| **tcLB** | **50** | **LB（Load Board）** |
| tcIndexESD | 51 | Index ESD |
| tcATCHotAir1~2 | 53,54 | ATC Hot Air |
| tcOutSht1~2 | 55,56 | Out Shuttle |
| tcBase1~6 | 57~62 | TriTemp Base |
| tcDoor1~2 | 67,68 | Index Door |
| **tcLBUp** | **69** | **LB 上表面** |
| **tcLBDown** | **70** | **LB 下表面** |
| tcTotalCount | 71 | 總數 |

### LB 溫度相關變數

| 變數 | 所在 | 說明 |
|------|------|------|
| `Temperature.bLBTempFunction` | cprod.h | LB 溫度功能開關 |
| `Temperature.dLBTempHighSettingValue` | cprod.h | LB 溫度上限設定值（Frank 20241231） |
| `Temperature.dLBTempLowSettingValue` | cprod.h | LB 溫度下限設定值 |
| `Temperature.bLBTempHighAlarm_Enable` | cprod.h | LB 高溫 Alarm 開關（Jimmychiu 20251215） |
| `Temperature.bLBTempLowAlarm_Enable` | cprod.h | LB 低溫 Alarm 開關 |
| `RunInfo.ShowTempComp[tcLB]` | cprod.h | LB 即時溫度顯示 |
| `RunInfo.ShowTempComp[tcLBUp]` | cprod.h | LB 上表面即時溫度 |
| `RunInfo.ShowTempComp[tcLBDown]` | cprod.h | LB 下表面即時溫度 |
| `UN150Read[tcLB]` | — | LB 溫度讀值（double） |
| `UN150Read[tcLBUp]` | — | LB 上表面溫度讀值 |
| `UN150Read[tcLBDown]` | — | LB 下表面溫度讀值 |

### 設定檔（Temp_Set.ini）
- Section: `[LB Temp Function]`
- Key: `LB_Temp_High_Setting` → `dLBTempHighSettingValue`
- Key: `LB_Temp_Low_Setting` → `dLBTempLowSettingValue`

## 新增 SECS 變數 SOP

### 新增 SV（唯讀狀態變數）
1. 在 `uHGemHT9045_SV.cpp` 的 `AddSV()` 中，找到合適位置插入
2. 選擇未使用的 SVID
3. 呼叫 `HGemPtr->SetSVDataPointer(...)` 
4. 確認資料來源指標有效（變數已宣告且初始化）

### 新增 EC（設備常數，可讀寫）
1. 在 `uHGemHT9045_EC.cpp` 的 `AddEC()` 中插入
2. 選擇未使用的 ECID
3. 呼叫 `HGemPtr->SetECDataPointer(...)`
4. 若需支援 S2F15 寫入，確認 `SetECValue()` 有對應處理

### 新增 Event（CEID）
1. 在 `uHGemHT9045.h` 的 `ETypeStruct` enum 新增項目
2. 在 `uHGemHT9045.cpp` 的 `AddCEID()` 註冊
3. 在 `AddReport()` 綁定 Report（含哪些 SVID）
4. 在業務邏輯觸發點呼叫 `HGem->SendCEIDReport(CEID)`

## 前置條件
- 所有 SV/EC 註冊受 `CosFunction.bEnable_SECS_GEM == true` 保護
- EC 額外受 `CosFunction.bGPIBUseSECSGENData` 保護
