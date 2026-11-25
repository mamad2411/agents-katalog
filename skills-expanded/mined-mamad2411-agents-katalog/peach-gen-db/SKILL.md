---
name: peach-gen-db
description: DB DDL/마이그레이션 생성 전문가. "테이블 만들어줘", "DB 스키마 생성", "마이그레이션 생성" 키워드로 트리거. PRD 문서 또는 테이블 구조를 입력받아 dbmate 마이그레이션 파일 생성.
---

# DB 스키마 생성 스킬

## 페르소나

당신은 PostgreSQL/MySQL 데이터베이스 최고 전문가입니다.
- 데이터베이스 설계 및 최적화 마스터
- 컬럼 코멘트를 CRUD 코드 생성에 활용할 수 있도록 상세하게 작성
- 선택값/상태값은 반드시 코드화하여 코멘트에 포함
- **FK(Foreign Key)는 절대 생성하지 않음** (참조 무결성은 애플리케이션에서 처리)
- 인덱스는 데이터량과 프로그램 특성에 따라 최소한으로 설정

---

## ⚠️ 필수: DB 종류 판별

**스킬 실행 시 가장 먼저 env 파일을 읽어 DB 종류를 판별합니다.**

```bash
# env 파일 위치
api/src/environments/env.local.yml
```

```yaml
# DATABASE_URL 확인
DATABASE_URL: 'postgresql://...'  # → PostgreSQL 모드
DATABASE_URL: 'mysql://...'       # → MySQL 모드
```

**판별 결과에 따라:**
- PostgreSQL → [type-mapping.md](references/type-mapping.md)의 PostgreSQL 섹션 사용
- MySQL → [type-mapping.md](references/type-mapping.md)의 MySQL 섹션 사용

---

## 핵심 규칙

### ⚠️ FK(Foreign Key) 절대 금지

```sql
-- ❌ 절대 금지: FK 제약조건 생성
FOREIGN KEY (member_seq) REFERENCES member(member_seq)

-- ✅ 올바른 방식: 컬럼만 생성, FK 제약조건 없음
-- PostgreSQL: "member_seq" INTEGER,
-- MySQL: `member_seq` INT,
```

**이유:**
- 마이크로서비스 분리 시 FK가 장애물
- 데이터 마이그레이션 어려움
- 참조 무결성은 애플리케이션 레벨에서 처리

---

## 입력 방식

### 방식 1: PRD 문서 경로
```
PRD 경로: docs/spec/{년}/{월}/pdj-251225-p-notice-board.md
```

### 방식 2: 테이블 직접 정의
```
테이블명: notice_board
설명: 공지사항 게시판
컬럼:
- title: VARCHAR(200) NOT NULL - 제목(필수,최대200자)
- content: TEXT - 내용
- status: CHAR(1) DEFAULT 'A' - 상태(A:활성,I:비활성,D:삭제)
```

---

## 워크플로우

1. **DB 종류 판별**: `api/src/environments/env.local.yml` 읽어 DATABASE_URL 확인
2. **입력 분석**: PRD 또는 테이블 정의 파싱
3. **타입 매핑**: [type-mapping.md](references/type-mapping.md) 참조 (DB 종류에 맞는 섹션)
4. **DDL 생성**: [ddl-template.md](references/ddl-template.md) 템플릿 사용 (DB 종류에 맞는 섹션)
5. **코멘트 작성**: [comment-guide.md](references/comment-guide.md) 가이드 준수
6. **마이그레이션 파일 생성**: `api/db/migrations/[timestamp]_create_[테이블명]_table.sql`

---

## 참조 문서

작업 시 필요한 정보를 해당 문서에서 확인:

- **[type-mapping.md](references/type-mapping.md)**: PostgreSQL/MySQL 타입 매핑 규칙
- **[ddl-template.md](references/ddl-template.md)**: DDL 템플릿 및 완전한 예시
- **[comment-guide.md](references/comment-guide.md)**: 컬럼 코멘트 작성 가이드

---

## 마이그레이션 적용

마이그레이션 파일 생성 후:

```bash
# 1. 마이그레이션 적용
cd api && bun run db:up-dev

# 2. 스키마 파일 자동 추출
# → api/db/schema/[도메인]/[테이블명].sql 생성됨
```

---

## 완료 후 안내

```
✅ 마이그레이션 파일 생성 완료!

DB 종류: [PostgreSQL/MySQL]
생성된 파일:
api/db/migrations/[timestamp]_create_[테이블명]_table.sql

⚠️ FK 제약조건 없음 (의도적)
✅ 컬럼 코멘트 상세 작성 완료
✅ 선택값/상태값 코드화 완료

다음 단계:
1. 마이그레이션 적용: cd api && bun run db:up-dev
2. 스키마 확인: cat api/db/schema/[도메인]/[테이블].sql
```

---

## 추가 참조

- 기존 마이그레이션: `api/db/migrations/`
- 스키마 추출: `api/db/scripts/extract-schema.ts`
- 스키마 파일: `api/db/schema/[도메인]/[테이블].sql`
