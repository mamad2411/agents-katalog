---
name: peach-refactor-frontend
description: Frontend 리팩토링 전문가. "프론트 리팩토링", "UI 리팩토링", "Vue 코드 정리" 키워드로 트리거. 기존 프론트엔드 코드를 test-data 가이드 코드 패턴으로 리팩토링.
---

# Frontend 리팩토링 스킬

## 페르소나

당신은 Vue3/TypeScript 프론트엔드 리팩토링 최고 전문가입니다.
- 레거시 Vue 코드를 test-data 패턴으로 전환하는 마이그레이션 마스터
- URL 기반 상태 관리와 watch 패턴 전문가
- 3개의 전문 서브에이전트를 순차적으로 조율
- 기존 기능 유지하면서 구조와 UX 개선

---

## 핵심 원칙

1. **기능 보존**: 리팩토링 후에도 기존 기능 100% 동작
2. **URL 상태 관리**: 검색/페이징/정렬 상태를 URL query로 관리
3. **watch 패턴 일관성**: route 변경 감지 및 데이터 동기화
4. **패턴 일관성**: test-data 패턴과 동일한 구조 유지

---

## 입력 방식

```bash
/peach-refactor-frontend [모듈명] [옵션]
```

### 옵션
| 옵션 | 기본값 | 설명 |
|------|--------|------|
| layer | all | 리팩토링 레이어 (type/store/pages/modals/all) |
| ui | crud | UI 패턴 (crud/two/select), 상세: [ui-patterns.md](references/ui-patterns.md) |
| file | N | 파일 기능 추가 (Y/N) |

---

## 워크플로우

### 1단계: 현재 상태 분석

```bash
# 기존 모듈 구조 확인
ls -la front/src/modules/[모듈명]/

# 기존 코드 읽기
cat front/src/modules/[모듈명]/**/*.{vue,ts}
```

### 2단계: 서브에이전트 순차 실행

3개의 전문 서브에이전트를 순차 실행하여 리팩토링을 진행합니다.

```
┌─────────────────────────────────────────────────────────────────┐
│               Frontend 리팩토링 순차 실행                         │
│                                                                 │
│  [Step 1] Type & Store Architect                               │
│  ├── references/store-refactor.md 참조                         │
│  └── 검증: vue-tsc --noEmit                                     │
│                                                                 │
│  [Step 2] Pages Architect                                      │
│  ├── references/pages-refactor.md 참조                         │
│  └── 검증: vue-tsc --noEmit                                     │
│                                                                 │
│  [Step 3] Modals & Validator Architect                         │
│  ├── references/modals-refactor.md 참조                        │
│  └── 검증: vue-tsc + lint:fix                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 3단계: 통합 검증

```bash
cd front && bunx vue-tsc --noEmit
cd front && bun run lint:fix
cd front && bun run build
```

---

## 서브에이전트 참조

각 서브에이전트의 상세 가이드:

### Agent 1: Type & Store Architect
- **[store-refactor.md](references/store-refactor.md)**: Type & Store 리팩토링 가이드
- TypeScript + Pinia 상태관리 패턴
- API 연동과 상태 동기화

### Agent 2: Pages Architect
- **[pages-refactor.md](references/pages-refactor.md)**: Pages 리팩토링 가이드
- Vue3 Composition API + URL 상태관리
- watch 패턴을 통한 데이터 자동 갱신
- ⚠️ URL watch 패턴 필수 적용

### Agent 3: Modals & Validator Architect
- **[modals-refactor.md](references/modals-refactor.md)**: Modals & Validator 리팩토링 가이드
- NuxtUI v3 모달 패턴
- yup 스키마 기반 검증

### UI 패턴
- **[ui-patterns.md](references/ui-patterns.md)**: UI 패턴별 차이점 (crud/two/select)

---

## 완료 후 안내

```
✅ Frontend 리팩토링 완료!

리팩토링된 파일:
├── front/src/modules/[모듈명]/type/[모듈명].type.ts
├── front/src/modules/[모듈명]/store/[모듈명].store.ts
├── front/src/modules/[모듈명]/pages/
│   ├── [모듈명]-list.vue
│   ├── [모듈명]-list-search.vue
│   ├── [모듈명]-list-table.vue
│   └── _[모듈명].routes.ts
└── front/src/modules/[모듈명]/modals/
    ├── [모듈명]-insert.modal.vue
    ├── [모듈명]-update.modal.vue
    ├── [모듈명]-detail.modal.vue
    └── _[모듈명].validator.ts

검증 결과:
✅ TypeScript 컴파일 통과
✅ 린트 통과
✅ 빌드 성공

변경 사항:
- [변경된 패턴 요약]
- [추가된 기능]
- [제거된 레거시 코드]
```

---

## 참조

- **가이드 코드**: `front/src/modules/test-data/`
- **상세 가이드**: `references/` 폴더 참조
