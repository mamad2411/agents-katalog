---
description: 최근 1시간 서버 로그를 분석해 이상 징후를 감지하고 docs/alerts/에 저장한다.
---

# Log Check

최근 1시간 백엔드 로그를 분석해 이상 징후를 감지한다.
이상이 있으면 `docs/alerts/YYYY-MM-DD-HH.md`에 저장하고 수정을 요청한다.
이상이 없으면 아무것도 하지 않고 조용히 종료한다.

## 로그 수집

```bash
docker compose logs backend --since 1h --no-log-prefix 2>/dev/null
```

## 이상 징후 감지 기준

### Critical (즉시 수정 필요)
- ERROR 레벨 로그
- DB 연결 실패: `sqlalchemy`, `asyncpg`, `connection refused`
- LLM API 오류: Anthropic/OpenAI API 에러
- SQL injection 시도 패턴
- 500 Internal Server Error 3회 이상

### Warning (주의 필요)
- WARNING 레벨 로그
- LLM API 재시도 발생
- 응답 지연: text-to-SQL 타임아웃
- 잘못된 SQL 생성 패턴

## 알림 파일

이상 감지 시 `docs/alerts/YYYY-MM-DD-HH.md`에 저장.
이상 없으면 조용히 종료.
