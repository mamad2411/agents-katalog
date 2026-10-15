---
name: peach-db-query
description: |
  개발 DB에 SQL을 직접 실행하여 데이터를 조회하는 스킬.
  "DB 확인", "데이터 조회", "테이블 조회", "SQL 실행", "데이터 검증" 키워드로 트리거.
  AI 에이전트가 백엔드/프론트엔드 개발 중 개발 DB 데이터를 즉시 확인할 때 사용.
user-invocable: true
---

# DB 데이터 조회 스킬

## 페르소나

개발 DB 데이터 확인 전문가.
백엔드/프론트엔드 개발 및 테스트 중 실제 DB 데이터를 즉시 확인하여 개발 진행을 돕는다.

---

## ⚠️ 안전 규칙 (절대 준수)

### Tier 1 — 직접 실행 (SELECT)

- SELECT 쿼리만 AI가 직접 실행하고 결과를 반환한다
- **LIMIT 100 기본 적용** — 미지정 시 자동 추가
- 고급 패턴(Window Function, CTE, JSONB 등)은 [query-patterns.md](references/query-patterns.md) 참조

### Tier 2 — SQL 제시만 (INSERT / UPDATE / DELETE)

- AI는 **SQL을 생성하여 보여주기만** 한다 — 직접 실행하지 않는다
- 사용자가 직접 CLI에서 실행하도록 안내한다
- 제시 형식:

```
⚠️ DML — 직접 실행이 필요합니다
─────────────────────
SQL:   UPDATE [테이블] SET status = 'A' WHERE [테이블]_seq = 42;
대상:  [테이블] 테이블
조건:  PK 단건 (WHERE [테이블]_seq = 42)

확인용 SELECT:
SELECT * FROM [테이블] WHERE [테이블]_seq = 42;

실행 방법:
PGPASSWORD='[pw]' psql -h [host] -p [port] -U [user] -d [db] -c "위 SQL"
─────────────────────
```

### Tier 3 — 절대 금지 (DDL)

- DROP / ALTER / TRUNCATE / CREATE — **SQL 생성 자체를 하지 않는다**
- 요청 시 응답: "DDL은 마이그레이션으로 처리해야 합니다. `/peach-db-migrate` 스킬을 사용하세요."

### 환경 제한

- **개발 환경만 허용** — `env.local.yml` 또는 `env.dev.yml` 접속 정보만 사용
- **프로덕션 접속 금지** — `env.prod.yml` DATABASE_URL 사용 절대 금지

---

## CLI 설치 전략 (OS별)

**PostgreSQL (psql)**

| OS | 전략 | 명령 |
|----|------|------|
| macOS | brew 직접 설치 (Docker 불필요) | `brew install libpq` + PATH 등록 |
| Linux | 패키지 매니저 | `apt-get install -y postgresql-client` |
| Windows | Docker fallback | `docker run --rm postgres:16 psql ...` |

**MySQL (mysql)**

| OS | 전략 | 명령 |
|----|------|------|
| macOS | brew 직접 설치 (Docker 불필요) | `brew install mysql-client` + PATH 등록 |
| Linux | 패키지 매니저 | `apt-get install -y mysql-client` |
| Windows | Docker fallback | `docker run --rm mysql:8 mysql ...` |

> **macOS에서 Docker 사용 금지** — brew가 훨씬 빠르고 이후에도 재사용 가능.
> Docker 이미지 최초 다운로드는 postgres:16 ~300MB, mysql:8 ~500MB로 불필요한 대기가 발생한다.
> 설치 상세 절차 및 PATH 설정 → [cli-설치-가이드.md](references/cli-설치-가이드.md)

---

## 프리플라이트: CLI 확인 + 자동 설치

### Step P-1: OS 감지

```bash
uname -s   # Darwin=macOS / Linux / MINGW64_NT=Windows
```

### Step P-2: CLI 확인 및 설치

**macOS — CLI 직접 설치 (강력 권장, Docker 사용 금지)**

```bash
# psql 확인
which psql && psql --version || echo "psql 없음"

# mysql 확인
which mysql && mysql --version || echo "mysql 없음"
```

psql 없음 → 사용자에게 설치 승인 요청 후 자동 실행:

```bash
brew install libpq
echo 'export PATH="/opt/homebrew/opt/libpq/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
# 현재 세션 즉시 적용
export PATH="/opt/homebrew/opt/libpq/bin:$PATH"
psql --version   # 설치 확인
```

> **libpq keg-only 주의**: brew가 libpq를 keg-only로 설치하므로 반드시 PATH에 추가해야 함.
> PATH 추가 없이 `psql` 실행 시 "command not found" 발생.
> `~/.zshrc` 등록으로 영구 적용 + `export` 명령으로 현재 세션 즉시 적용.

mysql 없음 → 사용자에게 설치 승인 요청 후 자동 실행:

```bash
brew install mysql-client
echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"
mysql --version   # 설치 확인
```

**Linux (Ubuntu/Debian) — 패키지 매니저로 설치**

```bash
sudo apt-get install -y postgresql-client   # PostgreSQL
sudo apt-get install -y mysql-client        # MySQL
```

**Windows (Git Bash) — Docker fallback (CLI 설치 불가 환경 전용)**

> Docker fallback은 **Windows 전용**. macOS/Linux는 CLI 설치가 간단하므로 Docker 사용 금지.

```bash
# Docker 설치 확인 (선행 필수)
docker --version && echo "Docker 사용 가능" || echo "Docker 없음 — CLI 직접 설치 필요"
```

PostgreSQL (Docker):
```bash
# URL의 특수문자는 인코딩 유지 (env.local.yml의 URL 그대로 사용)
docker run --rm postgres:16 psql \
  "postgresql://[user]:[encoded_password]@[host]:[port]/[dbname]" \
  -c "[SQL]" 2>/dev/null
```

MySQL (Docker):
```bash
# -p'password' — 특수문자 포함 시 반드시 따옴표로 감싸기
docker run --rm mysql:8 mysql \
  -h [host] -P [port] -u [user] -p'[password]' [dbname] \
  -e "[SQL]" 2>/dev/null
```

> **주의**: `2>/dev/null`은 Docker pull 진행 메시지를 숨긴다.
> 최초 실행 시 이미지 다운로드(postgres:16 ~300MB, mysql:8 ~500MB)가 발생할 수 있다.
> 이후 실행은 캐시로 1~2초 내 시작된다.

---

## 워크플로우

### Step 1: DB 종류 판별

**Node/Java 프로젝트 — env.yml에서 DATABASE_URL 탐지:**
```bash
grep "DATABASE_URL" api/src/environments/env.local.yml 2>/dev/null || \
grep "DATABASE_URL" api/env.local.yml 2>/dev/null
```

- `postgresql://` → PostgreSQL 모드
- `mysql://` → MySQL 모드

**PHP 프로젝트 — conf.php에서 db_* 변수 탐지:**
```bash
# 우선 탐색 경로
grep "db_host\|db_port\|db_dbname\|db_user\|db_password\|db_division" src/cfg/conf.php 2>/dev/null || \
grep "db_host\|db_port\|db_dbname\|db_user\|db_password\|db_division" cfg/conf.php 2>/dev/null || \
# fallback: 전체 탐색
find . -name "conf.php" | xargs grep -l "db_host" 2>/dev/null | head -1 | \
  xargs grep "db_host\|db_port\|db_dbname\|db_user\|db_password\|db_division" 2>/dev/null
```

- `db_division = 'pdo'` 또는 `'mysqli'` → MySQL 모드
- `db_division = 'postgresql'` → PostgreSQL 모드
- 상세 패턴은 [php-project-db-접속.md](references/php-project-db-접속.md) 참조

### Step 2: 접속 정보 파싱

DATABASE_URL에서 host, port, user, password, dbname 추출.

예시 URL 파싱:
```
postgresql://peach:peach%21%25%23@dev.mng.dien.co.kr:55432/peach
→ host=dev.mng.dien.co.kr, port=55432, user=peach, password=peach!%# (URL 디코딩), db=peach
```

URL 인코딩 디코딩: `%21` → `!`, `%25` → `%`, `%23` → `#`

### Step 3: SQL 실행

**PostgreSQL:**
```bash
PGPASSWORD='[password]' psql -h [host] -p [port] -U [user] -d [db] -c "[SQL]"
```

**MySQL:**
```bash
mysql -h [host] -P [port] -u [user] -p'[password]' [db] -e "[SQL]"
```

### Step 4: 결과 해석

결과를 분석하여 개발 맥락에서 의미 있는 정보를 전달한다.

---

## 자주 사용하는 조회 패턴

자세한 패턴은 [query-patterns.md](references/query-patterns.md) 참조.

---

## 출력 포맷

psql 기본 테이블 포맷 사용 (가독성 최고):

```
 column1 | column2 | column3
---------+---------+---------
 value1  | value2  | value3
(N rows)
```

컬럼 수가 많아 가로로 긴 경우 `-x` 확장 모드 사용:
```bash
PGPASSWORD='...' psql ... -x -c "[SQL]"
```
