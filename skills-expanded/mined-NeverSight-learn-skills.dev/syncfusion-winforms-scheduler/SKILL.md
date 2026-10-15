---
name: syncfusion-winforms-scheduler
description: Guide for implementing Syncfusion Windows Forms Scheduler (Event Calendar) control for scheduling appointments and event management. Use this skill when implementing calendar functionality, appointment scheduling, or event management in Windows Forms applications. Covers schedule views, recurring appointments, calendar navigation, appointment dragging, and data binding.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Windows Forms Scheduler (Event Calendar)

The Syncfusion Windows Forms Scheduler is a comprehensive calendar control that provides scheduling functionality similar to Microsoft Outlook. It enables users to create, view, and manage appointments across multiple view types (Month, Day, Week, WorkWeek, CustomWeek) with support for recurring appointments, drag-and-drop operations, touch gestures, and extensive customization options.

## When to Use This Skill

Use this skill when you need to:

- **Build calendar and scheduling interfaces** in Windows Forms applications
- **Display appointments** in Month, Day, Week, WorkWeek, or CustomWeek views
- **Implement recurring appointments** (daily, weekly, monthly, yearly, or time-based recurrence)
- **Enable appointment CRUD operations** (Create, Read, Update, Delete) with data persistence
- **Add drag-and-drop functionality** for appointment scheduling and rescheduling
- **Customize calendar appearance** (colors, themes, headers, navigation, prime time)
- **Support touch interactions** (swipe, zoom, pan) for modern devices
- **Bind schedule data** to custom data providers or databases
- **Create Outlook-style calendar applications** with navigation calendars and time slots
- **Manage time intervals** with seconds/minutes precision for detailed scheduling

## Component Overview

The Windows Forms Scheduler control is built around the Grid control and provides:

- **Multiple View Types:** Month, Day, Week, WorkWeek, and CustomWeek views
- **Navigation Calendar:** Multi-month calendar for date selection
- **Appointment Management:** Full CRUD support with dialog-based editing
- **Recurrence Engine:** Complex recurring patterns with time-based intervals
- **Data Architecture:** Flexible data binding through interfaces (IScheduleAppointment, IScheduleDataProvider)
- **Interactive Features:** Drag-and-drop, resizing, context menus, tooltips
- **Touch Support:** Swipe scrolling, zooming, and gesture-based navigation
- **Appearance Customization:** Extensive styling options for all UI elements
- **Theme Support:** Office 2003/2007/2010, Metro, and custom themes

**Key Components:**
- **ScheduleControl:** Main user control containing all scheduling functionality
- **ScheduleAppointment:** Data object representing individual appointments
- **ScheduleDataProvider:** Base class for data management and persistence
- **NavigationCalendar:** Multi-month calendar for date navigation
- **Caption Panel:** Navigation buttons and header display
- **Navigation Panel:** Sidebar containing navigation calendar and custom controls

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and assembly deployment
- Creating ScheduleControl via designer or code
- Data binding with SimpleScheduleDataProvider
- Basic appointment CRUD operations (insert, edit, delete)
- Saving and loading appointment data
- Setting appointment text colors

### Views and Navigation
📄 **Read:** [references/views-and-navigation.md](references/views-and-navigation.md)
- Schedule view types (Month, Day, Week, WorkWeek, CustomWeek)
- Changing views programmatically and via context menu
- Navigation calendar configuration and properties
- Navigation panel and caption panel customization
- Week number display and calendar layout
- Date navigation and selection events

### Appointments and Data Management
📄 **Read:** [references/appointments-and-data.md](references/appointments-and-data.md)
- ScheduleAppointment class properties (StartTime, EndTime, Subject, Content, etc.)
- ScheduleAppointmentList collection methods
- ScheduleDataProvider base class implementation
- Data interfaces (IScheduleAppointment, IScheduleAppointmentList, IScheduleDataProvider)
- Creating custom data providers
- Drop list data (labels, markers, reminders, locations, owners)
- CommitChanges and SaveOnCloseBehavior
- NewScheduleAppointment, AddItem, RemoveItem methods

### Recurrence Appointments
📄 **Read:** [references/recurrence-appointments.md](references/recurrence-appointments.md)
- Recurrence rule syntax and format
- Rule types (Every DAY, WEEKDAY, WEEKEND, WEEK, MONTH, QUARTER, YEAR)
- Time-based recurrence (Every SEC, Every MIN, Every HR)
- AllowSecondsInAppointment property for sub-hour intervals
- Adding recurrence via appointment dialog UI
- Adding recurrence programmatically via RecurrenceRule property
- IRecurringScheduleAppointment and IRecurringScheduleDataProvider interfaces
- Complex recurrence patterns with end dates and intervals

### Customizing Appearance
📄 **Read:** [references/customizing-appearance.md](references/customizing-appearance.md)
- Appearance property and ScheduleAppearance object
- Border customization (ClickItemBorderColor, DragColor, SolidBorderColor)
- Caption and header customization
- Display item format strings for dates and times
- Navigation calendar appearance (colors, selection, today marker)
- Prime time configuration (start/end times and colors)
- Time column customization (24-hour format, font sizes, colors)
- Visual styles and Metro theme support
- ThemesEnabled property
- **ThemeChanged event:** Subscribe to ThemeChanged via `scheduleControl1.GetScheduleHost().ThemeChanged` (not directly on ScheduleControl)

### Touch and Interaction
📄 **Read:** [references/touch-and-interaction.md](references/touch-and-interaction.md)
- EnableTouchMode property for touch support
- Touch swiping (vertical scrolling and horizontal navigation)
- Touch zooming to change views
- Appointment dragging and resizing
- ItemChanging event and ItemDragHitContext
 - Use `e.ProposedItem` in ItemChanging event handlers for appointment details
- Detecting drag context (Schedule vs Calendar areas)
- Canceling drag operations based on drop location
- ItemAction enumeration

## Quick Start Example

```csharp
using System;
using System.Windows.Forms;
using Syncfusion.Windows.Forms.Schedule;

namespace SchedulerApp
{
    public partial class Form1 : Form
    {
        private ScheduleControl scheduleControl1;
        
        public Form1()
        {
            InitializeComponent();
            InitializeScheduler();
        }
        
        private void InitializeScheduler()
        {
            // Create ScheduleControl
            scheduleControl1 = new ScheduleControl();
            scheduleControl1.Location = new Point(20, 20);
            scheduleControl1.Size = new Size(800, 600);
            
            // Set up data provider
            SimpleScheduleDataProvider data = new SimpleScheduleDataProvider();
            data.MasterList = new SimpleScheduleAppointmentList();
            data.FileName = "appointments.schedule";
            
            // Configure view and data binding
            scheduleControl1.ScheduleType = ScheduleViewType.Month;
            scheduleControl1.DataSource = data;
            
            // Add to form
            this.Controls.Add(scheduleControl1);
        }
    }
}
```

## Common Patterns

### Creating and Adding Appointments

```csharp
// Get the data provider
SimpleScheduleDataProvider dataProvider = scheduleControl1.DataSource as SimpleScheduleDataProvider;

// Create new appointment
IScheduleAppointment appointment = dataProvider.NewScheduleAppointment();
appointment.StartTime = DateTime.Now.AddHours(1);
appointment.EndTime = DateTime.Now.AddHours(2);
appointment.Subject = "Team Meeting";
appointment.Content = "Discuss project milestones";
appointment.LabelValue = 2; // Business category
appointment.ForeColor = Color.Blue;

// Add to data provider
dataProvider.AddItem(appointment);

// Save changes
dataProvider.CommitChanges();
```

### Creating Recurring Appointments

```csharp
// Cast to recurring data provider
IRecurringScheduleDataProvider recurringProvider = 
    scheduleControl1.DataSource as IRecurringScheduleDataProvider;

// Create recurring appointment
IScheduleAppointment app = recurringProvider.NewScheduleAppointment();
IRecurringScheduleAppointment recurringItem = app as IRecurringScheduleAppointment;

if (recurringItem != null)
{
    recurringItem.StartTime = new DateTime(2026, 03, 24, 9, 0, 0);
    recurringItem.EndTime = new DateTime(2026, 03, 24, 10, 0, 0);
    recurringItem.Subject = "Daily Standup";
    
    // Recurrence rule: Every weekday
    recurringItem.RecurrenceRule = "03/24/2026;06/30/2026;Every WEEKDAY";
    
    // Add recurring appointments
    recurringProvider.AddNewRecurringAppointments(recurringItem, new DateTime(2026, 12, 31));
}
```

### Changing Views Programmatically

```csharp
// Switch to Day view
scheduleControl1.ScheduleType = ScheduleViewType.Day;

// Switch to Week view
scheduleControl1.ScheduleType = ScheduleViewType.Week;

// Switch to WorkWeek view (Monday-Friday)
scheduleControl1.ScheduleType = ScheduleViewType.WorkWeek;

// Switch to Month view
scheduleControl1.ScheduleType = ScheduleViewType.Month;
```

### Customizing Appearance

```csharp
// Access appearance object
ScheduleAppearance appearance = scheduleControl1.Appearance;

// Customize colors
appearance.CaptionBackColor = Color.FromArgb(0, 114, 198);
appearance.PrimeTimeCellColor = Color.LightBlue;
appearance.NonPrimeTimeCellColor = Color.White;

// Set prime time hours (9 AM to 5 PM)
appearance.PrimeTimeStart = new TimeSpan(9, 0, 0);
appearance.PrimeTimeEnd = new TimeSpan(17, 0, 0);

// Apply Metro theme
appearance.VisualStyle = Syncfusion.Windows.Forms.GridVisualStyles.Metro;

// Customize navigation calendar
appearance.NavigationCalendarBackColor = Color.White;
appearance.NavigationCalendarSelectionColor = Color.Blue;
appearance.NavigationCalendarTodayColor = Color.Red;
```

### Enabling Touch Support

```csharp
// Enable touch mode for swipe, zoom, and pan gestures
scheduleControl1.EnableTouchMode = true;

// Users can now:
// - Swipe vertically to scroll in Day/WorkWeek views
// - Swipe horizontally to navigate previous/next
// - Zoom to change view types (like Outlook)
```

### Handling Appointment Drag Events

```csharp
// Subscribe to ItemChanging event
scheduleControl1.ItemChanging += ScheduleControl1_ItemChanging;

private void ScheduleControl1_ItemChanging(object sender, ScheduleAppointmentCancelEventArgs e)
{
    if (e.Action == ItemAction.ItemDrag)
    {
        // Get drag context (Calendar or Schedule area)
        Console.WriteLine($"Dropped in: {e.ItemDragHitContext}");
        
        // Cancel drops to calendar area
        if (e.ItemDragHitContext == ItemDragHitContext.Calendar)
        {
            MessageBox.Show("Cannot drop appointments in calendar area");
            e.Cancel = true;
        }
    }
}
```

## Key Classes and Interfaces

### ScheduleControl
Main control providing scheduling functionality:
- `DataSource`: IScheduleDataProvider - Data source for appointments
- `ScheduleType`: ScheduleViewType - Current view (Month/Day/Week/WorkWeek/CustomWeek)
- `Appearance`: ScheduleAppearance - Appearance customization object
- `Calendar`: NavigationCalendar - Navigation calendar control
- `EnableAlerts`: bool - Enable appointment reminders
- `EnableTouchMode`: bool - Enable touch gestures

### ScheduleAppointment (IScheduleAppointment)
Represents individual appointments:
- `StartTime`, `EndTime`: DateTime - Appointment time range
- `Subject`: string - Appointment title
- `Content`: string - Detailed description
- `AllDay`: bool - All-day appointment flag
- `LabelValue`: int - Category/label identifier
- `MarkerValue`: int - Status marker (Free, Busy, Tentative, Out of Office)
- `ReminderValue`: int - Reminder time interval
- `LocationValue`: int - Location identifier
- `ForeColor`: Color - Text color
- `UniqueID`: int - Unique identifier
- `Owner`: int - Owner identifier for multi-user scenarios

### ScheduleDataProvider (IScheduleDataProvider)
Base class for data management:
- `GetScheduleForDay(DateTime day)`: Get appointments for specific day
- `GetSchedule(DateTime start, DateTime end)`: Get appointments in date range
- `NewScheduleAppointment()`: Create new appointment object
- `AddItem(IScheduleAppointment)`: Add appointment
- `RemoveItem(IScheduleAppointment)`: Remove appointment
- `CommitChanges()`: Save modifications
- `SaveOnCloseBehaviorAction`: Auto-save behavior on control disposal

## Common Use Cases

1. **Outlook-Style Calendar Application**
   - Monthly view with navigation calendar
   - Appointment creation via double-click
   - Drag-and-drop rescheduling
   - Recurring meeting support

2. **Resource Scheduling System**
   - Day/Week views for resource allocation
   - Color-coded appointments by resource type
   - Drag-to-assign functionality
   - Time slot management with custom intervals

3. **Event Management Application**
   - Multi-day event display in Month view
   - All-day event support
   - Event categorization with labels
   - Custom location and reminder configuration

4. **Healthcare Appointment System**
   - WorkWeek view for doctor schedules
   - 15-minute time intervals
   - Patient appointment tracking
   - Recurring appointment patterns (weekly checkups)

5. **Time Tracking and Logging**
   - Minute/second precision with AllowSecondsInAppointment
   - Custom data provider for database integration
   - Time-based recurrence (every N minutes/hours)
   - Detailed time column customization

6. **Touch-Enabled Tablet Scheduling**
   - EnableTouchMode for tablet devices
   - Swipe navigation between dates
   - Zoom gestures to change views
   - Touch-friendly appointment editing

## Related Skills

- [Implementing Data Grids](../../grids/implementing-data-grids/) - For appointment list views
- [Implementing Date Pickers](../implementing-date-pickers/) - For date selection UI components
- [Implementing Calendars](../implementing-calendars/) - For standalone calendar components

## Next Steps

Start with **[Getting Started](references/getting-started.md)** to install and configure the Scheduler control, then explore specific features through the navigation guide above based on your application requirements.