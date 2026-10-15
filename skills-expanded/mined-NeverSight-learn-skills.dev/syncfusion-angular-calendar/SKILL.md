---
name: syncfusion-angular-calendar
description: Comprehensive guide for implementing the Syncfusion Angular Calendar component. Use this when working with date selection, multi-date selection, month/year/decade views, or calendar navigation in Angular applications. Covers Calendar API, events, styling, and accessibility.
metadata:
  author: "Syncfusion Inc"
  category: "Calendars"
  version: "33.1.44"
---

# Implementing Syncfusion Angular Calendar

A comprehensive guide for implementing the Syncfusion Essential JS 2 Calendar component in Angular applications. Learn to create date pickers, manage calendar views, handle events, and customize styling.

## Calendar Overview

The Syncfusion Angular Calendar component is a date selection widget that provides:

- **Multiple calendar views:** Month (default), Year, and Decade views with smooth navigation
- **Date selection modes:** Single date or multiple dates with `isMultiSelection` property
- **Navigation control:** `navigateTo()` method for programmatic view switching
- **Date manipulation methods:** `addDate()` and `removeDate()` for multi-selection management
- **Comprehensive event system:** change, created, navigated, renderDayCell, destroyed events
- **Localization support:** Locale-specific formatting, day header formats, first day of week
- **Accessibility:** Full WCAG 2.2 compliance, keyboard navigation, RTL support
- **Rich customization:** CSS classes, custom rendering, day cell customization
- **Persistence:** Optional state persistence across page reloads

**Package:** `@syncfusion/ej2-angular-calendars`

## Documentation Navigation

Read the following references based on your specific needs:

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Package installation and module setup
- CSS theme imports and dependencies
- Basic calendar implementation
- Component initialization in Angular
- Running and testing setup

### Calendar Views
📄 **Read:** [references/calendar-views.md](references/calendar-views.md)
- Month view (default display)
- Year view implementation
- Decade view implementation
- View navigation and transitions
- `start` property usage
- `depth` property for restricting views

### Date Selection
📄 **Read:** [references/date-selection.md](references/date-selection.md)
- Single date selection
- Multiple date selection (`isMultiSelection`)
- `value` property for single dates
- `values` array for multiple dates
- Min/max date constraints
- Date range validation

### Events & Methods
📄 **Read:** [references/events-and-methods.md](references/events-and-methods.md)
- Event handlers (change, created, navigated, renderDayCell, destroyed)
- `addDate()` method for multi-selection
- `removeDate()` method for multi-selection
- `navigateTo()` for programmatic navigation
- `currentView()` to get active view
- `getPersistData()` to retrieve persistence data
- `destroy()` to destroy the calendar widget
- RenderDayCell for custom day styling

### Calendar Navigation
📄 **Read:** [references/calendar-navigation.md](references/calendar-navigation.md)
- Month navigation controls
- Year and Decade view switching
- Today button (`showTodayButton`)
- `firstDayOfWeek` property
- Week number display (`weekNumber`)
- Keyboard shortcuts and navigation

### Accessibility & Globalization
📄 **Read:** [references/accessibility-and-globalization.md](references/accessibility-and-globalization.md)
- WCAG 2.2 and Section 508 compliance
- WAI-ARIA attributes and roles
- Keyboard navigation (arrows, enter, spacebar)
- Screen reader compatibility
- Localization (locale property)
- Day header formats (Short, Narrow, Abbreviated, Wide)
- RTL (Right-to-Left) support

### Styling & Customization
📄 **Read:** [references/styling-and-customization.md](references/styling-and-customization.md)
- CSS class customization (.e-calendar, .e-day-cell, .e-selected)
- Theme selection (Material, Bootstrap, Tailwind, Fabric)
- Dark mode implementation
- Custom day cell styling via renderDayCell
- Disabled dates styling
- Hover and focus states

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete property reference (value, values, isMultiSelection, min, max, start, depth, showTodayButton, locale, dayHeaderFormat, weekNumber, weekRule, firstDayOfWeek, cssClass, enableRtl, enabled, calendarMode, keyConfigs, enablePersistence, serverTimezoneOffset)
- All method signatures with examples (addDate, removeDate, navigateTo, currentView, getPersistData, destroy)
- Event argument types (ChangedEventArgs, NavigatedEventArgs, RenderDayCellEventArgs)
- Key configurations for keyboard shortcuts
- Calendar modes (Gregorian, Islamic)
- Return types and descriptions

## Quick Start Example

```typescript
// app.component.ts
import { Component } from '@angular/core';
import { ChangedEventArgs } from '@syncfusion/ej2-calendars';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  // Single date selection
  selectedDate: Date = new Date();
  
  // Multiple date selection
  selectedDates: Date[] = [
    new Date(2026, 2, 15),
    new Date(2026, 2, 20),
    new Date(2026, 2, 25)
  ];
  
  // Calendar configuration
  minDate: Date = new Date(2020, 0, 1);
  maxDate: Date = new Date(2030, 11, 31);
  
  // Event handler
  onCalendarChange(args: ChangedEventArgs): void {
    console.log('Selected date:', args.value);
  }
}
```

```html
<!-- app.component.html -->
<div style="padding: 20px; font-family: Arial, sans-serif;">
  <h2>Single Date Selection</h2>
  <ejs-calendar 
    [(ngModel)]="selectedDate"
    [min]="minDate"
    [max]="maxDate"
    (change)="onCalendarChange($event)">
  </ejs-calendar>
  <p>Selected: {{ selectedDate | date:'medium' }}</p>

  <h2>Multiple Date Selection</h2>
  <ejs-calendar 
    [(ngModel)]="selectedDates"
    [isMultiSelection]="true"
    [showTodayButton]="true">
  </ejs-calendar>
  <p>Selected dates: {{ selectedDates.length }} dates</p>
</div>
```

```css
/* app.component.css */
@import '../node_modules/@syncfusion/ej2-base/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-calendars/styles/material3.css';

:host ::ng-deep .e-calendar {
  margin: 20px 0;
}

:host ::ng-deep .e-selected {
  background-color: #3f51b5;
  color: white;
}
```

## Common Patterns

### Pattern 1: Custom Date Range (Two Calendar Instances)

The Calendar component does not have built-in range selection. Use two separate Calendar instances with `min`/`max` constraints and the `change` event to implement a custom date range picker:

```typescript
export class AppComponent {
  startDate: Date = new Date();
  endDate: Date = new Date();
  
  onStartDateChange(args: ChangedEventArgs): void {
    this.startDate = args.value;
    // Ensure end date is not before start date
    if (this.endDate < this.startDate) {
      this.endDate = this.startDate;
    }
  }
  
  onEndDateChange(args: ChangedEventArgs): void {
    this.endDate = args.value;
  }
  
  getDaysInRange(): number {
    const timeDiff = this.endDate.getTime() - this.startDate.getTime();
    return Math.ceil(timeDiff / (1000 * 3600 * 24)) + 1;
  }
}
```

```html
<!-- Two separate Calendar instances for range selection -->
<ejs-calendar [(ngModel)]="startDate" (change)="onStartDateChange($event)"></ejs-calendar>
<ejs-calendar [(ngModel)]="endDate" [min]="startDate" (change)="onEndDateChange($event)"></ejs-calendar>
```

> **Note:** For a built-in range picker, use the [`DateRangePicker`](../implementing-daterangepicker/SKILL.md) component instead.

### Pattern 2: Calendar with Disabled Dates

Disable specific dates (weekends, holidays) using renderDayCell event:

```typescript
export class AppComponent {
  holidays: Date[] = [
    new Date(2026, 11, 25), // Christmas
    new Date(2026, 0, 1),   // New Year
  ];
  
  onRenderDayCell(args: RenderDayCellEventArgs): void {
    // Disable weekends
    if (args.date.getDay() === 0 || args.date.getDay() === 6) {
      args.isDisabled = true;
    }
    
    // Disable holidays
    if (this.isHoliday(args.date)) {
      args.isDisabled = true;
    }
  }
  
  private isHoliday(date: Date): boolean {
    return this.holidays.some(holiday => 
      holiday.toDateString() === date.toDateString()
    );
  }
}
```

### Pattern 3: Multi-Selection with Add/Remove

Manage multiple selected dates programmatically:

```typescript
export class AppComponent {
  @ViewChild('calendar') calendarRef!: CalendarComponent;
  selectedDates: Date[] = [];
  
  addDateToSelection(date: Date): void {
    // Check if already selected
    if (!this.selectedDates.some(d => 
        d.toDateString() === date.toDateString())) {
      this.calendarRef.addDate(date);
    }
  }
  
  removeDateFromSelection(date: Date): void {
    this.calendarRef.removeDate(date);
  }
  
  clearAllDates(): void {
    if (this.selectedDates.length > 0) {
      this.calendarRef.removeDate(this.selectedDates);
    }
  }
}
```

### Pattern 4: Year/Decade View Navigation

Implement navigation to different calendar views:

```typescript
export class AppComponent {
  @ViewChild('calendar') calendarRef!: CalendarComponent;
  
  navigateToYear(year: number): void {
    const dateInYear = new Date(year, 0, 1);
    this.calendarRef.navigateTo('Year', dateInYear);
  }
  
  navigateToDecade(startYear: number): void {
    const dateInDecade = new Date(startYear, 0, 1);
    this.calendarRef.navigateTo('Decade', dateInDecade);
  }
  
  getCurrentView(): string {
    return this.calendarRef.currentView();
  }
}
```

### Pattern 5: Reactive Form Integration

Integrate Calendar with Angular Reactive Forms:

```typescript
export class AppComponent implements OnInit {
  dateForm: FormGroup;
  
  constructor(private fb: FormBuilder) {
    this.dateForm = this.fb.group({
      eventDate: [new Date(), Validators.required],
      eventName: ['', Validators.required]
    });
  }
  
  ngOnInit(): void {
    // Subscribe to date changes
    this.dateForm.get('eventDate')?.valueChanges.subscribe(date => {
      console.log('Event date changed:', date);
    });
  }
  
  submitForm(): void {
    if (this.dateForm.valid) {
      console.log('Form values:', this.dateForm.value);
    }
  }
}
```

```html
<form [formGroup]="dateForm" (ngSubmit)="submitForm()">
  <div>
    <label for="eventDate">Event Date:</label>
    <ejs-calendar 
      id="eventDate"
      formControlName="eventDate">
    </ejs-calendar>
  </div>
  
  <div>
    <label for="eventName">Event Name:</label>
    <input 
      id="eventName"
      type="text"
      formControlName="eventName">
  </div>
  
  <button type="submit" [disabled]="!dateForm.valid">Submit</button>
</form>
```

## Key Props Reference

| Prop | Type | Description | Example |
|------|------|-------------|---------|
| `value` | `Date` | Single selected date | `[value]="selectedDate"` |
| `values` | `Date[]` | Multiple selected dates | `[values]="selectedDates"` |
| `isMultiSelection` | `boolean` | Enable multiple date selection | `[isMultiSelection]="true"` |
| `min` | `Date` | Minimum selectable date | `[min]="minDate"` |
| `max` | `Date` | Maximum selectable date | `[max]="maxDate"` |
| `start` | `CalendarView` | Initial view (Month/Year/Decade) | `start="Month"` |
| `depth` | `CalendarView` | Maximum view level | `depth="Month"` |
| `showTodayButton` | `boolean` | Display today button | `[showTodayButton]="true"` |
| `locale` | `string` | Culture/language code | `locale="fr-FR"` |
| `dayHeaderFormat` | `DayHeaderFormats` | Day format (Short/Narrow/Abbreviated/Wide) | `dayHeaderFormat="Abbreviated"` |
| `weekNumber` | `boolean` | Show week numbers | `[weekNumber]="true"` |
| `weekRule` | `WeekRule` | Rule for first week of year (FirstDay/FirstFullWeek/FirstFourDayWeek) | `weekRule="FirstFourDayWeek"` |
| `firstDayOfWeek` | `number` | First day (0=Sunday, 1=Monday) | `[firstDayOfWeek]="1"` |
| `cssClass` | `string` | Custom CSS classes | `cssClass="custom-calendar"` |
| `enableRtl` | `boolean` | Enable RTL layout | `[enableRtl]="true"` |
| `enabled` | `boolean` | Enable/disable component | `[enabled]="true"` |
| `calendarMode` | `CalendarType` | Calendar mode (Gregorian/Islamic) | `calendarMode="Islamic"` |
| `keyConfigs` | `{ [key: string]: string }` | Custom keyboard shortcuts | `[keyConfigs]="keyConfigs"` |
| `enablePersistence` | `boolean` | Persist state across page reloads | `[enablePersistence]="true"` |
| `serverTimezoneOffset` | `number \| null` | Server timezone offset for initial date processing | `[serverTimezoneOffset]="330"` |

## Common Use Cases

**Use Case 1: Event Booking System**
- User selects start and end dates for event
- Disable past dates and weekends
- Solution: Combine min/max dates with renderDayCell for disable logic
- Reference: [Calendar Views](references/calendar-views.md) + [Events & Methods](references/events-and-methods.md)

**Use Case 2: Conference Schedule**
- Display multiple highlighted dates (conference days)
- Allow year/decade navigation for planning
- Solution: Use isMultiSelection, highlight dates, navigate between views
- Reference: [Date Selection](references/date-selection.md) + [Calendar Navigation](references/calendar-navigation.md)

**Use Case 3: Accessible Booking Form**
- Calendar integrated in form with keyboard navigation
- Screen reader compatible, WCAG 2.2 compliant
- Solution: Use Reactive Forms + Calendar events
- Reference: [Accessibility & Globalization](references/accessibility-and-globalization.md)

**Use Case 4: International Date Picker**
- Support multiple languages and date formats
- Show RTL for Arabic, Hebrew
- Solution: Use locale property and localization
- Reference: [Accessibility & Globalization](references/accessibility-and-globalization.md)

**Use Case 5: Dynamic Date Constraints**
- Disable dates based on business logic (availability, holidays)
- Update constraints based on user selections
- Solution: Use renderDayCell with dynamic logic
- Reference: [Events & Methods](references/events-and-methods.md) + [Calendar Views](references/calendar-views.md)

## Related Skills

- **[Implementing Syncfusion Angular Components](../../SKILL.md)** - Main library guide for all Angular components
- **[DatePicker](../implementing-datepicker/SKILL.md)** - Calendar popup with overlay functionality
- **[Scheduler](../implementing-scheduler/SKILL.md)** - Advanced calendar with events and appointments
- **[DateRangePicker](../implementing-daterangepicker/SKILL.md)** - Specialized date range selection component

---

**Next Steps:** Choose a reference guide above based on your specific needs, or explore the common patterns section for your use case.
