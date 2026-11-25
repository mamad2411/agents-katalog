---
name: rag_search
description: 検索クエリー(query) から、RAG検索結果を表示する。
---

## 手順

### STEP 1: 検索クエリー(query)を確認する

* ユーザーに、検索クエリー(query)を質問する:

```
検索クエリー(query) を入力してください。
例: hello
```

### STEP 2: python スクリプトを実行する

* RAG検索から、要約して、検索結果を出力する。

```
python scripts/rag_search.py --query {query}
```

