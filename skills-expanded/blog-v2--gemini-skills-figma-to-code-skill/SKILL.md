---
name: figma-to-code
description: 피그마 설계를 분석하여 Dan DevLog (v2) 프로젝트의 Tailwind CSS v4 기반 기술 스택 및 컨벤션에 맞춰 코드로 변환합니다. src/components/common 내의 Flex, Button 등 커스텀 컴포넌트를 우선적으로 활용합니다.
---

# Figma to Code Skill

이 스킬은 피그마 설계를 분석하여 Dan DevLog (v2) 프로젝트의 표준 기술 스택과 컨벤션에 맞는 React 코드로 변환하는 가이드를 제공합니다.

## 프로젝트 표준 기술 스택

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4, `tailwind-merge`, `clsx` (`cn` 유틸리티 사용)
- **UI Library**: 프로젝트 내부의 공통 컴포넌트 (`src/components/common/`)
- **Icons**: Humbleicons 또는 `src/components/icon/`
- **Data Fetching**: TanStack Query (React Query)
- **Animation**: Framer Motion

## 주요 참조 문서

- **Tailwind v4 패턴 가이드**: `references/tailwind-v4-pattern.md`를 참고하여 최신 `@theme` 색상 토큰(예: `gray-900`, `primary`, `dgray-400` 등)과 레이아웃 패턴을 정확히 사용해야 합니다. 코드를 변환하기 전에 **반드시 해당 패턴 문서를 읽고 숙지하세요**.

## 워크플로우

1. **디자인 분석 (`get_design_context`)**: 피그마 URL 또는 Node ID를 사용하여 디자인 메타데이터와 코드를 추출합니다.
2. **컴포넌트 매핑**: 디자인의 각 요소를 가급적 `src/components/common/` 내의 컴포넌트로 매핑합니다.
3. **레이아웃 구조화**: `Flex` 컴포넌트를 사용하여 레이아웃을 구성합니다. (`$gap`, `$direction`, `$alignItems`, `$justifyContent` 등 활용)
4. **스타일링 적용**: `cn` 유틸리티와 Tailwind CSS v4 클래스(참조 문서의 토큰)를 사용하여 세부 스타일을 조합합니다.
5. **서버/클라이언트 분리**: 가능하면 서버 컴포넌트를 유지하고, 인터랙션이 필요할 때만 최상단에 `'use client'`를 추가합니다.

## 코드 변환 원칙

### 1. 내부 공통 컴포넌트 우선 사용
디자인 요소가 기존 공통 컴포넌트에 존재하는 경우, 직접 구현하는 대신 재사용합니다.
- `Button`: 버튼 컴포넌트. 추가 클래스는 `className`을 통해 `cn()`으로 병합됩니다.
- `Flex`: 1차원 레이아웃. Tailwind의 `flex` 클래스 대신 `$direction`, `$alignItems`, `$justifyContent`, `$gap` 속성을 통해 제어합니다.

### 2. 레이아웃 컨벤션
- 마진(Margin) 대신 **Gap** 사용을 권장합니다 (`Flex`의 `$gap` 속성 활용).
- 패딩(Padding)은 컴포넌트 내부에서 Tailwind 클래스로 처리합니다 (`p-4`, `px-6` 등).

### 3. 스타일링 (Tailwind v4 & `cn` 유틸리티)
- 클래스 조합 시에는 `cn` 함수(`@/libs/utils`)를 사용합니다.
- 하드코딩된 색상값이나 임의의 픽셀값(Arbitrary values) 대신 `references/tailwind-v4-pattern.md`에 정의된 테마 변수 클래스를 활용합니다.

### 4. 코드 구조
- **Client Component**: 상태나 이벤트 리스너가 필요하면 파일 최상단에 `'use client';`를 명시합니다.
- **Props**: 컴포넌트의 Props 타입은 TypeScript로 명확하게 정의합니다.
- **Import Alias**: `@/components/...`, `@/libs/utils` 등 프로젝트의 Path Alias를 사용합니다.

## 예시: 변환 패턴

### 가로 배치 (Header/Action Bar)
```tsx
'use client';

import Flex from '@/components/common/Flex';
import Button from '@/components/common/Button';

export function ActionHeader() {
  return (
    <Flex 
      $justifyContent="space-between" 
      $alignItems="center" 
      className="w-full border-b border-gray-200 px-6 py-4"
    >
      <h1 className="text-xl font-bold text-gray-900">제목</h1>
      <Flex $gap={8} $alignItems="center">
        <Button className="border border-gray-300 text-gray-700">취소</Button>
        <Button className="bg-primary text-white hover:opacity-90">저장</Button>
      </Flex>
    </Flex>
  );
}
```

### 세로 배치 (Card List)
```tsx
import Flex from '@/components/common/Flex';
import Avatar from '@/components/common/Avatar';

export function ProfileCard() {
  return (
    <Flex $direction="column" $gap={16} $alignItems="center" className="rounded-xl border border-gray-200 bg-white p-6">
      <Avatar src="/assets/avatar.gif" alt="프로필 이미지" />
      <Flex $direction="column" $gap={4} $alignItems="center">
        <span className="text-lg font-semibold text-gray-900">사용자 이름</span>
        <span className="text-sm text-dgray-400">user@example.com</span>
      </Flex>
    </Flex>
  );
}
```

## 참고 사항
- 이미지 자산은 `public/` 디렉토리에 배치하고 기존 `Avatar` 등을 활용합니다.
- 복잡한 디자인을 코드로 짤 때는 참조 문서(`tailwind-v4-pattern.md`)에 명시된 토큰 매핑 규칙을 철저히 준수하세요.