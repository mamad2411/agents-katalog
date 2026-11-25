---
name: clec-episode-organizer
description: Organize user-scoped CLEC episodes into traceable Traditional Chinese Obsidian pages. Use when Codex must group X, pCloud, Google Drive, Bilibili, Odysee, and RSS or Podcast sources by five-digit episode number; obtain and review transcripts through media-transcript; clean readable transcripts with the confirmed CLEC lexicon; anonymize students; or build the standard three-layer episode page.
---

# CLEC Episode Organizer

把一個 CLEC 五位數編號視為一集。平台只是來源、附件或備份；同一編號只建立一篇節目主頁。

## 核心規則

1. 只處理使用者指定的集數或日期範圍，不擴大掃描其他專案或 Vault。
2. 以 `canonical_id: clec-<五位編號>` 合併來源；日期相近或內容相似都不足以證明是同一集。
3. 無法確認歸屬、標題或角色時，標示「尚未確認」或 `〔需核對〕`，不要猜。
4. 分層保存原始來源、原始字幕／ASR、繁體原稿、整理版與人工修訂，不互相覆寫。
5. 預設 `status: pending-editorial-review`、`publish_to_website: false`；未經使用者明確要求，不發布網站或外部資料庫。
6. 使用繁體中文、台灣用語與日常中文。一般正文使用「台灣、平台、台幣」；正式名稱例外。
7. 先使用目標 Vault 的 `CLEC｜常用詞與逐字稿校對資料庫.md`；沒有時才讀 `references/clec-transcription-lexicon.md`。詞庫只能協助查證，不能代替音訊。

## 執行順序

### 1. 確認範圍與現況

- 確認集數、日期範圍、目標 Vault 與交付內容。
- 只讀該集現有主頁、metadata、來源紀錄及逐字稿檔案。
- 修改前確認檔案是否已存在及是否有其他未預期變更。

若使用者指定日期範圍，先列出期間內可見項目，再依五位數編號分組。沒有編號、編號衝突或短篇後綴無法判定者，放入「尚未確認」，先回報後再逐集整理。

### 2. 建立來源清單

每個來源至少記錄：

- `platform`：X、pCloud、Google Drive、Bilibili、Odysee、RSS／Podcast 等。
- `relationship`：`original-post`、`slides`、`video-archive`、`video-backup`、`audio-edition`、`transcript`、`related-post` 或 `unknown`。
- `verification`：`verified`、`user-confirmed`、`needs-review` 或 `not-found`。
- URL 與簡短說明。

同一集的已確認來源合併展示。搜尋不到只能寫「目前尚未確認」；學員整理頁只能列為延伸資料。

### 3. 取得並判斷逐字稿

字幕取得、媒體處理與語音辨識交給 `media-transcript`：

1. 人工字幕優先，其次是平台自動 CC 或 Podcast transcript。
2. 來源字幕只有少數不清楚處時，保留字幕並用同集局部音訊核對。
3. 主講與問答多個區段都不可讀、時間軸失效或大量缺漏時，保留原字幕作證據，再用完整音檔 ASR 重建。
4. 原始字幕／ASR、繁體轉換與整理版分開保存。

選擇與驗收細節必須讀 `references/transcript-quality-gates.md`。至少抽查開場、主講中段、主持人轉場、兩段問答、最後兩位學員、節目收尾與最後 30 秒。

### 4. 建立單集主頁

使用 `assets/episode-page-template.md`，固定三層閱讀：

1. `30 秒內看懂`：一句話重點、3～5 個重點、本集資料。
2. `3–5 分鐘理解主要論證`：背景、主要論證、策略或行動。
3. `願意深讀的人：證據、限制與延伸資料`：範圍、名詞與整理版逐字稿。

標題與摘要以國中閱讀程度撰寫；一般正文使用高中程度概念與日常中文；深度內容可以更進階，但術語第一次出現時要解釋。

主頁只嵌入整理版逐字稿，不顯示原始稿、模型、segment 數量、轉錄指令、內部待辦或技術驗證。若同一編號可能對應不同內容，保留簡潔的「編號重複」警示。

### 5. 統一標題與檔名

以使用者確認的 00574 格式為準：

`00574｜消費才是經濟之母，有錢人消費是道德.md`

- 主頁固定為 `<五位編號>｜<標題>.md`。
- 使用全形 `｜`，前後不加空格。
- YAML `title`、H1 與檔名去除 `.md` 後必須完全一致。
- 索引與相關頁使用完整 Wiki link。
- 標題以使用者確認版本優先；來源互相衝突時先詢問，不自行縮寫。
- 附屬檔使用相同分隔方式，例如 `<編號>｜整理版逐字稿.md`。

### 6. 製作整理版逐字稿

保留原始繁體稿不動，另建 `<編號>｜整理版逐字稿.md`。

依實際內容辨認課前補充、James 主講、主持人接手、學員分享與問答；不按固定分鐘數硬切，也不自動加入 `00:05`、`00:10` 等時間章節。

整理版只做：

- 補自然標點、分段與主題標題。
- 統一繁體中文與全形標點。
- 移除不影響語意的獨立語贅詞與可確認的相鄰機械重複。
- 修正使用者或可靠來源已確認的專有名詞。
- 保持原意、論證順序、數字、標的與口語節奏。

無法確認的詞保留原辨識並標 `〔需核對〕`。

H1 後固定依序放三個備註：

1. `> [!warning] 閱讀版仍需人工校對`
2. `> [!info] 講者標示方式`
3. `> [!note] 專有名詞校正`

三個標題與順序固定；底本、主持人、學員數與證據說明依該集事實填寫。專有名詞備註連到 `[[CLEC｜常用詞與逐字稿校對資料庫]]`。

### 7. 講者與匿名化

- James 老師保留姓名。
- 學員依第一次上台順序標為「學員 1、學員 2……」，同一輪追問沿用編號。
- 主持人姓名只能依自我介紹、James 稱呼、節目說明或使用者確認。
- 超過三小時的長片可把 James 視為主講人候選、Kate 或 Dona 視為主持人候選，但候選不能當成單集證據。
- 沒有逐句講者分離資料時，以一位學員一個對話區塊呈現，不硬猜每一句講者。
- 匿名化只替換已確認的完整身分字串；不使用寬鬆姓名規則掃描全文。

### 8. 批次校對

只有使用者明確指定資料夾時才批次處理：

1. 分開整理版 Markdown 與 raw、JSON、TXT、SRT、VTT。
2. 修改前後對所有非 Markdown 原始檔計算並比對 SHA-256。
3. 只修改整理版／閱讀版 Markdown，只套用 `user-confirmed` 或 `verified` 詞形。
4. 長詞優先；`QQ`、`QQM`、`OD`、`ODC` 等短詞使用完整詞界。
5. 依上下文才能判斷的詞不可機械取代。
6. 出現 UTF-8 亂碼立即停止並修復。
7. 完成後掃描誤辨詞、亂碼與短代號殘留，並抽查每個有修改的檔案。

需要從時間段 JSON 產生閱讀版時，使用 `scripts/build_readable_transcript.py`。設定必須由人工提供分段、來源說明、匿名對照及替換規則；腳本不得自行判斷學員身分。`scripts/build_readable_transcript.mjs` 僅保留舊設定相容性。

### 9. 驗證與交付

交付前確認：

- canonical ID、日期、語言、狀態與來源角色正確。
- 主頁檔名、YAML `title`、H1 與 Wiki link 一致。
- 原始稿及原始媒體衍生檔未被覆寫。
- 主講、主持人與問答分界合理，學員編號連續且身分字串未殘留。
- 已確認名詞已修正；未知詞仍標 `〔需核對〕`。
- 最後兩位學員、節目最後一句、實際音訊結尾及最後 30 秒已抽查。
- 疑似重複幻覺或收尾後無音訊依據的文字不進入衍生稿。
- 主頁只顯示整理版逐字稿。
- 不把投資觀點寫成獲利保證或個人建議。

只回報實際更新的檔案、已確認來源、待確認來源、仍需人工審閱項目與發布狀態。

## 按需讀取

- 需要完整主頁骨架：`assets/episode-page-template.md`
- 判斷 CC、局部 ASR、完整 ASR 或驗收逐字稿：`references/transcript-quality-gates.md`
- 校對專有名詞：優先讀 Vault 詞庫，否則讀 `references/clec-transcription-lexicon.md`
- 需要已確認案例：`references/00574-verified-example.md`
- 從時間段 JSON 產生閱讀版：`scripts/build_readable_transcript.py`
