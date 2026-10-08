---
name: rsun-user-stories
description: 將 PRD 功能需求拆解為 INVEST 標準的 User Stories，並撰寫 Given/When/Then 驗收標準（Acceptance Criteria）。當 Sprint 規劃前、開發啟動前需要拆解工作時使用。
user-invocable: true
allowed-tools: "Read Write"
---

# rsun-user-stories — 用戶故事 + 驗收標準

User Stories 是開發團隊與 PM 之間的共同語言。好的 User Story 讓開發者知道「誰要用、用來幹嘛、什麼叫做完成」，同時保留實作自由度。

**適用時機：**
- PRD 確認後，開發 Sprint 啟動前
- 工作包太大需要拆細時
- 需要明確定義「完成的標準」（Definition of Done）時

---

## INVEST 標準（好 User Story 的 6 個條件）

寫完每個 User Story 後，用這 6 個標準檢查：

| 字母 | 意義 | 問自己 |
|------|------|--------|
| **I** | Independent（獨立）| 這個 story 可以單獨開發嗎？不依賴其他 story？ |
| **N** | Negotiable（可議）| 這是需求，不是合約；實作方式可以討論 |
| **V** | Valuable（有價值）| 這對用戶或業務有什麼具體價值？ |
| **E** | Estimable（可估算）| 開發者看到這個能估工時嗎？ |
| **S** | Small（夠小）| 一個 Sprint（2 週）內能完成嗎？拆不拆？ |
| **T** | Testable（可測試）| 有辦法驗證「完成了」嗎？ |

---

## User Story 格式

### 標準格式

```
身為 [用戶角色]，
我希望 [執行某個動作或獲得某個功能]，
以便 [達到某個目的或解決某個問題]。
```

### 角色定義（在同一個專案中要一致）

先定義專案中的所有角色，再開始寫 stories：

```
- [角色 A]：[一句話描述這個角色]
- [角色 B]：[一句話描述這個角色]
- [系統]：有時候 story 的主詞是「系統」（排程、通知等）
```

### 常見錯誤

❌ 「身為用戶，我希望系統很快」→ 這是非功能需求，不是 story
❌ 「身為工程師，我希望建立 API endpoint」→ 角色應該是業務用戶，不是工程師
❌ 太大的 story：「身為用戶，我希望完成整個結帳流程」→ 需要拆成多個 stories

---

## Acceptance Criteria（驗收標準）

每個 User Story 必須有 **Given/When/Then** 格式的驗收標準。

### Given/When/Then 格式

```
Given [前提條件，用戶的當前狀態或系統的初始狀態]
When [用戶執行的動作]
Then [預期的結果]
```

### 寫法要求

- 一個 Story 可以有多個 scenario（正常路徑 + 例外處理）
- 使用**具體的數字和狀態**，不用模糊詞（不要說「快速」，要說「3 秒內」）
- **一定要包含 Edge Case**（空值、無權限、超時、重複提交）

### 範例

**User Story：**
> 身為仲介，我希望篩選特定州別的物件，以便快速找到我負責的區域。

**Acceptance Criteria：**
```
Scenario 1：正常篩選
  Given 我在物件列表頁
  When 我選擇「Victoria」作為州別篩選
  Then 列表只顯示 state = "Victoria" 的物件
  And 篩選條件顯示在篩選欄，方便識別當前條件

Scenario 2：無結果
  Given 我在物件列表頁
  When 我選擇某個沒有物件的州別
  Then 顯示「此區域目前無物件」的提示
  And 提供「清除篩選」的操作

Scenario 3：多選篩選
  Given 我選擇了 2 個州別（Victoria + NSW）
  When 列表載入
  Then 顯示這兩個州的所有物件，合計正確
```

---

## User Story Map（大功能的組織方式）

當功能較大時，用三層結構組織：

```
Epic（史詩）
├── Feature（功能）
│   ├── User Story 1
│   ├── User Story 2
│   └── User Story 3（with Acceptance Criteria）
└── Feature（功能）
    └── ...
```

**Epic：** 一個大的業務目標（如「物件管理」、「用戶認證」）
**Feature：** Epic 下的功能群組（如「物件刊登」、「物件搜尋」）
**Story：** 具體的可開發單元（符合 INVEST）

---

## 輸出格式（Sprint 準備清單）

```markdown
# User Stories — [專案名稱] Sprint [N]

**日期：** YYYY-MM-DD
**對應 PRD：** [PRD 連結]

---

## Epic: [Epic 名稱]

### Feature: [功能名稱]

---

#### Story [編號]：[簡短標題]

**Story：**
> 身為 [角色]，我希望 [功能]，以便 [目的]。

**優先級：** P0 / P1 / P2
**複雜度：** S / M / L（對應估價 WBS 等級）
**預估工時：** [X hr]

**Acceptance Criteria：**

```
Scenario 1：[場景名]
  Given ...
  When ...
  Then ...

Scenario 2：[例外場景]
  Given ...
  When ...
  Then ...
```

**技術備注：** [工程師需要知道的實作限制，選填]
**UI 參考：** [Figma 連結 / 截圖，選填]

---

[重複上述格式]

---

## INVEST 自查表

- [ ] 所有 Story 都可以獨立開發？
- [ ] 沒有 Story 超過 40hr（L 等級）？
- [ ] 每個 Story 都有至少 2 個 Acceptance Criteria Scenario？
- [ ] Edge Case 都有對應的 Scenario？
- [ ] 優先級都標注了？
```

---

## 與估價的關係

User Stories 是估價的精細化版本：

```
WBS 工作包（rsun-estimate）
  ↓ 開發前細化
User Stories（rsun-user-stories）
  ↓ 開發中追蹤
Sprint 任務（Jira / Linear / Notion）
```

- WBS 的「複雜度 M = 16-40hr」的工作包，通常拆成 3-5 個 User Stories
- Acceptance Criteria 是 QA 測試的依據
- Story 的 Estimable 估算應和 WBS Buffer 工時一致

---

## 注意事項

- **不要跳過 Edge Case**：「無資料時顯示什麼」「無權限時跳哪裡」是開發中最容易被遺忘的
- **Acceptance Criteria 不是 UI 規格**：不要在 AC 裡說「按鈕是藍色的」，那是設計稿的工作
- **技術備注 ≠ 實作規格**：只寫工程師必須知道的業務限制，不要替工程師設計實作
