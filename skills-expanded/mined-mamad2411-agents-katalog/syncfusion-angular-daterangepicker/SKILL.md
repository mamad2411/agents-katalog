---
name: syncfusion-angular-daterangepicker
description: Comprehensive guide for implementing the Syncfusion Angular DateRangePicker component. Use this when working with date range selection, preset ranges, range validation, or date constraints in Angular applications. Covers DateRangePicker API, events, formatting, and accessibility patterns.
metadata:
  author: "Syncfusion Inc"
  category: "Calendars"
  version: "33.1.44"
---

# Implementing Syncfusion Angular DateRangePicker

A comprehensive guide for implementing the Syncfusion Essential JS 2 DateRangePicker component in Angular applications. Learn to create date range pickers, handle range selection, manage events, and customize styling.

## DateRangePicker Overview

The Syncfusion Angular DateRangePicker component is a specialized date selection widget that provides:

- **Dual calendar display:** Start and end date selection with synchronized calendars
- **Preset ranges:** Predefined options like "Last 7 Days", "This Month", "Last Month", "Custom"
- **Range validation:** Min/max dates, disabled ranges, required range length
- **Date formatting:** Customizable date format with separators and pattern support
- **Event system:** Created, destroyed, change, select, rangeSelected, open, close, renderDayCell events
- **Keyboard shortcuts:** Tab, arrow keys, enter, escape for full keyboard accessibility
- **Localization support:** Locale-specific formatting, day headers, month names
- **Accessibility:** Full WCAG 2.2 compliance, ARIA attributes, screen reader support
- **Rich customization:** CSS classes, custom templates, day cell rendering
- **Mobile optimization:** Touch-friendly interface, responsive design, full-screen mode

**Package:** `@syncfusion/ej2-angular-calendars`

## Documentation Navigation

Read the following references based on your specific needs:

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Package installation and module setup
- CSS theme imports and dependencies
- Basic DateRangePicker implementation
- Component initialization in Angular
- Start and end date configuration
- Running and testing setup

### Date Range Selection
📄 **Read:** [references/date-range-selection.md](references/date-range-selection.md)
- Single click range selection
- Sequential date selection (click start, then end)
- Date range value binding (`startDate`, `endDate` properties)
- Min/max date constraints
- Range validation and error handling
- Disabled date ranges
- Clearing selections

### Preset Ranges
📄 **Read:** [references/preset-ranges.md](references/preset-ranges.md)
- Predefined range options (Last 7 Days, Last Month, etc.)
- Custom preset configuration
- Programmatic preset application
- Dynamic preset generation
- Preset change events
- Combining presets with constraints

### Events & Methods
📄 **Read:** [references/events-and-methods.md](references/events-and-methods.md)
- Event handlers (change, select, rangeSelected, open, close)
- Range selection event details (startDate, endDate, daySpan)
- Programmatic methods (show(), hide(), getSelectedRange())
- Created and destroyed lifecycle events
- RenderDayCell for custom styling
- Method return types and parameters

### Date Formatting & Constraints
📄 **Read:** [references/date-formatting-and-constraints.md](references/date-formatting-and-constraints.md)
- Date format patterns and separators
- Multiple format support (format and inputFormats)
- Min/max date constraints
- Min/max days validation
- Disabled dates configuration
- Format error handling
- Locale-specific formats

### Keyboard Navigation & Accessibility
📄 **Read:** [references/keyboard-navigation-and-accessibility.md](references/keyboard-navigation-and-accessibility.md)
- Tab and Shift+Tab navigation
- Arrow keys for date navigation
- Enter for range selection and confirmation
- Escape to close picker
- Alt key shortcuts
- Screen reader compatibility
- ARIA labels and roles
- WCAG 2.2 AA compliance
- Focus management

### Styling & Customization
📄 **Read:** [references/styling-and-customization.md](references/styling-and-customization.md)
- CSS class customization (.e-daterangepicker, .e-calendar, .e-range-header)
- Theme selection (Material, Bootstrap, Tailwind, Fabric)
- Dark mode implementation
- Custom day cell styling via renderDayCell
- Disabled date styling
- Preset button styling
- Hover and focus states
- Responsive layout customization

### Globalization & Localization
📄 **Read:** [references/globalization-and-localization.md](references/globalization-and-localization.md)
- Locale property for date formatting
- RTL (Right-to-Left) support for Arabic, Hebrew
- Day header formats (Short, Narrow, Abbreviated, Wide)
- Month names and day names localization
- Custom locale support
- Timezone handling
- Date format localization

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete property reference with descriptions
- All method signatures with return types
- Event argument types and structures
- Type interfaces (RangeEventArgs, NavigatingEventArgs, etc.)
- CSS classes and styling hooks
- Browser support matrix

## Quick Start Example

```typescript
// app.component.ts
import { Component } from '@angular/core';
import { RangeEventArgs } from '@syncfusion/ej2-calendars';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  // Date range properties
  startDate: Date = new Date(2026, 2, 1);  // March 1, 2026
  endDate: Date = new Date(2026, 2, 31);   // March 31, 2026
  
  // Constraints
  minDate: Date = new Date(2020, 0, 1);
  maxDate: Date = new Date(2030, 11, 31);
  
  // Range display
  selectedRange: string = '';
  
  // Event handler
  onRangeChange(args: RangeEventArgs): void {
    console.log('Start Date:', args.startDate);
    console.log('End Date:', args.endDate);
    console.log('Days in range:', args.daySpan);
    this.updateRangeDisplay();
  }
  
  updateRangeDisplay(): void {
    if (this.startDate && this.endDate) {
      const start = this.startDate.toLocaleDateString();
      const end = this.endDate.toLocaleDateString();
      this.selectedRange = `${start} - ${end}`;
    }
  }
}
```

```html
<!-- app.component.html -->
<div style="padding: 20px; font-family: Arial, sans-serif;">
  <h2>DateRangePicker Example</h2>
  
  <div style="margin-bottom: 20px;">
    <label for="dateRange">Select Date Range:</label>
    <ejs-daterangepicker 
      id="dateRange"
      placeholder="Select a date range"
      [startDate]="startDate"
      [endDate]="endDate"
      [min]="minDate"
      [max]="maxDate"
      (change)="onRangeChange($event)">
    </ejs-daterangepicker>
  </div>
  
  <div *ngIf="selectedRange" style="padding: 10px; background-color: #f0f0f0;">
    <p><strong>Selected Range:</strong> {{ selectedRange }}</p>
  </div>
</div>
```

```css
/* app.component.css */
@import '../node_modules/@syncfusion/ej2-base/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-inputs/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-popups/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-calendars/styles/material3.css';

:host ::ng-deep .e-daterangepicker {
  margin: 10px 0;
  width: 100%;
}

:host ::ng-deep .e-range-header {
  background-color: #3f51b5;
  color: white;
}
```

## Common Patterns

### Pattern 1: Preset Date Ranges

Quick selection buttons for common date ranges:

```typescript
export class AppComponent {
  presets: any[] = [
    { label: 'Today', start: new Date(), end: new Date() },
    { label: 'Last 7 Days', start: this.getDateDaysAgo(7), end: new Date() },
    { label: 'Last 30 Days', start: this.getDateDaysAgo(30), end: new Date() },
    { label: 'This Month', start: this.getFirstDayOfMonth(), end: new Date() },
    { label: 'Last Month', start: this.getFirstDayOfLastMonth(), end: this.getLastDayOfLastMonth() }
  ];
  
  startDate: Date = new Date();
  endDate: Date = new Date();
  
  selectPreset(preset: any): void {
    this.startDate = preset.start;
    this.endDate = preset.end;
  }
  
  private getDateDaysAgo(days: number): Date {
    const date = new Date();
    date.setDate(date.getDate() - days);
    return date;
  }
  
  private getFirstDayOfMonth(): Date {
    return new Date(new Date().getFullYear(), new Date().getMonth(), 1);
  }
  
  private getFirstDayOfLastMonth(): Date {
    const date = new Date();
    return new Date(date.getFullYear(), date.getMonth() - 1, 1);
  }
  
  private getLastDayOfLastMonth(): Date {
    const date = new Date();
    return new Date(date.getFullYear(), date.getMonth(), 0);
  }
}
```

```html
<div>
  <div style="margin-bottom: 10px;">
    <button *ngFor="let preset of presets" 
            (click)="selectPreset(preset)"
            style="margin-right: 5px; padding: 8px 12px;">
      {{ preset.label }}
    </button>
  </div>
  
  <ejs-daterangepicker 
    [startDate]="startDate"
    [endDate]="endDate">
  </ejs-daterangepicker>
</div>
```

### Pattern 2: Date Range Validation

Validate date ranges with custom constraints:

```typescript
export class AppComponent {
  @ViewChild('daterangepicker') drp!: DateRangePickerComponent;
  
  startDate: Date = new Date();
  endDate: Date = new Date();
  rangeError: string = '';
  
  minDate: Date = new Date(2020, 0, 1);
  maxDate: Date = new Date(2030, 11, 31);
  minDays: number = 1;      // At least 1 day
  maxDays: number = 90;     // At most 90 days
  
  onRangeChange(args: RangeEventArgs): void {
    this.rangeError = '';
    
    // Validate date range
    if (args.daySpan < this.minDays) {
      this.rangeError = `Range must be at least ${this.minDays} day(s)`;
      return;
    }
    
    if (args.daySpan > this.maxDays) {
      this.rangeError = `Range cannot exceed ${this.maxDays} days`;
      return;
    }
    
    this.startDate = args.startDate;
    this.endDate = args.endDate;
  }
  
  isRangeValid(): boolean {
    return this.rangeError === '';
  }
}
```

### Pattern 3: Reactive Form Integration

Integrate DateRangePicker with Reactive Forms:

```typescript
export class AppComponent implements OnInit {
  reportForm: FormGroup;
  
  constructor(private fb: FormBuilder) {
    this.reportForm = this.fb.group({
      reportName: ['', Validators.required],
      startDate: [new Date(2026, 0, 1), Validators.required],
      endDate: [new Date(), Validators.required]
    });
  }
  
  ngOnInit(): void {
    this.reportForm.get('startDate')?.valueChanges.subscribe(date => {
      console.log('Start date changed:', date);
      this.validateDateRange();
    });
    
    this.reportForm.get('endDate')?.valueChanges.subscribe(date => {
      console.log('End date changed:', date);
      this.validateDateRange();
    });
  }
  
  validateDateRange(): void {
    const start = this.reportForm.get('startDate')?.value;
    const end = this.reportForm.get('endDate')?.value;
    
    if (start && end && start > end) {
      this.reportForm.get('endDate')?.setErrors({ 'invalidRange': true });
    } else {
      this.reportForm.get('endDate')?.setErrors(null);
    }
  }
  
  submitForm(): void {
    if (this.reportForm.valid) {
      console.log('Form values:', this.reportForm.value);
    }
  }
}
```

```html
<form [formGroup]="reportForm" (ngSubmit)="submitForm()">
  <div>
    <label>Report Name:</label>
    <ejs-textbox 
      formControlName="reportName"
      placeholder="Enter report name">
    </ejs-textbox>
  </div>
  
  <div>
    <label>Report Period:</label>
    <ejs-daterangepicker 
      [formControl]="reportForm.get('startDate')"
      [endDate]="reportForm.get('endDate')?.value">
    </ejs-daterangepicker>
  </div>
  
  <button type="submit" [disabled]="!reportForm.valid">Generate Report</button>
</form>
```

### Pattern 4: Dynamic Range Constraints

Update range constraints based on business logic:

```typescript
export class AppComponent {
  startDate: Date = new Date();
  endDate: Date = new Date();
  
  // Dynamic constraints
  minDate: Date = new Date();
  maxDate: Date = new Date();
  
  reportType: string = 'daily';
  
  onReportTypeChange(type: string): void {
    this.reportType = type;
    this.updateConstraints();
  }
  
  private updateConstraints(): void {
    const today = new Date();
    
    switch (this.reportType) {
      case 'daily':
        // Last 7 days only
        this.minDate = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);
        this.maxDate = today;
        break;
      
      case 'monthly':
        // Last 12 months
        this.minDate = new Date(today.getFullYear() - 1, today.getMonth(), 1);
        this.maxDate = today;
        break;
      
      case 'yearly':
        // Last 5 years
        this.minDate = new Date(today.getFullYear() - 5, 0, 1);
        this.maxDate = today;
        break;
    }
  }
}
```

### Pattern 5: Disabled Date Ranges

Disable specific date ranges (holidays, blackout dates):

```typescript
export class AppComponent {
  disabledRanges: Array<{start: Date, end: Date}> = [
    { start: new Date(2026, 11, 20), end: new Date(2026, 11, 31) }, // Christmas season
    { start: new Date(2026, 0, 1), end: new Date(2026, 0, 3) }      // New Year
  ];
  
  startDate: Date = new Date();
  endDate: Date = new Date();
  
  onRenderDayCell(args: RenderDayCellEventArgs): void {
    // Disable dates in disabled ranges
    for (const range of this.disabledRanges) {
      if (args.date >= range.start && args.date <= range.end) {
        args.isDisabled = true;
        break;
      }
    }
  }
}
```

## Key Props Reference

| Prop | Type | Description | Example |
|------|------|-------------|---------|
| `startDate` | `Date` | Start date of the range | `[startDate]="start"` |
| `endDate` | `Date` | End date of the range | `[endDate]="end"` |
| `value` | `Date[]` or `DateRange` | Selected date range (array or object) | `[(ngModel)]="dateRange"` |
| `min` | `Date` | Minimum selectable date | `[min]="minDate"` |
| `max` | `Date` | Maximum selectable date | `[max]="maxDate"` |
| `minDays` | `number` | Minimum days in range | `[minDays]="1"` |
| `maxDays` | `number` | Maximum days in range | `[maxDays]="90"` |
| `format` | `string` | Date display format | `format="dd/MM/yyyy"` |
| `separator` | `string` | Range separator character | `separator=" to "` |
| `placeholder` | `string` | Placeholder text | `placeholder="Select date range"` |
| `presets` | `PresetsModel[]` | Predefined range options | `[presets]="presets"` |
| `strictMode` | `boolean` | Strict date validation | `[strictMode]="true"` |
| `readonly` | `boolean` | Read-only input field | `[readonly]="false"` |
| `enabled` | `boolean` | Enable/disable component | `[enabled]="true"` |
| `locale` | `string` | Culture/language code | `locale="en-US"` |
| `enableRtl` | `boolean` | Enable RTL layout | `[enableRtl]="false"` |
| `cssClass` | `string` | Custom CSS classes | `cssClass="custom-drp"` |
| `width` | `number \| string` | Component width | `width="300px"` |
| `allowEdit` | `boolean` | Allow manual text input | `[allowEdit]="true"` |
| `openOnFocus` | `boolean` | Open picker on input focus | `[openOnFocus]="true"` |
| `showClearButton` | `boolean` | Show clear button | `[showClearButton]="true"` |
| `depth` | `CalendarView` | Calendar view depth | `depth="Month"` |

## Common Use Cases

**Use Case 1: Report Date Range Selection**
- User selects date range for report generation
- Apply min/max date constraints
- Support preset ranges (Last 7 Days, Last Month, etc.)
- Solution: Combine startDate/endDate with presets and min/max constraints
- Reference: [Preset Ranges](references/preset-ranges.md) + [Date Formatting & Constraints](references/date-formatting-and-constraints.md)

**Use Case 2: Booking System Range**
- Select check-in and check-out dates for booking
- Disable past dates and blackout dates
- Show day count in range
- Solution: Use min date constraint, renderDayCell for disabled ranges, calculate daySpan
- Reference: [Date Range Selection](references/date-range-selection.md) + [Events & Methods](references/events-and-methods.md)

**Use Case 3: Analytics Date Filter**
- Select date range for analytics dashboard
- Multiple preset options for quick selection
- Responsive mobile-friendly interface
- Solution: Use presets with responsive styling and touch optimization
- Reference: [Preset Ranges](references/preset-ranges.md) + [Styling & Customization](references/styling-and-customization.md)

**Use Case 4: Accessible Form Field**
- DateRangePicker integrated in form with full keyboard accessibility
- Screen reader compatible, WCAG 2.2 compliant
- Solution: Use with Reactive Forms, proper ARIA labels
- Reference: [Keyboard Navigation & Accessibility](references/keyboard-navigation-and-accessibility.md)

**Use Case 5: International Date Picker**
- Support multiple languages and date formats
- Show RTL for Arabic, Hebrew
- Locale-specific formatting
- Solution: Use locale property and format customization
- Reference: [Globalization & Localization](references/globalization-and-localization.md)

## Related Skills

- **[Implementing Syncfusion Angular Components](../../SKILL.md)** - Main library guide for all Angular components
- **[Calendar](../implementing-calendar/SKILL.md)** - Single calendar component for date selection
- **[DatePicker](../implementing-datepicker/SKILL.md)** - Single date picker with calendar overlay
- **[DateTimePicker](../implementing-datetimepicker/SKILL.md)** - Date and time selection combined
- **[TimePicker](../implementing-timepicker/SKILL.md)** - Time selection component

---

**Next Steps:** Choose a reference guide above based on your specific needs, or explore the common patterns section for your use case.
