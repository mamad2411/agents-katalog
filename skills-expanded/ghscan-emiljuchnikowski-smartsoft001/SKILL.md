---
name: angular-components-sidebar-navigation
description: Sidebar navigation component API with logo, expandable sections and profile footer using InjectionToken pattern.
user-invocable: false
---

# Sidebar Navigation Component

The `<smart-sidebar-navigation>` component renders a full-height application sidebar with optional logo, vertical navigation groups, expandable sub-sections, and a profile footer. It follows the Base + Standard + Wrapper pattern with an InjectionToken-based extension mechanism. The abstract `SidebarNavigationBaseComponent` defines the shared API — `options` (`ISidebarNavOptions`), `cssClass` (alias `class`), and outputs `itemClick` and `itemToggle`. `SidebarNavigationStandardComponent` is a barebones placeholder using native `<nav>`, `<ul>`, `<li>`, `<a>`, `<button>` elements and `<img>` for logo/avatar. `SidebarNavigationComponent` is the public wrapper that renders `SidebarNavigationStandardComponent` by default and accepts a custom replacement via `SIDEBAR_NAVIGATION_STANDARD_COMPONENT_TOKEN`.

## When to Use This Skill

- Developer wants to use or customize the application sidebar (with logo, expandable sub-menus, profile footer)
- Developer asks about `<smart-sidebar-navigation>`, `SidebarNavigationComponent`, `SidebarNavigationStandardComponent`, or `SidebarNavigationBaseComponent`

## Components

### SidebarNavigationComponent (`<smart-sidebar-navigation>`)

Main wrapper. Delegates to `SidebarNavigationStandardComponent` by default. When `SIDEBAR_NAVIGATION_STANDARD_COMPONENT_TOKEN` is provided, renders the injected component via `NgComponentOutlet`. Re-emits `itemClick` and `itemToggle`.

### SidebarNavigationStandardComponent (`<smart-sidebar-navigation-standard>`)

Barebones placeholder using native HTML. Renders an outer wrapper with `cssClass`, an optional `<div class="sidebar-logo">` (with `<img>` plus optional dark variant `<img>` and optional `<a>` link), a `<nav class="sidebar-navigation">` (with `aria-label` from `options.ariaLabel` or default `"Sidebar"`), and a `<ul>` of groups. Each group renders an optional `<div class="group-title">` and a `<ul>` of items.

Items render in three forms:

- `<a class="item-link">` (when `href` provided)
- `<button class="item-button">` (when no `href`, emits `itemClick`)
- `<button class="item-toggle">` followed by `<ul class="children">` (when `expandable === true`, emits `itemToggle`)

Items get `current` class and `aria-current="page"` when `item.current === true`. The toggle button manages local expanded state (initial value taken from `item.expanded`). Supports `iconTpl`, `initial` (e.g. team letter), `label`, and `badge`.

When `options.profile` is present, renders a `<li class="profile">` at the bottom containing `<a class="profile-link">` with `<img class="profile-avatar">`, optional `.sr-only` text, and `.profile-name`.

### SidebarNavigationBaseComponent (abstract)

Abstract base directive. Exposes:

- `options: InputSignal<ISidebarNavOptions | undefined>`
- `cssClass: InputSignal<string>` (alias `class`)
- `itemClick: OutputEmitterRef<ISidebarNavItemClick>`
- `itemToggle: OutputEmitterRef<ISidebarNavItemToggle>`
- protected `resolvedGroups: Signal<ISidebarNavGroup[]>` — normalizes `options.items` into a single-group structure alongside `options.groups`
- protected `expandedOverrides: WritableSignal<Record<string, boolean>>` — internal toggle state per item id
- protected `isExpanded(item)` / `toggleExpanded(item)` — helpers for managing expandable items

`ISidebarNavItemClick = { itemId: string }`.
`ISidebarNavItemToggle = { itemId: string; expanded: boolean }`.

## API

### Inputs

| Input     | Type                                           | Default | Description                                 |
| --------- | ---------------------------------------------- | ------- | ------------------------------------------- |
| `options` | `InputSignal<ISidebarNavOptions \| undefined>` | -       | Sidebar navigation configuration            |
| `class`   | `InputSignal<string>`                          | `''`    | External CSS classes (alias for `cssClass`) |

### Outputs

| Output       | Type                                      | Description                                             |
| ------------ | ----------------------------------------- | ------------------------------------------------------- |
| `itemClick`  | `OutputEmitterRef<ISidebarNavItemClick>`  | Emitted when a button-type nav item or child is clicked |
| `itemToggle` | `OutputEmitterRef<ISidebarNavItemToggle>` | Emitted when an expandable item is toggled              |

### ISidebarNavOptions

```typescript
type SmartSidebarNavLayout =
  | 'light'
  | 'dark'
  | 'with-expandable-sections'
  | 'with-secondary-navigation'
  | 'brand';

interface ISidebarNavOptions {
  layout?: SmartSidebarNavLayout;
  ariaLabel?: string;
  logo?: ISidebarNavLogo;
  items?: ISidebarNavItem[];
  groups?: ISidebarNavGroup[];
  profile?: ISidebarNavProfile;
}

interface ISidebarNavLogo {
  url?: string;
  urlDark?: string;
  alt?: string;
  href?: string;
  tpl?: TemplateRef<unknown>;
}

interface ISidebarNavGroup {
  id?: string;
  title?: string;
  items: ISidebarNavItem[];
}

interface ISidebarNavItem {
  id: string;
  label?: string;
  href?: string;
  current?: boolean;
  badge?: string | number;
  iconTpl?: TemplateRef<unknown>;
  initial?: string;
  expandable?: boolean;
  expanded?: boolean;
  children?: ISidebarNavItem[];
}

interface ISidebarNavProfile {
  name?: string;
  avatarUrl?: string;
  avatarAlt?: string;
  href?: string;
  srOnlyText?: string;
}
```

When both `items` and `groups` are provided, `items` is rendered first as a leading single-group section.

## SIDEBAR_NAVIGATION_STANDARD_COMPONENT_TOKEN

```typescript
import { SIDEBAR_NAVIGATION_STANDARD_COMPONENT_TOKEN } from '@smartsoft001/angular';

providers: [
  {
    provide: SIDEBAR_NAVIGATION_STANDARD_COMPONENT_TOKEN,
    useValue: MyCustomSidebarNavigationComponent,
  },
];
```

## Extending the Base Class

```typescript
import {
  ChangeDetectionStrategy,
  Component,
  input,
  ViewEncapsulation,
} from '@angular/core';

import { SidebarNavigationBaseComponent } from '@smartsoft001/angular';

@Component({
  selector: 'my-custom-sidebar-navigation',
  template: `…`,
  encapsulation: ViewEncapsulation.None,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class MyCustomSidebarNavigationComponent extends SidebarNavigationBaseComponent {
  // NgComponentOutlet passes 'cssClass' by canonical name, not the 'class' alias.
  override cssClass = input<string>('');
}
```

## Usage Examples

```html
<!-- Flat list with logo and profile -->
<smart-sidebar-navigation
  [options]="{
    logo: { url: '/logo.svg', alt: 'Acme' },
    items: [
      { id: 'dashboard', label: 'Dashboard', href: '/', current: true, badge: 5 },
      { id: 'team', label: 'Team', href: '/team' },
      { id: 'projects', label: 'Projects', href: '/projects', badge: 12 },
    ],
    profile: {
      name: 'Tom Cook',
      avatarUrl: '/avatar.jpg',
      href: '/me',
      srOnlyText: 'Your profile',
    },
  }"
/>

<!-- With teams group (initials) -->
<smart-sidebar-navigation
  [options]="{
    items: mainItems,
    groups: [
      {
        title: 'Your teams',
        items: [
          { id: 'h', label: 'Heroicons', initial: 'H', href: '/h' },
          { id: 't', label: 'Tailwind Labs', initial: 'T', href: '/t' },
        ],
      },
    ],
  }"
  (itemClick)="onItem($event)"
/>

<!-- With expandable sections -->
<smart-sidebar-navigation
  [options]="{
    items: [
      { id: 'dashboard', label: 'Dashboard', href: '/' },
      {
        id: 'teams',
        label: 'Teams',
        expandable: true,
        children: [
          { id: 'eng', label: 'Engineering', href: '/eng' },
          { id: 'hr', label: 'Human Resources', href: '/hr' },
        ],
      },
    ],
  }"
  (itemToggle)="onToggle($event)"
/>
```

## File Locations

- Wrapper: `packages/shared/angular/src/lib/components/sidebar-navigation/sidebar-navigation.component.ts`
- Standard: `packages/shared/angular/src/lib/components/sidebar-navigation/standard/standard.component.ts`
- Base class: `packages/shared/angular/src/lib/components/sidebar-navigation/base/base.component.ts`
- Token: `packages/shared/angular/src/lib/shared.inectors.ts` (`SIDEBAR_NAVIGATION_STANDARD_COMPONENT_TOKEN`)
- Interfaces: `packages/shared/angular/src/lib/models/interfaces.ts` (`ISidebarNavOptions`, `ISidebarNavGroup`, `ISidebarNavItem`, `ISidebarNavLogo`, `ISidebarNavProfile`, `SmartSidebarNavLayout`)
