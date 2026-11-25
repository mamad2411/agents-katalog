---
name: peach-db-extract-schema
description: |
  DB 스키마 추출 스킬. DB의 현재 상태를 테이블별 DDL 파일로 추출하여 schema/ 폴더에 저장.
  "스키마 추출", "스키마 업데이트", "extract-schema", "DB 스키마 동기화",
  "스키마 파일 갱신", "DB 구조 확인", "DDL 추출", "스키마 최신화" 키워드로 트리거.
  스키마 파일과 실제 DB 상태가 다를 수 있다고 판단되면 이 스킬을 사용하라.
---

# DB 스키마 추출

마이그레이션 없이 **DB의 현재 상태를 스키마 파일로 재추출**한다.

> `bun run db:up-dev` / `db:down-dev` 실행 시에는 extract-schema가 자동 체이닝되므로,
> 이 스킬은 **수동 추출이 필요할 때만** 사용한다.

## 워크플로우

### 1단계: 스키마 추출 실행

```bash
cd api && bun run db:extract-schema
```

### 2단계: 결과 요약

실행 결과에서 아래 4가지 수치를 보여준다:
- **Created**: 새로 생성된 스키마 파일
- **Updated**: DDL이 변경되어 갱신된 파일
- **Unchanged**: 변경 없는 파일
- **Deleted**: DB에서 삭제된 테이블의 스키마 파일 정리

### 3단계: 변경 파일 상세

Updated 또는 Created 파일이 있으면:
- 변경된 파일 목록을 보여준다.
- 주요 변경 내용(컬럼 추가/삭제, 인덱스 변경 등)을 요약한다.

## 출력 파일 위치

```
api/db/schema/{도메인}/{테이블명}.sql
```

도메인은 테이블명의 첫 번째 `_` 앞 부분으로 자동 분류된다:
- `kacta_staff.sql` → `schema/kacta/kacta_staff.sql`
- `common_file.sql` → `schema/common/common_file.sql`
- `member.sql` → `schema/member/member.sql`

## 추출 내용

- CREATE TABLE DDL (컬럼, 타입, 기본값, NOT NULL)
- COMMENT ON TABLE / COLUMN (한글 코멘트)
- CREATE INDEX (Partial Index WHERE 절 포함)
- PRIMARY KEY CONSTRAINT

## 사용 시점

- 다른 개발자가 DB를 직접 변경한 후 스키마 파일 동기화
- 스키마 파일과 실제 DB 상태 불일치 의심 시
- 마이그레이션 없이 DB 구조만 확인하고 싶을 때
- 새 프로젝트 환경에서 최초 스키마 파일 생성 시
