---
name: revit-wpf-mvvm
description: "Chuẩn WPF + CommunityToolkit.Mvvm cho Revit Add-In. Patterns ObservableObject, [ObservableProperty], [RelayCommand], DI inject ViewModel, async command với CancellationToken, IRecipient<T> + WeakReferenceMessenger. TRIGGER when: tạo/sửa file `*ViewModel.cs`, `*View.xaml`, hoặc task có keyword 'mvvm', 'wpf', 'view model', 'binding', 'observable'. Khi viết hoặc review code WPF + MVVM trong Revit Add-In dùng Nice3point template. Keywords: wpf, mvvm, communitytoolkit, observableobject, relaycommand, binding, revit."
user-invocable: true
when_to_use: "Khi viết hoặc review code WPF + MVVM trong Revit Add-In dùng Nice3point template."
category: revit
keywords: [wpf, mvvm, communitytoolkit, observableobject, relaycommand, binding, revit]
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

# Revit WPF + MVVM Toolkit Standards

Stabs: WPF (.NET 8 / .NET Framework 4.8) + `CommunityToolkit.Mvvm` 8.4+ + DI qua `Microsoft.Extensions.DependencyInjection`.

## ViewModel pattern (mandatory)

```csharp
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Microsoft.Extensions.Logging;

namespace MyAddIn.ViewModels;

public sealed partial class WallReportViewModel : ObservableObject
{
    private readonly ILogger<WallReportViewModel> _logger;
    private readonly IWallService _wallService;

    public WallReportViewModel(
        ILogger<WallReportViewModel> logger,
        IWallService wallService)
    {
        _logger = logger;
        _wallService = wallService;
    }

    [ObservableProperty]
    private string _searchText = string.Empty;

    [ObservableProperty]
    [NotifyCanExecuteChangedFor(nameof(RunReportCommand))]
    private bool _isBusy;

    public ObservableCollection<WallInfo> Walls { get; } = new();

    [RelayCommand(CanExecute = nameof(CanRunReport))]
    private async Task RunReportAsync(CancellationToken token)
    {
        IsBusy = true;
        try
        {
            var walls = await _wallService.GetAllWallsAsync(token);
            Walls.Clear();
            foreach (var wall in walls) Walls.Add(wall);
        }
        finally
        {
            IsBusy = false;
        }
    }

    private bool CanRunReport() => !IsBusy;
}
```

**Yêu cầu bắt buộc:**
- `sealed partial class` (toolkit dùng source generator → cần `partial`).
- Kế thừa `ObservableObject` (auto `INotifyPropertyChanged`).
- Constructor inject mọi dependency, gán vào `_field` readonly.
- `[ObservableProperty]` trên private field → tự sinh public property.
- `[RelayCommand]` trên method → tự sinh `XxxCommand`. Method `async Task` → command tự handle.
- Long-running command **PHẢI** nhận `CancellationToken` (toolkit pass tự động).
- `[NotifyCanExecuteChangedFor]` khi property ảnh hưởng `CanExecute`.

## View pattern

`Views/WallReportView.xaml`:

```xml
<Window x:Class="MyAddIn.Views.WallReportView"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Wall Report"
        Width="800" Height="600"
        WindowStartupLocation="CenterOwner">
    <Window.Resources>
        <ResourceDictionary>
            <ResourceDictionary.MergedDictionaries>
                <ResourceDictionary Source="pabs://application:,,,/MyAddIn;component/Resources/Themes/Theme.xaml"/>
            </ResourceDictionary.MergedDictionaries>
        </ResourceDictionary>
    </Window.Resources>

    <Grid Margin="{DynamicResource Spacing.Large}">
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="*"/>
            <RowDefinition Height="Auto"/>
        </Grid.RowDefinitions>

        <TextBox Grid.Row="0"
                 Style="{DynamicResource SearchTextBox}"
                 Text="{Binding SearchText, UpdateSourceTrigger=PropertyChanged}"/>

        <DataGrid Grid.Row="1"
                  ItemsSource="{Binding Walls}"
                  IsReadOnly="True"
                  Margin="{DynamicResource Spacing.MediumVertical}"/>

        <Button Grid.Row="2"
                Content="Run Report"
                Style="{DynamicResource PrimaryButton}"
                Command="{Binding RunReportCommand}"
                HorizontalAlignment="Right"/>
    </Grid>
</Window>
```

`Views/WallReportView.xaml.cs` (code-behind **tối thiểu**):

```csharp
namespace MyAddIn.Views;

public partial class WallReportView : Window
{
    public WallReportView(WallReportViewModel viewModel)
    {
        InitializeComponent();
        DataContext = viewModel;
    }
}
```

**Yêu cầu bắt buộc:**
- Code-behind CHỈ chứa `InitializeComponent()` + `DataContext = viewModel` (constructor injection).
- KHÔNG set `DataContext` trong XAML (sẽ phá DI).
- KHÔNG dùng `x:Name` để truy cập control từ code-behind (vi phạm MVVM).
- Mọi style dùng `DynamicResource` (cho phép swap theme runtime — xem `revit-xaml-styles`).

## DI registration

`Configuration/HostingConfiguration.cs`:

```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Serilog;
using Serilog.Extensions.Logging;

namespace MyAddIn.Configuration;

public static class HostingConfiguration
{
    public static IServiceCollection AddMyAddInServices(this IServiceCollection services)
    {
        // Services (singleton hoặc transient theo lifecycle)
        services.AddSingleton<IWallService, WallService>();

        // ViewModels — Transient (mỗi lần mở UI → instance mới)
        services.AddTransient<WallReportViewModel>();

        // Views — Transient, inject ViewModel qua constructor
        services.AddTransient<WallReportView>();

        return services;
    }
}
```

`Commands/StartupCommand.cs`:

```csharp
[Transaction(TransactionMode.Manual)]
public class StartupCommand : ExternalCommand
{
    public override void Execute()
    {
        var view = Host.GetService<WallReportView>();
        // Set owner cho modal đúng kiểu — Revit MainWindow
        var helper = new System.Windows.Interop.WindowInteropHelper(view)
        {
            Owner = UiApplication.MainWindowHandle
        };
        view.ShowDialog();
    }
}
```

## Modal vs Modeless

| Modal (`ShowDialog`) | Modeless (`Show`) |
|---|---|
| Block Revit UI | User vẫn tương tác Revit |
| Đơn giản, không cần External Event | Phải dùng `ExternalEvent` để gọi Revit API từ ViewModel |
| Default cho 90% case | Chỉ khi UX cần (vd. picker, panel side) |

**Modeless yêu cầu:**
1. Tạo `IExternalEventHandler` implementation.
2. `ExternalEvent.Create(handler)` lưu instance trong service singleton.
3. ViewModel gọi `_externalEvent.Raise()` thay vì gọi trực tiếp Revit API.
4. KHÔNG bao giờ truy cập `Document` từ background thread.

## References

- `references/mvvm-toolkit-patterns.md` — Full pattern catalog (`[ObservableProperty]`, `[RelayCommand]`, Messenger, validation)
- `references/wpf-do-dont.md` — Anti-patterns và quy ước

## Tóm tắt do/don't

| ✅ DO | ❌ DON'T |
|---|---|
| `sealed partial class XxxViewModel : ObservableObject` | Kế thừa `INotifyPropertyChanged` thủ công |
| Constructor inject `ILogger<T>`, services | `Activator.CreateInstance` |
| `[ObservableProperty] private string _name;` | Viết `public string Name { get; set; }` + `OnPropertyChanged()` thủ công |
| `[RelayCommand] async Task FooAsync(CancellationToken token)` | `ICommand Foo => new RelayCommand(...)` |
| `DataContext = viewModel` trong code-behind | `<Window.DataContext><vm:XxxViewModel/></Window.DataContext>` |
| Mọi style → `DynamicResource` | `StaticResource` (không swap theme được) |
| Modal `ShowDialog()` + set owner Revit MainWindow | Show không owner (popup lạc) |
| Modeless qua `ExternalEvent` | Gọi `Document.NewTransaction` từ ViewModel trực tiếp |
