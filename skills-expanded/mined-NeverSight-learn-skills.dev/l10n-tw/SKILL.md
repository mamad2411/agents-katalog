---
name: l10n-tw
description: 將開源專案的 PO/POT 翻譯並驗證成正體中文（zh-TW）PO 檔的 SOP 與工具。當使用者提到翻譯、在地化、l10n、zh_TW／zh-Hant、正體中文、gettext、PO／POT 檔或 Weblate 上傳時使用。
compatibility: Requires uv (with polib), gettext (msgfmt), git, and optionally the gh CLI; needs network access for git operations.
metadata:
  author: l10n-tw
  version: "1.9"
  hermes:
    tags:
      - l10n
      - translation
      - gettext
      - po
      - zh-tw
      - localization
---
# PO Translation — Chinese Localization Project

開源專案正體中文在地化的 SOP 與工具。

## 參考文件

翻譯前務必閱讀 [`references/l10n-tw-guide.md`](references/l10n-tw-guide.md)，內含：

- **基本守則** — 12 條翻譯品質規範（禁止機器翻譯直接提交、禁止簡轉繁不做轉換等）
- **翻譯風格與術語訂立方法** — 情境限定直譯原則、術語發想三步驟
- **譯文格式規範** — 標點符號、空格排版、快捷鍵字元、變數位置交換、日期時間格式等
- **PO 檔頭格式規範** — 檔頭必填欄位與範例
- **語言地區表示法** — 正體中文 vs 繁體中文、各語言文字體系譯法

> 來源檔來自 [Translation Project](https://translationproject.org/) 平台時，
> 翻譯完成後的品質驗收須符合 [`references/translation-project.md`](references/translation-project.md) 的 TP 格式條件。

## 目錄結構

```
l10n-tw/
├── SKILL.md                        # 本文件 — 流程說明
├── references/
│   ├── l10n-tw-guide.md            # 翻譯規範與指引（必讀）
│   ├── terminology.md              # 用語對照表
│   ├── github.md                   # GitHub 操作參考
│   ├── locale.md                   # 語言環境命名策略
│   ├── gettext-tools.md            # gettext 工具組參考
│   └── translation-project.md      # TP 平台專案品質驗收規範（來源為 TP 時必讀）
├── scripts/
│   ├── po_gen.py                     # POT + <potstem>-translations.py → PO
│   ├── po_verify.py                  # POT ↔ PO 驗證比對
│   ├── po_align_check.py             # CLI 求助文字對齊檢查（顯示寬度）
│   ├── po_preflight.py               # 來源檔預檢（編碼/檔頭/fuzzy/重複）
│   ├── po_to_pot.py                # 任意 PO → POT（萃取模板）
│   ├── po_to_translations.py       # PO → <potstem>-translations.py（保留舊譯文）
│   ├── fix_terminology.py          # 依 references/terminology.md 修正 translations 檔（translations.py 或 .po）
│   ├── extract_batch.py            # 批次翻譯：PO/POT → 待翻譯 JSON
│   ├── merge_batches.py            # 批次 JSON → <potstem>-translations.py
│   ├── apply_translations.py       # 批次 JSON → 直接套用至 PO（情境 D）
│   └── regression_test.py          # 回歸測試
└── ...                             # 專案目錄動態，位於 PO/POT 所在目錄
```

> **目錄約定**：專案目錄是**動態**的，以要翻譯的 PO 或 POT 檔所在目錄為主，不綁定
> `skills/l10n-tw/` 下的固定位置。所有非暫存產出檔案（`<potstem>-translations.py`、生成的 PO）
> 須與來源 POT 或 PO 位於同一層目錄。
>
> **來源僅 repo URL**（本地無 PO/POT）：clone 與翻譯工作目錄**分離**，避免污染 clone repo。
> - clone／fork 至暫存工作區 `$TMPDIR/l10n-tw/<project>/`（本環境慣例 `/tmp/opencode/l10n-tw/`），或使用者指定目錄；**不得** clone 進技能目錄或目前所在專案 repo 內部
> - 於 clone 外建立姊妹工作目錄 `<project>-work/`，將來源 POT／PO 複製至其中；`<potstem>-translations.py`、批次 JSON、生成的 PO 等全部產出留在工作目錄，不寫入 clone
> - 交付時才把最終 PO（與 LINGUAS 修改）從工作目錄複製回 clone 對應位置，再進行 git 操作
>
> **翻譯檔命名**：一律使用 `<potstem>-translations.py` 配對 `<potstem>.pot`
> （potstem = POT 檔名主體，如 `template.pot` → `template-translations.py`）。
> `regression_test.py` 依此規則探索；既有以預設 `translations.py` 命名的舊專案
> 仍向後相容（單一未配對 POT 的目錄會回退使用）。

## 核心概念

1. **所有專案的最終產出是 PO 檔**，但中間的**單一真相來源是 `<potstem>-translations.py`**（下稱 translations 檔）。
2. **POT 或 PO 只是起點**：讀取後都轉成 translations 檔，再統一產出 PO。
3. **無論來源格式或專案大小**，最後都走 `fix_terminology.py` → `po_gen.py` → `po_verify.py` + `msgfmt`。

> 批次 JSON 只是大型專案的工作草稿，最終仍須合併回 translations 檔，
> 才能讓 `regression_test.py` 掃到並回測。

## 快速決策表

先確認三個問題：來源格式、來源語言、專案規模。然後照表執行對應流程。


| 來源格式 | 來源語言 | 規模  | 既有翻譯 | 流程                                                                                                                               |
| ---- | ---- | --- | ---- | -------------------------------------------------------------------------------------------------------------------------------- |
| POT  | —    | 小   | 無    | 手建 `<potstem>-translations.py` → `fix_terminology.py` → `po_gen.py` → `po_verify.py`                                                              |
| POT  | —    | 大   | 無    | `extract_batch.py` → 填 `batchN.json` → `merge_batches.py` → `fix_terminology.py` → `po_gen.py` → `po_verify.py`                  |
| PO   | 繁體中文 | 小   | 保留   | `po_to_translations.py` → `fix_terminology.py` → 手動補洞 → `po_gen.py` → `po_verify.py`                                             |
| PO   | 繁體中文 | 小   | 不保留  | 同 POT 小專案                                                                                                                        |
| PO   | 繁體中文 | 大   | 保留   | `extract_batch.py --all` → 審修 `batchN.json` → `merge_batches.py` → `fix_terminology.py` → `po_gen.py` → `po_verify.py`           |
| PO   | 繁體中文 | 大   | 不保留  | 同 POT 大專案                                                                                                                        |
| PO   | 其他語言 | 小   | 不保留  | `po_to_pot.py` → 手建 `<potstem>-translations.py` → `fix_terminology.py` → `po_gen.py` → `po_verify.py`                                    |
| PO   | 其他語言 | 大   | 不保留  | `po_to_pot.py` → `extract_batch.py` → 填 `batchN.json` → `merge_batches.py` → `fix_terminology.py` → `po_gen.py` → `po_verify.py` |
| PO   | 繁體中文 | 任一   | 保留   | 局部補翻：`extract_batch.py --all` → 審修 `batchN.json` → `apply_translations.py` → 情境 D 驗證 SOP                                    |


**規模門檻**：建議 **2000 條 msgid** 以下使用單一 `<potstem>-translations.py`；超過則考慮批次流程。
（實際上 2000 條以下仍可用單一檔案管理，視編輯便利性調整。）

---

## 環境準備（首次執行必做）

所有工具腳本只依賴 Python 標準庫與 `polib`（回歸測試 `regression_test.py` 使用）。
**開始任何翻譯任務前**，先確認 polib 可用：

```bash
uv run python3 -c "import polib"
```

- 正常輸出（無錯誤）→ 環境就緒，直接開始。
- 報 `No module named 'polib'` → 依序執行：

```bash
uv venv                  # 建立 .venv（僅首次；已有則略過）
uv pip install polib     # 安裝 polib（須在 venv 建立之後）
uv run python3 -c "import polib"   # 確認成功後再繼續
```

> **為什麼要檢查**：`uv run` 在找不到 .venv 時會**靜默退回裸 Python（不報錯）**，
> 所以「指令能跑」不代表環境就緒——polib 缺席時，回歸測試會以
> `No module named 'polib'` 讓所有專案全數 FAIL。安裝順序不可顛倒：
> `uv pip install` 在沒有 venv 時會直接報
> `No virtual environment found`。若環境禁止建立 venv（PEP 668
> externally-managed），回報使用者處理，不得擅自 `--system` 安裝。

---

## 情境 A：來源是 POT

### A1. 小專案（&lt; 2000 條）

1. 建立專案目錄，放入 `template.pot`。
2. 在相同目錄建立 `template-translations.py`（`<potstem>-translations.py`）：
  ```python
   TRANSLATIONS = {
       "msgid 原文": "正體中文翻譯",
       "Another string": "另一個字串",
       "Showing <b>%d</b> result": ["顯示 <b>%d</b> 條結果"],
   }
  ```
  - `msgid` 用 ASCII 單引號 `'` 包起。
  - 多行字串用 real `\n`。
  - 複數條目用 Python list。
3. 執行通用驗證步驟（見下方）。

### A2. 大專案（≥ 2000 條）

1. 切批：依 POT 行號範圍 `[start, end]`（1-based，含兩端）提取待翻譯條目。
  ```bash
   uv run python3 skills/l10n-tw/scripts/extract_batch.py \
     <path/to/template.pot> <batch1.json> <start1> <end1>
  ```
2. 在每個 `batchN.json` 填入譯文：`{"msgid": "正體中文翻譯"}`。
  - 不要修改 msgid 與 XML 標籤。
3. 合併為 translations 檔：
  ```bash
   uv run python3 skills/l10n-tw/scripts/merge_batches.py \
     batch1.json batch2.json ... -o template-translations.py
  ```
4. 執行通用驗證步驟。

---

## 情境 B：來源是 PO（繁體中文）

先確認是否保留既有翻譯。若上游也同時提供新的 POT，請以新 POT 作為 `po_gen.py` 的輸入，
舊 PO 只當翻譯來源。

### B1. 小專案 + 保留既有翻譯

1. 從舊 PO 抽出非空譯文（輸出檔名對應新 POT 的 potstem）：
  ```bash
   uv run python3 skills/l10n-tw/scripts/po_to_translations.py \
     <path/to/old-zh_TW.po> -o <potstem>-translations.py
  ```
2. 執行通用驗證步驟。`po_gen.py` 會報告 missing 條目，依新 POT 補翻。

### B2. 小專案 + 不保留

同 [A1. 小專案](#a1-小專案小於-2000-條)。

### B3. 大專案 + 保留既有翻譯

1. 用 `--all` 從舊 PO 抽出全部條目（保留既有 msgstr）：
  ```bash
   uv run python3 skills/l10n-tw/scripts/extract_batch.py --all \
     <path/to/old-zh_TW.po> <batch1.json> <start1> <end1>
  ```
2. 逐批審修、補翻。
3. 合併為 translations 檔（同 A2 步驟 3）。
4. 執行通用驗證步驟。

### B4. 大專案 + 不保留

同 [A2. 大專案](#a2-大專案大於等於-2000-條)。

---

## 情境 C：來源是 PO（其他語言）

其他語言的 PO 不保留其譯文，只當作取得 POT 與 msgid 清單的來源。

### C1. 小專案

1. 萃取 POT：
  ```bash
   uv run python3 skills/l10n-tw/scripts/po_to_pot.py \
     <path/to/source.po> -o <path/to/project.pot>
  ```
2. 手建 `<potstem>-translations.py`（同 A1 步驟 2）。
3. 執行通用驗證步驟。

### C2. 大專案

1. 萃取 POT（同 C1 步驟 1）。
2. 切批、填譯文、合併（同 A2 步驟 1–3）。
3. 執行通用驗證步驟。

---

## 通用驗證步驟

無論哪個情境，完成翻譯後都依序執行。**工具不適用時不得跳過對應檢查**——改用下方列出的替代方式，或人工檢查並載明。

### 路徑 × 驗證工具適用性

| 驗證項目 | 標準路徑（情境 A/B/C，translations 檔） | PO 直接路徑（情境 D） |
|---|---|---|
| 用語修正 | `fix_terminology.py <potstem>-translations.py` | `fix_terminology.py <output.po>`（PO 模式） |
| 生成 PO | `po_gen.py`（translation 檔 → PO） | 不需生成，直接編輯 |
| 驗證 PO | `po_verify.py <pot>.pot <output.po>` + `msgfmt -cv` | 同左；無 POT 時先 `po_to_pot.py` 萃取 |
| 對齊檢查 | `po_align_check.py <pot>.pot <output.po>` | 同左 |
| 回歸測試 | `regression_test.py --root` | 不涵蓋（已知限制，見情境 D） |
| 佔位符／空格標點抽查 | 人工抽查（見品質自檢清單） | 同左 |

> 判斷「工具不適用」前先確認：例如 PO 直接路徑沒有 POT，**不是**跳過 `po_verify.py` 的理由，
> 而是用 `po_to_pot.py` 萃取出 POT 再驗證。

### 1. 用語修正

```bash
uv run python3 skills/l10n-tw/scripts/fix_terminology.py \
  <path/to/<potstem>-translations.py>
```

輸入為 `.po` 檔時自動切換為 PO 模式，掃描所有 msgstr（含複數）：

```bash
uv run python3 skills/l10n-tw/scripts/fix_terminology.py \
  <path/to/output.po>
```

預設會讀取技能內 `references/terminology.md`；若要指定其他術語表，用
`--terms <path/to/terminology.md>`。

術語表標記三種語意，自動化程度不同：

- `不翻「X」` — **禁用詞**（中國用語，如「默認」「用戶」），自動替換為 TW 欄位譯法
- `留意「X」` — **僅掃描不替換**（語境敏感詞，如「文件」在 document 語境是合法譯法），
  出現於「👀 Scan-only terms」報告，由譯者**人工判定**後決定是否修正
- `對應「anchor」` + 上述標記 — **英文錨定**（msgid 命中 anchor 詞才作用），解決
  msgstr 用詞正確與否取決於英文 msgid 語境的術語，如：
  - `對應「line」「lines」留意「行」` — msgid 含 line/lines 且 msgstr 用「行」時，
    出現於「👀 錨定掃描命中」報告（附 msgid＋msgstr 摘錄），逐條人工判定：
    line 語境（第 %d 列、每列）改為「列」，合法複詞（換行、執行、行為）保留
  - `對應「keyring」「key ring」不翻「金鑰環」` — msgid 含 keyring/key ring 時
    自動改為「鑰匙圈」

> 特別注意：自動替換只處理「不翻」禁用詞，**不處理**「留意」詞——因為
> 字串層級無法區分語境（如「項目」= item 合法 vs project 禁用）。誤改
> 會破壞既有譯文，寧可保留在掃描報告中人工處理。
>
> 特別是從既有 PO 起步時，簡轉繁會帶入中國用語，必須跑過一次。
> 錨定詞比對為**詞界、大小寫不敏感**：`recvline`、`headline` 不會誤觸發
> `line`，但 `command-line`、`1.5 lines`、`Line spacing` 會（後兩者
> 語境由人工判定）。

**完成標準**：輸出**沒有**「⚠️ Remaining banned terms」（自動替換已全清）；
「👀 Scan-only terms」殘留時，逐項人工檢視，認定合法（如 document 語境的「文件」）
或修正後視為完成；「👀 錨定掃描命中」逐條依 msgid 語境判定，line 語境的「行」修正為
「列」，合法複詞（換行／執行／行為等）保留並於證據中載明。

### 2. 生成 PO

```bash
uv run python3 skills/l10n-tw/scripts/po_gen.py \
  <path/to/template.pot> \
  -t <path/to/template-translations.py> \
  -o <path/to/output.zh_TW.po>
```

> 輸出路徑原則上應與來源 POT 同層目錄；專案另有指定工作目錄時，依指定目錄輸出。
>
> **Translation Project 專案**：標頭須符合 TP 格式，生成時務必加上
> `--team "Chinese (traditional) <zh-l10n@lists.slat.org>"`。
> 檔頭開頭註解（`SOME DESCRIPTIVE TITLE.` 樣板）、{PACKAGE-NAME} 判定與品質驗收條件，
> 詳見 [`references/translation-project.md`](references/translation-project.md)。

**完成標準**：輸出顯示「All entries translated」，無 missing，且輸出檔案位於與 POT 相同（或專案指定）的目錄。

### 3. 驗證 PO

```bash
uv run python3 skills/l10n-tw/scripts/po_verify.py \
  <path/to/template.pot> <path/to/output.po> --comments

msgfmt -cv <path/to/output.po> -o /dev/null
```

確認：

- Entry count matches（無遺漏、無多餘）
- Coverage 100%
- No fuzzy markers
- 註解行保留
- `msgfmt` 無 c-format 錯誤
- 格式符合 `references/l10n-tw-guide.md` 規範

**完成標準**：`po_verify.py` 與 `msgfmt` 皆退出碼 0。

### 4. 對齊檢查（CLI 求助文字）

Translation Project 等指令型套件的 `--help` 輸出會把每個選項補空格到固定**顯示欄位**，
讓說明文字對齊同一欄。CJK 字元是雙欄寬，翻譯後選項寬度改變，補空格數必須依顯示寬度
重算，否則說明欄會位移。

```bash
uv run python3 skills/l10n-tw/scripts/po_align_check.py \
  <path/to/template.pot> <path/to/output.po>
```

- 選項行（前導空白 ≥2 且有 2+ 空格分隔）：譯文說明欄位必須等於原文欄位
- 續行（前導空白 ≥10 的純縮排）：譯文縮排欄位必須等於原文
- 含 `\t` 的行跳過（Tab 對齊由 Tab 本身保證）；譯文換行結構與原文不同時跳過該行
- 譯文選項顯示寬度超過原文說明欄 → 報「無法對齊（需人工決定）」
- 無 CLI 求助對齊行的專案 → 印「無 CLI 求助對齊行」即通過（**不是**跳過檢查的理由）

**完成標準**：退出碼 0。退出碼 1 時依報告逐條調整補空格數（見
`references/l10n-tw-guide.md` 3.11），重新生成後再驗證直至 0。

### 5. 回歸測試（修改腳本後必跑）

**前置檢查**：先確認 polib 已安裝（缺少時所有專案會全數 FAIL）：

```bash
uv run python3 -c "import polib"
```

若報 `No module named 'polib'`，依「[環境準備](#環境準備首次執行必做)」章節的
SOP（`uv venv` → `uv pip install polib`）建立環境後重試。確認無誤後再執行：

```bash
uv run python3 skills/l10n-tw/scripts/regression_test.py --root <projects-dir>
```

`--root` 為必填，指向含 (POT, translations 檔) 專案對的目錄（不會隱式掃描 cwd）；
執行前會列出將載入的 translations 檔並要求確認，非互動環境請加 `--yes`。

**完成標準**：所有專案顯示 `[OK]`。

---

## 腳本參考


| 腳本                      | 用途       | 輸入                                 | 輸出                     |
| ----------------------- | -------- | ---------------------------------- | ---------------------- |
| `po_gen.py`             | 生成 PO    | `template.pot` + `<potstem>-translations.py` | `zh_TW.po`             |
| `po_verify.py`          | 驗證 PO    | `template.pot` + `zh_TW.po`        | 報告 + exit code         |
| `po_align_check.py`     | CLI 對齊檢查 | `template.pot` + `zh_TW.po`        | 報告 + exit code         |
| `po_preflight.py`       | 來源檔預檢    | 來源 `.pot`／`.po`                    | 報告 + exit code         |
| `po_to_pot.py`          | 萃取 POT   | 任意 PO                              | 無翻譯的 POT               |
| `po_to_translations.py` | 抽出舊譯文    | 繁體中文 PO                            | `<potstem>-translations.py` |
| `extract_batch.py`      | 切批       | PO 或 POT                           | `batchN.json`          |
| `merge_batches.py`      | 合併批次     | 多個 `batchN.json`                   | `<potstem>-translations.py` |
| `apply_translations.py` | 直接套用至 PO | `batchN.json` + 既有 PO              | 更新後的 PO                |
| `fix_terminology.py`    | 用語正規化    | translations 檔（`translations.py` 或 `.po`） | 修正後的同格式檔            |
| `regression_test.py`    | 回歸測試     | 所有專案                               | 比對報告                   |


### 情境 D：PO 直接路徑（apply_translations.py）

`merge_batches.py` + `po_gen.py` 是標準流程（情境 A/B/C）；若你偏好直接編輯 PO 檔——
例如上游只有既有 PO、任務只是局部補翻——可用 `apply_translations.py` 把 `batchN.json`
直接套用至既有 PO：

```bash
uv run python3 skills/l10n-tw/scripts/apply_translations.py \
  <batchN.json> -o <path/to/output.po>
```

**此路徑的驗證 SOP（品質檢查同等重要，不可跳過）：**

1. **用語修正**（PO 模式）：
   ```bash
   uv run python3 skills/l10n-tw/scripts/fix_terminology.py <path/to/output.po>
   ```
2. **生成／取得 POT**：有上游新 POT 直接用；否則從既有 PO 萃取：
   ```bash
   uv run python3 skills/l10n-tw/scripts/po_to_pot.py <path/to/output.po> -o <path/to/project.pot>
   ```
3. **驗證 PO**：
   ```bash
   uv run python3 skills/l10n-tw/scripts/po_verify.py <path/to/project.pot> <path/to/output.po> --comments
   msgfmt -cv <path/to/output.po> -o /dev/null
   ```
4. **對齊檢查**（CLI 求助文字）：
   ```bash
   uv run python3 skills/l10n-tw/scripts/po_align_check.py <path/to/project.pot> <path/to/output.po>
   ```
5. **品質自檢清單**（見下方）逐項檢查。

注意：此路徑不產出 translations 檔，因此 `regression_test.py` 不會涵蓋這些專案——
這是**已知限制**，不是省略其他檢查的理由。

---

## Gettext 工具參考

手動使用 gettext 工具組（msgfmt／msgmerge／msginit／iconv）的常見情境、命令與格式字串變數交換範例，見 [`references/gettext-tools.md`](references/gettext-tools.md)。

---

## Workflow

### 制定翻譯計畫

動手翻譯前，先與使用者**共同**制定翻譯計畫：把以下事項整理成一份計畫摘要，**展示給使用者確認後**，才進入 Phase 1。不要跳過此步驟直接開始翻譯。

1. **來源格式與條數** — 確認來源是 POT 或 PO、來源語言、需翻譯的條數；≥ 2000 條時採用批次翻譯（每批 100–160 條）。來源僅 repo URL 時，先 clone 至暫存工作區勘察 `po/` 內容（POT 或 PO、來源語言、條數、既有 zh_TW），再回報
2. **情境與流程選定** — 對照「快速決策表」點出將走的情境（A／B／C／D）與規模（小／大）
3. **既有翻譯去留** — 來源為正體中文 PO 且部分已有翻譯時，確認保留或重新翻譯
  - 保留：使用本文件「情境 B」對應流程
  - 重新翻譯：使用「情境 A」或「情境 C」流程
4. **提交方式** — 確認完成後如何交付：手動上傳（如 Weblate 網頁上傳 PO）、git commit + PR（慣例見 `references/github.md`）、或其他管道
5. **分批切割**（大專案適用） — 列出預計批次範圍
6. **翻譯者身份（Last-Translator）** — 產出 PO 前確認翻譯者身份，來源依序為：
  - `--translator` 參數 → `L10N_TW_TRANSLATOR` 環境變數 → `skills/l10n-tw/.env` 設定檔
  - 三者皆無時依以下三步驟處理：
    1. 詢問使用者姓名與 email
    2. **必須接著問**是否寫入 `skills/l10n-tw/.env` 永久保存，供以後翻譯任務自動套用
    3. 同意 → 建立／寫入 `.env`（格式 `L10N_TW_TRANSLATOR="Name <email>"`）並回報已保存；拒絕 → 僅本次使用該身份，不寫入檔案

**[GATE] 翻譯計畫確認** — 將上述摘要展示給使用者，明確等使用者確認後才開始 Phase 1。計畫未經確認，不得進行翻譯。

- **完成標準：** 來源格式、條數、情境/流程、是否批次、既有翻譯去留、提交方式、翻譯者身份（含是否保存至 `.env`）皆經使用者確認

### Phase 1 — 前置準備

1. **Reconnaissance** — 確認 i18n 框架（gettext / GResource XML / Blueprint）、locale 命名慣例（看既有 .po 檔名或 LINGUAS）、POT msgid 數量
  - **完成標準：** i18n 框架已確認、locale 命名已確認、POT msgid 數量已記錄
2. **Fork** — 透過 `gh repo fork <upstream> --remote-name fork`，再重構 remote（origin=fork, upstream=upstream）。遠端命名慣例見 `references/github.md`。來源僅 repo URL 時，先在暫存工作區建立 clone（如 `gh repo clone <upstream> $TMPDIR/l10n-tw/<project>`），再於 clone 內執行 fork 與 remote 重構
  - **完成標準：** `git remote -v` 顯示正確的 origin 與 upstream
3. **取得 POT** — 從上游取得最新的 POT；若上游沒有 POT，只有既有 PO 檔，則用 `po_to_pot.py` 萃取。來源僅 repo URL 時，將 clone 內的 POT／PO 複製至工作目錄 `<project>-work/`，以其為來源
  - **完成標準：** 專案工作目錄中存在 `<project>.pot`
4. **來源檔格式驗證** — 建立 translations 檔之前，先確認來源 POT／PO 內容格式符合規範，否則後續 `po_gen.py`／`po_verify.py`／`po_to_pot.py`／`po_to_translations.py` 會失敗或靜默產出錯誤結果。
  ```bash
   uv run python3 skills/l10n-tw/scripts/po_preflight.py <path/to/source.pot_or_po>
  ```

   `po_preflight.py` 會檢查：編碼與 BOM、檔頭條目、必填檔頭欄位（`Content-Type`、`Plural-Forms` 等）、`msgfmt -cv` 格式合法性、檔頭／條目級 `#, fuzzy` 旗標、重複 `(msgctxt, msgid)`、過時 `#~` 條目、行尾。檔頭格式基準見 [`references/l10n-tw-guide.md`](references/l10n-tw-guide.md)「四、PO 檔頭格式規範」。
  - **異常處置（軟停止）** — 腳本退出碼 1 時，把回報的異常清單展示給使用者，由使用者決定先修正來源檔或以現況繼續；不強制中止流程
  - **完成標準：** `po_preflight.py` 退出碼 0；若退出碼 1，所有異常已展示給使用者並取得處置決定
5. **建立專案目錄** — 將 `<project>.pot` 放入專案目錄，建立 `<project>-translations.py`。預設所有非暫存產出檔案（`<potstem>-translations.py`、生成的 PO）與 POT 位於同一層
  - 專案目錄預設與來源檔案 `<project>.pot` 或 `<project>.po` 同一層
  - 如果另有指定工作目錄者，以指定目錄為優先。
  - 來源僅 repo URL 時，專案目錄＝工作目錄 `<project>-work/`（clone 外）
  - **完成標準：** 專案目錄包含 `<project>.pot` 與 `<project>-translations.py`

### Phase 2 — 翻譯

6. **依情境選擇流程** — 對照「快速決策表」選擇 A、B、C 情境，並依規模選擇小／大專案流程。
  - 翻譯品質要求：用語一致性參考 `references/terminology.md`、格式規範與風格指引參考 `references/l10n-tw-guide.md`、禁止直接從 zh_CN 轉換。
  - **完成標準：** 所有 msgid 皆有翻譯，無直接從 zh_CN 轉換的內容，符合 `references/l10n-tw-guide.md` 規範

### Phase 3 — 生成與驗證

7. 執行「通用驗證步驟」：用語修正 → `po_gen.py` → `po_verify.py` + `msgfmt` → `po_align_check.py` → `regression_test.py`
  - `msgfmt` 驗證用參數：`-o /dev/null`，避免產生暫存檔 `messages.mo`
  - **完成標準：** `po_verify.py` 與 `msgfmt` 皆退出碼 0，且回歸測試所有專案 `[OK]`

**[GATE] 交付前品質自檢清單** — 進入 Phase 4 前逐項檢查，**每一項都要展示檢查輸出證據**
（命令輸出／掃描報告），不得僅口頭宣稱「已檢查」：

- [ ] **用語掃描**：`fix_terminology.py`（translations 檔或 PO 模式）輸出無「⚠️ Remaining banned terms」；「👀 Scan-only terms」殘留已逐項人工判定（合法保留或修正）
- [ ] **完整性**：`po_verify.py` 輸出 Coverage 100%、無 untranslated、無 fuzzy、無 missing/extra
- [ ] **格式合法**：`msgfmt -cv` 退出碼 0，無 c-format 錯誤
- [ ] **佔位符抽查**：`%s`／`%d`／`%1` 等變數與 msgid 一一對應（數量一致，語序可調）
- [ ] **排版抽查**：中英／中數間半形空格、全形標點、快捷鍵格式符合 `references/l10n-tw-guide.md` 3.1–3.3（抽查新翻譯，不限全部條目）
- [ ] **CLI 對齊檢查**：`po_align_check.py` 退出碼 0（適用含 CLI 求助文字的專案；無求助文字時印「無 CLI 求助對齊行」即視為通過）
- [ ] **TP 檔頭檢查**：來源為 Translation Project 平台專案時，依 `references/translation-project.md`「TP 品質驗收清單」逐項勾選（非 TP 專案免勾）
- [ ] **EOF／格式檢查**：產出 PO 以恰好一個換行結尾、無尾端空白（證據：`po_verify.py`／`po_preflight.py` 的檢查輸出，違反時退出碼非零）

**完成標準：** 八項全部勾選並附輸出證據。任一項因工具限制無法自動執行時，必須改以人工檢查並在證據中載明方式——**不得以「工具只吃 translations.py」或「無 POT」為由跳過**（無 POT 時用 `po_to_pot.py` 萃取；工具真的不可用才允許人工替代）。

### Phase 4 — 交付（事先詢問）

交付前須先確認使用者選擇哪種方式。

- **方式一：commit/PR** — 適用 git repo
  1. **[GATE] Show PO to user** — 展示產出的 PO 成品要先審核，**確認後才能繼續下一步**
  2. **回填 clone** — 來源僅 repo URL 時，將工作目錄產出的 PO（與 LINGUAS 修改）複製回 clone 對應位置，確認 `git status` 僅含交付物
  3. **Branch** — 命名 `zh-tw-translation`；monorepo 用 `<project>-zh-tw` 避免混淆。慣例見 `references/github.md`
    - **完成標準：** branch 已建立，名稱符合慣例
  4. **[GATE] Show diff + commit message** — `git diff --cached` 展示變更，同時展示 commit message（`git commit -m "..."`），等確認後才能 commit
  5. **[GATE] Show PR draft** — 展示 PR title + body 草稿，等確認後才能 push 與 `gh pr create`
- **方式二：手動上傳** — 適用 Weblate 等其他翻譯平台
  - 只輸出 PO 檔，不做其他後續處理

---

## GitHub Operations

遠端設定、分支命名、commit/PR 格式等詳細操作請見 [`references/github.md`](references/github.md)。

## 重要慣例

- **LINGUAS 檔案**：插入字母順序（zh_TW 在 zh_CN 後面）。注意 line ending：GNOME 專案可能用 CRLF
- **用語一致性**：參考 `references/terminology.md`。credential=憑證、folder=資料夾、open=開啟、configure=設定
- **語言環境命名**：跟著上游走，不幫上游決定標準。請見 [`references/locale.md`](references/locale.md) 了解 zh_TW 與 zh_Hant 的選擇原則
- **不要直接從 zh_CN 轉換**：簡→繁會帶入中國用語（軟件/文件/信息），逐條從 POT 翻
- **翻譯品質守則**：翻譯前詳閱 [`references/l10n-tw-guide.md`](references/l10n-tw-guide.md)，特別是基本守則（禁止機器/AI 直接提交、禁止簡轉繁、用語前後一致等）
- **產出檔案目錄**：專案目錄動態，以要翻譯的 PO/POT 所在目錄為主；產出檔案（`<potstem>-translations.py`、生成的 PO）與來源 POT 位於同一層目錄
- **驗證暫存檔清理**：若任務中沒有要輸出 `.mo` 檔，純為驗證用途而產生的 `messages.mo`（`msgfmt` 預設輸出）應於作業後清理

---

## 已知坑

1. **多行 msgid** — PO 標準格式把長字串跨多行續寫。`po_gen.py` 有對應支援，但 `po_verify` 若回報 MISSING/EXTRA 時先確認是否為多行 msgid 問題
2. `**More Colors...` vs `More Colors…`** — 三個點（ASCII `...`）與 Unicode 省略號 `…` 是不同的 msgid，兩者都要有對應翻譯
3. `**translations 檔與 committed PO 可能 drift** — 手動編輯 PO 後 translations 檔不會自動同步。修改技能腳本後應執行 `regression_test.py`，由 drift 導致的差異須回寫到 translations 檔再重新生成 PO
4. `**#` 開頭的 fuzzy flag** — 產生 PO 後須確認 header 的 `#, fuzzy` 已移除
5. **execute_code 不載入 env** — 需要 gh CLI / git 操作時要用 terminal 工具
6. **跳脫字元** — `\n`、`\"`、`\\` 在 PO 裡有特殊意義
7. **翻譯用語一致性** — 同一專案內不要同一個英文詞用不同中文翻法
8. **Locale 命名混亂** — `zh_TW`（GNU gettext 傳統） vs `zh_Hant`（BCP 47 現代標準），依上游決定。詳見 `references/locale.md`
9. **舊 PO 譯文可能與新 POT 對不上** — 上游更新後 msgid 可能變動；轉成 translations 檔後用 `po_gen.py` 的 missing 報告補洞
10. **批次流程一定要合併回 translations 檔** — 若停留在 `apply_translations.py` 產出的 PO，`regression_test.py` 不會涵蓋
11. **polib 未安裝** — 回歸測試報 `No module named 'polib'` 時，依「[環境準備](#環境準備首次執行必做)」執行 `uv venv` + `uv pip install polib`（順序不可顛倒）。`uv run` 在無 .venv 時會靜默退回裸 Python，不能以「指令能跑」判斷環境就緒
12. **`split('\n')` 幻影尾元素** — 以換行結尾的輸入經 `text.split('\n')` 會多出 `''` 尾元素，join 重建後檔尾變雙換行。任何以「讀入 → 逐行處理 → 重建」為模式的腳本，輸出前必須過 `po_gen.normalize_eof()`（恰好一個 `\n`）；此類缺陷 `msgfmt`／條目級檢查看不見，須靠 `po_verify.py`／`po_preflight.py` 的 EOF 檢查攔截
13. **`line` 譯為「列」而非「行」** — 指令套件的設定檔解析錯誤訊息（`line %d`、`%d lines`）中，line 依社群慣例譯為「列」（直行橫列）。`fix_terminology.py` 的 `對應「line」「lines」留意「行」` 錨定規則會掃描回報，但「行」也可能出現在合法複詞（換行、執行、行為、行號）中，須依 msgid 語境人工判定，不得一律機械替換
14. **CLI 求助文字對齊** — 翻譯含 CJK 後選項寬度改變，補空格須依**顯示寬度**（CJK=2 欄）重算使說明欄位與原文一致；`po_align_check.py` 偵測偏移。譯文換行結構與原文不同（如合併續行）時檢查器會跳過該行——此時人工確認對齊即可。Tab 對齊的專案由 Tab 本身保證，檢查器自動跳過

