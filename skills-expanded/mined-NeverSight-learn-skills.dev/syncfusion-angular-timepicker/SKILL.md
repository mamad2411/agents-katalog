---
name: syncfusion-angular-timepicker
description: Comprehensive guide for implementing the Syncfusion Angular TimePicker component. Use this when working with time selection inputs, time formatting, or timepicker event handling in Angular applications. Covers TimePicker API, styling, methods, and accessibility patterns.
metadata:
  author: "Syncfusion Inc"
  category: "Calendars"
  version: "33.1.44"
---

# Implementing Syncfusion Angular TimePicker

A comprehensive guide for implementing the Syncfusion Essential JS 2 TimePicker component in Angular applications. Learn to create time selection interfaces, manage time inputs, handle events, and customize styling.

## TimePicker Overview

The Syncfusion Angular TimePicker component is a dedicated time selection widget that provides:

- **Time Selection:** Popup list with configurable time intervals for selection
- **Flexible Formatting:** Custom time formats, skeleton options, and locale-aware formatting
- **Time Intervals:** Configurable step intervals (15, 30, 60 minutes, etc.) for time selection
- **Range Constraints:** Min/max time with strict validation and boundary enforcement
- **Comprehensive Event System:** change, focus, blur, open, close, created, destroyed, cleared, itemRender events
- **Masked Input Support:** Optional masked input format for guided user entry
- **Persistence & RTL:** State persistence across reloads and right-to-left language support
- **Advanced Features:** Strict mode validation, floating labels, keyboard customization, timezone support
- **Accessibility:** Full WCAG 2.2 compliance, keyboard navigation, WAI-ARIA support
- **Theme Support:** Material, Bootstrap, Tailwind, Fabric with light/dark variants
- **Mobile Optimized:** Full screen mode on mobile devices, touch-friendly interface

**Package:** `@syncfusion/ej2-angular-calendars`

## Documentation Navigation

Read the following references based on your specific needs:

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Package installation via npm and ng add
- NgModule vs Standalone component setup
- CSS theme imports and dependencies
- Basic timepicker implementation
- Component initialization and running the application
- Development server setup

### Basic Implementation
📄 **Read:** [references/basic-implementation.md](references/basic-implementation.md)
- Simple time picker with ngModel
- Two-way data binding patterns
- Readonly and disabled states
- Basic validation and constraints
- Event handling fundamentals
- ViewChild component access

### Time Configuration
📄 **Read:** [references/time-configuration.md](references/time-configuration.md)
- Time format customization (format property)
- TimeFormatObject and skeleton options
- Step intervals and time granularity
- Min/max time constraints
- ScrollTo position for time scrolling
- Popup list configuration

### Events & Callbacks
📄 **Read:** [references/events-and-callbacks.md](references/events-and-callbacks.md)
- Change event with ChangeEventArgs
- Focus/blur event handling
- Open/close popup events
- Created/destroyed lifecycle events
- Cleared event when clear button is used
- ItemRender for custom time formatting

### Methods & Imperative Access
📄 **Read:** [references/methods-and-imperative-access.md](references/methods-and-imperative-access.md)
- ViewChild access and component references
- show() to open the time popup
- hide() to close the time popup
- focusIn/focusOut for focus management
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
- OpenOnFocus popup trigger

### Styling & Customization
📄 **Read:** [references/styling-and-customization.md](references/styling-and-customization.md)
- CSS class customization (cssClass property)
- Theme selection and switching
- Dark mode implementation
- Component width and z-index configuration
- HTML attribute injection (htmlAttributes)
- Placeholder and enabled state styling
- Disabled date styling and appearance

### Accessibility & Globalization
📄 **Read:** [references/accessibility-and-globalization.md](references/accessibility-and-globalization.md)
- WCAG 2.2 and Section 508 compliance standards
- WAI-ARIA attributes and roles
- Keyboard navigation (arrows, enter, space, escape)
- Screen reader compatibility and announcements
- Localization and locale property usage
- Time format variations
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
import { ChangeEventArgs } from '@syncfusion/ej2-calendars';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  // Simple time value
  timeValue: Date = new Date();
  
  // Configuration
  minTime: Date = new Date(2026, 2, 24, 8, 0);   // 8:00 AM
  maxTime: Date = new Date(2026, 2, 24, 20, 0);  // 8:00 PM
  format: string = 'hh:mm a';
  step: number = 30;  // 30-minute intervals
  
  // Event handler
  onTimeChange(args: ChangeEventArgs): void {
    console.log('Selected Time:', args.value);
    console.log('Selected Text:', args.text);
    console.log('Is User Interaction:', args.isInteracted);
  }
  
  onPopupOpen(): void {
    console.log('Time popup opened');
  }
  
  onPopupClose(): void {
    console.log('Time popup closed');
  }
}
```

```html
<!-- app.component.html -->
<div style="padding: 20px;">
  <h2>Select a Time</h2>
  
  <ejs-timepicker
    id="timepicker"
    [value]="timeValue"
    [format]="format"
    [min]="minTime"
    [max]="maxTime"
    [step]="step"
    placeholder="Select time"
    (change)="onTimeChange($event)"
    (open)="onPopupOpen()"
    (close)="onPopupClose()">
  </ejs-timepicker>
  
  <p *ngIf="timeValue">
    Selected Time: {{ timeValue | date:'shortTime' }}
  </p>
</div>
```

## Common Patterns

### Pattern 1: Business Hours Time Selection

Select time within business hours (9 AM - 6 PM):

```typescript
export class AppComponent {
  minTime: Date = new Date(2026, 2, 24, 9, 0);   // 9:00 AM
  maxTime: Date = new Date(2026, 2, 24, 18, 0);  // 6:00 PM
  timeValue: Date = new Date(2026, 2, 24, 10, 0);
  format: string = 'hh:mm a';
  step: number = 15;  // 15-minute intervals
}
```

```html
<ejs-timepicker
  [value]="timeValue"
  [min]="minTime"
  [max]="maxTime"
  [step]="step"
  [format]="format"
  placeholder="Select appointment time">
</ejs-timepicker>
```

### Pattern 2: 24-Hour Format

Display time in 24-hour military format:

```typescript
export class AppComponent {
  timeValue: Date = new Date();
  format: string = 'HH:mm';  // 24-hour format
  step: number = 30;
}
```

```html
<ejs-timepicker
  [value]="timeValue"
  [format]="format"
  [step]="step"
  placeholder="Select time (24-hour)">
</ejs-timepicker>
```

### Pattern 3: Masked Input for Guided Entry

Use masked input to guide users through time entry:

```typescript
export class AppComponent {
  timeValue: Date;
  enableMask: boolean = true;
  maskPlaceholder = {
    hour: 'hh',
    minute: 'mm',
    second: 'ss'
  };
  format: string = 'hh:mm:ss a';
}
```

```html
<ejs-timepicker
  [value]="timeValue"
  [enableMask]="enableMask"
  [maskPlaceholder]="maskPlaceholder"
  format="hh:mm:ss a">
</ejs-timepicker>
```

### Pattern 4: Reactive Forms Integration

Integrate timepicker with Angular Reactive Forms:

```typescript
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

export class AppComponent {
  appointmentForm: FormGroup;
  
  constructor(private fb: FormBuilder) {
    this.appointmentForm = this.fb.group({
      appointmentTime: [
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
  <ejs-timepicker
    formControlName="appointmentTime"
    format="hh:mm a"
    placeholder="Select time">
  </ejs-timepicker>
  
  <button (click)="submitForm()" [disabled]="!appointmentForm.valid">
    Submit
  </button>
</form>
```

### Pattern 5: Time Range Selection

Select start and end times for a duration:

```typescript
export class AppComponent {
  startTime: Date = new Date();
  endTime: Date = new Date(Date.now() + 3600000);  // +1 hour
  
  onStartTimeChange(args: ChangeEventArgs): void {
    // Ensure end time is after start time
    if (args.value && this.endTime <= args.value) {
      this.endTime = new Date(args.value.getTime() + 3600000);  // +1 hour
    }
  }
}
```

```html
<div>
  <label>Start Time:</label>
  <ejs-timepicker
    [value]="startTime"
    format="hh:mm a"
    (change)="onStartTimeChange($event)">
  </ejs-timepicker>
  
  <label>End Time:</label>
  <ejs-timepicker
    [value]="endTime"
    [min]="startTime"
    format="hh:mm a">
  </ejs-timepicker>
</div>
```

## Key Properties Reference

| Property | Type | Purpose |
|----------|------|---------|
| `value` | Date | Selected time value for two-way binding |
| `format` | string | Time display format (e.g., 'hh:mm a') |
| `min` | Date | Minimum selectable time |
| `max` | Date | Maximum selectable time |
| `step` | number | Time interval in minutes (15, 30, 60) |
| `enabled` | boolean | Enable/disable the component |
| `readonly` | boolean | Make input readonly (select from popup only) |
| `placeholder` | string | Placeholder text in input |
| `enableMask` | boolean | Enable masked input mode |
| `strictMode` | boolean | Enforce valid values only |
| `enableRtl` | boolean | Right-to-left language support |
| `enablePersistence` | boolean | Persist value across page reloads |
| `scrollTo` | Date | Default scroll position in time list |
| `locale` | string | Locale for formatting (e.g., 'en-US', 'de-DE') |
| `cssClass` | string | Custom CSS class for styling |
| `width` | string | Component width |
| `zIndex` | number | Z-index for popup |
| `showClearButton` | boolean | Show/hide clear icon |
| `openOnFocus` | boolean | Open popup on input focus |
| `floatLabelType` | string | Floating label behavior (Never/Always/Auto) |

## Common Use Cases

### Appointment Booking System
- Select available time slots from a list
- Restrict to business hours with min/max time
- Use 15 or 30-minute step intervals
- Handle form validation with required validators
- Display selected time confirmation

### Shift Management
- Select shift start and end times
- Apply shift time constraints
- Support multiple timezone offsets
- Handle shift transitions (spanning midnight)
- Export times in ISO format

### Meeting Scheduling
- Select meeting time with business hours constraint
- Use 30-minute step intervals for standard durations
- Display time in user's locale format
- Prevent double bookings with validation
- Sync with calendar component for availability

### Time Tracking
- Record clock-in and clock-out times
- Restrict to business hours
- Use masked input for quick entry
- Persist times for audit trail
- Export times for payroll integration

### Event Registration
- Select event attendance time slot
- Show available time ranges
- Use clear button for corrections
- Support multiple time formats
- Accessibility for assistive technologies

## Next Steps

1. **Start with Getting Started** → Install and configure the component
2. **Build Basic Implementation** → Create simple time pickers
3. **Add Event Handling** → Respond to user interactions
4. **Implement Advanced Features** → Add masked input, persistence, RTL
5. **Customize Appearance** → Apply themes and custom styles
6. **Ensure Accessibility** → Support keyboard and screen readers
7. **Reference API** → Consult complete API documentation as needed

---

**Ready to get started?** Begin with [references/getting-started.md](references/getting-started.md) for installation and setup instructions.
