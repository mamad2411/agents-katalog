---
name: oidc-hosted-page-react
description: Implement "Sign in with SSO" in React SPA applications using SSOJet OIDC with PKCE.
---

# Implement SSOJet OIDC (React)

This expert AI assistant guide walks you through integrating "Sign in with SSO" functionality into an existing login page in a React application using SSOJet as an OIDC identity provider. The goal is to modify the existing login flow to add SSO support without disrupting the current traditional login functionality (e.g., email/password).

## 1. Prerequisites

- An existing React 18+ application with a login page (e.g., created with Vite or Create React App).
- Basic knowledge of React hooks and React Router.
- An active SSOJet account.
- [SSO Connection Setup Guide](https://docs.ssojet.com/en/how-to-guides/integrations//)
- Required library: `oidc-client-ts`, `react-oidc-context`.

## 2. Implementation Steps

### Step 1: Create Application in SSOJet

1. Log in to the SSOJet Dashboard.
2. Navigate to **Applications**.
3. Create a new application (e.g., "MyReactApp", type **Single Page App (SPA)**).
4. Configure the callback URI (e.g., `http://localhost:5173/auth/callback`).
5. Retrieve **Client ID**.
6. Copy the **Issuer URL** from the **Advanced > Endpoints** section.

> **Note:** For SPAs, the recommended flow is **Authorization Code with PKCE** (no Client Secret required on the front-end).

### Step 2: Modify the Existing React Project

#### Substep 2.1: Install Dependencies

Run the following command to install the required libraries:

```bash
npm install oidc-client-ts react-oidc-context react-router-dom
```

#### Substep 2.2: Configure OIDC Provider

Create a dedicated configuration file (e.g., `src/lib/oidcConfig.ts`):

```typescript
// src/lib/oidcConfig.ts
import { WebStorageStateStore } from 'oidc-client-ts';

export const oidcConfig = {
  authority: 'https://auth.ssojet.com', // Your SSOJet Issuer URL
  client_id: 'your_client_id',
  redirect_uri: 'http://localhost:5173/auth/callback',
  post_logout_redirect_uri: 'http://localhost:5173/login',
  response_type: 'code',
  scope: 'openid profile email',
  userStore: new WebStorageStateStore({ store: window.localStorage }),
};
```

#### Substep 2.3: Wrap App with Auth Provider

Update your `src/main.tsx` to wrap the application with the OIDC provider:

```tsx
// src/main.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from 'react-oidc-context';
import { oidcConfig } from './lib/oidcConfig';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <AuthProvider {...oidcConfig}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </AuthProvider>
  </React.StrictMode>
);
```

#### Substep 2.4: Update Login Page/UI

Modify your existing login component (e.g., `src/pages/Login.tsx`) to include the "Sign in with SSO" toggle:

```tsx
// src/pages/Login.tsx
import { useState } from 'react';
import { useAuth } from 'react-oidc-context';

export default function LoginPage() {
  const [isSSO, setIsSSO] = useState(false);
  const [email, setEmail] = useState('');
  const auth = useAuth();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    if (isSSO) {
      // Trigger SSO login via the OIDC library with login_hint
      auth.signinRedirect({
        extraQueryParams: { login_hint: email },
      });
    } else {
      // Existing password login logic here
      console.log('Processing traditional login...');
    }
  };

  return (
    <div className="login-container">
      <h1>Sign In</h1>
      <form onSubmit={handleLogin}>
        <div>
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        {!isSSO && (
          <div>
            <label htmlFor="password">Password</label>
            <input type="password" id="password" required />
          </div>
        )}

        <button type="submit">
          {isSSO ? 'Continue with SSO' : 'Sign In'}
        </button>
      </form>

      <button type="button" onClick={() => setIsSSO(!isSSO)}>
        {isSSO ? 'Back to Password Login' : 'Sign in with SSO'}
      </button>
    </div>
  );
}
```

#### Substep 2.5: Create Callback Component

Create a callback component to handle the OIDC redirect (e.g., `src/pages/AuthCallback.tsx`):

```tsx
// src/pages/AuthCallback.tsx
import { useEffect } from 'react';
import { useAuth } from 'react-oidc-context';
import { useNavigate } from 'react-router-dom';

export default function AuthCallback() {
  const auth = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (auth.isAuthenticated) {
      console.log('Authenticated User:', auth.user?.profile);
      navigate('/dashboard');
    }
    if (auth.error) {
      console.error('OIDC Callback Error:', auth.error);
      navigate('/login?error=oidc_failed');
    }
  }, [auth.isAuthenticated, auth.error, navigate]);

  if (auth.isLoading) {
    return <p>Authenticating...</p>;
  }

  return null;
}
```

#### Substep 2.6: Configure Routes

Update your `src/App.tsx` to include the callback route:

```tsx
// src/App.tsx
import { Routes, Route } from 'react-router-dom';
import LoginPage from './pages/Login';
import AuthCallback from './pages/AuthCallback';
import Dashboard from './pages/Dashboard';

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/auth/callback" element={<AuthCallback />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/" element={<LoginPage />} />
    </Routes>
  );
}
```

**Dashboard Page** (`src/pages/Dashboard.tsx`):

```tsx
// src/pages/Dashboard.tsx
import { useAuth } from 'react-oidc-context';
import { Navigate } from 'react-router-dom';

export default function Dashboard() {
  const auth = useAuth();

  if (!auth.isAuthenticated) {
    return <Navigate to="/login" />;
  }

  return (
    <div>
      <h1>Dashboard</h1>
      <pre>{JSON.stringify(auth.user?.profile, null, 2)}</pre>
      <button onClick={() => auth.signoutRedirect()}>Logout</button>
    </div>
  );
}
```

### Step 3: Test the Modified Connection

1. Start your application: `npm run dev`.
2. Navigate to your login page (e.g., `http://localhost:5173/login`).
3. Verify that the traditional login form (Email + Password) is visible by default.
4. Click **"Sign in with SSO"** and ensure:
   - The password field disappears.
   - The submit button changes to "Continue with SSO".
5. Enter a test email and submit.
   - You should be redirected to the SSOJet login page.
6. Authenticate with SSOJet.
   - You should be redirected back to `/auth/callback` and then to `/dashboard`.

## 3. Additional Considerations

- **Error Handling**: Use `auth.error` from the `useAuth` hook to display OIDC-specific errors in the UI.
- **Styling**: Adapt the example JSX to match your application's design system (e.g., Material UI, Chakra UI).
- **Security**: Since this is a SPA, **PKCE** is automatically handled by `oidc-client-ts`. Never store a Client Secret in the front-end.
- **Protected Routes**: Create a wrapper component that checks `auth.isAuthenticated` before rendering child routes.

## 4. Support

- **Contact SSOJet support**: Reach out if you have integration questions.
- **Check browser console**: Use browser developer tools to debug OIDC flow issues.
- **Library Documentation**: Refer to the [react-oidc-context documentation](https://github.com/authts/react-oidc-context) and [oidc-client-ts documentation](https://github.com/authts/oidc-client-ts) for advanced configuration.
