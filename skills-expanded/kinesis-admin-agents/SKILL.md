# AGENTS SPECIFICATION

Generated: 2025-11-13T21:40:12.241Z
Last Updated: 2025-11-14T10:49:43.175Z

## Project Overview
Kinesis Admin: Web UI to manage AWS Kinesis data streams across multiple accounts/regions. Frontend in React/TypeScript (Vite + Bun) using Ant Design. Backend (to be added) will expose a secure REST/GraphQL API proxying AWS SDK operations (Kinesis, CloudWatch Metrics, IAM, STS) with role assumption.

## Frontend Stack
- Package manager/runtime: Bun (packageManager field in package.json)
- Build/dev: Vite
- Language: TypeScript (strict)
- UI Library: React 18 + Ant Design 5
- Entry HTML: frontend/index.html mounts root div via src/main.tsx
- Global styles: antd/dist/reset.css imported in main.tsx
- App shell & routing: Ant Design Layout (Header + Content) in src/App.tsx using react-router-dom v6.

## Planned Frontend Modules
1. Stream List: paginate, search, filter by status, region, account; row click opens Stream Overview. Includes a "Delete All Streams" button with confirmation.
2. Stream Detail: shard list, retention, encryption type, consumers, tags, enhanced monitoring. Includes a form to publish messages to the stream, a button to delete the stream, and decodes messages from Base64.
3. Shard Explorer: get iterator, sample records, throughput metrics, iterator type selection.
4. Put Test Record: form with partition key, explicit hash key, JSON payload editor + validation.
5. Scaling Wizard: propose shard split/merge actions, cost impact estimation.
6. Retention & Monitoring: adjust retention hours, enable metrics, CloudWatch charts (latency, incoming/outgoing bytes/records, iterator age).
7. Consumers Dashboard: list subscribers (KCL, Lambda, Firehose), lag estimation, last sequence processed.
8. Tag & Policy Manager: view/add/remove tags, IAM policy simulator for stream actions.
9. Multi-Account/Region Selector: dropdowns with remembered recent selections.
10. Audit Log View: show recent administrative actions (client-side until backend persists).

## Backend
- Language: Go (>=1.22) using gosoline framework.
- Entry: main.go runs gosoline application with http server module.
- Config: config.dist.yml (embedded via go:embed in main.go) defines api module and account role mappings; treat as source of truth. By default, it's configured under `cloud.aws.defaults` to use LocalStack for local development.
- API Port: 8080 (config.dist.yml api.port).
- Handler: KinesisHandler (handler.go) constructed via NewKinesisHandler (creates gosoKinesis client with alias "default"); router wiring now resides directly in main.go (no separate router.go).
- Endpoints:
  - ${API_BASE_URL}/api/list (GET) returns paginated stream names aggregated via ListStreams.
  - ${API_BASE_URL}/api/stream (DELETE, body {"streamName":"name"}) deletes a stream via DeleteStream (frontend Table action uses react-query mutation). Fallback endpoint: POST ${API_BASE_URL}/api/stream/delete for environments where DELETE routing fails.
  - ${API_BASE_URL}/api/stream/describe?streamName=name (GET) returns metadata via DescribeStream.
  - ${API_BASE_URL}/api/stream/messages?streamName=name&limit=N (GET) returns recent messages (LATEST iterator per shard).
  - ${API_BASE_URL}/api/stream/message (POST, body {"streamArn":"arn", "data":"...", "partitionKey":"..."}) publishes a message to a stream. If partitionKey is omitted, a UUIDv4 is generated.
- Dependencies: github.com/justtrackio/gosoline (core), gosoKinesis client; aws-sdk-go-v2 transitively.
- Auth (planned): Cognito/OIDC JWT -> role ARN mapping; assume role via STS per account/region.
- Observability: Use gosoline logging/metrics; add tracing later.
- Deployment: build single binary; target ECS Fargate or Lambda.
- Next Steps: pagination & region/account selection via query params; extend Stream Overview with shards list & metrics (currently uses /api/stream/describe and /api/stream/messages auto-refresh).

## Frontend Configuration
- Runtime config: API base URL loaded from /config.json (public/config.json in dev, dist/config.json after build).
- Dev mode: Vite proxies /api to backend (http://localhost:8080 or VITE_API_BASE_URL env var).
- Prod mode: Edit dist/config.json after build to configure apiBaseUrl (e.g., {"apiBaseUrl": "https://api.example.com/api"}) - no rebuild required.
- Config loading: main.tsx calls loadConfig() before rendering; components use getApiBaseUrl() from config.ts.
- Deployment: Mount or replace dist/config.json at runtime for Docker/K8s deployments.

## Security & Constraints
- Never expose long-term AWS credentials to frontend.
- Use signed backend operations; enforce input validation (partition key length, payload size < 1MB).
- Rate limit mutating actions (create/delete/scale) per user.
- Implement optimistic UI only for trivial tag edits; await confirmation for scaling/deletes.

## State Management
- Lightweight: React Query (TanStack Query) for data fetching & caching (QueryClientProvider in main.tsx).
- Global context: auth/session, selected account & region.

## Non-Functional Goals
- Fast initial load (< 150KB JS before code-splitting).
- Accessible components (Ant Design defaults + additional aria labels for custom tables).
- Dark mode (Ant Design algorithm) toggle in header.

## Testing (Future)
- Unit: Vitest + React Testing Library.
- E2E: Playwright for critical flows (list streams, put record, scale stream).

## Deployment (Future)
- Frontend: Served by Caddy web server (in Docker) or can be deployed to CDN/S3.
- Backend: AWS Lambda (API Gateway) or container (ECS/Fargate) behind ALB; prefer Lambda for simplicity.

## Agent Usage Guidelines
- When adding features, modify only necessary files under frontend/src.
- Maintain strict TypeScript; do not disable linting or tsconfig strict flags.
- Prefer Ant Design components (Table, Form, Input, Select, Card, Statistic, Tabs) over custom.
- Use React Query (once installed) for data fetching; avoid manual useEffect data loads.
- Keep functions pure; isolate AWS shape types into a dedicated types.ts when introduced.
- Always return an error from handlers on failure using fmt.Errorf; never swallow or skip shard errors (abort immediately) (added 2025-11-13T19:41:48.843Z, updated 2025-11-13T20:08:52.465Z).
- Update this file ONLY when architectural decisions change.
- **New Features (Nov 13-14, 2025):**
  - Added a "Publish Message" feature to the stream overview page.
  - Added a "Delete All Streams" feature to the stream list page.
  - Added a "Delete Stream" button to the stream overview page.
  - Messages are now decoded from Base64 in the stream overview page.
  - Frontend API base URL now configurable at runtime via config.json (no rebuild required).
  - Docker deployment now uses Caddy to serve frontend with backend on separate port (8081).

## Future Enhancements
- WebSocket/SSE for real-time shard metrics.
- Saved queries for frequent record sampling patterns.
- Export stream configuration as IaC JSON template.

End of specification.
