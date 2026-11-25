---
name: oidc-hosted-page-angular
description: Implement "Sign in with SSO" in Angular SPA applications using SSOJet OIDC with PKCE.
---

# Implement SSOJet OIDC (Angular)

This expert AI assistant guide walks you through integrating "Sign in with SSO" functionality into an existing login page in an Angular application using SSOJet as an OIDC identity provider. The goal is to modify the existing login flow to add SSO support without disrupting the current traditional login functionality (e.g., email/password).

## 1. Prerequisites

- An existing Angular 15+ application with a login page.
- Basic knowledge of Angular routing, services, and components.
- An active SSOJet account.
- [SSO Connection Setup Guide](https://docs.ssojet.com/en/how-to-guides/integrations//)
- Required library: `angular-auth-oidc-client`.

## 2. Implementation Steps

### Step 1: Create Application in SSOJet

1. Log in to the SSOJet Dashboard.
2. Navigate to **Applications**.
3. Create a new application (e.g., "MyAngularApp", type **Single Page App (SPA)**).
4. Configure the callback URI (e.g., `http://localhost:4200/auth/callback`).
5. Retrieve **Client ID**.
6. Copy the **Issuer URL** from the **Advanced > Endpoints** section.

> **Note:** For SPAs, the recommended flow is **Authorization Code with PKCE** (no Client Secret required on the front-end).

### Step 2: Modify the Existing Angular Project

#### Substep 2.1: Install Dependencies

Run the following command to install the required library:

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
        authority: 'https://auth.ssojet.com', // Your SSOJet Issuer URL
        redirectUrl: 'http://localhost:4200/auth/callback',
        postLogoutRedirectUri: 'http://localhost:4200/login',
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
  ssojet: {
    issuerUrl: 'https://auth.ssojet.com',
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

  login(loginHint?: string): void {
    // Pass login_hint as an extra parameter
    this.oidcService.authorize(undefined, {
      customParams: { login_hint: loginHint || '' },
    });
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

Modify your existing login component (e.g., `src/app/login/login.component.ts`):

```typescript
// src/app/login/login.component.ts
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, CommonModule],
  template: `
    <div class="login-container">
      <h1>Sign In</h1>

      <form (ngSubmit)="handleLogin()">
        <div>
          <label for="email">Email</label>
          <input type="email" id="email" [(ngModel)]="email" name="email" required />
        </div>

        <div *ngIf="!isSSO">
          <label for="password">Password</label>
          <input type="password" id="password" [(ngModel)]="password" name="password" required />
        </div>

        <button type="submit">
          {{ isSSO ? 'Continue with SSO' : 'Sign In' }}
        </button>
      </form>

      <button type="button" (click)="toggleSSO()">
        {{ isSSO ? 'Back to Password Login' : 'Sign in with SSO' }}
      </button>
    </div>
  `,
})
export class LoginComponent {
  isSSO = false;
  email = '';
  password = '';

  constructor(private authService: AuthService) {}

  toggleSSO(): void {
    this.isSSO = !this.isSSO;
  }

  handleLogin(): void {
    if (this.isSSO) {
      // Trigger SSO login via the OIDC library
      this.authService.login(this.email);
    } else {
      // Existing password login logic here
      console.log('Processing traditional login...');
    }
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
        this.router.navigate(['/login'], { queryParams: { error: 'oidc_failed' } });
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
  { path: 'login', component: LoginComponent },
  { path: 'auth/callback', component: AuthCallbackComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: '', redirectTo: '/login', pathMatch: 'full' },
];
```

### Step 3: Test the Modified Connection

1. Start your application: `ng serve`.
2. Navigate to your login page (e.g., `http://localhost:4200/login`).
3. Verify that the traditional login form (Email + Password) is visible by default.
4. Click **"Sign in with SSO"** and ensure:
   - The password field disappears.
   - The submit button changes to "Continue with SSO".
5. Enter a test email and submit.
   - You should be redirected to the SSOJet login page.
6. Authenticate with SSOJet.
   - You should be redirected back to `/auth/callback` and then to `/dashboard`.

## 3. Additional Considerations

- **Error Handling**: Subscribe to `OidcSecurityService` events to handle specific OIDC errors gracefully.
- **Styling**: Adapt the example template to match your application's design system (e.g., Angular Material).
- **Security**: Since this is a SPA, **PKCE** is automatically handled by `angular-auth-oidc-client`. Never store a Client Secret in the front-end.
- **Route Guards**: Use `AutoLoginPartialRoutesGuard` from the library to protect routes that require authentication.

## 4. Support

- **Contact SSOJet support**: Reach out if you have integration questions.
- **Check browser console**: Use browser developer tools to debug OIDC flow issues.
- **Library Documentation**: Refer to the [angular-auth-oidc-client documentation](https://github.com/damienbod/angular-auth-oidc-client) for advanced configuration.
