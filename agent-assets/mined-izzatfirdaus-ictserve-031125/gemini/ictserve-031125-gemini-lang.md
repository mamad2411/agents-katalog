# lang Directory - GEMINI Instructions

This file provides instructions for the Gemini AI related to the `lang` directory of the ICTServe project.

## Directory Overview

The `lang` directory contains all localization/translation files for the Laravel application. This enables the application to support multiple languages.

## Supported Languages

* **ms (Bahasa Melayu):** Primary language - Malay
* **en (English):** Secondary language - English

## Directory Structure

```
lang/
├── ms/
│   ├── auth.php
│   ├── validation.php
│   ├── passwords.php
│   ├── pagination.php
│   ├── messages.php (custom)
│   └── ...
├── en/
│   ├── auth.php
│   ├── validation.php
│   ├── passwords.php
│   ├── pagination.php
│   ├── messages.php (custom)
│   └── ...
├── ms.json (optional - for simple key-value translations)
└── en.json (optional - for simple key-value translations)
```

## Instructions

* **Consistency:** When adding new translation keys, add them to ALL language files (ms and en) to maintain consistency.
* **Key Naming:** Use descriptive, hierarchical keys. For example: `tickets.created_success`, `validation.required`.
* **Translation Syntax:** Use the `__()` helper function in PHP and Blade templates: `{{ __('messages.welcome') }}`
* **Parameters:** Support dynamic values using placeholders: `__('messages.greeting', ['name' => $user->name])`
* **JSON Files:** Use JSON files for simple one-to-one translations (like button labels). Use PHP files for more complex translations with parameters.
* **Locale Switching:** The application locale should be set via middleware (SetLocale middleware).

## Usage Examples

### In PHP/Controllers

```php
// Simple translation
$message = __('messages.welcome');

// With parameters
$message = __('messages.greeting', ['name' => $user->name]);

// Pluralization
$message = trans_choice('messages.apples', $count);
```

### In Blade Templates

```blade
<!-- Simple translation -->
<h1>{{ __('messages.welcome') }}</h1>

<!-- With parameters -->
<p>{{ __('messages.greeting', ['name' => $user->name]) }}</p>

<!-- Alternative syntax -->
<p>@lang('messages.welcome')</p>

<!-- JSON translations (simpler) -->
<button>{{ __('Save') }}</button>
```

### In JavaScript (if needed)
Translation strings can be made available to JavaScript using Laravel's built-in features or packages like `laravel-lang/lang`.

## Translation File Structure

### PHP Array Files

```php
<?php

return [
    'welcome' => 'Welcome to our application',
    'greeting' => 'Hello, :name!',
    'apples' => '{0} There are none|{1} There is one|[2,*] There are many',
];
```

### JSON Files

```json
{
    "Save": "Simpan",
    "Cancel": "Batal",
    "Delete": "Padam"
}
```

## Best Practices

* Keep translation keys organized and grouped by feature/module
* Use descriptive keys rather than English text as keys
* Maintain alphabetical order within translation files for easier maintenance
* Add comments for context when translations might be ambiguous
* Test the application in all supported languages
* Use professional translators for important user-facing text
* Consider cultural differences, not just direct translations
* Keep line length reasonable for UI translations (shorter text for buttons, labels)

## Filament Localization

Filament provides its own translation files. To customize Filament translations:

1. Publish Filament translations: `php artisan vendor:publish --tag=filament-translations`
2. Modify the published files in `lang/vendor/filament/`
3. Ensure Filament respects the application locale via middleware

## Validation Messages

Laravel's validation messages are in `validation.php`. Custom validation messages can be added there or in FormRequest classes:

```php
public function messages(): array
{
    return [
        'email.required' => __('validation.custom.email.required'),
        'name.min' => __('validation.custom.name.min'),
    ];
}
```

## Date and Number Formatting

Use Carbon for date localization and PHP's NumberFormatter for numbers:

```php
// Dates
Carbon::setLocale(app()->getLocale());
echo $date->translatedFormat('d F Y'); // "15 Januari 2025"

// Currency
$fmt = new NumberFormatter(app()->getLocale(), NumberFormatter::CURRENCY);
echo $fmt->formatCurrency($amount, 'MYR');
```
