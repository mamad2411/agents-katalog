---
name: ide-mod-handoff
description: 현재 Codex 세션의 대화 기록 주소와 재개 명령을 요청할 때 사용해요.
---

셸에서 다음 명령을 실행하고 출력 두 줄을 그대로 답하세요. 첫 줄에 파일 경로만 놓으세요. 실패하면 오류를 전달하세요.

```sh
node "$(realpath "${CODEX_HOME:-$HOME/.codex}/skills/ide-mod-handoff")/../../../bin/codex-handoff.mjs"
```
