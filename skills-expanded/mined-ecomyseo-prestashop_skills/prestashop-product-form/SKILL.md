---
name: prestashop-product-form
description: Skill for modifying the PrestaShop Product and Combination forms (V2) using Symfony Form Modifiers. Compatible PS 8.1+ and PS 9.
---

# PrestaShop Product Form Skill (V2)

This skill covers the modern way (PrestaShop 8.1+/9) to hook into and modify the product and combination forms in the back-office using the `FormBuilderModifier`.

> **IMPORTANT**: Product V2 fue introducido en PS 8.1. En PS 8.0 estos hooks NO existen. En PS 9 es el unico sistema.

## 1. Technical Guide

### Hooking into the Product Form
Use the `hookActionProductFormBuilderModifier` hook to access the form builder.

```php
declare(strict_types=1);

public function hookActionProductFormBuilderModifier(array $params): void
{
    // PS 8: se puede usar service locator
    // PS 9 (Symfony 6.4): usar constructor injection (ver seccion servicios)
    /** @var \PrestaShopBundle\Form\FormBuilderModifier $formBuilderModifier */
    $formBuilderModifier = $this->get('prestashop.bundle.form.form_builder_modifier');

    $formBuilder = $params['form_builder'];
    $productId = isset($params['id']) ? (int) $params['id'] : null;

    // Example: Adding a field to the description tab
    $descriptionTab = $formBuilder->get('description');
    $formBuilderModifier->addAfter(
        $descriptionTab,
        'description', // field to add after
        'my_custom_field',
        \Symfony\Component\Form\Extension\Core\Type\TextType::class,
        [
            'label' => $this->trans('My Custom Field', [], 'Modules.Mymodule.Admin'),
            'data' => 'current value', // fetch from DB in real usage
        ]
    );
}
```

### Hooking into the Combination Form
Use the `hookActionCombinationFormFormBuilderModifier` hook.

```php
public function hookActionCombinationFormFormBuilderModifier(array $params): void
{
    $formBuilder = $params['form_builder'];
    // Similar usage to product form
}
```

### Saving Custom Data
Use `hookActionAfterUpdateProductFormHandler` and `hookActionAfterCreateProductFormHandler`.

```php
public function hookActionAfterUpdateProductFormHandler(array $params): void
{
    $productId = (int) $params['id'];
    $formData = $params['form_data'];
    $customValue = $formData['my_custom_field'] ?? '';

    // Logic to save $customValue for $productId
}

// Tambien para productos NUEVOS
public function hookActionAfterCreateProductFormHandler(array $params): void
{
    $productId = (int) $params['id'];
    $formData = $params['form_data'];
    $customValue = $formData['my_custom_field'] ?? '';

    // Logic to save $customValue for $productId
}
```

### Hook Registration (install)
```php
public function install()
{
    return parent::install()
        && $this->registerHook('actionProductFormBuilderModifier')
        && $this->registerHook('actionAfterUpdateProductFormHandler')
        && $this->registerHook('actionAfterCreateProductFormHandler')
        && $this->registerHook('actionCombinationFormFormBuilderModifier');
}
```

## 2. Professional Development Guide

### Architecture Checklist
- **Modifiers**: Create a dedicated service class (e.g., `ProductFormModifier`) to handle the logic instead of putting it all in the main module file.
- **Form Types**: For complex modifications or new tabs, create custom `AbstractType` classes.
- **Dependency Injection**: Use `services.yml` to register your modifiers. En PS 9 (Symfony 6.4), `$this->get()` esta deprecated. Usar constructor injection.

### Service Registration (PS 9 compatible)
```yaml
services:
    MyModule\Form\ProductFormModifier:
        arguments:
            - '@prestashop.bundle.form.form_builder_modifier'
            - '@translator'
        public: true
```

### Custom Tabs
To add a new tab, you usually add a "Tab" (the header) and a "TabContent" (the vertical section). PrestaShop 8.1+ uses specific form types for this in the product V2 page.

### Compatibilidad PS 8.0 vs 8.1+
Si el modulo debe funcionar en PS 8.0 (Product V1), detectar la version:
```php
if (version_compare(_PS_VERSION_, '8.1.0', '>=')) {
    // Product V2 hooks disponibles
} else {
    // Usar displayAdminProductsExtra (legacy)
}
```

## 3. User Guide

### Requirements
- Product V2 hooks: PrestaShop 8.1+ y PrestaShop 9.
- En PS 8.0, usar `displayAdminProductsExtra` como alternativa.

## Rules & Best Practices
- **Strict Typing**: Always use `declare(strict_types=1);` in your modifier classes.
- **Namespace**: Classes inside `src/` must be properly namespaced.
- **Safety**: Verify if the field exists before using `addAfter` or `get`.
- **`ClassName::class`**: Usar libremente (valido desde PHP 5.5). Solo evitar `$obj::class` si se necesita compatibilidad con PHP < 8.0 (PS 8.0).
