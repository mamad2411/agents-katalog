# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quy tắc làm việc (bắt buộc đọc)

Bộ rule chi tiết nằm ở **[AGENTS.md](./AGENTS.md)** — đọc trước khi sửa backend. Những điểm cốt lõi:

- Mặc định chọn giải pháp **đơn giản nhất nhưng robust**. Phản kháng đề xuất tách thêm service, thêm DB/broker/framework mới khi PostgreSQL + những gì repo đang có đã đủ.
- Giữ đúng phân tầng `handler → service → repository`: handler không viết SQL, repository không biết HTTP status, service không nhận `echo.Context`, gateway không chứa business rule của domain service.
- **Không được vô tình làm yếu các reliability pattern** là xương sống của hệ thống: transaction bundle (`createOrderTx`, `RunInTx`), SQL compare-and-set (`UpdateStock`, `ApplyWebhookResult`), row lock (`lockAndConsumeCoupon`, `FOR UPDATE`), cursor pagination, lease-claim async (`ClaimPendingOutbox`), outbox/inbox/idempotency. Làm yếu pattern nào phải giải trình rõ trong PR.
- Docs ở root/`docs/` phải khớp path source thật. Nếu route/runtime/flow/contract đổi thì cập nhật docs tương ứng ngay trong cùng thay đổi (xem AGENTS.md §18 và §20 về vai trò từng file docs).
- Ngôn ngữ tài liệu và commit trong repo là tiếng Việt — giữ nhất quán.

## Lệnh thường dùng

Backend chạy qua `Makefile` (từ root). Mỗi target lặp qua từng Go module:

```bash
make ci          # fmt + tidy + vet + test — chạy trước khi coi PR là "ổn"
make test        # go test ./... cho từng module
make vet         # go vet ./...
make fmt         # gofmt toàn bộ backend
make tidy        # go mod tidy từng module
```

**Chạy 1 test / test của 1 service**: mỗi service là một Go module độc lập, phải `cd` vào module rồi mới `go test` (chạy `go test` từ root sẽ không thấy code):

```bash
cd services/order-service && go test ./...                          # toàn bộ 1 service
cd services/order-service && go test ./internal/service/order/...   # 1 package
cd services/order-service && go test ./internal/handler/ -run TestCreateOrder -v   # 1 test
```

Docker / runtime local:

```bash
make docker-config     # render deployments/docker/docker-compose.yml từ .env.local (fallback .env.example)
make compose-up        # build + up toàn stack
make compose-down
make migrate-up        # migrate-down / migrate-force cũng có
```

Frontend (thư mục `client/`, React 18 + Vite + TS):

```bash
make client-install    # hoặc: cd client && npm install
make client-dev        # vite dev server
make client-build      # tsc -b && vite build
cd client && npm run lint      # eslint
```

Sau `compose-up`, smoke check: `curl http://localhost:8080/health` (gateway) và `curl http://localhost/health` (Nginx edge). Public API test qua `api-gateway` (`:8080`); Postgres/Redis/RabbitMQ **không** publish port ra host mặc định.

Contract public đầy đủ xem ở `http://localhost:8080/swagger` (Swagger UI) hoặc `/openapi.yaml`. Spec là file **viết tay** ở `api-gateway/internal/docs/openapi.yaml`, nhúng vào binary bằng `go:embed` — **thêm/xoá/đổi route ở `api-gateway/internal/handler/` thì phải sửa spec trong cùng thay đổi**, nếu không `api-gateway/internal/docs/docs_test.go` sẽ đỏ (test so khớp hai chiều với `e.Routes()` thật).

## Kiến trúc (big picture)

Backend là **monorepo Go đa-module** — `pkg/`, `proto/`, `api-gateway/` và mỗi `services/*-service/` đều có `go.mod` riêng (danh sách đầy đủ ở biến `MODULES` trong Makefile). Không có go.work; đây là lý do phải `cd` vào module khi test/build lẻ.

Tổ chức theo domain, giao tiếp qua HTTP (public), gRPC (nội bộ) và RabbitMQ (event bất đồng bộ):

- **`api-gateway/`** — reverse proxy HTTP (Echo) là entrypoint public duy nhất: tracing, metrics, Redis rate limiter, retry chọn lọc, circuit breaker. Không nhồi business logic vào đây.
- **`user-service` / `product-service` / `order-service` / `payment-service`** — mỗi cái một PostgreSQL database riêng (`ecommerce_user`, `ecommerce_product`, `ecommerce_order`, `ecommerce_payment`). PostgreSQL là source of truth chính. **Không dùng ORM** — persistence qua `database/sql` + `lib/pq` + SQL migration (auto-run khi startup).
- **`cart-service`** — dùng Redis làm storage chính, không có SQL migration.
- **`product-service`** cung cấp gRPC cho `cart-service` và `order-service` để verify product truth; tích hợp **optional** MinIO (media) và Elasticsearch (search) — phải degrade gracefully khi chúng lỗi.
- **`order-service` / `payment-service`** phát event qua RabbitMQ bằng **outbox pattern**; `payment-service` xử lý MoMo webhook với idempotency + inbox/outbox.
- **`notification-service`** consume RabbitMQ bằng **inbox pattern** + Redis dedupe, có email worker và wishlist alert worker; downstream phải chịu được duplicate delivery.

Sơ đồ luồng, bảng thành phần và hạ tầng đầy đủ ở [README.md](./README.md).

Mỗi service theo layout: `cmd/main.go` (wiring thật) → `internal/handler` (API boundary, có thể có `internal/grpc`) → `internal/service` (business logic) → `internal/repository` (SQL/Redis/RabbitMQ) → `internal/model`, `internal/dto`. `pkg/` giữ shared: `config`, `database`, `logger`, `middleware`, `observability`, `response`, `validation`. `proto/` là gRPC contract.

### Config

`Makefile` → `.env.local` (fallback `.env.example`) → Docker Compose mount `deployments/docker/config/<service>.yaml` vào container qua `CONFIG_PATH` → `pkg/config` load default + file + env override. Thêm config production-critical: thêm vào `pkg/config`, đặt default local an toàn, cập nhật YAML trong `deployments/docker/config/`, cập nhật `.env.example`; startup phải **fail fast** nếu thiếu secret/endpoint bắt buộc.

Môi trường phân biệt qua `APP_ENV` (default `development`). Với `APP_ENV=production`, `pkg/config.Load` chạy `validateProductionSecrets` và từ chối khởi động nếu còn secret mặc định (JWT, DB/RabbitMQ password, webhook secret, pepper, MinIO key, dev accounts). Thêm secret mới thì thêm cả check vào hàm này và biến vào `.env.production.example`. Production chạy qua `make docker-config-prod` / `compose-up-prod` với `.env.production`.

## Khi debug / audit

README có bảng **"Hot Path Khi Audit Issue"** map từng triệu chứng (order tạo lặp, coupon dùng quá số lần, payment webhook replay, inventory oversell, notification gửi lặp, refund worker kẹt...) tới file/function cụ thể. Bắt đầu từ đó thay vì grep mù.

## Tài liệu tham chiếu

- [AGENTS.md](./AGENTS.md) — bộ rule đầy đủ (kiến trúc, clean code, error handling, DB, security, testing, review checklist).
- [HUONG_DAN_CHAY.md](./HUONG_DAN_CHAY.md) — chạy toàn bộ hệ thống từ đầu (backend compose + frontend + test + lỗi thường gặp).
- [DOCKER_GUIDE.md](./DOCKER_GUIDE.md) — compose/runtime/debug local stack.
- [API_TESTING_GUIDE.md](./API_TESTING_GUIDE.md) — route public, smoke/negative/idempotency/webhook-replay flow.
- [LOGIC_FLOW.md](./LOGIC_FLOW.md) — flow end-to-end từ API boundary xuống service/repository/async worker.
- [PROJECTS.md](./PROJECTS.md) — trạng thái triển khai theo feature/layer, test/verify/deploy checklist.
- [FRONTEND_GUIDELINES.md](./FRONTEND_GUIDELINES.md) — quy ước cho `client/`.
- [docs/README.md](./docs/README.md) — bản đồ tài liệu (annotated source map, deep-dive runtime, learning roadmap).

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
