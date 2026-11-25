---
name: git-pull-commit-push
description: Executes git pull, git commit, and git push at the end of a task when the user asks for "깃풀커푸".
---

# 깃풀커푸 (Git Pull, Commit, Push)

사용자가 "깃풀커푸"를 지시하면, 모든 작업이 완료된 후 최종적으로 다음 작업을 수행해야 합니다:

1. `git pull` (원격 저장소의 최신 변경사항을 가져와 병합)
2. `git add .` (모든 변경사항 스테이징)
3. `git commit -m "Auto-commit by Antigravity: [작업 내용 요약]"` (적절한 커밋 메시지 작성)
4. `git push` (원격 저장소에 푸시)

이 작업은 해당 태스크의 맨 마지막에 수행되어야 하며, 터미널 명령을 통해 실행하여 성공 여부를 확인해야 합니다.
오류가 발생하면 오류를 해결하고 다시 시도하세요.
