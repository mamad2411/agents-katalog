---
name: syncfusion-aspnetcore-scheduler
description: Implement Syncfusion ASP.NET Core Scheduler component for scheduling appointments, events, and resource management. Use this when creating calendar scheduling solutions with appointment management, resource scheduling, multiple calendar views (day, week, month, timeline), recurring events, and CRUD operations. This skill covers data binding, timezone support, event templates, and timescale configuration.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Calendars"
---

# Implementing ASP.NET Core Scheduler

The Syncfusion ASP.NET Core Scheduler is a comprehensive component for managing appointments, events, and schedules. It provides rich functionality for creating calendar-based applications with support for multiple views, resources, recurring events, and extensive customization options.

## When to Use This Skill

- **Appointment Management:** Creating, editing, and deleting calendar appointments
- **Multi-User Scheduling:** Implementing resource scheduling for multiple users or resources
- **Calendar Views:** Displaying events in day, week, month, timeline, or agenda formats
- **Recurring Events:** Managing repeating appointments with complex recurrence rules
- **Data Integration:** Binding local or remote data sources to the Scheduler
- **Custom Templates:** Customizing event appearance and templates
- **Working Hours:** Configuring business hours, working days, and timezones
- **Event Operations:** Drag-and-drop rescheduling, resizing, and inline editing

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and NuGet package setup
- Adding Tag Helper and script resources
- Registering Script Manager
- Basic Scheduler initialization
- Populating appointments and setting default date/view

### Appointment Management
📄 **Read:** [references/appointments.md](references/appointments.md)
- Appointment data structure and field mapping
- Creating normal, all-day, spanned, and recurring events
- Appointment properties (Id, Subject, StartTime, EndTime, Location, Description)
- Recurring appointments and recurrence rules
- Exception handling for recurring events
- Drag-and-drop and inline editing

### CRUD Operations
📄 **Read:** [references/crud-operations.md](references/crud-operations.md)
- Adding appointments (editor window, addEvent method, server-side insertion)
- Editing appointments (saveEvent method, normal and recurring events)
- Deleting appointments (deleteEvent method, handling series vs occurrences)
- Handling conflicts and validation
- Server-side database operations
- Batch operations for multiple changes

### Views and Configuration
📄 **Read:** [references/views-and-modes.md](references/views-and-modes.md)
- Available view types (Day, Week, WorkWeek, Month, Year, Agenda, MonthAgenda, Timeline views)
- Setting currentView and switching between views
- View-specific configurations using e-schedule-views
- Customizing start/end hours, working days, timescales
- Date format and weekend display settings

### Scheduling Features
📄 **Read:** [references/scheduling-features.md](references/scheduling-features.md)
- Timescale configuration (interval and slot count)
- Working days and business hours setup
- Timezone support (IANA timezones)
- Recurrence patterns (RFC 5545 format)
- Resource configuration and grouping
- Complete scheduling configuration example

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Local data binding with DataSource
- Remote data binding with ODataV4Adaptor
- Custom adaptor creation
- Query parameters and filters
- AJAX data loading
- CRUD action configuration with UrlAdaptor
- Google Calendar integration

### Customization and Templates
📄 **Read:** [references/customization.md](references/customization.md)
- Event templates and cell templates
- Event customization using eventRendered event
- CSS class customization
- Tooltip templates and display options
- Custom editor window configuration
- Overlapping event prevention

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Resource grouping and multi-resource scheduling
- Timezone support and conversion
- Virtual scrolling for performance
- State persistence
- Exporting and printing
- Localization and accessibility
- Inline appointment editing
- Read-only mode and appointment blocking

## Quick Start Example

```cshtml
<!-- _Layout.cshtml -->
<head>
    <!-- refer syncfusion theme -->
    <!-- refer syncfusion script -->
</head>
<body>
    <!-- Scheduler will render here -->
    <ejs-scripts></ejs-scripts>
</body>

<!-- Index.cshtml -->
@addTagHelper *, Syncfusion.EJ2

<ejs-schedule id="schedule" width="100%" height="550" selectedDate="new DateTime(2024, 3, 28)" currentView="Week">
    <e-schedule-eventsettings dataSource="ViewBag.datasource"></e-schedule-eventsettings>
</ejs-schedule>

// Controller
public class HomeController : Controller
{
    public IActionResult Index()
    {
        ViewBag.datasource = new List<AppointmentData>
        {
            new AppointmentData { 
                Id = 1, 
                Subject = "Meeting", 
                StartTime = new DateTime(2024, 3, 28, 9, 0, 0),
                EndTime = new DateTime(2024, 3, 28, 10, 0, 0)
            }
        };
        return View();
    }
}

public class AppointmentData
{
    public int Id { get; set; }
    public string Subject { get; set; }
    public DateTime StartTime { get; set; }
    public DateTime EndTime { get; set; }
}
```

## Common Patterns

### Adding Events Programmatically
```csharp
// Use addEvent method to create appointments
<script>
var scheduleObj = document.getElementById('schedule').ej2_instances[0];
scheduleObj.addEvent({
    Id: 2,
    Subject: 'New Meeting',
    StartTime: new Date(2024, 2, 28, 10, 0),
    EndTime: new Date(2024, 2, 28, 11, 0)
});
</script>
```

### Handling CRUD Operations
```csharp
// Server-side in DataManager with CrudUrl
var dataManager = new DataManager() {
    Url = "Home/GetData",
    Adaptor = "UrlAdaptor",
    CrudUrl = "Home/UpdateData",
    // Configure server-side CORS with explicit allowed origins rather than relying on a client-side CrossDomain flag.
};
```

### Creating Recurring Events
```csharp
// RecurrenceRule follows iCalendar (RFC 5545) format
new AppointmentData {
    Id = 1,
    Subject = "Daily Standup",
    StartTime = new DateTime(2024, 3, 28, 9, 0, 0),
    EndTime = new DateTime(2024, 3, 28, 9, 30, 0),
    RecurrenceRule = "FREQ=DAILY;INTERVAL=1;COUNT=10"
}
```

### Configuring Multiple Views
```cshtml
<ejs-schedule id="schedule" currentView="Week">
    <e-schedule-views>
        <e-schedule-view option="Day"></e-schedule-view>
        <e-schedule-view option="Week"></e-schedule-view>
        <e-schedule-view option="Month"></e-schedule-view>
        <e-schedule-view option="TimelineDay"></e-schedule-view>
    </e-schedule-views>
</ejs-schedule>
```

## Key Properties and Events

### Core Scheduler Properties
- `currentView`: Active view type (Day, Week, WorkWeek, Month, Year, Agenda, MonthAgenda, TimelineDay, TimelineWeek, TimelineWorkWeek, TimelineMonth, TimelineYear)
- `selectedDate`: Current date displayed on Scheduler
- `readonly`: Disables all CRUD operations when true
- `allowDragAndDrop`: Enables drag-and-drop (default: true)
- `allowResizing`: Enables event resizing (default: true)
- `allowMultiDrag`: Enables dragging multiple events simultaneously
- `allowInline`: Enables inline editing of event subject
- `allowOverlap`: Prevents overlapping events when false
- `height` and `width`: Dimension settings
- `cssClass`: Custom CSS class for styling

### Event Settings Properties
- `dataSource`: Binds appointment data (array or DataManager)
- `template`: Custom template for event display
- `enableTooltip`: Shows tooltip for appointments
- `tooltipTemplate`: Customizes tooltip content
- `enableMaxHeight`: Events occupy full cell height
- `enableIndicator`: Shows more indicator for multiple events
- `spannedEventPlacement`: AllDayRow or TimeSlot for multi-day events
- `sortComparer`: Custom sort function for overlapping events
- `editFollowingEvents`: Allows editing current and following recurring events

### Event Field Mapping
- `id`: Unique appointment identifier (required)
- `subject`: Appointment title
- `startTime`: Start date/time (required)
- `endTime`: End date/time (required)
- `isAllDay`: All-day event flag
- `location`: Event location
- `description`: Event details
- `recurrenceRule`: Recurrence pattern (iCalendar format)
- `recurrenceID`: Parent recurring event ID for exceptions
- `recurrenceException`: Excluded dates from recurrence
- `followingID`: Parent event ID for "following events" edits
- `startTimezone`: Start time timezone (IANA timezone names)
- `endTimezone`: End time timezone
- `isReadonly`: Individual event read-only flag
- `isBlock`: Time slot blocking flag

### Important Events
- `actionBegin`: Triggered before CRUD actions
- `actionComplete`: Triggered after CRUD actions complete
- `actionFailure`: Triggered on server errors
- `eventRendered`: Triggered before event rendering (customization)
- `dragStart`: Triggered when dragging begins
- `dragStop`: Triggered when dragging ends
- `resizeStart`: Triggered when resizing begins
- `popupOpen`: Triggered before editor window opens
- `tooltipOpen`: Triggered before tooltip displays
- `dataBound`: Triggered after data binding completes

### Public Methods
- `addEvent(eventData)`: Add single or multiple appointments
- `saveEvent(eventData, action)`: Update existing appointments
- `deleteEvent(eventData, action)`: Delete appointments
- `getEvents()`: Retrieve all appointments
- `getCurrentViewEvents()`: Get appointments in current view
- `getEventDetails(element)`: Get event data from UI element
- `refreshEvents()`: Refresh appointments without full reload
- `navigateTo(date)`: Navigate to specific date
- `navigatePrevious()`: Go to previous time period
- `navigateNext()`: Go to next time period
- `isSlotAvailable(date, endDate, resourceId)`: Check slot availability
- `openOverlapAlert()`: Show overlap validation alert

## Related Skills
- [Data Binding Patterns](../data-binding/) - Connecting data sources
- [Custom Event Templates](../customization/) - Styling and presentation
- [Resource Scheduling](../advanced-features/) - Multi-user and resource management
