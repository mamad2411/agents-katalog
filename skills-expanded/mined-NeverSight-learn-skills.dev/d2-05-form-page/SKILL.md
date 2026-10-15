---
name: d2-05-form-page
description: "Builds the create/update form page in up-app using ReactiveFormsModule with FormGroup/FormControl validation. Supports flexible capabilities: create (new records) and save (update records). Redeploys after changes. Use when the user asks for Day 2 step 5 of the CRUD drill, or asks to build the add/edit form page for up-app. Features are based on capabilities selected in d2-03."
compatibility: "Requires Docker + Docker Compose, an existing up-app project with the entity service and search page's routes already in place (from earlier drill steps), and ReactiveFormsModule imported in app.config.ts."
---

# Day 2 · Step 5 — Form page with capability-based create/update

**Note:** This skill adapts based on capabilities selected in d2-03-main-menu:
- If `create` is selected: allows creating new records
- If `save` is selected: allows updating existing records
- Both can be selected for full create/update functionality

**Routes:** Already defined in **d2-03-main-menu** (complete app.routes.ts). This skill uses:
- `/<entity>/new` route for creating new records
- `/<entity>/:id/edit` route for editing existing records

**Prerequisites:** Add `ReactiveFormsModule` to `app.config.ts`:
```typescript
import { ReactiveFormsModule } from '@angular/forms';
import { provideClientHydration } from '@angular/platform-browser';
import { ApplicationConfig } from '@angular/core';

export const appConfig: ApplicationConfig = {
  providers: [
    provideClientHydration(),
    ReactiveFormsModule,
    // ... other providers
  ],
};
```

`up-app/src/app/pages/<entity>-form/<entity>-form.component.ts` (standalone component with FormGroup):
- Import `ReactiveFormsModule`, `FormBuilder`, `FormGroup`, `Validators`.
- Create `form: FormGroup` with `FormControl` for each entity field, add `Validators.required` and other rules (e.g., `minLength`, `min`).
- On init, read `id` from route (`ActivatedRoute`). No `id` (or `id === 'new'`) → create mode (empty form). `id` present → edit mode (call `getById(id)` and `form.patchValue(data)` to prefill).
- **Cancel** button → `router.navigate(['/<entity>'])` without saving.
- **Save** button → check `form.valid` before submit; create mode calls `save(form.value)`, edit mode calls `update(id, form.value)`; on success, `router.navigate(['/<entity>'])`.
- Disable Submit button when form is invalid (`[disabled]="form.invalid"`).

Component TypeScript:
```typescript
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { <Entity>Service } from '../../services/<entity>.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-<entity>-form',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './<entity>-form.component.html',
  styleUrls: ['./<entity>-form.component.css']
})
export class <Entity>FormComponent implements OnInit {
  form: FormGroup;
  isEdit = false;

  constructor(
    private fb: FormBuilder,
    private <entity>Service: <Entity>Service,
    private route: ActivatedRoute,
    private router: Router
  ) {
    this.form = this.fb.group({
      empCode: ['', [Validators.required, Validators.minLength(2)]],
      empName: ['', [Validators.required, Validators.minLength(3)]],
      address: [''],
      phoneNo: ['']
    });
  }

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id');
    if (id && id !== 'new') {
      this.isEdit = true;
      this.<entity>Service.getById(+id).subscribe(data => {
        this.form.patchValue(data);
      });
    }
  }

  onSave() {
    if (this.form.invalid) return;
    const id = this.route.snapshot.paramMap.get('id');
    if (this.isEdit && id) {
      this.<entity>Service.update(+id, this.form.value).subscribe(() => {
        this.router.navigate(['/<entity>']);
      });
    } else {
      this.<entity>Service.save(this.form.value).subscribe(() => {
        this.router.navigate(['/<entity>']);
      });
    }
  }

  onCancel() {
    this.router.navigate(['/<entity>']);
  }
}
```

Template (with validation, focus ring, and standard Tailwind):
```html
<div class="min-h-screen bg-gray-50 flex items-center justify-center p-4">
  <div class="bg-white rounded-lg shadow-lg p-8 max-w-md w-full">
    <h2 class="text-3xl font-bold mb-6 text-gray-900">{{ isEdit ? "Edit" : "Add New" }} <Entity></h2>

    <form [formGroup]="form" (ngSubmit)="onSave()">
      <div class="mb-6">
        <label class="block font-semibold mb-2 text-gray-700">Employee Code</label>
        <input
          type="text"
          formControlName="empCode"
          class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
          placeholder="e.g., EMP001"
        />
        @if (form.get("empCode")?.hasError("required") && form.get("empCode")?.touched) {
          <p class="text-red-500 text-sm mt-1 font-semibold">Employee Code is required</p>
        }
        @if (form.get("empCode")?.hasError("minlength") && form.get("empCode")?.touched) {
          <p class="text-red-500 text-sm mt-1 font-semibold">Code must be at least 2 characters</p>
        }
      </div>

      <div class="mb-6">
        <label class="block font-semibold mb-2 text-gray-700">Employee Name</label>
        <input
          type="text"
          formControlName="empName"
          class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
          placeholder="e.g., John Doe"
        />
        @if (form.get("empName")?.hasError("required") && form.get("empName")?.touched) {
          <p class="text-red-500 text-sm mt-1 font-semibold">Employee Name is required</p>
        }
        @if (form.get("empName")?.hasError("minlength") && form.get("empName")?.touched) {
          <p class="text-red-500 text-sm mt-1 font-semibold">Name must be at least 3 characters</p>
        }
      </div>

      <div class="mb-6">
        <label class="block font-semibold mb-2 text-gray-700">Address</label>
        <input
          type="text"
          formControlName="address"
          class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
          placeholder="Optional"
        />
      </div>

      <div class="mb-6">
        <label class="block font-semibold mb-2 text-gray-700">Phone Number</label>
        <input
          type="text"
          formControlName="phoneNo"
          class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
          placeholder="Optional"
        />
      </div>

      <div class="flex gap-4 mt-8">
        <button
          type="submit"
          [disabled]="form.invalid"
          class="flex-1 bg-green-500 hover:bg-green-600 disabled:bg-gray-300 text-white font-semibold px-6 py-3 rounded-lg transition disabled:cursor-not-allowed"
        >
          Save
        </button>
        <button
          type="button"
          (click)="onCancel()"
          class="flex-1 bg-gray-400 hover:bg-gray-500 text-white font-semibold px-6 py-3 rounded-lg transition"
        >
          Cancel
        </button>
      </div>
    </form>
  </div>
</div>
```

**Form Customization:**
- Replace `empCode`, `empName`, `address`, `phoneNo` with your entity's actual property names and validators
- Add/remove form fields to match your entity structure
- Adjust validator rules (required, minLength, pattern, etc.) per field

**Validators Reference:**
- `Validators.required`: Field cannot be empty
- `Validators.minLength(n)`: Minimum length requirement
- `Validators.pattern(regex)`: Custom regex pattern matching
- `Validators.min(n)` / `Validators.max(n)`: Number range validation

**Error Display:**
- Show error messages when field has error AND has been touched
- Use `form.get('fieldName')?.hasError('errorType')` for specific error checking

