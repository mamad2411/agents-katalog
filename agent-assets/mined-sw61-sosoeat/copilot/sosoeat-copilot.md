# 📜 프로젝트 컨벤션 및 개발 가이드

프로젝트의 지속 가능한 유지보수와 원활한 협업을 위한 **소소잇(sosoeat)** 개발 가이드입니다. 일관성 있는 코드 작성을 위해 본 내용을 참고하여 개발해 주세요.

---

## 📑 목차

1. [📂 프로젝트 및 컴포넌트 구조](#1-프로젝트-및-컴포넌트-구조)
2. [🏷️ 명명 규칙 (Naming)](#2-명명-규칙-naming)
3. [🎨 스토리북 경로 컨벤션](#3-스토리북-경로-컨벤션)
4. [🚀 코드 스타일 및 패턴](#4-코드-스타일-및-패턴)
5. [🛠️ 리팩토링 원칙](#5-리팩토링-원칙)
6. [📝 협업 및 테스트 규칙](#6-협업-및-테스트-규칙)

---

## 1. 📂 프로젝트 및 컴포넌트 구조

### 💡 컴포넌트 설계 원칙

- **계층형 설계**: Atomic Design을 변형한 2단계를 권장합니다.
  - `ui/`: 원자(Atomic) 단위의 순수 UI (shadcn 기반).
  - `common/`: UI 조각들을 조합한 전역 공통 패턴 컴포넌트.
- **Colocation**: 특정 페이지 전용 컴포넌트는 해당 라우트의 `_components/` 폴더에서 관리하는 것을 권장합니다.
- **내부 컴포넌트**: 대형 컴포넌트 내부에서만 쓰이는 하위 조각들은 해당 폴더 내의 **`_components/` 서브 폴더** 활용을 권장합니다.
- **파일 응집도**: 컴포넌트(`.tsx`), 테스트(`.test.tsx`), 스토리북(`.stories.tsx`)은 가급적 **동일한 폴더**에 한꺼번에 둡니다.

### 📝 파일 구성 규칙

- **Barrel Pattern**: 각 컴포넌트 폴더의 `index.ts`에서 `export * from './파일명'` 형식을 지향합니다.
- **관심사 분리 (Suffix)**: 파일이 복잡해질 경우 다음 접미사를 활용해 파일을 세분화합니다.
  - `*.types.ts`: 타입 정의 전용
  - `*.schema.ts`: 데이터 유효성 검사(Zod) 전용
  - `*.constants.ts`: 상수 및 전용 설정 전용
  - `*.utils.ts`: 내부 전용 헬퍼 함수 전용
  - `hooks/use-*.ts`: 상태 관리 및 비즈니스 로직 전용

---

## 2. 🏷️ 명명 규칙 (Naming)

| 대상                  | 규칙         | 예시                              |
| :-------------------- | :----------- | :-------------------------------- |
| **폴더명**            | `kebab-case` | `user-profile/`, `main-layout/`   |
| **파일명**            | `kebab-case` | `login-button.tsx`, `use-auth.ts` |
| **컴포넌트**          | `PascalCase` | `Avatar`, `SearchInput`           |
| **커스텀 훅**         | `camelCase`  | `useIsMounted`, `useToggle`       |
| **유틸/함수**         | `camelCase`  | `formatDate`, `calculatePrice`    |
| **타입 & 인터페이스** | `PascalCase` | `UserProfile`, `ButtonProps`      |

> [!CAUTION]
> **Type vs Interface**: 객체 타입 정의 시 확장성을 위해 **`interface` 사용을 지향**합니다.

---

## 3. 🎨 스토리북 경로 컨벤션

Storybook 내에서의 컴포넌트 계층 구조는 다음과 같은 명명 규칙을 따릅니다. `.stories.tsx` 파일의 `title` 속성을 통해 다음과 같이 설정합니다.

| 컴포넌트 위치                 | 추천 `title` 예시                    | 비고                      |
| :---------------------------- | :----------------------------------- | :------------------------ |
| `src/components/ui/`          | `'Components/ui/Button'`             | 원자(Atomic) 단위 UI      |
| `src/components/common/`      | `'Components/common/CommentItem'`    | 공통 패턴 컴포넌트        |
| `src/app/[page]/_components/` | `'Pages/[page-name]/CommentSection'` | 특정 페이지 전용 컴포넌트 |

```typescript
const meta = {
  title: 'Components/common/CommentItem',
  component: CommentItem,
} satisfies Meta<typeof CommentItem>;
```

---

## 4. 🚀 코드 스타일 및 패턴

### ✅ 기본 문법 및 패턴

- **함수 정의**: 특별한 제약이 없다면 **화살표 함수(`=>`)** 사용을 지향합니다.
- **상태 관리(Zustand)**: 불필요한 리렌더링 방지를 위해 **Selector 방식**으로 상태를 구독하는 것을 권장합니다.
- **데이터 처리(TanStack Query)**: `services/`에서 API 호출부와 Query 훅을 통합 관리하는 것을 권장합니다.
- **임포트(Import)**: 가독성을 위해 `React 관련 -> 외부 라이브러리 -> @/* 내부 경로 -> 상대 경로` 순으로 정렬하는 것을 권장합니다.

### 🛠️ 라이브러리 및 유틸 활용

- **날짜**: 모든 날짜 포맷팅/계산은 **`date-fns`** 사용을 권장합니다.
- **스타일**: 조건부 클래스 조합 시 **`cn()` 유틸리티** 사용을 지향합니다.
- **폼**: 복잡한 입력 및 유효성 검사는 **`react-hook-form` + `zod`** 활용을 권장합니다.
- **클린업**: `useEffect` 내 side-effect는 **Clean-up 함수**를 통해 제거하는 것을 권장합니다.

---

## 5. 🛠️ 리팩토링 원칙

유지보수 효율을 높이기 위해 다음 원칙을 수시로 적용합니다.

- **단일 책임 (SRP)**: 하나의 함수/컴포넌트는 오직 한 가지 역할만 담당하도록 설계하는 것을 지향합니다.
- **이른 반환 (Early Return)**: 복잡한 중첩보다 조건에 맞지 않을 때 빠르게 반환하여 가독성을 높이는 것을 권장합니다.
- **중복 로직 추출 (DRY)**: **3곳 이상** 반복되는 로직은 `utils/` 또는 `hooks/`로 공통화하는 것을 지향합니다.
- **적정 규모 유지**: 파일이 **200라인을 초과**하거나 로직이 비대해지면 커스텀 훅이나 하위 컴포넌트로 분리하는 것을 권장합니다.

---

## 6. 📝 협업 및 테스트 규칙

### 🌿 브랜치 및 커밋 전략

- **브랜치 네이밍**: `type/#issuenumber-description` (예: `feat/#12-login-page`)
- **커밋 메시지**: `feat`, `fix`, `docs`, `design`, `style`, `refactor`, `test`, `chore` 타입 사용을 권장합니다.
  - > [!TIP]
    > `type: description` 형식을 지키는 것을 지향합니다.

### 🧪 테스트 규칙

- **언어**: 테스트 케이스 설명(`describe`, `it`)은 **한글 작성**을 권장합니다.
- **문법**: 문장형 표현에 적합한 **`it` 구문 사용**을 권장합니다.
- **규모**: 컴포넌트 개발 시 최소한의 단위 테스트(`.test.tsx`) 포함을 지향합니다.
