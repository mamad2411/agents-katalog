---
name: simple-history-logging-api
description: A developer guide on using the Simple History Logging API to record custom events from your own plugins or themes.
---

# Simple History Logging API

Simple History includes a robust Logging API that allows developers to easily record custom events occurring within their themes or plugins. This ensures that site admins have a complete audit trail of custom application behavior alongside standard WordPress events.

## 1. Basic Logging
The simplest way to log an event is to use the `SimpleLogger()` function.
You can log events at different severity levels (info, warning, error, etc.).

```php
// Log a basic informational message
SimpleLogger()->info("Custom plugin settings were updated.");

// Log a warning
SimpleLogger()->warning("Payment gateway API connection timed out.");
```

## 2. Contextual Logging
It's highly recommended to provide context with your log entries. Context allows you to store structured data that can be used later for filtering or displaying detailed information in the event row.

```php
SimpleLogger()->info(
    "User {user_email} downloaded the premium whitepaper '{document_title}'",
    array(
        "user_email" => $current_user->user_email,
        "document_title" => $post->post_title,
        "document_id" => $post->ID,
        "_initiator" => SimpleLoggerLogInitiators::WEB_USER
    )
);
```
*Note: Any variables in the message string wrapped in `{}` will be automatically replaced by the matching key in the context array.*

## 3. Creating a Custom Logger
For larger plugins, you should create a dedicated Logger class extending `SimpleLogger`.
This allows you to group events, define custom labels, and create specialized HTML output for the event details panel.

```php
class MyCustomPlugin_Logger extends SimpleLogger {
    public $slug = 'MyCustomPlugin_Logger';

    public function getInfo() {
        return array(
            'name' => 'My Custom Plugin',
            'description' => 'Logs actions from My Custom Plugin',
            'capability' => 'manage_options',
            'messages' => array(
                'settings_updated' => 'Settings updated for My Custom Plugin',
            )
        );
    }
}
```
Register the logger on the `simple_history/add_custom_logger` hook.

## 4. Best Practices
- Always use the `_initiator` context key to specify who or what triggered the event (e.g., `WEB_USER`, `WP_CLI`, `WP_CRON`).
- Avoid logging highly sensitive information like plain text passwords or credit card numbers.
