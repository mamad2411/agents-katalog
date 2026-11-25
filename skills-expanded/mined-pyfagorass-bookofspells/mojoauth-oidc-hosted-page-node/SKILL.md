---
name: mojoauth-oidc-hosted-page-node
description: Implement passwordless authentication in Node.js Express applications using MojoAuth OIDC Hosted Login Page.
---

# Implement MojoAuth OIDC (Node.js / Express)

This expert AI assistant guide walks you through integrating passwordless authentication into an existing Node.js Express application using MojoAuth's Hosted Login Page as an OIDC identity provider. MojoAuth handles all authentication methods (Magic Links, Email OTP, SMS OTP, Social Login, Passkeys) through its hosted page.

## 1. Prerequisites

- An existing Node.js application with Express.
- Basic knowledge of Express.js routing and middleware.
- An active MojoAuth account.
- [MojoAuth OIDC Setup Guide](https://docs.mojoauth.com/hosted-login-page/)
- Required libraries: `openid-client`, `express-session`.

## 2. Implementation Steps

### Step 1: Configure Application in MojoAuth

1. Log in to the [MojoAuth Dashboard](https://mojoauth.com/dashboard).
2. Note your **MojoAuth Domain** (e.g., `your-app.mojoauth.com`).
3. Configure the **Redirect URI** (e.g., `http://localhost:3000/auth/callback`).
4. Retrieve **Client ID** and **Client Secret**.
5. Enable your preferred authentication methods.

### Step 2: Modify the Existing Node.js Project

#### Substep 2.1: Install Dependencies

Run the following command to install the required libraries:

```bash
npm install openid-client express-session dotenv
```

#### Substep 2.2: Configure Environment Variables

Create a `.env` file in the project root:

```env
MOJOAUTH_DOMAIN=your-app.mojoauth.com
MOJOAUTH_CLIENT_ID=your_client_id
MOJOAUTH_CLIENT_SECRET=your_client_secret
MOJOAUTH_REDIRECT_URI=http://localhost:3000/auth/callback
SESSION_SECRET=a_strong_random_secret
PORT=3000
```

#### Substep 2.3: Configure OIDC Client

Create a dedicated utility file for OIDC configuration (e.g., `lib/oidc.js`):

```javascript
// lib/oidc.js
const { Issuer } = require('openid-client');

let _client = null;

async function getClient() {
  if (_client) return _client;

  const mojoauthIssuer = await Issuer.discover(
    `https://${process.env.MOJOAUTH_DOMAIN}`
  );

  _client = new mojoauthIssuer.Client({
    client_id: process.env.MOJOAUTH_CLIENT_ID,
    client_secret: process.env.MOJOAUTH_CLIENT_SECRET,
    redirect_uris: [process.env.MOJOAUTH_REDIRECT_URI],
    response_types: ['code'],
  });

  return _client;
}

module.exports = { getClient };
```

#### Substep 2.4: Update Login Page/UI

Since MojoAuth handles all authentication on its Hosted Login Page, your login page only needs a **"Sign In" button**:

```html
<!-- views/login.ejs -->
<div class="login-container">
  <h1>Welcome</h1>
  <p>Sign in with your preferred method — passwordless, social login, or passkeys.</p>

  <a href="/auth/login" class="sign-in-button">Sign In with MojoAuth</a>

  <p class="powered-by">Powered by MojoAuth — Passwordless Authentication</p>
</div>
```

#### Substep 2.5: Update Backend Logic

Create the necessary routes to handle the OIDC flow.

**1. Login Route** (`routes/auth.js`):

```javascript
// routes/auth.js
const express = require('express');
const router = express.Router();
const { getClient } = require('../lib/oidc');

// Initiate MojoAuth OIDC login
router.get('/login', async (req, res) => {
  const client = await getClient();

  // Generate a random state for CSRF protection
  const state = Math.random().toString(36).substring(2, 15);
  req.session.oidc_state = state;

  const authorizationUrl = client.authorizationUrl({
    scope: 'openid profile email',
    state,
  });

  return res.redirect(authorizationUrl);
});

module.exports = router;
```

**2. Callback Handler Route** (`routes/callback.js`):

```javascript
// routes/callback.js
const express = require('express');
const router = express.Router();
const { getClient } = require('../lib/oidc');

router.get('/callback', async (req, res) => {
  const client = await getClient();
  const params = client.callbackParams(req);

  try {
    const storedState = req.session.oidc_state;
    const tokenSet = await client.callback(
      process.env.MOJOAUTH_REDIRECT_URI,
      params,
      { state: storedState }
    );
    const userinfo = await client.userinfo(tokenSet.access_token);

    // Clear the OIDC state from session
    delete req.session.oidc_state;

    // TODO: Create a session for the user based on `userinfo`
    req.session.user = userinfo;
    console.log('Authenticated User:', userinfo);

    // Redirect to the dashboard or intended page
    res.redirect('/dashboard');
  } catch (error) {
    console.error('OIDC Callback Error:', error);
    res.redirect('/login?error=auth_failed');
  }
});

module.exports = router;
```

**3. Main Application Setup** (`app.js`):

```javascript
// app.js
require('dotenv').config();
const express = require('express');
const session = require('express-session');

const authRoutes = require('./routes/auth');
const callbackRoutes = require('./routes/callback');

const app = express();

app.set('view engine', 'ejs');
app.use(express.urlencoded({ extended: true }));
app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: { secure: false, httpOnly: true, maxAge: 3600000 },
}));

// Routes
app.get('/login', (req, res) => res.render('login'));
app.use('/auth', authRoutes);
app.use('/auth', callbackRoutes);

app.get('/dashboard', (req, res) => {
  if (!req.session.user) return res.redirect('/login');
  res.send(`<h1>Dashboard</h1><pre>${JSON.stringify(req.session.user, null, 2)}</pre><a href="/auth/logout">Logout</a>`);
});

app.get('/auth/logout', (req, res) => {
  req.session.destroy();
  res.redirect('/login');
});

app.listen(process.env.PORT || 3000, () => {
  console.log(`Server running on http://localhost:${process.env.PORT || 3000}`);
});
```

### Step 3: Test the Implementation

1. Start your application: `node app.js`.
2. Navigate to `http://localhost:3000/login`.
3. Click **"Sign In with MojoAuth"**.
4. You should be redirected to the MojoAuth Hosted Login Page.
5. Authenticate using any available method.
6. After successful authentication, you should be redirected back to `/auth/callback` and then to `/dashboard`.

## 3. Additional Considerations

- **Error Handling**: Enhance the callback route to handle specific OIDC errors gracefully.
- **Styling**: Adapt the example HTML/CSS to match your application's design system.
- **Security**: Use `express-session` with a production-ready store (e.g., Redis, MongoDB) and enable `secure: true` for cookies in production.
- **Environment Variables**: Never commit `.env` to source control. Use secrets management in production.

## 4. Support

- **MojoAuth Documentation**: [mojoauth.com/docs](https://mojoauth.com/docs)
- **Check application logs**: Use server-side logging to debug OIDC flow issues.
- **Library Documentation**: Refer to the [openid-client documentation](https://github.com/panva/node-openid-client) for advanced configuration.
