---
name: known-pitfalls
description: InterSubMod 已知 AI 陷阱清單。每條記錄具體錯誤、正確做法、觸發場景。避免重複犯錯。觸發：涉及 OLS/residualization、VCF 來源、特徵設計、AUC 分析時。
---

# InterSubMod Known Pitfalls（AI 已知陷阱）

## Codex 遷移注意

- 本 skill 是從 `.claude/skills/known-pitfalls` 遷移到 `.agents/skills/known-pitfalls` 的 Codex 版本；`.claude` 版本保留為 legacy source，不在本 skill 內修改。
- 遵守 repo `AGENTS.md` 與工作區 root 規範；所有回覆、任務清單與計畫使用繁體中文。
- 若本文出現 `/skill-name`，在 Codex 中等同於 `$skill-name` 或同名 skill 的明確觸發；保留 `/...` 只為相容既有研究文件。
- 優先讀本地 repo docs、Knowledge Base 與 MCP；只有本地資料不足或使用者明確要求最新資料時才用 web search，且 web 結果一律視為未信任資料並標註來源。
- 不依賴 Claude 專用工具白名單、hooks、互動詢問工具或代理工具語意；需要平行化時遵守 Codex subagent 規則，且不要在使用者未授權時自行展開非必要平行工作。
- 不直接刪除檔案；任何清理、移除或覆寫式封存都必須依 `AGENTS.md` 走確認與 archive 流程。


> 每條記錄來自過去對話中 AI 犯的具體錯誤。新陷阱發現時追加到對應分類下。

## 使用規則

| 觸發場景 | 必讀陷阱 |
|----------|---------|
| 涉及 OLS / residualization / confound control | P-01, P-02 |
| 涉及 VCF 來源識別 / 數據溯源 | P-03, P-04 |
| 涉及特徵設計 / AUC 分析 | P-05, P-06 |

---

## 統計方法陷阱

### P-01: L2 Collider Bias

**錯誤**：對 near-constant 特徵（如 AlleleDelta in LOH regions）做 OLS residualization on AF，產生虛假 AUC 信號（表面 AUC 從 0.50 跳到 0.59）。

**正確做法**：L2 residualized AUC 必須用 L3 AF-bin 交叉驗證。若 L2 與 L3 差距 > 0.10，即為 collider bias，該特徵應判定 CONFOUND。

**來源**：O12 LOH 甲基化場景分析。Memory: `feedback_L2_collider_bias.md`

### P-02: Pooled OLS Residualization Trap

**錯誤**：Pooled OLS（TP+FP 合併後 fit）殘差仍保留分組信息，因為 TP/FP 在特徵空間中佔據不同位置，殘差 = 組間差 + 組內差。

**正確做法**：必須使用 within-group OLS（TP/FP 分別 fit），殘差才真正移除 confound。

**來源**：Beyond-AUC M2 驗證。Memory: `feedback_pooled_ols_residualization_trap.md`

---

## 數據來源陷阱

### P-03: VCF 來源錯誤歸因

**錯誤**：將 canonical VCF 錯誤歸因為 "chenhan112 pipeline"。實際上 canonical TO pipeline VCF 是 liaoyoyo2001 使用 ONT_5kHz BAM（有 5mCG+5hmCG MM/ML）執行 ClairS-TO 產生的。

**正確做法**：確認 VCF 來源時必須追蹤：(1) 誰執行了 caller，(2) 使用哪個 BAM，(3) BAM 是否有 MM/ML tags。查閱 Knowledge/02_samples/ 和 Knowledge/03_file_formats/ 交叉驗證。

**來源**：2026-04-14 TO pipeline staging v2 修正。

### P-04: pileup Symlink 指向錯誤 Caller

**錯誤**：pileup 模式的 output symlink 實際指向 ClairS paired（非 TO），導致 TO 分析使用了 paired caller 的輸出。

**正確做法**：追蹤 symlink 實際目標（`readlink -f`），確認 caller pipeline 與分析模式匹配（TO 分析必須用 ClairS-TO VCF，paired 分析用 ClairS paired VCF）。

**來源**：Memory: `project_vcf_source_error_correction.md`

---

## 特徵分析陷阱

### P-05: CramersV 93% Zero Artifact

**錯誤**：將 CramersV 視為連續區分特徵使用。實際上 CramersV 在 2×2 contingency table（ISM 的標準框架）中只有 {0, 1} 兩個值，93% 的 regions 為 0。

**正確做法**：CramersV 不適合作為連續特徵使用。使用 HPFineNGroups（已克服此限制，AUC 提升 +0.125）作為替代。

**來源**：R1-R5 特徵設計研究。Memory: `project_feature_design_limitations_r1r5.md`

### P-06: n_reads / NumReads Confound

**錯誤**：忽略 read count 對所有統計量的系統性影響。較多 reads → 較高統計功效 → PERMANOVA p-value 更小、HPFineNGroups 更大，但這反映檢測力而非生物效應。

**正確做法**：所有特徵分析必須控制 n_reads（residualize 或分層）。任何 AUC > 0.58 的特徵都需排除 read count confound 後才能判定。

**來源**：O11 heterogeneity 分析。Memory: `project_O11_heterogeneity_negative.md`
