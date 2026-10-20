---
name: angular-core
description: "Angular patterns and testable architecture"
allowed-tools: []
---

# Hevery: Testable Architecture

Miško Hevery's core belief: **If it's hard to test, it's hard to use.** Testability is not a feature—it's a design constraint that produces better architecture.

## The Foundational Principle

> "The secret to writing testable code is to write code that is easy to test."

This sounds circular but isn't. Code that's easy to test has:
- Clear inputs and outputs
- No hidden dependencies
- Single responsibilities
- Explicit state management

## Core Principles

### 1. Dependency Injection Is Architecture

DI isn't just a pattern—it's the foundation of maintainable systems.

**Not this:**
```typescript
class UserService {
  private http = new HttpClient();  // Hidden dependency
  private cache = new CacheService();  // Hidden dependency

  getUser(id: string) {
    return this.http.get(`/users/${id}`);
  }
}
```

**This:**
```typescript
@Injectable({ providedIn: 'root' })
class UserService {
  constructor(
    private http: HttpClient,  // Explicit, injectable
    private cache: CacheService  // Explicit, injectable
  ) {}

  getUser(id: string) {
    return this.http.get(`/users/${id}`);
  }
}
```

**Why it matters:**
- Tests can provide mocks
- Dependencies are visible in constructor
- Swapping implementations is trivial
- Circular dependencies are caught at compile time

### 2. The Law of Demeter for DI

Only inject what you directly use. Don't inject a service to get another service.

**Not this:**
```typescript
class OrderComponent {
  constructor(private userService: UserService) {}

  getDiscount() {
    // Reaching through userService to get pricingService
    return this.userService.pricingService.calculateDiscount();
  }
}
```

**This:**
```typescript
class OrderComponent {
  constructor(private pricingService: PricingService) {}

  getDiscount() {
    return this.pricingService.calculateDiscount();
  }
}
```

### 3. Constructor Does Nothing

Constructors are for assignment only. No logic, no calls, no initialization.

**Not this:**
```typescript
class DashboardComponent {
  data: any[];

  constructor(private api: ApiService) {
    this.data = this.api.fetchData();  // Logic in constructor
    this.processData();  // Method call in constructor
  }
}
```

**This:**
```typescript
class DashboardComponent implements OnInit {
  data: any[];

  constructor(private api: ApiService) {}  // Assignment only

  ngOnInit() {
    this.api.fetchData().subscribe(data => {
      this.data = this.processData(data);
    });
  }
}
```

**Why:** Constructors run during DI resolution. Side effects there are:
- Hard to test (can't construct without triggering)
- Order-dependent (which service constructs first?)
- Error-prone (what if API fails during construction?)

### 4. Prefer Composition Over Inheritance in Components

Angular components should compose, not inherit.

**Not this:**
```typescript
class BaseTableComponent {
  sort() { /* ... */ }
  filter() { /* ... */ }
  paginate() { /* ... */ }
}

class UserTableComponent extends BaseTableComponent {
  // Inherits everything, even what it doesn't need
}
```

**This:**
```typescript
// Composable services
@Injectable()
class SortService { sort<T>(data: T[]) { /* ... */ } }

@Injectable()
class FilterService { filter<T>(data: T[]) { /* ... */ } }

class UserTableComponent {
  constructor(
    private sortService: SortService,
    private filterService: FilterService
    // Only inject what you need
  ) {}
}
```

### 5. Smart Components vs Presentational Components

Separate concerns: Smart components manage state, presentational components render.

```
SMART COMPONENT              PRESENTATIONAL COMPONENT
──────────────              ────────────────────────
Knows about services        Knows only @Input/@Output
Manages state               Stateless (mostly)
Handles side effects        Pure rendering
Few in app                  Many in app
Hard to test                Easy to test
```

**Example:**
```typescript
// Smart component - has dependencies
@Component({
  template: `<user-card [user]="user$ | async" (delete)="onDelete($event)">`
})
class UserContainerComponent {
  user$ = this.store.select(selectCurrentUser);
  constructor(private store: Store) {}
  onDelete(userId: string) { this.store.dispatch(deleteUser({ userId })); }
}

// Presentational component - pure I/O
@Component({
  template: `<div>{{user.name}}</div><button (click)="delete.emit(user.id)">Delete</button>`
})
class UserCardComponent {
  @Input() user: User;
  @Output() delete = new EventEmitter<string>();
}
```

### 6. Avoid Global State

Global state (window, localStorage, static variables) breaks testability.

**Not this:**
```typescript
class ThemeService {
  getTheme() {
    return localStorage.getItem('theme');  // Global state
  }
}
```

**This:**
```typescript
// Abstract the global behind an injectable token
const STORAGE = new InjectionToken<Storage>('storage');

@Injectable()
class ThemeService {
  constructor(@Inject(STORAGE) private storage: Storage) {}

  getTheme() {
    return this.storage.getItem('theme');
  }
}

// In tests: provide mock storage
// In app: provide localStorage
```

### 7. Signals and Fine-Grained Reactivity

With Angular's signals, prefer fine-grained reactivity over coarse change detection.

```typescript
// Modern Angular with signals
@Component({
  template: `
    <div>Count: {{ count() }}</div>
    <div>Doubled: {{ doubled() }}</div>
  `
})
class CounterComponent {
  count = signal(0);
  doubled = computed(() => this.count() * 2);

  increment() {
    this.count.update(c => c + 1);
  }
}
```

**Benefits:**
- No zone.js overhead
- Precise update tracking
- Better performance
- Easier to reason about

## The Hevery Test

Before committing any Angular code, ask:

1. **Can I test this in isolation?** Without setting up the entire app?
2. **Are all dependencies explicit?** Visible in the constructor?
3. **Is the constructor boring?** Just assignments, no logic?
4. **Can I swap implementations?** For testing or different environments?
5. **Is this component smart or presentational?** And is it correctly categorized?
6. **Am I reaching through services?** Or injecting what I directly need?

## When Reviewing Code

Apply these checks:

- [ ] All dependencies injected via constructor
- [ ] No `new` keyword for services (except DTOs/models)
- [ ] Constructor contains only assignments
- [ ] No global state access (window, localStorage, static)
- [ ] Smart/presentational separation maintained
- [ ] Services are tree-shakeable (`providedIn: 'root'` or explicit providers)
- [ ] No logic in templates beyond simple expressions
- [ ] Signals used for new reactive state

## When NOT to Use This Skill

Use a different skill when:
- **Applying design patterns** → Use `design-patterns`
- **Writing Java code** → Use `java` (similar DI principles, different idioms)
- **General code clarity** → Use `clarity`
- **Performance optimization** → Use `angular-perf`

Hevery is the **Angular architecture skill**—use it for DI, testability, and component design.

## Sources

- Hevery, "Misko's Guide to Writing Testable Code" (Google internal, widely shared)
- Angular documentation (authored/influenced by Hevery)
- "Angular: Up and Running" - Shyam Seshadri
- Angular team design documents and RFCs

---

*"The key to testability is the ability to construct the object under test in isolation."* — Miško Hevery
