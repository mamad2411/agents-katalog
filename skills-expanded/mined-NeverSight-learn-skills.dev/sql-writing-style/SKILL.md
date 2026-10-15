---
name: sql-writing-style
description: SQLを書くときに使用する。読み手が一瞥して理解できるSQLを書くためのスタイルルール。
metadata:
  tags: [sql, code-quality, style]
---

# SQL Writing Style

SQLは実行回数より読まれる回数のほうが多い。読み手の認知負荷を最小にする。

各ルールは「見出し（`### 採番. ルールの要旨`）＋1行の理由＋`bad` / `good` の対比例」で書く。ルールを追加するときはこの節構造を踏襲する。

## ルール

### 1. テーブルエイリアスは全文を使う。無意味な短縮をしない

`FROM stores s` のような1文字エイリアスで読み手に逆引きを強いるのは避ける。ただし自己結合や、極端に長いテーブル名で全文表記がかえって読みにくくなる場合は、意味が伝わる短縮エイリアスを許す。

```sql
-- bad
FROM stores s
JOIN users u ON u.store_id = s.id

-- good
FROM stores
JOIN users ON users.store_id = stores.id
```
