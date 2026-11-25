---
name: syncfusion-angular-datetimepicker
description: Comprehensive guide for implementing the Syncfusion Angular DateTimePicker component. Use this when working with combined date and time selection inputs, datetime formatting, or calendar-time pickers in Angular applications. Covers DateTimePicker API, events, styling, and localization patterns.
metadata:
  author: "Syncfusion Inc"
  category: "Calendars"
  version: "33.1.44"
---

# Implementing Syncfusion Angular DatetimePicker

A comprehensive guide for implementing the Syncfusion Essential JS 2 DatetimePicker component in Angular applications. Learn to create date and time selection interfaces, manage calendars and time pickers, handle events, and customize styling.

## DatetimePicker Overview

The Syncfusion Angular DatetimePicker component is a combined date and time selection widget that provides:

- **Integrated Date & Time Selection:** Calendar popup for dates + time picker dropdown for time selection
- **Flexible Formatting:** Custom date formats, time formats, and locale-aware formatting
- **Calendar Views:** Month (default), Year, and Decade views with smooth navigation
- **Time Intervals:** Configurable step intervals (15, 30, 60 minutes, etc.) for time selection
- **Range Constraints:** Min/max dates and min/max time with strict validation
- **Comprehensive Event System:** change, focus, blur, open, close, created, destroyed, navigated, renderDayCell events
- **Masked Input Support:** Optional masked input format for guided user entry
- **Persistence & RTL:** State persistence across reloads and right-to-left language support
- **Advanced Features:** Strict mode validation, floating labels, keyboard customization, timezone support
- **Accessibility:** Full WCAG 2.2 compliance, keyboard navigation, WAI-ARIA support
- **Theme Support:** Material, Bootstrap, Tailwind, Fabric with light/dark variants
- **Mobile Optimized:** Full screen mode on mobile devices, touch-friendly interface

**Package:** `@syncfusion/ej2-angular-datetimepickers`

## Documentation Navigation

Read the following references based on your specific needs:

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Package installation via npm and ng add
- NgModule vs Standalone component setup
- CSS theme imports and dependencies
- Basic datetimepicker implementation
- Component initialization and running the application
- Development server setup

### Basic Implementation
📄 **Read:** [references/basic-implementation.md](references/basic-implementation.md)
- Simple datetime picker with ngModel
- Two-way data binding patterns
- Readonly and disabled states
- Basic validation and constraints
- Event handling fundamentals
- ViewChild component access

### Date & Time Configuration
📄 **Read:** [references/date-time-configuration.md](references/date-time-configuration.md)
- Date format customization (format property)
- Time format configuration (timeFormat property)
- ISO date string handling
- Date range constraints (min/max dates)
- Time range constraints (minTime/maxTime)
- Parsing multiple input formats (inputFormats)

### Calendar & Time Views
📄 **Read:** [references/calendar-and-time-views.md](references/calendar-and-time-views.md)
- Calendar view modes (month, year, decade)
- Start and depth properties for view control
- Time picker popup configuration
- Time step intervals and granularity
- ScrollTo position for time scrolling
- Today button and clear button behavior

### Events & Callbacks
📄 **Read:** [references/events-and-callbacks.md](references/events-and-callbacks.md)
- Change event with ChangedEventArgs
- Focus/blur event handling
- Open/close popup events
- Created/destroyed lifecycle events
- Navigate event for calendar navigation
- RenderDayCell for custom day styling
- Cleared event when clear button is used

### Methods & Imperative Access
📄 **Read:** [references/methods-and-imperative-access.md](references/methods-and-imperative-access.md)
- ViewChild access and component references
- currentView() to get active calendar view
- navigateTo() for programmatic navigation
- focusIn/focusOut for focus management
- destroy() for cleanup and resource release
- getPersistData() for state persistence

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Masked input mode with mask placeholders
- State persistence across page reloads
- RTL (Right-to-Left) language support
- Floating label types and behavior
- Strict mode validation and error states
- Keyboard shortcuts and key configuration
- Timezone offset handling
- Full screen mode for mobile devices
- Clear button visibility and behavior

### Styling & Customization
📄 **Read:** [references/styling-and-customization.md](references/styling-and-customization.md)
- CSS class customization (cssClass property)
- Theme selection and switching
- Dark mode implementation
- Component width and z-index configuration
- HTML attribute injection (htmlAttributes)
- Calendar mode selection (Gregorian vs Islamic)
- Day header format options
- Disabled dates and styling states

### Accessibility & Globalization
📄 **Read:** [references/accessibility-and-globalization.md](references/accessibility-and-globalization.md)
- WCAG 2.2 and Section 508 compliance standards
- WAI-ARIA attributes and roles
- Keyboard navigation (arrows, enter, space, escape)
- Screen reader compatibility and announcements
- Localization and locale property usage
- Day header format variations
- First day of week customization
- Week numbers and week rules
- RTL text direction support

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete property reference with types and defaults
- All method signatures with parameters and return types
- All events with event argument types
- Property descriptions and use cases
- Method examples and common patterns
- Type interfaces and enums
- Key configuration for keyboard shortcuts
- Comprehensive property-by-property guide

## Quick Start Example

```typescript
// app.component.ts
import { Component } from '@angular/core';
import { ChangedEventArgs } from '@syncfusion/ej2-datetimepickers';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  // Simple datetime value
  dateTimeValue: Date = new Date();
  
  // Configuration
  minDate: Date = new Date(2020, 0, 1);
  maxDate: Date = new Date(2030, 11, 31);
  dateFormat: string = 'dd/MM/yyyy hh:mm a';
  timeFormat: string = 'hh:mm a';
  
  // Event handler
  onDateTimeChange(args: ChangedEventArgs): void {
    console.log('Selected DateTime:', args.value);
    console.log('Event Type:', args.type);
  }
  
  onPopupOpen(): void {
    console.log('Popup opened');
  }
  
  onPopupClose(): void {
    console.log('Popup closed');
  }
}
```

```html
<!-- app.component.html -->
<div style="padding: 20px;">
  <h2>Select Date & Time</h2>
  
  <ejs-datetimepicker
    id="datetimepicker"
    [value]="dateTimeValue"
    [format]="dateFormat"
    [timeFormat]="timeFormat"
    [min]="minDate"
    [max]="maxDate"
    placeholder="Select date and time"
    (change)="onDateTimeChange($event)"
    (open)="onPopupOpen()"
    (close)="onPopupClose()">
  </ejs-datetimepicker>
  
  <p *ngIf="dateTimeValue">
    Selected: {{ dateTimeValue | date:'medium' }}
  </p>
</div>
```

## Common Patterns

### Pattern 1: Datetime Range Selection

Select a start and end datetime for appointments, bookings, or events:

```typescript
export class AppComponent {
  startDateTime: Date = new Date();
  endDateTime: Date = new Date(Date.now() + 3600000); // +1 hour
  
  onStartChange(args: ChangedEventArgs): void {
    // Ensure end is after start
    if (this.endDateTime <= args.value) {
      this.endDateTime = new Date((args.value as Date).getTime() + 3600000);
    }
  }
}
```

### Pattern 2: Business Hours Only

Restrict time selection to business hours (9 AM - 5 PM):

```typescript
export class AppComponent {
  minTime: Date = new Date(2026, 2, 24, 9, 0);  // 9:00 AM
  maxTime: Date = new Date(2026, 2, 24, 17, 0); // 5:00 PM
  
  datetimeValue: Date = new Date(2026, 2, 24, 10, 0);
}
```

```html
<ejs-datetimepicker
  [value]="datetimeValue"
  [minTime]="minTime"
  [maxTime]="maxTime"
  timeFormat="hh:mm a">
</ejs-datetimepicker>
```

### Pattern 3: Masked Input for Guided Entry

Use masked input to guide users through the datetime format:

```typescript
export class AppComponent {
  datetimeValue: Date;
  maskPlaceholder = {
    day: 'dd',
    month: 'mm',
    year: 'yyyy',
    hour: 'hh',
    minute: 'mm',
    second: 'ss'
  };
}
```

```html
<ejs-datetimepicker
  [value]="datetimeValue"
  [enableMask]="true"
  [maskPlaceholder]="maskPlaceholder"
  format="dd/MM/yyyy hh:mm:ss">
</ejs-datetimepicker>
```

### Pattern 4: Reactive Forms Integration

Integrate datetimepicker with Angular Reactive Forms:

```typescript
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

export class AppComponent {
  appointmentForm: FormGroup;
  
  constructor(private fb: FormBuilder) {
    this.appointmentForm = this.fb.group({
      appointmentDateTime: [
        new Date(),
        [Validators.required]
      ]
    });
  }
  
  submitForm(): void {
    if (this.appointmentForm.valid) {
      console.log(this.appointmentForm.value);
    }
  }
}
```

```html
<form [formGroup]="appointmentForm">
  <ejs-datetimepicker
    formControlName="appointmentDateTime"
    format="dd/MM/yyyy hh:mm a">
  </ejs-datetimepicker>
  
  <button (click)="submitForm()" [disabled]="!appointmentForm.valid">
    Submit
  </button>
</form>
```

### Pattern 5: Disabled Dates

Disable weekends and specific dates:

```typescript
export class AppComponent {
  datetimeValue: Date;
  
  onRenderDayCell(args: RenderDayCellEventArgs): void {
    // Disable weekends (0 = Sunday, 6 = Saturday)
    if ((args.date as Date).getDay() === 0 || (args.date as Date).getDay() === 6) {
      args.isDisabled = true;
    }
    
    // Disable specific dates
    const disabledDates = [5, 15, 25]; // 5th, 15th, 25th of each month
    if (disabledDates.includes((args.date as Date).getDate())) {
      args.isDisabled = true;
    }
  }
}
```

```html
<ejs-datetimepicker
  [value]="datetimeValue"
  (renderDayCell)="onRenderDayCell($event)">
</ejs-datetimepicker>
```

## Key Properties Reference

| Property | Type | Purpose |
|----------|------|---------|
| `value` | Date | Selected datetime value for two-way binding |
| `format` | string | Date display format (e.g., 'dd/MM/yyyy hh:mm a') |
| `timeFormat` | string | Time display format in popup (e.g., 'hh:mm a') |
| `min` | Date | Minimum selectable date |
| `max` | Date | Maximum selectable date |
| `minTime` | Date | Minimum selectable time |
| `maxTime` | Date | Maximum selectable time |
| `step` | number | Time interval in minutes (15, 30, 60) |
| `enabled` | boolean | Enable/disable the component |
| `readonly` | boolean | Make input readonly (select from popup only) |
| `placeholder` | string | Placeholder text in input |
| `enableMask` | boolean | Enable masked input mode |
| `strictMode` | boolean | Enforce valid values only |
| `enableRtl` | boolean | Right-to-left language support |
| `enablePersistence` | boolean | Persist value across page reloads |
| `start` | CalendarView | Initial calendar view (Month/Year/Decade) |
| `depth` | CalendarView | Maximum calendar view level |
| `locale` | string | Locale for formatting (e.g., 'en-US', 'de-DE') |

## Common Use Cases

### Appointment Booking System
- Use date range selection with business hours time constraints
- Display available time slots based on min/max time
- Handle form validation with required validators
- Show selected datetime confirmation

### Event Scheduling
- Select start and end datetimes for events
- Disable weekend dates with renderDayCell
- Use step intervals for common durations (30, 60 min)
- Format output for API submission

### Shift Management
- Select shift start and end times
- Apply shift time constraints (min/max time)
- Handle date transitions (shifts spanning midnight)
- Support multiple timezone offsets

### Billing & Invoicing
- Select invoice date and time
- Restrict to past dates only
- Display in user's locale format
- Export with ISO format

## Next Steps

1. **Start with Getting Started** → Install and configure the component
2. **Build Basic Implementation** → Create simple datetime pickers
3. **Add Event Handling** → Respond to user interactions
4. **Implement Advanced Features** → Add masked input, persistence, RTL
5. **Customize Appearance** → Apply themes and custom styles
6. **Ensure Accessibility** → Support keyboard and screen readers
7. **Reference API** → Consult complete API documentation as needed

---

**Ready to get started?** Begin with [references/getting-started.md](references/getting-started.md) for installation and setup instructions.
