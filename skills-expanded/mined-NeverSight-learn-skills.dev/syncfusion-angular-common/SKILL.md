---
name: syncfusion-angular-common
description: Common utilities and features for Syncfusion Angular components. Use this skill when the user needs to implement animations, drag-and-drop, state persistence, RTL support, localization, globalization, security, templates, and advanced features for Syncfusion Angular components.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Common Features"
---

# Common Features in Syncfusion Angular Components

Syncfusion Angular components include comprehensive common utilities and features that enhance user experience, ensure cross-cultural support, and provide foundational capabilities across all components. This skill covers installation setup, animations, globalization, state management, and security considerations for building robust Angular applications.

## Table of Contents

- [Navigation Guide](#documentation-and-navigation-guide)
- [Quick Start](#quick-start)
- [Common Features](#common-features)

## Documentation and Navigation Guide

### Getting Started & Framework Setup
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Angular CLI installation and project creation
- Standalone components vs. module-based configuration
- npm package installation with `ng add` command
- ASP.NET Core and ASP.NET MVC integration
- Component initialization
- Quick start examples

### Globalization
📄 **Read:** [references/globalization.md](references/globalization.md)
- Right-to-left (RTL) support for Arabic, Hebrew, Persian languages
- Localization (l10n) for multi-language support
- Internationalization (i18n) with CLDR data
- Number and currency formatting
- Date and time formatting

### Advanced Features & Utilities
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Animation effects (FadeIn, ZoomOut, SlideUp, etc.)
- Animation timing (duration, delay, global settings)
- Drag-and-drop interactions (Draggable, Droppable)
- Template customization and optimization
- State persistence with enablePersistence
- Security best practices and HTML sanitization

## Quick Start

### Install Syncfusion Angular Package

```bash
ng add @syncfusion/ej2-angular-grids
```

### Import Styles

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-calendars/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-dropdowns/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-angular-grids/styles/tailwind3.css";
```

### Register License Key

```typescript
// src/main.ts
import { registerLicense } from '@syncfusion/ej2-base';

// Call this before initializing any Syncfusion components
registerLicense('Your license key here');
```

### Basic Component Setup

```typescript
import { Component } from '@angular/core';
import { GridModule, PageService } from '@syncfusion/ej2-angular-grids';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [GridModule],
  providers: [PageService],
  template: `
    <ejs-grid [dataSource]="data" [allowPaging]="true">
      <e-columns>
        <e-column field="OrderID" width="100"></e-column>
        <e-column field="CustomerID" width="100"></e-column>
        <e-column field="Freight" width="100" format="C2"></e-column>
      </e-columns>
    </ejs-grid>
  `
})
export class AppComponent {
  data = [
    { OrderID: 10248, CustomerID: 'VINET', Freight: 32.38 },
    { OrderID: 10249, CustomerID: 'TOMSP', Freight: 11.61 }
  ];
}
```

## Common Features

### Enable State Persistence

```typescript
<ejs-grid 
  id="persistGrid"
  [dataSource]="data" 
  [enablePersistence]="true"
>
  <!-- Component content -->
</ejs-grid>
```

### Enable RTL Support

```typescript
import { enableRtl } from '@syncfusion/ej2-base';

// Global RTL enablement
enableRtl(true);

// OR per-component
<ejs-grid [dataSource]="data" enableRtl="true"></ejs-grid>
```

### Add Animation Effects

```typescript
import { Component, ViewChild } from '@angular/core';
import { Animation } from '@syncfusion/ej2-base';

@Component({
  template: `<div #element class="box"></div>`
})
export class AnimationComponent {
  @ViewChild('element') element!: any;

  ngAfterViewInit() {
    const animation = new Animation({ duration: 5000, delay: 2000 });
    animation.animate(this.element.nativeElement, { name: 'FadeOut' });
  }
}
```

### Implement Drag-and-Drop

```typescript
import { Component, ViewChild } from '@angular/core';
import { Draggable, Droppable } from '@syncfusion/ej2-base';

@Component({
  template: `
    <div #draggable id="draggable">Drag me</div>
    <div #droppable id="droppable">Drop here</div>
  `
})
export class DragDropComponent {
  @ViewChild('draggable') draggable!: any;
  @ViewChild('droppable') droppable!: any;

  ngAfterViewInit() {
    new Draggable(this.draggable.nativeElement, { clone: false });
    
    new Droppable(this.droppable.nativeElement, {
      drop: (e) => {
        console.log('Dropped!', e.droppedElement);
      }
    });
  }
}
```




