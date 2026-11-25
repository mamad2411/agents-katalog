---
name: error-handling-frontend
description: Angular error-handling strategy for BallastLane — a single HttpInterceptor that normalizes backend ProblemDetails into one AppError type, services that propagate (never swallow) errors, per-component visible error state, and 401→logout routing. Load this skill when adding an HTTP call, wiring the error interceptor, or handling failure/validation states in a component.
---

# Error Handling — Frontend

## Centralized HTTP Errors

- **One `HttpInterceptor` handles ProblemDetails responses from the backend** — it parses the RFC 9457 shape the `error-handling-backend` skill guarantees, and normalizes it into a single app-level error type before it reaches any component.
- **DON'T** parse or branch on raw HTTP error shapes inside individual services or components — that logic belongs in the interceptor, once.

```typescript
// DO — interceptor normalizes once
@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<unknown>, next: HttpHandler) {
    return next.handle(req).pipe(
      catchError((err: HttpErrorResponse) => {
        const appError = toAppError(err); // maps ProblemDetails -> AppError
        return throwError(() => appError);
      })
    );
  }
}
```

## Service-Level Error Handling

- **Services propagate errors, they don't swallow them.** A service method returns the `Observable` as-is (post-interceptor); it doesn't `catchError` and return a default/empty value unless that's a genuine, intentional fallback (e.g. "no tasks yet" is not an error).

```typescript
// DO
getAll(): Observable<Task[]> {
  return this.http.get<Task[]>(`${this.apiUrl}/tasks`);
}

// DON'T — silently swallowing errors makes failures invisible to the component
getAll(): Observable<Task[]> {
  return this.http.get<Task[]>(`${this.apiUrl}/tasks`).pipe(catchError(() => of([])));
}
```

## Component-Level Error State

- **Every component that triggers an HTTP call exposes a visible error state** (a signal like `error = signal<string | null>(null)`, or a local `errorMessage`/`showError` field to match the auth components — see the `angular-feature-based` skill), shown in the template — never a silently failed action with no feedback.
- **Validation errors (400) render inline near the relevant field**; auth errors (401) redirect to login; not-found (404) shows an explicit empty/not-found state; server errors (500) show a generic retry message — don't show raw backend error text to the user.

```typescript
// DO
createTask() {
  this.taskService.create(this.form.value).subscribe({
    next: () => this.router.navigate(['/tasks']),
    error: (err: AppError) => this.error.set(err.userMessage),
  });
}
```

## Auth-Specific Handling

- **401 responses trigger the auth interceptor's logout/redirect flow**, not a generic error banner — keep this distinct from other error types since it needs a different user action (log in again) rather than "something went wrong." See the `security-frontend` skill for the `InterceptorService`→`LogoutService` chain that owns this.
