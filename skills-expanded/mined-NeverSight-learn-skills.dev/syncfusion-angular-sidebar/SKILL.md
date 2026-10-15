---
name: syncfusion-angular-sidebar
description: Guide for implementing Syncfusion Angular Sidebar component for navigation, collapsible menus, and dynamic content. Use this when creating sidebars with multiple positioning options, animations, gestures, docking, responsive behavior, TreeView/ListView content, and backdrop overlays. This skill covers sidebar navigation, toggle menus, responsive navigation panels, collapsible layouts, and expanding/collapsing navigation elements.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation"
---

# Implementing Syncfusion Angular Sidebar Component

The **Sidebar** is an expandable and collapsible navigation component that acts as a side container for primary or secondary content alongside main content. It supports flexible show/hide behavior, multiple positioning modes (left, right, top, bottom), various expand types (Push, Slide, Over, Auto), docking for compact states, touch gestures, animations, responsive behavior, and rich content including TreeView and ListView.

## When to Use This Skill

- Implementing collapsible navigation menus or sidebars
- Creating responsive navigation that adapts to screen size
- Building expandable panels with icon-only docked states
- Adding gesture-based sidebar toggle on touch devices
- Positioning sidebars in various directions (left, right, top, bottom)
- Implementing backdrop overlays to focus on sidebar content
- Creating multi-level navigation with TreeView or ListView
- Managing sidebar visibility with auto-close behavior
- Building toggle buttons with show(), hide(), toggle() methods
- Applying animations and RTL support to sidebars

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Angular CLI setup and project initialization (Recommended)
- Installing Syncfusion packages (Ivy and ngcc versions)
- Importing modules and CSS styles
- Creating basic sidebar component
- ViewChild setup and initialization

### SystemJS Setup (Alternative)
📄 **Read:** [references/systemjs-setup.md](references/systemjs-setup.md)
- SystemJS configuration and installation
- systemjs.config.js setup with Syncfusion mappings
- UMD bundle configuration
- Creating Sidebar with SystemJS
- Development server and running the application
- SystemJS vs Angular CLI comparison

### Sidebar Positioning and Behavior
📄 **Read:** [references/sidebar-positioning.md](references/sidebar-positioning.md)
- Sidebar types: Push, Slide, Over, Auto
- Positioning: Left, Right, Top, Bottom
- Fixed positioning for static sidebars
- Docking with enableDock and dockSize properties
- Multiple sidebars on same page
- dataBind() for dynamic property updates

### Sidebar Interactions and Control
📄 **Read:** [references/sidebar-interactions.md](references/sidebar-interactions.md)
- Control methods: show(), hide(), toggle()
- Auto-close with mediaQuery for responsive behavior
- closeOnDocumentClick for external click handling
- Backdrop overlay with showBackdrop
- Touch gesture support with enableGestures
- Open and close event handling

### Sidebar Content and Components
📄 **Read:** [references/sidebar-content.md](references/sidebar-content.md)
- ListView integration for list-based content
- TreeView integration for hierarchical menus
- Custom HTML content and menu items
- Target element configuration
- Content structure and layout patterns

### Animations and Styling
📄 **Read:** [references/animations-and-styles.md](references/animations-and-styles.md)
- Animation control with animate property
- Animation types and variations
- CSS theming with Material3 and other themes
- RTL (right-to-left) support with enableRtl
- Responsive design patterns
- CRG (Custom Resource Generator) usage

### Advanced Features and Patterns
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Persistence with enablePersistence
- RTL implementation details
- Accessibility features
- Hiding sidebars with routing
- Performance optimization
- Edge cases and troubleshooting

## Quick Start Example

```typescript
import { SidebarModule } from '@syncfusion/ej2-angular-navigations';
import { Component, ViewChild } from '@angular/core';
import { SidebarComponent } from '@syncfusion/ej2-angular-navigations';

@Component({
  imports: [SidebarModule],
  standalone: true,
  selector: 'app-root',
  template: `<ejs-sidebar #sidebar id="default-sidebar">
              <div class="title">Sidebar Content</div>
            </ejs-sidebar>
            <div>
              <div class="title">Main Content</div>
              <button (click)="toggleSidebar()">Toggle Sidebar</button>
            </div>`,
  styles: [`
    .title { padding: 20px; font-weight: bold; }
  `]
})
export class AppComponent {
  @ViewChild('sidebar') sidebar?: SidebarComponent;

  toggleSidebar() {
    this.sidebar?.toggle();
  }
}
```

## Target Property Behavior

The sidebar's `target` property controls which element is affected when the sidebar expands/collapses. There are **two distinct modes**:

### Implicit Targeting (Recommended - Default Behavior)

**No `target` property is specified.** The sidebar automatically targets the **next sibling `<div>`** element:

```typescript
<ejs-sidebar id="sidebar" type="Push"></ejs-sidebar>
<div>  <!-- Automatically becomes target - no wrapper needed -->
  <div class="content">Main Content</div>
</div>
```

✅ **Advantages:**
- Simple and clean code
- No wrapper element needed
- Perfect for straightforward layouts
- **Use this for most applications**

---

### Explicit Targeting (Advanced - When You Need Control)

Use the **`[target]="'#selector'"`** property to explicitly specify which element to affect:

```typescript
<ejs-sidebar [target]="'#content-area'" type="Push"></ejs-sidebar>
<div id="content-area">              <!-- Explicit target -->
  <div>                              <!-- ⚠️ REQUIRED: Inner wrapper -->
    <div class="content">Main Content</div>
  </div>
</div>
```

⚠️ **IMPORTANT:** When using explicit `target`, you **MUST include an inner wrapper `<div>`** inside the target container for CSS transforms to work correctly.

**Use explicit targeting when:**
- You want to exclude certain elements (header, footer) from sidebar effects
- You have complex layouts with multiple sections
- You need fine-grained control over transformation

---

### When to Use Each Mode

| Mode | When to Use | Complexity | Wrapper Needed |
|------|-------------|-----------|-----------------|
| **Implicit** (No target) | Default for most layouts | Simple | ❌ No |
| **Explicit** (With target) | Complex layouts, selective targeting | Advanced | ✅ Yes (inner) |

**See detailed examples in [references/sidebar-positioning.md](references/sidebar-positioning.md#target-property---when-and-how-to-use)**

---

## API Properties Reference

The Sidebar component exposes the following properties to control its behavior and appearance:

### animate
**Type:** `boolean` | **Default:** `true`

Enable or disable animation transitions when expanding or collapsing the sidebar.

```typescript
// Example: Disable animations for instant toggle
<ejs-sidebar [animate]="false"></ejs-sidebar>

// Example: Enable animations (default)
<ejs-sidebar [animate]="true"></ejs-sidebar>
```

---

### closeOnDocumentClick
**Type:** `boolean` | **Default:** `false`

Specifies whether the sidebar closes when clicking outside of it on the main content area.

```typescript
// Example: Auto-close sidebar on document click
<ejs-sidebar [closeOnDocumentClick]="true"></ejs-sidebar>

// Example: In component
this.closeOnClick = true;
```

---

### dockSize
**Type:** `string | number` | **Default:** `'auto'`

Specifies the width of the sidebar when in dock state (collapsed but still visible with icons).

```typescript
// Example: Set dock size to 72 pixels
<ejs-sidebar [dockSize]="'72px'" [enableDock]="true"></ejs-sidebar>

// Example: Set as number
<ejs-sidebar [dockSize]="72" [enableDock]="true"></ejs-sidebar>

// Example: In component
public dockSize: string = '72px';
```

---

### enableDock
**Type:** `boolean` | **Default:** `false`

Enables the docking state where sidebar shows icons only and expands on hover or click.

```typescript
// Example: Enable docking for icon-only sidebar
<ejs-sidebar [enableDock]="true" [dockSize]="'72px'">
  <div class="sidebar-item" title="Home">
    <i class="e-icons e-home"></i>
  </div>
  <div class="sidebar-item" title="Settings">
    <i class="e-icons e-settings"></i>
  </div>
</ejs-sidebar>

// Example: In component
public enableDock = true;
public dockSize = '72px';
```

---

### enableGestures
**Type:** `boolean` | **Default:** `true`

Enables touch gestures (swipe) to open/close the sidebar on touch devices.

```typescript
// Example: Enable gesture support (default)
<ejs-sidebar [enableGestures]="true"></ejs-sidebar>

// Example: Disable gestures for specific use cases
<ejs-sidebar [enableGestures]="false"></ejs-sidebar>
```

---

### enablePersistence
**Type:** `boolean` | **Default:** `false`

Enable persisting the sidebar state (open/closed, position, type) between page reloads using localStorage.

```typescript
// Example: Enable persistence to remember sidebar state
<ejs-sidebar [enablePersistence]="true"></ejs-sidebar>

// Persisted states:
// 1. Position (Left/Right)
// 2. Type (Push/Slide/Over/Auto)
// 3. Open/Closed state
```

---

### enableRtl
**Type:** `boolean` | **Default:** `false`

Specifies right-to-left layout for the sidebar, useful for RTL languages like Arabic and Hebrew.

```typescript
// Example: Enable RTL layout
<ejs-sidebar [enableRtl]="true"></ejs-sidebar>

// Example: Dynamically set based on language
public isRtl = document.documentElement.lang === 'ar';
<ejs-sidebar [enableRtl]="isRtl"></ejs-sidebar>
```

---

### isOpen
**Type:** `boolean` | **Default:** `false`

Gets or sets whether the sidebar is in open (expanded) or closed (collapsed) state.

```typescript
// Example: Initially open sidebar
<ejs-sidebar [isOpen]="true"></ejs-sidebar>

// Example: Initially closed (default)
<ejs-sidebar [isOpen]="false"></ejs-sidebar>

// Example: Toggle state from component
@ViewChild('sidebar') sidebar?: SidebarComponent;

toggleOpen() {
  this.sidebar!.isOpen = !this.sidebar!.isOpen;
}

// Note: When sidebar type is 'Auto', this property is ignored on mobile devices
```

---

### mediaQuery
**Type:** `string | MediaQueryList` | **Default:** `null`

Specifies a media query string that automatically opens the sidebar when the query matches.

```typescript
// Example: Open sidebar on screens wider than 600px
<ejs-sidebar [mediaQuery]="'(min-width: 600px)'"></ejs-sidebar>

// Example: Using MediaQueryList object
public mediaQuery = window.matchMedia('(min-width: 768px)');
<ejs-sidebar [mediaQuery]="mediaQuery"></ejs-sidebar>

// Example: Common breakpoints
// Mobile: '(max-width: 600px)'
// Tablet: '(min-width: 601px) and (max-width: 1024px)'
// Desktop: '(min-width: 1025px)'
```

---

### position
**Type:** `SidebarPosition` | **Default:** `'Left'`

Specifies the position of the sidebar: `'Left'` or `'Right'`.

```typescript
// Example: Position sidebar on the left (default)
<ejs-sidebar [position]="'Left'"></ejs-sidebar>

// Example: Position sidebar on the right
<ejs-sidebar [position]="'Right'"></ejs-sidebar>

// Example: Set position dynamically
public sidebarPosition: SidebarPosition = 'Left';
<ejs-sidebar [position]="sidebarPosition"></ejs-sidebar>
```

Available values:
- `'Left'` - Sidebar appears on the left side
- `'Right'` - Sidebar appears on the right side

---

### showBackdrop
**Type:** `boolean` | **Default:** `false`

Specifies whether to display an overlay backdrop on the main content when sidebar is open.

```typescript
// Example: Show backdrop overlay
<ejs-sidebar [showBackdrop]="true"></ejs-sidebar>

// Example: Backdrop with auto-close on click
<ejs-sidebar [showBackdrop]="true" [closeOnDocumentClick]="true"></ejs-sidebar>

// Example: Combine with other properties
<ejs-sidebar 
  [showBackdrop]="true" 
  [closeOnDocumentClick]="true"
  [type]="'Over'">
</ejs-sidebar>
```

---

### target
**Type:** `HTMLElement | string` | **Default:** `null`

Specifies which element the sidebar will affect (push/slide/transform). See [Target Property Behavior](#target-property-behavior) section above.

⚠️ **Important:** When using explicit target with transform types (Push/Slide), include an inner wrapper `<div>` inside the target container.

```typescript
// ✅ Example: Explicit targeting with ID selector (CORRECT - with wrapper)
<ejs-sidebar [target]="'#content-area'" [type]="'Push'"></ejs-sidebar>
<div id="content-area">
  <div>  <!-- Required wrapper for transforms -->
    <div>Content here</div>
  </div>
</div>

// ✅ Example: Explicit targeting with CSS class (CORRECT - with wrapper)
<ejs-sidebar [target]="'.main-content'" [type]="'Push'"></ejs-sidebar>
<div class="main-content">
  <div>  <!-- Required wrapper for transforms -->
    <div>Content here</div>
  </div>
</div>

// ✅ Example: Pass HTMLElement directly
@ViewChild('targetDiv') targetElement?: ElementRef;
<ejs-sidebar [target]="targetElement?.nativeElement" [type]="'Push'"></ejs-sidebar>
<div #targetDiv>
  <div>  <!-- Required wrapper for transforms -->
    <div>Content here</div>
  </div>
</div>
```

---

### type
**Type:** `SidebarType` | **Default:** `'Auto'`

Specifies how the sidebar expands: `'Push'`, `'Slide'`, `'Over'`, or `'Auto'`.

```typescript
// Example: Push type - sidebar pushes content aside
<ejs-sidebar [type]="'Push'"></ejs-sidebar>

// Example: Slide type - sidebar slides over and translates content
<ejs-sidebar [type]="'Slide'"></ejs-sidebar>

// Example: Over type - sidebar floats over content
<ejs-sidebar [type]="'Over'"></ejs-sidebar>

// Example: Auto type - Over on mobile, Push on desktop
<ejs-sidebar [type]="'Auto'"></ejs-sidebar>
```

Available values:
- `'Push'` - Sidebar pushes main content to the side
- `'Slide'` - Sidebar slides and translates main content
- `'Over'` - Sidebar floats over main content
- `'Auto'` - Responsive (Over on mobile, Push on desktop)

---

### width
**Type:** `string | number` | **Default:** `'280px'`

Specifies the width of the sidebar in its expanded state. Can be set in pixels, percentages, or em units.

```typescript
// Example: Set width in pixels
<ejs-sidebar [width]="'300px'"></ejs-sidebar>

// Example: Set width as number (treated as pixels)
<ejs-sidebar [width]="300"></ejs-sidebar>

// Example: Set width in percentage
<ejs-sidebar [width]="'50%'"></ejs-sidebar>

// Example: Set width in em units
<ejs-sidebar [width]="'20em'"></ejs-sidebar>

// Example: Responsive width
public sidebarWidth = window.innerWidth < 768 ? '100%' : '300px';
<ejs-sidebar [width]="sidebarWidth"></ejs-sidebar>
```

---

### zIndex
**Type:** `string | number` | **Default:** `1000`

Specifies the z-index of the sidebar. Only applicable when sidebar type is `'Over'` or `'Auto'` on mobile.

```typescript
// Example: Set z-index for layering
<ejs-sidebar [zIndex]="1000"></ejs-sidebar>

// Example: High z-index to appear above other modals
<ejs-sidebar [zIndex]="9999" [type]="'Over'"></ejs-sidebar>
```

---

## API Methods Reference

The Sidebar component provides the following methods for programmatic control:

### show(e?: Event)

**Description:** Shows the sidebar if it's currently closed.

**Parameters:**
- `e` (optional) - The event triggering the show action (MouseEvent | Event)

**Returns:** `void`

**Example:**

```typescript
import { Component, ViewChild } from '@angular/core';
import { SidebarComponent } from '@syncfusion/ej2-angular-navigations';

@Component({
  selector: 'app-root',
  template: `
    <ejs-sidebar #sidebar></ejs-sidebar>
    <button (click)="openSidebar()">Open Sidebar</button>
  `
})
export class AppComponent {
  @ViewChild('sidebar') sidebar?: SidebarComponent;

  // Method 1: Show without event
  openSidebar() {
    this.sidebar?.show();
  }

  // Method 2: Show with event
  openSidebarWithEvent(event: MouseEvent) {
    this.sidebar?.show(event);
  }
}
```

---

### hide(e?: Event)

**Description:** Hides the sidebar if it's currently open.

**Parameters:**
- `e` (optional) - The event triggering the hide action (MouseEvent | Event)

**Returns:** `void`

**Example:**

```typescript
@Component({
  selector: 'app-root',
  template: `
    <ejs-sidebar #sidebar></ejs-sidebar>
    <button (click)="closeSidebar()">Close Sidebar</button>
  `
})
export class AppComponent {
  @ViewChild('sidebar') sidebar?: SidebarComponent;

  // Method 1: Hide without event
  closeSidebar() {
    this.sidebar?.hide();
  }

  // Method 2: Hide with click event
  closeSidebarOnClick(event: MouseEvent) {
    this.sidebar?.hide(event);
  }
}
```

---

### toggle()

**Description:** Toggles the sidebar between open and closed states.

**Returns:** `void`

**Example:**

```typescript
@Component({
  selector: 'app-root',
  template: `
    <ejs-sidebar #sidebar id="sidebar" [isOpen]="false">
      <button (click)="toggleMenu()">Close</button>
    </ejs-sidebar>
    <button (click)="toggleMenu()">☰ Menu</button>
  `
})
export class AppComponent {
  @ViewChild('sidebar') sidebar?: SidebarComponent;

  toggleMenu() {
    this.sidebar?.toggle();
  }
}
```

---

### destroy()

**Description:** Removes the sidebar control from the DOM and detaches all event handlers and attributes.

**Returns:** `void`

**Example:**

```typescript
@Component({
  selector: 'app-root',
  template: `
    <ejs-sidebar #sidebar></ejs-sidebar>
    <button (click)="destroySidebar()">Destroy Sidebar</button>
  `
})
export class AppComponent {
  @ViewChild('sidebar') sidebar?: SidebarComponent;

  // Destroy and remove the sidebar
  destroySidebar() {
    this.sidebar?.destroy();
  }
}
```

---

### dataBind()

**Description:** Applies pending property changes to the sidebar component. Use this method after dynamically changing sidebar properties to ensure changes are rendered immediately.

**Returns:** `void`

**Example:**

```typescript
@Component({
  selector: 'app-root',
  template: `
    <ejs-sidebar 
      #sidebar 
      [width]="sidebarWidth"
      [type]="sidebarType">
    </ejs-sidebar>
    <button (click)="changeSidebarProperties()">Change Properties</button>
  `
})
export class AppComponent {
  @ViewChild('sidebar') sidebar?: SidebarComponent;

  sidebarWidth = '280px';
  sidebarType = 'Push';

  // Change sidebar properties dynamically
  changeSidebarProperties() {
    // Modify properties
    this.sidebarWidth = '350px';
    this.sidebarType = 'Slide';
    
    // Apply changes to the component
    (this.sidebar as SidebarComponent).dataBind();
  }

  // Another example: Toggle width on docked state
  updateDockSize() {
    (this.sidebar as SidebarComponent).dockSize = '100px';
    (this.sidebar as SidebarComponent).dataBind();
  }
}
```

---

## API Events Reference

The Sidebar component emits the following events during its lifecycle and interactions:

### open

**Description:** Triggers when the sidebar is opened.

**Event Arguments:** [`EventArgs`](../../sidebar-api/eventArgs.md)

**EventArgs Properties:**
- `cancel` (boolean) - Set to true to prevent the open action
- `element` (HTMLElement) - The sidebar DOM element
- `event` (MouseEvent | Event) - The original browser event
- `isInteracted` (boolean) - Whether the user interacted to trigger the open
- `model` (SidebarModel) - The sidebar model instance

**Example:**

```typescript
@Component({
  selector: 'app-root',
  template: `
    <ejs-sidebar 
      #sidebar
      (open)="onOpen($event)">
    </ejs-sidebar>
  `
})
export class AppComponent {
  @ViewChild('sidebar') sidebar?: SidebarComponent;

  onOpen(event: any) {
    console.log('Sidebar opened');
    console.log('Event:', event.event);
    console.log('Element:', event.element);
    console.log('Is Interacted:', event.isInteracted);
    
    // Prevent opening if needed
    // event.cancel = true;
  }
}
```

---

### close

**Description:** Triggers when the sidebar is closed.

**Event Arguments:** [`EventArgs`](../../sidebar-api/eventArgs.md)

**EventArgs Properties:**
- `cancel` (boolean) - Set to true to prevent the close action
- `element` (HTMLElement) - The sidebar DOM element
- `event` (MouseEvent | Event) - The original browser event
- `isInteracted` (boolean) - Whether the user interacted to trigger the close
- `model` (SidebarModel) - The sidebar model instance

**Example:**

```typescript
@Component({
  selector: 'app-root',
  template: `
    <ejs-sidebar 
      #sidebar
      (close)="onClose($event)">
    </ejs-sidebar>
  `
})
export class AppComponent {
  @ViewChild('sidebar') sidebar?: SidebarComponent;

  onClose(event: any) {
    console.log('Sidebar closed');
    console.log('Is Interacted:', event.isInteracted);
    
    // Prevent closing if needed
    // event.cancel = true;
  }
}
```

---

### change

**Description:** Triggers when the sidebar state changes between open and closed.

**Event Arguments:** [`ChangeEventArgs`](../../sidebar-api/changeEventArgs.md)

**ChangeEventArgs Properties:**
- `element` (HTMLElement) - The sidebar DOM element
- `name` (string) - Event name: 'change'

**Example:**

```typescript
@Component({
  selector: 'app-root',
  template: `
    <ejs-sidebar 
      #sidebar
      (change)="onChange($event)">
    </ejs-sidebar>
  `
})
export class AppComponent {
  @ViewChild('sidebar') sidebar?: SidebarComponent;

  onChange(event: any) {
    console.log('Sidebar state changed');
    console.log('Event name:', event.name);
    console.log('Element:', event.element);
  }
}
```

---

### created

**Description:** Triggers when the sidebar component is created and initialized.

**Event Arguments:** `Object`

**Example:**

```typescript
@Component({
  selector: 'app-root',
  template: `
    <ejs-sidebar 
      #sidebar
      (created)="onCreated($event)"
      style="visibility: hidden">
    </ejs-sidebar>
  `
})
export class AppComponent {
  @ViewChild('sidebar') sidebar?: SidebarComponent;

  onCreated(event: any) {
    console.log('Sidebar created and initialized');
    // Make sidebar visible after creation
    (this.sidebar as SidebarComponent).element.style.visibility = '';
  }
}
```

---

### destroyed

**Description:** Triggers when the sidebar component is destroyed.

**Event Arguments:** `Object`

**Example:**

```typescript
@Component({
  selector: 'app-root',
  template: `
    <ejs-sidebar 
      #sidebar
      (destroyed)="onDestroyed($event)">
    </ejs-sidebar>
  `
})
export class AppComponent {
  @ViewChild('sidebar') sidebar?: SidebarComponent;

  onDestroyed(event: any) {
    console.log('Sidebar destroyed');
    // Cleanup any additional resources
  }
}
```

---

## Common Patterns

### Pattern 1: Toggle Button Sidebar
Open/close sidebar with button clicks using the toggle() method. Perfect for mobile navigation and responsive layouts.

```typescript
// In component.ts
toggleSidebar() {
  this.sidebar?.toggle();
}

// In template
<button (click)="toggleSidebar()">Toggle</button>
```

### Pattern 2: Responsive Auto-Close
Automatically collapse sidebar on small screens using mediaQuery property.

```typescript
public mediaQuery = window.matchMedia('(max-width: 600px)');
// In template
<ejs-sidebar [mediaQuery]="mediaQuery" [isOpen]="true">
```

### Pattern 3: Docked Navigation with Icons
Create a compact icon-only docked state that expands on click.

```typescript
public enableDock = true;
public dockSize = '72px';
// In template
<ejs-sidebar [enableDock]="enableDock" [dockSize]="dockSize">
```

### Pattern 4: Backdrop for Focus
Use backdrop to overlay main content and focus on sidebar.

```typescript
// In template
<ejs-sidebar [showBackdrop]="true" [closeOnDocumentClick]="true">
```

## Key Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `type` | Push \| Slide \| Over \| Auto | Auto | Expand behavior and content interaction |
| `position` | Left \| Right | Left | Sidebar direction and positioning |
| `width` | string \| number | 280px | Sidebar width in expanded state |
| `dockSize` | string \| number | auto | Width when docked/collapsed |
| `enableDock` | boolean | false | Enable compact docked state |
| `isOpen` | boolean | false | Initial open/closed state |
| `animate` | boolean | true | Enable expand/collapse animations |
| `showBackdrop` | boolean | false | Display overlay on main content |
| `closeOnDocumentClick` | boolean | false | Close when clicking outside |
| `enableGestures` | boolean | true | Enable touch swipe gestures |
| `mediaQuery` | string \| MediaQueryList | null | Auto-close on screen size match |
| `enableRtl` | boolean | false | Right-to-left layout support |
| `enablePersistence` | boolean | false | Persist state between page reloads |

## Common Use Cases

1. **App Navigation Menu** - Top-level navigation with toggle button
2. **Mobile Menu** - Responsive sidebar that auto-closes on small screens
3. **Settings Panel** - Docked icon-based panel expanding to show options
4. **Hierarchical Navigation** - TreeView-based nested menu structure
5. **Content Sidebar** - Always-visible sidebar alongside main content
6. **Mail Application** - Folder tree with email list (ListView + TreeView)
7. **Dashboard Layout** - Collapsible widget panel
8. **RTL Application** - Right-to-left sidebar for Arabic/Hebrew interfaces

## See Also

- [Syncfusion Angular Sidebar Documentation](https://ej2.syncfusion.com/angular/documentation/api/sidebar)
- [Sidebar API Reference](./api/overview.md)
- [Component Events and Properties](./sidebar-api/sidebarModel.md)
