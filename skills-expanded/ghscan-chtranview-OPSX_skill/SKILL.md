---
name: opsx-sdd
description: 'OpenSpec OPSX 變更生命週期管理。使用 /opsx-sdd 查看路由表、/opsx-explore 探索需求、/opsx-propose 建立提案、/opsx-apply 實作任務、/opsx-verify 驗證實作、/opsx-archive 歸檔變更。適用於任何專案的 spec-driven 開發流程。Use when: user types opsx-sdd, opsx-explore, opsx-propose, opsx-apply, opsx-verify, opsx-archive, or wants structured change management.'
metadata:
  author: opsx-sdd
  version: "1.0"
---

# OpenSpec OPSX · Spec-Driven 變更生命週期管理

以一個入口指令與五個階段指令，驅動 AI 執行從探索、提案、實作、驗證到歸檔的完整變更管理流程。
AI 直接操作檔案系統管理 `openspec/` 目錄結構，不依賴外部 CLI。

---

## 指令路由表

當使用者輸入 `/opsx-sdd` 時，直接輸出以下路由表：

| 指令 | 用途 | 用法範例 | 詳細指引 |
|------|------|---------|----------|
| `/opsx-sdd` | 入口 — 顯示本路由表並引導下一步 | → 輸入 `/opsx-sdd` 或 `/opsx-sdd <描述>` | 本文件（[SKILL.md](./SKILL.md)） |
| `/opsx-explore` | 思考夥伴 — 探索想法、調查問題、釐清需求（不寫程式碼） | → 輸入 `/opsx-explore <主題>` | [explore.md](./references/explore.md) |
| `/opsx-propose` | 建立變更提案 — 一步到位生成 proposal / specs / design / tasks | → 輸入 `/opsx-propose <change-name>` | [propose.md](./references/propose.md) |
| `/opsx-apply` | 任務實作 — 逐一執行 tasks.md 中的待辦事項並標記完成 | → 輸入 `/opsx-apply <change-name>` | [apply.md](./references/apply.md) |
| `/opsx-verify` | 三維度驗證 — Completeness / Correctness / Coherence | → 輸入 `/opsx-verify <change-name>` | [verify.md](./references/verify.md) |
| `/opsx-archive` | 歸檔變更 — 同步 delta specs 並移至 archive | → 輸入 `/opsx-archive <change-name>` | [archive.md](./references/archive.md) |

## 流程總覽

```
 explore        propose                    apply          verify         archive
┌──────────┐  ┌────────────────────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ 想清楚    │─→│ 初始化結構 + 寫計畫     │─→│ 逐一實作  │─→│ 三維檢核  │─→│ 正式歸檔  │
│（可跳過） │  │ openspec/              │  │          │  │（可跳過） │  │          │
└──────────┘  └────────────────────────┘  └──────────┘  └──────────┘  └──────────┘
                                                │               │
                                                └───← 修復 ←────┘
```

**最小路徑：** `propose → apply → archive`
**完整路徑：** `explore → propose → apply → verify → archive`

> **與 OpenSpec CLI 的差異**
> - 本 skill 在 `<workspace>/<name>/` 下建立 `openspec/`（支援一個 workspace 多個子專案）；OpenSpec CLI 預設在專案根目錄直接建立 `openspec/`。
> - 未提供獨立 `/opsx-sync` 指令；delta spec 同步併入 `/opsx-archive`（OpenSpec 官方 sync 為可選獨立步驟）。

### OpenSpec 目錄建立規則

`/opsx-propose` 會在 `<workspace>/<name>/` 下建立並操作 `openspec/` 結構，
所有後續指令都共用此結構：

```
<workspace>/
└── <name>/                              ← 專案根目錄（propose 時建立）
    ├── openspec/                        ← OPSX artifacts（propose 時建立）
    │   ├── config.yaml
    │   ├── specs/
    │   └── changes/
    │       ├── <name>/                  ← 活躍變更（proposal / specs / design / tasks）
    │       └── archive/                 ← 歸檔後移至 YYYY-MM-DD-<name>/
    └── (原始碼)                          ← apply 時在此寫程式碼
```

---

## Artifacts 結構

`/opsx-propose` 在 `<workspace>/<name>/` 建立專案目錄，所有 artifacts 位於其中的 `openspec/` 下：

```
<workspace>/
└── <name>/                                  ← 專案根目錄
    ├── openspec/
    │   ├── config.yaml                      ← 專案配置（schema 設定）
    │   ├── specs/                           ← 主規格（source of truth）
    │   │   └── <capability>/spec.md
    │   ├── changes/                         ← 變更（活躍 + 歸檔）
    │   │   ├── <name>/                      ← 活躍變更
    │   │   │   ├── .openspec.yaml            ← 變更元資料（schema, dates）
    │   │   │   ├── proposal.md               ← 提案（Intent / Scope / Approach）
    │   │   │   ├── design.md                ← 技術設計（Architecture / Decisions）
    │   │   │   ├── tasks.md                 ← 實作清單（checkbox-based）
    │   │   │   └── specs/                   ← Delta specs
    │   │   │       └── <capability>/spec.md ← ADDED / MODIFIED / REMOVED / RENAMED
    │   │   └── archive/                     ← 已歸檔變更
    │   │       └── YYYY-MM-DD-<name>/
    └── (原始碼)                              ← apply 時在此目錄寫程式碼
```

| Artifact | 內容 | 用途 |
|----------|------|------|
| `.openspec.yaml` | 元資料（schema, dates） | 變更索引 |
| `proposal.md` | Intent / Scope / Approach | WHY + WHAT |
| `specs/` | Delta specs（`### Requirement:` + `#### Scenario:`） | 結構化行為規格（**必要**） |
| `design.md` | Architecture / Decisions / Tradeoffs | HOW |
| `tasks.md` | checkbox 任務清單 `- [ ]` / `- [x]` | 實作追蹤 |

**Artifact 產出順序**：`proposal` → `specs` → `design` → `tasks`，每個 artifact 依賴前置 artifact。

**Delta specs 重要性**：`specs/` 是 spec-driven schema 的核心。
它定義系統「應該做什麼」，提供可追蹤的需求與可測試的場景，
並在歸檔時同步至主規格（`<workspace>/<name>/openspec/specs/`）作為 source of truth。

---

## 檔案系統操作（無 CLI 依賴）

此 skill 不依賴 OpenSpec CLI。AI 直接操作檔案系統。
所有路徑相對於**專案根目錄** `<workspace>/<name>/`：

| 操作 | 方式 |
|------|------|
| **建立專案目錄** | 建立 `<workspace>/<name>/` 作為專案根目錄 |
| **初始化 openspec** | 在 `<workspace>/<name>/openspec/` 建立結構（config.yaml + specs/ + changes/） |
| **列出活躍 changes** | 讀取 `<workspace>/<name>/openspec/changes/`，排除 `archive/` 子目錄 |
| **建立新 change** | 建立 `<workspace>/<name>/openspec/changes/<name>/` 並寫入 `.openspec.yaml` |
| **檢查狀態** | 讀取 `<workspace>/<name>/openspec/changes/<name>/.openspec.yaml` 並檢查各 artifact 是否存在 |
| **取得 artifact 規則** | 依 schema（spec-driven）的慣例決定 artifact 內容結構 |
| **實作程式碼** | 在 `<workspace>/<name>/`（專案根目錄）下撰寫原始碼 |
| **歸檔** | 將 `<workspace>/<name>/openspec/changes/<name>/` 移至 `<workspace>/<name>/openspec/changes/archive/YYYY-MM-DD-<name>/` |
| **同步 specs** | 讀取 delta specs，按 RENAMED→REMOVED→MODIFIED→ADDED 順序合併至 `<workspace>/<name>/openspec/specs/` |

### .openspec.yaml 格式

```yaml
schema: spec-driven
name: <change-name>
created: "YYYY-MM-DD"
status: active          # active | archived
artifacts:
  proposal: pending     # pending | done
  specs: pending        # pending | done
  design: pending       # pending | done
  tasks: pending        # pending | done
```

### 初始化專案與 openspec 結構

`/opsx-propose` 執行時，在主工作目錄下建立專案目錄與 openspec 結構：

```
<workspace>/<name>/              ← 專案根目錄
└── openspec/
    ├── config.yaml              ← schema: spec-driven
    ├── specs/                   ← 空目錄
    └── changes/                 ← 空目錄
```

`config.yaml` 預設內容：

```yaml
schema: spec-driven
```

---

## 全域設定

| 設定 | 值 |
|------|-----|
| 輸出語言 | zh-TW |
| Schema | spec-driven |
| 日期格式 | YYYY-MM-DD |
| 編碼 | UTF-8 |

---

## YAML Pipeline 參考

結構化的 YAML 流程定義位於 [references/yaml/](./references/yaml/)，作為 AI 執行各指令的補充參考（`/opsx-sdd` 入口直接使用本文件，無獨立 YAML）：

- [_index.yaml](./references/yaml/_index.yaml) — 指令路由索引與工作流程定義
- [opsx-explore.yaml](./references/yaml/opsx-explore.yaml) — 探索模式結構化定義
- [opsx-propose.yaml](./references/yaml/opsx-propose.yaml) — 提案流程結構化定義
- [opsx-apply.yaml](./references/yaml/opsx-apply.yaml) — 實作流程結構化定義
- [opsx-verify.yaml](./references/yaml/opsx-verify.yaml) — 驗證流程結構化定義
- [opsx-archive.yaml](./references/yaml/opsx-archive.yaml) — 歸檔流程結構化定義

---

## Spec 格式（行為規格）

Delta specs 採用行為規格格式：

```markdown
### Requirement: [需求名稱]

[SHALL/MUST/SHOULD 聲明]

#### Scenario: [場景描述]

- **GIVEN** [前置條件]
- **WHEN** [觸發動作]
- **THEN** [預期結果]
```

---

## 三維度驗證

| 維度 | 檢查內容 | 問題嚴重度 |
|------|---------|-----------|
| **Completeness** | tasks 完成度、spec 需求覆蓋 | 🔴 CRITICAL |
| **Correctness** | 實作與 spec 意圖一致、場景覆蓋 | 🟡 WARNING |
| **Coherence** | 遵循 design 決策、模式一致 | 🔵 SUGGESTION |
