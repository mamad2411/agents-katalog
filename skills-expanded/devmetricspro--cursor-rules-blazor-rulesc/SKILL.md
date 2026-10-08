---
alwaysApply: false
---

# Blazor Server Best Practices for DevMetrics Pro

## Blazor Component Structure

### Component Organization
```
Components/
├── Layout/
│   ├── MainLayout.razor          # Main app layout
│   ├── NavMenu.razor            # Navigation sidebar
│   └── TopBar.razor             # Top navigation bar
├── Pages/
│   ├── Dashboard.razor          # Page components (routable)
│   ├── Developers.razor
│   └── Repositories.razor
├── Shared/
│   ├── StatCard.razor           # Reusable components
│   ├── MetricChart.razor
│   └── LoadingSpinner.razor
└── Dashboard/                    # Feature-specific components
    ├── CommitGraph.razor
    └── ActivityHeatmap.razor
```

## Render Modes (Blazor .NET 8+)

### Understanding Render Modes
DevMetrics Pro uses **Blazor Server** with SignalR for real-time updates.

✅ **Use InteractiveServer render mode**:
```razor
@page "/dashboard"
@rendermode InteractiveServer

<h3>Dashboard</h3>
```

### When to Use Each Render Mode:
- `InteractiveServer`: Real-time dashboard, live updates (our default)
- `InteractiveWebAssembly`: Offline analysis (future sprint)
- `InteractiveAuto`: Hybrid approach (not used in MVP)

## Component File Structure

### .razor File Structure
✅ **CORRECT ORDER**:
```razor
@page "/developers"
@rendermode InteractiveServer

@* Usings *@
@using DevMetricsPro.Application.DTOs
@using DevMetricsPro.Application.Interfaces

@* Injected Services *@
@inject IDeveloperService DeveloperService
@inject ILogger<Developers> Logger

@* HTML Markup *@
<PageTitle>Developers - DevMetrics Pro</PageTitle>

<MudText Typo="Typo.h4" Class="mb-4">Developers</MudText>

@if (_isLoading)
{
    <MudProgressCircular Indeterminate="true" />
}
else
{
    <MudGrid>
        @foreach (var developer in _developers)
        {
            <MudItem xs="12" sm="6" md="4">
                <DeveloperCard Developer="@developer" />
            </MudItem>
        }
    </MudGrid>
}

@* Code Block *@
@code {
    private bool _isLoading = true;
    private List<DeveloperDto> _developers = new();

    protected override async Task OnInitializedAsync()
    {
        await LoadDevelopersAsync();
    }

    private async Task LoadDevelopersAsync()
    {
        _isLoading = true;
        try
        {
            _developers = await DeveloperService.GetAllDevelopersAsync();
        }
        finally
        {
            _isLoading = false;
        }
    }
}
```

## Component Parameters

### Defining Parameters
✅ **Use `[Parameter]` attribute**:
```razor
@code {
    [Parameter]
    public required DeveloperDto Developer { get; set; }
    
    [Parameter]
    public EventCallback<Guid> OnDeleteClick { get; set; }
    
    [Parameter]
    public string? CssClass { get; set; }
}
```

### Parameter Validation
✅ **Validate required parameters**:
```razor
@code {
    [Parameter]
    public required DeveloperDto Developer { get; set; }
    
    protected override void OnParametersSet()
    {
        if (Developer is null)
        {
            throw new ArgumentNullException(nameof(Developer));
        }
    }
}
```

## Lifecycle Methods

### Order of Execution
1. `SetParametersAsync`
2. `OnInitialized` / `OnInitializedAsync`
3. `OnParametersSet` / `OnParametersSetAsync`
4. `OnAfterRender` / `OnAfterRenderAsync`

### When to Use Each:
```razor
@code {
    // Load data once when component initializes
    protected override async Task OnInitializedAsync()
    {
        _data = await LoadDataAsync();
    }
    
    // React to parameter changes
    protected override async Task OnParametersSetAsync()
    {
        if (DeveloperId != _previousDeveloperId)
        {
            await LoadDeveloperAsync(DeveloperId);
            _previousDeveloperId = DeveloperId;
        }
    }
    
    // Access JavaScript or DOM (runs after render)
    protected override async Task OnAfterRenderAsync(bool firstRender)
    {
        if (firstRender)
        {
            await JSRuntime.InvokeVoidAsync("initializeChart");
        }
    }
}
```

## State Management

### Component State
✅ **Private fields for component state**:
```razor
@code {
    private bool _isLoading;
    private string _searchText = string.Empty;
    private List<DeveloperDto> _developers = new();
    private DeveloperDto? _selectedDeveloper;
}
```

### Trigger Re-render
✅ **Call `StateHasChanged()` when needed**:
```razor
@code {
    private async Task LoadDataAsync()
    {
        _isLoading = true;
        StateHasChanged(); // Force re-render to show spinner
        
        _data = await Service.GetDataAsync();
        
        _isLoading = false;
        // StateHasChanged() called automatically after async method
    }
}
```

### When to Call StateHasChanged():
- After updating state in async callbacks
- When updating state from background threads
- When state changes outside component lifecycle

## Event Handling

### Button Click Events
✅ **Use async event handlers**:
```razor
<MudButton OnClick="HandleDeleteAsync" Color="Color.Error">
    Delete
</MudButton>

@code {
    private async Task HandleDeleteAsync()
    {
        var confirmed = await DialogService.ShowMessageBox(
            "Confirm Delete",
            "Are you sure?",
            yesText: "Delete", cancelText: "Cancel");
            
        if (confirmed == true)
        {
            await DeveloperService.DeleteAsync(Developer.Id);
            await OnDeleteClick.InvokeAsync(Developer.Id);
        }
    }
}
```

### EventCallback
✅ **Use EventCallback for parent-child communication**:
```razor
@* Child Component *@
<MudButton OnClick="NotifyParent">Click Me</MudButton>

@code {
    [Parameter]
    public EventCallback<string> OnButtonClick { get; set; }
    
    private async Task NotifyParent()
    {
        await OnButtonClick.InvokeAsync("Button was clicked!");
    }
}

@* Parent Component *@
<ChildComponent OnButtonClick="HandleChildClick" />

@code {
    private void HandleChildClick(string message)
    {
        Logger.LogInformation("Child said: {Message}", message);
    }
}
```

## Dependency Injection

### Service Injection
✅ **Inject services at component level**:
```razor
@inject IDeveloperService DeveloperService
@inject ILogger<DeveloperList> Logger
@inject ISnackbar Snackbar
@inject NavigationManager Navigation
```

### Custom Services
✅ **Create component-specific services**:
```csharp
// Register in Program.cs
builder.Services.AddScoped<MetricCalculationService>();

// Inject in component
@inject MetricCalculationService MetricService
```

## Error Handling

### Try-Catch in Components
✅ **Handle errors gracefully**:
```razor
@code {
    private string? _errorMessage;
    
    private async Task LoadDataAsync()
    {
        _isLoading = true;
        _errorMessage = null;
        
        try
        {
            _data = await Service.GetDataAsync();
        }
        catch (Exception ex)
        {
            _errorMessage = "Failed to load data. Please try again.";
            Logger.LogError(ex, "Error loading data");
            Snackbar.Add(_errorMessage, Severity.Error);
        }
        finally
        {
            _isLoading = false;
        }
    }
}
```

### Error Boundaries
✅ **Use ErrorBoundary for unhandled errors**:
```razor
<ErrorBoundary>
    <ChildContent>
        <DashboardContent />
    </ChildContent>
    <ErrorContent Context="ex">
        <div class="alert alert-danger">
            <h4>An error occurred</h4>
            <p>@ex.Message</p>
        </div>
    </ErrorContent>
</ErrorBoundary>
```

## Performance Optimization

### Avoid Unnecessary Re-renders
✅ **Use `ShouldRender()` to prevent re-renders**:
```razor
@code {
    private int _counter;
    
    protected override bool ShouldRender()
    {
        // Only re-render when counter is even
        return _counter % 2 == 0;
    }
}
```

### Virtualization for Large Lists
✅ **Use Virtualize for large datasets**:
```razor
<Virtualize Items="@_developers" Context="developer">
    <DeveloperCard Developer="@developer" />
</Virtualize>
```

### Avoid Inline Lambdas in Loops
❌ **DON'T**:
```razor
@foreach (var item in items)
{
    <MudButton OnClick="@(() => DeleteItem(item))">Delete</MudButton>
}
```

✅ **DO**:
```razor
@foreach (var item in items)
{
    var currentItem = item; // Capture variable
    <MudButton OnClick="@(() => DeleteItem(currentItem))">Delete</MudButton>
}
```

Or better, use a method:
```razor
@foreach (var item in items)
{
    <MudButton OnClick="@(_ => HandleDelete(item))">Delete</MudButton>
}

@code {
    private async Task HandleDelete(Developer developer)
    {
        await DeleteItem(developer);
    }
}
```

## MudBlazor Conventions

### Component Usage
✅ **Use MudBlazor consistently**:
```razor
@* Cards *@
<MudCard Elevation="2">
    <MudCardHeader>
        <CardHeaderContent>
            <MudText Typo="Typo.h6">@Title</MudText>
        </CardHeaderContent>
    </MudCardHeader>
    <MudCardContent>
        @* Content *@
    </MudCardContent>
</MudCard>

@* Buttons *@
<MudButton Variant="Variant.Filled" Color="Color.Primary" OnClick="HandleClick">
    Save
</MudButton>

@* Forms *@
<MudTextField @bind-Value="_email" Label="Email" Variant="Variant.Outlined" />
```

### Snackbar for Notifications
✅ **Use Snackbar for user feedback**:
```razor
@inject ISnackbar Snackbar

@code {
    private async Task SaveAsync()
    {
        try
        {
            await Service.SaveAsync();
            Snackbar.Add("Saved successfully!", Severity.Success);
        }
        catch (Exception ex)
        {
            Snackbar.Add("Failed to save", Severity.Error);
        }
    }
}
```

## SignalR for Real-time Updates

### Hub Connection
✅ **Connect to SignalR hub**:
```razor
@implements IAsyncDisposable
@inject NavigationManager Navigation

@code {
    private HubConnection? _hubConnection;
    
    protected override async Task OnInitializedAsync()
    {
        _hubConnection = new HubConnectionBuilder()
            .WithUrl(Navigation.ToAbsoluteUri("/metricshub"))
            .WithAutomaticReconnect()
            .Build();
            
        _hubConnection.On<MetricUpdate>("ReceiveMetricUpdate", HandleMetricUpdate);
        
        await _hubConnection.StartAsync();
    }
    
    private void HandleMetricUpdate(MetricUpdate update)
    {
        // Update component state
        _latestMetric = update;
        StateHasChanged();
    }
    
    public async ValueTask DisposeAsync()
    {
        if (_hubConnection is not null)
        {
            await _hubConnection.DisposeAsync();
        }
    }
}
```

## Component Organization Best Practices

### Small, Focused Components
✅ Break large components into smaller ones:
```razor
@* DashboardPage.razor *@
<PageTitle>Dashboard</PageTitle>

<DashboardHeader />
<StatsCards Metrics="@_metrics" />
<ActivitySection Activities="@_activities" />
<LeaderboardSection Developers="@_topDevelopers" />
```

### Shared Components
✅ Create reusable components in `Components/Shared/`:
```razor
@* Components/Shared/LoadingSpinner.razor *@
<div class="d-flex justify-center my-4">
    <MudProgressCircular Indeterminate="true" Size="Size.Large" />
</div>

@* Usage *@
@if (_isLoading)
{
    <LoadingSpinner />
}
```

## Routing

### Page Routes
✅ **Define routes clearly**:
```razor
@page "/developers"
@page "/developers/{DeveloperId:guid}"

@code {
    [Parameter]
    public Guid? DeveloperId { get; set; }
}
```

### Navigation
✅ **Use NavigationManager for programmatic navigation**:
```razor
@inject NavigationManager Navigation

@code {
    private void NavigateToDeveloper(Guid id)
    {
        Navigation.NavigateTo($"/developers/{id}");
    }
}
```

## CSS and Styling

### Component-Scoped CSS
✅ **Use .razor.css for component-specific styles**:
```
DeveloperCard.razor
DeveloperCard.razor.css
```

```css
/* DeveloperCard.razor.css */
.developer-card {
    transition: transform 0.2s;
}

.developer-card:hover {
    transform: translateY(-4px);
}
```

### MudBlazor Classes
✅ **Use MudBlazor utility classes**:
```razor
<div class="d-flex justify-space-between align-center mb-4">
    <MudText Typo="Typo.h4">Dashboard</MudText>
    <MudButton Color="Color.Primary">Action</MudButton>
</div>
```

## Common Patterns

### Loading State Pattern
```razor
@if (_isLoading)
{
    <LoadingSpinner />
}
else if (_errorMessage is not null)
{
    <ErrorMessage Message="@_errorMessage" />
}
else if (!_data.Any())
{
    <EmptyState Message="No data available" />
}
else
{
    @* Render data *@
}
```

### Form Validation Pattern
```razor
<EditForm Model="@_model" OnValidSubmit="HandleValidSubmit">
    <DataAnnotationsValidator />
    <MudTextField @bind-Value="_model.Email" 
                  Label="Email" 
                  For="@(() => _model.Email)" />
    <ValidationSummary />
    <MudButton ButtonType="ButtonType.Submit">Submit</MudButton>
</EditForm>
```

## Anti-Patterns to Avoid

❌ **DON'T** call StateHasChanged() unnecessarily
❌ **DON'T** put business logic in components (use services)
❌ **DON'T** create large monolithic components
❌ **DON'T** forget to dispose of resources (IAsyncDisposable)
❌ **DON'T** use synchronous APIs (use async/await)
❌ **DON'T** hardcode URLs or configuration values

## Quick Checklist

Before committing Blazor components:
- [ ] Component is focused and single-responsibility
- [ ] Uses InteractiveServer render mode
- [ ] All injected services are needed
- [ ] Error handling in place
- [ ] Loading states handled
- [ ] EventCallbacks used for parent communication
- [ ] Implements IAsyncDisposable if using resources
- [ ] No business logic (delegated to services)
- [ ] Consistent with MudBlazor design system
# Blazor Server Best Practices for DevMetrics Pro

## Blazor Component Structure

### Component Organization
```
Components/
├── Layout/
│   ├── MainLayout.razor          # Main app layout
│   ├── NavMenu.razor            # Navigation sidebar
│   └── TopBar.razor             # Top navigation bar
├── Pages/
│   ├── Dashboard.razor          # Page components (routable)
│   ├── Developers.razor
│   └── Repositories.razor
├── Shared/
│   ├── StatCard.razor           # Reusable components
│   ├── MetricChart.razor
│   └── LoadingSpinner.razor
└── Dashboard/                    # Feature-specific components
    ├── CommitGraph.razor
    └── ActivityHeatmap.razor
```

## Render Modes (Blazor .NET 8+)

### Understanding Render Modes
DevMetrics Pro uses **Blazor Server** with SignalR for real-time updates.

✅ **Use InteractiveServer render mode**:
```razor
@page "/dashboard"
@rendermode InteractiveServer

<h3>Dashboard</h3>
```

### When to Use Each Render Mode:
- `InteractiveServer`: Real-time dashboard, live updates (our default)
- `InteractiveWebAssembly`: Offline analysis (future sprint)
- `InteractiveAuto`: Hybrid approach (not used in MVP)

## Component File Structure

### .razor File Structure
✅ **CORRECT ORDER**:
```razor
@page "/developers"
@rendermode InteractiveServer

@* Usings *@
@using DevMetricsPro.Application.DTOs
@using DevMetricsPro.Application.Interfaces

@* Injected Services *@
@inject IDeveloperService DeveloperService
@inject ILogger<Developers> Logger

@* HTML Markup *@
<PageTitle>Developers - DevMetrics Pro</PageTitle>

<MudText Typo="Typo.h4" Class="mb-4">Developers</MudText>

@if (_isLoading)
{
    <MudProgressCircular Indeterminate="true" />
}
else
{
    <MudGrid>
        @foreach (var developer in _developers)
        {
            <MudItem xs="12" sm="6" md="4">
                <DeveloperCard Developer="@developer" />
            </MudItem>
        }
    </MudGrid>
}

@* Code Block *@
@code {
    private bool _isLoading = true;
    private List<DeveloperDto> _developers = new();

    protected override async Task OnInitializedAsync()
    {
        await LoadDevelopersAsync();
    }

    private async Task LoadDevelopersAsync()
    {
        _isLoading = true;
        try
        {
            _developers = await DeveloperService.GetAllDevelopersAsync();
        }
        finally
        {
            _isLoading = false;
        }
    }
}
```

## Component Parameters

### Defining Parameters
✅ **Use `[Parameter]` attribute**:
```razor
@code {
    [Parameter]
    public required DeveloperDto Developer { get; set; }
    
    [Parameter]
    public EventCallback<Guid> OnDeleteClick { get; set; }
    
    [Parameter]
    public string? CssClass { get; set; }
}
```

### Parameter Validation
✅ **Validate required parameters**:
```razor
@code {
    [Parameter]
    public required DeveloperDto Developer { get; set; }
    
    protected override void OnParametersSet()
    {
        if (Developer is null)
        {
            throw new ArgumentNullException(nameof(Developer));
        }
    }
}
```

## Lifecycle Methods

### Order of Execution
1. `SetParametersAsync`
2. `OnInitialized` / `OnInitializedAsync`
3. `OnParametersSet` / `OnParametersSetAsync`
4. `OnAfterRender` / `OnAfterRenderAsync`

### When to Use Each:
```razor
@code {
    // Load data once when component initializes
    protected override async Task OnInitializedAsync()
    {
        _data = await LoadDataAsync();
    }
    
    // React to parameter changes
    protected override async Task OnParametersSetAsync()
    {
        if (DeveloperId != _previousDeveloperId)
        {
            await LoadDeveloperAsync(DeveloperId);
            _previousDeveloperId = DeveloperId;
        }
    }
    
    // Access JavaScript or DOM (runs after render)
    protected override async Task OnAfterRenderAsync(bool firstRender)
    {
        if (firstRender)
        {
            await JSRuntime.InvokeVoidAsync("initializeChart");
        }
    }
}
```

## State Management

### Component State
✅ **Private fields for component state**:
```razor
@code {
    private bool _isLoading;
    private string _searchText = string.Empty;
    private List<DeveloperDto> _developers = new();
    private DeveloperDto? _selectedDeveloper;
}
```

### Trigger Re-render
✅ **Call `StateHasChanged()` when needed**:
```razor
@code {
    private async Task LoadDataAsync()
    {
        _isLoading = true;
        StateHasChanged(); // Force re-render to show spinner
        
        _data = await Service.GetDataAsync();
        
        _isLoading = false;
        // StateHasChanged() called automatically after async method
    }
}
```

### When to Call StateHasChanged():
- After updating state in async callbacks
- When updating state from background threads
- When state changes outside component lifecycle

## Event Handling

### Button Click Events
✅ **Use async event handlers**:
```razor
<MudButton OnClick="HandleDeleteAsync" Color="Color.Error">
    Delete
</MudButton>

@code {
    private async Task HandleDeleteAsync()
    {
        var confirmed = await DialogService.ShowMessageBox(
            "Confirm Delete",
            "Are you sure?",
            yesText: "Delete", cancelText: "Cancel");
            
        if (confirmed == true)
        {
            await DeveloperService.DeleteAsync(Developer.Id);
            await OnDeleteClick.InvokeAsync(Developer.Id);
        }
    }
}
```

### EventCallback
✅ **Use EventCallback for parent-child communication**:
```razor
@* Child Component *@
<MudButton OnClick="NotifyParent">Click Me</MudButton>

@code {
    [Parameter]
    public EventCallback<string> OnButtonClick { get; set; }
    
    private async Task NotifyParent()
    {
        await OnButtonClick.InvokeAsync("Button was clicked!");
    }
}

@* Parent Component *@
<ChildComponent OnButtonClick="HandleChildClick" />

@code {
    private void HandleChildClick(string message)
    {
        Logger.LogInformation("Child said: {Message}", message);
    }
}
```

## Dependency Injection

### Service Injection
✅ **Inject services at component level**:
```razor
@inject IDeveloperService DeveloperService
@inject ILogger<DeveloperList> Logger
@inject ISnackbar Snackbar
@inject NavigationManager Navigation
```

### Custom Services
✅ **Create component-specific services**:
```csharp
// Register in Program.cs
builder.Services.AddScoped<MetricCalculationService>();

// Inject in component
@inject MetricCalculationService MetricService
```

## Error Handling

### Try-Catch in Components
✅ **Handle errors gracefully**:
```razor
@code {
    private string? _errorMessage;
    
    private async Task LoadDataAsync()
    {
        _isLoading = true;
        _errorMessage = null;
        
        try
        {
            _data = await Service.GetDataAsync();
        }
        catch (Exception ex)
        {
            _errorMessage = "Failed to load data. Please try again.";
            Logger.LogError(ex, "Error loading data");
            Snackbar.Add(_errorMessage, Severity.Error);
        }
        finally
        {
            _isLoading = false;
        }
    }
}
```

### Error Boundaries
✅ **Use ErrorBoundary for unhandled errors**:
```razor
<ErrorBoundary>
    <ChildContent>
        <DashboardContent />
    </ChildContent>
    <ErrorContent Context="ex">
        <div class="alert alert-danger">
            <h4>An error occurred</h4>
            <p>@ex.Message</p>
        </div>
    </ErrorContent>
</ErrorBoundary>
```

## Performance Optimization

### Avoid Unnecessary Re-renders
✅ **Use `ShouldRender()` to prevent re-renders**:
```razor
@code {
    private int _counter;
    
    protected override bool ShouldRender()
    {
        // Only re-render when counter is even
        return _counter % 2 == 0;
    }
}
```

### Virtualization for Large Lists
✅ **Use Virtualize for large datasets**:
```razor
<Virtualize Items="@_developers" Context="developer">
    <DeveloperCard Developer="@developer" />
</Virtualize>
```

### Avoid Inline Lambdas in Loops
❌ **DON'T**:
```razor
@foreach (var item in items)
{
    <MudButton OnClick="@(() => DeleteItem(item))">Delete</MudButton>
}
```

✅ **DO**:
```razor
@foreach (var item in items)
{
    var currentItem = item; // Capture variable
    <MudButton OnClick="@(() => DeleteItem(currentItem))">Delete</MudButton>
}
```

Or better, use a method:
```razor
@foreach (var item in items)
{
    <MudButton OnClick="@(_ => HandleDelete(item))">Delete</MudButton>
}

@code {
    private async Task HandleDelete(Developer developer)
    {
        await DeleteItem(developer);
    }
}
```

## MudBlazor Conventions

### Component Usage
✅ **Use MudBlazor consistently**:
```razor
@* Cards *@
<MudCard Elevation="2">
    <MudCardHeader>
        <CardHeaderContent>
            <MudText Typo="Typo.h6">@Title</MudText>
        </CardHeaderContent>
    </MudCardHeader>
    <MudCardContent>
        @* Content *@
    </MudCardContent>
</MudCard>

@* Buttons *@
<MudButton Variant="Variant.Filled" Color="Color.Primary" OnClick="HandleClick">
    Save
</MudButton>

@* Forms *@
<MudTextField @bind-Value="_email" Label="Email" Variant="Variant.Outlined" />
```

### Snackbar for Notifications
✅ **Use Snackbar for user feedback**:
```razor
@inject ISnackbar Snackbar

@code {
    private async Task SaveAsync()
    {
        try
        {
            await Service.SaveAsync();
            Snackbar.Add("Saved successfully!", Severity.Success);
        }
        catch (Exception ex)
        {
            Snackbar.Add("Failed to save", Severity.Error);
        }
    }
}
```

## SignalR for Real-time Updates

### Hub Connection
✅ **Connect to SignalR hub**:
```razor
@implements IAsyncDisposable
@inject NavigationManager Navigation

@code {
    private HubConnection? _hubConnection;
    
    protected override async Task OnInitializedAsync()
    {
        _hubConnection = new HubConnectionBuilder()
            .WithUrl(Navigation.ToAbsoluteUri("/metricshub"))
            .WithAutomaticReconnect()
            .Build();
            
        _hubConnection.On<MetricUpdate>("ReceiveMetricUpdate", HandleMetricUpdate);
        
        await _hubConnection.StartAsync();
    }
    
    private void HandleMetricUpdate(MetricUpdate update)
    {
        // Update component state
        _latestMetric = update;
        StateHasChanged();
    }
    
    public async ValueTask DisposeAsync()
    {
        if (_hubConnection is not null)
        {
            await _hubConnection.DisposeAsync();
        }
    }
}
```

## Component Organization Best Practices

### Small, Focused Components
✅ Break large components into smaller ones:
```razor
@* DashboardPage.razor *@
<PageTitle>Dashboard</PageTitle>

<DashboardHeader />
<StatsCards Metrics="@_metrics" />
<ActivitySection Activities="@_activities" />
<LeaderboardSection Developers="@_topDevelopers" />
```

### Shared Components
✅ Create reusable components in `Components/Shared/`:
```razor
@* Components/Shared/LoadingSpinner.razor *@
<div class="d-flex justify-center my-4">
    <MudProgressCircular Indeterminate="true" Size="Size.Large" />
</div>

@* Usage *@
@if (_isLoading)
{
    <LoadingSpinner />
}
```

## Routing

### Page Routes
✅ **Define routes clearly**:
```razor
@page "/developers"
@page "/developers/{DeveloperId:guid}"

@code {
    [Parameter]
    public Guid? DeveloperId { get; set; }
}
```

### Navigation
✅ **Use NavigationManager for programmatic navigation**:
```razor
@inject NavigationManager Navigation

@code {
    private void NavigateToDeveloper(Guid id)
    {
        Navigation.NavigateTo($"/developers/{id}");
    }
}
```

## CSS and Styling

### Component-Scoped CSS
✅ **Use .razor.css for component-specific styles**:
```
DeveloperCard.razor
DeveloperCard.razor.css
```

```css
/* DeveloperCard.razor.css */
.developer-card {
    transition: transform 0.2s;
}

.developer-card:hover {
    transform: translateY(-4px);
}
```

### MudBlazor Classes
✅ **Use MudBlazor utility classes**:
```razor
<div class="d-flex justify-space-between align-center mb-4">
    <MudText Typo="Typo.h4">Dashboard</MudText>
    <MudButton Color="Color.Primary">Action</MudButton>
</div>
```

## Common Patterns

### Loading State Pattern
```razor
@if (_isLoading)
{
    <LoadingSpinner />
}
else if (_errorMessage is not null)
{
    <ErrorMessage Message="@_errorMessage" />
}
else if (!_data.Any())
{
    <EmptyState Message="No data available" />
}
else
{
    @* Render data *@
}
```

### Form Validation Pattern
```razor
<EditForm Model="@_model" OnValidSubmit="HandleValidSubmit">
    <DataAnnotationsValidator />
    <MudTextField @bind-Value="_model.Email" 
                  Label="Email" 
                  For="@(() => _model.Email)" />
    <ValidationSummary />
    <MudButton ButtonType="ButtonType.Submit">Submit</MudButton>
</EditForm>
```

## Anti-Patterns to Avoid

❌ **DON'T** call StateHasChanged() unnecessarily
❌ **DON'T** put business logic in components (use services)
❌ **DON'T** create large monolithic components
❌ **DON'T** forget to dispose of resources (IAsyncDisposable)
❌ **DON'T** use synchronous APIs (use async/await)
❌ **DON'T** hardcode URLs or configuration values

## Quick Checklist

Before committing Blazor components:
- [ ] Component is focused and single-responsibility
- [ ] Uses InteractiveServer render mode
- [ ] All injected services are needed
- [ ] Error handling in place
- [ ] Loading states handled
- [ ] EventCallbacks used for parent communication
- [ ] Implements IAsyncDisposable if using resources
- [ ] No business logic (delegated to services)
- [ ] Consistent with MudBlazor design system
