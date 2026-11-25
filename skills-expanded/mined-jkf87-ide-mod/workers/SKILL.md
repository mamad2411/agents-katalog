---
name: workers
description: Show the current Herdr pane's worker tree when the user types /workers or asks which workers this pane supervises.
---

현재 작업반장의 워커 트리를 요청하면 현재 agy 셸의 run_command로 다음 명령을 실행해요.

```sh
node ~/ide-mod/bin/workers.mjs tree --mine
```

출력을 줄바꿈 그대로 코드 블록에 보여 줘요. 오류가 나오면 오류 메시지를 그대로 보여 줘요.
