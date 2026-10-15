---
name: syncfusion-angular-inputs
description: A comprehensive guide to implementing Syncfusion Angular Input components, including Uploader, NumericTextBox, TextBox, Signature, CheckBox, OTP Input, RangeSlider, and TextArea. This guide is intended for building Angular applications with file upload UIs supporting async and chunked uploads, drag‑and‑drop functionality, numeric inputs with validation and formatting, text inputs with floating labels and custom adornments, digital signature capture with undo, redo, and export capabilities, checkbox multi‑select and indeterminate states, seamless form integration, accessibility compliance, one‑time password (OTP) inputs, programmatic row adjustments, and slider tick customization and styling.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Inputs"
---

# Implementing Syncfusion Angular Inputs

## Uploader

The Syncfusion Angular Uploader (`ejs-uploader`) is a full-featured file upload component that supports asynchronous uploads, chunk uploading of large files, drag-and-drop, clipboard paste, directory upload, file validation, templates, form integration, JWT authentication, and comprehensive event handling.

### Component Overview

The Syncfusion Angular Uploader provides:

- **Async upload modes:** Auto upload (default) or manual upload with action buttons
- **Chunk upload:** Split large files into configurable byte-size chunks with retry logic
- **Sequential upload:** Process files one at a time to reduce server traffic
- **File sources:** Browse dialog, drag-and-drop, clipboard paste, directory selection
- **Validation:** File type (extensions), min/max size, custom count limits, duplicate prevention
- **Templates:** Customize the file list item structure; build fully custom upload UIs
- **Form support:** HTML form submission, template-driven forms (ngModel), reactive forms (FormGroup)
- **Accessibility:** WCAG 2.2, Section 508, keyboard navigation, screen reader support
- **Localization:** Customize all static text via L10n

### Documentation & Navigation Guide

> ⚠️ **Agentic use note:** This guide links to multiple reference documents. AI agents should read only the sections relevant to the task at hand — do **not** chain through all references automatically. Follow least-privilege reading: fetch only what is needed.

#### Getting Started
📄 **Read:** [references/getting-started.md](references/uploader-getting-started.md)
- Installation of `@syncfusion/ej2-angular-inputs` ⚠️ **Always verify the package version and integrity before running `npm install` in production pipelines (supply-chain hygiene).**
- Package setup, CSS imports, and Angular standalone component usage
- Adding the `<ejs-uploader>` component
- Configuring async settings (saveUrl, removeUrl)
- Handling success and failure events
- Adding a custom drop area

#### Asynchronous Upload
📄 **Read:** [references/async-upload.md](references/uploader-async-upload.md)
- Multiple and single file upload modes (`multiple` property)
- Save action configuration and server-side handling
- Remove action and `postRawFile` usage
- Auto upload vs manual upload (`autoUpload` property)
- Sequential upload (`sequentialUpload`)
- Preloaded files (`files` property)
- Adding custom HTTP headers to upload requests

#### Chunk Upload
📄 **Read:** [references/chunk-upload.md](references/uploader-chunk-upload.md)
- Enabling chunk upload via `asyncSettings.chunkSize`
- Pause, resume, and cancel chunk uploads
- Retry configuration (`retryCount`, `retryAfterDelay`)
- `chunkSuccess` and `chunkFailure` events
- Server-side chunk assembly implementation

#### File Validation
📄 **Read:** [references/validation.md](references/uploader-validation.md)
- Restricting file types with `allowedExtensions`
- Min/max file size constraints (`minFileSize`, `maxFileSize`)
- Limiting upload count via the `selected` event
- Preventing duplicate file uploads
- MIME type validation before upload
- Image/* validation on drag-and-drop

#### File Sources
📄 **Read:** [references/file-sources.md](references/uploader-file-sources.md)
- Paste images from clipboard
- Directory (folder) upload with `directoryUpload`
- Drag-and-drop with built-in and custom drop areas
- Custom drop area styling (`.e-upload-drag-hover`)
- Triggering file browse from an external button

#### Templates & Custom UI
📄 **Read:** [references/templates-and-custom-ui.md](references/uploader-templates-and-custom-ui.md)
- File list template with the `template` property
- Building a completely custom upload UI (hiding default list with `showFileList`)
- Customizing action buttons with HTML elements (`buttons` property)
- Customizing the progress bar appearance
- Preview images before uploading
- Resize images before uploading to server

#### Form Integration
📄 **Read:** [references/form-integration.md](references/uploader-form-integration.md)
- Using Uploader inside HTML forms (synchronous submission)
- Template-driven forms with `ngModel`
- Reactive forms with `FormGroup`
- Required field validation (`required` attribute)
- Reset behavior with form reset

#### Styling & Appearance
📄 **Read:** [references/styling-and-appearance.md](references/uploader-styling-and-appearance.md)
- Customizing the uploader wrapper dimensions
- Styling the browse button
- Customizing the drop area text
- Customizing the file list container
- Hiding the default drop area
- CSS class reference for key Uploader elements

#### Accessibility & Localization
📄 **Read:** [references/accessibility-and-localization.md](references/uploader-accessibility-and-localization.md)
- WCAG 2.2, Section 508, keyboard shortcuts
- Screen reader and RTL support
- Localizing all static labels and messages with L10n

#### Advanced How-To Patterns
📄 **Read:** [references/advanced-patterns.md](references/uploader-advanced-patterns.md)
- Upload files programmatically with the `upload()` method
- Invisible (background) upload
- Adding additional form data with `customFormData`
- JWT authentication for upload/remove requests
- Show confirmation dialog before removing files
- Get total size of selected files
- Sort selected files in the file list
- Open and edit uploaded files from the server
- Convert uploaded images to binary format

#### API Reference
📄 **Read:** [references/api.md](references/uploader-api.md)
- Complete properties, methods, and events reference
- AsyncSettingsModel, ButtonsPropsModel, FilesPropModel
- All event argument types and their fields

### Quick Start Example

Minimal file uploader with async upload (Angular 21+ standalone):

```typescript
import { Component } from '@angular/core';
import { UploaderModule } from '@syncfusion/ej2-angular-inputs';

@Component({
  imports: [UploaderModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <ejs-uploader
      [asyncSettings]="asyncSettings"
      [autoUpload]="false"
      (success)="onSuccess($event)"
      (failure)="onFailure($event)">
    </ejs-uploader>
  `
})
export class AppComponent {
  public asyncSettings = {
    saveUrl: 'https://your-api/upload/save',    // Replace with your actual endpoint
    removeUrl: 'https://your-api/upload/remove' // Replace with your actual endpoint
  };

  onSuccess(args: any): void {
    console.log('Upload operation:', args.operation, 'File:', args.file.name);
  }

  onFailure(args: any): void {
    console.error('Upload failed:', args.file.name);
  }
}
```

**CSS Theme Setup** (`styles.css`):
```css
@import 'node_modules/@syncfusion/ej2-base/styles/material3.css';
@import 'node_modules/@syncfusion/ej2-buttons/styles/material3.css';
@import 'node_modules/@syncfusion/ej2-inputs/styles/material3.css';
@import 'node_modules/@syncfusion/ej2-popups/styles/material3.css';
@import 'node_modules/@syncfusion/ej2-angular-inputs/styles/material3.css';
```

### Common Patterns

#### Pattern 1: Auto Upload with Drag-and-Drop
```typescript
// Automatically uploads dropped or browsed files
<ejs-uploader
  [asyncSettings]="asyncSettings"
  [dropArea]="dropElement"
  [multiple]="true"
  (success)="onSuccess($event)">
</ejs-uploader>
```

#### Pattern 2: Chunk Upload for Large Files
```typescript
<ejs-uploader
  [asyncSettings]="chunkSettings"
  (chunkSuccess)="onChunkSuccess($event)"
  (chunkFailure)="onChunkFailure($event)">
</ejs-uploader>

// In component:
chunkSettings = {
  saveUrl: 'https://your-api/upload/save',    // Replace with your actual endpoint
  removeUrl: 'https://your-api/upload/remove', // Replace with your actual endpoint
  chunkSize: 500000  // 500 KB chunks
};
```

#### Pattern 3: Validated Upload (Type + Size)
```typescript
<ejs-uploader
  [asyncSettings]="asyncSettings"
  allowedExtensions=".jpg,.png,.pdf"
  [minFileSize]="1024"
  [maxFileSize]="5000000">
</ejs-uploader>
```

#### Pattern 4: Preloaded Files
```typescript
<ejs-uploader
  [asyncSettings]="asyncSettings"
  [files]="preloadedFiles">
</ejs-uploader>

// In component:
preloadedFiles = [
  { name: 'report', size: 200000, type: '.pdf' },
  { name: 'photo', size: 500000, type: '.jpg' }
];
```

### Pattern 5: JWT-Authenticated Upload
```typescript
<ejs-uploader
  [asyncSettings]="asyncSettings"
  (uploading)="addAuthHeader($event)"
  (removing)="addAuthHeader($event)">
</ejs-uploader>

// ⚠️ Never hardcode tokens — always retrieve from a secure auth service (e.g., Angular AuthService or OAuth library).
// ⚠️ Always transmit tokens over HTTPS only. Never pass tokens as URL query parameters.
addAuthHeader(args: any): void {
  args.currentRequest.setRequestHeader('Authorization', `Bearer ${this.token}`);
}
```

### Key Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `[asyncSettings]` | AsyncSettingsModel | `{saveUrl:'',removeUrl:''}` | Server save/remove URLs and chunk config |
| `[autoUpload]` | boolean | `true` | Upload immediately on file selection |
| `[multiple]` | boolean | `true` | Allow selecting multiple files |
| `[allowedExtensions]` | string | `''` | Comma-separated allowed extensions (e.g., `.jpg,.png`) |
| `[minFileSize]` | number | `0` | Minimum file size in bytes |
| `[maxFileSize]` | number | `30000000` | Maximum file size in bytes (~28.6 MB) |
| `[files]` | FilesPropModel[] | `[]` | Preloaded files from server |
| `[dropArea]` | string \| HTMLElement | `null` | Custom drop target element or selector |
| `[directoryUpload]` | boolean | `false` | Enable folder/directory upload |
| `[sequentialUpload]` | boolean | `false` | Upload files one at a time |
| `[showFileList]` | boolean | `true` | Show/hide default file list |
| `[template]` | any | `null` | Custom file list item template |
| `[buttons]` | ButtonsPropsModel | `{browse,clear,upload}` | Customize button text/HTML |
| `[enabled]` | boolean | `true` | Enable or disable the component |
| `[cssClass]` | string | `''` | Additional CSS classes on root element |
| `[enableRtl]` | boolean | `false` | Right-to-left rendering |
| `[enableHtmlSanitizer]` | boolean | `true` | Prevent XSS in filenames |
| `[dropEffect]` | DropEffect | `'Default'` | Drag effect: Copy, Move, Link, None |

### Key Events

| Event | When it Fires | Key Args |
|-------|---------------|----------|
| `(selected)` | Files selected or dropped | `filesData`, `cancel`, `modifiedFilesData` |
| `(uploading)` | Before each file upload starts | `fileData`, `currentRequest`, `customFormData`, `cancel` |
| `(success)` | Upload or remove succeeds | `file`, `operation` (`upload`\|`remove`), `event` |
| `(failure)` | Upload or remove fails | `file`, `operation`, `event` |
| `(progress)` | Upload progress | `file`, `event` (loaded, total) |
| `(removing)` | Before file remove request | `filesData`, `postRawFile`, `currentRequest` |
| `(beforeRemove)` | Before remove confirmation | `filesData`, `cancel` |
| `(beforeUpload)` | Before upload process | `fileData`, `customFormData` |
| `(change)` | File list changes | `file` |
| `(clearing)` | Before clear all action | `cancel` |
| `(chunkSuccess)` | Each chunk uploads OK | `chunkIndex`, `totalChunk`, `chunkSize`, `file` |
| `(chunkFailure)` | Each chunk fails | `chunkIndex`, `totalChunk`, `chunkSize`, `file`, `cancel` |
| `(chunkUploading)` | Before each chunk upload | `fileData`, `currentRequest`, `customFormData` |
| `(pausing)` | Chunk upload paused | `file`, `chunkIndex` |
| `(resuming)` | Chunk upload resumed | `file`, `chunkIndex` |
| `(canceling)` | Upload canceled | `file` |
| `(fileListRendering)` | Before each file item renders | `element`, `fileInfo` |
| `(actionComplete)` | All files processed | `fileData` |
| `(created)` | Component initialized | — |

### Key Methods

| Method | Purpose |
|--------|---------|
| `upload(files?, custom?)` | Programmatically start upload for selected or specific files |
| `remove(fileData?, custom?, postRawFile?)` | Remove a file from list or server |
| `cancel(fileData?)` | Cancel an in-progress chunk upload |
| `pause(fileData?, custom?)` | Pause a chunk upload |
| `resume(fileData?, custom?)` | Resume a paused chunk upload |
| `retry(fileData?, fromCanceledStage?, custom?)` | Retry a failed or canceled upload |
| `clearAll()` | Clear all files from the list |
| `getFilesData(index?)` | Get file data array shown in the list |
| `createFileList(fileData)` | Programmatically create file list items |
| `sortFileList(filesData?)` | Sort file list alphabetically |
| `bytesToSize(bytes)` | Convert bytes to human-readable KB/MB string |
| `destroy()` | Destroy the component and detach events |

### Common Use Cases

**Use Case 1: Profile Photo Upload**
- `multiple="false"`, `allowedExtensions=".jpg,.png,.gif,.webp"`, `maxFileSize=5000000`
- Use `selected` event to preview before upload
- Auto upload with progress indicator

**Use Case 2: Document Upload Portal**
- Multiple files, `allowedExtensions=".pdf,.doc,.docx,.xlsx"`
- Chunk upload for large files with pause/resume
- Sequential upload to manage server load

**Use Case 3: Image Gallery Batch Upload**
- Multiple files, directory upload enabled
- Preview thumbnails using `selected` event + FileReader
- Sort by file name before upload

**Use Case 4: Secure File Upload (API-Authenticated)**
- JWT token injected via `uploading` event header
- Custom `customFormData` to pass metadata
- Server validates token before saving

**Use Case 5: Form with Required File**
- `autoUpload=false`, synchronous form submission
- Required attribute validation with `data-required-message`
- Template-driven or reactive form binding

### Next Steps

1. **Getting Started** → Install package and render basic uploader
2. **Async Upload** → Configure save/remove URLs and upload modes
3. **Validation** → Add extension and size constraints
4. **Chunk Upload** → Handle large files with pause/resume
5. **Templates** → Customize file list appearance
6. **Form Integration** → Bind to Angular forms
7. **Advanced Patterns** → JWT auth, programmatic upload, custom UI
8. **API Reference** → Full properties, methods, events list

---

**For detailed implementation, start with [references/getting-started.md](references/uploader-getting-started.md)**

## NumericTextBox

### Component Overview

The Syncfusion Angular NumericTextBox is a specialized input control for numeric values. It provides:
- **Numeric validation** with min/max ranges and strict mode
- **Formatting** (currency, percentage, decimals)
- **Spin buttons** for value adjustment
- **Adornments** (prepend/append templates for icons, labels)
- **Accessibility** (WCAG 2.2, ARIA, keyboard navigation)
- **Localization** (multiple cultures and RTL support)
- **Form integration** (reactive forms, template-driven forms)

---

### Documentation and Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/numerictextbox-getting-started.md)
- Installation and package setup
- Angular 21+ standalone component setup
- Basic NumericTextBox implementation
- CSS imports and theme configuration
- Range validation with min/max
- Simple formatting example
- Precision and decimals control
- Two-way binding setup
- Reactive forms integration

#### Formats and Number Styling
📄 **Read:** [references/formats-styling.md](references/numerictextbox-formats-styling.md)
- Standard formats (currency `c2`, percentage `p`, numbers `n`)
- Custom numeric format strings
- Decimal place control
- Currency symbols and localization
- Styling NumericTextBox wrapper and icons
- CSS customization patterns

#### Spinners and Step Control
📄 **Read:** [references/spinners-and-step.md](references/numerictextbox-spinners-and-step.md)
- Spin button visibility (`showSpinButton`)
- Step value configuration (`step` property)
- Customizing spin up/down arrow icons
- Arrow key interactions
- Disabling spin buttons

#### Adornments and Templates
📄 **Read:** [references/adornments-and-templates.md](references/numerictextbox-adornments-and-templates.md)
- Adding prefix/suffix with `prependTemplate` and `appendTemplate`
- Currency symbols and unit labels
- Action buttons and icons
- Status indicators without affecting validation
- Template usage patterns

#### Validation and Form Integration
📄 **Read:** [references/validation-and-forms.md](references/numerictextbox-validation-and-forms.md)
- Range validation (min/max with strictMode)
- Custom validation rules
- Error and warning states
- Reactive forms patterns

#### Advanced Patterns and Edge Cases
📄 **Read:** [references/advanced-patterns.md](references/numerictextbox-advanced-patterns.md)
- Maintaining trailing zeros on focus
- Preventing nullable input (always require a value)
- Nullable input configuration
- Clear button behavior
- Read-only and disabled states
- Focus and blur event handling
- Float label types (Always, Auto, Never)
- Performance optimization

#### Accessibility and Migration
📄 **Read:** [references/accessibility-and-migration.md](references/numerictextbox-accessibility-and-migration.md)
- WCAG 2.2 Level AA compliance
- ARIA attributes (spinbutton role, aria-valuemin, aria-valuemax, etc.)
- Keyboard navigation (Arrow Up/Down)
- Screen reader support
- RTL support for right-to-left languages
- EJ1 to EJ2 API migration guide
- Localization and globalization

#### Globalization and Localization
📄 **Read:** [references/globalization.md](references/numerictextbox-globalization.md)
- Locale property configuration
- Culture-specific number formatting
- RTL (right-to-left) support
- International number formats

#### API Reference
📄 **Read:** [references/api.md](references/numerictextbox-api.md)
- All component properties with types, defaults, and descriptions
- All public methods with signatures and usage examples
- All events with argument interface details
- `ChangeEventArgs`, `NumericBlurEventArgs`, `NumericFocusEventArgs` interfaces
- Complete summary tables for quick lookup

---

### Quick Start Example

```typescript
import { NumericTextBoxModule } from '@syncfusion/ej2-angular-inputs';
import { Component } from '@angular/core';

@Component({
  imports: [NumericTextBoxModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <ejs-numerictextbox
      value="100"
      min="10"
      max="1000"
      step="5"
      format="c2"
      placeholder="Enter amount">
    </ejs-numerictextbox>
  `
})
export class AppComponent {}
```

---

### Common Patterns

#### Currency Input with Validation
```typescript
<ejs-numerictextbox
  value="50.00"
  format="c2"
  currency="USD"
  min="0"
  max="10000"
  decimals="2"
  strictMode="true">
</ejs-numerictextbox>
```

#### Percentage Input
```typescript
<ejs-numerictextbox
  value="25"
  format="p"
  min="0"
  max="100"
  step="1">
</ejs-numerictextbox>
```

#### With Adornments (Unit Label)
```typescript
<ejs-numerictextbox
  value="100"
  [appendTemplate]="appendUnit">
</ejs-numerictextbox>

<ng-template #appendUnit>
  <span class="unit-label">kg</span>
</ng-template>
```

#### Two-Way Binding with Form Control
```typescript
<ejs-numerictextbox
  [(ngModel)]="quantity"
  min="1"
  max="100"
  step="1">
</ejs-numerictextbox>
```

---

### Key Properties

| Property | Type | Purpose | Default |
|----------|------|---------|---------|
| `value` | number | Current numeric value | `null` |
| `min` | number | Minimum allowed value | `Number.MIN_VALUE` |
| `max` | number | Maximum allowed value | `Number.MAX_VALUE` |
| `step` | number | Increment/decrement amount | `1` |
| `decimals` | number | Decimal places allowed | `null` |
| `format` | string | Number format (e.g., 'c2', 'n2', 'p') | `null` |
| `currency` | string | Currency code (e.g., 'USD', 'EUR') | `null` |
| `strictMode` | boolean | Enforce min/max validation | `false` |
| `showSpinButton` | boolean | Show up/down spinner buttons | `true` |
| `showClearButton` | boolean | Show clear button | `false` |
| `readonly` | boolean | Prevent editing | `false` |
| `disabled` | boolean | Disable the component | `false` |
| `locale` | string | Culture code (e.g., 'de-DE', 'fr-FR') | `'en-US'` |
| `enableRtl` | boolean | Enable right-to-left mode | `false` |
| `placeholder` | string | Hint text | `null` |
| `floatLabelType` | string | Label float behavior ('Auto', 'Always', 'Never') | `'Never'` |

---

### Common Use Cases

1. **E-Commerce Quantity Input** — Product quantity selector with min/max validation
2. **Financial Forms** — Currency input with currency symbol and decimal places
3. **Scientific Applications** — High-precision decimal inputs
4. **Survey/Form Data** — Percentage inputs with 0-100 range
5. **Multi-Language Support** — Numbers formatted per user locale
6. **Accessibility-First Forms** — WCAG-compliant numeric inputs
7. **Mobile-Friendly** — Touch-friendly spin buttons and keyboard input

---

### See Also

- [Syncfusion Angular Input Controls](https://www.syncfusion.com/angular-components/angular-textbox)
- [Angular Forms Documentation](https://angular.dev/guide/forms)
- [WCAG 2.2 Accessibility Guidelines](https://www.w3.org/TR/WCAG22/)
- [Syncfusion Theme Studio](https://ej2.syncfusion.com/angular/documentation/appearance/theme-studio)


## TextBox

The Syncfusion Angular TextBox component is a feature-rich input element that enhances the native HTML input with floating labels, validation states, adornments (prepended/appended elements), accessibility support, and comprehensive styling options. This skill guides you through implementation patterns, configuration, and best practices.

### Component Overview

The TextBox component provides:

| Feature | Purpose |
|---------|---------|
| **Floating Labels** | Animated labels that float above input when focused or filled |
| **Validation States** | Visual feedback (error, warning, success) with CSS classes |
| **Adornments** | Prepend/append custom HTML elements (icons, buttons, units) |
| **Clear Button** | Built-in clear functionality to reset input value |
| **Disabled/Read-only States** | Control user interaction and editability |
| **HTML Attributes** | Support for standard input attributes (type, maxlength, etc.) |
| **Multiline Support** | Textarea configuration with row/column sizing |
| **Accessibility** | WCAG 2.2 compliance, keyboard navigation, ARIA attributes |
| **RTL Support** | Right-to-left language support |
| **Styling Options** | CSS classes, validation colors, responsive sizing |

---

### Documentation and Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/textbox-getting-started.md)
- Installation and package setup
- Create your first TextBox component
- CSS imports and theme selection
- Floating label implementation
- Basic event binding and data binding
- Common setup issues and solutions

#### Input Features and State Management
📄 **Read:** [references/input-features.md](references/textbox-input-features.md)
- Clear button implementation (showClearButton)
- Disabled state (enabled property)
- Read-only state (readonly property)
- HTML attributes configuration (htmlAttributes)
- Supporting input types and attributes
- State management patterns for forms

#### Adornments and Customization
📄 **Read:** [references/adornments-customization.md](references/textbox-adornments-customization.md)
- Prepend and append template usage
- Icon adornments for visual context
- Button adornments (password toggle, clear)
- Validation status indicators
- Unit indicators (currency, temperature, etc.)
- Performance and accessibility considerations

#### Validation States and Error Handling
📄 **Read:** [references/validation-states.md](references/textbox-validation-states.md)
- Error, warning, and success validation states
- CSS class approach (e-error, e-warning, e-success)
- Visual feedback patterns
- Adding asterisk for required fields
- Form integration with validation
- Custom error message display

#### Styling and Appearance Customization
📄 **Read:** [references/styling-appearance.md](references/textbox-styling-appearance.md)
- CSS structure and class hierarchy
- Basic sizing (height, font, padding)
- Floating label color customization
- Validation state color changes
- Borders, rounded corners, and advanced styling
- Dynamic styling based on input value
- Theme integration and customization

#### Multiline and Sizing Features
📄 **Read:** [references/multiline-sizing.md](references/textbox-multiline-sizing.md)
- Multiline textarea configuration
- Row and column sizing
- Responsive sizing patterns
- Height adjustments and constraints
- Character counting implementation
- Text wrapping and overflow handling

#### Accessibility and Migration
📄 **Read:** [references/accessibility-migration.md](references/textbox-accessibility-migration.md)
- WCAG 2.2 and Section 508 compliance
- Keyboard navigation support
- ARIA attributes (aria-labelledby, aria-invalid, aria-disabled)
- Screen reader compatibility
- Migration from CSS TextBox to Angular component
- RTL and mobile accessibility

---

### Quick Start Example

**Create a floating label TextBox:**

```typescript
import { Component } from '@angular/core';
import { TextBoxModule } from '@syncfusion/ej2-angular-inputs';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [TextBoxModule],
  template: `
    <div style="margin: 50px;">
      <h2>Angular TextBox Example</h2>
      <ejs-textbox 
        #textbox
        [floatLabelType]="'Auto'"
        placeholder="Enter your name"
        (input)="onInput($event)"
      ></ejs-textbox>
      <p>Value: {{ textValue }}</p>
    </div>
  `
})
export class AppComponent {
  textValue = '';

  onInput(event: any) {
    this.textValue = event.target.value;
  }
}
```

**Key Points:**
- Use `floatLabelType="'Auto'"` for automatic floating labels
- Import `TextBoxModule` from `@syncfusion/ej2-angular-inputs`
- Use standard Angular `(input)` event binding
- Set `placeholder` for the floating label text

---

### Common Patterns

#### Pattern 1: Email Input with Icon Adornment
```typescript
<ejs-textbox
  placeholder="Email"
  [floatLabelType]="'Auto'"
  [appendTemplate]="'appendTemplate'"
></ejs-textbox>
<ng-template #appendTemplate>
  <span class="e-input-group-icon">✉</span>
</ng-template>
```
**When to Use:** Email, username, or other fields with visual context

#### Pattern 2: Password Toggle
```typescript
<ejs-textbox
  [type]="passwordVisible ? 'text' : 'password'"
  placeholder="Password"
  [floatLabelType]="'Auto'"
  [appendTemplate]="'toggleTemplate'"
></ejs-textbox>
<ng-template #toggleTemplate>
  <button (click)="togglePassword()">👁</button>
</ng-template>

// Component
togglePassword() {
  this.passwordVisible = !this.passwordVisible;
}
```
**When to Use:** Password fields requiring visibility toggle

#### Pattern 3: Validation with Error Display
```typescript
<ejs-textbox
  [cssClass]="isValid ? 'e-success' : 'e-error'"
  placeholder="Phone"
  (change)="validatePhone($event)"
></ejs-textbox>
<p *ngIf="!isValid" style="color: red;">{{ errorMessage }}</p>
```
**When to Use:** Form fields with validation feedback

#### Pattern 4: Currency Input with Unit Indicator
```typescript
<ejs-textbox
  type="number"
  placeholder="Amount"
  [prependTemplate]="'prependTemplate'"
></ejs-textbox>
<ng-template #prependTemplate>
  <span style="padding: 0 8px;">$</span>
</ng-template>
```
**When to Use:** Currency, temperature, or measurement inputs

---

### Key Props and Configuration

Refer to the full API summary in [references/api.md](references/textbox-api.md).

| Property / Method | Type | Purpose |
|------------------|------|--------|
| `floatLabelType` | string | 'Auto' | 'Always' | 'Never' - Controls floating label behavior |
| `placeholder` | string | Text shown when empty; used for floating labels |
| `value` | string | Current input value |
| `enabled` | boolean | Enable/disable the input (default: true) |
| `readonly` | boolean | Make input read-only (selectable but not editable) |
| `showClearButton` | boolean | Display clear button when field has content |
| `cssClass` | string | Custom CSS classes (e.g., 'e-error', 'e-warning', 'e-success', 'e-small', 'e-bigger', 'e-outline', 'e-corner') |
| `htmlAttributes` | object | Standard HTML attributes (name, maxlength, type, etc.) |
| `prependTemplate` | template | Template for content prepended before the input |
| `appendTemplate` | template | Template for content appended after the input |
| `multiline` | boolean | Enable textarea mode (renders a `<textarea>`) |
| `addIcon(position, icons)` | method | Add icon(s) programmatically (`position` = 'append'|'prepend') |
| `addAttributes(attributes)` | method | Add HTML attributes programmatically (e.g., `maxlength`) |
| `removeAttributes(names[])` | method | Remove previously added attributes |
| `focusIn()` / `focusOut()` | method | Programmatically focus or blur the component |
| `destroy()` | method | Destroy the component instance and detach handlers |
| `getPersistData()` | method | Return persisted state string (when `enablePersistence` is used) |

**Notes:**
- Use CSS class `e-corner` together with `e-outline` to show rounded corners for box-model TextBoxes.
- `rows` and `cols` are **not** component properties. To set them on a multiline TextBox, use `addAttributes({rows: '5'} as any)` in the `(created)` event handler (see `references/multiline-sizing.md`).
- For programmatic input creation (dynamic forms), use `Input.createInput` from `@syncfusion/ej2-inputs` (see `references/input-features.md`).

---

### Common Use Cases

#### 1. **Contact Form**
Multiple TextBox fields with floating labels, validation states, and required field indicators. See [validation-states.md](references/textbox-validation-states.md) and [accessibility-migration.md](references/textbox-accessibility-migration.md).

#### 2. **Search Input with Clear Button**
TextBox with `showClearButton=true` for quick input reset. See [input-features.md](references/textbox-input-features.md).

#### 3. **Styled Input with Icon Prefix/Suffix**
TextBox with `prependTemplate` or `appendTemplate` for visual context. See [adornments-customization.md](references/textbox-adornments-customization.md).

#### 4. **Password Field with Toggle**
Password input with visibility toggle button via append template. See [adornments-customization.md](references/textbox-adornments-customization.md).

#### 5. **Multiline Comment Field**
Textarea with row sizing and character counting. See [multiline-sizing.md](references/textbox-multiline-sizing.md).

#### 6. **Accessible Form Field**
TextBox with proper ARIA attributes and keyboard support for compliance. See [accessibility-migration.md](references/textbox-accessibility-migration.md).

---

### Related Documentation

- **Syncfusion Angular Inputs**: https://ej2.syncfusion.com/angular/documentation/textbox
- **TextBox API Reference**: https://ej2.syncfusion.com/angular/documentation/api/textbox/
- **Angular Input Guide**: [Angular Official Docs](https://angular.io/guide/forms)
- **WCAG Accessibility**: https://www.w3.org/TR/WCAG22/

---

### Next Steps

1. Start with [references/textbox-getting-started.md](references/textbox-getting-started.md) to set up your first TextBox
2. Explore [references/textbox-input-features.md](references/textbox-input-features.md) for state management
3. Use [references/textbox-adornments-customization.md](references/textbox-adornments-customization.md) for custom UI
4. Reference [references/textbox-validation-states.md](references/textbox-validation-states.md) for form validation
5. Customize styling with [references/textbox-styling-appearance.md](references/textbox-styling-appearance.md)
6. Handle advanced cases in [references/textbox-multiline-sizing.md](references/textbox-multiline-sizing.md) and [references/textbox-accessibility-migration.md](references/textbox-accessibility-migration.md)

---

## Signature

The Syncfusion Angular Signature component (`ejs-signature`) provides a smooth, canvas-based digital signature capture experience with comprehensive features including undo/redo operations, multiple export formats, customizable strokes, and full accessibility support.

**Package:** `@syncfusion/ej2-angular-inputs`  
**Selector:** `ejs-signature` (on a `<canvas>` element)  
**Module:** `SignatureModule`

### Component Overview

The Signature component provides:

- **Smooth Stroke Rendering:** Velocity-based stroke width adjustment for natural signing
- **Complete Action History:** Undo/redo with snapshot tracking
- **Multiple Export Formats:** PNG, JPEG, SVG, Base64, or Blob
- **Full Customization:** Stroke properties, colors, and background images
- **Accessibility First:** WCAG 2.2 compliant with keyboard shortcuts
- **Read-only and Disabled States:** For view-only or restricted scenarios
- **Background Persistence:** Option to include/exclude background in saved files

### Documentation and Navigation Guide

> ⚠️ **Agentic use note:** Read only the sections relevant to your task — do **not** chain through all references automatically.

#### Getting Started
📄 **Read:** [references/signature-getting-started.md](references/signature-getting-started.md)
- Angular 21 setup and standalone architecture
- Package installation and dependencies
- CSS theme imports and configuration
- Basic component rendering
- First running application

#### Drawing Signatures Programmatically
📄 **Read:** [references/signature-drawing-signatures.md](references/signature-drawing-signatures.md)
- `draw()` method for text-based signatures
- Font family and font size options
- Render text as signature with custom styling
- User input integration for drawing

#### User Interactions
📄 **Read:** [references/signature-user-interactions.md](references/signature-user-interactions.md)
- Undo and redo functionality with `canUndo()`/`canRedo()` checks
- Clear method for erasing signatures
- Disabled state for preventing user input
- Read-only mode for view-only scenarios
- Button state management and change events

#### Customization and Styling
📄 **Read:** [references/signature-customization.md](references/signature-customization.md)
- Stroke width control (`minStrokeWidth`, `maxStrokeWidth`, `velocity`)
- Stroke color customization with hex/RGB/named colors
- Background color setup
- Background image integration
- Real-time property updates

#### Opening and Saving Signatures
📄 **Read:** [references/signature-open-save.md](references/signature-open-save.md)
- Load pre-drawn signatures using `load()` method
- Base64 encoding and URL support
- Save as Base64 with `getSignature()`
- Save as Blob with `saveAsBlob()`
- Save as image file (`save()` method)
- `saveWithBackground` property for background inclusion

#### Toolbar Integration
📄 **Read:** [references/signature-toolbar-integration.md](references/signature-toolbar-integration.md)
- Complete toolbar setup with undo/redo/save buttons
- Color picker integration for stroke and background colors
- Stroke width controls with dropdown
- Clear and disable toggles
- Button state management with change events
- Full working toolbar example

#### Accessibility
📄 **Read:** [references/signature-accessibility.md](references/signature-accessibility.md)
- WCAG 2.2 and Section 508 compliance
- Keyboard shortcuts (Ctrl+Z, Ctrl+Y, Ctrl+S, Delete)
- Screen reader support and keyboard navigation
- Color contrast and focus indicators
- Mobile device support

#### API Reference
📄 **Read:** [references/signature-api.md](references/signature-api.md)
- Complete properties reference (`backgroundColor`, `strokeColor`, `disabled`, etc.)
- All methods (`undo`, `redo`, `clear`, `draw`, `save`, `load`, etc.)
- Events and event arguments (`change`, `beforeSave`, `created`)
- Parameters and return types

### Quick Start Example

```typescript
import { Component } from '@angular/core';
import { SignatureModule } from '@syncfusion/ej2-angular-inputs';

@Component({
  imports: [SignatureModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <div class="e-section-control">
      <h4>Sign here</h4>
      <canvas ejs-signature #signature id="signature"></canvas>
    </div>
  `
})
export class AppComponent {}
```

**CSS Theme Setup** (`styles.css`):
```css
@import 'node_modules/@syncfusion/ej2-base/styles/material3.css';
@import 'node_modules/@syncfusion/ej2-inputs/styles/material3.css';
@import 'node_modules/@syncfusion/ej2-angular-inputs/styles/material3.css';
```

### Common Patterns

#### Pattern 1: Capture and Save Signature
```typescript
import { Component, ViewChild } from '@angular/core';
import { SignatureComponent, SignatureModule } from '@syncfusion/ej2-angular-inputs';

@Component({
  imports: [SignatureModule],
  standalone: true,
  selector: 'app-save-signature',
  template: `
    <canvas ejs-signature #signature id="signature"></canvas>
    <button (click)="saveSignature()">Save as PNG</button>
  `
})
export class SaveSignatureComponent {
  @ViewChild('signature') public signature?: SignatureComponent;

  saveSignature(): void {
    if (!this.signature?.isEmpty()) {
      this.signature?.save('Png', 'MySignature');
    }
  }
}
```

#### Pattern 2: Undo/Redo with State Management
```typescript
change(): void {
  this.undoButton.disabled = !this.signature?.canUndo();
  this.redoButton.disabled = !this.signature?.canRedo();
  this.clearButton.disabled = this.signature?.isEmpty() ?? true;
}
```

#### Pattern 3: Load and Verify Signature
```typescript
loadSignature(): void {
  const base64String = (document.getElementById('signatureInput') as any).value;
  try {
    this.signature?.load(base64String);
  } catch (error) {
    console.error('Invalid signature format');
  }
}
```

### Key Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `strokeColor` | string | `'#000000'` | Pen stroke color |
| `backgroundColor` | string | `'#ffffff'` | Canvas background color |
| `backgroundImage` | string | `''` | Background image URL ⚠️ Validate and allowlist URLs; avoid untrusted or user-supplied values to prevent mixed-content or open-redirect issues |
| `minStrokeWidth` | number | `0.5` | Minimum stroke width |
| `maxStrokeWidth` | number | `2.0` | Maximum stroke width |
| `velocity` | number | `0.7` | Stroke velocity factor |
| `saveWithBackground` | boolean | `false` | Include background when saving |
| `disabled` | boolean | `false` | Disable signature input |
| `isReadOnly` | boolean | `false` | Read-only (view-only) mode |
| `enablePersistence` | boolean | `false` | Persist signature across reloads |
| `cssClass` | string | `''` | Additional CSS classes |

### Key Methods

| Method | Purpose |
|--------|---------|
| `undo()` | Undo the last stroke |
| `redo()` | Redo the last undone stroke |
| `canUndo()` | Returns `true` if undo is available |
| `canRedo()` | Returns `true` if redo is available |
| `clear()` | Erase all strokes |
| `isEmpty()` | Returns `true` if no strokes drawn |
| `draw(text, font?, fontSize?)` | Draw text as a signature |
| `save(type?, fileName?)` | Save as PNG/JPEG/SVG file |
| `getSignature(type?)` | Get signature as Base64 string |
| `saveAsBlob(type?)` | Get signature as a Blob |
| `getBlob(type?)` | Returns a Blob of the signature |
| `load(signature)` | Load a Base64 or URL signature |
| `refresh()` | Refresh and redraw the canvas |
| `destroy()` | Destroy the component |

### Key Events

| Event | When it Fires | Key Args |
|-------|---------------|----------|
| `(change)` | After each stroke completes | `isEmpty` |
| `(beforeSave)` | Before `save()` executes | `fileName`, `fileType`, `cancel` |
| `(created)` | Component initialized | — |

### Common Use Cases

1. **Contract/Agreement Signing** — Capture user signature and save as Base64 for backend storage
2. **Feedback Forms** — Embedded signature field with clear/undo controls
3. **Document Approval** — Load existing signature, verify it is not empty before form submit
4. **Toolbar-Driven Signing** — Full toolbar with color pickers, stroke width, undo/redo, save
5. **Programmatic Signature** — Draw typed name as a styled signature via `draw()` method

---

**For detailed implementation, start with [references/signature-getting-started.md](references/signature-getting-started.md)**

---

## CheckBox

The Syncfusion Angular CheckBox (`ejs-checkbox`) is a graphical UI element that lets users select one or more options. It supports **checked**, **unchecked**, and **indeterminate** states, flexible label positioning, size variants, two-way binding with `ngModel`, full accessibility compliance, and rich CSS customization.

**Package:** `@syncfusion/ej2-angular-buttons`  
**Selector:** `ejs-checkbox`  
**Module:** `CheckBoxModule`

### Component Overview

The CheckBox component provides:

- **Three States:** Checked, unchecked, and indeterminate (partial selection)
- **Label Control:** Caption text with before/after positioning
- **Size Variants:** Default and small (`e-small`) sizes
- **Form Support:** `name`/`value` attributes for HTML form submission, `ngModel` two-way binding
- **Accessibility:** WCAG 2.2, Section 508, keyboard navigation (Space key), screen reader support
- **Custom Styling:** Color variants, round frames, custom check icons via CSS classes
- **RTL Support:** Right-to-left rendering

### Documentation and Navigation Guide

> ⚠️ **Agentic use note:** Read only the sections relevant to your task — do **not** chain through all references automatically.

#### Getting Started
📄 **Read:** [references/checkbox-getting-started.md](references/checkbox-getting-started.md)
- Installing `@syncfusion/ej2-angular-buttons` via `ng add`
- `CheckBoxModule` import in standalone component's `imports[]`
- CSS theme imports (material theme)
- Minimal `ejs-checkbox` setup and running the app
- Checked, unchecked, and indeterminate states

#### Label and Size
📄 **Read:** [references/checkbox-label-and-size.md](references/checkbox-label-and-size.md)
- `label` property for caption text
- `labelPosition` (`"Before"` / `"After"`)
- Small size via `cssClass="e-small"`
- Default vs. small size examples

#### Style and Appearance
📄 **Read:** [references/checkbox-style-and-appearance.md](references/checkbox-style-and-appearance.md)
- Color variant customization (primary, success, warning, danger, info) via `cssClass`
- Custom checkbox frame shapes (round checkbox with `e-custom`)
- Custom check icon with `e-checkicon`
- CSS rules for appearance override

#### Accessibility and RTL
📄 **Read:** [references/checkbox-accessibility.md](references/checkbox-accessibility.md)
- WCAG 2.2 / Section 508 compliance
- WAI-ARIA attributes (`aria-disabled`)
- Keyboard navigation (Space key)
- Right-to-left (`enableRtl`) support
- Screen reader support

#### How-To Guides
📄 **Read:** [references/checkbox-how-to.md](references/checkbox-how-to.md)
- Name and value in form submission
- Two-way binding with `ngModel`
- Enabling right-to-left display
- Customized checkbox appearance variants

#### API Reference
📄 **Read:** [references/checkbox-api.md](references/checkbox-api.md)
- All properties: `checked`, `cssClass`, `disabled`, `enableHtmlSanitizer`, `enablePersistence`, `enableRtl`, `htmlAttributes`, `indeterminate`, `label`, `labelPosition`, `locale`, `name`, `value`
- Methods: `click()`, `destroy()`, `focusIn()`
- Events: `change`, `created`

### Quick Start Example

```typescript
import { CheckBoxModule } from '@syncfusion/ej2-angular-buttons';
import { Component } from '@angular/core';

@Component({
  imports: [CheckBoxModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <div class="e-section-control">
      <ejs-checkbox label="Default"></ejs-checkbox>
    </div>`
})
export class AppComponent { }
```

**CSS Theme Setup** (`styles.css`):
```css
@import '../node_modules/@syncfusion/ej2-base/styles/material.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/material.css';
```

### Common Patterns

#### Checked, Unchecked, and Indeterminate States
```typescript
@Component({
  imports: [CheckBoxModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <ul>
      <li><ejs-checkbox label="Checked" [checked]="true"></ejs-checkbox></li>
      <li><ejs-checkbox label="Unchecked"></ejs-checkbox></li>
      <li><ejs-checkbox label="Indeterminate" [indeterminate]="true"></ejs-checkbox></li>
    </ul>`
})
export class AppComponent { }
```

#### Change Event Handler
```typescript
import { CheckBoxModule, ChangeEventArgs } from '@syncfusion/ej2-angular-buttons';
import { Component } from '@angular/core';

@Component({
  imports: [CheckBoxModule],
  standalone: true,
  selector: 'app-root',
  template: `<ejs-checkbox label="Subscribe" (change)="onChange($event)"></ejs-checkbox>`
})
export class AppComponent {
  onChange(args: ChangeEventArgs): void {
    console.log('Checked:', args.checked);
  }
}
```

#### Form Submission with Name and Value
```typescript
@Component({
  imports: [CheckBoxModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <form>
      <ejs-checkbox name="Sport" value="Cricket" label="Cricket" [checked]="true"></ejs-checkbox>
      <ejs-checkbox name="Sport" value="Hockey" label="Hockey" [checked]="true"></ejs-checkbox>
      <ejs-checkbox name="Sport" value="Tennis" label="Tennis" [disabled]="true"></ejs-checkbox>
      <button type="submit">Submit</button>
    </form>`
})
export class AppComponent { }
```

#### Two-Way Binding with ngModel
```typescript
import { CheckBoxModule } from '@syncfusion/ej2-angular-buttons';
import { FormsModule } from '@angular/forms';
import { Component } from '@angular/core';

@Component({
  imports: [CheckBoxModule, FormsModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <ejs-checkbox [(ngModel)]="isChecked" label="Enable Feature"></ejs-checkbox>
    <p>State: {{ isChecked }}</p>`
})
export class AppComponent {
  public isChecked: boolean = false;
}
```

### Key Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `label` | string | `''` | Caption text next to checkbox |
| `checked` | boolean | `false` | Checked state |
| `indeterminate` | boolean | `false` | Indeterminate (partial) state |
| `disabled` | boolean | `false` | Disabled state |
| `labelPosition` | `'Before' \| 'After'` | `'After'` | Label placement |
| `cssClass` | string | `''` | Custom CSS class(es) |
| `name` | string | `''` | Form field name |
| `value` | string | `''` | Form field value |
| `enableRtl` | boolean | `false` | Right-to-left rendering |
| `enablePersistence` | boolean | `false` | Persist state across page reloads via browser `localStorage` ⚠️ Do not enable for sensitive or security-critical state |
| `htmlAttributes` | object | `{}` | Additional HTML attributes |

### Key Methods

| Method | Purpose |
|--------|---------|
| `click()` | Programmatically toggle the checkbox |
| `focusIn()` | Set focus to the checkbox element |
| `destroy()` | Destroy the component instance |

### Key Events

| Event | When it Fires | Key Args |
|-------|---------------|----------|
| `(change)` | Checked state changes | `checked`, `event` |
| `(created)` | Component initialized | — |

### Common Use Cases

1. **Multi-Select Form Fields** — Group checkboxes with `name`/`value` for form POST
2. **Select All / Indeterminate** — Parent checkbox with `[indeterminate]` based on child states
3. **Feature Toggles** — Single checkbox with `ngModel` two-way binding
4. **Accessible Forms** — WCAG-compliant checkboxes with keyboard and screen reader support
5. **Styled Checkboxes** — Round or color-variant checkboxes via `cssClass`

---

**For detailed implementation, start with [references/checkbox-getting-started.md](references/checkbox-getting-started.md)**

## OTP Input

A focused skill for implementing and customizing the Syncfusion Angular `ejs-otpinput` component — a multi-box input control designed for one-time password (OTP) and verification code entry flows.

**Package:** `@syncfusion/ej2-angular-inputs`  
**Selector:** `ejs-otpinput`  
**Module:** `OtpInputModule`

### Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/otp-input-getting-started.md)
- Installation via `ng add`
- Angular standalone vs module setup
- Basic component rendering
- CSS/SCSS theme imports
- autoFocus and pre-filled value

#### Input Types & Value
📄 **Read:** [references/input-types-and-value.md](references/otp-input-input-types-and-value.md)
- Number type (digits only, default)
- Text type (alphanumeric OTP)
- Password type (masked entry)
- textTransform (uppercase/lowercase/none)
- Setting and reading the value property

#### Appearance & Layout
📄 **Read:** [references/appearance.md](references/otp-input-appearance.md)
- Configuring OTP length
- Disabled state
- CSS classes (e-success, e-warning, e-error)
- Separator between fields
- Placeholder (single char or per-field string)
- Styling modes: outlined, filled, underlined

#### Events
📄 **Read:** [references/events.md](references/otp-input-events.md)
- `created` — component ready
- `focus` / `blur` — field focus events
- `input` — per-character change
- `valueChanged` — full OTP entered/changed
- Practical: validate and submit on OTP completion

#### Accessibility
📄 **Read:** [references/accessibility.md](references/otp-input-accessibility.md)
- WCAG 2.2 / Section 508 / ADA compliance table
- ARIA attributes (`role=group`, `aria-label`)
- `ariaLabels` property for per-field screen reader text
- `htmlAttributes` for extra HTML attributes
- Keyboard navigation shortcuts
- RTL support (`enableRtl`)

#### API Reference
📄 **Read:** [references/api.md](references/otp-input-api.md)
- All properties with types and defaults
- Methods: `focusIn`, `focusOut`, `destroy`
- All events with argument interfaces
- Enum types: OtpInputStyle, OtpInputType, TextTransform

---

### Quick Start

```typescript
// app.ts (Angular 19+ standalone)
import { Component } from '@angular/core';
import { OtpInputModule } from '@syncfusion/ej2-angular-inputs';

@Component({
  standalone: true,
  imports: [OtpInputModule],
  selector: 'app-root',
  template: `
    <div style="width: 350px;">
      <div ejs-otpinput
        id="otpinput"
        [length]="6"
        placeholder="x"
        (valueChanged)="onOtpComplete($event)">
      </div>
    </div>
  `
})
export class AppComponent {
  onOtpComplete(args: any) {
    console.log('OTP entered:', args.value);
  }
}
```

```css
/* styles.css */
@import '@syncfusion/ej2-base/styles/material3.css';
@import '@syncfusion/ej2-inputs/styles/material3.css';
```

---

### Common Patterns

#### Numeric PIN (4 digits)
```html
<div ejs-otpinput [length]="4" type="number"></div>
```

#### Masked password entry
```html
<div ejs-otpinput [length]="6" type="password"></div>
```

#### OTP with separator and filled style
```html
<div ejs-otpinput [length]="6" separator="-" stylingMode="filled"></div>
```

#### Auto-submit when OTP is complete
```html
<div ejs-otpinput [length]="6" (valueChanged)="submitOtp($event)"></div>
```

#### Error state after failed verification
```html
<div ejs-otpinput [length]="6" cssClass="e-error" [disabled]="false"></div>
```

#### Accessible OTP with ARIA labels
```html
<div ejs-otpinput
  [length]="4"
  [ariaLabels]="['Digit 1', 'Digit 2', 'Digit 3', 'Digit 4']">
</div>
```
## Implementing Syncfusion Angular Range Slider

The Range Slider is a versatile input component from Syncfusion EJ2 Angular that enables users to select single values or ranges from a continuous range. It supports multiple slider types, custom formatting, keyboard navigation, and advanced accessibility features.

## Component Overview

The Syncfusion Angular Range Slider (`ejs-slider`) provides:

- **Three slider types:** Default (single), MinRange (start to current), Range (dual handles)
- **Orientations:** Horizontal and vertical
- **Interactive elements:** Tooltips, increment/decrement buttons, tick marks, limits
- **Advanced features:** Custom formatting, keyboard shortcuts, RTL support
- **Full accessibility:** WCAG 2.2, Section 508, keyboard navigation, ARIA attributes
- **Form integration:** Reactive forms and template-driven forms support

## Slider Types at a Glance

| Type | Use Case | Handles | Visual |
|------|----------|---------|--------|
| **Default** | Single value selection | 1 | Plain slider with one thumb |
| **MinRange** | Start-to-current range | 1 | Shows selection from min to thumb |
| **Range** | Min/max range selection | 2 | Shows selection between two thumbs |

## Documentation & Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/range-slider-getting-started.md)
- Installation of `@syncfusion/ej2-angular-inputs`
- Package setup and imports
- CSS theme configuration
- First working example
- Understanding slider types overview

### Slider Types & Orientation
📄 **Read:** [references/slider-types-and-orientation.md](references/range-slider-types-and-orientation.md)
- When to use Default vs MinRange vs Range types
- Horizontal slider implementation (default)
- Vertical slider for space-saving layouts
- Practical implementation examples
- Type selection decision matrix

### Ticks, Marks & Limits
📄 **Read:** [references/ticks-and-limits.md](references/range-slider-ticks-and-limits.md)
- Adding tick marks to slider track
- Configuring tick labels and format
- Setting min/max limits and boundaries
- Step value configuration
- Custom tick positioning

### Tooltips & Buttons
📄 **Read:** [references/tooltips-and-buttons.md](references/range-slider-tooltips-and-buttons.md)
- Enable/disable tooltips
- Tooltip placement (Before, After, Above, Below)
- Increment/decrement buttons setup
- Button behavior in range sliders
- Keyboard focus management

### Formatting & Value Display
📄 **Read:** [references/formatting-and-values.md](references/range-slider-formatting-and-values.md)
- Format API for numeric, percentage, currency formatting
- Custom value formatting with events
- Internationalization support
- Using `renderingTicks` event for label transformation
- Using `tooltipChange` event for tooltip customization

### Styling & Customization
📄 **Read:** [references/styling-and-customization.md](references/range-slider-styling-and-customization.md)
- CSS classes for track, handle, buttons, ticks
- Customizing colors and dimensions
- Theme Studio integration
- RTL (right-to-left) language support
- Responsive design patterns

### Forms, Validation & Accessibility
📄 **Read:** [references/form-integration-and-accessibility.md](references/range-slider-form-integration-and-accessibility.md)
- Reactive forms with FormControl
- Template-driven forms with ngModel
- Form validation and error states
- WCAG 2.2 and Section 508 compliance
- Keyboard shortcuts (Arrow keys, Home, End, PageUp/PageDown)
- ARIA attributes and screen reader support

### Advanced Scenarios
📄 **Read:** [references/advanced-scenarios.md](references/range-slider-advanced-scenarios.md)
- Date range slider implementation
- Time range slider implementation
- Numeric range slider with formatting
- Reveal slider from hidden state
- Performance optimization tips
- Common pitfalls and troubleshooting

### API Reference
📄 **Read:** [references/api.md](references/range-slider-api.md)
- Complete property listing (`value`, `type`, `min`, `max`, `step`, `orientation`, `ticks`, `tooltip`, `limits`, `colorRange`, `enabled`, `readonly`, `showButtons`, `customValues`, `enableRtl`, `cssClass`, `width`, `enableAnimation`, `enablePersistence`)
- All events (`change`, `changed`, `created`, `renderingTicks`, `renderedTicks`, `tooltipChange`)
- Methods (`destroy`, `reposition`)
- Data models: `TicksDataModel`, `TooltipDataModel`, `LimitDataModel`, `ColorRangeDataModel`
- EJ1 → EJ2 migration table
- Verified code examples using only documented APIs

## Quick Start Example

Here's a minimal range slider in Angular 21+ (standalone):

```typescript
import { SliderModule } from '@syncfusion/ej2-angular-inputs';
import { Component } from '@angular/core';

@Component({
  imports: [SliderModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <div id="container">
      <h3>Range Slider</h3>
      <ejs-slider 
        id="range-slider"
        type="Range"
        [min]="0"
        [max]="100"
        [value]="[20, 80]"
        (change)="onSliderChange($event)">
      </ejs-slider>
      <p>Selected range: {{ selectedRange | json }}</p>
    </div>
  `,
  styles: [`
    #container {
      padding: 20px;
    }
    ejs-slider {
      width: 300px;
    }
  `]
})
export class App {
  selectedRange = [20, 80];

  onSliderChange(event: any) {
    this.selectedRange = event.value;
    console.log('Range changed:', this.selectedRange);
  }
}
```

**CSS Theme Setup** (in `styles.css`):
```css
@import 'node_modules/@syncfusion/ej2-base/styles/material3.css';
@import 'node_modules/@syncfusion/ej2-buttons/styles/material3.css';
@import 'node_modules/@syncfusion/ej2-popups/styles/material3.css';
@import 'node_modules/@syncfusion/ej2-angular-inputs/styles/material3.css';
```

## Common Patterns

### Pattern 1: Range Slider with Limits
```typescript
<ejs-slider 
  type="Range"
  [min]="0"
  [max]="100"
  [value]="[25, 75]"
  [limits]="{ enabled: true, minStart: 10, minEnd: 90 }">
</ejs-slider>
```

### Pattern 2: Slider with Ticks and Tooltip
```typescript
<ejs-slider 
  type="Default"
  [value]="50"
  [ticks]="{ placement: 'Before', largeStep: 10, smallStep: 5 }"
  [tooltip]="{ isVisible: true, placement: 'After' }">
</ejs-slider>
```

### Pattern 3: Vertical Slider
```typescript
<ejs-slider 
  type="Range"
  [value]="[30, 70]"
  orientation="Vertical"
  [style.height]="'300px'">
</ejs-slider>
```

### Pattern 4: Percentage Formatted Slider
```typescript
<ejs-slider 
  type="Range"
  [value]="[20, 80]"
  [ticks]="{ format: 'P0' }"
  [tooltip]="{ format: 'P0' }">
</ejs-slider>
```

## Key Props & Configuration

### Properties

| Prop | Type | Default | Purpose |
|------|------|---------|---------|
| `type` | string | `'Default'` | Slider type: `'Default'`, `'MinRange'`, `'Range'` |
| `value` | `number \| number[]` | `null` | Current value; use `number[]` for Range type |
| `min` | number | `0` | Minimum slider value |
| `max` | number | `100` | Maximum slider value |
| `step` | number | `1` | Increment/decrement amount per interaction |
| `orientation` | string | `'Horizontal'` | `'Horizontal'` or `'Vertical'` |
| `ticks` | `TicksDataModel` | — | Tick marks (placement, largeStep, smallStep, format) |
| `tooltip` | `TooltipDataModel` | — | Tooltip (isVisible, placement, showOn, format) |
| `limits` | `LimitDataModel` | — | Restrict thumb movement; must set `enabled: true` |
| `colorRange` | `ColorRangeDataModel[]` | — | Color segments applied to the track |
| `enabled` | boolean | `true` | Enable/disable slider |
| `readonly` | boolean | `false` | Show value but block user interaction |
| `showButtons` | boolean | `false` | Show increment/decrement buttons |
| `enableRtl` | boolean | `false` | Right-to-left rendering |
| `customValues` | `string[] \| number[]` | `null` | Discrete value array; overrides min/max/step |
| `cssClass` | string | `''` | Custom CSS class(es) on the slider host element |
| `width` | `number \| string` | `null` | Slider width (px or CSS string) |
| `enableAnimation` | boolean | `true` | Animate thumb movement |
| `enablePersistence` | boolean | `false` | Persist value in localStorage across reloads |
| `locale` | string | `''` | Locale override for value formatting |

### Events

| Event | Fires when | Args key properties |
|-------|-----------|---------------------|
| `(change)` | **During** drag (continuous) | `args.value`, `args.previousValue` |
| `(changed)` | **After** drag completes (once) | `args.value`, `args.previousValue` |
| `(created)` | Slider is initialized | — |
| `(renderingTicks)` | Each tick is rendering | `args.value`, assign `args.text` |
| `(renderedTicks)` | All ticks have rendered | `args.ticksWrapper` (DOM) |
| `(tooltipChange)` | Tooltip is about to show | `args.value`, assign `args.text` |

### Methods (via `@ViewChild`)

| Method | Returns | Purpose |
|--------|---------|---------|
| `reposition()` | `void` | Re-render after reveal from hidden state |
| `destroy()` | `void` | Remove component and detach event listeners |

## Common Use Cases

**Use Case 1: Price Filter**
- Type: Range
- Range: $0-$1000 with $100 steps
- Format: Currency (e.g., "$250")
- Tooltips: Visible with currency format

**Use Case 2: Date Range Selector**
- Type: Range
- Range: 0-365 (days)
- Format: Custom (date string from number)
- Ticks: Monthly intervals

**Use Case 3: Volume Control**
- Type: Default
- Range: 0-100
- Format: Percentage (0% - 100%)
- Orientation: Vertical

**Use Case 4: Form Input with Validation**
- Type: Range
- Integration: Reactive FormControl
- Validation: Min 20, Max 80
- Error display on invalid state

## Next Steps

1. **Start with Getting Started** - Set up the component and understand types
2. **Choose your slider type** - Read "Slider Types & Orientation"
3. **Configure features** - Add ticks, tooltips, buttons as needed
4. **Format values** - Implement percentage, currency, or custom formats
5. **Add accessibility** - Review keyboard nav and ARIA attributes
6. **Style & customize** - Apply theme and CSS customization
7. **Integrate with forms** - Bind to FormControl or ngModel with validation
8. **Handle edge cases** - Review advanced scenarios and troubleshooting

---

**For detailed implementation, start with [references/getting-started.md](references/range-slider-getting-started.md)**

## Syncfusion Angular TextArea Component

The Syncfusion Angular TextArea (`ejs-textarea`) provides a feature-rich multiline text input with floating labels, resize modes, adornments, form integration, and full accessibility support.

## Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/textarea-getting-started.md)
- Package installation (`@syncfusion/ej2-angular-inputs`)
- Standalone Angular 19+ component setup
- CSS/theme imports
- Basic TextArea rendering
- Getting and setting values (value property, ngModel, change event)

### Configuration
📄 **Read:** [references/configuration.md](references/textarea-configuration.md)
- Floating label (`floatLabelType`: Auto / Always / Never)
- Placeholder with localization (`locale` property)
- Rows and columns (`rows` / `cols` properties)
- Max length (`maxLength` property)
- Resize modes (`resizeMode`: Vertical / Horizontal / Both / None)
- Width customization (`width` property)

### Adornments
📄 **Read:** [references/adornments.md](references/textarea-adornments.md)
- Prepend/append custom templates (`prependTemplate` / `appendTemplate`)
- Adornment flow and orientation (`adornmentFlow` / `adornmentOrientation`)
- Common patterns: icons, formatting buttons, action buttons

### Events
📄 **Read:** [references/events.md](references/textarea-events.md)
- `created`, `destroyed` lifecycle events
- `input` — real-time value changes (`InputEventArgs`)
- `change` — value changed on blur (`ChangedEventArgs`)
- `focus` / `blur` — focus state events (`FocusInEventArgs` / `FocusOutEventArgs`)

### Style & Appearance
📄 **Read:** [references/style-appearance.md](references/textarea-style-appearance.md)
- Size variants (`e-small`, `e-bigger`)
- Filled and outline modes (`e-filled`, `e-outline`)
- Custom CSS via `cssClass` property
- Disabled (`enabled: false`) and read-only (`readonly: true`) states
- Show/hide clear button (`showClearButton`)
- Rounded corners, static clear button, RTL (`enableRtl`)
- Custom background, text, and border color overrides
- Floating label color for validation states

### Form Support
📄 **Read:** [references/form-support.md](references/textarea-form-support.md)
- HTML form integration
- FormValidator integration (required, minLength, maxLength, pattern)
- State persistence (`enablePersistence`)
- Custom HTML attributes (`htmlAttributes`)

### API Reference
📄 **Read:** [references/api.md](references/textarea-api.md)
- All properties, methods, and events with types and defaults
- Enum types: `FloatLabelType`, `Resize`, `AdornmentsDirection`

## Quick Start

```bash
ng add @syncfusion/ej2-angular-inputs
```

```typescript
import { Component } from '@angular/core';
import { TextAreaModule } from '@syncfusion/ej2-angular-inputs';

@Component({
  standalone: true,
  imports: [TextAreaModule],
  selector: 'app-root',
  template: `
    <ejs-textarea
      id="comments"
      placeholder="Enter your comments"
      [floatLabelType]="'Auto'"
      [rows]="4"
      [maxLength]="500">
    </ejs-textarea>
  `
})
export class AppComponent {}
```

```css
/* styles.css */
@import '../node_modules/@syncfusion/ej2-base/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-inputs/styles/material3.css';
```

## Common Patterns

### Two-Way Binding with ngModel
```typescript
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { TextAreaModule } from '@syncfusion/ej2-angular-inputs';

@Component({
  standalone: true,
  imports: [TextAreaModule, FormsModule],
  selector: 'app-root',
  template: `<ejs-textarea [(ngModel)]="comment" placeholder="Add comment"></ejs-textarea>`
})
export class AppComponent {
  comment: string = '';
}
```

### Disabled TextArea
```html
<ejs-textarea [enabled]="false" value="Read-only content"></ejs-textarea>
```

### Resize Control
```html
<!-- Vertical resize only -->
<ejs-textarea resizeMode="Vertical" [rows]="4"></ejs-textarea>

<!-- No resize -->
<ejs-textarea resizeMode="None" [rows]="4" [cols]="50"></ejs-textarea>
```

### With Floating Label
```html
<ejs-textarea floatLabelType="Auto" placeholder="Description"></ejs-textarea>
```
