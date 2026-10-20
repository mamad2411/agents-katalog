---
name: angular-typescript
description: Angular and TypeScript standards (applies to **/*.ts files)
globs: ["**/*.ts"]
alwaysApply: false
---

# Angular 17+ / TypeScript Standards

Applied to all `.ts` files. Enforces modern Angular patterns.

## Components

**TEMPLATE**:
```typescript
import { Component, OnInit, inject, ChangeDetectionStrategy } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { DxDataGridModule } from 'devextreme-angular';

@Component({
  selector: 'app-user-list',
  standalone: true,
  imports: [CommonModule, MatButtonModule, DxDataGridModule],
  templateUrl: './user-list.component.html',
  styleUrls: ['./user-list.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class UserListComponent implements OnInit {
  private readonly userService = inject(UserService);
  private readonly cdr = inject(ChangeDetectorRef);

  users$ = this.userService.getUsers();
  selectedUser: User | null = null;

  ngOnInit(): void {
    // Component initialization
  }

  selectUser(user: User): void {
    this.selectedUser = user;
    this.cdr.markForCheck();
  }
}
```

**ALWAYS**:
- `standalone: true` (no NgModules for new code)
- `inject()` function (not constructor injection)
- `ChangeDetectionStrategy.OnPush` (performance)
- Include necessary imports in `imports: []`
- Type all properties (use proper types)

**NEVER**:
- Use `NgModules` for new components
- Constructor injection (use `inject()`)
- Constructor-based change detection
- Forget to import required modules

## Dependency Injection

**ALWAYS**:
```typescript
// ✅ Modern pattern (inject)
export class UserListComponent {
  private readonly userService = inject(UserService);
  private readonly logger = inject(NgxLogger);
  private readonly cdr = inject(ChangeDetectorRef);

  // Readonly fields prevent accidental mutation
  users$ = this.userService.getUsers();
}
```

**NEVER**:
```typescript
// ❌ Old pattern (constructor injection)
export class UserListComponent {
  constructor(
    private userService: UserService,
    private logger: NgxLogger
  ) {}
}
```

## Forms

**STRONGLY TYPED FORMS**:
```typescript
interface UserFormModel {
  email: string | null;
  firstName: string | null;
  lastName: string | null;
  password: string | null;
}

export class UserFormComponent {
  form = new FormGroup<{ [K in keyof UserFormModel]: FormControl<UserFormModel[K]> }>({
    email: new FormControl<string | null>(null, [
      Validators.required,
      Validators.email,
    ]),
    firstName: new FormControl<string | null>(null, [Validators.required]),
    lastName: new FormControl<string | null>(null, [Validators.required]),
    password: new FormControl<string | null>(null, [
      Validators.required,
      Validators.minLength(8),
    ]),
  });

  onSubmit(): void {
    if (this.form.invalid) return;

    const formValue = this.form.getRawValue(); // Fully typed!
    this.userService.createUser(formValue).subscribe(/* ... */);
  }
}
```

**ALWAYS**:
- Type form values with `FormGroup<T>`
- Use `Validators` for input validation
- Validate on blur or submit (not on every keystroke)

**NEVER**:
- Untyped forms (`FormGroup()` without generic)
- Validate in template
- Use `form.value as SomeType` (loses typing)

## Signals & State

**MODERN PATTERN (Signals)**:
```typescript
import { Component, signal, computed, effect } from '@angular/core';

@Component({
  selector: 'app-counter',
  standalone: true,
  template: `
    <button (click)="increment()">{{ count() }}</button>
    <p>Double: {{ doubleCount() }}</p>
  `,
})
export class CounterComponent {
  count = signal(0);
  doubleCount = computed(() => this.count() * 2);

  constructor() {
    effect(() => {
      console.log(`Count changed to: ${this.count()}`);
    });
  }

  increment(): void {
    this.count.update(c => c + 1);
  }
}
```

**WHEN TO USE**:
- Local component state → Signals
- Shared state → Services + Signals or State Management

**NEVER**:
- Use `BehaviorSubject` for simple state (use Signals instead)
- Create global state in components (use services)

## RxJS / Observables

**BEST PRACTICES**:
```typescript
export class UserDetailComponent {
  private readonly userService = inject(UserService);
  private readonly activatedRoute = inject(ActivatedRoute);
  private readonly destroy$ = new Subject<void>();

  user$: Observable<User> = this.activatedRoute.paramMap.pipe(
    switchMap(params => this.userService.getUserById(params.get('id')!)),
    catchError(error => {
      console.error('Error loading user', error);
      return of(null);
    }),
    takeUntilDestroyed(this.destroyRef),  // Modern way
  );

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

**ALWAYS**:
- Use `takeUntilDestroyed()` (modern) or `takeUntil(destroy$)`
- Use `async` pipe in templates (automatic unsubscribe)
- Use `switchMap` for dependent observables
- Use `catchError` for error handling

**NEVER**:
- Subscribe manually without unsubscribe
- Use `.subscribe()` in component.ts (use `async` pipe)
- Forget to unsubscribe (memory leaks)
- Use `merge` when `switchMap` is appropriate

## HTTP

**EXAMPLE**:
```typescript
@Injectable({ providedIn: 'root' })
export class UserService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = '/api/v1/users';

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(this.baseUrl).pipe(
      catchError(error => {
        console.error('Failed to load users', error);
        return of([]);
      }),
    );
  }

  getUserById(id: number): Observable<User> {
    return this.http.get<User>(`${this.baseUrl}/${id}`).pipe(
      catchError(error => {
        console.error(`Failed to load user ${id}`, error);
        throw error;
      }),
    );
  }

  createUser(user: CreateUserRequest): Observable<User> {
    return this.http.post<User>(this.baseUrl, user).pipe(
      tap(newUser => console.log('User created:', newUser)),
      catchError(error => {
        console.error('Failed to create user', error);
        throw error;
      }),
    );
  }
}
```

**ALWAYS**:
- Type all HTTP responses (`<T>` generic)
- Use `catchError` for error handling
- Use `tap` for side effects (logging, etc.)
- Provide in root or component

**NEVER**:
- Untyped HTTP responses (`this.http.get()` without `<T>`)
- Swallow errors silently
- Make HTTP calls directly in components

## Routing

**LAZY LOADING**:
```typescript
export const routes: Routes = [
  {
    path: 'users',
    loadComponent: () => import('./users/user-list.component').then(m => m.UserListComponent),
    children: [
      {
        path: ':id',
        loadComponent: () => import('./users/user-detail.component').then(m => m.UserDetailComponent),
      },
    ],
  },
  {
    path: 'admin',
    loadComponent: () => import('./admin/admin.component').then(m => m.AdminComponent),
    canActivate: [adminGuard],
  },
];
```

**ALWAYS**:
- Use `loadComponent` for lazy-loaded components
- Use route guards for protection
- Use data for route metadata
- Define routes once (in standalone or feature modules)

**GUARDS**:
```typescript
export const adminGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  if (authService.isAdmin()) {
    return true;
  }
  return inject(Router).createUrlTree(['/login']);
};
```

## DevExtreme Integration

**DATAGRID**:
```typescript
import { DxDataGridModule } from 'devextreme-angular';

@Component({
  selector: 'app-user-grid',
  standalone: true,
  imports: [DxDataGridModule],
  template: `
    <dx-data-grid
      [dataSource]="users$ | async"
      [columns]="columns"
      [paging]="{ pageSize: 10 }"
      [selection]="{ mode: 'single' }"
      (onSelectionChanged)="onSelectionChanged($event)"
    ></dx-data-grid>
  `,
})
export class UserGridComponent {
  users$ = inject(UserService).getUsers();

  columns = [
    { dataField: 'userId', caption: 'ID', width: 80 },
    { dataField: 'email', caption: 'Email', width: 200 },
    { dataField: 'firstName', caption: 'First Name', width: 150 },
    { dataField: 'lastName', caption: 'Last Name', width: 150 },
  ];

  onSelectionChanged(event: any): void {
    console.log('Selected user:', event.selectedRowsData[0]);
  }
}
```

**ALWAYS**:
- Define columns explicitly (don't auto-generate)
- Use `async` pipe for data binding
- Configure paging, sorting, filtering
- Use `dataField` to match model properties

## Styling

**CSS BEM CONVENTION**:
```scss
// Block
.sw-user-card {
  border: 1px solid #ccc;
  padding: 16px;

  // Element
  &__header {
    display: flex;
    justify-content: space-between;
  }

  &__title {
    font-size: 18px;
    font-weight: bold;
  }

  // Modifier
  &--active {
    border-color: green;
  }
}
```

**TEMPLATE**:
```html
<div class="sw-user-card sw-user-card--active">
  <div class="sw-user-card__header">
    <h2 class="sw-user-card__title">{{ user.name }}</h2>
  </div>
</div>
```

**ALWAYS**:
- Use `sw-` prefix for SmartWorkz styles
- Use BEM naming (block__element--modifier)
- Scope styles to component
- Use `::ng-deep` only as last resort

## Testing

**EXAMPLE**:
```typescript
describe('UserListComponent', () => {
  let component: UserListComponent;
  let fixture: ComponentFixture<UserListComponent>;
  let userService: jasmine.SpyObj<UserService>;

  beforeEach(async () => {
    const spy = jasmine.createSpyObj('UserService', ['getUsers']);
    await TestBed.configureTestingModule({
      imports: [UserListComponent],
      providers: [{ provide: UserService, useValue: spy }],
    }).compileComponents();

    userService = TestBed.inject(UserService) as jasmine.SpyObj<UserService>;
    fixture = TestBed.createComponent(UserListComponent);
    component = fixture.componentInstance;
  });

  it('should display users', (done) => {
    const mockUsers: User[] = [{ id: 1, name: 'John' }];
    userService.getUsers.and.returnValue(of(mockUsers));

    fixture.detectChanges();
    fixture.whenStable().then(() => {
      expect(component.users$).toBeDefined();
      done();
    });
  });
});
```

---

**Last Updated**: 2026-04-09

