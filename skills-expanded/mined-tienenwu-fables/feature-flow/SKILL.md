---
name: feature-flow
description: Use when a feature or refactor changes public contracts, schemas, shared integration points, cross-layer data flow, release behavior, or other high-risk architecture decisions.
---

> 🌐 [English version](https://github.com/tienenwu/fables/blob/main/en/feature-flow/SKILL.md) · 繁體中文（正本 / canonical）

# feature-flow — Harness 的 high-risk-feature profile

## 核心原則

本 skill 提供高風險功能的 spec／design／implementation 技巧與 artifact template；Harness 存在時，風險路由、狀態轉移、證據與契約生命週期一律由 Harness 決定。本 skill 不建立第二套狀態機。

若專案沒有 Harness，仍沿用下列 profile，但先建立 risk assessment 與單一產出根目錄 `docs/plans/<slug>/`。

## 何時用

適用：public API／schema／共用整合點、跨層資料流、migration、release、auth／付款／正式資料，或需求歧義與回滾成本都高的功能。

不適用：只因檔案多；低風險機械變更走 quick／standard。若 design 寫不出實質取捨、也沒有絕對升級條件，回 risk router 降級。

## Profile 狀態

### 1. Discovery / Risk

產出 `plan.md` 的 Risk Assessment：命中的 high-risk 絕對條件、quick 條件為何不成立、命中契約、既有可複製模式、外部副作用與驗證限制；不做數字加總。

檔案數只記錄爆炸半徑，不直接決定 profile。

### 2. Spec

產出 `spec.md`：Why、in/out scope、GIVEN-WHEN-THEN AC、假設、非目標與 rollback 條件。

只有昂貴歧義、產品／scope 取捨、public contract、不可逆或外部副作用需要使用者確認。命名與可逆內部選擇自行決定並記假設。

UI/UX 歧義必附 mockup／行為走查／截圖標註，讓錯誤理解在實作前暴露。

### 3. Design / Plan

產出 `plan.md`：架構與資料流、Key Decisions、介面、migration／rollback、phase、每 phase 的驗收，以及每個 AC 預定取得的 evidence。

每個 phase 必須可獨立驗證；若一個 phase 同時跨多個風險面，先拆分。既有同性質 pattern 優先於通用設計。

若有兩個以上工作包，`plan.md` 必須加入 Execution Graph，明列 dependency、writable scope、validation、可平行對象、handoff 與 integration owner。平行實作前先固定 shared contract 與 ownership；寫入重疊或無法安全切分者改為序列執行並記原因。計畫仍須可由單一 agent 依 dependency 執行。

### 4. Implement

可行時，每 phase 先取得會因缺少新行為而失敗的 test／schema check／模擬執行／diff assertion，再做最小實作；不可行時記錄原因與替代的 before／after evidence。機械檢查紅燈不得轉移。

實作推翻設計假設時，在 `plan.md` 加「偏離記錄」與新 evidence plan；不要偷偷改 scope，也不要為了文件一致性維持錯誤設計。

### 5. Verify / Review

`evidence.md` 逐條記 claim→evidence。Executable verifier 親跑 AC、build、test 與 baseline；semantic reviewer 審需求、契約、架構與 scope；auth／資料／release／不可逆面再加 adversarial challenge。

相同模型、相同 prompt、相同 evidence path 不算獨立冗餘。reviewer 從 diff、AC、evidence 與命中契約開始；若能指出明確風險理由，可以擴張唯讀探索並記錄範圍。無 fresh reviewer 時記錄「獨立性受限」，用實跑與 fresh read-back 補足。

### 6. Close

只有所有必要 claim 有證據、無新增 baseline failure、diff scope audit 通過，才能完成。`review.md` 記 residual risks、rollout／rollback 與未做項目。

只有使用者糾正、同類問題再次發生、incident／escaped defect、未文件化的重複限制，或新證據推翻既有契約時才建立 `contract-candidates.md`；沒有觸發事件就不建立空檔。一次觀察只能是 candidate，需再次發生、使用者裁決或事故證據才升 active。

## Evidence 最低要求

- 每個 AC：至少一個 test／command／read-back／manual evidence，含來源與結果。
- 回歸：與開工基線比較，不只寫「全綠」。
- scope：列出變動檔與其對應 task；範圍外既有 bug 另記、不順手修。
- release／實機限定行為：實際環境證據；debug／模擬器不能代替。

## 失敗訊號

- 同一設計假設兩輪仍失敗 → 回 Design，不繼續加例外。
- AC 無法驗證或無法達成 → 回 Spec 調整 scope，需使用者裁決。
- 一個 phase 同時打開多個無關風險面 → 回 Plan 拆分。
- 平行工作包的 shared contract 未固定或 writable scope 重疊 → 回 Plan 建立前置工作包或改為序列執行。
- reviewer 只有意見沒有 evidence gap／失敗情境 → 降為建議，不阻擋轉移。
- 流程同時寫入 `specs/changes/` 與 `docs/plans/` → 停止，選定 `docs/plans/<slug>/` 為 canonical。

## 紅線

- 未經明確授權 push、merge、deploy、刪除或執行不可逆操作。
- 以 reviewer PASS、CI 綠燈或 checklist 勾選代替功能證據。
- 因為「3+ 檔案」就自動使用本 profile。
- 把一次性偏好直接升成 active 契約。

## references 索引

| 檔案 | 何時讀 |
|---|---|
| `references/artifact-templates.md` | 建立實際適用的 `spec.md`／`plan.md`／`evidence.md`／`review.md`／`contract-candidates.md` |
| `references/lessons.md` | 路由拿不準、review 獨立性、設計被推翻或流程成本過高時 |
