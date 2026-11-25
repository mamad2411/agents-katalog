# Skill API 명세

- 공통 규칙: [api-spec-common.md](./api-spec-common.md)
- 인덱스: [api-spec-index.md](./api-spec-index.md)

## 1. 도메인 목적 / 개요
사용자별 보유 스킬 목록 조회와 일괄 교체 계약을 정의한다. 본 문서는 inventory 의 legacy 단수형 path 표기와 분리해 normalized path 인 `/api/users/{userId}/skills` 를 사용한다.

## 2. 주요 ERD 연관
- `tb_user_skill`
- `tb_user`

## 3. 참조 문서
- [api-spec-common.md](./api-spec-common.md)
- [api-spec-index.md](./api-spec-index.md)
- [adr.yaml](../adr.yaml)

## 4. 엔드포인트 목록
| Method | Path | Status | 목적 |
|---|---|---|---|
| `GET` | `/api/users/{userId}/skills` | `Documented` | 특정 사용자의 보유 스킬 목록을 조회한다. |
| `POST` | `/api/users/{userId}/skills` | `Documented` | 특정 사용자에게 스킬을 추가한다. |
| `PATCH` | `/api/users/{userId}/skills/{id}` | `Documented` | 특정 사용자의 특정 스킬 정보를 수정한다. |
| `DELETE` | `/api/users/{userId}/skills/{id}` | `Documented` | 특정 사용자의 특정 스킬을 삭제한다. |

## 5. 엔드포인트 상세

### GET /api/users/{userId}/skills
- 목적: 특정 사용자의 보유 스킬 목록을 조회한다.
- 상태: `Documented`
- 권한/접근 주체: `DIRECTOR`, `DEPT_HEAD` 만 호출한다. 자기 자신 조회와 `DEPT_HEAD` 의 `DIRECTOR` 조회는 성공 응답으로 처리하되 `skills: []` 로 비노출한다. `DEPT_HEAD` 는 같은 부서 사용자만 조회할 수 있다.
- 요청
  - Path: `userId`
- 응답 (`data` 기준)
  - `userId`
  - `skills[*]`: `skillId`, `skillName`, `skillLevel`, `updatedAt`
  - 정렬: `skillLevel` 내림차순을 우선한다.
- 요청 JSON 예시
```json
{
  "path": {
    "userId": 101
  }
}
```
- 응답 JSON 예시
```json
{
  "success": true,
  "data": {
    "userId": 101,
    "skills": [
      {
        "skillId": 1,
        "skillName": "WMS",
        "skillLevel": 5,
        "updatedAt": "2026-04-20T09:00:00Z"
      },
      {
        "skillId": 2,
        "skillName": "SQL",
        "skillLevel": 4,
        "updatedAt": "2026-04-18T09:00:00Z"
      }
    ]
  },
  "timestamp": "2026-04-21T03:00:00Z"
}
```
- 비노출 응답 JSON 예시
```json
{
  "success": true,
  "data": {
    "userId": 101,
    "skills": []
  },
  "timestamp": "2026-04-21T03:00:00Z"
}
```
- 상태/에러
  - 성공: `200 OK`
  - 대표 오류: `USER_NOT_FOUND`
  - 대표 오류: `AUTH_ACCESS_DENIED`
- ERD 연관
  - `tb_user_skill`
- 근거
  - source: checklist
  - source: class mapping

### POST /api/users/{userId}/skills
- 목적: 특정 사용자에게 스킬을 추가한다.
- 상태: `Documented`
- 권한/접근 주체: `DIRECTOR`, `DEPT_HEAD` 만 호출한다. `DIRECTOR` 는 자기 자신을 제외한 사용자를 대상으로 등록할 수 있고, `DEPT_HEAD` 는 자기 자신과 `DIRECTOR` 를 제외한 같은 부서 사용자만 대상으로 등록할 수 있다.
- 요청
  - Path: `userId`
  - Body: `skillName`, `skillLevel`
- 응답 (`data` 기준)
  - 빈 객체 (`ApiResponse.empty()`)
- 요청 JSON 예시
```json
{
  "path": {
    "userId": 101
  },
  "body": {
    "skillName": "WMS",
    "skillLevel": 5
  }
}
```
- 응답 JSON 예시
```json
{
  "success": true,
  "data": {},
  "timestamp": "2026-04-21T03:00:00Z"
}
```
- 상태/에러
  - 성공: `201 Created`
  - 대표 오류: `COMMON_VALIDATION_ERROR`
  - 대표 오류: `AUTH_ACCESS_DENIED`
  - 대표 오류: `USER_NOT_FOUND`
  - 대표 오류: `USER_SKILL_DUPLICATE_NAME`
- ERD 연관
  - `tb_user_skill`
- 근거
  - source: checklist
  - source: class mapping

### PATCH /api/users/{userId}/skills/{id}
- 목적: 특정 사용자의 특정 스킬 정보를 수정한다.
- 상태: `Documented`
- 권한/접근 주체: `DIRECTOR`, `DEPT_HEAD` 만 호출한다. `DIRECTOR` 는 자기 자신을 제외한 사용자를 대상으로 수정할 수 있고, `DEPT_HEAD` 는 자기 자신과 `DIRECTOR` 를 제외한 같은 부서 사용자만 대상으로 수정할 수 있다.
- 요청
  - Path: `userId`, `id` (스킬 레코드 식별자)
  - Body: `skillName`, `skillLevel` (null 필드는 기존 값 유지)
  - `skillName` 은 양끝 공백을 제거한 뒤 반영한다. blank 값은 기존 값 유지로 처리한다.
- 응답 (`data` 기준)
  - 빈 객체 (`ApiResponse.empty()`)
- 요청 JSON 예시
```json
{
  "path": {
    "userId": 101,
    "id": 1
  },
  "body": {
    "skillLevel": 5
  }
}
```
- 응답 JSON 예시
```json
{
  "success": true,
  "data": {},
  "timestamp": "2026-04-21T03:00:00Z"
}
```
- 상태/에러
  - 성공: `200 OK`
  - 대표 오류: `COMMON_VALIDATION_ERROR`
  - 대표 오류: `AUTH_ACCESS_DENIED`
  - 대표 오류: `USER_NOT_FOUND`
  - 대표 오류: `USER_SKILL_NOT_FOUND`
  - 대표 오류: `USER_SKILL_DUPLICATE_NAME`
- ERD 연관
  - `tb_user_skill`
- 근거
  - source: checklist
  - source: class mapping

### DELETE /api/users/{userId}/skills/{id}
- 목적: 특정 사용자의 특정 스킬을 삭제한다.
- 상태: `Documented`
- 권한/접근 주체: `DIRECTOR`, `DEPT_HEAD` 만 호출한다. `DIRECTOR` 는 자기 자신을 제외한 사용자를 대상으로 삭제할 수 있고, `DEPT_HEAD` 는 자기 자신과 `DIRECTOR` 를 제외한 같은 부서 사용자만 대상으로 삭제할 수 있다.
- 요청
  - Path: `userId`, `id` (스킬 레코드 식별자)
- 응답 (`data` 기준)
  - 빈 객체 (`ApiResponse.empty()`)
- 요청 JSON 예시
```json
{
  "path": {
    "userId": 101,
    "id": 1
  }
}
```
- 응답 JSON 예시
```json
{
  "success": true,
  "data": {},
  "timestamp": "2026-04-21T03:00:00Z"
}
```
- 상태/에러
  - 성공: `200 OK`
  - 대표 오류: `AUTH_ACCESS_DENIED`
  - 대표 오류: `USER_NOT_FOUND`
  - 대표 오류: `USER_SKILL_NOT_FOUND`
- ERD 연관
  - `tb_user_skill`
- 근거
  - source: checklist
  - source: class mapping

## 6. 추론 메모
- `{userId}`는 사용자 식별자, `{id}`는 스킬 레코드 식별자로 구분한다.
