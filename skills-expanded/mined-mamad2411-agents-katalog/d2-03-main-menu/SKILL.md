---
name: d2-03-main-menu
description: "Creates a main menu/navigation hub component with dynamically generated menu items based on selected capabilities (search, create, save, delete). Prompts for entity name and available actions, generates menu card and routes. Use when the user asks for Day 2 step 3 of the CRUD drill, or asks to build a main menu for up-app."
compatibility: "Requires an existing up-app project with routing already in place (from d2-00/d2-01/d2-02). Component is standalone."
---

# Day 2 · Step 3 — Main menu with capability-driven menu items

**Before starting:** Ask for:
1. **Entity name** (PascalCase, e.g., `Product`, `Order`, `Employee`) — REQUIRED
2. **Available capabilities** (select one or more: `search`, `create`, `save`, `delete`) — REQUIRED
   - `search`: Browse/list all records
   - `create`: Create new records
   - `save`: Save to database (used with create/edit)
   - `delete`: Delete records

Use exactly as specified. Menu buttons will be generated based on selected capabilities.

**Routing Setup** (`app.routes.ts`) — COMPLETE ROUTING TABLE FOR ALL PAGES:
- Import MenuComponent, all <Entity>SearchComponents, and all <Entity>FormComponents
- Add menu as the **default/landing page** route (path: '')
- Define entity routes for each program: search, create, edit
- This route table is shared by d2-03 (menu), d2-04 (search), and d2-05 (form)

```typescript
import { Routes } from '@angular/router';
import { MenuComponent } from './pages/menu/menu.component';
import { <Entity>SearchComponent } from './pages/<entity>-search/<entity>-search.component';
import { <Entity>FormComponent } from './pages/<entity>-form/<entity>-form.component';
// Add more imports for additional entities as needed

export const routes: Routes = [
  // Landing page (menu comes first!)
  { path: '', component: MenuComponent },

  // <Entity> CRUD routes
  { path: '<entity>', component: <Entity>SearchComponent },        // Search/list page
  { path: '<entity>/new', component: <Entity>FormComponent },      // Create new record
  { path: '<entity>/:id/edit', component: <Entity>FormComponent }, // Edit existing record

  // Add more entity routes here for additional programs:
  // { path: 'customer', component: CustomerSearchComponent },
  // { path: 'customer/new', component: CustomerFormComponent },
  // { path: 'customer/:id/edit', component: CustomerFormComponent },
];
```

**Route Usage:**
- **d2-03-main-menu** uses `{ path: '', component: MenuComponent }` — landing page
- **d2-04-search-delete-page** uses `/<entity>` route and navigates via `router.navigate(['/<entity>/new'])`, `router.navigate(['/<entity>', id, 'edit'])`
- **d2-05-form-page** uses `/<entity>/new` and `/<entity>/:id/edit` routes

Component TypeScript (capability-driven):
```typescript
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

interface MenuItem {
  name: string;
  icon: string;
  path: string;
}

interface Program {
  name: string;
  entity: string;
  icon: string;
  description: string;
  capabilities: string[];
  menuItems: MenuItem[];
}

@Component({
  selector: 'app-menu',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.css']
})
export class MenuComponent {
  appTitle = 'CRUD Dashboard';
  appSubtitle = 'Manage your data with ease';

  programs: Program[] = [];

  constructor(private router: Router) {
    this.programs = [
      {
        name: '<Entity>',
        entity: '<entity>',
        icon: '📦',
        description: 'Manage <entity> records',
        capabilities: ['search', 'create', 'save', 'delete'],
        menuItems: this.generateMenuItems('<entity>', ['search', 'create', 'save', 'delete'])
      },
      // Add more programs here:
      // { name: 'Customer', entity: 'customer', icon: '👥', description: 'Manage customer data', capabilities: [...], menuItems: ... }
    ];
  }

  generateMenuItems(entity: string, capabilities: string[]): MenuItem[] {
    const items: MenuItem[] = [];
    
    if (capabilities.includes('search')) {
      items.push({ name: 'Browse', icon: '📋', path: `/${entity}` });
    }
    if (capabilities.includes('create')) {
      items.push({ name: 'Create', icon: '✚', path: `/${entity}/new` });
    }
    
    return items;
  }

  navigate(path: string) {
    this.router.navigate([path]);
  }
}
```

Template (capability-driven menu with responsive card grid, standard Tailwind classes):
```html
<div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-6">
  <!-- Header -->
  <div class="max-w-6xl mx-auto mb-12">
    <div class="text-center mb-8">
      <h1 class="text-5xl font-bold text-gray-900">{{ appTitle }}</h1>
      <p class="text-gray-600 text-xl mt-4">{{ appSubtitle }}</p>
    </div>
  </div>

  <!-- Program Cards Grid -->
  <div class="max-w-6xl mx-auto">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      @for (program of programs; track program.entity) {
        <div class="bg-white rounded-xl shadow-md hover:shadow-xl transition-shadow p-6">
          <!-- Card Header -->
          <div class="flex items-center mb-4">
            <span class="text-5xl mr-4">{{ program.icon }}</span>
            <div>
              <h3 class="text-2xl font-bold text-gray-900">{{ program.name }}</h3>
              <p class="text-gray-600 text-sm">{{ program.description }}</p>
            </div>
          </div>

          <!-- Capabilities Badge -->
          <div class="flex flex-wrap gap-2 mb-4">
            @for (cap of program.capabilities; track cap) {
              <span class="bg-gray-100 text-gray-700 text-xs font-semibold px-3 py-1 rounded-full">
                {{ cap }}
              </span>
            }
          </div>

          <!-- Divider -->
          <div class="border-b border-gray-200 my-4"></div>

          <!-- Dynamic Menu Buttons -->
          <div class="flex flex-col gap-4">
            @for (item of program.menuItems; track item.name) {
              <button
                (click)="navigate(item.path)"
                [class]="item.name === 'Browse' ? 'w-full text-white font-semibold px-6 py-3 rounded-lg transition bg-blue-500 hover:bg-blue-600' : 'w-full text-white font-semibold px-6 py-3 rounded-lg transition bg-green-500 hover:bg-green-600'"
              >
                {{ item.icon }} {{ item.name }}
              </button>
            }
          </div>

          @if (program.menuItems.length === 0) {
            <p class="text-gray-600 text-sm text-center">No actions available for this program.</p>
          }
        </div>
      }
    </div>
  </div>

  <!-- Footer -->
  <div class="max-w-6xl mx-auto mt-12 text-center">
    <p class="text-gray-600 text-sm">Built with Angular + Tailwind CSS</p>
  </div>
</div>
```

**Design System (Standard Tailwind):**
- **Spacing:** p-6 (padding), mb-4/8/12, gap-2/4/8
- **Colors:** bg-blue-500/600, bg-green-500/600, text-gray-600, bg-gray-100
- **Shadows:** shadow-md, hover:shadow-xl (card elevation)
- **Typography:** text-5xl/2xl, font-bold/semibold
- **Layout:** grid responsive (1-2-3 columns), flex flex-col
- **Interactions:** rounded-lg, transition, hover states

