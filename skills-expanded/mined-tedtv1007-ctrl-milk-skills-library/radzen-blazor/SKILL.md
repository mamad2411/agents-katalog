---
name: radzen-blazor
description: >
  Guide for using Radzen Blazor component library (Radzen.Blazor NuGet package) in Blazor applications.
  Use when building Blazor apps with Radzen components: RadzenDataGrid, RadzenCard, RadzenButton,
  RadzenDialog, RadzenNotification, RadzenPanelMenu, RadzenStack, RadzenBadge, RadzenText,
  RadzenProgressBar, RadzenTextBox, RadzenIcon, or any component prefixed with "Radzen".
  Also use when troubleshooting theming, layout, service registration, or E2E testing selectors.
---

# Radzen Blazor Skill

Production-tested patterns for the **Radzen.Blazor** component library in .NET Blazor apps.

## Setup Checklist

### 1. NuGet Package
```xml
<!-- Both server and client .csproj if using InteractiveAuto -->
<PackageReference Include="Radzen.Blazor" Version="8.0.0" />
```

### 2. Service Registration
```csharp
// Server Program.cs AND Client Program.cs
using Radzen;
builder.Services.AddRadzenComponents();
```

### 3. _Imports.razor (both server + client)
```razor
@using Radzen
@using Radzen.Blazor
```

### 4. App.razor References
```html
<head>
  <!-- Pick ONE theme: material-base, material-dark, default-base, software-base, humanistic-base, standard-base -->
  <link rel="stylesheet" href="_content/Radzen.Blazor/css/material-base.css" />
  <link rel="stylesheet" href="app.css" />
</head>
<body>
  <Routes />
  <!-- Radzen JS MUST come BEFORE blazor.web.js -->
  <script src="_content/Radzen.Blazor/Radzen.Blazor.js"></script>
  <script src="_framework/blazor.web.js"></script>
</body>
```

### 5. Global Service Components (MainLayout.razor)
Place these once inside `<RadzenLayout>`:
```razor
<RadzenNotification />
<RadzenDialog />
<RadzenTooltip />
<RadzenContextMenu />
```

## Component Reference

### Layout
| Component | Purpose | Key Parameters |
|-----------|---------|----------------|
| `RadzenLayout` | Root layout shell | — |
| `RadzenHeader` | Fixed top header | `class` |
| `RadzenSidebar` | Side navigation panel | `class`, `Style` |
| `RadzenBody` | Main content area | — |
| `RadzenStack` | Flex container (most-used) | `Orientation`, `AlignItems`, `JustifyContent`, `Gap` |
| `RadzenRow` | CSS grid row | `Gap` |
| `RadzenColumn` | CSS grid column | `SizeSM`, `SizeMD`, `SizeLG` (1-12 grid) |

### Data Display
| Component | Purpose | Key Parameters |
|-----------|---------|----------------|
| `RadzenDataGrid<TItem>` | Data table | `Data`, `TItem`, `AllowSorting`, `AllowPaging`, `PageSize` |
| `RadzenDataGridColumn<TItem>` | Grid column | `Title`, `Property`, `Width`, `<Template>` |
| `RadzenCard` | Card container | `Style` |
| `RadzenBadge` | Status chip | `Text`, `BadgeStyle` (Success, Danger, Warning, Info, Light) |
| `RadzenText` | Typography | `TextStyle` (H3, H4, H6, Body1, Caption, Overline) |
| `RadzenIcon` | Material icon | `Icon` (material icon name string) |
| `RadzenProgressBar` | Linear progress | `Value`, `Max`, `ShowValue` |
| `RadzenProgressBarCircular` | Circular spinner | `Mode` (Indeterminate), `ShowValue` |

### Input & Actions
| Component | Purpose | Key Parameters |
|-----------|---------|----------------|
| `RadzenButton` | Clickable button | `Text`, `Icon`, `ButtonStyle`, `Size`, `Click` |
| `RadzenTextBox` | Text input | `@bind-Value`, `Placeholder`, `Change` |
| `RadzenPanelMenu` | Navigation menu | `Style` |
| `RadzenPanelMenuItem` | Menu item | `Text`, `Path`, `Icon` |

### ButtonStyle Enum
```
ButtonStyle.Primary | ButtonStyle.Secondary | ButtonStyle.Light | ButtonStyle.Danger | ButtonStyle.Warning | ButtonStyle.Info | ButtonStyle.Success | ButtonStyle.Dark
```

### BadgeStyle Enum
```
BadgeStyle.Success | BadgeStyle.Danger | BadgeStyle.Warning | BadgeStyle.Info | BadgeStyle.Light | BadgeStyle.Primary | BadgeStyle.Secondary
```

## Patterns

### Async Data Loading
```razor
@if (data == null)
{
    <RadzenProgressBarCircular ShowValue="false" Mode="ProgressBarMode.Indeterminate" />
}
else
{
    <!-- Render data -->
}
```

### DataGrid with Custom Templates
```razor
<RadzenDataGrid Data="@items" TItem="MyModel" AllowSorting="true">
    <Columns>
        <RadzenDataGridColumn TItem="MyModel" Property="Name" Title="Name" Width="200px" />
        <RadzenDataGridColumn TItem="MyModel" Title="Status" Width="100px">
            <Template Context="item">
                <RadzenBadge Text="@item.Status" BadgeStyle="@GetBadgeStyle(item)" />
            </Template>
        </RadzenDataGridColumn>
    </Columns>
</RadzenDataGrid>
```

### Responsive Grid (Stat Cards)
```razor
<RadzenRow Gap="1rem">
    <RadzenColumn SizeSM="6" SizeLG="3">
        <RadzenCard Style="padding: 1.25rem;">
            <RadzenStack Gap="0.5rem">
                <RadzenIcon Icon="lock" Style="color: var(--rz-primary);" />
                <RadzenText TextStyle="TextStyle.Overline">Label</RadzenText>
                <RadzenText TextStyle="TextStyle.H3">@value</RadzenText>
            </RadzenStack>
        </RadzenCard>
    </RadzenColumn>
</RadzenRow>
```

### Search/Filter Pattern
```razor
<RadzenTextBox @bind-Value="searchTerm" Placeholder="Search..." Change="@OnSearchChanged" />

@code {
    private string searchTerm = "";
    private IEnumerable<T>? filtered => items?.Where(i =>
        string.IsNullOrWhiteSpace(searchTerm) ||
        i.Name.Contains(searchTerm, StringComparison.OrdinalIgnoreCase));
    private void OnSearchChanged() => StateHasChanged();
}
```

### Navigation Menu
```razor
<RadzenPanelMenu Style="width: 250px;">
    <RadzenPanelMenuItem Text="Dashboard" Path="/" Icon="dashboard" />
    <RadzenPanelMenuItem Text="Certificates" Path="/certificates" Icon="lock" />
</RadzenPanelMenu>
```

### Button Click Handling
```razor
<!-- Use Click, NOT @onclick -->
<RadzenButton Text="Refresh" Icon="sync" ButtonStyle="ButtonStyle.Secondary" Click="@HandleRefresh" />

@code {
    private async Task HandleRefresh() { /* ... */ }
}
```

## Theming

### Available Themes
- `material-base.css` — Material Design (light)
- `material-dark-base.css` — Material Dark
- `default-base.css` — Radzen Default
- `software-base.css` — Software
- `humanistic-base.css` — Humanistic
- `standard-base.css` — Standard

### Radzen CSS Variables (material theme)
```css
--rz-primary      /* Brand primary color */
--rz-success      /* Green / positive */
--rz-warning      /* Orange / caution */
--rz-danger       /* Red / error */
--rz-info         /* Blue / informational */
--rz-border-radius /* Default border radius */
```

### Custom Override Pattern
```css
:root {
    --app-bg-1: #f7fafc;
    --card-bg: #ffffff;
    --card-border: #e6eef9;
}
.rz-card {
    border: 1px solid var(--card-border);
    box-shadow: 0 2px 8px rgba(15,23,42,0.04);
}
```

## E2E Testing Selectors (Playwright)

Radzen renders **standard HTML elements** — no shadow DOM. Use CSS selectors directly.

### Selector Cheat Sheet
| Radzen Component | CSS Selector | Notes |
|------------------|-------------|-------|
| RadzenCard | `.rz-card` | Standard div |
| RadzenBadge | `.rz-badge` | Span with text |
| RadzenButton | `.rz-button` | Standard button |
| RadzenDataGrid | `.rz-data-grid` | Table-based |
| Grid rows | `.rz-data-grid tbody tr` | Data rows only |
| Grid header | `.rz-data-grid thead th` | Column headers |
| RadzenTextBox | `.rz-textbox` | Standard input |
| RadzenPanelMenu | `.rz-nav-menu` | Navigation wrapper |
| RadzenHeader | `.rz-header` | App header |
| RadzenSidebar | `.rz-sidebar` | Sidebar panel |
| RadzenProgressBar | `.rz-progressbar` | Progress indicator |
| Badge variants | `.rz-badge-success`, `.rz-badge-danger` etc. | Status colors |

### Playwright Best Practices
```csharp
// Prefer role and text selectors over CSS when possible
await Expect(Page.GetByRole(AriaRole.Heading, new() { Name = "Dashboard" })).ToBeVisibleAsync();

// Text-based (good for badges and labels)
await Expect(Page.GetByText("PQC READY", new() { Exact = true })).ToBeVisibleAsync();

// Placeholder-based (good for inputs)
var search = Page.GetByPlaceholder("Search CN, Thumbprint...");
await search.FillAsync("internal");

// CSS selector for counting elements
var rows = Page.Locator(".rz-data-grid tbody tr");
var count = await rows.CountAsync();

// CAUTION: Radzen <RadzenIcon> renders icon name as inner text of <i> element
// GetByText("Dashboard") may match icon <i>dashboard</i> — use GetByRole(Heading) instead
```

### Strict Mode Gotcha
Radzen `RadzenIcon Icon="dashboard"` renders `<i class="rzi">dashboard</i>`. The icon name becomes text content. `GetByText("Dashboard")` will match both the icon and the heading. Always use:
```csharp
// ❌ Ambiguous — matches icon + heading
Page.GetByText("Dashboard")

// ✅ Specific — matches only heading
Page.GetByRole(AriaRole.Heading, new() { Name = "Dashboard" })
```

## Migration from FluentUI Blazor

### Package Changes
```diff
- <PackageReference Include="Microsoft.FluentUI.AspNetCore.Components" Version="4.11.3" />
- <PackageReference Include="Microsoft.FluentUI.AspNetCore.Components.Icons" Version="4.11.3" />
+ <PackageReference Include="Radzen.Blazor" Version="8.0.0" />
```

### Service Registration
```diff
- builder.Services.AddFluentUIComponents();
+ builder.Services.AddRadzenComponents();
```

### Component Mapping
| FluentUI | Radzen |
|----------|--------|
| `FluentLayout` | `RadzenLayout` |
| `FluentHeader` | `RadzenHeader` |
| `FluentBodyContent` | `RadzenBody` |
| `FluentNavMenu` | `RadzenPanelMenu` |
| `FluentNavLink` | `RadzenPanelMenuItem` |
| `FluentDataGrid` | `RadzenDataGrid` |
| `FluentButton` | `RadzenButton` |
| `FluentBadge` | `RadzenBadge` |
| `FluentCard` | `RadzenCard` |
| `FluentTextField` | `RadzenTextBox` |
| `FluentSearch` | `RadzenTextBox` (with placeholder) |
| `FluentProgressRing` | `RadzenProgressBarCircular` |
| `FluentStack` | `RadzenStack` |
| `FluentIcon` | `RadzenIcon` |

### E2E Selector Migration
| FluentUI selector | Radzen selector |
|-------------------|-----------------|
| `fluent-card` (shadow DOM) | `.rz-card` (standard CSS) |
| `fluent-data-grid-row` | `.rz-data-grid tbody tr` |
| `fluent-badge` | `.rz-badge` |
| `fluent-button` | `.rz-button` |
| `fluent-search` (shadow DOM JS eval) | `Page.GetByPlaceholder(...)` |
| `fluent-anchor` | `a.quick-action-link` or `RadzenButton` |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Components don't render | Verify `AddRadzenComponents()` in BOTH Program.cs files |
| JS interop error | Ensure `Radzen.Blazor.js` loads BEFORE `blazor.web.js` |
| Missing styles | Check theme CSS link in App.razor `<head>` |
| Icons not showing | Use Material Design icon names (lowercase, underscored): `dashboard`, `lock`, `rocket_launch` |
| Dialog/Toast not working | Add `<RadzenDialog />` and `<RadzenNotification />` in MainLayout |
| DataGrid empty | Ensure `Data` parameter is set and `TItem` matches the collection type |
| Badge unstyled | Use `BadgeStyle` enum, not string: `BadgeStyle.Success` not `"success"` |
