# auth feature

회원가입(=Google OAuth 첫 로그인) / 로그인 / 로그아웃 / 회원탈퇴.

- Auth.js v5 (`next-auth@5`) + `@auth/drizzle-adapter` + Neon Postgres.
- 세션 전략: **database**. 회원탈퇴 시 `users` 한 행 삭제 → ON DELETE CASCADE로 `accounts`/`sessions` 정리.
- 서버 액션은 `api/actions.ts`에 모음 (`signInWithGoogle`, `signOutAction`, `deleteAccountAction`).
- 클라이언트 컴포넌트는 직접 `signIn`/`signOut`을 호출하지 말고 위 server action을 통해서만 호출.
- Auth.js handler는 `model/handlers.ts` → `app/api/auth/[...nextauth]/route.ts`에서 재export.
- `auth()` 호출하는 페이지는 `export const dynamic = 'force-dynamic'`로 빌드 타임 정적화 회피.
- 새 보호 라우트 추가 시: 페이지 상단에서 `const session = await auth(); if (!session) redirect('/login')`.
