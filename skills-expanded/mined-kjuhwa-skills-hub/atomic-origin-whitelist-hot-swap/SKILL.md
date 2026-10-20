---
name: atomic-origin-whitelist-hot-swap
description: Go WebSocket (or CORS) origin whitelist stored in an atomic.Value so it can be reloaded without locks or restart; sensible env-driven defaults.
category: devops
version: 1.0.0
tags: [go, cors, websocket, atomic, config, hot-reload]
source_type: extracted-from-git
source_url: https://github.com/multica-ai/multica.git
source_ref: main
source_commit: 6cd49e132de7632b1f2aaa675c98e8eca9308bb7
source_project: multica
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
confidence: medium
---

## When to use

- Go HTTP/WebSocket server where the allowed-origins list may change at runtime (admin UI, SIGHUP config reload).
- You want the origin check on the request hot path to be lock-free.

## Steps

1. Store the slice in `atomic.Value`:
   ```go
   var allowedOrigins atomic.Value  // holds []string

   func init() { allowedOrigins.Store(loadFromEnv()) }

   func SetAllowedOrigins(origins []string) { allowedOrigins.Store(origins) }
   ```
2. Load with fallback chain of env vars so deployments with different conventions still work:
   ```go
   func loadFromEnv() []string {
       raw := strings.TrimSpace(os.Getenv("ALLOWED_ORIGINS"))
       if raw == "" { raw = strings.TrimSpace(os.Getenv("CORS_ALLOWED_ORIGINS")) }
       if raw == "" { raw = strings.TrimSpace(os.Getenv("FRONTEND_ORIGIN")) }
       if raw == "" {
           return []string{
               "http://localhost:3000",
               "http://localhost:5173",
               "http://localhost:5174",
           }
       }
       parts := strings.Split(raw, ",")
       out := make([]string, 0, len(parts))
       for _, p := range parts {
           if o := strings.TrimSpace(p); o != "" { out = append(out, o) }
       }
       return out
   }
   ```
3. Hot path check — no lock:
   ```go
   func checkOrigin(r *http.Request) bool {
       origin := r.Header.Get("Origin")
       if origin == "" { return true }
       for _, a := range allowedOrigins.Load().([]string) {
           if origin == a { return true }
       }
       return false
   }
   ```
4. Expose an admin-only HTTP endpoint or CLI command that calls `SetAllowedOrigins(newList)` to update without restart.
5. Log rejected origins at WARN so diagnosing "why is my new subdomain 403ing?" is easy:
   ```go
   slog.Warn("ws: rejected origin", "origin", origin)
   ```

## Example

Deployment scenario: add a new staging subdomain to the whitelist.
- Without hot-swap: edit env, restart server, all connected clients disconnect.
- With hot-swap: `POST /admin/allowed-origins` with the new list, existing connections unaffected, new connections accepted.

## Caveats

- `atomic.Value.Store` requires values of a concrete, consistent type — never store `nil` or change the stored type mid-run.
- For prefix/suffix/wildcard matching (not exact match), swap the loop for a compiled regex or matcher; keep the atomic swap.
- Origin check being permissive when `Origin` header is absent (`return true`) is standard for non-browser clients (CLI, backend-to-backend); verify it fits your threat model.
