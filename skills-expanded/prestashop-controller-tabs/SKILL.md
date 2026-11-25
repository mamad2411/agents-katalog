---
name: prestashop-controller-tabs
description: Skill for creating and managing Symfony Controllers and Admin Tabs in PrestaShop 8 and 9.
---

# PrestaShop Controller Tabs Skill

This skill provides patterns and best practices for implementing modern Symfony-based controllers and integrating them into the PrestaShop back-office via the Tab system.

## 1. Technical Guide

### Registry of Tabs in Module Constructor
In PrestaShop 8+, you can declare tabs directly in the `$this->tabs` property of the module's constructor. This is the preferred way as it handles installation and uninstallation automatically.

```php
public function __construct()
{
    $this->name = 'my_module';
    // ...
    $this->tabs = [
        [
            'route_name' => 'admin_my_module_configure',
            'class_name' => 'AdminMyModuleConfigure',
            'visible' => true,
            'name' => [
                'en' => $this->trans('My Module Config', [], 'Modules.Mymodule.Admin'),
                'es' => $this->trans('Configuración Mi Módulo', [], 'Modules.Mymodule.Admin'),
            ],
            'icon' => 'settings',
            'parent_class_name' => 'IMPROVE', // e.g., SELL, IMPROVE, CONFIGURE
        ],
    ];
}
```

### Manual Tab Installation (Fallback/Advanced)
If you need to install a tab manually (e.g., based on conditions), use the `Tab` class:

```php
private function installTab($className, $routeName, $parentClassName = 'IMPROVE')
{
    $tabId = (int) Tab::getIdFromClassName($className);
    if (!$tabId) {
        $tabId = null;
    }

    $tab = new Tab($tabId);
    $tab->active = 1;
    $tab->class_name = $className;
    $tab->route_name = $routeName;
    $tab->module = $this->name;
    $tab->id_parent = (int) Tab::getIdFromClassName($parentClassName);
    
    foreach (Language::getLanguages() as $lang) {
        $tab->name[$lang['id_lang']] = $this->trans('Tab Name', [], 'Modules.Mymodule.Admin', $lang['locale']);
    }

    return $tab->save();
}
```

## 2. Professional Development Guide

### Symfony Controller Structure
Controllers should be located in `src/Controller/Admin/` and follow the Symfony naming convention.

```php
namespace MyModule\Controller\Admin;

use PrestaShopBundle\Controller\Admin\FrameworkBundleAdminController;
use Symfony\Component\HttpFoundation\Response;

class ConfigurationController extends FrameworkBundleAdminController
{
    public const TAB_CLASS_NAME = 'AdminMyModuleConfiguration';

    public function indexAction(): Response
    {
        return $this->render('@Modules/my_module/views/templates/admin/index.html.twig', [
            'layoutTitle' => $this->trans('Configuration', 'Modules.Mymodule.Admin'),
        ]);
    }
}
```

### Routing configuration (`config/routes.yml`)
```yaml
admin_my_module_configure:
    path: /my-module/configure
    methods: [GET]
    defaults:
        _controller: 'MyModule\Controller\Admin\ConfigurationController::indexAction'
        _legacy_classname: AdminMyModuleConfiguration
        _legacy_link: AdminMyModuleConfiguration
```

## 3. User Guide

### How to access the new tabs
1. After installing the module, the new tabs will appear under the specified parent menu (e.g., "Improve").
2. Ensure you have cleared the PrestaShop cache if the tabs do not appear immediately.
3. Permissions can be managed in **Advanced Parameters > Team > Permissions** for the profile associated with the administrator.

## Rules & Best Practices
- **PHP Compatibility**: Use `get_class($controller)` instead of `::class` for objects if supporting PHP 7.4.
- **Translations**: Always use `$this->trans()` with the correct domain.
- **Security**: Include `if (!defined('_PS_VERSION_')) exit;` in all PHP files.
- **Header Licensing**: Always include the Ecom Experts / AFL-3.0 header.
