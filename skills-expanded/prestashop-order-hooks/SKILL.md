---
name: prestashop-order-hooks
description: Skill for extending the Admin Order View page (V2) in PrestaShop 8 and 9 using modern hooks.
---

# PrestaShop Order Hooks Skill

This skill explains how to modify and extend the Order View page in the PrestaShop Back Office (modern Symfony implementation).

## 1. Technical Guide

### Adding Buttons to the Toolbar
Use `hookActionGetAdminOrderButtons`.

```php
public function hookActionGetAdminOrderButtons(array $params)
{
    /** @var \PrestaShop\PrestaShop\Core\Action\ActionsBarButtonsCollection $bar */
    $bar = $params['actions_bar_buttons_collection'];

    $bar->add(
        new \PrestaShop\PrestaShop\Core\Action\ActionsBarButton(
            'btn-secondary', 
            ['href' => 'https://example.com'], 
            $this->trans('Custom Action', [], 'Modules.Mymodule.Admin')
        )
    );
}
```

### Displaying Content in Different Sections
- `displayAdminOrderMain`: Large central column.
- `displayAdminOrderSide`: Right sidebar top.
- `displayAdminOrderSideBottom`: Right sidebar bottom.
- `displayAdminOrderTop`: Top of the page (below toolbar).

### Adding New Tabs to the Order Page
- `displayAdminOrderTabLink`: The tab title/link.
- `displayAdminOrderTabContent`: The actual content of the tab.

```php
public function hookDisplayAdminOrderTabLink(array $params)
{
    return $this->context->smarty->fetch($this->local_path.'views/templates/admin/tab_link.tpl');
}

public function hookDisplayAdminOrderTabContent(array $params)
{
    $orderId = (int)$params['id_order'];
    // ... logic
    return $this->fetch('module:mymodule/views/templates/admin/tab_content.tpl');
}
```

## 2. Professional Development Guide

### Using Twig in Hooks
PrestaShop 8/9 prefers Twig for back-office rendering. Access the `twig` service:

```php
public function hookDisplayAdminOrderMain(array $params)
{
    $twig = $this->get('twig');
    return $twig->render('@Modules/mymodule/views/templates/admin/main.html.twig', [
        'orderId' => $params['id_order'],
    ]);
}
```

### Architecture
- **Presenters**: Use dedicated classes to prepare data for the view to keep the module class clean.
- **Repositories**: Use the `doctrine.orm.entity_manager` or a custom repository service to fetch order-related data.

## 3. User Guide

### How to use
The content added via these hooks will automatically integrate with the modern PrestaShop Order interface. Support for dark mode and responsive layouts is handled by the core UI kit.

## Rules & Best Practices
- **Security**: Always cast `id_order` to `(int)`.
- **Namespace**: Use proper namespaces for Presenters and Repositories in `src/`.
- **Translations**: Use the `Modules.[ModuleName].Admin` domain for all back-office translations.
