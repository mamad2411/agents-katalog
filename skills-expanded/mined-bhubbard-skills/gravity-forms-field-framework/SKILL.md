---
name: gravity-forms-field-framework
description: "Creating custom field types extending GF_Field."
---

# Gravity Forms Field Framework

The Field Framework provides a streamlined way to create new, custom field types for Gravity Forms by extending the base `GF_Field` class.

## Reference
[Field Framework Documentation](https://docs.gravityforms.com/category/developers/php-api/field-framework/)

## The GF_Field Class
Every field in Gravity Forms is an instance of `GF_Field`. By creating a child class, you can define how the field looks in the form editor, what settings it has, how it validates data, and how it renders on the front end.

### Basic Implementation

```php
if ( class_exists( 'GF_Field' ) ) {
    class GF_My_Custom_Field extends GF_Field {

        // Define the field type string
        public $type = 'my_custom_field';

        // Set the field title in the editor
        public function get_form_editor_field_title() {
            return esc_attr__( 'My Custom Field', 'my-text-domain' );
        }

        // Define which settings appear in the editor
        function get_form_editor_field_settings() {
            return array(
                'label_setting',
                'description_setting',
                'rules_setting',
                'css_class_setting',
            );
        }

        // Output the HTML for the front end
        public function get_field_input( $form, $value = '', $entry = null ) {
            $id = (int) $this->id;
            $input_name = "input_{$id}";
            $value = esc_attr( $value );
            $class = esc_attr( $this->size );
            
            return "<div class='ginput_container ginput_container_my_custom_field'>
                        <input type='text' name='{$input_name}' id='{$input_name}' value='{$value}' class='{$class}' />
                    </div>";
        }
    }
    
    // Register the field type with Gravity Forms
    GF_Fields::register( new GF_My_Custom_Field() );
}
```

## Best Practices
- Always register the field using `GF_Fields::register()` after defining the class.
- Return the proper HTML structure in `get_field_input()` so it aligns with Gravity Forms' built-in validation and styling features. Wrap inputs in `ginput_container`.
