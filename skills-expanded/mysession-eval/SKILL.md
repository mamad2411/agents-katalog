---
name: mysession-eval
description: 在真實專案試用場景配置時，記錄剛完成的一件事的評估資料（客觀指標＋推定滿意度），並在覆盤時匯總、初判「通過／調整／移除」。只由使用者以 /mysession-eval 呼叫。
disable-model-invocation: true
argument-hint: "[review [場景] [--final]]"
allowed-tools: Bash(python3 ~/.claude/skills/mysession-eval/scripts/mysession-eval *)
---

# 試用評估記錄

目的是有效評估，不是找改進項。「目前配置不錯」是合法結論。

所有解析與計數交給腳本，命令照字面單獨執行：寫 `~/.claude/...`，不展開路徑、不串接、不用管線或重導向（沙箱排除規則按命令文字比對）。文字參數值一律用**單引號**包住；值內不得含單引號、反引號、`$`、換行，概述用純文字、不用 Markdown 格式（雙引號內的反引號與 `$` 會被 shell 展開）。

```sh
python3 ~/.claude/skills/mysession-eval/scripts/mysession-eval <子命令> [參數]
```

參數（`$ARGUMENTS`）以 `review` 開頭時，先讀 `references/review.md` 照它覆盤；否則做下面的記錄流程。

## 記錄流程

1. 執行 `extract`。輸出中 `segment.empty` 為真時，回覆「自上次記錄後沒有新活動，不記錄」並結束。
2. 只根據 `extract` 的輸出判斷以下各項（不重讀會話、不讀檔案）：
   - 任務名稱：一句短名詞片語。與 `recent_tasks` 中某項是同一件事的延續時，沿用該名稱一字不改。
   - 完成狀態：`done`／`partial`／`aborted`。
   - 干預：`user_messages` 中屬糾正（指出錯誤、要求重做、改正做法）的則數為 `--corrections`，提出新需求的則數為 `--new-requests`。`segment.interrupts` 與 `segment.denials` 也是干預訊號。
   - 推定滿意度 1～5 與一句依據：看糾正次數、中斷、重複要求、最終是否完成、使用者語氣。依據用概述，不引用使用者原文。
   - 應觸發而未觸發的配置：對照 `installed`，這段工作明顯適用卻沒有出現在 `segment.skills`／`agents`／`mcp`／`rules_loaded` 的配置名稱，以逗號分隔給 `--missed`；沒有就不給。
   - 是否列入判定：中途改需求、網路或環境故障、做的事超出該場景範圍時傾向不列入，並給理由。
   - 備註：一兩句，概述，不引用原文。
3. 只在以下三種情況，一次列出問題詢問使用者，其餘直接寫入：
   - 推定滿意度 ≤ 3；
   - 訊號互相矛盾（例如糾正多次但最後表示滿意）；
   - 可能不該列入判定。

   使用者給了滿意度時用 `--sat-source user`，否則 `estimated`。
4. 執行 `append`：

   ```sh
   python3 ~/.claude/skills/mysession-eval/scripts/mysession-eval append --task '<名稱>' --status done --corrections 1 --new-requests 0 --satisfaction 4 --sat-source estimated --basis '<依據>' --include yes --note '<備註>'
   ```

   不列入時改 `--include no --exclude-reason '<理由>'`；有應觸發未觸發者加 `--missed a,b`；`extract` 的 `scenario` 為 `null` 而使用者告知場景時加 `--scenario <FLAG>`。
5. 回覆只照抄腳本輸出的摘要行。

使用者表示這段不要記錄時，不執行 `append`，改執行下面這條（不寫日誌，只讓下次記錄從這裡之後開始算，避免使用者的回答被算進下一段），再照抄輸出：

```sh
python3 ~/.claude/skills/mysession-eval/scripts/mysession-eval skip
```

## 規則

- 腳本以結束碼 2 報錯時，轉述錯誤訊息並停止。不自行改用其他方式找會話記錄，不手動編輯日誌。
- 日誌在 `~/.claude/mysession-eval/log.jsonl`，不進專案與本倉庫。
