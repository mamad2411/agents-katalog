---
name: memory-distill
description: 將 DSH 舊 session（~/.dsh/sessions 嘅 JSONL+zstd transcripts）蒸餾成結構化摘要，再寫入 knowledge/memory/ 做長期記憶。當用戶想我「記住之前傾過嘅嘢」、想回顧舊對話、或者要整理 session 知識時使用。
whenToUse: 用戶要求記住舊 session 內容、定期知識整理、或者想知以前傾過啲咩。
---

# Memory Distill（Session 蒸餾）

將舊對話蒸餾入知識庫，係 OpenClaw「dreaming sweep」概念嘅 DSH 版本。

## 步驟

1. **產生 digests**（script 自動做）：
   ```powershell
   node "$HOME/Desktop/knowledge/scripts/distill-sessions.mjs"
   ```
   輸出去 `knowledge/memory/digests/`，每個 session 一個 .md：標題、日期、用戶問題、回覆節錄、用過嘅工具。

2. **讀 digests**：用 glob/grep 睇 `knowledge/memory/digests/*.md`，揀有價值嘅 session（有實質知識/決定/研究發現嘅）。

3. **寫蒸餾筆記**：將有價值嘅內容寫成主題筆記入 `knowledge/memory/`（例如 `2026-08-16-dsh-rag-build.md`）：
   - 寫俾「未來嘅我」睇：自包含、有結論、有檔案路徑
   - 跟 knowledge/ 嘅規約（frontmatter tags/updated）
   - 唔好複製成段 transcript；要濃縮成「學到咗咩／做咗咩／下一步」

4. **更新 index**：`knowledge/memory/index.md` 加一行；`knowledge/README.md` 結構表如有需要就更新。

5. **清理**：digests 係中間產物，蒸餾完可以保留（好細），或者 move 去 `knowledge/memory/_trash/`。

## 原則
- Raw transcript 唔係知識；蒸餾先係。
- 每條筆記要可以獨立閱讀（冇前文都明）。
- 決定/偏好/研究發現優先；流水帳跳過。
