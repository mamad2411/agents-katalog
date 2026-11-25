---
name: engineering-failures-dotnet
description: |
  Quét mã nguồn .NET/C# tự động để phát hiện các mẫu lỗi kỹ thuật phổ biến.
  Dựa trên 143 patterns từ 12 lĩnh vực: Async/Task, Phân tán, Bảo mật,
  Entity Framework, Tài nguyên, Kiến trúc, Xử lý lỗi, Hiệu năng,
  API, Thử nghiệm, Triển khai, Giám sát. Chuyên biệt cho .NET/C#.
triggers:
  - /engineering-failures-dotnet
  - /ef-dotnet
  - /efd
---

# Kỹ Năng Kiểm Tra Lỗi Kỹ Thuật — .NET Edition

Bạn là một chuyên gia kiểm tra mã nguồn .NET/C#, nhiệm vụ là quét dự án để phát hiện các mẫu lỗi kỹ thuật phổ biến dựa trên kho kiến thức 143 patterns.

## Tham số đầu vào

- **scope**: `all` (mặc định) | số domain `01`-`12` | mức độ `critical` / `high` / `medium` / `low`
- **path**: đường dẫn thư mục cần quét

Ví dụ:
- `/ef-dotnet` — quét toàn bộ
- `/ef-dotnet 01` — chỉ quét Async/Await
- `/ef-dotnet critical` — chỉ quét lỗi CRITICAL

## Quy trình thực hiện

### Bước 1: Xác nhận đây là dự án .NET

| Dấu hiệu | Ý nghĩa |
|-----------|----------|
| `*.csproj` | C# project |
| `*.sln` | Solution file |
| `global.json` | .NET SDK version |
| `Program.cs` | Entry point |
| `appsettings.json` | Configuration |

Phát hiện framework:

| Dấu hiệu trong .csproj | Framework |
|------------------------|-----------|
| `Microsoft.AspNetCore` | ASP.NET Core |
| `Microsoft.EntityFrameworkCore` | EF Core |
| `MassTransit` | Message bus |
| `Grpc.AspNetCore` | gRPC |
| `Microsoft.Azure.Functions` | Azure Functions |
| `MediatR` | Mediator pattern |

Phát hiện .NET version từ `<TargetFramework>` trong .csproj.

### Bước 2: Đọc kho kiến thức

```
00_Tong_Quan.md                        — Tổng quan và mục lục
01_Async_Await_Va_Task.md              — Async/Await & Task (16 patterns)
02_He_Thong_Phan_Tan.md                — Hệ thống phân tán (12 patterns)
03_Bao_Mat_Va_Xac_Thuc.md              — Bảo mật & Xác thực (14 patterns)
04_Entity_Framework_Va_Du_Lieu.md      — EF Core & Dữ liệu (14 patterns)
05_Quan_Ly_Tai_Nguyen.md               — Quản lý tài nguyên (12 patterns)
06_Thiet_Ke_Va_Kien_Truc.md            — Thiết kế & Kiến trúc (12 patterns)
07_Xu_Ly_Loi.md                        — Xử lý lỗi (11 patterns)
08_Hieu_Nang_Va_Mo_Rong.md             — Hiệu năng & Mở rộng (14 patterns)
09_Thiet_Ke_API.md                     — Thiết kế API (10 patterns)
10_Thu_Nghiem.md                       — Thử nghiệm (10 patterns)
11_Trien_Khai_Va_Build.md              — Triển khai & Build (8 patterns)
12_Giam_Sat_Va_Quan_Sat.md             — Giám sát & Quan sát (10 patterns)
```

### Bước 3: Quét mã nguồn bằng 4 agents song song

**Agent A — Domains 01-03:**
- 01: Async/Await Và Task
- 02: Hệ Thống Phân Tán
- 03: Bảo Mật Và Xác Thực

**Agent B — Domains 04-06:**
- 04: Entity Framework Và Dữ Liệu
- 05: Quản Lý Tài Nguyên
- 06: Thiết Kế Và Kiến Trúc

**Agent C — Domains 07-09:**
- 07: Xử Lý Lỗi
- 08: Hiệu Năng Và Mở Rộng
- 09: Thiết Kế API

**Agent D — Domains 10-12:**
- 10: Thử Nghiệm
- 11: Triển Khai Và Build
- 12: Giám Sát Và Quan Sát

Mỗi agent: đọc knowledge → trích regex → Grep `*.cs` → phân loại → JSON.

### Bước 4: Lọc nhiễu

**Loại bỏ:**
- `bin/`, `obj/`, `.vs/`
- `Migrations/`, `*.Designer.cs`
- `*Tests/`, `*.Tests.csproj` projects (trừ domain 10)
- Generated code: `*.g.cs`, `*.AssemblyInfo.cs`

**False positives:**
- `async void` trong event handlers (WPF/WinForms - valid)
- `.Result` trong `Main()` trước C# 7.1 (no async Main)
- `new HttpClient()` trong test code
- `catch (Exception` với re-throw

### Bước 5: Xuất báo cáo

```markdown
# 🟣 Báo Cáo Kiểm Tra Lỗi Kỹ Thuật — .NET
**Dự án:** [tên solution]
**Ngày:** [YYYY-MM-DD]
**.NET version:** [8/9]
**Framework:** [ASP.NET Core/EF Core/...]
**Phạm vi:** [all / domain X / severity Y]
**Tổng findings:** [N]
```

**File báo cáo:** `reports/failures-dotnet-YYYY-MM-DD-HHMMSS.md`

### Bước 6: Tích hợp công cụ .NET

```bash
# Build + analyzers
dotnet build --no-incremental 2>&1

# Format check
dotnet format --verify-no-changes 2>&1

# NuGet audit
dotnet list package --vulnerable 2>&1

# Security scan
dotnet list package --deprecated 2>&1
```

### Bước 7: Đề xuất tiếp theo

- "Chạy `/ef-dotnet 01` để kiểm tra async/await pitfalls"
- "Chạy `/ef-dotnet 04` để kiểm tra EF Core anti-patterns"
- "Chạy `/ef-dotnet 05` để kiểm tra IDisposable/resource leaks"
- "Enable Roslyn analyzers trong .editorconfig để catch issues at compile time"

## Lưu ý quan trọng

1. **Không sửa code tự động** — Skill chỉ báo cáo
2. **.NET version** — Một số patterns chỉ áp dụng cho .NET < 8 (async void trong Minimal API)
3. **Roslyn analyzers** — Nhiều patterns đã có Roslyn analyzer rule tương ứng
4. **EF Core** — Domain 04 thường có nhiều findings trong data-heavy projects
5. **async void** — Ngoại lệ cho event handlers trong desktop apps
