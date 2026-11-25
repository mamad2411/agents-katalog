---
name: branch
description: 作業開始時にフィーチャーブランチを作成する。
---

# Branch

作業開始時にブランチを作成して切り替える。

## ブランチ命名規則

形式: `{type}/{short-description}`

| type | 用途 |
|------|------|
| `feat` | 新機能 |
| `fix` | バグ修正 |
| `chore` | 雑務・設定変更 |
| `refactor` | リファクタリング |

例: `feat/add-login`, `fix/null-pointer`

コンテキストからタスク内容を読み取り、ブランチ名を提案してユーザーに確認する。

## 実行

```bash
git checkout -b {branch-name}
```
