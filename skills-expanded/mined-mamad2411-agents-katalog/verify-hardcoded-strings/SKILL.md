---
name: verify-hardcoded-strings
description: "UI 컴포넌트에서 하드코딩된 문자열(비영어 텍스트, 에러 메시지)을 탐지합니다. naia-os shell 수정 후 반드시 실행."
disable-model-invocation: true
---

# Hardcoded String 검증

## 목적

naia-os shell UI 컴포넌트에서 사용자에게 보이는 하드코딩 문자열을 탐지합니다.

## Workflow

### Step 1: 비영어 하드코딩 탐지

```bash
# .tsx/.ts 파일에서 하드코딩 한국어 탐지 (i18n 함수 사용 없이)
grep -rn '[ㄱ-ㅎㅏ-ㅣ가-힣]' shell/src --include="*.tsx" --include="*.ts" | grep -v 'i18n\|t(\|useTranslation\|\.json\|\/\/\|\/\*\|\.test\.'
```

### Step 2: 에러 메시지 하드코딩 탐지

```bash
# throw new Error / console.error 에 하드코딩 메시지가 있는지
grep -rn 'throw new Error("' shell/src --include="*.ts" --include="*.tsx"
```

사용자에게 보이는 에러 메시지는 i18n 키를 통해야 함.

### Step 3: 결과 보고

- **PASS**: 하드코딩 문자열 없음
- **FAIL**: 하드코딩 문자열 발견 시 파일:라인과 함께 보고

## Exceptions

- 테스트 파일(`.test.ts`, `.test.tsx`, `.spec.ts`)
- 스토리북 파일(`.stories.tsx`)
- 타입 정의 파일(`.d.ts`)
- CSS/스타일 파일 내 `content` 속성
- 개발자 도구용 로그 (debug 레벨)

## PASS/FAIL 기준

| 조건 | 결과 |
|------|------|
| 탐지된 하드코딩 문자열 0개 | PASS |
| 1개 이상 발견 | FAIL |
