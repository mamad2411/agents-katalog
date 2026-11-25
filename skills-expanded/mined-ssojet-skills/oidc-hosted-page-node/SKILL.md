---
name: oidc-hosted-page-node
description: Implement "Sign in with SSO" in Node.js Express applications using SSOJet OIDC Authorization Code flow.
---

# Implement SSOJet OIDC (Node.js / Express)

This expert AI assistant guide walks you through integrating "Sign in with SSO" functionality into an existing login page in a Node.js Express application using SSOJet as an OIDC identity provider. The goal is to modify the existing login flow to add SSO support without disrupting the current traditional login functionality (e.g., email/password).

## 1. Prerequisites

- An existing Node.js application with Express and a login page.
- Basic knowledge of Express.js routing and middleware.
- An active SSOJet account.
- [SSO Connection Setup Guide](https://docs.ssojet.com/en/how-to-guides/integrations//)
- Required libraries: `openid-client`, `express-session`.

## 2. Implementation Steps

### Step 1: Create Application in SSOJet

1. Log in to the SSOJet Dashboard.
2. Navigate to **Applications**.
3. Create a new application (e.g., "MyNodeApp", type **Regular Web App**).
4. Configure the callback URI (e.g., `http://localhost:3000/auth/callback`).
5. Retrieve **Client ID** and **Client Secret**.
6. Copy the **Issuer URL** from the **Advanced > Endpoints** section.

### Step 2: Modify the Existing Node.js Project

#### Substep 2.1: Install Dependencies

Run the following command to install the required libraries:

```bash
npm install openid-client express-session dotenv
```

#### Substep 2.2: Configure Environment Variables

Create a `.env` file in the project root:

```env
SSOJET_ISSUER_URL=https://auth.ssojet.com
SSOJET_CLIENT_ID=your_client_id
SSOJET_CLIENT_SECRET=your_client_secret
SSOJET_REDIRECT_URI=http://localhost:3000/auth/callback
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

  const ssojetIssuer = await Issuer.discover(process.env.SSOJET_ISSUER_URL);
  _client = new ssojetIssuer.Client({
    client_id: process.env.SSOJET_CLIENT_ID,
    client_secret: process.env.SSOJET_CLIENT_SECRET,
    redirect_uris: [process.env.SSOJET_REDIRECT_URI],
    response_types: ['code'],
  });

  return _client;
}

module.exports = { getClient };
```

#### Substep 2.4: Update Login Page/UI

Modify your existing login page template (e.g., `views/login.ejs` or equivalent) to include the "Sign in with SSO" toggle:

```html
<!-- views/login.ejs -->
<div class="login-container">
  <h1>Sign In</h1>

  <form id="loginForm" action="/auth/login" method="POST">
    <div>
      <label for="email">Email</label>
      <input type="email" id="email" name="email" required />
    </div>

    <div id="passwordField">
      <label for="password">Password</label>
      <input type="password" id="password" name="password" required />
    </div>

    <input type="hidden" id="isSSO" name="isSSO" value="false" />

    <button type="submit" id="submitBtn">Sign In</button>
  </form>

  <button type="button" id="ssoToggle" onclick="toggleSSO()">
    Sign in with SSO
  </button>
</div>

<script>
  function toggleSSO() {
    const isSSO = document.getElementById('isSSO');
    const passwordField = document.getElementById('passwordField');
    const submitBtn = document.getElementById('submitBtn');
    const ssoToggle = document.getElementById('ssoToggle');

    if (isSSO.value === 'false') {
      isSSO.value = 'true';
      passwordField.style.display = 'none';
      document.getElementById('password').removeAttribute('required');
      submitBtn.textContent = 'Continue with SSO';
      ssoToggle.textContent = 'Back to Password Login';
    } else {
      isSSO.value = 'false';
      passwordField.style.display = 'block';
      document.getElementById('password').setAttribute('required', 'true');
      submitBtn.textContent = 'Sign In';
      ssoToggle.textContent = 'Sign in with SSO';
    }
  }
</script>
```

#### Substep 2.5: Update Backend Logic

Create the necessary routes to handle the OIDC flow.

**1. Login Route** (`routes/auth.js`):

```javascript
// routes/auth.js
const express = require('express');
const router = express.Router();
const { getClient } = require('../lib/oidc');

// Handle login form submission
router.post('/login', async (req, res) => {
  const { email, isSSO } = req.body;

  if (isSSO === 'true') {
    // Trigger SSO login
    const client = await getClient();

    // Generate a random state for CSRF protection
    const state = Math.random().toString(36).substring(2, 15);
    req.session.oidc_state = state;

    const authorizationUrl = client.authorizationUrl({
      scope: 'openid profile email',
      login_hint: email || undefined,
      state,
    });

    return res.redirect(authorizationUrl);
  }

  // Existing password login logic here
  console.log('Processing traditional login...');
  res.redirect('/dashboard');
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
      process.env.SSOJET_REDIRECT_URI,
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
    res.redirect('/login?error=oidc_failed');
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

app.listen(process.env.PORT || 3000, () => {
  console.log(`Server running on http://localhost:${process.env.PORT || 3000}`);
});
```

### Step 3: Test the Modified Connection

1. Start your application: `node app.js`.
2. Navigate to your login page (e.g., `http://localhost:3000/login`).
3. Verify that the traditional login form (Email + Password) is visible by default.
4. Click **"Sign in with SSO"** and ensure:
   - The password field disappears.
   - The submit button changes to "Continue with SSO".
5. Enter a test email and submit.
   - You should be redirected to the SSOJet login page.
6. Authenticate with SSOJet.
   - You should be redirected back to `/auth/callback` and then to `/dashboard`.

## 3. Additional Considerations

- **Error Handling**: Enhance the callback route to handle specific OIDC errors gracefully.
- **Styling**: Adapt the example HTML/CSS to match your application's design system.
- **Security**: Use `express-session` with a production-ready store (e.g., Redis, MongoDB) and enable `secure: true` for cookies in production.
- **Environment Variables**: Never commit `.env` to source control. Use secrets management in production.

## 4. Support

- **Contact SSOJet support**: Reach out if you have integration questions.
- **Check application logs**: Use server-side logging to debug OIDC flow issues.
- **Library Documentation**: Refer to the [openid-client documentation](https://github.com/panva/node-openid-client) for advanced configuration.
