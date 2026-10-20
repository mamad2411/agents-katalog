---
name: woocommerce-patterns
description: WooCommerce development patterns — checkout field customization, cart/order hooks, custom product types, payment gateway skeleton, and HPOS compatibility. Use when extending WooCommerce functionality.
---

# WooCommerce Development Patterns

## Introduction

Production-ready patterns for extending WooCommerce. Every example is PHP 8.0+ compatible, HPOS-aware, and follows WordPress Coding Standards with proper escaping and sanitization. Patterns cover checkout customization, cart and order hooks, custom product types, payment gateways, template overrides, and meta handling compatible with High-Performance Order Storage.

## When to Use This Skill

- Adding or modifying checkout fields (add, validate, save, display)
- Hooking into cart calculations, fees, or discounts
- Reacting to order status transitions
- Creating custom product types
- Building a payment gateway integration
- Overriding WooCommerce templates from a plugin or theme
- Migrating order meta access to be HPOS-compatible

## Core Concepts

**HPOS (High-Performance Order Storage)**: WooCommerce 8.2+ stores orders in custom tables instead of `wp_posts`. Always use `$order->update_meta_data()` / `$order->get_meta()` instead of `update_post_meta()` / `get_post_meta()` for order data.

**WooCommerce Guard Check**: Always verify WooCommerce is active before registering hooks. A missing guard causes fatal errors when WooCommerce is deactivated.

```php
if ( ! class_exists( 'WooCommerce' ) ) {
    return;
}
```

**Hook Lifecycle for Checkout Fields**: Render the field, validate on submission, save to order meta, then display in admin and emails. Skipping any stage creates data integrity issues.

**Escape Late, Sanitize Early**: Sanitize all input when it enters the system. Escape all output at the point of rendering.

## Quick Start

Every WooCommerce extension plugin should include the WC version headers and declare HPOS compatibility:

```php
<?php
/**
 * Plugin Name: Acme WooCommerce Extension
 * Version:     1.0.0
 * Requires PHP: 8.0
 *
 * WC requires at least: 8.0
 * WC tested up to:      9.4
 */

declare(strict_types=1);

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

// Declare HPOS compatibility (required for all plugins touching order data).
add_action( 'before_woocommerce_init', function (): void {
    if ( class_exists( \Automattic\WooCommerce\Utilities\FeaturesUtil::class ) ) {
        \Automattic\WooCommerce\Utilities\FeaturesUtil::declare_compatibility(
            'custom_order_tables',
            __FILE__,
            true
        );
    }
} );
```

See Pattern 1 for a complete checkout field example built on this foundation.

---

## Pattern 1: Custom Checkout Fields (Full Lifecycle)

The complete OOP pattern covering render, validate, save, admin display, and email output.

```php
<?php
/**
 * @package Acme\AcmePlugin\WooCommerce
 */

declare(strict_types=1);

namespace Acme\AcmePlugin\WooCommerce;

class CheckoutHooks {

    public function register(): void {
        if ( ! class_exists( 'WooCommerce' ) ) {
            return;
        }

        add_action( 'woocommerce_after_order_notes', [ $this, 'add_custom_checkout_field' ] );
        add_action( 'woocommerce_checkout_process', [ $this, 'validate_custom_checkout_field' ] );
        add_action( 'woocommerce_checkout_update_order_meta', [ $this, 'save_custom_checkout_field' ] );
        add_action( 'woocommerce_admin_order_data_after_billing_address', [ $this, 'display_custom_field_in_admin' ] );
        add_action( 'woocommerce_email_after_order_table', [ $this, 'add_custom_field_to_email' ], 10, 4 );
    }

    /**
     * Render: add a custom text field after order notes.
     */
    public function add_custom_checkout_field( \WC_Checkout $checkout ): void {
        woocommerce_form_field( 'acme_purchase_order', [
            'type'        => 'text',
            'class'       => [ 'form-row-wide' ],
            'label'       => esc_html__( 'Purchase Order Number', 'acme-plugin' ),
            'placeholder' => esc_attr__( 'PO-12345', 'acme-plugin' ),
            'required'    => false,
            'clear'       => true,
        ], $checkout->get_value( 'acme_purchase_order' ) );
    }

    /**
     * Validate: check format before order creation.
     */
    public function validate_custom_checkout_field(): void {
        $po_number = isset( $_POST['acme_purchase_order'] )
            ? sanitize_text_field( wp_unslash( $_POST['acme_purchase_order'] ) )
            : '';

        if ( ! empty( $po_number ) && ! preg_match( '/^PO-\d{4,10}$/', $po_number ) ) {
            wc_add_notice(
                esc_html__( 'Purchase Order Number must follow the format PO-12345.', 'acme-plugin' ),
                'error'
            );
        }
    }

    /**
     * Save: persist to order meta (HPOS-compatible).
     */
    public function save_custom_checkout_field( int $order_id ): void {
        $po_number = isset( $_POST['acme_purchase_order'] )
            ? sanitize_text_field( wp_unslash( $_POST['acme_purchase_order'] ) )
            : '';

        if ( ! empty( $po_number ) ) {
            $order = wc_get_order( $order_id );
            if ( $order ) {
                $order->update_meta_data( '_acme_purchase_order', $po_number );
                $order->save();
            }
        }
    }

    /**
     * Admin display: show in order detail screen.
     */
    public function display_custom_field_in_admin( \WC_Order $order ): void {
        $po_number = $order->get_meta( '_acme_purchase_order' );

        if ( ! empty( $po_number ) ) {
            printf(
                '<p><strong>%s:</strong> %s</p>',
                esc_html__( 'Purchase Order', 'acme-plugin' ),
                esc_html( $po_number )
            );
        }
    }

    /**
     * Email: include in order confirmation emails.
     */
    public function add_custom_field_to_email(
        \WC_Order $order,
        bool $sent_to_admin,
        bool $plain_text,
        \WC_Email $email
    ): void {
        $po_number = $order->get_meta( '_acme_purchase_order' );

        if ( empty( $po_number ) ) {
            return;
        }

        if ( $plain_text ) {
            printf( "\n%s: %s\n", esc_html__( 'Purchase Order', 'acme-plugin' ), esc_html( $po_number ) );
        } else {
            printf( '<p><strong>%s:</strong> %s</p>', esc_html__( 'Purchase Order', 'acme-plugin' ), esc_html( $po_number ) );
        }
    }
}
```

### Modifying Built-In Checkout Fields

Use the `woocommerce_checkout_fields` filter to reorder, rename, remove, or change required status:

```php
add_filter( 'woocommerce_checkout_fields', function ( array $fields ): array {
    // Make phone optional.
    if ( isset( $fields['billing']['billing_phone'] ) ) {
        $fields['billing']['billing_phone']['required'] = false;
    }

    // Change placeholder.
    if ( isset( $fields['order']['order_comments'] ) ) {
        $fields['order']['order_comments']['placeholder'] = esc_attr__(
            'Special delivery instructions or gift message',
            'acme-plugin'
        );
    }

    // Reorder: move email before first name.
    if ( isset( $fields['billing']['billing_email'] ) ) {
        $fields['billing']['billing_email']['priority'] = 5;
    }

    // Remove a field: unset( $fields['billing']['billing_company'] );

    return $fields;
} );
```

---

## Pattern 2: Cart Fees and Order Status Hooks

Add conditional fees and react to order status transitions.

```php
<?php
declare(strict_types=1);

namespace Acme\AcmePlugin\WooCommerce;

class CartAndOrderHooks {

    public function register(): void {
        if ( ! class_exists( 'WooCommerce' ) ) {
            return;
        }

        add_action( 'woocommerce_cart_calculate_fees', [ $this, 'add_conditional_fee' ] );
        add_action( 'woocommerce_order_status_completed', [ $this, 'on_order_completed' ] );
        add_action( 'woocommerce_order_status_pending_to_processing', [ $this, 'on_new_paid_order' ] );
    }

    /**
     * Add a conditional handling fee based on shipping method.
     */
    public function add_conditional_fee( \WC_Cart $cart ): void {
        if ( is_admin() && ! defined( 'DOING_AJAX' ) ) {
            return;
        }

        $chosen_methods = WC()->session?->get( 'chosen_shipping_methods' );

        if ( is_array( $chosen_methods ) && in_array( 'flat_rate:2', $chosen_methods, true ) ) {
            $cart->add_fee(
                esc_html__( 'Rush Processing', 'acme-plugin' ),
                5.00,
                true   // Taxable.
            );
        }
    }

    /**
     * React when an order is marked completed.
     */
    public function on_order_completed( int $order_id ): void {
        $order = wc_get_order( $order_id );

        if ( ! $order ) {
            return;
        }

        // Grant access to a digital resource.
        $user_id = $order->get_customer_id();
        if ( $user_id > 0 ) {
            update_user_meta( $user_id, '_acme_has_purchased', true );
        }

        $order->add_order_note(
            esc_html__( 'Acme Plugin: Post-completion processing executed.', 'acme-plugin' )
        );
    }

    /** React to a specific status transition (pending -> processing). */
    public function on_new_paid_order( int $order_id ): void {
        $order = wc_get_order( $order_id );
        if ( $order ) {
            do_action( 'acme_fulfillment_request', $order );
        }
    }
}
```

---

## Pattern 3: Custom Product Type

Register a custom product type that appears in the product data dropdown.

```php
<?php
declare(strict_types=1);

namespace Acme\AcmePlugin\WooCommerce;

class BundleProductType {

    public function register(): void {
        if ( ! class_exists( 'WooCommerce' ) ) {
            return;
        }

        add_action( 'init', [ $this, 'register_product_type' ] );
        add_filter( 'product_type_selector', [ $this, 'add_product_type_option' ] );
        add_filter( 'woocommerce_product_data_tabs', [ $this, 'enable_product_tabs' ] );
        add_action( 'woocommerce_product_options_general_product_data', [ $this, 'show_custom_fields' ] );
        add_action( 'woocommerce_process_product_meta', [ $this, 'save_custom_fields' ] );
    }

    public function register_product_type(): void {
        if ( ! class_exists( 'WC_Product_Bundle_Type' ) ) {
            class_alias( BundleProduct::class, 'WC_Product_Bundle_Type' );
        }
    }

    public function add_product_type_option( array $types ): array {
        $types['bundle'] = esc_html__( 'Bundle', 'acme-plugin' );
        return $types;
    }

    public function enable_product_tabs( array $tabs ): array {
        if ( isset( $tabs['general'] ) ) {
            $tabs['general']['class'][] = 'show_if_bundle';
        }
        if ( isset( $tabs['inventory'] ) ) {
            $tabs['inventory']['class'][] = 'show_if_bundle';
        }
        return $tabs;
    }

    public function show_custom_fields(): void {
        echo '<div class="options_group show_if_bundle">';
        woocommerce_wp_text_input( [
            'id'          => '_bundle_discount',
            'label'       => esc_html__( 'Bundle Discount (%)', 'acme-plugin' ),
            'desc_tip'    => true,
            'description' => esc_html__( 'Percentage discount applied to the bundle total.', 'acme-plugin' ),
            'type'        => 'number',
            'custom_attributes' => [ 'step' => '0.01', 'min' => '0', 'max' => '100' ],
        ] );
        echo '</div>';
    }

    public function save_custom_fields( int $post_id ): void {
        $discount = isset( $_POST['_bundle_discount'] )
            ? sanitize_text_field( wp_unslash( $_POST['_bundle_discount'] ) )
            : '';
        update_post_meta( $post_id, '_bundle_discount', $discount );
    }
}

class BundleProduct extends \WC_Product {

    public function get_type(): string {
        return 'bundle';
    }
}
```

---

## Pattern 4: Payment Gateway Skeleton

Extend `WC_Payment_Gateway` with settings, payment processing, refunds, and webhook handling.

```php
<?php
declare(strict_types=1);

namespace Acme\AcmePlugin\WooCommerce;

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class AcmeGateway extends \WC_Payment_Gateway {

    public function __construct() {
        $this->id                 = 'acme_gateway';
        $this->icon               = '';
        $this->has_fields         = false;
        $this->method_title       = esc_html__( 'Acme Payments', 'acme-plugin' );
        $this->method_description = esc_html__( 'Accept payments via Acme.', 'acme-plugin' );
        $this->supports           = [ 'products', 'refunds' ];

        $this->init_form_fields();
        $this->init_settings();

        $this->title       = $this->get_option( 'title' );
        $this->description = $this->get_option( 'description' );
        $this->enabled     = $this->get_option( 'enabled' );

        add_action( 'woocommerce_update_options_payment_gateways_' . $this->id, [ $this, 'process_admin_options' ] );
        add_action( 'woocommerce_api_acme_gateway', [ $this, 'handle_webhook' ] );
    }

    public function init_form_fields(): void {
        $this->form_fields = [
            'enabled'     => [ 'title' => esc_html__( 'Enable/Disable', 'acme-plugin' ), 'type' => 'checkbox', 'label' => esc_html__( 'Enable Acme Payments', 'acme-plugin' ), 'default' => 'no' ],
            'title'       => [ 'title' => esc_html__( 'Title', 'acme-plugin' ), 'type' => 'text', 'default' => esc_html__( 'Acme Payments', 'acme-plugin' ) ],
            'description' => [ 'title' => esc_html__( 'Description', 'acme-plugin' ), 'type' => 'textarea', 'default' => esc_html__( 'Pay securely via Acme.', 'acme-plugin' ) ],
            'api_key'     => [ 'title' => esc_html__( 'API Key', 'acme-plugin' ), 'type' => 'password' ],
            'sandbox'     => [ 'title' => esc_html__( 'Sandbox Mode', 'acme-plugin' ), 'type' => 'checkbox', 'label' => esc_html__( 'Enable sandbox/test mode', 'acme-plugin' ), 'default' => 'yes' ],
        ];
    }

    /**
     * @return array{result: string, redirect?: string}
     */
    public function process_payment( $order_id ): array {
        $order = wc_get_order( $order_id );

        if ( ! $order ) {
            wc_add_notice( esc_html__( 'Order not found.', 'acme-plugin' ), 'error' );
            return [ 'result' => 'failure' ];
        }

        $endpoint = 'yes' === $this->get_option( 'sandbox' )
            ? 'https://sandbox.acme-pay.example/v1/charge'
            : 'https://api.acme-pay.example/v1/charge';

        $response = wp_remote_post( $endpoint, [
            'headers' => [
                'Authorization' => 'Bearer ' . $this->get_option( 'api_key' ),
                'Content-Type'  => 'application/json',
            ],
            'body'    => wp_json_encode( [
                'amount'    => (int) round( (float) $order->get_total() * 100 ),
                'currency'  => $order->get_currency(),
                'reference' => $order->get_order_key(),
            ] ),
            'timeout' => 30,
        ] );

        if ( is_wp_error( $response ) ) {
            wc_add_notice( esc_html__( 'Payment failed. Please try again.', 'acme-plugin' ), 'error' );
            $order->add_order_note( sprintf( 'Acme API error: %s', $response->get_error_message() ) );
            return [ 'result' => 'failure' ];
        }

        $body = json_decode( wp_remote_retrieve_body( $response ), true );

        if ( ! is_array( $body ) || 'success' !== ( $body['status'] ?? '' ) ) {
            wc_add_notice( esc_html__( 'Payment was declined.', 'acme-plugin' ), 'error' );
            return [ 'result' => 'failure' ];
        }

        // HPOS-compatible meta storage.
        $order->set_transaction_id( sanitize_text_field( $body['transaction_id'] ?? '' ) );
        $order->update_meta_data( '_acme_charge_id', sanitize_text_field( $body['charge_id'] ?? '' ) );
        $order->payment_complete( sanitize_text_field( $body['transaction_id'] ?? '' ) );
        $order->save();

        WC()->cart->empty_cart();

        return [
            'result'   => 'success',
            'redirect' => $this->get_return_url( $order ),
        ];
    }

    /** @return bool|\WP_Error */
    public function process_refund( $order_id, $amount = null, $reason = '' ): bool|\WP_Error {
        $order     = wc_get_order( $order_id );
        $charge_id = $order ? $order->get_meta( '_acme_charge_id' ) : '';

        if ( ! $order || empty( $charge_id ) ) {
            return new \WP_Error( 'acme_refund_error', esc_html__( 'No charge ID found.', 'acme-plugin' ) );
        }

        // Call refund endpoint (same sandbox/live pattern as process_payment).
        $endpoint = 'yes' === $this->get_option( 'sandbox' )
            ? 'https://sandbox.acme-pay.example/v1/refund'
            : 'https://api.acme-pay.example/v1/refund';

        $response = wp_remote_post( $endpoint, [
            'headers' => [ 'Authorization' => 'Bearer ' . $this->get_option( 'api_key' ), 'Content-Type' => 'application/json' ],
            'body'    => wp_json_encode( [ 'charge_id' => $charge_id, 'amount' => (int) round( (float) $amount * 100 ), 'reason' => sanitize_text_field( $reason ) ] ),
            'timeout' => 30,
        ] );

        if ( is_wp_error( $response ) ) {
            return $response;
        }

        $body = json_decode( wp_remote_retrieve_body( $response ), true );
        if ( is_array( $body ) && 'refunded' === ( $body['status'] ?? '' ) ) {
            $order->add_order_note( sprintf( esc_html__( 'Refunded %1$s via Acme (ID: %2$s)', 'acme-plugin' ), wc_price( (float) $amount ), sanitize_text_field( $body['refund_id'] ?? 'N/A' ) ) );
            return true;
        }

        return new \WP_Error( 'acme_refund_error', esc_html__( 'Refund failed.', 'acme-plugin' ) );
    }

    /** Handle incoming webhook/IPN. Verify signature, then process event. */
    public function handle_webhook(): void {
        $payload   = file_get_contents( 'php://input' );
        $data      = json_decode( $payload ?: '', true );
        $signature = sanitize_text_field( $_SERVER['HTTP_X_ACME_SIGNATURE'] ?? '' );

        if ( ! is_array( $data ) || ! hash_equals( hash_hmac( 'sha256', $payload ?: '', $this->get_option( 'api_key' ) ), $signature ) ) {
            status_header( 403 );
            exit;
        }

        $order_id = wc_get_order_id_by_order_key( sanitize_text_field( $data['reference'] ?? '' ) );
        $order    = wc_get_order( $order_id );

        if ( $order && 'charge.completed' === ( $data['event'] ?? '' ) ) {
            $order->payment_complete( sanitize_text_field( $data['transaction_id'] ?? '' ) );
        }

        status_header( 200 );
        exit;
    }
}
```

**Register the gateway:**

```php
add_filter( 'woocommerce_payment_gateways', function ( array $gateways ): array {
    $gateways[] = \Acme\AcmePlugin\WooCommerce\AcmeGateway::class;
    return $gateways;
} );
```

---

## Pattern 5: HPOS-Compatible Meta Handling

### HPOS-Compatible vs Legacy Meta Access

```php
// --- WRONG (legacy, breaks under HPOS) ---
// update_post_meta( $order_id, '_acme_tracking', $tracking_number );
// $tracking = get_post_meta( $order_id, '_acme_tracking', true );

// --- CORRECT (works with both storage backends) ---
$order = wc_get_order( $order_id );

if ( $order ) {
    // Write.
    $order->update_meta_data( '_acme_tracking', sanitize_text_field( $tracking_number ) );
    $order->save(); // Always call save() after updating meta.

    // Read.
    $tracking = $order->get_meta( '_acme_tracking' );

    // Delete.
    $order->delete_meta_data( '_acme_tracking' );
    $order->save();
}
```

### Querying Orders (HPOS-Compatible)

```php
// --- WRONG (legacy WP_Query against wp_posts) ---
// $orders = new \WP_Query( [ 'post_type' => 'shop_order', 'meta_key' => '_acme_tracking' ] );

// --- CORRECT (uses wc_get_orders which works with HPOS) ---
$orders = wc_get_orders( [
    'meta_key'   => '_acme_tracking',
    'meta_value' => $tracking_number,
    'limit'      => 10,
    'status'     => 'completed',
    'orderby'    => 'date',
    'order'      => 'DESC',
] );

foreach ( $orders as $order ) {
    $order_number = $order->get_order_number();
}
```

---

## Pattern 6: WooCommerce Template Overrides

### Theme Override

WooCommerce looks for overrides in `yourtheme/woocommerce/`. Copy the original from `woocommerce/templates/` and modify:

```text
yourtheme/
  woocommerce/
    single-product/price.php
    checkout/form-billing.php
    emails/email-header.php
```

### Plugin Override

Filter the template path to point to your plugin's template directory:

```php
add_filter( 'woocommerce_locate_template', function (
    string $template,
    string $template_name,
    string $template_path
): string {
    $overrides = [ 'single-product/price.php', 'cart/cart-totals.php' ];

    if ( ! in_array( $template_name, $overrides, true ) ) {
        return $template;
    }

    $plugin_template = ACME_PLUGIN_DIR . 'templates/woocommerce/' . $template_name;

    return file_exists( $plugin_template ) ? $plugin_template : $template;
}, 10, 3 );
```

### Custom Plugin Templates (Theme-Overridable)

```php
/**
 * Render a custom template that themes can override.
 *
 * Theme path:  yourtheme/acme-plugin/order-tracking.php
 * Plugin path: acme-plugin/templates/order-tracking.php
 */
function acme_render_tracking_template( \WC_Order $order ): void {
    wc_get_template(
        'order-tracking.php',
        [
            'order'    => $order,
            'tracking' => $order->get_meta( '_acme_tracking' ),
        ],
        'acme-plugin/',
        ACME_PLUGIN_DIR . 'templates/'
    );
}
```

Template resolution order: theme `woocommerce/` directory, then plugin filter via `woocommerce_locate_template`, then WooCommerce defaults. Never edit core templates directly.

---

## Common Pitfalls and Best Practices

**WooCommerce Guard**: Check `class_exists( 'WooCommerce' )` in every class that uses WC functions. Fatal errors occur when WooCommerce is deactivated without this guard.

**HPOS Migration**:

- Use `$order->update_meta_data()` / `$order->get_meta()` instead of `update_post_meta()` / `get_post_meta()` for order data.
- Use `wc_get_orders()` instead of `WP_Query` with `post_type => 'shop_order'`.
- Always call `$order->save()` after `update_meta_data()` or `delete_meta_data()`.
- Declare HPOS compatibility in the main plugin file (see Quick Start).

**Checkout Field Validation**:

- Validate in `woocommerce_checkout_process` before save, not after.
- Use `wc_add_notice( $message, 'error' )` to surface validation errors.
- Always `sanitize_text_field( wp_unslash( $_POST['field'] ) )` before processing.

**Cart Fee Timing**:

- `woocommerce_cart_calculate_fees` can fire multiple times per page load.
- Guard with `if ( is_admin() && ! defined( 'DOING_AJAX' ) ) { return; }`.
- Use `$cart->add_fee()` rather than modifying totals directly.

**Payment Gateway Requirements**:

- `process_payment()` must return `['result' => 'success', 'redirect' => $url]`.
- Call `$order->payment_complete( $transaction_id )` on success.
- Call `WC()->cart->empty_cart()` after successful payment.
- Never store raw API keys in order meta -- use `$this->get_option()`.
- Add `'refunds'` to `$this->supports` and implement `process_refund()`.

---

## Hook Quick Reference

| Hook                                                 | Type   | Purpose                                    |
| ---------------------------------------------------- | ------ | ------------------------------------------ |
| `woocommerce_after_order_notes`                      | Action | Add custom checkout fields                 |
| `woocommerce_checkout_process`                       | Action | Validate fields before order creation      |
| `woocommerce_checkout_update_order_meta`             | Action | Save custom field data to order meta       |
| `woocommerce_checkout_fields`                        | Filter | Modify, reorder, or remove checkout fields |
| `woocommerce_order_status_completed`                 | Action | Order marked completed                     |
| `woocommerce_order_status_{from}_to_{to}`            | Action | Specific status transition                 |
| `woocommerce_payment_complete`                       | Action | Payment processed successfully             |
| `woocommerce_admin_order_data_after_billing_address` | Action | Admin order screen, after billing          |
| `woocommerce_email_after_order_table`                | Action | Order emails, after items table            |
| `woocommerce_cart_calculate_fees`                    | Action | Add fees or discounts to cart              |
| `woocommerce_before_calculate_totals`                | Action | Modify prices before totals                |
| `woocommerce_product_options_general_product_data`   | Action | General tab in product editor              |
| `woocommerce_process_product_meta`                   | Action | Save custom product fields                 |
| `product_type_selector`                              | Filter | Add custom product type to dropdown        |
| `woocommerce_payment_gateways`                       | Filter | Register a payment gateway class           |
| `woocommerce_update_options_payment_gateways_{id}`   | Action | Save gateway admin settings                |
| `woocommerce_api_{slug}`                             | Action | Handle incoming webhook/IPN                |
