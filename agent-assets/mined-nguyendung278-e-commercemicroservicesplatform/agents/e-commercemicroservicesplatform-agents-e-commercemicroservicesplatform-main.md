# AGENTS.md

## Mục tiêu

Repository này là một nền tảng thương mại điện tử viết chủ yếu bằng Go, tổ chức theo nhiều service, giao tiếp qua HTTP/gRPC, chạy local bằng Docker Compose, và đã có sẵn PostgreSQL, Redis, RabbitMQ, Prometheus, Grafana, Jaeger, MinIO, Elasticsearch.

Tài liệu này là bộ quy tắc làm việc dành cho mọi contributor và AI agent. Mục tiêu không phải viết cho đẹp, mà để giúp code mới:

- dễ đọc
- dễ sửa
- chạy ổn định ở production
- không tự tạo nợ kỹ thuật vô ích
- giúp người đọc trưởng thành theo hướng Senior Backend Golang

Nếu một thay đổi không làm code rõ hơn, an toàn hơn, hoặc nhanh hơn một cách có thể đo được, hãy cân nhắc không làm.

---

## 1. Bối cảnh thực tế của repo

Trước khi sửa code, hãy hiểu đúng cấu trúc hiện tại:

- `api-gateway/`: reverse proxy HTTP, không nên nhồi business logic vào đây.
- `services/*-service/`: mỗi service thường có `cmd/`, `internal/handler`, `internal/service`, `internal/repository`, `internal/model`, `internal/dto`.
- `pkg/`: shared packages như config, database, logger, middleware, observability, response, validation.
- `proto/`: contract gRPC giữa các service.
- `deployments/docker/`: local runtime gần production nhất trong repo.

Một số dependency là **bổ trợ**, không phải source of truth:

- PostgreSQL là nguồn dữ liệu chính.
- Redis chủ yếu phục vụ cart, rate limit, cache hoặc idempotency nếu thật sự cần.
- RabbitMQ dành cho event bất đồng bộ; không thay thế transaction đồng bộ.
- Elasticsearch và MinIO là optional integration; service phải degrade gracefully khi chúng lỗi.

Không viết tài liệu hoặc đề xuất như thể repo này là monolith. Cũng không mặc định đẻ thêm service mới chỉ vì repo hiện đang có nhiều service.

---

## 2. Quy tắc ra quyết định kiến trúc

Mặc định chọn giải pháp **đơn giản nhất nhưng robust**.

Khi đề xuất thay đổi kiến trúc hoặc stack, bắt buộc tự hỏi theo thứ tự này:

1. Có thể giải quyết ngay trong service hiện tại không?
2. Có thể giải quyết bằng PostgreSQL transaction, index, query tốt hơn, hoặc refactor package không?
3. Có thể tận dụng `pkg/` hiện có thay vì thêm framework mới không?
4. Thành phần mới tạo thêm failure mode gì?
5. Team sẽ phải vận hành thêm cái gì sau khi merge?

Mặc định phản kháng khi có đề xuất:

- tách thêm service mà domain chưa đủ lớn
- thêm database mới cho một nhu cầu nhỏ
- thêm broker cho luồng có thể xử lý bằng transaction đồng bộ
- thêm Kubernetes hoặc infra nặng khi Docker Compose đã đủ cho local/dev
- thêm framework backend mới vào luồng Go hiện có

Nếu vẫn buộc phải thêm thành phần mới, PR hoặc proposal phải nêu rõ:

- vấn đề hiện tại là gì
- vì sao giải pháp đơn giản hơn không đủ
- failure mode nào được giảm bớt
- cách migrate từ code hiện tại
- cách test local bằng workflow sẵn có

---

## 3. Quy ước tổ chức code trong repo này

### 3.1. Phân tầng trách nhiệm

- `handler`: parse request, validate input, gọi service, map lỗi sang HTTP/gRPC response.
- `service`: business logic, rule nghiệp vụ, orchestration giữa repository/client/broker.
- `repository`: SQL/raw persistence, transaction, lock, scan row.
- `model`: domain model hoặc persistence model.
- `dto`: request/response object cho API boundary.

Không đảo vai trò các tầng:

- handler không viết SQL
- repository không biết HTTP status code
- service không nhận `echo.Context`
- gateway không chứa business rule của domain service

### 3.2. Đường dẫn chuẩn khi thêm feature

Tài liệu và code mới phải phản ánh đúng cấu trúc hiện tại, không dùng các path đã lỗi thời như `internal/delivery/http` hay `api-gateway/main.go` nếu thực tế repo đang dùng nơi khác.

Trong repo này, đường đi đúng thường là:

- HTTP handler: `services/<service>/internal/handler/`
- gRPC handler: `services/<service>/internal/grpc/`
- main wiring: `services/<service>/cmd/main.go`
- gateway proxy: `api-gateway/internal/proxy/service_proxy.go`

### 3.3. Interface

Chỉ tạo interface khi có lợi ích rõ ràng:

- để test bằng fake/mock dễ hơn
- để tách dependency ngoài như gRPC client, search index, object storage
- để ẩn implementation chi tiết khỏi consumer

Ưu tiên đặt interface ở phía **consumer**, không đặt “repository/service interface” chỉ vì thói quen.

Nếu hệ thống hiện chỉ có một implementation và không cần fake trong test, interface có thể là thừa.

---

## 4. Clean code và readability

### 4.1. Hàm

Ưu tiên hàm:

- ngắn
- tên rõ mục đích
- ít nhánh lồng nhau
- trả lỗi sớm
- không làm nhiều hơn một việc chính

Khi một hàm bắt đầu phải cuộn màn hình nhiều lần mới đọc hết, hãy cân nhắc tách nhỏ theo intent thay vì tách cơ học.

### 4.2. Tên biến và tên hàm

- Dùng tên theo domain: `order`, `payment`, `outstanding`, `coupon`, `productID`.
- Không dùng tên mơ hồ kiểu `data`, `obj`, `temp`, `handler2`.
- Biến vòng đời ngắn có thể ngắn gọn, nhưng ở business flow thì phải nói rõ ý nghĩa.

### 4.3. Comment

Chỉ viết comment khi nó bổ sung giá trị mà code chưa tự nói được:

- lý do tồn tại của rule nghiệp vụ
- constraint production
- failure mode
- trade-off thiết kế

Không comment lại điều hiển nhiên từ code.

Comment phải bám code hiện tại. Nếu refactor làm comment sai, phải sửa hoặc xoá comment ngay trong cùng PR.

### 4.4. Một file thay đổi tốt là file làm người khác dễ đọc hơn

Khi sửa code cũ, ưu tiên sửa luôn những điểm nhỏ gây khó đọc nếu chi phí thấp:

- gom magic number thành hằng số có tên
- đổi tên biến khó hiểu
- tách helper scan/validate/normalize
- loại bỏ code chết, import thừa, branch không thể xảy ra

Không mở rộng refactor lan man vượt quá phạm vi nếu chưa chứng minh được lợi ích.

---

## 5. Error handling

### 5.1. Nguyên tắc chung

- Không nuốt lỗi im lặng.
- Không trả lỗi quá chung chung ở tầng thấp.
- Wrap lỗi bằng `%w` khi đi qua boundary quan trọng.
- Dùng `errors.Is` và `errors.As` cho domain error rõ ràng.

Ví dụ kỳ vọng:

- repository: `fmt.Errorf("failed to create order: %w", err)`
- service: map sang domain error như `ErrProductNotFound`, `ErrInvalidCursor`
- handler: map domain error sang HTTP status phù hợp

### 5.2. Không leak chi tiết nội bộ ra API

Client chỉ nên nhận:

- message đủ hiểu để hành động
- error code/message an toàn

Không trả raw SQL error, stack trace, DSN, secret, webhook secret, token hash, hoặc internal endpoint ra response.

### 5.3. Với lỗi có thể chấp nhận tạm thời

Nếu dependency phụ lỗi như search, object storage, broker, hãy cân nhắc degrade gracefully khi nghiệp vụ cho phép. Nhưng phải log đủ ngữ cảnh để điều tra.

Graceful degradation là có chủ đích, không phải nuốt lỗi vô điều kiện.

---

## 6. Logging

Repo đã dùng `zap`. Tiếp tục giữ logging dạng structured.

Mỗi log có ích phải trả lời được ít nhất một trong ba câu hỏi:

- chuyện gì vừa xảy ra
- xảy ra với entity nào
- tại sao thất bại hoặc chậm

Ưu tiên field thay vì ghép string:

- `service`
- `trace_id`, `span_id` khi có
- `user_id`, `order_id`, `payment_id`, `product_id`
- `status`, `latency_ms`, `routing_key`

Không log:

- password
- JWT/refresh token
- webhook secret
- raw Authorization header
- dữ liệu nhạy cảm không cần thiết

Không spam log mức `Error` cho lỗi business dự kiến như validation fail hoặc not found. Những lỗi đó thường nên dừng ở `Warn` hoặc map sang response mà không tạo nhiễu.

---

## 7. Context, timeout và concurrency

### 7.1. Context

- `context.Context` là tham số đầu tiên cho mọi hàm I/O hoặc có thể bị huỷ.
- Không tự tạo `context.Background()` ở deep layer trừ khi đang chủ động tạo background work có owner rõ ràng.
- Deadline/timeout phải đi cùng external call: DB, HTTP, gRPC, Redis, RabbitMQ publish quan trọng.

### 7.2. Goroutine

Không tạo goroutine nếu chưa xác định rõ:

- ai sở hữu lifecycle của nó
- khi nào nó dừng
- lỗi của nó được quan sát ở đâu
- backpressure xử lý thế nào

Mọi goroutine dài hạn phải có cơ chế dừng qua `context` hoặc signal. Tránh goroutine “thả nổi”.

### 7.3. Shared state

Nếu có thể tránh shared mutable state, hãy tránh.

Ưu tiên:

- immutable data flow
- channel khi thật sự giúp đơn giản hơn
- DB lock/version column khi bài toán là consistency dữ liệu dùng chung

Không dùng mutex như giải pháp mặc định cho bài toán vốn thuộc về transaction hoặc optimistic locking trong DB.

---

## 8. Database và query optimization

### 8.1. SQL

- Dùng parameterized query, không nối string với input người dùng.
- Chỉ select cột cần thiết.
- Đặt tên helper scan/mapper rõ ràng và tái sử dụng.
- Khi thêm query mới cho endpoint quan trọng, phải nghĩ luôn đến index.

### 8.2. Pagination

- Với bảng tăng nhanh và endpoint public/hot path, ưu tiên cursor pagination.
- Chỉ dùng `OFFSET/LIMIT` cho backoffice hoặc tập dữ liệu nhỏ, có lý do rõ ràng.
- Nếu vẫn dùng offset, phải chấp nhận chi phí `COUNT(*)` và scan sâu; đừng giả vờ nó miễn phí.

Lưu ý từ code hiện tại:

- `product-service` đã có cursor pagination cho catalog và đã có index listing.
- `order-service` vẫn còn `COUNT(*) + OFFSET/LIMIT` ở luồng admin; đây là vùng cần theo dõi khi dữ liệu lớn dần.

### 8.3. Transaction

Transaction phải nằm ở nơi giữ được business invariant.

Nếu một flow cần nhiều bước “cùng thành công hoặc cùng thất bại”, không trải nó ra nhiều repo call rời rạc.

Ưu tiên:

- một transaction rõ ràng
- helper kiểu `RunInTx(...)` nếu pattern lặp lại nhiều nơi
- row lock/optimistic locking cho inventory, coupon, balance, payment dedupe

### 8.4. Tối ưu bằng số liệu thay vì cảm giác

Trước khi kết luận chậm:

- bật metric/tracing
- dùng `EXPLAIN ANALYZE`
- benchmark hoặc profile đoạn nghi ngờ

Đừng thêm cache, Redis lock, hay Elasticsearch chỉ vì “có thể nhanh hơn”.

---

## 9. API design

### 9.1. HTTP API

- Dùng route, method, status code đúng semantics.
- Request/response phải ổn định và dễ đoán.
- Dùng envelope chuẩn từ `pkg/response` để giữ nhất quán.
- Validation ở boundary, business rule ở service.
- Mọi route public phải có mặt trong `api-gateway/internal/docs/openapi.yaml`. Spec là contract viết tay, không sinh tự động, nên sửa route mà quên sửa spec là làm docs nói dối — `docs_test.go` chặn việc đó.

### 9.2. gRPC và inter-service calls

- Chỉ thêm RPC mới khi có nhu cầu gọi nội bộ thực sự.
- Proto là contract; sửa proto phải nghĩ tới compatibility.
- Không biến gRPC thành đường vòng để né việc thiết kế boundary tốt.

### 9.3. Idempotency và retry-safety

Các API có khả năng bị client retry hoặc webhook gọi lặp phải có cơ chế idempotency rõ ràng, đặc biệt ở payment, order, inventory.

Nếu một endpoint POST có side effect quan trọng, hãy tự hỏi: “client retry 2 lần thì chuyện gì xảy ra?”

---

## 10. Dependency management và cấu hình

- Mỗi dependency runtime mới phải có lý do rõ ràng.
- Ưu tiên thư viện phổ biến, ổn định, ít magic.
- Không kéo framework lớn chỉ để giải quyết một nhu cầu nhỏ.

Với config:

- mọi giá trị production-critical phải cấu hình được qua env/file
- startup nên fail fast nếu thiếu secret hoặc endpoint bắt buộc
- default chỉ phục vụ local/dev, không được khiến production chạy “tạm được” trong trạng thái nguy hiểm

Khi thêm config mới:

1. thêm vào `pkg/config`
2. thêm default hợp lý cho local
3. cập nhật file config trong `deployments/docker/config/`
4. cập nhật `.env.example` nếu cần
5. nói rõ config đó là bắt buộc hay optional

---

## 11. Security

Mọi thay đổi backend phải tự kiểm tra tối thiểu các điểm sau:

- input đã validate chưa
- query đã parameterized chưa
- endpoint đã kiểm tra auth/authz đúng chưa
- log có lộ dữ liệu nhạy cảm không
- file upload có kiểm tra content type/kích thước chưa
- webhook có verify signature chưa
- redirect/callback URL có bị mở quá mức không
- rate limit có cần áp dụng không

Không merge “tạm hardcode secret”, “tạm bỏ verify”, hoặc “tạm mở public route” mà không có lý do rất mạnh và thời hạn gỡ bỏ rõ ràng.

---

## 12. Observability

Repo đã có:

- structured logging
- Prometheus metrics
- OpenTelemetry tracing
- Jaeger/Grafana trong local stack

Code mới phải tận dụng những thứ đã có trước khi đòi thêm công cụ mới.

Kỳ vọng tối thiểu cho feature quan trọng:

- log được path thành công/thất bại
- có trace qua boundary HTTP/gRPC nếu flow đi qua nhiều service
- có metric hoặc ít nhất không làm mù dashboard hiện tại

Nếu một background job, queue consumer, hoặc external integration mới được thêm vào, phải nghĩ ngay đến:

- success/failure count
- retry count
- processing latency
- dead-letter hoặc cách cô lập message hỏng

---

## 13. Testing

### 13.1. Mức test mong đợi

- service: unit test cho business rule, table-driven nếu phù hợp
- repository: integration test cho SQL, especially query/transaction quan trọng
- handler: test mapping request/response và error code
- integration xuyên boundary: chỉ thêm khi giá trị cao, không viết cho có

### 13.2. Những thứ đáng test nhất

- rule dễ sai và khó nhìn bằng mắt
- race condition hoặc duplicate side effect
- validation boundary
- transaction rollback path
- permission/authz path
- pagination/sort/filter
- webhook/event handling

### 13.3. Benchmark và profiling

Với hot path hoặc code xử lý dữ liệu lớn, cân nhắc thêm benchmark hoặc profiling plan. Repo hiện có metrics/tracing nhưng chưa coi benchmark/pprof là thói quen mặc định; đây là điểm nên nâng cấp.

---

## 14. Tiêu chuẩn khi thêm feature

Mỗi feature backend nên đi theo checklist này:

1. Xác định boundary: HTTP, gRPC, event, hay chỉ nội bộ service.
2. Xác định data model và migration nếu cần.
3. Viết repository trước cho phần persistence quan trọng.
4. Viết service để giữ rule nghiệp vụ rõ ràng.
5. Viết handler và map lỗi chuẩn.
6. Nếu qua gateway, cập nhật proxy/route đúng chỗ.
7. Thêm test tương ứng.
8. Kiểm tra log, metric, timeout, authz.
9. Cập nhật docs nếu flow hoặc path thay đổi.
10. Tự hỏi xem thay đổi này có tạo thêm nợ kỹ thuật hoặc failure mode mới không.

Feature hoàn chỉnh không chỉ là “API chạy được”, mà là:

- có contract rõ
- có đường rollback
- có test đủ tin cậy
- có khả năng quan sát khi lỗi
- không phá style chung của repo

---

## 15. Tiêu chuẩn khi refactor

Refactor tốt phải làm ít nhất một trong các điều sau một cách đo được hoặc nhìn thấy rõ:

- giảm duplication
- giảm coupling
- làm flow dễ test hơn
- giảm latency/query count/allocations
- làm error handling nhất quán hơn
- làm code đọc dễ hơn cho người đến sau

Không gọi là refactor nếu thực chất chỉ là:

- đổi tên lung tung không thêm rõ nghĩa
- tách file nhưng không giảm độ phức tạp
- thêm abstraction không có consumer thật
- thêm framework để thay cho code đơn giản đang chạy ổn

Với refactor lớn, nên làm theo lát cắt nhỏ, giữ behaviour cũ, có test khóa hành vi trước.

---

## 16. Review checklist bắt buộc trước khi merge

Trước khi kết luận PR “ổn”, hãy tự check:

- [ ] Code có bám đúng phân tầng `handler -> service -> repository` không?
- [ ] Tên hàm, biến, package có nói đúng intent không?
- [ ] Có chỗ nào lặp logic nên gom lại không?
- [ ] Error có được wrap/map đúng tầng không?
- [ ] Có log nào thiếu context hoặc lộ dữ liệu nhạy cảm không?
- [ ] Query mới có index/supporting migration nếu cần không?
- [ ] Có chỗ nào dùng `OFFSET/LIMIT`, `COUNT(*)`, load-all rồi tính trong Go mà sẽ thành bottleneck không?
- [ ] External call đã có timeout/retry/idempotency strategy phù hợp chưa?
- [ ] Goroutine/background worker có lifecycle rõ ràng chưa?
- [ ] Test có bao phủ path thành công, path lỗi, và rule nghiệp vụ chính chưa?
- [ ] Docs có còn khớp với code và đường dẫn thực tế không?

---

## 17. Những định hướng nên ưu tiên ngay trong repo này

Từ code hiện tại, các hướng cải thiện có giá trị thực tế cao là:

- tiếp tục chuẩn hoá transaction helper cho các write flow nhiều bước (đã bắt đầu ở các luồng như product review)
- giảm phụ thuộc vào `COUNT(*) + OFFSET` ở các list endpoint lớn
- bổ sung idempotency cho payment/webhook path
- mở rộng áp dụng outbox/inbox pattern cho tất cả các event publish quan trọng (đã có bước đầu ở order/notification service)
- mở rộng thêm benchmark/pprof cho các hot path thay vì tối ưu cảm tính (đã bắt đầu có ở phần review service)
- giữ tài liệu khớp với path thật của source code

Mọi tài liệu hoặc roadmap mới phải ưu tiên những việc này trước các chủ đề “oách” nhưng xa thực tế hơn như saga choreography hoặc tách thêm service.

---

## 18. Kỷ Luật Cập Nhật Tài Liệu

Repo này có nhiều file tài liệu ở root và trong `docs/`. Nếu flow, route, runtime hoặc contract đổi mà docs không đổi theo, nợ kỹ thuật sẽ tăng rất nhanh.

Khi thay đổi code liên quan tới runtime thật, contributor và AI agent phải tự hỏi:

1. Route public có đổi không? Nếu có, **bắt buộc** sửa `api-gateway/internal/docs/openapi.yaml` trong cùng thay đổi — `docs_test.go` so khớp hai chiều spec với `e.Routes()` nên quên là test đỏ ngay.
2. Docker Compose/runtime local có đổi không?
3. Flow end-to-end hoặc async semantics có đổi không?
4. Trạng thái triển khai, test hoặc backlog có đổi không?

Nếu câu trả lời là có, phải cập nhật tài liệu tương ứng ngay trong cùng thay đổi hoặc cùng đợt làm việc.

### 18.1. Source of truth khi viết docs

Khi viết hoặc sửa docs, ưu tiên kiểm tra các file sau trước:

- `deployments/docker/docker-compose.yml`
- `deployments/docker/config/*.yaml`
- `api-gateway/cmd/main.go`
- `api-gateway/internal/handler/*.go`
- `api-gateway/internal/docs/openapi.yaml`
- `api-gateway/internal/proxy/*.go`
- `services/*-service/cmd/main.go`
- `services/*-service/internal/handler/`
- `services/*-service/internal/service/`
- `services/*-service/internal/repository/`
- `pkg/config/config.go`
- `pkg/middleware/*`
- `pkg/observability/*`

Không copy-paste hoặc lặp lại route/path cũ chỉ vì tài liệu khác đã ghi như vậy.

### 18.2. Cách viết docs đúng trong repo này

Tài liệu tốt trong repo này nên:

- chỉ rõ file path thật
- chỉ rõ service, handler, service layer, repository nào giữ invariant
- nói rõ source of truth nằm ở Postgres, Redis, RabbitMQ hay client state
- nói rõ chỗ nào đã production-oriented và chỗ nào mới dừng ở mức “đủ chạy local”
- nói rõ failure mode và trade-off, không chỉ mô tả happy path

Tài liệu không nên:

- mô tả repo như monolith
- nói “có thể”, “có lẽ”, “thường là” khi source code đã thể hiện rõ
- gọi `client/` hay `frontend/` là entrypoint chính nếu compose/runtime thật đang khác
- biến những route/helper test cũ thành contract chính thức

---

## 19. Những Pattern Backend Phải Giữ Khi Sửa Code

Một số pattern hiện tại là xương sống reliability của hệ thống. Khi refactor hoặc mở rộng, phải giữ hoặc nâng cấp chúng một cách có chủ đích, không được vô tình làm yếu đi.

### 19.1. Transaction bundle

Ví dụ:

- `createOrderTx`
- `CreateWithIdempotency` ở payment
- `ProfileTxManager.RunInTx`
- `ProductReviewTxManager.RunInTx`

Ý nghĩa:

- nhiều write phải cùng commit hoặc cùng rollback
- event/outbox/idempotency record không được tách rời entity chính

### 19.2. SQL compare-and-set

Ví dụ:

- `UpdateStock`
- `ReserveStockForOrder` (CAS từng item + ledger idempotent trong một transaction)
- `ExpirePendingReservation`
- `ApplyWebhookResult`

Ý nghĩa:

- condition phải nằm trong `WHERE`
- quyết định mutate hay no-op bằng `RowsAffected`, không dựa vào snapshot cũ trong memory

### 19.3. Row lock

Ví dụ:

- `lockAndConsumeCoupon`
- `GetReviewByProductAndUserForUpdate`
- `SELECT status ... FOR UPDATE` trong `ApplyInboxStatusTransition`

Ý nghĩa:

- serialize critical section ngay ở DB row
- tránh lost update và race condition khi nhiều replica cùng chạy

### 19.4. Cursor pagination

Ví dụ:

- `product-service` catalog list
- `order-service` list by cursor

Ý nghĩa:

- hot path phải ưu tiên cursor khi dữ liệu tăng nhanh
- ordering phải có tie-breaker ổn định như `created_at, id`

### 19.5. Lease claim + retry-safe async

Ví dụ:

- `ClaimPendingOutbox`
- `ClaimPendingReturnRefunds`
- `notification-service/internal/inbox/redis_store.go`

Ý nghĩa:

- worker có thể scale ngang
- process crash giữa chừng không làm mất việc
- downstream phải vẫn chịu được duplicate delivery

### 19.6. Outbox / inbox / idempotency

Ví dụ:

- outbox ở order/payment
- inbox transition ở order/payment
- payment/order idempotency key

Ý nghĩa:

- publish retry-safe
- webhook replay-safe
- POST quan trọng chịu được client retry

Nếu một thay đổi làm suy yếu một trong các pattern này, phải nêu rõ trong PR hoặc proposal:

- pattern cũ là gì
- vì sao nó không còn phù hợp
- pattern mới thay thế bằng gì
- test nào chứng minh behavior vẫn an toàn

---

## 20. Trách Nhiệm Của Từng File Tài Liệu Ở Root

Để tránh trùng lặp lộn xộn, mỗi file tài liệu ở root nên giữ một vai trò rõ ràng:

- `README.md`
  - entrypoint tổng quan cho người mới
  - runtime local thật, thành phần chính, đường đọc source
- `DOCKER_GUIDE.md`
  - compose/runtime/debug/playbook vận hành local
  - URL, container, network, config, symptom-based debugging
- `API_TESTING_GUIDE.md`
  - route public testable qua gateway
  - smoke flow, negative flow, idempotency flow, webhook/replay verification
- `LOGIC_FLOW.md`
  - flow end-to-end từ UI/API boundary tới service/repository/async worker
  - source of truth, invariant, file map theo flow
- `PROJECTS.md`
  - trạng thái triển khai theo feature/layer
  - test/coverage/verify/deploy checklist
- `docs/annotated/README.md`
  - source map chi tiết nhất theo service, file, function, hot path
- `docs/deep-dive/README.md`
  - phân tích hành vi runtime, code quality, failure mode, hardening direction
- `docs/learning/README.md`
  - roadmap học source và checklist audit khi tự đọc repo

Nếu sửa một file mà nội dung thực ra thuộc trách nhiệm của file khác, hãy:

1. rút gọn phần overview ở file hiện tại
2. link sang file đúng vai trò
3. giữ thông tin không bị nhân bản mâu thuẫn

---

## Kết luận

Tiêu chuẩn của repo này không phải “code chạy được”, mà là:

- code đủ rõ để người khác duy trì
- đủ an toàn để deploy
- đủ quan sát để debug
- đủ thực dụng để học đúng nghề backend Go

Nếu phải chọn giữa code ngắn hơn và code rõ hơn, ưu tiên code rõ hơn.
Nếu phải chọn giữa giải pháp hiện đại hơn và giải pháp vận hành đơn giản hơn, ưu tiên giải pháp đơn giản hơn.
Nếu phải chọn giữa thêm thành phần mới và tận dụng tốt Go + PostgreSQL + những gì repo đang có, ưu tiên tận dụng cái đang có.
