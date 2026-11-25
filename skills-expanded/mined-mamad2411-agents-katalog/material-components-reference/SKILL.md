---
name: material-components-reference
description: Angular Material components quick reference. Use when searching for Material component APIs, theming patterns, or CDK utilities.
---

# Angular Material Components Quick Reference

A comprehensive reference guide for Angular Material components, APIs, theming patterns, CDK utilities, and common recipes. This skill provides quick access to component documentation, implementation patterns, and accessibility best practices.

## Table of Contents

1. [Form Controls](#form-controls)
2. [Navigation](#navigation)
3. [Layout](#layout)
4. [Data Display](#data-display)
5. [Popups & Modals](#popups--modals)
6. [Buttons & Indicators](#buttons--indicators)
7. [CDK Utilities](#cdk-utilities)
8. [Theming Patterns](#theming-patterns)
9. [Accessibility Checklist](#accessibility-checklist)
10. [Common Recipes](#common-recipes)
11. [Material Icons](#material-icons)
12. [Animation Patterns](#animation-patterns)
13. [Performance Tips](#performance-tips)
14. [Responsive Patterns](#responsive-patterns)

---

## Form Controls

### Input

**Description**: Text input field with Material styling and validation.

```typescript
// TypeScript
import { MatInputModule } from '@angular/material/input';
import { FormControl, ReactiveFormsModule } from '@angular/forms';

export class InputComponent {
  email = new FormControl('', [Validators.required, Validators.email]);
}
```

```html
<!-- HTML -->
<mat-form-field appearance="outline" class="w-full">
  <mat-label>Email Address</mat-label>
  <input matInput
    [formControl]="email"
    type="email"
    placeholder="user@example.com"
    required>
  <mat-icon matPrefix>mail</mat-icon>

  <!-- Error messages -->
  <mat-error *ngIf="email.hasError('required')">
    Email is required
  </mat-error>
  <mat-error *ngIf="email.hasError('email')">
    Invalid email format
  </mat-error>

  <!-- Hint text -->
  <mat-hint>Enter a valid email address</mat-hint>
</mat-form-field>
```

**Key Properties**:
- `appearance`: "fill" | "outline" (default: "fill")
- `floatLabel`: "always" | "auto" | "never"
- `hideRequiredMarker`: boolean
- `subscriptSizing`: "fixed" | "dynamic"

**Validation States**:
- `pristine` / `dirty`: Form control state
- `touched` / `untouched`: User interaction state
- `valid` / `invalid`: Validation state
- `pending`: Async validation in progress

---

### Select

**Description**: Dropdown selection component.

```typescript
// TypeScript
import { MatSelectModule } from '@angular/material/select';

export class SelectComponent {
  selectedFruit = new FormControl('apple');
  fruits = [
    { value: 'apple', label: 'Apple' },
    { value: 'banana', label: 'Banana' },
    { value: 'orange', label: 'Orange' }
  ];
}
```

```html
<!-- Single selection -->
<mat-form-field appearance="outline">
  <mat-label>Select Fruit</mat-label>
  <mat-select [formControl]="selectedFruit">
    <mat-optgroup label="Popular">
      <mat-option *ngFor="let fruit of fruits" [value]="fruit.value">
        {{ fruit.label }}
      </mat-option>
    </mat-optgroup>
  </mat-select>
</mat-form-field>

<!-- Multiple selection -->
<mat-form-field appearance="outline">
  <mat-label>Select Multiple Fruits</mat-label>
  <mat-select [formControl]="selectedFruits" multiple>
    <mat-option *ngFor="let fruit of fruits" [value]="fruit.value">
      {{ fruit.label }}
    </mat-option>
  </mat-select>
</mat-form-field>
```

**API Reference**:
```typescript
@Component()
export class SelectComponent {
  @ViewChild('select') select!: MatSelect;

  // Methods
  this.select.open();           // Open dropdown
  this.select.close();          // Close dropdown
  this.select.focus();          // Focus select
  this.select.compareWith;      // Custom comparison function
}
```

---

### Checkbox

**Description**: Checkbox input with indeterminate state support.

```typescript
// TypeScript
export class CheckboxComponent {
  isChecked = new FormControl(false);
  isIndeterminate = false;

  toggleAll(checked: boolean): void {
    this.isChecked.setValue(checked);
    // Update child checkboxes
  }
}
```

```html
<!-- Basic checkbox -->
<mat-checkbox [formControl]="isChecked" color="primary">
  I agree to terms
</mat-checkbox>

<!-- Indeterminate checkbox (parent/child) -->
<mat-checkbox
  [checked]="isIndeterminate || allChecked"
  [indeterminate]="isIndeterminate"
  (change)="toggleAll($event.checked)"
  color="primary">
  Select All
</mat-checkbox>

<mat-checkbox *ngFor="let item of items"
  [formControl]="item.control"
  color="primary">
  {{ item.label }}
</mat-checkbox>
```

**Properties**:
- `checked`: boolean
- `indeterminate`: boolean - neither checked nor unchecked
- `disabled`: boolean
- `color`: "primary" | "accent" | "warn"

---

### Radio Button

**Description**: Radio button group for single selection.

```typescript
export class RadioComponent {
  selectedOption = new FormControl('option1');
  options = [
    { value: 'option1', label: 'Option 1' },
    { value: 'option2', label: 'Option 2' },
    { value: 'option3', label: 'Option 3' }
  ];
}
```

```html
<!-- Vertical layout -->
<mat-radio-group [formControl]="selectedOption">
  <mat-radio-button *ngFor="let opt of options" [value]="opt.value">
    {{ opt.label }}
  </mat-radio-button>
</mat-radio-group>

<!-- Horizontal layout -->
<mat-radio-group [formControl]="selectedOption">
  <mat-label>Choose option:</mat-label>
  <mat-radio-button
    *ngFor="let opt of options"
    [value]="opt.value"
    color="primary">
    {{ opt.label }}
  </mat-radio-button>
</mat-radio-group>
```

---

### Datepicker

**Description**: Date selection with calendar widget.

```typescript
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';

export class DatepickerComponent {
  selectedDate = new FormControl(new Date());
  minDate = new Date(2020, 0, 1);
  maxDate = new Date(2030, 11, 31);

  // Custom date filter
  dateFilter = (d: Date | null): boolean => {
    if (!d) return true;
    const day = d.getDay();
    // Disable weekends
    return day !== 0 && day !== 6;
  };
}
```

```html
<!-- Basic datepicker -->
<mat-form-field appearance="outline">
  <mat-label>Select Date</mat-label>
  <input matInput
    [matDatepicker]="picker"
    [formControl]="selectedDate">
  <mat-datepicker-toggle matSuffix [for]="picker"></mat-datepicker-toggle>
  <mat-datepicker #picker></mat-datepicker>
</mat-form-field>

<!-- Advanced datepicker -->
<mat-form-field appearance="outline">
  <mat-label>Select Date</mat-label>
  <input matInput
    [matDatepicker]="advancedPicker"
    [formControl]="selectedDate"
    [min]="minDate"
    [max]="maxDate">
  <mat-datepicker-toggle matSuffix [for]="advancedPicker"></mat-datepicker-toggle>
  <mat-datepicker #advancedPicker
    [dateFilter]="dateFilter"
    startView="month"
    panelClass="custom-datepicker">
  </mat-datepicker>
</mat-form-field>
```

**API Reference**:
```typescript
// Programmatic control
@ViewChild('picker') datepicker!: MatDatepicker<Date>;

openDatepicker(): void {
  this.datepicker.open();
}

closeDatepicker(): void {
  this.datepicker.close();
}

// Format date
import { DatePipe } from '@angular/common';
formattedDate = this.datePipe.transform(this.selectedDate.value, 'yyyy-MM-dd');
```

---

### Slider

**Description**: Range slider input for numeric values.

```typescript
import { MatSliderModule } from '@angular/material/slider';

export class SliderComponent {
  sliderValue = new FormControl(50);
  rangeValue = new FormControl({ start: 20, end: 80 });

  min = 0;
  max = 100;
  step = 5;
}
```

```html
<!-- Single slider -->
<mat-slider min="0" max="100" step="5" [formControl]="sliderValue">
  <input matSliderThumb>
</mat-slider>
<p>Value: {{ sliderValue.value }}</p>

<!-- Range slider -->
<mat-slider [formControl]="rangeValue">
  <input matSliderStartThumb>
  <input matSliderEndThumb>
</mat-slider>
<p>Range: {{ rangeValue.value.start }} - {{ rangeValue.value.end }}</p>

<!-- With tick marks -->
<mat-slider min="0" max="100" step="10">
  <input matSliderThumb>
  <mat-slider-visual-thumb></mat-slider-visual-thumb>
</mat-slider>
```

---

### Autocomplete

**Description**: Autocomplete input with filtering suggestions.

```typescript
import { MatAutocompleteModule } from '@angular/material/autocomplete';

export class AutocompleteComponent {
  control = new FormControl('');
  filteredOptions$!: Observable<string[]>;

  options = [
    'Apple', 'Apricot', 'Avocado',
    'Banana', 'Blueberry',
    'Cherry', 'Coconut'
  ];

  constructor() {
    this.filteredOptions$ = this.control.valueChanges.pipe(
      startWith(''),
      map(value => this.filterOptions(value || ''))
    );
  }

  private filterOptions(filterValue: string): string[] {
    const filter = filterValue.toLowerCase();
    return this.options.filter(opt =>
      opt.toLowerCase().includes(filter)
    );
  }
}
```

```html
<mat-form-field appearance="outline">
  <mat-label>Autocomplete</mat-label>
  <input matInput
    [matAutocomplete]="auto"
    [formControl]="control">
  <mat-autocomplete #auto="matAutocomplete">
    <mat-option *ngFor="let option of filteredOptions$ | async"
      [value]="option">
      {{ option }}
    </mat-option>

    <mat-optgroup label="No matches" *ngIf="(filteredOptions$ | async)?.length === 0">
      <mat-option disabled>No results found</mat-option>
    </mat-optgroup>
  </mat-autocomplete>
</mat-form-field>
```

---

### Slide Toggle

**Description**: Toggle switch control.

```typescript
import { MatSlideToggleModule } from '@angular/material/slide-toggle';

export class SlideToggleComponent {
  isDarkMode = new FormControl(false);
  isNotificationEnabled = new FormControl(true);
}
```

```html
<!-- Basic toggle -->
<mat-slide-toggle [formControl]="isDarkMode" color="primary">
  Dark Mode
</mat-slide-toggle>

<!-- With label -->
<mat-slide-toggle [formControl]="isNotificationEnabled"
  labelPosition="before">
  Enable Notifications
</mat-slide-toggle>

<!-- Disabled state -->
<mat-slide-toggle [formControl]="isNotificationEnabled" disabled>
  Feature Disabled
</mat-slide-toggle>
```

---

### Form Field

**Description**: Container for form controls with consistent styling.

```html
<!-- Appearance variants -->
<mat-form-field appearance="fill">
  <mat-label>Fill Appearance</mat-label>
  <input matInput>
</mat-form-field>

<mat-form-field appearance="outline">
  <mat-label>Outline Appearance</mat-label>
  <input matInput>
</mat-form-field>

<!-- With validation -->
<mat-form-field appearance="outline" [formGroup]="form">
  <mat-label>Email</mat-label>
  <input matInput formControlName="email" required>

  <mat-icon matPrefix>email</mat-icon>
  <mat-icon matSuffix *ngIf="form.get('email')?.valid">check_circle</mat-icon>

  <mat-error *ngIf="form.get('email')?.hasError('required')">
    Email is required
  </mat-error>
  <mat-error *ngIf="form.get('email')?.hasError('email')">
    Invalid email
  </mat-error>

  <mat-hint align="end">
    {{ form.get('email')?.value?.length || 0 }}/255
  </mat-hint>
</mat-form-field>

<!-- Form Field properties -->
<mat-form-field
  appearance="outline"
  [subscriptSizing]="'dynamic'"
  [hideRequiredMarker]="false"
  [floatLabel]="'auto'">
  <mat-label>Full name</mat-label>
  <input matInput required>
</mat-form-field>
```

---

## Navigation

### Toolbar

**Description**: Header navigation and branding bar.

```typescript
import { MatToolbarModule } from '@angular/material/toolbar';

@Component({
  selector: 'app-toolbar',
  standalone: true,
  imports: [MatToolbarModule, MatIconModule, MatButtonModule],
  template: `
    <mat-toolbar color="primary" class="shadow-lg">
      <button mat-icon-button class="example-icon" aria-label="menu">
        <mat-icon>menu</mat-icon>
      </button>
      <span class="spacer"></span>
      <span>My Application</span>
      <span class="spacer"></span>
      <button mat-icon-button class="example-icon" aria-label="favorite">
        <mat-icon>favorite</mat-icon>
      </button>
    </mat-toolbar>
  `,
  styles: [`
    .spacer {
      flex: 1 1 auto;
    }
  `]
})
export class ToolbarComponent {}
```

**API Reference**:
```typescript
// Properties
color: 'primary' | 'accent' | 'warn';  // Color theme
```

---

### Side Navigation (Sidenav)

**Description**: Drawer navigation with responsive behavior.

```typescript
import { MatSidenavModule } from '@angular/material/sidenav';

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [MatSidenavModule],
  template: `
    <mat-sidenav-container class="sidenav-container" autosize>
      <mat-sidenav
        #sidenav
        mode="side"
        [opened]="isOpen"
        (click)="sidenav.close()"
        class="sidenav">
        <nav>
          <a mat-list-item routerLink="/dashboard">Dashboard</a>
          <a mat-list-item routerLink="/users">Users</a>
          <a mat-list-item routerLink="/settings">Settings</a>
        </nav>
      </mat-sidenav>

      <mat-sidenav-content>
        <mat-toolbar color="primary">
          <button mat-icon-button (click)="sidenav.toggle()">
            <mat-icon>menu</mat-icon>
          </button>
          <h1 class="flex-1">Title</h1>
        </mat-toolbar>

        <main class="content">
          <!-- Page content here -->
        </main>
      </mat-sidenav-content>
    </mat-sidenav-container>
  `
})
export class LayoutComponent {
  isOpen = true;

  @ViewChild('sidenav') sidenav!: MatSidenav;
}
```

**Mode Options**:
- `side`: Always visible (desktop)
- `over`: Overlays content (mobile)
- `push`: Pushes content to the side

---

### Tabs

**Description**: Tabbed navigation component.

```typescript
import { MatTabsModule } from '@angular/material/tabs';

@Component({
  selector: 'app-tabs',
  standalone: true,
  imports: [MatTabsModule],
  template: `
    <mat-tab-group
      [selectedIndex]="selectedTabIndex"
      (selectedIndexChange)="onTabChange($event)"
      dynamicHeight>

      <mat-tab label="Tab One">
        <ng-template mat-tab-label>
          <mat-icon>home</mat-icon>
          <span class="ml-2">Home</span>
        </ng-template>
        <p>Content for tab one</p>
      </mat-tab>

      <mat-tab label="Tab Two" disabled>
        <p>Content for tab two</p>
      </mat-tab>

      <mat-tab label="Tab Three">
        <p>Content for tab three</p>
      </mat-tab>
    </mat-tab-group>
  `
})
export class TabsComponent {
  selectedTabIndex = 0;

  onTabChange(event: MatTabChangeEvent): void {
    console.log('Selected tab:', event.index);
  }
}
```

---

### Menu

**Description**: Context menu and dropdown navigation.

```typescript
import { MatMenuModule } from '@angular/material/menu';

@Component({
  selector: 'app-menu',
  standalone: true,
  imports: [MatMenuModule, MatButtonModule],
  template: `
    <button mat-button [matMenuTriggerFor]="menu">
      File
      <mat-icon>arrow_drop_down</mat-icon>
    </button>

    <mat-menu #menu="matMenu">
      <button mat-menu-item>
        <mat-icon>note</mat-icon>
        <span>New</span>
      </button>
      <button mat-menu-item>
        <mat-icon>folder_open</mat-icon>
        <span>Open</span>
      </button>
      <mat-divider></mat-divider>
      <button mat-menu-item>
        <mat-icon>exit_to_app</mat-icon>
        <span>Exit</span>
      </button>
    </mat-menu>
  `
})
export class MenuComponent {}
```

**Advanced Menu**:
```html
<!-- Nested menu -->
<button mat-button [matMenuTriggerFor]="mainMenu">Menu</button>

<mat-menu #mainMenu="matMenu">
  <button mat-menu-item [matMenuTriggerFor]="subMenu">
    Submenu
    <mat-icon matMenuTriggerFor="subMenu">arrow_right</mat-icon>
  </button>
</mat-menu>

<mat-menu #subMenu="matMenu">
  <button mat-menu-item>Option 1</button>
  <button mat-menu-item>Option 2</button>
</mat-menu>
```

---

## Layout

### Card

**Description**: Container component for grouped content.

```typescript
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-card',
  standalone: true,
  imports: [MatCardModule, MatButtonModule],
  template: `
    <mat-card class="max-w-md">
      <mat-card-header>
        <mat-card-title>Card Title</mat-card-title>
        <mat-card-subtitle>Subtitle</mat-card-subtitle>
      </mat-card-header>

      <img mat-card-image src="image.jpg" alt="Image">

      <mat-card-content>
        <p>Card content here</p>
      </mat-card-content>

      <mat-card-actions>
        <button mat-button>Action 1</button>
        <button mat-button>Action 2</button>
      </mat-card-actions>
    </mat-card>
  `
})
export class CardComponent {}
```

---

### List

**Description**: Ordered and unordered lists with Material styling.

```typescript
import { MatListModule } from '@angular/material/list';

@Component({
  selector: 'app-list',
  standalone: true,
  imports: [MatListModule, MatIconModule],
  template: `
    <!-- Simple list -->
    <mat-list>
      <mat-list-item *ngFor="let item of items">
        <mat-icon matListItemIcon>folder</mat-icon>
        <div matListItemTitle>{{ item.name }}</div>
        <div matListItemLine>{{ item.description }}</div>
      </mat-list-item>
    </mat-list>

    <!-- Selection list -->
    <mat-selection-list #list>
      <mat-list-option *ngFor="let item of items" [value]="item">
        {{ item.name }}
      </mat-list-option>
    </mat-selection-list>

    <button (click)="getSelected()">
      Get Selected: {{ list.selectedOptions.selected.length }}
    </button>
  `
})
export class ListComponent {
  items = [
    { name: 'Item 1', description: 'Description 1' },
    { name: 'Item 2', description: 'Description 2' }
  ];

  getSelected(): void {
    console.log(this.items);
  }
}
```

---

### Grid List

**Description**: Responsive grid layout for tile-based content.

```typescript
import { MatGridListModule } from '@angular/material/grid-list';

@Component({
  selector: 'app-grid',
  standalone: true,
  imports: [MatGridListModule, MatCardModule],
  template: `
    <mat-grid-list cols="3" rowHeight="200px" gutterSize="20px">
      <mat-grid-tile *ngFor="let tile of tiles"
        [colspan]="tile.cols"
        [rowspan]="tile.rows">
        <mat-card>{{ tile.name }}</mat-card>
      </mat-grid-tile>
    </mat-grid-list>
  `
})
export class GridComponent {
  tiles = [
    { name: 'Tile 1', cols: 1, rows: 1 },
    { name: 'Tile 2', cols: 2, rows: 1 },
    { name: 'Tile 3', cols: 1, rows: 2 }
  ];
}
```

---

## Data Display

### Data Table

**Description**: Feature-rich table with sorting, filtering, and pagination.

```typescript
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatSortModule } from '@angular/material/sort';

export interface UserData {
  id: string;
  name: string;
  email: string;
  role: string;
}

@Component({
  selector: 'app-data-table',
  standalone: true,
  imports: [MatTableModule, MatPaginatorModule, MatSortModule, CommonModule],
  template: `
    <div class="table-container">
      <!-- Search filter -->
      <mat-form-field>
        <mat-label>Filter</mat-label>
        <input matInput (keyup)="applyFilter($event)"
          placeholder="Search...">
      </mat-form-field>

      <!-- Table -->
      <table mat-table [dataSource]="dataSource" matSort
        class="w-full">

        <!-- ID Column -->
        <ng-container matColumnDef="id">
          <th mat-header-cell *matHeaderCellDef mat-sort-header>ID</th>
          <td mat-cell *matCellDef="let element">{{ element.id }}</td>
        </ng-container>

        <!-- Name Column -->
        <ng-container matColumnDef="name">
          <th mat-header-cell *matHeaderCellDef mat-sort-header>Name</th>
          <td mat-cell *matCellDef="let element">{{ element.name }}</td>
        </ng-container>

        <!-- Email Column -->
        <ng-container matColumnDef="email">
          <th mat-header-cell *matHeaderCellDef mat-sort-header>Email</th>
          <td mat-cell *matCellDef="let element">{{ element.email }}</td>
        </ng-container>

        <!-- Role Column -->
        <ng-container matColumnDef="role">
          <th mat-header-cell *matHeaderCellDef mat-sort-header>Role</th>
          <td mat-cell *matCellDef="let element">
            <mat-chip [color]="element.role === 'admin' ? 'warn' : 'primary'">
              {{ element.role }}
            </mat-chip>
          </td>
        </ng-container>

        <!-- Actions Column -->
        <ng-container matColumnDef="actions">
          <th mat-header-cell *matHeaderCellDef>Actions</th>
          <td mat-cell *matCellDef="let element">
            <button mat-icon-button>
              <mat-icon>edit</mat-icon>
            </button>
            <button mat-icon-button color="warn">
              <mat-icon>delete</mat-icon>
            </button>
          </td>
        </ng-container>

        <!-- Header and rows -->
        <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
        <tr mat-row *matRowDef="let row; columns: displayedColumns;"></tr>
      </table>

      <!-- Paginator -->
      <mat-paginator
        [pageSizeOptions]="[5, 10, 25, 100]"
        [pageSize]="10"
        showFirstLastButtons>
      </mat-paginator>
    </div>
  `,
  styles: [`
    .table-container {
      width: 100%;
      overflow: auto;
    }
    table {
      width: 100%;
    }
  `]
})
export class DataTableComponent implements OnInit {
  displayedColumns: string[] = ['id', 'name', 'email', 'role', 'actions'];
  dataSource!: MatTableDataSource<UserData>;

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  users: UserData[] = [
    { id: '1', name: 'John Doe', email: 'john@example.com', role: 'admin' },
    { id: '2', name: 'Jane Smith', email: 'jane@example.com', role: 'user' }
  ];

  ngOnInit(): void {
    this.dataSource = new MatTableDataSource(this.users);
  }

  ngAfterViewInit(): void {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  applyFilter(event: Event): void {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }
}
```

---

### Chips

**Description**: Small, interactive elements for labels and tags.

```typescript
import { MatChipsModule } from '@angular/material/chips';

@Component({
  selector: 'app-chips',
  standalone: true,
  imports: [MatChipsModule, MatIconModule],
  template: `
    <!-- Basic chips -->
    <mat-chip-set aria-label="Basic chips">
      <mat-chip>Basic Chip</mat-chip>
      <mat-chip disabled>Disabled Chip</mat-chip>
    </mat-chip-set>

    <!-- Selectable chips -->
    <mat-chip-set aria-label="Selectable chips">
      <mat-chip selected>Selected Chip</mat-chip>
      <mat-chip>Unselected Chip</mat-chip>
    </mat-chip-set>

    <!-- Removable chips -->
    <mat-chip-set aria-label="Removable chips">
      <mat-chip removable (removed)="removeChip(chip)">
        {{ chip }}
        <mat-icon matChipRemove>cancel</mat-icon>
      </mat-chip>
    </mat-chip-set>
  `
})
export class ChipsComponent {
  chips = ['Chip 1', 'Chip 2', 'Chip 3'];

  removeChip(chip: string): void {
    this.chips = this.chips.filter(c => c !== chip);
  }
}
```

---

### Expansion Panel

**Description**: Collapsible panel for hiding/showing content.

```typescript
import { MatExpansionModule } from '@angular/material/expansion';

@Component({
  selector: 'app-expansion',
  standalone: true,
  imports: [MatExpansionModule],
  template: `
    <mat-accordion multi>
      <mat-expansion-panel [expanded]="step === 0" (opened)="setStep(0)">
        <mat-expansion-panel-header>
          <mat-panel-title>Personal Data</mat-panel-title>
        </mat-expansion-panel-header>

        <form [formGroup]="form">
          <mat-form-field>
            <mat-label>First Name</mat-label>
            <input matInput formControlName="firstName">
          </mat-form-field>
        </form>

        <mat-action-row>
          <button mat-button color="primary" (click)="nextStep()">
            Next
          </button>
        </mat-action-row>
      </mat-expansion-panel>

      <mat-expansion-panel [expanded]="step === 1" (opened)="setStep(1)">
        <mat-expansion-panel-header>
          <mat-panel-title>Address</mat-panel-title>
        </mat-expansion-panel-header>

        <form [formGroup]="form">
          <mat-form-field>
            <mat-label>City</mat-label>
            <input matInput formControlName="city">
          </mat-form-field>
        </form>

        <mat-action-row>
          <button mat-button color="warn" (click)="prevStep()">
            Previous
          </button>
          <button mat-button color="primary" (click)="nextStep()">
            Next
          </button>
        </mat-action-row>
      </mat-expansion-panel>
    </mat-accordion>
  `
})
export class ExpansionComponent {
  step = 0;
  form = new FormGroup({
    firstName: new FormControl(''),
    city: new FormControl('')
  });

  setStep(index: number): void {
    this.step = index;
  }

  nextStep(): void {
    this.step++;
  }

  prevStep(): void {
    this.step--;
  }
}
```

---

## Popups & Modals

### Dialog

**Description**: Modal dialog for forms and confirmations.

```typescript
import { MatDialogModule, MatDialog } from '@angular/material/dialog';

// Dialog component
@Component({
  selector: 'app-confirm-dialog',
  standalone: true,
  imports: [MatDialogModule, MatButtonModule],
  template: `
    <h2 mat-dialog-title>{{ data.title }}</h2>
    <mat-dialog-content>
      <p>{{ data.message }}</p>
    </mat-dialog-content>
    <mat-dialog-actions align="end">
      <button mat-button (click)="onCancel()">Cancel</button>
      <button mat-raised-button color="warn" (click)="onConfirm()">
        Delete
      </button>
    </mat-dialog-actions>
  `
})
export class ConfirmDialogComponent {
  constructor(
    public dialogRef: MatDialogRef<ConfirmDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { title: string; message: string }
  ) {}

  onCancel(): void {
    this.dialogRef.close(false);
  }

  onConfirm(): void {
    this.dialogRef.close(true);
  }
}

// Component using dialog
@Component({
  selector: 'app-dialog-user',
  standalone: true,
  imports: [MatButtonModule]
})
export class DialogUserComponent {
  constructor(private dialog: MatDialog) {}

  deleteUser(userId: string): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      width: '400px',
      data: {
        title: 'Delete User',
        message: `Are you sure you want to delete user ${userId}?`
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        console.log('User deleted');
      }
    });
  }
}
```

**Dialog Configuration**:
```typescript
const dialogRef = this.dialog.open(DialogComponent, {
  width: '500px',                           // Width
  height: 'auto',                           // Height
  data: { /* data to pass */ },             // Pass data to dialog
  disableClose: true,                       // Prevent closing by clicking outside
  hasBackdrop: true,                        // Show backdrop
  backdropClass: 'custom-backdrop',         // Custom backdrop class
  panelClass: ['custom-dialog-class'],      // Custom dialog class
  position: { top: '10px', left: '10px' },  // Position
  enterAnimationDuration: 1000,              // Animation duration
  exitAnimationDuration: 500
});
```

---

### Tooltip

**Description**: Contextual help text on hover.

```typescript
import { MatTooltipModule } from '@angular/material/tooltip';

@Component({
  selector: 'app-tooltip',
  standalone: true,
  imports: [MatTooltipModule, MatButtonModule],
  template: `
    <!-- Basic tooltip -->
    <button mat-raised-button
      matTooltip="Helpful information">
      Hover me
    </button>

    <!-- Positioned tooltip -->
    <button mat-raised-button
      matTooltip="Help text"
      matTooltipPosition="above">
      Top tooltip
    </button>

    <!-- Custom delay and class -->
    <button mat-raised-button
      matTooltip="Custom tooltip"
      [matTooltipShowDelay]="500"
      [matTooltipHideDelay]="200"
      matTooltipClass="custom-tooltip">
      Custom tooltip
    </button>
  `,
  styles: [`
    ::ng-deep .custom-tooltip {
      font-size: 16px !important;
      background-color: darkblue !important;
    }
  `]
})
export class TooltipComponent {}
```

---

### Snackbar

**Description**: Bottom notification/toast messages.

```typescript
import { MatSnackBarModule, MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-snackbar',
  standalone: true,
  imports: [MatSnackBarModule, MatButtonModule]
})
export class SnackbarComponent {
  constructor(private snackBar: MatSnackBar) {}

  showMessage(): void {
    const snackBarRef = this.snackBar.open('Message sent', 'Undo', {
      duration: 5000,
      horizontalPosition: 'end',
      verticalPosition: 'bottom',
      panelClass: ['success-snackbar']
    });

    snackBarRef.onAction().subscribe(() => {
      console.log('Undo action clicked');
    });

    snackBarRef.afterDismissed().subscribe(result => {
      if (result.dismissedByAction) {
        console.log('Dismissed by action');
      }
    });
  }

  showError(): void {
    this.snackBar.open('Error occurred', '', {
      duration: 3000,
      panelClass: ['error-snackbar'],
      horizontalPosition: 'center',
      verticalPosition: 'top'
    });
  }
}
```

---

### Progress Spinner & Bar

**Description**: Loading indicators.

```typescript
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatProgressBarModule } from '@angular/material/progress-bar';

@Component({
  selector: 'app-progress',
  standalone: true,
  imports: [MatProgressSpinnerModule, MatProgressBarModule],
  template: `
    <!-- Spinner -->
    <mat-spinner></mat-spinner>
    <mat-spinner diameter="50" strokeWidth="5"></mat-spinner>

    <!-- Determinate spinner -->
    <mat-progress-spinner
      mode="determinate"
      [value]="progress">
    </mat-progress-spinner>

    <!-- Progress bar -->
    <mat-progress-bar mode="indeterminate"></mat-progress-bar>

    <!-- Determinate progress bar -->
    <mat-progress-bar mode="determinate" [value]="progress"></mat-progress-bar>

    <!-- Buffered progress bar -->
    <mat-progress-bar
      mode="buffer"
      [value]="progress"
      [bufferValue]="bufferProgress">
    </mat-progress-bar>
  `
})
export class ProgressComponent {
  progress = 30;
  bufferProgress = 60;
}
```

---

## Buttons & Indicators

### Buttons

**Description**: Various button types and styles.

```typescript
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-buttons',
  standalone: true,
  imports: [MatButtonModule, MatIconModule],
  template: `
    <!-- Text button -->
    <button mat-button>Basic</button>

    <!-- Raised button -->
    <button mat-raised-button color="primary">Raised</button>

    <!-- Flat button -->
    <button mat-stroked-button color="accent">Stroked</button>

    <!-- Icon button -->
    <button mat-icon-button>
      <mat-icon>favorite</mat-icon>
    </button>

    <!-- FAB (Floating Action Button) -->
    <button mat-fab color="primary">
      <mat-icon>add</mat-icon>
    </button>

    <!-- Mini FAB -->
    <button mat-mini-fab color="accent">
      <mat-icon>edit</mat-icon>
    </button>

    <!-- Button with icon -->
    <button mat-raised-button color="primary">
      <mat-icon>download</mat-icon>
      Download
    </button>

    <!-- Disabled button -->
    <button mat-raised-button disabled>Disabled</button>
  `
})
export class ButtonsComponent {}
```

**Button Colors**:
- `primary`: Primary theme color
- `accent`: Accent theme color
- `warn`: Warning/error color

---

### Badge

**Description**: Numeric badge indicator.

```typescript
import { MatBadgeModule } from '@angular/material/badge';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-badge',
  standalone: true,
  imports: [MatBadgeModule, MatIconModule],
  template: `
    <!-- Basic badge -->
    <mat-icon matBadge="15" matBadgeColor="warn">
      mail
    </mat-icon>

    <!-- Hidden badge -->
    <mat-icon matBadge="0" matBadgeHidden="true">
      notifications
    </mat-icon>

    <!-- Positioned badge -->
    <button mat-button matBadge="3" matBadgePosition="above before">
      Items
    </button>

    <!-- Dynamic badge -->
    <mat-icon [matBadge]="notificationCount"
      matBadgeColor="warn"
      [matBadgeHidden]="notificationCount === 0">
      notifications
    </mat-icon>
  `
})
export class BadgeComponent {
  notificationCount = 5;
}
```

---

## CDK Utilities

### Virtual Scrolling

**Description**: Efficiently render long lists.

```typescript
import { ScrollingModule } from '@angular/cdk/scrolling';

@Component({
  selector: 'app-virtual-scroll',
  standalone: true,
  imports: [ScrollingModule, CommonModule],
  template: `
    <cdk-virtual-scroll-viewport itemSize="50" class="h-96 border">
      <div *cdkVirtualFor="let item of items; trackBy: trackById"
        class="p-4 border-b">
        {{ item.name }}
      </div>
    </cdk-virtual-scroll-viewport>
  `
})
export class VirtualScrollComponent {
  items = Array.from({ length: 10000 }, (_, i) => ({
    id: i,
    name: `Item ${i}`
  }));

  trackById(index: number, item: any): number {
    return item.id;
  }
}
```

---

### Drag and Drop

**Description**: Drag-and-drop functionality.

```typescript
import { DragDropModule } from '@angular/cdk/drag-drop';

@Component({
  selector: 'app-drag-drop',
  standalone: true,
  imports: [DragDropModule, CommonModule],
  template: `
    <div class="grid grid-cols-2 gap-4">
      <!-- Source list -->
      <div cdkDropList #sourceList="cdkDropList">
        <h3>Available</h3>
        <div *ngFor="let item of availableItems"
          cdkDrag
          class="p-4 bg-gray-100 rounded cursor-move">
          {{ item }}
        </div>
      </div>

      <!-- Drop zone -->
      <div cdkDropList
        [cdkDropListData]="selectedItems"
        [cdkDropListDisabled]="false"
        [cdkDropListSortingDisabled]="false"
        (cdkDropListDropped)="onDrop($event)"
        class="p-4 bg-blue-50 rounded min-h-96 border-2 border-blue-300">
        <h3>Selected</h3>
        <div *ngFor="let item of selectedItems; let i = index"
          cdkDrag
          [cdkDragData]="item"
          class="p-4 bg-white rounded mb-2 shadow">
          {{ item }}
        </div>
        <p *ngIf="selectedItems.length === 0" class="text-gray-400">
          Drop items here
        </p>
      </div>
    </div>
  `
})
export class DragDropComponent {
  availableItems = ['Item 1', 'Item 2', 'Item 3', 'Item 4'];
  selectedItems: string[] = [];

  onDrop(event: CdkDragDrop<string[]>): void {
    if (event.previousContainer === event.container) {
      moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
    } else {
      copyArrayItem(
        event.previousContainer.data,
        event.container.data,
        event.previousIndex,
        event.currentIndex
      );
    }
  }
}
```

---

### Overlay

**Description**: Position floating elements (tooltips, dropdowns, etc.).

```typescript
import { OverlayModule } from '@angular/cdk/overlay';

@Component({
  selector: 'app-overlay',
  standalone: true,
  imports: [OverlayModule, CommonModule]
})
export class OverlayComponent {
  isOpen = false;

  constructor(private overlay: Overlay) {}

  openOverlay(origin: HTMLElement): void {
    const positionStrategy = this.overlay
      .position()
      .flexibleConnectedTo(origin)
      .withPositions([
        {
          originX: 'start',
          originY: 'bottom',
          overlayX: 'start',
          overlayY: 'top'
        }
      ]);

    const scrollStrategy = this.overlay.scrollStrategies.reposition();

    const overlayRef = this.overlay.create({
      positionStrategy,
      scrollStrategy
    });

    this.isOpen = true;
  }
}
```

---

## Theming Patterns

### Custom Theme

**Description**: Create custom Material themes.

```scss
// Custom theme file (_custom-theme.scss)
@import '@angular/material/theming';

// Define custom palette
$custom-primary: mat.define-palette($mat-blue, 500);
$custom-accent: mat.define-palette($mat-pink, A200, A100, A400);
$custom-warn: mat.define-palette($mat-red);

// Create theme
$custom-theme: mat.define-light-theme((
  color: (
    primary: $custom-primary,
    accent: $custom-accent,
    warn: $custom-warn
  )
));

// Include theme for all Material components
@include mat.all-component-themes($custom-theme);

// Custom component themes
.custom-component {
  @include mat.color($custom-theme);
}
```

**Application**:
```typescript
// styles.scss
@import 'theme/custom-theme';
```

---

### Dark Mode Theme

**Description**: Light and dark theme switching.

```scss
// Define both light and dark themes
$light-theme: mat.define-light-theme(/* ... */);
$dark-theme: mat.define-dark-theme(/* ... */);

// Apply light theme by default
@include mat.all-component-colors($light-theme);

// Apply dark theme when class is present
.dark-mode {
  @include mat.all-component-colors($dark-theme);
}
```

```typescript
// Service to manage theme
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class ThemeService {
  isDarkMode = signal(false);

  toggleDarkMode(): void {
    this.isDarkMode.update(value => !value);
    document.documentElement.classList.toggle(
      'dark-mode',
      this.isDarkMode()
    );
  }
}
```

---

## Accessibility Checklist

### Keyboard Navigation
- [ ] All interactive elements are keyboard accessible
- [ ] Tab order is logical
- [ ] Keyboard shortcuts documented

### Screen Readers
- [ ] `aria-label` on icon buttons
- [ ] `aria-describedby` for form help text
- [ ] `role` attributes where needed
- [ ] `aria-live` for dynamic content

### Color Contrast
- [ ] WCAG AA contrast ratio (4.5:1 minimum)
- [ ] Don't rely on color alone

### Forms
- [ ] Labels associated with inputs
- [ ] Error messages linked to fields
- [ ] Required fields marked

**Example with ARIA**:
```html
<button mat-icon-button
  aria-label="Delete user"
  (click)="deleteUser()">
  <mat-icon>delete</mat-icon>
</button>

<mat-form-field>
  <mat-label>Email</mat-label>
  <input matInput
    type="email"
    aria-describedby="email-hint"
    required>
  <mat-hint id="email-hint">Enter a valid email</mat-hint>
  <mat-error id="email-error">Invalid email</mat-error>
</mat-form-field>
```

---

## Common Recipes

### Loading State in Form

```typescript
@Component({
  selector: 'app-loading-form',
  standalone: true,
  imports: [MatButtonModule, MatFormFieldModule, MatInputModule, ReactiveFormsModule],
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <mat-form-field>
        <mat-label>Email</mat-label>
        <input matInput formControlName="email" required>
      </mat-form-field>

      <button mat-raised-button color="primary" [disabled]="isLoading()">
        <mat-icon *ngIf="isLoading()" matPrefix>hourglass_top</mat-icon>
        {{ isLoading() ? 'Submitting...' : 'Submit' }}
      </button>
    </form>
  `
})
export class LoadingFormComponent {
  form = new FormGroup({
    email: new FormControl('', [Validators.required, Validators.email])
  });

  isLoading = signal(false);

  constructor(private apiService: ApiService) {}

  onSubmit(): void {
    if (this.form.valid) {
      this.isLoading.set(true);
      this.apiService.submit(this.form.value)
        .pipe(
          finalize(() => this.isLoading.set(false)),
          first()
        )
        .subscribe();
    }
  }
}
```

---

### Confirmation Dialog with Result

```typescript
deleteItem(itemId: string): void {
  this.dialog.open(ConfirmDialogComponent, {
    data: { title: 'Delete Item', message: 'Are you sure?' }
  }).afterClosed().subscribe(confirmed => {
    if (confirmed) {
      this.service.delete(itemId).subscribe();
    }
  });
}
```

---

### Paginated Table with Filter

```typescript
@Component({
  template: `
    <mat-form-field>
      <input matInput (keyup)="applyFilter($event)">
    </mat-form-field>

    <table mat-table [dataSource]="dataSource" matSort>
      <!-- columns -->
    </table>

    <mat-paginator [pageSizeOptions]="[5, 10, 25]"
      showFirstLastButtons>
    </mat-paginator>
  `
})
export class PaginatedTableComponent implements OnInit {
  @ViewChild(MatSort) sort!: MatSort;
  @ViewChild(MatPaginator) paginator!: MatPaginator;

  dataSource = new MatTableDataSource<any>();

  ngOnInit(): void {
    this.loadData();
  }

  ngAfterViewInit(): void {
    this.dataSource.sort = this.sort;
    this.dataSource.paginator = this.paginator;
  }

  applyFilter(event: Event): void {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
    this.dataSource.paginator?.firstPage();
  }

  loadData(): void {
    // Load data
  }
}
```

---

## Material Icons

### Using Icons

```typescript
import { MatIconModule } from '@angular/material/icon';

@Component({
  imports: [MatIconModule],
  template: `
    <!-- Material icon -->
    <mat-icon>home</mat-icon>

    <!-- Icon with color -->
    <mat-icon color="primary">favorite</mat-icon>

    <!-- Icon in button -->
    <button mat-icon-button>
      <mat-icon>settings</mat-icon>
    </button>

    <!-- SVG icon -->
    <mat-icon svgIcon="custom-icon"></mat-icon>

    <!-- Font icon -->
    <mat-icon fontIcon="fa-solid fa-star"></mat-icon>
  `
})
export class IconsComponent {
  constructor(private matIconRegistry: MatIconRegistry, private sanitizer: DomSanitizer) {
    // Register custom SVG
    this.matIconRegistry.addSvgIcon(
      'custom-icon',
      this.sanitizer.bypassSecurityTrustResourceUrl('assets/custom-icon.svg')
    );
  }
}
```

**Popular Icons**:
- Navigation: `home`, `menu`, `arrow_back`, `search`
- Communication: `mail`, `phone`, `notifications`, `chat`
- File: `folder`, `file_download`, `cloud_upload`, `delete`
- Action: `edit`, `delete`, `save`, `settings`, `logout`
- UI: `favorite`, `star`, `check_circle`, `close`, `more_vert`

---

## Animation Patterns

### Slide-in Animation

```typescript
import { trigger, transition, style, animate } from '@angular/animations';

@Component({
  selector: 'app-slide-in',
  standalone: true,
  animations: [
    trigger('slideIn', [
      transition(':enter', [
        style({ transform: 'translateX(-100%)' }),
        animate('300ms ease-out', style({ transform: 'translateX(0)' }))
      ]),
      transition(':leave', [
        animate('300ms ease-in', style({ transform: 'translateX(-100%)' }))
      ])
    ])
  ],
  template: `<div @slideIn>Content</div>`
})
export class SlideInComponent {}
```

---

### Fade-in Animation

```typescript
@Component({
  animations: [
    trigger('fadeIn', [
      transition(':enter', [
        style({ opacity: 0 }),
        animate('300ms', style({ opacity: 1 }))
      ])
    ])
  ]
})
export class FadeComponent {}
```

---

## Performance Tips

### 1. Use TrackBy with Lists
```typescript
<mat-option *ngFor="let item of items; trackBy: trackById">
  {{ item.name }}
</mat-option>

trackById(index: number, item: any): any {
  return item.id;
}
```

### 2. Lazy Load Dialogs
```typescript
async openDialog(): Promise<void> {
  const { DialogComponent } = await import('./dialog.component');
  this.dialog.open(DialogComponent);
}
```

### 3. Virtual Scrolling for Large Lists
```html
<cdk-virtual-scroll-viewport itemSize="50" class="h-96">
  <mat-option *cdkVirtualFor="let item of items">
    {{ item }}
  </mat-option>
</cdk-virtual-scroll-viewport>
```

### 4. ChangeDetectionStrategy.OnPush
```typescript
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush
})
```

---

## Responsive Patterns

### Responsive Grid
```typescript
@Component({
  template: `
    <mat-grid-list [cols]="cols" rowHeight="200px">
      <mat-grid-tile *ngFor="let tile of tiles">
        {{ tile }}
      </mat-grid-tile>
    </mat-grid-list>
  `
})
export class ResponsiveGridComponent implements OnInit {
  cols = 3;

  @HostListener('window:resize', ['$event'])
  onResize(event: Event): void {
    const width = (event.target as Window).innerWidth;
    this.cols = width < 600 ? 1 : width < 960 ? 2 : 3;
  }
}
```

---

### Responsive Toolbar
```html
<mat-toolbar color="primary">
  <button mat-icon-button>
    <mat-icon>menu</mat-icon>
  </button>

  <span class="spacer"></span>

  <!-- Hide on mobile -->
  <nav class="hidden sm:block">
    <button mat-button>Home</button>
    <button mat-button>About</button>
  </nav>
</mat-toolbar>
```

---

## Search Index

**Common Searches**:
- Form controls: input, select, checkbox, radio, datepicker, slider, toggle
- Navigation: toolbar, sidenav, tabs, menu
- Data: table, list, grid, chips, expansion
- Popups: dialog, tooltip, snackbar, menu
- CDK: virtual scroll, drag-drop, overlay
- Theming: custom colors, dark mode, palettes
- Icons: Material Icons, custom SVG, font icons
- Animation: slide, fade, transform, keyframes
- Accessibility: ARIA, keyboard, screen readers
- Performance: trackBy, lazy loading, OnPush

---

## Version Notes

- **Latest**: Material 17+
- **Angular**: 17.0+
- **TypeScript**: 5.0+
- **RxJS**: 7.8+

**Useful Resources**:
- [Material Documentation](https://material.angular.io)
- [CDK Documentation](https://material.angular.io/cdk/categories)
- [Material Theme Generator](https://material.io/resources/color/#!/?view.left=0&view.right=0)
- [Material Icon Library](https://fonts.google.com/icons)

---

**Last Updated**: November 2025
**Skill Version**: 1.0
**For**: Angular Material 17+
