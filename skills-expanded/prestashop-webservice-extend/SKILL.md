---
name: prestashop-webservice-extend
description: Skill for adding new resources to the legacy XML WebService in PrestaShop.
---

# PrestaShop WebService Extend Skill

This skill explains how to expose module entities through the legacy PrestaShop WebService API.

## 1. Technical Guide

### Registering the Hook
The module must register the `addWebserviceResources` hook.

```php
public function install()
{
    return parent::install() && $this->registerHook('addWebserviceResources');
}
```

### Exposing the Resource
Return an array where the key is the alias of the resource and the value contains the class name and description.

```php
public function hookAddWebserviceResources($params)
{
    return [
        'my_module_articles' => [
            'description' => 'Access to module articles',
            'class' => 'MyArticle', // Must extend ObjectModel
            'forbidden_method' => [] // Optional: ['DELETE', 'PUT']
        ]
    ];
}
```

## 2. Professional Development Guide

### ObjectModel Requirement
The class specified in the WS resource **MUST** be an `ObjectModel` and must be correctly loaded or autoloaded.

```php
class MyArticle extends ObjectModel
{
    public $title;
    public static $definition = [
        'table' => 'my_article',
        'primary' => 'id_my_article',
        'fields' => [
            'title' => ['type' => self::TYPE_STRING, 'validate' => 'isString', 'webservice' => true],
        ],
    ];
}
```

### Security
Ensure that all fields you want to expose have `'webservice' => true` in their definition. Fields without this property or set to `false` will be hidden in the API.

## 3. User Guide

### How to use
1. Go to **Advanced Parameters > Web Service**.
2. Create or edit an API Key.
3. You will see `my_module_articles` in the list of permissions. Grant GET, POST, etc. as needed.

## Rules & Best Practices
- **Aliases**: Use a prefix with your module name to avoid resource name collisions.
- **Performance**: For large datasets, the XML WebService can be slow. Consider using the new REST API for PrestaShop 9.
- **Licensing**: Always include the Ecom Experts / AFL-3.0 header.
