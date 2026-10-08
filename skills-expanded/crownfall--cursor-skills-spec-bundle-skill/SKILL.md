---
name: spec-bundle
description: Crownfall Task 種別に応じた spec 読み込み Bundle を適用する。Impl 開始時・Task 依頼時に使う。
---

# Spec Bundle Loader

Task 実装前に、種別に応じた spec のみを読む。全文ロード禁止。

正式定義: `docs/specs/implementation/10_Impl依頼テンプレート.md`

## 全 Task 共通（General Start）

**Read**
- `docs/project/CurrentState.md`
- `docs/project/CurrentSprint.md`

**Do Not Read**
- `docs/archives/**`
- `docs/specs/` 全文
- World/Lore（`docs/specs/world/`）— Task 明示要求時のみ

## Bundle 一覧

### Room / Branch / Dungeon Task

**Read**: CODEMAP, `docs/specs/game/05_ダンジョン.md`, 該当 Decision  
**Skip**: アート spec, archives Completed

### Equipment / Loot Task

**Read**: CODEMAP, `docs/specs/game/07_武器_装備.md`, `docs/specs/implementation/03_Resource設計.md`  
**Skip**: ダンジョン spec

### Combat Task

**Read**: CODEMAP, `docs/specs/game/08_戦闘_AI.md`  
**Skip**: archives, アート spec

### ProjectDocs Update Task

**Read**: CurrentState, CurrentSprint, 更新対象 spec のみ

## 手順

1. Task 番号・種別を特定
2. 上記 Bundle の **Read** のみ読む
3. `docs/specs/implementation/CODEMAP.md` で現行コードの実態を確認
4. 仕様不足は推測せず質問
