---
name: pull-update
description: 외부에서 가져온 페르소나의 원본 리포에서 최신 업데이트를 가져올 때 호출.
allowed-tools: Read, Bash, Grep
---

# Pull Update from Origin

import된 페르소나의 원본 GitHub 리포에서 최신 변경사항을 가져온다.

## 절차

### 1. 현재 상태 확인
```bash
git status
git log --oneline -5
git remote -v
```

### 2. 로컬 변경사항 보존
```bash
# 커밋되지 않은 변경사항이 있으면 먼저 커밋
git add -A
git commit -m "Save local changes before update" 2>/dev/null || true
```

### 3. 업데이트 가져오기
```bash
git fetch origin
git merge origin/master --no-edit || git merge origin/main --no-edit
```

### 4. 충돌 발생 시
- 충돌 파일 목록을 사용자에게 보여주고
- 각 충돌을 수동으로 해결
- `git add <resolved-file>` → `git commit`

### 5. 업데이트 후 보안 점검 제안
업데이트 완료 후 사용자에게 물어보기:
> "업데이트가 완료되었습니다. 새로 추가된 코드의 보안 점검을 진행할까요?"

Yes인 경우 `/security-review` 스킬 호출.

### 6. import-meta.json 업데이트
```bash
# 현재 HEAD 커밋 해시로 installedCommit 업데이트
git rev-parse HEAD
```
`import-meta.json`의 `installedCommit` 필드를 새 해시로 업데이트.
