---
name: syncfusion-winui-calendar
description: Implements Syncfusion WinUI Calendar (SfCalendar) control for date selection in desktop applications. Use this when building date pickers, date selection interfaces (single, multiple, or range), month/year navigation, or calendar views. This skill covers calendar configuration, date restrictions, blackout dates, week numbers, localization, and customization for Windows desktop applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# WinUI Calendar (SfCalendar)

Comprehensive guide for implementing the Syncfusion WinUI Calendar (SfCalendar) control for date selection in Windows desktop applications. The Calendar control supports single, multiple, and range date selection with extensive customization options, navigation between different views, date restrictions, and localization.

## When to Use This Skill

Use this skill when you need to:
- **Create calendar controls** for date selection in WinUI desktop applications
- **Select dates** in single, multiple, or range modes
- **Navigate views** between month, year, decade, and century
- **Restrict dates** using min/max dates and blackout dates
- **Customize UI** with templates, special date highlighting, and styling
- **Localize calendars** for different cultures and languages
- **Display week numbers** with various calculation rules
- **Handle date selection events** for validation or business logic
- **Implement accessible** date pickers with keyboard navigation
- **Troubleshoot** calendar rendering or data binding issues

## Component Overview

**SfCalendar** is the primary date selection control for WinUI desktop applications, offering:

- **Selection Modes:** Single, Multiple, Range, or None
- **View Navigation:** Month, Year, Decade, and Century views
- **Date Restrictions:** MinDate, MaxDate, and BlackoutDates collections
- **Customization:** Cell templates, special date highlighting, and theme integration
- **Localization:** Support for multiple calendar types and cultures
- **Week Numbers:** Configurable week numbering with ISO 8601 support
- **Keyboard Support:** Full keyboard navigation and accessibility
- **Data Binding:** MVVM-friendly with SelectedDate and SelectedDates binding

**Control Structure:**
- Month view with day cells (default)
- Year view with month cells
- Decade view with year cells
- Century view with decade cells
- Header for navigation and current view title
- Navigation buttons for scrolling

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Creating a WinUI 3 desktop application
- Installing Syncfusion.Calendar.WinUI NuGet package
- Adding Calendar control in XAML
- Adding Calendar control in C#
- Basic date selection
- Control structure overview

### Selection Features
📄 **Read:** [references/selection.md](references/selection.md)
- Selection modes: None, Single, Multiple, Range
- SelectedDate property (single selection)
- SelectedDates collection (multiple/range selection)
- Programmatic date selection
- Selection changed events
- Data binding selected dates

### Navigation and Display
📄 **Read:** [references/navigation.md](references/navigation.md)
- Display modes: Month, Year, Decade, Century
- Navigating between views
- SetDisplayDate method to bring dates into view
- Min/Max display mode restrictions
- Selection based on view restrictions
- Navigation direction (vertical/horizontal scrolling)

### Date Restrictions
📄 **Read:** [references/date-restrictions.md](references/date-restrictions.md)
- MinDate and MaxDate properties
- Restricting selectable date ranges
- BlackoutDates collection
- Blocking specific dates from selection
- Validating date selection
- Styling disabled dates

### Localization and Formatting
📄 **Read:** [references/localization-formatting.md](references/localization-formatting.md)
- Culture and language support
- FormatString for custom date formats
- Abbreviated day and month names
- RTL (Right-to-Left) support
- FlowDirection property
- Date formatting patterns

### UI Customization
📄 **Read:** [references/customization.md](references/customization.md)
- Cell templates (DataTemplate)
- Special date highlighting with icons
- Custom cell styling
- Header customization
- Background and foreground colors
- Border and appearance customization
- Theme integration

### Week Numbers
📄 **Read:** [references/week-numbers.md](references/week-numbers.md)
- ShowWeekNumbers property
- WeekNumberRule options
- Week number formatting
- FirstDay, FirstFourDayWeek, FirstFullWeek rules
- Culture-specific week calculations

## Quick Start Example

Here's a minimal working example to get started:

### 1. Add Namespace

**XAML:**
```xml
<Window xmlns:calendar="using:Syncfusion.UI.Xaml.Calendar">
```

**C#:**
```csharp
using Syncfusion.UI.Xaml.Calendar;
```

### 2. Create Basic Calendar (XAML)

```xml
<Window
    x:Class="CalendarApp.MainWindow"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:calendar="using:Syncfusion.UI.Xaml.Calendar">
    
    <Grid>
        <calendar:SfCalendar x:Name="sfCalendar" />
    </Grid>
</Window>
```

### 3. Or Create Programmatically (C#)

```csharp
using Syncfusion.UI.Xaml.Calendar;

namespace CalendarApp
{
    public sealed partial class MainWindow : Window
    {
        public MainWindow()
        {
            this.InitializeComponent();
            
            // Create calendar programmatically
            SfCalendar sfCalendar = new SfCalendar();
            this.Content = sfCalendar;
        }
    }
}
```

### 4. Select a Date (Optional)

```csharp
// Select today's date
sfCalendar.SelectedDate = DateTimeOffset.Now;

// Or select a specific date
sfCalendar.SelectedDate = new DateTimeOffset(new DateTime(2026, 3, 22));
```

## Common Patterns

### Pattern 1: Single Date Selection

```xml
<calendar:SfCalendar 
    x:Name="calendar"
    SelectionMode="Single"
    SelectedDate="{x:Bind ViewModel.SelectedDate, Mode=TwoWay}" />
```

```csharp
// Access selected date
DateTimeOffset? selected = calendar.SelectedDate;
```

### Pattern 2: Multiple Date Selection

```xml
<calendar:SfCalendar 
    x:Name="calendar"
    SelectionMode="Multiple"
    SelectedDates="{x:Bind ViewModel.SelectedDates, Mode=TwoWay}" />
```

```csharp
// Access multiple selected dates
DateTimeOffsetCollection selectedDates = calendar.SelectedDates;
```

### Pattern 3: Date Range Selection

```xml
<calendar:SfCalendar 
    x:Name="calendar"
    SelectionMode="Range" />
```

### Pattern 4: Restrict Date Range

```xml
<calendar:SfCalendar 
    x:Name="calendar"
    MinDate="2026-01-01"
    MaxDate="2026-12-31" />
```

```csharp
// Set date restrictions in code
calendar.MinDate = new DateTimeOffset(new DateTime(2026, 1, 1));
calendar.MaxDate = new DateTimeOffset(new DateTime(2026, 12, 31));
```

### Pattern 5: Block Specific Dates

```csharp
// Create blackout dates collection
DateTimeOffsetCollection blackoutDates = new DateTimeOffsetCollection();
blackoutDates.Add(new DateTimeOffset(new DateTime(2026, 3, 25))); // Holiday
blackoutDates.Add(new DateTimeOffset(new DateTime(2026, 12, 25))); // Christmas

calendar.BlackoutDates = blackoutDates;
```

### Pattern 6: Navigate to Specific Month

```csharp
// Navigate to a specific date's month
calendar.SetDisplayDate(new DateTimeOffset(new DateTime(2026, 6, 15)));
```

### Pattern 7: Restrict Navigation to Year View

```xml
<calendar:SfCalendar 
    x:Name="calendar"
    MinDisplayMode="Month"
    MaxDisplayMode="Year" />
```

### Pattern 8: ViewModel Data Binding

```csharp
public class CalendarViewModel : INotifyPropertyChanged
{
    private DateTimeOffset? selectedDate;
    
    public DateTimeOffset? SelectedDate
    {
        get => selectedDate;
        set
        {
            selectedDate = value;
            OnPropertyChanged(nameof(SelectedDate));
        }
    }
    
    public event PropertyChangedEventHandler PropertyChanged;
    
    protected void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}
```

```xml
<calendar:SfCalendar 
    SelectedDate="{x:Bind ViewModel.SelectedDate, Mode=TwoWay}" />
```

## Key Properties Reference

### Selection Properties

| Property | Type | Description |
|----------|------|-------------|
| `SelectedDate` | DateTimeOffset? | Gets or sets the selected date (single selection mode) |
| `SelectedDates` | DateTimeOffsetCollection | Gets or sets the collection of selected dates (multiple/range modes) |
| `SelectedRange` | DateTimeOffsetRange | Gets the selected date range when SelectionMode is Range |
| `SelectionMode` | CalendarSelectionMode | Date selection mode: None, Single, Multiple, Range |
| `SelectionHighlightMode` | SelectionHighlightMode | Highlight style for selected dates: Outline, Filled |
| `SelectionShape` | SelectionShape | Shape of selection indicator: Circle, Rectangle |

### Date Restriction Properties

| Property | Type | Description |
|----------|------|-------------|
| `MinDate` | DateTimeOffset | Minimum selectable date (default: 1/1/1920) |
| `MaxDate` | DateTimeOffset | Maximum selectable date (default: 12/31/2120) |
| `BlackoutDates` | DateTimeOffsetCollection | Collection of non-selectable (blocked) dates |

### Display and Navigation Properties

| Property | Type | Description |
|----------|------|-------------|
| `DisplayMode` | CalendarDisplayMode | Current view: Month, Year, Decade, Century |
| `MinDisplayMode` | CalendarDisplayMode | Minimum view level users can navigate to |
| `MaxDisplayMode` | CalendarDisplayMode | Maximum view level users can navigate to |
| `NavigationDirection` | CalendarNavigationDirection | Scroll direction within view: Vertical, Horizontal |
| `OutOfScopeVisibility` | OutOfScopeVisibility | Show/hide dates from adjacent months: Enabled, Hidden |
| `HeaderInfo` | object | Custom header content for the calendar |

### Localization and Formatting Properties

| Property | Type | Description |
|----------|------|-------------|
| `CalendarIdentifier` | string | Calendar system type: GregorianCalendar, HijriCalendar, HebrewCalendar, etc. |
| `FirstDayOfWeek` | FirstDayOfWeek | First day of week: Sunday, Monday, Tuesday, etc. |
| `DayFormat` | string | Format pattern for day numbers (e.g., "{day.integer(2)}") |
| `MonthFormat` | string | Format pattern for month names (e.g., "{month.full}") |
| `DayOfWeekFormat` | string | Format pattern for day-of-week headers (e.g., "{dayofweek.abbreviated(3)}") |
| `MonthHeaderFormat` | string | Format pattern for month/year header (e.g., "{month.full} {year.full}") |
| `NumberOfWeeksInView` | int | Number of week rows displayed in month view (default: 6) |

### Week Number Properties

| Property | Type | Description |
|----------|------|-------------|
| `ShowWeekNumbers` | bool | Display week numbers column (default: false) |
| `WeekNumberRule` | CalendarWeekRule | Week calculation rule: FirstDay, FirstFourDayWeek, FirstFullWeek |
| `WeekNumberFormat` | string | Format for week numbers (use # as placeholder, e.g., "W #") |

## Common Use Cases

### Event Scheduling Application
Create event scheduling interfaces where users select single dates for appointments, meetings, or reminders with future date restrictions and business day filtering.

### Vacation Request System
Build vacation management systems with multiple date selection, blackout dates for company holidays, and range selection for consecutive vacation days.

### Appointment Booking Calendar
Implement booking systems with dynamic date availability, blackout dates for unavailable slots, and real-time availability checking through ItemPrepared event.

### International Date Picker
Develop multi-language applications with localized calendars supporting different calendar types (Hijri, Hebrew, Persian), RTL languages, and culture-specific formatting.

### Date Range Filtering
Create data filtering interfaces where users select date ranges for reports, analytics dashboards, or transaction queries with min/max date boundaries.

### Credit Card Expiry Selector
Implement month/year-only selectors for credit card expiration dates by restricting navigation to Year and Decade views only.


---

**Next Steps:** Read the reference documentation above based on what you need to implement. Start with [getting-started.md](references/getting-started.md) for initial setup, then explore specific features as needed.
