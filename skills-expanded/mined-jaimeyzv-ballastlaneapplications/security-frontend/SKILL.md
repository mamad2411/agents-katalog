---
name: security-frontend
description: Frontend security for BallastLane's cookie-based auth — no token storage (HttpOnly cookie is the only credential), a functional interceptor adding withCredentials to every request, centralized 401→logout with double-invocation guards, optimistic/idempotent logout, the authGuard vs noAuthGuard pair, and XSS/[innerHTML] safety. Load this skill when wiring the interceptor, guards, logout flow, or reviewing frontend security.
---

# Security — Frontend

⚠️ Confirmed real pattern is **cookie-based auth end to end**, matching the backend's `HttpOnly`/`Secure`/`SameSite=None` cookies (see the `security-backend` skill). There is **no Bearer-token storage** anywhere on the frontend.

## No Manual Token Handling

- **There is no token to store on the frontend.** The backend sets `HttpOnly` cookies, which JavaScript cannot read by design — a feature, not a gap to fill. Don't add `localStorage`/`sessionStorage` token storage or a `token()` signal; there's nothing to put in it.
- **Session state is a derived boolean**, not a stored credential — see `AuthService`'s `BehaviorSubject<boolean>` in the `angular-feature-based` skill. The only "credential" the browser holds is the cookie itself, managed by the browser's cookie jar, invisible to app code.

## Every Request Carries Credentials — Confirmed Real Pattern

- **A functional `HttpInterceptorFn` clones every outgoing request with `withCredentials: true`**, ensuring cookies are sent cross-origin to the API. This replaces the Bearer-token-attaching interceptor pattern entirely.

```typescript
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const interceptorService = inject(InterceptorService);
  const authReq = req.clone({ withCredentials: true });
  return next(authReq).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401) interceptorService.handleUnauthorized();
      return throwError(() => error);
    })
  );
};
```

- **401 handling is centralized in the interceptor**, delegating to a small `InterceptorService` → `LogoutService` chain rather than handling logout inline. This indirection exists specifically to avoid a circular dependency between the interceptor function and the logout flow — keep the separation.

## Logout — Confirmed Real Pattern Is Optimistic + Idempotent

- **Client-side state clears immediately**, the backend logout call fires without blocking navigation, and failures are only warned about, not surfaced — the user is always taken to `/login` regardless of whether the backend call succeeds. A deliberate UX choice, not an oversight.
- **Double-invocation guards exist at two levels** — `InterceptorService.isHandling` and `LogoutService.isLoggingOut` (the latter with a `setTimeout` reset) — because a burst of concurrent 401s could otherwise trigger logout multiple times. Route any new logout-triggering call sites through `LogoutService`; don't duplicate the guard logic.

## Route Guards — Two Distinct Shapes, Both Real

- **`authGuard`** (protect a route that requires a session): check the synchronous `isAuthenticated` flag first for a fast path; if false, make a live call to `/api/auth/validate` (the real source of truth) before denying — don't trust a stale local flag alone to deny access.
- **`noAuthGuard`** (protect a route that requires *no* session, e.g. login/register): wait for `authService.initComplete`, then redirect away if already authenticated. Applying the wrong guard shape is a common copy-paste mistake — confirm which a new route needs.

```typescript
export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  if (authService.isAuthenticated) return of(true);
  return http.get<boolean>(apiUrl, { observe: 'response' }).pipe(
    map(response => response.ok),
    catchError(() => { logoutService.logout(); return of(false); })
  );
};

export const noAuthGuard: CanActivateFn = () => {
  return from(authService.initComplete).pipe(
    switchMap(() => authService.isAuthenticated$.pipe(
      take(1),
      switchMap(isAuth => isAuth ? (router.navigate(['/tasks']), of(false)) : of(true))
    ))
  );
};
```

## XSS & Safe Rendering

- **Never use `[innerHTML]` with unsanitized user/API input.** Render task titles/descriptions via standard interpolation (`{{ task.title }}`), which Angular escapes by default.
- **`HttpOnly` cookies already remove JWT theft-via-XSS as an attack path** — a successful XSS here can't read the auth cookie. It can still act *as* the logged-in user (the browser attaches the cookie automatically), so input sanitization and avoiding `[innerHTML]` still matter — for a different reason than token theft.

## Environment Configuration

- **API base URL lives in `environment.apiBaseUrl`** (`@env/environment`) — every service builds its URL from this, not a hardcoded string.
- **No secrets belong in frontend code.** There's no token to leak under this cookie-based model; the same rule applies to anything else sensitive (third-party API keys stay backend-only).
