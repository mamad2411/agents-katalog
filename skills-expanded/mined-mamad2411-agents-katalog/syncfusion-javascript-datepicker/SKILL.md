---
name: syncfusion-javascript-datepicker
description: Implement Syncfusion EJ2 DatePicker in TypeScript applications for intuitive date selection. Use this skill whenever the user needs to add date picking functionality, configure date ranges, format dates for different locales, highlight special dates, or create inline calendars. Includes setup, date formatting, behavior customization, special date highlighting, state persistence, keyboard navigation, and accessibility.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion JavaScript DatePicker

The Syncfusion EJ2 DatePicker is a feature-rich component for selecting dates with intuitive calendar navigation. It supports multiple calendar views (month, year, decade, century), date range constraints, custom formatting, special date highlighting, and full keyboard accessibility.

## When to Use This Skill

Use DatePicker when you need to:
- **Add date selection** - Users pick dates through a calendar popup or inline display
- **Constrain date ranges** - Limit selectable dates between min/max values
- **Format dates** - Display dates in culture-specific or custom formats
- **Highlight special dates** - Mark birthdays, events, holidays with custom styling
- **Support inline calendar** - Display persistent calendar always visible
- **Enable keyboard navigation** - Allow Alt+Down, arrow keys, and other shortcuts
- **Persist date selections** - Save and restore selected dates across sessions
- **Ensure accessibility** - Provide WCAG 2.2 compliance and screen reader support

## Quick Start Example

```typescript
import { DatePicker } from '@syncfusion/ej2-calendars';
import '@syncfusion/ej2-base/styles/material.css';
import '@syncfusion/ej2-calendars/styles/material.css';

// Create DatePicker from input element
const datePicker = new DatePicker({
  value: new Date(),
  placeholder: 'Select a date',
  min: new Date(2024, 0, 1),
  max: new Date(2026, 11, 31),
  format: 'MMM dd, yyyy'
});

datePicker.appendTo('#datepicker');

// Handle value changes
datePicker.change = (args) => {
  console.log('Selected date:', args.value);
};
```

**HTML:**
```html
<input id="datepicker" />
```

## Key Features

- **Calendar Views**: Month → Year → Decade → Century (drill-down/up navigation)
- **Date Range**: minDate/maxDate constraints with disabled date styling
- **Strict Mode**: Validate input and prevent invalid dates
- **Formatting**: Culture-specific and custom date formats
- **Special Dates**: Highlight birthdays, events, holidays with custom styling
- **Inline Display**: Always-visible calendar instead of popup
- **Keyboard Navigation**: Full Alt+key and Ctrl+key support
- **State Persistence**: Save/restore selections with localStorage
- **Accessibility**: WCAG 2.2 compliant, screen reader support, ARIA attributes
- **Theming**: Material, Fabric, Bootstrap themes with customization

## Documentation & Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Creating DatePicker from input element
- Basic date selection example
- CSS theme imports
- Initial value configuration
- Change event handling

### Date Formatting & Display
📄 **Read:** [references/date-formats.md](references/date-formats.md)
- Format pattern syntax (d, dd, M, MM, yyyy, etc.)
- Standard date formats (default, short, medium, full, UTC)
- Header format customization
- Day header format (short/medium/long)
- Tooltip formatting on hover
- Locale-specific date formats
- Culture considerations

### Behavior Settings & Date Range
📄 **Read:** [references/behavior-settings.md](references/behavior-settings.md)
- Selected date and value property
- Date range constraints (minDate, maxDate)
- Strict mode validation (enableStrictMode)
- Calendar start/depth levels (month, year, decade, century)
- Inline mode display
- Change events and callbacks
- Multi-view navigation patterns

### Special Dates & Visual Enhancement
📄 **Read:** [references/special-dates.md](references/special-dates.md)
- Highlighting special dates with custom styling
- Special date array structure
- Field mapping configuration (date, iconCSS, tooltip)
- Icon CSS classes for markers
- Custom tooltips on hover
- Use cases: birthdays, events, holidays
- Color-coded date categories

### Customization & Styling
📄 **Read:** [references/customization.md](references/customization.md)
- Setting dimensions (height, width)
- Responsive width (100% for mobile)
- Footer display and "Today" button
- Popup button visibility
- Show/hide other month days
- CSS class customization
- Theme switching and Theme Studio
- Advanced styling examples

### State Persistence
📄 **Read:** [references/state-persistence.md](references/state-persistence.md)
- Saving date selections to localStorage
- Retrieving persisted state on load
- Automatic restoration on page refresh
- Clearing saved state
- Multi-page state sharing patterns
- State management best practices
- Debugging state issues

### Accessibility & Keyboard Navigation
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- Keyboard shortcut keys (Alt+Down, arrows, Enter, Esc)
- Ctrl combinations for view navigation
- Enabling keyboard navigation (allowKeyboardNavigation)
- Screen reader support
- ARIA attributes
- Focus management
- Keyboard testing checklist

## Common Patterns

### Pattern 1: Date Range Picker (Min/Max)

```typescript
const datePicker = new DatePicker({
  value: new Date(2025, 5, 15),
  min: new Date(2025, 0, 1),      // Start of year
  max: new Date(2025, 11, 31),    // End of year
  format: 'MMM dd, yyyy',
  enableStrictMode: true          // Prevent out-of-range dates
});

datePicker.appendTo('#datepicker');
```

**Use when:** Users can only select dates within a specific range (booking dates, membership periods, fiscal years).

### Pattern 2: Inline Calendar (Always Visible)

```typescript
const datePicker = new DatePicker({
  displayInline: true,
  showFooter: true,
  value: new Date()
});

datePicker.appendTo('#calendar');
```

**Use when:** Calendar should always be visible (dashboard, schedule builder, appointment interface).

### Pattern 3: Format for International Audiences

```typescript
const datePicker = new DatePicker({
  locale: 'de-DE',              // German format
  dateFormat: 'dd.MM.yyyy',
  value: new Date()
});

datePicker.appendTo('#datepicker');
```

**Use when:** Application must display dates in locale-specific format (international apps, multi-language support).

### Pattern 4: Highlight Important Dates

```typescript
const specialDates = [
  { specialdate: '28/06/2025', customClass: 'birthday', tooltip: 'John\'s Birthday' },
  { specialdate: '25/12/2025', customClass: 'holiday', tooltip: 'Christmas' },
  { specialdate: '01/01/2026', customClass: 'holiday', tooltip: 'New Year' }
];

const datePicker = new DatePicker({
  specialDates: specialDates,
  fields: { date: 'specialdate', iconCSS: 'customClass', tooltip: 'tooltip' }
});

datePicker.appendTo('#datepicker');
```

**Use when:** Calendar needs visual markers for events, holidays, or important dates.

### Pattern 5: Year/Decade Navigation

```typescript
const datePicker = new DatePicker({
  startLevel: 'year',            // Start in year view
  depthLevel: 'year',            // Return value when year selected
  dateFormat: 'MMMM yyyy'
});

datePicker.appendTo('#datepicker');
```

**Use when:** Users primarily select month/year without specific day (billing period, report month).

## Key Configuration Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `value` | Date | null | Selected date |
| `min` | Date/String | null | Minimum selectable date |
| `max` | Date/String | null | Maximum selectable date |
| `format` | String | 'M/d/yyyy' | Display format pattern |
| `dateFormat` | String | Based on locale | Alias for format |
| `locale` | String | 'en-US' | Culture/language for formatting |
| `displayInline` | Boolean | false | Always-visible calendar |
| `enableStrictMode` | Boolean | true | Reject invalid dates |
| `startLevel` | String | 'month' | Initial calendar view |
| `depthLevel` | String | 'month' | When to return value |
| `showFooter` | Boolean | true | Show "Today" button |
| `showPopupButton` | Boolean | true | Show calendar toggle button |
| `showOtherMonths` | Boolean | true | Show days from adjacent months |
| `specialDates` | Array | [] | Highlighted date array |
| `fields` | Object | {} | Special date field mapping |
| `change` | Function | null | Fired when date changes |
| `created` | Function | null | Fired on initialization |

## Best Practices

### 1. Always Set Date Format Explicitly

```typescript
// ✓ Good: Explicit format prevents confusion
const datePicker = new DatePicker({
  format: 'dd/MM/yyyy',
  value: new Date()
});

// ✗ Avoid: Relying on browser locale
const datePicker = new DatePicker({
  value: new Date()
});
```

### 2. Use Strict Mode for Validation

```typescript
// ✓ Good: Strict mode prevents invalid dates
const datePicker = new DatePicker({
  enableStrictMode: true,
  min: new Date(2025, 0, 1),
  max: new Date(2025, 11, 31)
});

// ✗ Avoid: Loose validation
const datePicker = new DatePicker({
  enableStrictMode: false
});
```

### 3. Handle Change Events Properly

```typescript
// ✓ Good: Check both value and previous date
datePicker.change = (args) => {
  console.log('Previous:', args.prevDate);
  console.log('New:', args.value);
  // Trigger validation or dependent updates
};

// ✗ Avoid: Ignoring event arguments
datePicker.change = () => {
  console.log('Date changed');
};
```

### 4. Consider Responsive Design

```typescript
// ✓ Good: Responsive width
const datePicker = new DatePicker({
  width: '100%',
  value: new Date()
});

// ✗ Avoid: Fixed width on mobile
const datePicker = new DatePicker({
  width: '300px'
});
```

### 5. Provide Clear Placeholder Text

```typescript
// ✓ Good: Helpful placeholder
const datePicker = new DatePicker({
  placeholder: 'Select checkout date (YYYY-MM-DD)',
  value: new Date()
});

// ✗ Avoid: No context
const datePicker = new DatePicker({
  value: new Date()
});
```

## Common Gotchas

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| Dates show in wrong format | Locale not set or mismatch | Set `locale` and `dateFormat` explicitly |
| Min/max not working | Dates in wrong timezone | Use consistent Date objects or ISO strings |
| Special dates not showing | Field mapping incorrect | Verify `fields` property matches data structure |
| Keyboard shortcuts not working | `allowKeyboardNavigation` false | Enable in config (may be control default) |
| Inline calendar too large | Parent container constrained | Set explicit width/height on parent |
| State not persisting | localStorage disabled | Check browser settings and privacy mode |

## Next Steps

1. **Choose your use case** from Common Patterns above
2. **Read the specific reference** for detailed implementation
3. **Check the Key Configuration Properties** for available options
4. **Review Best Practices** before deployment
5. **Test with keyboard** to verify accessibility

## Related Components

- **TimePicker** - Time selection complementary to DatePicker
- **DateRangePicker** - Select start and end dates
- **DateTimePicker** - Combined date and time picker
- **Calendar** - Month view without date input
