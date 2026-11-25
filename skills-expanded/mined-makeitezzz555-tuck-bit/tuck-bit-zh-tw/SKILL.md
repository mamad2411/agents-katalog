---
name: tuck-bit-zh-tw
description: "TuckBit 是專為程式設計代理打造的可攜式技能，協助選擇適當的脈絡、工具與驗證步驟，不犧牲正確性。"
license: MIT
compatibility: Portable Agent Skills; project-scoped install only.
metadata:
  author: TuckBit contributors
  version: "0.4.0"
  locale: zh-TW
---

# TuckBit — 繁體中文

> 核心技能檔案已翻譯；技術參考資料暫時維持英文，仍需社群審閱。

最佳化每單位資源所產生的正確且經過驗證的結果，而非單純減少 token 數量。

四項預設能力：登錄、脈絡、驗證及預算。協作編排和指標屬於選用功能。

## 標準工作流程

從使用者的確切要求、實際可用的指示及已授權工具出發。保留所有限制、核准事項及必要檢查。

1. 定義目標、限制、風險及停止條件；簡單工作不需要冗長規劃。
2. 精準找出相關程式碼、文件或工具，只有需要時才擴大搜尋範圍。
3. 優先使用主機內建的工具探索功能；中繼資料僅是線索，絕不是執行授權。
4. 小型任務使用單一代理；只有在責任和驗收條件明確時，才分派獨立工作。
5. 先執行針對性測試，再對最終版本完成所有必要的整合及安全檢查。
6. 提供可驗證的變更、測試、風險及阻礙紀錄。善用檢查點，避免無止盡輪詢。

## 只載入相關參考資料

- `references/task-contract.md` — task contracts / host instructions.
- `references/workflows.md` — Fast / Standard / Deep workflows.
- `references/registry.md` — discovery and permission limits.
- `references/context.md` — source-linked evidence and checkpoints.
- `references/verification.md` — tests and integration checks.
- `references/budget.md` — bounded iterations.
- `references/orchestration.md` — optional independent agents.
- `references/metrics.md` — optional evaluation.

## 強制遵守的界線

不得略過安全檢查、降低正確性、捏造數據、讀取憑證、繞過核准或執行未獲授權的破壞性操作。權限仍由主機管理。

**開發者預覽版。安裝本身無法證明技能已啟用，也不保證節省 token。**
