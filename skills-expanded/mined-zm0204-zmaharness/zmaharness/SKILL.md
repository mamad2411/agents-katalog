---
name: zmaharness
description: 當任務符合 T1～T5 且協作有明確收益時，用 zMAHarness 提議唯讀分析，依使用者的對話決定派工、獨立驗收並繼續原任務。
---

# zMAHarness 協作

主控 Agent（日常預設 Codex Sol High）平常直接完成原任務。一般工作不預載 Harness，也不為了提議協作主動查額度。
只有符合下列條件且有實際收益，才提出一次協作建議。門檻沿用本機 TOML 的 `[triggers]`。

| 觸發 | 可觀察的理由 |
| --- | --- |
| T1 | 同一錯誤經不同修正達 `t1_failed_fix_rounds` 輪仍失敗 |
| T2 | 變更觸及 `t2_risky_paths` 且差異行數達 `t2_risky_diff_lines` |
| T3 | 預計讀取達 `t3_read_files` 或 `t3_read_kb`，預期產出很小 |
| T4 | 既有 Codex 額度快照達 `t4_codex_used_percent`，且有低成本驗收方法。缺快照時不用 T4 |
| T5 | 使用者主動要求協作，或呼叫 `$zmaharness`（Codex）/`/zmaharness`（Claude Code） |

## 出卡前檢查與選模

決定提議協作後，先依檔案大小與可讀範圍決定模式，再判斷任務與等級，然後只執行一次：

`python -B -m mah route --repo <目標專案根目錄> --task <review|second_opinion|research> --level <light|standard|deep> --mode <bundle|worktree> --controller <codex|claude|other>`

| 等級 | 何時用 |
| --- | --- |
| `light` | T3 大量資料整理、小型常規檢查 |
| `standard` | T2 一般高風險 Review、研究需要整合較多線索 |
| `deep` | T2 跨模組交互複雜、T1 第二意見、需要異質視角的深度推理 |

- `--controller`：Codex 主控填 `codex`，Claude Code 主控填 `claude`，其他填 `other`。
- `--repo` 使用主控目前工作資料夾所屬的 Git 專案。目標不在目前工作資料夾內，或屬於雲端硬碟、網頁等非本機 Git 專案資料時，不在協作範圍內，不出卡。
- `ok` 為 `false`（結束碼 30）或 `card` 為 `false` 時不出卡，用一句話說明 `reasons` 後由主控自己繼續原任務。
- 【建議模型】與選項 2 用 `recommended.display`，選項 3 用 `alternate.display`；`alternate` 為 `null` 時省略選項 3。卡片只顯示 `display`，不顯示 Adapter 名稱。
- `note` 不為 `null` 時，把它（依使用者語言）放進【為什麼建議協作？】。
- `needs_unsandboxed_dispatch` 為 `true` 時，【授權限制】加「派工時需核准一次沙盒外執行」。
- 建卡與派工的 Adapter、模型 ID、effort 一律照抄輸出的 `adapter`、`model`、`effort`。
- `warnings` 不為空時，在卡片外用一句話轉告使用者一次。
- `/usage` 額度查詢只能由 `mah` 內部透過程式呼叫，**主控不得自己在 shell 執行含 `/usage` 的指令**（特別禁止在 Git Bash 執行）。

## 對話內提議

卡片與回覆一律使用使用者提問的語言。`zMAHarness`、模型 ID 與指令名（`$zmaharness`、`/zmaharness`、`mah ...`）保留原文。
下方標題與選項為中文範本，翻譯時須保留語意與順序。中文環境使用「【zMAHarness 協作建議】」，
其他語言使用對應翻譯，例如英文「[zMAHarness Collaboration Proposal]」。

使用主控的原生互動提問工具（Codex Desktop 原生提問卡；Claude Code 用 AskUserQuestion）
送出**單一問題**，把資訊、三個選項與「或自行輸入回覆」放在同一頁，一步完成，不拆題、不翻頁。
問題文字第一行放依語言規則顯示的卡片標題，空一行後，每項資訊獨立一行，格式為「【欄位名稱】內容」。
問題文字一律使用純文字，禁止 Markdown 與「｜」分隔符號。

- 【觸發原因】例如「【觸發原因】T5 · 使用者主動要求」。
- 【建議模型】填 `mah route` 輸出的 `recommended.display`。
- 【任務與範圍】顯示 Review、Second Opinion 或 Research，以及 Context-Bundle 或 Disposable Worktree。
  列出實際涵蓋的檔案名稱，必要時用相對路徑區分同名檔。若 Worker 可查閱工作樹內的關聯檔案，也要明列可查閱範圍。
- 【授權限制】顯示 `僅 1 次 · 唯讀（自動等待模型完成）`。這是對話核准（`codex_prompt`）與 Context-Bundle 的固定次數；本機設定 `approval.mode = "manual_cli"` 時，Disposable Worktree 卡片可到 `limits.max_dispatches_per_grant`，此時顯示實際卡片的次數，並註明「需在終端機親手核准」。`needs_unsandboxed_dispatch` 為 `true` 時，再加「派工時需核准一次沙盒外執行」。
- 【為什麼建議協作？】用一句白話說明本次協作的收益及選模原因，不提私人專案名稱；若 `mah route` 回傳 `note`，併入本欄。

依提問工具實際提供的欄位排版。下方選項範本定義各選項的意思，依工具能力分配到相應欄位。

- **有 `preview`**（例如 Claude Code 的 AskUserQuestion）。`header` 填 `zMAHarness`。
  問題文字只放標題、空行、【觸發原因】和【任務與範圍】。範圍摘要在一行列出任務類型、檔案數與模式。
  選項用短 `label`。每個協作選項的 `description` 用一行列出模型 · effort、任務、授權。
  每個協作選項的 `preview` 使用 Markdown，以 `## 建議方案` 或 `## 備選方案` 開頭，
  依序列出粗體欄位「模型」、「任務」、「模式」、「範圍」、「授權」。模型 ID 與 effort 用行內程式碼，
  範圍以條列顯示實際檔案與可查閱的關聯範圍。最後以 `### 為什麼？` 加一句說明該方案，不提私人專案名稱。
  「不同意」的 `preview` 以 Markdown 條列四項：不派工、不呼叫外部模型、立即繼續原任務、同一任務不再追問。
- **有 `header`、`description`，無 `preview`**（例如 Codex Plan 模式的 `request_user_input`）。
  `header` 填 `zMAHarness`，問題文字放完整五項，每項一行。選項用 `label` 加 `description`，
  協作選項在說明中列出該選項的模型 · effort、任務、授權。
- **只有問題文字與選項字串**（例如 Codex 一般模式的 `request_user_input_async`）。
  問題文字放完整五項，每項一行。每個協作選項的字串都須寫出模型 ID 和 effort，
  例如「繼續協作（建議：<recommended.display>）」。不得只寫「繼續協作（建議）」或「繼續協作（備選）」。

依檔案大小及可讀範圍在出卡前決定模式，並把模式及範圍列在卡上。

- **Context-Bundle**：只用於 1～2 個核心檔案，且完整檔案加上任務指示封裝後，總大小不超過本機 TOML 的 `limits.max_task_bytes`（預設 32 KB）。
- **Disposable Worktree**：超過 2 個檔案、單檔太大、封裝後超過上限，或需查閱關聯檔案時使用。卡片須列出 Worker 可查閱的範圍。
- 嚴禁為了符合上限而截斷或刪減檔案。

核准後嚴禁自動從 Context-Bundle 改成可讀範圍更大的 Disposable Worktree。需要擴大範圍時，重新提議並等待回覆。

1. `不同意（由主控 Agent 自己繼續完成）`
2. `繼續協作（主控 Agent 建議：<recommended.display>）`
3. `繼續協作（改用備選：<alternate.display>）`（`alternate` 為 `null` 時省略本選項）

**T1～T5 都必須暫停等待。** 原生卡片一送出，立即結束或暫停本輪，等待使用者對該卡片
點選或手打回覆。初始的 T5 請求或 `$zmaharness`／`/zmaharness` 呼叫只觸發提議。即使初始請求已指定模型與
檔案，也不得在顯示卡片的同一輪執行 `card create`、`grant approve` 或 `dispatch`。
只有收到該卡片的回覆後，才能在下一輪依該回覆進行授權與派工。原生互動工具不可用時，
回報限制並由主控 Agent 本地繼續原任務。Card ID、雜湊、Grant、工作目錄及證據檔留在背景。

- **不同意**　主控 Agent 立即在本地繼續原任務，同一問題不再提議或追問。若已有待核准卡片，
  在收到回覆後以 `mah card reject <card_id>` 記錄拒絕。寫入失敗時仍繼續原任務。
- **點選繼續協作**　採用選項標明的模型與 effort，維持卡片上的任務、範圍和授權限制。
- **手打覆寫**　使用者可在自由輸入框指定模型、別名、effort 或縮小檔案範圍（例如「換 4argon」、「用 medium」或「只看 io.py」）。
  執行 `mah route ... --override "<字樣>" [--effort <effort>] --card-effort <卡片 effort> [--adapter <Adapter>]`。
  `resolved` 為 `false` 時依 `choices` 用單頁卡片澄清；`ok` 為 `false` 時轉告 `reasons`（例如 Orchestrator 或模式不支援）並改提一般可用模型；
  `note` 有額度提醒時照實告訴使用者。手打不受異質與額度排除限制，其餘欄位沿用卡片。
  若原模式無法維持縮小後的範圍或所選模型不支援該模式，先提出符合新範圍與模式的卡片並等待核准。

## 輕量主控

只有自然觸發 T1、T2 或 T5 時，才直接讀取 `%LOCALAPPDATA%\zMAHarness\harness.local.toml` 的
`[controller]`。缺少檔案或欄位時，`light_models` 預設 `[]`，`suggested_controller` 預設
`Codex Sol High`。只有從執行環境確認自己的模型 ID 且與 `light_models` 其中一項完全相符，
才算輕量主控。無法確認 ID 時一律視為非輕量。禁止模型自行評估能力。

輕量主控沿用「對話內提議」的語言、單頁、手打覆寫及強制暫停規則，並依提問工具欄位選用同樣的排版。
五項資訊以選項 3 的協作內容為準。有 `preview` 時，問題文字用摘要，選項 3 的 `preview` 用建議方案格式呈現完整資訊。
有 `description` 時，切換主控選項用短標籤，說明列出建議主控與在介面切換後回覆的步驟。
只支援選項字串時，切換主控保留建議主控與回覆步驟，協作選項寫出模型 ID、effort 與任務。
三個選項改為：

1. `不同意（目前主控自己繼續）`
2. `切換主控（建議：<suggested_controller>；請你在介面切換後回覆）`
3. 以 `--level deep` 呼叫 `mah route`，取輸出的 `recommended` 作為強模型與 effort。
   - 仍在規劃、尚未開始實作，且本次要審查的是實作計畫時，使用 `繼續協作：用 <recommended.display> Review 目前計畫`。
     使用既有 `review` 模板，把實作計畫寫進 `task.md`。Context-Bundle 將計畫放入任務指示，
     隨 `bundle create` 封裝。相關原始檔沿用核准的 Context-Bundle／Worktree 規則。
   - 其他情況沿用原觸發對應的任務類型與範圍，只更換模型與 effort。例如 T1 卡關時使用
     `繼續協作：用 <recommended.display> 做 Second Opinion`。T5 指定 Research 或 Review 時沿用指定任務。

選項 1 立即繼續原任務，同一任務不再追問。選項 2 由使用者在介面切換後回覆，再繼續原任務。

`--via codex_prompt` 代表「主控對話內核准」，適用任何主控。這筆紀錄由主控寫入，CLI 無法替使用者把關，因此只在使用者明確同意後執行。
本機設定 `approval.mode = "manual_cli"` 時，主控不得執行 `grant approve`；CLI 會以結束碼 10 拒絕 `codex_prompt`。
請把完整的 `python -B -m mah grant approve <card_id> --sha <完整 SHA-256> --via manual_cli` 交給使用者在自己的互動終端機執行並親手輸入確認碼，使用者回報完成後再派工。
收到使用者同意協作的回覆後，才讀取 [references/dispatch.md](references/dispatch.md) 並照著執行。
拒絕或只選切換主控時不讀取。
