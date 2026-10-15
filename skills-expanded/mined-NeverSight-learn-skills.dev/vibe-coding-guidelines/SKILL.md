---
name: vibe-coding-guidelines
description: 在非程式開發者要用 vibe coding 與 coding agent 協作時使用。常見觸發像「幫我整理開發準則」「定義交付邊界」「規劃驗證方式」。輸出需求表達、邊界與風險控管準則；不直接取代實作。
version: 2026.3.31
homepage: https://github.com/AllanYiin/skills/tree/main/skills/vibe-coding-guidelines
license: MIT
metadata: {"author":"Allan Yiin","language":"zh-TW","category":"engineering","short-description":"非程式開發者進行 vibe coding 時給 coding agent 的開發準則"}
---

# Vibe Coding Guidelines

## Purpose

把「不懂程式的使用者」的需求，交付成一個可解壓縮後直接點一下就能啟動的專案：
- Windows：雙擊 `run_app.bat`（它是 `scripts/project_launcher.py` 生成/維護的 Windows wrapper，不是另一份可自由發明的新主入口）
- macOS：雙擊 `run_app.command`（若無法執行，請先 `chmod +x run_app.command`；若首次被系統阻擋，依提示到「系統設定 > 隱私權與安全性」允許後再執行）
- Linux：雙擊或執行 `run_app.sh`（若無法執行，請先 `chmod +x run_app.sh`）

同時提供繁體中文介面、狀態持久化、友善錯誤訊息與 logs；若使用者提供 SVG / mockup / 畫面規格，介面方向必須尊重原規格，不能擅自改風格。若是工作台型 UI，嚴格禁止 stacked UI / stacked cards 疊首頁；必須先定義唯一主任務，並讓該功能盡量佔據最大、最中央、最先被看的畫面區域。任何工作台或流程頁都要把 task model、state model、資訊分類、content audit 與 visibility plan 寫進規格與 `AGENTS.md`，不能只留一句「請簡潔」。

## Scope

### In scope

- 以 Windows / Linux / macOS 為目標的 Python（優先）或必要時的 Python+Node 專案交付
- 一鍵啟動（自建 venv、自裝 requirements、自動開瀏覽器/視窗）
- 專案規格→開發計畫→`todo.md` 檢核→逐檔寫入→測試→打包 ZIP
- 各平台坑位（編碼、路徑、port、權限、防毒/權限政策）避雷；Windows 特例會額外標註
- OpenAI Responses 串流對話、Whisper STT、Nano Banana 2（Gemini 3.1 Flash Image）圖像（T2I/I2I）整合規範

### Out of scope

- 需要使用者自行開 cmd/PowerShell 手動輸入指令才能完成的交付
- 需要 WSL/Linux 才能執行的方案
- 需要使用者自行調整系統環境變數才能運作的方案（除非已提供 UI 內設定流程）

## Primary use cases

1) **交付可一鍵啟動的 Windows 應用（ZIP）**
- Trigger examples: 「幫我做一個 Windows 工具/小程式」「我要下載解壓後直接點 run 就能跑」「打包成 ZIP 給我」
- Expected result: ZIP 內含 `run_app.bat`、`requirements.txt`、`README.md`、`todo.md`；解壓後雙擊可啟動；錯誤寫入 `logs/` 且 UI 以繁中提示。

2) **既有專案的最小修改（不重構）**
- Trigger examples: 「這個專案在 Windows 跑不起來」「中文亂碼」「port 被佔用」「缺套件/requirements 不對」
- Expected result: 保持原 UI/介面/API 不變，做最小改動修好；提供被修改檔案的完整內容；再打包 ZIP。

3) **加入 AI 功能且強制串流**
- Trigger examples: 「加 ChatGPT 串流」「加語音轉文字」「加生圖/修圖」「用 OpenAI Responses API」
- Expected result: 所有 LLM 文字輸出皆 streaming；金鑰不硬編碼；model 由 env/config 管；STT/T2I/I2I 依規範接入。

## Workflow overview

最新流程以這個順序為準：

1) 先釐清/補齊規格，並把需求整理到 `specs/requirements.md`；至少寫清楚功能、輸入輸出、UI、資料保存、錯誤處理、打包方式，以及使用情境判定需要的四個軸。
2) 產出並寫入 `todo.md`，後續以它作為唯一工作清單；若需求變動，先更新 `specs/requirements.md`，再更新 `todo.md`。
3) 先讀 `references/usage_scene_decision_tree.md`，判定 `usage_scene` 與 `project_profile`；資訊不足時才反問最少問題，並把結果寫入根目錄 `project.config.json`。
4) 依使用情境先生成根目錄 `AGENTS.md`，組成固定為「核心規則 + 使用情境規則 + 技術補充規則 + 專案特例」。
5) 再讀 `references/apsm_decision_tree.md` 做 APSM 技術選型，決定 `archetype` / `architecture` / `frontend` / `backend` / `apsm_version`，並補完 `project.config.json`。
6) 根據使用情境與 APSM 一起選目錄模板並建立骨架，至少補齊固定檔案、`README.md`、`specs/requirements.md`、`todo.md`、`.env.example`、`scripts/project_launcher.py`、`scripts/apsm_validate.py` 與 `.venv/`。
7) 立刻執行 `python scripts/apsm_validate.py --project <target-project>`；先修完結構 errors，再繼續功能實作。
8) 逐檔完成實作與必要測試，避免 placeholder；若需求包含 AI，再依規範整合 Responses 串流、Whisper、Nano Banana 2，並確保金鑰與設定管理合規。
9) 在目標專案根目錄執行 `python scripts/project_launcher.py`，完成依賴驗證、launcher 生成、runtime metadata 建立與常見啟動修正；之後至少做一次本機啟動驗證，並再跑 `python scripts/apsm_validate.py --project <target-project> --strict`。
10) 確認 launcher、logs、runtime metadata 與錯誤訊息都符合規範後，壓縮成 ZIP 交付。

## Routing boundaries

- Neighboring skills / workflows:
  - `spec-organizer`：需求還沒整理成可開發規格。
  - `frontend-design`：重點是前端視覺與互動，而不是整個可執行專案交付規範。
  - `technical-documentation-writer`：只需要文件，不需要交付可啟動專案。
- Negative triggers:
  - 「幫我只做一段文案」
  - 「只討論概念，不要產出專案」
  - 「只改一個元件顏色，不做整體交付」
- Handoff rule: 若任務不涉及可執行專案交付、啟動器、打包或新手協作規範，就不應啟動這個 skill。

## Language coverage

- Primary language(s): 繁體中文、英文。
- Mixed-language trigger phrases: vibe coding、run_app.bat、ZIP delivery、project launcher、streaming chat、Windows tool。
- Locale-specific wording risks: 使用者說「做個小工具」常隱含 Windows 一鍵啟動與零指令體驗，需要主動寫進規格。

## Success criteria

- `project.config.json` 除了 APSM 欄位外，還要包含 `usage_scene` 與 `project_profile`。
- 根目錄必須存在 `AGENTS.md`，而且內容要對齊使用情境、技術選型與專案特例。
- 預設場景必須是 `scene_b_shared_tool`，只有明確符合個人黑盒工具時才降到場景 A。

- 使用者不需手動安裝依賴、不需手動輸入指令；只需解壓縮→點一下啟動（Windows：`run_app.bat`／macOS：`run_app.command`／Linux：`run_app.sh`）。
- 跨平台可啟動：ZIP 內同時包含 `run_app.bat` / `run_app.command` / `run_app.sh`，且三者皆可在對應平台啟動。
- `run_app.bat` / `run_app.command` / `run_app.sh` 都是由 `scripts/project_launcher.py`（必要時搭配 `scripts/project_launcher_posix.py`）生成或維護的 launcher wrapper；agent 應沿用或修改這條生成鏈，不得另外自創平行的 `run_app.bat` 主流程。
- 編碼穩定：`.py/.json/.md` 為 UTF-8（建議無 BOM）；`run_app.bat` 預設 ASCII-only，不以 ANSI/CP950 為策略，也不預設加入 `chcp 65001`；`run_app.command` / `run_app.sh` 使用 UTF-8 LF。
- 重要流程（I/O、網路、LLM）不閃退：有全域 try/except、UI 友善錯誤、`logs/` 有 stack trace。
- port 衝突不可假裝已自動處理；若尚未實作完整動態 port 協調，至少要清楚提示衝突原因與下一步。若要支援動態 port，必須以服務實際綁定後回報的 port 為單一事實來源，並同步更新 URL / API base / log / 啟動器狀態。
- AI 回應必為 streaming；金鑰不出現在 logs。
- 在規劃目錄前已完成 APSM 選型，且根目錄有可機器判讀的 `project.config.json`（含 `apsm_version` 與 `archetype`）；agent 不需要靠猜測目錄來反推架構。
- `python scripts/apsm_validate.py --project <target-project> --strict` 可通過，代表 `project.config.json`、目錄結構、必要啟動檔與 `.env` 關鍵欄位一致。
- 已執行過 `project_launcher.py` 的專案，必須另外具備 `.runtime/ports.json`、`.runtime/launcher_state.json` 與 `logs/launcher.log` 等 machine-readable runtime metadata。
- 若有 viewer / editor / diff / preview 類工作台，必須只聚焦一個唯一主任務；主任務必須佔據最大、最中央、最先被看的區域，次要資訊退到側欄、drawer、tab 或折疊層，不得做成 stacked UI / stacked cards 首頁。
- 若有 viewer / editor / diff / preview 類工作台，`specs/requirements.md` 與 `AGENTS.md` 必須都寫出：primary task、task model、state model、資訊角色分類、首屏主要群組上限與 disclosure 規則。
- 若有 viewer / editor / diff / preview 類工作台，`specs/requirements.md` 與 `AGENTS.md` 必須都寫出 content audit：`must-see-now`、`next-step-only`、`error-only`、`on-demand-reference`、`keep-off-first-viewport`。
- 每個延後揭露的區塊都要寫出：為何現在先隱藏、什麼事件會讓它出現、會放在 inline / accordion / drawer / modal / tab 哪一種容器。
- 工作台首頁預設只允許 2-3 個主要視覺群組，且只有 1 個主 CTA；`reference` 類資訊不得長期佔據主舞台。
- 空狀態不可只留白；必須清楚說明缺少什麼、為何沒有內容、下一步要做什麼。

## Instructions

### Step 0: Inputs 期望

- 若使用者有提供規格：直接進入 Step 1。
- 若規格不足：自行補齊並以「白話文確認」列出：核心功能、限制、UI 版型（只有在未指定時才預設左右分欄；若規格已指定結構，不得擅改）、資料保存方式、輸出檔案（ZIP）。
- 若屬工作台、dashboard、viewer、editor、review tool 或 setup flow，額外補齊：唯一主任務、task model、state model、資訊分類、visibility plan。
- 若屬工作台、dashboard、viewer、editor、review tool 或 setup flow，先讀 `references/ui-workbench-guardrails.md`，再把相應約束寫進 `specs/requirements.md` 與 `AGENTS.md`。
- 若屬工作台、dashboard、viewer、editor、review tool 或 setup flow，先做 content audit，把需求分成 `must-see-now`、`next-step-only`、`error-only`、`on-demand-reference`、`keep-off-first-viewport`，再決定首屏配置。

### Step 1: 產生並維護 todo.md 與 specs/requirements.md

- 在 `specs/requirements.md` 內另外整理四個判定軸，並直接對應到 `project_profile` 四欄：使用者是誰（`user_type`）、使用週期（`usage_duration`）、修改頻率（`change_frequency`）、壞掉代價（`failure_cost`）。
- 若描述已足夠，直接推定；若資訊不足且會影響場景分類，再反問最少問題。

- 把所有子任務寫成 checklist。
- 把當前確認過的規格整理到根目錄 `specs/requirements.md`；至少包含：功能範圍、輸入輸出、UI/互動、資料保存、外部依賴、驗收條件。
- 若有工作台型 UI（viewer、editor、diff、preview、審閱台），規格內必須額外寫明：唯一主任務、主畫面責任、task model、state model、各資訊區塊的角色（`action-critical`、`decision-supporting`、`status-feedback`、`reference`、`exception-handling`、`audit/history`）、次要資訊應退到哪裡、首屏最多 2-3 個主要視覺群組、空狀態的下一步指引；嚴格禁止 stacked UI / stacked cards 疊首頁。
- 若有工作台型 UI（viewer、editor、diff、preview、審閱台），規格內還必須寫出 content audit 結果：哪些資訊現在必須看、哪些是下一步才需要、哪些只有出錯才需要、哪些只是可查參考、哪些不該進首屏。
- 每個延後揭露區塊都要補 `hidden_now_because`、`reveal_trigger`、`container` 三欄；寫不出這三欄就代表 reveal / hide 決策仍然不夠清楚。
- 若首屏已出現 4 個以上大群組，或任務有明確先後順序且後一步高度依賴前一步輸出，優先改成 tabs / wizard / step navigation，而不是繼續加卡片。
- 若使用者後續補需求，先更新 `specs/requirements.md`，再更新 `todo.md`；不要讓規格只散落在對話裡。
- 後續每完成一項就打勾；任何新需求都先更新 todo.md。

### Step 2: 使用情境判定與 AGENTS.md 組裝

- 先讀 `references/usage_scene_decision_tree.md`，判斷 `usage_scene`，不要直接從技術棧反推場景。
- `usage_scene` 只能是：
  - `scene_a_personal_blackbox`
  - `scene_b_shared_tool`
  - `scene_c_internal_tool`
  - `scene_d_engineer_maintained`
- `project_profile` 至少包含：
  - `user_type`
  - `usage_duration`
  - `change_frequency`
  - `failure_cost`
- 上述四欄就是 Step 1 提到的四個判定軸；欄位值域與判定規則以 `references/usage_scene_decision_tree.md` 為準。
- 資訊不足時，預設 `scene_b_shared_tool`，不要預設 A。
- 把 `usage_scene` 與 `project_profile` 寫進根目錄 `project.config.json`。
- 在 APSM 技術選型之前，先產生根目錄 `AGENTS.md`。
- `AGENTS.md` 的組成固定為：
  - 核心規則
  - 使用情境規則
  - 技術補充規則
  - 專案特例
- `AGENTS.md` 至少要寫出：專案定位、最高原則、目錄與檔案規範、實作規範、UI / UX 規範、修改規範、測試與打包規範、專案特例。
- 若專案有主工作台，`AGENTS.md` 的 UI / UX 規範必須額外包含：
  - 先定義唯一主任務，再畫版面；盡量一次只聚焦一個功能
  - 先寫 task model、state model、資訊分類與 visibility plan，再允許切版
  - 主畫面只能讓主任務佔據中央、首要視線與最大化畫面區域
  - 次要資訊退到側欄、drawer、tab 或折疊層；`reference` 類資訊預設 on-demand
  - `exception-handling` 類資訊只在對應 state 顯示
  - 首屏最多 2-3 個主要視覺群組，且只能有 1 個主 CTA
  - 先做 content audit：`must-see-now`、`next-step-only`、`error-only`、`on-demand-reference`、`keep-off-first-viewport`
  - 每個 deferred block 都要寫出隱藏理由、揭露事件與容器策略
  - 若同時出現 4 個以上大區塊，或流程有明顯先後依賴，就改用 tabs / wizard / step navigation
  - 嚴格禁止 stacked UI / stacked cards 首頁
  - 空狀態要交代缺少內容、原因與下一步

### Step 3: APSM 技術選型與專案類型宣告

- APSM 是技術補充層，不是主分類；主分類先看使用情境。
- `project.config.json` 除了 APSM 欄位外，還要保留 `usage_scene` 與 `project_profile`，讓場景規則、技術規則與 validator 對齊。

- APSM（AI Project Structure Model）是這個 skill 的目錄規劃中樞。先定義 machine-readable config，再映射到目錄模板；不要跳過這一步。
- 選型時先走 `references/apsm_decision_tree.md`；決策樹只負責篩選，不能取代完整模板矩陣。
- APSM 是兩層模型：`archetype` 負責 AI/新手入口分類，`architecture/frontend/backend` 負責精確技術組合。不要把這兩層混在一起。
- 在規劃任何目錄結構前，先明確決定五個欄位：`archetype`、`architecture`、`frontend`、`backend`、`apsm_version`；不要直接從 A1/B3 之類模板反推需求。
- 技術選型原則：
  - 預設以 Python 優先；只有在需要瀏覽器級 SPA、SSR/MPA 框架能力，或明確需要 Node 生態時，才引入 Node。
  - 若只是簡單表單、內部工具或模板渲染頁面，優先考慮 `single_service + python_templates + python_api`。
  - 若前端與後端需要獨立啟動、獨立部署或 API 本身要獨立存在，才選 `separated`。
  - 若仍想維持單一 repo 但前後端要分開組織，選 `monorepo`（`src/server` + `src/web`）。
  - `archetype` 推薦值：
  - `web_app`：`separated` 類型的 Web 前端 + API
  - `monorepo`：前後端都放在 `src/`
  - `python_fullstack`：Python template rendering
  - `fullstack_app`：目前此 skill 為相容既有 B4 模板保留的延伸 archetype（`single_service + node_ssr + node_api`）
  - `service_api`：API-only 單體服務（`single_service + none + python_api/node_api`）
- 根目錄必須寫入 `project.config.json`，至少包含：
  ```json
  {
    "name": "my-vibe-app",
    "apsm_version": "1.0",
    "archetype": "web_app",
    "architecture": "separated",
    "frontend": "node_spa",
    "backend": "python_api",
    "version": "0.1.0"
  }
  ```
- `project.config.json` 是 APSM 的單一真相來源；`specs/requirements.md` 是需求真相來源。後續 `README.md` 的目錄說明、啟動入口與 `.env` 規劃都必須與兩者一致。
- 可接受的 canonical 組合與對應模板，見 `references/directory_structure_recommendations.md`；若需求不吻合，先調整選型，再選最接近的模板，不要擅自發明新 root 規則。

### Step 4: 目錄與固定檔案規範

- 固定檔案除了 `project.config.json`、`specs/requirements.md`、`README.md`、`todo.md` 外，還要包含根目錄 `AGENTS.md`。
- `AGENTS.md` 是正式產物，不是可有可無的補充說明。

- 目標專案的相對路徑 `scripts/project_launcher.py` 必須存在；這支檔案來自此 skill 內的 `scripts/project_launcher.py`。
- 目標專案的相對路徑 `scripts/apsm_validate.py` 也必須存在；這支檔案負責做 APSM 結構檢核。
- 交付完成時，目標專案根目錄必有：`project.config.json`、`specs/requirements.md`、`.venv/`（不打包）、`requirements.txt`、`run_app.bat`、`run_app.command`、`run_app.sh`、`.env`（不進版控）、`.env.example`、`README.md`、`todo.md`。
- `run_app.bat` 是根目錄 `scripts/project_launcher.py` 的 Windows 啟動 wrapper；若需要修 launcher 行為，優先修改/重跑 `project_launcher.py`，不要另外手寫一份脫鉤的 `run_app.bat`。
- 執行過 `project_launcher.py` 後，專案還應該有 `.runtime/ports.json`、`.runtime/launcher_state.json` 與 `logs/launcher.log` 等 runtime metadata；這些檔案是 APSM Runtime 的機器判讀介面。
- 目錄結構是技術選型結果，不是起點；必須先完成 Step 2，再依專案型態（前後端分離 / monorepo / single-service）選擇目錄。
- 規範細節放在 `references/directory_structure_recommendations.md`。

### Step 5: APSM 目錄結構檢核

- validator 也要檢查 `usage_scene` / `project_profile` / `AGENTS.md`，避免只有技術模板對齊、但場景規則沒有落地。

- 建立骨架後，立刻執行：
  ```bash
  python scripts/apsm_validate.py --project <target-project>
  ```
- validator 至少要檢查：
  - `project.config.json` 是否存在、JSON 是否合法、`apsm_version` 是否支援、`archetype` 是否與組合一致
  - `architecture/frontend/backend` 組合是否在 skill 支援清單內
  - 根目錄固定檔案是否齊全
  - 對應模板的關鍵目錄與關鍵入口檔是否存在
  - `.env` 是否具備該組合所需的 host/port key
  - 若已執行過 launcher，`.runtime/ports.json` 與 `.runtime/launcher_state.json` 也要能通過 JSON 與 key 檢查
- 若 validator 報錯，先修結構，再繼續開發；不要把結構錯誤帶到功能實作階段。

### Step 5: Windows 專屬硬規則

- `.bat` 只能用 Windows 指令（`dir/copy/del/rmdir/set`），禁止 `ls/rm/cp/export`。
- Python 路徑一律用 `os.path.join`/`pathlib`；禁止手寫 `\\`。
- 檔案讀寫顯式指定 `encoding='utf-8'`。
- `run_app.bat` 預設只放 ASCII 文案；若真的要輸出中文等非 ASCII，才允許例外採 `chcp 65001` + UTF-8，且必須在實際 Windows 環境驗證。
- 避免過深目錄以免 260 字元限制；遇到 Defender 阻擋要在 README 說明操作。

### Step 6: AI 功能整合規範（需要才用）

- Chat：一律 OpenAI Responses API + streaming；對話/視覺用 `input` messages + parts。
- STT：先 Whisper（`whisper-1`），失敗再用 Responses `input_audio` fallback。
- 圖像：預設 Nano Banana 2（Gemini 3.1 Flash Image）做 T2I/I2I；加上 no-text guardrail。
- 若需要本地模型/離線推論，優先評估 ONNX + ONNX Runtime；除非有明確理由，避免把 PyTorch 當成預設交付依賴。
- 金鑰：只從 env/config 讀；不要硬編碼。
- 若是前後端分離（例如 FastAPI/Flask + React/Vue），後端必須處理 CORS，至少允許本機前端開發位址；前端 API base 必須和根目錄設定一致。

（詳細程式型樣與封裝策略見 `references/openai_nanobanana_guidelines.md`。）

### Step 7: 錯誤處理與 logging

- 主入口必包 `try/except`，禁止閃退。
- UI 顯示「白話錯誤 + 請複製以下訊息給 AI 助手」；下方附完整 traceback。
- logs 目錄分級記錄（INFO/ERROR），不得寫入 API key。
- 若用 toast 顯示錯誤，停留時間要足夠，且內容應可選取/複製；不要讓錯誤訊息一閃而過。
- 若有使用 mocking / 假資料 / 假 API，必須在對話、README 或 UI 中明確揭露，不可讓使用者誤以為是真實資料流。

### Step 8: 一鍵啟動與打包

- 先將此 skill 內相對路徑 `scripts/project_launcher.py` 與 `scripts/apsm_validate.py` 的內容寫入目標專案的相對路徑。
- 主入口請維持 `scripts/project_launcher.py`；它負責跨平台高階分類、修復與 launcher 生成，不應改成平台後綴名稱。
- 雖然 PDF 原始規格傾向單一 `run_app`，但此 skill 為了維持 Windows/macOS/Linux 的零指令雙擊體驗，仍保留 `run_app.bat` / `run_app.command` / `run_app.sh` 三入口；不要擅自改回單檔。
- `run_app.bat` 是由 `scripts/project_launcher.py` 生成/維護的 Windows wrapper，不是獨立規格或另一套 hand-written launcher；若專案內已存在這條鏈，禁止 agent 自作主張另外寫一份新的 `run_app.bat` 取代它。
- 若要沿用來源 skill 的分平台流程，或要在 POSIX 環境單獨驗證，也可一併帶入此 skill 內的 `scripts/project_launcher_posix.py`，並以 `python scripts/project_launcher_posix.py` 生成/檢查 `run_app.sh` 與 `run_app.command`。舊名 `scripts/project_launcher_linux.py` 僅保留相容別名，不建議再當主名稱。
- 再於目標專案根目錄執行：`python scripts/project_launcher.py` 以：
  - 自動掃描 imports → 修正/生成 `requirements.txt`
  - 保守修正入口檔常見的 relative import 問題，並在改寫前產生 `.bak` 備份
  - 建立 venv、安裝依賴、`pip check`、import test
  - seed `.runtime/ports.json`、`.runtime/launcher_state.json` 與必要 log 檔，讓 validator 與後續除錯都有單一可讀位置
  - 偵測後端/前端入口與設定中可推得的 host/port
  - 生成 `run_app.bat` / `run_app.command` / `run_app.sh`；只有在 URL 可推得時才嘗試自動開瀏覽器。啟動器應先做 readiness probe 並把結果寫進 log 與終端，但即使 probe 失敗也仍要嘗試開瀏覽器，避免使用者誤以為系統卡死
- 交付前打包 ZIP：在根目錄執行 `python scripts/project_launcher.py --package`
  - 預設輸出：`release/<資料夾名>.zip`
  - 可用 `--package-out` 指定 ZIP 路徑
  - ZIP 會排除：`.venv/`、`__pycache__/`、`node_modules/`、`logs/`、`.env`、`.launcher.env`
  - ZIP 會保留：`dist/`、`build/`（靜態站/前端成品常用）
- 若要支援真正安全的動態 port：
  - 優先讓服務自行綁定可用 port，之後再回讀實際 port；不要先掃描一個空 port 再假設仍可用
  - 將實際 port 同步回寫到瀏覽器 URL、前端 API base、log、以及啟動器自己的狀態檔
  - 在開瀏覽器前做 readiness check；若服務尚未 ready，就不要自動打開錯誤頁面

### Step 9: Finalization and QA

- 對照 `references/quality_checklist.md` 全部通過。
- `python scripts/apsm_validate.py --project <target-project> --strict` 必須在交付前通過一次。
- `.runtime/ports.json` 與 `.runtime/launcher_state.json` 必須存在且為合法 JSON；若 launcher 已寫入 runtime state，就不能留空殼檔。
- 至少做一次「解壓到新資料夾→雙擊 run_app.bat」的乾淨啟動驗證。

## Testing plan

### Triggering tests

- Should trigger:
  - 「幫我做一個 Windows 小工具，解壓後直接雙擊就能跑」
  - 「這個專案 Windows 上中文亂碼/port 衝突，幫我修」
  - 「加 OpenAI 串流對話 + 語音轉文字 + 生圖」
- Should NOT trigger:
  - 純概念性討論（不需要交付可執行專案）
  - 純翻譯/摘要，且不涉及 Windows 交付

### Functional tests

- Test case: 一鍵啟動
  - Given: 新解壓縮的專案資料夾
  - When: 點一下啟動（Windows：`run_app.bat`／macOS：`run_app.command`／Linux：`run_app.sh`）
  - Then: 自動建立 venv、安裝依賴、啟動服務/視窗；只有在 URL 可推得且已通過 readiness check 的設計下才自動開啟前端。失敗時顯示繁中說明並寫入 `logs/`。

- Test case: APSM 結構檢核
  - Given: 已產生 `project.config.json` 與目錄骨架的專案
  - When: 執行 `python scripts/apsm_validate.py --project <target-project> --strict`
  - Then: 輸出 valid 結果；若缺檔、組合非法、`.env` key 不完整、或 `.runtime/*.json` 結構不合法，會以 error code 與路徑回報。

- Test case: 串流輸出
  - Given: 啟用 OpenAI Responses chat
  - When: 發送訊息
  - Then: UI 逐 token 更新；中斷或錯誤可保留已生成內容。

## Troubleshooting

- 症狀：macOS/Linux 雙擊 `run_app.*` 沒反應或提示沒有執行權限
  - 修正：在 Terminal 執行 `chmod +x run_app.sh run_app.command` 後再執行/雙擊。
- 症狀：macOS 雙擊 `.command` 被系統阻擋
  - 修正：依 README 指引到「系統設定 > 隱私權與安全性」允許開啟；必要時再補 `chmod +x`。

- 症狀：`attempted relative import with no known parent package`
  - 原因：入口檔相對匯入
  - 修正：`project_launcher.py` 會保守修正常見入口檔的 relative import，並先寫出 `.bak` 備份；若仍失敗，再改成套件入口（例如 `python -m package.module`）或手動修正。

## Resources

- `references/usage_scene_decision_tree.md`：先判斷使用情境 A/B/C/D，再輸出 `usage_scene`、`project_profile` 與 `AGENTS.md`

- 以下皆為此 skill 目錄內的相對路徑；若要套用到目標專案，需先把對應內容寫入目標專案的相對位置。
- `scripts/project_launcher.py`：一鍵啟動腳本生成與依賴驗證；實際使用時應寫入目標專案的 `scripts/project_launcher.py`
- `scripts/apsm_validate.py`：APSM 結構檢核器；驗證 `project.config.json`、目錄模板與必要檔案是否一致
- `scripts/project_launcher_posix.py`：POSIX 相容入口；適合保留 split-platform 流程或在 Linux/macOS 上單獨驗證 launcher 行為
- `scripts/project_launcher_linux.py`：僅供相容舊流程的別名；名稱容易誤導，不建議作為新的主要引用
- `references/openai_nanobanana_guidelines.md`：OpenAI Responses 串流 + Nano Banana 2 圖像 + STT 規範
- `references/apsm_decision_tree.md`：APSM 決策樹；先用它篩選 `archetype` / `architecture` / `frontend` / `backend`，再去查模板細節
- `references/ui-workbench-guardrails.md`：給 coding agent 的 task-first UI 約束，避免 stacked dashboard / card farm 首屏
- `references/linux_platform_pitfalls.md`：Linux 權限、Shell 啟動、`xdg-open` 與背景執行避雷
- `references/macos_platform_pitfalls.md`：macOS Finder、`.command`、Gatekeeper、`open` 與權限避雷
- `references/linux_macos_platform_pitfalls.md`：Linux/macOS 導讀與共通原則，相容舊連結用
- `references/windows_platform_pitfalls.md`：Windows 常見錯誤與硬規則
- `references/directory_structure_recommendations.md`：目錄結構建議與 port/env 規範
- `references/quality_checklist.md`：交付前 QA 清單
