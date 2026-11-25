---
name: syncfusion-angular-scheduler
description: Implement and configure Syncfusion Angular Scheduler (Schedule) component for calendar and event management. Use this when building schedulers, calendar systems, event management applications, appointment booking interfaces, or resource scheduling solutions. This skill covers timeline views, day/week/month views, recurring events, time slot management, and working hours configuration.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Calendars"
---

# Implementing Syncfusion Angular Scheduler

A comprehensive guide for implementing the Syncfusion Angular Scheduler component for event and appointment management with multiple view modes, resource grouping, timezone support, and extensive customization options.

## When to Use This Skill

Use this skill when you need to:

- **Event and Appointment Management**: Create calendar applications with event scheduling, editing, and management
- **Resource Scheduling**: Manage multiple resources (rooms, equipment, people) with grouping and filtering
- **Timeline Views**: Display events in horizontal timeline format for project planning or resource allocation
- **Booking Systems**: Build appointment booking interfaces for healthcare, salon, or meeting room management
- **Calendar Applications**: Implement full-featured calendar systems with recurring events and reminders
- **Multi-Timezone Support**: Handle events across different timezones for global teams
- **Work Hour Management**: Configure working days, hours, and holidays for business applications

## Component Overview

The **Syncfusion Angular Scheduler** (ejs-schedule) is a feature-rich calendar and event management component that provides:

- **11+ View Modes**: Day, Week, WorkWeek, Month, Year, Agenda, MonthAgenda, Timeline variants
- **Event Types**: Normal, spanned, all-day, and recurring events with complex recurrence patterns
- **Data Binding**: Local and remote data with CRUD operations, DataManager integration
- **Resource Management**: Single and multiple resource grouping with custom templates
- **Time Configuration**: Customizable timescale, timezone support, working hours/days
- **Rich Customization**: Cell templates, editor templates, event templates, custom styling
- **Advanced Features**: Drag-drop, resize, clipboard operations, virtual scrolling, export (ICS/Excel/PDF)
- **Accessibility**: WCAG 2.1 compliant with keyboard navigation and screen reader support
- **Localization**: Multi-language and RTL support

**Package**: `@syncfusion/ej2-angular-schedule`

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

Read this reference when you need to:
- Install and set up the Angular Scheduler package
- Configure module registration and view services (Day, Week, Month, Agenda, Timeline)
- Create your first scheduler with basic configuration
- Add CSS theme imports
- Understand component initialization

### Views and Display Configuration
📄 **Read:** [references/views-and-display.md](references/views-and-display.md)

Read this reference when you need to:
- Configure available view modes (Day, Week, WorkWeek, Month, Year, Agenda)
- Set up Timeline views (TimelineDay, TimelineWeek, TimelineMonth, TimelineYear)
- Switch between different views programmatically
- Customize view-specific settings and intervals
- Configure calendar mode and display options
- Handle view navigation

### Events and Appointments
📄 **Read:** [references/appointments.md](references/appointments.md)

Read this reference when you need to:
- Understand event types (normal, spanned, all-day, recurring)
- Define event data structure and required fields
- Create and render events programmatically
- Configure event templates and custom rendering
- Handle event interactions (click, double-click, hover)
- Add custom fields to events

### Data Binding and CRUD Operations
📄 **Read:** [references/data-binding.md](references/data-binding.md)

Read this reference when you need to:
- Bind local data (arrays) to the scheduler
- Connect to remote data sources (OData, Web API, REST services)
- Use DataManager for advanced data operations
- Configure field mapping for custom data structures
- Implement CRUD operations (Create, Read, Update, Delete)
- Handle data adapters and custom queries

### Resources and Grouping
📄 **Read:** [references/resources.md](references/resources.md)

Read this reference when you need to:
- Configure single or multiple resources (rooms, employees, equipment)
- Set up resource grouping (by date or by resource)
- Customize resource colors and styling
- Create resource templates
- Filter and manage resource visibility
- Handle resource-based events

### Time Configuration
📄 **Read:** [references/time-configuration.md](references/time-configuration.md)

Read this reference when you need to:
- Configure timescale intervals and time slots
- Set start and end hours for day views
- Define working days and working hours
- Handle timezone support and conversions
- Manage multiple timezones
- Customize time formats and display

### Editor Customization
📄 **Read:** [references/editor-customization.md](references/editor-customization.md)

Read this reference when you need to:
- Customize the event editor dialog
- Create custom editor templates
- Add custom fields to the editor
- Configure editor validation rules
- Customize quick info popups
- Handle editor events

### Cell Customization
📄 **Read:** [references/cell-customization.md](references/cell-customization.md)

Read this reference when you need to:
- Create cell templates for custom rendering
- Customize date header templates
- Style time cells and work cells
- Configure month cell templates
- Create resource header templates
- Add custom content to cells

### Recurrence Editor
📄 **Read:** [references/recurrence-editor.md](references/recurrence-editor.md)

Read this reference when you need to:
- Understand recurrence rule format (RRULE)
- Configure recurrence patterns (Daily, Weekly, Monthly, Yearly)
- Use the standalone recurrence editor component
- Handle FREQ, INTERVAL, BYDAY, BYMONTHDAY parameters
- Manage exception dates (EXDATE)
- Edit recurring event series or single occurrences

### Header Customization
📄 **Read:** [references/header-customization.md](references/header-customization.md)

Read this reference when you need to:
- Customize the header toolbar
- Add or remove toolbar items
- Create custom toolbar buttons
- Configure header rows
- Customize date range display
- Handle header events

### Clipboard Operations
📄 **Read:** [references/clipboard-operations.md](references/clipboard-operations.md)

Read this reference when you need to:
- Enable copy (Ctrl+C), cut (Ctrl+X), paste (Ctrl+V) operations
- Configure clipboard settings
- Create custom clipboard actions
- Handle clipboard events

### Exporting and Printing
📄 **Read:** [references/exporting.md](references/exporting.md)

Read this reference when you need to:
- Export events to ICS/iCal format
- Export scheduler to Excel
- Export scheduler to PDF
- Configure export options
- Implement print functionality

### Styling and Themes
📄 **Read:** [references/styling-themes.md](references/styling-themes.md)

Read this reference when you need to:
- Apply built-in themes (Material, Bootstrap, Fabric, etc.)
- Customize component styling with CSS
- Configure custom event colors
- Style cells and views
- Create responsive designs

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)

Read this reference when you need to:
- Enable virtual scrolling for large datasets
- Configure lazy loading
- Set component dimensions (height, width)
- Enable row auto-height
- Handle drag-and-drop operations
- Resize events
- Manage multiple scheduler instances

### State Persistence
📄 **Read:** [references/state-persistence.md](references/state-persistence.md)

Read this reference when you need to:
- Enable state persistence
- Configure which properties to persist
- Use localStorage integration
- Restore previous state
- Clear persisted state

### Accessibility
📄 **Read:** [references/accessibility.md](references/accessibility.md)

Read this reference when you need to:
- Implement WCAG 2.1 compliance
- Configure keyboard navigation
- Set up ARIA attributes
- Support screen readers
- Manage focus states
- Use high contrast themes

### Localization and Internationalization
📄 **Read:** [references/localization.md](references/localization.md)

Read this reference when you need to:
- Set up multi-language support
- Load culture files
- Enable RTL (Right-to-Left) support
- Customize date/time formatting
- Create custom localizations

## Quick Start Example

Here's a minimal working example to get started with the Angular Scheduler:

```typescript
import { Component } from '@angular/core';
import { ScheduleModule, EventSettingsModel, View } from '@syncfusion/ej2-angular-schedule';
import { DayService, WeekService, WorkWeekService, MonthService, AgendaService } from '@syncfusion/ej2-angular-schedule';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ScheduleModule],
  providers: [DayService, WeekService, WorkWeekService, MonthService, AgendaService],
  template: `
    <ejs-schedule 
      width='100%' 
      height='550px'
      [selectedDate]="selectedDate"
      [eventSettings]="eventSettings">
    </ejs-schedule>
  `
})
export class AppComponent {
  public selectedDate: Date = new Date(2024, 0, 15);
  public eventSettings: EventSettingsModel = {
    dataSource: [
      {
        Id: 1,
        Subject: 'Team Meeting',
        StartTime: new Date(2024, 0, 15, 10, 0),
        EndTime: new Date(2024, 0, 15, 11, 30)
      },
      {
        Id: 2,
        Subject: 'Project Review',
        StartTime: new Date(2024, 0, 15, 14, 0),
        EndTime: new Date(2024, 0, 15, 15, 30)
      }
    ]
  };
}
```

**CSS Import** (in styles.css):
```css
@import '../node_modules/@syncfusion/ej2-base/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-calendars/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-dropdowns/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-inputs/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-lists/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-popups/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-navigations/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-angular-schedule/styles/material3.css';
```

## Common Patterns

### Pattern 1: Scheduler with Multiple Views

```typescript
import { Component } from '@angular/core';
import { ScheduleModule, View } from '@syncfusion/ej2-angular-schedule';
import { DayService, WeekService, MonthService, TimelineViewsService, TimelineMonthService } from '@syncfusion/ej2-angular-schedule';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ScheduleModule],
  providers: [DayService, WeekService, MonthService, TimelineViewsService, TimelineMonthService],
  template: `
    <ejs-schedule 
      width='100%' 
      height='550px'
      [currentView]="currentView"
      [views]="views"
      [eventSettings]="eventSettings">
    </ejs-schedule>
  `
})
export class AppComponent {
  public currentView: View = 'Week';
  public views: View[] = ['Day', 'Week', 'Month', 'TimelineWeek', 'TimelineMonth'];
  public eventSettings: object = { dataSource: [] };
}
```

### Pattern 2: Scheduler with Resources

```typescript
import { Component } from '@angular/core';
import { ScheduleModule, EventSettingsModel, GroupModel } from '@syncfusion/ej2-angular-schedule';
import { WeekService, MonthService } from '@syncfusion/ej2-angular-schedule';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ScheduleModule],
  providers: [WeekService, MonthService],
  template: `
    <ejs-schedule 
      width='100%' 
      height='550px'
      [group]="group"
      [eventSettings]="eventSettings">
      <e-resources>
        <e-resource 
          field='RoomId' 
          title='Room' 
          name='Rooms' 
          [dataSource]='roomDataSource'
          textField='RoomText' 
          idField='Id' 
          colorField='RoomColor'>
        </e-resource>
      </e-resources>
    </ejs-schedule>
  `
})
export class AppComponent {
  public group: GroupModel = { resources: ['Rooms'] };
  
  public roomDataSource: object[] = [
    { RoomText: 'Room 1', Id: 1, RoomColor: '#cb6bb2' },
    { RoomText: 'Room 2', Id: 2, RoomColor: '#56ca85' }
  ];

  public eventSettings: EventSettingsModel = {
    dataSource: [
      {
        Id: 1,
        Subject: 'Meeting',
        StartTime: new Date(2024, 0, 15, 10, 0),
        EndTime: new Date(2024, 0, 15, 11, 0),
        RoomId: 1
      }
    ]
  };
}
```

### Pattern 3: Remote Data Binding

```typescript
import { Component } from '@angular/core';
import { ScheduleModule, EventSettingsModel } from '@syncfusion/ej2-angular-schedule';
import { DataManager, WebApiAdaptor } from '@syncfusion/ej2-data';
import { WeekService, MonthService } from '@syncfusion/ej2-angular-schedule';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ScheduleModule],
  providers: [WeekService, MonthService],
  template: `
    <ejs-schedule 
      width='100%' 
      height='550px'
      [eventSettings]="eventSettings">
    </ejs-schedule>
  `
})
export class AppComponent {
  private dataManager: DataManager = new DataManager({
    url: 'https://js.syncfusion.com/demos/ejservices/api/Schedule/LoadData',
    adaptor: new WebApiAdaptor(),
    crossDomain: true
  });

  public eventSettings: EventSettingsModel = {
    dataSource: this.dataManager
  };
}
```

### Pattern 4: Recurring Events

```typescript
import { Component } from '@angular/core';
import { ScheduleModule, EventSettingsModel } from '@syncfusion/ej2-angular-schedule';
import { WeekService, MonthService } from '@syncfusion/ej2-angular-schedule';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ScheduleModule],
  providers: [WeekService, MonthService],
  template: `
    <ejs-schedule 
      width='100%' 
      height='550px'
      [eventSettings]="eventSettings">
    </ejs-schedule>
  `
})
export class AppComponent {
  public eventSettings: EventSettingsModel = {
    dataSource: [
      {
        Id: 1,
        Subject: 'Daily Standup',
        StartTime: new Date(2024, 0, 15, 9, 0),
        EndTime: new Date(2024, 0, 15, 9, 30),
        RecurrenceRule: 'FREQ=DAILY;INTERVAL=1;COUNT=10' // Repeats daily for 10 days
      },
      {
        Id: 2,
        Subject: 'Weekly Review',
        StartTime: new Date(2024, 0, 15, 14, 0),
        EndTime: new Date(2024, 0, 15, 15, 0),
        RecurrenceRule: 'FREQ=WEEKLY;BYDAY=MO;INTERVAL=1' // Every Monday
      }
    ]
  };
}
```

## Key Configuration Options

### Core Properties

| Property | Type | Description |
|----------|------|-------------|
| `currentView` | View | Active view mode (Day, Week, Month, etc.) |
| `selectedDate` | Date | Currently selected date |
| `eventSettings` | EventSettingsModel | Event data source and field mappings |
| `views` | View[] | Array of views to display in the scheduler |
| `height` | string | Scheduler height (e.g., '550px', '100%') |
| `width` | string | Scheduler width (e.g., '100%', '800px') |

### Event Settings

| Property | Type | Description |
|----------|------|-------------|
| `dataSource` | object[] \| DataManager | Event data source |
| `fields` | FieldModel | Field mapping for custom data structure |
| `enableTooltip` | boolean | Enable event tooltips |
| `template` | string | Custom event template |

### View Services (Must inject in providers)

- `DayService` - Day view
- `WeekService` - Week view
- `WorkWeekService` - Work week view
- `MonthService` - Month view
- `YearService` - Year view
- `AgendaService` - Agenda view
- `MonthAgendaService` - Month agenda view
- `TimelineViewsService` - Timeline day, week, work week views
- `TimelineMonthService` - Timeline month view
- `TimelineYearService` - Timeline year view

### Common Events

| Event | Description |
|-------|-------------|
| `eventClick` | Triggered when an event is clicked |
| `cellClick` | Triggered when a cell is clicked |
| `cellDoubleClick` | Triggered when a cell is double-clicked |
| `popupOpen` | Triggered before editor/quick info popup opens |
| `actionBegin` | Triggered before CRUD operations |
| `actionComplete` | Triggered after CRUD operations |
| `dataBinding` | Triggered before data binding |
| `dataBound` | Triggered after data binding |

## Common Use Cases

### 1. Appointment Booking System
Create a booking interface for healthcare, salons, or services with resource management, time slots, and availability checking.

**Read**: getting-started.md, resources.md, time-configuration.md

### 2. Meeting Room Scheduler
Manage multiple meeting rooms with resource grouping, conflict detection, and availability display.

**Read**: resources.md, appointments.md, data-binding.md

### 3. Project Timeline
Display project tasks in timeline views with drag-drop, resize, and milestone tracking.

**Read**: views-and-display.md, advanced-features.md, appointments.md

### 4. Team Calendar
Create a shared team calendar with recurring events, multiple timezones, and resource filtering.

**Read**: appointments.md, recurrence-editor.md, time-configuration.md, resources.md

### 5. Employee Shift Planning
Plan and manage employee shifts with working hours, multiple resources, and timeline views.

**Read**: time-configuration.md, resources.md, views-and-display.md

### 6. Event Management Portal
Build event management systems with export to calendar apps (ICS), custom editor forms, and templates.

**Read**: appointments.md, editor-customization.md, exporting.md

### 7. Multi-Timezone Calendar
Handle events across different timezones for global teams with timezone conversion and display.

**Read**: time-configuration.md, appointments.md

### 8. Custom Calendar Application
Create fully customized calendar applications with custom cells, templates, and styling.

**Read**: cell-customization.md, editor-customization.md, styling-themes.md
