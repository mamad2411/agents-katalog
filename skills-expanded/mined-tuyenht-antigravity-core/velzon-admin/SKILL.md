---
name: Velzon Admin Dashboard
description: "Kiến trúc xây dựng Admin Dashboard hoàn cấp theo tiêu chuẩn Velzon chuyên nghiệp nhất."
---

# Velzon Admin Dashboard Skill

## Overview

Velzon is a premium admin & dashboard template (v4.4.1) providing **200+ pre-built pages** across 8 dashboard types, 12+ app modules, and comprehensive UI components. This skill encodes the architectural patterns, component conventions, and layout system for building production admin dashboards.

**Based on:** Velzon Admin & Dashboard Template v4.4.1 (All 11 variants)

## When to Use

Auto-activate when the request involves:
- Building admin panels or dashboards
- Creating management screens (CRUD, lists, details, forms)
- Keywords: "admin", "dashboard", "admin panel", "login", "authentication", "bảng điều khiển", "quản lý", "management", "đăng nhập"
- Data tables, stat widgets, chart dashboards

## 🚨 Bundled Assets — MANDATORY

> [!CAUTION]
> **This skill ships with pre-built image assets.** You MUST use them instead of generating new images.
> **NEVER use `generate_image` for logos, favicons, or error pages when bundled files exist.**

### Asset Location

All bundled assets are at: `.agent/skills/velzon-admin/assets/images/`

### Available Assets (USE THESE)

| File | Purpose | When to Use |
|------|---------|-------------|
| `logo-dark.png` | Dark logo (dark text, for light backgrounds) | Sidebar header, print headers |
| `logo-light.png` | Light logo (white text, for dark/gradient backgrounds) | Auth pages, dark sidebar |
| `logo-sm.png` | Small square icon logo | Collapsed sidebar, favicon fallback |
| `favicon.ico` | Browser tab icon | `<link rel="icon">` in HTML head |
| `404-error.png` | 404 Not Found illustration | Error 404 page |
| `error500.png` | 500 Server Error illustration | Error 500 page |
| `error.svg` | Generic error SVG | Fallback error pages |
| `cover-pattern.png` | Profile cover pattern | User profile page |
| `modal-bg.png` | Modal background | Modals with branded backgrounds |
| `chat-bg-pattern.png` | Chat background pattern | Chat/messaging pages |
| `horizontal.png` | Horizontal layout preview | Layout customizer/RightSidebar |
| `vertical.png` | Vertical layout preview | Layout customizer/RightSidebar |
| `user-dummy-img.jpg` | Default user avatar | Users without uploaded avatar |
| `multi-user.jpg` | Multi-user group avatar | Team/group displays |
| `new.png` | New item icon | New document/item actions |

### Copy Pattern

When building a project, copy bundled assets to the project's asset directory:
```bash
# PowerShell
Copy-Item -Recurse ".agent/skills/velzon-admin/assets/images/*" -Destination "src/assets/images/" -Force

# Bash
cp -r .agent/skills/velzon-admin/assets/images/* src/assets/images/
```

### Rules
1. **ALWAYS check** `assets/images/` for existing files BEFORE considering image generation
2. **COPY** bundled assets into the target project's public/assets directory
3. **ONLY use `generate_image`** for images NOT available in the bundle (e.g., custom product photos, user-specific content)
4. **Auth pages**: Use `logo-light.png` (visible on gradient backgrounds)
5. **Sidebar**: Use `logo-dark.png` (full) + `logo-sm.png` (collapsed)

---

## 🚨 CSS Foundation — MANDATORY

> [!WARNING]
> **Without Velzon's compiled CSS, ALL layout will break.** Import these in EVERY project.

### Required CSS Files (import order matters)

| # | File | Source | Purpose |
|---|------|--------|---------|
| 0 | `layout.js` (⚠️) | `.agent/skills/velzon-admin/assets/js/` | **FOUC prevention — MUST load BEFORE CSS** |
| 1 | `bootstrap.min.css` | `.agent/skills/velzon-admin/assets/css/` | Core Bootstrap 5 |
| 2 | `icons.min.css` | Same directory | Icon fonts (BoxIcons, Remix, MDI, Line Awesome) |
| 3 | `app.min.css` | Same directory | Velzon layout engine (sidebar, header, footer) — **OVERRIDE Bootstrap** |
| 4 | `custom.min.css` | Same directory | Velzon custom component overrides |
| 5 | `fonts.css` | Same directory | @font-face for Inter + CJK web fonts |

### Copy Pattern
```bash
# Copy CSS from Antigravity-Core skill assets to project
mkdir -p public/assets/css
cp .agent/skills/velzon-admin/assets/css/bootstrap.min.css public/assets/css/
cp .agent/skills/velzon-admin/assets/css/icons.min.css public/assets/css/
cp .agent/skills/velzon-admin/assets/css/app.min.css public/assets/css/
cp .agent/skills/velzon-admin/assets/css/custom.min.css public/assets/css/
```

### Import in Root Layout (Next.js)
```tsx
// app/layout.tsx — import CSS BEFORE globals.css
import '/public/assets/css/bootstrap.min.css';
import '/public/assets/css/icons.min.css';
import '/public/assets/css/app.min.css';
import '/public/assets/css/custom.min.css';
import './globals.css'; // LTR overrides + Tailwind conflicts
```

### Rules
1. **NEVER skip** CSS imports — inline styles are NOT acceptable for layout components
2. **globals.css** is ONLY for LTR overrides and Tailwind conflict resolution
3. **Icons** (`bx`, `ri`, `mdi`, `la`) come from `icons.min.css` — if icons show □, this file is missing

---

## 🚨 Fidelity Mandate — EXACT MATCH

> [!IMPORTANT]
> **Pixel-Perfect & Behavior-Perfect Requirement:** Whenever generating a component, page, or layout for Velzon Admin, you MUST ensure that all UI/UX details, including animations, CSS classes, HTML structures, plugin configurations, and interactive scripts EXACTLY MATCH the original Velzon Admin template.

### Guidelines for Exact Matching:
1. **Interactive Utilities:** For tooltips, modals, offcanvas, dropdowns, always use the exact Bootstrap 5 / Reactstrap / Inertia integration code patterns provided in `reference/component-patterns.md`. 
2. **Micro-animations & Effects:** Pay close attention to CSS classes that trigger animations (e.g., `card-animate`, `waves-effect`, `avatar-title`). Do not drop these classes.
3. **Data Visualizations & Widgets:** When rendering charts (ApexCharts), stat widgets, or tables, the layout grids, spacing utilities (`p-`, `m-`, `gap-`), colors (`--vz-*`), and initialization logic must mirror the original Velzon reference.
4. **Sidebars, Menus & Layouts:** The core layout structures (Vertical, Horizontal, TwoColumn, etc.), sidebar components, and menu configurations MUST mirror the exact Velzon-Admin visual presentation, behaviors (like hover, active states, auto-close), and nesting logic.
5. **Target Language Neutrality:** Whether outputting for React, Next.js, EJS, Blade, or PHP, the rendered DOM structure and classes MUST be identical to the canonical Velzon HTML.

---

## Technology Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| React | 19.1 | UI framework |
| TypeScript | 5.8 | Type safety |
| Bootstrap | 5.3.7 | CSS framework |
| Reactstrap | 9.2.3 | Bootstrap React components |
| Redux Toolkit | 2.8 | State management |
| TanStack Table | 8.21 | Data tables with sorting/filtering |
| ApexCharts | 4.7 | Primary chart library |
| Formik + Yup | 2.4 / 1.6 | Form management + validation |
| react-countup | 6.5 | Animated number widgets |
| Flatpickr | 4.0 | Date/time picker |
| Remix Icons | - | Primary icon set (ri-*) |

## Core Architecture

### Page Structure Pattern

Every admin page follows this structure:

```tsx
const MyPage = () => {
  document.title = "Page Title | App Name";
  
  return (
    <React.Fragment>
      <div className="page-content">
        <Container fluid>
          <BreadCrumb title="Page Title" pageTitle="Category" />
          <Row>
            {/* Page content here */}
          </Row>
        </Container>
      </div>
    </React.Fragment>
  );
};
```

### Layout System

Three layout types, managed via `data-layout` attribute:
- **Vertical** (default): Left sidebar + main content
- **Horizontal**: Top navigation bar + main content
- **TwoColumn**: Icon sidebar + expanded menu + main content
- ~~Semi Box~~: **REMOVED** from customizer per spec

Layout wrapper: `#layout-wrapper` > Header + Sidebar + `.main-content` > `.page-content`

### Layout Persistence (★ sessionStorage)

> [!CAUTION]
> Velzon HTML gốc dùng **sessionStorage** (CONFIRM: `layout.js` source code).
> - **14 data-\* attributes** được persist: data-layout, data-sidebar-size, data-bs-theme,
>   data-layout-width, data-sidebar, data-sidebar-image, data-layout-direction,
>   data-layout-position, data-layout-style, data-topbar, data-preloader,
>   data-body-image, data-theme, data-theme-colors
> - Trong Next.js/React: dùng Redux store + `changeHTMLAttribute()` (xem `source/react-ts/slices/layouts/`)
> - Trong Non-React (HTML/PHP/Laravel): `app.js` tự xử lý sessionStorage
> - **KHÔNG dùng localStorage** cho layout state (chỉ dùng cho i18n `I18N_LANGUAGE`)
> - Xem chi tiết: `admin-shell-template.md` § Dual Strategy + § Theme Customizer (LOCKED values + Pruning spec)

### CSS Variable System

All Velzon-specific variables use `--vz-*` prefix:
```css
--vz-primary, --vz-secondary, --vz-success, --vz-info, --vz-warning, --vz-danger
--vz-card-bg, --vz-body-color, --vz-body-bg
--vz-border-color, --vz-light, --vz-dark
```

Bootstrap utilities enhanced with `-subtle` suffix for backgrounds:
- `bg-primary-subtle`, `bg-success-subtle`, `bg-warning-subtle`, etc.

### Component Imports

Always import from Reactstrap (NOT raw Bootstrap classes for interactive components):
```tsx
import { Container, Row, Col, Card, CardBody, CardHeader, Button,
         Modal, ModalBody, ModalHeader, ModalFooter,
         Input, Label, Form, FormFeedback,
         Table, Badge, UncontrolledDropdown, DropdownToggle,
         DropdownMenu, DropdownItem, Nav, NavItem, NavLink,
         TabContent, TabPane } from "reactstrap";
```

## Multi-Stack Support

Velzon supports 11 variants. Choose based on your project:

| Variant | When to Use | Reference File |
|---------|-------------|---------------|
| **React-TS** | Standalone React SPA (default) | Core skill files |
| **React+Inertia** | Laravel + Inertia.js + React (Baoson Platform) | [inertia-bridge.md](reference/inertia-bridge.md) |
| **Next-TS** | Next.js App Router (BSWeb SaaS) | [nextjs-patterns.md](reference/nextjs-patterns.md) |
| **Node.js** | Express.js + EJS (server-side rendering) | [nodejs-patterns.md](reference/nodejs-patterns.md) |
| **Ajax** | jQuery AJAX single-page shell | [ajax-patterns.md](reference/ajax-patterns.md) |
| **ASP.NET Core** | ASP.NET Core 8 + Razor (.cshtml) | [aspnet-mvc-patterns.md](reference/aspnet-mvc-patterns.md) |
| **ASP.NET MVC** | ASP.NET MVC (.NET Framework) + Razor | [aspnet-mvc-patterns.md](reference/aspnet-mvc-patterns.md) |
| **Laravel** | Laravel + Blade (server-side) | [html-php-patterns.md](reference/html-php-patterns.md) |
| **HTML** | Static HTML + Bootstrap + Gulp | [html-php-patterns.md](reference/html-php-patterns.md) |
| **PHP** | PHP with includes | [html-php-patterns.md](reference/html-php-patterns.md) |
| **React** | React JS (no TypeScript) | Same as React-TS minus types |

### Stack Detection
- `composer.json` + `inertiajs` → use **React+Inertia** patterns
- `next.config.js` → use **Next-TS** patterns
- `app.js` + `express` + `.ejs` views → use **Node.js** patterns
- `.csproj` + `Program.cs` + `.cshtml` views → use **ASP.NET Core** patterns
- `.csproj` + `Global.asax.cs` + `.cshtml` views → use **ASP.NET MVC** patterns
- `index.html` + AJAX nav + HTML fragment pages → use **Ajax** patterns
- `composer.json` + Blade views → use **Laravel** patterns
- `gulpfile.js` + HTML → use **HTML** patterns
- Otherwise → default **React-TS** patterns

## Velzon Shell — Source Files (2-Layer Reference)

> [!IMPORTANT]
> `source/` contains the **CANONICAL SHELL** (layout frame) of Velzon Admin, organized in 2 layers.
> This ensures **every project** generated by `/create-admin` has an **identical visual shell** regardless of framework.

### Directory Structure

```
source/
├── html-canonical/              ← Layer 1: Canonical DOM (for ALL non-React frameworks)
│   ├── sidebar.html             ← 78KB: Full sidebar DOM (logo switching, menu nesting, categories, badges)
│   ├── topbar.html              ← Topbar (6 dropdowns: Search, Language, FullScreen, DarkMode, Notifications, Profile)
│   ├── customizer.html          ← Theme customizer panel (PRUNED: no Theme/Boxed/Compact/SidebarView)
│   ├── admin-shell.html         ← ⭐ COMPILED TEMPLATE — single source of truth for all frameworks
│   ├── footer.html              ← Footer bar
│   ├── main.html                ← Main content wrapper
│   ├── page-title.html          ← BreadCrumb
│   ├── head-css.html            ← CSS imports (fonts, icons, bootstrap)
│   ├── vendor-scripts.html      ← JS dependencies
│   ├── title-meta.html          ← Meta tags
│   └── menu.html                ← Menu structure
│
├── react-ts/                    ← Layer 2: React/Next.js implementation
│   ├── layouts/                 ← Layout entry, Header, Sidebar, Footer, LayoutMenuData (48KB)
│   ├── header-components/       ← 6 topbar dropdowns (Search, Language, FullScreen, DarkMode, Notifications, Profile)
│   ├── theme-customizer/        ← RightSidebar.tsx (125KB: all theme options)
│   ├── dashboard/               ← DashboardPage, StatCard, WelcomeBanner, RecentActivity
│   ├── slices/layouts/          ← Redux slice (state + actions for layout/theme)
│   └── common/                  ← withRouter, BreadCrumb
│
├── auth-css/                    ← Auth page styling (self-contained, framework-agnostic)
│   ├── auth.css                 ← 834 lines: glass card, gradient bg, form styling (@import fonts.css)
│   └── auth-theme.css           ← Tailwind v4 @theme color tokens (18 colors for auth pages)
│
└── scss/                        ← Framework-agnostic design tokens
    ├── _variables.scss           ← 71KB: Color palette (#405189, #0ab39c), fonts (Poppins), sizes
    ├── _variables-custom.scss    ← Velzon custom vars (sidebar width, header height, gradients)
    └── _variables-dark.scss      ← Dark mode overrides (#1a1d21 body, #212529 sidebar)

assets/                          ← Static resources (copy nguyên block vào project public/)
├── css/
│   ├── app.min.css              ← 442KB: Velzon core styles
│   ├── bootstrap.min.css        ← 283KB: Bootstrap 5
│   ├── custom.min.css           ← Project-specific overrides
│   ├── icons.min.css            ← 607KB: 5 icon families (ri-*, mdi-*, bx-*, la-*) @font-face → ../fonts/
│   └── fonts.css                ← Global font system: Inter + NotoSans CJK + Velzon typography tokens
├── fonts/                       ← 11 woff2-only files (modern browsers 97%+)
│   ├── Inter-roman.woff2        ← 344KB: Latin + Vietnamese + Cyrillic (text)
│   ├── Inter-italic.woff2       ← 379KB (text)
│   ├── NotoSansJP.woff2         ← 4.0MB: Japanese CJK (on-demand via unicode-range)
│   ├── NotoSansKR.woff2         ← 3.8MB: Korean CJK (on-demand)
│   ├── NotoSansSC.woff2         ← 7.6MB: Chinese Simplified CJK (on-demand)
│   ├── remixicon.woff2          ← 162KB: ri-* icons (dashboard, widgets)
│   ├── materialdesignicons-webfont.woff2 ← 387KB: mdi-* icons
│   ├── boxicons.woff2           ← 113KB: bx-* icons (sidebar, menu)
│   ├── la-brands-400.woff2      ← 83KB: la-* brand icons (social)
│   ├── la-regular-400.woff2     ← 13KB: la-* UI icons
│   └── la-solid-900.woff2       ← 94KB: la-* solid icons
└── images/
    ├── flags/                   ← Country flag icons
    └── sidebar/                 ← Sidebar decoration
```

### Framework Routing Rules

| Target Framework | Read From | Action |
|---|---|---|
| **ALL frameworks** | `source/html-canonical/admin-shell.html` | ⭐ **PRIMARY SOURCE** — Read this first, then convert |
| **React / Next.js / Inertia+React** | + `source/react-ts/*` | Supplement with React component patterns, adapt imports |
| **Vue / Nuxt** | `source/html-canonical/*` | Convert DOM to `<template>` syntax, keep CSS classes |
| **Laravel / Blade** | `source/html-canonical/*` | Convert to `@extends`/`@section` directives |
| **PHP** | `source/html-canonical/*` | Convert to `<?php include ?>` partials |
| **Node.js / EJS** | `source/html-canonical/*` | Convert to `<%- include() %>` partials |
| **ASP.NET / Razor** | `source/html-canonical/*` | Convert to `@RenderSection`/Partial views |
| **All frameworks** | `source/scss/*` | Use as single source of truth for colors, fonts, sizes |
| **All frameworks** | `assets/css/*` + `assets/fonts/*` | **MANDATORY**: Copy full CSS + fonts bundle |

### Invariance Rules

> [!CAUTION]
> Regardless of framework, the rendered output **MUST** match:
> 1. **DOM structure**: `#layout-wrapper` > `#page-topbar` + `.app-menu` + `.main-content`
> 2. **CSS classes**: All Bootstrap 5 + Velzon custom classes (`--vz-*` prefix)
> 3. **Sidebar dark theme**: Default color `#405189` (indigo)
> 4. **Menu structure**: Categories (`.menu-title`) → Items (`.nav-item`) → Submenus (`.collapse > .nav-sm`)
> 5. **Topbar dropdowns** (left→right): Search → Language → FullScreen → DarkMode → Notifications → Profile (6 items — ~~WebApps~~ ~~Cart~~ REMOVED)
> 6. **Shell components OUTSIDE #layout-wrapper** (in order): BackToTop → Preloader → CustomizerTrigger → RightSidebar
> 7. **Footer**: Configurable branding (companyName/companyUrl) + LiveClock (i18n-synced, updates every second)
> 8. **Header buttons**: ALL use `btn-icon btn-topbar material-shadow-none btn-ghost-secondary rounded-circle`
> 9. **3 LOCKED values**: `data-theme="default"`, `data-layout-width="fluid"`, `data-layout-style="default"` — NOT changeable via customizer
> 10. **Customizer pruned**: No Theme selector, No Boxed, No Compact sidebar, No Sidebar View. Footer = Reset + Close (i18n)
> 11. **Full verification**: Use 15-point checklist from implementation plan

---

## Reference Files

Read these for detailed patterns:

| File | Content |
|------|---------|
| [component-patterns.md](reference/component-patterns.md) | Reusable component code patterns |
| [layout-system.md](reference/layout-system.md) | Layout architecture and sidebar menu |
| [dashboard-patterns.md](reference/dashboard-patterns.md) | Dashboard-specific building patterns |
| [page-catalog.md](reference/page-catalog.md) | Complete 200+ page route catalog |
| [design-tokens.md](reference/design-tokens.md) | Color palette, typography, spacing, shadows, dark mode |
| [tailwind-mapping.md](reference/tailwind-mapping.md) | **Bootstrap → Tailwind CSS** mapping table + config template |
| [inertia-bridge.md](reference/inertia-bridge.md) | Laravel + Inertia.js adaptation patterns |
| [nextjs-patterns.md](reference/nextjs-patterns.md) | Next.js App Router adaptation patterns |
| [html-php-patterns.md](reference/html-php-patterns.md) | HTML/PHP/Laravel Blade patterns |
| [nodejs-patterns.md](reference/nodejs-patterns.md) | Node.js Express + EJS patterns |
| [ajax-patterns.md](reference/ajax-patterns.md) | jQuery AJAX single-page shell patterns |
| [aspnet-mvc-patterns.md](reference/aspnet-mvc-patterns.md) | ASP.NET Core 8 + MVC Razor patterns |
| [component-registry.md](reference/component-registry.md) | **🚨 MANDATORY** — Canonical component table, cross-variant directory map, creation/inheritance rules |
| [package-versions.md](reference/package-versions.md) | **Version Lock** — Exact dependency versions for all Velzon packages (React, charts, forms, icons, utils) |
| [asset-catalog.md](reference/asset-catalog.md) | Complete image, font, SCSS, plugin inventory |
| [api-and-helpers.md](reference/api-and-helpers.md) | API client, auth flows, i18n, toast, file upload, avatars |
| [auth-login-template.md](reference/auth-login-template.md) | **BaoSon login design**: glassmorphism card, configurable admin prefix, i18n, OAuth |
| [saas-admin-starter.md](reference/saas-admin-starter.md) | **SaaS Admin Starter Kit**: Auth + RBAC + User Mgmt + Dashboard (universal, all frameworks) |

## Quick Reference: Common Patterns

### 1. Stat Widget Card
```tsx
<Col xl={3} md={6}>
  <Card className="card-animate">
    <CardBody>
      <div className="d-flex align-items-center">
        <div className="flex-grow-1 overflow-hidden">
          <p className="text-uppercase fw-medium text-muted text-truncate mb-0">
            {label}
          </p>
        </div>
        <div className="flex-shrink-0">
          <h5 className={"fs-14 mb-0 text-" + badgeClass}>
            <i className={"fs-13 align-middle " + icon}></i> {percentage}%
          </h5>
        </div>
      </div>
      <div className="d-flex align-items-end justify-content-between mt-4">
        <div>
          <h4 className="fs-22 fw-semibold ff-secondary mb-4">
            <CountUp start={0} end={value} prefix="$" separator="," duration={4} />
          </h4>
          <Link to="#" className="text-decoration-underline">{linkText}</Link>
        </div>
        <div className="avatar-sm flex-shrink-0">
          <span className={"avatar-title rounded fs-3 bg-" + color + "-subtle"}>
            <i className={`text-${color} ${iconClass}`}></i>
          </span>
        </div>
      </div>
    </CardBody>
  </Card>
</Col>
```

### 2. Data Table Page
```tsx
<Card>
  <CardHeader className="border-0">
    <div className="d-flex align-items-center">
      <h5 className="card-title mb-0 flex-grow-1">Table Title</h5>
      <div className="flex-shrink-0">
        <Button color="success" className="add-btn" onClick={toggle}>
          <i className="ri-add-line align-bottom me-1"></i> Add
        </Button>
      </div>
    </div>
  </CardHeader>
  <CardBody>
    <TableContainer
      columns={columns}
      data={data}
      isGlobalFilter={true}
      customPageSize={10}
      divClass="table-responsive table-card mb-1"
      tableClass="align-middle table-nowrap"
      theadClass="table-light text-muted"
      SearchPlaceholder="Search..."
    />
  </CardBody>
</Card>
```

### 3. Redux Slice Pattern
```tsx
// reducer.ts
import { createSlice } from "@reduxjs/toolkit";
import { getData } from './thunk';

const MySlice = createSlice({
  name: 'MyFeature',
  initialState: { data: [], error: {} },
  reducers: {},
  extraReducers: (builder) => {
    builder.addCase(getData.fulfilled, (state, action) => {
      state.data = action.payload;
    });
    builder.addCase(getData.rejected, (state, action) => {
      state.error = action.error.message;
    });
  }
});

// thunk.ts
import { createAsyncThunk } from "@reduxjs/toolkit";
export const getData = createAsyncThunk("myFeature/getData", async () => {
  const response = await apiCall();
  return response;
});
```

### 4. Delete Confirmation Modal
```tsx
<Modal isOpen={show} toggle={onCloseClick} centered>
  <ModalBody className="py-3 px-5">
    <div className="mt-2 text-center">
      <i className="ri-delete-bin-line display-5 text-danger"></i>
      <div className="mt-4 pt-2 fs-15 mx-4 mx-sm-5">
        <h4>Are you sure?</h4>
        <p className="text-muted mx-4 mb-0">
          Are you sure you want to remove this record?
        </p>
      </div>
    </div>
    <div className="d-flex gap-2 justify-content-center mt-4 mb-2">
      <Button color="light" onClick={onCloseClick}>Close</Button>
      <Button color="danger" onClick={onDeleteClick}>Yes, Delete It!</Button>
    </div>
  </ModalBody>
</Modal>
```

### 5. BreadCrumb
```tsx
<BreadCrumb title="Page Title" pageTitle="Parent Category" />
```

## CSS Class Conventions

| Class | Usage |
|-------|-------|
| `card-animate` | Hover animation on cards |
| `card-height-100` | Full-height card |
| `avatar-xs/sm/md/lg/xl` | Avatar sizing |
| `avatar-title` | Centered icon in avatar |
| `ff-secondary` | Secondary font family |
| `fs-10` to `fs-24` | Font sizes |
| `text-truncate` | Ellipsis overflow |
| `material-shadow-none` | Remove material shadow |
| `btn-soft-*` | Soft/subtle button variant |
| `table-nowrap` | No-wrap table cells |
| `table-card` | Card-style table |

## Icon System

Primary: **Remix Icons** (`ri-*` prefix)
```html
<i className="ri-dashboard-2-line"></i>    <!-- Line style -->
<i className="ri-dashboard-2-fill"></i>    <!-- Fill style -->
<i className="ri-add-line align-bottom me-1"></i>  <!-- Common button icon -->
<i className="ri-delete-bin-line"></i>      <!-- Delete -->
<i className="ri-pencil-fill"></i>          <!-- Edit -->
<i className="ri-eye-fill"></i>             <!-- View -->
```

Also available: BoxIcons (`bx bx-*`), Material Design, Feather, Line Awesome, Crypto Icons.

## Build & Dev Commands

### Per-Variant Commands

| Variant | Path | Install | Dev Server | Build |
|---------|------|---------|------------|-------|
| **React-TS** | `React-TS/Master/` | `pnpm install` | `pnpm start` (CRA) | `pnpm build` |
| **Next.js** | `Nextjs/Master/` | `pnpm install` | `pnpm dev` (Next 16) | `pnpm build` |
| **HTML** | `HTML/Master/` | `pnpm install` | `pnpm exec gulp` (BrowserSync) | `pnpm exec gulp build` |
| **Laravel** | `Laravel/` | `composer install && pnpm install` | `php artisan serve` + `pnpm dev` | `pnpm build` |
| **PHP** | `PHP/` | N/A (static includes) | Local PHP server | N/A |

### CSS/SCSS Compilation

SCSS is compiled automatically by CRA/webpack (React-TS) or Gulp (HTML):
- **React-TS**: Webpack (via react-scripts) processes `app.scss` and `themes.scss` via `sass` package
- **HTML**: Gulp compiles via `gulp-sass` with source maps
- **Next.js**: SCSS imported directly in layout components

### i18n Configuration

```tsx
// i18n.ts
import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import LanguageDetector from "i18next-browser-languagedetector";

i18n.use(LanguageDetector).use(initReactI18next).init({
  fallbackLng: "en",
  resources: {
    en: { translation: require("./locales/en.json") },
    sp: { translation: require("./locales/sp.json") },
    gr: { translation: require("./locales/gr.json") },  // German
    it: { translation: require("./locales/it.json") },
    ru: { translation: require("./locales/ru.json") },
    ch: { translation: require("./locales/ch.json") },
    fr: { translation: require("./locales/fr.json") },
    ar: { translation: require("./locales/ar.json") },
  },
});
```

**Available Locales:** `en`, `sp`, `gr` (German), `it`, `ru`, `ch`, `fr`, `ar`
**Usage:** `const { t } = useTranslation(); <span>{t("Dashboard")}</span>`

