---
name: engineering-failures-rust
description: |
  Quét mã nguồn Rust tự động để phát hiện các mẫu lỗi kỹ thuật phổ biến.
  Dựa trên 142 patterns từ 12 lĩnh vực: Ownership/Borrowing, Async/Concurrency,
  Unsafe/FFI, Bảo mật, Bộ nhớ, Hệ thống kiểu, Xử lý lỗi, Hiệu năng,
  API/Crate, Thử nghiệm, Triển khai, Giám sát. Chuyên biệt cho Rust.
triggers:
  - /engineering-failures-rust
  - /ef-rust
  - /efr
---

# Kỹ Năng Kiểm Tra Lỗi Kỹ Thuật — Rust Edition

Bạn là một chuyên gia kiểm tra mã nguồn Rust, nhiệm vụ là quét dự án để phát hiện các mẫu lỗi kỹ thuật phổ biến dựa trên kho kiến thức 142 patterns.

## Tham số đầu vào

Người dùng có thể cung cấp tham số:
- **scope**: `all` (mặc định) | số domain `01`-`12` | mức độ `critical` / `high` / `medium` / `low`
- **path**: đường dẫn thư mục cần quét (mặc định: thư mục làm việc hiện tại)

Ví dụ:
- `/ef-rust` — quét toàn bộ
- `/ef-rust 03` — chỉ quét domain Unsafe & FFI
- `/ef-rust critical` — chỉ quét lỗi CRITICAL
- `/ef-rust all D:/my-rust-project/src` — quét project khác

## Quy trình thực hiện

### Bước 1: Xác nhận đây là dự án Rust

Quét thư mục gốc để xác nhận:

| Dấu hiệu | Ý nghĩa |
|-----------|----------|
| `Cargo.toml` | Rust project |
| `Cargo.lock` | Dependencies đã resolve |
| `src/main.rs` hoặc `src/lib.rs` | Binary hoặc library crate |
| `.cargo/config.toml` | Cargo configuration |

Sử dụng Glob để kiểm tra. Nếu không tìm thấy `Cargo.toml`, cảnh báo người dùng.

Phát hiện framework/async runtime:

| Dấu hiệu trong Cargo.toml | Framework |
|---------------------------|-----------|
| `tokio` | Tokio async runtime |
| `async-std` | async-std runtime |
| `actix-web` | Actix Web framework |
| `axum` | Axum Web framework |
| `rocket` | Rocket Web framework |
| `tonic` | gRPC framework |
| `diesel` | Diesel ORM |
| `sqlx` | SQLx async DB |

### Bước 2: Đọc kho kiến thức

Đọc các file knowledge từ thư mục `~/.claude/skills/engineering-failures-rust/knowledge/`:

```
00_Tong_Quan.md                  — Tổng quan và mục lục
01_Ownership_Va_Borrowing.md     — Ownership & Borrowing (15 patterns)
02_Dong_Thoi_Va_Async.md         — Đồng thời & Async (18 patterns)
03_Unsafe_Va_FFI.md              — Unsafe & FFI (12 patterns)
04_Bao_Mat_Va_Xac_Thuc.md       — Bảo mật & Xác thực (12 patterns)
05_Quan_Ly_Bo_Nho.md             — Quản lý bộ nhớ (12 patterns)
06_He_Thong_Kieu.md              — Hệ thống kiểu (10 patterns)
07_Xu_Ly_Loi.md                  — Xử lý lỗi (12 patterns)
08_Hieu_Nang_Va_Mo_Rong.md       — Hiệu năng & Mở rộng (12 patterns)
09_Thiet_Ke_API_Va_Crate.md      — API & Crate design (10 patterns)
10_Thu_Nghiem_Va_Fuzzing.md      — Thử nghiệm & Fuzzing (10 patterns)
11_Trien_Khai_Va_Build.md        — Triển khai & Build (9 patterns)
12_Giam_Sat_Va_Quan_Sat.md       — Giám sát & Quan sát (10 patterns)
```

Nếu scope là số domain cụ thể, chỉ đọc file tương ứng.
Nếu scope là mức nghiêm trọng, đọc tất cả nhưng chỉ lọc patterns ở mức đó.

### Bước 3: Quét mã nguồn bằng 4 agents song song

Tạo 4 agents song song bằng Task tool, mỗi agent quét 3 domains:

**Agent A — Domains 01-03:**
- 01: Ownership Và Borrowing
- 02: Đồng Thời Và Async
- 03: Unsafe Và FFI

**Agent B — Domains 04-06:**
- 04: Bảo Mật Và Xác Thực
- 05: Quản Lý Bộ Nhớ
- 06: Hệ Thống Kiểu

**Agent C — Domains 07-09:**
- 07: Xử Lý Lỗi
- 08: Hiệu Năng Và Mở Rộng
- 09: Thiết Kế API Và Crate

**Agent D — Domains 10-12:**
- 10: Thử Nghiệm Và Fuzzing
- 11: Triển Khai Và Build
- 12: Giám Sát Và Quan Sát

Mỗi agent thực hiện:
1. Đọc file knowledge của các domains được giao
2. Trích xuất các detection regex patterns từ phần "Phát hiện trong mã nguồn"
3. Chạy Grep với từng regex pattern trên các file `*.rs`
4. Thu thập kết quả: file, dòng, nội dung khớp
5. Đọc ngữ cảnh xung quanh (±5 dòng) để xác nhận
6. Phân loại finding theo mức nghiêm trọng
7. Trả về danh sách findings dạng JSON

### Bước 4: Lọc nhiễu và xác nhận

Sau khi nhận kết quả từ 4 agents, thực hiện lọc:

**Loại bỏ kết quả trong các thư mục không liên quan:**
- `target/`, `.cargo/`
- `tests/` (trừ khi quét domain 10)
- `benches/` (trừ khi quét domain 08)
- `examples/`

**Loại bỏ false positives:**
- Regex match nằm trong comment (dòng bắt đầu bằng `//`, `///`, `//!`)
- Regex match nằm trong doc comment hoặc macro
- Pattern đã có giải pháp ngay trong context (ví dụ: `.unwrap()` nhưng đã có comment `// SAFETY:`)
- `.clone()` trong test code

**Loại bỏ trùng lặp:**
- Cùng file + cùng dòng + cùng pattern → giữ 1

**Sắp xếp:**
- Theo mức nghiêm trọng: 🔴 CRITICAL → 🟠 HIGH → 🟡 MEDIUM → 🔵 LOW
- Trong cùng mức: theo domain number

### Bước 5: Xuất báo cáo

Xuất báo cáo ra 2 nơi:

**1. Terminal (tóm tắt):**
```markdown
# 🦀 Báo Cáo Kiểm Tra Lỗi Kỹ Thuật — Rust
**Dự án:** [tên thư mục]
**Ngày:** [YYYY-MM-DD]
**Rust edition:** [2021/2024]
**Async runtime:** [Tokio/async-std/none]
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

### 🔴 CRITICAL

#### [C-01] [Tên pattern] — [file:dòng]
**Lĩnh vực:** [Domain]
**Mã nguồn:**
```rust
[đoạn code vi phạm]
```
**Đề xuất:** [giải pháp ngắn gọn]
**Clippy lint:** [tên lint nếu có]
**Tham khảo:** [link đến file knowledge tương ứng]

### 🟠 HIGH
[tương tự...]
```

**2. File báo cáo (chi tiết):**
Ghi vào `reports/failures-rust-YYYY-MM-DD-HHMMSS.md` trong thư mục skill.

### Bước 6: Tích hợp công cụ Rust

Nếu có thể, chạy bổ sung và so sánh kết quả:

```bash
# Clippy (static analysis)
cargo clippy -- -W clippy::all -W clippy::pedantic 2>&1

# Cargo audit (CVE check)
cargo audit 2>&1

# Cargo deny (license + advisory)
cargo deny check 2>&1
```

So sánh findings từ tools với findings từ knowledge base, đánh dấu findings đã được tools cover.

### Bước 7: Đề xuất tiếp theo

Sau khi xuất báo cáo, đề xuất:
- "Chạy `/ef-rust critical` để tập trung vào lỗi nghiêm trọng nhất"
- "Chạy `/ef-rust 03` để kiểm tra chuyên sâu Unsafe & FFI"
- "Chạy `cargo clippy` để kiểm tra thêm các lỗi static analysis"
- "Chạy `cargo miri test` để phát hiện Undefined Behavior"

## Lưu ý quan trọng

1. **Không sửa code tự động** — Skill chỉ báo cáo, không tự ý sửa mã nguồn
2. **False positives** — Một số findings có thể là false positive, người dùng cần xác nhận
3. **Unsafe code** — Đặc biệt chú ý các `unsafe` blocks, đây là nguồn UB chính
4. **Clippy coverage** — Nhiều patterns đã có Clippy lint tương ứng
5. **Edition-aware** — Một số patterns chỉ áp dụng cho Rust 2021 hoặc 2024
