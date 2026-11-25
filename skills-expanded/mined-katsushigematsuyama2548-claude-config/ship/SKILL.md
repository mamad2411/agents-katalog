---
name: ship
description: 作業完了時にコミット・プッシュ・PR作成を行う。
---

# Ship

作業完了時の commit → push → PR 作成 → main 戻りを一括実行する。

## 前提

- `.claude/` は**常にコミット対象外**（専用リポジトリで管理するため）
- 除外方法: プロジェクトの `.gitignore` に `.claude/` を含める

## 手順

### 1. 変更確認

```bash
git status
git diff
```

### 2. ステージング（.claude/ を除外）

```bash
git add .
git restore --staged .claude/
```

`.gitignore` に `.claude/` が入っていれば `restore` は不要だが、念のため実行する。

### 3. コミット

コンテキストと変更差分から適切なコミットメッセージを生成する。

```bash
git commit -m "{message}"
```

### 4. プッシュ

```bash
git push -u origin HEAD
```

### 5. PR 作成

CLAUDE.md のリポジトリ情報を参照してタイトル・本文を生成する。

```bash
gh pr create --title "{title}" --body "{body}" --base main
```

### 6. main に戻る

```bash
git checkout main
```
