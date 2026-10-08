---
name: sop-deploy
description: 部署 SOP — 強制品質 checklist + pre-deploy 確認，不得跳過任何 checkpoint
allowed-tools: Read, Bash
---

# 部署 SOP

部署前，**必須依序完成以下所有步驟**，不得跳過任何 ⛔ CHECKPOINT。

## 使用方式
```
/sop-deploy
```

## 執行步驟

### ⛔ STEP 1 — 載入品質 Checklist

讀取（依序嘗試）：
1. `.knowledge/quality-checklist.md`
2. `.knowledge/company/standards/quality-checklist.md`

逐項列出所有檢查項目，確認每項的當前狀態。

> ✋ 確認 checklist 已讀、項目已列出後再繼續。

---

### ⛔ STEP 2 — 確認所有任務狀態
!`find .tasks -name "*.md" | xargs grep -l "| 狀態 |" 2>/dev/null | xargs grep "| 狀態 |" 2>/dev/null`

確認：
- 本 Sprint 所有任務均為 `done`
- 無 `in_progress`、`in_review`、`blocked` 的未結任務

> ✋ 若有未結任務，**禁止繼續部署**，回報 L1 處理。

---

### ⛔ STEP 3 — 執行 Pre-deploy 檢查
執行 `/pre-deploy`（讀取 `.claude/commands/pre-deploy.md` 並依步驟執行）

對照 STEP 1 載入的 checklist，逐項勾選：
- 已完成 → `- [x]`
- 未完成 → 停止，回報原因

> ✋ **所有 checklist 項目通過後才可繼續**。若有未通過項目，記錄原因並停止。

---

### STEP 4 — 執行部署

依專案部署方式執行（參考 CLAUDE.md 或 dev-plan 的部署指令）。

---

### ⛔ STEP 5 — 記錄 Gate G5
執行 `/gate-record G5 通過 {備註}`（讀取 `.claude/commands/gate-record.md` 並依步驟執行）

---

### STEP 6 — 輸出部署結果

```
✅ 部署完成

Sprint：Sprint N
品質 Checklist：全部通過 ✅
未結任務：無 ✅
Gate G5：已記錄 ✅
部署時間：{timestamp}

下一步：PM 執行 /sprint-retro
```
