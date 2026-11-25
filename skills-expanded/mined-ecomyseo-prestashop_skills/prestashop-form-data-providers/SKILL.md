---
name: prestashop-form-data-providers
description: Skill for modifying core PrestaShop form data using modern Data Provider hooks in PS 8/9.
---

# PrestaShop Form Data Providers Skill

This skill explains how to use the `action*FormDataProviderData` and `action*FormDataProviderDefaultData` hooks to modify the data before it is displayed in modern Symfony forms (like the Product V2 form).

## 1. Technical Guide

### Modifying Default Data (New objects)
Use `hookActionProductFormDataProviderDefaultData` to set default values for new products.

```php
public function hookActionProductFormDataProviderDefaultData(array $params): void
{
    // $params['data'] is an array mirroring the form structure
    $params['data']['details']['references']['mpn'] = 'DEFAULT_MPN_123';
}
```

### Modifying Existing Data
Use `hookActionProductFormDataProviderData` to modify data being loaded for an existing object.

```php
public function hookActionProductFormDataProviderData(array $params): void
{
    $productId = (int) $params['id'];
    $currentMpn = $params['data']['details']['references']['mpn'];

    if ($this->shouldPrefixMpn()) {
        $params['data']['details']['references']['mpn'] = 'PREFIX_' . $currentMpn;
    }
}
```

### Supported Entities
These hooks are generally available for any modern form using a `FormDataProvider`. Most commonly:
- `Product` (V2)
- `Combination`
- `Category` (in newer versions)

## 2. Professional Development Guide

### Advantages over Overrides
- **Non-destructive**: You are only modifying the array of data used by the form, not the database structure or core classes.
- **Composable**: Multiple modules can hook into the same data and add their own modifications without conflicts.

### Best Practices
- **Path Awareness**: You must know the exact array path of the field you want to modify. Refer to the form type definitions or dump the `$params['data']` during development.
- **Conditional Logic**: Always check if the store context or object ID is correct for your modification.

## 3. User Guide

### Debugging
If values are not appearing as expected:
1. Ensure the module is hooked to the correct event.
2. Check the PrestaShop version (hook availability depends on the Symfony migration state of that specific page).
3. Clear Symfony cache (`var/cache/`).

## Rules & Best Practices
- **Performance**: Avoid heavy database queries inside these hooks as they are called during every form load.
- **Safety**: Check for the existence of array keys before accessing/modifying them to avoid "Undefined Index" errors.
