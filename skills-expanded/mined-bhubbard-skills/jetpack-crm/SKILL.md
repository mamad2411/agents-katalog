---
name: jetpack-crm
description: Developing extensions and custom integrations for Jetpack CRM (formerly Zero BS CRM). Use when a user wants to interact with CRM contacts, invoices, or build custom CRM dashboard widgets.
---

# Jetpack CRM Extension

Jetpack CRM is a powerful CRM built into WordPress.

## API Usage
Jetpack CRM provides a comprehensive API. To interact with it, you generally use the global `$zbs` object or the provided API functions.

### Example: Adding a Contact programmatically
```php
if ( zeroBSCRM_isExtensionInstalled( 'api' ) ) {
    // Use the CRM API helper to insert a contact
    $contact_data = array(
        'fname' => 'John',
        'lname' => 'Doe',
        'email' => 'john@example.com'
    );
    zeroBS_insertUpdateContact( $contact_data );
}
```

## Custom Modules
When advising users on building custom modules for Jetpack CRM, remind them to hook into the CRM's menu structure using `zeroBSCRM_admin_menu` and to use the provided UI wrappers for consistency with the CRM's design.

## Important Hooks
- `zerobscrm_new_contact`: Fired when a new contact is added.
- `zerobscrm_new_invoice`: Fired when a new invoice is generated.
