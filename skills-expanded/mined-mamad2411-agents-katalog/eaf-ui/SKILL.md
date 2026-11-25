---
name: eaf-ui
description: Expert guidance for developing, maintaining, and extending EAF (Enterprise Application Foundation) UI using Angular 18, TypeScript 5.2, PrimeNG 17, and RxJS 7. Covers standalone components, signals, reactive forms, HTTP services, authentication, route guards, data tables, and EAF-specific UI patterns. Use this skill when creating Angular components, implementing authentication flows, building data tables with PrimeNG, configuring routing, or troubleshooting frontend issues. Do NOT use for backend API development, database work, or non-Angular frontend frameworks.
---

# EAF UI Development Skill

You are an expert in EAF (Enterprise Application Foundation) UI development using Angular 18. You develop, maintain, and extend the Angular frontend that consumes EAF APIs. You write functional, maintainable, performant, and scalable UI code following Angular and TypeScript best practices.

## Project Context

EAF is an open source middleware platform built on ASP.NET Boilerplate (ABP). The UI layer provides a modern Angular 18 frontend for consuming EAF REST APIs.

### Technology Stack
- **Angular Version**: 18
- **TypeScript Version**: 5.2
- **Node.js Version**: 20.20.0
- **UI Framework**: Bootstrap 5
- **Component Library**: PrimeNG 17
- **Charts**: Chart.js
- **Reactive Programming**: RxJS 7
- **Build Tool**: Angular CLI
- **State Management**: RxJS with NgRx (optional)
- **HTTP**: Angular HttpClient

### Project Structure

```
angular/
├── src/
│   ├── app/
│   │   ├── components/        # Reusable components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API services
│   │   ├── models/           # TypeScript interfaces
│   │   ├── guards/           # Route guards
│   │   ├── interceptors/     # HTTP interceptors
│   │   ├── shared/           # Shared modules
│   │   ├── layout/           # Layout components
│   │   └── core/             # Core services (auth, session)
│   ├── assets/               # Static assets
│   ├── environments/         # Environment configs
│   └── styles/               # Global styles
├── angular.json              # Angular CLI config
├── package.json              # Dependencies
└── tsconfig.json             # TypeScript config
```

## Angular 19 Best Practices

### Standalone Components

Angular 19 uses standalone components by default:

```typescript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-user-list',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="user-list">
      <!-- Template -->
    </div>
  `,
  styles: [`
    .user-list { /* styles */ }
  `]
})
export class UserListComponent {
  // Component logic
}
```

### Signals (Reactive State)

Use Angular signals for reactive state management:

```typescript
import { Component, signal, computed, effect } from '@angular/core';

@Component({
  selector: 'app-user-profile',
  standalone: true,
  template: `
    <h2>{{ name() }}</h2>
    <p>Email: {{ email() }}</p>
    <p>Display Name: {{ displayName() }}</p>
  `
})
export class UserProfileComponent {
  private name = signal('John Doe');
  private email = signal('john@example.com');
  
  displayName = computed(() => `${this.name()} (${this.email()})`);
  
  constructor() {
    effect(() => {
      console.log('Name changed:', this.name());
    });
  }
  
  updateName(newName: string) {
    this.name.set(newName);
  }
}
```

### Services with Dependency Injection

```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl = 'api/services/app/user';
  
  constructor(private http: HttpClient) {}
  
  getAll(input: GetAllUsersInput): Observable<PagedResultDto<UserDto>> {
    return this.http.post<PagedResultDto<UserDto>>(
      `${this.apiUrl}/all`,
      input
    );
  }
  
  create(input: CreateUserDto): Observable<UserDto> {
    return this.http.post<UserDto>(
      `${this.apiUrl}/create`,
      input
    );
  }
  
  delete(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }
}
```

## EAF-Specific UI Patterns

### Authentication Service

```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { map, tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'api/TokenAuth';
  private currentUserSubject = new BehaviorSubject<UserDto | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();
  
  constructor(private http: HttpClient) {}
  
  login(credentials: LoginModel): Observable<AuthenticateResultModel> {
    return this.http.post<AuthenticateResultModel>(
      `${this.apiUrl}/Authenticate`,
      credentials
    ).pipe(
      tap(result => {
        if (result.success) {
          localStorage.setItem('token', result.result.accessToken);
          this.currentUserSubject.next(result.result);
        }
      })
    );
  }
  
  logout(): void {
    localStorage.removeItem('token');
    this.currentUserSubject.next(null);
  }
  
  isAuthenticated(): boolean {
    return !!localStorage.getItem('token');
  }
  
  getCurrentUser(): UserDto | null {
    return this.currentUserSubject.value;
  }
}
```

### HTTP Interceptor for JWT

```typescript
import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor
} from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable()
export class JwtInterceptor implements HttpInterceptor {
  intercept(
    request: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    const token = localStorage.getItem('token');
    
    if (token) {
      request = request.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`
        }
      });
    }
    
    return next.handle(request);
  }
}
```

### Route Guards

```typescript
import { inject } from '@angular/core';
import {
  CanActivateFn,
  Router,
  ActivatedRouteSnapshot,
  RouterStateSnapshot
} from '@angular/router';
import { AuthService } from '../services/auth.service';

export const authGuard: CanActivateFn = (
  route: ActivatedRouteSnapshot,
  state: RouterStateSnapshot
) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  
  if (authService.isAuthenticated()) {
    return true;
  }
  
  router.navigate(['/login'], { queryParams: { returnUrl: state.url } });
  return false;
};

export const permissionGuard: CanActivateFn = (
  route: ActivatedRouteSnapshot,
  state: RouterStateSnapshot
) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  
  const requiredPermission = route.data['permission'];
  
  if (!requiredPermission || authService.hasPermission(requiredPermission)) {
    return true;
  }
  
  router.navigate(['/access-denied']);
  return false;
};
```

### Data Tables with PrimeNG

```typescript
import { Component, OnInit } from '@angular/core';
import { TableModule } from 'primeng/table';
import { UserService } from '../services/user.service';
import { UserDto, GetAllUsersInput } from '../models/user.models';

@Component({
  selector: 'app-user-list',
  standalone: true,
  imports: [TableModule, CommonModule],
  template: `
    <p-table [value]="users" [paginator]="true" [rows]="10">
      <ng-template pTemplate="header">
        <tr>
          <th>Name</th>
          <th>Email</th>
          <th>Actions</th>
        </tr>
      </ng-template>
      <ng-template pTemplate="body" let-user>
        <tr>
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
          <td>
            <button (click)="editUser(user.id)">Edit</button>
            <button (click)="deleteUser(user.id)">Delete</button>
          </td>
        </tr>
      </ng-template>
    </p-table>
  `
})
export class UserListComponent implements OnInit {
  users: UserDto[] = [];
  loading = true;
  
  constructor(private userService: UserService) {}
  
  ngOnInit(): void {
    this.loadUsers();
  }
  
  loadUsers(): void {
    this.userService.getAll({ skipCount: 0, maxResultCount: 10 })
      .subscribe({
        next: (result) => {
          this.users = result.items;
          this.loading = false;
        },
        error: (error) => {
          console.error('Error loading users:', error);
          this.loading = false;
        }
      });
  }
  
  editUser(id: string): void {
    // Navigate to edit page
  }
  
  deleteUser(id: string): void {
    this.userService.delete(id).subscribe({
      next: () => {
        this.loadUsers();
      },
      error: (error) => {
        console.error('Error deleting user:', error);
      }
    });
  }
}
```

### Forms with Reactive Forms

```typescript
import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  ReactiveFormsModule,
  FormBuilder,
  FormGroup,
  Validators
} from '@angular/forms';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-user-create',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <form [formGroup]="userForm" (ngSubmit)="onSubmit()">
      <div>
        <label for="name">Name:</label>
        <input id="name" formControlName="name">
        <div *ngIf="userForm.get('name')?.invalid && userForm.get('name')?.touched">
          Name is required
        </div>
      </div>
      
      <div>
        <label for="email">Email:</label>
        <input id="email" formControlName="email">
        <div *ngIf="userForm.get('email')?.invalid && userForm.get('email')?.touched">
          Invalid email format
        </div>
      </div>
      
      <button type="submit" [disabled]="userForm.invalid">Create User</button>
    </form>
  `
})
export class UserCreateComponent {
  private fb = inject(FormBuilder);
  private userService = inject(UserService);
  
  userForm: FormGroup;
  
  constructor() {
    this.userForm = this.fb.group({
      name: ['', [Validators.required, Validators.maxLength(100)]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]]
    });
  }
  
  onSubmit(): void {
    if (this.userForm.valid) {
      this.userService.create(this.userForm.value).subscribe({
        next: (result) => {
          console.log('User created:', result);
          // Navigate or show success message
        },
        error: (error) => {
          console.error('Error creating user:', error);
        }
      });
    }
  }
}
```

## Component Patterns

### Smart vs Dumb Components

**Smart Component (Container)**:
```typescript
import { Component, inject } from '@angular/core';
import { UserService } from '../services/user.service';
import { UserDto } from '../models/user.models';

@Component({
  selector: 'app-user-container',
  standalone: true,
  template: `
    <app-user-list
      [users]="users()"
      [loading]="loading()"
      (userEdit)="onEditUser($event)"
      (userDelete)="onDeleteUser($event)"
    ></app-user-list>
  `
})
export class UserContainerComponent {
  private userService = inject(UserService);
  
  users = signal<UserDto[]>([]);
  loading = signal(false);
  
  constructor() {
    this.loadUsers();
  }
  
  loadUsers(): void {
    this.loading.set(true);
    this.userService.getAll({ skipCount: 0, maxResultCount: 10 }).subscribe({
      next: (result) => {
        this.users.set(result.items);
        this.loading.set(false);
      },
      error: (error) => {
        console.error('Error loading users:', error);
        this.loading.set(false);
      }
    });
  }
  
  onEditUser(id: string): void {
    // Handle edit
  }
  
  onDeleteUser(id: string): void {
    this.userService.delete(id).subscribe({
      next: () => this.loadUsers(),
      error: (error) => console.error('Error deleting user:', error)
    });
  }
}
```

**Dumb Component (Presentation)**:
```typescript
import { Component, input, output } from '@angular/core';
import { UserDto } from '../models/user.models';

@Component({
  selector: 'app-user-list',
  standalone: true,
  template: `
    <div *ngIf="loading()">Loading...</div>
    <ul *ngIf="!loading()">
      <li *ngFor="let user of users()">
        {{ user.name }} - {{ user.email }}
        <button (click)="userEdit.emit(user.id)">Edit</button>
        <button (click)="userDelete.emit(user.id)">Delete</button>
      </li>
    </ul>
  `
})
export class UserListComponent {
  users = input<UserDto[]>([]);
  loading = input<boolean>(false);
  userEdit = output<string>();
  userDelete = output<string>();
}
```

### Content Projection

```typescript
import { Component } from '@angular/core';

@Component({
  selector: 'app-card',
  standalone: true,
  template: `
    <div class="card">
      <div class="card-header">
        <ng-content select="[card-header]"></ng-content>
      </div>
      <div class="card-body">
        <ng-content select="[card-body]"></ng-content>
      </div>
      <div class="card-footer">
        <ng-content select="[card-footer]"></ng-content>
      </div>
    </div>
  `
})
export class CardComponent {}
```

Usage:
```html
<app-card>
  <div card-header>User Profile</div>
  <div card-body>John Doe</div>
  <div card-footer>Save</div>
</app-card>
```

## Routing

### Route Configuration

```typescript
import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    redirectTo: '/dashboard',
    pathMatch: 'full'
  },
  {
    path: 'login',
    loadComponent: () => import('./pages/login/login.component').then(m => m.LoginComponent)
  },
  {
    path: 'dashboard',
    loadComponent: () => import('./pages/dashboard/dashboard.component').then(m => m.DashboardComponent),
    canActivate: [authGuard]
  },
  {
    path: 'users',
    loadComponent: () => import('./pages/users/user-list/user-list.component').then(m => m.UserListComponent),
    canActivate: [authGuard, permissionGuard],
    data: { permission: 'Pages.Users' }
  },
  {
    path: 'users/:id',
    loadComponent: () => import('./pages/users/user-detail/user-detail.component').then(m => m.UserDetailComponent),
    canActivate: [authGuard]
  },
  {
    path: '**',
    loadComponent: () => import('./pages/not-found/not-found.component').then(m => m.NotFoundComponent)
  }
];
```

### Lazy Loading

```typescript
{
  path: 'admin',
  loadChildren: () => import('./modules/admin/admin.routes').then(m => m.adminRoutes)
}
```

## State Management

### Using Signals for Local State

```typescript
import { Component, signal, computed, effect } from '@angular/core';

@Component({
  selector: 'app-user-detail',
  standalone: true,
  template: `
    <div *ngIf="loading()">Loading...</div>
    <div *ngIf="error()">{{ error() }}</div>
    <div *ngIf="user()">
      <h2>{{ user()?.name }}</h2>
      <p>{{ user()?.email }}</p>
    </div>
  `
})
export class UserDetailComponent {
  user = signal<UserDto | null>(null);
  loading = signal(false);
  error = signal<string | null>(null);
  
  hasError = computed(() => !!this.error());
  
  loadUser(id: string): void {
    this.loading.set(true);
    this.error.set(null);
    
    this.userService.getUser(id).subscribe({
      next: (result) => {
        this.user.set(result);
        this.loading.set(false);
      },
      error: (err) => {
        this.error.set('Failed to load user');
        this.loading.set(false);
      }
    });
  }
}
```

## Testing

### Component Tests

```typescript
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { UserListComponent } from './user-list.component';
import { UserService } from '../services/user.service';
import { of } from 'rxjs';

describe('UserListComponent', () => {
  let component: UserListComponent;
  let fixture: ComponentFixture<UserListComponent>;
  let userServiceSpy: jasmine.SpyObj<UserService>;
  
  beforeEach(async () => {
    const spy = jasmine.createSpyObj('UserService', ['getAll']);
    
    await TestBed.configureTestingModule({
      imports: [UserListComponent],
      providers: [
        { provide: UserService, useValue: spy }
      ]
    }).compileComponents();
    
    fixture = TestBed.createComponent(UserListComponent);
    component = fixture.componentInstance;
    userServiceSpy = TestBed.inject(UserService) as jasmine.SpyObj<UserService>;
  });
  
  it('should create', () => {
    expect(component).toBeTruthy();
  });
  
  it('should load users on init', () => {
    const mockUsers = [{ id: '1', name: 'John', email: 'john@example.com' }];
    userServiceSpy.getAll.and.returnValue(of({ items: mockUsers, totalCount: 1 }));
    
    component.ngOnInit();
    fixture.detectChanges();
    
    expect(component.users()).toEqual(mockUsers);
    expect(component.loading()).toBe(false);
  });
});
```

### Service Tests

```typescript
import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { UserService } from './user.service';

describe('UserService', () => {
  let service: UserService;
  let httpMock: HttpTestingController;
  
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [UserService]
    });
    
    service = TestBed.inject(UserService);
    httpMock = TestBed.inject(HttpTestingController);
  });
  
  afterEach(() => {
    httpMock.verify();
  });
  
  it('should be created', () => {
    expect(service).toBeTruthy();
  });
  
  it('should get all users', () => {
    const mockUsers = { items: [], totalCount: 0 };
    
    service.getAll({}).subscribe(result => {
      expect(result).toEqual(mockUsers);
    });
    
    const req = httpMock.expectOne('api/services/app/user/all');
    expect(req.request.method).toBe('POST');
    req.flush(mockUsers);
  });
});
```

## Performance Optimization

### OnPush Change Detection

```typescript
import { Component, ChangeDetectionStrategy } from '@angular/core';

@Component({
  selector: 'app-user-list',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `<!-- template -->`
})
export class UserListComponent {}
```

### TrackBy in ngFor

```html
<div *ngFor="let user of users(); trackBy: trackById">
  {{ user.name }}
</div>
```

```typescript
trackById(index: number, user: UserDto): string {
  return user.id;
}
```

### Lazy Loading Components

```typescript
import { loadComponent } from '@angular/elements';

// Load component on demand
async loadEditorComponent() {
  const { EditorComponent } = await import('./editor.component');
  // Use the component
}
```

## Best Practices

### TypeScript

```typescript
// Use interfaces for data models
interface UserDto {
  id: string;
  name: string;
  email: string;
}

// Use types for unions
type UserRole = 'admin' | 'user' | 'guest';

// Use enums for constants
enum UserStatus {
  Active = 'active',
  Inactive = 'inactive',
  Pending = 'pending'
}
```

### Error Handling

```typescript
this.userService.getAll({}).subscribe({
  next: (result) => {
    this.users.set(result.items);
  },
  error: (error) => {
    console.error('Error:', error);
    this.error.set('Failed to load users');
  },
  complete: () => {
    this.loading.set(false);
  }
});
```

### Accessibility

```html
<button [attr.aria-label]="buttonLabel">Click</button>
<input [attr.aria-required]="true">
<nav aria-label="Main navigation">
```

### Responsive Design

```scss
.user-list {
  @media (max-width: 768px) {
    flex-direction: column;
  }
}
```

## Common Issues and Solutions

### Memory Leaks

```typescript
import { DestroyRef } from '@angular/core';

@Component({
  selector: 'app-user-list',
  standalone: true
})
export class UserListComponent {
  private destroyRef = inject(DestroyRef);
  
  ngOnInit(): void {
    const subscription = this.userService.getAll({}).subscribe();
    
    this.destroyRef.onDestroy(() => {
      subscription.unsubscribe();
    });
  }
}
```

### Change Detection Issues

Use signals and OnPush change detection:
```typescript
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class MyComponent {
  data = signal([]);
}
```

### RxJS Memory Leaks

```typescript
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

this.userService.getAll({})
  .pipe(takeUntilDestroyed(this.destroyRef))
  .subscribe();
```

## When in Doubt

- Use standalone components
- Prefer signals over BehaviorSubjects
- Use OnPush change detection
- Keep components small and focused
- Use lazy loading for routes
- Test components and services
- Follow Angular style guide
- Use TypeScript strictly
- Handle errors gracefully
- Optimize for performance
