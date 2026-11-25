---
name: syncfusion-winui-calendar-date-picker
description: Implements Syncfusion WinUI Calendar Date Picker (SfCalendarDatePicker) control for date selection with calendar dropdown. Use this when building calendar date pickers, date input controls, or dropdown calendar interfaces in WinUI desktop applications. This skill covers date restrictions, blackout dates, calendar localization, week numbers, and customization.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion WinUI Calendar Date Picker

Comprehensive guide for implementing the Calendar Date Picker control in WinUI 3 desktop applications. The `SfCalendarDatePicker` provides an intuitive, touch-friendly interface for selecting dates from a drop-down calendar with extensive customization options.

## When to Use This Skill

Use this skill when you need to:
- Implement date input with calendar drop-down in WinUI applications
- Add date selection with visual calendar interface
- Restrict date selection using min/max dates or blackout dates
- Customize calendar appearance and behavior
- Support multiple calendar systems (Gregorian, Hebrew, Hijri, etc.)
- Display week numbers in calendar
- Implement navigation between month/year/decade/century views
- Create localized date pickers for different cultures
- Handle date validation and selection events
- Block specific dates (weekends, holidays) from selection

## Component Overview

The `SfCalendarDatePicker` control combines a text editor with a drop-down calendar, allowing users to select dates either by typing or by choosing from the calendar. It supports various date formats, calendar types, and extensive customization options.

**Key Features:**
- Date selection via drop-down calendar or keyboard input
- Min/max date restrictions
- Blackout dates to prevent specific date selection
- Dynamic date blocking with custom logic
- Multiple calendar systems support (Gregorian, Hebrew, Hijri, etc.)
- Localization for different cultures and languages
- Week number display with configurable rules
- View navigation (month, year, decade, century)
- Customizable date formats and display
- Theme and template customization
- Touch-friendly interface
- Built-in validation and events

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

Start here for initial implementation. This covers:
- Installing the Syncfusion.Calendar.WinUI NuGet package
- Creating WinUI 3 application setup
- Basic XAML and C# implementation
- Programmatic and interactive date selection
- Null value handling with AllowNull property
- Header and description setup
- Watermark text (PlaceholderText)
- SelectedDateChanged and SelectedDateChanging events
- Edit modes (Mask vs Normal/free form editing)
- Drop-down button visibility
- Submit buttons configuration

### Date Selection and Restriction
📄 **Read:** [references/date-selection-restriction.md](references/date-selection-restriction.md)

Learn how to control which dates users can select:
- SelectedDate property for getting/setting dates
- MinDate and MaxDate for date range restrictions
- BlackoutDates collection for blocking specific dates
- Dynamic date blocking using CalendarItemPrepared event
- Blocking weekend days or holidays
- Custom display text for specific dates
- SelectionHighlightMode (Outline vs Filled)
- SelectionShape (Circle vs Rectangle)
- Validation patterns and edge cases

### UI Customization
📄 **Read:** [references/ui-customization.md](references/ui-customization.md)

Customize the visual appearance and behavior:
- ShowClearButton to show/hide the clear button
- DropDownPlacement for alignment (Left, Right, Top, Bottom, Center)
- DropDownWidth and DropDownHeight for sizing
- OutOfScopeVisibility to show/hide leading and trailing dates
- Custom item templates using AttachedFlyout and DropDownFlyout
- EventDataConverter pattern for highlighting special dates
- Theme key customization (colors, fonts, borders)
- CalendarItem styling with ContentTemplate
- Advanced template patterns

### Localization and Formatting
📄 **Read:** [references/localization-formatting.md](references/localization-formatting.md)

Configure calendar types, languages, and date formats:
- CalendarIdentifier for different calendar systems (Gregorian, Hebrew, Hijri, Korean, Taiwan, Thai, Persian, UmAlQura)
- Language property for culture-specific display
- DisplayDateFormat for editor text format
- DayFormat, MonthFormat, DayOfWeekFormat for calendar display
- MonthHeaderFormat for header customization
- FirstDayOfWeek to set week start day
- NumberOfWeeksInView to control visible weeks
- DateTimeFormatter patterns

### Navigation Between Views
📄 **Read:** [references/navigation.md](references/navigation.md)

Control view modes and navigation behavior:
- DisplayMode property (Month, Year, Decade, Century)
- MinDisplayMode and MaxDisplayMode for view restrictions
- View navigation patterns for specific use cases (e.g., credit card expiry)
- Keyboard shortcuts for navigation (Tab, Arrow keys, Ctrl+Arrow, PageUp/Down, Home/End)
- Mouse interaction patterns
- Selection based on view restrictions

### Week Numbers
📄 **Read:** [references/week-numbers.md](references/week-numbers.md)

Display and customize week numbers:
- ShowWeekNumbers property to enable week display
- WeekNumberRule (FirstDay, FirstFourDayWeek, FirstFullWeek)
- WeekNumberFormat for custom formatting with prefix/suffix
- WeekNumberTemplate for complete customization
- WeekNameTemplate for day name customization
- CalendarItemTemplateSelector usage

## Quick Start Example

### Installation

Install the NuGet package:

```powershell
Install-Package Syncfusion.Calendar.WinUI
```

### Basic Implementation

**XAML:**
```xml
<Window
    xmlns:calendar="using:Syncfusion.UI.Xaml.Calendar">
    
    <Grid>
        <calendar:SfCalendarDatePicker 
            x:Name="calendarDatePicker"
            Header="Select Date"
            PlaceholderText="Choose a date"
            SelectedDate="{x:Bind ViewModel.SelectedDate, Mode=TwoWay}"
            MinDate="2024-01-01"
            MaxDate="2024-12-31"
            DisplayDateFormat="MM/dd/yyyy" />
    </Grid>
</Window>
```

**C#:**
```csharp
using Syncfusion.UI.Xaml.Calendar;

// Create instance
SfCalendarDatePicker datePicker = new SfCalendarDatePicker();

// Configure properties
datePicker.Header = "Select Date";
datePicker.PlaceholderText = "Choose a date";
datePicker.SelectedDate = DateTimeOffset.Now;
datePicker.MinDate = new DateTimeOffset(new DateTime(2024, 1, 1));
datePicker.MaxDate = new DateTimeOffset(new DateTime(2024, 12, 31));
datePicker.DisplayDateFormat = "MM/dd/yyyy";

// Handle selection changed
datePicker.SelectedDateChanged += (s, e) =>
{
    var oldDate = e.OldDate;
    var newDate = e.NewDate;
    // Process date change
};

this.Content = datePicker;
```

## Common Patterns

### Pattern 1: Date Range Restriction

Restrict users to select dates within a specific range:

```csharp
// Only allow dates in current year
datePicker.MinDate = new DateTimeOffset(new DateTime(DateTime.Now.Year, 1, 1));
datePicker.MaxDate = new DateTimeOffset(new DateTime(DateTime.Now.Year, 12, 31));
```

### Pattern 2: Block Weekend Days

Prevent selection of weekend days:

```csharp
datePicker.CalendarItemPrepared += (s, e) =>
{
    if (e.ItemInfo.ItemType == CalendarItemType.Day &&
        (e.ItemInfo.Date.DayOfWeek == DayOfWeek.Saturday ||
         e.ItemInfo.Date.DayOfWeek == DayOfWeek.Sunday))
    {
        e.ItemInfo.IsBlackout = true;
    }
};
```

### Pattern 3: Credit Card Expiry Date Selection

Allow only month and year selection:

```xml
<calendar:SfCalendarDatePicker 
    MinDisplayMode="Year"
    MaxDisplayMode="Decade"
    DisplayDateFormat="MM/yyyy" />
```

### Pattern 4: Localized Date Picker

Create a date picker for a specific culture:

```csharp
datePicker.CalendarIdentifier = "HebrewCalendar";
datePicker.Language = "he-IL";
datePicker.FirstDayOfWeek = DayOfWeek.Sunday;
```

## Key Properties at a Glance

### Date Selection
- **SelectedDate** - Gets or sets the currently selected date
- **AllowNull** - Allows null value when no date is selected

### Date Restrictions
- **MinDate** - Minimum selectable date (default: 1/1/1920)
- **MaxDate** - Maximum selectable date (default: 12/31/2120)
- **BlackoutDates** - Collection of dates to block from selection

### Display and Formatting
- **DisplayDateFormat** - Format string for editor display (default: "d")
- **DayFormat** - Format for day numbers in calendar
- **MonthFormat** - Format for month names
- **DayOfWeekFormat** - Format for day-of-week headers
- **MonthHeaderFormat** - Format for month/year header

### Calendar Configuration
- **CalendarIdentifier** - Calendar system (Gregorian, Hebrew, Hijri, etc.)
- **FirstDayOfWeek** - First day of the week (default: Sunday)
- **NumberOfWeeksInView** - Number of weeks shown in month view (default: 6)

### Navigation and Views
- **DisplayMode** - Current view mode (Month, Year, Decade, Century)
- **MinDisplayMode** - Minimum allowed view mode
- **MaxDisplayMode** - Maximum allowed view mode

### Week Numbers
- **ShowWeekNumbers** - Displays week numbers (default: false)
- **WeekNumberRule** - Rule for first week of year (FirstDay, FirstFourDayWeek, FirstFullWeek)
- **WeekNumberFormat** - Format string for week numbers (default: "#")

### UI Customization
- **PlaceholderText** - Watermark text when no date is selected
- **OutOfScopeVisibility** - Show/hide out-of-scope dates (Enabled, Hidden)
- **DropDownWidth** - Width of drop-down calendar
- **DropDownHeight** - Height of drop-down calendar
- **SelectionHighlightMode** - Highlight style (Outline, Filled)
- **SelectionShape** - Selection shape (Circle, Rectangle)

## Additional Resources

- [Syncfusion WinUI Calendar Date Picker Documentation](https://help.syncfusion.com/winui/calendar-datepicker/getting-started)
- [GitHub Samples](https://github.com/SyncfusionExamples/syncfusion-winui-tools-calendardatepicker-examples)
- [API Reference](https://help.syncfusion.com/cr/winui/Syncfusion.UI.Xaml.Calendar.SfCalendarDatePicker.html)
