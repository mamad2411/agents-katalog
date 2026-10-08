# cmd/ — Lambda entry points

| Function | Routes | Notes |
|---|---|---|
| `interactions` | `/api/v1/likes`, `/api/v1/comments`, `/api/v1/comments/{id}/like`, `/api/v1/geo`, `/api/v1/visits` | Likes + comments + visits/geo; DynamoDB + SES (admin notification on new comment, sent synchronously, best-effort). `/geo` reflects CloudFront-Viewer-* headers; `/visits` (GET/POST) tracks per-country visit counts |
| `contact` | `/api/v1/contact`, `/api/v1/subscriptions`, `/api/v1/subscriptions/confirm` (POST) | Contact email + double-opt-in subscriptions; DynamoDB rate limits/tokens, SES email/contact list |
| `admin` | `/api/v1/admin/comments...` (GET/PUT/DELETE) | Comment moderation; protected in prod by the authorizer |
| `authorizer` | n/a — `lambda.Start(auth.HandleRequest)` | API Gateway TOKEN authorizer doing Basic Auth; **not a chi app** |
| `notifications` | n/a — S3 event handler | Validates `notification-events/*.json`, deduplicates by commit SHA, lists SES topic opt-ins, sends update mail |

Gotchas:

- Each HTTP lambda builds its router in one `newRouter(...)` function, called from both
  `init()` and `main()`'s local-server branch — edit routes there.
- The **authorizer is never deployed locally** — `deploy-localstack.sh` skips it and the
  local API Gateway uses `authorization NONE`, so admin endpoints are open in LocalStack.
  It is only built/deployed by CI.
- `admin/main.go` mounts the handler under `/api/v1/admin` and the handler's own routes
  are prefixed `/comments` — the effective paths are `/api/v1/admin/comments[/{id}]`.
- Prod builds are linux/arm64 `provided.al2023` with handler binary named `bootstrap`;
  local LocalStack builds are amd64.
