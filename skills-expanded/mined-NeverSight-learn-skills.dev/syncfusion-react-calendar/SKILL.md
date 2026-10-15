---
name: syncfusion-react-calendar
description: Comprehensive guide for implementing the Syncfusion React Calendar component with quick navigation, when-to-use guidance, and reference links for common tasks. Use this skill for copy-paste-ready examples and decision guidance for date selection UI in React applications.
metadata:
  author: "Syncfusion Inc"
  category: "Calendars"
  version: "33.1.44"
---

# Implementing Calendar (React)

## Table of Contents
- [When to Use This Skill](#when-to-use-this-skill)
- [Overview](#overview)
- [Quick Start (React)](#quick-start-react)
- [Guidance & Patterns](#guidance--patterns)
- [References](#references)
- [Troubleshooting & Tips](#troubleshooting--tips)

## Overview

This skill provides: a short React Quick Start, recommended patterns (single-date, range selection, controlled components), and two reference files: a React-specific getting-started and a concise API reference derived from the Syncfusion React Calendar docs.

Target package: `@syncfusion/ej2-react-calendars` (CalendarComponent)

## Quick Start (React)

### Install

```bash
npm install @syncfusion/ej2-react-calendars @syncfusion/ej2-base
```

### Basic Example (App.jsx)

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

## Guidance & Patterns

- **Controlled component:** keep source-of-truth in React state and update `value` via `change` event.
- **Multi-selection:** use `isMultiSelection={true}` with `values` prop and `addDate()`/`removeDate()` methods.
- **Programmatic navigation:** use a `ref` to call `navigateTo(view, date)` — both arguments are required (see references/getting-started-react.md).
- **Date ranges:** for range selection, use DateRangePicker (separate component). The Calendar itself does not have a built-in range highlight mode.
- **Accessibility:** use wrapper elements with `role="region"` and a separate `aria-live` region for announcements — these are not direct Calendar props.
- **Week numbers:** enable with `weekNumber={true}` (the correct prop name).

## References

Navigate to the reference that matches your current task:

### Getting Started
📄 **Read:** [references/getting-started-react.md](references/getting-started-react.md)
- Installation and npm setup
- React component examples
- CSS/theme imports
- Using refs and methods

### Date Selection
📄 **Read:** [references/date-selection.md](references/date-selection.md)
- Single date selection
- Multiple dates and ranges
- Min/max constraints
- Disabling specific dates

### Calendar Views
📄 **Read:** [references/calendar-views.md](references/calendar-views.md)
- Month, Year, Decade views
- Navigating between views
- Initial and depth controls
- Programmatic navigation

### Styling & Customization
📄 **Read:** [references/styling-customization.md](references/styling-customization.md)
- Theme selection and switching
- CSS class customization
- Custom day cell rendering
- RTL and responsive design

### Events & Methods
📄 **Read:** [references/events-methods.md](references/events-methods.md)
- Event handlers (change, created, renderDayCell)
- Using refs and imperative methods
- Advanced renderDayCell hook
- Event tracking patterns

### Accessibility & Globalization
📄 **Read:** [references/accessibility-globalization.md](references/accessibility-globalization.md)
- WCAG 2.1 compliance
- Keyboard navigation
- ARIA attributes
- Locale support and RTL
- Testing for accessibility

### API Reference (Quick Lookup)
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Props, events, methods at a glance
- Common enums and types
- Link to upstream docs

## Troubleshooting & Tips

- **Styles not applied:** confirm CSS imports point to `node_modules/@syncfusion/ej2-calendars/styles/` and are loaded before component styles.
- **React state mismatch:** use the `value` prop and `change` event to keep React state in sync — do not rely on framework-specific bindings.
- **Multiple date selection not working:** ensure `isMultiSelection={true}` and use `values` (not `value`) for the initial array.
- **`navigateTo` not working:** the method requires two arguments — `navigateTo(view: CalendarView, date: Date)`.
- **"Cannot find module":** run `npm install @syncfusion/ej2-react-calendars @syncfusion/ej2-base` and confirm `package.json`.
- **Week numbers not showing:** use `weekNumber={true}` (not `showWeekNumber`).

---
