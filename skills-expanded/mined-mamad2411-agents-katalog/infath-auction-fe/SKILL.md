# Angular Project - AI Development Guidelines

## Project Overview
This is a modern Angular application built with:
- Angular 19+ (Standalone Components)
- Zoneless change detection (Signals-based)
- Server-Side Rendering (SSR)
- PrimeNG component library
- Tailwind CSS for styling
- Template-driven forms

## Core Principles
1. **Simplicity First**: Code should be simple, readable, and maintainable
2. **Separation of Concerns**: Create reusable components and services
3. **Type Safety**: No `any` types allowed - everything must be properly typed
4. **Modern Angular**: Use latest Angular 19+ syntax and patterns
5. **Test Coverage**: Every generated code must have corresponding test functions in .spec file

---

## File Structure Requirements

### Component Files
Each component MUST have four files:
```
component-name/
├── component-name.ts        # Component logic
├── component-name.html      # Template
├── component-name.scss      # Styles
└── component-name.spec.ts   # Unit tests
```

**Never** use inline templates or inline styles except for very small, trivial components.

### Page Structure
Each page should have:
```
pages/page-name/
├── page-name.ts             # Page component
├── page-name.html           # Page template
├── page-name.scss           # Page styles
├── page-name.spec.ts        # Page tests
├── services/
│   └── page-name.service.ts # Page-specific service
└── interfaces/
    └── page-name.interface.ts # Page-specific interfaces
```

---

## Angular Best Practices

### 1. State Management - Use Signals (REQUIRED)
This is a **zoneless application**. All trackable state MUST use Angular Signals.

❌ **WRONG:**
```typescript
export class MyComponent {
  count = 0;
  user: User | null = null;
}
```

✅ **CORRECT:**
```typescript
export class MyComponent {
  count = signal(0);
  user = signal<User | null>(null);

  // Computed values
  doubleCount = computed(() => this.count() * 2);
}
```

### 2. Template Syntax - Modern Angular Control Flow
Always use Angular 19+ control flow syntax.

❌ **WRONG:**
```html
<div *ngIf="isLoggedIn">Welcome</div>
<div *ngFor="let item of items">{{ item }}</div>
<div [ngSwitch]="status">
  <div *ngSwitchCase="'active'">Active</div>
</div>
```

✅ **CORRECT:**
```html
@if (isLoggedIn()) {
  <div>Welcome</div>
}

@for (item of items(); track item.id) {
  <div>{{ item }}</div>
}

@switch (status()) {
  @case ('active') {
    <div>Active</div>
  }
  @default {
    <div>Unknown</div>
  }
}
```

### 3. Dependency Injection - Use inject() Function
Use the modern `inject()` function instead of constructor injection.

❌ **WRONG:**
```typescript
export class MyComponent {
  constructor(
    private userService: UserService,
    private router: Router
  ) {}
}
```

✅ **CORRECT:**
```typescript
export class MyComponent {
  private userService = inject(UserService);
  private router = inject(Router);
}
```

### 4. Service Injection Scope
Follow proper service injection hierarchy:

**Page-Specific Services:**
```typescript
@Injectable()  // No providedIn - inject in component
export class AuctionPageService {
  // Service used only in auction page
}

// In component:
@Component({
  providers: [AuctionPageService]  // Provide here
})
export class AuctionPage {
  private auctionService = inject(AuctionPageService);
}
```

**Project-Wide Services:**
```typescript
@Injectable({
  providedIn: 'root'  // Available everywhere
})
export class AuthService {
  // Service used across the application
}
```

### 5. Type Safety - No "any" Allowed
Every variable, parameter, and return type must be properly typed.

❌ **WRONG:**
```typescript
fetchData(): any {
  return this.http.get('/api/data');
}

processItems(items: any[]) {
  // ...
}
```

✅ **CORRECT:**
```typescript
// Create interface file
interface UserData {
  id: string;
  name: string;
  email: string;
}

fetchData(): Observable<UserData[]> {
  return this.http.get<UserData[]>('/api/data');
}

processItems(items: UserData[]): void {
  // ...
}
```

**Interface Organization:**
- Create `*.interface.ts` files per page/feature
- Use descriptive interface names
- Export all interfaces for reusability

### 6. API Calls - Exception Handling Required
ALL API calls must have proper error handling.

❌ **WRONG:**
```typescript
loadUsers(): void {
  this.http.get<User[]>('/api/users').subscribe(users => {
    this.users.set(users);
  });
}
```

✅ **CORRECT:**
```typescript
loadUsers(): void {
  this.http.get<User[]>('/api/users').subscribe({
    next: (users) => {
      this.users.set(users);
      this.error.set(null);
    },
    error: (error) => {
      console.error('Failed to load users:', error);
      this.error.set('Unable to load users. Please try again.');
      this.users.set([]);
    }
  });
}

// Or with async/await:
async loadUsers(): Promise<void> {
  try {
    const users = await firstValueFrom(
      this.http.get<User[]>('/api/users')
    );
    this.users.set(users);
    this.error.set(null);
  } catch (error) {
    console.error('Failed to load users:', error);
    this.error.set('Unable to load users. Please try again.');
    this.users.set([]);
  }
}
```

### 7. Forms - Template-Driven Only
Use template-driven forms, NOT reactive forms.

❌ **WRONG:**
```typescript
loginForm = new FormGroup({
  email: new FormControl(''),
  password: new FormControl('')
});
```

✅ **CORRECT:**
```typescript
// In component:
email = signal('');
password = signal('');

// In template:
<form #loginForm="ngForm" (ngSubmit)="onSubmit()">
  <input
    type="email"
    name="email"
    [(ngModel)]="email"
    required
    email
  />
  <input
    type="password"
    name="password"
    [(ngModel)]="password"
    required
    minlength="6"
  />
  <button type="submit" [disabled]="loginForm.invalid">Submit</button>
</form>
```

---

## UI Component Library - PrimeNG

### Component Usage
ALL UI components must use PrimeNG. Do not create custom buttons, inputs, tables, etc.

✅ **CORRECT:**
```typescript
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { TableModule } from 'primeng/table';
import { CardModule } from 'primeng/card';

@Component({
  imports: [ButtonModule, InputTextModule, TableModule, CardModule]
})
```

```html
<p-button label="Submit" icon="pi pi-check"></p-button>
<p-inputText [(ngModel)]="value" placeholder="Enter text"></p-inputText>
<p-table [value]="items()"></p-table>
<p-card header="Title">Content</p-card>
```

### Common PrimeNG Components:
- Buttons: `<p-button>`
- Inputs: `<p-inputText>`, `<p-inputTextarea>`, `<p-password>`
- Dropdowns: `<p-dropdown>`, `<p-multiSelect>`
- Tables: `<p-table>`
- Dialogs: `<p-dialog>`
- Cards: `<p-card>`
- Menus: `<p-menubar>`, `<p-menu>`
- Messages: `<p-toast>`, `<p-message>`
- Progress: `<p-progressBar>`, `<p-progressSpinner>`

**Reference**: https://primeng.org/

---

## Styling - Tailwind CSS

### Utility Classes Only
Use Tailwind utility classes for all styling. Avoid custom CSS unless absolutely necessary.

✅ **CORRECT:**
```html
<div class="flex items-center justify-between p-4 bg-blue-500 rounded-lg shadow-md">
  <h1 class="text-2xl font-bold text-white">Title</h1>
  <button class="px-4 py-2 bg-white text-blue-500 rounded hover:bg-gray-100">
    Click Me
  </button>
</div>
```

### Custom Tailwind Values
If a utility doesn't exist, extend `tailwind.config.js` first:

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        'brand-primary': '#FF6B6B',
        'brand-secondary': '#4ECDC4',
      },
      spacing: {
        '128': '32rem',
      }
    }
  }
}
```

Then use it:
```html
<div class="bg-brand-primary p-128">Content</div>
```

### SCSS Files
Keep SCSS files minimal. Only use for:
1. PrimeNG theme overrides
2. Complex animations
3. Truly custom styles that can't be done with Tailwind

---

## SSR Considerations

### DO NOT Use localStorage
This application uses Server-Side Rendering. `localStorage` is not available on the server.

❌ **WRONG:**
```typescript
localStorage.setItem('token', token);
const user = localStorage.getItem('user');
```

✅ **CORRECT - Use Cookies:**
```typescript
import { inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';

export class AuthService {
  private platformId = inject(PLATFORM_ID);
  private isBrowser = isPlatformBrowser(this.platformId);

  setToken(token: string): void {
    if (this.isBrowser) {
      document.cookie = `token=${token}; path=/; secure; samesite=strict`;
    }
  }

  getToken(): string | null {
    if (!this.isBrowser) return null;

    const cookies = document.cookie.split(';');
    const tokenCookie = cookies.find(c => c.trim().startsWith('token='));
    return tokenCookie ? tokenCookie.split('=')[1] : null;
  }
}
```

### Platform Check Pattern
Always check platform before using browser-only APIs:

```typescript
import { inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';

export class MyService {
  private platformId = inject(PLATFORM_ID);

  doSomethingBrowserOnly(): void {
    if (isPlatformBrowser(this.platformId)) {
      // Safe to use window, document, localStorage, etc.
      window.scrollTo(0, 0);
    }
  }
}
```

---

## Component Reusability

### Create Reusable Components
Follow the Single Responsibility Principle. Extract reusable UI patterns.

**Example Structure:**
```
components/
├── shared/
│   ├── auction-card/          # Reusable auction card
│   ├── user-avatar/           # Reusable avatar
│   ├── loading-spinner/       # Reusable loader
│   └── error-message/         # Reusable error display
```

### Reusable Component Pattern:
```typescript
@Component({
  selector: 'app-auction-card',
  imports: [CardModule, ButtonModule],
  template: `
    <p-card>
      <h3 class="text-xl font-bold">{{ auction().title }}</h3>
      <p class="text-gray-600">{{ auction().description }}</p>
      <p-button
        label="Bid Now"
        (onClick)="onBid.emit(auction())"
      ></p-button>
    </p-card>
  `
})
export class AuctionCard {
  // Input as signal (Angular 19+)
  auction = input.required<Auction>();

  // Output
  onBid = output<Auction>();
}
```

Usage:
```html
@for (auction of auctions(); track auction.id) {
  <app-auction-card
    [auction]="auction"
    (onBid)="handleBid($event)"
  />
}
```

---

## Code Quality Standards

### 1. Readability
- Use descriptive variable names
- Keep functions small (max 20-30 lines)
- Add comments for complex logic
- Use blank lines to separate logical sections

### 2. Simplicity
- Avoid over-engineering
- Don't create abstractions until needed
- Prefer composition over inheritance
- Keep component logic simple

### 3. Consistency
- Follow existing patterns in the codebase
- Use consistent naming conventions
- Maintain consistent file structure

### 4. Error Messages
Make error messages user-friendly:
```typescript
// Bad
this.error.set(error);

// Good
this.error.set('Unable to load auctions. Please check your connection and try again.');
```

---

## Naming Conventions

### Files
- Components: `auction-list.ts`, `user-profile.ts`
- Services: `auction.service.ts`, `auth.service.ts`
- Interfaces: `auction.interface.ts`, `user.interface.ts`
- Guards: `auth.guard.ts`
- Pipes: `date-format.pipe.ts`

### Classes/Interfaces
- Components: `AuctionList`, `UserProfile`
- Services: `AuctionService`, `AuthService`
- Interfaces: `Auction`, `User`, `AuctionResponse`
- Guards: `authGuard` (functional), `AuthGuard` (class-based)

### Variables/Properties
- Signals: `count`, `userName`, `isLoading`
- Methods: `loadData()`, `handleSubmit()`, `onBidClick()`
- Private: `_internalState` (prefix with underscore)

---

## Testing Requirements

### Test Coverage (MANDATORY)
**Every piece of generated code MUST have corresponding test functions in the .spec file.**

- ✅ Each component method must have at least one test
- ✅ Each service method must have at least one test
- ✅ Each guard must have test cases for allowed and blocked scenarios
- ✅ Each pipe must have test cases for different input scenarios
- ✅ Test both success and error scenarios for API calls
- ✅ Test signal state changes and computed values

### Spec File Template
Every component must have a corresponding spec file:

```typescript
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AuctionList } from './auction-list';

describe('AuctionList', () => {
  let component: AuctionList;
  let fixture: ComponentFixture<AuctionList>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AuctionList]
    }).compileComponents();

    fixture = TestBed.createComponent(AuctionList);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should display auctions', () => {
    component.auctions.set([
      { id: '1', title: 'Test Auction', price: 100 }
    ]);
    fixture.detectChanges();

    const compiled = fixture.nativeElement;
    expect(compiled.querySelector('.auction-title')?.textContent)
      .toContain('Test Auction');
  });

  it('should load auctions on init', async () => {
    await component.loadAuctions();
    expect(component.auctions().length).toBeGreaterThan(0);
  });

  it('should handle loading state', async () => {
    expect(component.isLoading()).toBe(false);
    const loadPromise = component.loadAuctions();
    expect(component.isLoading()).toBe(true);
    await loadPromise;
    expect(component.isLoading()).toBe(false);
  });

  it('should handle errors gracefully', async () => {
    // Mock service to throw error
    spyOn(component['auctionService'], 'getAuctions').and.returnValue(
      throwError(() => new Error('API Error'))
    );

    await component.loadAuctions();
    expect(component.error()).toBeTruthy();
    expect(component.auctions()).toEqual([]);
  });
});
```

### Service Testing Template
Every service must have comprehensive tests:

```typescript
import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { AuctionListService } from './auction-list.service';
import { AuctionListResponse } from './auction-list.interface';

describe('AuctionListService', () => {
  let service: AuctionListService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [AuctionListService]
    });

    service = TestBed.inject(AuctionListService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should fetch auctions', () => {
    const mockResponse: AuctionListResponse = {
      auctions: [{ id: '1', title: 'Test', currentBid: 100 }],
      total: 1,
      page: 1
    };

    service.getAuctions().subscribe(response => {
      expect(response).toEqual(mockResponse);
      expect(response.auctions.length).toBe(1);
    });

    const req = httpMock.expectOne('/api/auctions?page=1');
    expect(req.request.method).toBe('GET');
    req.flush(mockResponse);
  });

  it('should handle errors', () => {
    service.getAuctions().subscribe({
      next: () => fail('should have failed'),
      error: (error) => {
        expect(error.status).toBe(500);
      }
    });

    const req = httpMock.expectOne('/api/auctions?page=1');
    req.flush('Error', { status: 500, statusText: 'Server Error' });
  });
});
```

### Guard Testing Template
Every guard must test both allow and deny scenarios:

```typescript
import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { authGuard } from './auth.guard';
import { AuthService } from '../services/auth.service';

describe('authGuard', () => {
  let authService: jasmine.SpyObj<AuthService>;
  let router: jasmine.SpyObj<Router>;

  beforeEach(() => {
    const authServiceSpy = jasmine.createSpyObj('AuthService', [
      'isAuthenticated',
      'setRedirectUrl'
    ]);
    const routerSpy = jasmine.createSpyObj('Router', ['createUrlTree']);

    TestBed.configureTestingModule({
      providers: [
        { provide: AuthService, useValue: authServiceSpy },
        { provide: Router, useValue: routerSpy }
      ]
    });

    authService = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;
    router = TestBed.inject(Router) as jasmine.SpyObj<Router>;
  });

  it('should allow authenticated users', () => {
    authService.isAuthenticated.and.returnValue(true);

    const result = TestBed.runInInjectionContext(() =>
      authGuard({} as any, { url: '/auctions' } as any)
    );

    expect(result).toBe(true);
  });

  it('should redirect unauthenticated users', () => {
    authService.isAuthenticated.and.returnValue(false);
    const urlTree = {} as any;
    router.createUrlTree.and.returnValue(urlTree);

    const result = TestBed.runInInjectionContext(() =>
      authGuard({} as any, { url: '/auctions' } as any)
    );

    expect(result).toBe(urlTree);
    expect(authService.setRedirectUrl).toHaveBeenCalledWith('/auctions');
    expect(router.createUrlTree).toHaveBeenCalledWith(['/login']);
  });
});
```

---

## Quick Reference Checklist

Before submitting any code, verify:

- [ ] Component has .ts, .html, .scss, and .spec.ts files
- [ ] All state uses Signals (`signal()`, `computed()`)
- [ ] Using `@if`, `@for`, `@switch` syntax (not `*ngIf`, `*ngFor`)
- [ ] Using `inject()` function (not constructor injection)
- [ ] Services have correct injection scope
- [ ] All API calls have try/catch or error handling
- [ ] No `any` types - all types properly defined
- [ ] Interfaces exist in separate `.interface.ts` files
- [ ] Using PrimeNG components (not custom UI)
- [ ] Using Tailwind utility classes for styling
- [ ] No inline styles
- [ ] Use custom styles in component scss file by minimal (if needed)
- [ ] Forms are template-driven (not reactive)
- [ ] Reusable components extracted where appropriate
- [ ] No `localStorage` usage - cookies used instead
- [ ] Code is simple and readable
- [ ] Platform checks for browser-only APIs
- [ ] **Every method/function has corresponding test in .spec file**
- [ ] **Tests cover both success and error scenarios**
- [ ] **Signal state changes are tested**

---

## Example: Complete Page Implementation

```typescript
// auction-list.interface.ts
export interface Auction {
  id: string;
  title: string;
  description: string;
  currentBid: number;
  endDate: Date;
  imageUrl: string;
}

export interface AuctionListResponse {
  auctions: Auction[];
  total: number;
  page: number;
}

// auction-list.service.ts
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuctionListResponse } from './auction-list.interface';

@Injectable()  // Page-specific service
export class AuctionListService {
  private http = inject(HttpClient);
  private apiUrl = '/api/auctions';

  getAuctions(page: number = 1): Observable<AuctionListResponse> {
    return this.http.get<AuctionListResponse>(
      `${this.apiUrl}?page=${page}`
    );
  }
}

// auction-list.ts
import { Component, signal, inject } from '@angular/core';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { CardModule } from 'primeng/card';
import { AuctionListService } from './auction-list.service';
import { Auction } from './auction-list.interface';

@Component({
  selector: 'app-auction-list',
  imports: [TableModule, ButtonModule, CardModule],
  providers: [AuctionListService],
  templateUrl: './auction-list.html',
  styleUrl: './auction-list.scss'
})
export class AuctionList {
  private auctionService = inject(AuctionListService);

  auctions = signal<Auction[]>([]);
  isLoading = signal(false);
  error = signal<string | null>(null);

  async ngOnInit(): Promise<void> {
    await this.loadAuctions();
  }

  async loadAuctions(): Promise<void> {
    this.isLoading.set(true);
    this.error.set(null);

    try {
      const response = await firstValueFrom(
        this.auctionService.getAuctions()
      );
      this.auctions.set(response.auctions);
    } catch (error) {
      console.error('Failed to load auctions:', error);
      this.error.set('Unable to load auctions. Please try again later.');
    } finally {
      this.isLoading.set(false);
    }
  }
}
```

```html
<!-- auction-list.html -->
<div class="container mx-auto p-4">
  <h1 class="text-3xl font-bold mb-6">Active Auctions</h1>

  @if (isLoading()) {
    <p-progressSpinner></p-progressSpinner>
  }

  @if (error()) {
    <p-message severity="error" [text]="error()!"></p-message>
  }

  @if (!isLoading() && !error()) {
    <p-table [value]="auctions()">
      <ng-template pTemplate="header">
        <tr>
          <th>Title</th>
          <th>Current Bid</th>
          <th>Actions</th>
        </tr>
      </ng-template>
      <ng-template pTemplate="body" let-auction>
        <tr>
          <td>{{ auction.title }}</td>
          <td class="font-bold text-green-600">
            \${{ auction.currentBid }}
          </td>
          <td>
            <p-button
              label="View"
              icon="pi pi-eye"
              size="small"
            ></p-button>
          </td>
        </tr>
      </ng-template>
    </p-table>
  }
</div>
```

---

## Additional Resources

- [Angular Documentation](https://angular.dev/)
- [Angular Signals Guide](https://angular.dev/guide/signals)
- [PrimeNG Components](https://primeng.org/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)

---

**Last Updated**: 2025-10-27
**Angular Version**: 19+
**Maintained By**: Development Team

