---
name: syncfusion-aspnetcore-circulargauge
description: Creating and customizing Syncfusion Circular Gauge - a circular data visualization component for displaying numeric values. ALWAYS use this skill when users need to implement circular gauges, display metrics on a circular scale, configure gauge axes, add pointers or ranges, create data visualization gauges, customize gauge appearance, handle user interactions with gauges, or build dashboards with circular gauge components.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion Circular Gauge

- [When to Use This Skill](#when-to-use-this-skill)
- [Component Overview](#component-overview)
- [Documentation and Navigation Guide](#documentation-and-navigation-guide)
  - [Getting Started with Circular Gauge](#getting-started-with-circular-gauge)
  - [Configuring Gauge Axes](#configuring-gauge-axes)
  - [Working with Pointers](#working-with-pointers)
  - [Adding and Customizing Ranges](#adding-and-customizing-ranges)
  - [Annotations and Custom Content](#annotations-and-custom-content)
  - [Gauge Appearance and Styling](#gauge-appearance-and-styling)
  - [User Interactions](#user-interactions)
  - [Internationalization and Localization](#internationalization-and-localization)
  - [Export and Print Functionality](#export-and-print-functionality)
  - [Accessibility and WCAG Compliance](#accessibility-and-wcag-compliance)
  - [Sizing and Dimensions](#sizing-and-dimensions)
- [Quick Start Example](#quick-start-example)
  - [Pages/_ViewImports.cshtml](#pages_viewimportscshtml)
  - [Pages/Shared/_Layout.cshtml](#pagesshared_layoutcshtml)
  - [Pages/Index.cshtml.cs](#pagesindexcshtmlcs)
  - [Pages/Index.cshtml](#pagesindexcshtml)
- [Common Patterns](#common-patterns)
  - [Pattern 1: Dashboard with Multiple Gauges](#pattern-1-dashboard-with-multiple-gauges)
  - [Pattern 2: Interactive Gauge with Drag](#pattern-2-interactive-gauge-with-drag)
  - [Pattern 3: Gauge with Ranges and Alerts](#pattern-3-gauge-with-ranges-and-alerts)
  - [Pattern 4: Localized Gauge](#pattern-4-localized-gauge)
- [Key Props and Configuration](#key-props-and-configuration)
- [Common Use Cases](#common-use-cases)
- [Next Steps](#next-steps)
- [Combined Mistakes and Future References](#combined-mistakes-and-future-references)

## When to Use This Skill

Use this skill whenever a user needs to:

- Create or implement a Syncfusion Circular Gauge component in an ASP.NET Core Razor Pages application.
- Display numeric values on a circular scale.
- Configure gauge axes, pointers, and ranges.
- Customize gauge appearance by using component properties.
- Add interactivity such as tooltips, pointer drag-and-drop, and event handlers.
- Export or print gauge content when export and print modules are required.
- Support international locales and right-to-left rendering.
- Implement accessible gauge visualizations.
- Build dashboard-style data visualizations with one or more Circular Gauge components.

## Component Overview

The Circular Gauge is a data visualization component used to display numeric values on a circular scale. It is suitable for dashboards, status indicators, monitoring screens, and KPI visualizations.

All gauge elements are rendered using SVG, which makes the component scalable and suitable for responsive layouts.

Key features include:

- Multiple pointers such as needle, marker, and range bar pointers.
- Multiple axes with independent minimum, maximum, radius, ticks, labels, ranges, and pointers.
- Customizable ranges for categorizing value zones.
- Annotations for placing custom text or visual content inside the gauge.
- User interactions such as tooltip display and pointer dragging.
- Export and print support when the required export or print settings are enabled.
- Internationalization support for localized number display.
- Right-to-left rendering support.
- Accessibility support through proper component rendering and assistive descriptions.

## Documentation and Navigation Guide

### Getting Started with Circular Gauge

Read this topic when you need to set up the Circular Gauge for the first time in an ASP.NET Core Razor Pages application.

Covered areas:

- Installing the latest `Syncfusion.EJ2.AspNet.Core` NuGet package.
- Configuring `_ViewImports.cshtml`.
- Adding the Syncfusion script reference in `_Layout.cshtml`.
- Registering the Syncfusion script manager.
- Creating the first Circular Gauge in `Index.cshtml`.
- Passing gauge values from `Index.cshtml.cs`.

### Configuring Gauge Axes

Read this topic when you need to configure the gauge scale.

Covered areas:

- Axis minimum and maximum values.
- Start and end angles.
- Axis radius in percentage or pixel values.
- Axis direction.
- Major ticks and minor ticks.
- Label positioning and formatting.
- Multiple axes in a single Circular Gauge.

### Working with Pointers

Read this topic when you need to display values on the gauge.

Covered areas:

- Needle pointer configuration.
- Marker pointer configuration.
- Range bar pointer configuration.
- Multiple pointers on the same axis.
- Pointer radius and pointer width.
- Pointer animation.
- Pointer drag behavior.

### Adding and Customizing Ranges

Read this topic when you need to visually divide the gauge into meaningful zones.

Covered areas:

- Creating one or more ranges.
- Setting range start and end values.
- Customizing range color.
- Setting range radius.
- Setting range start width and end width.
- Creating warning, danger, and success zones.
- Supporting interactive range drag when needed.

### Annotations and Custom Content

Read this topic when you need to place additional content inside or around the gauge.

Covered areas:

- Adding text annotations.
- Positioning annotations using angle and radius.
- Displaying dynamic values in the center of the gauge.
- Placing custom HTML content.
- Creating dashboard labels and value indicators.

### Gauge Appearance and Styling

Read this topic when you need to modify the visual appearance using Circular Gauge properties.

Covered areas:

- Gauge title.
- Title style.
- Gauge background.
- Border settings.
- Center position using `centerX` and `centerY`.
- Width and height.
- Margin configuration.
- Semi-circular and quarter-circular gauge layouts.

### User Interactions

Read this topic when you need to make the gauge interactive.

Covered areas:

- Enabling tooltips.
- Customizing tooltip content.
- Enabling pointer drag.
- Handling drag start, drag move, and drag end events.
- Updating values interactively.
- Handling mouse events.

### Internationalization and Localization

Read this topic when you need to display culture-specific gauge content.

Covered areas:

- Locale-based number formatting.
- Grouping separators.
- Currency or percentage formatting through label formatting.
- Right-to-left rendering.
- Locale-specific dashboard labels.

### Export and Print Functionality

Read this topic when you need to export or print the Circular Gauge.

Covered areas:

- Enabling print support.
- Enabling image export.
- Enabling PDF export.
- Exporting gauge content as image formats.
- Exporting gauge content as PDF.
- Printing the gauge from the browser.

### Accessibility and WCAG Compliance

Read this topic when you need to make the Circular Gauge easier to use with assistive technologies.

Covered areas:

- Description text for assistive technology.
- Keyboard focus behavior.
- Tab index configuration.
- Color contrast considerations.
- Meaningful title and labels.
- Avoiding color-only communication for critical values.

### Sizing and Dimensions

Read this topic when you need to control the rendered size of the gauge.

Covered areas:

- Setting width in pixels.
- Setting width in percentage.
- Setting height in pixels.
- Responsive container behavior.
- Axis radius relative to the gauge area.
- Preventing clipping in smaller containers.

## Quick Start Example

The following quick start uses a complete ASP.NET Core Razor Pages structure.

This example intentionally uses:

- No Syncfusion stylesheet link.
- No custom style block.
- No Syncfusion license registration content.
- No `@namespace` directive in `_ViewImports.cshtml`.
- A fully qualified model declaration in `Index.cshtml`.

Use the latest package version consistently in both the NuGet package and CDN script reference.

Install the NuGet package:

```powershell
Install-Package Syncfusion.EJ2.AspNet.Core -Version 33.2.7
```

Or install using .NET CLI:

```bash
dotnet add package Syncfusion.EJ2.AspNet.Core --version 33.2.7
```

### Pages/_ViewImports.cshtml

```html
@addTagHelper *, Microsoft.AspNetCore.Mvc.TagHelpers
@addTagHelper *, Syncfusion.EJ2
```

### Pages/Shared/_Layout.cshtml

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <title>@ViewData["Title"] - Circular Gauge Demo</title>

    <!-- Syncfusion ASP.NET Core controls script -->
    <script src="https://cdn.syncfusion.com/ej2/33.2.7/dist/ej2.min.js"></script>
</head>
<body>
    <header>
        <nav>
            <a asp-area="" asp-page="/Index">Circular Gauge Demo</a>
        </nav>
    </header>

    <main role="main">
        @RenderBody()
    </main>

    <!-- Syncfusion ASP.NET Core Script Manager -->
    <ejs-scripts></ejs-scripts>

    @await RenderSectionAsync("Scripts", required: false)
</body>
</html>
```

### Pages/Index.cshtml.cs

```csharp
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace CircularGaugeGettingStarted.Pages
{
    public class IndexModel : PageModel
    {
        public string GaugeTitle { get; set; } = "Speed";

        public double MinimumValue { get; set; } = 0;

        public double MaximumValue { get; set; } = 120;

        public double PointerValue { get; set; } = 70;

        public double SafeRangeStart { get; set; } = 0;

        public double SafeRangeEnd { get; set; } = 50;

        public double WarningRangeStart { get; set; } = 50;

        public double WarningRangeEnd { get; set; } = 80;

        public double DangerRangeStart { get; set; } = 80;

        public double DangerRangeEnd { get; set; } = 120;

        public void OnGet()
        {
        }
    }
}
```

### Pages/Index.cshtml

```html
@page
@model CircularGaugeGettingStarted.Pages.IndexModel

@{
    ViewData["Title"] = "Circular Gauge";
}

<h1>ASP.NET Core Circular Gauge</h1>
<p>Basic Circular Gauge with axis, pointer, and ranges.</p>

<ejs-circulargauge id="speedGauge"
                    title="@Model.GaugeTitle"
                    width="100%"
                    height="450px">
    <e-circulargauge-axes>
        <e-circulargauge-axis startAngle="240"
                              endAngle="120"
                              minimum="@Model.MinimumValue"
                              maximum="@Model.MaximumValue"
                              radius="90%">
            <e-circulargauge-ranges>
                <e-circulargauge-range start="@Model.SafeRangeStart"
                                       end="@Model.SafeRangeEnd"
                                       color="#30B32D"
                                       radius="80%">
                </e-circulargauge-range>
                <e-circulargauge-range start="@Model.WarningRangeStart"
                                       end="@Model.WarningRangeEnd"
                                       color="#FFDD00"
                                       radius="80%">
                </e-circulargauge-range>
                <e-circulargauge-range start="@Model.DangerRangeStart"
                                       end="@Model.DangerRangeEnd"
                                       color="#F03E3E"
                                       radius="80%">
                </e-circulargauge-range>
            </e-circulargauge-ranges>
            <e-circulargauge-pointers>
                <e-circulargauge-pointer value="@Model.PointerValue">
                </e-circulargauge-pointer>
            </e-circulargauge-pointers>
        </e-circulargauge-axis>
    </e-circulargauge-axes>
</ejs-circulargauge>
```

## Common Patterns

### Pattern 1: Dashboard with Multiple Gauges

Use this pattern when a dashboard needs to show multiple metrics such as speed, temperature, pressure, score, or utilization.

Implementation approach:

- Create separate `<ejs-circulargauge>` instances for each metric.
- Use unique `id` values for every gauge.
- Store values in `Index.cshtml.cs`.
- Bind each gauge title and pointer value from the page model.
- Keep gauge dimensions consistent for a clean dashboard layout.

Example model values:

```csharp
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace CircularGaugeGettingStarted.Pages
{
    public class IndexModel : PageModel
    {
        public double SpeedValue { get; set; } = 70;

        public double TemperatureValue { get; set; } = 45;

        public double PressureValue { get; set; } = 90;

        public void OnGet()
        {
        }
    }
}
```

Example `Index.cshtml` structure:

```html
@page
@model CircularGaugeGettingStarted.Pages.IndexModel

@{
    ViewData["Title"] = "Gauge Dashboard";
}

<h1>Gauge Dashboard</h1>

<ejs-circulargauge id="speedGauge" title="Speed" width="100%" height="300px">
    <e-circulargauge-axes>
        <e-circulargauge-axis minimum="0" maximum="120">
            <e-circulargauge-pointers>
                <e-circulargauge-pointer value="@Model.SpeedValue">
                </e-circulargauge-pointer>
            </e-circulargauge-pointers>
        </e-circulargauge-axis>
    </e-circulargauge-axes>
</ejs-circulargauge>

<ejs-circulargauge id="temperatureGauge" title="Temperature" width="100%" height="300px">
    <e-circulargauge-axes>
        <e-circulargauge-axis minimum="0" maximum="100">
            <e-circulargauge-pointers>
                <e-circulargauge-pointer value="@Model.TemperatureValue">
                </e-circulargauge-pointer>
            </e-circulargauge-pointers>
        </e-circulargauge-axis>
    </e-circulargauge-axes>
</ejs-circulargauge>

<ejs-circulargauge id="pressureGauge" title="Pressure" width="100%" height="300px">
    <e-circulargauge-axes>
        <e-circulargauge-axis minimum="0" maximum="150">
            <e-circulargauge-pointers>
                <e-circulargauge-pointer value="@Model.PressureValue">
                </e-circulargauge-pointer>
            </e-circulargauge-pointers>
        </e-circulargauge-axis>
    </e-circulargauge-axes>
</ejs-circulargauge>
```

### Pattern 2: Interactive Gauge with Drag

Use this pattern when users need to change a gauge value directly by dragging the pointer.

Implementation approach:

- Set `enablePointerDrag="true"` on the Circular Gauge.
- Use pointer drag events when value changes need to be tracked.
- Update the server only after drag completion if persistent storage is required.
- Avoid saving values continuously during drag movement unless real-time updates are required.

Example:

```html
@page
@model CircularGaugeGettingStarted.Pages.IndexModel

@{
    ViewData["Title"] = "Interactive Gauge";
}

<h1>Interactive Circular Gauge</h1>
<p>Drag the pointer to change the value.</p>


<ejs-circulargauge id="interactiveGauge"
                    title="Interactive Speed"
                    width="100%"
                    height="450px"
                    enablePointerDrag="true">
    <e-circulargauge-axes>
        <e-circulargauge-axis minimum="0"
                              maximum="120"
                              startAngle="240"
                              endAngle="120">
            <e-circulargauge-pointers>
                <e-circulargauge-pointer value="@Model.SpeedValue">
                </e-circulargauge-pointer>
            </e-circulargauge-pointers>
        </e-circulargauge-axis>
    </e-circulargauge-axes>
</ejs-circulargauge>

```

### Pattern 3: Gauge with Ranges and Alerts

Use this pattern when the gauge must communicate safe, warning, and danger zones.

Recommended range design:

- Green range for normal values.
- Yellow range for warning values.
- Red range for danger values.

Example:

```html
@page
@model CircularGaugeGettingStarted.Pages.IndexModel

@{
    ViewData["Title"] = "Gauge with Ranges";
}

<h1>Gauge with Ranges</h1>

<ejs-circulargauge id="rangeGauge"
                    title="System Load"
                    width="100%"
                    height="450px">
    <e-circulargauge-axes>
        <e-circulargauge-axis minimum="0"
                              maximum="120"
                              startAngle="240"
                              endAngle="120">
            <e-circulargauge-ranges>
                <e-circulargauge-range start="0"
                                       end="50"
                                       color="#30B32D"
                                       radius="80%">
                </e-circulargauge-range>
                <e-circulargauge-range start="50"
                                       end="80"
                                       color="#FFDD00"
                                       radius="80%">
                </e-circulargauge-range>
                <e-circulargauge-range start="80"
                                       end="120"
                                       color="#F03E3E"
                                       radius="80%">
                </e-circulargauge-range>
            </e-circulargauge-ranges>
            <e-circulargauge-pointers>
                <e-circulargauge-pointer value="@Model.SpeedValue">
                </e-circulargauge-pointer>
            </e-circulargauge-pointers>
        </e-circulargauge-axis>
    </e-circulargauge-axes>
</ejs-circulargauge>
```

### Pattern 4: Localized Gauge

Use this pattern when a gauge should support culture-specific text direction or number display.

Implementation approach:

- Use `locale` to apply culture-specific formatting where localization resources are configured.
- Use `enableRtl="true"` for right-to-left rendering.
- Use meaningful title text from the server-side model.
- Avoid hardcoding user-facing labels when the application supports multiple languages.

Example:

```html
@page
@model CircularGaugeGettingStarted.Pages.IndexModel

@{
    ViewData["Title"] = "Localized Gauge";
}

<h1>Localized Circular Gauge</h1>

<ejs-circulargauge id="localizedGauge"
                    title="@Model.GaugeTitle"
                    width="100%"
                    height="450px"
                    locale="en-US"
                    enableRtl="false"
                    useGroupingSeparator="true">
    <e-circulargauge-axes>
        <e-circulargauge-axis minimum="0"
                              maximum="100000"
                              startAngle="240"
                              endAngle="120">
            <e-circulargauge-pointers>
                <e-circulargauge-pointer value="65000">
                </e-circulargauge-pointer>
            </e-circulargauge-pointers>
        </e-circulargauge-axis>
    </e-circulargauge-axes>
</ejs-circulargauge>
```

## Key Props and Configuration

| Property | Purpose | Common Values |
|----------|---------|---------------|
| `title` | Sets the gauge title text. | `"Speed"`, `"Temperature"`, `"System Load"` |
| `centerX` | Sets the horizontal center position of the gauge. | `"50%"`, `"100px"` |
| `centerY` | Sets the vertical center position of the gauge. | `"50%"`, `"100px"` |
| `width` | Sets the gauge width. | `"400px"`, `"100%"` |
| `height` | Sets the gauge height. | `"450px"`, `"100%"` |
| `background` | Sets the gauge background color. | `"transparent"`, `"#f5f5f5"`, `"white"` |
| `enablePointerDrag` | Enables pointer dragging. | `true`, `false` |
| `enableRtl` | Enables right-to-left rendering. | `true`, `false` |
| `useGroupingSeparator` | Enables grouping separators for numeric labels. | `true`, `false` |
| `allowPrint` | Enables print support. | `true`, `false` |
| `allowImageExport` | Enables image export support. | `true`, `false` |
| `allowPdfExport` | Enables PDF export support. | `true`, `false` |
| `description` | Provides assistive description text. | `"Speed gauge showing current speed"` |

## Common Use Cases

1. Performance dashboards for displaying KPIs and business metrics.
2. Real-time monitoring screens for temperature, pressure, speed, or load values.
3. Progress indicators for completion percentage or goal tracking.
4. Resource utilization views for CPU, memory, disk, or network usage.
5. Speedometer-style displays for speed, RPM, or throughput.
6. Quality score dashboards for ratings, compliance levels, or satisfaction scores.
7. Alert-based monitoring where colored ranges indicate safe, warning, and danger zones.
8. Interactive input scenarios where a user drags the pointer to select a numeric value.

## Next Steps

- Use the Quick Start Example when creating a new Circular Gauge page.
- Use the axes topic when configuring scale behavior.
- Use the pointers topic when controlling how values are displayed.
- Use the ranges topic when showing safe, warning, and danger zones.
- Use the interaction topic when enabling pointer drag or tooltip behavior.
- Use the localization topic when supporting multiple cultures or right-to-left display.
- Use the export and print topic only when those features are required.
- Keep `Index.cshtml.cs` responsible for values and page data.
- Keep `Index.cshtml` responsible for Circular Gauge markup.
- Keep `_Layout.cshtml` responsible for the Syncfusion script reference and `<ejs-scripts>` registration.