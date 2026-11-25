---
name: mojoauth-oidc-hosted-page-nextjs
description: Implement passwordless authentication in Next.js applications using MojoAuth OIDC Hosted Login Page with the App Router.
---

# Implement MojoAuth OIDC (Next.js)

This expert AI assistant guide walks you through integrating passwordless authentication into a Next.js application using MojoAuth's Hosted Login Page as an OIDC identity provider. MojoAuth handles all authentication methods (Magic Links, Email OTP, SMS OTP, Social Login, Passkeys) through its hosted page — your app simply redirects there and handles the callback.

## 1. Prerequisites

- An existing Next.js application (App Router).
- Basic knowledge of Next.js and its common tools.
- An active MojoAuth account.
- [MojoAuth OIDC Setup Guide](https://docs.mojoauth.com/hosted-login-page/)
- Required library: `openid-client` (standard for Node.js OIDC integration).

## 2. Implementation Steps

### Step 1: Configure Application in MojoAuth

1. Log in to the [MojoAuth Dashboard](https://mojoauth.com/dashboard).
2. Note your **MojoAuth Domain** (e.g., `your-app.mojoauth.com`).
3. Configure the **Redirect URI** (e.g., `http://localhost:3000/api/auth/callback`).
4. Retrieve **Client ID** and **Client Secret**.
5. Enable your preferred authentication methods (Magic Link, Email OTP, Social Login, Passkeys).

### Step 2: Modify the Existing Next.js Project

#### Substep 2.1: Install Dependencies

Run the following command to install the required OIDC library:

```bash
npm install openid-client
```

#### Substep 2.2: Configure Environment Variables

Add to your `.env.local`:

```env
MOJOAUTH_DOMAIN=your-app.mojoauth.com
MOJOAUTH_CLIENT_ID=your_client_id
MOJOAUTH_CLIENT_SECRET=your_client_secret
MOJOAUTH_REDIRECT_URI=http://localhost:3000/api/auth/callback
```

#### Substep 2.3: Configure OIDC

Create a dedicated utility file for OIDC configuration (`lib/oidc.ts`):

```typescript
// lib/oidc.ts
import { Issuer } from 'openid-client';

let _client: any = null;

export async function getClient() {
  if (_client) return _client;

  const mojoauthIssuer = await Issuer.discover(
    `https://${process.env.MOJOAUTH_DOMAIN}`
  );

  _client = new mojoauthIssuer.Client({
    client_id: process.env.MOJOAUTH_CLIENT_ID!,
    client_secret: process.env.MOJOAUTH_CLIENT_SECRET!,
    redirect_uris: [process.env.MOJOAUTH_REDIRECT_URI!],
    response_types: ['code'],
  });

  return _client;
}
```

#### Substep 2.4: Update Login Page/UI

Create or modify your login page (`app/login/page.tsx`). Since MojoAuth handles all authentication on its Hosted Login Page, you only need a **"Sign In" button** that redirects the user:

```tsx
'use client';

import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const router = useRouter();

  const handleLogin = () => {
    // Redirect to the API route that initiates MojoAuth OIDC flow
    window.location.href = '/api/auth/login';
  };

  return (
    <div className="login-container">
      <h1>Welcome</h1>
      <p>Sign in with your preferred method — passwordless, social login, or passkeys.</p>

      <button
        onClick={handleLogin}
        className="bg-blue-600 text-white p-3 rounded-lg w-full"
      >
        Sign In with MojoAuth
      </button>

      <p className="text-sm text-gray-500 mt-4">
        Powered by MojoAuth — Passwordless Authentication
      </p>
    </div>
  );
}
```

#### Substep 2.5: Update Backend Logic

Create the necessary API routes to handle the OIDC flow.

**1. Login Initiation Route** (`app/api/auth/login/route.ts`):

```typescript
import { NextResponse } from 'next/server';
import { getClient } from '@/lib/oidc';

export async function GET(request: Request) {
  const client = await getClient();

  // Generate a random state for CSRF protection
  const state = Math.random().toString(36).substring(2, 15);

  const authorizationUrl = client.authorizationUrl({
    scope: 'openid profile email',
    state,
  });

  const response = NextResponse.redirect(authorizationUrl);
  // Store state in a cookie to verify in the callback
  response.cookies.set('oidc_state', state, {
    httpOnly: true,
    secure: true,
    sameSite: 'lax',
    maxAge: 3600,
  });

  return response;
}
```

**2. Callback Handler Route** (`app/api/auth/callback/route.ts`):

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { getClient } from '@/lib/oidc';

export async function GET(request: NextRequest) {
  const client = await getClient();
  const params = client.callbackParams(request.url);

  try {
    const storedState = request.cookies.get('oidc_state')?.value;
    const tokenSet = await client.callback(
      process.env.MOJOAUTH_REDIRECT_URI,
      params,
      { state: storedState }
    );
    const userinfo = await client.userinfo(tokenSet.access_token!);

    // TODO: Create a session for the user based on `userinfo`
    // userinfo contains: sub, name, email, email_verified, etc.
    console.log('Authenticated User:', userinfo);

    // Redirect to the dashboard or intended page
    return NextResponse.redirect(new URL('/dashboard', request.url));
  } catch (error) {
    console.error('OIDC Callback Error:', error);
    return NextResponse.redirect(new URL('/login?error=auth_failed', request.url));
  }
}
```

### Step 3: Test the Implementation

1. Start your application: `npm run dev`.
2. Navigate to your login page (e.g., `/login`).
3. Click **"Sign In with MojoAuth"**.
4. You should be redirected to the MojoAuth Hosted Login Page.
5. Authenticate using any available method (Magic Link, OTP, Social Login, Passkeys).
6. After successful authentication, you should be redirected back to `/api/auth/callback` and then to `/dashboard`.

## 3. Additional Considerations

- **Error Handling**: Enhance the callback route to handle specific OIDC errors gracefully.
- **Styling**: Adapt the login page to match your application's design system.
- **Security**: Integrate the user information returned in the callback with your existing session management system (e.g., setting cookies or JWTs).
- **Environment Variables**: Store sensitive values like `MOJOAUTH_CLIENT_SECRET` in `.env.local` and access them via `process.env`.
- **MojoAuth Hosted Page Customization**: Customize the look and feel of the Hosted Login Page from the MojoAuth Dashboard to match your brand.

## 4. Support

- **MojoAuth Documentation**: [mojoauth.com/docs](https://mojoauth.com/docs)
- **Check application logs**: Use server-side logging to debug OIDC flow issues.
- **Library Documentation**: Refer to the [openid-client documentation](https://github.com/panva/node-openid-client) for advanced configuration.
