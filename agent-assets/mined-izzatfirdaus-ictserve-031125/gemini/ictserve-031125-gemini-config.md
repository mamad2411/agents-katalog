# config Directory - GEMINI Instructions

This file provides instructions for the Gemini AI related to the `config` directory of the ICTServe project.

## Directory Overview

The `config` directory contains all configuration files for the Laravel application. These files control various aspects of the application including:

* **app.php:** Core application configuration (name, environment, timezone, locale, etc.)
* **database.php:** Database connections and settings
* **mail.php:** Email configuration
* **filesystems.php:** File storage configuration
* **cache.php:** Cache store configuration
* **queue.php:** Queue driver configuration
* **auth.php:** Authentication guards and providers
* **services.php:** Third-party service credentials and settings
* **And many more...**

## Instructions

* **Environment Variables:** ALWAYS use `config()` helper instead of `env()` outside of config files. For example, use `config('app.name')` instead of `env('APP_NAME')`.
* **Configuration Caching:** In production, Laravel caches configuration files for performance. After making changes, run `php artisan config:cache` to rebuild the cache.
* **Custom Configuration:** When adding new configuration options, create appropriately named files or add to existing ones following Laravel conventions.
* **Sensitive Data:** Never hardcode sensitive information (API keys, passwords, secrets) directly in config files. Use environment variables defined in `.env`.
* **Array Syntax:** Use modern array syntax `[]` instead of `array()`.
* **Type Safety:** Be mindful of data types. Use appropriate PHP types (bool, int, string, array) for configuration values.

## Key Configuration Files

* **app.php:** Application name, environment, debug mode, URL, timezone, locale
* **database.php:** Database connections (MySQL, PostgreSQL, SQLite, etc.)
* **bedrock.php:** AWS Bedrock AI service configuration
* **filament.php:** Filament admin panel settings
* **livewire.php:** Livewire component configuration
* **horizon.php:** Laravel Horizon queue monitoring (if using Redis queues)
* **logging.php:** Log channels and levels

## Best Practices

* Read from config files using `config('file.key')` helper
* Use environment variables for deployment-specific values
* Keep configuration DRY - don't duplicate values
* Document complex configuration options with comments
* Use type-appropriate defaults when calling `config('key', 'default')`
