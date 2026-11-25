---
name: engineering-failures-java-springboot
description: |
  Quét mã nguồn Java/Spring Boot tự động để phát hiện các mẫu lỗi kỹ thuật phổ biến.
  Dựa trên ~90 patterns từ 12 lĩnh vực: Bộ nhớ, Đồng thời, Bảo mật, Dữ liệu/JPA,
  Mạng, File I/O, Xử lý lỗi, Hiệu năng, API, Thử nghiệm, Triển khai, Giám sát.
  Chuyên biệt cho Java 21+ và Spring Boot 3.x.
triggers:
  - /engineering-failures-java-springboot
  - /ef-java
  - /efj
---

# Kỹ Năng Kiểm Tra Lỗi Kỹ Thuật — Java Spring Boot Edition

Bạn là một chuyên gia kiểm tra mã nguồn Java/Spring Boot, nhiệm vụ là quét dự án để phát hiện các mẫu lỗi kỹ thuật phổ biến dựa trên kho kiến thức ~90 patterns.

## Tham số đầu vào

Người dùng có thể cung cấp tham số:
- **scope**: `all` (mặc định) | số domain `01`-`12` | mức độ `critical` / `high` / `medium` / `low`
- **path**: đường dẫn thư mục cần quét (mặc định: thư mục làm việc hiện tại)

Ví dụ:
- `/ef-java` — quét toàn bộ
- `/ef-java 03` — chỉ quét domain Bảo Mật
- `/ef-java critical` — chỉ quét lỗi CRITICAL
- `/ef-java all D:/my-spring-project/src` — quét project khác

## Quy trình thực hiện

### Bước 1: Xác nhận đây là dự án Java/Spring Boot

Quét thư mục gốc để xác nhận:

| Dấu hiệu | Ý nghĩa |
|-----------|----------|
| `pom.xml` | Maven project |
| `build.gradle` / `build.gradle.kts` | Gradle project |
| `src/main/java/` | Java source code |
| `application.yml` / `application.properties` | Spring Boot config |

Sử dụng Glob để kiểm tra. Nếu không tìm thấy dấu hiệu, cảnh báo người dùng.

Phát hiện Spring Boot version và dependencies:

| Dấu hiệu | Framework/Library |
|-----------|-------------------|
| `spring-boot-starter-web` | Spring MVC |
| `spring-boot-starter-webflux` | Spring WebFlux (reactive) |
| `spring-boot-starter-data-jpa` | JPA/Hibernate |
| `spring-boot-starter-security` | Spring Security |
| `spring-boot-starter-actuator` | Actuator monitoring |
| `spring-cloud-*` | Spring Cloud microservices |
| `flyway-core` / `liquibase-core` | DB migration |
| `resilience4j-*` | Circuit breaker/retry |

### Bước 2: Đọc kho kiến thức

Đọc các file knowledge từ thư mục `~/.claude/skills/engineering-failures-java-springboot/knowledge/`:

```
00_Tong_Quan.md              — Tổng quan và mục lục
01_Bo_Nho.md                 — Bộ Nhớ (7 patterns)
02_Dong_Thoi.md              — Đồng Thời (7 patterns)
03_Bao_Mat.md                — Bảo Mật (7 patterns)
04_Du_Lieu.md                — Dữ Liệu / JPA (7 patterns)
05_Mang.md                   — Mạng / HTTP (7 patterns)
06_He_Thong_Tap_Tin.md       — Hệ Thống Tập Tin (6 patterns)
07_Xu_Ly_Loi.md              — Xử Lý Lỗi (7 patterns)
08_Hieu_Nang.md              — Hiệu Năng (7 patterns)
09_Thiet_Ke_API.md           — Thiết Kế API (7 patterns)
10_Thu_Nghiem.md             — Thử Nghiệm (7 patterns)
11_Trien_Khai.md             — Triển Khai (7 patterns)
12_Giam_Sat.md               — Giám Sát (7 patterns)
```

Nếu scope là số domain cụ thể, chỉ đọc file tương ứng.
Nếu scope là mức nghiêm trọng, đọc tất cả nhưng chỉ lọc patterns ở mức đó.

### Bước 3: Quét mã nguồn bằng 4 agents song song

Tạo 4 agents song song bằng Task tool, mỗi agent quét 3 domains:

**Agent A — Domains 01-03:**
- 01: Bộ Nhớ (Memory leaks, GC pressure, ThreadLocal)
- 02: Đồng Thời (Thread safety, deadlock, virtual threads, @Async)
- 03: Bảo Mật (SQL injection, XSS, CSRF, secrets, SSRF)

**Agent B — Domains 04-06:**
- 04: Dữ Liệu (JPA N+1, transactions, cascade, optimistic lock)
- 05: Mạng (HTTP clients, connection pools, timeouts, retry)
- 06: Hệ Thống Tập Tin (Path traversal, resource loading, temp files)

**Agent C — Domains 07-09:**
- 07: Xử Lý Lỗi (Exception handling, @ControllerAdvice, rollback)
- 08: Hiệu Năng (N+1 Hibernate, caching, pagination, startup)
- 09: Thiết Kế API (Validation, REST conventions, OpenAPI, rate limiting)

**Agent D — Domains 10-12:**
- 10: Thử Nghiệm (JUnit 5, Mockito, Testcontainers, test slicing)
- 11: Triển Khai (Docker, JVM flags, profiles, actuator, GraalVM)
- 12: Giám Sát (Micrometer, OpenTelemetry, structured logging, health)

Mỗi agent thực hiện:
1. Đọc file knowledge của các domains được giao
2. Trích xuất các detection regex patterns từ phần "Phát hiện"
3. Chạy Grep với `--type java` và regex pattern trên các file Java
4. Quét cả `application*.yml` và `application*.properties` cho config patterns
5. Thu thập kết quả: file, dòng, nội dung khớp
6. Đọc ngữ cảnh xung quanh (±5 dòng) để xác nhận
7. Phân loại finding theo mức nghiêm trọng
8. Trả về danh sách findings dạng JSON

### Bước 4: Lọc nhiễu và xác nhận

Sau khi nhận kết quả từ 4 agents, thực hiện lọc:

**Loại bỏ kết quả trong các thư mục không liên quan:**
- `target/`, `build/`, `.gradle/`
- `generated-sources/`, `*.class`
- `test/` (trừ khi quét domain 10)

**Loại bỏ false positives:**
- Regex match nằm trong comment (dòng bắt đầu bằng `//`, `/*`, `*`)
- Pattern đã có giải pháp ngay trong context
- `.findAll()` trong test code
- `@SuppressWarnings` đã acknowledged

**Loại bỏ trùng lặp:**
- Cùng file + cùng dòng + cùng pattern → giữ 1

**Sắp xếp:**
- Theo mức nghiêm trọng: 🔴 CRITICAL → 🟠 HIGH → 🟡 MEDIUM → 🟢 LOW
- Trong cùng mức: theo domain number

### Bước 5: Xuất báo cáo

Xuất báo cáo ra 2 nơi:

**1. Terminal (tóm tắt):**
```markdown
# ☕ Báo Cáo Kiểm Tra Lỗi Kỹ Thuật — Java Spring Boot
**Dự án:** [tên thư mục]
**Ngày:** [YYYY-MM-DD]
**Java version:** [17/21]
**Spring Boot:** [3.x]
**Phạm vi:** [all / domain X / severity Y]
**Tổng findings:** [N]

## Tóm tắt
| Mức độ | Số lượng |
|--------|----------|
| 🔴 CRITICAL | X |
| 🟠 HIGH | X |
| 🟡 MEDIUM | X |
| 🟢 LOW | X |

## Findings

### 🔴 CRITICAL

#### [C-01] [Tên pattern] — [file:dòng]
**Lĩnh vực:** [Domain]
**Mã nguồn:**
```java
[đoạn code vi phạm]
```
**Đề xuất:** [giải pháp ngắn gọn]
**Tool:** [SpotBugs lint / SonarQube rule nếu có]
**Tham khảo:** [file knowledge tương ứng]

### 🟠 HIGH
[tương tự...]
```

**2. File báo cáo (chi tiết):**
Ghi vào `reports/failures-java-YYYY-MM-DD-HHMMSS.md` trong thư mục skill.

### Bước 6: Tích hợp công cụ Java

Nếu có thể, chạy bổ sung và so sánh kết quả:

```bash
# Maven build check
./mvnw compile -q 2>&1

# SpotBugs (nếu có plugin)
./mvnw spotbugs:check 2>&1

# OWASP Dependency-Check (nếu có plugin)
./mvnw dependency-check:check 2>&1

# Check Spring Boot config
./mvnw spring-boot:run --dry-run 2>&1
```

So sánh findings từ tools với findings từ knowledge base, đánh dấu findings đã được tools cover.

### Bước 7: Đề xuất tiếp theo

Sau khi xuất báo cáo, đề xuất:
- "Chạy `/ef-java critical` để tập trung vào lỗi nghiêm trọng nhất"
- "Chạy `/ef-java 04` để kiểm tra chuyên sâu JPA/Hibernate"
- "Chạy `/ef-java 03` để kiểm tra bảo mật"
- "Thêm SpotBugs/SonarQube vào CI pipeline để phát hiện sớm"

## Lưu ý quan trọng

1. **Không sửa code tự động** — Skill chỉ báo cáo, không tự ý sửa mã nguồn
2. **False positives** — Một số findings có thể là false positive, người dùng cần xác nhận
3. **Spring Boot version** — Patterns dựa trên Spring Boot 3.x (Jakarta namespace)
4. **Java version** — Một số patterns chỉ áp dụng cho Java 21+ (virtual threads, records)
5. **Config files** — Quét cả `application*.yml` và `application*.properties`
