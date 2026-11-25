---
name: mojoauth-oidc-hosted-page-angular
description: Implement passwordless authentication in Angular SPA applications using MojoAuth OIDC Hosted Login Page with PKCE.
---

# Implement MojoAuth OIDC (Angular)

This expert AI assistant guide walks you through integrating passwordless authentication into an Angular application using MojoAuth's Hosted Login Page as an OIDC identity provider. MojoAuth handles all authentication methods (Magic Links, Email OTP, SMS OTP, Social Login, Passkeys) through its hosted page.

## 1. Prerequisites

- An existing Angular 15+ application.
- Basic knowledge of Angular routing, services, and components.
- An active MojoAuth account.
- [MojoAuth OIDC Setup Guide](https://docs.mojoauth.com/hosted-login-page/)
- Required library: `angular-auth-oidc-client`.

## 2. Implementation Steps

### Step 1: Configure Application in MojoAuth

1. Log in to the [MojoAuth Dashboard](https://mojoauth.com/dashboard).
2. Note your **MojoAuth Domain** (e.g., `your-app.mojoauth.com`).
3. Configure the **Redirect URI** (e.g., `http://localhost:4200/auth/callback`).
4. Retrieve **Client ID**.
5. Enable your preferred authentication methods.

> **Note:** For SPAs, the recommended flow is **Authorization Code with PKCE** (no Client Secret required on the front-end).

### Step 2: Modify the Existing Angular Project

#### Substep 2.1: Install Dependencies

```bash
npm install angular-auth-oidc-client
```

#### Substep 2.2: Configure OIDC Module

Register the OIDC module in your `app.config.ts` (standalone) or `app.module.ts`:

```typescript
// app.config.ts (Standalone API - Angular 15+)
import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideAuth, LogLevel } from 'angular-auth-oidc-client';
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideAuth({
      config: {
        authority: 'https://your-app.mojoauth.com', // Your MojoAuth Domain
        redirectUrl: 'http://localhost:4200/auth/callback',
        postLogoutRedirectUri: 'http://localhost:4200/',
        clientId: 'your_client_id',
        scope: 'openid profile email',
        responseType: 'code',
        silentRenew: true,
        useRefreshToken: true,
        logLevel: LogLevel.Debug,
      },
    }),
  ],
};
```

#### Substep 2.3: Configure Environment

Create environment files for your configuration (e.g., `src/environments/environment.ts`):

```typescript
// src/environments/environment.ts
export const environment = {
  production: false,
  mojoauth: {
    domain: 'your-app.mojoauth.com',
    clientId: 'your_client_id',
    redirectUri: 'http://localhost:4200/auth/callback',
  },
};
```

#### Substep 2.4: Create Auth Service

Create a dedicated authentication service (e.g., `src/app/services/auth.service.ts`):

```typescript
// src/app/services/auth.service.ts
import { Injectable } from '@angular/core';
import { OidcSecurityService } from 'angular-auth-oidc-client';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AuthService {
  constructor(private oidcService: OidcSecurityService) {}

  get isAuthenticated$(): Observable<boolean> {
    return new Observable((observer) => {
      this.oidcService.isAuthenticated$.subscribe(({ isAuthenticated }) => {
        observer.next(isAuthenticated);
      });
    });
  }

  get userData$() {
    return this.oidcService.userData$;
  }

  login(): void {
    // Redirect to MojoAuth Hosted Login Page
    this.oidcService.authorize();
  }

  logout(): void {
    this.oidcService.logoff();
  }

  checkAuth(): Observable<any> {
    return this.oidcService.checkAuth();
  }
}
```

#### Substep 2.5: Update Login Page/UI

Since MojoAuth handles all authentication on its Hosted Login Page, your login component only needs a **"Sign In" button**:

```typescript
// src/app/login/login.component.ts
import { Component } from '@angular/core';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  template: `
    <div class="login-container">
      <h1>Welcome</h1>
      <p>Sign in with your preferred method — passwordless, social login, or passkeys.</p>

      <button (click)="handleLogin()">
        Sign In with MojoAuth
      </button>

      <p class="powered-by">Powered by MojoAuth — Passwordless Authentication</p>
    </div>
  `,
})
export class LoginComponent {
  constructor(private authService: AuthService) {}

  handleLogin(): void {
    this.authService.login();
  }
}
```

#### Substep 2.6: Create Callback Component

Create a callback component to handle the OIDC redirect (e.g., `src/app/auth/callback.component.ts`):

```typescript
// src/app/auth/callback.component.ts
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { OidcSecurityService } from 'angular-auth-oidc-client';

@Component({
  selector: 'app-auth-callback',
  standalone: true,
  template: `<p>Authenticating...</p>`,
})
export class AuthCallbackComponent implements OnInit {
  constructor(
    private oidcService: OidcSecurityService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.oidcService.checkAuth().subscribe(({ isAuthenticated, userData }) => {
      if (isAuthenticated) {
        console.log('Authenticated User:', userData);
        this.router.navigate(['/dashboard']);
      } else {
        this.router.navigate(['/'], { queryParams: { error: 'auth_failed' } });
      }
    });
  }
}
```

#### Substep 2.7: Configure Routes

Update your `app.routes.ts` to include the callback route:

```typescript
// app.routes.ts
import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { AuthCallbackComponent } from './auth/callback.component';
import { DashboardComponent } from './dashboard/dashboard.component';

export const routes: Routes = [
  { path: '', component: LoginComponent },
  { path: 'auth/callback', component: AuthCallbackComponent },
  { path: 'dashboard', component: DashboardComponent },
];
```

### Step 3: Test the Implementation

1. Start your application: `ng serve`.
2. Navigate to `http://localhost:4200/`.
3. Click **"Sign In with MojoAuth"**.
4. You should be redirected to the MojoAuth Hosted Login Page.
5. Authenticate using any available method.
6. After successful authentication, you should be redirected back to `/auth/callback` and then to `/dashboard`.

## 3. Additional Considerations

- **Error Handling**: Subscribe to `OidcSecurityService` events to handle specific OIDC errors gracefully.
- **Styling**: Adapt the example template to match your application's design system (e.g., Angular Material).
- **Security**: Since this is a SPA, **PKCE** is automatically handled by `angular-auth-oidc-client`. Never store a Client Secret in the front-end.
- **Route Guards**: Use `AutoLoginPartialRoutesGuard` from the library to protect routes that require authentication.

## 4. Support

- **MojoAuth Documentation**: [mojoauth.com/docs](https://mojoauth.com/docs)
- **Check browser console**: Use browser developer tools to debug OIDC flow issues.
- **Library Documentation**: Refer to the [angular-auth-oidc-client documentation](https://github.com/damienbod/angular-auth-oidc-client) for advanced configuration.
