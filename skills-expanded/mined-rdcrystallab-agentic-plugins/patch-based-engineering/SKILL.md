---
name: patch-based-engineering
description: Use when a downstream customization exists as a patch, commit range, or custom branch and needs to become a reusable reconstruction workflow. Extract feature intent into specs/patches.md, reapply from spec, and validate the spec with a clean-baseline spec-only pass. 中文觸發詞：『把這個 patch 變成 spec』、『重建這個客製化』、『從 commit range 抽出需求』、『驗證 patches.md 能不能獨立重做』、『spec-only reapply』等。
---

# Patch-Based Engineering

把一次性的 patch 變成未來可重建的工程能力。

## 目標

當你面對的是「下游客製化會持續跟 upstream 漂移」的問題，真正要保留的不是某次 diff，而是：

1. 這組修改想恢復什麼行為
2. 邊界在哪裡
3. 未來怎麼在乾淨 baseline 上穩定重做

這個 skill 的預設 artifact 都放在 `specs/`：

- `specs/patches.md`：前向規格，給未來重建用
- `specs/patched.md`：本次實作 ledger，記錄事實與驗證

## 什麼時候用

- 手上有 `changes.patch`、某段 commit range，或一條舊 custom branch
- patch 已經不能直接套用，但功能仍要持續保留
- 想把 scattered edits 收斂成幾個 `feature-xx`
- 想驗證 spec 本身，不只驗證這次 code 恰好能跑

## 什麼時候不要用

- 只是要保留一次性的 hotfix diff
- patch 內容非常小，且未來不會跟 upstream 長期演進
- 你已經有完整、可維護的上游 feature branch，不需要再做 spec-first 重建

## 兩份文件的分工

| 檔案 | 角色 | 應包含 |
|------|------|--------|
| `specs/patches.md` | forward spec | scope, required behavior, non-goals, implementation anchors, test plan |
| `specs/patched.md` | delivery ledger | changed files, restored behavior, validation results, gaps / ambiguities |

**不要**把這兩份文件混寫。`patches.md` 不是 diff summary；`patched.md` 也不是 wish list。

## 建議流程

### 1. Extract spec

先從 patch / commit range 抽 feature intent，去掉 incidental changes，寫成 `specs/patches.md`。

使用：

```text
/patch-based-engineering:extract-patch-spec <patch-file|commit-range|branch>
```

### 2. Reapply from spec

根據 `specs/patches.md` 在目前 baseline 上重建功能，並把本次實際落地情況寫進 `specs/patched.md`。

使用：

```text
/patch-based-engineering:reapply-patch-spec
```

### 3. Validate the spec

在乾淨 baseline 上做一次 **spec-only reapply**。驗證對象不是原始 patch，而是 `specs/patches.md` 是否足以引導重建。

使用：

```text
/patch-based-engineering:validate-patch-spec <baseline-ref>
```

## 何時用 agent

如果你要的是完整 workflow，而不是單一步驟，直接用 `patch-based-engineering` agent。它會決定何時該：

- 先抽 spec
- 再重建
- 最後跑 clean-baseline validation

## 寫 spec 的硬規則

1. 以 `feature-xx` 為單位，不要以檔名為單位
2. 先寫 intent，再寫 implementation anchors
3. Required behavior 要包含成功、失敗、fallback、相容性邊界
4. Test plan 要同時有 automated expectations、manual scenarios、acceptance rule
5. 明確列出 non-goals，避免未來回補時 scope 膨脹

## 驗證 spec 的硬規則

1. clean baseline 必須看不到原本的 customized implementation
2. spec-only pass 只能把 `specs/patches.md` 當 source of truth
3. 若重建結果漂掉，應回頭補強 spec，而不是直接放寬驗證標準
4. 修改面若大量擴散，代表 implementation anchors 或 scope 還不夠清楚
