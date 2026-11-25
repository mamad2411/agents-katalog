---
name: oidc-hosted-page-php
description: Implement "Sign in with SSO" in vanilla PHP applications using SSOJet OIDC.
---

# Implement SSOJet OIDC (PHP)

This expert AI assistant guide walks you through integrating "Sign in with SSO" functionality into an existing PHP application using SSOJet as an OIDC identity provider.

## 1. Prerequisites

- An existing PHP 8.0+ application with a login page.
- Composer for dependency management.
- An active SSOJet account.
- [SSO Connection Setup Guide](https://docs.ssojet.com/en/how-to-guides/integrations//)
- Required package: `jumbojett/openid-connect-php`.

## 2. Implementation Steps

### Step 1: Create Application in SSOJet

1. Log in to the SSOJet Dashboard.
2. Navigate to **Applications**.
3. Create a new application (e.g., "MyPHPApp", type **Regular Web App**).
4. Configure the callback URI (e.g., `http://localhost:8000/callback.php`).
5. Retrieve **Client ID** and **Client Secret**.
6. Copy the **Issuer URL** from the **Advanced > Endpoints** section.

### Step 2: Modify the Existing PHP Project

#### Substep 2.1: Install Dependencies

```bash
composer require jumbojett/openid-connect-php
```

#### Substep 2.2: Configure Environment

Create a `config.php` file:

```php
<?php
// config.php
return [
    'issuer_url'    => 'https://auth.ssojet.com',
    'client_id'     => 'your_client_id',
    'client_secret' => 'your_client_secret',
    'redirect_uri'  => 'http://localhost:8000/callback.php',
];
```

#### Substep 2.3: Update Login Page/UI

Modify your login page (`login.php`):

```html
<!-- login.php -->
<?php session_start(); ?>
<!DOCTYPE html>
<html>
<head><title>Sign In</title></head>
<body>
<div class="login-container">
    <h1>Sign In</h1>

    <?php if (isset($_GET['error'])): ?>
        <p style="color: red;">Authentication failed. Please try again.</p>
    <?php endif; ?>

    <form id="loginForm" method="POST" action="auth.php">
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

    <button type="button" onclick="toggleSSO()">Sign in with SSO</button>
</div>
<script>
function toggleSSO() {
    const f = document.getElementById('isSSO');
    const p = document.getElementById('passwordField');
    const b = document.getElementById('submitBtn');
    if (f.value === 'false') {
        f.value = 'true'; p.style.display = 'none';
        document.getElementById('password').removeAttribute('required');
        b.textContent = 'Continue with SSO';
    } else {
        f.value = 'false'; p.style.display = 'block';
        document.getElementById('password').setAttribute('required','true');
        b.textContent = 'Sign In';
    }
}
</script>
</body>
</html>
```

#### Substep 2.4: Update Backend Logic

**1. Auth Handler** (`auth.php`):

```php
<?php
// auth.php
session_start();
require_once 'vendor/autoload.php';

use Jumbojett\OpenIDConnectClient;

$config = require 'config.php';
$isSSO = $_POST['is_sso'] ?? 'false';
$email = $_POST['email'] ?? '';

if ($isSSO === 'true') {
    $oidc = new OpenIDConnectClient(
        $config['issuer_url'],
        $config['client_id'],
        $config['client_secret']
    );
    $oidc->setRedirectURL($config['redirect_uri']);
    $oidc->addScope(['openid', 'profile', 'email']);

    // Store email for login_hint
    $_SESSION['login_hint'] = $email;

    $oidc->authenticate();
    // The library handles the redirect automatically
} else {
    // Existing password login logic here
    error_log('Processing traditional login...');
    header('Location: /dashboard.php');
    exit;
}
```

**2. Callback Handler** (`callback.php`):

```php
<?php
// callback.php
session_start();
require_once 'vendor/autoload.php';

use Jumbojett\OpenIDConnectClient;

$config = require 'config.php';

try {
    $oidc = new OpenIDConnectClient(
        $config['issuer_url'],
        $config['client_id'],
        $config['client_secret']
    );
    $oidc->setRedirectURL($config['redirect_uri']);
    $oidc->addScope(['openid', 'profile', 'email']);
    $oidc->authenticate();

    // Get user info
    $name = $oidc->requestUserInfo('name');
    $email = $oidc->requestUserInfo('email');
    $sub = $oidc->requestUserInfo('sub');

    // TODO: Create a session for the user
    $_SESSION['user'] = [
        'sub'   => $sub,
        'name'  => $name,
        'email' => $email,
    ];

    error_log('Authenticated User: ' . json_encode($_SESSION['user']));
    header('Location: /dashboard.php');
    exit;
} catch (Exception $e) {
    error_log('OIDC Callback Error: ' . $e->getMessage());
    header('Location: /login.php?error=oidc_failed');
    exit;
}
```

### Step 3: Test the Modified Connection

1. Start your application: `php -S localhost:8000`.
2. Navigate to `http://localhost:8000/login.php`.
3. Click **"Sign in with SSO"**, enter a test email, and submit.
4. You should be redirected to SSOJet, then back to `/dashboard.php`.

## 3. Additional Considerations

- **Security**: Store secrets outside the web root. Use HTTPS in production.
- **Session Management**: Use secure session configuration in `php.ini`.
- **Styling**: Adapt the HTML to match your application's design system.

## 4. Support

- **Contact SSOJet support**: Reach out if you have integration questions.
- **Library Documentation**: Refer to the [openid-connect-php documentation](https://github.com/jumbojett/OpenID-Connect-PHP).
