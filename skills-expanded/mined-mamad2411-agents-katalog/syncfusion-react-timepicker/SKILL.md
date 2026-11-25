---
name: syncfusion-react-timepicker
description: Implement Syncfusion React TimePicker component for user time selection, scheduling interfaces, and appointment booking. Use this skill whenever users need to add time picker inputs for appointment systems, scheduling apps, time-based filtering, shift management, or time range selection. Covers installation, time format customization, min/max constraints, event handling, form integration, validation patterns, and mobile responsive behavior.
metadata:
  author: "Syncfusion Inc"
  category: "Calendars"
  version: "33.1.44"
---

# Implementing Syncfusion React TimePicker Component

The Syncfusion React TimePicker component provides a user-friendly way to select time values in applications. It supports multiple time formats, time range constraints, keyboard navigation, form integration, and mobile-optimized full-screen mode.

## Documentation Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation via npm (@syncfusion/ej2-react-calendars)
- CalendarModule setup in app.module.ts
- CSS imports and theme configuration
- Basic TimePicker implementation
- Component registration with useRef
- Running development server
- Common troubleshooting

### Time Format and Display
📄 **Read:** [references/time-format-and-display.md](references/time-format-and-display.md)
- Format string options (24-hour, 12-hour formats)
- TimeFormatObject with skeleton property
- Locale-based time formatting
- Placeholder text customization
- Float label types (Never, Always, Auto)
- htmlAttributes for DOM attributes
- Masked input with enableMask
- Mask placeholder configuration

### Time Range and Selection
📄 **Read:** [references/time-range-and-selection.md](references/time-range-and-selection.md)
- Minimum and maximum time constraints
- Time step intervals (15, 30, 60 minutes)
- ScrollTo default position
- Value binding and two-way updates
- Read-only and disabled states
- OpenOnFocus behavior
- Time popup list population
- Stepped time intervals

### Events and Methods
📄 **Read:** [references/events-and-methods.md](references/events-and-methods.md)
- Event handlers (change, open, close, blur, focus)
- Event argument structures
- Methods (show, hide, focusIn, focusOut)
- Imperative control with useRef
- Lifecycle events (created, destroyed)
- Event patterns and best practices
- Clearing values and state reset
- ItemRender for custom formatting

### Customization and Styling
📄 **Read:** [references/customization-and-styling.md](references/customization-and-styling.md)
- CSS class customization with cssClass
- Theme options (Material, Bootstrap, Fluent, Tailwind)
- Full-screen mode for mobile devices
- RTL (right-to-left) language support
- Strict mode validation
- Z-index management
- Width and height configuration
- Accessibility features
- Theme Studio integration

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete properties list (26 properties)
- All methods with signatures (5 methods)
- All events with event arguments (9 events)
- Type definitions and interfaces
- Default values and constraints
- Use cases for each property

### Advanced Patterns
📄 **Read:** [references/advanced-patterns.md](references/advanced-patterns.md)
- Form submission with validation
- Keyboard shortcuts and keyConfigs
- Server timezone offset handling
- Persistence and localStorage
- Multi-component integration
- Performance optimization
- Error handling patterns
- Complex validation scenarios

## Quick Start

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

## Common Patterns

### Pattern 1: Time Picker with Min/Max Constraints

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

### Pattern 2: Form with Time Picker Submission

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

### Pattern 3: Time Picker with Custom Format

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

### Pattern 4: Event Handling and State Management

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

### Pattern 5: Masked Time Input

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

## Key Props Reference

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

## Related Skills

- [Implementing Checkbox](../checkbox/implementing-checkbox/) - For multi-select time options
- [Implementing DatePicker](../calendars/implementing-calendar/) - For date and time selection
- [Implementing Range Slider](../range-slider/implementing-range-slider/) - For time range selection

---

**Next Steps:**
- Read [references/getting-started.md](references/getting-started.md) to install and set up your first TimePicker
- Explore [references/time-format-and-display.md](references/time-format-and-display.md) for format options
- Check [references/time-range-and-selection.md](references/time-range-and-selection.md) for time constraints
- See [references/advanced-patterns.md](references/advanced-patterns.md) for complex scenarios
