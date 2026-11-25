---
name: nativephp-desktop
description: Build native desktop applications with NativePHP for Desktop v2 (nativephp/desktop) on Laravel. Covers installation, windows, menus, notifications, dialogs, system APIs, SQLite databases, queues, child processes, broadcasting, building, publishing, and security. Use when building NativePHP desktop apps, Electron+Laravel apps, Native\Desktop facades, or php artisan native:run/native:build.
---

# NativePHP for Desktop v2

NativePHP lets you build **native desktop apps** with **Laravel + PHP + HTML/CSS/JS**. It bundles PHP (via Static PHP CLI) with an **Electron** shell. UI is your choice: Livewire, Inertia, React, Vue, or plain Blade.

**Package:** `nativephp/desktop` ^2.0 | **Namespace:** `Native\Desktop\` | **Requires:** PHP 8.3+, Laravel 11+, Node 22+

## Quick Start

```bash
composer require nativephp/desktop
php artisan native:install
php artisan native:run          # dev build
composer native:dev             # native:run + npm run dev concurrently
```

Test in browser first, then run natively. Code changes require **restarting** `native:run` (app is copied into Electron build env).

## Architecture

1. Electron shell starts
2. `php artisan migrate` runs (production/user DB)
3. `php artisan serve` starts PHP server
4. `NativeAppServiceProvider::boot()` runs (open windows, menus, hotkeys)
5. `ApplicationBooted` event fires

Configure app bootstrap in `app/Providers/NativeAppServiceProvider.php` (published by installer).

## NativeAppServiceProvider

```php
namespace App\Providers;

use Native\Desktop\Facades\Window;
use Native\Desktop\Facades\Menu;
use Native\Desktop\Contracts\ProvidesPhpIni;

class NativeAppServiceProvider implements ProvidesPhpIni
{
    public function boot(): void
    {
        Menu::default();
        Window::open()
            ->width(1200)
            ->height(800)
            ->rememberState();
    }

    public function phpIni(): array
    {
        return ['memory_limit' => '512M', 'max_execution_time' => '0'];
    }
}
```

## Core Facades

| Facade | Purpose | Reference |
|---|---|---|
| `Window` | Open/close/resize native windows | [windows.md](references/the-basics/windows.md) |
| `Menu` | Application & context menus | [application-menu.md](references/the-basics/application-menu.md) |
| `MenuBar` | macOS menu bar / system tray apps | [menu-bar.md](references/the-basics/menu-bar.md) |
| `Notification` | OS system notifications | [notifications.md](references/the-basics/notifications.md) |
| `Dialog` | File open/save dialogs | [dialogs.md](references/the-basics/dialogs.md) |
| `Alert` | Native alert/confirm dialogs | [alerts.md](references/the-basics/alerts.md) |
| `App` | Quit, relaunch, focus, badge, locale | [application.md](references/the-basics/application.md) |
| `System` | Encrypt/decrypt, TouchID, print, theme | [system.md](references/the-basics/system.md) |
| `Clipboard` | Read/write clipboard | [clipboard.md](references/the-basics/clipboard.md) |
| `GlobalShortcut` | System-wide hotkeys | [global-hotkeys.md](references/the-basics/global-hotkeys.md) |
| `ChildProcess` | Managed background processes | [child-processes.md](references/digging-deeper/child-processes.md) |
| `QueueWorker` | Start/stop queue workers | [queues.md](references/digging-deeper/queues.md) |

Full list: [facades-and-commands.md](references/facades-and-commands.md)

## Windows (most used API)

```php
use Native\Desktop\Facades\Window;

// Open (default id: 'main')
Window::open('settings')
    ->route('settings')
    ->title('Settings')
    ->width(600)->height(400)
    ->minWidth(400)->minHeight(300)
    ->rememberState()
    ->resizable(true);

// Control
Window::close('settings');
Window::resize(800, 600, 'main');
Window::minimize('main');
Window::maximize('main');
Window::get('settings')->url(route('home'));
Window::get('settings')->title('New Title');
Window::current();  // focused window info
Window::all();

// Advanced
Window::open()->alwaysOnTop();
Window::open()->titleBarHidden();          // custom title bar: -webkit-app-region: drag
Window::open()->preventLeaveDomain();      // lock to domain
Window::open()->preventLeavePage();        // lock to single page
Window::open()->suppressNewWindows();      // block target=_blank
Window::open()->skipTaskbar();
Window::open()->backgroundColor('#00000050');
```

## Notifications

```php
use Native\Desktop\Facades\Notification;

Notification::title('Export complete')
    ->message('Your file is ready')
    ->event(\App\Events\ExportClicked::class)
    ->reference($exportId)
    ->show();
```

## Dialogs & Alerts

```php
use Native\Desktop\Dialog;
use Native\Desktop\Facades\Alert;

$path = Dialog::new()
    ->title('Select file')
    ->filter('Images', ['jpg', 'png'])
    ->multiple()
    ->open();

$index = Alert::new()
    ->title('Confirm')
    ->buttons(['Yes', 'No'])
    ->type('question')
    ->show('Delete this item?');
// $index: 0 = Yes, 1 = No
```

## Global Hotkeys

```php
use Native\Desktop\Facades\GlobalShortcut;

GlobalShortcut::key('CmdOrCtrl+Shift+A')
    ->event(\App\Events\ToggleApp::class)
    ->register();

GlobalShortcut::key('CmdOrCtrl+Shift+A')->unregister();
```

## Menu Bar Apps

```php
use Native\Desktop\Facades\MenuBar;

MenuBar::create()
    ->route('dashboard')
    ->icon(storage_path('app/iconTemplate.png'))  // 22x22, Template suffix for macOS
    ->label('Online')
    ->width(400)->height(500)
    ->showDockIcon();  // for apps that also use windows
```

## Broadcasting (PHP ↔ JS)

Native events broadcast on `nativephp` channel. In JavaScript:

```javascript
window.addEventListener('native:init', () => {
    Native.on('Native\\Desktop\\Events\\Windows\\WindowBlurred', (payload) => {});
});
```

In Livewire:

```php
#[On('native:'.WindowFocused::class)]
public function windowFocused() { $this->focused = true; }
```

See [broadcasting.md](references/digging-deeper/broadcasting.md).

## Databases (SQLite only)

- **Dev:** `nativephp.sqlite` in build directory — migrate manually: `php artisan native:migrate`
- **Production:** `{appdata}/database/database.sqlite` — auto-migrated on version change
- Bump `version` in `config/nativephp.php` every release to trigger migrations

```bash
php artisan native:migrate
php artisan native:migrate:fresh   # destructive
php artisan native:seed
```

## Files & Storage

`storage_path()` rewrites to Electron `appData`. Use Laravel `Storage` facade:

```php
Storage::disk('desktop')->put('report.pdf', $data);
Storage::disk('documents')->get('notes.txt');
Storage::disk('user_home')->path('');
```

See [files.md](references/digging-deeper/files.md).

## Queues & Background Work

Default: one queue worker on `default` queue. Configure in `config/nativephp.php`:

```php
'queue_workers' => [
    'default' => [],
    'heavy' => ['queues' => ['exports'], 'memory_limit' => 1024, 'timeout' => 600],
],
```

For long-running CLI processes, use `ChildProcess` instead. See [queues.md](references/digging-deeper/queues.md).

## Building & Publishing

```bash
# Bump version in config/nativephp.php first!
php artisan native:build          # current platform
php artisan native:build win      # cross-compile
php artisan native:publish        # build + upload to updater
```

Pre/post build hooks in `config/nativephp.php`:

```php
'prebuild' => ['npm run build', 'php artisan optimize'],
'postbuild' => [],
```

Build output: `nativephp/electron/dist`. See [building.md](references/publishing/building.md).

### Code signing env vars

```dotenv
# macOS
NATIVEPHP_APPLE_ID=
NATIVEPHP_APPLE_ID_PASS=
NATIVEPHP_APPLE_TEAM_ID=

# Windows (Azure Trusted Signing)
AZURE_TENANT_ID=
AZURE_CLIENT_ID=
AZURE_CLIENT_SECRET=
NATIVEPHP_AZURE_PUBLISHER_NAME=
```

Stripped from `.env` at build time via `cleanup_env_keys`.

## Configuration

Key `config/nativephp.php` values:

```php
'version' => env('NATIVEPHP_APP_VERSION', '1.0.0'),
'app_id' => env('NATIVEPHP_APP_ID', 'com.myapp.desktop'),
'provider' => \App\Providers\NativeAppServiceProvider::class,
'cleanup_env_keys' => ['AWS_*', '*_SECRET', ...],
```

See [configuration.md](references/getting-started/configuration.md).

## Security Essentials

- `.env` is bundled — never ship secrets; use `cleanup_env_keys`
- Encrypt user secrets: `System::encrypt()` / `System::decrypt()`
- `PreventRegularBrowserAccess` middleware applied in production builds
- Do NOT bypass the PHP ↔ Electron auth bridge
- Only read/write in `appdata` and user home directories

See [security.md](references/digging-deeper/security.md).

## Development Tips

| Topic | Detail |
|---|---|
| Hot reload | Run `npm run dev` alongside `native:run` for Vite HMR |
| Code changes | Restart `native:run` — code is copied to Electron env |
| App icons | `public/icon.png` (512x512), `icon.ico`, `icon.icns`, `IconTemplate.png` |
| Debugging | Dev tools available in debug builds — see [debugging.md](references/getting-started/debugging.md) |
| v1 → v2 | `nativephp/electron` → `nativephp/desktop`, `Native\Laravel` → `Native\Desktop`, `native:serve` → `native:run` |

## Documentation Index

### Getting Started
- [introduction.md](references/getting-started/introduction.md) — What NativePHP is/isn't
- [installation.md](references/getting-started/installation.md) — Requirements & install
- [configuration.md](references/getting-started/configuration.md) — `nativephp.php` config
- [development.md](references/getting-started/development.md) — Dev workflow, hot reload
- [env-files.md](references/getting-started/env-files.md) — `.env` security at build
- [debugging.md](references/getting-started/debugging.md) — Debug builds & DevTools
- [upgrade-guide.md](references/getting-started/upgrade-guide.md) — v1 → v2 migration

### The Basics
- [app-lifecycle.md](references/the-basics/app-lifecycle.md) — Boot sequence
- [windows.md](references/the-basics/windows.md) — Window management (full API)
- [menu-bar.md](references/the-basics/menu-bar.md) — Menu bar / tray apps
- [application-menu.md](references/the-basics/application-menu.md) — App menus
- [notifications.md](references/the-basics/notifications.md) — System notifications
- [dialogs.md](references/the-basics/dialogs.md) — File dialogs
- [alerts.md](references/the-basics/alerts.md) — Alert dialogs
- [global-hotkeys.md](references/the-basics/global-hotkeys.md) — Global shortcuts
- [application.md](references/the-basics/application.md) — App-level control
- [system.md](references/the-basics/system.md) — Encryption, printing, theme
- [clipboard.md](references/the-basics/clipboard.md) — Clipboard access
- [settings.md](references/the-basics/settings.md) — Persistent settings
- [screens.md](references/the-basics/screens.md) — Display info
- [shell.md](references/the-basics/shell.md) — Open URLs/files
- [power-monitor.md](references/the-basics/power-monitor.md) — Power events

### Digging Deeper
- [broadcasting.md](references/digging-deeper/broadcasting.md) — PHP ↔ JS events
- [databases.md](references/digging-deeper/databases.md) — SQLite setup
- [files.md](references/digging-deeper/files.md) — Filesystem & storage disks
- [queues.md](references/digging-deeper/queues.md) — Background jobs
- [child-processes.md](references/digging-deeper/child-processes.md) — Managed processes
- [security.md](references/digging-deeper/security.md) — Security guide
- [php-binaries.md](references/digging-deeper/php-binaries.md) — PHP runtime

### Publishing
- [building.md](references/publishing/building.md) — Production builds
- [publishing.md](references/publishing/publishing.md) — Publish & distribute
- [updating.md](references/publishing/updating.md) — Auto-updater config

### Testing
- [basics.md](references/testing/basics.md) — Testing overview
- [windows.md](references/testing/windows.md) — Window fakes

### Quick Reference
- [facades-and-commands.md](references/facades-and-commands.md) — All facades, commands, config keys

## Common Gotchas

- **Changes not showing** — restart `native:run`; dev builds copy code into Electron env
- **Migrations not running in dev** — use `php artisan native:migrate`, not `migrate`
- **Interactive JS dead after Livewire** — not applicable here, but re-init if using Flowbite etc.
- **App won't open on other Macs** — notarization required; set Apple env vars
- **Secrets in production** — `.env` ships with the app; use `cleanup_env_keys`
- **nodeIntegration** — disabled by default in v2; use `Window::webPreferences(['nodeIntegration' => true])` if needed
- **Cross-compile** — `native:build win` from Mac may not work on all platforms
