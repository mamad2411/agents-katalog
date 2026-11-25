---
name: peach-db-migrate
description: |
  dbmate 마이그레이션 전체 관리 스킬. 상태 확인, 실행(up), 롤백(down), 새 마이그레이션 생성을 처리.
  "마이그레이션 실행", "DB 업", "DB 다운", "마이그레이션 상태", "마이그레이션 생성",
  "dbmate", "migration", "테이블 변경 적용", "스키마 반영", "DB 롤백" 키워드로 트리거.
  DB 마이그레이션과 관련된 어떤 요청이든 이 스킬을 사용하라.
---

# DB 마이그레이션

모든 명령은 `api/` 디렉토리에서 실행한다.

## 워크플로우

### 1단계: 현재 상태 확인 (항상 먼저 실행)

어떤 작업이든 시작 전에 현재 마이그레이션 상태를 확인한다.

```bash
cd api && bun run db:status-dev
```

사용자에게 적용된 마이그레이션 목록과 미적용 마이그레이션을 보여준다.

### 2단계: 의도에 따라 분기

#### 상태 확인만 요청한 경우
→ 1단계 결과를 보여주고 종료.

#### 마이그레이션 실행 (up)
```bash
cd api && bun run db:up-dev
```
- dbmate 마이그레이션 실행 후 `extract-schema`가 자동 실행된다.
- 스키마 파일(`db/schema/`)이 자동 갱신된다.
- 결과를 보여주고, 변경된 스키마 파일 목록을 안내한다.

#### 마이그레이션 롤백 (down)
```bash
cd api && bun run db:down-dev
```
- **실행 전 반드시**: 롤백 대상 마이그레이션 파일명을 보여주고, 사용자 승인을 받은 후 실행한다.
- 가장 최근 마이그레이션 1건만 롤백된다.
- 롤백 후 `extract-schema`가 자동 실행된다.

#### 새 마이그레이션 생성
```bash
cd api && bun run db:new {migration_name}
```
- `db/migrations/YYYYMMDDHHMMSS_{migration_name}.sql` 파일이 생성된다.
- 생성된 파일을 열고, 아래 템플릿 구조를 안내한다:

```sql
-- migrate:up


-- migrate:down

```

### 3단계: 결과 보고

실행 결과를 요약하고, 오류 발생 시 원인을 분석한다.

## 파일 위치

| 경로 | 용도 |
|------|------|
| `api/db/migrations/` | 마이그레이션 파일 |
| `api/db/schema/` | 추출된 스키마 파일 |
| `api/db/dev.env` | DB 연결 정보 |

## 오류 대응

| 증상 | 원인 | 해결 |
|------|------|------|
| 연결 실패 | DATABASE_URL 오류 또는 DB 서버 다운 | `api/db/dev.env` 확인, DB 서버 상태 점검 |
| already applied | 마이그레이션이 이미 적용됨 | `db:status-dev`로 현재 상태 확인 후 안내 |
| SQL syntax error | 마이그레이션 파일 문법 오류 | 오류 메시지의 라인/컬럼 정보로 파일 수정 |
| index already exists | 중복 인덱스 생성 시도 | `CREATE INDEX IF NOT EXISTS`로 변경 또는 기존 인덱스 확인 |
