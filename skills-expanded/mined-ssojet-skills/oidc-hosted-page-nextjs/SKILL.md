---
name: oidc-hosted-page-nextjs
description: Implement "Sign in with SSO" in Next.js applications using SSOJet OIDC Authorization Code flow with the App Router.
---

# Implement SSOJet OIDC (Next.js)

This expert AI assistant guide walks you through integrating "Sign in with SSO" functionality into an existing login page in a Next.js application using SSOJet as an OIDC identity provider. The goal is to modify the existing login flow to add SSO support without disrupting the current traditional login functionality (e.g., email/password).

## 1. Prerequisites

- An existing Next.js application with a login page.
- Basic knowledge of Next.js and its common tools (e.g., App Router).
- An active SSOJet account.
- [SSO Connection Setup Guide](https://docs.ssojet.com/en/how-to-guides/integrations//)
- Required libraries: `openid-client` (standard for Node.js OIDC integration).

## 2. Implementation Steps

### Step 1: Create Application in SSOJet

1. Log in to the SSOJet Dashboard.
2. Navigate to **Applications**.
3. Create a new application (e.g., "MyNextjsApp", type **Regular Web App**).
4. Configure the callback URI (e.g., `http://localhost:3000/api/auth/callback`).
5. Retrieve **Client ID** and **Client Secret**.
6. Copy the **Issuer URL** from the **Advanced > Endpoints** section.
7. ![Create Application in SSOJet](/img/ssojet-applications-stepX.png)

### Step 2: Modify the Existing Next.js Project

#### Substep 2.1: Install Dependencies

Run the following command to install the required OIDC library:

```bash
npm install openid-client
```

#### Substep 2.2: Configure OIDC

Configure the OIDC provider with your SSOJet credentials. It is recommended to create a dedicated utility file for this configuration (e.g., `lib/oidc.ts`).

```typescript
// lib/oidc.ts
import { Issuer } from 'openid-client';

export async function getClient() {
  const ssojetIssuer = await Issuer.discover('${ISSUER_URL}'); // e.g. https://auth.ssojet.com
  return new ssojetIssuer.Client({
    client_id: '${cli_curf51oulvtc716e50eg.ad4a67ec19ac4507b744a1686ec9bff8.MGMpt3uV99Lftv5KkHF7pk}',
    client_secret: '${CLIENT_SECRET}',
    redirect_uris: ['http://localhost:3000/api/auth/callback'],
    response_types: ['code'],
  });
}
```

#### Substep 2.3: Update Login Page/UI

Modify your existing login component (e.g., `app/login/page.tsx`) to include the "Sign in with SSO" toggle.

```tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const [isSSO, setIsSSO] = useState(false);
  const [email, setEmail] = useState('');
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isSSO) {
      // Trigger SSO login by redirecting to our API route
      window.location.href = `/api/auth/login?login_hint=${encodeURIComponent(email)}`;
    } else {
      // Existing password login logic here
      console.log('Processing traditional login...');
    }
  };

  return (
    <div className="login-container">
      <h1>Sign In</h1>
      <form onSubmit={handleLogin} className="flex flex-col gap-4">
        <div>
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="border p-2 rounded"
          />
        </div>

        {!isSSO && (
          <div>
            <label>Password</label>
            <input type="password" required className="border p-2 rounded" />
          </div>
        )}

        <button type="submit" className="bg-blue-600 text-white p-2 rounded">
          {isSSO ? 'Continue with SSO' : 'Sign In'}
        </button>

        <button
          type="button"
          onClick={() => setIsSSO(!isSSO)}
          className="text-sm text-blue-500 underline"
        >
          {isSSO ? 'Back to Password Login' : 'Sign in with SSO'}
        </button>
      </form>
    </div>
  );
}
```

#### Substep 2.4: Update Backend Logic

Create the necessary API routes to handle the OIDC flow.

**1. Login Initiation Route** (`app/api/auth/login/route.ts`):

```typescript
import { NextResponse } from 'next/server';
import { getClient } from '@/lib/oidc';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const login_hint = searchParams.get('login_hint');
  const client = await getClient();

  // Generate a random state for CSRF protection
  const state = Math.random().toString(36).substring(2, 15);

  const authorizationUrl = client.authorizationUrl({
    scope: 'openid profile email',
    login_hint: login_hint || undefined,
    state,
  });

  const response = NextResponse.redirect(authorizationUrl);
  // Store state in a cookie to verify in the callback
  response.cookies.set('oidc_state', state, { 
    httpOnly: true, 
    secure: true, 
    sameSite: 'lax',
    maxAge: 3600 
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
    const tokenSet = await client.callback('http://localhost:3000/api/auth/callback', params, { state: storedState });
    const userinfo = await client.userinfo(tokenSet.access_token!);
    
    // TODO: Create a session for the user based on `userinfo`
    console.log('Authenticated User:', userinfo);

    // Redirect to the dashboard or intended page
    return NextResponse.redirect(new URL('/dashboard', request.url));
  } catch (error) {
    console.error('OIDC Callback Error:', error);
    return NextResponse.redirect(new URL('/login?error=oidc_failed', request.url));
  }
}
```

### Step 3: Test the Modified Connection

1. Start your application: `npm run dev`.
2. Navigate to your login page (e.g., `/login`).
3. Verify that the traditional login form (Email + Password) is visible by default.
4. Click **"Sign in with SSO"** and ensure:
   - The password field disappears.
   - The submit button changes to "Continue with SSO".
5. Enter a test email and submit.
   - You should be redirected to the SSOJet login page.
6. Authenticate with SSOJet.
   - You should be redirected back to `/api/auth/callback` and then to `/dashboard`.

## 3. Additional Considerations

- **Error Handling**: Enhance the callback route to handle specific OIDC errors gracefully.
- **Styling**: Adapt the example CSS classes to match your application's design system.
- **Security**: Integrate the user information returned in the callback with your existing session management system (e.g., setting cookies or JWTs).
- **Environment Variables**: Store sensitive values like `CLIENT_SECRET` and `ISSUER_URL` in `.env.local` and access them via `process.env`.

## 4. Support

- **Contact SSOJet support**: Reach out if you have integration questions.
- **Check application logs**: Use server-side logging to debug OIDC flow issues.
- **Library Documentation**: Refer to the [openid-client documentation](https://github.com/panva/node-openid-client) for advanced configuration.
