---
name: moonshine-security-v4
description: Use when working on MoonShine v4 authentication, authorization, login, guards, custom user models, Socialite, 2FA, JWT, role-based access, Laravel policies, auth pipelines, or custom auth responses.
---

# MoonShine v4 -- Security (Authentication & Authorization)

## 1. Authentication Basics

MoonShine ships with a self-contained authentication system backed by its own guard, user model, and middleware stack. The `MoonShineAuth` helper class provides runtime access:

```php
use MoonShine\Laravel\MoonShineAuth;

$guard = MoonShineAuth::getGuard();          // Active guard instance
$guardName = MoonShineAuth::getGuardName();  // 'moonshine'
$userModel = MoonShineAuth::getModel();      // Configured user model instance
```

The `Authenticate` middleware checks `moonshineConfig()->isAuthEnabled()` and redirects unauthenticated requests to the login page.

## 2. Configuration

All authentication settings live in `config/moonshine.php` under the `auth` key:

```php
// config/moonshine.php
'auth' => [
    'enabled' => true,
    'guard' => 'moonshine',
    'model' => MoonshineUser::class,
    'middleware' => [
        Authenticate::class,
    ],
    'pipelines' => [],
],

'user_fields' => [
    'username' => 'email',
    'password' => 'password',
    'name' => 'name',
    'avatar' => 'avatar',
],
```

- `enabled` -- toggle the entire auth system on or off.
- `guard` -- the Laravel guard name MoonShine uses.
- `model` -- Eloquent model representing admin users.
- `middleware` -- array of middleware classes protecting MoonShine routes (v4 uses an array, not a single class).
- `pipelines` -- ordered list of pipeline classes that run during login.

## 3. Disabling Authentication

Set `enabled` to `false` to remove all auth checks from the panel:

```php
'auth' => [
    'enabled' => false,
],
```

## 4. Custom User Model

Replace the default `MoonshineUser` with your own model:

```php
// config/moonshine.php
'auth' => [
    'model' => App\Models\Admin::class,
],
```

## 5. Custom User Fields & Profile

### Field mapping via config

When your model uses different column names, map them in `user_fields`:

```php
// config/moonshine.php
'user_fields' => [
    'username' => 'login',
    'password' => 'pass',
    'name' => 'full_name',
    'avatar' => 'profile_image',
],
```

### Field mapping via MoonShineServiceProvider

```php
$config
    ->userField('username', 'login')
    ->userField('password', 'pass')
    ->userField('name', 'full_name')
    ->userField('avatar', 'profile_image');
```

### Custom profile page

Replace the built-in profile page via config:

```php
// config/moonshine.php
'pages' => [
    'profile' => App\MoonShine\Pages\CustomProfile::class,
],
```

Or via the service provider:

```php
$config->changePage(
    \MoonShine\Laravel\Pages\ProfilePage::class,
    \App\MoonShine\Pages\CustomProfile::class
);
```

### Custom login page

```php
// config/moonshine.php
'pages' => [
    'login' => App\MoonShine\Pages\CustomLogin::class,
],
```

## 6. Role-Based Access

Create middleware to restrict panel access by role, then register it in `config/moonshine.php` under the `middleware` array:

```php
namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class CheckAdminRole
{
    public function handle(Request $request, Closure $next): Response
    {
        if ($request->user() && ! $request->user()->hasRole('admin')) {
            abort(403, 'Access denied.');
        }
        return $next($request);
    }
}
```

```php
// config/moonshine.php
'middleware' => [
    \App\Http\Middleware\CheckAdminRole::class,
],
```

## 7. Authentication Pipelines

Pipelines run after username/password validation but before the session is created. They can redirect users (e.g., to a 2FA challenge page) or add custom checks.

### How the pipeline executes

The `AuthenticateController` sends the request through configured pipelines via Laravel's `Pipeline` facade. If a pipeline returns a `RedirectResponse` or `MoonShine\Crud\JsonResponse`, the login flow stops. Otherwise, authentication proceeds.

### Configuring pipelines

Via config:

```php
// config/moonshine.php
'auth' => [
    'pipelines' => [
        TwoFactorAuthentication::class,
        PhoneVerification::class,
    ],
],
```

Via MoonShineServiceProvider:

```php
$config->authPipelines([
    \App\MoonShine\AuthPipelines\TwoFactorAuthentication::class,
    \App\MoonShine\AuthPipelines\PhoneVerification::class,
]);
```

### Writing a custom pipeline

A pipeline class must implement a `handle` method that receives the request and a `$next` closure:

```php
namespace App\MoonShine\AuthPipelines;

use Closure;
use Illuminate\Http\Request;
use MoonShine\Laravel\Models\MoonshineUser;

class PhoneVerification
{
    public function handle(Request $request, Closure $next)
    {
        $user = MoonshineUser::query()
            ->where('email', $request->get('username'))
            ->first();

        if (! is_null($user) && ! is_null($user->getAttribute('phone'))) {
            $request->session()->put([
                'login.id' => $user->getKey(),
                'login.remember' => $request->boolean('remember'),
            ]);

            return redirect()->route('sms-challenge');
        }

        return $next($request);
    }
}
```

Pipeline order matters -- they execute sequentially.

## 8. Custom Auth Responses (NEW in v4)

MoonShine v4 introduces `authenticateUsing()` and `logoutUsing()` methods to completely override the behavior during authentication and logout.

### authenticateUsing

Override behavior after successful authentication. The callback receives a `$default` closure that executes the standard logic:

```php
// In MoonShineServiceProvider
use Closure;
use Symfony\Component\HttpFoundation\Response;

$config->authenticateUsing(function (Closure $default): Response {
    // Custom redirect after login
    return redirect()->to('/dashboard');

    // Or use the default behavior
    // return $default();
});
```

### logoutUsing

Override behavior during logout:

```php
use Closure;
use Symfony\Component\HttpFoundation\Response;

$config->logoutUsing(function (Closure $default): Response {
    // Custom redirect after logout
    return redirect()->to('/');

    // Or use the default behavior
    // return $default();
});
```

### Combined usage example

```php
use Closure;
use Symfony\Component\HttpFoundation\Response;

$config->authenticateUsing(function (Closure $default): Response {
    logger()->info('User logged in', ['user' => auth()->id()]);

    return $default();
});

$config->logoutUsing(function (Closure $default): Response {
    logger()->info('User logged out');

    return redirect()->to('/');
});
```

## 9. Authorization

MoonShine uses standard Laravel Policies. By default, policy checks are disabled on resources. Enable them with the `$withPolicy` property.

### Enabling policies on a resource

```php
namespace App\MoonShine\Resources;

use MoonShine\Laravel\Resources\ModelResource;

class PostResource extends ModelResource
{
    protected bool $withPolicy = true;
}
```

### Available policy methods

| Policy method | Controls | Ability enum |
|---------------|----------|--------------|
| `viewAny` | Index page | `Ability::VIEW_ANY` |
| `view` | Detail page | `Ability::VIEW` |
| `create` | Creating a record | `Ability::CREATE` |
| `update` | Editing a record | `Ability::UPDATE` |
| `delete` | Deleting a record | `Ability::DELETE` |
| `massDelete` | Mass deletion | `Ability::MASS_DELETE` |
| `restore` | Restoring soft-deleted record | `Ability::RESTORE` |
| `forceDelete` | Permanent deletion | `Ability::FORCE_DELETE` |

Note: In v4, the Ability enum lives at `MoonShine\Support\Enums\Ability` (was `MoonShine\Laravel\Enums\Ability` in v3).

### Writing a policy

Each policy method receives the auth user model as its first argument. Methods that operate on a specific record also receive the model instance. The first type-hint must match your configured auth model (default: `MoonshineUser`):

```php
namespace App\Policies;

use App\Models\Post;
use Illuminate\Auth\Access\HandlesAuthorization;
use MoonShine\Laravel\Models\MoonshineUser;

class PostPolicy
{
    use HandlesAuthorization;

    public function viewAny(MoonshineUser $user) { return true; }
    public function view(MoonshineUser $user, Post $model) { return true; }
    public function create(MoonshineUser $user) { return true; }
    public function update(MoonshineUser $user, Post $model) { return true; }
    public function delete(MoonshineUser $user, Post $model) { return true; }
    public function massDelete(MoonshineUser $user) { return true; }
    public function restore(MoonshineUser $user, Post $model) { return true; }
    public function forceDelete(MoonshineUser $user, Post $model) { return true; }
}
```

Generate a policy scaffold: `php artisan moonshine:policy PostPolicy`

For models outside `app/Models`, register policies manually:

```php
use Illuminate\Support\Facades\Gate;

Gate::policy(MoonshineUser::class, MoonshineUserPolicy::class);
```

See [references/auth-extensions.md](references/auth-extensions.md) for a complete policy example with real authorization logic.

## 10. Additional Authorization Logic

### authorizationRules

Add authorization logic that applies across all resources:

```php
use MoonShine\Contracts\Core\ResourceContract;
use MoonShine\Support\Enums\Ability;
use Illuminate\Database\Eloquent\Model;

// In MoonShineServiceProvider boot()
$config->authorizationRules(
    static function (ResourceContract $resource, Model $user, Ability $ability, Model $item): bool {
        return true;
    }
);
```

Global rules run alongside resource-level policies. When `$withPolicy = true`, both the policy and all global rules must return `true` for access to be granted.

## 11. Socialite

The `moonshine/socialite` package integrates Laravel Socialite for social login.

```shell
composer require moonshine/socialite
php artisan migrate
php artisan vendor:publish --provider="MoonShine\Socialite\Providers\SocialiteServiceProvider"
```

Configure drivers in `config/moonshine-socialite.php`, add `HasMoonShineSocialite` trait to user model, and update `auth.model` in config. The `SocialAuth` component is auto-added to profile/login pages. See [references/auth-extensions.md](references/auth-extensions.md) for complete setup.

## 12. Two-Factor Authentication

The `moonshine/two-factor` package adds TOTP-based 2FA via an auth pipeline.

```shell
composer require moonshine/two-factor
php artisan migrate
```

Add `TwoFactorAuthPipe::class` to `auth.pipelines` in config (or via `$config->authPipelines()`), add `TwoFactorAuthenticatable` trait to user model, and update `auth.model`. The `TwoFactor` component is auto-added to the profile page. See [references/auth-extensions.md](references/auth-extensions.md) for complete setup.

## 13. JWT

MoonShine can operate in API mode with JWT token-based authentication. For full details, see the **moonshine-frontend-v4** skill (API section).

## 14. Cross-References

- **moonshine-setup-v4** -- Auth configuration keys in `config/moonshine.php`, guard setup, user field mapping.
- **moonshine-resources-v4** -- Resource-level authorization with `$withPolicy`, `isCan()`, and `getGateAbilities()`.
- **moonshine-frontend-v4** -- JWT-based API authentication for headless/SPA use cases.
- [references/auth-extensions.md](references/auth-extensions.md) -- Full code examples for pipelines, policies, Socialite, 2FA, custom auth responses, middleware, and authorization rules.

## v3 to v4 Migration Notes

| Change | v3 | v4 |
|--------|----|----|
| Ability enum | `MoonShine\Laravel\Enums\Ability` | `MoonShine\Support\Enums\Ability` |
| JsonResponse | `MoonShine\Laravel\Http\Responses\MoonShineJsonResponse` | `MoonShine\Crud\JsonResponse` |
| Auth middleware config | Single class | Array of middleware classes |
| Custom auth responses | Not available | `authenticateUsing()` and `logoutUsing()` methods |

## Login Flow Summary

1. User submits credentials to `AuthenticateController::authenticate()`.
2. `LoginFormRequest` validates `username` and `password` fields, applies rate limiting.
3. If auth pipelines are configured, the request passes through each one in order.
4. If a pipeline returns a redirect or JSON response, the flow stops (e.g., 2FA challenge).
5. If `authenticateUsing()` is configured, it controls the post-login response.
6. Otherwise, `LoginFormRequest::authenticate()` calls `MoonShineAuth::getGuard()->attempt()`.
7. On success, the session is regenerated and the user is redirected to the home route.
8. On failure, a `ValidationException` is thrown with rate-limiter tracking.
