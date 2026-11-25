# Travel Companion — Agent Instructions

## 프로젝트 개요

여행하면서 기억하고 싶은 순간을 기록하는 앱. 사진·위치·메모를 활용해 여행의 추억을 시각화하고 공유하는 모바일/웹 애플리케이션.

**핵심 기능**
- 사진 업로드 및 EXIF GPS 추출
- 지도 위 마커 표시 및 여행 경로 시각화
- 시간순/위치별 여행 스토리 생성
- 여행 기록 공유 (링크, SNS)
- 여행 타임라인 및 갤러리 뷰

**모바일 앱 작업 시 필독**: `apps/mobile/` 코드를 수정할 때는 [`docs/mobile/constitution.md`](docs/mobile/constitution.md)를 먼저 읽는다. 소스 파일별 명세 문서 매핑, 기능 추가 체크리스트, 테스트·명세 작성 규칙이 정의되어 있다.

---

## 명령어

```bash
# 루트 (웹 기본)
npm run dev          # Next.js dev server (Turbopack)
npm run build        # Next.js production build
npm test             # TypeScript check + Jest (web) + Jest (mobile)
npm run lint         # ESLint (web)

# 웹만 (apps/web)
npm run test --workspace=apps/web          # tsc --noEmit && jest
npm run test:watch --workspace=apps/web    # jest --watch
npm run test:e2e --workspace=apps/web      # Playwright

# Jest 단일 실행
npx jest path/to/__tests__/route.test.ts --workspace=apps/web
npx jest -t "test name" --workspace=apps/web

# 모바일만 (apps/mobile)
npm test --prefix apps/mobile              # Jest 단위 테스트
npm run e2e:build --prefix apps/mobile     # Detox 빌드 (네이티브 코드 변경 시에만)
npm run e2e:test --prefix apps/mobile      # Detox E2E (웹 dev 서버 필수)
```

> **중요**: `npm run build` 실행 전 dev 서버를 반드시 종료한다 (`.next` 충돌 발생).
> 커밋 전 순서: `npm run build` → `npm test` (모두 통과 후 커밋).

---

## 아키텍처

**모노레포** (npm workspaces):
```
apps/web/        → Next.js 15 PWA (App Router)
apps/mobile/     → Expo iOS (React Native)
packages/shared/ → 공통 TypeScript 타입
```

### 웹 앱 (`apps/web`)

- `app/api/` — REST API Route Handlers (Next.js App Router)
- `app/[locale]/` — 다국어 페이지 (en/ko). `next-intl` 기반, `/checkin` → `/en/checkin` 자동 리다이렉트
- `components/` — React 컴포넌트 (Tailwind CSS)
- `hooks/` — 커스텀 훅
- `lib/` — 유틸리티, Supabase 클라이언트
- `i18n/` — next-intl routing.ts, request.ts
- `messages/` — 웹 i18n 메시지 (en.json, ko.json)

경로 alias: `@/` → `apps/web/`

**기술 스택**: Next.js 15 / TypeScript / Tailwind CSS / Google Maps API / exifr / browser-image-compression / next-intl / Vercel 배포

### 모바일 앱 (`apps/mobile`)

Expo React Native (iOS). CRUD는 Supabase JS SDK 직접 호출, Places / Calendar / AI 등 서버 비밀 키가 필요한 기능만 Next.js REST API 경유.

- `src/lib/api/` — 도메인별 API 모듈 (`trips.ts`, `checkins.ts`, `nearby.ts`, `storage.ts`, `places.ts`, `calendar.ts`, `settings.ts`, `rest-client.ts`, `supabase-client.ts`)
- `src/lib/api.ts` — 하위 호환 re-export (점진적 제거 예정)
- `src/lib/supabase.ts` — Supabase 클라이언트 (iOS Keychain 세션 저장)
- `src/store/` — Zustand 전역 상태 (trips, checkins)
- `src/hooks/` — 데이터 훅
- `src/screens/` — 화면 컴포넌트
- `src/i18n/` — i18next 초기화, en.json/ko.json 메시지

모바일 환경변수 파일:
- `.env.development` — 시뮬레이터 (`EXPO_PUBLIC_API_URL=http://localhost:3000`)
- `.env.production` — 실기기 (`EXPO_PUBLIC_API_URL=https://...vercel.app`)

모바일 실행:
- 시뮬레이터: `npx expo run:ios`
- 실기기: `npx expo run:ios --device --configuration Release`
- E2E 빌드: `cd apps/mobile && npm run e2e:build` (네이티브 코드 변경 시에만)
- E2E 테스트 전 웹 dev 서버 필수, 시뮬레이터에 로그인 세션 필요

### 인증

`getAuthenticatedClient(request)` (`lib/supabase/server.ts`) — 단일 함수로 두 가지 방식 처리:
- **쿠키**: 웹 브라우저 세션 (자동)
- **Bearer 토큰**: 모바일 앱 (`Authorization: Bearer <access_token>`)

모든 인증 필요 API 라우트는 이 함수를 사용한다.

### 공유 패키지

`packages/shared/src/types.ts` — `Trip`, `Checkin`, `TripFormData`, `CheckinInsert` 등.
웹·모바일 모두 `@travel-companion/shared`로 import.

`packages/shared/src/utils/` — 공통 순수 함수:
- `trip.ts` — `buildTripMetaMap()` (cover_photo_url, first_checkin_date 계산)
- `date.ts` — `formatTripDate()`, `formatDateDisplay()`, `parseLocalDate()`, `toISODateString()`
- `geo.ts` — `haversineDistance()`

`packages/shared/messages/` — 웹·모바일 공통 i18n 메시지 (카테고리 레이블 등).

---

## 개발 가이드라인

### Git
- 한국어/영어 커밋 메시지 혼용 가능
- Feature branch 사용, 주요 기능 완성 시 커밋
- main 브랜치 push → Vercel 자동 배포
- **커밋 전 반드시**: `npm run lint` → `npm run build` → `npm test` (모두 통과 후 커밋)
  - `npm run lint` 결과에 error 또는 warning이 하나라도 있으면 커밋하지 않는다
- **dev 서버 실행 중 `npm run build` 금지** (`.next` 충돌 발생)
- AI 에이전트가 작성한 커밋에는 사용한 도구의 co-author 라인을 추가한다.

  **일반 형식**:
  ```
  Co-Authored-By: <ToolName> <model-or-version> <noreply-email>
  ```
  - `<ToolName>` — AI 도구 이름 (필수)
  - `<model-or-version>` — 모델/버전 식별자 (도구 관행에 따라 공백·대괄호 등 자유 형식, 생략 가능)
  - `<noreply-email>` — 해당 서비스의 noreply 이메일

  **도구별 예시**:
  ```
  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
  Co-Authored-By: Copilot <223556219+Copilot@users.noreply.github.com>
  Co-Authored-By: opencode[claude-sonnet-4.6] <opencode@noreply>
  ```

### 코드 스타일
- TypeScript strict mode
- ESLint + Prettier
- 함수형 컴포넌트 + Hooks
- 컴포넌트 기반 아키텍처
- 모바일 앱에서 이미지를 표시할 때는 `react-native`의 `Image` 대신 **`expo-image`의 `Image`를 사용**한다. 메모리+디스크 캐시를 제공하며 `resizeMode` → `contentFit`으로 prop명이 다르다. 캐싱 전략 상세: `docs/cache.md`

---

## 주요 컨벤션

### API Route 패턴

```typescript
// 모든 인증 필요 라우트
export async function GET(request: Request) {
  const { user, supabase } = await getAuthenticatedClient(request);
  if (!user) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  // ...
}
// 에러 응답은 항상 { error: 'message' } 형태
```

### API Route 테스트

- 테스트는 route 파일 옆 `__tests__/route.test.ts`에 위치
- 파일 최상단에 `/** @jest-environment node */` pragma 필수
- `@/lib/supabase/server` mock 후 `getAuthenticatedClient` 주입 패턴
- `docs/api/` 문서에 명시된 응답 필드가 실제 응답에 포함되는지 assertion으로 검증
- **클라이언트 필수 필드 검증**: 클라이언트(웹·모바일)가 분기 로직·URL 생성·표시에 사용하는 필드는
  별도 케이스로 타입과 존재를 명시적으로 assert한다. 케이스 이름은 `'클라이언트 필수 필드가 응답에 포함된다'`.

  ```typescript
  it('클라이언트 필수 필드가 응답에 포함된다', async () => {
    // ...mock 설정...
    const place = body.place;
    // place_id: 지도 링크 생성 분기 로직에 사용 (없으면 좌표 링크로 폴백)
    expect(typeof place.place_id).toBe('string');
    expect(place.place_id.length).toBeGreaterThan(0);
    // latitude, longitude: 지도 이동 및 좌표 링크 생성에 사용
    expect(typeof place.latitude).toBe('number');
    expect(typeof place.longitude).toBe('number');
  });
  ```

### API 응답 타입 관리

- **응답 타입은 `packages/shared/src/types.ts`에 정의**하고, 웹·모바일이 함께 참조한다.
- API Route Handler는 응답 객체에 `satisfies <SharedType>`을 붙여 컴파일 타임에 필드 누락을 검출한다.

  ```typescript
  import type { PlaceDetails } from '@travel-companion/shared';
  return NextResponse.json({ place: { name, place_id, latitude, longitude } satisfies PlaceDetails });
  ```

- 외부 API(Google 등)를 경유하는 엔드포인트에서는 요청 시 이미 알고 있는 ID를 응답 폴백으로 보존한다.

  ```typescript
  // 외부 API 응답에 place_id가 빠져도 요청 ID로 보존
  setSelectedPlace({ name: details.name || fallbackName, place_id: details.place_id || requestedPlaceId });
  ```

### 문서 업데이트 규칙

| 변경 대상 | 함께 업데이트할 문서 |
|-----------|---------------------|
| `apps/web/app/api/**` Route Handler 추가/수정 | `docs/api/<endpoint>.md` + 해당 `__tests__/route.test.ts` |
| 웹 컴포넌트/화면/훅 추가·변경 | `docs/ui/web.md` |
| 모바일 컴포넌트/화면/훅 추가·변경 | `docs/ui/mobile.md` |
| API 응답 필드 추가/제거 | 해당 엔드포인트를 호출하는 `apps/mobile/src/lib/api/` 모듈의 인터페이스 확인 |
| 모바일 API 인터페이스 필드 추가 | 대응하는 서버 라우트 응답 + `__tests__/route.test.ts` |

---

## 환경변수

**Web** (`apps/web/.env.local`):
```
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=
NEXT_PUBLIC_PHOTO_CDN_URL=     # Cloudflare Worker URL (이미지 CDN)
GEMINI_API_KEY=                # 서버 전용 (AI 기능)
GEMINI_MODEL=                  # 선택사항, 기본값 gemini-2.5-flash-lite
GOOGLE_CLIENT_ID=              # Google Calendar 연동
GOOGLE_CLIENT_SECRET=          # Google Calendar 연동
```

**Mobile** (`apps/mobile/.env.development` / `.env.production`):
```
EXPO_PUBLIC_SUPABASE_URL=
EXPO_PUBLIC_SUPABASE_ANON_KEY=
EXPO_PUBLIC_API_URL=http://localhost:3000   # development
EXPO_PUBLIC_API_URL=https://...            # production
EXPO_PUBLIC_PHOTO_CDN_URL=                 # Cloudflare Worker URL (이미지 CDN)
```

---

## 문서

| 문서 | 위치 | 설명 |
|------|------|------|
| 아키텍처 | `docs/architecture.md` | 전체 시스템 구성, 성능·보안·AI·테스트 |
| API | `docs/api/` | 웹 REST API 엔드포인트 명세 |
| 웹 UI | `docs/ui/web.md` | 웹 화면/컴포넌트/훅 |
| 모바일 UI | `docs/ui/mobile.md` | 모바일 화면/컴포넌트/훅/백엔드 연계 |
| **모바일 개발 헌법** | **`docs/mobile/constitution.md`** | **모바일 소스 파일별 명세·테스트 규칙 (모바일 수정 시 필독)** |
| 모바일 컴포넌트 명세 | `docs/mobile/component-specs.md` | `components/` 동작 요구사항 |
| 모바일 화면 섹션 명세 | `docs/mobile/screen-section-specs.md` | `screens/` 서브컴포넌트 동작 요구사항 |
| 모바일 스토어 명세 | `docs/mobile/store-specs.md` | Zustand 스토어·RootNavigator 동작 요구사항 |
| DB & 인증 | `docs/db_and_auth.md` | Supabase 스키마, RLS, OAuth 설정 |
| 성능 | `docs/performance_cloudfare.md` | Cloudflare Worker 캐싱 전략 |
| 보안 | `docs/security.md` | 이미지 접근 제어 방안 |
