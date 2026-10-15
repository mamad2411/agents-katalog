---
name: d2-04-search-delete-page
description: "Builds the search/list page in up-app loading all records via the entity service. Supports flexible capabilities: search (list), edit, and optionally delete. Use when the user asks for Day 2 step 4 of the CRUD drill, or asks to build the search/list page for up-app. Features are based on capabilities selected in d2-03."
compatibility: "Requires an existing up-app project with the entity service already created (from the api-service step)."
---

# Day 2 · Step 4 — Search page with capability-based features

**Note:** This skill adapts based on capabilities selected in d2-03-main-menu:
- If `search` is selected: shows list with Edit button
- If `delete` is also selected: adds Delete button with inline confirmation popup
- If only `search`: no Delete button

`up-app/src/app/pages/<entity>-search/<entity>-search.component.ts` (standalone component):
- Use `signal<Entity[]>([])` to store the items list; on data fetch, call `.set()` to update.
- On init, call `<entity>Service.getAll()` and `this.items.set(data)` to update signal.
- If `create` capability enabled: Header bar with an **Add** button → `router.navigate(['/<entity>/new'])`.
- Add **Back** button that navigates to home/menu → `router.navigate(['/'])`.
- Per row (use `@for` with `track item.id`): 
  - **Edit** button → `router.navigate(['/<entity>', item.id, 'edit'])` (always included)
  - **Delete** button (only if `delete` capability selected) → show confirmation popup; if confirmed, call `<entity>Service.delete(id)` and update signal with `.set()` on success.

**Routes:** Already defined in **d2-03-main-menu** (complete app.routes.ts). This skill uses those routes for navigation.

Component TypeScript:
```typescript
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { signal } from '@angular/core';
import { <Entity>Service, <Entity> } from '../../services/<entity>.service';

@Component({
  selector: 'app-<entity>-search',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './<entity>-search.component.html',
  styleUrls: ['./<entity>-search.component.css']
})
export class <Entity>SearchComponent implements OnInit {
  items = signal<<Entity>[]>([]);
  
  // Capability flags (set based on selections from d2-03)
  hasCreateCapability = true;   // Set to false if 'create' not selected
  hasDeleteCapability = true;   // Set to false if 'delete' not selected

  constructor(
    private router: Router,
    private <entity>Service: <Entity>Service
  ) {}

  ngOnInit() {
    this.<entity>Service.getAll().subscribe(data => {
      this.items.set(data);
    });
  }

  onBack() {
    this.router.navigate(['/']);  // Navigate back to menu/home
  }

  onAdd() {
    this.router.navigate([`/<entity>/new`]);
  }

  onEdit(id: number | undefined) {
    if (id) {
      this.router.navigate(['/<entity>', id, 'edit']);
    }
  }

  onDelete(item: <Entity>) {
    if (confirm(`Delete "<property name from item>"?`)) {
      if (item.id) {
        this.<entity>Service.delete(item.id).subscribe(() => {
          const current = this.items();
          this.items.set(current.filter(i => i.id !== item.id));
        });
      }
    }
  }
}
```

Template (with flexible columns, Back button, and capability-based Delete):
```html
<div class="min-h-screen bg-gray-50">
  <div class="max-w-4xl mx-auto p-6">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <div class="flex items-center gap-4">
        <button
          (click)="onBack()"
          class="bg-gray-500 hover:bg-gray-600 text-white font-semibold px-4 py-2 rounded-lg transition"
        >
          ← Back
        </button>
        <h1 class="text-4xl font-bold text-gray-900"><Entity> List</h1>
      </div>
      @if (hasCreateCapability) {
        <button
          (click)="onAdd()"
          class="bg-green-500 hover:bg-green-600 text-white font-semibold px-6 py-3 rounded-lg transition shadow-md"
        >
          + Add New
        </button>
      }
    </div>

    <!-- Table -->
    <div class="bg-white rounded-lg shadow-md overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full">
          <thead>
            <tr class="bg-gray-100 border-b border-gray-200">
              <!-- Replace with your entity's columns, e.g.: -->
              <th class="px-6 py-3 text-left font-semibold text-gray-700">Code</th>
              <th class="px-6 py-3 text-left font-semibold text-gray-700">Name</th>
              <th class="px-6 py-3 text-left font-semibold text-gray-700">Address</th>
              <th class="px-6 py-3 text-left font-semibold text-gray-700">Phone</th>
              <th class="px-6 py-3 text-center font-semibold text-gray-700">Actions</th>
            </tr>
          </thead>
          <tbody>
            @for (item of items(); track item.id) {
              <tr class="border-b border-gray-100 hover:bg-gray-50 transition">
                <!-- Replace with your entity's properties, e.g.: -->
                <td class="px-6 py-3 text-gray-900 font-medium">{{ item.empCode }}</td>
                <td class="px-6 py-3 text-gray-900">{{ item.empName }}</td>
                <td class="px-6 py-3 text-gray-700">{{ item.address || "-" }}</td>
                <td class="px-6 py-3 text-gray-700">{{ item.phoneNo || "-" }}</td>
                <td class="px-6 py-3 text-center">
                  <button
                    (click)="onEdit(item.id)"
                    class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg mr-2 transition text-sm font-semibold"
                  >
                    Edit
                  </button>
                  @if (hasDeleteCapability) {
                    <button
                      (click)="onDelete(item)"
                      class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition text-sm font-semibold"
                    >
                      Delete
                    </button>
                  }
                </td>
              </tr>
            }
          </tbody>
        </table>
      </div>

      @if (items().length === 0) {
        <div class="text-center py-8 text-gray-600">
          <p class="text-lg">No <entity> found. 
            @if (hasCreateCapability) {
              <a href="javascript:" (click)="onAdd()" class="text-blue-500 hover:underline">Create one</a>.
            } @else {
              Contact your administrator to create records.
            }
          </p>
        </div>
      }
    </div>
  </div>
</div>
```

**Column Customization:**
- Replace `empCode`, `empName`, `address`, `phoneNo` with your entity's actual property names
- Add/remove table header `<th>` and table data `<td>` columns to match your entity structure
- Use `|| "-"` to display dashes for empty/null optional fields

**Capability Flags:**
- Set `hasCreateCapability` and `hasDeleteCapability` based on selections from d2-03
- If `false`, the Add and Delete buttons won't appear
- Adapt buttons dynamically to your CRUD requirements

