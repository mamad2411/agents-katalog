# Virtual Try-On 서비스 디자인 시스템 규칙

> **프로젝트**: Virtual Try-On Service  
> **기술 스택**: Next.js 14, TypeScript, TailwindCSS, Three.js  
> **작성일**: 2025.12.06

---

## 1. 디자인 토큰 정의

### 색상
디자인 토큰은 TailwindCSS 설정에서 정의됩니다. 다음 색상 팔레트를 사용하세요:

**Primary 색상:**
- `primary-500`: #6366F1 (Indigo-500) - 메인 브랜드 색상
- `primary-600`: #4F46E5 (Indigo-600) - 어두운 변형
- `primary-400`: #818CF8 (Indigo-400) - 밝은 변형

**Secondary 색상:**
- `secondary-500`: #EC4899 (Pink-500) - 강조 색상
- `secondary-600`: #DB2777 (Pink-600) - 어두운 변형
- `secondary-400`: #F472B6 (Pink-400) - 밝은 변형

**Neutral 색상:**
- `background`: #FFFFFF (흰색)
- `background-secondary`: #F9FAFB (Gray-50)
- `text-primary`: #111827 (Gray-900)
- `text-secondary`: #6B7280 (Gray-500)
- `border`: #E5E7EB (Gray-200)

**상태 색상:**
- `success`: #10B981 (Green-500)
- `warning`: #F59E0B (Amber-500)
- `error`: #EF4444 (Red-500)
- `info`: #3B82F6 (Blue-500)

### 타이포그래피
**폰트 패밀리:**
- Primary: `Inter` (Sans-serif)
- Code: `'Fira Code', monospace`

**폰트 크기 (rem):**
- Display: 3rem (48px) / line-height: 3.5rem (56px) / weight: 700
- H1: 2.25rem (36px) / line-height: 2.75rem (44px) / weight: 700
- H2: 1.875rem (30px) / line-height: 2.375rem (38px) / weight: 600
- H3: 1.5rem (24px) / line-height: 2rem (32px) / weight: 600
- H4: 1.25rem (20px) / line-height: 1.75rem (28px) / weight: 600
- Body Large: 1.125rem (18px) / line-height: 1.75rem (28px) / weight: 400
- Body: 1rem (16px) / line-height: 1.5rem (24px) / weight: 400
- Body Small: 0.875rem (14px) / line-height: 1.25rem (20px) / weight: 400
- Caption: 0.75rem (12px) / line-height: 1rem (16px) / weight: 400

### 간격
4px 그리드 시스템 사용:
- `space-1`: 0.25rem (4px)
- `space-2`: 0.5rem (8px)
- `space-3`: 0.75rem (12px)
- `space-4`: 1rem (16px)
- `space-5`: 1.25rem (20px)
- `space-6`: 1.5rem (24px)
- `space-8`: 2rem (32px)
- `space-10`: 2.5rem (40px)
- `space-12`: 3rem (48px)
- `space-16`: 4rem (64px)
- `space-20`: 5rem (80px)
- `space-24`: 6rem (96px)

### 테두리 반경
- `rounded-sm`: 0.25rem (4px)
- `rounded-md`: 0.5rem (8px)
- `rounded-lg`: 0.75rem (12px)
- `rounded-xl`: 1rem (16px)
- `rounded-full`: 9999px

### 그림자
- `shadow-sm`: 0 1px 2px 0 rgba(0, 0, 0, 0.05)
- `shadow-md`: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)
- `shadow-lg`: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)
- `shadow-xl`: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)

---

## 2. 컴포넌트 라이브러리

### 컴포넌트 아키텍처
- **프레임워크**: Next.js 14 App Router
- **언어**: TypeScript
- **스타일링**: TailwindCSS (utility-first)
- **3D 렌더링**: Three.js + React Three Fiber

### 컴포넌트 구조
```
components/
├── ui/              # 기본 UI 컴포넌트 (Button, Input, Card 등)
├── layout/          # 레이아웃 컴포넌트 (Header, Sidebar, Footer)
├── features/        # 기능별 컴포넌트
│   ├── ImageUpload
│   ├── ImageComparison
│   ├── AvatarPreview
│   └── 3DViewer
└── shared/          # 공유 컴포넌트 (Navigation, UserMenu 등)
```

### 컴포넌트 패턴
- TypeScript를 사용한 함수형 컴포넌트 사용
- Props는 인터페이스로 타입 지정
- 스타일링은 TailwindCSS 클래스 사용
- 모바일 우선 반응형 디자인 준수

**참고**: 상세한 컴포넌트 개발 규칙은 `.cursor/rules/component_rules.mdc` 참고

**컴포넌트 예시:**
```typescript
// components/ui/Button.tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  onClick?: () => void;
}

export const Button = ({ 
  variant = 'primary', 
  size = 'md', 
  children,
  onClick 
}: ButtonProps) => {
  const baseStyles = 'rounded-lg font-semibold transition-colors';
  const variantStyles = {
    primary: 'bg-primary-500 text-white hover:bg-primary-600',
    secondary: 'bg-secondary-500 text-white hover:bg-secondary-600',
    outline: 'border-2 border-primary-500 text-primary-500 hover:bg-primary-50'
  };
  const sizeStyles = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  };

  return (
    <button
      className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]}`}
      onClick={onClick}
    >
      {children}
    </button>
  );
};
```

---

## 3. 프레임워크 & 라이브러리

### 프론트엔드 스택
- **프레임워크**: Next.js 14.x (App Router)
- **언어**: TypeScript 5.x
- **스타일링**: TailwindCSS 3.x
- **3D**: Three.js 0.160+ / React Three Fiber 8.x
- **상태 관리**: Zustand 4.x / React Query 5.x

### 빌드 시스템
- **번들러**: Next.js 내장 (Turbopack)
- **패키지 매니저**: npm 또는 pnpm
- **타입 체킹**: TypeScript 컴파일러

---

## 4. 에셋 관리

### 이미지 저장소
- **스토리지**: Cloudflare R2 (S3 호환)
- **CDN**: Cloudflare CDN
- **최적화**: Next.js Image 컴포넌트 자동 최적화
- **포맷**: WebP (우선), JPEG, PNG

### 에셋 구조
```
public/
├── images/
│   ├── avatars/
│   ├── garments/
│   └── try-on-results/
└── icons/
```

### 이미지 사용 패턴
```typescript
import Image from 'next/image';

<Image
  src="/images/garments/example.jpg"
  alt="의상 예시"
  width={800}
  height={600}
  className="rounded-lg"
/>
```

---

## 5. 아이콘 시스템

### 아이콘 라이브러리
- 아이콘은 **Lucide React** 또는 **Heroicons** 사용
- 트리 쉐이킹을 위해 개별적으로 import

### 아이콘 사용 패턴
```typescript
import { Upload, Download, Share2 } from 'lucide-react';

<Upload className="w-5 h-5 text-primary-500" />
```

### 아이콘 명명 규칙
- 컴포넌트 이름은 PascalCase 사용
- 설명적인 이름 사용 (예: `UploadIcon`, `DownloadIcon`)

---

## 6. 스타일링 접근 방식

### CSS 방법론
- **주요**: TailwindCSS 유틸리티 클래스
- **전역 스타일**: 최소화, 기본 리셋만 사용
- **CSS Modules**: 사용 안 함 (TailwindCSS 선호)

### 전역 스타일
```css
/* app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-background text-text-primary;
    font-family: 'Inter', sans-serif;
  }
}
```

### 반응형 디자인
- 모바일 우선 접근 방식
- 브레이크포인트:
  - `sm`: 640px
  - `md`: 768px
  - `lg`: 1024px
  - `xl`: 1280px
  - `2xl`: 1536px

**예시:**
```typescript
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* 반응형 그리드 */}
</div>
```

---

## 7. 프로젝트 구조

### 디렉토리 구성
```
app/                    # Next.js App Router 페이지
├── (auth)/            # 인증 라우트 (login, register)
├── (main)/            # 메인 앱 라우트
│   ├── dashboard/
│   ├── try-on/
│   └── avatar/
└── api/               # API 라우트

components/            # React 컴포넌트
├── ui/               # 기본 UI 컴포넌트
├── layout/           # 레이아웃 컴포넌트
├── features/         # 기능 컴포넌트
└── shared/           # 공유 컴포넌트

lib/                   # 유틸리티 함수
├── api/              # API 클라이언트
├── utils/            # 헬퍼 함수
└── hooks/            # 커스텀 React 훅

types/                 # TypeScript 타입 정의

public/                # 정적 에셋
```

### 기능별 구성
각 기능은 독립적으로 구성:
```
features/try-on/
├── components/
│   ├── ImageUpload.tsx
│   └── ResultViewer.tsx
├── hooks/
│   └── useTryOn.ts
├── types/
│   └── try-on.types.ts
└── utils/
    └── image-processing.ts
```

---

## 8. Figma 통합 가이드라인

### 디자인 토큰 매핑
Figma에서 디자인을 추출할 때:
1. Figma 색상을 TailwindCSS 색상 토큰으로 매핑
2. Figma 타이포그래피를 TailwindCSS 텍스트 클래스로 매핑
3. Figma 간격을 TailwindCSS 간격 유틸리티로 매핑
4. Figma 그림자를 TailwindCSS 그림자 클래스로 매핑

### 컴포넌트 추출
1. Figma에서 재사용 가능한 컴포넌트 식별
2. 컴포넌트 스타일 추출 (색상, 간격, 타이포그래피)
3. TailwindCSS 클래스를 사용한 TypeScript 컴포넌트 생성
4. 반응형 동작이 Figma 브레이크포인트와 일치하는지 확인

### 디자인 시스템 동기화
- Figma 디자인 토큰을 TailwindCSS 설정과 동기화 유지
- 디자인과 구현 간 차이점 문서화
- 가능한 경우 Figma 변수를 디자인 토큰으로 사용

---

## 9. 3D 뷰어 통합

### Three.js 설정
- React 통합을 위해 React Three Fiber 사용
- 3D 렌더링을 위한 Canvas 컴포넌트
- 3D 아바타 뷰어를 위한 별도 컴포넌트

### 3D 컴포넌트 패턴
```typescript
import { Canvas } from '@react-three/fiber';

<Canvas>
  <ambientLight />
  <pointLight position={[10, 10, 10]} />
  <AvatarModel />
</Canvas>
```

---

## 10. 모범 사례

### 접근성
- 시맨틱 HTML 요소 사용
- 색상 대비 비율 ≥ 4.5:1 보장
- 이미지에 alt 텍스트 제공
- 키보드 네비게이션 지원

### 성능
- 최적화를 위해 Next.js Image 컴포넌트 사용
- 3D 컴포넌트 지연 로딩
- 기능 라우트 코드 분할
- 번들 크기 최적화 (트리 쉐이킹)

### 코드 품질
- TypeScript strict 모드 활성화
- 코드 포맷팅을 위한 ESLint + Prettier
- JSDoc을 사용한 컴포넌트 문서화
- 일관된 명명 규칙
