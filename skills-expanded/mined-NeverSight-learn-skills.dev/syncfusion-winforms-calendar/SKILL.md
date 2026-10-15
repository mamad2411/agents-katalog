---
name: syncfusion-winforms-calendar
description: Guides implementation of Syncfusion WinForms SfCalendar control for date selection and calendar viewing. Use this when working with calendar controls, date pickers, or multi-view calendars with Month/Year/Decade/Century views. Covers date selection modes, view navigation, date restrictions, special dates, and appearance customization for Windows Forms.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Calendars (SfCalendar)

This skill guides the implementation of Syncfusion's SfCalendar, a powerful calendar control for date selection with multiple views (Month, Year, Decade, Century), comprehensive customization options, and support for special dates, blackout dates, and date range restrictions.

## When to Use This Skill

Use this skill when you need to:
- Add a calendar control for date selection in WinForms applications
- Implement date pickers with single or multiple date selection
- Build appointment or event date selectors
- Create date range selection interfaces
- Display calendars with Month, Year, Decade, and Century views
- Restrict date selection with minimum and maximum date ranges
- Highlight special dates with custom icons and descriptions
- Block specific dates from selection using blackout dates
- Customize calendar appearance with themes and cell styling
- Localize calendars for different cultures and languages
- Implement weekend and holiday highlighting
- Build scheduling interfaces with visual date indicators

## Component Overview

**Control:** `SfCalendar`  
**Namespace:** `Syncfusion.WinForms.Input`  
**Assemblies Required:**
- `Syncfusion.Core.WinForms.dll`
- `Syncfusion.SfInput.WinForms.dll`
- `Syncfusion.Shared.Base.dll`

### Key Capabilities

The SfCalendar provides comprehensive calendar functionality:
- **Multiple Views**: Month, Year, Decade, and Century views for quick date navigation
- **Date Selection**: Single date, multiple dates, or date range selection modes
- **Date Restrictions**: MinDate and MaxDate properties to limit selectable date ranges
- **Special Dates**: Highlight important dates with custom icons and descriptions
- **Blackout Dates**: Block specific dates from selection with distinct styling
- **Appearance**: Rich theming options, cell customization, and visual styles
- **Globalization**: Culture-based localization, first day of week, date formats
- **Navigation**: Easy navigation between views with Today and None buttons
- **Accessibility**: Touch, keyboard, and mouse support for various interaction modes

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and assembly requirements
- Adding SfCalendar via designer
- Adding SfCalendar via code
- Namespace imports and basic setup
- Setting initial date value
- Complete setup example

### Date Selection
📄 **Read:** [references/date-selection.md](references/date-selection.md)
- Single date selection mode
- Multiple date selection
- Date range selection
- MinDate and MaxDate restrictions
- Blackout dates (blocking specific dates)
- Special dates with icons and descriptions
- Selection changed events
- Programmatic date selection

### Views and Navigation
📄 **Read:** [references/views-and-navigation.md](references/views-and-navigation.md)
- Month view (default view)
- Year view for month selection
- Decade view for year selection
- Century view for decade selection
- Navigating between views
- Today button functionality
- None button for clearing selection
- Header customization

### Appearance Customization
📄 **Read:** [references/appearance-customization.md](references/appearance-customization.md)
- Visual styles and themes (Office2016, Metro, etc.)
- Cell customization and styling
- Cell templates for custom rendering
- Color customization (background, foreground, borders)
- Font customization
- Weekend cell highlighting
- Current date highlighting
- Border and padding settings

### Globalization
📄 **Read:** [references/globalization.md](references/globalization.md)
- Culture and localization support
- Setting first day of week
- Date format customization
- Month and day name localization
- Right-to-left (RTL) support
- Culture-specific calendar systems

## Quick Start Example

Here's a basic calendar with date selection:

**C#:**
```csharp
using Syncfusion.WinForms.Input;
using System;
using System.Windows.Forms;

public class CalendarForm : Form
{
    private SfCalendar calendar;
    private Label lblSelected;
    
    public CalendarForm()
    {
        // Create calendar
        calendar = new SfCalendar
        {
            Location = new Point(20, 20),
            Size = new Size(350, 300)
        };
        
        // Handle selection change
        calendar.SelectedDateChanged += Calendar_SelectedDateChanged;
        
        // Create label to show selected date
        lblSelected = new Label
        {
            Location = new Point(20, 330),
            Size = new Size(350, 30),
            Text = "No date selected"
        };
        
        this.Controls.Add(calendar);
        this.Controls.Add(lblSelected);
        this.Text = "Calendar Example";
        this.Size = new Size(400, 420);
    }
    
    private void Calendar_SelectedDateChanged(object sender, EventArgs e)
    {
        if (calendar.SelectedDate.HasValue)
        {
            lblSelected.Text = $"Selected: {calendar.SelectedDate.Value:D}";
        }
    }
}
```

**VB.NET:**
```vb
Imports Syncfusion.WinForms.Input
Imports System
Imports System.Windows.Forms

Public Class CalendarForm
    Inherits Form
    
    Private calendar As SfCalendar
    Private lblSelected As Label
    
    Public Sub New()
        ' Create calendar
        calendar = New SfCalendar With {
            .Location = New Point(20, 20),
            .Size = New Size(350, 300)
        }
        
        ' Handle selection change
        AddHandler calendar.SelectedDateChanged, AddressOf Calendar_SelectedDateChanged
        
        ' Create label to show selected date
        lblSelected = New Label With {
            .Location = New Point(20, 330),
            .Size = New Size(350, 30),
            .Text = "No date selected"
        }
        
        Me.Controls.Add(calendar)
        Me.Controls.Add(lblSelected)
        Me.Text = "Calendar Example"
        Me.Size = New Size(400, 420)
    End Sub
    
    Private Sub Calendar_SelectedDateChanged(sender As Object, e As EventArgs)
        If calendar.SelectedDate.HasValue Then
            lblSelected.Text = $"Selected: {calendar.SelectedDate.Value:D}"
        End If
    End Sub
End Class
```

## Common Patterns

### Pattern 1: Date Picker with Range Restrictions

Limit selectable dates to a specific range:

**C#:**
```csharp
SfCalendar calendar = new SfCalendar();

// Restrict to future dates only (starting from today)
calendar.MinDate = DateTime.Today;
calendar.MaxDate = DateTime.Today.AddMonths(6);

// Set initial date
calendar.SelectedDate = DateTime.Today;
```

### Pattern 2: Appointment Selector with Special Dates

Highlight appointments or special dates:

**C#:**
```csharp
SfCalendar calendar = new SfCalendar();

// Add special dates (appointments, holidays, etc.)
calendar.SpecialDates.Add(new SpecialDate
{
    Date = new DateTime(2026, 3, 25),
    Description = "Team Meeting",
    IconImage = Properties.Resources.MeetingIcon
});

calendar.SpecialDates.Add(new SpecialDate
{
    Date = new DateTime(2026, 3, 28),
    Description = "Project Deadline",
    IconImage = Properties.Resources.DeadlineIcon
});
```

### Pattern 3: Multi-Select Calendar

Allow selecting multiple dates:

**C#:**
```csharp
SfCalendar calendar = new SfCalendar();

// Enable multiple selection
calendar.AllowMultipleSelection = true;

// Get selected dates
calendar.SelectionChanged += (s, e) =>
{
    var dates = calendar.SelectedDates;
    MessageBox.Show($"Selected {dates.Count} dates");
};
```

## Key Properties

| Property | Type | Description |
|----------|------|-------------|
| **SelectedDate** | `DateTime?` | Gets or sets the currently selected date |
| **SelectedDates** | `ObservableCollection<DateTime>` | Gets or sets collection of selected dates for multiple selection |
| **MinDate** | `DateTime` | Minimum selectable date |
| **MaxDate** | `DateTime` | Maximum selectable date |
| **AllowMultipleSelection** | `bool` | Enables multiple date selection |
| **ShowToday** | `bool` | Shows or hides Today button |
| **ShowNone** | `bool` | Shows or hides None button for clearing selection |
| **BlackoutDates** | `ObservableCollection<DateTime>` | Collection of dates to block from selection |
| **SpecialDates** | `ObservableCollection<SpecialDate>` | Collection of special dates with icons and descriptions |
| **Culture** | `CultureInfo` | Culture for localization and formatting |
| **FirstDayOfWeek** | `DayOfWeek` | First day of the week (Sunday, Monday, etc.) |
| **Style** | `SfCalendarStyle` | Visual style settings for appearance |

## Common Use Cases

1. **Date Picker**: Single date selection for forms and input dialogs
2. **Appointment Scheduler**: Select dates for appointments with special date highlighting
3. **Date Range Selector**: Select start and end dates for reports or bookings
4. **Holiday Calendar**: Display holidays and special events with custom icons
5. **Availability Calendar**: Block unavailable dates using blackout dates for booking systems
6. **Multi-Date Selector**: Select multiple dates for batch operations or recurring events
7. **Localized Calendar**: Display calendars in different languages and cultures for global applications

---

## Next Steps

Start with **[Getting Started](references/getting-started.md)** to install and configure the SfCalendar, then explore specific features through the navigation guide above based on your application requirements.
