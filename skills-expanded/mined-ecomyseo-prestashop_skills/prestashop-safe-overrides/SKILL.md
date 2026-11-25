---
name: prestashop-safe-overrides
description: Skill for implementing safe, manually copied overrides in PrestaShop 8/9 to avoid native installer conflicts.
---

# PrestaShop Safe Overrides Skill (V8 Mode)

This skill describes the "Blindados" override method, which avoids using the native `installOverrides()` system of PrestaShop to prevent "Conflict" errors and store blocks.

## 1. Technical Guide

### The Manual Copy Strategy
Instead of putting files in the module's `override/` directory and letting PS auto-install them, we place them in a custom directory (e.g., `override_v8/`) and copy them manually during the install process if they don't already exist.

### Implementation in Module Class
```php
/**
 * Safe Installation of Overrides
 */
public function installSafeOverrides()
{
    $overrides = [
        'classes/Product.php',
        'classes/Category.php'
    ];

    foreach ($overrides as $path) {
        $source = _PS_MODULE_DIR_ . $this->name . '/override_v8/' . $path;
        $destination = _PS_ROOT_DIR_ . '/override/' . $path;

        if (!file_exists($destination)) {
            $dir = dirname($destination);
            if (!is_dir($dir)) {
                mkdir($dir, 0755, true);
            }
            copy($source, $destination);
        }
    }
    
    // Clear class index to recognize new overrides
    if (file_exists(_PS_ROOT_DIR_ . '/var/cache/pro_/class_index.php')) {
        @unlink(_PS_ROOT_DIR_ . '/var/cache/pro_/class_index.php');
    }
    if (file_exists(_PS_ROOT_DIR_ . '/var/cache/dev/class_index.php')) {
        @unlink(_PS_ROOT_DIR_ . '/var/cache/dev/class_index.php');
    }

    return true;
}
```

## 2. Professional Development Guide

### ObjectModel Extension
When overriding an `ObjectModel`, ensure you update the static `$definition` if you are adding fields.

```php
class Product extends ProductCore
{
    public $my_custom_field;

    public function __construct($id = null, $id_lang = null, $id_shop = null)
    {
        self::$definition['fields']['my_custom_field'] = [
            'type' => self::TYPE_STRING, 
            'validate' => 'isCleanHtml', 
            'size' => 255
        ];
        parent::__construct($id, $id_lang, $id_shop);
    }
}
```

### Why avoid `installOverrides()`?
- **Conflict detection**: PrestaShop blocks installation if another module overrides the same file/method.
- **Stability**: Failures in native override installation can lead to blank screens if the class index gets corrupted.

## 3. User Guide

### Maintenance
- If the module is uninstalled, overrides should be removed manually if they were not modified by other processes, or left if they contain essential data structures.
- Always clear the PrestaShop cache after manual override changes.

## Rules & Best Practices
- **Never use `::class`**: Use `get_class()` for PHP 7.4 compatibility.
- **Namespace**: Never use namespaces in override files.
- **Integrity**: Always check for the existence of the core class before attempting to override it.
