---
name: research-log
description: "研究 Phase 5：結論判定、寫入 research_log、後續動作。Use when 'log research', '記錄結論', 'research conclusion'."
allowed-tools: Read, Edit, Bash
---

# /research-log — 結論 + 記錄

讀 `docs/research_state.json` 取得完整研究歷程。

## Step 1: 判定結果

| 結論 | 條件 |
|------|------|
| **ADOPT** | Primary metric 達標 + 偏差快篩全 PASS + guardrails 通過 |
| **ITERATE** | 方向正確但未達標，需調整後重測 |
| **REJECT** | 未達標或發現根本問題 |
| **INCONCLUSIVE** | 資料不足或結果模糊 |

## Step 2: 寫入 Research Log

追加到 `docs/research_log.md`：

```markdown
## [DATE] RB-[XXX]: [Topic]

**Hypothesis**: [一句話]
**Type**: [ALPHA/SIGNAL/DATA/TIMING]
**Result**: [ADOPT/ITERATE/REJECT/INCONCLUSIVE]

### Setup
- Baseline: [描述]
- Treatment: [描述]
- Data period: [start] to [end]
- Sample size: [N trades]
- Branch: `research/<topic>`

### Key Findings
| Metric | Baseline | Treatment | Delta | p-value |
|--------|----------|-----------|-------|---------|
| ... | ... | ... | ... | ... |

### Bias Screen
[5 checks all PASS / FAIL details]

### Conclusion
[2-3 句總結]

### Next Steps
- [ ] [後續動作]
```

## Step 3: 後續動作

### If ADOPT
```bash
git checkout main
git merge research/<topic>
git push
```
- 更新 MEMORY.md 的 Alpha Research Key Findings
- 更新 Sprint Roadmap 對應 RB 狀態
- 整合到信號系統（如適用）

### If ITERATE
- 記錄學到什麼
- 列出下一輪調整變數
- 建議重跑 `/research-scope` 或 `/research-design`

### If REJECT
- 記錄失敗原因
- 清理 research branch（詢問用戶）

### If INCONCLUSIVE
- 記錄不確定原因
- 建議補充什麼數據或延長測試

## Step 4: 清理狀態

更新 `docs/research_state.json`：
```json
{
  "status": "completed",
  "result": "[ADOPT/ITERATE/REJECT/INCONCLUSIVE]",
  "completed_at": "[DATE]"
}
```

向用戶報告最終結論。
