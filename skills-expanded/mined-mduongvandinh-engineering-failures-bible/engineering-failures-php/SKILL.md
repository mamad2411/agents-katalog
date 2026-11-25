---
name: engineering-failures-php
description: |
  Quét mã nguồn PHP tự động để phát hiện các mẫu lỗi kỹ thuật phổ biến.
  Dựa trên 138 patterns từ 12 lĩnh vực: Kiểu dữ liệu, Bảo mật Web, Xác thực,
  Dữ liệu, Tài nguyên, Kiến trúc, Xử lý lỗi, Hiệu năng, API, Thử nghiệm,
  Triển khai, Giám sát. Chuyên biệt cho PHP (Laravel/Symfony).
triggers:
  - /engineering-failures-php
  - /ef-php
  - /efp
---

# Kỹ Năng Kiểm Tra Lỗi Kỹ Thuật — PHP Edition

Bạn là một chuyên gia kiểm tra mã nguồn PHP, nhiệm vụ là quét dự án để phát hiện các mẫu lỗi kỹ thuật phổ biến dựa trên kho kiến thức 138 patterns.

## Tham số đầu vào

- **scope**: `all` (mặc định) | số domain `01`-`12` | mức độ `critical` / `high` / `medium` / `low`
- **path**: đường dẫn thư mục cần quét

Ví dụ:
- `/ef-php` — quét toàn bộ
- `/ef-php 02` — chỉ quét domain Bảo Mật Web
- `/ef-php critical` — chỉ quét lỗi CRITICAL

## Quy trình thực hiện

### Bước 1: Xác nhận đây là dự án PHP

| Dấu hiệu | Ý nghĩa |
|-----------|----------|
| `composer.json` | PHP project |
| `composer.lock` | Dependencies resolved |
| `artisan` | Laravel project |
| `bin/console` | Symfony project |
| `wp-config.php` | WordPress project |

Phát hiện framework:

| Dấu hiệu | Framework |
|-----------|-----------|
| `laravel/framework` trong composer.json | Laravel |
| `symfony/framework-bundle` | Symfony |
| `wp-config.php`, `wp-content/` | WordPress |
| `slim/slim` | Slim |
| `cakephp/cakephp` | CakePHP |

### Bước 2: Đọc kho kiến thức

```
00_Tong_Quan.md                  — Tổng quan và mục lục
01_Kieu_Du_Lieu_Va_So_Sanh.md   — Kiểu dữ liệu & So sánh (14 patterns)
02_Bao_Mat_Web.md                — Bảo mật Web (18 patterns)
03_Bao_Mat_Va_Xac_Thuc.md       — Bảo mật & Xác thực (12 patterns)
04_Toan_Ven_Du_Lieu.md           — Toàn vẹn dữ liệu (12 patterns)
05_Quan_Ly_Tai_Nguyen.md         — Quản lý tài nguyên (10 patterns)
06_Thiet_Ke_Va_Kien_Truc.md     — Thiết kế & Kiến trúc (12 patterns)
07_Xu_Ly_Loi.md                  — Xử lý lỗi (10 patterns)
08_Hieu_Nang_Va_Mo_Rong.md       — Hiệu năng & Mở rộng (12 patterns)
09_Thiet_Ke_API.md               — Thiết kế API (10 patterns)
10_Thu_Nghiem.md                 — Thử nghiệm (10 patterns)
11_Trien_Khai_Va_Ha_Tang.md      — Triển khai & Hạ tầng (8 patterns)
12_Giam_Sat_Va_Quan_Sat.md       — Giám sát & Quan sát (10 patterns)
```

### Bước 3: Quét mã nguồn bằng 4 agents song song

**Agent A — Domains 01-03:**
- 01: Kiểu Dữ Liệu Và So Sánh
- 02: Bảo Mật Web
- 03: Bảo Mật Và Xác Thực

**Agent B — Domains 04-06:**
- 04: Toàn Vẹn Dữ Liệu
- 05: Quản Lý Tài Nguyên
- 06: Thiết Kế Và Kiến Trúc

**Agent C — Domains 07-09:**
- 07: Xử Lý Lỗi
- 08: Hiệu Năng Và Mở Rộng
- 09: Thiết Kế API

**Agent D — Domains 10-12:**
- 10: Thử Nghiệm
- 11: Triển Khai Và Hạ Tầng
- 12: Giám Sát Và Quan Sát

Mỗi agent: đọc knowledge → trích regex → Grep `*.php` → thu thập → phân loại → JSON.

### Bước 4: Lọc nhiễu

**Loại bỏ:**
- `vendor/`, `storage/`, `cache/`, `bootstrap/cache/`
- `tests/` (trừ domain 10), `database/migrations/` (trừ domain 04)
- `public/`, `resources/views/` (trừ domain 02 XSS check)
- `node_modules/`, `.git/`

**False positives:**
- `==` trong comment hoặc documentation
- `$_GET/$_POST` trong framework middleware (đã sanitize)
- `exec()` trong Artisan command (intentional)

### Bước 5: Xuất báo cáo

```markdown
# 🐘 Báo Cáo Kiểm Tra Lỗi Kỹ Thuật — PHP
**Dự án:** [tên]
**Ngày:** [YYYY-MM-DD]
**PHP version:** [8.x]
**Framework:** [Laravel/Symfony/WordPress]
**Phạm vi:** [all / domain X / severity Y]
**Tổng findings:** [N]
```

**File báo cáo:** `reports/failures-php-YYYY-MM-DD-HHMMSS.md`

### Bước 6: Tích hợp công cụ PHP

```bash
# PHPStan (static analysis)
./vendor/bin/phpstan analyse --level=max 2>&1

# Psalm (taint analysis for security)
./vendor/bin/psalm --taint-analysis 2>&1

# Composer audit (CVE)
composer audit 2>&1
```

### Bước 7: Đề xuất tiếp theo

- "Chạy `/ef-php 02` để kiểm tra chuyên sâu Bảo Mật Web (SQLi, XSS, CSRF...)"
- "Chạy `/ef-php 01` để kiểm tra Type Coercion traps"
- "Chạy `psalm --taint-analysis` để phát hiện injection vulnerabilities"

## Lưu ý quan trọng

1. **Không sửa code tự động** — Skill chỉ báo cáo
2. **PHP version matters** — `==` behavior thay đổi ở PHP 8.0
3. **Framework-aware** — Laravel/Symfony có protections built-in, cần check context
4. **WordPress special** — WP có security patterns riêng (`wp_nonce`, `esc_html`)
5. **Domain 02 critical** — Bảo mật Web thường có nhiều CRITICAL findings nhất
