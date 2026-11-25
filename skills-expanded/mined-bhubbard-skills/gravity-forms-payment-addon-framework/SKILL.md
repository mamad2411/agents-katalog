---
name: gravity-forms-payment-addon-framework
description: "Creating payment gateways extending GFPaymentAddOn."
---

# Gravity Forms Payment Add-On Framework

The `GFPaymentAddOn` class extends `GFFeedAddOn` and handles the complexities of payment integrations. It automatically handles calculating totals, creating transactions, fulfilling orders, and updating entry payment statuses.

## Reference
[GFPaymentAddOn Documentation](https://docs.gravityforms.com/gfpaymentaddon/)

## Core Concepts

### Authorization and Capture
The payment add-on framework standardizes the payment process into authorization and capture steps.

### Entry Payment Statuses
The framework manages standard statuses: `Processing`, `Authorized`, `Paid`, `Failed`, `Refunded`, and `Voided`.

### Mandatory Overrides
To create a payment add-on, you must extend `GFPaymentAddOn` and implement several required methods.

```php
class GF_My_Payment_AddOn extends GFPaymentAddOn {

    // ... instance setup and properties ...

    // Identify features your gateway supports
    protected $_requires_credit_card = true;
    protected $_supports_callbacks = true;

    public function init() {
        parent::init();
    }

    // Process the payment
    public function authorize( $feed, $submission_data, $form, $entry ) {
        // Interact with your payment gateway API to authorize the transaction
        
        // Return authorization data
        return array(
            'is_authorized' => true,
            'error_message' => '',
            'transaction_id' => '123456789',
            'captured_payment' => array(
                'amount' => $submission_data['payment_amount']
            )
        );
    }
}
```

## Best Practices
- Use `$_requires_credit_card = true` if the gateway requires credit card fields on the form. The framework will automatically enforce the presence of a Credit Card field.
- Do not manually update the entry's `payment_status` using `GFAPI`. Return the correct array structure from `authorize()`, and the framework will update the entry and append standard payment notes.
