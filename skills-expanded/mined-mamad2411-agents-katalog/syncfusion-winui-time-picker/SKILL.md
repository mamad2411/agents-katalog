---
name: syncfusion-winui-time-picker
description: Implements Syncfusion WinUI TimePicker (SfTimePicker) control for time input and selection in desktop applications. Use this when building time input controls, time selection interfaces, or dropdown time spinners. This skill covers time restrictions, time formatting, dropdown spinner customization, and time selection for scheduling and appointment scenarios in WinUI applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# WinUI TimePicker (SfTimePicker) Implementation Guide

Comprehensive guide for implementing the Syncfusion WinUI TimePicker control in Windows desktop applications. The SfTimePicker provides an intuitive, touch-friendly interface to select time from a dropdown spinner with support for time restrictions, formatting, localization, and extensive customization.

## When to Use This Skill

Use this skill when you need to:
- Implement time selection in WinUI 3 desktop applications
- Add time input controls with dropdown spinner
- Create appointment scheduling or time entry forms
- Restrict time selection to specific ranges or intervals
- Implement 12-hour or 24-hour time formats
- Customize dropdown time spinner appearance
- Support localized time input with RTL layouts
- Validate and format time input in Windows apps
- Hide or disable specific times from selection

## Component Overview

The **SfTimePicker** control provides a modern time selection experience for WinUI applications with:

**Key Features:**
- **Dropdown Time Spinner** - Select time from hour, minute, and meridiem (AM/PM) columns
- **Time Restrictions** - Set minimum/maximum times and blackout specific times
- **Multiple Formats** - Support for 12-hour and 24-hour clock formats
- **Localization** - Multi-language support with RTL layout
- **Edit Modes** - Mask editing with auto-correction or free-form input
- **Extensive Customization** - Customize dropdown button, header, spinner cells, and templates
- **Validation** - Built-in validation with change events for custom logic
- **Accessibility** - Full keyboard navigation and WCAG compliance

**Control Structure:**
- Text editor for direct time input
- Dropdown button to open time spinner
- Dropdown spinner with hour, minute, and meridiem columns
- Optional dropdown header for hints
- Submit/Cancel buttons (optional)

**NuGet Package:** `Syncfusion.Editors.WinUI`

**Namespace:** `Syncfusion.UI.Xaml.Editors`

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

Use this reference for initial setup and basic implementation:
- Installing the Syncfusion.Editors.WinUI NuGet package
- Adding SfTimePicker to XAML and C# code
- Understanding component structure (editor, dropdown, spinner)
- Setting selected time programmatically with `SelectedTime` property
- Interactive time selection from dropdown
- Allowing null values with `AllowNull` property
- Adding header and description text
- Customizing header with `HeaderTemplate`
- Setting watermark text with `PlaceholderText`
- Handling time changed events with `SelectedTimeChanged`

### Time Restrictions
📄 **Read:** [references/time-restrictions.md](references/time-restrictions.md)

Use this reference for controlling time selection:
- Limiting available times with `MinTime` and `MaxTime` properties
- Blocking specific times using `BlackoutTimes` collection
- Creating custom time intervals (e.g., 5-minute, 15-minute increments)
- Using `TimeFieldPrepared` event to customize time intervals
- Hiding submit buttons with `ShowSubmitButtons` property
- Selecting time directly as you scroll the spinner
- Canceling time changes with `SelectedTimeChanging` event
- Implementing custom validation logic
- Handling edge cases and validation errors

### Localization and Formatting
📄 **Read:** [references/localization-formatting.md](references/localization-formatting.md)

Use this reference for formatting and localizing time display:
- Switching between 12-hour and 24-hour formats with `ClockIdentifier`
- Changing flow direction for RTL languages with `FlowDirection`
- Localizing the control with `Language` property
- Customizing time display format with `DisplayTimeFormat`
- Understanding format patterns (hh:mm tt, HH:mm, h:mm, etc.)
- Using mask edit mode for auto-correcting input
- Using normal edit mode for free-form input validation
- Input behavior and automatic field correction
- Showing/hiding the clear button with `ShowClearButton`

### Dropdown Customization
📄 **Read:** [references/dropdown-customization.md](references/dropdown-customization.md)

Use this reference for customizing the dropdown container:
- Customizing dropdown button UI with `DropDownButtonTemplate`
- Hiding dropdown button with `ShowDropDownButton` property
- Changing dropdown alignment with `DropDownPlacement`
- Opening/closing dropdown programmatically with `IsOpen` property
- Setting dropdown height with `DropDownHeight` property
- Controlling visible items with `VisibleItemsCount` property
- Understanding dropdown smart positioning
- Keyboard shortcuts for opening dropdown (Alt+Down)

### Dropdown Header Customization
📄 **Read:** [references/dropdown-header-customization.md](references/dropdown-header-customization.md)

Use this reference for customizing the dropdown header:
- Adding hints in dropdown header with `DropDownHeader` property
- Showing/hiding header with `ShowDropDownHeader` property
- Customizing header appearance with `DropDownHeaderTemplate`
- Creating custom header layouts with icons and text
- Hiding column headers with `ShowColumnHeaders` property
- Understanding column header customization
- Header styling best practices

### Dropdown Spinner Customization
📄 **Read:** [references/dropdown-spinner-customization.md](references/dropdown-spinner-customization.md)

Use this reference for customizing dropdown spinner cells and columns:
- Changing cell size with `ItemWidth` and `ItemHeight` properties
- Restricting cell width with `MinItemWidth` and `MaxItemWidth`
- Styling all cells with `ItemContainerStyle` property
- Customizing cell templates with `ItemTemplate`
- Conditional cell styling with `ItemTemplateSelector`
- Customizing individual columns with `TimeFieldPrepared` event
- Changing column headers, intervals, and cell sizes per column
- Adding icons or custom content to specific time cells
- Performance optimization for large customizations

## Quick Start Example

### Basic TimePicker Implementation

**XAML:**
```xml
<Window xmlns:editors="using:Syncfusion.UI.Xaml.Editors">
    <Grid>
        <editors:SfTimePicker 
            x:Name="sfTimePicker"
            Header="Select Time"
            PlaceholderText="Pick a time"
            Width="250" />
    </Grid>
</Window>
```

**C#:**
```csharp
using Syncfusion.UI.Xaml.Editors;

// Create TimePicker programmatically
SfTimePicker timePicker = new SfTimePicker();
timePicker.Header = "Select Time";
timePicker.PlaceholderText = "Pick a time";

// Set selected time
timePicker.SelectedTime = new DateTimeOffset(
    new DateTime(2024, 1, 1, 14, 30, 0));

// Handle time changed event
timePicker.SelectedTimeChanged += (s, e) => {
    var oldTime = e.OldDateTime;
    var newTime = e.NewDateTime;
    // Handle time change
};
```

## Common Patterns

### Time Selection with Restrictions

Restrict time selection to business hours (9 AM - 5 PM):

```csharp
// Requires: using Syncfusion.UI.Xaml.Editors;
sfTimePicker.MinTime = new DateTimeOffset(
    new DateTime(DateTime.Now.Year, DateTime.Now.Month, 
                 DateTime.Now.Day, 9, 0, 0));
sfTimePicker.MaxTime = new DateTimeOffset(
    new DateTime(DateTime.Now.Year, DateTime.Now.Month, 
                 DateTime.Now.Day, 17, 0, 0));
```

### 24-Hour Format

Switch to 24-hour clock format:

```xml
<editors:SfTimePicker 
    ClockIdentifier="24HourClock"
    DisplayTimeFormat="HH:mm" />
```

### Custom Time Intervals

Allow only 15-minute intervals:

```csharp
using System.Collections.ObjectModel;
using Syncfusion.UI.Xaml.Editors;

sfTimePicker.TimeFieldPrepared += (s, e) => {
    if (e.Column?.Field == DateTimeField.Minute) {
        var minutes = new ObservableCollection<string>();
        for (int i = 0; i < 60; i += 15) {
            minutes.Add(i.ToString("00"));
        }
        e.Column.ItemsSource = minutes;
    }
};
```

### Blocking Lunch Hour

Prevent selection during lunch break (12 PM - 1 PM):

```csharp
using Syncfusion.UI.Xaml.Editors;

var blackoutTimes = new DateTimeOffsetCollection();
for (int minute = 0; minute < 60; minute++) {
    blackoutTimes.Add(new DateTimeOffset(
        new DateTime(DateTime.Now.Year, DateTime.Now.Month, 
                     DateTime.Now.Day, 12, minute, 0)));
}
sfTimePicker.BlackoutTimes = blackoutTimes;
```

## Key Properties

### Core Properties

| Property | Type | Description |
|----------|------|-------------|
| `SelectedTime` | DateTimeOffset? | Gets or sets the selected time value |
| `MinTime` | DateTimeOffset | Minimum selectable time (default: 1/1/1921 10:37:16 PM) |
| `MaxTime` | DateTimeOffset | Maximum selectable time (default: 12/31/2121 10:37:16 PM) |
| `BlackoutTimes` | DateTimeOffsetCollection | Collection of times to disable from selection |
| `AllowNull` | bool | Allows null value for SelectedTime (default: false) |
| `PlaceholderText` | string | Watermark text shown when SelectedTime is null |

### Formatting Properties

| Property | Type | Description |
|----------|------|-------------|
| `ClockIdentifier` | string | Clock format: "12HourClock" or "24HourClock" |
| `DisplayTimeFormat` | string | Format pattern for displaying time (e.g., "hh:mm tt", "HH:mm") |
| `EditMode` | DateTimeEditMode | Edit mode: Mask (auto-correct) or Normal (validate on Enter) |
| `ShowClearButton` | bool | Shows/hides the clear button (default: true) |

### Dropdown Properties

| Property | Type | Description |
|----------|------|-------------|
| `ShowDropDownButton` | bool | Shows/hides dropdown button (default: true) |
| `DropDownButtonTemplate` | DataTemplate | Template for customizing dropdown button |
| `DropDownPlacement` | FlyoutPlacementMode | Dropdown alignment (Auto, Bottom, Top, etc.) |
| `IsOpen` | bool | Opens/closes dropdown programmatically |
| `DropDownHeight` | double | Fixed height for dropdown spinner |
| `VisibleItemsCount` | int | Number of visible items in dropdown (default: -1) |

### Dropdown Header Properties

| Property | Type | Description |
|----------|------|-------------|
| `ShowDropDownHeader` | bool | Shows/hides dropdown header (default: false) |
| `DropDownHeader` | object | Content for dropdown header |
| `DropDownHeaderTemplate` | DataTemplate | Template for dropdown header customization |
| `ShowColumnHeaders` | bool | Shows/hides column headers in spinner (default: true) |

### Spinner Customization Properties

| Property | Type | Description |
|----------|------|-------------|
| `ItemWidth` | double | Width of spinner cells (default: 80) |
| `ItemHeight` | double | Height of spinner cells (default: 40) |
| `MinItemWidth` | double | Minimum width for spinner cells (default: 0) |
| `MaxItemWidth` | double | Maximum width for spinner cells (default: Infinity) |
| `ItemContainerStyle` | Style | Style applied to all spinner cells |
| `ItemTemplate` | DataTemplate | Template for spinner cell content |
| `ItemTemplateSelector` | DataTemplateSelector | Conditional templates for spinner cells |

### Events

| Event | Description |
|-------|-------------|
| `SelectedTimeChanged` | Fires after SelectedTime changes, provides old and new values |
| `SelectedTimeChanging` | Fires before SelectedTime updates, allows cancellation |
| `TimeFieldPrepared` | Fires when dropdown spinner columns are prepared, allows customization |

## Common Use Cases

### Appointment Scheduling
Use TimePicker for booking appointments with restricted business hours, blocked lunch times, and 15-30 minute intervals.

### Time Entry Forms
Implement time input in forms with validation, nullable times, and custom formats based on user locale.

### Shift Management
Create shift time selectors with restricted ranges (e.g., morning: 6AM-2PM, evening: 2PM-10PM, night: 10PM-6AM).

### Meeting Scheduler
Build meeting time pickers with blackout times for existing meetings and custom intervals (30 min or 1 hour slots).

### Timer Applications
Use TimePicker for setting alarm times, countdown timers, or reminder schedules with 24-hour format.

### Localized Applications
Implement time selection with right-to-left layout for Arabic/Hebrew languages and locale-specific formats.

### Custom Time Intervals
Create specialized time pickers for industries requiring specific intervals (e.g., transportation schedules, medical appointments).
