---
name: peach-add-cron
description: |
  주기적 실행 Cron 작업 코드를 생성하는 스킬. node-cron 기반 TypeScript Service + 로그 기록 + server.ts 통합.
  "크론 작업", "주기적 실행", "스케줄러 생성" 키워드로 트리거.
---

# Cron 작업 코드 생성

## 페르소나

당신은 백그라운드 작업 스케줄링 최고 전문가입니다.
- node-cron 기반 스케줄러 마스터
- 적응형 스케줄링 알고리즘 설계
- Cron 로깅 및 모니터링 전문가
- 에러 복구 및 재시도 로직 구현

## 입력 정보 수집

사용자로부터 다음 정보 수집:

1. **모듈명** (필수): kebab-case (예: `log-cleanup`, `sms-result-processor`)
2. **작업 설명** (필수): 크론 작업이 수행할 내용
3. **실행 주기** (필수):
   - Cron expression (예: `'0 2 * * *'` → 매일 새벽 2시)
   - 또는 한글 설명 (예: "매일 새벽 2시", "1분마다")
4. **스케줄러 타입**:
   - **고정 스케줄**: node-cron 기본 (시간 기반)
   - **적응형 스케줄**: 백그라운드 무한 루프 (데이터 양 기반)

## 생성 프로세스

### 1. 참조 패턴 확인

#### 적응형 스케줄러인 경우
[sms-result-pattern.md](references/sms-result-pattern.md) 읽고 핵심 패턴 파악:
- 무한 루프 백그라운드 실행
- 적응형 대기 시간 조정
- Cron 로그 기록
- 치명적 에러 처리

#### server.ts 통합
[server-integration.md](references/server-integration.md) 읽고 등록 패턴 파악:
- node-cron 사용법
- Cron expression 작성
- 시간대 설정

### 2. 파일 생성

생성 위치: `api/src/modules/{{module-name}}/`

#### Service 파일 (`service/{{module-name}}.service.ts`)
- [cron-service-template.ts](assets/cron-service-template.ts) 참조
- 적응형 스케줄러 로직
- Cron 로그 기록
- 서버 정보 수집
- 에러 처리 (치명적/일반)

#### DAO 파일 (`dao/{{module-name}}.dao.ts`)
- `countPending()`: 미처리 건수 조회
- `findPending()`: 미처리 항목 조회
- `insertCronLog()`: Cron 로그 생성
- `updateCronLog()`: Cron 로그 업데이트

#### server.ts 통합 코드
- [server-cron-integration.ts](assets/server-cron-integration.ts) 참조
- import문 추가
- `start{{SchedulerMethodName}}()` 메서드 추가
- `koaServer()` 메서드 내에서 호출

### 3. 템플릿 변수 치환

템플릿의 변수를 실제 값으로 치환:
- `{{MODULE_NAME}}`: 모듈명 (kebab-case)
- `{{ServiceClassName}}`: Service 클래스명 (PascalCase)
- `{{DaoClassName}}`: DAO 클래스명 (PascalCase)
- `{{JOB_NAME}}`: 작업명 (kebab-case)
- `{{SchedulerMethodName}}`: 스케줄러 메서드명 (PascalCase)
- `{{작업 설명}}`: 작업 설명 (한글)
- `{{cron-expression-description}}`: 실행 주기 설명

### 4. Cron Expression 변환

한글 설명을 Cron expression으로 변환:

| 한글 설명 | Cron Expression | 설명 |
|-----------|-----------------|------|
| 5초마다 | `'*/5 * * * * *'` | 5초 간격 |
| 1분마다 | `'0 * * * * *'` | 매분 0초 |
| 매일 새벽 2시 | `'0 2 * * *'` | 매일 02:00:00 |
| 매주 일요일 자정 | `'0 0 * * 0'` | 일요일 00:00:00 |
| 매월 1일 자정 | `'0 0 1 * *'` | 매월 1일 00:00:00 |

### 5. common_log_cron 테이블 생성

Cron 로그 저장을 위한 테이블 생성 (없는 경우):

```sql
CREATE TABLE common_log_cron (
  log_seq INT AUTO_INCREMENT PRIMARY KEY,
  job_name VARCHAR(100) NOT NULL,
  job_type VARCHAR(20) NOT NULL,       -- 'auto' / 'manual'
  start_time DATETIME NOT NULL,
  end_time DATETIME,
  duration INT,                         -- 실행 시간 (초)
  status VARCHAR(20) NOT NULL,          -- 'running' / 'success' / 'failed'
  processed_count INT DEFAULT 0,
  success_count INT DEFAULT 0,
  failed_count INT DEFAULT 0,
  error_message TEXT,
  error_stack TEXT,
  server_info VARCHAR(200),             -- IP|hostname|pid|version|platform
  detail_log TEXT,                      -- JSON 상세 로그
  insert_seq INT NOT NULL,
  insert_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_seq INT,
  update_date DATETIME
);
```

### 6. server.ts 수동 통합

생성된 [server-cron-integration.ts](assets/server-cron-integration.ts) 코드를 server.ts에 수동으로 추가:

1. import문을 파일 상단에 추가
2. `start{{SchedulerMethodName}}()` 메서드를 Server 클래스에 추가
3. `koaServer()` 메서드 내 스케줄러 시작 부분에 호출 추가

## 출력

생성된 파일 경로와 통합 안내:
1. 생성된 Service 파일 경로
2. 생성된 DAO 파일 경로
3. server.ts에 추가할 코드 (코드 블록으로 표시)
4. 테스트 실행 방법

## 예시

```
사용자: "매일 새벽 2시에 오래된 로그를 삭제하는 크론 작업 만들어줘"

생성 결과:
- api/src/modules/log-cleanup/service/log-cleanup.service.ts
- api/src/modules/log-cleanup/dao/log-cleanup.dao.ts
- server.ts 통합 코드

실행 주기: 매일 새벽 2시 (0 2 * * *)
시간대: Asia/Seoul
```

## 검증 단계

```bash
# 타입 체크
cd api && bun run build

# 린트 체크
cd api && bun run lint:fixed

# Cron 로그 테이블 존재 확인
# common_log_cron 테이블이 없으면 생성 안내
```

## 완료 조건

- [ ] bun run build 성공
- [ ] bun run lint:fixed 통과
- [ ] server.ts 통합 코드 제공
- [ ] common_log_cron 테이블 확인/생성 안내
