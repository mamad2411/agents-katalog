---
name: ide-mod-workers
description: 현재 Herdr 패인이 일을 맡긴 워커 트리를 요청할 때 사용해요.
---

현재 턴의 훅에 ‘ide-mod 워커 트리 조회 결과’가 있으면 그 내용을 그대로 표시하세요. 훅 결과가 없으면 셸에서 다음 명령을 실행하고 출력된 워커 트리를 줄바꿈과 들여쓰기를 유지해서 보여 주세요. 실패하면 오류를 전달하세요.

```sh
node "$(realpath "${CODEX_HOME:-$HOME/.codex}/skills/ide-mod-workers")/../../../bin/workers.mjs" tree --mine
```

셸 샌드박스가 허더 소켓을 차단했다면 이 조회 명령 하나에 대한 권한을 요청하세요.
