---
name: geckoui
description: Use this skill when the user asks about "GeckoUI", "geckoui", "@geckoui/geckoui", "Gecko UI components", "Button component", "Input component", "Select component", "Menu component", "Alert component", "Dialog component", "Drawer component", "Calendar component", "Switch component", "Checkbox component", "Radio component", "Tooltip component", "Pagination component", "OTPInput", "DateInput", "DateRangeInput", "CounterInput", "LoadingButton", "Spinner", "Textarea", "Label", "InputError", "ConfirmDialog", "GeckoUIPortal", "Toast", "RHFInput", "RHFSelect", "RHFCheckbox", "RHFRadio", "RHFSwitch", "RHFTextarea", "RHFDateInput", "RHFFilePicker", "RHFError", "GeckoUI theming", "oklch theme", "--color-primary", "--color-surface", "--color-text", "--color-border", "data-variant", "data-color", "data-size", "module augmentation", or needs to build React UIs with GeckoUI components.
version: "1.0.0"
---

# GeckoUI

React component library with Tailwind CSS v4, OKLCH theming, and React Hook Form integration.

## Setup

```bash
pnpm add @geckoui/geckoui
```

```tsx
import "@geckoui/geckoui/styles.css";
```

For Tailwind CSS v4 projects, import inside `@layer`:

```css
@import "tailwindcss";

@layer components {
  @import "@geckoui/geckoui/styles.css";
}
```

Add `GeckoUIPortal` to your layout (required for Dialog, Drawer, ConfirmDialog, Toast):

```tsx
import { GeckoUIPortal } from "@geckoui/geckoui";

<body>
  {children}
  <GeckoUIPortal />
</body>;
```

## Components

### Button

```tsx
<Button variant="filled" color="primary" size="md">Click</Button>
<Button variant="outlined">Cancel</Button>
<Button variant="ghost">Learn More</Button>
<Button variant="icon">X</Button>
<Button disabled>Disabled</Button>
```

| Prop      | Type                                          | Default     |
| --------- | --------------------------------------------- | ----------- |
| `variant` | `"filled" \| "outlined" \| "ghost" \| "icon"` | `"filled"`  |
| `color`   | `"primary"` (extensible)                      | `"primary"` |
| `size`    | `"xs" \| "sm" \| "md" \| "lg" \| "xl"`        | `"md"`      |

Extends `ButtonHTMLAttributes`. Uses `data-variant`, `data-color`, `data-size` attributes.

### LoadingButton

```tsx
<LoadingButton loading loadingText="Saving...">Save</LoadingButton>
<LoadingButton loading spinnerPosition="end">Submit</LoadingButton>
```

| Prop              | Type               | Default   |
| ----------------- | ------------------ | --------- |
| `loading`         | `boolean`          | -         |
| `spinnerPosition` | `"start" \| "end"` | `"start"` |
| `loadingText`     | `string`           | -         |

Extends `ButtonProps`.

### Input

```tsx
<Input placeholder="Email" />
<Input prefix="$" suffix=".00" />
<Input disabled value="readonly" />
```

| Prop             | Type              | Default |
| ---------------- | ----------------- | ------- |
| `prefix`         | `ReactNode \| FC` | -       |
| `suffix`         | `ReactNode \| FC` | -       |
| `className`      | `string`          | -       |
| `inputClassName` | `string`          | -       |

`className` targets the outer wrapper (contains prefix + input + suffix). `inputClassName` targets the actual `<input>` element. Extends `InputHTMLAttributes` (except `prefix`). Uses `data-state="enabled" | "disabled"`.

### Textarea

```tsx
<Textarea placeholder="Message" rows={4} />
<Textarea autoResize />
```

| Prop         | Type      | Default |
| ------------ | --------- | ------- |
| `autoResize` | `boolean` | `false` |

Extends `TextareaAutosizeProps`.

### Select

```tsx
// Single
<Select value={value} onChange={setValue} placeholder="Choose">
  <SelectOption value="a" label="Option A" />
  <SelectOption value="b" label="Option B" />
</Select>

// Multiple
<Select multiple value={values} onChange={setValues} filterable>
  <SelectOption value="red" label="Red" />
  <SelectOption value="blue" label="Blue" />
</Select>
```

| Prop                   | Type                                   | Default                          |
| ---------------------- | -------------------------------------- | -------------------------------- |
| `value`                | `T` or `T[]`                           | -                                |
| `onChange`             | `(v: T) => void` or `(v: T[]) => void` | -                                |
| `multiple`             | `boolean`                              | `false`                          |
| `filterable`           | `boolean \| "inline" \| "dropdown"`    | `false`                          |
| `placeholder`          | `string`                               | -                                |
| `placeholderClassName` | `string`                               | -                                |
| `disabled`             | `boolean`                              | -                                |
| `clearable`            | `boolean`                              | `false`                          |
| `closeMenuOnSelect`    | `boolean`                              | `true` (single), `false` (multi) |
| `placement`            | `Placement`                            | `"bottom-start"`                 |
| `floatingStrategy`     | `Strategy`                             | -                                |
| `hideDefaultEmptyUI`   | `boolean`                              | -                                |
| `prefix`               | `ReactNode \| FC`                      | -                                |
| `suffix`               | `ReactNode \| FC`                      | -                                |
| `wrapperClassName`     | `string`                               | -                                |
| `menuClassName`        | `string`                               | -                                |

`wrapperClassName` targets the outer container. `menuClassName` targets the dropdown panel. `placeholderClassName` targets the placeholder text.

**SelectOption props:** `value` (required), `label` (required), `disabled`, `visibility`, `hideCheckIcon`, `onClick`, `onRemove`, `className` (string or render fn), `children` (ReactNode or render fn).

**SelectTrigger:** render-props for custom trigger, receives `{ keyword, selectedOptions, handleChange, options, toggleMenu, open, openMenu, closeMenu, hasValue, filteredOptions, handleInputChange, handleKeyboardInteraction }`.

**SelectConsumer:** render-props for accessing full Select context: `<SelectConsumer render={(ctx) => ...} />`.

### Menu

```tsx
// Default button
<Menu label="Actions">
  <MenuItem onClick={() => {}}>Edit</MenuItem>
  <MenuItem onClick={() => {}}>Delete</MenuItem>
  <MenuItem disabled>Archived</MenuItem>
</Menu>

// Custom trigger
<Menu>
  <MenuTrigger>
    {({ toggleMenu }) => <Button onClick={toggleMenu}>Options</Button>}
  </MenuTrigger>
  <MenuItem onClick={() => {}}>Edit</MenuItem>
</Menu>
```

**Menu props:** `label`, `disabled`, `placement`, `floatingStrategy`, `className` (outer wrapper), `menuClassName` (dropdown panel), `buttonClassName` (default button).

**MenuItem props:** `onClick`, `disabled`, `children`.

**MenuTrigger:** render function receiving `{ open, toggleMenu, openMenu, closeMenu, disabled }`.

### Alert

```tsx
<Alert variant="error" title="Error" description="Something went wrong" />
<Alert variant="success" title="Done!" onRemove={() => {}} />
<Alert variant="warning" title="Warning" condensed />
```

| Prop            | Type                                                       | Default     |
| --------------- | ---------------------------------------------------------- | ----------- |
| `variant`       | `"error" \| "warning" \| "info" \| "success" \| "default"` | `"default"` |
| `title`         | `ReactNode \| FC`                                          | required    |
| `description`   | `ReactNode \| FC`                                          | -           |
| `condensed`     | `boolean`                                                  | `false`     |
| `onRemove`      | `() => void`                                               | -           |
| `icon`          | `ReactNode \| FC`                                          | -           |
| `iconClassName` | `string`                                                   | -           |

`iconClassName` targets the icon element. Uses `data-variant`, `data-condensed` attributes.

### Dialog

```tsx
Dialog.show({
  content: ({ dismiss }) => (
    <div>
      <h3>Title</h3>
      <p>Content</p>
      <Button onClick={dismiss}>Close</Button>
    </div>
  ),
  className: "max-w-md",
  dismissOnEsc: true,
  dismissOnOutsideClick: true
});
```

| Prop                    | Type                           | Default |
| ----------------------- | ------------------------------ | ------- |
| `content`               | `ReactNode \| FC<{ dismiss }>` | -       |
| `className`             | `string`                       | -       |
| `dismissOnEsc`          | `boolean`                      | `true`  |
| `dismissOnOutsideClick` | `boolean`                      | `true`  |

`className` targets the dialog panel. **Built-in styles:** `bg-surface-primary`, `p-6`, `rounded-md`, `shadow-xl`, `max-w-[400px]`. Override via `className`.

### ConfirmDialog

```tsx
ConfirmDialog.show({
  title: "Delete?",
  content: "This cannot be undone.",
  confirmButtonLabel: "Delete",
  cancelButtonLabel: "Cancel",
  onConfirm: async ({ dismiss }) => {
    await deleteItem();
    dismiss();
  },
  onCancel: ({ dismiss }) => {
    dismiss();
  }
});
```

| Prop                    | Type                                       | Default |
| ----------------------- | ------------------------------------------ | ------- |
| `title`                 | `string`                                   | -       |
| `content`               | `ReactNode \| FC`                          | -       |
| `confirmButtonLabel`    | `string`                                   | -       |
| `cancelButtonLabel`     | `string`                                   | -       |
| `onConfirm`             | `(e: { preventDefault, dismiss }) => void` | -       |
| `onCancel`              | `(e: { preventDefault, dismiss }) => void` | -       |
| `className`             | `string`                                   | -       |
| `titleClassName`        | `string`                                   | -       |
| `contentClassName`      | `string`                                   | -       |
| `dismissOnEsc`          | `boolean`                                  | `true`  |
| `dismissOnOutsideClick` | `boolean`                                  | `true`  |

**Built-in styles:** Same dialog panel styles as Dialog. Title is `text-base font-semibold`, content is `text-sm text-muted`, actions are right-aligned.

### Drawer

```tsx
<Drawer open={isOpen} handleClose={() => setOpen(false)} placement="right">
  <div className="p-6">Drawer content</div>
</Drawer>
```

**Built-in styles:** `bg-surface-primary`, `shadow-xl`, `overflow-y-auto`, no padding. `max-w-md` for left/right, `max-h-[50%]` for top/bottom. Override via `className`.

| Prop                | Type                                     | Default   |
| ------------------- | ---------------------------------------- | --------- |
| `open`              | `boolean`                                | required  |
| `handleClose`       | `() => void`                             | -         |
| `placement`         | `"top" \| "bottom" \| "left" \| "right"` | `"right"` |
| `hideBackdrop`      | `boolean`                                | `false`   |
| `allowClickOutside` | `boolean`                                | `false`   |
| `dismissOnEscape`   | `boolean`                                | `true`    |
| `className`         | `string`                                 | -         |
| `backdropClassName` | `string`                                 | -         |

`className` targets the drawer panel. `backdropClassName` targets the backdrop overlay. Uses `data-placement`, `data-state="open" | "closed"` on the panel.

### Tooltip

```tsx
<Tooltip content="Helpful text" side="top" triggerAsChild>
  <Button>Hover me</Button>
</Tooltip>
```

| Prop               | Type                        | Default |
| ------------------ | --------------------------- | ------- |
| `content`          | `string \| ReactNode \| FC` | -       |
| `side`             | `Placement`                 | `"top"` |
| `sideOffset`       | `number`                    | `12`    |
| `triggerAsChild`   | `boolean`                   | `false` |
| `delayDuration`    | `number`                    | `700`   |
| `backgroundColor`  | `string`                    | -       |
| `className`        | `string`                    | -       |
| `triggerClassName` | `string`                    | -       |
| `arrowClassName`   | `string`                    | -       |

`className` targets the tooltip content. `triggerClassName` targets the trigger wrapper. `arrowClassName` targets the arrow `<svg>`.

### Calendar

```tsx
// Single date
<Calendar selectedDate={date} onSelectDate={setDate} />

// Date range
<Calendar mode="range" selectedRange={range} onSelectRange={setRange} numberOfMonths={2} />
```

### DateInput / DateRangeInput

```tsx
<DateInput value={date} onChange={setDate} format="MM/DD/YYYY" />
<DateInput value={date} onChange={setDate} disabled />
<DateRangeInput value={range} onChange={setRange} numberOfMonths={2} />
```

| Prop                   | Type                                                             | Default          |
| ---------------------- | ---------------------------------------------------------------- | ---------------- |
| `value`                | `string \| null` (DateInput) / `DateRange` (Range)               | -                |
| `onChange`             | `(v: string \| null) => void` / `(v: DateRange \| null) => void` | -                |
| `format`               | `"DD/MM/YYYY" \| "MM/DD/YYYY" \| "YYYY/MM/DD"`                   | -                |
| `separator`            | `string`                                                         | -                |
| `rangeSeparator`       | `string` (DateRangeInput only)                                   | -                |
| `placeholder`          | `string`                                                         | -                |
| `disabled`             | `boolean`                                                        | -                |
| `readOnly`             | `boolean`                                                        | -                |
| `hasError`             | `boolean`                                                        | -                |
| `prefix`               | `ReactNode \| FC`                                                | -                |
| `suffix`               | `ReactNode \| FC`                                                | -                |
| `hideCalendarIcon`     | `boolean`                                                        | -                |
| `hideClearIcon`        | `boolean`                                                        | -                |
| `hideCalendar`         | `boolean`                                                        | `false`          |
| `calendarPlacement`    | `Placement`                                                      | `"bottom-start"` |
| `floatingStrategy`     | `Strategy`                                                       | -                |
| `numberOfMonths`       | `1 \| 2` (DateRangeInput only)                                   | -                |
| `className`            | `string`                                                         | -                |
| `wrapperClassName`     | `string`                                                         | -                |
| `calendarClassName`    | `string`                                                         | -                |
| `placeholderClassName` | `string`                                                         | -                |

`className` targets the input container. `wrapperClassName` targets the outer wrapper (includes floating calendar). `calendarClassName` targets the calendar popup. `placeholderClassName` targets the placeholder text.

### Switch

```tsx
<label className="flex items-center gap-3">
  <Switch size="md" />
  <span>Enable notifications</span>
</label>
```

| Prop             | Type                         | Default |
| ---------------- | ---------------------------- | ------- |
| `size`           | `"sm" \| "md"` (extensible)  | `"md"`  |
| `checked`        | `boolean`                    | -       |
| `defaultChecked` | `boolean`                    | -       |
| `onChange`       | `(checked: boolean) => void` | -       |
| `className`      | `string`                     | -       |
| `thumbClassName` | `string`                     | -       |

`className` targets the outer `<label>` (the visual track). `thumbClassName` targets the sliding thumb circle. Renders hidden `<input type="checkbox" role="switch">` + visual label. Uses CSS `:has(input:checked)`.

### Checkbox

```tsx
<label className="flex items-center gap-2">
  <Checkbox checked={val} onChange={(e) => setVal(e.target.checked)} />
  <span>Agree</span>
</label>
<Checkbox partial /> {/* indeterminate */}
```

### Radio

```tsx
<label><Radio name="plan" value="free" /> Free</label>
<label><Radio name="plan" value="pro" /> Pro</label>
```

### OTPInput

```tsx
<OTPInput value={otp} onChange={setOtp} length={6} onOTPComplete={(v) => verify(v)} />
```

| Prop             | Type                      | Default  |
| ---------------- | ------------------------- | -------- |
| `value`          | `string`                  | required |
| `onChange`       | `(value: string) => void` | required |
| `length`         | `number`                  | `6`      |
| `numberOnly`     | `boolean`                 | `true`   |
| `aspectRatio`    | `string \| number`        | `0.94`   |
| `onOTPComplete`  | `(value: string) => void` | -        |
| `disabled`       | `boolean`                 | -        |
| `className`      | `string`                  | -        |
| `inputClassName` | `string`                  | -        |

`className` targets the grid container. `inputClassName` targets each individual input cell.

### CounterInput

```tsx
<CounterInput value={count} onChange={setCount} min={0} max={100} size="md" />
```

| Prop              | Type                                | Default  |
| ----------------- | ----------------------------------- | -------- |
| `value`           | `number`                            | required |
| `onChange`        | `(value: number) => void`           | required |
| `min`             | `number`                            | -        |
| `max`             | `number`                            | -        |
| `step`            | `number`                            | `1`      |
| `size`            | `"sm" \| "md" \| "lg"` (extensible) | `"md"`   |
| `disabled`        | `boolean`                           | -        |
| `readOnly`        | `boolean`                           | -        |
| `editable`        | `boolean`                           | `false`  |
| `inputClassName`  | `string`                            | -        |
| `buttonClassName` | `string`                            | -        |

`inputClassName` targets the number display input. `buttonClassName` targets the increment/decrement buttons.

### Pagination

```tsx
<Pagination currentPage={page} totalPages={10} onChange={setPage} />
```

### Spinner

```tsx
<Spinner />
<Spinner className="stroke-red-500" />
```

### Label / InputError

```tsx
<Label required tooltip="Help text">Email</Label>
<InputError>Invalid email</InputError>
```

### Toast

```tsx
import { toast } from "@geckoui/geckoui";

toast.success("Saved!");
toast.error("Failed");
toast.info("Info");
toast.warning("Warning");
```

## React Hook Form

All RHF components accept `name` (required), `rules`, `control`, and `disabled`. Use inside `<FormProvider>` or pass `control` explicitly.

```tsx
import { FormProvider, useForm } from "react-hook-form";

const methods = useForm({ defaultValues: { email: "", country: "" } });

<FormProvider {...methods}>
  <form onSubmit={methods.handleSubmit(onSubmit)}>
    <RHFInput name="email" placeholder="Email" />
    <RHFSelect name="country" placeholder="Select country">
      <SelectOption value="us" label="US" />
      <SelectOption value="uk" label="UK" />
    </RHFSelect>
    <RHFTextarea name="bio" placeholder="Bio" />
    <RHFCheckbox name="terms" value={true} uncheckedValue={false} single label="Agree" />
    <RHFRadio name="plan" value="pro" label="Pro" />
    <RHFSwitch name="notifications" />
    <RHFDateInput name="birthDate" />
    <RHFOTPInput name="otp" length={6} />
    <RHFCounterInput name="quantity" min={1} max={10} />
    <RHFError name="email" />
    <Button type="submit">Submit</Button>
  </form>
</FormProvider>;
```

| Base Component   | RHF Component     | Extra Props                                                                           |
| ---------------- | ----------------- | ------------------------------------------------------------------------------------- |
| Input            | RHFInput          | `transform`, `onChange`, `onBlur`                                                     |
| Textarea         | RHFTextarea       | `onChange`, `onBlur`                                                                  |
| Select           | RHFSelect         | `onChange`                                                                            |
| Checkbox         | RHFCheckbox       | `label`, `labelClassName`, `value`, `uncheckedValue`, `single`, `onChange`, `partial` |
| Radio            | RHFRadio          | `label`, `labelClassName`, `value`, `onChange`                                        |
| Switch           | RHFSwitch         | `value`, `uncheckedValue`, `onChange`                                                 |
| DateInput        | RHFDateInput      | `onChange`                                                                            |
| DateRangeInput   | RHFDateRangeInput | `onChange`                                                                            |
| OTPInput         | RHFOTPInput       | -                                                                                     |
| CounterInput     | RHFCounterInput   | `onChange`                                                                            |
| Input (number)   | RHFNumberInput    | `positiveOnly`, `strict`, `maxFractionDigits`, `maxWholeDigitPlaces`                  |
| Input (currency) | RHFCurrencyInput  | `currency: { symbol, code }`                                                          |
| -                | RHFFileInput      | `multiple`, `render`, `inputClassName`                                                |
| -                | RHFFilePicker     | `render` (drag & drop)                                                                |
| -                | RHFError          | `render`                                                                              |
| -                | RHFInputGroup     | `label`, `labelClassName`, `errorClassName` (wraps label + input + error)             |

## Module Augmentation

Extend built-in variant/color/size maps:

```tsx
declare module "@geckoui/geckoui" {
  interface ButtonColorMap {
    secondary: unknown;
    danger: unknown;
  }
}
```

Then add styles:

```css
.GeckoUIButton[data-variant="filled"][data-color="secondary"] {
  /* your styles */
}
```

**Extensible interfaces:** `ButtonVariantMap`, `ButtonColorMap`, `ButtonSizeMap`, `AlertVariantMap`, `SwitchSizeMap`, `CounterInputSizeMap`, `DrawerPlacementMap`.

## Styling

Components use `data-*` attributes for variants/states. Target with attribute selectors:

```css
.GeckoUIButton[data-variant="filled"][data-color="primary"] {
}
.GeckoUIButton[data-size="lg"] {
}
.GeckoUIAlert[data-variant="error"] {
}
.GeckoUIDrawer__drawer[data-placement="right"][data-state="open"] {
}
```

## References

For theming details (all CSS variables, oklch values, dark mode, custom theme output format):

- `references/theming.md` — Complete theming reference
