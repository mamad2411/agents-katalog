---
name: todo_delete
description: TODO(やる事) 削除APIにID送信する。
---

## 手順

### STEP 1: TODO(やる事)削除IDを確認する

* ユーザーに、削除ID(ID)を質問する:

```
削除 (ID) を入力してください。
例: 1
```

### STEP 2: python スクリプトを実行する

```
python scripts/todo_delete.py --id {id}
```

