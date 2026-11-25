---
name: syncfusion-javascript-inputs
description: Comprehensive guide for implementing Syncfusion TypeScript input components including ColorPicker, MaskedTextBox, OtpInput, Slider, TextArea, NumericTextBox, Rating, Signature, TextBox, uploader. Use this when adding color selection, masked formatting, OTP entry, range sliders, multiline text, numeric inputs, file upload, star ratings, signature capture, or text inputs to a TypeScript application.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Inputs"
---

# Syncfusion javascript inputs

# ColorPicker

The ColorPicker component is a user interface for selecting and adjusting color values. It supports HEX, RGB, and HSV color models, palette and picker modes, opacity control, inline rendering, custom preset palettes, and dual-mode switching.

---

### Documentation and Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/colorpicker-getting-started.md)
- Installation and package setup (`@syncfusion/ej2-inputs`)
- Required CSS imports and theme configuration
- Basic initialization with `<input type="color">`
- Picker mode vs. palette mode
- Inline rendering with `inline: true`
- Pre-setting a color value
- Lifecycle events: `created`

#### Modes and Display
📄 **Read:** [references/modes-display.md](references/colorpicker-modes-display.md)
- `mode: 'Picker'` — HSV gradient area, hue slider, opacity slider
- `mode: 'Palette'` — color grid tiles
- `modeSwitcher` — show/hide mode-toggle button
- `inline: true` — render embedded without popup
- `createPopupOnClick` — lazy popup creation
- `showButtons` — show/hide Apply/Cancel
- `showRecentColors` — recent color strip (palette mode only)

#### Palette Customization
📄 **Read:** [references/palette-customization.md](references/colorpicker-palette-customization.md)
- Default palette colors (100-color grid)
- `presetColors` — custom color groups with named sections
- `columns` — number of tiles per row
- `noColor` — no-color transparent tile
- `beforeTileRender` event — customize tile elements
- Custom palette groups (multiple named sections)

#### Color Value and Conversion
📄 **Read:** [references/color-value-conversion.md](references/colorpicker-color-value-conversion.md)
- `value` property — HEX8 format (`#rrggbbaa`)
- `getValue(value?, type?)` — convert between HEX, HEXA, RGB, RGBA, HSV, HSVA
- Reading color from `change` and `select` events (`currentValue.hex`, `currentValue.rgba`)
- Opacity handling with `enableOpacity`
- Setting programmatic color changes with `value` + `dataBind()`

#### Opacity and Accessibility
📄 **Read:** [references/opacity-accessibility.md](references/colorpicker-opacity-accessibility.md)
- `enableOpacity` — show/hide opacity slider and alpha channel
- `enableRtl` — right-to-left layout
- `disabled` — disable the component
- `enablePersistence` — persist selected value across reloads
- `cssClass` — custom CSS classes for styling
- Keyboard navigation in picker and palette modes
- `focusIn()` — programmatic focus

#### Events
📄 **Read:** [references/events.md](references/colorpicker-events.md)
- `change` — fires when color is applied (Apply button or immediate if `showButtons: false`)
- `select` — fires on color selection when `showButtons: true`
- `beforeOpen` / `open` — popup open lifecycle (cancel support)
- `beforeClose` — popup close lifecycle (cancel support)
- `beforeModeSwitch` / `onModeSwitch` — mode switch lifecycle
- `beforeTileRender` — palette tile customization
- `created` — component ready

#### API Reference
📄 **Read:** [references/api.md](references/colorpicker-api.md)
- All 14 properties with types and defaults
- All 11 methods with parameter tables
- All 9 events with argument interfaces
- Event argument interfaces: `ColorPickerEventArgs`, `PaletteTileEventArgs`, `BeforeOpenCloseEventArgs`, `OpenEventArgs`, `ModeSwitchEventArgs`

---

### Quick Start

#### Minimal Picker (Popup Mode)

```typescript
import { ColorPicker } from '@syncfusion/ej2-inputs';

const colorPicker: ColorPicker = new ColorPicker({
  value: '#008000ff',
  change: (args) => {
    console.log('Selected hex:', args.currentValue.hex);
    console.log('Selected rgba:', args.currentValue.rgba);
  }
});
colorPicker.appendTo('#color-picker');
```

```html
<input type="color" id="color-picker" />
```

#### Palette Mode (Inline)

```typescript
import { ColorPicker } from '@syncfusion/ej2-inputs';

const colorPicker: ColorPicker = new ColorPicker({
  mode: 'Palette',
  inline: true,
  showButtons: false,
  change: (args) => {
    document.getElementById('preview').style.backgroundColor = args.currentValue.rgba;
  }
});
colorPicker.appendTo('#color-picker');
```

---

### Common Patterns

| Goal | Property / Method |
|---|---|
| Set initial color | `value: '#ff5733ff'` |
| Palette grid layout | `mode: 'Palette'` |
| Embed in page | `inline: true` |
| Hide Apply/Cancel | `showButtons: false` |
| Custom color groups | `presetColors: { primary: [...], accent: [...] }` |
| Disable opacity | `enableOpacity: false` |
| Transparent option | `noColor: true` (palette mode only) |
| Show recent colors | `showRecentColors: true` (palette mode only) |
| Convert color format | `colorPicker.getValue(hex, 'rgba')` |
| Toggle popup | `colorPicker.toggle()` |
| Focus component | `colorPicker.focusIn()` |
| Apply changes | `colorPicker.value = '#ff0000'; colorPicker.dataBind()` |

## MaskedTextBox

The MaskedTextBox (`@syncfusion/ej2-inputs`) enforces structured input by applying a mask pattern that guides and validates user input character by character. Use it whenever you need to ensure input follows a specific format — phone numbers, dates, IP addresses, SSNs, zip codes, and more.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/maskedtextbox-getting-started.md)
- Installation and CSS imports
- Basic MaskedTextBox setup
- Setting the `mask` property
- Placeholder and float label
- Minimal working example

#### Mask Configuration
📄 **Read:** [references/mask-configuration.md](references/maskedtextbox-mask-configuration.md)
- Standard mask elements table (0, 9, #, L, ?, &, C, A, a, <, >, |, \\)
- Custom characters via `customCharacters`
- Regular expression masks
- Prompt character customization (`promptChar`)

#### Value Access and Programmatic Control
📄 **Read:** [references/value-access.md](references/maskedtextbox-value-access.md)
- `value` property (raw, unmasked)
- `getMaskedValue()` method (with mask format)
- Setting value programmatically
- Reading input in `change` event
- `focusIn()` / `focusOut()` methods

#### Customization and Appearance
📄 **Read:** [references/customization.md](references/maskedtextbox-customization.md)
- `cssClass` for custom styling
- `floatLabelType` (Never / Always / Auto)
- `enableRtl`, `enabled`, `readonly`
- `showClearButton`
- `htmlAttributes` for extra HTML attributes
- `width`, `placeholder`
- CSS overrides for wrapper and hover states

#### Adornments
📄 **Read:** [references/adornments.md](references/maskedtextbox-adornments.md)
- `prependTemplate` — inject HTML before the input (icons, labels, country codes)
- `appendTemplate` — inject HTML after the input (buttons, icons, unit suffixes)
- `e-input-separator` class for visual dividers
- Common adornment patterns table

#### Events and Interaction
📄 **Read:** [references/events.md](references/maskedtextbox-events.md)
- `change` event with `MaskChangeEventArgs`
- `focus` event with `MaskFocusEventArgs` (cursor positioning)
- `blur` event with `MaskBlurEventArgs`
- `created` and `destroyed` events
- Setting cursor position at start/end/custom position

#### Validation and How-To
📄 **Read:** [references/validation-how-to.md](references/maskedtextbox-validation-how-to.md)
- FormValidator integration with custom rules
- Numeric keypad on mobile (`htmlAttributes: { type: 'tel' }`)
- Checking for complete vs. partial input
- Accessibility (ARIA attributes, WCAG compliance)

#### API Reference
📄 **Read:** [references/api.md](references/maskedtextbox-api.md)
- All properties, methods, events, and interfaces
- Complete MaskedTextBox API surface

---

### Quick Start

```typescript
import { MaskedTextBox } from '@syncfusion/ej2-inputs';

// CSS in styles.css:
// @import '../node_modules/@syncfusion/ej2-base/styles/material.css';
// @import '../node_modules/@syncfusion/ej2-inputs/styles/material.css';

// HTML: <input id="mask" type="text" />

let mask: MaskedTextBox = new MaskedTextBox({
    mask: '000-000-0000',
    placeholder: 'Phone Number',
    floatLabelType: 'Always'
});
mask.appendTo('#mask');
```

---

### Common Patterns

| Scenario | Pattern |
|---|---|
| Phone number | `mask: '(999) 999-9999'` |
| US zip code | `mask: '00000'` or `mask: '00000-9999'` |
| Date | `mask: '00/00/0000'` |
| IP address | `mask: '[0-2][0-9][0-9].[0-2][0-9][0-9].[0-2][0-9][0-9].[0-2][0-9][0-9]'` |
| Credit card | `mask: '0000 0000 0000 0000'` |
| Time (AM/PM) | `mask: '00:00 >PM'` with `customCharacters: { P: 'P,A,p,a', M: 'M,m' }` |
| Letters only | `mask: 'LLLLLL'` |
| Alphanumeric | `mask: 'AAAAAA'` |
| Mixed case control | `mask: '>LLL<LLL'` (first 3 upper, next 3 lower) |

#### Read the raw value

```typescript
let mask: MaskedTextBox = new MaskedTextBox({
    mask: '(999) 999-9999',
    change: (args) => {
        console.log('Raw value:', args.value);           // digits only
        console.log('Masked value:', args.maskedValue);  // with mask chars
    }
});
mask.appendTo('#mask');

// Or programmatically:
const raw = mask.value;
const formatted = mask.getMaskedValue();
```

#### Floating label with pre-filled value

```typescript
let mask: MaskedTextBox = new MaskedTextBox({
    mask: '(999) 9999-999',
    value: '8674321756',
    placeholder: 'Mobile Number',
    floatLabelType: 'Auto'
});
mask.appendTo('#mask');
```
##  OTP Input

The OTP Input (`@syncfusion/ej2-inputs`) renders a set of individual input fields for one-time password entry. It supports configurable length, input types (number/text/password), styling modes, separators, placeholders, accessibility attributes, and full event handling. Use it for 2FA screens, OTP verification forms, and PIN entry flows.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/otp-input-getting-started.md)
- Installation and CSS imports
- Basic OTP Input initialization
- Setting and reading the `value` property
- `autoFocus` for auto-focusing on render
- Minimal working example

#### Input Types and Value
📄 **Read:** [references/input-types.md](references/otp-input-input-types.md)
- `type` — `number` (default), `text`, `password`
- `value` — pre-setting or reading the OTP value
- Choosing the right type for numeric vs alphanumeric OTPs

#### Appearance and Configuration
📄 **Read:** [references/appearance.md](references/otp-input-appearance.md)
- `length` — number of OTP input fields (default 4)
- `disabled` — disabling the entire control
- `cssClass` — custom and predefined classes (`e-success`, `e-warning`, `e-error`)
- `enableRtl` — right-to-left rendering

#### Styling Modes
📄 **Read:** [references/styling-modes.md](references/otp-input-styling-modes.md)
- `stylingMode` — `outlined` (default), `filled`, `underlined`
- When to use each mode

#### Placeholder
📄 **Read:** [references/placeholder.md](references/otp-input-placeholder.md)
- Single character placeholder (same for all fields)
- Multi-character placeholder (one character per field)

#### Separator
📄 **Read:** [references/separator.md](references/otp-input-separator.md)
- `separator` — character displayed between each input field
- Common separator patterns (`/`, `-`, `·`)

#### Events
📄 **Read:** [references/events.md](references/otp-input-events.md)
- `created` — fires after component is rendered
- `focus` / `blur` — focus in/out events (`OtpFocusEventArgs`)
- `input` — fires on each individual field change (`OtpInputEventArgs`)
- `valueChanged` — fires when all fields are filled and focus-out (`OtpChangedEventArgs`)

#### Accessibility
📄 **Read:** [references/accessibility.md](references/otp-input-accessibility.md)
- WCAG 2.2, Section 508, ARIA compliance
- `ariaLabels` — per-field ARIA label array
- `htmlAttributes` — custom HTML attributes
- Keyboard navigation (Arrow keys, Tab, Shift+Tab)

#### API Reference
📄 **Read:** [references/api.md](references/otp-input-api.md)
- All properties, methods, events, and interfaces
- Complete OTP Input API surface

---

### Quick Start

```typescript
import { OtpInput } from '@syncfusion/ej2-inputs';

// CSS in styles.css:
// @import '../node_modules/@syncfusion/ej2-base/styles/material.css';
// @import '../node_modules/@syncfusion/ej2-inputs/styles/material.css';

// HTML: <div id="otp_input"></div>

let otpInput: OtpInput = new OtpInput({
    length: 6,
    placeholder: 'x',
    stylingMode: 'outlined'
});
otpInput.appendTo('#otp_input');
```

---

### Common Patterns

| Scenario | Key Properties |
|---|---|
| 4-digit numeric OTP | `type: 'number'` (default) |
| 6-digit numeric OTP | `length: 6` |
| Alphanumeric code | `type: 'text'` |
| Hidden/password entry | `type: 'password'` |
| Dash separator | `separator: '-'` |
| Auto focus on load | `autoFocus: true` |
| Outlined style (default) | `stylingMode: 'outlined'` |
| Filled style | `stylingMode: 'filled'` |
| Underlined style | `stylingMode: 'underlined'` |
| Pre-filled value | `value: '1234'` |
| Disabled state | `disabled: true` |
| Success state styling | `cssClass: 'e-success'` |
| Error state styling | `cssClass: 'e-error'` |

#### Capture completed OTP value

```typescript
import { OtpInput, OtpChangedEventArgs } from '@syncfusion/ej2-inputs';

let otpInput: OtpInput = new OtpInput({
    length: 6,
    valueChanged: (args: OtpChangedEventArgs) => {
        console.log('Entered OTP:', args.value);
        // Trigger verification here
    }
});
otpInput.appendTo('#otp_input');
```

#### Password-masked OTP with separator

```typescript
import { OtpInput } from '@syncfusion/ej2-inputs';

let otpInput: OtpInput = new OtpInput({
    length: 6,
    type: 'password',
    separator: '-',
    stylingMode: 'outlined',
    autoFocus: true
});
otpInput.appendTo('#otp_input');
```

## Range Slider

The Range Slider (`@syncfusion/ej2-inputs`) allows users to select a single value or a range of values by dragging handles over a track. It supports three types (Default, MinRange, Range), ticks, tooltips, limits, orientation, formatting, accessibility, and form validation.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/range-slider-getting-started.md)
- Installation and dependencies (`@syncfusion/ej2-inputs`, `@syncfusion/ej2-base`, `@syncfusion/ej2-popups`, `@syncfusion/ej2-buttons`)
- CSS theme imports
- Basic Slider initialization and `appendTo`
- Setting `value`, `min`, `max`, `step`
- Orientation (horizontal/vertical)
- Show/hide buttons (`showButtons`)

#### Slider Types and Core Configuration
📄 **Read:** [references/types-and-configuration.md](references/range-slider-types-and-configuration.md)
- `type` — `Default`, `MinRange`, `Range`
- Single value vs range value (`value: 30` vs `value: [30, 70]`)
- `min`, `max`, `step` configuration
- `enabled`, `readonly`, `enableRtl`
- `enableAnimation`, `cssClass`, `width`
- Reversible slider (swap min/max values)

#### Ticks and Formatting
📄 **Read:** [references/ticks-and-format.md](references/range-slider-ticks-and-format.md)
- `ticks` object: `placement`, `largeStep`, `smallStep`, `showSmallTicks`, `format`
- Tick placement options: `Before`, `After`, `Both`, `None`
- Format API (Numeric N, Percentage P, Currency C, `#` specifiers)
- Custom formatting via `renderingTicks` and `tooltipChange` events
- Date/time formatting patterns
- Custom numeric value formatting

#### Tooltip
📄 **Read:** [references/tooltip-and-buttons.md](references/range-slider-tooltip-and-buttons.md)
- `tooltip` object: `isVisible`, `placement`, `showOn`, `format`, `cssClass`
- Tooltip placement: `Before`, `After`
- `showOn` values: `Auto`, `Always`, `Hover`, `Focus`, `Click`
- `showButtons` — increment/decrement buttons
- Localization with `L10n` for button labels

#### Limits
📄 **Read:** [references/limits.md](references/range-slider-limits.md)
- `limits` object: `enabled`, `minStart`, `minEnd`, `maxStart`, `maxEnd`, `startHandleFixed`, `endHandleFixed`
- Restricting handle movement range
- Locking handles in place
- Default/MinRange limits vs Range limits

#### Customization and Styling
📄 **Read:** [references/customization.md](references/range-slider-customization.md)
- CSS class overrides for track, handle, limits, ticks, buttons
- Dynamic color changes via `change` event
- Gradient/color-band styling
- Thumb shape customization (square, circle, oval, image)
- Custom tick labels via `renderedTicks` event

#### Advanced How-To
📄 **Read:** [references/advanced-how-to.md](references/range-slider-advanced-how-to.md)
- Date format slider (milliseconds-based)
- Time format slider
- Custom numeric formatting (Km, decimal, leading zeros)
- Reversible slider pattern
- Show slider from hidden state using `refresh()`
- Form validation with `FormValidator` and `changed` event

#### Accessibility
📄 **Read:** [references/accessibility.md](references/range-slider-accessibility.md)
- WCAG 2.2, Section 508 compliance
- WAI-ARIA attributes (`role=slider`, `aria-valuemin/max/now/text`, `aria-orientation`, `aria-label`)
- Keyboard navigation (Arrow keys, Home, End, Page Up/Down)

#### API Reference
📄 **Read:** [references/api.md](references/range-slider-api.md)
- All properties, methods, events, and sub-model interfaces
- `TicksDataModel`, `TooltipDataModel`, `LimitDataModel`
- Event argument types

---

### Quick Start

```typescript
import { Slider } from '@syncfusion/ej2-inputs';

// CSS in styles.css:
// @import '../node_modules/@syncfusion/ej2-base/styles/material.css';
// @import '../node_modules/@syncfusion/ej2-inputs/styles/material.css';
// @import '../node_modules/@syncfusion/ej2-popups/styles/material.css';
// @import '../node_modules/@syncfusion/ej2-buttons/styles/material.css';

// HTML: <div id="slider"></div>

let slider: Slider = new Slider({
    value: 30,
    min: 0,
    max: 100,
    step: 1
});
slider.appendTo('#slider');
```

---

### Common Patterns

| Scenario | Key Configuration |
|---|---|
| Single value slider | `type: 'Default'` (default), `value: 30` |
| Min-range shadow | `type: 'MinRange'`, `value: 30` |
| Range with two handles | `type: 'Range'`, `value: [30, 70]` |
| Vertical orientation | `orientation: 'Vertical'` |
| Show ticks | `ticks: { placement: 'After', largeStep: 20 }` |
| Show tooltip always | `tooltip: { isVisible: true, showOn: 'Always' }` |
| Increment/decrement buttons | `showButtons: true` |
| Restrict handle movement | `limits: { enabled: true, minStart: 10, minEnd: 40 }` |
| Currency format tooltip | `tooltip: { isVisible: true, format: 'C2' }` |
| Percentage format | `ticks: { format: 'P0' }` |
| Reversible (descending) | `min: 100, max: 0` |
| RTL layout | `enableRtl: true` |
| Disabled slider | `enabled: false` |
| Read-only slider | `readonly: true` |

#### Range Slider with Ticks and Tooltip

```typescript
import { Slider } from '@syncfusion/ej2-inputs';

let rangeSlider: Slider = new Slider({
    type: 'Range',
    value: [20, 80],
    min: 0,
    max: 100,
    step: 5,
    ticks: { placement: 'After', largeStep: 20, smallStep: 5, showSmallTicks: true },
    tooltip: { isVisible: true, placement: 'Before', showOn: 'Always' }
});
rangeSlider.appendTo('#range-slider');
```

#### Listen to value changes

```typescript
import { Slider, SliderChangeEventArgs } from '@syncfusion/ej2-inputs';

let slider: Slider = new Slider({
    value: 30,
    changed: (args: SliderChangeEventArgs) => {
        console.log('Final value:', args.value);
    },
    change: (args: SliderChangeEventArgs) => {
        console.log('While dragging:', args.value);
    }
});
slider.appendTo('#slider');
```
## TextArea

The TextArea (`@syncfusion/ej2-inputs`) provides a rich multiline text input with built-in support for floating labels, resize modes, adornments, max length enforcement, form integration, and full event handling. Use it whenever you need multiline user input — comment boxes, feedback forms, description fields, and more.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/textarea-getting-started.md)
- Installation and package dependencies
- CSS imports and theme setup
- Basic TextArea initialization
- Setting and getting values (`value` property)
- Reading value from `change` event
- Minimal working example

#### Floating Label and Localization
📄 **Read:** [references/floating-label.md](references/textarea-floating-label.md)
- `floatLabelType` — `Never`, `Always`, `Auto` behavior
- `placeholder` property usage
- Localization with `locale` property
- Loading translations with `L10n`

#### Resize and Dimensions
📄 **Read:** [references/resize.md](references/textarea-resize.md)
- `resizeMode` — `Vertical`, `Horizontal`, `Both`, `None`
- `width` property for explicit width control
- `rows` and `cols` properties for visible dimensions

#### Styles and Appearance
📄 **Read:** [references/styles-appearance.md](references/textarea-styles-appearance.md)
- Sizing classes: `e-small`, `e-bigger`
- Filled (`e-filled`) and Outline (`e-outline`) modes
- `cssClass` for custom styling
- `enabled` (disabled state) and `readonly` properties
- `showClearButton` and `e-static-clear` class
- Rounded corners, background/text color customization
- Floating label color (success/warning states)
- Mandatory asterisk on placeholder

#### Adornments
📄 **Read:** [references/adornments.md](references/textarea-adornments.md)
- `prependTemplate` — HTML before the textarea (icons, buttons)
- `appendTemplate` — HTML after the textarea (action buttons)
- `adornmentFlow` — `Horizontal` or `Vertical` layout
- `adornmentOrientation` — how items inside adornments are arranged
- `AdornmentsDirection` type usage

#### Max Length
📄 **Read:** [references/max-length.md](references/textarea-max-length.md)
- `maxLength` property for character limit enforcement
- User feedback on limit reached

#### Events
📄 **Read:** [references/events.md](references/textarea-events.md)
- `created`, `destroyed` events
- `input` event — fires on every keystroke (`InputEventArgs`)
- `change` event — fires on focus-out with changed value (`ChangedEventArgs`)
- `focus` event — fires on focus-in (`FocusInEventArgs`)
- `blur` event — fires on focus-out (`FocusOutEventArgs`)

#### Methods
📄 **Read:** [references/methods.md](references/textarea-methods.md)
- `focusIn()` — programmatically set focus
- `focusOut()` — programmatically remove focus
- `getPersistData()` — retrieve persisted state properties
- `addAttributes()` / `removeAttributes()` — dynamic HTML attributes
- `dataBind()` — apply pending property changes immediately
- `refresh()` — re-render the component
- `destroy()` — remove component from DOM

#### Form Support
📄 **Read:** [references/form-support.md](references/textarea-form-support.md)
- HTML form integration
- `FormValidator` integration with validation rules
- Required, minLength, maxLength rules
- Custom placement of error messages

#### API Reference
📄 **Read:** [references/api.md](references/textarea-api.md)
- All properties, methods, events, and interfaces
- Complete TextArea API surface

---

### Quick Start

```typescript
import { TextArea } from '@syncfusion/ej2-inputs';

// CSS in styles.css:
// @import '../node_modules/@syncfusion/ej2-base/styles/material.css';
// @import '../node_modules/@syncfusion/ej2-inputs/styles/material.css';

// HTML: <textarea id="default"></textarea>

let textareaObj: TextArea = new TextArea({
    placeholder: 'Enter your comments',
    floatLabelType: 'Auto',
    resizeMode: 'Vertical'
});
textareaObj.appendTo('#default');
```

---

### Common Patterns

| Scenario | Key Properties |
|---|---|
| Auto-floating label | `floatLabelType: 'Auto'` |
| Max 200 chars | `maxLength: 200` |
| Vertical resize only | `resizeMode: 'Vertical'` |
| Outline style (Material) | `cssClass: 'e-outline'` |
| Filled style (Material) | `cssClass: 'e-filled'` |
| Read-only content | `readonly: true` |
| Disabled state | `enabled: false` |
| Always show clear button | `showClearButton: true, cssClass: 'e-static-clear'` |
| Pre-set value | `value: 'Initial text'` |
| Custom dimensions | `rows: 5, cols: 40` |
| RTL layout | `enableRtl: true` |

#### Read value on change

```typescript
import { TextArea, ChangedEventArgs } from '@syncfusion/ej2-inputs';

let textareaObj: TextArea = new TextArea({
    placeholder: 'Enter your comments',
    floatLabelType: 'Auto',
    change: (args: ChangedEventArgs) => {
        console.log('Value:', args.value);
    }
});
textareaObj.appendTo('#default');
```

#### Outline TextArea with floating label and max length

```typescript
import { TextArea } from '@syncfusion/ej2-inputs';

let textareaObj: TextArea = new TextArea({
    placeholder: 'Feedback',
    floatLabelType: 'Auto',
    cssClass: 'e-outline',
    maxLength: 500,
    resizeMode: 'Vertical',
    rows: 4
});
textareaObj.appendTo('#default');
```
## NumericTextBox

The Syncfusion EJ2 TypeScript NumericTextBox (`@syncfusion/ej2-inputs`) is a feature-rich numeric input control that supports range validation, number formatting (standard and custom), decimal precision, spin buttons, adornments, localization, RTL, and full WCAG 2.2 accessibility.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/numerictextbox-getting-started.md)
- Installation and package dependencies
- Project setup (webpack quickstart)
- CSS theme imports
- Basic NumericTextBox initialization
- Range validation with `min`, `max`, `step`
- Formatting with `format`
- Decimal precision with `decimals` and `validateDecimalOnType`

#### Formats
📄 **Read:** [references/formats.md](references/numerictextbox-formats.md)
- Standard formats: `n`, `p` (percentage), `c` (currency)
- Custom format strings using `#` and `0` specifiers
- Combining format with `min`, `max` for percentage inputs
- Currency format with `currency` property

#### Adornments (Prefix/Suffix Templates)
📄 **Read:** [references/adornments.md](references/numerictextbox-adornments.md)
- `prependTemplate` – add elements before the input (currency symbols, icons)
- `appendTemplate` – add elements after the input (units, action buttons)
- Linking two NumericTextBox instances via `change` event
- Custom action icons with click event handlers

#### Globalization & Localization
📄 **Read:** [references/globalization.md](references/numerictextbox-globalization.md)
- `locale` property for culture-specific formatting
- `L10n.load()` to override spin button tooltip text
- CLDR data setup for non-English cultures
- RTL support with `enableRtl`
- Currency formatting with `currency` and `format: 'c2'`

#### Style & Appearance
📄 **Read:** [references/style-appearance.md](references/numerictextbox-style-appearance.md)
- Customizing wrapper element height and font size
- Customizing spin button icons CSS
- Applying custom `cssClass` for UI appearance changes
- Overriding `e-spin-up` and `e-spin-down` icon glyphs

#### How-To Recipes
📄 **Read:** [references/how-to.md](references/numerictextbox-how-to.md)
- Customize spin button up/down arrow icons
- Customize step value and hide spin buttons
- Customize UI appearance with `cssClass`
- Maintain trailing zeros while focused
- Perform custom validation using FormValidator
- Prevent nullable input (default to 0 instead of null)

#### Accessibility
📄 **Read:** [references/accessibility.md](references/numerictextbox-accessibility.md)
- WAI-ARIA roles and attributes (`spinbutton` role)
- Keyboard interaction (Arrow Up/Down)
- WCAG 2.2, Section 508 compliance
- Screen reader support details

#### API Reference
📄 **Read:** [references/api.md](references/numerictextbox-api.md)
- All properties with types and defaults
- All methods (`increment`, `decrement`, `getText`, `focusIn`, `focusOut`, `dataBind`, etc.)
- All events (`change`, `blur`, `focus`, `created`, `destroyed`)
- Event argument types (`ChangeEventArgs`, `NumericBlurEventArgs`, `NumericFocusEventArgs`)

---

### Quick Start

```bash
npm install @syncfusion/ej2-inputs
```

```html
<!-- index.html -->
<input id="numeric" type="text" />
```

```ts
import { NumericTextBox } from '@syncfusion/ej2-inputs';

let numeric: NumericTextBox = new NumericTextBox({
  value: 10,
  min: 0,
  max: 100,
  step: 1,
  format: 'n2',
  placeholder: 'Enter a number',
  floatLabelType: 'Auto'
});

numeric.appendTo('#numeric');
```

```css
/* styles.css – import one theme */
@import '../../node_modules/@syncfusion/ej2-base/styles/material.css';
@import '../../node_modules/@syncfusion/ej2-inputs/styles/material.css';
```

---

### Common Patterns

#### Currency Input
```ts
let currency: NumericTextBox = new NumericTextBox({
  format: 'c2',
  value: 100,
  placeholder: 'Price',
  floatLabelType: 'Auto'
});
currency.appendTo('#currency');
```

#### Percentage Input
```ts
let percent: NumericTextBox = new NumericTextBox({
  format: 'p2',
  value: 0.5,
  min: 0,
  max: 1,
  step: 0.01,
  placeholder: 'Percentage',
  floatLabelType: 'Auto'
});
percent.appendTo('#percent');
```

#### Hidden Spin Buttons with Custom Step
```ts
let numeric: NumericTextBox = new NumericTextBox({
  step: 5,
  showSpinButton: false,
  min: 0,
  max: 100,
  value: 20
});
numeric.appendTo('#numeric');
```

#### Read-Only NumericTextBox
```ts
let numeric: NumericTextBox = new NumericTextBox({
  value: 42,
  readonly: true
});
numeric.appendTo('#numeric');
```

#### Programmatic Increment / Decrement
```ts
numeric.increment(5);   // increase value by 5
numeric.decrement(2);   // decrease value by 2
```

#### Disable the Component
```ts
let numeric: NumericTextBox = new NumericTextBox({
  value: 10,
  enabled: false
});
numeric.appendTo('#numeric');
```

#### Clear Button
```ts
let numeric: NumericTextBox = new NumericTextBox({
  value: 10,
  showClearButton: true
});
numeric.appendTo('#numeric');
```

#### Mouse Wheel Disabled
```ts
let numeric: NumericTextBox = new NumericTextBox({
  value: 10,
  allowMouseWheel: false
});
numeric.appendTo('#numeric');
```

---

### Key Props at a Glance

| Property | Type | Default | Purpose |
|---|---|---|---|
| `value` | number | null | Current numeric value |
| `min` | number | null | Minimum allowed value |
| `max` | number | null | Maximum allowed value |
| `step` | number | 1 | Increment/decrement step |
| `format` | string | 'n2' | Display format when unfocused |
| `decimals` | number | null | Decimal precision when focused |
| `validateDecimalOnType` | boolean | false | Restrict decimals while typing |
| `strictMode` | boolean | true | Clamp value to min/max on blur |
| `floatLabelType` | FloatLabelType | 'Never' | Label float behavior |
| `placeholder` | string | null | Hint text / float label |
| `showSpinButton` | boolean | true | Show/hide spin buttons |
| `showClearButton` | boolean | false | Show clear (×) icon |
| `readonly` | boolean | false | Read-only mode |
| `enabled` | boolean | true | Enable/disable control |
| `enableRtl` | boolean | false | Right-to-left layout |
| `locale` | string | '' | Culture code |
| `currency` | string | null | ISO 4217 currency code |
| `cssClass` | string | null | Custom CSS class |
| `width` | number\|string | null | Component width |
| `allowMouseWheel` | boolean | true | Enable mouse wheel change |
| `enablePersistence` | boolean | false | Persist value across reloads |
| `prependTemplate` | string\|Function | null | HTML before input |
| `appendTemplate` | string\|Function | null | HTML after input |
| `htmlAttributes` | object | {} | Extra HTML attributes |

## Rating

The Rating component (`@syncfusion/ej2-inputs`) lets users select a value on a numeric scale by clicking or tapping symbols (stars by default). It supports precision ratings, custom templates, labels, tooltips, and full accessibility compliance.

### Dependencies

```
@syncfusion/ej2-inputs
  └── @syncfusion/ej2-base
  └── @syncfusion/ej2-popups
```

### Quick Start

```ts
import { Rating } from '@syncfusion/ej2-inputs';

let rating: Rating = new Rating({ value: 3.0 });
rating.appendTo('#rating');
```

```css
@import "../../node_modules/@syncfusion/ej2-base/styles/material.css";
@import "../../node_modules/@syncfusion/ej2-inputs/styles/material.css";
@import "../../node_modules/@syncfusion/ej2-popups/styles/material.css";
```

```html
<input id="rating" />
```

---

### Documentation and Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/rating-getting-started.md)
- Installation and package setup
- CSS imports and theme configuration
- Basic Rating initialization
- Setting the `value` property
- Running the application

#### Selection and Value Control
📄 **Read:** [references/selection.md](references/rating-selection.md)
- Setting and reading the rating value
- Minimum value with `min` property
- Single-selection mode (`enableSingleSelection`)
- Show/hide reset button (`allowReset`)
- Programmatic reset via `reset()` method

#### Precision Modes
📄 **Read:** [references/precision-modes.md](references/rating-precision-modes.md)
- Full precision (whole numbers)
- Half precision (0.5 increments)
- Quarter precision (0.25 increments)
- Exact precision (0.1 increments)
- `PrecisionType` enum usage

#### Labels
📄 **Read:** [references/labels.md](references/rating-labels.md)
- Showing the current value as a label (`showLabel`)
- Label positions: Top, Bottom, Left, Right (`labelPosition`)
- Custom label template (`labelTemplate`)
- `LabelPosition` enum values

#### Tooltip
📄 **Read:** [references/tooltip.md](references/rating-tooltip.md)
- Enabling/disabling tooltip on hover (`showTooltip`)
- Custom tooltip template (`tooltipTemplate`)
- Tooltip appearance customization via `cssClass`

#### Templates (Custom Symbols)
📄 **Read:** [references/templates.md](references/rating-templates.md)
- `emptyTemplate` for unrated items
- `fullTemplate` for rated items
- Emoji icons as rating symbols
- SVG icons as rating symbols
- PNG images as rating symbols
- Template context: `value` and `index`

#### Appearance and Styling
📄 **Read:** [references/appearance.md](references/rating-appearance.md)
- Changing item count (`itemsCount`)
- Disabled state (`disabled`)
- Visibility control (`visible`)
- Read-only mode (`readOnly`)
- Custom CSS with `cssClass`
- Changing icon border color, fill color, item spacing
- Swapping the default icon using CSS

#### Events
📄 **Read:** [references/events.md](references/rating-events.md)
- `valueChanged` – fires when rating changes
- `beforeItemRender` – fires before each item renders
- `onItemHover` – fires on item hover
- `created` – fires after render completes
- Event argument types: `RatingChangedEventArgs`, `RatingItemEventArgs`, `RatingHoverEventArgs`

#### Accessibility
📄 **Read:** [references/accessibility.md](references/rating-accessibility.md)
- WAI-ARIA attributes (`role=slider`, `aria-valuenow`, etc.)
- Keyboard navigation shortcuts
- WCAG 2.2 / Section 508 compliance
- RTL support

#### API Reference
📄 **Read:** [references/api.md](references/rating-api.md)
- All 16 properties with types and defaults
- All 7 methods
- All 4 events and their argument types

---

### Common Patterns

#### Rating with reset button and label

```ts
import { Rating } from '@syncfusion/ej2-inputs';

let rating: Rating = new Rating({
  value: 3.0,
  allowReset: true,
  showLabel: true
});
rating.appendTo('#rating');
```

#### Half-precision rating with change handler

```ts
import { Rating, PrecisionType, RatingChangedEventArgs } from '@syncfusion/ej2-inputs';

let rating: Rating = new Rating({
  value: 2.5,
  precision: PrecisionType.Half,
  valueChanged: (args: RatingChangedEventArgs) => {
    console.log('New rating:', args.value);
  }
});
rating.appendTo('#rating');
```

#### Read-only display rating

```ts
import { Rating } from '@syncfusion/ej2-inputs';

let rating: Rating = new Rating({
  value: 4.0,
  readOnly: true,
  showLabel: true
});
rating.appendTo('#rating');
```

#### Custom item count with min value

```ts
import { Rating } from '@syncfusion/ej2-inputs';

let rating: Rating = new Rating({
  value: 3,
  itemsCount: 10,
  min: 1
});
rating.appendTo('#rating');
```
## Signature

The Syncfusion EJ2 TypeScript Signature (`@syncfusion/ej2-inputs`) is a canvas-based control that allows users to draw smooth signatures using variable-width bezier curve interpolation with mouse, touch, or stylus input. It supports text-drawing, stroke/background customization, save/load operations, undo/redo history, and full WCAG 2.2 accessibility.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/signature-getting-started.md)
- Package dependencies (`@syncfusion/ej2-inputs`, `@syncfusion/ej2-base`)
- Project setup with webpack quickstart
- CSS theme imports
- HTML canvas element setup
- Basic Signature initialization
- Default canvas dimensions (300 × 150)

#### Customization
📄 **Read:** [references/customization.md](references/signature-customization.md)
- Stroke width: `maxStrokeWidth`, `minStrokeWidth`, `velocity`
- Stroke color with `strokeColor` (hex, RGB, named colors)
- Background color with `backgroundColor`
- Background image with `backgroundImage`
- Saving with background using `saveWithBackground`

#### Open & Save
📄 **Read:** [references/open-save.md](references/signature-open-save.md)
- Load pre-drawn signatures via `load(url, width?, height?)` (Base64 or hosted URL)
- Save as image (PNG/JPEG/SVG) via `save(type?, fileName?)`
- Get Base64 string via `getSignature()`
- Save as Blob via `saveAsBlob()`
- Get Blob via `getBlob(url)`
- Control background inclusion with `saveWithBackground`

#### User Interaction
📄 **Read:** [references/user-interaction.md](references/signature-user-interaction.md)
- Undo via `undo()` and guard with `canUndo()`
- Redo via `redo()` and guard with `canRedo()`
- Clear canvas via `clear()`
- Check empty state via `isEmpty()`
- Disable component with `disabled` property
- Read-only mode with `isReadOnly` property
- `change` event for reacting to strokes, undo, redo, and clear
- `created` event on first render
- `beforeSave` event for keyboard save (Ctrl+S) customization

#### Toolbar Integration
📄 **Read:** [references/toolbar-integration.md](references/signature-toolbar-integration.md)
- Integrating Signature with EJ2 Toolbar component
- Wiring Undo/Redo/Clear/Save toolbar buttons
- Adding ColorPicker for stroke and background color
- Adding DropDownList for stroke width control
- Enabling/disabling toolbar items based on `canUndo`, `canRedo`, `isEmpty`
- Using `change` event to keep toolbar state in sync

#### Accessibility
📄 **Read:** [references/accessibility.md](references/signature-accessibility.md)
- WCAG 2.2 and Section 508 compliance
- Keyboard shortcuts (Ctrl+Z, Ctrl+Y, Ctrl+S, Delete)
- Screen reader support
- Mobile/touch device support

#### API Reference
📄 **Read:** [references/api.md](references/signature-api.md)
- All properties with types and defaults
- All methods (`draw`, `load`, `save`, `saveAsBlob`, `getSignature`, `getBlob`, `undo`, `redo`, `clear`, `canUndo`, `canRedo`, `isEmpty`, `refresh`, `destroy`)
- All events (`change`, `created`, `beforeSave`)
- Supporting types (`SignatureFileType`, `SignatureChangeEventArgs`, `SignatureBeforeSaveEventArgs`)

---

### Quick Start

```bash
npm install @syncfusion/ej2-inputs
```

```html
<!-- index.html -->
<canvas id="signature"></canvas>
```

```ts
import { Signature } from '@syncfusion/ej2-inputs';

let signature: Signature = new Signature({}, '#signature');
```

```css
/* styles.css */
@import '../../node_modules/@syncfusion/ej2-base/styles/material.css';
@import '../../node_modules/@syncfusion/ej2-inputs/styles/material.css';
```

> The Signature component renders with the default HTML canvas size (300 × 150) when no explicit `width` or `height` is set on the canvas element.

---

### Common Patterns

#### Draw Text as Signature
```ts
// Draw "John Doe" in Arial, size 30
signature.draw('John Doe', 'Arial', 30);
```

#### Save Signature as PNG
```ts
signature.save('Png', 'my-signature');
```

#### Get Base64 and Reload
```ts
const base64 = signature.getSignature();       // returns base64 PNG string
signature.load(base64);                         // reload the same signature
```

#### Undo / Redo with Guards
```ts
if (signature.canUndo()) { signature.undo(); }
if (signature.canRedo()) { signature.redo(); }
```

#### Disable and Read-Only
```ts
signature.disabled   = true;   // user cannot draw; opacity shows disabled state
signature.isReadOnly = true;   // focusable but drawing is prevented
```

#### React to Signature Changes
```ts
let signature: Signature = new Signature({
  change: (args) => {
    console.log('Signature changed; empty?', signature.isEmpty());
  }
}, '#signature');
```
## TextBox

The Syncfusion EJ2 TypeScript TextBox (`@syncfusion/ej2-inputs`) is a feature-rich text input component that supports floating labels, multiline (textarea) mode, icon groups, adornments, validation states, sizing, RTL, autocomplete, and full WCAG 2.2 accessibility.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/textbox-getting-started.md)
- Installation and package dependencies
- Project setup (webpack quickstart)
- CSS theme imports
- Basic TextBox initialization
- Adding icons with `addIcon()`
- Floating label with `floatLabelType`

#### Multiline (Textarea) Mode
📄 **Read:** [references/multiline.md](references/textbox-multiline.md)
- Enable multiline with `multiline: true`
- Floating label on multiline inputs
- Auto-resize based on content
- Disable resize via CSS
- Limit text length with `addAttributes({ maxlength })`
- Character count in `input` event

#### Groups, Icons & Clear Button
📄 **Read:** [references/groups.md](references/textbox-groups.md)
- Adding icons with `addIcon('append' | 'prepend', iconClass)`
- Icon with floating label
- `showClearButton` to show a clear (×) icon
- Floating label without `required` attribute
- Multi-line input with floating label

#### Adornments (Prefix/Suffix Templates)
📄 **Read:** [references/adornments.md](references/textbox-adornments.md)
- `prependTemplate` – add icons or text before input
- `appendTemplate` – add icons or buttons after input
- Password visibility toggle pattern
- Delete/clear icon pattern with `dataBind()`

#### Validation States
📄 **Read:** [references/validation.md](references/textbox-validation.md)
- Apply `e-warning`, `e-error`, `e-success` via `cssClass`
- Change floating label color for validation states (CSS)
- Change TextBox color based on value (keyup + regex)

#### Sizing
📄 **Read:** [references/sizing.md](references/textbox-sizing.md)
- Normal size (default)
- Small size via `cssClass: 'e-small'`
- Bigger size via `cssClass: 'e-bigger'`
- Combining sizing with icons and float labels

#### Style & Appearance
📄 **Read:** [references/style-appearance.md](references/textbox-style-appearance.md)
- Filled mode: `cssClass: 'e-filled'`
- Outlined mode: `cssClass: 'e-outline'`
- Customize background color and text color (CSS override)
- Customize floating label color (CSS)
- Rounded corners with `cssClass: 'e-corner'`
- Scoping styles with `cssClass`

#### How-To Recipes
📄 **Read:** [references/how-to.md](references/textbox-how-to.md)
- Add TextBox programmatically using `Input.createInput()`
- Add floating label programmatically
- Add floating label to read-only TextBox
- Set disabled state (`enabled: false`)
- Set read-only state (`readonly: true`)
- Set rounded corner (`cssClass: 'e-corner'`)
- Change floating label color for validation states
- Change TextBox color based on value (keyup regex)
- Customize background and text color

#### Accessibility
📄 **Read:** [references/accessibility.md](references/textbox-accessibility.md)
- WAI-ARIA role `textbox` and attributes
- `aria-placeholder`, `aria-labelledby`
- WCAG 2.2, Section 508, screen reader support
- RTL support

#### API Reference
📄 **Read:** [references/api.md](references/textbox-api.md)
- All properties with types and defaults
- All methods (`addIcon`, `addAttributes`, `removeAttributes`, `focusIn`, `focusOut`, `dataBind`, etc.)
- All events (`change`, `input`, `blur`, `focus`, `created`, `destroyed`)
- Event argument types

---

### Quick Start

```bash
npm install @syncfusion/ej2-inputs
```

```html
<!-- index.html -->
<input id="firstName" />
```

```ts
import { TextBox } from '@syncfusion/ej2-inputs';

let textBox: TextBox = new TextBox({
  placeholder: 'Enter your name',
  floatLabelType: 'Auto'
});

textBox.appendTo('#firstName');
```

```css
/* styles.css */
@import '../../node_modules/@syncfusion/ej2-base/styles/material.css';
@import '../../node_modules/@syncfusion/ej2-inputs/styles/material.css';
```

---

### Common Patterns

#### Floating Label Types
```ts
// Auto – floats label above on focus or when value entered
let autoFloat: TextBox = new TextBox({ placeholder: 'Name', floatLabelType: 'Auto' });
autoFloat.appendTo('#auto');

// Always – label always floats above
let alwaysFloat: TextBox = new TextBox({ placeholder: 'Name', floatLabelType: 'Always' });
alwaysFloat.appendTo('#always');

// Never – label stays as placeholder (default)
let neverFloat: TextBox = new TextBox({ placeholder: 'Name', floatLabelType: 'Never' });
neverFloat.appendTo('#never');
```

#### TextBox with Icon
```ts
import { TextBox } from '@syncfusion/ej2-inputs';

let iconTextBox: TextBox = new TextBox({
  placeholder: 'Enter Date',
  created: () => {
    iconTextBox.addIcon('append', 'e-icons e-date-range');
  }
});
iconTextBox.appendTo('#textbox');
```

#### Multiline / Textarea
```ts
import { TextBox } from '@syncfusion/ej2-inputs';

let textarea: TextBox = new TextBox({
  placeholder: 'Enter your address',
  multiline: true,
  floatLabelType: 'Auto'
});
textarea.appendTo('#textarea');
```

#### Password Input with Visibility Toggle
```ts
import { TextBox } from '@syncfusion/ej2-inputs';

let passwordBox: TextBox = new TextBox({
  placeholder: 'Password',
  type: 'password',
  floatLabelType: 'Auto',
  appendTemplate: '<span class="e-input-separator"></span><span id="eye-icon" class="e-icons e-eye"></span>',
  created: () => {
    const eyeIcon = document.querySelector('#eye-icon') as HTMLElement;
    if (eyeIcon) {
      eyeIcon.addEventListener('click', () => {
        if (passwordBox.type === 'password') {
          passwordBox.type = 'text';
          eyeIcon.className = 'e-icons e-eye-slash';
        } else {
          passwordBox.type = 'password';
          eyeIcon.className = 'e-icons e-eye';
        }
        passwordBox.dataBind();
      });
    }
  }
});
passwordBox.appendTo('#password');
```

#### Validation States
```ts
import { TextBox } from '@syncfusion/ej2-inputs';

let errorBox: TextBox = new TextBox({ placeholder: 'Error state', cssClass: 'e-error' });
errorBox.appendTo('#error');

let warningBox: TextBox = new TextBox({ placeholder: 'Warning state', cssClass: 'e-warning' });
warningBox.appendTo('#warning');

let successBox: TextBox = new TextBox({ placeholder: 'Success state', cssClass: 'e-success' });
successBox.appendTo('#success');
```

#### Disabled and Read-Only
```ts
// Disabled
let disabled: TextBox = new TextBox({ placeholder: 'Disabled', enabled: false });
disabled.appendTo('#disabled');

// Read-only
let readOnly: TextBox = new TextBox({ placeholder: 'Read-only', readonly: true });
readOnly.appendTo('#readonly');
```

#### Clear Button
```ts
let clearable: TextBox = new TextBox({
  placeholder: 'Type to clear',
  showClearButton: true,
  floatLabelType: 'Auto'
});
clearable.appendTo('#clearable');
```

---

### Key Props at a Glance

| Property | Type | Default | Purpose |
|---|---|---|---|
| `value` | string | null | Text content |
| `placeholder` | string | null | Hint text / float label |
| `floatLabelType` | FloatLabelType | 'Never' | Label float behavior |
| `multiline` | boolean | false | Enable textarea mode |
| `type` | string | 'text' | Input type (text, password, email, etc.) |
| `enabled` | boolean | true | Enable/disable the control |
| `readonly` | boolean | false | Read-only mode |
| `showClearButton` | boolean | false | Show clear (×) icon |
| `cssClass` | string | '' | Custom CSS class(es) |
| `width` | number\|string | null | Component width |
| `enableRtl` | boolean | false | Right-to-left layout |
| `autocomplete` | string | 'on' | Browser autocomplete ('on'\|'off') |
| `locale` | string | '' | Culture/locale override |
| `enablePersistence` | boolean | false | Persist value across reloads |
| `prependTemplate` | string\|Function | null | HTML before input |
| `appendTemplate` | string\|Function | null | HTML after input |
| `htmlAttributes` | object | {} | Extra HTML attributes |

## Uploader

The Syncfusion Uploader component provides a robust, feature-rich file upload solution for TypeScript applications. It supports multiple upload modes, file validation, drag-and-drop, chunked uploads for large files, and extensive customization options.

### Component Overview

The Uploader component offers:
- **Multiple upload modes**: Async, chunked, and form-based uploads
- **Comprehensive validation**: File type, size, and count restrictions
- **Rich UI**: Customizable templates, themes, and styling options
- **Advanced features**: JWT authentication, localization, image preview/resize, progress tracking
- **Developer-friendly**: Full TypeScript support with type definitions, events, and methods

### Documentation Navigation Guide

#### Getting Started
📄 **Read:** [references/uploader-getting-started.md](references/uploader-getting-started.md)
- Dependencies and package requirements
- Installation via quickstart project, npm, or CDN
- TypeScript module imports
- Basic component initialization
- HTML structure and CSS imports
- Drop area configuration
- Async settings configuration
- Success and failure event handling
- Your first upload example
- Key configuration options

#### File Validation
📄 **Read:** [references/uploader-file-validation.md](references/uploader-file-validation.md)
- File type validation with allowedExtensions
- File size restrictions (minFileSize, maxFileSize)
- Maximum files count limiting with isModified flag
- Duplicate file validation
- Pre-upload validation strategies
- Custom validation logic
- Validation event handling

#### Upload Modes & Features
📄 **Read:** [references/uploader-upload-modes.md](references/uploader-upload-modes.md)
- Async upload configuration (single/multiple/sequential)
- Preloaded files with `files` property
- Save/Remove action with server-side examples
- Adding custom HTTP headers to upload requests
- Chunked upload with retryCount and retryAfterDelay
- Drag-and-drop with `dropArea` property
- Paste-to-upload from clipboard
- Directory upload with `directoryUpload` property
- Form submission with file upload
- File source options and events
- Event handling and callbacks (pause/resume/cancel)

#### Customization & Styling
📄 **Read:** [references/uploader-customization-and-styling.md](references/uploader-customization-and-styling.md)
- Component-specific CSS selectors (wrapper, browse button, drop text, file container)
- CSS customization and themes
- Button template customization
- Progress bar styling
- Appearance modifications
- RTL (Right-to-Left) support
- Responsive design patterns

#### Advanced Features
📄 **Read:** [references/uploader-advanced-features.md](references/uploader-advanced-features.md)
- JWT authentication (uploading + removing events with currentRequest)
- Server-side JWT validation (ASP.NET Core example)
- Localization with full key reference table
- File preview functionality
- Image resizing before upload
- File list template and custom template (showFileList)
- Form data binding
- File removal and cleanup handlers

#### How-To Guides & Patterns
📄 **Read:** [references/uploader-how-to-guides.md](references/uploader-how-to-guides.md)
- Programmatic upload triggers
- Invisible/hidden uploader UI
- Additional data with uploads
- Confirmation dialogs for removal
- Custom button elements
- MIME type validation
- Convert images to binary format
- File size check using `bytesToSize` method
- Hide drop areas
- Open/edit uploaded files
- Sort selected files
- External button triggers
- Image validation on drop
- WAI-ARIA accessibility compliance and keyboard shortcuts

#### Troubleshooting & Patterns
📄 **Read:** [references/uploader-troubleshooting-and-examples.md](references/uploader-troubleshooting-and-examples.md)
- Common issues and solutions (including name attribute mismatch)
- Browser compatibility notes
- Performance optimization techniques
- Edge cases and gotchas
- Form support pattern (non-async uploads with FormValidator)
- Real-world implementation patterns
- Debugging tips and techniques

#### API Reference
📄 **Read:** [references/uploader-api.md](references/uploader-api.md)
- Complete properties reference with types, descriptions, and defaults
- All public methods with parameter tables and return types
- All events with event argument details and usage examples
- Supporting interfaces: `AsyncSettingsModel`, `ButtonsPropsModel`, `FilesPropModel`, `FileInfo`, `ValidationMessages`
- Event argument interfaces: `SelectedEventArgs`, `UploadingEventArgs`, `RemovingEventArgs`, `BeforeRemoveEventArgs`, `BeforeUploadEventArgs`, `ActionCompleteEventArgs`, `CancelEventArgs`, `ClearingEventArgs`, `FileListRenderingEventArgs`, `PauseResumeEventArgs`
- `DropEffect` enum values
- Deprecated APIs noted with recommended replacements

---

### Quick Start Example

Here's a minimal TypeScript example to get started:

```typescript
import { Uploader } from '@syncfusion/ej2-inputs';

// Initialize Uploader component
const uploaderObj = new Uploader({
  asyncSettings: {
    saveUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Remove'
  },
  allowedExtensions: '.jpg,.png,.pdf'
});

// Render to DOM element with id 'fileupload'
uploaderObj.appendTo('#fileupload');

// Handle file selection
uploaderObj.selected = (args: any) => {
  console.log('Files selected:', args.filesData);
};

// Handle upload completion
uploaderObj.success = (args: any) => {
  console.log('Upload successful:', args.responseText);
};
```

HTML element:
```html
<input type="file" id="fileupload" name="UploadFiles" />
```

---

### Common Patterns

#### Pattern 1: Validated File Upload
Restrict uploads to specific file types and sizes:

```typescript
const uploader = new Uploader({
  asyncSettings: {
    saveUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/save',
    removeUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/remove'
  },
  allowedExtensions: '.jpg,.jpeg,.png,.gif',
  minFileSize: 5000,      // 5 KB
  maxFileSize: 5242880    // 5 MB
});
uploader.appendTo('#fileupload');
```

#### Pattern 2: Drag-and-Drop Upload
Enable modern file upload UX:

```typescript
const uploader = new Uploader({
  asyncSettings: {
    saveUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/save',
    removeUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/remove'
  },
  dropEffect: 'Copy',
  multiple: true,
  allowedExtensions: '.pdf,.doc,.docx'
});
uploader.appendTo('#fileupload');

// Files that are dropped also trigger the selected event
uploader.selected = (args: SelectedEventArgs) => {
  console.log('Files selected/dropped:', args.filesData);
};
```

#### Pattern 3: Large File Chunked Upload
Handle large files with resumable chunks:

```typescript
const uploader = new Uploader({
  asyncSettings: {
    saveUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/save-chunk',
    removeUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/remove',
    chunkSize: 5242880 // 5 MB chunks
  },
  allowedExtensions: '.iso,.zip,.rar',
  minFileSize: 26214400  // 25 MB minimum
});
uploader.appendTo('#fileupload');

uploader.chunkSuccess = (args: any) => {
  console.log('Chunk uploaded:', args.chunkIndex, 'size:', args.chunkSize);
};

uploader.chunkFailure = (args: any) => {
  console.log('Chunk failed for:', args.file.name, 'chunk:', args.chunkIndex);
};
```

#### Pattern 4: File Preview Before Upload
Display images and details before uploading:

```typescript
const uploader = new Uploader({
  asyncSettings: {
    saveUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/save',
    removeUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/remove'
  },
  allowedExtensions: '.jpg,.jpeg,.png'
});
uploader.appendTo('#fileupload');

uploader.selected = (args: any) => {
  // Render preview for each file
  args.filesData.forEach((file: any) => {
    const reader = new FileReader();
    reader.onload = (e: any) => {
      const preview = document.createElement('img');
      preview.src = e.target.result;
      preview.style.maxWidth = '100px';
      document.getElementById('preview')?.appendChild(preview);
    };
    reader.readAsDataURL(file.rawFile);
  });
};
```

---

### Key Properties & Events

> For the complete API reference including all properties, methods, events, and type definitions, see **[references/uploader-api.md](references/uploader-api.md)**.

#### Essential Properties
| Property | Type | Purpose |
|----------|------|---------|
| `asyncSettings` | `AsyncSettingsModel` | Configure upload endpoint and behavior |
| `allowedExtensions` | `string` | Comma-separated file extensions to allow |
| `minFileSize` | `number` | Minimum file size in bytes |
| `maxFileSize` | `number` | Maximum file size in bytes |
| `multiple` | `boolean` | Allow multiple file selection |
| `autoUpload` | `boolean` | Auto-upload on file selection |
| `sequentialUpload` | `boolean` | Upload files one after another |
| `showFileList` | `boolean` | Show or hide the default file list |
| `template` | `string \| Function` | Custom file item template |
| `directoryUpload` | `boolean` | Enable folder/directory upload |
| `dropArea` | `string \| HTMLElement` | Custom drag-and-drop target |
| `dropEffect` | `DropEffect` | Visual drag-and-drop effect |
| `files` | `FilesPropModel[]` | Preloaded files on render |
| `enabled` | `boolean` | Enable or disable the component |
| `enableRtl` | `boolean` | Right-to-left rendering |
| `enableHtmlSanitizer` | `boolean` | Prevent XSS in filenames |
| `buttons` | `ButtonsPropsModel` | Customize button labels/content |
| `cssClass` | `string` | Custom CSS class on root element |
| `htmlAttributes` | `object` | Additional HTML attributes |
| `locale` | `string` | Override global localization |

#### Key Events
| Event | Triggered | Use Case |
|-------|-----------|----------|
| `selected` | File(s) selected | Validate, preview, or modify files |
| `uploading` | Before upload starts | Add headers, metadata, show progress |
| `beforeUpload` | Before upload process | Add parameters to upload request |
| `success` | Upload completes successfully | Handle server response |
| `failure` | Upload fails | Retry logic, error handling |
| `removing` | File being removed | Confirm removal, add custom data |
| `beforeRemove` | Before remove sent to server | Prevent or modify removal request |
| `actionComplete` | All files processed | Batch completion handling |
| `chunkUploading` | Each chunk starts | Add data to chunk requests |
| `chunkSuccess` | Chunk uploaded | Progress tracking |
| `chunkFailure` | Chunk failed | Retry or error handling |
| `pausing` | Chunk upload paused | Track pause state |
| `resuming` | Paused upload resumed | Track resume state |
| `canceling` | Chunk upload canceled | Track cancel state |
| `clearing` | File list being cleared | Prevent or confirm clearing |
| `fileListRendering` | Each file item rendered | Customize file item structure |
| `progress` | File uploading (AJAX progress) | Real-time progress bar updates |
| `change` | File list changes | React to add/remove actions |
| `created` | Component created | Post-init setup |

---

### Common Use Cases

**Use Case 1: Product Image Upload**  
Validate images, resize before upload, show preview → See `references/uploader-advanced-features.md`

**Use Case 2: Document Management**  
Multiple file types, large file support, form integration → See `references/uploader-upload-modes.md` and `references/uploader-advanced-features.md`

**Use Case 3: User Avatar Upload**  
Single image, size validation, custom styling → See `references/uploader-getting-started.md` and `references/uploader-customization-and-styling.md`

**Use Case 4: Secure File Uploads**  
JWT authentication, server validation, error handling → See `references/uploader-advanced-features.md` and `references/uploader-troubleshooting-and-examples.md`

---

### Related Skills
- Implementing Form Validation
- Handling Async Operations in TypeScript
- Custom Event Handling

---

**Next Step:** Start with `references/uploader-getting-started.md` to learn installation and basic setup, jump directly to the reference matching your use case, or consult `references/uploader-api.md` for the complete API reference.


