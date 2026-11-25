---
name: code-audit
description: Deep comprehensive code audit across quality, security, architecture compliance, test coverage, and documentation sync. Triggers: AUDIT, 審計, audit, 全面審查, deep review, 深度審查, 健檢, health check, 程式碼審計, codebase audit, 完整檢查, full check.
version: 1.0.0
category: quality
compatibility:
  - claude-code
  - github-copilot
  - vscode
  - codex-cli
orchestrates:
  - code-reviewer
  - security-reviewer
  - test-generator
  - ddd-architect
  - skill-health-check
dependencies:
  - code-reviewer
  - security-reviewer
allowed-tools:
  - read_file
  - grep_search
  - semantic_search
  - get_errors
  - run_in_terminal
  - list_dir
---

# 深度程式碼審計

## 描述

對整個程式庫進行系統性的深度審計，涵蓋程式碼品質、安全性、架構合規性、測試覆蓋率和文檔同步度。比 `code-reviewer`（單檔審查）和 `code-review-workflow`（PR 審查）更全面，適合定期健檢。

## 觸發條件

- 「程式碼審計」「AUDIT」「全面審查」
- 「deep review」「深度審查」「健檢」
- 「codebase audit」「完整檢查」

## 法規依據

- 憲法：CONSTITUTION.md 第一章（DDD 架構）
- 子法：bylaws/ddd-architecture.md
- 子法：bylaws/git-workflow.md

---

## 🔧 審計流程（5 大維度）

### Phase 1: 🏗️ 架構合規性審計

**目標**：驗證 DDD 分層架構是否被正確遵守

```powershell
# 檢查目錄結構
Get-ChildItem -Path src/ -Directory -Recurse | Select-Object FullName
```

**檢查清單**：

| 項目 | 檢查方式 | 嚴重度 |
|------|----------|--------|
| Domain 層無外部依賴 | `grep_search` Domain 層的 import | 🔴 Critical |
| Repository Interface 在 Domain | 檢查 interfaces 位置 | 🔴 Critical |
| 依賴方向正確 | 分析 import 圖 | 🔴 Critical |
| Application 層不過度膨脹 | 計算行數 | 🟡 Medium |
| Presentation 只呼叫 Application | 檢查 import | 🟠 High |

```python
# 偵測 Domain 層違規 import 的搜尋模式
# ❌ Domain 層不應出現這些：
import_violations = [
    "from fastapi",
    "from flask",
    "from sqlalchemy",
    "from django",
    "import requests",
    "from infrastructure",
    "from presentation",
]
```

### Phase 2: 📊 程式碼品質審計

**自動化工具**：

```powershell
# Ruff - 全面 linting
uv run ruff check src/ --output-format=grouped --statistics

# Ruff - 格式檢查
uv run ruff format --check src/

# MyPy - 型別安全
uv run mypy src/ --ignore-missing-imports --show-error-codes

# Vulture - 死碼偵測
uv run vulture src/ --min-confidence 80

# 圈複雜度
uv run ruff check src/ --select=C901 --output-format=concise
```

**人工檢查項目**：

| 指標 | 閾值 | 工具 |
|------|------|------|
| 函數長度 | < 50 行 | grep + 人工 |
| 類別大小 | < 300 行 | grep + 人工 |
| 圈複雜度 | McCabe < 10 | ruff C901 |
| 重複程式碼 | 無明顯重複 | semantic_search |
| 命名一致性 | snake_case/CamelCase | ruff |
| 型別覆蓋率 | 公開 API 100% | mypy |

### Phase 3: 🔒 安全性審計

**呼叫 `security-reviewer` skill 執行 OWASP Top 10 檢查**

```powershell
# Bandit - 靜態安全分析
uv run bandit -r src/ -ll -f txt

# 依賴漏洞
uv run pip-audit 2>/dev/null || echo "pip-audit 未安裝"

# Secrets 偵測
git log --all --diff-filter=A -- "*.env" "*.key" "*.pem" 2>/dev/null || true
```

**額外安全檢查**：

```
grep_search("password|secret|api_key|token|private_key", src/)
grep_search("pickle\.load|yaml\.load|eval\(|exec\(", src/)
grep_search('f"SELECT|f"INSERT|f"UPDATE|f"DELETE', src/)
```

### Phase 4: 🧪 測試覆蓋率審計

**呼叫 `test-generator` 的分析能力**

```powershell
# 執行測試並產生覆蓋率
uv run pytest tests/ \
    --cov=src \
    --cov-report=term-missing \
    --cov-fail-under=80 \
    -q --no-header 2>/dev/null || echo "pytest 未配置"
```

**測試品質評估**：

| 指標 | 標準 |
|------|------|
| 覆蓋率 | ≥ 80% |
| Domain 層覆蓋 | ≥ 90% |
| 邊界測試 | 有 |
| 錯誤路徑測試 | 有 |
| 整合測試 | 有（獨立標記） |

### Phase 5: 📚 文檔同步審計

**檢查所有文檔是否與程式碼同步**：

| 文檔 | 檢查方式 |
|------|----------|
| README.md | 功能列表 vs 實際 src/ |
| CHANGELOG.md | 最新版本是否有記錄 |
| ARCHITECTURE.md | 架構描述 vs 實作 |
| Memory Bank | 上次更新時間 |
| API 文檔 | 端點 vs 路由定義 |

```powershell
# 檢查 Memory Bank 最後更新
git log -1 --format="%ai" -- memory-bank/ 2>/dev/null
```

---

## 📊 審計報告格式

```markdown
# 🔬 程式碼審計報告

📅 審計日期：YYYY-MM-DD
📁 審計範圍：src/, tests/
🔍 審計師：AI Assistant

---

## 🎯 評分總覽

| 維度 | 分數 | 等級 | 說明 |
|------|------|------|------|
| 🏗️ 架構合規 | ?/10 | 🟢🟡🔴 | ... |
| 📊 程式碼品質 | ?/10 | 🟢🟡🔴 | ... |
| 🔒 安全性 | ?/10 | 🟢🟡🔴 | ... |
| 🧪 測試覆蓋 | ?/10 | 🟢🟡🔴 | ... |
| 📚 文檔同步 | ?/10 | 🟢🟡🔴 | ... |
| **總分** | **?/50** | | |

### 評分標準
- 🟢 8-10：優秀，無重大問題
- 🟡 5-7：可接受，有改進空間
- 🔴 0-4：亟需改善

---

## 🔴 Critical Issues（阻擋級）
> 必須在下次 release 前修復

1. ...

## 🟠 High Issues（重要）
1. ...

## 🟡 Medium Issues（改進）
1. ...

## 🟢 Positive Findings（優點）
1. ...

---

## 📈 趨勢分析

與上次審計比較（如有記錄）：
- 架構合規：↑ / → / ↓
- 品質分數：↑ / → / ↓
- 測試覆蓋：XX% → XX%

---

## 📋 改進行動計畫

### 立即（本週）
- [ ] ...

### 短期（本月）
- [ ] ...

### 長期（本季）
- [ ] ...

---

## 📝 審計備註
- 審計結果已記錄至 memory-bank/decisionLog.md
- 下次建議審計日期：YYYY-MM-DD
```

---

## 🎮 使用方式

| 指令 | 效果 |
|------|------|
| `「審計」`或 `「AUDIT」` | 完整 5 維度審計 |
| `「快速審計」` | 僅執行自動化工具 |
| `「審計 安全性」` | 僅 Phase 3 安全審計 |
| `「審計 架構」` | 僅 Phase 1 架構審計 |
| `「審計 測試」` | 僅 Phase 4 測試覆蓋 |

---

## 🔄 與其他 Skills 的關係

```
code-audit (審計編排器)
├── code-reviewer (品質審查)
├── security-reviewer (安全審查)
├── test-generator (測試分析)
├── ddd-architect (架構驗證)
└── skill-health-check (自身健康)
```

| 情境 | 動作 |
|------|------|
| 發現安全問題 | 調用 security-reviewer 深入分析 |
| 發現架構違規 | 調用 ddd-architect 提供修正建議 |
| 測試不足 | 調用 test-generator 生成測試 |
| 品質問題 | 調用 code-refactor 提供重構方案 |
| 審計完成 | 調用 memory-updater 記錄結果 |

---

## ⚠️ 注意事項

1. **全面審計可能耗時**：大型專案建議分 Phase 執行
2. **首次審計設定基線**：記錄分數作為後續比較基準
3. **記錄到 Memory Bank**：審計結果寫入 decisionLog.md
4. **不自動修改**：審計只產生報告，修復由專門 Skill 負責
5. **定期執行**：建議每月或每個 milestone 後執行
