---
name: syncfusion-winui-scheduler
description: Implements Syncfusion WinUI Scheduler (SfScheduler) control for appointment and calendar management in desktop applications. Use this when building scheduler views, appointment booking systems, or resource scheduling in WinUI. This skill covers view types (Day, Week, Month, Timeline), appointment management, recurrence patterns, and drag-and-drop interactions.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion WinUI Scheduler (SfScheduler)

Comprehensive guide for implementing the Syncfusion® SfScheduler control in WinUI applications. SfScheduler provides a rich set of scheduling and calendar capabilities with 8+ view types, appointment management, resource grouping, and extensive customization options for managing schedules and events.

## When to Use This Skill

Use this skill immediately when the user needs to:
- Implement a calendar or scheduler component for WinUI applications
- Create appointment booking or event management interfaces
- Build meeting scheduling or time management tools
- Display events in Day, Week, Month, or Timeline views
- Handle appointment drag-and-drop or editing
- Implement resource-based scheduling (rooms, employees, equipment)
- Support recurring appointments or events
- Manage time zones for appointments
- Create calendar views with accessibility features
- Build load-on-demand appointment loading for performance

## Scheduler Overview

The **Syncfusion WinUI Scheduler (SfScheduler)** is a comprehensive calendar and scheduling control that displays appointments in multiple view types and allows users to create, edit, and manage appointments efficiently.

### Key Features

- **8 Built-in Views:** Day, Week, WorkWeek, TimelineDay, TimelineWeek, TimelineWorkWeek, TimelineMonth, and Month
- **Appointment Management:** Create, edit, delete appointments with built-in editor
- **Drag-and-Drop:** Reschedule appointments via intuitive drag-and-drop
- **Recurring Events:** Daily, weekly, monthly, yearly recurrence patterns with exceptions
- **Resource Grouping:** Group appointments by resources (people, rooms, equipment)
- **Time Zone Support:** Handle appointments across multiple time zones
- **Accessibility:** Full keyboard navigation, screen reader support, WCAG compliance
- **Localization:** Support for global date/time formats and cultures
- **Theming:** Fluent Design System with Light, Dark, and HighContrast themes
- **Load-on-Demand:** Performance optimization for large appointment datasets
- **Context Menu:** Built-in and customizable context menus
- **Reminders:** Appointment reminder notifications

### Component Identity

- **Package:** `Syncfusion.Scheduler.WinUI`
- **Namespace:** `Syncfusion.UI.Xaml.Scheduler`
- **Class:** `SfScheduler`

## Documentation and Navigation Guide

This section provides guidance on which reference file to read based on the user's needs. Each reference contains comprehensive documentation, code examples, and troubleshooting guidance.

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- NuGet package installation and setup
- Creating your first WinUI Scheduler application
- Basic scheduler initialization in XAML and C#
- Minimal working example with appointments
- ViewType configuration (Day, Week, Month, etc.)
- Setting the first day of the week
- Namespace imports and basic structure

### Appointment Management

#### Core Appointments
📄 **Read:** [references/appointments.md](references/appointments.md)
- Understanding ScheduleAppointment class and ScheduleAppointmentCollection
- Creating schedule appointments with StartTime, EndTime, Subject
- Adding appointments to the scheduler
- Custom appointment mapping with AppointmentMapping property
- Binding custom business objects to appointments
- All-day appointments with IsAllDay property
- Spanning appointments across multiple days
- Appointment ordering and internal arrangement
- Using ItemsSource for data binding

#### Appointment Editing
📄 **Read:** [references/appointment-editing.md](references/appointment-editing.md)
- Built-in appointment editor dialog
- Creating appointments through the UI
- Editing existing appointments
- Deleting appointments via editor
- Customizing the editor dialog appearance
- Validation rules for appointments
- Handling editor events
- Programmatic appointment editing

#### Appointment Drag and Drop
📄 **Read:** [references/appointment-drag-drop.md](references/appointment-drag-drop.md)
- Enabling/disabling drag-and-drop functionality
- Rescheduling appointments via drag
- Drag-and-drop events (AppointmentDragStarting, AppointmentDragOver, AppointmentDrop)
- Restricting drag-and-drop to specific views or time slots
- Visual feedback during drag operations
- Handling drag-drop validation
- Preventing specific appointments from being dragged

### View Types and Configuration

#### Day and Week Views
📄 **Read:** [references/day-week-views.md](references/day-week-views.md)
- Day view configuration with ViewType.Day
- Week view setup with ViewType.Week
- WorkWeek view (Monday-Friday) with ViewType.WorkWeek
- Customizing time intervals with TimeInterval property
- Adjusting time slot height with TimeIntervalSize
- Configuring flexible working days
- Setting non-working days with NonWorkingDays property
- Time ruler format customization
- Start and end hour configuration

#### Timeline Views
📄 **Read:** [references/timeline-views.md](references/timeline-views.md)
- TimelineDay view for horizontal day display
- TimelineWeek view for weekly timeline
- TimelineWorkWeek view for workweek timeline
- TimelineMonth view for monthly timeline
- Customizing time intervals in timeline views
- Adjusting time slot width with TimeIntervalSize
- Horizontal scrolling behavior
- Timeline-specific customization options
- Flexible working days in timeline views

#### Month View
📄 **Read:** [references/month-view.md](references/month-view.md)
- Month view configuration with ViewType.Month
- Agenda view integration
- Configuring number of weeks displayed
- Appointment indicators in month cells
- Month cell appearance customization
- Leading and trailing dates display
- Month navigation patterns
- Today date highlighting

### Navigation and Display

#### Date Navigation
📄 **Read:** [references/date-navigations.md](references/date-navigations.md)
- Navigating to specific dates programmatically
- DisplayDate property for current visible date
- Forward and backward navigation
- ViewChanged event for tracking view changes
- Handling date change events
- Programmatic view switching
- Date range validation

#### Header Customization
📄 **Read:** [references/header.md](references/header.md)
- Customizing scheduler header appearance
- Date header format customization
- Day header format configuration
- Header template customization
- Header height adjustment
- Header text styling
- View header patterns

### Resource Management

#### Resource Grouping
📄 **Read:** [references/resource-grouping.md](references/resource-grouping.md)
- Understanding resource concept (people, rooms, equipment)
- Creating SchedulerResource objects with Id, Name, Foreground, Background
- Adding resources to ResourceCollection
- Assigning appointments to resources
- ResourceGroupType.Resource for resource-based grouping
- ResourceGroupType.Date for date-based grouping
- Multiple resource support
- Resource appearance customization
- Sharing appointments across resources

### Events and Interactions

#### Scheduler Events
📄 **Read:** [references/events.md](references/events.md)
- ViewChanged event for view type changes
- CellTapped event for cell interactions
- CellDoubleTapped event for double-tap handling
- AppointmentTapped event for appointment selection
- Setting up event handlers in XAML and code
- Event argument properties and data
- Handling user interactions

#### Context Menu and Commands
📄 **Read:** [references/context-flyout-commands.md](references/context-flyout-commands.md)
- Built-in context menu functionality
- Adding custom context menu items
- Context menu commands
- Handling context menu events
- Customizing menu appearance
- Command patterns for actions

### Advanced Features

#### Time Zone Support
📄 **Read:** [references/time-zone.md](references/time-zone.md)
- Setting scheduler TimeZone property
- Appointment-specific time zones with StartTimeZone and EndTimeZone
- Display time zone configuration
- Handling daylight savings time
- Converting appointments across time zones
- Time zone display in UI
- Best practices for multi-timezone applications

#### Load-on-Demand
📄 **Read:** [references/load-on-demand.md](references/load-on-demand.md)
- Enabling load-on-demand for performance
- QueryAppointments event for dynamic loading
- Loading indicator display
- Handling large appointment datasets efficiently
- Date range-based loading
- Performance optimization techniques
- Lazy loading patterns

#### Reminders
📄 **Read:** [references/reminder.md](references/reminder.md)
- Configuring appointment reminders
- Reminder alert functionality
- Reminder window customization
- Snooze functionality
- Custom reminder intervals
- Reminder notifications

### Accessibility and Localization

#### Accessibility
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- Keyboard navigation (Tab, Arrow keys, Enter, Escape)
- Screen reader support (Narrator compatibility)
- WCAG 2.1 compliance
- Focus indicators and visual feedback
- Accessible appointment creation and editing
- High contrast theme support
- Accessibility best practices

#### Localization
📄 **Read:** [references/localization.md](references/localization.md)
- Setting up localization for scheduler
- Creating resource files (.resw) for cultures
- Culture-specific date and time formatting
- Localizing scheduler UI strings
- RTL (Right-to-Left) language support
- Multiple language support patterns

### Customization and Theming

#### Themes
📄 **Read:** [references/themes.md](references/themes.md)
- Built-in Fluent Design themes (Light, Dark, HighContrast)
- Applying themes to scheduler
- Custom theme creation
- Color customization with ThemeResource
- Overriding theme keys
- Theme resource files on GitHub
- Responsive theme switching

## Quick Start Example

Here's a minimal example to get started with the WinUI Scheduler:

### XAML Setup

```xml
<Window
    x:Class="SchedulerApp.MainWindow"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:scheduler="using:Syncfusion.UI.Xaml.Scheduler">
    
    <Grid>
        <scheduler:SfScheduler x:Name="Schedule" 
                              ViewType="Week" 
                              FirstDayOfWeek="Monday" />
    </Grid>
</Window>
```

### C# Code-Behind

```csharp
using Syncfusion.UI.Xaml.Scheduler;
using System;

namespace SchedulerApp
{
    public sealed partial class MainWindow : Window
    {
        public MainWindow()
        {
            this.InitializeComponent();
            
            // Create appointment collection
            var appointments = new ScheduleAppointmentCollection();
            
            // Add a sample appointment
            appointments.Add(new ScheduleAppointment
            {
                StartTime = DateTime.Now.Date.AddHours(10),
                EndTime = DateTime.Now.Date.AddHours(12),
                Subject = "Team Meeting",
                Location = "Conference Room A",
                Notes = "Discuss Q1 goals"
            });
            
            // Set appointments to scheduler
            Schedule.ItemsSource = appointments;
        }
    }
}
```

### Result
This creates a Week view scheduler with one appointment scheduled from 10 AM to 12 PM today.

## Common Patterns

### Pattern 1: Custom Appointment Binding

When working with custom business objects instead of `ScheduleAppointment`:

```csharp
// Custom appointment class
public class Meeting
{
    public string Title { get; set; }
    public DateTime From { get; set; }
    public DateTime To { get; set; }
    public bool AllDay { get; set; }
}
```

```xml
<scheduler:SfScheduler x:Name="Schedule" 
                      ItemsSource="{Binding Meetings}">
    <scheduler:SfScheduler.AppointmentMapping>
        <scheduler:AppointmentMapping
            Subject="Title"
            StartTime="From"
            EndTime="To"
            IsAllDay="AllDay"/>
    </scheduler:SfScheduler.AppointmentMapping>
</scheduler:SfScheduler>
```

### Pattern 2: Recurring Appointments

```csharp
var recurringAppointment = new ScheduleAppointment
{
    StartTime = DateTime.Now.Date.AddHours(9),
    EndTime = DateTime.Now.Date.AddHours(10),
    Subject = "Daily Standup",
    RecurrenceRule = "FREQ=DAILY;INTERVAL=1;COUNT=10"
};
```

### Pattern 3: Resource-Based Scheduling

```csharp
// Create resources
var resources = new ObservableCollection<SchedulerResource>
{
    new SchedulerResource 
    { 
        Id = "1", 
        Name = "Conference Room A",
        Background = new SolidColorBrush(Colors.Blue)
    },
    new SchedulerResource 
    { 
        Id = "2", 
        Name = "Conference Room B",
        Background = new SolidColorBrush(Colors.Green)
    }
};

Schedule.ResourceCollection = resources;
Schedule.ResourceGroupType = ResourceGroupType.Resource;

// Assign appointment to resource
var appointment = new ScheduleAppointment
{
    StartTime = DateTime.Now.Date.AddHours(10),
    EndTime = DateTime.Now.Date.AddHours(11),
    Subject = "Product Demo",
    ResourceIdCollection = new ObservableCollection<object> { "1" }
};
```

### Pattern 4: View Type Switching

```csharp
// Switch between views programmatically
public void SwitchToMonthView()
{
    Schedule.ViewType = SchedulerViewType.Month;
}

public void SwitchToTimelineView()
{
    Schedule.ViewType = SchedulerViewType.TimelineWeek;
}
```

### Pattern 5: Time Zone Handling

```csharp
// Set scheduler time zone
Schedule.TimeZone = TimeZoneInfo.FindSystemTimeZoneById("Pacific Standard Time");

// Appointment with specific time zones
var appointment = new ScheduleAppointment
{
    StartTime = new DateTime(2024, 3, 22, 10, 0, 0),
    EndTime = new DateTime(2024, 3, 22, 11, 0, 0),
    Subject = "Cross-timezone Meeting",
    StartTimeZone = TimeZoneInfo.FindSystemTimeZoneById("Pacific Standard Time"),
    EndTimeZone = TimeZoneInfo.FindSystemTimeZoneById("Eastern Standard Time")
};
```

## Key Properties Reference

### Essential Properties

| Property | Type | Description |
|----------|------|-------------|
| `ViewType` | `SchedulerViewType` | Sets the view type (Day, Week, Month, Timeline variants) |
| `ItemsSource` | `IEnumerable` | Data source for appointments |
| `DisplayDate` | `DateTime` | Currently displayed date in scheduler |
| `FirstDayOfWeek` | `DayOfWeek` | First day of the week (Sunday, Monday, etc.) |
| `TimeZone` | `TimeZoneInfo` | Time zone for displaying appointments |

### Appearance Properties

| Property | Type | Description |
|----------|------|-------------|
| `DaysViewSettings` | `DaysViewSettings` | Settings for Day/Week/WorkWeek views |
| `TimelineViewSettings` | `TimelineViewSettings` | Settings for Timeline views |
| `MonthViewSettings` | `MonthViewSettings` | Settings for Month view |

### Resource Properties

| Property | Type | Description |
|----------|------|-------------|
| `ResourceCollection` | `ObservableCollection<SchedulerResource>` | Collection of resources |
| `ResourceGroupType` | `ResourceGroupType` | Grouping type (None, Resource, Date) |

### Appointment Mapping

| Property | Type | Description |
|----------|------|-------------|
| `AppointmentMapping` | `AppointmentMapping` | Maps custom object properties to appointment properties |

### View-Specific Settings

**DaysViewSettings:**
- `TimeInterval` - Time slot interval (e.g., 30 minutes, 1 hour)
- `TimeIntervalSize` - Height of time slots
- `NonWorkingDays` - Days to mark as non-working

**TimelineViewSettings:**
- `TimeInterval` - Time slot interval for timeline
- `TimeIntervalSize` - Width of time slots in timeline

**MonthViewSettings:**
- `NumberOfWeeksInView` - Number of weeks to display
- `ShowAgendaView` - Show/hide agenda view

## Common Use Cases

### 1. Meeting Room Booking System
Create a resource-based scheduler showing conference room availability with drag-drop booking.

**When to use:** Building room reservation systems, equipment scheduling
**Key features:** Resource grouping, drag-drop, appointment editing

### 2. Employee Shift Scheduler
Display employee shifts across multiple days with color-coded schedules.

**When to use:** Shift planning, workforce management, retail scheduling
**Key features:** Resource grouping, Week/Month views, custom appointment colors

### 3. Doctor Appointment System
Manage patient appointments with time slots and recurring appointments.

**When to use:** Healthcare scheduling, appointment booking systems
**Key features:** Day/Week views, recurring appointments, appointment editing

### 4. Event Calendar
Display events in a monthly calendar view with event details.

**When to use:** Event management, conference scheduling, activity calendars
**Key features:** Month view, all-day events, custom appointment templates

### 5. Project Timeline
Show project milestones and tasks in a timeline view.

**When to use:** Project management, Gantt-like views, planning tools
**Key features:** Timeline views, spanning appointments, resource grouping

### 6. Multi-Timezone Scheduler
Handle appointments across different time zones for global teams.

**When to use:** Remote team coordination, international scheduling
**Key features:** Time zone support, time zone conversion, time display

**Best practices:**
- Use load-on-demand for large appointment datasets (>1000 appointments)
- Bind to `ObservableCollection` for automatic UI updates
- Implement `INotifyPropertyChanged` in custom appointment classes
- Use `AppointmentMapping` for custom business objects
- Provide clear visual feedback during drag-drop operations
- Use meaningful colors for different appointment types or resources
- Enable keyboard navigation for accessibility
- Use theme resources for consistent appearance
- Validate appointment overlaps if required by business logic
- Handle time zone conversions carefully

## Troubleshooting

### Appointments Not Showing
- Verify `ItemsSource` is properly bound
- Check that `StartTime` and `EndTime` are within visible date range
- Ensure `ViewType` is set correctly
- Confirm appointments are added to the collection

### Drag-Drop Not Working
- Check that appointments are not read-only
- Verify drag-drop is enabled (default is enabled)
- Ensure target time slot is valid for the appointment

### Resource Grouping Not Visible
- Verify `ResourceGroupType` is not set to `None`
- Check that `ResourceCollection` is populated
- Ensure appointments have correct `ResourceIdCollection` values

### Performance Issues
- Implement load-on-demand for large datasets
- Reduce the number of simultaneously visible appointments
- Optimize custom templates if used

## Next Steps

Based on the user's specific needs, guide them to the appropriate reference file from the **Documentation and Navigation Guide** section above. Each reference provides in-depth coverage with code examples, edge cases, and troubleshooting.

For general questions about WinUI components or other Syncfusion controls, refer to the parent skill:
- [Implementing Syncfusion WinUI Components](../../SKILL.md)

---

**NuGet Package:** `Syncfusion.Scheduler.WinUI`  
**Namespace:** `Syncfusion.UI.Xaml.Scheduler`  
**API Reference:** https://help.syncfusion.com/cr/winui/Syncfusion.UI.Xaml.Scheduler.html
