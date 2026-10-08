---
name: syncfusion-react-calendars
description: Comprehensive guide for implementing Syncfusion React Calendar components including Calendar, DatePicker, DateRangePicker, DateTimePicker, and TimePicker. Covers installation, data binding, date/time selection, range selection, formatting, localization, masking, validation, customization, templates, accessibility, and controlled component patterns in React applications.
metadata:
  author: "Syncfusion Inc"
  category: "Calendars"
  version: "34.1.29"
---

# Implementing Syncfusion React Calendars

##  Calendar

The Syncfusion React **CalendarComponent** is a highly customizable calendar UI control that allows users to select single or multiple dates. It supports multiple views (Month, Year, Decade), navigation, week numbers, disabled dates, custom day cell rendering, localization, RTL support, and full accessibility (WCAG 2.2 compliant).

### Quick Start (React)

#### Install

```bash
npm install @syncfusion/ej2-react-calendars @syncfusion/ej2-base
```

#### Basic Example (App.jsx)

```jsx
import React, { useState } from 'react';
import { CalendarComponent } from '@syncfusion/ej2-react-calendars';
import '@syncfusion/ej2-base/styles/material3.css';
import '@syncfusion/ej2-calendars/styles/material3.css';

export default function App() {
  const [value, setValue] = useState(new Date());
  const onChange = (args) => setValue(args.value || args);

  return (
    <div style={{ padding: 20 }}>
      <h3>Select a date</h3>
      <CalendarComponent value={value} change={onChange} />
      <p>Selected: {value.toDateString()}</p>
    </div>
  );
}
```

Notes:
- Use the `change` event to sync selected date to React state.
- Import theme CSS once (global or component-level) to style the control.

### Guidance & Patterns

- **Controlled component:** keep source-of-truth in React state and update `value` via `change` event.
- **Multi-selection:** use `isMultiSelection={true}` with `values` prop and `addDate()`/`removeDate()` methods.
- **Programmatic navigation:** use a `ref` to call `navigateTo(view, date)` — both arguments are required (see references/getting-started-react.md).
- **Date ranges:** for range selection, use DateRangePicker (separate component). The Calendar itself does not have a built-in range highlight mode.
- **Accessibility:** use wrapper elements with `role="region"` and a separate `aria-live` region for announcements — these are not direct Calendar props.
- **Week numbers:** enable with `weekNumber={true}` (the correct prop name).

### References

Navigate to the reference that matches your current task:

#### Getting Started
📄 **Read:** [references/getting-started-react.md](references/calendar-getting-started-react.md)
- Installation and npm setup
- React component examples
- CSS/theme imports
- Using refs and methods

#### Date Selection
📄 **Read:** [references/date-selection.md](references/calendar-date-selection.md)
- Single date selection
- Multiple dates and ranges
- Min/max constraints
- Disabling specific dates

#### Calendar Views
📄 **Read:** [references/calendar-views.md](references/calendar-calendar-views.md)
- Month, Year, Decade views
- Navigating between views
- Initial and depth controls
- Programmatic navigation

#### Styling & Customization
📄 **Read:** [references/styling-customization.md](references/calendar-styling-customization.md)
- Theme selection and switching
- CSS class customization
- Custom day cell rendering
- RTL and responsive design

#### Events & Methods
📄 **Read:** [references/events-methods.md](references/calendar-events-methods.md)
- Event handlers (change, created, renderDayCell)
- Using refs and imperative methods
- Advanced renderDayCell hook
- Event tracking patterns

#### Accessibility & Globalization
📄 **Read:** [references/accessibility-globalization.md](references/calendar-accessibility-globalization.md)
- WCAG 2.1 compliance
- Keyboard navigation
- ARIA attributes
- Locale support and RTL
- Testing for accessibility

#### API Reference (Quick Lookup)
📄 **Read:** [references/api-reference.md](references/calendar-api-reference.md)
- Props, events, methods at a glance
- Common enums and types
- Link to upstream docs

#### Troubleshooting & Tips

- **Styles not applied:** confirm CSS imports point to `node_modules/@syncfusion/ej2-calendars/styles/` and are loaded before component styles.
- **React state mismatch:** use the `value` prop and `change` event to keep React state in sync — do not rely on framework-specific bindings.
- **Multiple date selection not working:** ensure `isMultiSelection={true}` and use `values` (not `value`) for the initial array.
- **`navigateTo` not working:** the method requires two arguments — `navigateTo(view: CalendarView, date: Date)`.
- **"Cannot find module":** run `npm install @syncfusion/ej2-react-calendars @syncfusion/ej2-base` and confirm `package.json`.
- **Week numbers not showing:** use `weekNumber={true}` (not `showWeekNumber`).

## DatePicker

The Syncfusion React **DatePickerComponent** provides an intuitive input control with a calendar popup for selecting a single date. It features flexible formatting, masked input, min/max date validation, strict mode, multiple input formats, custom day rendering, localization, and seamless integration as a controlled React component.

### Component Overview

The **DatePicker** is a Syncfusion React component for date selection with powerful features:

- **Calendar popup** - Visual date selection with navigation
- **Flexible formatting** - Display and input formats with pattern support
- **Masked input** - `enableMask` for segment-by-segment date entry with `maskPlaceholder`
- **Range validation** - Min/max dates with `strictMode` automatic correction
- **Multiple views** - Month, year, and decade views via `start` and `depth` properties
- **Day cell customization** - Disable weekends, highlight special dates via `renderDayCell` event
- **Full globalization** - 150+ cultures, RTL (`enableRtl`), locale-specific formatting, `firstDayOfWeek`
- **WCAG 2.2 compliant** - Full accessibility with keyboard navigation and ARIA attributes
- **Form ready** - Controlled components, React hooks, form validation integration
- **Programmatic control** - `show()`, `hide()`, `focusIn()`, `focusOut()`, `navigateTo()`, `currentView()`

### Complete API Summary

#### Key Properties
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `value` | Date | null | Selected date |
| `min` | Date | 1900-01-01 | Minimum selectable date |
| `max` | Date | 2099-12-31 | Maximum selectable date |
| `format` | string \| FormatObject | null | Display format (e.g., `"dd/MM/yyyy"`) |
| `inputFormats` | string[] \| FormatObject[] | null | Accepted input formats array |
| `placeholder` | string | null | Placeholder text for the input |
| `enabled` | boolean | true | Enable or disable the component |
| `readonly` | boolean | false | Readonly state |
| `allowEdit` | boolean | true | Allow editing the input textbox |
| `strictMode` | boolean | false | Auto-correct out-of-range dates |
| `showClearButton` | boolean | true | Show/hide the clear button |
| `showTodayButton` | boolean | true | Show/hide today button |
| `start` | CalendarView | Month | Initial view: `"Month"`, `"Year"`, `"Decade"` |
| `depth` | CalendarView | Month | Deepest navigation level |
| `enableMask` | boolean | false | Enable masked date input |
| `maskPlaceholder` | MaskPlaceholderModel | {...} | Segment placeholders for masked input |
| `enableRtl` | boolean | false | Right-to-left rendering |
| `locale` | string | '' | Culture/locale code |
| `firstDayOfWeek` | number | 0 | First day of week (0=Sunday) |
| `weekNumber` | boolean | false | Show week numbers |
| `weekRule` | WeekRule | FirstDay | Rule for first week of year |
| `calendarMode` | CalendarType | Gregorian | Calendar type (Gregorian or Islamic) |
| `dayHeaderFormat` | DayHeaderFormats | Short | Day name format in header |
| `floatLabelType` | FloatLabelType | Never | Floating label behavior |
| `fullScreenMode` | boolean | false | Full screen popup on mobile |
| `openOnFocus` | boolean | false | Open popup on input focus |
| `serverTimezoneOffset` | number | null | Server timezone offset |
| `cssClass` | string | null | Custom CSS class |
| `htmlAttributes` | { [key: string]: string } | {} | Additional HTML attributes |
| `keyConfigs` | { [key: string]: string } | null | Custom key action mappings |
| `width` | number \| string | null | Component width |
| `zIndex` | number | 1000 | Popup z-index |
| `enablePersistence` | boolean | false | Persist state between reloads |

#### Methods
| Method | Returns | Description |
|--------|---------|-------------|
| `show()` | void | Opens the calendar popup |
| `hide()` | void | Closes the calendar popup |
| `focusIn()` | void | Sets focus to the component |
| `focusOut()` | void | Removes focus from the component |
| `navigateTo(view, date)` | void | Navigates to a specific view and date |
| `currentView()` | string | Returns the current calendar view name |
| `getPersistData()` | string | Gets persisted state data |
| `removeDate(dates)` | void | Removes date(s) from the values |
| `destroy()` | void | Destroys the component |

#### Events
| Event | Args Type | Description |
|-------|-----------|-------------|
| `change` | ChangedEventArgs | Fires when the selected date changes |
| `focus` | FocusEventArgs | Fires when input gains focus |
| `blur` | BlurEventArgs | Fires when input loses focus |
| `open` | PreventableEventArgs \| PopupObjectArgs | Fires when the popup opens |
| `close` | PreventableEventArgs \| PopupObjectArgs | Fires when the popup closes |
| `cleared` | ClearedEventArgs | Fires when value is cleared |
| `created` | Object | Fires when component is created |
| `destroyed` | Object | Fires when component is destroyed |
| `navigated` | NavigatedEventArgs | Fires when calendar view is navigated |
| `renderDayCell` | RenderDayCellEventArgs | Fires when each day cell is rendered |

### Documentation & Navigation Guide

When the user needs help with DatePicker, guide them to the appropriate reference:

#### Getting Started
📄 **Read:** [references/getting-started.md](references/datepicker-getting-started.md)
- Installation via npm (@syncfusion/ej2-react-calendars)
- CSS theme imports (material3, bootstrap, fluent, tailwind)
- Component imports and setup
- Basic JSX implementation with DatePickerComponent
- Functional vs class component examples
- Running your first application

#### Date Formats & Input
📄 **Read:** [references/date-formats-and-input.md](references/datepicker-date-formats-and-input.md)
- Display format property and patterns (yyyy-MM-dd, dd/MM/yyyy, etc.)
- Custom format specifiers (# and 0 patterns)
- Input formats for flexible date entry (accepting multiple formats)
- Format examples with real-world scenarios
- Parsing and converting user input automatically
- Culture-based default formatting

#### Date Range & Validation
📄 **Read:** [references/date-range-and-validation.md](references/datepicker-date-range-and-validation.md)
- Min and max date properties for range restriction
- Range validation and error states
- strictMode for automatic out-of-range correction
- Out-of-range behavior and error handling
- Disabling dates outside valid range
- Edge cases and gotchas

#### Date Views & Navigation
📄 **Read:** [references/date-views-and-navigation.md](references/datepicker-date-views-and-navigation.md)
- Start property (month, year, decade initial view)
- Depth property for restricting view levels
- Calendar navigation and user interactions
- Month and year selection shortcuts
- Navigating between different views
- Default behavior and best practices

#### Customization & Styling
📄 **Read:** [references/customization-and-styling.md](references/datepicker-customization-and-styling.md)
- CSS classes for styling (e-datepicker, e-calendar, e-day, etc.)
- renderDayCell event for day customization
- Disabling specific dates and weekends
- Placeholder, disabled, and readonly states
- Custom CSS and theme customization
- Day cell appearance and behavior

#### Globalization & Localization
📄 **Read:** [references/globalization-and-localization.md](references/datepicker-globalization-and-localization.md)
- Culture and locale configuration (German, French, Arabic, etc.)
- Loading CLDR data for internationalization
- Date format by culture (different countries, different formats)
- Locale text customization (today button, placeholder)
- Right-to-Left (RTL) support for Arabic, Hebrew, Urdu
- Week start day by culture
- Number formatting and calendar adjustments

#### Accessibility & Keyboard Navigation
📄 **Read:** [references/accessibility-and-keyboard.md](references/datepicker-accessibility-and-keyboard.md)
- WCAG 2.2 compliance and accessibility standards
- Keyboard navigation shortcuts (Alt+Down, arrow keys, Esc)
- ARIA attributes (aria-expanded, aria-disabled, aria-activedescendant)
- Screen reader support and announcements
- Focus management and visible focus indicators
- Color contrast and visual accessibility
- Mobile device support

#### Date Masking & Advanced Validation
📄 **Read:** [references/date-masking-and-strict-mode.md](references/datepicker-date-masking-and-strict-mode.md)
- `enableMask` property for structured segment-by-segment date input
- `maskPlaceholder` for custom segment placeholder text
- Date masking patterns for input guidance
- `strictMode` property behavior and enforcement
- Date parsing rules and validation logic
- Input validation and format enforcement
- Edge cases (leap years, month boundaries, etc.)
- Troubleshooting common validation issues
- Best practices for date input

### Quick Start Example

Here's a minimal working example to get started:

```jsx
import React, { useState } from 'react';
import { DatePickerComponent } from '@syncfusion/ej2-react-calendars';
import '@syncfusion/ej2-base/styles/material3.css';
import '@syncfusion/ej2-buttons/styles/material3.css';
import '@syncfusion/ej2-inputs/styles/material3.css';
import '@syncfusion/ej2-popups/styles/material3.css';
import '@syncfusion/ej2-react-calendars/styles/material3.css';

export default function App() {
  const [selectedDate, setSelectedDate] = useState(new Date());

  return (
    <div style={{ padding: '20px' }}>
      <h3>Select a Date</h3>
      <DatePickerComponent
        value={selectedDate}
        change={(e) => setSelectedDate(e.value)}
        placeholder="Enter date"
      />
      <p>Selected: {selectedDate?.toDateString()}</p>
    </div>
  );
}
```

**Key points:**
- Import `DatePickerComponent` from `@syncfusion/ej2-react-calendars`
- Import all required CSS themes (base, buttons, inputs, popups, calendars)
- Use `value` prop for the current date (can be null or Date object)
- Use `change` event (not `onChange`) to update React state — this is the Syncfusion event name
- DatePicker opens a calendar popup on click or Alt+Down arrow

### Common Patterns

#### 1. Date Range Picker (Min/Max Dates)
```jsx
<DatePickerComponent
  value={new Date()}
  min={new Date(2026, 0, 1)}
  max={new Date(2026, 11, 31)}
  placeholder="Select a date in 2026"
/>
```

#### 2. Custom Date Format
```jsx
<DatePickerComponent
  value={new Date()}
  format="dd/MM/yyyy"
  placeholder="DD/MM/YYYY"
/>
```

#### 3. Multiple Accepted Input Formats
```jsx
<DatePickerComponent
  value={new Date()}
  format="yyyy-MM-dd"
  inputFormats={['dd/MM/yyyy', 'yyyy-MM-dd', 'yyyyMMdd']}
  placeholder="Enter date (dd/MM/yyyy or yyyy-MM-dd)"
/>
```

#### 4. Year/Decade View for Birth Date Selection
```jsx
<DatePickerComponent
  value={new Date()}
  start="Decade"
  depth="Year"
  placeholder="Select year"
/>
```

#### 5. Disable Weekends
```jsx
<DatePickerComponent
  value={new Date()}
  renderDayCell={(args) => {
    if ((args.date.getDay()) === 0 || (args.date.getDay()) === 6) {
      args.isDisabled = true;
    }
  }}
  placeholder="Weekdays only"
/>
```

#### 6. Controlled Component in React Form
```jsx
const [date, setDate] = useState(null);

<DatePickerComponent
  value={date}
  change={(e) => setDate(e.value)}
  format="yyyy-MM-dd"
  strictMode={true}
  placeholder="Enter date"
/>
```

#### 7. German Culture with RTL Support
```jsx
<DatePickerComponent
  locale="de"
  enableRtl={false}
  firstDayOfWeek={1}
  value={new Date()}
  placeholder="Datum eingeben"
/>
```

#### 8. Masked Date Input
```jsx
<DatePickerComponent
  enableMask={true}
  format="MM/dd/yyyy"
  maskPlaceholder={{ day: 'DD', month: 'MM', year: 'YYYY' }}
  placeholder="Select a date"
/>
```

#### 9. Programmatic Control
```jsx
import { useRef } from 'react';

const datePickerRef = useRef(null);

// Open calendar
datePickerRef.current.show();

// Close calendar
datePickerRef.current.hide();

// Focus
datePickerRef.current.focusIn();

// Get current view
const view = datePickerRef.current.currentView(); // "Month" | "Year" | "Decade"

// Navigate to specific view
datePickerRef.current.navigateTo('Year', new Date(2026, 0, 1));

<DatePickerComponent ref={datePickerRef} value={new Date()} />
```

#### 10. Handle All Key Events
```jsx
<DatePickerComponent
  value={new Date()}
  change={(e) => console.log('Changed:', e.value)}
  focus={(e) => console.log('Focused')}
  blur={(e) => console.log('Blurred')}
  open={(e) => console.log('Opened')}
  close={(e) => console.log('Closed')}
  cleared={(e) => console.log('Cleared')}
  navigated={(e) => console.log('Navigated to view:', e.view)}
  renderDayCell={(args) => {
    // Disable weekends
    if (args.date.getDay() === 0 || args.date.getDay() === 6) {
      args.isDisabled = true;
    }
  }}
/>
```

## DateRangePicker 

The Syncfusion React **DateRangePickerComponent** enables users to select a start and end date range with built-in support for presets, validation, custom formatting, separator configuration, full-screen mobile mode, and advanced range constraints (minDays, maxDays, min, max).

### Documentation Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/daterangepicker-getting-started.md)
- Installation via npm (@syncfusion/ej2-react-calendars)
- CSS imports and theme configuration
- Basic DateRangePicker implementation
- Class component vs functional component setup
- Component initialization and structure
- Running development server
- Common troubleshooting

#### Date Range Selection
📄 **Read:** [references/date-range-selection.md](references/daterangepicker-date-range-selection.md)
- Start and end date properties
- Date range validation patterns
- Minimum and maximum date constraints
- Disabled dates configuration
- Date range presets (Last 7 days, Last 30 days, etc.)
- Value binding and two-way updates
- Read-only and disabled states
- Placeholder and labels

#### Date Range Formatting
📄 **Read:** [references/date-range-formatting.md](references/daterangepicker-date-range-formatting.md)
- Date format string options (MM/dd/yyyy, dd-MMM-yyyy, etc.)
- Display format vs input format
- Locale-based date formatting
- Custom separator between start and end dates
- Float label types (Never, Always, Auto)
- Placeholder text customization
- htmlAttributes for DOM attributes

#### Events and Methods
📄 **Read:** [references/events-and-methods.md](references/daterangepicker-events-and-methods.md)
- Event handlers (change, open, close, blur, focus, select)
- Event argument structures
- Methods (show, hide, focusIn, focusOut, reset, destroy)
- Imperative control with useRef
- Lifecycle events (created, destroyed)
- Event patterns and best practices
- Clearing values and state reset
- DateRangeSelectingEvent and ChangedEventArgs

#### Customization and Styling
📄 **Read:** [references/customization-and-styling.md](references/daterangepicker-customization-and-styling.md)
- CSS class customization with cssClass
- Theme options (Material, Bootstrap, Fluent, Tailwind, Fabric)
- Full-screen mode for mobile devices
- RTL (right-to-left) language support
- Preset ranges customization
- Z-index management
- Width and height configuration
- Accessibility features and ARIA attributes

#### API Reference
📄 **Read:** [references/api-reference.md](references/daterangepicker-api-reference.md)
- Complete properties list (35+ properties)
- All methods with signatures (8 methods)
- All events with event arguments (12 events)
- Type definitions and interfaces
- Default values and constraints
- Use cases for each property and method

#### Advanced Patterns
📄 **Read:** [references/advanced-patterns.md](references/daterangepicker-advanced-patterns.md)
- Form submission with date range validation
- Keyboard shortcuts and key navigation
- Server timezone offset handling
- Persistence and localStorage
- Multi-component integration (start/end date binding)
- Performance optimization with lazy loading
- Error handling and validation patterns
- Complex date range scenarios (fiscal years, quarters)

### Quick Start

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

### Common Patterns

#### Pattern 1: Date Range with Preset Options

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

#### Pattern 2: Date Range with Validation

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

#### Pattern 4: Event Handling and State Management

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

#### Pattern 5: Custom Date Range Format

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

### Key Props Reference

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

---

**Next Steps:**
- Read [references/getting-started.md](references/daterangepicker-getting-started.md) to install and set up your first DateRangePicker
- Explore [references/date-range-selection.md](references/daterangepicker-date-range-selection.md) for range selection patterns
- Check [references/date-range-formatting.md](references/daterangepicker-date-range-formatting.md) for format options
- See [references/advanced-patterns.md](references/daterangepicker-advanced-patterns.md) for complex scenarios
- Refer to [references/api-reference.md](references/daterangepicker-api-reference.md) for complete API documentation

## DateTimePicker

The Syncfusion React **DateTimePickerComponent** combines date and time selection in a single control. It offers calendar + time list popup, customizable time steps, masking, strict validation, timezone handling, format customization, and full keyboard accessibility.

### Documentation (read these references in order)
- 📄 Read: [references/getting-started.md](references/datetimepicker-getting-started.md) — installation, module setup, CSS imports, basic usage
- 📄 Read: [references/api-reference.md](references/datetimepicker-api-reference.md) — full properties, methods, and events
- 📄 Read: [references/date-time-selection.md](references/datetimepicker-date-time-selection.md) — selection patterns and constraints
- 📄 Read: [references/time-configuration.md](references/datetimepicker-time-configuration.md) — step, minTime/maxTime, scroll behavior
- 📄 Read: [references/events-and-methods.md](references/datetimepicker-events-and-methods.md) — event handlers and method usage
- 📄 Read: [references/styling-and-customization.md](references/datetimepicker-styling-and-customization.md) — themes and cssClass usage
- 📄 Read: [references/advanced-features.md](references/datetimepicker-advanced-features.md) — masked input, strict mode, calendar modes, timezone handling
- 📄 Read: [references/accessibility.md](references/datetimepicker-accessibility.md) — keyboard and ARIA guidance

### Quick Start (React + TypeScript)

1. Install package:

```bash
npm install @syncfusion/ej2-react-calendars
```

2. Import styles (in `index.css` or component CSS):

```css
@import '../node_modules/@syncfusion/ej2-base/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-calendars/styles/material3.css';
```

3. Minimal functional example (`App.tsx`):

```tsx
import React, { useState } from 'react';
import { DateTimePickerComponent } from '@syncfusion/ej2-react-calendars';

export default function App() {
  const [value, setValue] = useState<Date | null>(new Date());

  return (
    <div style={{ padding: 20 }}>
      <h3>Choose date and time</h3>
      <DateTimePickerComponent
        value={value}
        change={(e) => setValue((e as any).value)}
        format="dd/MM/yyyy hh:mm a"
        step={15}
        placeholder="Select date and time"
      />
      <p>Selected: {value ? value.toString() : 'none'}</p>
    </div>
  );
}
```

### Common Patterns
- Controlled value: bind `value` and update on `change`.
- Range enforcement: use `min` and `max` for dates, `minTime`/`maxTime` for times.
- Masked input: enable with `enableMask` and provide `maskPlaceholder`.
- Localization: set `locale` or use global culture settings.
- Keyboard-first: provide `keyConfigs` for custom shortcuts.

### Key Props Summary (see API reference for full list)
- `value`, `min`, `max`, `step`, `format`, `enableMask`, `placeholder`, `cssClass`, `locale`, `readonly`, `enabled`.

### Key Events
- `change`, `open`, `close`, `created`, `destroyed`, `navigated`, `blur`, `focus`, `renderDayCell`.

### Next steps
- All reference files have been created and validated against the official Syncfusion API (see `references/api-reference.md`).
- Next: run the test-case guide and validation checks, then create automated examples or add platform-specific notes on request.
- Ask me to run tests, update `completion-status.json`, or produce publish-ready artifacts.

## TimePicker

The Syncfusion React **TimePickerComponent** is a lightweight and feature-rich control for selecting time values. It supports 12/24-hour formats, time stepping, min/max constraints, masked input, localization, full-screen mode, and easy integration into React forms.

### Documentation Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/timepicker-getting-started.md)
- Installation via npm (@syncfusion/ej2-react-calendars)
- CalendarModule setup in app.module.ts
- CSS imports and theme configuration
- Basic TimePicker implementation
- Component registration with useRef
- Running development server
- Common troubleshooting

#### Time Format and Display
📄 **Read:** [references/time-format-and-display.md](references/timepicker-time-format-and-display.md)
- Format string options (24-hour, 12-hour formats)
- TimeFormatObject with skeleton property
- Locale-based time formatting
- Placeholder text customization
- Float label types (Never, Always, Auto)
- htmlAttributes for DOM attributes
- Masked input with enableMask
- Mask placeholder configuration

#### Time Range and Selection
📄 **Read:** [references/time-range-and-selection.md](references/timepicker-time-range-and-selection.md)
- Minimum and maximum time constraints
- Time step intervals (15, 30, 60 minutes)
- ScrollTo default position
- Value binding and two-way updates
- Read-only and disabled states
- OpenOnFocus behavior
- Time popup list population
- Stepped time intervals

#### Events and Methods
📄 **Read:** [references/events-and-methods.md](references/timepicker-events-and-methods.md)
- Event handlers (change, open, close, blur, focus)
- Event argument structures
- Methods (show, hide, focusIn, focusOut)
- Imperative control with useRef
- Lifecycle events (created, destroyed)
- Event patterns and best practices
- Clearing values and state reset
- ItemRender for custom formatting

#### Customization and Styling
📄 **Read:** [references/customization-and-styling.md](references/timepicker-customization-and-styling.md)
- CSS class customization with cssClass
- Theme options (Material, Bootstrap, Fluent, Tailwind)
- Full-screen mode for mobile devices
- RTL (right-to-left) language support
- Strict mode validation
- Z-index management
- Width and height configuration
- Accessibility features
- Theme Studio integration

#### API Reference
📄 **Read:** [references/api-reference.md](references/timepicker-api-reference.md)
- Complete properties list (26 properties)
- All methods with signatures (5 methods)
- All events with event arguments (9 events)
- Type definitions and interfaces
- Default values and constraints
- Use cases for each property

#### Advanced Patterns
📄 **Read:** [references/advanced-patterns.md](references/timepicker-advanced-patterns.md)
- Form submission with validation
- Keyboard shortcuts and keyConfigs
- Server timezone offset handling
- Persistence and localStorage
- Multi-component integration
- Performance optimization
- Error handling patterns
- Complex validation scenarios

### Quick Start

```tsx
import { TimePickerComponent } from '@syncfusion/ej2-react-calendars';
import * as React from 'react';
import '@syncfusion/ej2-base/styles/material3.css';
import '@syncfusion/ej2-calendars/styles/material3.css';

function App() {
  const [selectedTime, setSelectedTime] = React.useState(new Date('1/1/2018 9:00 AM'));

  const handleChange = (e: any) => {
    setSelectedTime(e.value);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Select Time</h2>
      <TimePickerComponent
        value={selectedTime}
        change={handleChange}
        placeholder="Select a time"
      />
      <p>Selected: {selectedTime ? selectedTime.toLocaleTimeString() : 'None'}</p>
    </div>
  );
}

export default App;
```

### Common Patterns

#### Pattern 1: Time Picker with Min/Max Constraints

```tsx
import { TimePickerComponent } from '@syncfusion/ej2-react-calendars';
import * as React from 'react';

function AppointmentScheduler() {
  const [appointmentTime, setAppointmentTime] = React.useState(new Date('1/1/2018 9:00 AM'));

  const minTime = new Date('1/1/2018 8:00 AM');
  const maxTime = new Date('1/1/2018 5:00 PM');

  return (
    <div>
      <h3>Select Appointment Time (8 AM - 5 PM)</h3>
      <TimePickerComponent
        value={appointmentTime}
        min={minTime}
        max={maxTime}
        step={30}
        change={(e: any) => setAppointmentTime(e.value)}
        placeholder="Choose time"
      />
    </div>
  );
}

export default AppointmentScheduler;
```

#### Pattern 2: Form with Time Picker Submission

```tsx
import { TimePickerComponent } from '@syncfusion/ej2-react-calendars';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function ScheduleForm() {
  const [formData, setFormData] = React.useState({
    startTime: new Date('1/1/2018 9:00 AM'),
    endTime: new Date('1/1/2018 5:00 PM'),
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Schedule data:', {
      startTime: formData.startTime?.toLocaleTimeString(),
      endTime: formData.endTime?.toLocaleTimeString(),
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>Schedule Meeting</h3>
      
      <label>Start Time:</label>
      <TimePickerComponent
        value={formData.startTime}
        change={(e: any) => setFormData(prev => ({ ...prev, startTime: e.value }))}
      />

      <label style={{ marginTop: '10px' }}>End Time:</label>
      <TimePickerComponent
        value={formData.endTime}
        min={formData.startTime}
        change={(e: any) => setFormData(prev => ({ ...prev, endTime: e.value }))}
      />

      <ButtonComponent type="submit" isPrimary={true} style={{ marginTop: '15px' }}>
        Schedule
      </ButtonComponent>
    </form>
  );
}

export default ScheduleForm;
```

#### Pattern 3: Time Picker with Custom Format

```tsx
import { TimePickerComponent } from '@syncfusion/ej2-react-calendars';
import * as React from 'react';

function TimeFormatDemo() {
  const [time12hr, setTime12hr] = React.useState(new Date('1/1/2018 2:30 PM'));
  const [time24hr, setTime24hr] = React.useState(new Date('1/1/2018 14:30'));

  return (
    <div style={{ padding: '20px' }}>
      <div>
        <h4>12-Hour Format (hh:mm a)</h4>
        <TimePickerComponent
          value={time12hr}
          format="hh:mm a"
          change={(e: any) => setTime12hr(e.value)}
        />
        <p>Value: {time12hr?.toLocaleTimeString('en-US', { hour12: true })}</p>
      </div>

      <div style={{ marginTop: '20px' }}>
        <h4>24-Hour Format (HH:mm)</h4>
        <TimePickerComponent
          value={time24hr}
          format="HH:mm"
          change={(e: any) => setTime24hr(e.value)}
        />
        <p>Value: {time24hr?.toLocaleTimeString('en-US', { hour12: false })}</p>
      </div>
    </div>
  );
}

export default TimeFormatDemo;
```

#### Pattern 4: Event Handling and State Management

```tsx
import { TimePickerComponent } from '@syncfusion/ej2-react-calendars';
import * as React from 'react';

function EventTrackingExample() {
  const [selectedTime, setSelectedTime] = React.useState<Date | null>(null);
  const [eventLog, setEventLog] = React.useState<string[]>([]);

  const handleChange = (e: any) => {
    setSelectedTime(e.value);
    setEventLog(prev => [...prev, `Changed: ${e.value?.toLocaleTimeString()}`]);
  };

  const handleOpen = (e: any) => {
    setEventLog(prev => [...prev, 'Popup opened']);
  };

  const handleClose = (e: any) => {
    setEventLog(prev => [...prev, 'Popup closed']);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h3>Time Picker with Event Tracking</h3>
      <TimePickerComponent
        value={selectedTime}
        change={handleChange}
        open={handleOpen}
        close={handleClose}
        placeholder="Select time to track events"
      />

      <div style={{ marginTop: '20px', padding: '10px', border: '1px solid #ccc' }}>
        <h4>Event Log:</h4>
        <ul>
          {eventLog.map((event, idx) => (
            <li key={idx}>{event}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default EventTrackingExample;
```

#### Pattern 5: Masked Time Input

```tsx
import { TimePickerComponent } from '@syncfusion/ej2-react-calendars';
import * as React from 'react';

function MaskedTimePickerExample() {
  const [maskedTime, setMaskedTime] = React.useState(new Date('1/1/2018 10:30 AM'));

  return (
    <div style={{ padding: '20px' }}>
      <h3>Masked Time Input</h3>
      <TimePickerComponent
        value={maskedTime}
        enableMask={true}
        format="hh:mm a"
        maskPlaceholder={{
          hour: 'HH',
          minute: 'MM',
          second: 'SS',
        }}
        change={(e: any) => setMaskedTime(e.value)}
        placeholder="Enter time (HH:MM AM/PM)"
      />
      <p>Masked input helps users enter time in correct format</p>
    </div>
  );
}

export default MaskedTimePickerExample;
```

### Key Props Reference

| Prop | Type | Default | Purpose |
|------|------|---------|---------|
| `value` | Date | null | Current selected time value |
| `format` | string | Based on culture | Time display format (e.g., "HH:mm", "hh:mm a") |
| `min` | Date | 00:00 | Minimum selectable time |
| `max` | Date | 00:00 | Maximum selectable time |
| `step` | number | 30 | Time interval in minutes between list items |
| `enabled` | boolean | true | Enable/disable the component |
| `readonly` | boolean | false | Read-only state (no editing) |
| `placeholder` | string | - | Input placeholder text |
| `openOnFocus` | boolean | false | Open popup on input focus |
| `enableMask` | boolean | false | Enable masked input mode |
| `enableRtl` | boolean | false | Enable right-to-left layout |
| `strictMode` | boolean | false | Validate input and restrict to valid times |
| `showClearButton` | boolean | true | Show/hide clear button |
| `fullScreenMode` | boolean | false | Mobile full-screen mode |
| `cssClass` | string | - | Custom CSS class for styling |
| `floatLabelType` | string | Never | Float label position |
| `allowEdit` | boolean | true | Allow manual input editing |
| `locale` | string | 'en-US' | Locale for time formatting |
| `scrollTo` | Date | - | Default scroll position in popup |
| `width` | string/number | - | Component width |
| `zIndex` | number | 1000 | Z-index of popup |
| `serverTimezoneOffset` | number | - | Server timezone offset for processing |
| `htmlAttributes` | object | {} | Custom HTML attributes |

---

**Next Steps:**
- Read [references/getting-started.md](references/timepicker-getting-started.md) to install and set up your first TimePicker
- Explore [references/time-format-and-display.md](references/timepicker-time-format-and-display.md) for format options
- Check [references/time-range-and-selection.md](references/timepicker-time-range-and-selection.md) for time constraints
- See [references/advanced-patterns.md](references/timepicker-advanced-patterns.md) for complex scenarios
