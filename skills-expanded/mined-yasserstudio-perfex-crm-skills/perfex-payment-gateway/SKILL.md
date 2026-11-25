---
name: perfex-payment-gateway
description: Use whenever the user is creating, modifying, or debugging a Perfex CRM payment gateway module — a class extending `App_gateway` in `modules/<module>/libraries/<Id>_gateway.php`, calling `setId`, `setName`, `setSettings`, implementing `process_payment($data)`, or registering via `register_payment_gateway`. Also trigger when the user says "create a payment gateway for Perfex", "my gateway webhook gets CSRF blocked", "process_payment not firing", "Stripe/PayPal/Mollie integration for Perfex", "payment gateway settings not saving", "encrypted setting", or "how do I handle the payment callback in Perfex". Covers the App_gateway lifecycle, settings encryption, webhook CSRF exclusion, and the Stripe API (Basil) changes in Perfex 3.3.0.
license: MIT
metadata:
  author: yasserstudio
  version: "1.5.0"
---

# Perfex Payment Gateway Development

You are a Perfex CRM payment-gateway engineer. Your job is to build gateway modules that extend `App_gateway` correctly — with encrypted secrets, proper webhook CSRF exclusion, and defensive callback handling — so payments process reliably across Stripe API updates and concurrent invoice payments.

Perfex supports custom payment gateways as modules since **v2.3.4**. A gateway is a class in `modules/<module>/libraries/<Id>_gateway.php` that extends `App_gateway` and implements `process_payment($data)`.

## File structure

```
modules/my_gateway/
├── my_gateway.php                    # module entry (hooks, register_payment_gateway)
├── install.php                       # optional: module-owned tables (transaction log, webhook log)
├── libraries/
│   └── My_gateway_gateway.php        # class My_gateway_gateway extends App_gateway
├── controllers/
│   └── My_gateway_webhook.php        # webhook receiver (CSRF-excluded)
├── views/
│   └── payment_form.php              # optional inline payment form
└── language/
    └── english/
        └── my_gateway_lang.php
```

The library filename **must** end with `_gateway.php`. Class name must match filename (capitalized first letter).

## Gateway class skeleton

```php
<?php
defined('BASEPATH') or exit('No direct script access allowed');

class My_gateway_gateway extends App_gateway
{
    public function __construct()
    {
        parent::__construct();

        $this->setId('my_gateway');

        $this->setName('My Gateway');

        $this->setSettings([
            [
                'name'      => 'api_key',
                'encrypted' => true,
                'label'     => 'API Key',
                'type'      => 'input',
            ],
            [
                'name'      => 'api_secret',
                'encrypted' => true,
                'label'     => 'API Secret',
                'type'      => 'input',
            ],
            [
                'name'      => 'test_mode',
                'label'     => 'Test Mode',
                'type'      => 'yes_no',
                'default_value' => '1',
            ],
            [
                'name'          => 'currencies',
                'label'         => 'settings_paymentmethod_currencies',
                'default_value' => 'USD,EUR',
            ],
        ]);
    }

    public function process_payment($data)
    {
        // $data is the POST from the invoice "Pay" form plus what Payments_model adds
        // (see "The $data array" below). No $data['currency'] key exists.
        $invoice  = $data['invoice'];                 // tblinvoices row (object)
        $amount   = $data['amount'];                  // float, already includes gateway_fee
        $currency = $invoice->currency_name;          // ISO code, e.g. 'USD'

        // Build the charge via your gateway's API
        $api_key = $this->decryptSetting('api_key');

        // ... gateway-specific logic ...

        // Redirect to gateway checkout page
        redirect($checkout_url);
    }
}
```

## Registration (module entry file)

```php
// my_gateway.php
register_payment_gateway('my_gateway_gateway', 'my_gateway');
```

First param: class name (lowercase). Second param: module system name. After activation, the gateway appears in **Setup → Settings → Payment Gateways**.

## Settings system

| Type | Renders as | Stored as |
|---|---|---|
| `input` | Text input | Plain or encrypted string |
| `textarea` | Multi-line input | Plain or encrypted string |
| `yes_no` | Toggle switch | `'1'` or `'0'` |
| *(no type)* | Text input | Plain string |

### Encrypted settings

Set `'encrypted' => true` on any setting holding secrets (API keys, webhook signing keys). Perfex encrypts at rest using the application encryption key. Access via `$this->decryptSetting('name')` — never read directly from DB.

```php
// ✅ Correct — decrypts automatically
$secret = $this->decryptSetting('api_secret');

// ❌ Wrong — returns encrypted gibberish
$secret = $this->getSetting('api_secret');
```

### Reading non-encrypted settings

```php
$mode = $this->getSetting('test_mode');  // '1' or '0'
$currencies = explode(',', $this->getSetting('currencies'));
```

## Webhook handling

External gateways POST payment confirmations to your callback URL. Two requirements:

### 1. CSRF exclusion

Perfex's global CSRF protection blocks external POSTs. Ship the exclusion **inside the module** — `application/hooks/InitModules.php` picks it up automatically:

```php
// modules/my_gateway/config/csrf_exclude_uris.php
defined('BASEPATH') or exit('No direct script access allowed');

return [
    'my_gateway_webhook/handle',
];
```

Entries are regexes matched `^…$` against the URI (no leading slash) — use `[0-9a-z]+`, not `(:any)`. The `csrf_exclude_uris` filter (`perfex-security`) is the same mechanism by hand; never edit `application/config/config.php` — it is overwritten on update.

Also know that core switches CSRF **off entirely** for any request whose `REQUEST_URI` contains the substring `gateways/` (`config.php`). That's how the built-in gateway callbacks work; a controller you route under `gateways/…` needs no exclusion — and any other endpoint that happens to match the substring is unprotected too.

### 2. Webhook controller

Extend `App_Controller` — that's what core's own `controllers/gateways/*.php` do. `AdminController` redirects unauthenticated requests to the login page, and neither admin nor client base classes add anything a server-to-server POST needs.

```php
<?php
defined('BASEPATH') or exit('No direct script access allowed');

class My_gateway_webhook extends App_Controller
{
    public function handle()
    {
        $payload = file_get_contents('php://input');
        $sig     = $this->input->get_request_header('X-Signature');

        // The library is loaded by register_payment_gateway() on every request
        // while the module is active; load defensively anyway.
        if (!$this->load->is_loaded('my_gateway_gateway')) {
            $this->load->library('my_gateway/my_gateway_gateway');
        }
        $gateway = $this->my_gateway_gateway;

        $secret = $gateway->decryptSetting('webhook_secret');
        if (!$sig || !hash_equals(hash_hmac('sha256', $payload, $secret), $sig)) {
            log_activity('my_gateway: webhook signature mismatch');
            $this->output->set_status_header(401);
            return;
        }

        $event = json_decode($payload, true);
        if (($event['type'] ?? '') !== 'payment.completed') {
            $this->output->set_status_header(200);   // ack events you don't handle
            return;
        }

        $invoice_id = (int) ($event['metadata']['invoice_id'] ?? 0);
        $trans_id   = $event['transaction_id'] ?? '';

        $this->load->model(['invoices_model', 'payments_model']);
        $invoice = $this->invoices_model->get($invoice_id);

        if (!$invoice) {
            log_activity('my_gateway: webhook for unknown invoice ' . $invoice_id);
        } elseif ($this->payments_model->transaction_exists($trans_id, $invoice_id)) {
            log_activity('my_gateway: duplicate webhook for transaction ' . $trans_id);   // PSP retry — already recorded
        } else {
            $gateway->addPayment([
                'invoiceid'     => $invoice_id,
                'amount'        => $event['amount'] / 100,        // minor units → major; check your PSP
                'transactionid' => $trans_id,
                'paymentmethod' => $event['method'] ?? '',        // optional, free text
            ]);
        }

        $this->output->set_status_header(200);
    }
}
```

Use **`$gateway->addPayment()`**, not `payments_model->add()` directly: it sets `paymentmode` from `getId()`, reconciles the processing-fee attempt (see below), and is what every core gateway calls. Log with `log_activity()` (DB-backed, visible in Utilities → Activity Log) — `log_message()` is a no-op in production (see `perfex-core-apis`).

## The `$data` array in `process_payment`

`Payments_model::process_payment()` takes the raw POST from the invoice "Pay" form and adds keys before calling your gateway:

| Key | Type | Description |
|---|---|---|
| `invoice` | object | Full invoice row from `tblinvoices` (`->id`, `->hash`, `->currency_name`, `->total`, `->clientid`…) |
| `invoiceid` | int | Same as `invoice->id` |
| `amount` | float | Amount to charge — partial-payment aware, **and already includes `gateway_fee`** |
| `paymentmode` | string | Your gateway ID |
| `gateway_fee` | float | Result of `getFee($amount)` — `0.0` unless you enabled processing fees |
| `payment_attempt` | object\|null | `tblpayment_attempts` row for this click (`->id`, `->reference`, `->amount`, `->fee`) — 3.x |
| *(everything else)* | mixed | Whatever the form POSTed |

There is **no `currency` key** — read `$data['invoice']->currency_name` (ISO code) or `get_currency($data['invoice']->currency)` for the full row. Redirect URLs aren't passed either: build them with `site_url('invoice/' . $invoice->id . '/' . $invoice->hash)` for the customer-facing invoice.

**Core does not re-validate the gateway on POST.** `is_payment_mode_allowed_for_invoice()` (per-invoice allowed modes) and your `currencies` setting are only consulted when the pay form is *rendered*. The form lives on the public invoice-hash URL, so a crafted or stale POST can reach `process_payment()` with a gateway/currency combination the admin excluded. Re-check both at the top of `process_payment()`:

```php
if (!is_payment_mode_allowed_for_invoice($this->getId(), $data['invoice']->id)) {   // checks allowed modes AND the currencies setting
    set_alert('danger', _l('invoice_html_payment_modes_not_selected'));
    redirect(site_url('invoice/' . $data['invoice']->id . '/' . $data['invoice']->hash));
}
```

Same for the amount: re-derive it server-side if your PSP lets the customer edit it.

### Processing fees (3.x)

`App_gateway` supports a per-gateway fee, off by default. Declare `public bool $processingFees = true;` on your class — that adds the `fee_fixed` / `fee_percent` settings and makes `getFee()` return non-zero (overriding `getFixedFee()` / `getPercentageFee()` alone does nothing). Core then records a `tblpayment_attempts` row and bumps `$data['amount']`. To reconcile, carry the attempt's reference through your PSP round-trip and hand it back:

```php
// process_payment(): stash it in the checkout session / metadata
$reference = $data['payment_attempt']->reference ?? null;

// webhook / return handler
$gateway->addPayment([
    'invoiceid'                 => $invoice_id,
    'amount'                    => $charged,               // gross, including the fee
    'transactionid'             => $trans_id,
    'payment_attempt_reference' => $reference,             // addPayment() subtracts the fee and deletes the attempt
]);
```

Note `addPayment()` reads `$data['payment_attempt_reference']` without `isset` — always pass the key (null is fine) or PHP 8 warns. If you record payments any other way, fees are double-counted or lost.

## Stripe API (Basil) changes — Perfex 3.3.0+

Perfex 3.3.0 updated to Stripe API version "Basil". If your module wraps Stripe:

- **Webhooks must be recreated** after upgrading to 3.3.0 — event payload format changed
- Stripe now respects allowed payment methods from the Stripe Dashboard (no longer hardcoded in Perfex)
- The `after_invoice_added` hook now fires **before** email sending (changed in 3.2.0) — if your gateway listens to this hook to auto-charge, the invoice email may not have been sent yet

## Existing gateway reference

Study Perfex's built-in gateways for patterns:
- `application/libraries/gateways/` — Stripe, PayPal, 2Checkout, Mollie
- `application/controllers/gateways/` — webhook receivers for built-in gateways

## Common pitfalls

- **Filename must end with `_gateway.php`** — `My_gateway.php` alone won't be detected.
- **`setId()` is lowercase `[a-z0-9_]`** — underscores are fine (core ships `paypal_checkout`, `stripe_ideal`); no hyphens, no spaces. The ID becomes the `paymentmode` stored on every payment record and the `paymentmethod_<id>_*` option keys, so never change it after release.
- **Don't store card data** — let the external gateway handle PCI compliance. Your module only stores transaction IDs.
- **`process_payment` is called on every "Pay Now" click** — it must be idempotent or create a new checkout session each time. Don't create duplicate charges.
- **Test with multiple currencies** — the `currencies` setting is a comma-separated string that Perfex checks before showing the gateway as available for an invoice.
- **Webhook retries** — most gateways retry failed webhooks. Your handler must be idempotent: check `tblinvoicepaymentrecords` for the `transactionid` before inserting (as above), and verify the invoice still exists — a deleted invoice plus a late webhook is a real sequence.
- **Stale `paymentmode` on the public invoice URL** — the pay form is reachable via the invoice hash link without login. If your gateway is deactivated while a customer has the page open, the POST arrives with a `paymentmode` core can no longer resolve. Stock 3.4 dereferences the instance and fatals; guard your own controller paths the same way core should (`if (!$gateway || empty($gateway->instance)) return false;`).

## Related skills

- **`perfex-security`** — CSRF exclusion mechanics, webhook signature verification, `app_generate_hash()` for nonces.
- **`perfex-module-dev`** — module lifecycle, `register_payment_gateway()` lives in the module entry file.
- **`perfex-database`** — if you add a `tbl<module>_transactions` table for logging.

## Upstream docs

- Perfex payment gateway guide: https://help.perfexcrm.com/module-as-payment-gateway/
- Perfex module basics: https://help.perfexcrm.com/module-basics/
- Stripe API changelog: https://stripe.com/docs/changelog

---

*Verified against Perfex CRM 3.4.0 core source on 2026-09-15 with `scripts/verify-against-core.sh`. Version-specific notes in the text are from official changelogs.*
