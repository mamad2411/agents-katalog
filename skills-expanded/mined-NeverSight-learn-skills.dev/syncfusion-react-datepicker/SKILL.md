---
name: syncfusion-react-datepicker
description: Implement Syncfusion React DatePicker component with comprehensive guidance on date selection, formatting, validation, and accessibility. Use this when working with date input fields, date range pickers, custom date formats, locale-specific date handling, or keyboard navigation. This skill covers installation, setup, date formatting, validation, styling, globalization, and accessibility features.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Calendars"
---

# Implementing DatePicker

## Component Overview

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

## Complete API Summary

### Key Properties
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

### Methods
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

### Events
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

## Documentation & Navigation Guide

When the user needs help with DatePicker, guide them to the appropriate reference:

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation via npm (@syncfusion/ej2-react-calendars)
- CSS theme imports (material3, bootstrap, fluent, tailwind)
- Component imports and setup
- Basic JSX implementation with DatePickerComponent
- Functional vs class component examples
- Running your first application

### Date Formats & Input
📄 **Read:** [references/date-formats-and-input.md](references/date-formats-and-input.md)
- Display format property and patterns (yyyy-MM-dd, dd/MM/yyyy, etc.)
- Custom format specifiers (# and 0 patterns)
- Input formats for flexible date entry (accepting multiple formats)
- Format examples with real-world scenarios
- Parsing and converting user input automatically
- Culture-based default formatting

### Date Range & Validation
📄 **Read:** [references/date-range-and-validation.md](references/date-range-and-validation.md)
- Min and max date properties for range restriction
- Range validation and error states
- strictMode for automatic out-of-range correction
- Out-of-range behavior and error handling
- Disabling dates outside valid range
- Edge cases and gotchas

### Date Views & Navigation
📄 **Read:** [references/date-views-and-navigation.md](references/date-views-and-navigation.md)
- Start property (month, year, decade initial view)
- Depth property for restricting view levels
- Calendar navigation and user interactions
- Month and year selection shortcuts
- Navigating between different views
- Default behavior and best practices

### Customization & Styling
📄 **Read:** [references/customization-and-styling.md](references/customization-and-styling.md)
- CSS classes for styling (e-datepicker, e-calendar, e-day, etc.)
- renderDayCell event for day customization
- Disabling specific dates and weekends
- Placeholder, disabled, and readonly states
- Custom CSS and theme customization
- Day cell appearance and behavior

### Globalization & Localization
📄 **Read:** [references/globalization-and-localization.md](references/globalization-and-localization.md)
- Culture and locale configuration (German, French, Arabic, etc.)
- Loading CLDR data for internationalization
- Date format by culture (different countries, different formats)
- Locale text customization (today button, placeholder)
- Right-to-Left (RTL) support for Arabic, Hebrew, Urdu
- Week start day by culture
- Number formatting and calendar adjustments

### Accessibility & Keyboard Navigation
📄 **Read:** [references/accessibility-and-keyboard.md](references/accessibility-and-keyboard.md)
- WCAG 2.2 compliance and accessibility standards
- Keyboard navigation shortcuts (Alt+Down, arrow keys, Esc)
- ARIA attributes (aria-expanded, aria-disabled, aria-activedescendant)
- Screen reader support and announcements
- Focus management and visible focus indicators
- Color contrast and visual accessibility
- Mobile device support

### Date Masking & Advanced Validation
📄 **Read:** [references/date-masking-and-strict-mode.md](references/date-masking-and-strict-mode.md)
- `enableMask` property for structured segment-by-segment date input
- `maskPlaceholder` for custom segment placeholder text
- Date masking patterns for input guidance
- `strictMode` property behavior and enforcement
- Date parsing rules and validation logic
- Input validation and format enforcement
- Edge cases (leap years, month boundaries, etc.)
- Troubleshooting common validation issues
- Best practices for date input

## Quick Start Example

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

## Common Patterns

### 1. Date Range Picker (Min/Max Dates)
```jsx
<DatePickerComponent
  value={new Date()}
  min={new Date(2026, 0, 1)}
  max={new Date(2026, 11, 31)}
  placeholder="Select a date in 2026"
/>
```

### 2. Custom Date Format
```jsx
<DatePickerComponent
  value={new Date()}
  format="dd/MM/yyyy"
  placeholder="DD/MM/YYYY"
/>
```

### 3. Multiple Accepted Input Formats
```jsx
<DatePickerComponent
  value={new Date()}
  format="yyyy-MM-dd"
  inputFormats={['dd/MM/yyyy', 'yyyy-MM-dd', 'yyyyMMdd']}
  placeholder="Enter date (dd/MM/yyyy or yyyy-MM-dd)"
/>
```

### 4. Year/Decade View for Birth Date Selection
```jsx
<DatePickerComponent
  value={new Date()}
  start="Decade"
  depth="Year"
  placeholder="Select year"
/>
```

### 5. Disable Weekends
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

### 6. Controlled Component in React Form
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

### 7. German Culture with RTL Support
```jsx
<DatePickerComponent
  locale="de"
  enableRtl={false}
  firstDayOfWeek={1}
  value={new Date()}
  placeholder="Datum eingeben"
/>
```

### 8. Masked Date Input
```jsx
<DatePickerComponent
  enableMask={true}
  format="MM/dd/yyyy"
  maskPlaceholder={{ day: 'DD', month: 'MM', year: 'YYYY' }}
  placeholder="Select a date"
/>
```

### 9. Programmatic Control
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

### 10. Handle All Key Events
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

