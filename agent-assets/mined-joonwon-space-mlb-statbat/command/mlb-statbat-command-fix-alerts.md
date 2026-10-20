---
description: docs/alerts/ 의 미처리 알림을 읽고 원인을 파악해 코드를 수정한다.
---

# Fix Alerts

`docs/alerts/` 에 쌓인 로그 알림 파일을 읽고, 원인을 분석해 코드를 수정한다.

## 사용법

```
/fix-alerts               → 미처리 알림 전체 처리
/fix-alerts critical      → Critical 항목만 처리
```

## 워크플로우

1. `docs/alerts/*.md` 파일 목록 수집
2. 심각도별 정렬 (Critical → Warning)
3. 각 이슈의 추정 원인과 관련 소스 파일 확인
4. 코드 수정 후 로컬 검증
5. 커밋 + push
6. CI 결과 확인
7. 알림 파일에 처리 결과 기록

## 이슈 유형별 확인 포인트

**LLM API 오류**
- `backend/app/text_to_sql.py` — 프롬프트, 모델 설정, 에러 처리
- API 키 유효성, rate limiting 확인

**DB 오류**
- `backend/app/database.py` — 커넥션 풀 설정
- docker compose ps로 postgres 컨테이너 상태 확인

**SQL 생성 오류**
- `backend/app/text_to_sql.py` — SQL 검증 로직
- 생성된 SQL의 안전성 확인

**500 Internal Server Error**
- 해당 엔드포인트 핸들러 확인
- 예외 처리 누락 여부 확인
