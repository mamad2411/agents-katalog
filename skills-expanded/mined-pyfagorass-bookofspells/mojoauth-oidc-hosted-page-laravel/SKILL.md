---
name: mojoauth-oidc-hosted-page-laravel
description: Implement passwordless authentication in Laravel applications using MojoAuth OIDC with Socialite.
---

# Implement MojoAuth OIDC (PHP / Laravel)

This expert AI assistant guide walks you through integrating passwordless authentication into a Laravel application using MojoAuth's Hosted Login Page as an OIDC identity provider. MojoAuth handles all authentication methods (Magic Links, Email OTP, SMS OTP, Social Login, Passkeys) through its hosted page.

## 1. Prerequisites

- An existing Laravel 10+ application.
- PHP 8.1+ and Composer.
- An active MojoAuth account.
- [MojoAuth OIDC Setup Guide](https://docs.mojoauth.com/hosted-login-page/)
- Required package: `laravel/socialite`.

## 2. Implementation Steps

### Step 1: Configure Application in MojoAuth

1. Log in to the [MojoAuth Dashboard](https://mojoauth.com/dashboard).
2. Note your **MojoAuth Domain** (e.g., `your-app.mojoauth.com`).
3. Configure the **Redirect URI** (e.g., `http://localhost:8000/auth/callback`).
4. Retrieve **Client ID** and **Client Secret**.
5. Enable your preferred authentication methods.

### Step 2: Modify the Existing Laravel Project

#### Substep 2.1: Install Dependencies

```bash
composer require laravel/socialite
```

#### Substep 2.2: Configure Environment Variables

Add to your `.env` file:

```env
MOJOAUTH_DOMAIN=your-app.mojoauth.com
MOJOAUTH_CLIENT_ID=your_client_id
MOJOAUTH_CLIENT_SECRET=your_client_secret
MOJOAUTH_REDIRECT_URI=http://localhost:8000/auth/callback
```

Add to `config/services.php`:

```php
'mojoauth' => [
    'domain' => env('MOJOAUTH_DOMAIN'),
    'client_id' => env('MOJOAUTH_CLIENT_ID'),
    'client_secret' => env('MOJOAUTH_CLIENT_SECRET'),
    'redirect' => env('MOJOAUTH_REDIRECT_URI'),
],
```

#### Substep 2.3: Create MojoAuth Socialite Provider

```php
<?php
// app/Providers/MojoAuthProvider.php
namespace App\Providers;

use Laravel\Socialite\Two\AbstractProvider;
use Laravel\Socialite\Two\User;

class MojoAuthProvider extends AbstractProvider
{
    protected $scopes = ['openid', 'profile', 'email'];
    protected $scopeSeparator = ' ';

    protected function getAuthUrl($state)
    {
        return $this->buildAuthUrlFromBase(
            'https://' . config('services.mojoauth.domain') . '/oauth/authorize', $state
        );
    }

    protected function getTokenUrl()
    {
        return 'https://' . config('services.mojoauth.domain') . '/oauth2/token';
    }

    protected function getUserByToken($token)
    {
        $response = $this->getHttpClient()->get(
            'https://' . config('services.mojoauth.domain') . '/oauth/userinfo',
            ['headers' => ['Authorization' => 'Bearer ' . $token]]
        );
        return json_decode($response->getBody(), true);
    }

    protected function mapUserToObject(array $user)
    {
        return (new User())->setRaw($user)->map([
            'id' => $user['sub'] ?? null,
            'name' => $user['name'] ?? null,
            'email' => $user['email'] ?? null,
        ]);
    }
}
```

Register in `AppServiceProvider.php`:

```php
use Laravel\Socialite\Facades\Socialite;
use App\Providers\MojoAuthProvider;

public function boot(): void
{
    Socialite::extend('mojoauth', function ($app) {
        $config = $app['config']['services.mojoauth'];
        return new MojoAuthProvider($app['request'], $config['client_id'], $config['client_secret'], $config['redirect']);
    });
}
```

#### Substep 2.4: Update Login Page/UI

Since MojoAuth handles all authentication on its Hosted Login Page, your login view only needs a **"Sign In" link**:

```html
<!-- resources/views/auth/login.blade.php -->
<div class="login-container">
    <h1>Welcome</h1>
    <p>Sign in with your preferred method — passwordless, social login, or passkeys.</p>

    @if ($errors->any())
      <p style="color: red;">{{ $errors->first() }}</p>
    @endif

    <a href="{{ route('auth.login') }}" class="sign-in-button">Sign In with MojoAuth</a>

    <p class="powered-by">Powered by MojoAuth — Passwordless Authentication</p>
</div>
```

#### Substep 2.5: Update Backend Logic

**Auth Controller** (`app/Http/Controllers/AuthController.php`):

```php
<?php
namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Laravel\Socialite\Facades\Socialite;
use Illuminate\Support\Facades\Auth;
use App\Models\User;

class AuthController extends Controller
{
    public function login()
    {
        return Socialite::driver('mojoauth')->redirect();
    }

    public function callback(Request $request)
    {
        try {
            $mojoauthUser = Socialite::driver('mojoauth')->user();
            $user = User::updateOrCreate(
                ['email' => $mojoauthUser->getEmail()],
                ['name' => $mojoauthUser->getName(), 'mojoauth_id' => $mojoauthUser->getId()]
            );
            Auth::login($user);
            return redirect('/dashboard');
        } catch (\Exception $e) {
            \Log::error('OIDC Callback Error: ' . $e->getMessage());
            return redirect('/login')->withErrors(['auth' => 'Authentication failed.']);
        }
    }
}
```

**Routes** (`routes/web.php`):

```php
use App\Http\Controllers\AuthController;
Route::get('/login', fn() => view('auth.login'))->name('login');
Route::get('/auth/login', [AuthController::class, 'login'])->name('auth.login');
Route::get('/auth/callback', [AuthController::class, 'callback']);
```

### Step 3: Test the Implementation

1. Start your application: `php artisan serve`.
2. Navigate to `http://localhost:8000/login`.
3. Click **"Sign In with MojoAuth"**.
4. You should be redirected to the MojoAuth Hosted Login Page.
5. Authenticate using any available method.
6. After successful authentication, you should be redirected back to `/dashboard`.

## 3. Additional Considerations

- **Security**: Never commit `.env` to source control.
- **Database**: Add a `mojoauth_id` column to the `users` table via migration.
- **Styling**: Adapt the Blade templates to match your design system.

## 4. Support

- **MojoAuth Documentation**: [mojoauth.com/docs](https://mojoauth.com/docs)
- **Library Documentation**: Refer to the [Laravel Socialite documentation](https://laravel.com/docs/socialite).
