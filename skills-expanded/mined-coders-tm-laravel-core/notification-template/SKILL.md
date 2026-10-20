---
name: notification-template-system
description: "Manages template-based email and push notifications with Blade rendering. Activates when creating notification classes, editing notification templates or Blade files, using shortcodes/variables, working with NotificationMail or NotificationTemplateRenderer, or seeding notification templates."
license: MIT
metadata:
    author: coderstm
---

# Notification System Instructions

## Purpose

The notification system provides template-based email and push notifications with support for:

- **Dynamic Templates**: Database-driven notification templates stored as Blade files
- **Multiple Channels**: Email, SMS, push notifications, and database notifications
- **Blade Variables**: Clean object syntax (`{{ $user->name }}`, `{{ $order->number }}`)
- **Blade Templates**: Full Blade directive support in notification templates
- **Security**: Template validation and dangerous code prevention
- **Custom Mailable**: HTML email rendering via custom `NotificationMail` class

## Architecture

### Notification Flow

```
Notification Event
    → Notification Class (construct with data)
    → Load Template from Database
    → Render Blade Variables ({{ $user->name }}, {{ $order->number }})
    → Render Blade Directives ({{ $variable }}, @if, @foreach)
    → Build HTML Email via NotificationMail
    → Send via Channel (mail, sms, push, database)
```

### Email Rendering System

The system uses a custom `Coderstm\Mail\NotificationMail` Mailable class that:

1. Renders the Blade view (`emails/notification.blade.php`)
2. Wraps content in responsive HTML email template
3. Uses `htmlString` to avoid escaping HTML
4. Works with both package and Orchestra Testbench environments

**Key Files:**

- `src/Mail/NotificationMail.php` - Custom Mailable class
- `src/Notifications/BaseNotification.php` - Base notification (returns NotificationMail)
- `resources/views/emails/notification.blade.php` - Email wrapper template
- `workbench/resources/views/emails/notification.blade.php` - Testbench copy
- `stubs/database/templates/**/*.blade.php` - Individual notification templates

## Notification Template Structure

### Database Model (`Coderstm\Models\Notification`)

```php
protected $fillable = [
    'label',      // Human-readable name: "Signup", "Invoice sent"
    'subject',    // Email subject with shortcodes/Blade
    'type',       // Unique identifier: "user:signup", "admin:new-enquiry"
    'content',    // Email body with shortcodes/Blade (HTML)
    'is_default', // Is this the default template for this type?
];
```

### Template Types

**User Notifications:**

- `user:signup` - Welcome email after registration
- `user:subscription-cancel` - Cancellation confirmation
- `user:subscription-canceled` - Subscription ended
- `user:subscription-downgrade` - Plan downgrade notice
- `user:subscription-upgraded` - Plan upgrade confirmation
- `user:subscription-renewed` - Subscription renewal confirmation
- `user:subscription-expired` - Subscription expiration notice
- `user:invoice-sent` - Invoice delivery
- `user:order-confirmation` - Order placed confirmation
- `user:order-shipped` - Shipping notification with tracking
- `user:order-delivered` - Delivery confirmation
- `user:order-canceled` - Order cancellation notice
- `user:payment-success` - Payment confirmation
- `user:payment-failed` - Payment failure alert
- `user:partial-refund` - Partial refund processed
- `user:order-refunded` - Full refund processed
- `user:abandoned-cart` - Cart recovery reminder

**Admin Notifications:**

- `admin:new-admin` - New admin user created
- `admin:new-enquiry` - New enquiry submitted
- `admin:hold` - User account held
- `admin:hold-release` - User account released
- `admin:subscription-canceled` - User subscription canceled
- `admin:subscription-expired` - User subscription expired
- `admin:new-order` - New order received
- `admin:order-canceled` - Order canceled by customer
- `admin:payment-failed` - Payment failure alert
- `admin:refund-processed` - Refund processed notification
- `admin:low-stock` - Low inventory alert
- `admin:out-of-stock` - Out of stock alert

**Enquiry Notifications:**

- `enquiry:message` - New enquiry message
- `enquiry:reply` - Enquiry reply from admin
- `enquiry:reply-user` - Enquiry reply from user

**Push Notifications:**

- `push:message` - Generic push notification

**Task Notifications:**

- `task:added` - Task assigned to user

**Import Notifications:**

- `import:completed` - Data import finished

## Shortcode Reference

### Blade Variable Format

**All templates use Blade variables for clean, readable syntax:**

| Variable                       | Value                 | Example                      |
| ------------------------------ | --------------------- | ---------------------------- |
| `{{ $user->first_name }}`      | User's first name     | John                         |
| `{{ $user->email }}`           | User's email          | john@example.com             |
| `{{ $order->number }}`         | Order number          | #ORD-12345                   |
| `{{ $order->total }}`          | Formatted order total | $99.00                       |
| `{{ $variant->product_name }}` | Product name          | Premium Widget               |
| `{{ $cart->recovery_url }}`    | Cart recovery link    | https://example.com/cart/... |
| `{{ $app->name }}`             | Application name      | MyApp                        |

### User Variables

Available via `$user->getShortCodes()`:

| Variable                    | Value                    | Example          |
| --------------------------- | ------------------------ | ---------------- |
| `{{ $user->name }}`         | Full name (first + last) | John Doe         |
| `{{ $user->first_name }}`   | User's first name        | John             |
| `{{ $user->last_name }}`    | User's last name         | Doe              |
| `{{ $user->id }}`           | User ID                  | 123              |
| `{{ $user->email }}`        | User's email             | john@example.com |
| `{{ $user->phone_number }}` | User's phone             | +1234567890      |

### Subscription Variables

Available via `$subscription->getShortCodes()`:

| Variable                             | Value            | Example      |
| ------------------------------------ | ---------------- | ------------ |
| `{{ $subscription->plan_label }}`    | Plan name        | Premium Plan |
| `{{ $subscription->plan_price }}`    | Formatted price  | $99.00       |
| `{{ $subscription->billing_cycle }}` | Billing interval | Monthly      |
| `{{ $subscription->expires_at }}`    | Expiration date  | Dec 31, 2025 |
| `{{ $subscription->billing_url }}`   | Billing page URL | /billing     |

### Order Variables

Available via `$order->getShortCodes()`:

| Variable                         | Value            | Example      |
| -------------------------------- | ---------------- | ------------ |
| `{{ $order->number }}`           | Order number     | #ORD-12345   |
| `{{ $order->total }}`            | Formatted total  | $99.00       |
| `{{ $order->status }}`           | Order status     | Completed    |
| `{{ $order->date }}`             | Order date       | Dec 15, 2025 |
| `{{ $order->tracking_number }}`  | Tracking number  | TRACK123     |
| `{{ $order->tracking_company }}` | Tracking company | FedEx        |
| `{{ $order->customer_name }}`    | Customer name    | John Doe     |

### Cart/Checkout Variables

Available via `$checkout->getShortCodes()`:

| Variable                    | Value           | Example      |
| --------------------------- | --------------- | ------------ |
| `{{ $cart->total }}`        | Cart total      | $99.00       |
| `{{ $cart->item_count }}`   | Number of items | 3            |
| `{{ $cart->recovery_url }}` | Recovery link   | /cart/abc123 |

### Product/Variant Variables

Available via `$variant->getShortCodes()`:

| Variable                       | Value              | Example        |
| ------------------------------ | ------------------ | -------------- |
| `{{ $variant->product_name }}` | Product name       | Premium Widget |
| `{{ $variant->sku }}`          | SKU                | WIDGET-001     |
| `{{ $variant->price }}`        | Price              | $49.99         |
| `{{ $variant->stock }}`        | Available quantity | 10             |

### App Variables

Available via `$app`:

| Variable            | Value            | Example  |
| ------------------- | ---------------- | -------- |
| `{{ $app->name }}`  | Application name | MyApp    |
| `{{ $app->email }}` | Support email    | support@ |

## Creating New Notifications

### Step 1: Create Notification Class

**Modern Approach (Recommended):**

```php
<?php

namespace Coderstm\Notifications\Shop;

use Coderstm\Models\Shop\Order;
use Coderstm\Models\Notification as Template;
use Coderstm\Notifications\BaseNotification;

class OrderConfirmationNotification extends BaseNotification
{
    public $order;
    public $subject;
    public $message;

    public function __construct(Order $order)
    {
        $this->order = $order;

        // Load template from database
        $template = Template::default('user:order-confirmation');

        // Render using NotificationTemplateRenderer with order data
        $rendered = $template->render([
            'order' => $order->getShortCodes(),
        ]);

        parent::__construct($rendered['subject'], $rendered['content']);
    }

    public function via($notifiable): array
    {
        return ['mail', 'database'];
    }

    public function toArray($notifiable): array
    {
        return [
            'order_id' => $this->order->id,
            'order_number' => $this->order->formated_id,
            'total' => $this->order->total(),
            'status' => $this->order->status,
        ];
    }
}
```

### Step 2: Create Template Metadata (JSON)

**Using Blade Variables:**

```json
{
    "label": "Order Confirmation",
    "subject": "Order Confirmation - Order #{{ $order->number }}",
    "is_default": true,
    "type": "user:order-confirmation"
}
```

**Note:** The content is stored in a separate `.blade.php` file (e.g., `user/order-confirmation.blade.php`), not in the JSON file.

### Step 3: Create Blade Template

Create the corresponding Blade template file in `stubs/database/templates/`:

**Example: `stubs/database/templates/user/order-confirmation.blade.php`**

```blade
<table cellpadding="0" cellspacing="0" role="presentation" width="100%"><tr><td style="font-size:14px;line-height:1.5;">
    <p style="margin:0 0 16px;font-size:14px;line-height:1.5;">Dear {{ $order->customer->first_name }},</p>
    <p style="margin:0 0 16px;font-size:14px;line-height:1.5;">Thank you for your order! We're processing it now.</p>

    <table cellpadding="0" cellspacing="0" role="presentation" width="100%" style="background:#f5f5f5;font-size:14px;margin:20px 0;">
        <tr>
            <td style="padding:12px;">
                <strong>Order #{{ $order->number }}</strong><br>
                Order Date: {{ $order->date }}<br>
                Total: {{ $order->total }}
            </td>
        </tr>
    </table>

    <p style="margin:0 0 12px;font-size:14px;font-weight:600;">Order Items:</p>
    <table cellpadding="0" cellspacing="0" role="presentation" width="100%" style="background:#ffffff;border:1px solid #e5e7eb;font-size:14px;">
        <thead>
            <tr>
                <th align="left" style="padding:12px;font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;color:#6b7280;border-bottom:1px solid #e5e7eb;">Item</th>
                <th align="center" width="60" style="padding:12px;font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;color:#6b7280;border-bottom:1px solid #e5e7eb;">Qty</th>
                <th align="right" width="80" style="padding:12px;font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;color:#6b7280;border-bottom:1px solid #e5e7eb;">Price</th>
                <th align="right" width="100" style="padding:12px;font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;color:#6b7280;border-bottom:1px solid #e5e7eb;">Total</th>
            </tr>
        </thead>
        <tbody>
            @foreach($order->items as $item)
            <tr style="border-bottom:1px solid #f3f4f6;">
                <td style="padding:12px;font-size:14px;">{{ $item['name'] }}</td>
                <td align="center" style="padding:12px;font-size:14px;">{{ $item['quantity'] }}</td>
                <td align="right" style="padding:12px;font-size:14px;">{{ $item['price'] }}</td>
                <td align="right" style="padding:12px;font-size:14px;font-weight:600;">{{ $item['total'] }}</td>
            </tr>
            @endforeach
        </tbody>
    </table>

    <table cellpadding="0" cellspacing="0" role="presentation" width="100%" style="margin:20px auto;text-align:center;" align="center">
        <tr>
            <td align="center">
                <a href="{{ $order->url }}" style="border-radius:4px;color:#ffffff;display:inline-block;text-decoration:none;padding:0 12px;font-size:14px;line-height:28px;font-weight:500;background:#3869d4;">View Order Details</a>
            </td>
        </tr>
    </table>

    <p style="margin:0 0 16px;font-size:14px;line-height:1.5;">Best regards,<br>{{ $app->name }} Team</p>
</td></tr></table>
```

### Step 4: Seed Template

Templates are automatically seeded by `NotificationSeeder` which reads JSON metadata and Blade files:

```php
// In NotificationSeeder or test setUp()
$notifications = json_decode(
    file_get_contents(__DIR__ . '/../data/notifications.json'),
    true
);

foreach ($notifications as $notification) {
    Notification::updateOrCreate(
        ['type' => $notification['type']],
        $notification
    );
}
```

### Step 4: Send Notification

```php
// In controller or service
$user->notify(new UserWelcomeNotification($user));

// Or via facade
Notification::send($users, new UserWelcomeNotification($user));
```

## Using Blade Directives in Templates

### Basic Example

```html
<table cellpadding="0" cellspacing="0" role="presentation" width="100%"><tr><td>
    Hello {{ $user->first_name }}, @if($isPremium)
    <p>Thank you for being a premium member!</p>
    <p>Your plan: {{ $plan->label }} at {{ $plan->price }}</p>
    @else
    <p><a href="{{ $upgradeUrl }}">Upgrade to Premium</a></p>
    @endif
</td></tr></table>
```

### Conditionals

```html
<!-- In template content -->
<table cellpadding="0" cellspacing="0" role="presentation" width="100%"><tr><td>
    Hello {{ $user->first_name }}, @if($isPremium)
    <p>Thank you for being a premium member!</p>
    @else
    <p><a href="{{ $upgradeUrl }}">Upgrade to Premium</a></p>
    @endif
</td></tr></table>
```

```php
// In notification class
$rendered = $notification->render([
    'user' => $user->getShortCodes(),
    'isPremium' => $user->subscription?->plan->isPremium(),
    'upgradeUrl' => url('/upgrade'),
]);
```

### Loops

```html
<p>Your subscription includes:</p>
<ul>
    @foreach($features as $feature)
    <li>{{ $feature->name }}</li>
    @endforeach
</ul>
```

```php
$rendered = $notification->render([
    'features' => $plan->features,
]);
```

### Model Property Access

```html
<table cellpadding="0" cellspacing="0" role="presentation" width="100%"><tr><td>
    Email: {{ $user->email }}<br />
    Phone: {{ $user->phone_number }}<br />
    Plan: {{ $subscription->plan->label }}
</td></tr></table>
```

```php
$rendered = $notification->render([
    'user' => $user,
    'subscription' => $subscription,
]);
```

## Security Considerations

### Dangerous Directives Blocked

The `MaskSensitiveConfig` compiler blocks dangerous functions:

- ❌ `exec()`, `shell_exec()`, `system()`
- ❌ `file_get_contents()`, `file_put_contents()`
- ❌ `eval()`, `assert()`
- ❌ `DB::raw()`, `DB::statement()`
- ❌ `config()` writes, `settings()` writes
- ❌ Inline PHP tags: `<?php ?>`

### Allowed Directives

- ✅ `@if/@else/@endif`
- ✅ `@foreach/@endforeach`
- ✅ `{{ $variable }}`
- ✅ `{{ $model->property }}`
- ✅ `@isset/@empty`
- ✅ Standard Blade helpers

### Template Validation

```php
// Validate template before saving
$validation = $notification->validate();

if (!$validation['subject']['valid']) {
    throw new \Exception($validation['subject']['error']);
}

if (!$validation['content']['valid']) {
    throw new \Exception($validation['content']['error']);
}
```

## Best Practices

### 1. Use getShortCodes() for Data

```php
// ✅ Recommended - use model's getShortCodes()
$rendered = $template->render([
    'user' => $user->getShortCodes(),
    'order' => $order->getShortCodes(),
]);
```

### 2. Use Blade Variables for Complex Logic

```php
// ✅ Good - use Blade for conditionals and loops
@if($isPremium)
    {{ $plan->label }}
@endif

@foreach($features as $feature)
    {{ $feature->name }}
@endforeach
```

### 3. Use Name Accessor

```php
// ✅ Good - uses accessor from getShortCodes()
'name' => $user->name // Accessor concatenates first + last

// ❌ Bad - manual concatenation
'name' => "{$user->first_name} {$user->last_name}"
```

### 4. Format Values in getShortCodes()

```php
// ✅ Good - pre-formatted in getShortCodes()
public function getShortCodes(): array
{
    return [
        'plan_price' => $this->plan->formatPrice(),    // "$99.00"
        'expires_at' => $this->expires_at->format('M d, Y'),
    ];
}

// ❌ Bad - raw values
public function getShortCodes(): array
{
    return [
        'plan_price' => $this->plan->price,  // 99.00
        'expires_at' => $this->expires_at,   // Carbon object
    ];
}
```

### 5. Use Optional Chaining

```php
// ✅ Good - handles null subscription
'plan_label' => optional($user->subscription)->plan->label

// ❌ Bad - will error if no subscription
'plan_label' => $user->subscription->plan->label
```

### 6. Keep Templates Simple

```php
// ✅ Good - simple Blade variable
{{ $plan->label }}

// ⚠️ Avoid - complex logic in template
{{ $subscription->plan->price > 100 ? 'Premium' : 'Basic' }}

// ✅ Better - calculate in getShortCodes()
'plan_type' => $subscription->plan->price > 100 ? 'Premium' : 'Basic'
```

### 7. Use Standardized Font Sizes

All templates use consistent font sizes for a uniform appearance:

| Context | Size | Usage |
|---------|------|-------|
| Primary text | `font-size:14px` | Body `<p>` tags, table values, buttons, item titles, section titles |
| Secondary text | `font-size:12px` | Labels, table headers `(th)`, small notes, variant text |
| Emphasized | `font-size:15px;font-weight:700` | Total amount display |

### 8. Use Standard Panel Style for Alerts

Use full-background panels instead of quote-style left borders:

```html
<table cellpadding="0" cellspacing="0" role="presentation" width="100%" style="margin:20px 0;">
    <tr>
        <td style="background:#dbeafe;color:#1e40af;padding:12px;font-size:14px;line-height:1.5;">Info content</td>
    </tr>
</table>
```

Available background/color pairs:
- Info: `background:#dbeafe; color:#1e40af`
- Success: `background:#d1fae5; color:#065f46`
- Warning: `background:#fef3c7; color:#92400e`
- Danger: `background:#fee2e2; color:#991b1b`
- Neutral: `background:#edf2f7; color:#718096`

### 9. Test All Templates

```php
public function test_notification_template_renders_correctly()
{
    $user = User::factory()->create();
    $template = Notification::default('user:signup');

    $rendered = $template->render([
        'user' => $user->getShortCodes(),
    ]);

    $this->assertStringContainsString($user->name, $rendered['subject']);
    $this->assertStringContainsString($user->first_name, $rendered['content']);
    $this->assertStringNotContainsString('{{', $rendered['content']);
}
```

## Related Files

- **Models**: `src/Models/Notification.php`
- **Renderer**: `src/Services/NotificationTemplateRenderer.php`
- **Security**: `src/Services/MaskSensitiveConfig.php`
- **Base Class**: `src/Notifications/BaseNotification.php`
- **Templates**: `stubs/database/data/notifications.json`
- **Seeder**: `stubs/database/seeders/NotificationSeeder.php`
- **Helper**: `lib/helpers.php` (`replace_short_code()`)
- **Tests**: `tests/Feature/NotificationTemplateRenderingTest.php`
