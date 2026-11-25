---
name: auth-pattern
version: 1.0.0
last_updated: 2026-06-05
description: Scaffold enterprise authentication and authorization patterns. Use when implementing JWT auth, role-based access control, realm-based permissions, or session management in web applications.
triggers:
  - /auth-pattern
  - implement authentication
  - add authorization
  - role-based access
  - realm permissions
  - JWT authentication
  - session management
---

# Enterprise Auth Pattern

Production-tested authentication and authorization patterns from IoT Admin Backend.

## When to Use

- Implementing JWT-based authentication
- Adding role-based access control (RBAC)
- Building realm-based permission systems
- Creating session state management
- Adding auth interceptors for API calls

## When NOT to Use

- Simple API key authentication (no roles needed)
- OAuth-only flows (use OAuth libraries instead)
- Serverless/stateless auth (no session needed)

---

## Quick Start

1. Choose auth pattern (JWT + Realms recommended)
2. Implement session state machine
3. Add auth interceptor for HTTP calls
4. Define realms and roles
5. Add route guards for protected pages
6. Test with positive/negative auth scenarios

---

## Core Patterns

### Pattern 1: Realm-Based Authorization

**The 3-tier hierarchy per resource:**

```
ADMIN ─┬─ Full access (create, read, update, delete, configure)
       │
EDIT  ─┼─ Modify access (create, read, update, delete)
       │
READ  ─┴─ View access (read only)
```

**Why this pattern diverges from standard RBAC:**
- Roles are scoped to realms (resources), not global
- Hierarchical inheritance (ADMIN includes EDIT, EDIT includes READ)
- Fine-grained without explosion of role combinations

**Implementation:**

```typescript
// Realm definition
export interface Realm {
  id: string;      // e.g., "users", "devices", "settings"
  name: string;
  roles: RealmRole[];
}

export enum RealmRole {
  ADMIN = 'admin',
  EDIT = 'edit',
  READ = 'read'
}

// User's realm assignments
export interface UserRealms {
  userId: string;
  realms: Realm[];
}

// Authorization check with hierarchy
function hasRole(userRealms: Realm[], realmId: string, requiredRole: RealmRole): boolean {
  const realm = userRealms.find(r => r.id === realmId);
  if (!realm) return false;

  // ADMIN has all permissions
  if (realm.roles.includes(RealmRole.ADMIN)) return true;

  // EDIT includes READ
  if (requiredRole === RealmRole.READ && realm.roles.includes(RealmRole.EDIT)) {
    return true;
  }

  return realm.roles.includes(requiredRole);
}
```

---

### Pattern 2: Session State Machine

**Type-safe state transitions:**

```
┌──────────────┐     login()      ┌───────────────┐
│ Disconnected │ ───────────────→ │   Connected   │
└──────────────┘                  └───────────────┘
       ↑                                 │
       │         logout() or            │
       └─────────────────────────────────┘
                  token expired
```

**Implementation:**

```typescript
// State interface
interface SessionState {
  isAuthenticated: boolean;
  connect(credentials: Credentials): Promise<void>;
  disconnect(): void;
  refresh(): Promise<void>;
}

// Disconnected state
class DisconnectedState implements SessionState {
  isAuthenticated = false;

  async connect(credentials: Credentials): Promise<void> {
    const tokens = await authService.login(credentials);
    session.transition(new ConnectedState(tokens));
  }

  disconnect(): void { /* no-op */ }
  refresh(): Promise<void> { return Promise.reject('Not authenticated'); }
}

// Connected state
class ConnectedState implements SessionState {
  isAuthenticated = true;

  constructor(private tokens: AuthTokens) {}

  connect(): Promise<void> { return Promise.resolve(); /* already connected */ }

  disconnect(): void {
    authService.logout();
    session.transition(new DisconnectedState());
  }

  async refresh(): Promise<void> {
    const newTokens = await authService.refresh(this.tokens.refreshToken);
    this.tokens = newTokens;
  }
}

// Session manager
class Session {
  private state: SessionState = new DisconnectedState();

  transition(newState: SessionState): void {
    this.state = newState;
  }

  get isAuthenticated(): boolean {
    return this.state.isAuthenticated;
  }
}
```

---

### Pattern 3: Auth Interceptor

**Automatic token injection + 401 handling:**

```typescript
class AuthInterceptor {
  private isRefreshing = false;
  private refreshQueue: Array<() => void> = [];

  async intercept(request: Request): Promise<Response> {
    // Skip public endpoints
    if (this.isPublicEndpoint(request.url)) {
      return fetch(request);
    }

    // Add token
    const authenticatedRequest = this.addToken(request);
    const response = await fetch(authenticatedRequest);

    // Handle 401
    if (response.status === 401) {
      return this.handle401(request);
    }

    return response;
  }

  private addToken(request: Request): Request {
    const token = session.accessToken;
    if (!token) return request;

    return new Request(request, {
      headers: {
        ...request.headers,
        'Authorization': `Bearer ${token}`
      }
    });
  }

  private async handle401(request: Request): Promise<Response> {
    // Prevent multiple simultaneous refreshes
    if (this.isRefreshing) {
      return new Promise(resolve => {
        this.refreshQueue.push(() => resolve(this.intercept(request)));
      });
    }

    this.isRefreshing = true;

    try {
      await session.refresh();
      this.processQueue();
      return this.intercept(request); // Retry with new token
    } catch (error) {
      session.disconnect();
      throw new AuthenticationError('Session expired');
    } finally {
      this.isRefreshing = false;
    }
  }

  private processQueue(): void {
    this.refreshQueue.forEach(callback => callback());
    this.refreshQueue = [];
  }
}
```

---

### Pattern 4: Route Guards

**Declarative route protection:**

```typescript
// Guard definition
function createAuthGuard(realm: string, role: RealmRole) {
  return (route: Route): boolean => {
    if (!session.isAuthenticated) {
      router.navigate('/login');
      return false;
    }

    if (!authorization.hasRole(realm, role)) {
      router.navigate('/unauthorized');
      return false;
    }

    return true;
  };
}

// Usage in routes
const routes = [
  {
    path: '/admin/users',
    component: UserListComponent,
    guard: createAuthGuard('users', RealmRole.EDIT)
  },
  {
    path: '/settings',
    component: SettingsComponent,
    guard: createAuthGuard('settings', RealmRole.ADMIN)
  },
  {
    path: '/dashboard',
    component: DashboardComponent,
    guard: createAuthGuard('dashboard', RealmRole.READ)
  }
];
```

---

### Pattern 5: JWT Token Handling

**Parse and validate JWTs client-side:**

```typescript
class WebToken {
  readonly header: JwtHeader;
  readonly payload: JwtPayload;
  readonly signature: string;

  static parse(token: string): WebToken {
    const [headerB64, payloadB64, signature] = token.split('.');
    return new WebToken(
      JSON.parse(atob(headerB64)),
      JSON.parse(atob(payloadB64)),
      signature
    );
  }

  isExpired(): boolean {
    // exp is in seconds, Date.now() is in milliseconds
    return Date.now() >= this.payload.exp * 1000;
  }

  expiresIn(): number {
    return this.payload.exp * 1000 - Date.now();
  }

  get userId(): string {
    return this.payload.sub;
  }

  get roles(): string[] {
    return this.payload.roles || [];
  }

  get realms(): Realm[] {
    return this.payload.realms || [];
  }
}

interface JwtPayload {
  sub: string;           // Subject (user ID)
  exp: number;           // Expiration (seconds since epoch)
  iat: number;           // Issued at
  roles?: string[];      // Global roles (optional)
  realms?: Realm[];      // Realm-scoped roles
}
```

---

## Procedure

### Step 1: Define Realms

Identify protected resources and their access levels:

```typescript
const realms = [
  { id: 'users', name: 'User Management', roles: ['admin', 'edit', 'read'] },
  { id: 'devices', name: 'Device Management', roles: ['admin', 'edit', 'read'] },
  { id: 'settings', name: 'System Settings', roles: ['admin'] },
  { id: 'reports', name: 'Reports', roles: ['read'] }
];
```

**Checkpoint**: Each resource has clear access levels defined.

### Step 2: Implement Session

Create session state machine with login/logout/refresh.

**Checkpoint**: Can log in, log out, and refresh tokens programmatically.

### Step 3: Add Interceptor

Implement auth interceptor for HTTP client.

**Checkpoint**: Requests include Authorization header, 401s trigger refresh.

### Step 4: Create Authorization Service

Implement hasRole() with hierarchy support.

**Checkpoint**: ADMIN implies EDIT, EDIT implies READ.

### Step 5: Add Route Guards

Protect routes with realm/role requirements.

**Checkpoint**: Unauthorized users redirected, authorized users access granted.

### Step 6: Test Auth Flows

| Scenario | Expected Result |
|----------|----------------|
| Valid credentials | Login succeeds, token stored |
| Invalid credentials | Login fails, error shown |
| Expired token | Auto-refresh, request retried |
| Refresh fails | Logout, redirect to login |
| Missing realm | Access denied (403) |
| Insufficient role | Access denied (403) |

---

## Failure Modes & Recovery

| Issue | Recovery |
|-------|----------|
| Token expired during request | Interceptor auto-refreshes and retries |
| Refresh token expired | Force logout, redirect to login |
| Missing realm assignment | Show "Contact admin for access" |
| API returns 403 | Check realm/role, update UI accordingly |
| Network error during refresh | Queue requests, retry on reconnect |

---

## Security Considerations

### Token Storage
- **Recommended**: HttpOnly cookies (immune to XSS)
- **Alternative**: Memory only (lost on refresh)
- **Avoid**: localStorage (vulnerable to XSS)

### Token Refresh
- Refresh before expiration (e.g., at 80% of lifetime)
- Use sliding window refresh
- Invalidate old refresh tokens on use

### Role Validation
- Always validate roles server-side
- Client-side checks are for UX only
- Never trust client-provided roles

---

## Framework-Specific Notes

### Angular
- Use `HttpInterceptor` for auth interceptor
- Use `CanActivate` guards for routes
- Store session in service with `@Injectable({ providedIn: 'root' })`

### React
- Use axios interceptors or fetch wrapper
- Use React Router's `loader` or custom `ProtectedRoute`
- Store session in Context or Zustand/Redux

### Vue
- Use axios interceptors
- Use Vue Router's `beforeEach` guard
- Store session in Pinia

---

## References

- [Realm Authorization Deep Dive](references/realm-authorization.md)
- [Session State Machine](references/session-state-machine.md)
- [JWT Best Practices](references/jwt-best-practices.md)

---

## Metadata

```yaml
author: Christian Kusmanow / Claude
version: 1.0.0
last_updated: "2026-01-23"
source: IoT Admin Backend (40_Resources/AwesomeNodes/IoT Admin Backend.md)
patterns:
  - Realm-based authorization (3-tier hierarchy)
  - Session state machine
  - Auth interceptor with refresh queue
  - Route guards with realm/role
  - JWT token handling
```
