---
name: gravity-forms-feed-addon-framework
description: "Creating feed-based add-ons extending GFFeedAddOn."
---

# Gravity Forms Feed Add-On Framework

The `GFFeedAddOn` class extends `GFAddOn` and is used specifically for creating add-ons that pass data from Gravity Forms to third-party services (e.g., MailChimp, Zapier, CRMs).

## Reference
[GFFeedAddOn Documentation](https://docs.gravityforms.com/gffeedaddon/)

## Core Concepts

### Feeds
A feed is a configuration that maps Gravity Forms fields to a third-party service's fields. A user can create multiple feeds per form.

### Processing Feeds
The core method you must implement is `process_feed()`. This is automatically called by the framework after a form is successfully submitted, provided the feed's conditional logic is met.

```php
class GF_My_Feed_AddOn extends GFFeedAddOn {

    // ... instance setup and properties (similar to GFAddOn) ...

    public function feed_settings_fields() {
        return array(
            array(
                'title'  => 'Feed Settings',
                'fields' => array(
                    array(
                        'name'    => 'feedName',
                        'label'   => 'Name',
                        'type'    => 'text',
                        'class'   => 'medium',
                        'required'=> true,
                    ),
                    array(
                        'name'      => 'mappedFields',
                        'label'     => 'Map Fields',
                        'type'      => 'field_map',
                        'field_map' => array(
                            array( 'name' => 'firstName', 'label' => 'First Name' ),
                            array( 'name' => 'lastName', 'label' => 'Last Name' ),
                        )
                    ),
                )
            )
        );
    }

    public function process_feed( $feed, $entry, $form ) {
        // Retrieve feed configuration
        $feed_name = $feed['meta']['feedName'];
        
        // Retrieve mapped field values
        $field_map = $this->get_field_map_fields( $feed, 'mappedFields' );
        $first_name_field_id = $field_map['firstName'];
        $first_name = rgar( $entry, $first_name_field_id );

        // Send data to API...
    }
}
```

## Best Practices
- Always use the `field_map` setting type to let users map GF fields to your target API fields. The framework handles the UI for this automatically.
- Support background processing if your API calls take significant time. The framework has built-in support for asynchronous feed processing.
