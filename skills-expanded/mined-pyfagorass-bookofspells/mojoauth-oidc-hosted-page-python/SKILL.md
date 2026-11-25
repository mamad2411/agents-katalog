---
name: mojoauth-oidc-hosted-page-python
description: Implement passwordless authentication in Python Flask applications using MojoAuth OIDC Hosted Login Page.
---

# Implement MojoAuth OIDC (Python / Flask)

This expert AI assistant guide walks you through integrating passwordless authentication into a Python Flask application using MojoAuth's Hosted Login Page as an OIDC identity provider. MojoAuth handles all authentication methods (Magic Links, Email OTP, SMS OTP, Social Login, Passkeys) through its hosted page.

## 1. Prerequisites

- An existing Python Flask application.
- Python 3.8+ installed.
- An active MojoAuth account.
- [MojoAuth OIDC Setup Guide](https://docs.mojoauth.com/hosted-login-page/)
- Required libraries: `authlib`, `flask`, `python-dotenv`.

## 2. Implementation Steps

### Step 1: Configure Application in MojoAuth

1. Log in to the [MojoAuth Dashboard](https://mojoauth.com/dashboard).
2. Note your **MojoAuth Domain** (e.g., `your-app.mojoauth.com`).
3. Configure the **Redirect URI** (e.g., `http://localhost:5000/auth/callback`).
4. Retrieve **Client ID** and **Client Secret**.
5. Enable your preferred authentication methods.

### Step 2: Modify the Existing Flask Project

#### Substep 2.1: Install Dependencies

```bash
pip install authlib flask python-dotenv requests
```

#### Substep 2.2: Configure Environment Variables

Create a `.env` file in the project root:

```env
MOJOAUTH_DOMAIN=your-app.mojoauth.com
MOJOAUTH_CLIENT_ID=your_client_id
MOJOAUTH_CLIENT_SECRET=your_client_secret
MOJOAUTH_REDIRECT_URI=http://localhost:5000/auth/callback
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
    """Initialize the OAuth registry with the MojoAuth provider."""
    oauth.init_app(app)
    oauth.register(
        name='mojoauth',
        client_id=os.getenv('MOJOAUTH_CLIENT_ID'),
        client_secret=os.getenv('MOJOAUTH_CLIENT_SECRET'),
        server_metadata_url=f"https://{os.getenv('MOJOAUTH_DOMAIN')}/.well-known/openid-configuration",
        client_kwargs={
            'scope': 'openid profile email',
        },
    )
```

#### Substep 2.4: Update Login Page/UI

Since MojoAuth handles all authentication on its Hosted Login Page, your login page only needs a **"Sign In" link**:

```html
<!-- templates/login.html -->
<!DOCTYPE html>
<html>
<head><title>Sign In</title></head>
<body>
  <div class="login-container">
    <h1>Welcome</h1>
    <p>Sign in with your preferred method — passwordless, social login, or passkeys.</p>

    {% if error %}
      <p style="color: red;">{{ error }}</p>
    {% endif %}

    <a href="/auth/login" class="sign-in-button">Sign In with MojoAuth</a>

    <p class="powered-by">Powered by MojoAuth — Passwordless Authentication</p>
  </div>
</body>
</html>
```

#### Substep 2.5: Update Backend Logic

**Main Application Setup** (`app.py`):

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


@app.route('/auth/login')
def login():
    # Generate a random state for CSRF protection
    state = secrets.token_urlsafe(16)
    session['oidc_state'] = state

    redirect_uri = os.getenv('MOJOAUTH_REDIRECT_URI')
    return oauth.mojoauth.authorize_redirect(
        redirect_uri,
        state=state,
    )


@app.route('/auth/callback')
def callback():
    try:
        # Verify state
        stored_state = session.pop('oidc_state', None)
        received_state = request.args.get('state')

        if stored_state != received_state:
            return redirect('/login?error=state_mismatch')

        token = oauth.mojoauth.authorize_access_token()
        userinfo = token.get('userinfo')

        if not userinfo:
            userinfo = oauth.mojoauth.userinfo()

        # TODO: Create a session for the user based on `userinfo`
        session['user'] = dict(userinfo)
        print('Authenticated User:', userinfo)

        # Redirect to the dashboard or intended page
        return redirect('/dashboard')
    except Exception as e:
        print(f'OIDC Callback Error: {e}')
        return redirect('/login?error=auth_failed')


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

### Step 3: Test the Implementation

1. Start your application: `python app.py`.
2. Navigate to `http://localhost:5000/login`.
3. Click **"Sign In with MojoAuth"**.
4. You should be redirected to the MojoAuth Hosted Login Page.
5. Authenticate using any available method.
6. After successful authentication, you should be redirected back to `/auth/callback` and then to `/dashboard`.

## 3. Additional Considerations

- **Error Handling**: Enhance the callback route to handle specific OIDC errors gracefully.
- **Styling**: Adapt the example HTML/CSS to match your application's design system.
- **Security**: Use a production-grade session backend (e.g., Redis via `flask-session`) and serve over HTTPS.
- **Environment Variables**: Never commit `.env` to source control. Use secrets management in production.

## 4. Support

- **MojoAuth Documentation**: [mojoauth.com/docs](https://mojoauth.com/docs)
- **Check application logs**: Use server-side logging to debug OIDC flow issues.
- **Library Documentation**: Refer to the [Authlib documentation](https://docs.authlib.org/en/latest/) for advanced configuration.
