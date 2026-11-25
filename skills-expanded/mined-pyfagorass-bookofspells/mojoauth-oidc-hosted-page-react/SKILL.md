---
name: mojoauth-oidc-hosted-page-react
description: Implement passwordless authentication in React SPA applications using MojoAuth OIDC Hosted Login Page with PKCE.
---

# Implement MojoAuth OIDC (React)

This expert AI assistant guide walks you through integrating passwordless authentication into an existing React application using MojoAuth's Hosted Login Page as an OIDC identity provider. MojoAuth handles all authentication methods (Magic Links, Email OTP, SMS OTP, Social Login, Passkeys) through its hosted page — your app simply redirects there and handles the callback.

## 1. Prerequisites

- An existing React 18+ application (e.g., created with Vite or Create React App).
- Basic knowledge of React hooks and React Router.
- An active MojoAuth account.
- [MojoAuth OIDC Setup Guide](https://docs.mojoauth.com/hosted-login-page/)
- Required libraries: `oidc-client-ts`, `react-oidc-context`.

## 2. Implementation Steps

### Step 1: Configure Application in MojoAuth

1. Log in to the [MojoAuth Dashboard](https://mojoauth.com/dashboard).
2. Note your **MojoAuth Domain** (e.g., `your-app.mojoauth.com`).
3. Configure the **Redirect URI** (e.g., `http://localhost:5173/auth/callback`).
4. Retrieve **Client ID**.
5. Enable your preferred authentication methods (Magic Link, Email OTP, Social Login, Passkeys).

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
  authority: 'https://your-app.mojoauth.com', // Your MojoAuth Domain
  client_id: 'your_client_id',
  redirect_uri: 'http://localhost:5173/auth/callback',
  post_logout_redirect_uri: 'http://localhost:5173/',
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

Since MojoAuth handles all authentication on its Hosted Login Page, your login page only needs a **"Sign In" button** that triggers the OIDC redirect:

```tsx
// src/pages/Login.tsx
import { useAuth } from 'react-oidc-context';

export default function LoginPage() {
  const auth = useAuth();

  const handleLogin = () => {
    // Redirect to MojoAuth Hosted Login Page via OIDC
    auth.signinRedirect();
  };

  return (
    <div className="login-container">
      <h1>Welcome</h1>
      <p>Sign in with your preferred method — passwordless, social login, or passkeys.</p>

      <button onClick={handleLogin}>
        Sign In with MojoAuth
      </button>

      <p className="powered-by">
        Powered by MojoAuth — Passwordless Authentication
      </p>
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
      navigate('/?error=auth_failed');
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
      <Route path="/" element={<LoginPage />} />
      <Route path="/auth/callback" element={<AuthCallback />} />
      <Route path="/dashboard" element={<Dashboard />} />
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
    return <Navigate to="/" />;
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

### Step 3: Test the Implementation

1. Start your application: `npm run dev`.
2. Navigate to `http://localhost:5173/`.
3. Click **"Sign In with MojoAuth"**.
4. You should be redirected to the MojoAuth Hosted Login Page.
5. Authenticate using any available method (Magic Link, OTP, Social Login, Passkeys).
6. After successful authentication, you should be redirected back to `/auth/callback` and then to `/dashboard`.

## 3. Additional Considerations

- **Error Handling**: Use `auth.error` from the `useAuth` hook to display authentication errors in the UI.
- **Styling**: Adapt the example JSX to match your application's design system (e.g., Material UI, Chakra UI).
- **Security**: Since this is a SPA, **PKCE** is automatically handled by `oidc-client-ts`. Never store a Client Secret in the front-end.
- **Protected Routes**: Create a wrapper component that checks `auth.isAuthenticated` before rendering child routes.
- **MojoAuth Hosted Page Customization**: Customize the look and feel of the Hosted Login Page from the MojoAuth Dashboard to match your brand.

## 4. Support

- **MojoAuth Documentation**: [mojoauth.com/docs](https://mojoauth.com/docs)
- **Check browser console**: Use browser developer tools to debug OIDC flow issues.
- **Library Documentation**: Refer to the [react-oidc-context documentation](https://github.com/authts/react-oidc-context) and [oidc-client-ts documentation](https://github.com/authts/oidc-client-ts) for advanced configuration.
