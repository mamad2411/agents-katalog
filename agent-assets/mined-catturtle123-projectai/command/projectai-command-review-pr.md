---
description: PR을 리뷰하고 피드백 제공
---

# /review-pr - PR 리뷰 명령어

PR을 리뷰하고 피드백을 제공합니다.

## 사용법

```
/review-pr <PR번호>
/review-pr <PR_URL>
```

## 입력

- PR URL 또는 번호: $ARGUMENTS

## 리뷰 항목

1. **코드 품질**: Kotlin 컨벤션 준수 여부
2. **아키텍처**: 레이어 분리 원칙 준수
3. **에러 처리**: AppException + ErrorCode 사용
4. **테스트**: TDD 원칙, AAA 패턴
5. **보안**: SQL Injection, XSS 등 보안 이슈
6. **성능**: N+1 쿼리, 불필요한 DB 호출

## 리뷰 절차

1. `gh pr diff $ARGUMENTS`로 변경사항 확인
2. 변경된 파일별 코드 리뷰
3. `.claude/skills/code-quality-guard/skill.md` 코드 리뷰 체크리스트 기반 검증
4. 피드백 작성 및 제출
