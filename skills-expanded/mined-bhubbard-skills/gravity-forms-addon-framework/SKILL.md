---
name: gravity-forms-addon-framework
description: "Creating custom add-ons extending GFAddOn."
---

# Gravity Forms Add-On Framework

The Add-On Framework provides base classes to facilitate the creation of custom Add-Ons for Gravity Forms.

## Reference
[Add-On Framework Documentation](https://docs.gravityforms.com/category/developers/php-api/add-on-framework/)

## The GFAddOn Class
`GFAddOn` is the base class for simple add-ons that require plugin settings, form settings, and specific script/stylesheet enqueuing.

### Basic Implementation
To create an add-on, extend the `GFAddOn` class and override its methods.

```php
GFForms::include_addon_framework();

class GF_Simple_AddOn extends GFAddOn {

    protected $_version = '1.0';
    protected $_min_gravityforms_version = '2.5';
    protected $_slug = 'simpleaddon';
    protected $_path = 'simpleaddon/simpleaddon.php';
    protected $_full_path = __FILE__;
    protected $_title = 'Gravity Forms Simple Add-On';
    protected $_short_title = 'Simple Add-On';

    private static $_instance = null;

    public static function get_instance() {
        if ( self::$_instance == null ) {
            self::$_instance = new GF_Simple_AddOn();
        }
        return self::$_instance;
    }

    public function init() {
        parent::init();
        // Add custom hooks here
    }

    public function plugin_settings_fields() {
        return array(
            array(
                'title'  => 'Simple Add-On Settings',
                'fields' => array(
                    array(
                        'name'    => 'my_custom_setting',
                        'label'   => 'Custom Setting',
                        'type'    => 'text',
                        'class'   => 'medium',
                    )
                )
            )
        );
    }
}
```

## Best Practices
- Define your plugin settings and form settings by overriding `plugin_settings_fields()` and `form_settings_fields()`. The framework will automatically render the UI and save the data.
- Enqueue scripts using the `scripts()` and `styles()` methods provided by the framework to ensure they are only loaded when necessary (e.g., only on pages with forms).
