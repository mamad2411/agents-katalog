---
name: syncfusion-react-datetimepicker
description: Comprehensive guide for implementing the Syncfusion React DateTimePicker component. Use this when working with combined date and time inputs, datetime formatting, localization, or keyboard-accessible UIs in React applications. Covers component setup, event handling, and accessibility patterns.
metadata:
  author: "Syncfusion Inc"
  category: "Calendars"
  version: "33.1.44"
---

# DateTimePicker (implementing-datetimepicker)

## Component Overview
The Syncfusion `DateTimePickerComponent` provides a combined calendar and time picker with extensive configurability: min/max dates, time steps, masked input, localization, strict validation, RTL, and accessible keyboard navigation.

## Documentation (read these references in order)
- 📄 Read: [references/getting-started.md](references/getting-started.md) — installation, module setup, CSS imports, basic usage
- 📄 Read: [references/api-reference.md](references/api-reference.md) — full properties, methods, and events
- 📄 Read: [references/date-time-selection.md](references/date-time-selection.md) — selection patterns and constraints
- 📄 Read: [references/time-configuration.md](references/time-configuration.md) — step, minTime/maxTime, scroll behavior
- 📄 Read: [references/events-and-methods.md](references/events-and-methods.md) — event handlers and method usage
- 📄 Read: [references/styling-and-customization.md](references/styling-and-customization.md) — themes and cssClass usage
- 📄 Read: [references/advanced-features.md](references/advanced-features.md) — masked input, strict mode, calendar modes, timezone handling
- 📄 Read: [references/accessibility.md](references/accessibility.md) — keyboard and ARIA guidance

## Quick Start (React + TypeScript)

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

## Common Patterns
- Controlled value: bind `value` and update on `change`.
- Range enforcement: use `min` and `max` for dates, `minTime`/`maxTime` for times.
- Masked input: enable with `enableMask` and provide `maskPlaceholder`.
- Localization: set `locale` or use global culture settings.
- Keyboard-first: provide `keyConfigs` for custom shortcuts.

## Key Props Summary (see API reference for full list)
- `value`, `min`, `max`, `step`, `format`, `enableMask`, `placeholder`, `cssClass`, `locale`, `readonly`, `enabled`.

## Key Events
- `change`, `open`, `close`, `created`, `destroyed`, `navigated`, `blur`, `focus`, `renderDayCell`.

## Next steps
- All reference files have been created and validated against the official Syncfusion API (see `references/api-reference.md`).
- Next: run the test-case guide and validation checks, then create automated examples or add platform-specific notes on request.
- Ask me to run tests, update `completion-status.json`, or produce publish-ready artifacts.
