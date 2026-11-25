---
name: ks-react
description: React + TypeScript + Vite 프로젝트 구조 및 UI 규칙. Knock client 기준 FSD-lite 레이어, MUI 9 테마/토큰, shared/ui·form 컴포넌트 계층을 적용합니다.
---

# KS React

Knock `client/`를 기준으로 한 KS 개인 프로젝트 React 규칙.

## 폴더 구조 (FSD-lite)

```txt
src/
├── app/          # Router, ProtectedRoute, Providers
├── api/          # axios, endpoints, domain API, mock
├── stores/       # zustand (use*Store.ts)
├── pages/        # <route>/ui/<Name>Page.tsx — widget 조합만
├── widgets/      # kebab-case/ + PascalCase.tsx
└── shared/
    ├── theme/    # tokens.ts, darkTheme.ts
    ├── ui/       # Panel, SectionHeader, SplitPane, StatusChip, EmptyState
    ├── form/     # KeyValueTable, HttpMethodSelect, BodyEditor, VariableHintTextField
    ├── components/index.ts  # barrel re-export
    ├── hooks/
    └── utils/
```

## 레이어 역할

- **pages**: 상태 최소, widget 배치만
- **widgets**: 도메인 UI 블록 (Query + Zustand 연동)
- **shared/ui**: 레이아웃·표시 primitive
- **shared/form**: 입력·편집 컴포넌트
- **api**: mock/real 동일 시그니처

## 스타일링 (MUI 9)

- `sx` + `createTheme` `styleOverrides` 사용
- `styled()` / `@emotion/styled` 지양
- spacing·layout 값은 `shared/theme/tokens.ts` 참조 (magic number 금지)
- `size="small"` 기본 (theme `defaultProps`)
- MUI 9 slot API: `slotProps` (deprecated `*TypographyProps` 대신)

## UI 위계

1. `SectionHeader` — 11px uppercase section label + optional actions
2. `Panel` — paper 배경, 12px padding, optional border
3. Content — tabs, tables, editors

## 액션 버튼 규칙

- **contained primary**: 화면당 하나 (Send)
- **outlined**: Save, secondary actions
- **text**: Manage, Add row

## 네이밍

| 영역 | 규칙 |
|------|------|
| widgets | `widgets/app-shell/AppShell.tsx` |
| pages | `pages/login/ui/LoginPage.tsx` |
| stores | `useAuthStore.ts` |
| api | `api/auth/authApi.ts` |
| path alias | `@/*` → `src/*` |

## 참고 문서

- Knock UI spec: `client/docs/ui-spec.md`
- Knock architecture: `client/docs/architecture.md`
