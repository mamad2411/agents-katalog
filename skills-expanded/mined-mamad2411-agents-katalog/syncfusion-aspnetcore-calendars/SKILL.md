---
name: syncfusion-aspnetcore-calendars
description: Comprehensive guide for implementing Syncfusion ASP.NET Core Calendar components including Calendar, DatePicker, DateRangePicker, DateTimePicker, and TimePicker. Use this skill ALWAYS and immediately when the user asks about any Syncfusion ASP.NET Core calendar, date picker, date range picker, time picker, datetime picker, calendar views, multi-selection, Islamic calendar, date range restriction, week numbers, day cell customization, renderDayCell, date selection, range selection, date formatting, date masking, globalization, localization, strict mode, accessibility, or any related calendar/date/time UI in ASP.NET Core tag helper applications.
metadata:
  author: "Syncfusion Inc"
  category: "Calendars"
  version: "33.1.44"
---

# Implementing Syncfusion ASP.NET Core Calendars

## TimePicker

The **TimePicker** is an intuitive input component that allows users to select a time value from a popup list or type it directly. It supports time ranges, strict mode, masking, globalization, RTL, accessibility, and rich customization options.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/timepicker-getting-started.md)
- NuGet package installation and setup
- Tag helper registration and script/style references
- Basic TimePicker rendering with `<ejs-timepicker>`
- Setting value, min, and max time
- Configuring time format and step interval
- TimePickerFor model binding

#### Time Range
📄 **Read:** [references/time-range.md](references/timepicker-range.md)
- Setting min and max time boundaries with `Min` and `Max`
- Behavior when value is out-of-range
- Two-TimePicker range selection (start/end time)
- Enabling/disabling end time based on start time selection
- Business hours selection pattern

#### Strict Mode
📄 **Read:** [references/strict-mode.md](references/timepicker-strict-mode.md)
- Enabling `StrictMode` to enforce valid time entry
- Clamping out-of-range values to min/max
- Default (non-strict) mode with error class indication
- Null behavior for invalid values in non-strict mode

#### Globalization
📄 **Read:** [references/globalization.md](references/timepicker-globalization.md)
- Setting culture with `Locale` property
- Loading CLDR data for non-English cultures
- L10n placeholder localization
- RTL support with `EnableRtl` for Arabic, Hebrew
- German and Arabic culture examples

#### Time Masking
📄 **Read:** [references/time-masking.md](references/timepicker-masking.md)
- Enabling masked input with `EnableMask`
- Mask pattern based on format string
- Custom mask placeholder with `MaskPlaceholder` (hour, minute, second)
- Keyboard navigation within masked segments

#### Style and Appearance
📄 **Read:** [references/style-appearance.md](references/timepicker-style-appearance.md)
- CSS customization using `CssClass` property
- Available CSS class targets (wrapper, icon, popup, list items)
- Customizing input, popup button, popup list, hover/active states
- Full-screen popup mode on mobile with `FullScreenMode`
- Wrapper height, font-size, background-color overrides

#### Accessibility
📄 **Read:** [references/accessibility.md](references/timepicker-accessibility.md)
- WCAG 2.2 AA compliance details
- WAI-ARIA attributes: aria-haspopup, aria-selected, aria-disabled, etc.
- Full keyboard interaction table
- Screen reader support
- RTL, color contrast, mobile device support

#### How-To Guides
📄 **Read:** [references/how-to.md](references/timepicker-how-to.md)
- Client-side form validation using FormValidator
- CSS customization with custom class names
- TimePickerFor rendering with model binding and form POST

#### API Reference
📄 **Read:** [references/api.md](references/timepicker-api.md)
- All properties with types, defaults, and descriptions
- All events (Change, Open, Close, Focus, Blur, Cleared, ItemRender, Created, Destroyed)
- CSS class reference table
- MaskPlaceholder sub-properties
- Complete tag helper attribute syntax

---

### Quick Start

**1. Install NuGet package:**
```
Install-Package Syncfusion.EJ2.AspNet.Core
```

**2. Register Tag Helper** in `~/Pages/_ViewImports.cshtml`:
```cshtml
@addTagHelper *, Syncfusion.EJ2
```

**3. Add CSS and script** in `~/Pages/Shared/_Layout.cshtml`:
```html
<link rel="stylesheet" href="https://cdn.syncfusion.com/ej2/fluent.css" />
<script src="https://cdn.syncfusion.com/ej2/dist/ej2.min.js"></script>
```

**4. Add Script Manager** at end of `<body>`:
```html
<ejs-scripts></ejs-scripts>
```

**5. Render the TimePicker:**
```cshtml
<ejs-timepicker id="timepicker"></ejs-timepicker>
```

---

### Common Patterns

#### TimePicker with Value, Min, and Max
```cshtml
@{
    var minVal = new DateTime(2022, 05, 07, 1, 00, 00);
    var maxVal = new DateTime(2022, 05, 07, 11, 00, 00);
    var value  = new DateTime(2022, 05, 07, 4, 00, 00);
}
<ejs-timepicker id="timepicker" value="value" min="minVal" max="maxVal"></ejs-timepicker>
```

#### Custom Format and Step
```cshtml
@{
    var value = new DateTime(2022, 05, 07, 4, 00, 00);
}
<ejs-timepicker id="timepicker" format="HH:mm" step="60" value="value"></ejs-timepicker>
```

#### Strict Mode
```cshtml
<ejs-timepicker id="timepicker"
    value="@ViewBag.value"
    min="@ViewBag.minVal"
    max="@ViewBag.maxVal"
    strictMode="true">
</ejs-timepicker>
```

#### Masked Input
```cshtml
<ejs-timepicker id="timepicker" enableMask="true"></ejs-timepicker>
```

#### RTL (Right-to-Left)
```cshtml
<ejs-timepicker id="timepicker" placeholder="Select a time" enableRtl="true"></ejs-timepicker>
```

## DatePicker

The **DatePicker** is a graphical user interface control that allows users to select or enter a date value from a calendar popup or by typing directly into the input field. It supports date range restriction, custom formats, masked input, globalization, strict mode, calendar view configuration, RTL, and accessibility.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/datepicker-getting-started.md](references/datepicker-getting-started.md)
- NuGet package installation and setup
- Tag helper registration and script/style references
- Basic `<ejs-datepicker>` rendering
- Setting `value`, `min`, and `max` dates
- `DatePickerFor` model binding and form POST

#### Date Range
📄 **Read:** [references/datepicker-date-range.md](references/datepicker-date-range.md)
- Setting `min` and `max` to restrict the selectable date range
- Out-of-range behavior in default vs. strict mode
- Error class indication for invalid/out-of-range dates
- Updating `min`/`max` from code-behind

#### Strict Mode
📄 **Read:** [references/datepicker-strict-mode.md](references/datepicker-strict-mode.md)
- `strictMode="true"`: clamps out-of-range input to `min`/`max`
- `strictMode="false"` (default): accepts input, applies error class
- Choosing the right mode for validation vs. display scenarios

#### Date Format
📄 **Read:** [references/datepicker-date-format.md](references/datepicker-date-format.md)
- `format` property for custom display format (e.g., `yyyy-MM-dd`)
- `inputFormats` for accepting multiple user-entry formats
- Common format token reference

#### Date Masking
📄 **Read:** [references/datepicker-date-masking.md](references/datepicker-date-masking.md)
- Enabling masked input with `enableMask`
- Mask pattern derived from `format`
- `maskPlaceholder` sub-property customization (day, month, year)
- Keyboard navigation within masked segments
- Localized mask placeholder for non-English cultures

#### Views and Calendar Configuration
📄 **Read:** [references/datepicker-view.md](references/datepicker-view.md)
- `start` property for initial calendar view (Month/Year/Decade)
- `depth` property to restrict navigation depth
- `dayHeaderFormat` for day header display (Short/Narrow/Abbreviated/Wide)
- `weekNumber` and `firstDayOfWeek` configuration

#### Globalization
📄 **Read:** [references/datepicker-globalization.md](references/datepicker-globalization.md)
- Setting culture with `locale` property
- Loading CLDR data for non-English cultures
- `L10n` localization for today button and placeholder text
- RTL support with `enableRtl` for Arabic, Hebrew
- German and Arabic culture examples

#### Style and Appearance
📄 **Read:** [references/datepicker-style-appearance.md](references/datepicker-style-appearance.md)
- `cssClass` for scoped style overrides
- CSS class reference table (wrapper, icon, popup, day cells)
- Customizing input wrapper, icon, and calendar popup
- `renderDayCell` event for per-cell customization
- `fullScreenMode` for mobile devices
- `floatLabelType` for floating label behavior

#### Accessibility
📄 **Read:** [references/datepicker-accessibility.md](references/datepicker-accessibility.md)
- WCAG 2.2 AA compliance
- WAI-ARIA attributes (`aria-expanded`, `aria-disabled`, `aria-activedescendant`)
- Full keyboard interaction tables (input and calendar popup)
- Screen reader support and RTL

#### How-To Guides
📄 **Read:** [references/datepicker-how-to.md](references/datepicker-how-to.md)
- Client-side validation with `FormValidator`
- `DatePickerFor` model binding and server-side form POST
- Set placeholder and readonly state
- Disable the DatePicker (`enabled="false"`)
- Open popup on input focus (`openOnFocus` or `show()` method)
- Prevent popup from closing (`preventDefault`)
- Customize day header format

#### API Reference
📄 **Read:** [references/datepicker-api.md](references/datepicker-api.md)
- All properties with types, defaults, and descriptions
- All events with descriptions and args
- `MaskPlaceholder` sub-properties
- CSS class reference table
- Complete tag helper attribute syntax

---

### Quick Start

**1. Install NuGet package:**
```
Install-Package Syncfusion.EJ2.AspNet.Core
```

**2. Register Tag Helper** in `~/Pages/_ViewImports.cshtml`:
```cshtml
@addTagHelper *, Syncfusion.EJ2
```

**3. Add CSS and script** in `~/Pages/Shared/_Layout.cshtml`:
```html
<link rel="stylesheet" href="https://cdn.syncfusion.com/ej2/fluent.css" />
<script src="https://cdn.syncfusion.com/ej2/dist/ej2.min.js"></script>
```

**4. Add Script Manager** at end of `<body>`:
```html
<ejs-scripts></ejs-scripts>
```

**5. Render the DatePicker:**
```cshtml
<ejs-datepicker id="datepicker" placeholder="Select a date"></ejs-datepicker>
```

---

### Common Patterns

#### DatePicker with Value, Min, and Max
```cshtml
@{
    var minDate = new DateTime(2025, 5, 5);
    var maxDate = new DateTime(2025, 5, 27);
    var value   = new DateTime(2025, 5, 15);
}
<ejs-datepicker id="datepicker"
    value="@value"
    min="@minDate"
    max="@maxDate"
    placeholder="Select a date">
</ejs-datepicker>
```

#### Custom Format
```cshtml
<ejs-datepicker id="datepicker"
    format="yyyy-MM-dd"
    placeholder="YYYY-MM-DD">
</ejs-datepicker>
```

#### Strict Mode
```cshtml
<ejs-datepicker id="datepicker"
    min="@ViewBag.MinDate"
    max="@ViewBag.MaxDate"
    strictMode="true">
</ejs-datepicker>
```

#### Masked Input
```cshtml
<ejs-datepicker id="datepicker" enableMask="true"></ejs-datepicker>
```

#### DatePickerFor (Model Binding)
```cshtml
@model AppModel
<ejs-datepickerfor id="date" for="@Model.Date" placeholder="Select a date">
</ejs-datepickerfor>
```

#### RTL (Right-to-Left)
```cshtml
<ejs-datepicker id="datepicker" locale="ar" enableRtl="true"></ejs-datepicker>
```

## DateTimePicker

The **DateTimePicker** is a graphical user interface control that allows users to select both a date and a time value from a combined popup (calendar + time list), or type directly into the input field. It supports date-time range restriction, custom formats, input format flexibility, masked input, globalization, strict mode, calendar view configuration, RTL, and accessibility.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/datetimepicker-getting-started.md](references/datetimepicker-getting-started.md)
- NuGet package installation and setup
- Tag helper registration and script/style references
- Basic `<ejs-datetimepicker>` rendering
- Setting `value`, `min`, and `max` date-time
- `DateTimePickerFor` model binding and form POST
- `openOnFocus`, `readonly`, and `showClearButton` options

#### Date and Time Range
📄 **Read:** [references/datetimepicker-date-time-range.md](references/datetimepicker-date-time-range.md)
- Setting `min` and `max` to restrict full date-time range
- Setting `minTime` and `maxTime` for per-day time restriction
- Out-of-range behavior in default vs. strict mode
- Priority rules when both min/max and minTime/maxTime are set
- Updating range values from code-behind

#### Strict Mode
📄 **Read:** [references/datetimepicker-strict-mode.md](references/datetimepicker-strict-mode.md)
- `strictMode="true"`: clamps out-of-range input to `min`/`max`
- `strictMode="false"` (default): accepts input, applies error class
- Choosing the right mode for validation vs. display scenarios

#### Date Time Format
📄 **Read:** [references/datetimepicker-date-time-format.md](references/datetimepicker-date-time-format.md)
- `format` property for custom display format (e.g., `yyyy-MM-dd hh:mm`)
- `timeFormat` for time popup list display
- `inputFormats` for accepting multiple user-entry formats
- Common format token reference

#### Date Time Masking
📄 **Read:** [references/datetimepicker-masking.md](references/datetimepicker-masking.md)
- Enabling masked input with `enableMask`
- Mask pattern derived from `format`
- `maskPlaceholder` sub-property customization (day, month, year, hour, minute, second)
- Keyboard navigation within masked segments
- Localized mask placeholder for non-English cultures

#### Globalization
📄 **Read:** [references/datetimepicker-globalization.md](references/datetimepicker-globalization.md)
- Setting culture with `locale` property
- Loading CLDR data for non-English cultures
- `L10n` localization for today button and placeholder text
- RTL support with `enableRtl` for Arabic, Hebrew
- German and Arabic culture examples

#### Style and Appearance
📄 **Read:** [references/datetimepicker-style-appearance.md](references/datetimepicker-style-appearance.md)
- `cssClass` for scoped style overrides
- CSS class reference table (wrapper, icons, time popup, calendar popup)
- Customizing input wrapper, date/time icons, and popups
- `renderDayCell` event for per-cell customization
- `fullScreenMode` for mobile devices
- `floatLabelType` for floating label behavior

#### Accessibility
📄 **Read:** [references/datetimepicker-accessibility.md](references/datetimepicker-accessibility.md)
- WCAG 2.2 AA compliance
- WAI-ARIA attributes (`aria-expanded`, `aria-disabled`, `aria-activedescendant`)
- Full keyboard interaction tables (input, calendar popup, and time popup)
- Screen reader support and RTL

#### How-To Guides
📄 **Read:** [references/datetimepicker-how-to.md](references/datetimepicker-how-to.md)
- `DateTimePickerFor` model binding and server-side form POST
- Disable the DateTimePicker (`enabled="false"`)
- Set placeholder and readonly state
- Customize day header format (`dayHeaderFormat`)
- Disable specific dates via `renderDayCell`
- Calendar view configuration (`start` / `depth`)
- Week number display and state persistence

#### API Reference
📄 **Read:** [references/datetimepicker-api.md](references/datetimepicker-api.md)
- All properties with types, defaults, and descriptions
- All events with descriptions
- `MaskPlaceholder` sub-properties
- CSS class reference table
- Enum values (CalendarView, DayHeaderFormats, CalendarType, FloatLabelType, WeekRule)
- Complete tag helper attribute syntax

---

### Quick Start

**1. Install NuGet package:**
```
Install-Package Syncfusion.EJ2.AspNet.Core
```

**2. Register Tag Helper** in `~/Pages/_ViewImports.cshtml`:
```cshtml
@addTagHelper *, Syncfusion.EJ2
```

**3. Add CSS and script** in `~/Pages/Shared/_Layout.cshtml`:
```html
<link rel="stylesheet" href="https://cdn.syncfusion.com/ej2/fluent.css" />
<script src="https://cdn.syncfusion.com/ej2/dist/ej2.min.js"></script>
```

**4. Add Script Manager** at end of `<body>`:
```html
<ejs-scripts></ejs-scripts>
```

**5. Render the DateTimePicker:**
```cshtml
<ejs-datetimepicker id="datetimepicker" placeholder="Select a date and time"></ejs-datetimepicker>
```

---

### Common Patterns

#### DateTimePicker with Value, Min, and Max
```cshtml
@{
    var minVal = new DateTime(2019, 5, 5, 2, 0, 0);
    var maxVal = new DateTime(2019, 5, 25, 2, 0, 0);
    var value  = new DateTime(2019, 5, 10, 10, 0, 0);
}
<ejs-datetimepicker id="datetimepicker"
    value="value"
    min="minVal"
    max="maxVal">
</ejs-datetimepicker>
```

#### Custom Format
```cshtml
<ejs-datetimepicker id="datetimepicker"
    format="yyyy-MM-dd HH:mm"
    placeholder="YYYY-MM-DD HH:mm">
</ejs-datetimepicker>
```

#### Strict Mode
```cshtml
<ejs-datetimepicker id="datetimepicker"
    min="@ViewBag.minVal"
    max="@ViewBag.maxVal"
    strictMode="true">
</ejs-datetimepicker>
```

#### Masked Input
```cshtml
<ejs-datetimepicker id="datetimepicker" enableMask="true"></ejs-datetimepicker>
```

#### DateTimePickerFor (Model Binding)
```cshtml
@model BookingModel
<ejs-datetimepicker id="datetimepicker" for="BookingDateTime"></ejs-datetimepicker>
```

#### RTL (Right-to-Left)
```cshtml
<ejs-datetimepicker id="datetimepicker" locale="ar" enableRtl="true"></ejs-datetimepicker>
```

---

## DateRangePicker

The **DateRangePicker** is a graphical user interface control that allows users to select a start and end date from a dual-calendar popup or by typing directly into the input field. It supports date range restriction, range span limits, custom formats, input format flexibility, presets, globalization, strict mode, day cell customization, RTL, and accessibility.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/daterangepicker-getting-started.md](references/daterangepicker-getting-started.md)
- NuGet package installation and setup
- Tag helper registration and script/style references
- Basic `<ejs-daterangepicker>` rendering
- Setting `startDate` and `endDate`
- `DateRangePickerFor` model binding and form POST

#### Range Restriction
📄 **Read:** [references/daterangepicker-range-restriction.md](references/daterangepicker-range-restriction.md)
- Setting `min` and `max` to restrict selectable dates
- Range span with `minDays` and `maxDays`
- `strictMode` behavior: clamping vs. error class
- Out-of-range behavior summary table

#### Date Format
📄 **Read:** [references/daterangepicker-date-format.md](references/daterangepicker-date-format.md)
- `format` property for custom display format
- `inputFormats` array for flexible user entry
- `separator` for custom delimiter between dates
- Common format token reference

#### Customization
📄 **Read:** [references/daterangepicker-customization.md](references/daterangepicker-customization.md)
- `renderDayCell` event for disabling/styling individual cells
- `firstDayOfWeek` configuration
- `dayHeaderFormat` (Short/Narrow/Abbreviated/Wide)
- Calendar view `start` and `depth`
- `weekNumber` and `weekRule` configuration
- Presets for quick range selection
- `openOnFocus`, `readonly`, `allowEdit`, `showClearButton`
- `enablePersistence` for state retention across reloads

#### Globalization
📄 **Read:** [references/daterangepicker-globalization.md](references/daterangepicker-globalization.md)
- `locale` property for culture setting
- Loading CLDR data for non-English cultures
- `L10n` localization (placeholder, startLabel, endLabel, applyText, cancelText, selectedDays, days, customRange)
- `enableRtl` for Arabic, Hebrew
- German and Arabic culture examples

#### Style and Appearance
📄 **Read:** [references/daterangepicker-style-appearance.md](references/daterangepicker-style-appearance.md)
- `cssClass` for scoped style overrides
- CSS customization for wrapper, icon, range header, calendar content
- Footer Apply/Cancel button customization
- `floatLabelType` for floating label behavior
- `fullScreenMode` for mobile devices
- Complete CSS class reference table

#### Accessibility
📄 **Read:** [references/daterangepicker-accessibility.md](references/daterangepicker-accessibility.md)
- WCAG 2.2 AA compliance
- WAI-ARIA attributes (`aria-expanded`, `aria-disabled`, `aria-activedescendant`)
- Input and calendar keyboard interaction tables
- Screen reader support and RTL

#### How-To Guides
📄 **Read:** [references/daterangepicker-how-to.md](references/daterangepicker-how-to.md)
- `DateRangePickerFor` model binding and server-side form POST
- Set placeholder text
- Disable the DateRangePicker (`enabled="false"`)
- Customize day header format
- CSS customization with `cssClass` and CSS class reference

#### API Reference
📄 **Read:** [references/daterangepicker-api.md](references/daterangepicker-api.md)
- All properties with types, defaults, and descriptions
- All events with descriptions
- Presets sub-properties (`label`, `start`, `end`)
- Enum values (CalendarView, DayHeaderFormats, FloatLabelType, WeekRule)
- CSS class reference table
- Complete tag helper attribute syntax

---

### Quick Start

**1. Install NuGet package:**
```
Install-Package Syncfusion.EJ2.AspNet.Core
```

**2. Register Tag Helper** in `~/Pages/_ViewImports.cshtml`:
```cshtml
@addTagHelper *, Syncfusion.EJ2
```

**3. Add CSS and script** in `~/Pages/Shared/_Layout.cshtml`:
```html
<link rel="stylesheet" href="https://cdn.syncfusion.com/ej2/fluent.css" />
<script src="https://cdn.syncfusion.com/ej2/dist/ej2.min.js"></script>
```

**4. Add Script Manager** at end of `<body>`:
```html
<ejs-scripts></ejs-scripts>
```

**5. Render the DateRangePicker:**
```cshtml
<ejs-daterangepicker id="daterangepicker" placeholder="Select a Range"></ejs-daterangepicker>
```

---

### Common Patterns

#### DateRangePicker with Start and End Date
```cshtml
@{
    var startDate = new DateTime(2022, 11, 09);
    var endDate   = new DateTime(2022, 11, 21);
}
<ejs-daterangepicker id="daterangepicker"
    startDate="startDate"
    endDate="endDate"
    placeholder="Select a Range">
</ejs-daterangepicker>
```

#### Min/Max Date Restriction
```cshtml
<ejs-daterangepicker id="daterangepicker"
    min="@ViewBag.minDate"
    max="@ViewBag.maxDate"
    placeholder="Enter a Range">
</ejs-daterangepicker>
```

#### Range Span Limits
```cshtml
<ejs-daterangepicker id="daterangepicker"
    minDays="5"
    maxDays="10"
    placeholder="Select 5–10 days">
</ejs-daterangepicker>
```

#### Strict Mode
```cshtml
<ejs-daterangepicker id="daterangepicker"
    strictMode="true"
    min="@ViewBag.minDate"
    max="@ViewBag.maxDate"
    startDate="@ViewBag.startDate"
    endDate="@ViewBag.endDate">
</ejs-daterangepicker>
```

#### Custom Format with Input Formats
```cshtml
<ejs-daterangepicker id="daterangepicker"
    format="dd/MMM/yy"
    inputFormats="@(new string[] { "dd/MM/yyyy", "yyyyMMdd" })"
    placeholder="DD/MMM/YY">
</ejs-daterangepicker>
```

#### DateRangePickerFor (Model Binding)
```cshtml
@model DateRangeModel
<form method="post">
    <ejs-daterangepicker id="daterangepickerFor" ejs-for="@Model.value">
    </ejs-daterangepicker>
    <ejs-button id="submitButton" content="Submit"></ejs-button>
</form>
```

#### RTL (Right-to-Left)
```cshtml
<ejs-daterangepicker id="daterangepicker" locale="ar" enableRtl="true"></ejs-daterangepicker>
```

## Calendar

The **Calendar** is a graphical user interface control that displays a Gregorian (or Islamic) calendar, allowing users to select a date by navigating month, year, and decade views. It supports date range restriction, multi-selection, view configuration, day cell customization, globalization, RTL, accessibility, and rich styling.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/calendar-getting-started.md](references/calendar-getting-started.md)
- NuGet package installation and setup
- Tag helper registration and script/style references
- Basic Calendar rendering with `<ejs-calendar>`
- Setting `value`, `min`, and `max` dates
- Common initialization patterns (disabled, persistence, cssClass)

#### Calendar Views
📄 **Read:** [references/calendar-views.md](references/calendar-views.md)
- Available views: Month, Year, Decade
- `start` property for initial view on render
- `depth` property to restrict navigation depth
- Year picker and decade picker patterns
- View navigation rules and constraints

#### Date Range
📄 **Read:** [references/calendar-date-range.md](references/calendar-date-range.md)
- Setting `min` and `max` to restrict selectable dates
- Out-of-range behavior and value clamping
- Dynamic min/max updates via JavaScript
- Future-only, past-only, and fixed range examples

#### Multi Selection
📄 **Read:** [references/calendar-multi-select.md](references/calendar-multi-select.md)
- Enabling multi-date selection with `isMultiSelection`
- Setting pre-selected dates with `values` array
- Selecting a full week using the `change` event
- Handling `args.values` in event handlers

#### Customization
📄 **Read:** [references/calendar-customization.md](references/calendar-customization.md)
- `renderDayCell` event to disable or style individual cells
- Disabling weekends
- Highlighting specific dates with custom CSS or tooltips
- Highlighting weekends
- `dayHeaderFormat`: Short, Narrow, Abbreviated, Wide
- `firstDayOfWeek` configuration
- `weekNumber` and `weekRule` properties
- CSS class reference table

#### Globalization
📄 **Read:** [references/calendar-globalization.md](references/calendar-globalization.md)
- Setting culture with `locale` property
- Loading CLDR data for non-English cultures
- `L10n` localization for Today button text
- RTL support with `enableRtl` (Arabic, Hebrew)
- Islamic Calendar mode with `calendarMode`

#### Style and Appearance
📄 **Read:** [references/calendar-style-appearance.md](references/calendar-style-appearance.md)
- `cssClass` for scoped appearance overrides
- Background, border, hover, title, and nav icon customization
- Today button and selected cell CSS
- Show dates of other months with CSS
- Complete CSS class reference

#### Accessibility
📄 **Read:** [references/calendar-accessibility.md](references/calendar-accessibility.md)
- WCAG 2.2 AA compliance details
- WAI-ARIA attributes: aria-label, aria-selected, aria-disabled, aria-activedescendant
- Full keyboard interaction table (all navigation keys)
- Screen reader support
- RTL and mobile device accessibility

#### How-To Guides
📄 **Read:** [references/calendar-how-to.md](references/calendar-how-to.md)
- Change the first day of the week (`firstDayOfWeek`)
- Customize day header format (`dayHeaderFormat`)
- Render week numbers (`weekNumber`)
- Select a sequence of dates (full week selection)
- Add a clear button to the Calendar footer (`created` event)
- Show dates of other months (CSS approach)
- Skip a month on navigation (`navigated` event + `navigateTo`)

#### API Reference
📄 **Read:** [references/calendar-api.md](references/calendar-api.md)
- All properties with types, defaults, and descriptions
- All events (Change, Created, Destroyed, Navigated, RenderDayCell)
- Enum reference (CalendarType, CalendarView, DayHeaderFormats, WeekRule)
- CSS class reference table
- Complete tag helper attribute syntax

---

### Quick Start

**1. Install NuGet package:**
```
Install-Package Syncfusion.EJ2.AspNet.Core
```

**2. Register Tag Helper** in `~/Pages/_ViewImports.cshtml`:
```cshtml
@addTagHelper *, Syncfusion.EJ2
```

**3. Add CSS and script** in `~/Pages/Shared/_Layout.cshtml`:
```html
<link rel="stylesheet" href="https://cdn.syncfusion.com/ej2/fluent.css" />
<script src="https://cdn.syncfusion.com/ej2/dist/ej2.min.js"></script>
```

**4. Add Script Manager** at end of `<body>`:
```html
<ejs-scripts></ejs-scripts>
```

**5. Render the Calendar:**
```cshtml
<ejs-calendar id="calendar"></ejs-calendar>
```

---

### Common Patterns

#### Calendar with Value, Min, and Max
```cshtml
@{
    var minDate   = new DateTime(DateTime.Now.Year, DateTime.Now.Month, 5);
    var maxDate   = new DateTime(DateTime.Now.Year, DateTime.Now.Month, 27);
    var todayDate = DateTime.Now;
}
<ejs-calendar id="calendar"
    value="todayDate"
    min="minDate"
    max="maxDate">
</ejs-calendar>
```

#### Year View (start in Year, drill down to Month)
```cshtml
<ejs-calendar id="calendar"
    start="Syncfusion.EJ2.Calendars.CalendarView.Year"
    depth="Syncfusion.EJ2.Calendars.CalendarView.Month">
</ejs-calendar>
```

#### Multi-Selection
```cshtml
<ejs-calendar id="calendar"
    isMultiSelection="true"
    values="@ViewBag.multiValues">
</ejs-calendar>
```

#### Disable Weekends
```cshtml
<ejs-calendar id="calendar" renderDayCell="disableWeekends"></ejs-calendar>
<script>
    function disableWeekends(args) {
        if (args.date.getDay() === 0 || args.date.getDay() === 6) {
            args.isDisabled = true;
        }
    }
</script>
```

#### Week Numbers with RTL
```cshtml
<ejs-calendar id="calendar"
    weekNumber="true"
    locale="ar"
    enableRtl="true">
</ejs-calendar>
```

#### Islamic Calendar
```cshtml
<ejs-calendar id="calendar"
    calendarMode="Syncfusion.EJ2.Calendars.CalendarType.Islamic">
</ejs-calendar>
```