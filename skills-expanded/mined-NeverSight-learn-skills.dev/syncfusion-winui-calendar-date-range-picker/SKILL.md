---
name: syncfusion-winui-calendar-date-range-picker
description: Implements Syncfusion WinUI CalendarDateRangePicker (SfCalendarDateRangePicker) control for selecting date ranges in desktop applications. Use this when building date range pickers, range selection calendars, or start/end date input interfaces. This skill covers range selection, preset ranges, blackout dates, date restrictions, week numbers, localization, and calendar customization for WinUI applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Calendar DateRange Picker

The WinUI CalendarDateRangePicker (SfCalendarDateRangePicker) control provides an intuitive, touch-friendly interface to quickly select a date range from a drop-down calendar. It supports different date formats, date range restrictions, preset items, week numbers, localization, and extensive UI customization options.

## When to Use This Skill

Use this skill when you need to:

- **Implement date range selection** - Allow users to select a continuous range of dates (start date and end date) from a calendar
- **Add CalendarDateRangePicker to WinUI apps** - Install, configure, and use the SfCalendarDateRangePicker control
- **Configure range selection** - Set selected range programmatically, handle range change events, validate range selection
- **Restrict date selection** - Apply min/max dates, blackout specific dates, limit range duration, block weekend dates
- **Customize calendar UI** - Change drop-down alignment, customize item templates, apply themes, modify appearance
- **Support localization** - Use different calendar types (Gregorian, Hebrew, Hijri, etc.), change languages, apply RTL
- **Format date display** - Customize how dates and ranges are displayed in the editor and calendar
- **Show preset ranges** - Display predefined date ranges (This Week, This Month, Last Month, This Year, Custom Range)
- **Enable week numbers** - Show week numbers in the calendar with customizable rules and formats
- **Handle navigation** - Control view navigation (month, year, decade, century), keyboard shortcuts
- **Validate date ranges** - Ensure selected ranges meet minimum/maximum duration requirements

## Component Overview

The CalendarDateRangePicker control consists of:

- **Editor** - Text input displaying the selected date range
- **Drop-down button** - Opens the calendar drop-down
- **Drop-down calendar** - Interactive calendar for range selection with month/year/decade/century views
- **Preset items panel** - Optional list of predefined date ranges
- **Submit buttons** - Optional OK/Cancel buttons for range confirmation
- **Week numbers column** - Optional display of week numbers
- **Header and description** - Optional title and helper text

**Key capabilities:**
- Touch-friendly range selection
- Multiple calendar systems (Gregorian, Hebrew, Hijri, Korean, etc.)
- Customizable date formats
- Date range restrictions and validation
- Blackout dates support
- Preset date ranges
- Week number display
- Keyboard navigation
- Theme customization

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

**Use when:**
- Installing the CalendarDateRangePicker control for the first time
- Adding the control to XAML or C# code
- Setting the selected range programmatically or interactively
- Configuring header, description, and placeholder text
- Handling selection changed events (SelectedDateRangeChanged)
- Showing or hiding the drop-down button
- Configuring submit buttons (OK/Cancel)
- Understanding basic control structure and setup

### UI Customization
📄 **Read:** [references/ui-customization.md](references/ui-customization.md)

**Use when:**
- Changing drop-down alignment (top, bottom, left, right, center)
- Customizing drop-down calendar size
- Creating custom calendar item templates
- Highlighting special dates with custom styling
- Applying theme keys for colors and fonts
- Customizing day, week, and header appearance
- Using AttachedFlyout and DropDownFlyout for advanced customization
- Styling the CalendarItem control
- Creating event-based date decorations

### Localization and Formatting
📄 **Read:** [references/localization-formatting.md](references/localization-formatting.md)

**Use when:**
- Using different calendar types (Hebrew, Hijri, Korean, Thai, Persian, etc.)
- Changing the display language (Arabic, French, Japanese, etc.)
- Customizing editor display format (DisplayDateFormat)
- Formatting calendar days, months, and headers
- Changing the first day of the week
- Implementing right-to-left (RTL) flow direction
- Applying locale-specific date formatting
- Supporting international date conventions

### Navigation Between Views
📄 **Read:** [references/navigation.md](references/navigation.md)

**Use when:**
- Enabling navigation between month, year, decade, and century views
- Restricting navigation with MinDisplayMode and MaxDisplayMode
- Implementing view-based selection (e.g., month/year for credit cards)
- Understanding keyboard navigation shortcuts
- Controlling which views users can access
- Navigating to specific dates or view levels
- Handling view switching in code

### Restricting Date Range Selection
📄 **Read:** [references/date-restrictions.md](references/date-restrictions.md)

**Use when:**
- Setting minimum and maximum selectable dates (MinDate, MaxDate)
- Blocking specific dates using BlackoutDates collection
- Disabling weekend dates or holidays dynamically
- Using ItemPrepared event for custom date restrictions
- Limiting range duration (MinDatesCountInRange, MaxDatesCountInRange)
- Validating selected date ranges
- Preventing invalid date range selection
- Customizing display text for blocked dates

### Preset Items
📄 **Read:** [references/preset-items.md](references/preset-items.md)

**Use when:**
- Showing predefined date ranges (This Week, This Month, Last Month, This Year)
- Creating custom preset items collection
- Implementing PresetTemplate for custom preset UI
- Handling preset selection events
- Hiding calendar when preset is selected (ShowCalendar)
- Calculating date ranges for preset items
- Allowing custom range selection alongside presets

### Week Numbers
📄 **Read:** [references/week-numbers.md](references/week-numbers.md)

**Use when:**
- Enabling week number display (ShowWeekNumbers)
- Configuring week number rules (FirstDay, FirstFourDayWeek, FirstFullWeek)
- Customizing week number format with prefix/suffix
- Using WeekNumberTemplate for custom week number appearance
- Customizing WeekNameTemplate for day-of-week headers
- Understanding CalendarWeekRule options
- Applying week-based business logic

## Quick Start

### Basic Implementation

**XAML:**
```xaml
<Window xmlns:calendar="using:Syncfusion.UI.Xaml.Calendar">
    <Grid>
        <calendar:SfCalendarDateRangePicker 
            x:Name="sfCalendarDateRangePicker"
            HorizontalAlignment="Center"
            VerticalAlignment="Center"
            PlaceholderText="Select a date range" />
    </Grid>
</Window>
```

**C#:**
```csharp
using Syncfusion.UI.Xaml.Calendar;

SfCalendarDateRangePicker sfCalendarDateRangePicker = new SfCalendarDateRangePicker();
sfCalendarDateRangePicker.PlaceholderText = "Select a date range";
this.Content = sfCalendarDateRangePicker;
```

### Setting Selected Range Programmatically

```csharp
// Set a date range
sfCalendarDateRangePicker.SelectedRange = new DateTimeOffsetRange(
    new DateTimeOffset(new DateTime(2026, 3, 1)), 
    new DateTimeOffset(new DateTime(2026, 3, 15))
);

// Clear selection
sfCalendarDateRangePicker.SelectedRange = null;
```

### Handling Selection Changes

```csharp
sfCalendarDateRangePicker.SelectedDateRangeChanged += (sender, e) =>
{
    var startOld = e.RangeStartOldValue;
    var startNew = e.RangeStartNewValue;
    var endOld = e.RangeEndOldValue;
    var endNew = e.RangeEndNewValue;
    
    // Process the new range
    if (startNew.HasValue && endNew.HasValue)
    {
        TimeSpan duration = endNew.Value - startNew.Value;
        Debug.WriteLine($"Selected range: {duration.Days} days");
    }
};
```

## Common Patterns

### Pattern 1: Date Range with Restrictions

```csharp
// Restrict to future dates within 90 days
sfCalendarDateRangePicker.MinDate = DateTimeOffset.Now;
sfCalendarDateRangePicker.MaxDate = DateTimeOffset.Now.AddDays(90);
sfCalendarDateRangePicker.MinDatesCountInRange = 3;  // Minimum 3 days
sfCalendarDateRangePicker.MaxDatesCountInRange = 14; // Maximum 14 days
```

### Pattern 2: Blocking Weekend Dates

```csharp
sfCalendarDateRangePicker.ItemPrepared += (sender, e) =>
{
    if (e.ItemInfo.ItemType == CalendarItemType.Day &&
        (e.ItemInfo.Date.DayOfWeek == DayOfWeek.Saturday ||
         e.ItemInfo.Date.DayOfWeek == DayOfWeek.Sunday))
    {
        e.ItemInfo.IsBlackout = true;
    }
};
```

### Pattern 3: With Header and Description

```xaml
<calendar:SfCalendarDateRangePicker 
    Header="Travel Dates"
    Description="Select your departure and return dates"
    PlaceholderText="Choose dates"
    Width="300" />
```

### Pattern 4: Custom Display Format

```csharp
// Display as full date names
sfCalendarDateRangePicker.DisplayDateFormat = "{0:D} - {1:D}";
// Example: "Saturday, March 1, 2026 - Sunday, March 15, 2026"
```

### Pattern 5: Localized Calendar

```csharp
// Hebrew calendar with RTL support
sfCalendarDateRangePicker.CalendarIdentifier = "HebrewCalendar";
sfCalendarDateRangePicker.Language = "he-IL";
sfCalendarDateRangePicker.FlowDirection = FlowDirection.RightToLeft;
```

## Key Properties

### Selection Properties
- **SelectedRange** - Gets or sets the selected date range (DateTimeOffsetRange)
- **MinDatesCountInRange** - Minimum number of dates in the selected range
- **MaxDatesCountInRange** - Maximum number of dates in the selected range

### Restriction Properties
- **MinDate** - Minimum selectable date (default: 1/1/1920)
- **MaxDate** - Maximum selectable date (default: 12/31/2120)
- **BlackoutDates** - Collection of dates to disable

### Display Properties
- **DisplayDateFormat** - Format for displaying the selected range in the editor (default: "{0:d}-{1:d}")
- **PlaceholderText** - Watermark text when no range is selected
- **Header** - Title above the control
- **HeaderTemplate** - Custom template for the header
- **Description** - Helper text below the control

### Calendar Properties
- **CalendarIdentifier** - Calendar system (Gregorian, Hebrew, Hijri, etc.)
- **FirstDayOfWeek** - Starting day of the week
- **ShowWeekNumbers** - Display week numbers
- **WeekNumberRule** - Rule for determining first week (FirstDay, FirstFourDayWeek, FirstFullWeek)
- **WeekNumberFormat** - Format for week numbers (default: "#")

### Format Properties
- **DayFormat** - Format for day numbers in calendar
- **MonthFormat** - Format for month names in year view
- **MonthHeaderFormat** - Format for month/year header
- **DayOfWeekFormat** - Format for day-of-week names

### Navigation Properties
- **MinDisplayMode** - Minimum view level (Month, Year, Decade, Century)
- **MaxDisplayMode** - Maximum view level (Month, Year, Decade, Century)

### Drop-down Properties
- **ShowDropDownButton** - Show or hide the drop-down button
- **ShowSubmitButtons** - Show or hide OK/Cancel buttons
- **ShowCalendar** - Show or hide the calendar in drop-down
- **DropDownPlacement** - Alignment of drop-down (Bottom, Top, Left, Right, Center)
- **DropDownHeight** - Height of the drop-down calendar

### Preset Properties
- **Preset** - Collection of preset date ranges
- **PresetTemplate** - Template for displaying preset items
- **PresetPosition** - Position of preset items (Left, Right, Top, Bottom)

## Common Use Cases

1. **Booking Systems** - Hotel reservations, flight bookings, rental services
2. **Reporting Tools** - Select date ranges for reports and analytics
3. **Project Management** - Define project start and end dates, sprint planning
4. **Calendar Applications** - Event scheduling, meeting planning
5. **Financial Applications** - Select statement periods, transaction date ranges
6. **HR Systems** - Leave management, vacation planning, time tracking
7. **E-commerce** - Delivery date selection, promotional period setup
8. **Healthcare** - Appointment scheduling, treatment duration planning

## Related Skills

- [Calendar](../syncfusion-winui-calendar/) - For single date selection
- [CalendarDatePicker](../syncfusion-winui-calendar-date-picker/) - For single date picker with drop-down
