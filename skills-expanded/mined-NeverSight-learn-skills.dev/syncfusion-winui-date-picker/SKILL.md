---
name: syncfusion-winui-date-picker
description: Implements Syncfusion WinUI DatePicker (SfDatePicker) control for date input and selection in desktop applications. Use this when building date input controls, calendar dropdown pickers, or date selection interfaces. This skill covers date restrictions, date formatting, calendar types, dropdown spinners, localization, and blackout dates for WinUI applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# WinUI DatePicker (SfDatePicker)

A comprehensive guide for implementing the Syncfusion WinUI DatePicker control - an intuitive, touch-friendly date selection control with dropdown spinner, multiple date formats, date restrictions, and extensive customization options.

## When to Use This Skill

Use this skill when you need to:
- Add date input controls to WinUI desktop applications
- Implement date pickers with dropdown calendar spinners
- Restrict date selection to specific ranges or block certain dates
- Support multiple calendar systems (Hebrew, Hijri, Persian, etc.)
- Customize date display and edit formats
- Implement localized date pickers with RTL support
- Create touch-friendly date selection interfaces
- Validate date input with custom rules
- Customize dropdown appearance and behavior
- Handle date selection events and validation

## Component Overview

The **SfDatePicker** control provides a modern date input experience for WinUI 3 desktop applications. It combines an editable text field with a dropdown date spinner, supporting various date formats, calendar types, and validation rules.

**Key Characteristics:**
- Touch-friendly dropdown date spinner interface
- Multiple date format support (display and edit formats)
- Date range restrictions (MinDate, MaxDate)
- Blackout dates for blocking specific dates
- Multiple calendar types (Gregorian, Hebrew, Hijri, Persian, etc.)
- Localization and RTL support
- Mask and free-form editing modes
- Customizable dropdown UI and spinner cells
- Built-in validation and watermark text
- XAML and C# configuration support

**Package:** `Syncfusion.Editors.WinUI`  
**Namespace:** `Syncfusion.UI.Xaml.Editors`  
**Control:** `SfDatePicker`

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

Start here for initial setup and basic usage:
- Installing Syncfusion.Editors.WinUI package
- Adding SfDatePicker to XAML and C# code
- Setting and getting selected date (SelectedDate property)
- Interactive date selection from dropdown
- Enabling null values (AllowNull property)
- Adding placeholder text (watermark)
- Configuring header and description
- Customizing header template
- Handling date changed events (SelectedDateChanged)

### Date Restriction
📄 **Read:** [references/date-restriction.md](references/date-restriction.md)

Learn how to restrict and validate date selection:
- Setting minimum and maximum date ranges (MinDate, MaxDate)
- Blocking specific dates with BlackoutDates collection
- Dynamically disabling dates (DateFieldItemPrepared event)
- Blocking weekend dates programmatically
- Hiding submit buttons for immediate selection
- Canceling date changes (SelectedDateChanging event)
- Date validation patterns and error handling

### Localization and Formatting
📄 **Read:** [references/localization-formatting.md](references/localization-formatting.md)

Configure calendar types, formats, and localization:
- Changing calendar type (CalendarIdentifier: Hebrew, Hijri, Persian, etc.)
- Setting flow direction for RTL languages
- Localizing with Language property
- Customizing display format (DisplayDateFormat)
- Formatting day, month, year fields (DayFormat, MonthFormat, YearFormat)
- Mask editing mode with auto-correction
- Free-form editing mode (EditMode)
- Showing/hiding clear button (ShowClearButton)

### Dropdown Customization
📄 **Read:** [references/dropdown-customization.md](references/dropdown-customization.md)

Customize the dropdown button and container:
- Customizing dropdown button UI (DropDownButtonTemplate)
- Hiding dropdown button (ShowDropDownButton)
- Changing dropdown alignment (DropDownPlacement)
- Opening dropdown programmatically (IsOpen property)
- Setting dropdown height (DropDownHeight)
- Controlling visible items count (VisibleItemsCount)

### Dropdown Header Customization
📄 **Read:** [references/dropdown-header-customization.md](references/dropdown-header-customization.md)

Configure the dropdown header area:
- Adding hints in dropdown header (DropDownHeader)
- Showing/hiding dropdown header (ShowDropDownHeader)
- Customizing header UI (DropDownHeaderTemplate)
- Hiding column headers (ShowColumnHeaders)
- Header layout patterns

### Spinner Customization
📄 **Read:** [references/spinner-customization.md](references/spinner-customization.md)

Customize the date spinner cells and columns:
- Setting cell dimensions (ItemWidth, ItemHeight)
- Restricting cell width (MinItemWidth, MaxItemWidth)
- Styling spinner cells (ItemContainerStyle)
- Custom cell templates (ItemTemplate)
- Conditional cell appearance (ItemTemplateSelector)
- Customizing columns (DateFieldPrepared event)
- Formatting individual date fields
- Enabling date looping in spinner

## Quick Start Example

### Basic DatePicker Setup

**XAML:**
```xml
<Window
    x:Class="DatePickerDemo.MainWindow"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:editors="using:Syncfusion.UI.Xaml.Editors">
    
    <Grid>
        <editors:SfDatePicker 
            x:Name="datePicker"
            Header="Select Date"
            PlaceholderText="Choose a date"
            SelectedDate="2026-03-22"
            Width="250" 
            Height="75" />
    </Grid>
</Window>
```

**C#:**
```csharp
using Syncfusion.UI.Xaml.Editors;

namespace DatePickerDemo
{
    public sealed partial class MainWindow : Window
    {
        public MainWindow()
        {
            this.InitializeComponent();
            
            // Creating an instance of the Date Picker control
            SfDatePicker sfDatePicker = new SfDatePicker();
            this.Content = sfDatePicker;
        }
    }
}
```

## Common Patterns

### Pattern 1: Date Range Restriction
```xml
<editors:SfDatePicker 
    x:Name="datePicker"
    MinDate="2026-01-01"
    MaxDate="2026-12-31"
    Header="Select date within 2026" />
```

### Pattern 2: Blocking Specific Dates
```csharp
// In ViewModel or code-behind
public DateTimeOffsetCollection BlockedDates { get; set; }

public void InitializeBlockedDates()
{
    BlockedDates = new DateTimeOffsetCollection();
    BlockedDates.Add(new DateTimeOffset(new DateTime(2026, 12, 25))); // Christmas
    BlockedDates.Add(new DateTimeOffset(new DateTime(2026, 1, 1)));   // New Year
}
```

```xml
<editors:SfDatePicker 
    BlackoutDates="{Binding BlockedDates}" />
```

### Pattern 3: Custom Date Format
```xml
<editors:SfDatePicker 
    DisplayDateFormat="MMMM dd, yyyy"
    DayFormat="{}{day.integer}"
    MonthFormat="{}{month.full}"
    YearFormat="{}{year.full}" />
```

### Pattern 4: Localized DatePicker with Calendar Type
```xml
<editors:SfDatePicker 
    CalendarIdentifier="HebrewCalendar"
    Language="he-IL"
    FlowDirection="RightToLeft" />
```

### Pattern 5: Null Value Support
```xml
<editors:SfDatePicker 
    AllowNull="True"
    SelectedDate="{x:Null}"
    PlaceholderText="Select a date" />
```

### Pattern 6: Immediate Selection (No Submit Button)
```xml
<editors:SfDatePicker 
    ShowSubmitButtons="False" />
```

## Key Properties Reference

### Date Selection
| Property | Type | Description |
|----------|------|-------------|
| `SelectedDate` | `DateTimeOffset?` | Gets or sets the selected date |
| `AllowNull` | `bool` | Allows null value selection |

### Date Restriction
| Property | Type | Description |
|----------|------|-------------|
| `MinDate` | `DateTimeOffset` | Minimum selectable date (default: 1/1/1921) |
| `MaxDate` | `DateTimeOffset` | Maximum selectable date (default: 12/31/2121) |
| `BlackoutDates` | `DateTimeOffsetCollection` | Collection of blocked dates |

### Formatting
| Property | Type | Description |
|----------|------|-------------|
| `DisplayDateFormat` | `string` | Display format in editor (default: "d") |
| `DayFormat` | `string` | Day field format in spinner |
| `MonthFormat` | `string` | Month field format in spinner |
| `YearFormat` | `string` | Year field format in spinner |

### Localization
| Property | Type | Description |
|----------|------|-------------|
| `CalendarIdentifier` | `string` | Calendar type (Gregorian, Hebrew, Hijri, etc.) |
| `Language` | `string` | Language/culture for localization |

### Dropdown Configuration
| Property | Type | Description |
|----------|------|-------------|
| `DropDownHeader` | `object` | Header content in dropdown |
| `ShowDropDownHeader` | `bool` | Shows/hides dropdown header |
| `ShowColumnHeaders` | `bool` | Shows/hides spinner column headers |
| `ShowDropDownButton` | `bool` | Shows/hides dropdown button |
| `IsOpen` | `bool` | Opens/closes dropdown programmatically |
| `DropDownHeight` | `double` | Height of dropdown spinner |
| `VisibleItemsCount` | `int` | Number of visible items in spinner |

### Spinner Item Sizing
| Property | Type | Description |
|----------|------|-------------|
| `ItemWidth` | `double` | Width of spinner cells (default: 80) |
| `ItemHeight` | `double` | Height of spinner cells (default: 40) |
| `MinItemWidth` | `double` | Minimum cell width |
| `MaxItemWidth` | `double` | Maximum cell width |

### UI Customization
| Property | Type | Description |
|----------|------|-------------|
| `PlaceholderText` | `string` | Watermark text when no date selected |
| `Header` | `object` | Header content above control |
| `Description` | `object` | Description text below control |
| `ItemTemplate` | `DataTemplate` | Template for spinner cells |
| `ItemTemplateSelector` | `DataTemplateSelector` | Conditional cell templates |
| `ItemContainerStyle` | `Style` | Style for spinner cells |
| `ShowClearButton` | `bool` | Shows/hides clear button in editor |
| `ShowSubmitButtons` | `bool` | Shows/hides OK/Cancel buttons |

### Editing
| Property | Type | Description |
|----------|------|-------------|
| `EditMode` | `DateTimeEditMode` | Mask or Normal editing mode |

### Events
| Event | Description |
|-------|-------------|
| `SelectedDateChanged` | Fires when selected date changes |
| `SelectedDateChanging` | Fires before date changes (cancelable) |
| `DateFieldItemPrepared` | Fires for each spinner item (for customization) |
| `DateFieldPrepared` | Fires for each spinner column (for customization) |

## Common Use Cases

### Use Case 1: Appointment Scheduler
Date picker for selecting appointment dates with working hours only:
```csharp
// Block weekends and restrict to business days
datePicker.DateFieldItemPrepared += (s, e) =>
{
    if (e.ItemInfo.DateTime.Value.DayOfWeek == DayOfWeek.Saturday ||
        e.ItemInfo.DateTime.Value.DayOfWeek == DayOfWeek.Sunday)
    {
        e.ItemInfo.IsEnabled = false;
    }
};
```

### Use Case 2: Booking System
Date picker with blackout dates for unavailable dates:
```csharp
// Mark booked dates as unavailable
var bookedDates = GetBookedDatesFromDatabase();
datePicker.BlackoutDates = new DateTimeOffsetCollection();
foreach (var date in bookedDates)
{
    datePicker.BlackoutDates.Add(new DateTimeOffset(date));
}
```

### Use Case 3: Birth Date Entry
Date picker for entering historical dates:
```xml
<editors:SfDatePicker 
    Header="Date of Birth"
    MaxDate="{x:Bind CurrentDate}"
    MinDate="1920-01-01"
    DisplayDateFormat="MMMM dd, yyyy" />
```

### Use Case 4: Multi-Language Application
Localized date picker with automatic RTL detection:
```csharp
// Set based on user's locale
datePicker.Language = currentUser.PreferredLanguage;
datePicker.CalendarIdentifier = currentUser.CalendarType;
```

### Use Case 5: Custom Branded UI
Date picker with custom colors and icons:
```xml
<editors:SfDatePicker>
    <editors:SfDatePicker.DropDownButtonTemplate>
        <DataTemplate>
            <FontIcon Glyph="&#xE787;" Foreground="Blue" />
        </DataTemplate>
    </editors:SfDatePicker.DropDownButtonTemplate>
</editors:SfDatePicker>
```

## Additional Resources

- **NuGet Package:** [Syncfusion.Editors.WinUI](https://www.nuget.org/packages/Syncfusion.Editors.WinUI)
- **Official Documentation:** [WinUI DatePicker Docs](https://help.syncfusion.com/winui/date-picker/overview)
- **GitHub Examples:** [SyncfusionExamples/syncfusion-winui-tools-datepicker-examples](https://github.com/SyncfusionExamples/syncfusion-winui-tools-datepicker-examples)

---

**Next Steps:** Choose a documentation section above based on your implementation needs, or start with the Getting Started guide for basic setup.
