---
name: go-middleware-context-injection
description: Chi middleware that resolves workspace membership and injects workspace ID and member record into request.Context(), with typed accessors and shared context keys.
category: architecture
version: 1.0.0
tags: [go, chi, middleware, multi-tenancy, context]
source_type: extracted-from-git
source_url: https://github.com/multica-ai/multica.git
source_ref: main
source_commit: 6cd49e132de7632b1f2aaa675c98e8eca9308bb7
source_project: multica
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
confidence: high
---

## When to use

- Go HTTP service with multi-tenant workspaces.
- You want every workspace-scoped handler to receive a pre-validated workspace ID and member record, not re-resolve them per-route.

## Steps

1. Private context keys to avoid collision with stdlib:
   ```go
   type contextKey int
   const (
       ctxKeyWorkspaceID contextKey = iota
       ctxKeyMember
   )
   ```
2. Typed accessors — exported so handlers never read raw context values:
   ```go
   func WorkspaceIDFromContext(ctx context.Context) string {
       id, _ := ctx.Value(ctxKeyWorkspaceID).(string)
       return id
   }
   func MemberFromContext(ctx context.Context) (db.Member, bool) {
       m, ok := ctx.Value(ctxKeyMember).(db.Member)
       return m, ok
   }
   func SetMemberContext(ctx context.Context, wsID string, m db.Member) context.Context {
       ctx = context.WithValue(ctx, ctxKeyWorkspaceID, wsID)
       return context.WithValue(ctx, ctxKeyMember, m)
   }
   ```
3. Resolver extracted from request — supports multiple identifier shapes in priority order. Return three outcomes: success, "no identifier" (400), "invalid identifier" (404):
   ```go
   var errWorkspaceNotFound = errors.New("workspace not found")
   type workspaceResolver func(*http.Request) (string, error)

   func resolveWorkspaceUUID(q *db.Queries) workspaceResolver {
       return func(r *http.Request) (string, error) {
           if slug := r.Header.Get("X-Workspace-Slug"); slug != "" {
               ws, err := q.GetWorkspaceBySlug(r.Context(), slug)
               if err != nil { return "", errWorkspaceNotFound }
               return ws.ID.String(), nil
           }
           if id := r.Header.Get("X-Workspace-ID"); id != "" { return id, nil }
           return "", nil
       }
   }
   ```
4. Middleware factory that optionally enforces role:
   ```go
   func RequireWorkspaceMember(q *db.Queries) func(http.Handler) http.Handler {
       return buildMiddleware(q, resolveWorkspaceUUID(q), nil)
   }
   func RequireWorkspaceRole(q *db.Queries, roles ...string) func(http.Handler) http.Handler {
       return buildMiddleware(q, resolveWorkspaceUUID(q), roles)
   }
   func buildMiddleware(q *db.Queries, resolve workspaceResolver, roles []string) func(http.Handler) http.Handler {
       return func(next http.Handler) http.Handler {
           return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
               wsID, err := resolve(r)
               if err != nil { writeError(w, 404, "workspace not found"); return }
               if wsID == "" { writeError(w, 400, "workspace identifier required"); return }
               userID := r.Header.Get("X-User-ID")
               if userID == "" { writeError(w, 401, "not authenticated"); return }
               m, err := q.GetMemberByUserAndWorkspace(r.Context(), ...)
               if err != nil { writeError(w, 404, "workspace not found"); return }
               if len(roles) > 0 && !contains(roles, m.Role) { writeError(w, 403, "forbidden"); return }
               next.ServeHTTP(w, r.WithContext(SetMemberContext(r.Context(), wsID, m)))
           })
       }
   }
   ```
5. Mount with chi:
   ```go
   r.Route("/api", func(r chi.Router) {
       r.Use(auth.RequireAuth)
       r.Group(func(r chi.Router) {
           r.Use(middleware.RequireWorkspaceMember(queries))
           r.Get("/issues", listIssues)
           r.Post("/issues", createIssue)
       })
       r.Group(func(r chi.Router) {
           r.Use(middleware.RequireWorkspaceRole(queries, "admin", "owner"))
           r.Delete("/workspace", deleteWorkspace)
       })
   })
   ```

## Example

In a handler:
```go
func listIssues(w http.ResponseWriter, r *http.Request) {
    wsID := middleware.WorkspaceIDFromContext(r.Context())
    member, _ := middleware.MemberFromContext(r.Context())
    issues, err := queries.ListIssuesByWorkspace(r.Context(), wsID)
    // ...
}
```

## Caveats

- Keep resolver priority deterministic and document it — frontend uses slug, CLI uses UUID, and a legacy client might send both. Decide which wins and stick to it.
- "not authenticated" (401) is different from "not a member of this workspace" (404) is different from "member but wrong role" (403). Return the right status or UX is confused.
- Consider caching slug→UUID lookup (slug is immutable) if it shows up in p99 latency.
