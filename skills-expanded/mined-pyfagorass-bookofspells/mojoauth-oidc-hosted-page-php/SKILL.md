---
name: mojoauth-oidc-hosted-page-php
description: Implement passwordless authentication in vanilla PHP applications using MojoAuth OIDC.
---

# Implement MojoAuth OIDC (PHP)

This expert AI assistant guide walks you through integrating passwordless authentication into an existing PHP application using MojoAuth's Hosted Login Page as an OIDC identity provider. MojoAuth handles all authentication methods (Magic Links, Email OTP, SMS OTP, Social Login, Passkeys) through its hosted page.

## 1. Prerequisites

- An existing PHP 8.0+ application.
- Composer for dependency management.
- An active MojoAuth account.
- [MojoAuth OIDC Setup Guide](https://docs.mojoauth.com/hosted-login-page/)
- Required package: `jumbojett/openid-connect-php`.

## 2. Implementation Steps

### Step 1: Configure Application in MojoAuth

1. Log in to the [MojoAuth Dashboard](https://mojoauth.com/dashboard).
2. Note your **MojoAuth Domain** (e.g., `your-app.mojoauth.com`).
3. Configure the **Redirect URI** (e.g., `http://localhost:8000/callback.php`).
4. Retrieve **Client ID** and **Client Secret**.
5. Enable your preferred authentication methods.

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
    'domain'        => 'your-app.mojoauth.com',
    'client_id'     => 'your_client_id',
    'client_secret' => 'your_client_secret',
    'redirect_uri'  => 'http://localhost:8000/callback.php',
];
```

#### Substep 2.3: Update Login Page/UI

Since MojoAuth handles all authentication on its Hosted Login Page, your login page only needs a **"Sign In" link**:

```html
<!-- login.php -->
<?php session_start(); ?>
<!DOCTYPE html>
<html>
<head><title>Sign In</title></head>
<body>
<div class="login-container">
    <h1>Welcome</h1>
    <p>Sign in with your preferred method — passwordless, social login, or passkeys.</p>

    <?php if (isset($_GET['error'])): ?>
        <p style="color: red;">Authentication failed. Please try again.</p>
    <?php endif; ?>

    <a href="auth.php" class="sign-in-button">Sign In with MojoAuth</a>

    <p class="powered-by">Powered by MojoAuth — Passwordless Authentication</p>
</div>
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

$oidc = new OpenIDConnectClient(
    'https://' . $config['domain'],
    $config['client_id'],
    $config['client_secret']
);
$oidc->setRedirectURL($config['redirect_uri']);
$oidc->addScope(['openid', 'profile', 'email']);

// Redirect to MojoAuth Hosted Login Page
$oidc->authenticate();
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
        'https://' . $config['domain'],
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
    header('Location: /login.php?error=auth_failed');
    exit;
}
```

### Step 3: Test the Implementation

1. Start your application: `php -S localhost:8000`.
2. Navigate to `http://localhost:8000/login.php`.
3. Click **"Sign In with MojoAuth"**.
4. You should be redirected to the MojoAuth Hosted Login Page.
5. Authenticate using any available method.
6. After successful authentication, you should be redirected back to `/dashboard.php`.

## 3. Additional Considerations

- **Security**: Store secrets outside the web root. Use HTTPS in production.
- **Session Management**: Use secure session configuration in `php.ini`.
- **Styling**: Adapt the HTML to match your application's design system.

## 4. Support

- **MojoAuth Documentation**: [mojoauth.com/docs](https://mojoauth.com/docs)
- **Library Documentation**: Refer to the [openid-connect-php documentation](https://github.com/jumbojett/OpenID-Connect-PHP).
