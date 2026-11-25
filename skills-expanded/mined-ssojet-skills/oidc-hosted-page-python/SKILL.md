---
name: oidc-hosted-page-python
description: Implement "Sign in with SSO" in Python Flask applications using SSOJet OIDC Authorization Code flow.
---

# Implement SSOJet OIDC (Python / Flask)

This expert AI assistant guide walks you through integrating "Sign in with SSO" functionality into an existing login page in a Python Flask application using SSOJet as an OIDC identity provider. The goal is to modify the existing login flow to add SSO support without disrupting the current traditional login functionality (e.g., email/password).

## 1. Prerequisites

- An existing Python Flask application with a login page.
- Python 3.8+ installed.
- An active SSOJet account.
- [SSO Connection Setup Guide](https://docs.ssojet.com/en/how-to-guides/integrations//)
- Required libraries: `authlib`, `flask`, `python-dotenv`.

## 2. Implementation Steps

### Step 1: Create Application in SSOJet

1. Log in to the SSOJet Dashboard.
2. Navigate to **Applications**.
3. Create a new application (e.g., "MyFlaskApp", type **Regular Web App**).
4. Configure the callback URI (e.g., `http://localhost:5000/auth/callback`).
5. Retrieve **Client ID** and **Client Secret**.
6. Copy the **Issuer URL** from the **Advanced > Endpoints** section.

### Step 2: Modify the Existing Flask Project

#### Substep 2.1: Install Dependencies

Run the following command to install the required libraries:

```bash
pip install authlib flask python-dotenv requests
```

#### Substep 2.2: Configure Environment Variables

Create a `.env` file in the project root:

```env
SSOJET_ISSUER_URL=https://auth.ssojet.com
SSOJET_CLIENT_ID=your_client_id
SSOJET_CLIENT_SECRET=your_client_secret
SSOJET_REDIRECT_URI=http://localhost:5000/auth/callback
FLASK_SECRET_KEY=a_strong_random_secret
```

#### Substep 2.3: Configure OIDC Client

Create a dedicated utility file for OIDC configuration (e.g., `lib/oidc.py`):

```python
# lib/oidc.py
import os
from authlib.integrations.flask_client import OAuth

oauth = OAuth()

def init_oauth(app):
    """Initialize the OAuth registry with the SSOJet provider."""
    oauth.init_app(app)
    oauth.register(
        name='ssojet',
        client_id=os.getenv('SSOJET_CLIENT_ID'),
        client_secret=os.getenv('SSOJET_CLIENT_SECRET'),
        server_metadata_url=f"{os.getenv('SSOJET_ISSUER_URL')}/.well-known/openid-configuration",
        client_kwargs={
            'scope': 'openid profile email',
        },
    )
```

#### Substep 2.4: Update Login Page/UI

Modify your existing login template (e.g., `templates/login.html`) to include the "Sign in with SSO" toggle:

```html
<!-- templates/login.html -->
<!DOCTYPE html>
<html>
<head><title>Sign In</title></head>
<body>
  <div class="login-container">
    <h1>Sign In</h1>

    {% if error %}
      <p style="color: red;">{{ error }}</p>
    {% endif %}

    <form id="loginForm" method="POST" action="/auth/login">
      <div>
        <label for="email">Email</label>
        <input type="email" id="email" name="email" required />
      </div>

      <div id="passwordField">
        <label for="password">Password</label>
        <input type="password" id="password" name="password" required />
      </div>

      <input type="hidden" id="isSSO" name="is_sso" value="false" />

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
</body>
</html>
```

#### Substep 2.5: Update Backend Logic

Create the necessary routes to handle the OIDC flow.

**1. Main Application Setup** (`app.py`):

```python
# app.py
import os
import secrets
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, session, render_template, request
from lib.oidc import oauth, init_oauth

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Initialize OAuth
init_oauth(app)


@app.route('/login')
def login_page():
    error = request.args.get('error')
    return render_template('login.html', error=error)


@app.route('/auth/login', methods=['POST'])
def login():
    email = request.form.get('email')
    is_sso = request.form.get('is_sso')

    if is_sso == 'true':
        # Generate a random state for CSRF protection
        state = secrets.token_urlsafe(16)
        session['oidc_state'] = state

        redirect_uri = os.getenv('SSOJET_REDIRECT_URI')
        return oauth.ssojet.authorize_redirect(
            redirect_uri,
            login_hint=email,
            state=state,
        )

    # Existing password login logic here
    print('Processing traditional login...')
    return redirect('/dashboard')


@app.route('/auth/callback')
def callback():
    try:
        # Verify state
        stored_state = session.pop('oidc_state', None)
        received_state = request.args.get('state')

        if stored_state != received_state:
            return redirect('/login?error=state_mismatch')

        token = oauth.ssojet.authorize_access_token()
        userinfo = token.get('userinfo')

        if not userinfo:
            userinfo = oauth.ssojet.userinfo()

        # TODO: Create a session for the user based on `userinfo`
        session['user'] = dict(userinfo)
        print('Authenticated User:', userinfo)

        # Redirect to the dashboard or intended page
        return redirect('/dashboard')
    except Exception as e:
        print(f'OIDC Callback Error: {e}')
        return redirect('/login?error=oidc_failed')


@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if not user:
        return redirect('/login')
    return f"<h1>Dashboard</h1><pre>{user}</pre><a href='/auth/logout'>Logout</a>"


@app.route('/auth/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### Step 3: Test the Modified Connection

1. Start your application: `python app.py`.
2. Navigate to your login page (e.g., `http://localhost:5000/login`).
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
- **Security**: Use a production-grade session backend (e.g., Redis via `flask-session`) and serve over HTTPS.
- **Environment Variables**: Never commit `.env` to source control. Use secrets management in production.

## 4. Support

- **Contact SSOJet support**: Reach out if you have integration questions.
- **Check application logs**: Use server-side logging to debug OIDC flow issues.
- **Library Documentation**: Refer to the [Authlib documentation](https://docs.authlib.org/en/latest/) for advanced configuration.
