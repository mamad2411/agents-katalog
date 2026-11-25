---
name: gravity-forms-php-api
description: "Provides best practices and references for using the Gravity Forms PHP API to interact with forms on the same server."
---

# Gravity Forms PHP API

## Introduction

The PHP API provides tools for developers to access Gravity Forms when developing in the same server/site as Gravity Forms. It allows you to manipulate data, create add-ons, and build custom fields.

## Core Components

### 1. API Functions (GFAPI)
The `GFAPI` class provides methods to perform CRUD operations on Forms and Entries. It is the recommended way to interact with Gravity Forms data programmatically, rather than querying the database directly.
- **Reference**: [API Functions Documentation](https://docs.gravityforms.com/category/developers/php-api/api-functions/)
- **Common Methods**:
  - `GFAPI::get_entry( $entry_id )`
  - `GFAPI::update_entry( $entry )`
  - `GFAPI::get_form( $form_id )`
  - `GFAPI::add_entry( $entry )`

### 2. Add-On Framework
The Add-On Framework provides a set of base classes to facilitate the creation of custom Add-Ons. It handles initialization, settings pages, permissions, and script enqueuing.
- **Reference**: [Add-On Framework Documentation](https://docs.gravityforms.com/category/developers/php-api/add-on-framework/)
- **Common Classes**:
  - `GFAddOn`: Base class for simple add-ons.
  - `GFFeedAddOn`: Base class for add-ons that process form submissions and send data to third-party services.
  - `GFPaymentAddOn`: Base class for payment gateways.

### 3. Field Framework
The Field Framework provides classes and methods that can be used to create custom Gravity Forms field types.
- **Reference**: [Field Framework Documentation](https://docs.gravityforms.com/category/developers/php-api/field-framework/)
- **Base Class**: Extend `GF_Field` to define a new field type, its settings, and its rendering logic.

### 4. Constants
Gravity Forms supports several constants that can be defined in `wp-config.php` to customize behavior, such as disabling automatic updates or changing logging settings.
- **Reference**: [Constants Documentation](https://docs.gravityforms.com/category/developers/php-api/constants/)

## Best Practices
- Always use `GFAPI` instead of direct SQL queries when reading or writing forms and entries to ensure hooks are fired and data is formatted correctly.
- When creating a new Add-On, always start by extending the appropriate class in the Add-On Framework to save time and ensure standard UI/UX.
