---
name: prestashop-module-routes
description: Skill for defining custom front-office routes and Pretty URLs in PrestaShop modules.
---

# PrestaShop Module Routes Skill

This skill explains how to use the `moduleRoutes` hook to create user-friendly (Pretty) URLs for your module's front controllers.

## 1. Technical Guide

### Registering the Hook
The module must be registered to the `moduleRoutes` hook.

```php
public function install()
{
    return parent::install() && $this->registerHook('moduleRoutes');
}
```

### Implementing `hookModuleRoutes`
This hook must return an array of route definitions.

```php
public function hookModuleRoutes()
{
    return [
        'module-mymodule-list' => [
            'rule' => 'custom-path/list',
            'keywords' => [],
            'controller' => 'list', // references controllers/front/list.php
            'params' => [
                'fc' => 'module',
                'module' => $this->name
            ]
        ],
        'module-mymodule-view' => [
            'rule' => 'custom-path/view/{id}-{slug}',
            'keywords' => [
                'id' => ['regexp' => '[0-9]+', 'param' => 'id'],
                'slug' => ['regexp' => '[_a-zA-Z0-9\-\.]+', 'param' => 'slug'],
            ],
            'controller' => 'view',
            'params' => [
                'fc' => 'module',
                'module' => $this->name
            ]
        ]
    ];
}
```

### Generating URLs with Pretty Routes
```php
$link = $this->context->link->getModuleLink('mymodule', 'view', ['id' => 10, 'slug' => 'my-product']);
// Output: https://store.com/custom-path/view/10-my-product
```

## 2. Professional Development Guide

### Friendly URLs Requirement
- These routes only work if **Traffic & SEO > Set up URLs > Friendly URL** is enabled in the Back Office.
- If Friendly URLs are disabled, PrestaShop fallbacks to the standard `?fc=module&module=...` query parameters.

### Regex Best Practices
- Always use specific regex for parameters like `id` (`[0-9]+`) to avoid route collisions.
- The `rule` should be unique enough to not clash with CMS pages or Category pages.

## 3. User Guide

### How to use
1. Install the module.
2. Go to **Traffic & SEO** and save URLs to regenerate `.htaccess` if needed (usually automatic).
3. Access your module via the custom rules defined.

## Rules & Best Practices
- **Uniqueness**: Route names (keys in the array) must be unique.
- **Compatibility**: This method works across PrestaShop 1.7, 8, and 9 for legacy Front Controllers.
- **SEO**: Use keywords in URLs to improve SEO ranking for module-generated pages.
