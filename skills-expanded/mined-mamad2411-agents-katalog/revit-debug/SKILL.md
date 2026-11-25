---
name: revit-debug
description: "Debug Revit Add-In trong Revit process. F5 workflow (build → deploy → launch Revit → attach), troubleshoot lỗi thường gặp (FileLoadException, add-in không hiện, RevitAPI.dll not found), Serilog logging, breakpoint trong External Command. TRIGGER when: task chứa 'debug revit', 'F5', 'không build được', 'add-in không load', 'attach process', 'FileLoadException', hoặc khi user báo lỗi runtime trong Revit. Khi debug add-in trong Revit, troubleshoot deploy issues, hoặc setup logging. Keywords: debug, revit, f5, deploy, attach, serilog, troubleshoot, ilrepack."
user-invocable: true
when_to_use: "Khi debug add-in trong Revit, troubleshoot deploy issues, hoặc setup logging."
category: revit
keywords: [debug, revit, f5, deploy, attach, serilog, troubleshoot, ilrepack]
metadata:
  author: hoang
  version: "1.0.0"
---

<!-- portable-host-contract:start -->
## Portable host contract

This skill is shared by Codex and Google Antigravity.

- Use the host's native task tracker. In Codex, use `update_plan`; in Antigravity, maintain the task-list artifact.
- Use native collaboration and user-input tools exposed by the host. Treat legacy tool names as capability descriptions, never literal calls.
- Resolve bundled resources from the project-local `.agents/skills/` tree. Do not create or write a user-global skill directory.
<!-- portable-host-contract:end -->

# Revit Add-In Debug Workflow

Tận dụng Nice3point SDK auto-deploy + LaunchRevit cho debug loop nhanh nhất.

## F5 Workflow (chuẩn)

1. **Chọn configuration** matching Revit version đã cài:
   - Revit 2024 → `Debug.R24`
   - Revit 2027 → `Debug.R27`

2. **Nhấn F5** trong Rider/Visual Studio. MSBuild auto-thực hiện:
   - Build project với `TargetFramework` đúng (net48 cho R22–R24, net8.0-windows cho R25+).
   - Pull đúng version `Nice3point.Revit.Api.RevitAPI` từ NuGet.
   - Copy DLL + `.addin` vào `%ProgramData%\Autodesk\Revit\Addins\<version>\` (do `<DeployAddin>true</DeployAddin>`).
   - Launch `Revit.exe` với debugger attach sẵn (do `<LaunchRevit>true</LaunchRevit>`).

3. **Đặt breakpoint** trong code (`Application.cs`, `*Command.cs`, `*ViewModel.cs`). Debugger sẽ dừng khi Revit gọi tới.

4. **Test trong Revit:**
   - Mở 1 project Revit bất kỳ (`.rvt`).
   - Vào tab Ribbon của add-in → click button.
   - Breakpoint hit → step debug bình thường.

## `.csproj` config bắt buộc

```xml
<PropertyGroup>
    <UseWPF>true</UseWPF>
    <DeployAddin>true</DeployAddin>     <!-- Auto copy vào Addins folder -->
    <LaunchRevit>true</LaunchRevit>     <!-- F5 mở Revit -->
    <IsRepackable>true</IsRepackable>   <!-- ILRepack gộp DLL -->
    <EnableDynamicLoading>true</EnableDynamicLoading>  <!-- Assembly isolation .NET Core -->
</PropertyGroup>
```

## Troubleshoot Matrix

| Triệu chứng | Nguyên nhân | Cách fix |
|---|---|---|
| F5 không mở Revit | `<LaunchRevit>true</LaunchRevit>` chưa có | Thêm vào `.csproj`. Hoặc Revit version chưa cài đúng đường dẫn `<host-path>`. |
| Build fail `RevitAPI.dll not found` | Configuration không match Revit installed | Đổi sang `Debug.R<XX>` đúng version đã cài. |
| Add-in không hiện trong Revit ribbon | `.addin` manifest chưa copy hoặc namespace sai | 1. Verify `<DeployAddin>true</DeployAddin>`. 2. Check `%ProgramData%\Autodesk\Revit\Addins\<version>\<addin>.addin` tồn tại. 3. Mở `.addin` xem `<Assembly>` đúng path DLL không. |
| `FileLoadException` khi load DLL | DLL phụ thuộc xung đột version với add-in khác | Bật `<IsRepackable>true</IsRepackable>` → ILRepack gộp deps vào 1 DLL. |
| `FileNotFoundException: CommunityToolkit.Mvvm` | Dependency không deploy | Check `<IsRepackable>` hoặc copy thủ công DLL phụ thuộc vào folder Addins. |
| Breakpoint không hit | Debugger không attach đúng process | 1. F5 lại. 2. Hoặc manual: Debug → Attach to Process → `Revit.exe`. |
| Lỗi compile sau khi tạo template | `dotnet new install` cài bản cũ | `dotnet new uninstall Nice3point.Revit.Templates && dotnet new install Nice3point.Revit.Templates` |
| Add-in crash Revit khi startup | Exception trong `OnStartupAsync()` không catch | Wrap try/catch trong `Application.OnStartupAsync`. Log qua Serilog. Check `%LocalAppData%\Autodesk\Revit\Addins\...\Logs\`. |
| Modal dialog hiện sau Revit window (không focus) | `Owner` chưa set | Trong command: `new WindowInteropHelper(view) { Owner = UiApplication.MainWindowHandle };` |
| Modeless command crash "Cannot modify document outside transaction" | Gọi Revit API từ ViewModel thread | Phải dùng `ExternalEvent.Create(handler)`, gọi `_externalEvent.Raise()` từ ViewModel. |
| Build OK nhưng change không reflect | Old DLL cached | 1. Đóng Revit. 2. `dotnet clean` + rebuild. 3. Xóa folder `bin/` thủ công nếu cần. |

## Attach to Process thủ công

Khi F5 không work (vd. dùng Visual Studio Code không hỗ trợ launch profile):

1. Mở Revit thủ công.
2. IDE: Debug → Attach to Process.
3. Chọn `Revit.exe` (PID đang chạy).
4. Đặt breakpoint trong code.
5. Trigger command trong Revit.

## Serilog logging setup

`Configuration/LoggerConfiguration.cs`:

```csharp
public static class LoggerConfiguration
{
    public static void Setup()
    {
        var logPath = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            "MyAddIn", "logs", "addin-.log");

        Log.Logger = new Serilog.LoggerConfiguration()
            .MinimumLevel.Debug()
            .WriteTo.File(logPath,
                rollingInterval: RollingInterval.Day,
                retainedFileCountLimit: 7,
                outputTemplate: "[{Timestamp:HH:mm:ss.fff} {Level:u3}] {SourceContext} {Message:lj}{NewLine}{Exception}")
            .Enrich.FromLogContext()
            .CreateLogger();
    }
}
```

Trong `Application.cs`:

```csharp
public override async Task OnStartupAsync()
{
    LoggerConfiguration.Setup();
    Log.Information("MyAddIn starting up. Revit version: {Version}", Application.VersionNumber);

    try
    {
        await Host.StartAsync();
        CreateRibbon();
    }
    catch (Exception ex)
    {
        Log.Fatal(ex, "Failed to start MyAddIn");
        throw;
    }
}
```

Log file output: `%LocalAppData%\MyAddIn\logs\addin-2026-05-17.log`.

## Debug tips theo loại bug

### UI không update khi data thay đổi
- Property dùng `[ObservableProperty]` không? (Phải có generator).
- Class có `partial` keyword không?
- Binding path đúng tên property (PascalCase)?
- DataContext có set đúng không? (Snoop với Snoop WPF tool.)

### Command không enable
- `CanExecute` method tồn tại + return đúng?
- `[NotifyCanExecuteChangedFor(nameof(XxxCommand))]` trên property phụ thuộc?

### Transaction lỗi
- Đang trong `[Transaction(TransactionMode.Manual)]` chưa? Phải có `using var t = doc.NewTransaction("..."); t.Start(); ...; t.Commit();`.
- Modeless: dùng `ExternalEvent`?

### Crash khi đóng modal
- DataContext implement `IDisposable` nhưng `Dispose` không được gọi → handle `Window.Closed` event.

## Tool hỗ trợ

- **Snoop WPF** (https://github.com/snoopwpf/snoopwpf): Inspect WPF visual tree khi Revit chạy.
- **dotPeek** / **ILSpy**: Decompile Revit API hoặc add-in khác để hiểu behavior.
- **Process Monitor (procmon)**: Track file access khi add-in load fail.
- **RevitLookup** (https://github.com/jeremytammik/RevitLookup): Khám phá Revit element/parameter live trong Revit.

## Workflow khi báo bug

1. **Đọc log** trước (`%LocalAppData%\MyAddIn\logs\`).
2. **Reproduce với breakpoint** ở entry point command.
3. **Step debug** đến chỗ exception.
4. **Check Output window** trong Visual Studio/Rider — nhiều exception silent ở đó.
5. **Nếu add-in không load:** check `Revit Journal` (`%LocalAppData%\Autodesk\Revit\<version>\Journals\journal.<n>.txt`).
