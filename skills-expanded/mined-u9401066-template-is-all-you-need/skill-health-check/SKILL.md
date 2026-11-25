---
name: skill-health-check
description: Check health, freshness, and consistency of all Skills, copilot-instructions.md, chatmodes, and bylaws. Triggers: SHC, health, 健康檢查, skill check, freshness, 翻新, 過期, stale, 檢查 skill, instruction check, audit skills, 技能檢查.
version: 1.0.0
category: maintenance
compatibility:
  - claude-code
  - github-copilot
  - vscode
  - codex-cli
dependencies: []
allowed-tools:
  - read_file
  - list_dir
  - grep_search
  - run_in_terminal
  - get_errors
---

# Skill & Instruction 健康檢查

## 描述

全面檢查專案中所有 Skills、Copilot Instructions、Chatmodes 和 Bylaws 的健康度、一致性和新鮮度。
這是一個**自省型 Skill**，讓 Copilot 能檢查自己的設定是否需要翻新。

## 觸發條件

- 「檢查 skill 健康度」「SHC」「skill health check」
- 「翻新 skill」「檢查過期」「audit skills」
- 「instruction check」「技能檢查」

---

## 🔧 操作步驟

### Step 1: 掃描 Skill 目錄結構

```
list_dir(".claude/skills/")
```

對每個 skill 子目錄：
1. 檢查 `SKILL.md` 存在
2. 讀取 frontmatter 驗證必要欄位
3. 記錄版本號與最後修改時間

**必要 frontmatter 欄位**：
- `name` — skill 識別名稱
- `description` — 包含觸發詞的描述
- `version` — 語義化版本
- `category` — 類別分類
- `compatibility` — 支援的平台列表
- `allowed-tools` 或 `dependencies` — 工具/依賴宣告

### Step 2: 檢查 copilot-instructions.md 同步性

```
read_file(".github/copilot-instructions.md")
```

比對：
- Instructions 中的 Skill 表格 vs 實際 `.claude/skills/` 目錄
- 觸發詞是否一致
- 是否有 instructions 中提到但不存在的 skill
- 是否有存在但未在 instructions 中登記的 skill

### Step 3: 驗證 Chatmode 健康

```
list_dir(".github/")  # 找 *.chatmode.md
```

檢查：
- frontmatter 格式正確
- `tools` 列表使用有效名稱
- description 是否有意義
- 是否有重複功能的 chatmode

### Step 4: Bylaws 一致性

```
list_dir(".github/bylaws/")
```

- bylaws 提及的 skill 名稱是否與實際一致
- CONSTITUTION.md 的原則是否被 skill 遵守

### Step 5: 依賴圖分析

解析所有 skill 的 `dependencies` 和 `orchestrates` 欄位：
- 繪製依賴關係
- 找出斷裂的依賴（宣告了但不存在的）
- 找出循環依賴
- 找出孤立的 skill（沒有被任何 workflow 引用）

### Step 6: 新鮮度評估

| 條件 | 狀態 |
|------|------|
| 90 天內更新 | 🟢 新鮮 |
| 90-180 天 | 🟡 建議檢查 |
| > 180 天 | 🔴 需要翻新 |

### Step 7: 自動修復建議

根據發現的問題，提供可選的自動修復：
- 更新 copilot-instructions.md 的 skill 表格
- 補齊缺少的 frontmatter 欄位
- 建議過期 skill 的更新方向

---

## 📊 輸出格式

```markdown
# 🏥 Skill & Instruction 健康報告

📅 檢查日期：YYYY-MM-DD
📁 Skills 位置：.claude/skills/

---

## 📊 總覽

| 指標 | 值 |
|------|-----|
| Skills 總數 | XX |
| 結構完整 | XX/XX ✅ |
| 版本新鮮 | XX 新鮮 / XX 過期 |
| 指令同步 | ✅ 同步 / ⚠️ 不同步 |
| 依賴完整 | ✅ 完整 / ❌ 斷裂 |

---

## 🗂️ Skill 清單

| Skill | 版本 | 類別 | 新鮮度 | 狀態 |
|-------|------|------|--------|------|
| git-precommit | v2.2.0 | workflow | 🟢 | ✅ |
| code-reviewer | v2.2.0 | quality | 🟢 | ✅ |
| ... | | | | |

---

## ✅ 健康項目
1. ...

## ⚠️ 需要關注
1. ...

## ❌ 需要修復
1. ...

---

## 🔗 依賴圖

```
git-precommit (workflow)
├── memory-updater
├── readme-updater
├── changelog-updater
├── roadmap-updater
└── ddd-architect

code-review-workflow (workflow)
├── code-reviewer
├── security-reviewer
├── test-generator
└── ddd-architect

feature-development (workflow)
├── ddd-architect
├── code-reviewer
├── test-generator
└── memory-updater
```

---

## 📋 建議行動

### 自動可修復
- [ ] 更新 copilot-instructions.md skill 表格
- [ ] 補齊 XXX skill 的 frontmatter

### 需要人工處理
- [ ] 翻新 XXX skill（已過期 XX 天）
- [ ] 更新 XXX skill 以匹配新版 VS Code API
```

---

## 🔄 與其他 Skills 關係

| 觸發場景 | 動作 |
|----------|------|
| `git-precommit` | 在 commit 前透過 hook 快速檢查 |
| `skill-generator` | 新 skill 建立後自動觸發同步檢查 |
| 定期維護 | 建議每月執行一次完整健康檢查 |

---

## 💡 VS Code Copilot 翻新檢查要點

以下是 Copilot 演進中可能影響 skill 的變更：

| 功能 | 檢查項目 |
|------|----------|
| Agent Mode | chatmode.md 是否使用 `agent` 而非舊的 `mode` |
| Prompt Files | .prompt.md 是否使用正確的 frontmatter |
| Tools | tools 列表是否使用當前有效的工具名稱 |
| Instructions | .instructions.md 是否遵循最新格式 |
| Skills | SKILL.md frontmatter 是否需要新增欄位 |

---

## ⚠️ 注意事項

1. **不會自動修改 skill 內容** — 只產生報告和建議
2. **修改前確認** — 自動修復建議需要用戶確認
3. **版本控制** — 修改後更新 skill 的 version 欄位
4. **回歸測試** — 翻新 skill 後用 `skill-generator` 驗證格式
