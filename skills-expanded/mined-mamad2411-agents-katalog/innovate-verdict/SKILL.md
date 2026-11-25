---
name: innovate-verdict
description: "創新 Phase 4：可行性裁定、評分、記錄到 innovation_log、銜接後續。Use when 'innovation verdict', '裁定', 'feasibility score', '可行性評估'."
allowed-tools: Read, Edit, Bash
---

# /innovate-verdict — 可行性裁定

讀 `docs/innovation_state.json` 取得完整探索歷程。

## Step 1: 綜合評分

| 維度 | 分數 (1-5) | 備註 |
|------|-----------|------|
| Alpha 潛力 | | [CAR/hit rate 數據] |
| 技術可行性 | | [實作難度] |
| 數據可得性 | | [數據來源穩定性] |
| 與現有系統整合 | | [需改多少模組] |
| 維護成本 | | [長期可持續性] |
| **總分** | **/25** | |

## Step 2: 裁定

| 分數 | 裁定 | 動作 |
|------|------|------|
| >= 20 | **FAST-TRACK** | 立即進入 `/research` 做正式研究（分配 RB 編號） |
| 15-19 | **PROMISING** | 排入 Sprint Roadmap |
| 10-14 | **SHELVE** | 記錄想法，等條件成熟 |
| < 10 | **PASS** | 不適合，記錄原因 |

## Step 3: 記錄到 Innovation Log

追加到 `docs/innovation_log.md`：

```markdown
## [DATE] Innovation: [Topic]

**Direction**: [OPTIMIZE/TRANSFER/DISCOVER/FRONTIER]
**Verdict**: [FAST-TRACK/PROMISING/SHELVE/PASS]
**Score**: [X/25]

### Key Findings
- [最重要的發現]

### POC Results
- [關鍵數據，如有]

### References
- [論文/Repo/討論連結]

### Next Steps
- [ ] [後續動作]
```

## Step 4: 銜接

### FAST-TRACK
建議用戶：
> 建議執行 `/research "具體假說"` 進入正式研究循環，分配 RB-[XXX] 編號。

### PROMISING
- 記錄到 Sprint Roadmap 的 Discovery Track
- 設定重訪日期

### SHELVE
- 存檔，設定重訪條件
> "當 [條件] 成熟時，值得重新探索。"

### PASS
- 記錄原因，避免未來重複探索

## Step 5: 清理狀態

更新 `docs/innovation_state.json`：
```json
{
  "status": "completed",
  "verdict": "[FAST-TRACK/PROMISING/SHELVE/PASS]",
  "score": N,
  "completed_at": "[DATE]"
}
```

向用戶報告最終裁定。
