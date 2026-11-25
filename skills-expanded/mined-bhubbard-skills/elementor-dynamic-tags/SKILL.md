---
name: elementor-dynamic-tags
description: Developer guide for creating and utilizing custom Dynamic Tags in Elementor.
---

# Elementor Custom Dynamic Tags Guide

## Overview
This skill focuses on the advanced developer capabilities surrounding Elementor's Dynamic Tags. While Elementor Pro provides numerous built-in tags (for post titles, meta data, ACF fields, etc.), developers often need to create custom dynamic tags to pull data from external APIs, complex database queries, or specific business logic.

## What is a Dynamic Tag?
Dynamic Tags allow users to populate widget fields (text, URLs, images) with dynamic data retrieved from the database or other sources, rather than static input.

## Creating a Custom Dynamic Tag

To create a custom dynamic tag, you must extend the appropriate base class provided by Elementor and register the tag via the `elementor/dynamic_tags/register` action.

### 1. Extending the Base Class
Depending on the type of data your tag returns, extend one of these classes:
*   `\Elementor\Core\DynamicTags\Tag`: Base class for most tags (returns strings).
*   `\Elementor\Core\DynamicTags\Data_Tag`: For tags returning arrays (e.g., gallery images).

### 2. Required Methods
Your custom tag class must implement the following methods:
*   `get_name()`: Returns a unique string identifier.
*   `get_title()`: Returns the translatable label seen in the UI.
*   `get_group()`: Defines which category the tag belongs to (e.g., `site`, `post`, `archive`).
*   `get_categories()`: Defines where the tag can be used (e.g., `[ \Elementor\Modules\DynamicTags\Module::TEXT_CATEGORY ]`, `URL_CATEGORY`, `IMAGE_CATEGORY`).
*   `render()`: Outputs the dynamic value.

### Example: A Simple Custom Tag (Current Year)

```php
// Ensure Elementor is loaded
if ( ! defined( 'ABSPATH' ) ) {
	exit; // Exit if accessed directly.
}

class My_Custom_Dynamic_Tag extends \Elementor\Core\DynamicTags\Tag {

	public function get_name() {
		return 'my-current-year';
	}

	public function get_title() {
		return esc_html__( 'Current Year', 'my-plugin' );
	}

	public function get_group() {
		return 'site';
	}

	public function get_categories() {
		return [ \Elementor\Modules\DynamicTags\Module::TEXT_CATEGORY ];
	}

	public function render() {
		echo date( 'Y' );
	}
}
```

### 3. Registering the Tag

Hook into Elementor to register your new class.

```php
add_action( 'elementor/dynamic_tags/register', function( $dynamic_tags_manager ) {
	require_once( __DIR__ . '/path/to/My_Custom_Dynamic_Tag.php' );
	$dynamic_tags_manager->register( new \My_Custom_Dynamic_Tag() );
} );
```

## Adding Controls to Dynamic Tags
You can add controls to your tag (like the "Before", "After", and "Fallback" settings found on default tags) by implementing the `_register_controls()` method in your class.

```php
	protected function register_controls() {
		$this->add_control(
			'my_prefix',
			[
				'label' => esc_html__( 'Prefix', 'my-plugin' ),
				'type' => \Elementor\Controls_Manager::TEXT,
			]
		);
	}
```
You can then access this setting in the `render()` method using `$this->get_settings('my_prefix')`.

## Best Practices
*   **Caching:** If your `render()` method involves expensive queries or API calls, implement WordPress transients or object caching to avoid performance bottlenecks.
*   **Security:** Always sanitize and escape the output in the `render()` method before echoing it, especially if the data comes from user input or external sources.
