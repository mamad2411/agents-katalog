---
name: revit-addin
description: "Scaffold và phát triển Revit Add-In với Nice3point.Revit.Templates. Hỗ trợ Revit 2022–2027, đa template (revit-addin/application/module/solution/benchmark/test), DI mode container mặc định, WPF + MVVM Toolkit, Serilog logging. TRIGGER when: user nói 'tạo add-in revit', 'revit plugin', 'nice3point', 'revit project mới', hoặc cwd có .csproj với Sdk=\"Nice3point.Revit.Sdk\". Khi tạo project Revit Add-In mới, scaffold module, hoặc setup multi-version Revit. Keywords: revit, addin, nice3point, scaffold, dotnet, wpf, mvvm, ribbon."
user-invocable: true
when_to_use: "Khi tạo project Revit Add-In mới, scaffold module, hoặc setup multi-version Revit."
category: revit
keywords: [revit, addin, nice3point, scaffold, dotnet, wpf, mvvm, ribbon]
argument-hint: "[task description]"
metadata:
  author: hoang
  version: "1.0.0"
  stabs: ["C#", ".NET 8", "Revit API 2022-2027", "Nice3point.Revit.Sdk"]
---

<!-- portable-host-contract:start -->
## Portable host contract

This skill is shared by Codex and Google Antigravity.

- Use the host's native task tracker. In Codex, use `update_plan`; in Antigravity, maintain the task-list artifact.
- Use native collaboration and user-input tools exposed by the host. Treat legacy tool names as capability descriptions, never literal calls.
- Resolve bundled resources from the project-local `.agents/skills/` tree. Do not create or write a user-global skill directory.
<!-- portable-host-contract:end -->

# Revit Add-In Scaffold & Development (Nice3point)

Source of truth: https://github.com/Nice3point/RevitTemplates

## Prerequisites

```bash
# Cài 1 lần
dotnet new install Nice3point.Revit.Templates
dotnet new list revit   # verify 6 templates
```

## 6 Templates có sẵn

| Short Name | Mục đích | Khi nào dùng |
|---|---|---|
| `revit-addin` | Add-in đơn lẻ | Mặc định, dự án nhỏ/vừa, 1 DLL |
| `revit-application` | Entry point của solution modular | Bắt buộc với kiến trúc nhiều module |
| `revit-module` | Module business logic | Reference vào application |
| `revit-solution` | Enterprise solution | Có CI/CD + Installer (WixSharp) + Autodesk bundle |
| `revit-benchmark` | BenchmarkDotNet trong Revit process | Đo perf API call |
| `revit-test` | TUnit chạy trong Revit process | Test cần Revit context |

## Default scaffold (recommended)

```bash
mkdir MyAddIn && cd MyAddIn
dotnet new revit-addin \
  --addinManifestType application \
  --addinUiWpf true \
  --addinDiMode container \
  --addinLogging true
```

**Tại sao default:**
- `application` → có Ribbon, sự kiện startup/shutdown (90% use case)
- `addinUiWpf true` → có sẵn View/ViewModel + CommunityToolkit.Mvvm
- `addinDiMode container` → DI nhẹ (`Microsoft.Extensions.DependencyInjection`), không cần full host lifecycle như `hosting`
- `addinLogging true` → Serilog có sẵn, log vào file

### Khi nào đổi default

| Tình huống | Đổi sang |
|---|---|
| Add-in headless (no UI, batch process) | `--addinManifestType dbApplication --addinUiWpf false` |
| Add-in chỉ 1 command đơn giản | `--addinManifestType command --addinDiMode disabled` |
| Project enterprise lớn | `--addinDiMode hosting` (full Microsoft.Extensions.Hosting) |

## Multi-version Revit 2022–2027

Project mặc định scaffold với configs:

```xml
<Configurations>Debug.R22;Debug.R23;Debug.R24;Debug.R25;Debug.R26;Debug.R27</Configurations>
<Configurations>$(Configurations);Release.R22;Release.R23;Release.R24;Release.R25;Release.R26;Release.R27</Configurations>
```

**Preprocessor constants** (load `references/multi-version-strategy.md` chi tiết):

| Constant | Đúng khi |
|---|---|
| `REVIT2022`..`REVIT2027` | Build cho đúng version đó |
| `REVIT2022_OR_GREATER`..`REVIT2027_OR_GREATER` | Build cho version ≥ đó |

**Quy tắc khi viết code đa version:**
- ❌ Không gọi API đã bị xóa trong version mới mà không có `#if !REVIT<XX>_OR_GREATER`.
- ❌ Không dùng `ElementId.IntegerValue` (xóa từ R23) trong code chung — phải wrap `#if REVIT2023_OR_GREATER ... #else ... #endif`.
- ✅ API mới (ForgeTypeId, UnitTypeId từ R21+) wrap `#if REVIT2021_OR_GREATER`.
- ✅ Mỗi method chứa preprocessor branch phải có comment `// Multi-version: <api-name>` để Grep tìm được.

## Cấu trúc project chuẩn

```
MyAddIn/
├── Application.cs                     ← Kế thừa ExternalApplication, tạo Ribbon
├── MyAddIn.csproj                     ← Sdk="Nice3point.Revit.Sdk"
├── MyAddIn.addin                      ← Revit manifest XML
├── Commands/                          ← External Commands
│   └── StartupCommand.cs
├── Configuration/
│   ├── HostingConfiguration.cs        ← DI setup (nếu addinDiMode != disabled)
│   └── LoggerConfiguration.cs         ← Serilog config
├── ViewModels/
│   └── MyAddInViewModel.cs            ← sealed partial, ObservableObject
├── Views/
│   ├── MyAddInView.xaml
│   └── MyAddInView.xaml.cs            ← code-behind tối thiểu, chỉ InitializeComponent
├── Models/                            ← POCO + DTO
├── Services/                          ← Business logic, inject qua DI
├── Resources/
│   ├── Icons/
│   │   ├── RibbonIcon16.png
│   │   └── RibbonIcon32.png
│   └── Themes/                        ← (nếu dùng skill revit-xaml-styles)
│       └── Theme.xaml
└── Properties/
    └── launchSettings.json            ← F5 → launch Revit.exe
```

**Quy tắc:**
- File C# (`Application.cs`, `MyAddInViewModel.cs`) — **PascalCase** (theo convention C#).
- File XAML asset (`Theme.xaml`, `ThemeDark.xaml`) — **PascalCase** (theo WPF convention).
- File config phụ (`launchSettings.json`, `appsettings.json`) — **camelCase** (theo .NET convention).
- Không dùng kebab-case cho `.cs`/`.xaml` (vi phạm convention ngôn ngữ).

## Nice3point.Revit.Toolkit highlights

Extension methods rút gọn code Revit API:

```csharp
// Cũ (Revit API gốc) — dài
var panel = application.CreateRibbonPanel("MyTab", "Commands");
var buttonData = new PushButtonData("btn", "Execute",
    Assembly.GetExecutingAssembly().Location, typeof(StartupCommand).FullName);
var button = panel.AddItem(buttonData) as PushButton;
button.LargeImage = new BitmapImage(new Uri("pabs://...icon32.png"));

// Mới (Nice3point.Toolkit) — gọn
var panel = Application.CreatePanel("Commands", "MyAddIn");
panel.AddPushButton<StartupCommand>("Execute")
     .SetImage("/MyAddIn;component/Resources/Icons/RibbonIcon16.png")
     .SetLargeImage("/MyAddIn;component/Resources/Icons/RibbonIcon32.png");
```

Đọc `references/nice3point-toolkit.md` để xem full extension method list.

## Workflow integration

| Step | Skill liên quan |
|---|---|
| Scaffold project mới | **`revit-addin`** (skill này) |
| Viết ViewModel/View | `revit-wpf-mvvm` |
| Style XAML | `revit-xaml-styles` |
| F5 debug trong Revit | `revit-debug` |
| Unit test | `revit-test` |
| Plan đa phase | `/bs:plan` (đã refactor cho Revit) |
| Implement | `/bs:cook` (đã refactor cho Revit) |

## References

- `references/nice3point-toolkit.md` — Full extension method catalog
- `references/multi-version-strategy.md` — Preprocessor pattern + API compat 2022–2027

## Quyết định project chốt cho repo này

| Quyết định | Giá trị |
|---|---|
| Revit versions | 2022–2027 (6 configs) |
| DI mode | `container` (mặc định), `hosting` cho `revit-solution` |
| UI | WPF + CommunityToolkit.Mvvm (luôn bật) |
| Logging | Serilog (luôn bật) |
| Manifest type | `application` (mặc định) |

Khi user yêu cầu khác giá trị mặc định → confirm trước bằng `host user-input capability`.
