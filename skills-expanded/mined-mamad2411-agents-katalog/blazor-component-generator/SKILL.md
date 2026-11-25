---
name: blazor-component-generator
description: 'Generate Blazor components following .NET 8+ conventions: code-behind pattern, parameters, EventCallback, lifecycle methods, RenderFragment, form validation, CSS isolation, and disposal.'
---

# Blazor Component Generator

Your goal is to generate well-structured Blazor components following .NET 8+ best practices.

## Component File Pair (Preferred Pattern)

Prefer the **code-behind pattern** for components with non-trivial logic:

**`MyComponent.razor`** — markup only:

```razor
@inherits MyComponentBase

<div class="my-component">
    <h3>@Title</h3>
    <p>@Description</p>
    <button @onclick="HandleClick" disabled="@IsLoading">
        @(IsLoading ? "Loading…" : "Submit")
    </button>
</div>
```

**`MyComponent.razor.cs`** — logic only:

```csharp
namespace YourApp.Components;

public partial class MyComponent : ComponentBase, IAsyncDisposable
{
    [Parameter] public string Title { get; set; } = string.Empty;
    [Parameter] public string Description { get; set; } = string.Empty;
    [Parameter] public EventCallback<string> OnSubmit { get; set; }

    [Inject] private IMyService MyService { get; set; } = default!;

    private bool IsLoading { get; set; }

    protected override async Task OnInitializedAsync()
    {
        IsLoading = true;
        try
        {
            await MyService.LoadAsync();
        }
        finally
        {
            IsLoading = false;
        }
    }

    private async Task HandleClick()
    {
        IsLoading = true;
        try
        {
            await OnSubmit.InvokeAsync(Title);
        }
        finally
        {
            IsLoading = false;
        }
    }

    public async ValueTask DisposeAsync()
    {
        await MyService.DisposeAsync();
    }
}
```

## Parameters

| Attribute | Use When |
|-----------|----------|
| `[Parameter]` | Direct parent-to-child value |
| `[Parameter] public RenderFragment? ChildContent` | Allow arbitrary child markup |
| `[Parameter] public RenderFragment<T>? ItemTemplate` | Templated child with context |
| `[CascadingParameter]` | Theme, auth state, form context — cross-cutting concerns only |
| `[SupplyParameterFromQuery]` | Bind from URL query string (`?id=5`) |
| `[SupplyParameterFromForm]` | Bind from form POST (SSR forms) |

### EventCallback vs Action

Always use `EventCallback<T>` (not `Action<T>`) for component events:

```csharp
// ✅ Correct — triggers StateHasChanged in parent automatically
[Parameter] public EventCallback<int> OnItemSelected { get; set; }

// ❌ Avoid — parent must call StateHasChanged manually
[Parameter] public Action<int>? OnItemSelected { get; set; }
```

## Lifecycle Methods

```csharp
// Called once on first render — use for data loading
protected override async Task OnInitializedAsync()
{
    data = await DataService.GetAsync();
}

// Called when parameters change — use when re-fetching based on parameter values
protected override async Task OnParametersSetAsync()
{
    if (Id != _previousId)
    {
        _previousId = Id;
        data = await DataService.GetByIdAsync(Id);
    }
}

// Called after render — use for JS interop (only safe place)
protected override async Task OnAfterRenderAsync(bool firstRender)
{
    if (firstRender)
    {
        await JsRuntime.InvokeVoidAsync("initChart", _chartRef);
    }
}
```

## List Rendering with @key

Always add `@key` to list-rendered components to help the diffing algorithm:

```razor
@foreach (var item in Items)
{
    <ItemCard @key="item.Id" Item="item" OnDelete="HandleDelete" />
}
```

## Templated Component (RenderFragment\<T\>)

```razor
@typeparam TItem

<ul>
    @foreach (var item in Items)
    {
        <li @key="item">@ItemTemplate(item)</li>
    }
</ul>

@code {
    [Parameter, EditorRequired] public IReadOnlyList<TItem> Items { get; set; } = [];
    [Parameter, EditorRequired] public RenderFragment<TItem> ItemTemplate { get; set; } = default!;
}
```

## Form Handling (EditForm)

```razor
<EditForm Model="formModel" OnValidSubmit="HandleValidSubmit" FormName="MyForm">
    <DataAnnotationsValidator />
    <ValidationSummary />

    <div class="mb-3">
        <label for="name">Name</label>
        <InputText id="name" class="form-control" @bind-Value="formModel.Name" />
        <ValidationMessage For="@(() => formModel.Name)" />
    </div>

    <button type="submit" class="btn btn-primary">Save</button>
</EditForm>

@code {
    private MyFormModel formModel = new();

    private async Task HandleValidSubmit()
    {
        await SaveService.SaveAsync(formModel);
    }
}
```

Model with validation:

```csharp
public class MyFormModel
{
    [Required(ErrorMessage = "Name is required")]
    [StringLength(100, MinimumLength = 2)]
    public string Name { get; set; } = string.Empty;

    [EmailAddress]
    public string? Email { get; set; }
}
```

## CSS Isolation

Create `MyComponent.razor.css` alongside the component:

```css
/* Scoped to this component only — no class prefixing needed */
.my-component {
    padding: 1rem;
    border: 1px solid var(--bs-border-color);
    border-radius: var(--bs-border-radius);
}

button {
    min-width: 120px;
}
```

## Disposal Pattern

Implement `IAsyncDisposable` whenever the component:
- Subscribes to `NavigationManager.LocationChanged`
- Subscribes to any .NET event
- Creates a timer (`PeriodicTimer`, `System.Timers.Timer`)
- Holds a JS object reference (`IJSObjectReference`)

```csharp
public partial class MyComponent : ComponentBase, IAsyncDisposable
{
    [Inject] private NavigationManager Nav { get; set; } = default!;

    protected override void OnInitialized()
    {
        Nav.LocationChanged += HandleLocationChanged;
    }

    private void HandleLocationChanged(object? sender, LocationChangedEventArgs e)
    {
        // handle navigation
        StateHasChanged();
    }

    public ValueTask DisposeAsync()
    {
        Nav.LocationChanged -= HandleLocationChanged;
        return ValueTask.CompletedTask;
    }
}
```

## Checklist

- [ ] Non-trivial logic lives in `.razor.cs` code-behind, not inline `@code`
- [ ] `partial class` matches the `.razor` file name exactly
- [ ] `IAsyncDisposable` implemented if subscribed to any event or timer
- [ ] `EventCallback<T>` used instead of `Action<T>` for component events
- [ ] `@key` used on all `@foreach` rendered components
- [ ] `[EditorRequired]` on mandatory parameters to catch missing values at design time
- [ ] CSS isolation file created alongside component
- [ ] No synchronous blocking calls in lifecycle methods
