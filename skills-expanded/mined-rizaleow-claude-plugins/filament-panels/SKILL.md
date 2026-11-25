---
description: Configure Filament v5 Panels — `PanelProvider` classes, multi-tenancy, auth (login/register/reset/profile), brand assets, navigation, plugin registration, dark mode, `canAccessPanel`. Use when creating or modifying a Filament panel, configuring tenancy, or wiring auth.
---

# Filament v5 Panels

A Panel is a self-contained admin app. Each panel is declared by a `PanelProvider` registered in `bootstrap/providers.php`. Multi-panel apps (`admin`, `app`, `portal`) just register multiple providers.

## Preflight

- `mcp__boost__filament_list_panels` — list registered panel IDs/paths.
- `mcp__boost__filament_list_installed_plugins` — see what Filament plugins are available to register.

## Canonical provider

```php
namespace App\Providers\Filament;

use Filament\Http\Middleware\Authenticate;
use Filament\Http\Middleware\AuthenticateSession;
use Filament\Http\Middleware\DisableBladeIconComponents;
use Filament\Http\Middleware\DispatchServingFilamentEvent;
use Filament\Pages\Dashboard;
use Filament\Panel;
use Filament\PanelProvider;
use Filament\Support\Colors\Color;
use Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse;
use Illuminate\Cookie\Middleware\EncryptCookies;
use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken;
use Illuminate\Routing\Middleware\SubstituteBindings;
use Illuminate\Session\Middleware\StartSession;
use Illuminate\View\Middleware\ShareErrorsFromSession;

class AdminPanelProvider extends PanelProvider
{
    public function panel(Panel $panel): Panel
    {
        return $panel
            ->id('admin')
            ->path('admin')
            ->default()
            ->login()
            ->passwordReset()
            ->emailVerification()
            ->profile()
            ->colors(['primary' => Color::Indigo])
            ->brandName('Acme Admin')
            ->brandLogo(asset('img/logo.svg'))
            ->favicon(asset('favicon.ico'))
            ->darkMode()
            ->sidebarCollapsibleOnDesktop()
            ->discoverResources(in: app_path('Filament/Resources'), for: 'App\\Filament\\Resources')
            ->discoverPages(in: app_path('Filament/Pages'), for: 'App\\Filament\\Pages')
            ->discoverWidgets(in: app_path('Filament/Widgets'), for: 'App\\Filament\\Widgets')
            ->pages([Dashboard::class])
            ->navigationGroups(['CRM', 'Billing', 'System'])
            ->middleware([
                EncryptCookies::class,
                AddQueuedCookiesToResponse::class,
                StartSession::class,
                AuthenticateSession::class,
                ShareErrorsFromSession::class,
                VerifyCsrfToken::class,
                SubstituteBindings::class,
                DisableBladeIconComponents::class,
                DispatchServingFilamentEvent::class,
            ])
            ->authMiddleware([Authenticate::class]);
    }
}
```

## Multi-tenancy

```php
->tenant(Team::class, slugAttribute: 'slug')
->tenantProfile(EditTeamProfile::class)
->tenantRegistration(RegisterTeam::class)
->tenantMenuItems([
    MenuItem::make()->label('Billing')->url(fn () => route('teams.billing')),
])
```

The tenant model must implement `Filament\Models\Contracts\HasTenants` on the User model and `HasCurrentTenantLabel` on the tenant. `Resource::getEloquentQuery()` is then automatically scoped to the current tenant via the model's `tenant()` relationship.

## Authorization gate

User model implements `FilamentUser`:

```php
use Filament\Models\Contracts\FilamentUser;
use Filament\Panel;

class User extends Authenticatable implements FilamentUser
{
    public function canAccessPanel(Panel $panel): bool
    {
        return $panel->getId() === 'admin'
            ? $this->is_admin
            : true;
    }
}
```

## Plugin registration

```php
->plugins([
    \BezhanSalleh\FilamentShield\FilamentShieldPlugin::make(),
    \Awcodes\Curator\CuratorPlugin::make(),
])
```

Each plugin defines its own configuration; call its static `make()` then chain plugin-specific methods.

## Brand & theming

- `->viteTheme('resources/css/filament/admin/theme.css')` — custom Tailwind theme. Run `php artisan filament:assets` after publishing.
- `->colors([...])` accepts `Color::*` palettes or hex strings.
- `->font('Inter')` — Google Font; use `->font('Inter', provider: GoogleFontProvider::class)` to be explicit.

## Navigation

- `protected static ?string $navigationGroup = 'CRM';` on Resources/Pages.
- `protected static ?int $navigationSort = 10;` to order.
- `->navigationItems([...])` on the panel for custom links.

## Domain routing

`->domain('admin.acme.test')` to bind the panel to a subdomain. Combine with `->path('')` for root-of-subdomain.

See also: filament-resources, filament-widgets, filament-custom-components.
