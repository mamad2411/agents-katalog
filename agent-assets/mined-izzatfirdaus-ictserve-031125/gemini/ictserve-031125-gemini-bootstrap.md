# bootstrap Directory - GEMINI Instructions

This file provides instructions for the Gemini AI related to the `bootstrap` directory of the ICTServe project.

## Directory Overview

The `bootstrap` directory contains files that bootstrap the Laravel application. This includes:

* **app.php:** The main application bootstrap file where middleware, routing, and exceptions are configured.
* **providers.php:** Contains application-specific service providers that are manually registered.
* **cache/:** Contains framework-generated cache files for optimization.

## Instructions

* **app.php:** This is the heart of Laravel 12's new streamlined structure. When configuring middleware, routing, or exception handling, make changes here instead of the old `app/Http/Kernel.php` (which no longer exists in Laravel 12).
* **Middleware:** Register web and API middleware in the `withMiddleware()` callback in `app.php`.
* **Routing:** Configure route files in the `withRouting()` callback. The default routes are `web.php`, `api.php`, `console.php`, and `channels.php`.
* **Exceptions:** Register custom exception handlers in the `withExceptions()` callback.
* **Service Providers:** Add custom service providers to `providers.php` if they need to be registered manually. Most providers are auto-discovered.
* **Cache Files:** Do not manually edit files in the `cache/` directory. These are generated automatically by Laravel.

## Laravel 12 Structure

Laravel 12 introduced a streamlined application structure:

* No `app/Http/Kernel.php` - use `bootstrap/app.php` instead
* No `app/Console/Kernel.php` - use `bootstrap/app.php` or `routes/console.php`
* Commands in `app/Console/Commands/` are automatically registered
* Service providers in `app/Providers/` are auto-discovered unless manually added to `bootstrap/providers.php`
