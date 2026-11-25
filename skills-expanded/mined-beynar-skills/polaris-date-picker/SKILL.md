---
name: polaris-date-picker
description: Shopify Polaris Date picker component. Use this skill when merchants need to select single dates or date ranges, calendar-based date selection. Provides visual calendar for consistently applied date selection across Shopify.
---

# Date picker

## When to use

Let merchants choose dates from a visual calendar. Use when merchants need to select a single day close to today or a range of dates.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `selected` | Range \| Date | - | Selected date or range |
| `month` | number | - | Month to show (0-11, 0=January) |
| `year` | number | - | Year to show |
| `id` | string | - | ID for element |
| `allowRange` | boolean | false | Allow range of dates to be selected |
| `disableDatesBefore` | Date | - | Disable selecting dates before this |
| `disableDatesAfter` | Date | - | Disable selecting dates after this |
| `disableSpecificDates` | Date[] | - | Disable specific dates |
| `multiMonth` | boolean | false | Selection can span multiple months |
| `weekStartsOn` | number | 0 | First day of week (0-6, 0=Sunday) |
| `dayAccessibilityLabelPrefix` | string | - | Prefix for selected days (single selection) |
| `onChange` | (date: Range) => void | - | Callback when date selected |
| `onMonthChange` | (month: number, year: number) => void | - | Callback when month changed |

## Examples

```jsx
import { DatePicker } from '@shopify/polaris';
import { useState, useCallback } from 'react';

function DatePickerExample() {
  const [{ month, year }, setDate] = useState({ month: 1, year: 2024 });
  const [selectedDates, setSelectedDates] = useState({
    start: new Date('Wed Feb 07 2024'),
    end: new Date('Wed Feb 07 2024'),
  });

  const handleMonthChange = useCallback(
    (month, year) => setDate({ month, year }),
    []
  );

  return (
    <DatePicker
      month={month}
      year={year}
      onChange={setSelectedDates}
      onMonthChange={handleMonthChange}
      selected={selectedDates}
    />
  );
}

// Single date
function SingleDatePicker() {
  const [{ month, year }, setDate] = useState({ month: 1, year: 2024 });
  const [selectedDate, setSelectedDate] = useState(new Date());

  return (
    <DatePicker
      month={month}
      year={year}
      onChange={setSelectedDate}
      onMonthChange={(m, y) => setDate({ month: m, year: y })}
      selected={selectedDate}
    />
  );
}
```

## Best practices

- Use smart defaults and highlight common selections
- Close after single date selection unless range required
- Set start date on first click, end date on second click for ranges
- Not for dates many years in future/past
- Follow date format guidelines
- Always provide text field alternative for accessibility

## Accessibility

- Always give users option to enter date via text field
- If using within popover, use button to trigger instead of focus
- Keyboard: Tab through previous/next buttons and calendar, Arrow keys to navigate dates, Enter to select

## Related patterns

- Date picking pattern in documentation

## Related components

- Text field: for manual date entry
- Popover: for overlay containing date picker
