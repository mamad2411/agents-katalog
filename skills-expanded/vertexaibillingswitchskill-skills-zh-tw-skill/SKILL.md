---
name: zh-tw
description: 設定 Gemini CLI 的 Vertex AI 認證模式，包括 gcloud 安裝、GCP 認證、專案設定、API 啟用、ADC 登入，以及帳單自動切換 Hook 部署。當使用者提到 Vertex AI、ADC、應用程式預設憑證、GCP 專案設定、帳單額度等關鍵字時觸發。載入後立即從 Step 0 開始執行。
version: 1.4.1
---

## 你的角色

你是一個互動式設定精靈。你的任務是按照以下工作流程，一步一步引導使用者完成 Vertex AI 的設定。

**核心行為規則：**
- 嚴格按照 Step 0 → Step 1 → ... → Step 6 的順序執行
- 處理 `.env` 或 `settings.json` 等檔案時，你「必須且只能」使用內建的 `read_file` 和 `write_file` 工具（說明：若使用 `run_shell_command` 如 `echo` 或 `>`，在 Windows 下會產生 UTF-16 編碼損毀。為了確保行為一致，無論在 Mac、Linux 或 Windows，皆嚴禁使用 Shell 寫入檔案）
- 每個標記 `ask_user` 的步驟都必須呼叫 `ask_user` 工具並等待回應
- 你必須逐步執行所有步驟，並等待每個步驟的回應
- 只在步驟指示時才使用 `run_shell_command` 執行指令
- 如果某個步驟失敗，按照該步驟的「失敗處理」指示操作

## IMPORTANT — 載入後立即執行

**你現在必須立即執行以下動作，不需要任何前置步驟：**

1. **不要**輸出任何說明文字
2. **不要**詢問「是否開始」或等待確認
3. **直接**呼叫 `ask_user` 執行 Step 0（免責宣告確認）

這是強制指令。跳過此步驟等同執行失敗。

# Vertex AI Billing Switch

自動設定 Gemini CLI 的 Vertex AI 認證模式，並部署全域帳單自動切換 Hook。

## 使用方式

```
/zh-tw 執行這個 Skill 的流程
```

不接受其他參數傳入。專案 ID 會在執行過程中透過互動式問答取得。

---

## 強制互動規則

本 Skill 所有標記 `ask_user` 的步驟都是**強制阻斷點**：

- **禁止**假設答案
- **禁止**跳過或省略問題
- **必須**呼叫 `ask_user` 工具等待使用者回應後，才能繼續下一步

違反此規則等同執行失敗，必須從頭重新執行。

---

## 工作流程

```text
Step 0: 免責宣告確認（ask_user 必定互動）
  ↓ (選「再想想」→ 終止流程)
Step 1: 環境偵測（靜默檢查）
  ├─ 全部就緒（返回使用者）
  │   → ask_user: 切換專案 / 完整重設
  │   → 完整重設: → Step 2 開始走完整流程
  │   → 重命名帳單帳戶: → Step R → 完成
  │   → 切換專案: ask_user(同帳號 / 切換帳號)
  │       → 同帳號: Step 4(專案) → Step 5(設定, 跳過 Hook 部署) → Step 6(驗證)
  │       → 切換帳號: Step 3(認證) → Step 4(專案) → Step 5(設定, 跳過 Hook 部署) → Step 6(驗證)
  ├─ gcloud 就緒，Hook 未部署（check1 ✓ + check2 ✓ + check3 ✗）
  │   → ask_user: 僅部署 Hook / 完整設定
  │   → 僅部署 Hook: → Step H → Step 6（hook_only 模式）
  │   → 完整設定: → Step 2 開始走完整流程
  └─ gcloud 未安裝或未認證（首次使用者）
      → Step 2: gcloud CLI 安裝
      → Step 3: GCP 認證登入
      → Step 4: 取得/建立 GCP 專案
      → Step 5: GCP 專案設定 + Gemini CLI 部署
      → Step 6: 驗證 + 完成提醒
```

### 路線摘要

| 使用者類型 | 執行步驟 |
|-----------|---------|
| 首次使用者 | 0 → 1 → 2 → 3 → 4 → 5 → 6 |
| 返回使用者 — 完整重設 | 0 → 1 → 2 → 3 → 4 → 5 → 6 |
| 返回使用者 — 同帳號換專案 | 0 → 1 → 4 → 5（跳過 Hook 部署）→ 6 |
| 返回使用者 — 切換帳號 | 0 → 1 → 3 → 4 → 5（跳過 Hook 部署）→ 6 |
| 返回使用者 — 僅部署 Hook（已設定 Vertex AI） | 0 → 1 → H → 6 |
| 返回使用者 — 重命名帳單帳戶 | 0 → 1 → R → 完成 |

---

## Step 0: 免責宣告確認

> **STOP — 強制互動點**
> 此步驟為技能啟動後的第一步，必定觸發，不可跳過。

**STOP — 必須呼叫 ask_user，禁止假設答案，等待回應後才能繼續。**

使用 `ask_user` 詢問：

```json
{"questions":[{"question":"請確認您稍後登入的 Google Cloud 帳號沒有綁定任何信用卡等付款方式，如有綁定造成扣款，本工具不負責。","header":"免責宣告","type":"choice","options":[{"label":"我知道","description":"我確認帳號未綁定付款方式，繼續執行"},{"label":"再想想","description":"我需要先確認，暫時中止流程"}]}]}
```

### 處理邏輯

**選「我知道」** → 繼續執行 Step 1

**選「再想想」** → 顯示以下訊息後立即終止流程：

> 已中止。請確認你的 Google Cloud 帳號未綁定任何付款方式後，重新執行 `/zh-tw 執行這個 Skill 的流程`。

---

## Step 1: 環境偵測

此步驟靜默執行，除非所有檢查通過才會觸發使用者互動。

### 檢查項目

使用 `run_shell_command` 依序執行以下檢查：

**1. 檢查 gcloud 是否已安裝：**

```bash
gcloud --version
```

**2. 檢查 gcloud 是否已認證（僅在檢查 1 通過時執行）：**

```bash
gcloud auth list --filter=status:ACTIVE --format="value(account)"
```

**3. 檢查 Hook 是否已部署（僅在檢查 1、2 皆通過時執行）：**

先取得使用者家目錄：

```bash
node -e "process.stdout.write(require('os').homedir())"
```

再檢查 Hook 檔案：

```bash
test -f {home_dir}/.gemini/hooks/vertex-ai-billing-switch-hook.mjs && echo "OK" || echo "MISSING"
```

### 判斷邏輯

**三項全部通過（返回使用者）** →

**STOP — 必須呼叫 ask_user，禁止假設答案，等待回應後才能繼續。**

使用 `ask_user`：

```json
{"questions":[{"question":"偵測到環境已設定完成。你想要做什麼？","header":"操作模式","type":"choice","options":[{"label":"切換專案/帳號","description":"更換 GCP 專案或 Google 帳號（跳過安裝步驟）"},{"label":"重命名帳單帳戶","description":"重命名帳單帳戶以便識別（例如 Trial_Exp_20260501）"},{"label":"完整重新設定","description":"從頭執行完整設定流程"}]}]}
```

- 選「完整重新設定」→ 繼續 **Step 2**（走完整流程）
- 選「重命名帳單帳戶」→ 進入 **Step R**
- 選「切換專案/帳號」→ 設定 `quick_switch = true`，接著：

**STOP — 必須呼叫 ask_user，禁止假設答案，等待回應後才能繼續。**

使用 `ask_user`：

```json
{"questions":[{"question":"你要切換到不同的 Google 帳號，還是只更換同帳號下的 GCP 專案？","header":"帳號切換","type":"choice","options":[{"label":"同帳號換專案","description":"保持目前的 Google 登入，只更換 GCP 專案"},{"label":"切換 Google 帳號","description":"登入不同的 Google 帳號（會開啟瀏覽器）"}]}]}
```

  - **選「同帳號換專案」** → 跳到 **Step 4**（不需要重新認證）
  - **選「切換 Google 帳號」** → 繼續 **Step 3**

**檢查 1、2 通過，檢查 3 未通過（gcloud 就緒，Hook 未部署）** →

**STOP — 必須呼叫 ask_user，禁止假設答案，等待回應後才能繼續。**

使用 `ask_user`：

```json
{"questions":[{"question":"已偵測到 gcloud 已安裝且已認證，但帳單切換 Hook 尚未部署。你想要做什麼？","header":"操作模式","type":"choice","options":[{"label":"僅部署 Hook","description":"使用現有 Vertex AI 設定，只部署帳單切換 Hook"},{"label":"完整重新設定","description":"從頭執行完整設定流程"}]}]}
```

- 選「僅部署 Hook」→ 設定 `hook_only = true`，進入 **Step H**
- 選「完整重新設定」→ 繼續 **Step 2**（走完整流程）

**檢查 1 或檢查 2 未通過（首次使用者）** → 直接進入 **Step 2**

---

## Step H：僅部署 Hook

> 從 Step 1 的 `hook_only = true` 分支進入。
> 使用者已設定好 Vertex AI，只需部署帳單切換 Hook。

### H-1：初始化變數

使用 `run_shell_command` 取得家目錄：

```bash
node -e "process.stdout.write(require('os').homedir())"
```

儲存為 `{home_dir}`，並設定：
- `{gcloud_cmd}` = `gcloud`（Step 1 已驗證可用）
- `{skill_dir}` 根據安裝方式：
  - 透過 Gemini CLI 安裝：`{home_dir}/.gemini/extensions/VertexAiBillingSwitchSkill/skills/zh-tw`
  - 手動安裝：`{home_dir}/.gemini/skills/zh-tw`

使用 `run_shell_command` 讀取目前 GCP 專案（僅供顯示與選項用）：

```bash
gcloud config get-value project
```

儲存為 `{detected_project}`（若為空或 `(unset)` 則標示為「未設定」）。

---

### H-2：選擇 GCP 專案

**STOP — 必須呼叫 ask_user，禁止假設答案，等待回應後才能繼續。**

> 若 `{detected_project}` 為「未設定」，在呼叫 ask_user 之前先告知使用者：「gcloud 尚未設定預設專案，建議選擇『指定其他專案』或『建立新專案』。」

使用 `ask_user`：

```json
{"questions":[{"question":"帳單切換 Hook 需要知道要監控哪個 GCP 專案。你想要使用哪個專案？","header":"GCP 專案","type":"choice","options":[{"label":"使用目前專案","description":"沿用 gcloud 目前設定的專案：{detected_project}"},{"label":"指定其他專案","description":"輸入現有的 GCP 專案 ID"},{"label":"建立新專案","description":"由 Skill 自動建立新的 GCP 專案"}]}]}
```

#### 選「使用目前專案」

設定 `{project_id}` = `{detected_project}`，直接進入 **H-4（確認部署）**。

#### 選「指定其他專案」

**STOP — 必須呼叫 ask_user，禁止假設答案，等待回應後才能繼續。**

使用 `ask_user`：

```json
{"questions":[{"question":"請輸入 GCP 專案 ID（通常以 gen-lang-client- 開頭）：","header":"專案 ID","type":"text","placeholder":"gen-lang-client-0123456789"}]}
```

驗證：若為空或明顯無效則重新詢問。儲存為 `{project_id}`，進入 **H-3（套用新專案設定）**。

#### 選「建立新專案」

**請讀取 `references/create-project.md`，執行完整的自動建立子流程（4-A 偵測帳單帳戶、4-B 輸入專案名稱、4-C 建立、4-D 連結帳單、4-E 確認）。**

取得 `{project_id}` 後，進入 **H-3（套用新專案設定）**。

---

### H-3：套用新專案設定（僅「指定其他專案」或「建立新專案」時執行）

先告知使用者：

> 正在將 GCP 專案切換為 `{project_id}`…

依序使用 `run_shell_command` 執行：

**更新 gcloud 預設專案：**
```bash
gcloud config set project {project_id}
```

**啟用 Vertex AI API：**
```bash
gcloud services enable aiplatform.googleapis.com --project={project_id}
```

**更新 `~/.gemini/.env`：**

1. 使用 `read_file` 讀取 `{home_dir}/.gemini/.env`（不存在則從空內容開始）
2. 移除既有的 `GOOGLE_CLOUD_PROJECT=` 和 `GOOGLE_CLOUD_LOCATION=` 行
3. 追加：
   ```
   GOOGLE_CLOUD_PROJECT={project_id}
   GOOGLE_CLOUD_LOCATION=global
   ```
4. 使用 `write_file` 寫回

完成後進入 **H-4（確認部署）**。

---

### H-4：確認部署

**STOP — 必須呼叫 ask_user，禁止假設答案，等待回應後才能繼續。**

使用 `ask_user`：

```json
{"questions":[{"question":"即將執行以下動作：1. 複製帳單切換 Hook 到 ~/.gemini/hooks/。2. 更新 settings.json 並啟用 Hook。3. 認證模式設為 Vertex AI。監控專案：{project_id}","header":"確認部署","type":"yesno"}]}
```

- **Yes** → 繼續執行 H-5
- **No** → 顯示「已取消。如需重新執行，請再次觸發本 Skill。」後終止流程

---

### H-5：部署 Hook

**請讀取 `references/deploy-hook.md` 並執行所有部署步驟（目錄建立、Hook 腳本複製、settings.json 非破壞性合併）。**

> 注意：忽略該文件開頭「`quick_switch = false` 時才執行」的前置條件，在 `hook_only = true` 路線中直接執行所有步驟。

完成後進入 **Step 6**（`hook_only = true`）。

---

## Step R：重命名帳單帳戶

> 從 Step 1 選擇「重命名帳單帳戶」進入。
> 此為獨立流程，不影響其他步驟。

**請讀取 `references/rename-accounts.md` 並執行完整的重命名流程（R-1 列出帳戶、R-2 選擇命名策略、R-3 收集到期日、R-4 確認、R-5 執行重命名）。**

完成或取消後，流程結束。顯示：

> 如需執行其他操作，請重新觸發此 Skill。

---

## Step 2: 環境前置檢查

### 初始化變數

使用 `run_shell_command` 取得家目錄：

```bash
node -e "process.stdout.write(require('os').homedir())"
```

儲存為 `{home_dir}`，並推導：`{skill_dir}` = `{home_dir}/.gemini/skills/zh-tw`

同時設定預設值：`{gcloud_cmd}` = `gcloud`（若 Windows 安裝後 PATH 未更新，此值將在 Step 2 末尾被覆寫為完整路徑）

### 檢查 gcloud CLI

> **優化提示：** 若 Step 1 已確認 gcloud 未安裝（檢查 1 失敗），跳過此指令，直接進入下方的條件互動點。

使用 `run_shell_command` 執行：

```bash
gcloud --version
```

### 判斷邏輯

- **指令成功**（gcloud 已安裝）→ 直接進入 Step 3
- **指令失敗**（gcloud 未安裝）→ 觸發互動點

### 條件觸發互動點（僅在 gcloud 未安裝時）

**STOP — 必須呼叫 ask_user，禁止假設答案，等待回應後才能繼續。**

使用 `ask_user` 詢問：

```json
{"questions":[{"question":"系統上尚未安裝 Google Cloud CLI (gcloud)，這是連接 Vertex AI 的必要工具。要如何處理？","header":"gcloud 安裝","type":"choice","options":[{"label":"自動安裝","description":"自動下載安裝 gcloud CLI（約 2-3 分鐘）"},{"label":"我自己安裝","description":"前往官網手動安裝後再回來"}]}]}
```

### 處理邏輯

**選「我自己安裝」** → 顯示以下訊息後結束流程：

> 請前往 https://cloud.google.com/sdk/docs/install 安裝 Google Cloud CLI。
> 安裝完成後，請重新執行 `/zh-tw 執行這個 Skill 的流程`。

**選「自動安裝」** → 先偵測作業系統平台：

使用 `run_shell_command`：

```bash
node -e "process.stdout.write(process.platform)"
```

根據平台結果分流：

---

#### 若為 `win32`（Windows）

**STOP — 必須呼叫 ask_user，禁止假設答案，等待回應後才能繼續。**

使用 `ask_user` 詢問：

```json
{"questions":[{"question":"Windows 上有兩種安裝 gcloud CLI 的方式，你要用哪一種？","header":"安裝方式","type":"choice","options":[{"label":"winget 安裝","description":"執行 winget install -e --id Google.CloudSDK"},{"label":"Google 官方安裝","description":"執行 PowerShell 下載官方安裝程式"}]}]}
```

**請讀取 `references/install-gcloud.md` § Windows 取得使用者選擇後的詳細安裝與驗證指令。**

---

#### 若為 `darwin`（macOS）

**STOP — 必須呼叫 ask_user，禁止假設答案，等待回應後才能繼續。**

使用 `ask_user` 詢問：

```json
{"questions":[{"question":"macOS 上有兩種安裝 gcloud CLI 的方式，你要用哪一種？","header":"安裝方式","type":"choice","options":[{"label":"Homebrew 安裝","description":"執行 brew install --cask gcloud-cli"},{"label":"Google 官方安裝","description":"執行 curl https://sdk.cloud.google.com | bash"}]}]}
```

**請讀取 `references/install-gcloud.md` § macOS 取得使用者選擇後的詳細安裝與驗證指令。**

---

#### 若為其他平台（Linux）

**請讀取 `references/install-gcloud.md` § Linux 取得安裝與驗證指令。**

---

## Step 3: GCP 認證登入

不論是首次使用者還是返回使用者（切換帳號），都必須執行此步驟。

### 執行動作

先告知使用者：

> 接下來會開啟瀏覽器進行 Google Cloud 帳號登入，請在瀏覽器中完成登入流程。

然後使用 `run_shell_command`：

若 `{gcloud_cmd}` = `gcloud`（PATH 正常）：
```bash
gcloud auth login
```

若 `{gcloud_cmd}` 為完整路徑（Windows 安裝後 PATH 未更新）：
```bash
powershell -Command "& '{gcloud_cmd}' auth login"
```

- **僅執行** `gcloud auth login`
- **不做** `set project`、不啟用 API、不做 ADC（此時尚不知道專案 ID）

### 失敗處理

- **登入失敗 — 瀏覽器未開啟**：若沒有瀏覽器視窗彈出，使用 `--no-launch-browser` 重試：

  若 `{gcloud_cmd}` = `gcloud`：
  ```bash
  gcloud auth login --no-launch-browser
  ```
  若 `{gcloud_cmd}` 為完整路徑：
  ```bash
  powershell -Command "& '{gcloud_cmd}' auth login --no-launch-browser"
  ```
  gcloud 會在終端機顯示一個 URL，請使用者複製到瀏覽器完成登入，再將驗證碼貼回終端機。

- **其他登入失敗**：使用者可能取消了瀏覽器登入，建議重新執行此 Skill。

---

## Step 4: 取得/建立 GCP 專案

> **STOP — 強制互動點**
> 此步驟為必要步驟，必定觸發，不可跳過。
> 專案 ID 一律透過 `ask_user` 取得，不接受參數傳入。

### 第一輪：確認是否有專案

**STOP — 必須呼叫 ask_user，禁止假設答案，等待回應後才能繼續。**

使用 `ask_user` 詢問：

```json
{"questions":[{"question":"你是否已經有 Google AI Studio 的 GCP 專案？","header":"GCP 專案","type":"yesno"}]}
```

### 處理邏輯

**回答「是」** → 進入第二輪

**回答「否」** → 進入第二輪替代流程

### 第二輪：輸入專案 ID

**STOP — 必須呼叫 ask_user，禁止假設答案，等待回應後才能繼續。**

使用 `ask_user` 詢問：

```json
{"questions":[{"question":"請輸入你的 GCP 專案 ID（使用 AI Studio 建立的專案通常以 gen-lang-client- 開頭）⚠️ 免責聲明：請確定這個 GCP 帳號內所有的帳單帳戶都沒有綁定信用卡，如有繳費情況概不負責。","header":"專案 ID","type":"text","placeholder":"gen-lang-client-0123456789"}]}
```

### 驗證

- 檢查使用者輸入是否為空
- 若為空或明顯無效，重新詢問
- 記錄 `{project_id}` 供後續步驟使用
- 進入 **Step 5**

### 第二輪替代流程：選擇建立方式

**STOP — 必須呼叫 ask_user，禁止假設答案，等待回應後才能繼續。**

使用 `ask_user` 詢問：

```json
{"questions":[{"question":"你想要如何建立 GCP 專案？","header":"建立方式","type":"choice","options":[{"label":"自動建立（gcloud）","description":"使用 gcloud CLI 自動建立新 GCP 專案，不需離開終端機"},{"label":"手動建立（AI Studio）","description":"前往 AI Studio 手動建立，完成後再回來"}]}]}
```

#### 選「手動建立（AI Studio）」→ 顯示以下建立引導後結束流程：

> **建立 GCP 專案步驟：**
>
> 1. 前往 [Google AI Studio](https://aistudio.google.com) 登入你的 Google 帳號
> 2. 點擊左下方的 Get API Key
> 3. 在 API Keys 頁面，點擊右上方的 Create API key 依照設定建立 Key
> 4. 在 API Keys 頁面，找到 **Project** 欄位，複製開頭為 `gen-lang-client-` 的 GCP 專案 ID
> 5. 在 API Keys 頁面，找到 **Billing Tier** 欄位，設定活動的 **$5 美元**抵免額方案
> 6. 完成後，請重新執行 `/zh-tw 執行這個 Skill 的流程`

#### 選「自動建立（gcloud）」→ 執行以下子流程：

**4-A: 偵測可用帳單帳戶**

使用 `run_shell_command`：

若 `{gcloud_cmd}` = `gcloud`：
```bash
gcloud billing accounts list --format="json"
```

若 `{gcloud_cmd}` 為完整路徑：
```bash
powershell -Command "& '{gcloud_cmd}' billing accounts list --format=json"
```

篩選 `open === true` 的帳戶。

- **無可用帳戶** → 顯示以下訊息後結束流程：

  > 未偵測到任何可用的帳單帳戶。請先前往 [Google AI Studio](https://aistudio.google.com) 設定 **$5 美元**抵免額方案後，重新執行 `/zh-tw 執行這個 Skill 的流程`。

- **有一個可用帳戶** → 記錄該帳戶，繼續 4-B

- **有多個可用帳戶** →

  **STOP — 必須呼叫 ask_user，禁止假設答案，等待回應後才能繼續。**

  使用 `ask_user` 讓使用者選擇（動態產生 choice options，最多取前 4 個帳戶）：

  ```json
{"questions":[{"question":"偵測到多個帳單帳戶，請選擇要連結到新專案的帳戶：","header":"帳單帳戶","type":"choice","options":[{"label":"{displayName1}","description":"帳戶 ID: {accountId1}"},{"label":"{displayName2}","description":"帳戶 ID: {accountId2}"}]}]}
```

**4-B: 輸入專案 ID 基礎名稱**

**STOP — 必須呼叫 ask_user，禁止假設答案，等待回應後才能繼續。**

使用 `ask_user`：

```json
{"questions":[{"question":"請輸入偏好的 GCP 專案 ID（小寫字母、數字、連字號，6-30 字元）。系統會自動加上隨機後綴確保唯一性。留空則使用預設名稱 'gemini-vertex'。","header":"專案 ID","type":"text","placeholder":"gemini-vertex"}]}
```

**請讀取 `references/create-project.md` 取得專案 ID 產生邏輯、專案建立（4-C）、帳單帳戶連結（4-D）與確認訊息（4-E）。**

記錄 `{project_id}` 供後續步驟使用。進入 **Step 5**。

---

## Step 5: 失敗處理預警（關於 ADC 登入）

在接下來的 Step 5 中，會讀取 `references/config-and-verify.md` 執行 ADC 登入。
若發生 **ADC 登入失敗 — 瀏覽器未開啟** 的情況，請「必須且只能」使用 `ask_user` 工具來引導使用者手動執行指令。

**STOP — 必須呼叫 ask_user，禁止假設答案，等待回應後才能繼續。**
使用 `ask_user`：

```json
{"questions":[{"question":"瀏覽器似乎無法自動開啟。為避免網址複製時混入 `|` 分隔線，請開啟一個「全新的終端機視窗/分頁」（請保持 Gemini CLI 執行不要關閉），手動複製並執行以下指令：\n\n{cmd_string}\n\n完成登入後，請點選下方確認繼續。","header":"手動 ADC 登入","type":"choice","options":[{"label":"我已完成登入","description":"繼續下一步"}]}]}
```
*提示： `{cmd_string}` 為 `gcloud auth application-default login --no-launch-browser --project={project_id}`（若有路徑則加上 `& "..."`）。*

---

## Step 5 & Step 6: 專案設定與驗證

**請讀取 `references/config-and-verify.md` 並依序執行其中的設定與驗證指令。**
