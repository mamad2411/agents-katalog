---
name: syncfusion-react-daterangepicker
description: Implement the Syncfusion React DateRangePicker component for date range selection, booking systems, and reporting interfaces. Use this when working with date range pickers for appointment booking, event scheduling, date filtering, or vacation requests. Covers date range validation, preset ranges, format customization, event handling, and form integration.
metadata:
  author: "Syncfusion Inc"
  category: "Calendars"
  version: "33.1.44"
---

# Implementing Syncfusion React DateRangePicker Component

The Syncfusion React DateRangePicker component provides an intuitive way to select a date range with support for preset ranges, date validation, multiple date formats, keyboard navigation, and mobile-optimized full-screen mode.

## Documentation Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation via npm (@syncfusion/ej2-react-calendars)
- CSS imports and theme configuration
- Basic DateRangePicker implementation
- Class component vs functional component setup
- Component initialization and structure
- Running development server
- Common troubleshooting

### Date Range Selection
📄 **Read:** [references/date-range-selection.md](references/date-range-selection.md)
- Start and end date properties
- Date range validation patterns
- Minimum and maximum date constraints
- Disabled dates configuration
- Date range presets (Last 7 days, Last 30 days, etc.)
- Value binding and two-way updates
- Read-only and disabled states
- Placeholder and labels

### Date Range Formatting
📄 **Read:** [references/date-range-formatting.md](references/date-range-formatting.md)
- Date format string options (MM/dd/yyyy, dd-MMM-yyyy, etc.)
- Display format vs input format
- Locale-based date formatting
- Custom separator between start and end dates
- Float label types (Never, Always, Auto)
- Placeholder text customization
- htmlAttributes for DOM attributes

### Events and Methods
📄 **Read:** [references/events-and-methods.md](references/events-and-methods.md)
- Event handlers (change, open, close, blur, focus, select)
- Event argument structures
- Methods (show, hide, focusIn, focusOut, reset, destroy)
- Imperative control with useRef
- Lifecycle events (created, destroyed)
- Event patterns and best practices
- Clearing values and state reset
- DateRangeSelectingEvent and ChangedEventArgs

### Customization and Styling
📄 **Read:** [references/customization-and-styling.md](references/customization-and-styling.md)
- CSS class customization with cssClass
- Theme options (Material, Bootstrap, Fluent, Tailwind, Fabric)
- Full-screen mode for mobile devices
- RTL (right-to-left) language support
- Preset ranges customization
- Z-index management
- Width and height configuration
- Accessibility features and ARIA attributes

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete properties list (35+ properties)
- All methods with signatures (8 methods)
- All events with event arguments (12 events)
- Type definitions and interfaces
- Default values and constraints
- Use cases for each property and method

### Advanced Patterns
📄 **Read:** [references/advanced-patterns.md](references/advanced-patterns.md)
- Form submission with date range validation
- Keyboard shortcuts and key navigation
- Server timezone offset handling
- Persistence and localStorage
- Multi-component integration (start/end date binding)
- Performance optimization with lazy loading
- Error handling and validation patterns
- Complex date range scenarios (fiscal years, quarters)

## Quick Start

```tsx
import { DateRangePickerComponent } from '@syncfusion/ej2-react-calendars';
import * as React from 'react';
import '@syncfusion/ej2-base/styles/material3.css';
import '@syncfusion/ej2-buttons/styles/material3.css';
import '@syncfusion/ej2-lists/styles/material3.css';
import '@syncfusion/ej2-inputs/styles/material3.css';
import '@syncfusion/ej2-popups/styles/material3.css';
import '@syncfusion/ej2-calendars/styles/material3.css';

function App() {
  const [selectedRange, setSelectedRange] = React.useState<[Date, Date] | null>(null);

  const handleDateRangeChange = (e: any) => {
    setSelectedRange([e.startDate, e.endDate]);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Select Date Range</h2>
      <DateRangePickerComponent
        id="daterangepicker"
        placeholder="Select a range"
        change={handleDateRangeChange}
      />
      {selectedRange && (
        <p>
          Selected: {selectedRange[0]?.toLocaleDateString()} - {selectedRange[1]?.toLocaleDateString()}
        </p>
      )}
    </div>
  );
}

export default App;
```

## Common Patterns

### Pattern 1: Date Range with Preset Options

```tsx
import { DateRangePickerComponent } from '@syncfusion/ej2-react-calendars';
import * as React from 'react';

function ReportingDashboard() {
  const [dateRange, setDateRange] = React.useState<[Date, Date] | null>(null);

  const getDateRangePresets = () => {
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(today.getDate() - 1);
    
    const last7Days = new Date(today);
    last7Days.setDate(today.getDate() - 7);
    
    const last30Days = new Date(today);
    last30Days.setDate(today.getDate() - 30);
    
    const thisMonth = new Date(today.getFullYear(), today.getMonth(), 1);
    const lastMonth = new Date(today.getFullYear(), today.getMonth(), 0);

    return [
      { text: 'Today', value: [today, today] },
      { text: 'Yesterday', value: [yesterday, yesterday] },
      { text: 'Last 7 Days', value: [last7Days, today] },
      { text: 'Last 30 Days', value: [last30Days, today] },
      { text: 'This Month', value: [thisMonth, today] },
      { text: 'Last Month', value: [new Date(today.getFullYear(), today.getMonth() - 1, 1), lastMonth] },
    ];
  };

  const handlePresetClick = (start: Date, end: Date) => {
    setDateRange([start, end]);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h3>Analytics Report</h3>
      <DateRangePickerComponent
        id="daterangepicker"
        placeholder="Select report date range"
        startDate={dateRange?.[0]}
        endDate={dateRange?.[1]}
        change={(e: any) => setDateRange([e.startDate, e.endDate])}
      />
      
      <div style={{ marginTop: '15px' }}>
        {getDateRangePresets().map((preset) => (
          <button
            key={preset.text}
            onClick={() => handlePresetClick(preset.value[0], preset.value[1])}
            style={{ marginRight: '10px', padding: '5px 10px' }}
          >
            {preset.text}
          </button>
        ))}
      </div>
    </div>
  );
}

export default ReportingDashboard;
```

### Pattern 2: Date Range with Validation

```tsx
import { DateRangePickerComponent } from '@syncfusion/ej2-react-calendars';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function BookingForm() {
  const [dateRange, setDateRange] = React.useState<[Date, Date] | null>(null);
  const [validationError, setValidationError] = React.useState<string>('');

  const minDate = new Date();
  const maxDate = new Date();
  maxDate.setDate(maxDate.getDate() + 90); // 90 days from now

  const handleDateRangeChange = (e: any) => {
    setValidationError('');
    
    if (!e.startDate || !e.endDate) {
      return;
    }

    const start = new Date(e.startDate);
    const end = new Date(e.endDate);

    // Validation checks
    if (start > end) {
      setValidationError('Start date must be before end date');
      return;
    }

    const daysDifference = (end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24);
    if (daysDifference > 30) {
      setValidationError('Date range cannot exceed 30 days');
      return;
    }

    setDateRange([start, end]);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (dateRange && !validationError) {
      console.log('Booking dates:', {
        checkIn: dateRange[0].toLocaleDateString(),
        checkOut: dateRange[1].toLocaleDateString(),
      });
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ padding: '20px', maxWidth: '500px' }}>
      <h3>Book Your Stay</h3>
      
      <label style={{ display: 'block', marginBottom: '8px' }}>
        Select Check-in and Check-out Dates (Max 30 days)
      </label>
      
      <DateRangePickerComponent
        id="daterangepicker"
        placeholder="Select check-in and check-out"
        min={minDate}
        max={maxDate}
        startDate={dateRange?.[0]}
        endDate={dateRange?.[1]}
        change={handleDateRangeChange}
        style={{ width: '100%', marginBottom: '8px' }}
      />

      {validationError && (
        <div style={{ color: 'red', marginBottom: '10px', fontSize: '14px' }}>
          ⚠️ {validationError}
        </div>
      )}

      <ButtonComponent 
        type="submit" 
        isPrimary={true} 
        disabled={!dateRange || !!validationError}
      >
        Book Now
      </ButtonComponent>
    </form>
  );
}

export default BookingForm;
```

<!-- Pattern 3 removed: examples using non-API props (e.g., `disabledDates`) deleted to match authoritative API reference -->

### Pattern 4: Event Handling and State Management

```tsx
import { DateRangePickerComponent } from '@syncfusion/ej2-react-calendars';
import * as React from 'react';

function EventTrackingExample() {
  const [dateRange, setDateRange] = React.useState<[Date, Date] | null>(null);
  const [eventLog, setEventLog] = React.useState<string[]>([]);

  const handleSelect = (e: any) => {
    setEventLog(prev => [
      ...prev, 
      `Selected: ${e.startDate?.toLocaleDateString()} to ${e.endDate?.toLocaleDateString()}`
    ]);
  };

  const handleChange = (e: any) => {
    setDateRange([e.startDate, e.endDate]);
    setEventLog(prev => [...prev, `Changed: ${new Date().toLocaleTimeString()}`]);
  };

  const handleOpen = (e: any) => {
    setEventLog(prev => [...prev, `Popup opened at ${new Date().toLocaleTimeString()}`]);
  };

  const handleClose = (e: any) => {
    setEventLog(prev => [...prev, `Popup closed at ${new Date().toLocaleTimeString()}`]);
  };

  const clearLog = () => {
    setEventLog([]);
  };

  return (
    <div style={{ padding: '20px', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
      <div>
        <h3>DateRangePicker</h3>
        <DateRangePickerComponent
          id="daterangepicker"
          placeholder="Select date range"
          select={handleSelect}
          change={handleChange}
          open={handleOpen}
          close={handleClose}
        />
      </div>

      <div style={{ padding: '10px', border: '1px solid #ccc', borderRadius: '4px' }}>
        <h3>Event Log</h3>
        <button 
          onClick={clearLog}
          style={{ 
            padding: '5px 10px', 
            marginBottom: '10px',
            backgroundColor: '#f0f0f0',
            border: '1px solid #ccc',
            cursor: 'pointer'
          }}
        >
          Clear Log
        </button>
        <ul style={{ maxHeight: '300px', overflowY: 'auto', margin: 0, paddingLeft: '20px' }}>
          {eventLog.map((event, idx) => (
            <li key={idx} style={{ marginBottom: '5px', fontSize: '12px' }}>
              {event}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default EventTrackingExample;
```

### Pattern 5: Custom Date Range Format

```tsx
import { DateRangePickerComponent } from '@syncfusion/ej2-react-calendars';
import * as React from 'react';

function DateFormatDemo() {
  const [formatType, setFormatType] = React.useState<'short' | 'long' | 'custom'>('short');
  const [dateRange, setDateRange] = React.useState<[Date, Date] | null>(null);

  const getFormat = () => {
    switch (formatType) {
      case 'short':
        return 'M/d/yyyy';
      case 'long':
        return 'MMMM d, yyyy';
      case 'custom':
        return 'dd-MMM-yy';
      default:
        return 'M/d/yyyy';
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h3>Date Range Format Options</h3>
      
      <div style={{ marginBottom: '15px' }}>
        <label style={{ marginRight: '10px' }}>Format Type:</label>
        {(['short', 'long', 'custom'] as const).map((format) => (
          <label key={format} style={{ marginRight: '15px' }}>
            <input
              type="radio"
              name="format"
              value={format}
              checked={formatType === format}
              onChange={(e) => setFormatType(e.target.value as any)}
            />
            {format.charAt(0).toUpperCase() + format.slice(1)}
          </label>
        ))}
      </div>

      <div style={{ marginBottom: '10px', padding: '10px', backgroundColor: '#f5f5f5' }}>
        <strong>Format String:</strong> {getFormat()}
      </div>

      <DateRangePickerComponent
        id="daterangepicker"
        placeholder="Select date range"
        format={getFormat()}
        startDate={dateRange?.[0]}
        endDate={dateRange?.[1]}
        change={(e: any) => setDateRange([e.startDate, e.endDate])}
      />

      {dateRange && (
        <div style={{ marginTop: '15px', padding: '10px', backgroundColor: '#e8f5e9' }}>
          <p>
            <strong>Formatted Output:</strong> {dateRange[0].toLocaleDateString('en-US')} - {dateRange[1].toLocaleDateString('en-US')}
          </p>
        </div>
      )}
    </div>
  );
}

export default DateFormatDemo;
```

## Key Props Reference

- Prop: `startDate`: Type: `Date` — Default: `null` — Initial start date of the range.
- Prop: `endDate`: Type: `Date` — Default: `null` — Initial end date of the range.
- Prop: `min`: Type: `Date` — Default: `new Date(1900, 0, 1)` — Minimum selectable date.
- Prop: `max`: Type: `Date` — Default: `new Date(2099, 11, 31)` — Maximum selectable date.
- Prop: `value`: Type: `Date[] | DateRange` — Default: `null` — Gets or sets the start and end date.
- Prop: `format`: Type: `string | RangeFormatObject` — Default: `null` — Date display and input format.
- Prop: `placeholder`: Type: `string` — Default: `null` — Input placeholder text.
- Prop: `enabled`: Type: `boolean` — Default: `true` — Enables or disables the component (use `enabled`, not `disabled`).
- Prop: `readonly`: Type: `boolean` — Default: `false` — Read-only state; prevents editing.
- Prop: `allowEdit`: Type: `boolean` — Default: `true` — Allow manual text editing of the input.
- Prop: `cssClass`: Type: `string` — Default: `''` — Adds a custom CSS class to the root element.
- Prop: `floatLabelType`: Type: `FloatLabelType | string` — Default: `Never` — Float label behavior (Never, Always, Auto).
- Prop: `separator`: Type: `string` — Default: `'-'` — Separator string between start and end date in the input.
- Prop: `locale`: Type: `string` — Default: `'en-US'` — Locale used for formatting and localization.
- Prop: `inputFormats`: Type: `string[] | RangeFormatObject[]` — Default: `null` — Acceptable input parsing formats.
- Prop: `keyConfigs`: Type: `object` — Default: `null` — Custom keyboard shortcuts mapping.
- Prop: `firstDayOfWeek`: Type: `number` — Default: `null` — First day of week for calendar rendering.
- Prop: `dayHeaderFormat`: Type: `DayHeaderFormats` — Default: `Short` — Day name format in header.
- Prop: `start`: Type: `CalendarView` — Default: `Month` — Initial calendar view when popup opens.
- Prop: `depth`: Type: `CalendarView` — Default: `Month` — Maximum navigation depth for the calendar.
- Prop: `weekNumber`: Type: `boolean` — Default: `false` — Show week numbers in calendar rows.
- Prop: `weekRule`: Type: `WeekRule` — Default: `FirstDay` — Rule that defines first week of the year.
- Prop: `minDays`: Type: `number` — Default: `null` — Minimum allowed span of days in a selection.
- Prop: `maxDays`: Type: `number` — Default: `null` — Maximum allowed span of days in a selection.
- Prop: `strictMode`: Type: `boolean` — Default: `false` — When true, only valid ranges can be entered.
- Prop: `showClearButton`: Type: `boolean` — Default: `true` — Toggle visibility of the clear button.
- Prop: `fullScreenMode`: Type: `boolean` — Default: `false` — Use full-screen popup on mobile.
- Prop: `htmlAttributes`: Type: `{ [key: string]: string }` — Default: `{}` — Additional HTML attributes applied to the component element.
- Prop: `serverTimezoneOffset`: Type: `number` — Default: `null` — Server timezone offset in minutes for initial value processing.
- Prop: `width`: Type: `number | string` — Default: `''` — Width of the component input.
- Prop: `zIndex`: Type: `number` — Default: `1000` — z-index for popup element.

## Related Skills

- [Implementing Calendar](../implementing-calendar/) - For single date selection
- [Implementing DatePicker](../implementing-calendar/) - For basic date picking
- [Implementing TimePicker](../implementing-timepicker/) - For time selection within ranges

---

**Next Steps:**
- Read [references/getting-started.md](references/getting-started.md) to install and set up your first DateRangePicker
- Explore [references/date-range-selection.md](references/date-range-selection.md) for range selection patterns
- Check [references/date-range-formatting.md](references/date-range-formatting.md) for format options
- See [references/advanced-patterns.md](references/advanced-patterns.md) for complex scenarios
- Refer to [references/api-reference.md](references/api-reference.md) for complete API documentation
