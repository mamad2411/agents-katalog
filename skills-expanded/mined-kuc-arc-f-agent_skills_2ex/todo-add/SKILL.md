---
name: todo_add
description: TODO(やる事) を、APIに送信する。
---

## 手順

### STEP 1: 送信メッセージ(message)を確認する

* ユーザーに、送信メッセージ(message)を質問する:

```
TODO送信メッセージ(message) を入力してください。
例: hello
```

### STEP 2: python スクリプトを実行する

```
python scripts/todo_add.py --message {message}
```

