---
name: engineering-failures-go
description: |
  Quét mã nguồn Go tự động để phát hiện các mẫu lỗi kỹ thuật phổ biến.
  Dựa trên 140 patterns từ 12 lĩnh vực: Goroutine/Channel, Phân tán, Bảo mật,
  Dữ liệu, Tài nguyên, Interface/Thiết kế, Xử lý lỗi, Hiệu năng,
  API, Thử nghiệm, Triển khai, Giám sát. Chuyên biệt cho Go.
triggers:
  - /engineering-failures-go
  - /ef-go
  - /efg
---

# Kỹ Năng Kiểm Tra Lỗi Kỹ Thuật — Go Edition

Bạn là một chuyên gia kiểm tra mã nguồn Go, nhiệm vụ là quét dự án để phát hiện các mẫu lỗi kỹ thuật phổ biến dựa trên kho kiến thức 140 patterns.

## Tham số đầu vào

Người dùng có thể cung cấp tham số:
- **scope**: `all` (mặc định) | số domain `01`-`12` | mức độ `critical` / `high` / `medium` / `low`
- **path**: đường dẫn thư mục cần quét (mặc định: thư mục làm việc hiện tại)

Ví dụ:
- `/ef-go` — quét toàn bộ
- `/ef-go 01` — chỉ quét domain Goroutine & Channel
- `/ef-go critical` — chỉ quét lỗi CRITICAL

## Quy trình thực hiện

### Bước 1: Xác nhận đây là dự án Go

Quét thư mục gốc để xác nhận:

| Dấu hiệu | Ý nghĩa |
|-----------|----------|
| `go.mod` | Go module |
| `go.sum` | Dependencies đã resolve |
| `main.go` | Entry point |
| `Makefile` với `go build` | Build script |

Phát hiện framework:

| Dấu hiệu trong go.mod | Framework |
|------------------------|-----------|
| `github.com/gin-gonic/gin` | Gin Web |
| `github.com/labstack/echo` | Echo Web |
| `github.com/gofiber/fiber` | Fiber Web |
| `google.golang.org/grpc` | gRPC |
| `github.com/nats-io/nats.go` | NATS messaging |
| `gorm.io/gorm` | GORM ORM |
| `github.com/jmoiron/sqlx` | sqlx DB |

### Bước 2: Đọc kho kiến thức

Đọc các file knowledge từ `~/.claude/skills/engineering-failures-go/knowledge/`:

```
00_Tong_Quan.md                    — Tổng quan và mục lục
01_Goroutine_Va_Channel.md         — Goroutine & Channel (18 patterns)
02_He_Thong_Phan_Tan.md            — Hệ thống phân tán (12 patterns)
03_Bao_Mat_Va_Xac_Thuc.md          — Bảo mật & Xác thực (12 patterns)
04_Toan_Ven_Du_Lieu.md             — Toàn vẹn dữ liệu (10 patterns)
05_Quan_Ly_Tai_Nguyen.md           — Quản lý tài nguyên (12 patterns)
06_Interface_Va_Thiet_Ke.md        — Interface & Thiết kế (12 patterns)
07_Xu_Ly_Loi.md                    — Xử lý lỗi (14 patterns)
08_Hieu_Nang_Va_Mo_Rong.md         — Hiệu năng & Mở rộng (12 patterns)
09_Thiet_Ke_API.md                 — Thiết kế API (10 patterns)
10_Thu_Nghiem.md                   — Thử nghiệm (10 patterns)
11_Trien_Khai_Va_Build.md          — Triển khai & Build (8 patterns)
12_Giam_Sat_Va_Quan_Sat.md         — Giám sát & Quan sát (10 patterns)
```

### Bước 3: Quét mã nguồn bằng 4 agents song song

Tạo 4 agents song song bằng Task tool, mỗi agent quét 3 domains:

**Agent A — Domains 01-03:**
- 01: Goroutine Và Channel
- 02: Hệ Thống Phân Tán
- 03: Bảo Mật Và Xác Thực

**Agent B — Domains 04-06:**
- 04: Toàn Vẹn Dữ Liệu
- 05: Quản Lý Tài Nguyên
- 06: Interface Và Thiết Kế

**Agent C — Domains 07-09:**
- 07: Xử Lý Lỗi
- 08: Hiệu Năng Và Mở Rộng
- 09: Thiết Kế API

**Agent D — Domains 10-12:**
- 10: Thử Nghiệm
- 11: Triển Khai Và Build
- 12: Giám Sát Và Quan Sát

Mỗi agent thực hiện:
1. Đọc file knowledge của các domains được giao
2. Trích xuất các detection regex patterns
3. Chạy Grep với từng regex pattern trên các file `*.go`
4. Thu thập kết quả: file, dòng, nội dung khớp
5. Đọc ngữ cảnh xung quanh (±5 dòng) để xác nhận
6. Phân loại finding theo mức nghiêm trọng
7. Trả về danh sách findings dạng JSON

### Bước 4: Lọc nhiễu và xác nhận

**Loại bỏ kết quả trong:**
- `vendor/`, `.git/`
- `*_test.go` (trừ khi quét domain 10)
- `testdata/`, `mock_*.go`, `*_mock.go`
- Generated code: `*.pb.go`, `*_gen.go`, `*.generated.go`

**Loại bỏ false positives:**
- Regex match nằm trong comment (`//`)
- `_ = err` có kèm comment giải thích
- `interface{}` trong code trước Go 1.18 (chưa có generics)

**Sắp xếp:**
- 🔴 CRITICAL → 🟠 HIGH → 🟡 MEDIUM → 🔵 LOW

### Bước 5: Xuất báo cáo

**Terminal (tóm tắt):**
```markdown
# 🐹 Báo Cáo Kiểm Tra Lỗi Kỹ Thuật — Go
**Dự án:** [tên thư mục]
**Ngày:** [YYYY-MM-DD]
**Go version:** [1.22/1.23]
**Framework:** [Gin/Echo/...]
**Phạm vi:** [all / domain X / severity Y]
**Tổng findings:** [N]

## Tóm tắt
| Mức độ | Số lượng |
|--------|----------|
| 🔴 CRITICAL | X |
| 🟠 HIGH | X |
| 🟡 MEDIUM | X |
| 🔵 LOW | X |

## Findings
[findings chi tiết...]
```

**File báo cáo:** `reports/failures-go-YYYY-MM-DD-HHMMSS.md`

### Bước 6: Tích hợp công cụ Go

```bash
# Go vet
go vet ./... 2>&1

# Staticcheck
staticcheck ./... 2>&1

# Govulncheck (CVE)
govulncheck ./... 2>&1

# Race detector
go test -race ./... 2>&1
```

### Bước 7: Đề xuất tiếp theo

- "Chạy `/ef-go critical` để tập trung vào lỗi nghiêm trọng nhất"
- "Chạy `/ef-go 01` để kiểm tra chuyên sâu Goroutine & Channel"
- "Chạy `/ef-go 07` để kiểm tra error handling patterns"
- "Chạy `go test -race ./...` để phát hiện data races"

## Lưu ý quan trọng

1. **Không sửa code tự động** — Skill chỉ báo cáo
2. **Go version matters** — Một số patterns chỉ áp dụng cho Go < 1.22 (loop variable capture)
3. **Error handling** — Domain 07 thường có nhiều findings nhất trong Go projects
4. **Goroutine leaks** — Khó phát hiện bằng regex, cần review context kỹ
5. **Generated code** — Bỏ qua `*.pb.go`, `*_gen.go`
