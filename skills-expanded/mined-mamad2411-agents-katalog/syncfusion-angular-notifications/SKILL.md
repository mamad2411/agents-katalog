---
name: syncfusion-angular-notifications
description: Comprehensive guide for implementing Syncfusion Angular notification components including Message, Skeleton and Toast. Use this when displaying informational, success, warning, or error alerts with severity levels, customizing message variants (Text, Outlined, Filled), handling close events, or showing content skeletons with shimmer/pulse animations during data loading. Covers MessageModule, SkeletonModule, accessibility, RTL, and custom CSS in Angular applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Notifications"
---

# Implementing Syncfusion Angular Notifications

---

## Message

The Syncfusion Angular Message component (`ejs-message`) displays contextual messages with severity-based icons and colors to communicate importance to the user. It supports multiple **severity types**, **visual variants**, **close icon**, **custom templates**, **content alignment**, **CSS customization**, and full **accessibility compliance**.

**Package:** `@syncfusion/ej2-angular-notifications`  
**Module:** `MessageModule`  
**Selector:** `ejs-message`

---

> 📋 All files linked under `references/` are read-only documentation and comply with the same security policy as this skill.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/message-getting-started.md](references/message-getting-started.md)
- Installing `@syncfusion/ej2-angular-notifications` via `ng add`
- CSS/SCSS theme imports (Material3)
- `MessageModule` import in standalone component
- Minimal `ejs-message` template setup
- Running the application

#### Severity Types
📄 **Read:** [references/message-severities.md](references/message-severities.md)
- `severity` property with all five values: Normal, Success, Info, Warning, Error
- Default severity (Normal)
- When to choose each severity type
- Code example with all severities

#### Visual Variants
📄 **Read:** [references/message-variants.md](references/message-variants.md)
- `variant` property: Text, Outlined, Filled
- Default variant (Text)
- Combining variant with severity
- Full example showing all combinations

#### Icons and Close Icon
📄 **Read:** [references/message-icons.md](references/message-icons.md)
- `showIcon` — hide/show the severity icon
- `showCloseIcon` — add a close icon to dismiss messages
- `(closed)` event — react when user closes a message
- Restoring visibility with `visible` property
- Custom icon using `cssClass`

#### Customization and Templates
📄 **Read:** [references/message-customization.md](references/message-customization.md)
- Content alignment: left (default), center (`e-content-center`), right (`e-content-right`)
- Rounded and square border styles via `cssClass`
- CSS-only message rendering (no script reference)
- Predefined CSS classes for manual DOM structure
- Rich HTML template via `<ng-template #content>`

#### Accessibility
📄 **Read:** [references/message-accessibility.md](references/message-accessibility.md)
- WCAG 2.2 / Section 508 compliance
- WAI-ARIA attributes (`role=alert`, `aria-label`)
- Keyboard interaction (Tab, Enter/Space for close icon)
- RTL support via `enableRtl`
- Screen reader behavior

#### API Reference
📄 **Read:** [references/message-api.md](references/message-api.md)
- All properties: `content`, `cssClass`, `enablePersistence`, `enableRtl`, `locale`, `severity`, `showCloseIcon`, `showIcon`, `variant`, `visible`
- Methods: `destroy()`, `getPersistData()`
- Events: `closed`, `created`, `destroyed`

---

### Quick Start

```bash
ng add @syncfusion/ej2-angular-notifications
```

```css
/* styles.css – added automatically by ng add */
/* NOTE: These are consumer-side stylesheet references only; no packages are installed or executed by this skill. */
@import '../node_modules/@syncfusion/ej2-base/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-angular-notifications/styles/message/material3.css';
```

```typescript
import { MessageModule } from '@syncfusion/ej2-angular-notifications';
import { Component } from '@angular/core';

@Component({
  imports: [MessageModule],
  standalone: true,
  selector: 'app-root',
  template: '<ejs-message content="Please read the comments carefully"></ejs-message>'
})
export class AppComponent { }
```

---

### Common Patterns

#### Message with Severity
```typescript
import { MessageModule } from '@syncfusion/ej2-angular-notifications';
import { Component } from '@angular/core';

@Component({
  imports: [MessageModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <ejs-message content="Editing is restricted"></ejs-message>
    <ejs-message content="Please read the comments carefully" severity="Info"></ejs-message>
    <ejs-message content="Your message has been sent successfully" severity="Success"></ejs-message>
    <ejs-message content="There was a problem with your network connection" severity="Warning"></ejs-message>
    <ejs-message content="A problem occurred while submitting your data" severity="Error"></ejs-message>
  `
})
export class AppComponent { }
```

#### Dismissable Message with Close Icon
```typescript
import { MessageModule } from '@syncfusion/ej2-angular-notifications';
import { Component, ViewChild } from '@angular/core';
import { MessageComponent } from '@syncfusion/ej2-angular-notifications';

@Component({
  imports: [MessageModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <ejs-message #msg severity="Warning" [showCloseIcon]="true" (closed)="onClosed()">
      There was a problem with your network connection
    </ejs-message>
    <button *ngIf="isClosed" (click)="reopen()">Show again</button>
  `
})
export class AppComponent {
  @ViewChild('msg') msg!: MessageComponent;
  isClosed = false;

  onClosed(): void {
    this.isClosed = true;
  }

  reopen(): void {
    this.msg.visible = true;
    this.isClosed = false;
  }
}
```

#### Filled Variant with Severity
```typescript
import { MessageModule } from '@syncfusion/ej2-angular-notifications';
import { Component } from '@angular/core';

@Component({
  imports: [MessageModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <ejs-message content="Your message has been sent successfully"
      severity="Success" variant="Filled">
    </ejs-message>
  `
})
export class AppComponent { }
```

---

### Key Props at a Glance

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `content` | `string \| object` | `null` | Text, HTML, or template content to display |
| `severity` | `string` | `'Normal'` | Severity type: Normal, Success, Info, Warning, Error |
| `variant` | `string` | `'Text'` | Visual style: Text, Outlined, Filled |
| `showIcon` | `boolean` | `true` | Show/hide the severity icon |
| `showCloseIcon` | `boolean` | `false` | Show/hide the close icon |
| `visible` | `boolean` | `true` | Show or hide the entire message |
| `cssClass` | `string` | `''` | Custom CSS class(es) appended to root element |
| `enableRtl` | `boolean` | `false` | Right-to-left rendering |
| `enablePersistence` | `boolean` | `false` | Persist component state across page reloads |
| `locale` | `string` | `''` | Override global culture/localization |

---

## Skeleton

The Skeleton component provides a visual placeholder for content that is loading or yet to be rendered. It helps improve perceived performance by showing users what content is coming, reducing cognitive load during loading states.

**Package:** `@syncfusion/ej2-angular-notifications`  
**Module:** `SkeletonModule`  
**Selector:** `ejs-skeleton`

---

### When to Use This Skill

- **Loading placeholders**: Display skeleton layouts while fetching data from APIs
- **Shimmer animations**: Add Wave, Pulse, or Fade effects to loading states
- **Multiple shapes**: Build complex layouts using Circle, Square, Rectangle, and Text shapes
- **Accessibility**: Ensure loading states are accessible with ARIA attributes and screen reader support
- **Custom styling**: Apply custom CSS classes and themes to match your design system
- **Conditional rendering**: Show/hide skeletons based on data loading states
- **RTL support**: Implement right-to-left layouts with the Skeleton component

---

> 📋 All files linked under `references/` are read-only documentation and comply with the same security policy as this skill.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/skeleton-getting-started.md](references/skeleton-getting-started.md)
- Installation and package setup
- Dependencies and CSS imports
- Basic skeleton implementation
- Angular 19+ standalone architecture
- Running your application with Skeleton

#### Shapes and Layout Design
📄 **Read:** [references/skeleton-shapes.md](references/skeleton-shapes.md)
- Circle shapes for avatars and profile pictures
- Square shapes for thumbnails and icons
- Rectangle shapes for images and cards
- Text shapes for paragraphs and content
- Combining shapes to build complete layouts
- Responsive sizing and responsive design

#### Shimmer Effects and Animation
📄 **Read:** [references/skeleton-shimmer-effects.md](references/skeleton-shimmer-effects.md)
- Wave effect (default animation)
- Pulse effect (fade in/out animation)
- Fade effect (opacity change animation)
- Changing effects dynamically
- Performance considerations for multiple skeletons

#### Styling and Customization
📄 **Read:** [references/skeleton-styles-customization.md](references/skeleton-styles-customization.md)
- Using cssClass for custom styling
- Customizing wave/background colors
- Setting width and height dimensions
- Controlling visibility with the visible property
- CSS variables for theming
- Theme Studio integration

#### Accessibility Features
📄 **Read:** [references/skeleton-accessibility.md](references/skeleton-accessibility.md)
- WCAG 2.2 and Section 508 compliance
- Screen reader support and live regions
- WAI-ARIA attributes (role, aria-label, aria-live, aria-busy)
- Right-to-Left (RTL) support
- Keyboard navigation and focus management
- Color contrast requirements
- Accessibility validation tools

#### API Reference
📄 **Read:** [references/skeleton-api.md](references/skeleton-api.md)
- All properties with descriptions and defaults
- Methods and lifecycle management
- Event handling patterns
- Type definitions (SkeletonType, ShimmerEffect)
- Property usage examples
- Complete API documentation

---

### Quick Start

```typescript
import { Component } from '@angular/core';
import { SkeletonModule } from '@syncfusion/ej2-angular-notifications';

@Component({
  imports: [SkeletonModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <div>
      <h2>Loading User Profile...</h2>
      <!-- Avatar skeleton -->
      <ejs-skeleton shape="Circle" width="60px"></ejs-skeleton>
      
      <!-- Name and description skeletons -->
      <ejs-skeleton width="30%" height="15px"></ejs-skeleton>
      <ejs-skeleton width="50%" height="15px"></ejs-skeleton>
      
      <!-- Content skeleton -->
      <ejs-skeleton shape="Rectangle" width="100%" height="150px"></ejs-skeleton>
    </div>
  `
})
export class AppComponent {}
```

---

### Common Patterns

#### Pattern 1: Card Loading Skeleton
Display a skeleton layout matching a card component during data loading:

```typescript
@Component({
  selector: 'app-card-skeleton',
  template: `
    <div class='card-skeleton'>
      <!-- Avatar -->
      <div class='avatar-section'>
        <ejs-skeleton shape="Circle" width="50px"></ejs-skeleton>
      </div>
      <!-- Content -->
      <div class='content-section'>
        <ejs-skeleton width="60%" height="12px"></ejs-skeleton>
        <ejs-skeleton width="40%" height="12px"></ejs-skeleton>
        <ejs-skeleton width="100%" height="80px"></ejs-skeleton>
      </div>
      <!-- Actions -->
      <div class='action-section'>
        <ejs-skeleton shape="Rectangle" width="30%" height="36px"></ejs-skeleton>
      </div>
    </div>
  `
})
export class CardSkeletonComponent {}
```

#### Pattern 2: List Loading with Pulse Effect
Show multiple skeleton rows with a pulsing shimmer effect:

```typescript
@Component({
  selector: 'app-list-skeleton',
  template: `
    <div class='list-skeleton'>
      <div class='list-item' *ngFor="let item of [1,2,3,4,5]">
        <ejs-skeleton shape="Circle" width="40px" shimmerEffect="Pulse"></ejs-skeleton>
        <div class='item-content'>
          <ejs-skeleton width="50%" height="14px" shimmerEffect="Pulse"></ejs-skeleton>
          <ejs-skeleton width="30%" height="12px" shimmerEffect="Pulse"></ejs-skeleton>
        </div>
      </div>
    </div>
  `
})
export class ListSkeletonComponent {}
```

#### Pattern 3: Conditional Skeleton Rendering
Show skeleton while loading, hide when content is ready:

```typescript
@Component({
  selector: 'app-conditional-skeleton',
  template: `
    <!-- Show skeleton while loading -->
    <div *ngIf="isLoading">
      <ejs-skeleton shape="Rectangle" width="100%" height="200px" 
                    shimmerEffect="Wave"></ejs-skeleton>
    </div>
    <!-- Show content when loaded -->
    <div *ngIf="!isLoading">
      <img [src]="imageUrl" alt="Loaded content">
    </div>
  `
})
export class ConditionalSkeletonComponent {
  isLoading = true;
  imageUrl = '';
  
  ngOnInit() {
    // Simulate loading
    setTimeout(() => {
      this.isLoading = false;
      this.imageUrl = 'assets/image.jpg';
    }, 2000);
  }
}
```

---

### Key Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `shape` | SkeletonType | 'Text' | Defines skeleton shape: Text, Circle, Square, Rectangle |
| `shimmerEffect` | ShimmerEffect | 'Wave' | Animation effect: Wave, Pulse, Fade |
| `width` | string \| number | '' | Skeleton width (required for Circle/Square) |
| `height` | string \| number | '' | Skeleton height |
| `visible` | boolean | true | Controls skeleton visibility |
| `cssClass` | string | '' | Custom CSS class for styling |
| `label` | string | 'Loading…' | Aria-label for accessibility |
| `enableRtl` | boolean | false | Enable right-to-left layout |
| `enablePersistence` | boolean | false | Persist state between page reloads |

### Common Use Cases

1. **Data Grid Loading**: Show skeleton rows while grid data is loading from server
2. **Image Gallery**: Display placeholder rectangles while images download
3. **Feed/Timeline**: Show multiple skeleton cards while loading feed items
4. **Profile Page**: Combine shapes to preview profile layout
5. **List with Avatars**: Use Circle + Text shapes for user lists
6. **Modal Content**: Display skeleton inside dialogs during async operations
7. **Product Cards**: Build skeleton matching product card layout
8. **Dashboard**: Create skeleton layouts for dashboard widgets

## Toast

The Syncfusion Angular Toast (`ejs-toast`) is a non-blocking notification component that displays brief messages at a defined position on the screen. Toasts auto-dismiss after a configurable timeout and support rich content via templates, action buttons, icons, and progress bars.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/toast-getting-started.md)
- Prerequisites and dependencies
- Installing `@syncfusion/ej2-angular-notifications`
- Adding CSS/theme imports
- Basic toast setup (standalone + NgModule)
- Showing a toast on component creation
- Running the application

#### Configuration
📄 **Read:** [references/configuration.md](references/toast-configuration.md)
- Title and content properties
- Custom target container
- Show/hide close button (`showCloseButton`)
- Progress bar (`showProgressBar`, `progressDirection`)
- Newest on top (`newestOnTop`)
- Width and height customization
- Icon using `icon` property
- `cssClass` for semantic types (e-success, e-info, e-warning, e-danger)
- `enableHtmlSanitizer`, `enableRtl`, `locale`

#### Position and Animation
📄 **Read:** [references/position-and-animation.md](references/toast-position-and-animation.md)
- Predefined X/Y positions (Left, Center, Right / Top, Bottom)
- Custom pixel/percentage positions
- Multiple toasts in different positions
- Animation configuration (`show`/`hide` effects, duration, easing)
- Default animation (FadeIn/FadeOut)

#### Templates and Action Buttons
📄 **Read:** [references/template-and-buttons.md](references/toast-template-and-buttons.md)
- HTML string and element ID templates
- Angular `ng-template` with `#template`, `#title`, `#content`
- Dynamic templates via `show()` method arguments
- Action buttons with `buttons` property and click handlers
- `ButtonModelPropsModel` configuration

#### Timeout and Events
📄 **Read:** [references/timeout-and-events.md](references/toast-timeout-and-events.md)
- `timeOut` property (default 5000ms)
- `extendedTimeout` on hover (default 1000ms)
- Static toast (timeOut: 0)
- All events: `created`, `open`, `close`, `click`, `beforeOpen`, `beforeClose`, `beforeSanitizeHtml`, `destroyed`
- Event argument types and cancellation patterns

#### Toast Utility Service
📄 **Read:** [references/toast-utility.md](references/toast-utility.md)
- `ToastUtility.show()` for minimal-code toasts
- Predefined types: Information, Success, Error, Warning
- Full `ToastModel` argument usage with events and positioning
- When to use utility vs component approach

#### How-To Guides
📄 **Read:** [references/how-to.md](references/toast-how-to.md)
- Close toast on click/tap
- Prevent duplicate toasts
- Restrict maximum visible toasts
- Add dynamic templates
- Render Angular `ng-template` in toast
- Show multiple toasts in various positions
- Customize progress bar theme and sizing
- Play audio before toast opens
- Prevent toast close with mobile swipe
- Show different types of toast

#### API Reference
📄 **Read:** [references/api.md](references/toast-api.md)
- All properties with types and defaults
- Methods: `show()`, `hide()`, `destroy()`
- All events with argument type links
- `ToastAnimationSettingsModel`, `ToastPositionModel`, `ButtonModelPropsModel`

---

### Quick Start

```typescript
// app.ts (Angular standalone)
import { Component, ViewChild } from '@angular/core';
import { ToastModule } from '@syncfusion/ej2-angular-notifications';

@Component({
  imports: [ToastModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <ejs-toast #toast (created)="onCreated()">
      <ng-template #title><div>Notification</div></ng-template>
      <ng-template #content><div>Your action was successful.</div></ng-template>
    </ejs-toast>
    <button (click)="toast.show()">Show Toast</button>
  `
})
export class App {
  @ViewChild('toast') toast: any;
  onCreated() { this.toast.show(); }
}
```

**Install:**
```bash
ng add @syncfusion/ej2-angular-notifications
```

**CSS (styles.css):**
```css
@import '@syncfusion/ej2-base/styles/material3.css';
@import '@syncfusion/ej2-buttons/styles/material3.css';
@import '@syncfusion/ej2-popups/styles/material3.css';
@import '@syncfusion/ej2-angular-notifications/styles/material3.css';
```

---

### Common Patterns

#### Success/Error/Warning/Info Toast
```typescript
// Using cssClass for semantic coloring
toastObj.show({ content: 'File saved!', cssClass: 'e-toast-success' });
toastObj.show({ content: 'Upload failed.', cssClass: 'e-toast-danger' });
toastObj.show({ content: 'Low disk space.', cssClass: 'e-toast-warning' });
toastObj.show({ content: 'Update available.', cssClass: 'e-toast-info' });
```

#### Quick Toast via ToastUtility
```typescript
import { ToastUtility } from '@syncfusion/ej2-angular-notifications';
ToastUtility.show('Operation successful', 'Success', 3000);
```

#### Toast with Progress Bar + Close Button
```html
<ejs-toast [showProgressBar]="true" [showCloseButton]="true" [timeOut]="4000">
</ejs-toast>
```

#### Toast Positioned Bottom-Center
```typescript
public position = { X: 'Center', Y: 'Bottom' };
```
```html
<ejs-toast [position]="position"></ejs-toast>
```

#### Action Buttons
```typescript
public buttons = [
  { model: { content: 'Undo' }, click: () => this.onUndo() },
  { model: { content: 'Dismiss' } }
];
```

#### Static Toast (no auto-dismiss)
```html
<ejs-toast [timeOut]="0" [showCloseButton]="true"></ejs-toast>
```

---

### Key Properties

| Property | Type | Default | Purpose |
|---|---|---|---|
| `title` | any | null | Toast heading text or HTML |
| `content` | any | null | Toast body text or HTML |
| `timeOut` | number | 5000 | Auto-dismiss after ms (0 = static) |
| `position` | ToastPositionModel | {X:'Left',Y:'Top'} | Screen position |
| `showCloseButton` | boolean | false | Show × dismiss button |
| `showProgressBar` | boolean | false | Show countdown progress bar |
| `progressDirection` | string | 'Rtl' | Progress bar direction (Ltr/Rtl) |
| `newestOnTop` | boolean | true | Insert new toasts before old ones |
| `cssClass` | string | null | Custom CSS classes |
| `icon` | string | null | CSS class for top-left icon |
| `target` | string/Element | null | Container element (default: body) |
| `width` | string/number | '300' | Toast width |
| `height` | string/number | 'auto' | Toast height |
| `buttons` | ButtonModelPropsModel[] | [{}] | Action buttons |
| `animation` | ToastAnimationSettingsModel | FadeIn/FadeOut | Show/hide animation |
| `extendedTimeout` | number | 1000 | Extra time on hover |
| `enableRtl` | boolean | false | Right-to-left rendering |

---

### Common Use Cases

| Scenario | Approach |
|---|---|
| Simple one-liner notification | Use `ToastUtility.show()` |
| Typed notification (success/error) | `cssClass: 'e-toast-success'` or `ToastUtility.show(..., 'Success', ...)` |
| Notification requiring user action | Add `buttons` array with click handlers |
| Persistent alert until dismissed | Set `timeOut: 0` + `showCloseButton: true` |
| Multiple simultaneous toasts | Use separate `ejs-toast` instances with different `target` containers |
| Notification in custom container | Set `target` property to element reference or selector |
| Prevent duplicate messages | Cancel in `beforeOpen` event if same title already visible |
| Mobile-friendly (no swipe dismiss) | Cancel `beforeClose` when `args.type === 'swipe'` |
| Progress indicator | `showProgressBar: true`, customize via `beforeOpen` event |
