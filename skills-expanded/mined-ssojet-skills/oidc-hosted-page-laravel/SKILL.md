---
name: oidc-hosted-page-laravel
description: Implement "Sign in with SSO" in Laravel applications using SSOJet OIDC with Socialite.
---

# Implement SSOJet OIDC (PHP / Laravel)

This expert AI assistant guide walks you through integrating "Sign in with SSO" functionality into an existing login page in a Laravel application using SSOJet as an OIDC identity provider.

## 1. Prerequisites

- An existing Laravel 10+ application with a login page.
- PHP 8.1+ and Composer.
- An active SSOJet account.
- [SSO Connection Setup Guide](https://docs.ssojet.com/en/how-to-guides/integrations//)
- Required package: `laravel/socialite`.

## 2. Implementation Steps

### Step 1: Create Application in SSOJet

1. Log in to the SSOJet Dashboard.
2. Navigate to **Applications**.
3. Create a new application (e.g., "MyLaravelApp", type **Regular Web App**).
4. Configure the callback URI (e.g., `http://localhost:8000/auth/callback`).
5. Retrieve **Client ID** and **Client Secret**.
6. Copy the **Issuer URL** from the **Advanced > Endpoints** section.

### Step 2: Modify the Existing Laravel Project

#### Substep 2.1: Install Dependencies

```bash
composer require laravel/socialite
```

#### Substep 2.2: Configure Environment Variables

Add to your `.env` file:

```env
SSOJET_ISSUER_URL=https://auth.ssojet.com
SSOJET_CLIENT_ID=your_client_id
SSOJET_CLIENT_SECRET=your_client_secret
SSOJET_REDIRECT_URI=http://localhost:8000/auth/callback
```

Add to `config/services.php`:

```php
'ssojet' => [
    'issuer_url' => env('SSOJET_ISSUER_URL'),
    'client_id' => env('SSOJET_CLIENT_ID'),
    'client_secret' => env('SSOJET_CLIENT_SECRET'),
    'redirect' => env('SSOJET_REDIRECT_URI'),
],
```

#### Substep 2.3: Create SSOJet Socialite Provider

```php
<?php
// app/Providers/SSOJetProvider.php
namespace App\Providers;

use Laravel\Socialite\Two\AbstractProvider;
use Laravel\Socialite\Two\User;

class SSOJetProvider extends AbstractProvider
{
    protected $scopes = ['openid', 'profile', 'email'];
    protected $scopeSeparator = ' ';

    protected function getAuthUrl($state)
    {
        return $this->buildAuthUrlFromBase(
            config('services.ssojet.issuer_url') . '/oauth2/authorize', $state
        );
    }

    protected function getTokenUrl()
    {
        return config('services.ssojet.issuer_url') . '/oauth2/token';
    }

    protected function getUserByToken($token)
    {
        $response = $this->getHttpClient()->get(
            config('services.ssojet.issuer_url') . '/oauth2/userinfo',
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
use App\Providers\SSOJetProvider;

public function boot(): void
{
    Socialite::extend('ssojet', function ($app) {
        $config = $app['config']['services.ssojet'];
        return new SSOJetProvider($app['request'], $config['client_id'], $config['client_secret'], $config['redirect']);
    });
}
```

#### Substep 2.4: Update Login Page/UI

Modify `resources/views/auth/login.blade.php`:

```html
<div class="login-container">
    <h1>Sign In</h1>
    <form id="loginForm" method="POST" action="{{ route('login') }}">
        @csrf
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
```

#### Substep 2.5: Update Backend Logic

**SSO Controller** (`app/Http/Controllers/SSOController.php`):

```php
<?php
namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Laravel\Socialite\Facades\Socialite;
use Illuminate\Support\Facades\Auth;
use App\Models\User;

class SSOController extends Controller
{
    public function login(Request $request)
    {
        if ($request->input('is_sso') === 'true') {
            return Socialite::driver('ssojet')
                ->with(['login_hint' => $request->input('email')])
                ->redirect();
        }
        // Existing password login logic
        $credentials = $request->validate(['email' => 'required|email', 'password' => 'required']);
        if (Auth::attempt($credentials)) {
            $request->session()->regenerate();
            return redirect('/dashboard');
        }
        return back()->withErrors(['email' => 'Invalid credentials.']);
    }

    public function callback(Request $request)
    {
        try {
            $ssojetUser = Socialite::driver('ssojet')->user();
            $user = User::updateOrCreate(
                ['email' => $ssojetUser->getEmail()],
                ['name' => $ssojetUser->getName(), 'ssojet_id' => $ssojetUser->getId()]
            );
            Auth::login($user);
            return redirect('/dashboard');
        } catch (\Exception $e) {
            \Log::error('OIDC Callback Error: ' . $e->getMessage());
            return redirect('/login')->withErrors(['sso' => 'SSO authentication failed.']);
        }
    }
}
```

**Routes** (`routes/web.php`):

```php
use App\Http\Controllers\SSOController;
Route::get('/login', fn() => view('auth.login'))->name('login');
Route::post('/login', [SSOController::class, 'login']);
Route::get('/auth/callback', [SSOController::class, 'callback']);
```

### Step 3: Test the Modified Connection

1. Start your application: `php artisan serve`.
2. Navigate to `http://localhost:8000/login`.
3. Click **"Sign in with SSO"**, enter a test email, and submit.
4. You should be redirected to SSOJet, then back to `/dashboard`.

## 3. Additional Considerations

- **Security**: Never commit `.env` to source control.
- **Database**: Add a `ssojet_id` column to the `users` table via migration.
- **Styling**: Adapt the Blade templates to match your design system.

## 4. Support

- **Contact SSOJet support**: Reach out if you have integration questions.
- **Library Documentation**: Refer to the [Laravel Socialite documentation](https://laravel.com/docs/socialite).
