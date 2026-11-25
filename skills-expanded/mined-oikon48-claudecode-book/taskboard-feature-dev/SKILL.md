---
name: taskboard-feature-dev
description: TaskBoardに新機能をTDDで追加するときに使用する。失敗するテストを先に書き、状態管理を整え、UIを更新し、最後にブラウザで動作を確認するまで一貫した手順で進める。
---

TaskBoardに機能を追加するときは、以下の順で進めてください。

1. 追加する機能のユーザー操作を確認する
2. 失敗するテストを先に追加する
3. `useTaskBoard` に状態管理を集約する
4. 既存コンポーネントの責務分担を変えずにUIを更新する
5. `npm run test:run` と `npm run build` で検証する
6. 必要に応じてPlaywright MCPで画面操作を確認する
